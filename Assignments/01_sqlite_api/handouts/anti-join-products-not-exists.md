<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture08_anti_join
name: SubLecture08_anti_join
title: "Anti-Joins: Products Never Purchased in a State"
description: ""
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Anti-Joins: Products Never Purchased in a State

An anti-join returns rows for which no related row exists. This handout uses the familiar purchases theme to find products that have never been purchased by a buyer in a selected state. It compares a direct `NOT EXISTS` expression with a set-based rewrite, then shows why indexing direction and query plans matter.

## Scenario and schema

An online store wants a list of products that have **never been purchased by a buyer in a chosen state**. The report should consider only completed purchases.

```text
products
  id, product_name, department

buyers
  id, state

purchases
  id, buyer_id, product_id, status, purchased_at, amount
```

For this worksheet, `:state` is a parameter such as `'IL'`.

```text
Wanted: product rows that have no matching completed purchase
        made by a buyer whose state is :state.
```

## What is an anti-join?

An ordinary join finds matches:

```text
products that have a qualifying purchase in Illinois
```

An **anti-join** finds rows for which no match exists:

```text
products that do not have a qualifying purchase in Illinois
```

```text
All products                         Products purchased in IL

[A][B][C][D][E][F]                  [B][D][F]
       anti-join result
             ↓
          [A][C][E]
```

SQL has no universal `ANTI JOIN` keyword, but `NOT EXISTS` and `LEFT JOIN ... IS NULL` are common ways to express the idea.

## The direct `NOT EXISTS` query

Here is the direct formulation:

```sql
SELECT
  pr.id,
  pr.product_name,
  pr.department
FROM products AS pr
WHERE NOT EXISTS (
  SELECT 1
  FROM purchases AS p
  JOIN buyers AS b
    ON b.id = p.buyer_id
  WHERE p.product_id = pr.id
    AND p.status = 'completed'
    AND b.state = :state
)
ORDER BY pr.product_name;
```

Read the inner query for one product:

```text
“Can the database find at least one completed purchase of this product
 made by a buyer in the requested state?”

Yes → exclude the product.
No  → return the product.
```

`EXISTS` can stop after the first matching purchase. That is helpful. It does not help much if the database must search a very large purchase history to discover that no match exists.

## Why the direct form can be slow

The condition `p.product_id = pr.id` refers to the outer `products` row. That makes this a **correlated subquery**: the inner query is logically evaluated in the context of each product.

Without suitable indexes, the conceptual work can look like this:

```text
for each product
    scan many purchases
    join each candidate purchase to its buyer
    check whether the buyer is in :state and the purchase is completed
```

```text
products                         large purchases table

product A  ──► scan/check ──► [purchase][purchase][purchase] ...
product B  ──► scan/check ──► [purchase][purchase][purchase] ...
product C  ──► scan/check ──► [purchase][purchase][purchase] ...
```

Inspect the actual plan:

```sql
EXPLAIN QUERY PLAN
SELECT pr.id, pr.product_name
FROM products AS pr
WHERE NOT EXISTS (
  SELECT 1
  FROM purchases AS p
  JOIN buyers AS b ON b.id = p.buyer_id
  WHERE p.product_id = pr.id
    AND p.status = 'completed'
    AND b.state = :state
);
```

Poor-plan clues may include output resembling:

```text
SCAN pr
CORRELATED SCALAR SUBQUERY
SCAN p
SEARCH b USING INTEGER PRIMARY KEY (rowid=?)
```

The exact wording varies by SQLite version. A correlated plan is not automatically bad: with an appropriate index, a small per-product existence lookup can be efficient. The problem is the combination of a large outer product set, a large child purchase table, and no efficient path into the relevant child rows.

`EXISTS` can stop after finding one match, but without a useful index the database may still scan many purchase rows for each product before it finds a match—or proves no match exists.

## Indexing the correlated lookup

If the `NOT EXISTS` form remains the best expression of the business rule, index the purchase table for the inner lookup:

```sql
CREATE INDEX idx_purchases_product_status_buyer
ON purchases(product_id, status, buyer_id);
```

This lets SQLite begin with the outer product ID, restrict to completed purchases, and obtain the buyer IDs needed for the join.

```text
For product 417:

index (product_id, status, buyer_id)
    ↓ seek to (417, 'completed', ...)
    ↓ examine only that product's completed purchases
    ↓ look up each buyer and test state
```

The buyer table's primary key already supports `b.id = p.buyer_id`. If state filtering is frequently used to start from buyers, this index is also useful:

```sql
CREATE INDEX idx_buyers_state_id
ON buyers(state, id);
```

Indexes are not decorations for queries; they are access paths. The index order should reflect where the query starts.

## A set-based rewrite: build the excluded set once

Another approach begins with buyers in the chosen state, finds the products they have purchased, and creates the exclusion set **once**:

```sql
WITH purchased_product_ids_in_state AS (
  SELECT DISTINCT
    p.product_id
  FROM buyers AS b
  JOIN purchases AS p
    ON p.buyer_id = b.id
  WHERE b.state = :state
    AND p.status = 'completed'
)
SELECT
  pr.id,
  pr.product_name,
  pr.department
FROM products AS pr
LEFT JOIN purchased_product_ids_in_state AS purchased
  ON purchased.product_id = pr.id
WHERE purchased.product_id IS NULL
ORDER BY pr.product_name;
```

```text
buyers in :state
      |
      | join only their completed purchases
      v
distinct purchased product IDs
      |
      | anti-join against all products
      v
products never purchased in :state
```

The CTE contains one row per purchased product ID because of `DISTINCT`. This matters: one popular product may have thousands of purchases, but the exclusion set needs only one marker saying “this product has been purchased in this state.”

### Indexes for the set-building direction

This version starts with `buyers.state`, then follows each selected buyer to purchases. Useful indexes are:

```sql
CREATE INDEX idx_buyers_state_id
ON buyers(state, id);

CREATE INDEX idx_purchases_buyer_status_product
ON purchases(buyer_id, status, product_id);
```

```text
idx_buyers_state_id
    find buyers in :state
             ↓
idx_purchases_buyer_status_product
    find each buyer's completed product IDs
```

Compare this with the earlier correlated strategy:

| Query direction                                              | Helpful purchases index          |
| ------------------------------------------------------------ | -------------------------------- |
| Start from every product, then test whether it was purchased | `(product_id, status, buyer_id)` |
| Start from buyers in one state, then find their purchases    | `(buyer_id, status, product_id)` |

There is no universally best index. The best path depends on which table and predicate provide the most useful starting point.

## Compare plans and timing

Use `EXPLAIN QUERY PLAN` for the CTE version:

```sql
EXPLAIN QUERY PLAN
WITH purchased_product_ids_in_state AS (
  SELECT DISTINCT p.product_id
  FROM buyers AS b
  JOIN purchases AS p ON p.buyer_id = b.id
  WHERE b.state = :state
    AND p.status = 'completed'
)
SELECT pr.id, pr.product_name
FROM products AS pr
LEFT JOIN purchased_product_ids_in_state AS purchased
  ON purchased.product_id = pr.id
WHERE purchased.product_id IS NULL;
```

The plan may still show scans, temporary storage for `DISTINCT`, or a materialized CTE. That is not necessarily a problem. The question is whether it avoids repeatedly scanning the large purchases table for each product.

In the SQLite command-line shell, turn on timing:

```text
.timer on
```

Run both query forms several times with representative data. Test at least two states:

```text
A state with few buyers or purchases
A state with many buyers or purchases
```

The set-based rewrite can be especially attractive when one state touches a much smaller subset of purchases than the entire child table. The indexed correlated version can be attractive when each product's existence probe is highly selective. Measure rather than declaring a winner based on vibes.

## Why `NOT IN` needs care

It is tempting to write:

```sql
SELECT pr.id, pr.product_name
FROM products AS pr
WHERE pr.id NOT IN (
  SELECT p.product_id
  FROM purchases AS p
  JOIN buyers AS b ON b.id = p.buyer_id
  WHERE b.state = :state
    AND p.status = 'completed'
);
```

This can be correct only when the subquery cannot return `NULL` for `product_id`. If even one `NULL` enters a `NOT IN` result, SQL's three-valued logic can cause the predicate to evaluate to unknown for every outer row, returning no products.

`NOT EXISTS` avoids that `NULL` trap, which is why it is often the safer default for anti-joins.

If the report is limited to a period such as 2026, add the date range inside the inner query or set-building CTE:

```sql
AND p.purchased_at >= '2026-01-01'
AND p.purchased_at <  '2027-01-01'
```

That condition determines whether a purchase counts as evidence that the product was purchased in the selected state. If this time filter is common and selective, incorporate it into the relevant purchases index after the leading columns used to reach the purchase rows.

## Summary

> **An anti-join asks which parent rows have no matching child rows.**

`NOT EXISTS` expresses that rule clearly, but it can become a costly correlated scan when the database searches a large purchases table once per product. Index the correlation path when using the baseline form, or build the selected state's purchased-product set once and anti-join against it. The right strategy depends on data distribution and the actual query plan.
