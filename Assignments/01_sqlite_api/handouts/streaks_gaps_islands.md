---
details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture05_streaks_gaps
name: SubLecture05_streaks_gaps
title: "Finding Buyer Purchase Streaks with Gaps and Islands"
description: "Solutions for dealing with streaks and gaps in query results"
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Finding Buyer Purchase Streaks with Gaps and Islands

A **purchase streak** is a consecutive run of calendar days on which a buyer made at least one purchase. For one specific buyer, the goal might be to return every streak, its start and end dates, and its length.

```text
Purchase days

2026-07-01
2026-07-02
2026-07-03
2026-07-06
2026-07-07
2026-07-10

Streaks

July 1–3     3 days
July 6–7     2 days
July 10      1 day
```

This is a classic **gaps-and-islands** problem:

- A **gap** is a missing day between purchase days.
- An **island** is one consecutive run of days.

The database must identify the gaps before it can group the islands. The words make it sound like a beach holiday; the query plan may disagree.

## Start with one row per purchase day

Buyers can place multiple purchases on the same day. A streak counts days, not individual receipts, so first reduce the data to distinct calendar days.


```sql
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
)
SELECT purchase_day
FROM purchase_days
ORDER BY purchase_day;
```

For example, these purchases:

```text
buyer_id   purchased_at
--------   -------------------
42         2026-07-01 09:10:00
42         2026-07-01 14:25:00
42         2026-07-02 11:05:00
42         2026-07-03 16:40:00
```

become:

```text
purchase_day
------------
2026-07-01
2026-07-02
2026-07-03
```

This step is important for both correctness and performance. Joining raw purchases directly can multiply rows: two purchases today joined to three purchases yesterday creates six joined pairs, which is impressive only if the goal was accidental arithmetic.

## Indexing the specific buyer's purchases

Because the query is for one buyer, begin with an index that locates that buyer's rows efficiently:

```sql
CREATE INDEX idx_purchases_buyer_purchased_at
ON purchases(buyer_id, purchased_at);
```

This index allows the database to find rows for `buyer_id = :buyer_id` and read them in timestamp order. It helps reduce the input to the streak calculation, although the query must still deduplicate days and identify gaps within that buyer's history.

Avoid wrapping an indexed timestamp in a function in the filter when a range will do. For example, if only a recent history is needed:

```sql
WHERE buyer_id = :buyer_id
  AND purchased_at >= '2026-01-01'
  AND purchased_at <  '2027-01-01'
```

The `date(purchased_at)` expression is reasonable in the `SELECT` that creates calendar-day values; placing it directly in a filter can make index range use harder.

## Approach 1: a self-join baseline

A self-join compares each purchase day with its immediate predecessor. A day is the **start of a streak** when the prior calendar day is absent.

```sql
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
)
SELECT current_day.purchase_day AS streak_start
FROM purchase_days AS current_day
LEFT JOIN purchase_days AS previous_day
  ON previous_day.purchase_day = date(current_day.purchase_day, '-1 day')
WHERE previous_day.purchase_day IS NULL
ORDER BY streak_start;
```

For the sample days, the result is:

```text
streak_start
------------
2026-07-01
2026-07-06
2026-07-10
```

The same idea finds streak ends by joining to the next day and looking for no match:

```sql
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
)
SELECT current_day.purchase_day AS streak_end
FROM purchase_days AS current_day
LEFT JOIN purchase_days AS next_day
  ON next_day.purchase_day = date(current_day.purchase_day, '+1 day')
WHERE next_day.purchase_day IS NULL
ORDER BY streak_end;
```

Self-joins are useful for explaining the problem because they make the comparison explicit:

```text
current day       previous day exists?      result
-----------       --------------------      ------
July 1            no                        start an island
July 2            yes (July 1)              continue island
July 3            yes (July 2)              continue island
July 6            no                        start an island
```

### The limits of the self-join approach

Finding starts and ends is straightforward. Pairing each start with its corresponding end, calculating lengths, or returning every island in one clean query becomes increasingly awkward. Repeated self-joins can also add work and make the query harder to maintain.

For a moderate number of distinct days for one buyer, an indexed self-join can be perfectly acceptable. For a general, reusable streak report, a window-function pattern is usually clearer and scales better.

## Approach 2: label islands with window functions

The scalable pattern has three steps:

1. Sort the distinct purchase days.
2. Use `LAG()` to see the prior purchase day.
3. Mark a new island after each gap, then use a running sum to assign an island number.

```sql
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
),
marked_days AS (
  SELECT
    purchase_day,
    CASE
      WHEN LAG(purchase_day) OVER (ORDER BY purchase_day)
           = date(purchase_day, '-1 day')
      THEN 0
      ELSE 1
    END AS starts_new_streak
  FROM purchase_days
),
labeled_days AS (
  SELECT
    purchase_day,
    SUM(starts_new_streak) OVER (
      ORDER BY purchase_day
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS streak_id
  FROM marked_days
)
SELECT
  MIN(purchase_day) AS streak_start,
  MAX(purchase_day) AS streak_end,
  COUNT(*) AS streak_days
FROM labeled_days
GROUP BY streak_id
ORDER BY streak_start;
```

For the sample data, the result is:

```text
streak_start   streak_end     streak_days
------------   ----------     -----------
2026-07-01     2026-07-03          3
2026-07-06     2026-07-07          2
2026-07-10     2026-07-10          1
```

## How the window pattern works

`LAG()` supplies the previous row in the ordered sequence:

```text
purchase_day   prior day from LAG()   consecutive?   starts_new_streak
------------   -------------------    ------------   -----------------
2026-07-01     NULL                   no             1
2026-07-02     2026-07-01             yes            0
2026-07-03     2026-07-02             yes            0
2026-07-06     2026-07-03             no             1
2026-07-07     2026-07-06             yes            0
2026-07-10     2026-07-07             no             1
```

The running `SUM()` turns each “new streak” marker into a stable group identifier:

```text
purchase_day   starts_new_streak   running sum = streak_id
------------   -----------------   -----------------------
2026-07-01             1                       1
2026-07-02             0                       1
2026-07-03             0                       1
2026-07-06             1                       2
2026-07-07             0                       2
2026-07-10             1                       3
```

After that, ordinary `GROUP BY streak_id` produces one result row per island.

## An alternative window trick: normalized dates

For consecutive daily values, another common pattern subtracts a row number from each date. Consecutive dates receive the same normalized value:

```sql
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
),
numbered_days AS (
  SELECT
    purchase_day,
    julianday(purchase_day)
      - ROW_NUMBER() OVER (ORDER BY purchase_day) AS island_key
  FROM purchase_days
)
SELECT
  MIN(purchase_day) AS streak_start,
  MAX(purchase_day) AS streak_end,
  COUNT(*) AS streak_days
FROM numbered_days
GROUP BY island_key
ORDER BY streak_start;
```

```text
purchase_day   row number   julianday(day) − row number   island
------------   ----------   ---------------------------   ------
July 1              1                 same value             1
July 2              2                 same value             1
July 3              3                 same value             1
July 6              4                 different value        2
```

This is compact, but the `LAG()` version often communicates the business rule more directly: a gap begins a new streak.

## Plan and performance considerations

Use SQLite's plan viewer on the full query:

```sql
EXPLAIN QUERY PLAN
WITH purchase_days AS (
  SELECT DISTINCT date(purchased_at) AS purchase_day
  FROM purchases
  WHERE buyer_id = :buyer_id
)
SELECT purchase_day
FROM purchase_days
ORDER BY purchase_day;
```

Plan output varies, but may mention an index search for the buyer and temporary B-trees for `DISTINCT`, ordering, or grouping. Window functions require a defined order, so the engine may sort the distinct days if they are not already produced in the needed order.

The important scaling property is that the window solution makes a small number of ordered passes over **D distinct purchase days** for the selected buyer, rather than repeatedly pairing raw purchase rows. The work is commonly dominated by sorting and grouping those days, roughly `O(D log D)` when a sort is required.

For a buyer with years of history, limit the date range if the product only needs recent streaks. For all buyers at once, the same window technique can use `PARTITION BY buyer_id`, but it will process the combined histories of every buyer and deserves careful measurement.

## Summary

> **A streak begins wherever the previous calendar day is missing.**

Deduplicate to one row per buyer-day first. A self-join is a clear way to find starts and ends, while `LAG()` plus a running `SUM()` labels every gaps-and-islands run in one scalable pattern. An index on `(buyer_id, purchased_at)` reduces the input efficiently; the window logic then identifies the consecutive-day structure.
