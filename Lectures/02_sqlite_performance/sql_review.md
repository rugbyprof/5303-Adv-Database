# SQL Review — Warm-up for the Performance Lecture

This is a quick refresher for students who have already taken an intro SQL course.
It is not a tutorial. Each section reminds you of one piece of SQL you will need
to read [queries.sql](queries.sql), using the same `perf.db` database. The output
shown below each query is real output from that database.

If a section feels new rather than familiar, go back to
[01_terms_concepts_intro/sql_basics.md](../01_terms_concepts_intro/sql_basics.md).

```bash
cd Lectures/02_sqlite_performance
sqlite3 perf.db
sqlite> .mode box
sqlite> .timer on
```

---

## 0. The database

This is a small store schema that has been scaled up to a million purchases.

```text
states ──< zipcodes ──< customers ──< cards >── card_types
                            │           │
                            └──< purchases >── products
                                    │
                                    └──> departments
```

| Table | Rows | Key | Notes |
| :--- | ---: | :--- | :--- |
| `customers` | 50,000 | `customer_id` | `email` is `UNIQUE`; `zipcode` → `zipcodes` |
| `cards` | 74,945 | `card_id` | Each card belongs to one customer and has one `card_type` |
| `products` | 5,000 | `product_id` | `unit_price` is between 0.80 and 399.98 |
| `purchases` | 1,000,000 | `purchase_id` | The **fact table**. Dates run from `2024-01-01` to `2026-08-31` |
| `zipcodes` / `states` | 700 / 51 | natural keys | These are lookup tables |
| `departments` / `card_types` | 22 / 13 | natural keys | These are lookup tables |

There is also a view called `purchase_details` that joins all of these tables
into one wide row per purchase.

Look around with these commands:

```sql
.tables
.schema purchases
SELECT * FROM purchases LIMIT 3;
```

```text
┌─────────────┬─────────────┬─────────┬────────────┬────────────┬────────┬───────────────┐
│ purchase_id │ customer_id │ card_id │ product_id │ department │ amount │ purchase_date │
├─────────────┼─────────────┼─────────┼────────────┼────────────┼────────┼───────────────┤
│ 1           │ 11086       │ 16629   │ 3109       │ Beauty     │ 362.83 │ 2024-09-23    │
│ 2           │ 26461       │ 39623   │ 2756       │ Grocery    │ 37.96  │ 2026-02-20    │
│ 3           │ 14108       │ 21180   │ 3295       │ Grocery    │ 133.75 │ 2024-10-03    │
└─────────────┴─────────────┴─────────┴────────────┴────────────┴────────┴───────────────┘
```

> SQLite has no separate `DATE` type. Dates are stored as ISO-8601 text
> (`YYYY-MM-DD`). In that format, sorting the text also sorts the dates, so
> `>=`, `BETWEEN` and `ORDER BY` all work as expected.

---

## 1. `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`

```sql
SELECT product_id, product_name, unit_price
FROM products
WHERE unit_price >= 399.5
ORDER BY unit_price DESC
LIMIT 5;
```

```text
┌────────────┬────────────────────────┬────────────┐
│ product_id │      product_name      │ unit_price │
├────────────┼────────────────────────┼────────────┤
│ 2358       │ Smart Bottle 2357      │ 399.98     │
│ 3130       │ Stainless Tripod 3129  │ 399.95     │
│ 398        │ Premium Lamp 397       │ 399.9      │
│ 4143       │ Insulated Lamp 4142    │ 399.87     │
│ 3722       │ Insulated Skillet 3721 │ 399.82     │
└────────────┴────────────────────────┴────────────┘
```

- `LIMIT n OFFSET k` skips `k` rows and then returns `n`. This is the usual way
  to page through results, and [queries.sql §02](queries.sql) shows why it gets
  slow on later pages.
- If you use `LIMIT` without `ORDER BY`, SQL does not promise which rows you get.

---

## 2. Filtering: `IN`, `BETWEEN`, `LIKE`, `AND`/`OR`

```sql
SELECT purchase_id, department, amount, purchase_date
FROM purchases
WHERE department IN ('Books', 'Music')
  AND purchase_date BETWEEN '2026-08-01' AND '2026-08-31'
  AND amount >= 390
ORDER BY amount DESC
LIMIT 5;
```

```text
┌─────────────┬────────────┬────────┬───────────────┐
│ purchase_id │ department │ amount │ purchase_date │
├─────────────┼────────────┼────────┼───────────────┤
│ 441515      │ Books      │ 399.9  │ 2026-08-07    │
│ 558198      │ Books      │ 399.9  │ 2026-08-12    │
│ 254558      │ Books      │ 399.69 │ 2026-08-29    │
│ 92994       │ Books      │ 399.53 │ 2026-08-27    │
│ 846007      │ Books      │ 399.34 │ 2026-08-16    │
└─────────────┴────────────┴────────┴───────────────┘
```

```sql
SELECT customer_id, first_name, last_name
FROM customers
WHERE last_name LIKE 'Knu%'      -- % = any run of characters, _ = exactly one
LIMIT 5;
```

- `BETWEEN a AND b` includes both ends.
- `AND` is evaluated before `OR`. When you mix them, add parentheses.
- In SQLite, `LIKE` ignores case for ASCII letters. `GLOB` is case-sensitive
  and uses `*` and `?` as wildcards. Whether `LIKE` can use an index is covered
  in [queries.sql §03](queries.sql).

---

## 3. Aggregates, `GROUP BY`, `HAVING`

Aggregates collapse many rows into one:

```sql
SELECT count(*)              AS n,
       round(sum(amount), 2) AS total,
       round(avg(amount), 2) AS avg_amt,
       min(amount), max(amount)
FROM purchases
WHERE purchase_date >= '2026-08-01';
```

```text
┌───────┬────────────┬─────────┬─────────────┬─────────────┐
│   n   │   total    │ avg_amt │ min(amount) │ max(amount) │
├───────┼────────────┼─────────┼─────────────┼─────────────┤
│ 31653 │ 6172698.18 │ 195.01  │ 0.8         │ 399.98      │
└───────┴────────────┴─────────┴─────────────┴─────────────┘
```

`GROUP BY` gives you one output row per group. `WHERE` filters **rows** before
they are grouped. `HAVING` filters **groups** after they are formed:

```sql
SELECT department, count(*) AS n, round(sum(amount), 2) AS revenue
FROM purchases
WHERE purchase_date >= '2026-08-01'      -- row filter
GROUP BY department
HAVING count(*) >= 1450                  -- group filter
ORDER BY revenue DESC;
```

```text
┌────────────┬──────┬───────────┐
│ department │  n   │  revenue  │
├────────────┼──────┼───────────┤
│ Outdoors   │ 1539 │ 300536.37 │
│ Automotive │ 1503 │ 295663.32 │
│ Home       │ 1459 │ 290077.0  │
│ Industrial │ 1468 │ 289277.98 │
│ Books      │ 1459 │ 288719.74 │
│ Garden     │ 1456 │ 288385.12 │
│ Jewelry    │ 1460 │ 274905.72 │
└────────────┴──────┴───────────┘
```

You can group by several columns, and each distinct combination becomes one row:

```sql
SELECT customer_id, card_type, count(*)
FROM cards
WHERE customer_id <= 3
GROUP BY customer_id, card_type;
```

**Logical order of evaluation.** This order explains most "column not found"
errors:

```text
FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

Because `WHERE` runs before `SELECT`, it cannot see an alias defined in
`SELECT`. `ORDER BY` runs after `SELECT`, so it can. SQLite is lenient here and
also lets `HAVING` and `GROUP BY` use aliases, but PostgreSQL is stricter, so
don't depend on it.

---

## 4. Inner joins

A join matches rows from two tables using a condition, which is usually
foreign key = primary key:

```sql
SELECT pu.purchase_date, pr.product_name, pu.amount
FROM purchases pu
JOIN products  pr ON pr.product_id = pu.product_id
WHERE pu.customer_id = 54
ORDER BY pu.purchase_date DESC
LIMIT 5;
```

```text
┌───────────────┬───────────────────────┬────────┐
│ purchase_date │     product_name      │ amount │
├───────────────┼───────────────────────┼────────┤
│ 2026-08-30    │ Premium Notebook 3729 │ 357.94 │
│ 2026-07-12    │ Ceramic Blender 3771  │ 375.34 │
│ 2026-07-01    │ Stainless Bottle 3663 │ 321.39 │
│ 2026-06-11    │ Deluxe Scooter 687    │ 164.29 │
│ 2026-05-31    │ Bamboo Lamp 1717      │ 313.83 │
└───────────────┴───────────────────────┴────────┘
```

A join combined with a group, for example counting customers per state
(customer → zipcode → state):

```sql
SELECT z.state_code, count(*) AS customers
FROM customers c
JOIN zipcodes  z ON z.zipcode = c.zipcode
GROUP BY z.state_code
ORDER BY customers DESC
LIMIT 5;
```

- The short names `pu`, `pr` and `c` are **table aliases**. When the same
  column name exists in two tables, you have to qualify it (`pu.product_id`).
- `JOIN ... USING (customer_id)` is shorthand for `ON a.customer_id = b.customer_id`
  when the column has the same name on both sides.
- A **view** is a saved query. `purchase_details` contains a 6-way join, so the
  query below is shorter to write but does the same work:

```sql
SELECT customer_name, state_code, product_name, amount, card_type
FROM purchase_details
WHERE purchase_id = 500000;
```

---

## 5. Outer joins and "rows with no match"

An inner join drops rows that have no partner. `LEFT JOIN` keeps every row from
the left table and fills in `NULL` where there is no match. That makes it the
standard tool for questions like "who never did X?":

```sql
-- Customers who have never made a purchase
SELECT count(*) AS no_purchase
FROM customers c
LEFT JOIN purchases pu ON pu.customer_id = c.customer_id
WHERE pu.purchase_id IS NULL;                         -- 5003
```

You can ask the same question with `NOT EXISTS`, and many people find it easier
to read:

```sql
-- Products that have never been sold
SELECT count(*)
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM purchases pu WHERE pu.product_id = p.product_id);   -- 1500
```

A third way is `NOT IN (subquery)`. It has a trap: if the subquery returns
even one `NULL`, the whole test returns no rows (see §8). Both the cost and the
trap are covered in [queries.sql §09](queries.sql).

---

## 6. Subqueries and CTEs

A **scalar subquery** returns one value that you can use like a constant:

```sql
SELECT product_id, product_name, unit_price
FROM products
WHERE unit_price > (SELECT avg(unit_price) FROM products)   -- 199.91
ORDER BY unit_price
LIMIT 3;
```

A **correlated** subquery refers to the outer row, so it runs once for each
outer row. Keep an eye on these, because [queries.sql §01](queries.sql) shows
what they cost:

```sql
SELECT pr.product_id,
       (SELECT count(*) FROM purchases pu WHERE pu.product_id = pr.product_id) AS times_sold
FROM products pr
WHERE pr.product_id <= 5;
```

A **CTE** (`WITH ...`) gives a subquery a name so the main query can read top
to bottom. For example, "aggregate first, then join":

```sql
WITH cust_totals AS (
    SELECT customer_id, count(*) AS n, sum(amount) AS spent
    FROM purchases
    WHERE purchase_date >= '2026-08-01'
    GROUP BY customer_id
)
SELECT c.customer_id, c.first_name, c.last_name, ct.n, round(ct.spent, 2) AS spent
FROM cust_totals ct
JOIN customers c USING (customer_id)
ORDER BY ct.spent DESC
LIMIT 5;
```

```text
┌─────────────┬────────────┬───────────┬─────┬───────────┐
│ customer_id │ first_name │ last_name │  n  │   spent   │
├─────────────┼────────────┼───────────┼─────┼───────────┤
│ 20912       │ Leslie     │ Hamilton  │ 878 │ 176635.87 │
│ 45070       │ Dennis     │ Dijkstra  │ 222 │ 44533.06  │
│ 19013       │ Edsger     │ Rossum    │ 163 │ 30304.09  │
│ 979         │ Barbara    │ Ritchie   │ 111 │ 24222.35  │
│ 40146       │ Dennis     │ Hamilton  │ 114 │ 21591.99  │
└─────────────┴────────────┴───────────┴─────┴───────────┘
```

(The data is deliberately skewed, so a few customers buy far more than
everyone else.)

`WITH RECURSIVE` lets a CTE refer to itself, which is useful for generating a
series of values. It appears in [queries.sql §08](queries.sql).

---

## 7. Window functions (a preview)

`GROUP BY` collapses rows. A window function computes across related rows
**but keeps every row**. `OVER (...)` defines which rows are "related":

```sql
SELECT purchase_date, amount,
       round(sum(amount) OVER (ORDER BY purchase_date, purchase_id), 2) AS running_total
FROM purchases
WHERE customer_id = 54
ORDER BY purchase_date, purchase_id
LIMIT 5;
```

```text
┌───────────────┬────────┬───────────────┐
│ purchase_date │ amount │ running_total │
├───────────────┼────────┼───────────────┤
│ 2024-01-22    │ 298.4  │ 298.4         │
│ 2024-03-14    │ 336.96 │ 635.36        │
│ 2024-03-19    │ 121.55 │ 756.91        │
│ 2024-06-14    │ 27.85  │ 784.76        │
│ 2024-08-04    │ 162.83 │ 947.59        │
└───────────────┴────────┴───────────────┘
```

- `PARTITION BY x` restarts the calculation for each value of `x`. It works
  like `GROUP BY`, except the rows are not collapsed.
- `row_number()`, `rank()`, `dense_rank()`, `lag()` and `lead()` only make
  sense with `OVER`.
- Frames (`ROWS BETWEEN ...`), ranking ties, and what windows cost at 1M rows
  are covered in [queries.sql §05–06](queries.sql).

---

## 8. `NULL` cheat sheet

`NULL` means "unknown", so any comparison with it is also unknown, and `WHERE`
only keeps rows where the condition is true.

```sql
SELECT NULL = NULL, NULL IS NULL, 1 IN (1, NULL), 2 NOT IN (1, NULL);
--       NULL           1              1               NULL   ← the NOT IN trap
```

| Want | Write | Not |
| :--- | :--- | :--- |
| Test for missing | `x IS NULL` | `x = NULL` |
| Count rows | `count(*)` | `count(col)`, which skips NULLs |
| Default a value | `coalesce(x, 0)` | |
| "Not in this list" | `NOT EXISTS (...)` | `NOT IN (subquery)` when the subquery column can be NULL |

---

## 9. One new tool: `EXPLAIN QUERY PLAN`

This is where the review ends and the lecture begins. Put `EXPLAIN QUERY PLAN`
in front of any query and SQLite tells you **how** it will run the query
instead of running it:

```sql
EXPLAIN QUERY PLAN SELECT * FROM purchases WHERE purchase_id = 500000;
-- SEARCH purchases USING INTEGER PRIMARY KEY (rowid=?)     ← jumps straight to 1 row

EXPLAIN QUERY PLAN SELECT count(*) FROM purchases WHERE amount > 395;
-- SCAN purchases                                            ← reads all 1,000,000 rows
```

In the `sqlite3` shell, `.eqp on` prints the plan for every query
automatically. That is how every section of `queries.sql` starts.

**Rule of thumb:** `SEARCH` means SQLite used an index to jump to the rows it
needs. `SCAN` means it read the whole table. `USE TEMP B-TREE` means it had to
sort. On a table with a million rows, these differences are what separate a
query that answers instantly from one that takes seconds.

---

## 10. SQL Query Progression

The following examples solve essentially the same problem:

> **Find the top 5 customers by total purchases since August 1, 2026.**

We will solve the problem four different ways:

>```text
>1. JOIN + GROUP BY
>        ↓
>2. Derived-Table Subquery
>        ↓
>3. Common Table Expression (CTE)
>        ↓
>4. Correlated Subquery
>```

---

### A. JOIN + GROUP BY

The most direct approach is to join the tables and perform the aggregation in the main query.

```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(*) AS n,
    ROUND(SUM(p.amount), 2) AS spent
FROM customers c
JOIN purchases p USING (customer_id)
WHERE p.purchase_date >= '2026-08-01'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY SUM(p.amount) DESC
LIMIT 5;
```

> Idea

>```text
>customers + purchases
 >       ↓
 >      JOIN
 >       ↓
 >     filter
 >       ↓
 >    GROUP BY
 >       ↓
 >   aggregate
>```

This is often the simplest solution when the aggregation can be performed directly on the joined data.

---

### B. Derived-Table Subquery

We can perform the aggregation **first** inside a subquery.

```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    ct.n,
    ROUND(ct.spent, 2) AS spent
FROM customers c
JOIN (
    SELECT
        customer_id,
        COUNT(*) AS n,
        SUM(amount) AS spent
    FROM purchases
    WHERE purchase_date >= '2026-08-01'
    GROUP BY customer_id
) AS ct
USING (customer_id)
ORDER BY ct.spent DESC
LIMIT 5;
```

#### Idea

The inner query creates a temporary result:

```text
customer_id | n | spent
------------+---+--------
101         | 8 | 425.50
102         | 3 | 217.25
103         | 9 | 812.75
```

The outer query then joins that result with `customers`.

>```text
>purchases
>    ↓
> subquery
>    ↓
>cust_totals
>    ↓
>JOIN customers
>```

---

### C. Common Table Expression (CTE)

A CTE pulls the subquery out of the `FROM` clause and gives it a name.

```sql
WITH cust_totals AS (
    SELECT
        customer_id,
        COUNT(*) AS n,
        SUM(amount) AS spent
    FROM purchases
    WHERE purchase_date >= '2026-08-01'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    ct.n,
    ROUND(ct.spent, 2) AS spent
FROM cust_totals ct
JOIN customers c USING (customer_id)
ORDER BY ct.spent DESC
LIMIT 5;
```

> #### Idea
>```text
>WITH cust_totals AS (...)
>           ↓
>     named result
>           ↓
>    main SELECT
>```

Conceptually, this is very similar to the derived-table solution:

```sql
FROM (
    SELECT ...
) AS cust_totals
```

becomes:

```sql
WITH cust_totals AS (
    SELECT ...
)
```

CTEs can make larger queries easier to read because intermediate results have meaningful names.

---

### D. Correlated Subquery

A correlated subquery references the row currently being processed by the outer query.

```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,

    (
        SELECT COUNT(*)
        FROM purchases p
        WHERE p.customer_id = c.customer_id
          AND p.purchase_date >= '2026-08-01'
    ) AS n,

    (
        SELECT ROUND(SUM(p.amount), 2)
        FROM purchases p
        WHERE p.customer_id = c.customer_id
          AND p.purchase_date >= '2026-08-01'
    ) AS spent

FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM purchases p
    WHERE p.customer_id = c.customer_id
      AND p.purchase_date >= '2026-08-01'
)
ORDER BY spent DESC
LIMIT 5;
```

The important relationship is:

```sql
p.customer_id = c.customer_id
```

The inner query depends on the **current customer** from the outer query.

Conceptually:

```text
FOR EACH customer
        ↓
run a related subquery
        ↓
find that customer's purchases
        ↓
calculate results
```

---

# Comparison

| Approach | Main Idea |
|---|---|
| `JOIN + GROUP BY` | Join the data and aggregate directly |
| Derived Table | Build an intermediate result inside `FROM` |
| CTE | Build a **named** intermediate result |
| Correlated Subquery | Run a related query using values from the current outer row |

A useful progression is:

```text
JOIN + GROUP BY
      │
      │ "Let's separate the aggregation."
      ▼
Derived Table
      │
      │ "Let's give that result a name."
      ▼
     CTE
      │
      │ "What if the inner query depends on each outer row?"
      ▼
Correlated Subquery
```

The goal is not to memorize four ways to write the same query. The goal is to recognize that SQL gives us several ways to **decompose a larger question into smaller questions**.


## Where each topic shows up in `queries.sql`

| Review topic | Used in |
| :--- | :--- |
| `WHERE`, `ORDER BY`, `LIMIT` | §01 reading plans, §02 pagination |
| `LIKE` | §03 full-text search |
| `count(*)`, `GROUP BY`, `HAVING` | §04 counting, §07 CTEs and aggregation |
| Joins, views | Throughout the file |
| `LEFT JOIN … IS NULL`, `NOT EXISTS`, `NOT IN` | §09 anti-joins |
| Subqueries, CTEs, `WITH RECURSIVE` | §01, §07, §08 sampling |
| Window functions | §05 window functions, §06 gaps and islands |
| `EXPLAIN QUERY PLAN` | Every section |

## Quick self-check

Write these without looking back. Each one takes a few lines.

1. Find the 3 customers with the most cards. Show their names and card counts.
2. Find total revenue per year. (Hint: `strftime('%Y', purchase_date)`.)
3. Find the departments where the average purchase in July 2026 was above $200.
4. Find customers in Texas (`TX`) who have never bought anything from `Books`.
5. For customer 54, show each purchase alongside the amount of the *previous*
   purchase. (Hint: `lag()`.)
