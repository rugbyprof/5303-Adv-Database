# Assignment 01 — The Queries

Every query for the assignment is written out below. **You do not write SQL for this assignment.** Your job is to put each query behind a FastAPI route, run the experiment, and explain what you see.

Each entry gives you:

- **Route** — the exact path to use. `driver.py` calls these paths, so don't rename them.
- **What it answers** — the question in plain English.
- **SQL** — copy it into `app/main.py` as written.
- **Why it behaves the way it does** — read this *after* you have run it, and check whether your numbers agree.

The `:name` placeholders are **named parameters**. Pass them as a dict, for example `run_query(db, Q01_SQL, {"customer_id": customer_id})`. Never paste values into the SQL string.

## The route pattern

Every read route looks the same. Put the SQL in a module-level constant and use the two helpers from `app/experiment.py`:

```python
from .experiment import get_exp_db, run_query

Q01_SQL = """
SELECT c.customer_id, c.first_name, c.last_name, c.email, c.zipcode, z.state_code
FROM customers c
JOIN zipcodes z ON z.zipcode = c.zipcode
WHERE c.customer_id = :customer_id
"""

@app.get("/customers/{customer_id}", dependencies=[Depends(require_api_key)])
def q01_customer(customer_id: int, db: sqlite3.Connection = Depends(get_exp_db)):
    return run_query(db, Q01_SQL, {"customer_id": customer_id})
```

- `get_exp_db` reads `?db=noidx_1m` (or any other database name) from the URL and opens that file in `data/`.
- `run_query` runs the SQL and returns `{"elapsed_ms", "row_count", "plan", "rows"}`.

Query-string parameters such as `start`, `end` and `state` become ordinary function arguments, the way FastAPI always handles them.

> **Route order matters.** FastAPI matches routes top to bottom. Declare
> `/purchases/page/fast` and `/purchases/sample` **before** any route shaped
> like `/purchases/{something}`. `/customers/{customer_id}/purchases` is fine
> because it has a different number of path segments.

---

## Phase 1 — Simple reads

### Q01 — One customer by id

**Route:** `GET /customers/{customer_id}`
**What it answers:** "Show me customer 42."

```sql
SELECT c.customer_id, c.first_name, c.last_name, c.email, c.zipcode, z.state_code
FROM customers c
JOIN zipcodes z ON z.zipcode = c.zipcode
WHERE c.customer_id = :customer_id
```

**Why it behaves this way:** `customer_id` is the `INTEGER PRIMARY KEY`, so SQLite jumps straight to the row. Then it uses the primary key on `zipcodes` to fetch the state. Primary keys are always indexed, so this query is instant in **both** databases at every size.

### Q02 — One page of products

**Route:** `GET /products?limit=50&offset=0`
**What it answers:** "Show me the first page of the product catalog."

```sql
SELECT product_id, product_name, unit_price
FROM products
ORDER BY product_id
LIMIT :limit OFFSET :offset
```

**Why it behaves this way:** The plan says `SCAN products`, but SQLite walks the table in primary-key order and stops after 50 rows. A "scan" that stops early is cheap. Q11 shows what happens when the offset is large.

### Q03 — Purchases in a date range

**Route:** `GET /purchases?start=2025-03-01&end=2025-03-08`
**What it answers:** "Show me the first 100 purchases from the first week of March 2025."

```sql
SELECT purchase_id, customer_id, product_id, department, amount, purchase_date
FROM purchases
WHERE purchase_date >= :start AND purchase_date < :end
ORDER BY purchase_date
LIMIT 100
```

**Why it behaves this way:** In `idx_*` the plan is `SEARCH purchases USING INDEX idx_purchases_date`. SQLite jumps to March 1st, reads 100 rows in date order, and stops. In `noidx_*` the plan is `SCAN purchases` plus `USE TEMP B-TREE FOR ORDER BY`. It reads **every** purchase, keeps the ones in range, sorts them, and then returns 100. This is the first query where the two databases diverge, and the gap grows with table size.

---

## Phase 2 — Where indexes matter

All seven queries run unchanged against both databases. What you measure is how much the index helps, and for some queries that it **doesn't**.

### Q04 — One customer's purchase history

**Route:** `GET /customers/{customer_id}/purchases`
**What it answers:** "Show me this customer's 100 most recent purchases, with product names."

```sql
SELECT pu.purchase_id, pu.purchase_date, pr.product_name, pu.department, pu.amount
FROM purchases pu
JOIN products pr ON pr.product_id = pu.product_id
WHERE pu.customer_id = :customer_id
ORDER BY pu.purchase_date DESC
LIMIT 100
```

**Why it behaves this way:** `purchases.customer_id` is a foreign key, and **SQLite does not index foreign keys automatically.** In `noidx_*` the plan is `SCAN pu`, which reads the whole table to find one customer's rows. In `idx_*` it is `SEARCH pu USING INDEX idx_purchases_customer (customer_id=?)`. The driver passes the customer with the *most* purchases (the "whale" that `--skew` creates), so this is a worst case.

### Q05 — Count purchases in one department

**Route:** `GET /stats/department-count?department=Games`
**What it answers:** "How many purchases were in the Games department?"

```sql
SELECT COUNT(*) AS num_purchases
FROM purchases
WHERE department = :department
```

**Why it behaves this way:** In `idx_*` the plan is `SEARCH purchases USING COVERING INDEX idx_purchases_department`. A **covering** index contains every column the query needs, so SQLite counts index entries and never touches the table. In `noidx_*` it reads every row. Note that the index still has to count every Games entry. It reads fewer, smaller entries, but the answer is not free.

### Q06 — A customer's purchase streaks

**Route:** `GET /customers/{customer_id}/streaks`
**What it answers:** "What were this customer's longest runs of buying something on consecutive days?" See the [gaps-and-islands handout](handouts/streaks_gaps_islands.md).

```sql
WITH days AS (
    SELECT DISTINCT purchase_date AS day
    FROM purchases
    WHERE customer_id = :customer_id
),
islands AS (
    SELECT day,
           julianday(day) - ROW_NUMBER() OVER (ORDER BY day) AS grp
    FROM days
)
SELECT MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM islands
GROUP BY grp
HAVING COUNT(*) >= 2
ORDER BY days DESC, streak_start
LIMIT 10
```

**Why it behaves this way:** Consecutive dates minus their row number give the same value, so each streak becomes one group. All of the expensive work is in the first step, which finds this customer's rows. In `idx_*` that step is a `SEARCH` through an index; in `noidx_*` it is a full `SCAN`. Read your plan to see *which* index SQLite picked, because it may not be the one you would guess. Everything after that step works on one customer's handful of dates, so it is cheap either way.

### Q07 — 90-day spending leaderboard

**Route:** `GET /stats/leaderboard?start=2026-06-02&end=2026-09-01`
**What it answers:** "Who were the top 20 spenders in the last 90 days, and what rank is each?" See the [ranking handout](handouts/ranking-by-90-day-window.md).

```sql
WITH spend AS (
    SELECT customer_id, SUM(amount) AS total
    FROM purchases
    WHERE purchase_date >= :start AND purchase_date < :end
    GROUP BY customer_id
)
SELECT customer_id, ROUND(total, 2) AS total,
       RANK() OVER (ORDER BY total DESC) AS rank
FROM spend
ORDER BY total DESC
LIMIT 20
```

**Why it behaves this way:** The covering index `idx_purchases_date_cust_amount (purchase_date, customer_id, amount)` lets SQLite read only the 90-day slice and only the three columns it needs. Even so, it must still sum *every* purchase in the window and sort every customer's total, because no index stores "rank". Expect roughly 2× faster with the index, not 100×.

### Q08 — Products never bought in a state (anti-join)

**Route:** `GET /products/dead?state=TX`
**What it answers:** "Which products has nobody in Texas ever bought?" See the [anti-join handout](handouts/anti-join-products-not-exists.md).

```sql
SELECT pr.product_id, pr.product_name
FROM products pr
WHERE NOT EXISTS (
    SELECT 1
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    WHERE pu.product_id = pr.product_id
      AND z.state_code  = :state
)
ORDER BY pr.product_id
LIMIT 100
```

**Why it behaves this way:** For **each** product, the inner query asks "is there at least one Texas purchase of this product?" In `idx_*`, `idx_purchases_product` lets SQLite jump to that product's purchases and stop at the first Texas buyer. In `noidx_*` it has to search the big table again for every product. Expect the biggest index win in the assignment.

### Q09 — Revenue by state

**Route:** `GET /stats/revenue-by-state`
**What it answers:** "Total purchases and revenue for each state."

```sql
SELECT z.state_code, COUNT(*) AS num_purchases, ROUND(SUM(pu.amount), 2) AS revenue
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY z.state_code
ORDER BY revenue DESC
```

**Why it behaves this way:** This query has no `WHERE`, so every purchase must be read whichever database you use. What the index changes is **how** each purchase is read. With `idx_purchases_cust_amount (customer_id, amount)` the purchase side is a `COVERING INDEX`, a compact copy of just the two needed columns. Without the index, SQLite reads full rows.

> **Why the index has to be covering:** If you remove the covering index and
> keep only the plain `idx_purchases_customer`, this query gets **slower**
> than having no index at all. SQLite follows the index and then jumps back
> to the table for `amount` once per row, which is a million random reads
> instead of one sequential scan. An index can make a query worse.

### Q10 — Top 10 products by revenue

**Route:** `GET /products/top`
**What it answers:** "Which 10 products brought in the most money?"

```sql
SELECT pr.product_id, pr.product_name,
       COUNT(*) AS num_purchases, ROUND(SUM(pu.amount), 2) AS revenue
FROM purchases pu
JOIN products pr ON pr.product_id = pu.product_id
GROUP BY pr.product_id
ORDER BY revenue DESC
LIMIT 10
```

**Why it behaves this way:** Q10 works the same way as Q09. The covering index `idx_purchases_prod_amount (product_id, amount)` already holds purchases grouped by product, so SQLite skips building a temporary B-tree for the `GROUP BY`. `LIMIT 10` doesn't save any work, because the database has to total every product before it can tell which 10 are on top.

---

## Phase 3 — When an index can't save you

These four queries are slow in **both** databases, and adding an index doesn't fix them. Each one has a rewrite: a second route with the same path plus `/fast`. Implement both versions, and confirm that they return the same rows (except Q12, which is random).

### Q11 — Deep pagination: `OFFSET` vs. keyset

**Routes:** `GET /purchases/page?offset=900000` and `GET /purchases/page/fast?after_id=900000`
**What it answers:** "Show me page 18,001 of all purchases (50 per page)." See the [pagination handout](handouts/offset-vs-keyset-pagination.md).

Slow:

```sql
SELECT purchase_id, customer_id, product_id, amount, purchase_date
FROM purchases
ORDER BY purchase_id
LIMIT 50 OFFSET :offset
```

Fast:

```sql
SELECT purchase_id, customer_id, product_id, amount, purchase_date
FROM purchases
WHERE purchase_id > :after_id
ORDER BY purchase_id
LIMIT 50
```

**Why:** `OFFSET 900000` doesn't skip rows. SQLite reads 900,000 rows and throws them away. The keyset version remembers the last id the client saw and uses the primary key to jump straight past it (`SEARCH ... (rowid>?)`). The cost of `OFFSET` grows with page depth. The cost of keyset stays the same on every page. The client has to send back the last `purchase_id` it received instead of a page number.

### Q12 — Random sample: `ORDER BY random()` vs. random ids

**Routes:** `GET /purchases/sample` and `GET /purchases/sample/fast`
**What it answers:** "Give me 10 random purchases." See the [random sampling handout](handouts/random-sampling.md).

Slow:

```sql
SELECT purchase_id, customer_id, product_id, amount, purchase_date
FROM purchases
ORDER BY random()
LIMIT 10
```

Fast: pick 10 random ids in Python, then fetch them by primary key.

```sql
SELECT purchase_id, customer_id, product_id, amount, purchase_date
FROM purchases
WHERE purchase_id IN (:id1, :id2, :id3, :id4, :id5, :id6, :id7, :id8, :id9, :id10)
```

```python
import random

@app.get("/purchases/sample/fast", dependencies=[Depends(require_api_key)])
def q12_sample_fast(db: sqlite3.Connection = Depends(get_exp_db)):
    max_id = db.execute("SELECT MAX(purchase_id) FROM purchases").fetchone()[0]
    ids = random.sample(range(1, max_id + 1), 10)
    params = {f"id{i}": v for i, v in enumerate(ids, start=1)}
    return run_query(db, Q12_FAST_SQL, params)
```

**Why:** `ORDER BY random()` gives every row a random number and then sorts all of them, a million rows sorted to keep 10. `MAX(purchase_id)` is a single primary-key lookup, and fetching 10 ids is 10 more. The shortcut assumes ids have no large gaps; heavy deletes would bias the sample (see the handout).

### Q13 — Revenue by month: scan vs. summary table

**Routes:** `GET /stats/revenue-by-month` and `GET /stats/revenue-by-month/fast`
**What it answers:** "Total purchases and revenue for every month."

Slow:

```sql
SELECT substr(purchase_date, 1, 7) AS month,
       COUNT(*) AS num_purchases, ROUND(SUM(amount), 2) AS revenue
FROM purchases
GROUP BY month
ORDER BY month
```

Fast (reads the `monthly_sales` table that `make_dbs.py` built from `sql/summary_tables.sql`):

```sql
SELECT month, SUM(num_purchases) AS num_purchases, ROUND(SUM(revenue), 2) AS revenue
FROM monthly_sales
GROUP BY month
ORDER BY month
```

**Why:** The question covers *all* of history, so every purchase must be added up. No index can avoid that. The fix is to do the adding once, ahead of time, into a small table (about 36,000 rows at 1M purchases instead of 1,000,000). The cost is staleness: purchases inserted after the summary was built are missing until you rebuild it. Phase 4 shows this.

### Q14 — State × department × month report (multi-CTE)

**Routes:** `GET /reports/cube?start=2025-01-01&end=2026-01-01&min_purchases=10` and `GET /reports/cube/fast` (same parameters)
**What it answers:** "For 2025, which (state, department, month) combinations had at least 10 purchases, and which brought in the most revenue?" See the [multi-CTE handout](handouts/multi-cte.md).

Slow:

```sql
WITH base AS (
    SELECT z.state_code, pu.department,
           substr(pu.purchase_date, 1, 7) AS month, pu.amount
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    WHERE pu.purchase_date >= :start AND pu.purchase_date < :end
),
cube AS (
    SELECT state_code, department, month,
           COUNT(*) AS num_purchases, SUM(amount) AS revenue
    FROM base
    GROUP BY state_code, department, month
)
SELECT state_code, department, month, num_purchases, ROUND(revenue, 2) AS revenue
FROM cube
WHERE num_purchases >= :min_purchases
ORDER BY revenue DESC
LIMIT 50
```

Fast:

```sql
SELECT state_code, department, month, num_purchases, ROUND(revenue, 2) AS revenue
FROM monthly_sales
WHERE month >= substr(:start, 1, 7) AND month < substr(:end, 1, 7)
  AND num_purchases >= :min_purchases
ORDER BY revenue DESC
LIMIT 50
```

**Why:** This is the trap from Q09 again. In `idx_*` the planner walks the `zipcodes → customers → purchases` indexes, but `department` is not in any covering index. So it jumps back to the table once per purchase, and the query ends up **slower than in `noidx_*`**. Compare your two columns. The summary table already holds exactly this (state, department, month) grain, so the rewrite is a filter over a small table.

---

## Phase 4 — Writes

### Q15 — Insert a purchase

**Route:** `POST /purchases?db=writes`
**What it does:** Inserts one purchase inside a transaction and returns the new row with status `201`. If the database stays locked longer than the busy timeout, it returns `503`.

```python
from .models import NewPurchase

@app.post("/purchases", status_code=201, dependencies=[Depends(require_api_key)])
def q15_create_purchase(body: NewPurchase, db: sqlite3.Connection = Depends(get_exp_db)):
    try:
        with db:  # BEGIN ... COMMIT, or ROLLBACK if anything raises
            row = db.execute(
                """
                INSERT INTO purchases
                    (customer_id, card_id, product_id, department, amount, purchase_date)
                VALUES (:customer_id, :card_id, :product_id, :department, :amount, :purchase_date)
                RETURNING purchase_id, customer_id, product_id, department, amount, purchase_date
                """,
                body.model_dump(mode="json"),
            ).fetchone()
    except sqlite3.OperationalError as exc:   # "database is locked"
        raise HTTPException(503, f"database error: {exc}") from exc
    return dict(row)
```

**Why it behaves this way:** SQLite allows **one writer at a time** for the whole file. When a second writer arrives, it waits up to `busy_timeout` milliseconds for the lock. If the lock is still held after that, it fails with `database is locked`. WAL mode lets readers continue while someone writes, but it never allows two writers at once. The [README](README.md#phase-4--write-concurrency-q15) explains how to measure this.
