# Assignment 01 — SQLite Behind an API: Where It Shines and Where It Breaks

**Weight:** _TBD_ · **Assigned:** _TBD_ · **Due:** _TBD_

## Goal

Wrap the normalized database from [Lecture 02 — SQLite](../../Lectures/02_sqlite/)
in a **FastAPI** service, scale the data up, add progressively nastier
endpoints, and write a memo on **when SQLite is the right backend and when it is
not**.

This is **not a benchmarking exercise.** Your evidence is `EXPLAIN QUERY PLAN`
output, whether a query holds a lock, whether the response time became
*user-visible*, and whether writes started failing — not p99 latency charts.

Every database topic in this course attaches to a usable API. The auth stub here
is deliberately thin; the token-based auth lecture will build on it.

## Prerequisites

- The [02_sqlite](../../Lectures/02_sqlite/) schema and walkthrough
- Python 3.11+
- `EXPLAIN QUERY PLAN` (covered in [sqlite_walkthrough.md §4](../../Lectures/02_sqlite/sqlite_walkthrough.md))
- FTS5 available in your SQLite build (check `pragma_compile_options`; see
  [requirements.md](../../Lectures/02_sqlite/requirements.md))

## Stack (required)

| Piece | Choice |
| :--- | :--- |
| Web framework | **FastAPI** + **uvicorn** (not Flask) |
| DB driver | `sqlite3` (stdlib, threadpool) **or** `aiosqlite` (async) — pick one, justify it in the memo |
| Serialization | Pydantic v2 response models |
| Tests | `pytest` + `httpx` (FastAPI `TestClient`) |
| Load / contention | a plain `asyncio.gather` script, or `oha` / `hey` — to *trigger* contention, not measure it |
| ORM | none required; raw SQL is the point (SQLAlchemy Core optional, for contrast) |

A starter scaffold is in [starter/](starter/): FastAPI app skeleton, a
connection helper with the right pragmas, an `X-API-Key` dependency, a data
generator, and smoke tests. Phase 1 endpoints are implemented as worked
examples; Phases 2–4 are `501 Not Implemented` stubs for you to fill in.

---

## The schema (recap)

From `Lectures/02_sqlite/sql/01_schema.sql` — eight tables:

```
states ─< zipcodes ─< customers ─< cards ─< purchases >─ products
                                    │                 │
                          card_types┘       departments┘
```

`purchases` is the fact table: `purchase_id`, FKs to `customer_id` / `card_id` /
`product_id` / `department`, plus `amount` (point-in-time price) and
`purchase_date` (ISO `TEXT`).

---

## Phase 0 — Setup & data scaling

1. Build the baseline DB from the lecture: `sqlite3 store.db ".read
   ../../Lectures/02_sqlite/rebuild.sql"` (from `starter/`), **or** use
   `scale_data.py`.
2. Connection pragmas (already in `starter/app/db.py`): `journal_mode=WAL`,
   `foreign_keys=ON`, `busy_timeout=5000`.
3. Scale the data with `starter/scale_data.py`:
   ```bash
   python scale_data.py --db store.db --customers 50000 --products 5000 --purchases 1000000 --skew
   ```
   - Grows `customers`, `cards`, and `products` too, so joins actually widen.
   - `--skew` gives a few customers thousands of purchases and leaves some
     products with zero sales — so aggregates and pagination have something to
     choke on.
4. Run at four sizes and keep the numbers: **1k** (lecture baseline), **100k**,
   **1M**, **5M** purchases.
5. Record the index inventory. Some foreign keys are intentionally left
   unindexed — find them.

**Deliverable:** a table of `(data size) × (endpoint) → (query plan, wall time)`
that you extend through every phase.

---

## Phase 1 — Simple reads (baseline: SQLite looks perfect)

Implemented in the starter as examples. Confirm the plans and timings.

| Method | Route | Notes |
| :--- | :--- | :--- |
| GET | `/customers/{id}` | primary-key lookup |
| GET | `/products?limit=&offset=` | small offsets only |
| GET | `/purchases?start=&end=` | date-range scan on `idx_purchases_date` |
| GET | `/departments` | whole small table |

**Expect:** flat response times across all four data sizes.

---

## Phase 2 — Joins & aggregates (fine — *if* the index exists)

Implement these:

| Method | Route | Query shape |
| :--- | :--- | :--- |
| GET | `/customers/{id}/purchases` | 3-table join, include product name + department |
| GET | `/stats/revenue-by-state` | join + `GROUP BY` |
| GET | `/stats/revenue-by-month` | `strftime('%Y-%m', …)` grouping |
| GET | `/products/top?by=revenue&limit=` | join + `GROUP BY` + `ORDER BY` + `LIMIT` |

**Exercise:** drop `idx_purchases_customer`, capture `EXPLAIN QUERY PLAN` for
`/customers/{id}/purchases` before and after, at 1M rows. Then add a *covering*
index and capture it a third time. Explain each plan.

---

## Phase 3 — Gnarly queries (now it gets user-visible)

Each route exposes one failure mode. Implement all eight, then **add two of your
own** and document what they demonstrate.

| Route | The nasty part | What it teaches |
| :--- | :--- | :--- |
| `GET /purchases?offset=900000` | deep `OFFSET` pagination | `OFFSET` re-scans every skipped row → fix with **keyset / seek** pagination (`WHERE purchase_id > :cursor`) and compare |
| `GET /products/search?q=` | `WHERE product_name LIKE '%'||:q||'%'` | leading wildcard can't use an index → full scan → add an **FTS5** table, compare plan + timing |
| `GET /purchases?…&total=true` | `COUNT(*)` of the filtered set for a page total | full scan on every request → discuss cached / approximate counts |
| `GET /customers/leaderboard` | window function ranking by 90-day trailing spend | large sort + scan; no index helps much |
| `GET /customers/{id}/streaks` | gaps-and-islands: consecutive purchase-day runs | self-join / window pattern that scales badly |
| `GET /reports/cube` | multi-CTE: revenue by `(state, department, month)` + `HAVING` | several full aggregations in one request |
| `GET /purchases/sample` | `ORDER BY random() LIMIT 10` | naive random sampling = full scan + sort every call |
| `GET /products/dead?state=` | anti-join: products never purchased in a given state (`NOT EXISTS`) | correlated scan over the large child table |

For each: `EXPLAIN QUERY PLAN`, wall time at 100k / 1M / 5M, and a one-paragraph
diagnosis. For the two with a fix (offset, search), show the before/after.

---

## Phase 4 — Write concurrency (the "when NOT to" evidence)

1. Implement `POST /purchases` — a real insert inside a transaction, returning
   the new row (`201`).
2. Fire 50, then 200 concurrent `POST`s (starter has an `asyncio.gather`
   script). Record what happens: `sqlite3.OperationalError: database is locked`
   / `SQLITE_BUSY`.
3. Apply mitigations **in order** and note where each one stops helping:
   `busy_timeout` → WAL → batching many inserts per transaction → a single
   serialized writer task (queue).
4. Add a **background writer** (e.g. an audit-log task on every request) that
   competes with the request-path writes. Observe.
5. Run **two `uvicorn` processes** against the same `store.db`. Then describe
   what breaks if that file were on a network share (NFS/SMB) instead of local
   disk.

**Answer with data:** at what write concurrency / rate does SQLite stop being
appropriate *for this workload*?

---

## Phase 5 — Decision memo (the deliverable that matters)

2–3 pages. For each scenario below, recommend **SQLite or not**, and cite
specific observations from your own endpoints and Phase 0–4 measurements.

1. Internal **read-only analytics dashboard**, ~10 analysts
2. A **mobile app's offline-first** local store
3. **High-write event ingestion** — thousands of writes/second
4. **Multi-region SaaS** with three application servers
5. **CI test fixture** — a fresh throwaway DB per test

Then: give two rules of thumb you would actually apply on the job, and name the
single measurement that would most change your recommendation.

The rubric weights **reasoning and evidence**, not raw numbers.

---

## Auth (thin now; the token lecture builds on it)

- Every route except `/health` depends on `require_api_key` (`X-API-Key`
  header). The starter checks the header against an `API_KEYS` env var.
- **Your task:** move keys into an `api_keys` table storing **hashed** keys
  (SHA-256 or Argon2 — see
  [encryption_and_passwords.md](../../Lectures/02_sqlite/encryption_and_passwords.md)),
  with `label` and `created_at`. `starter/sql/auth.sql` has a schema to start
  from. Verify with `hmac.compare_digest`.
- In the memo, state plainly: SQLite has **no** built-in users, roles, or
  row-level security — every bit of authz lives in the API layer.
- Structure the dependency so swapping `X-API-Key` for a JWT bearer token later
  touches only `app/auth.py`.

---

## Deliverables

| # | Item |
| :- | :--- |
| 1 | Repo: FastAPI app, `scale_data.py`, `pyproject.toml` / `requirements.txt`, tests that pass |
| 2 | All Phase 1–4 endpoints working; two original Phase 3 endpoints |
| 3 | [FINDINGS.md](FINDINGS_TEMPLATE.md) — query plans, before/after index, before/after FTS5, offset-vs-keyset, concurrency observations (paste the real error text) |
| 4 | The Phase 5 decision memo (`MEMO.md` or PDF) |
| 5 | A `curl` / HTTPie transcript **or** a 3–5 min screencast showing the failure modes live |

## Grading (100 pts)

| Area | Pts |
| :--- | :-- |
| Endpoints correct & properly typed (Pydantic, status codes, 404/401) | 20 |
| Data generator: scales, skews, reproducible | 10 |
| Phase 2 index exercise: three plans, correct explanation | 10 |
| Phase 3: eight endpoints + two original, each with plan + diagnosis | 20 |
| Phase 4: concurrency failures reproduced, mitigations tested honestly | 15 |
| Auth moved to hashed `api_keys` table | 5 |
| FINDINGS.md quality (evidence, not vibes) | 10 |
| Decision memo: scenario reasoning tied to observations | 10 |

## Stretch (bonus, max +10)

- Re-point one endpoint at **PostgreSQL in Docker**; contrast the *concurrency
  behavior*, not the speed.
- `ANALYZE` + `PRAGMA optimize`; build a covering index for `/reports/cube`.
- `PRAGMA query_only` read-only connections; a read/write connection split.
- Observe WAL checkpoint behavior and `-wal` file growth under sustained writes.

## Academic integrity

Generative tools may help you write boilerplate and explain query plans. The
diagnoses, the concurrency analysis, and the decision memo must be your own
reasoning about *your* measurements. Cite any external source you lean on.
