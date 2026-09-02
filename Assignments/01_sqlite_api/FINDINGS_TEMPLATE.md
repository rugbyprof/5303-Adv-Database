# FINDINGS — Assignment 01

> Copy this to `FINDINGS.md` and fill it in. Paste **real** output — query
> plans, timings, error text. Prose without evidence earns little.

## Environment

- SQLite version (`sqlite3 --version`):
- Python version / driver (`sqlite3` stdlib or `aiosqlite`):
- Machine (CPU, RAM, disk type — SSD vs. spinning vs. network):
- Data sizes generated: `purchases = {1k, 100k, 1M, 5M}`, `customers = …`,
  `products = …`, `--skew` yes/no

## Index inventory

| Table | Indexed columns | Left unindexed (and why it matters) |
| :--- | :--- | :--- |
| purchases | | |
| customers | | |
| … | | |

---

## Phase 1 — baseline

| Endpoint | 1k | 100k | 1M | 5M | Query plan (1-line summary) |
| :--- | :-- | :-- | :-- | :-- | :--- |
| `GET /customers/{id}` | | | | | |
| `GET /products?limit=50&offset=0` | | | | | |
| `GET /purchases?start=&end=` | | | | | |

Observation:

---

## Phase 2 — joins & aggregates

For each endpoint: the SQL, the `EXPLAIN QUERY PLAN`, and timing at 1M rows.

### `/customers/{id}/purchases`

```sql
-- your query
```
```
-- EXPLAIN QUERY PLAN
```

### Index exercise (`/customers/{id}/purchases`, 1M rows)

| State | Plan | Time |
| :--- | :--- | :--- |
| with `idx_purchases_customer` | | |
| after `DROP INDEX idx_purchases_customer` | | |
| after adding a covering index `(customer_id, product_id, department, amount, purchase_date)` | | |

What changed, and why:

### `/stats/revenue-by-state`, `/stats/revenue-by-month`, `/products/top`

```sql
```
```
-- plans
```

---

## Phase 3 — gnarly queries

For each: SQL · plan · time at 100k / 1M / 5M · one-paragraph diagnosis.

### `/purchases?offset=900000` — deep OFFSET

| | Plan | 1M | 5M |
| :--- | :--- | :-- | :-- |
| `LIMIT ? OFFSET ?` | | | |
| keyset: `WHERE purchase_id > ? ORDER BY purchase_id LIMIT ?` | | | |

Diagnosis:

### `/products/search?q=` — LIKE '%q%' → FTS5

| | Plan | 1M | 5M |
| :--- | :--- | :-- | :-- |
| `WHERE product_name LIKE '%'||?||'%'` | | | |
| FTS5 `MATCH` | | | |

FTS5 table definition used:

Diagnosis:

### `/purchases?...&total=true` — COUNT(*) of the filtered set

### `/customers/leaderboard` — 90-day trailing window

### `/customers/{id}/streaks` — gaps and islands

### `/reports/cube` — state × department × month + HAVING

### `/purchases/sample` — ORDER BY random() LIMIT 10

### `/products/dead?state=` — anti-join

### My two additional endpoints

1. `GET /…` — demonstrates:
2. `GET /…` — demonstrates:

---

## Phase 4 — write concurrency

### Baseline: `POST /purchases` × {50, 200} concurrent

```
-- paste the status-code spread + the exact exception text
```

### Mitigations

| Change | Concurrent POSTs that succeed | Where it stops helping |
| :--- | :--- | :--- |
| none (default) | | |
| `PRAGMA busy_timeout = 5000` | | |
| `journal_mode = WAL` | | |
| batch N inserts per transaction | | |
| single serialized writer task / queue | | |

### Background writer competing with request writes

Observation:

### Two `uvicorn` processes, same file

Observation:

### Same file on a network share

What breaks (don't run it — explain from the docs):

**At what write concurrency / rate does SQLite stop fitting this workload?**

---

## Auth

- [ ] Keys moved to `api_keys` table, stored hashed (`________` algorithm)
- [ ] Lookup by hash, `hmac.compare_digest`, `revoked_at` respected
- [ ] `require_api_key` public signature unchanged (JWT-swap ready)

Notes:
