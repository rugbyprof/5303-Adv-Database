<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: true
id: A01-01_sqlite_api
name: A01-01_sqlite_api
title: Sqlite api project
description: Fast api + Sqlite projects
category: Assignments
date_due:
  month: '09'
  day: '30'
  year: 2026
  hour: 13
```



# Assignment 01 — SQLite Behind an API: Where It Shines and Where It Breaks

**Weight:** _TBD_ · **Assigned:** _TBD_ · **Due:** _TBD_

## The short version

You get a working FastAPI app, a script that builds the databases, the SQL for every query, and a driver that runs the experiment. Your job:

1. **Build** six SQLite databases: three sizes, each **with** and **without** indexes.
2. **Implement** one API route per query by copying the SQL from [QUERIES.md](QUERIES.md).
3. **Run** `driver.py`. It calls every route against every database and writes a results table.
4. **Explain** what the numbers show, in [FINDINGS.md](FINDINGS_TEMPLATE.md).

You are **not** writing SQL, designing indexes, or building a benchmark harness; that part is done for you. The skill this assignment grades is **reading a query plan and explaining why a query is fast or slow**.

## What you'll learn

- Why the same query can take 0.1 ms on one database and 40 ms on another with identical data.
- How to read `EXPLAIN QUERY PLAN`: `SCAN` vs. `SEARCH`, and what "covering index" means.
- That indexes fix *most* slow queries, but some only get fixed by **rewriting** the query. Occasionally an index makes a query **slower**.
- Where SQLite stops being the right choice, which is concurrent **writes**.

## What's given vs. what you do

| Given to you | You do |
| :--- | :--- |
| `scale_data.py`: generates realistic data with **skew** (a few customers do most of the buying) | Run `make_dbs.py` once |
| `make_dbs.py` + `sql/*.sql`: builds `idx_*` and `noidx_*` databases | — |
| [QUERIES.md](QUERIES.md): all 15 queries with SQL and explanations | Wrap each one in a route (≈5 lines each) |
| `app/experiment.py`: `?db=` selection + `run_query()` (timing + plan) | Use it in every route |
| `driver.py`: runs everything, writes `results.md` | Run it, paste the table |
| `loadtest.py`: fires concurrent `POST`s | Run it 4 times (Phase 4) |
| — | Write [FINDINGS.md](FINDINGS_TEMPLATE.md): short answers backed by your numbers |

Everything lives in [starter_code/](starter_code/). Run every command below **from that folder**.

---

## Step 0 — Setup (about 10 minutes)

You need Python 3.11+ and the `sqlite3` command-line tool. For background, read the [SQLite lecture](../../Lectures/02_sqlite/) and the [SQLite performance lecture](../../Lectures/02_sqlite_performance/README.md); `EXPLAIN QUERY PLAN` is covered in [sqlite_walkthrough.md §4](../../Lectures/02_sqlite/sqlite_walkthrough.md).

```bash
cd Assignments/01_sqlite_api/starter_code
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q                            # 5 passed = your setup works
```

Build the databases (about 20 s, about 300 MB in `data/`, git-ignored):

```bash
python make_dbs.py
```

That creates six files:

| | 10k purchases | 100k purchases | 1M purchases |
| :--- | :--- | :--- | :--- |
| **no indexes** | `data/noidx_10k.db` | `data/noidx_100k.db` | `data/noidx_1m.db` |
| **indexes** | `data/idx_10k.db` | `data/idx_100k.db` | `data/idx_1m.db` |

Each pair holds **identical rows**. The only difference is indexes:

- **`noidx_*`** has only what SQLite creates automatically: `PRIMARY KEY` and `UNIQUE` lookups.
- **`idx_*`** adds the foreign-key indexes from the [lecture schema](../../Lectures/02_sqlite/sql/01_schema.sql) plus three covering indexes from [`sql/covering_indexes.sql`](starter_code/sql/covering_indexes.sql).
- **Both** get a small `monthly_sales` summary table from [`sql/summary_tables.sql`](starter_code/sql/summary_tables.sql), used in Phase 3.

Customers and products scale with purchases (1 customer per 20 purchases, 1 product per 200), so 1M purchases means 50,000 customers and 5,000 products. `make_dbs.py` prints the exact counts; copy them into FINDINGS.

## Step 1 — Implement the routes

Open [QUERIES.md](QUERIES.md) and [`app/main.py`](starter_code/app/main.py). Q01 is already done as an example; every other route follows the same pattern:

```python
Q03_SQL = """ ...copied from QUERIES.md... """

@app.get("/purchases", dependencies=[Depends(require_api_key)])
def q03_purchases(start: str, end: str, db: sqlite3.Connection = Depends(get_exp_db)):
    return run_query(db, Q03_SQL, {"start": start, "end": end})
```

Each route returns:

```json
{
  "elapsed_ms": 0.142,
  "row_count": 100,
  "plan": ["SEARCH purchases USING INDEX idx_purchases_date (purchase_date>? AND purchase_date<?)"],
  "rows": [ ... ]
}
```

Start the API and try each route in the browser as you go:

```bash
python -m app.main                   # http://127.0.0.1:8001/docs
```

```bash
curl -s "http://127.0.0.1:8001/customers/42?db=noidx_1m"
curl -s "http://127.0.0.1:8001/purchases?start=2025-03-01&end=2025-03-08&db=idx_1m"
```

(With `API_KEYS` unset the app runs in dev mode and doesn't check keys. If you set it, add `-H "X-API-Key: dev-key-123"`.)

**Checklist:** 14 slow-or-normal `GET` routes (Q01–Q14), 4 `/fast` routes (Q11–Q14), and 1 `POST` (Q15). That's 19 routes.

## Step 2 — Run the experiment

With the API running, open a second terminal:

```bash
python driver.py --sizes 10k         # quick check that every route works
python driver.py                     # the real run, all six databases (about a minute)
```

The driver calls every route 5 times on every database, keeps the **median** time, and writes:

- `results.md`: a ready-to-paste table, one row per query and one column per database.
- `results.csv`: the same data plus the full query plan for every (query, database) pair.

You do not time anything by hand.

---

## How to read your results

### What the time means

`elapsed_ms` is **milliseconds spent inside SQLite** running the query and fetching its rows. It does not include HTTP or JSON encoding, so it measures the database and nothing else. The driver reports the median of 5 runs, which hides one-off hiccups. Your numbers will differ from a classmate's, depending on CPU and disk; what should match is the **pattern**. Rules of thumb:

| Time | Meaning |
| :--- | :--- |
| under 1 ms | the database barely did anything |
| 1–50 ms | real work, but a user wouldn't notice |
| 100 ms + | a user notices if a page makes a few of these calls |
| 1,000 ms + | a user notices on a single call |

**Speedup** = slower time ÷ faster time. For example, 40 ms (`noidx`) ÷ 0.2 ms (`idx`) = a **200×** speedup.

### What the plan means

The `plan` lines come from `EXPLAIN QUERY PLAN`. You only need a few words:

| Plan says | Plain English | Usually |
| :--- | :--- | :--- |
| `SCAN purchases` | read **every row** of the table | slow on big tables |
| `SEARCH purchases USING INDEX idx_x (col=?)` | jump through an index to just the matching rows | fast |
| `SEARCH ... USING INTEGER PRIMARY KEY` | jump straight to a row by its id | fastest |
| `... USING COVERING INDEX idx_x` | the index has every column needed, so the table is never read | fast |
| `USE TEMP B-TREE FOR ORDER BY / GROUP BY` | build a temporary sorted structure first | extra work |
| `CORRELATED SCALAR SUBQUERY` | run the inner query once **per outer row** | depends on the inner query's plan |

When FINDINGS asks for a **plan summary**, write the one or two lines that matter, e.g. `SCAN purchases + TEMP B-TREE` vs. `SEARCH idx_purchases_date`. Don't describe what the query does; describe *how SQLite runs it*.

---

## Phase 1 — Simple reads (Q01–Q03)

**Expect:** Q01 and Q02 are flat (fast everywhere). Q03 is fast in `idx_*` and grows with size in `noidx_*`.

**In FINDINGS:** your results rows for Q01–Q03 and 2–3 sentences: Why is Q01 fast even with **no** added indexes? What did the Q03 plan look like in each database at 1M?

## Phase 2 — Where indexes matter (Q04–Q10)

**Expect:** big wins for queries that look up a *few* rows (Q04, Q05, Q06, Q08), and smaller wins for queries that must read *every* row (Q07, Q09, Q10).

**In FINDINGS:** your results rows and the speedup at 1M for each query. Then answer:

1. Which query had the largest speedup from indexes? Use its two plans to explain why.
2. Q09 reads every purchase in both databases, yet it's still faster in `idx_1m`. Find the word in its `idx` plan that explains this.
3. Q07 only got about 2× faster. Why can't an index make it 100× faster? (Hint: what does the query have to do after it finds the rows?)

## Phase 3 — When an index can't save you (Q11–Q14)

Each of these has a slow version and a `/fast` rewrite in [QUERIES.md](QUERIES.md).

**Expect:** the slow version is about the same speed in `idx_*` and `noidx_*`, and **Q14 is actually slower with indexes**. Every `/fast` version stays nearly flat as the data grows.

**In FINDINGS:** your results rows. For each of Q11–Q14, write **one or two sentences**: why the slow version is slow (point at the plan), and the trade-off the rewrite makes. Each fast version gives something up; QUERIES.md says what.

## Phase 4 — Write concurrency (Q15)

SQLite allows **one writer at a time** for the whole database file. This phase finds out what that means under load. Every run writes into a scratch copy, so your experiment databases stay clean:

```bash
cp data/idx_100k.db data/writes.db           # Windows: copy data\idx_100k.db data\writes.db
```

Do these **four runs**. For each one, stop the API (Ctrl-C), start it with the command shown, and then run the load test **twice**, with `--n 200` and `--n 500`:

| Run | Start the API with | What changes |
| :--- | :--- | :--- |
| A | `BUSY_TIMEOUT_MS=0 RELOAD=0 python -m app.main` | writers give up **instantly** if the file is locked |
| B | `BUSY_TIMEOUT_MS=5000 RELOAD=0 python -m app.main` | writers **wait** up to 5 s for the lock |
| C | `BUSY_TIMEOUT_MS=0 uvicorn app.main:app --port 8001 --workers 4` | 4 server processes, no waiting |
| D | `BUSY_TIMEOUT_MS=5000 uvicorn app.main:app --port 8001 --workers 4` | 4 server processes, waiting |

Windows PowerShell: set the variable first (`$env:BUSY_TIMEOUT_MS=0`), then run the command without the prefix.

```bash
python loadtest.py --method POST --path "/purchases?db=writes" --n 200
python loadtest.py --method POST --path "/purchases?db=writes" --n 500
```

`loadtest.py` prints how many requests got each status code, plus one example error:

```
POST http://127.0.0.1:8001/purchases?db=writes  x200  in 0.44s
  201: 35
  503: 165
  --- 503 ---
  {"detail":"database error: database is locked"}
```

**What to record** for each run, at each `n`:

- **succeeded**: the count of `201`s.
- **failed**: the count of `503`s. These are `database is locked`.
- **seconds**: the `in X.XXs` value.
- **writes/sec** = succeeded ÷ seconds.

**Then check the summary table.** Run this and compare the two numbers:

```bash
sqlite3 data/writes.db "SELECT COUNT(*) FROM purchases; SELECT SUM(num_purchases) FROM monthly_sales;"
```

**In FINDINGS:** the filled-in table, the exact error text, and three short answers:

1. What does `busy_timeout` actually do, and why did run B succeed where run A failed?
2. Did 4 worker processes (C, D) let SQLite write **faster**? Why or why not?
3. Why don't the two numbers from the summary-table check match? What does that cost the `/fast` routes in Phase 3?

## Phase 5 — Conclusions

Half a page in FINDINGS. For each scenario, say **SQLite: yes or no**, in 1–2 sentences, and cite **one number** from your own results:

1. An internal read-only dashboard used by ~10 analysts
2. A mobile app's offline local storage
3. Ingesting thousands of events per second from many servers
4. A fresh throwaway database for each automated test

---

## Deliverables

| # | Item |
| :--- | :--- |
| 1 | Your `starter_code/` folder with all 19 routes in `app/main.py`; `pytest` passes |
| 2 | `results.md` and `results.csv` from a full `driver.py` run |
| 3 | `FINDINGS.md`, filled in from [FINDINGS_TEMPLATE.md](FINDINGS_TEMPLATE.md) |

Don't commit `data/`; it's git-ignored and the grader rebuilds it.

## Grading (100 pts)

| Area | Pts |
| :--- | :--- |
| All 19 routes work, use the given SQL, and each `/fast` route returns the same rows as its slow twin (except Q12) | 30 |
| Full `driver.py` run: `results.md` covers all six databases | 10 |
| Phase 1–2 answers: correct, and each one points at a plan line or a number | 20 |
| Phase 3 answers: why it's slow + the trade-off, for each of Q11–Q14 | 15 |
| Phase 4: table complete, real error text, three answers | 15 |
| Phase 5 conclusions, each citing your own numbers | 10 |

Short and specific beats long. "Q08 went from 1181 ms to 12 ms because the `noidx` plan re-scans purchases for every product, while `idx` uses `SEARCH ... idx_purchases_product`" is a full-credit answer.

## Stretch (bonus, max +10)

- **5M rows:** add `"5m": 5_000_000` to `SIZES` in `make_dbs.py` and `driver.py`. Which conclusions change?
- **Keep the summary fresh:** write an `AFTER INSERT` trigger on `purchases` that updates `monthly_sales`, then redo Run B. What happens to writes/sec?
- **Search:** add `GET /products/search?q=` with `LIKE '%' || :q || '%'` and an FTS5 version (see the [FTS5 handout](handouts/lead_wildcard-vs-fts5.md)). Why does it barely matter at 5,000 products?
- **Auth:** move API keys into a hashed `api_keys` table (`sql/auth.sql`), keeping `require_api_key`'s signature.

---

## FAQ

**What do I put for data sizes in FINDINGS?**
Copy the row counts `make_dbs.py` printed. With the default settings that's 500 / 5,000 / 50,000 customers and 100 / 500 / 5,000 products.

**What goes in the "index inventory"?**
That table is gone. You run one command instead, which is in the template.

**Is the time column how long the query took?**
Yes: the median `elapsed_ms` that the driver measured. You don't time anything yourself.

**Is "plan summary" asking what the query does?**
No. It asks *how SQLite runs it*: the one or two `SCAN` / `SEARCH` lines that matter. See [How to read your results](#how-to-read-your-results).

**Do I need to create indexes myself?**
No. `make_dbs.py` builds both versions. Read [`sql/covering_indexes.sql`](starter_code/sql/covering_indexes.sql) so you know what's in `idx_*`. There are only six lines.

**Do I need a plan and time for every query at every size?**
The driver collects all of them. In your written answers, quote the plan lines that support your point, usually at 1M.

**How long should the Phase 3 explanations be?**
One or two sentences per query.

**Phase 4 mitigations?**
Replaced by the four runs above. You record four numbers per run.

## Academic integrity

Generative tools may help you write route boilerplate and explain plan output. The answers in FINDINGS must be about **your** measurements, in your own words. Cite any external source you lean on.
