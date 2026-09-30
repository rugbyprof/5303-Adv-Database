<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture06_multi_cte
name: SubLecture06_multi_cte
title: "Multi-CTE Revenue Reporting by State, Department, and Month"
description: ""
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>


# Multi-CTE Revenue Reporting by State, Department, and Month

Complex reporting queries are easier to understand when they are built as a sequence of named stages. A **common table expression** (CTE) gives each stage a name, allowing the query to read more like a data pipeline than a heroic paragraph of SQL.

This example calculates purchase revenue grouped by:

```text
(buyer state, product department, calendar month)
```

It also demonstrates the different jobs of `WHERE` and `HAVING`:

- `WHERE` filters **rows** before a stage aggregates them.
- `HAVING` filters **groups** after that stage has aggregated them.

## Assumed purchase schema

The query uses these simplified tables:

```text
purchases
  id, buyer_id, product_id, purchased_at, amount, status

buyers
  id, state

products
  id, department
```

`purchases.amount` is assumed to be the revenue amount for one purchase. In a system with order headers and line items, the base CTE would normally join to purchase lines and calculate an amount such as `quantity * unit_price` instead.

## The complete multi-CTE query

```sql
WITH
-- Stage 1: retain only purchase rows that can contribute to the report.
base_purchases AS (
  SELECT
    b.state,
    pr.department,
    date(p.purchased_at, 'start of month') AS revenue_month,
    p.id AS purchase_id,
    p.amount
  FROM purchases AS p
  JOIN buyers AS b
    ON b.id = p.buyer_id
  JOIN products AS pr
    ON pr.id = p.product_id
  WHERE p.status = 'completed'
    AND p.purchased_at >= '2026-01-01'
    AND p.purchased_at <  '2027-01-01'
    AND p.amount > 0
    AND b.state IS NOT NULL
    AND pr.department IS NOT NULL
),

-- Stage 2: aggregate individual purchases to the requested reporting grain.
monthly_department_revenue AS (
  SELECT
    state,
    department,
    revenue_month,
    COUNT(*) AS purchase_count,
    SUM(amount) AS revenue
  FROM base_purchases
  GROUP BY state, department, revenue_month
  HAVING COUNT(*) >= 10
     AND SUM(amount) >= 1000.00
),

-- Stage 3: apply a row-level business rule to the already-aggregated rows.
reporting_rows AS (
  SELECT
    state,
    department,
    revenue_month,
    purchase_count,
    revenue
  FROM monthly_department_revenue
  WHERE state IN ('IL', 'MN', 'WI')
    AND department <> 'Internal Test'
),

-- Stage 4: calculate each state's total revenue for each reporting month.
state_month_totals AS (
  SELECT
    state,
    revenue_month,
    SUM(revenue) AS state_month_revenue
  FROM reporting_rows
  GROUP BY state, revenue_month
  HAVING SUM(revenue) >= 5000.00
)

SELECT
  r.state,
  r.department,
  r.revenue_month,
  r.purchase_count,
  r.revenue,
  s.state_month_revenue,
  ROUND(100.0 * r.revenue / s.state_month_revenue, 1) AS percent_of_state_month_revenue
FROM reporting_rows AS r
JOIN state_month_totals AS s
  ON s.state = r.state
 AND s.revenue_month = r.revenue_month
ORDER BY
  r.revenue_month,
  r.state,
  r.revenue DESC,
  r.department;
```

## Reading the pipeline

```text
raw purchases
     |
     | WHERE: completed, date range, positive amount, valid dimensions
     v
base_purchases
     |
     | GROUP BY state, department, month
     | HAVING: at least 10 purchases and $1,000 revenue
     v
monthly_department_revenue
     |
     | WHERE: included states and non-test departments
     v
reporting_rows
     |
     | GROUP BY state, month
     | HAVING: state-month has at least $5,000 revenue
     v
state_month_totals
     |
     | JOIN the totals back to detailed reporting rows
     v
final report
```

Each CTE has a distinct grain:

| CTE                          | One row represents                              |
| ---------------------------- | ----------------------------------------------- |
| `base_purchases`             | One qualifying purchase                         |
| `monthly_department_revenue` | One `(state, department, month)` group          |
| `reporting_rows`             | One retained `(state, department, month)` group |
| `state_month_totals`         | One `(state, month)` group                      |

Keeping the grain explicit prevents accidental double counting when CTEs are joined together later.

## Stage 1: `WHERE` filters raw purchase rows

The first CTE uses `WHERE`:

```sql
WHERE p.status = 'completed'
  AND p.purchased_at >= '2026-01-01'
  AND p.purchased_at <  '2027-01-01'
  AND p.amount > 0
```

These predicates ask questions about an individual purchase row:

```text
Is this purchase completed?
Is this purchase in the reporting period?
Is its amount positive?
```

Rows that fail are removed **before** the `GROUP BY`. That is both semantically correct and usually more efficient because later aggregation sees fewer rows.

The half-open date range is intentional:

```text
inclusive start:  2026-01-01
exclusive end:    2027-01-01
```

It safely includes any timestamp during 2026, including `2026-12-31 23:59:59.999...`, without guessing the last possible fractional second.

## Stage 2: `HAVING` filters aggregate groups

The second CTE groups purchases by the reporting dimensions:

```sql
GROUP BY state, department, revenue_month
HAVING COUNT(*) >= 10
   AND SUM(amount) >= 1000.00
```

At this point, the query is no longer looking at one purchase row. It is looking at a group such as:

```text
state   department   month        purchases   revenue
-----   ----------   ----------   ---------   -------
IL      Electronics  2026-04-01       14      1830.00
```

The filter asks aggregate questions:

```text
Does this state-department-month group have at least 10 purchases?
Did it generate at least $1,000 in revenue?
```

Those questions require `HAVING` because `COUNT(*)` and `SUM(amount)` do not exist until after aggregation.

This would be invalid or conceptually wrong in a `WHERE` clause in the same query block:

```sql
-- Not valid in this aggregation stage:
WHERE SUM(amount) >= 1000.00
```

## Stage 3: `WHERE` can filter rows produced by an earlier CTE

After `monthly_department_revenue`, each result row already represents a complete `(state, department, month)` group. Therefore, this is again a row-level filter:

```sql
FROM monthly_department_revenue
WHERE state IN ('IL', 'MN', 'WI')
  AND department <> 'Internal Test'
```

It is structurally a different stage from the first `WHERE`, but the rule is the same: `WHERE` filters the rows that enter the current query block.

```text
In base_purchases, a row is one purchase.
In reporting_rows, a row is one state-department-month summary.

WHERE always filters rows; the meaning of “a row” depends on the stage.
```

This is why multi-CTE queries are useful. They let a report apply filters at the exact grain where the business rule makes sense.

## Stage 4: a second `HAVING` at a coarser grain

The `state_month_totals` CTE groups again, this time by just `(state, month)`:

```sql
GROUP BY state, revenue_month
HAVING SUM(revenue) >= 5000.00
```

This removes entire state-months that do not meet the report's overall revenue threshold. Joining the qualifying totals back to `reporting_rows` retains the individual department rows only for qualifying state-months.

```text
Before stage 4

IL, 2026-04: Electronics $1,830; Home $2,100; Outdoors $1,500
              total = $5,430  → retained

MN, 2026-04: Electronics $1,200; Home $1,100
              total = $2,300  → removed
```

This is a structural filter: it is applied at the `(state, month)` level, not at the raw-purchase or individual-department level.

## Why not put every condition in one `HAVING` clause?

It is technically possible to place some non-aggregate conditions in `HAVING`, but it is usually less clear and can limit optimization opportunities:

```sql
-- Works in some databases, but is not the clearest design.
GROUP BY state, department, revenue_month
HAVING state IN ('IL', 'MN', 'WI')
   AND SUM(amount) >= 1000.00
```

When a condition can be evaluated before aggregation, put it in `WHERE`. Use `HAVING` for conditions that depend on an aggregate at the current stage.

```text
Filter individual purchase rows?          WHERE
Filter aggregated groups in this stage?   HAVING
Filter a prior CTE's result rows?         WHERE in a later CTE
```

## Indexes for the base stage

The most expensive work often happens in `base_purchases`: filtering purchases and joining dimensions. A useful starting point for this report shape is:

```sql
CREATE INDEX idx_purchases_status_date
ON purchases(status, purchased_at);
```

This can help SQLite locate completed purchases inside the date range. If the query commonly reports a fixed state or a particular department, the best indexes may differ, and the joins and data distribution matter.

Use `EXPLAIN QUERY PLAN` with representative data:

```sql
EXPLAIN QUERY PLAN
WITH base_purchases AS (
  SELECT
    b.state,
    pr.department,
    date(p.purchased_at, 'start of month') AS revenue_month,
    p.amount
  FROM purchases AS p
  JOIN buyers AS b ON b.id = p.buyer_id
  JOIN products AS pr ON pr.id = p.product_id
  WHERE p.status = 'completed'
    AND p.purchased_at >= '2026-01-01'
    AND p.purchased_at <  '2027-01-01'
)
SELECT state, department, revenue_month, SUM(amount)
FROM base_purchases
GROUP BY state, department, revenue_month;
```

The report must still aggregate qualifying rows. An index can reduce how many rows it reads before aggregation; it cannot eliminate the need to calculate the requested revenue totals.

## Summary

> **Use `WHERE` to decide which rows enter a stage; use `HAVING` to decide which groups survive that stage.**

CTEs make those stages visible. In this report, purchases are first filtered, then summarized by `(state, department, month)`, then structurally filtered at both the department-month and state-month levels. That separation makes the logic easier to test, explain, and change without turning the query into an archaeological dig.
