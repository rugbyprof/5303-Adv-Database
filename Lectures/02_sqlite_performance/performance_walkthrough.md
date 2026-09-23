# SQLite Query Performance: Reading Plans and Fixing Slow Queries

[Lecture 02](../02_sqlite/) built a normalized store database and queried it
with 1,000 rows, where every query is instant. This lecture scales the same
schema to **1,000,000 purchases** and asks why some queries stay instant while
others take a second or more. It covers the concepts behind the Phase 3 "gnarly
queries" in [Assignment 01](../../Assignments/01_sqlite_api/):

- pagination
- search
- counting
- window functions
- gaps-and-islands
- multi-CTE reports
- random sampling
- anti-joins

One question runs through the whole lecture:

> **How many rows does this query touch, and does that number grow with the
> table or with the result?**

A query that touches a number of rows proportional to its _result_ stays fast
forever. A query that touches rows proportional to the _table_ gets slower
every time the table grows. Much of Phase 3 is learning to tell those apart from
the query plan, before a user notices.

---

## 0. Setup

Build a scaled database with the assignment's generator. It's seeded, so your
rows match the ones shown here. The build takes about 10 seconds.

```bash
cd Lectures/02_sqlite_performance
python ../../Assignments/01_sqlite_api/starter/scale_data.py \
    --db perf.db --customers 50000 --products 5000 --purchases 1000000 --skew
```

`--skew` makes a few customers and products extremely popular, like real data.
One customer has ~28,000 purchases. 10% of customers never buy anything, and
30% of products never sell.

Every script in [sql/](sql/) turns on two shell settings:

```
.eqp on      -- print the query plan before each result
.timer on    -- print wall time after it
```

Run one with `sqlite3 perf.db ".read sql/01_reading_plans.sql"`, or open
`sqlite3 perf.db`, type those two lines, and paste queries one at a time.

> **About the timings.** The numbers in this document were measured on an
> Apple-silicon laptop with the database already in the OS cache. Yours will
> differ. **Compare ratios, not absolute values:** 0.1 ms vs 120 ms tells the
> story on any machine. The first run of anything is slower (cold cache), so
> run it twice.

---

## 1. How SQLite finds rows

Everything in a SQLite file is a **B-tree**: a sorted, balanced tree of pages.

- **A table** is a B-tree keyed by its `rowid`. `INTEGER PRIMARY KEY` columns
  like `purchase_id` _are_ the rowid. The leaves hold the full rows.
- **An index** is a _separate_ B-tree whose keys are the indexed columns, and
  every entry **ends with the rowid** of its row. `idx_purchases_date` is really
  sorted by `(purchase_date, purchase_id)`.

```
idx_purchases_date                         purchases (table B-tree)
┌───────────────────────────┐              ┌─────────────────────────────────┐
│ ('2026-08-01', 3004)      │──rowid──►    │ 3004 │ cust │ card │ prod │ ... │
│ ('2026-08-01', 7719)      │──rowid──►    │ 7719 │ ...                      │
│ ('2026-08-02', 1122)      │   ...        │ ...                             │
└───────────────────────────┘              └─────────────────────────────────┘
```

That gives four basic costs. Everything later in the lecture combines these:

| Operation      | What happens                                                                  | Cost                                                            |
| :------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| **Seek**       | Descend the tree to one key                                                   | ~log(n). About 3–4 page reads at 1M rows                        |
| **Range walk** | Seek, then step through the next _k_ entries in order                         | log(n) + k                                                      |
| **Lookup**     | For each index entry, seek into the table by rowid to fetch the other columns | +1 seek **per row**, and the seeks jump around the file         |
| **Full scan**  | Read every leaf of the table in storage order                                 | n (sequential, so each row is cheap, but there are all of them) |

And one more:

- **Temp B-tree (sort).** If rows must come out in an order no index provides
  (`ORDER BY`, `GROUP BY`, `DISTINCT`, window `PARTITION BY`), SQLite inserts
  them all into a temporary B-tree first. That costs n·log(n) _on the rows fed
  into it_.

A **covering index** contains every column the query needs, so the lookup step
disappears entirely.

---

## 2. Reading `EXPLAIN QUERY PLAN`

Script: [sql/01_reading_plans.sql](sql/01_reading_plans.sql)

### The vocabulary

| Plan text                                            | Meaning                                                                                     | Grows with                 |
| :--------------------------------------------------- | :------------------------------------------------------------------------------------------ | :------------------------- |
| `SEARCH t USING INTEGER PRIMARY KEY (rowid=?)`       | Seek by rowid                                                                               | nothing (log n)            |
| `SEARCH t USING INDEX i (col=?)` / `(col>?)`         | Seek/range on an index, **then a table lookup per match**                                   | matching rows              |
| `SEARCH t USING COVERING INDEX i (...)`              | Seek/range on an index, no lookups                                                          | matching rows              |
| `SCAN t`                                             | Read the whole table                                                                        | **table**                  |
| `SCAN t USING INDEX i`                               | Walk the _whole_ index in order, with a lookup per row                                      | **table**, with random I/O |
| `SCAN t USING COVERING INDEX i`                      | Walk the whole index, no lookups                                                            | **table**, but fewer pages |
| `USE TEMP B-TREE FOR ORDER BY / GROUP BY / DISTINCT` | Sort everything that reached this point                                                     | rows fed in (n·log n)      |
| `USE TEMP B-TREE FOR LAST TERM OF ORDER BY`          | Rows arrive partly sorted; sort within each group                                           | rows fed in                |
| `CORRELATED SCALAR SUBQUERY n`                       | Run the subquery **once per outer row**                                                     | outer rows × subquery cost |
| `CO-ROUTINE x`                                       | A subquery/CTE streamed row by row into its parent                                          | —                          |
| `MATERIALIZE x`                                      | A subquery/CTE computed once into a temp table                                              | its size                   |
| `AUTOMATIC COVERING INDEX`                           | SQLite built a throwaway index for this one query. It's a hint that you may want a real one | —                          |
| `VIRTUAL TABLE INDEX …`                              | Handed to a virtual table module such as FTS5                                               | depends on the module      |

**What to look for:** a `SCAN` of a big table, a `TEMP B-TREE` fed by a big
table, or a `CORRELATED` subquery under a big outer loop. Any of these in an
endpoint means the endpoint slows down as the data grows.

### The examples (1M purchases)

| #   | Query                                          | Plan                                         |   Time |
| :-- | :--------------------------------------------- | :------------------------------------------- | -----: |
| 1   | `WHERE purchase_id = 500000`                   | `SEARCH … INTEGER PRIMARY KEY`               |  <1 ms |
| 2   | `count(*) WHERE purchase_date >= '2026-08-01'` | `SEARCH … COVERING INDEX idx_purchases_date` |  <1 ms |
| 3   | `purchase_id, amount WHERE purchase_date = …`  | `SEARCH … USING INDEX` (lookups)             |  <1 ms |
| 4   | `count(*) WHERE amount > 395`                  | `SCAN purchases`                             |  25 ms |
| 5   | `ORDER BY amount DESC LIMIT 5`                 | `SCAN` + `TEMP B-TREE FOR ORDER BY`          |  31 ms |
| 6   | `GROUP BY strftime('%Y', …)`                   | `SCAN` + `TEMP B-TREE FOR GROUP BY`          | 236 ms |

Note #5: **`LIMIT` doesn't save you from the scan.** The top 5 aren't known
until every row has been seen.

### Does it grow? The same queries at two sizes

| Query                             | 100k purchases | 1M purchases | Grows with                         |
| :-------------------------------- | -------------: | -----------: | :--------------------------------- |
| PK lookup                         |          <5 ms |        <5 ms | nothing                            |
| indexed date-range count          |          <1 ms |        <1 ms | result                             |
| unindexed filter (`amount > 395`) |           3 ms |        25 ms | table (×8)                         |
| `ORDER BY random() LIMIT 5`       |           5 ms |        45 ms | table (×9)                         |
| window over the whole table (§6)  |          64 ms |     1,153 ms | table, _worse_ than linearly (×18) |

This is the table you're building in the assignment: data size × endpoint →
plan and time. The rows that grow are the ones to diagnose.

### The planner can choose badly

Query #8 in the script, revenue per department for one month:

```sql
SELECT department, round(sum(amount), 2) AS revenue
FROM purchases
WHERE purchase_date >= '2026-08-01'
GROUP BY department;
```

```
`--SCAN purchases USING INDEX idx_purchases_department           327 ms
```

SQLite walked the **entire** department index, with a table lookup for every
one of 1M rows. It did that so rows arrive already grouped and no sort is
needed. The date filter matches only ~3% of rows, but the planner doesn't know
that. `ANALYZE` stats (`sqlite_stat1`) record _how many rows per key_ on
average, not how dates are distributed, so a range like `>= ?` gets a generic
guess.

Tell it not to use an index for the grouping term, with a unary `+`:

```sql
... GROUP BY +department;
```

```
|--SEARCH purchases USING INDEX idx_purchases_date (purchase_date>?)
`--USE TEMP B-TREE FOR GROUP BY                                   29 ms
```

That's 11× faster, from reading the plan. Other levers:
`FROM purchases INDEXED BY idx_purchases_date`, `FROM purchases NOT INDEXED`,
and keeping statistics current with `ANALYZE` / `PRAGMA optimize`. Watch for
`SCAN … USING INDEX idx_purchases_department` in your own reports. It shows up
again in §8.

### Walking an index is not free

The trap above generalizes. **An index helps when it lets you touch _few_
rows.** When the query touches all of them anyway, walking a non-covering index
turns one sequential scan into a million random lookups. In §6 that difference
is 786 ms (index walk) vs 231 ms (`NOT INDEXED`) vs 36 ms (covering index).

---

## 3. Pagination: `OFFSET` vs keyset

Script: [sql/02_pagination.sql](sql/02_pagination.sql)

`LIMIT 5 OFFSET 900000` still has to _produce_ the first 900,000 rows before it
can throw them away. Each skipped row is still joined, still read. The plan is
identical for page 1 and page 180,001. Only the time changes:

| Query                                                        | Plan                    |   Time |
| :----------------------------------------------------------- | :---------------------- | -----: |
| `ORDER BY purchase_id LIMIT 5 OFFSET 0` (+ join to products) | `SCAN pu`               |  <5 ms |
| `… LIMIT 5 OFFSET 900000`                                    | `SCAN pu`               | 118 ms |
| `… WHERE purchase_id > 900000 ORDER BY purchase_id LIMIT 5`  | `SEARCH pu … (rowid>?)` |  <1 ms |

**Keyset (seek) pagination:** the response includes the last key on the page,
and the client sends it back to get the next page. The query _seeks_ to that
key, so every page costs the same.

```sql
WHERE purchase_id > :cursor ORDER BY purchase_id LIMIT :page_size
```

**When the sort column isn't unique** (newest first by date), a date-only
cursor skips or repeats rows that share a date. Add the primary key as a
tie-breaker and compare them together as a **row value**:

```sql
WHERE (purchase_date, purchase_id) < (:last_date, :last_id)
ORDER BY purchase_date DESC, purchase_id DESC
LIMIT 5;
```

Because every index entry ends with the rowid, `idx_purchases_date` is already
in `(purchase_date, purchase_id)` order. It serves this `ORDER BY` with no sort
and seeks straight to the cursor.

**The trade-off:** there's no "jump to page 50,000" any more. You get only
next and previous from a known row. For an API feed or infinite scroll, that's
fine. For a UI with numbered pages, it's a product decision.

---

## 4. Search: `LIKE`, indexes, and FTS5

Script: [sql/03_search_fts5.sql](sql/03_search_fts5.sql). The examples search
`customers`, which has 50k rows.

### When can `LIKE` use an index?

A B-tree is sorted by the **start** of the string, so it can only help if the
pattern pins down the start:

| Pattern                                                | Can seek?                                   | Why                                                                                                                                 |
| :----------------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------- |
| `LIKE '%hopper%'`                                      | ❌                                          | Leading wildcard: a match could be anywhere in the sort order                                                                       |
| `email LIKE 'grace%'` on a normal index                | ❌                                          | SQLite's `LIKE` is case-**in**sensitive, but the index is sorted case-sensitively (`BINARY`), so a range seek could miss `'Grace…'` |
| `last_name LIKE 'Hop%'` with an index `COLLATE NOCASE` | ✅ `SEARCH … (last_name>? AND last_name<?)` | Collation matches, so the prefix becomes a range                                                                                    |
| `last_name LIKE '%per'` with the same index            | ❌                                          | Leading wildcard again. It scans the (smaller) index                                                                                |

In the plan, a scan of a _covering index_ (`SCAN customers USING COVERING INDEX
sqlite_autoindex_customers_1`) is still a scan of every entry.

### FTS5: an inverted index

A full-text index flips the problem around. Instead of "row → text", it stores
**token → list of rowids**, so finding a word is a seek, no matter where in the
text the word appears.

```sql
CREATE VIRTUAL TABLE customers_fts USING fts5(
    first_name, last_name, email,
    content = 'customers', content_rowid = 'customer_id'   -- external content
);
INSERT INTO customers_fts(customers_fts) VALUES ('rebuild');   -- index existing rows

SELECT c.* FROM customers_fts f JOIN customers c ON c.customer_id = f.rowid
WHERE customers_fts MATCH 'grace AND hop*'   -- boolean ops, prefix queries
ORDER BY f.rank                              -- bm25 relevance
LIMIT 5;
```

Things to understand before you use it:

- **External content** (`content='customers'`) means the FTS table stores only
  the index, not a second copy of the text. You join back by rowid for the
  columns you want.
- **It matches tokens, not substrings.** The default `unicode61` tokenizer splits
  `grace.hopper.45@example.com` into `grace | hopper | 45 | example | com`. So
  `MATCH 'ove'` finds **0** rows, while `LIKE '%ove%'` finds 2,494
  (every "l**ove**lace"). Decide which behavior your endpoint
  promises.
- **Want indexed substring search?** Use `tokenize='trigram'`. It indexes every
  3-character slice, and plain `LIKE '%ove%'` then uses the FTS index. The index
  is bigger, and patterns under 3 characters fall back to scanning.
- **It doesn't update itself.** With external content, you add `AFTER
INSERT/UPDATE/DELETE` triggers on the base table (in the script) or the index
  silently goes stale. That's extra work on every write. Remember it in Phase 4.
- **The build is a one-time cost** (~35 ms here, ~320 ms for trigram). The plan
  reads `SCAN customers_fts VIRTUAL TABLE INDEX 0:M…`. For a virtual table,
  "SCAN" just means "asked the module". The module then did an index lookup.

---

## 5. Counting: `COUNT(*)` isn't free

Script: [sql/04_counting.sql](sql/04_counting.sql)

**SQLite stores no row count.** Every `count(*)` walks something:

| Query                                       | Plan                                                                                             |  Time |
| :------------------------------------------ | :----------------------------------------------------------------------------------------------- | ----: |
| `count(*) FROM purchases`                   | `SCAN … USING COVERING INDEX idx_purchases_product` (the smallest B-tree with one entry per row) |  7 ms |
| `count(*) WHERE department = 'Books'`       | `SEARCH … COVERING INDEX (department=?)` (only the matching range)                               |  1 ms |
| `count(*) WHERE amount BETWEEN 100 AND 200` | `SCAN purchases`                                                                                 | 34 ms |
| …the _page_ of those same rows (`LIMIT 5`)  | `SCAN`, stops after 5 hits                                                                       | <1 ms |

The last two rows are the pattern behind "page + total": **the page stops early
and the count never does.** Adding `total` to a list endpoint can make it many
times slower, and the difference grows with the table.

Cheaper answers, from exact to approximate:

| Technique                                                        | Cost                  | Trade-off                                                           |
| :--------------------------------------------------------------- | :-------------------- | :------------------------------------------------------------------ |
| **Counter table kept by triggers**                               | O(1) read             | Every insert/delete also updates one hot row: more write contention |
| **Capped count**: `SELECT count(*) FROM (SELECT 1 … LIMIT 1001)` | Stops at 1,001        | UI shows "1,000+"                                                   |
| **Has-more**: fetch `LIMIT n+1` rows                             | Same as the page      | No total at all, just "next →"                                      |
| **Planner estimate**: row count from `sqlite_stat1`              | O(1)                  | Stale until the next `ANALYZE`, and whole-table only                |
| **Cache the total** (in the app, with a TTL)                     | O(1) most of the time | Can be wrong for a while after writes                               |

Which one is right is a product question: does anyone need the exact number?

---

## 6. Window functions

Script: [sql/05_window_functions.sql](sql/05_window_functions.sql)

A window function computes a value for each row from a set of related rows,
_without_ collapsing them the way `GROUP BY` does:

```
function(...) OVER ( PARTITION BY <restart for each group>
                     ORDER BY     <order within the group>
                     <frame>      <which rows around the current one> )
```

### Ranking

|   v | `row_number()` | `rank()` | `dense_rank()` |
| --: | -------------: | -------: | -------------: |
|  50 |              1 |        1 |              1 |
|  40 |              2 |        2 |              2 |
|  40 |              3 |        2 |              2 |
|  10 |              4 |        4 |              3 |

Pick based on what a tie should mean in your result. Two more rules:

- **You can't filter on a window in the same `SELECT`'s `WHERE`.** `WHERE` runs
  before windows are computed. Wrap it in a CTE or subquery and filter outside
  (`WHERE rnk <= 2`).
- **Aggregate first, window second.** Rank products by revenue _after_ `GROUP
BY` has shrunk 30k purchases to a few thousand product rows. The window's
  sort then runs over thousands of rows, not millions.

### Frames: `ROWS` vs `RANGE`

The frame picks which rows around the current one feed the function:

```sql
-- running total: everything from the start of the partition to here
sum(amount) OVER (ORDER BY purchase_date, purchase_id
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- trailing 30 DAYS ending at this row
sum(amount) OVER (ORDER BY julianday(purchase_date)
                  RANGE BETWEEN 29 PRECEDING AND CURRENT ROW)
```

- **`ROWS n PRECEDING`** counts _rows_: "the previous 29 purchases".
- **`RANGE n PRECEDING`** measures distance _in the ORDER BY value_: "purchases
  within 29 days". For that, the `ORDER BY` must be a single **number**, so
  order by `julianday(purchase_date)`, not the ISO text.

Here's customer 1, where the trailing 30-day sum resets whenever purchases are
more than 29 days apart:

| purchase_date | amount | running_total |                          spend_last_30_days |
| :------------ | -----: | ------------: | ------------------------------------------: |
| 2025-06-26    |  91.18 |        490.63 |                                       91.18 |
| 2025-07-23    | 399.76 |        890.39 | **490.94** ← 27 days after the previous row |
| 2025-12-05    | 109.11 |        999.50 |                                      109.11 |

### What windows cost

A window is only as cheap as the rows it has to order. Over one customer (an
index `SEARCH`, a few dozen rows), it takes microseconds. Over the whole fact
table, each customer's largest purchase looks like this:

| Version                                                                            | Plan highlights                                                                       |     Time |
| :--------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ | -------: |
| `row_number() OVER (PARTITION BY customer_id ORDER BY amount DESC)`, then `rn = 1` | `SCAN … USING INDEX idx_purchases_customer` + `TEMP B-TREE FOR LAST TERM OF ORDER BY` | 1,175 ms |
| `GROUP BY customer_id` + `max(amount)`                                             | `SCAN … USING INDEX idx_purchases_customer` (no sort)                                 |   786 ms |
| Same, `FROM purchases NOT INDEXED`                                                 | `SCAN purchases` + `TEMP B-TREE FOR GROUP BY`                                         |   231 ms |
| Same, with index `(customer_id, amount)`                                           | `SCAN … USING COVERING INDEX`                                                         |    36 ms |

Three lessons in that table:

1. A window over the whole table sorts the whole table. That shows up as super-linear
   growth: ×18 time for ×10 data (§2).
2. **Walking a non-covering index in order is often slower than scanning and
   sorting.** 1M random lookups lose to one sequential read plus an in-memory sort.
3. When a whole-table pass is unavoidable, a **covering index in the right
   order** removes both the lookups and the sort. It isn't free: every insert
   now maintains one more B-tree.

The daily 7-day moving average in the script spends almost all of its 766 ms in
the `GROUP BY purchase_date` pass (the same index-walk trap), not in the window.

---

## 7. Gaps and islands

Script: [sql/06_gaps_islands.sql](sql/06_gaps_islands.sql)

"Islands" are runs of consecutive values: days in a row, months in a row, ids
without holes. "Gaps" are the holes between them. The classic trick:

```
n    row_number   n - row_number
1        1             0   ┐
2        2             0   ├ island "0"
3        3             0   ┘
7        4             3   ┐ island "3"
8        5             3   ┘
12       6             6   ┐
13       7             6   │ island "6"
14       8             6   │
15       9             6   ┘
```

Inside a run, the value and its row number both go up by 1, so **their difference
is constant**, and it changes at every gap. `GROUP BY` that difference to get
one row per island: `min` = start, `max` = end, `count` = length.

Applied to real data, consecutive months in which customer 54 bought something:

1. Reduce to **one row per distinct month**. Duplicates break the "+1 per row"
   arithmetic.
2. Turn the month into an integer (`year*12 + month`) so that "consecutive"
   means "+1". For days, `julianday()` does this directly.
3. `m - row_number() OVER (ORDER BY m)` gives the island id. Group by it.

| first_month | last_month | months_in_a_row |
| :---------- | :--------- | --------------: |
| 2025-03     | 2026-02    |              12 |
| 2026-04     | 2026-08    |               5 |
| 2024-11     | 2025-01    |               3 |

**The `LAG` variant** does the same job: flag a row as a new island when
`value - lag(value) > 1`, then a running `sum()` of the flags numbers the
islands. Use it when "consecutive" is looser than +1 (for example, "no more
than 3 days apart").

**Why it scales badly:** for one customer it's an index `SEARCH` plus a few
tiny sorts (<1 ms). For **every** customer at once it's a `DISTINCT` over 1M
rows, then a `PARTITION BY` sort, then three `GROUP BY`s. That's five temp
B-trees stacked over the whole table: **1.5 s**. Count the `TEMP B-TREE` lines
in that plan.

---

## 8. CTEs and multi-level reports

Script: [sql/07_ctes_aggregation.sql](sql/07_ctes_aggregation.sql)

A CTE (`WITH x AS (…)`) **names** a step. It doesn't make anything faster by
itself. For any report query, ask **how many times it reads the big table.**

- **Two CTEs that each read `purchases` means two passes.** Revenue by
  (department, card type) _and_ each department's total, written as two CTEs,
  shows two scans in the plan (1,366 ms). Computing the department total from the
  first CTE's small result with `sum(revenue) OVER (PARTITION BY department)`
  needs one pass (1,021 ms). The saving is the whole second pass, and it grows
  with the table.
- **Inlined vs materialized.** SQLite may inline a CTE into the query that uses
  it (`CO-ROUTINE`) or compute it once into a temp table (`MATERIALIZE`). A CTE
  used more than once is normally materialized, and you can force either with
  `WITH x AS MATERIALIZED (…)` / `AS NOT MATERIALIZED (…)`.
- **No `ROLLUP` / `CUBE` in SQLite.** PostgreSQL has `GROUP BY ROLLUP(...)` and
  `CUBE(...)`. In SQLite, subtotals are `UNION ALL`s of several groupings. Build
  them all from **one materialized fine-grained CTE** (department × year: 66
  rows), not by re-reading 1M rows per level.
- **`HAVING` filters groups** after aggregation. It never reduces the rows that
  had to be read.
- **Make the unavoidable pass cheap.** Revenue per department: 241 ms as a plain
  scan with a sort, versus **35 ms** with a covering index `(department, amount)`
  that's already in `GROUP BY` order.

Look at the plans in this script. Nearly every one says `SCAN pu USING INDEX
idx_purchases_department`, the §2 trap again (the multi-key `GROUP BY` takes
1,273 ms). As an exercise, rerun them with `+pu.department` in the `GROUP BY`,
or `NOT INDEXED`, and compare.

---

## 9. Random sampling

Script: [sql/08_sampling.sql](sql/08_sampling.sql). The examples sample
`customers`.

`ORDER BY random() LIMIT 5` computes a random number for **every** row, sorts
them all, and keeps 5 (`SCAN` + `TEMP B-TREE FOR ORDER BY`). That's the full
cost of the table, on every call, and it grew ×9 from 100k to 1M purchases in §2.

Cheaper approaches use the fact that a rowid seek is O(log n):

| Technique                                                                | Cost     | Caveat                                                                              |
| :----------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------- |
| **Random probe**: `WHERE id >= <random in [1, max]> ORDER BY id LIMIT 1` | One seek | Rows right after a gap in the ids get picked more often                             |
| **N random ids** from a recursive CTE, then `WHERE id IN (…)`            | N seeks  | Missing ids return fewer rows, so ask for a few extra. Duplicates are possible      |
| **Precomputed sample table**, refreshed periodically                     | O(1)     | Not fresh on every call                                                             |
| **Random rows from a _filtered_ set**                                    | Hard     | Random ids mostly miss the filter. Probe repeatedly, or keep a list of eligible ids |

"Random" has a statistical meaning. Say in your write-up which guarantee your
endpoint gives: uniform, approximately uniform, or random-ish.

---

## 10. Anti-joins: "rows with no match"

Script: [sql/09_anti_joins.sql](sql/09_anti_joins.sql)

An anti-join keeps outer rows that have **no** partner in another table. Its
cost is:

> **(number of outer rows) × (cost of proving there's no partner)**

The job is to make that proof a single index seek.

### Three spellings

```sql
-- NOT EXISTS: the clearest statement of intent
WHERE NOT EXISTS (SELECT 1 FROM purchases pu WHERE pu.product_id = pr.product_id)

-- LEFT JOIN … IS NULL
LEFT JOIN purchases pu ON pu.product_id = pr.product_id WHERE pu.purchase_id IS NULL

-- NOT IN: be careful
WHERE product_id NOT IN (SELECT product_id FROM purchases)
```

**The `NOT IN` trap:** if the subquery returns even one `NULL`, `x NOT IN (…)`
is never true, so you silently get zero rows. `SELECT 3 NOT IN (1, 2, NULL)` is
`NULL`, not `1`. Prefer `NOT EXISTS`.

### The probe decides the cost

| Question                                                 | Probe plan                                                                                                                             |   Time |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | -----: |
| Products never sold (5,000 outer rows)                   | `SEARCH pu USING COVERING INDEX idx_purchases_product (product_id=?)`: one seek each                                                   |   6 ms |
| Customers who never bought **Books** (50,000 outer rows) | `SEARCH pu USING INDEX idx_purchases_customer (customer_id=?)`, then reads **every** purchase of that customer to check its department | 451 ms |
| Same, with index `(customer_id, department)`             | `SEARCH … COVERING INDEX (customer_id=? AND department=?)`: one seek each                                                              |  32 ms |

The middle row is where skew hurts. The probe cost for a customer is that
customer's purchase count, and one customer has ~28,000. A composite index
**containing every column the probe tests with `=`** turns each probe back into
one seek.

When the "partner" is several joins away (purchase → customer → zipcode →
state), the probe becomes a join inside `NOT EXISTS`. Read that plan closely:
which table does the probe _start_ from, does every step `SEARCH`, and how many
outer rows multiply it?

---

## 11. Diagnosing a slow endpoint

The procedure for every Phase 3 route:

1. **Get the plan** (`.eqp on`, or `db.explain(...)` in the starter).
2. **Find the line that grows with the table:** `SCAN` of a big table, a
   `TEMP B-TREE` fed by one, `SCAN … USING INDEX` (a whole-index walk with
   lookups), or a `CORRELATED` subquery under a big outer loop.
3. **Measure at two sizes** (100k and 1M). Flat means the cost follows the
   result. ~10× means linear in the table. More than 10× means a sort is
   involved.
4. **Pick a fix category:**

   | Fix                                                    | Examples                                                                                                     |
   | :----------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
   | **Index**: make the access a seek or a covering walk   | composite index for a probe, covering index for a report, `NOCASE` for prefix `LIKE`                         |
   | **Rewrite**: same answer, fewer rows touched           | keyset instead of `OFFSET`, aggregate-then-window, one pass instead of two, `NOT EXISTS` instead of `NOT IN` |
   | **Precompute**: pay at write time instead of read time | FTS5 index, counter table, summary/rollup table, sample table                                                |
   | **Change the contract**: answer a cheaper question     | "1,000+" instead of an exact total, next-page only, "random-ish"                                             |
   | **Accept it**: some reports are inherently O(table)    | Run it off the request path, cache it, or move it to a different system                                      |

5. **Write the diagnosis.** A good one-paragraph diagnosis has four parts:
   - **what** the plan does ("scans all 1M purchases and sorts them by…"),
   - **why** that's the plan ("no index provides this order; the filter can't
     seek because…"),
   - **the evidence**: the plan lines, plus times at two sizes,
   - **the fix**, and what it costs in index size, write speed or freshness.

   Every fix in the table above has a cost somewhere, usually in write
   performance, and that connects directly to Phase 4.

Measuring from Python: `sqlite3`'s `cursor.execute()` returns once the **first**
row is ready. Time `execute(...)` **plus** `fetchall()` with
`time.perf_counter()`, or a slow query will look fast.

---

## 12. Where each Phase 3 route fits

| Phase 3 route                 | Read                                                                                       |
| :---------------------------- | :----------------------------------------------------------------------------------------- |
| `GET /purchases?offset=`      | §3 Pagination (and §2 for reading the plan)                                                |
| `GET /products/search?q=`     | §4 Search: `LIKE` rules, FTS5, tokens vs substrings, sync triggers                         |
| `GET /purchases?…&total=true` | §5 Counting                                                                                |
| `GET /customers/leaderboard`  | §6 Window functions: frames (`RANGE` + `julianday`), aggregate first, whole-table cost     |
| `GET /customers/{id}/streaks` | §7 Gaps and islands (days instead of months; one customer vs. all)                         |
| `GET /reports/cube`           | §8 CTEs: counting passes, no `CUBE` in SQLite, the department-index trap, covering indexes |
| `GET /purchases/sample`       | §9 Random sampling                                                                         |
| `GET /products/dead?state=`   | §10 Anti-joins: probe cost, composite indexes, multi-join probes                           |

For your two original endpoints, pick a shape from this lecture that none of
the eight exercises. Some candidates: a correlated subquery under a big outer
loop, `SELECT DISTINCT` over a big join, `GROUP BY` on an expression, or a `LIKE`
on a `COLLATE NOCASE` index versus a `BINARY` one.
