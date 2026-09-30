<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture04_trailing_window
name: SubLecture04_trailing_window
title: "Ranking Buyers by 90-Day Trailing Spend"
description: "Different solutions to a 90 day window query with aggregation"
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Ranking Buyers by 90-Day Trailing Spend

Suppose an application needs a leaderboard of buyers by the money they have spent during the last 90 days:

```sql
WITH buyer_spend AS (
  SELECT
    buyer_id,
    SUM(amount) AS trailing_90_day_spend
  FROM purchases
  WHERE purchased_at >= date('now', '-90 days')
  GROUP BY buyer_id
)
SELECT
  buyer_id,
  trailing_90_day_spend,
  RANK() OVER (ORDER BY trailing_90_day_spend DESC) AS spend_rank
FROM buyer_spend
ORDER BY spend_rank;
```

This query is correct and expressive. It is also likely to be expensive when the `purchases` table is large. The work comes from two unavoidable stages:

1. Read the purchases in the 90-day window and calculate one sum per buyer.
2. Sort those buyer totals so the window function can assign ranks.

An index can reduce some input work, but no ordinary index stores the answer “this buyer is currently ranked 37th by the sum of all purchases in the last 90 days.” That answer must be computed unless it has been stored in advance.

## What the query is really doing

Imagine the 90-day filter returns these purchases:

```text
buyer_id   amount
--------   ------
101        30.00
205        90.00
101        70.00
314        50.00
205        20.00
```

The `GROUP BY` stage first produces one row per buyer:

```text
buyer_id   trailing_90_day_spend
--------   ---------------------
101        100.00
205        110.00
314         50.00
```

Then the window function needs those rows in descending spend order:

```text
buyer_id   trailing_90_day_spend   spend_rank
--------   ---------------------   ----------
205        110.00                      1
101        100.00                      2
314         50.00                      3
```

If two buyers have the same spend, `RANK()` gives them the same rank and leaves a gap afterward:

```text
buyer_id   spend   RANK()   DENSE_RANK()   ROW_NUMBER()
--------   -----   ------   ------------   ------------
205        110        1          1               1
101        100        2          2               2
407        100        2          2               3
314         50        4          3               4
```

Choose the function that matches the meaning required by the application:

| Function       | Tie behavior                                                                  |
| -------------- | ----------------------------------------------------------------------------- |
| `RANK()`       | Equal values share a rank; later ranks have gaps                              |
| `DENSE_RANK()` | Equal values share a rank; later ranks have no gaps                           |
| `ROW_NUMBER()` | Every row receives a distinct position; ties need a deterministic tie-breaker |

## Why a large scan happens

The predicate limits the query to 90 days, but the database still needs to inspect every purchase in that 90-day period to calculate each buyer's sum.

```text
purchases from the last 90 days

[buyer 101, $30] [buyer 205, $90] [buyer 101, $70] ...
        │                 │                 │
        └──── accumulate each buyer's total ┘
```

There is no shortcut that can derive `SUM(amount)` for every buyer without reading the contributing purchase values—or without using a previously maintained summary. If the date filter is broad, this scan can still involve millions of rows.

In SQLite, inspect the plan with:

```sql
EXPLAIN QUERY PLAN
WITH buyer_spend AS (
  SELECT buyer_id, SUM(amount) AS trailing_90_day_spend
  FROM purchases
  WHERE purchased_at >= date('now', '-90 days')
  GROUP BY buyer_id
)
SELECT
  buyer_id,
  trailing_90_day_spend,
  RANK() OVER (ORDER BY trailing_90_day_spend DESC) AS spend_rank
FROM buyer_spend
ORDER BY spend_rank;
```

Typical plan details may include messages resembling:

```text
SCAN purchases
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

The exact words vary by SQLite version and data layout. The key idea is that the engine may scan input rows, build grouped totals, and use temporary storage to sort the totals.

## Why a large sort happens

An ordinary B-tree index can order rows by stored columns such as `purchased_at`, `buyer_id`, or `amount`. This query sorts by a **derived value**:

```text
SUM(amount) for each buyer in the trailing 90 days
```

That value is not a column in `purchases`, and it changes whenever a relevant purchase is inserted, updated, or ages out of the 90-day window.

```text
Raw purchases                         Derived buyer totals

buyer 101: $30, $70        ──────►   buyer 101: $100
buyer 205: $90, $20        ──────►   buyer 205: $110
buyer 314: $50             ──────►   buyer 314:  $50
                                          │
                                          ▼
                              sort by total descending for ranking
```

No normal index on the raw purchase rows can already be ordered by all of those current, grouped sums. The database must create the buyer totals and then sort them to rank them.

In simplified terms, if `P` purchases fall within the window and `B` buyers have at least one purchase, the work is approximately:

```text
read and aggregate:  O(P)
rank-related sort:   O(B log B)
```

The details vary by engine, memory, disk spills, and aggregation strategy, but the important point remains: the query's expensive work scales with the entire 90-day population, not with the 20 leaderboard rows eventually displayed.

## What indexes can and cannot improve

An index can help locate the beginning of the time range:

```sql
CREATE INDEX idx_purchases_purchased_at
ON purchases(purchased_at);
```

This may allow an index range scan for `purchased_at >= ...` instead of reading older purchases. A covering index can sometimes reduce table lookups:

```sql
CREATE INDEX idx_purchases_date_buyer_amount
ON purchases(purchased_at, buyer_id, amount);
```

These can be useful improvements. They do **not** eliminate the need to read all qualifying 90-day purchases, add each amount into a buyer total, and order the resulting totals by spend.

| Task                                                 | Can a raw-purchases index help? | Why                                                          |
| ---------------------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| Exclude purchases older than 90 days                 | Often                           | An index on `purchased_at` can seek into the date range      |
| Read `buyer_id` and `amount` efficiently             | Sometimes                       | A covering index may avoid fetching table rows               |
| Calculate every current 90-day buyer sum             | Not completely                  | Each qualifying purchase contributes to a changing aggregate |
| Sort buyers by their calculated sums                 | No                              | The sort key is a derived aggregate, not a stored raw column |
| Return the top 20 current buyers without computation | No                              | The current ranking has not been stored anywhere             |

The precise claim is therefore not “indexes never help.” It is: **no ordinary index on the raw `purchases` table can make this dynamic aggregate-and-rank query a simple index lookup.**

## A tempting but misleading optimization

Adding `LIMIT 20` to the outer query does not mean the database can safely read only 20 purchase rows:

```sql
-- The LIMIT reduces output, not necessarily the aggregation work.
SELECT
  buyer_id,
  SUM(amount) AS trailing_90_day_spend
FROM purchases
WHERE purchased_at >= date('now', '-90 days')
GROUP BY buyer_id
ORDER BY trailing_90_day_spend DESC
LIMIT 20;
```

To know which 20 buyers have the largest totals, the database must first determine the totals for all eligible buyers. One buyer's final purchase in the input may change the leaderboard at the last moment. Databases are good, but they are not clairvoyant.

## The usual fix: precompute the summary

If the leaderboard is requested frequently, move the expensive calculation off the request path. Store a summary table with one row per buyer:

```sql
CREATE TABLE buyer_90_day_spend (
  buyer_id INTEGER PRIMARY KEY,
  trailing_90_day_spend NUMERIC NOT NULL,
  calculated_at TEXT NOT NULL
);
```

After populating or refreshing it, index the stored ranking key:

```sql
CREATE INDEX idx_buyer_90_day_spend_desc
ON buyer_90_day_spend(trailing_90_day_spend DESC, buyer_id);
```

The request-time leaderboard query becomes much smaller:

```sql
SELECT
  buyer_id,
  trailing_90_day_spend,
  RANK() OVER (ORDER BY trailing_90_day_spend DESC) AS spend_rank
FROM buyer_90_day_spend
ORDER BY trailing_90_day_spend DESC, buyer_id
LIMIT 20;
```

The aggregate over raw purchases has already happened during refresh. The index can now support reading the highest stored totals in order. If the application needs ranks only for the displayed top 20, the ranking work is correspondingly small.

## Refresh strategies and freshness tradeoffs

Because “trailing 90 days” changes continuously, the summary must be refreshed or maintained.

| Strategy                   | How it works                                                             | Freshness and cost                                                           |
| -------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Periodic full refresh      | Recalculate all buyer totals every hour or day                           | Simple; totals are stale between refreshes; refresh can be expensive         |
| Incremental updates        | Add new purchases to the affected buyer; subtract purchases that age out | Fresh and efficient at read time; more difficult correctness logic           |
| Daily aggregate table      | Store each buyer's spend per day, then sum the latest 90 daily rows      | Less raw data to scan; may be near-real-time rather than exact to the second |
| Background leaderboard job | Compute and store the top buyers separately                              | Fastest reads; only supports the dimensions the job precomputes              |

For example, a daily aggregate can reduce the raw data volume:

```sql
CREATE TABLE buyer_daily_spend (
  spend_date TEXT NOT NULL,
  buyer_id INTEGER NOT NULL,
  daily_spend NUMERIC NOT NULL,
  PRIMARY KEY (spend_date, buyer_id)
);
```

The 90-day calculation still aggregates, but it reads daily summary rows rather than every individual purchase. This is often a worthwhile trade when each buyer may place many purchases per day.

## Timing the comparison

In the SQLite command-line shell, enable timing:

```text
.timer on
```

Compare the live aggregate-and-rank query with a query against a refreshed summary table. Run each several times on representative data and inspect `EXPLAIN QUERY PLAN`. The first run may include disk reads, while later runs may benefit from cache warming.

Do not compare only the request time. Include the refresh cost and decide where it belongs: every user request, once per minute, hourly, or during a scheduled background job.

## Summary

> **A ranking by trailing spend is expensive because the ranking key must first be calculated from many rows.**

Indexes can help filter the 90-day window and reduce row-fetching overhead, but they cannot pre-sort buyer totals that do not yet exist. For a frequently requested leaderboard, precompute or maintain the 90-day spend summary, then index the stored total for fast ranking and retrieval.
