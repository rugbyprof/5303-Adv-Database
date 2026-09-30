<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture03_cached
name: SubLecture03_cached
title:  "Page Totals: Exact, Cached, and Approximate Counts"
description: "Performance using cache and approximate query counts"
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Page Totals: Exact, Cached, and Approximate Counts

Many paginated interfaces show a total such as “2,418 purchases found” or “Page 3 of 121.” Producing that number often requires a second query:

```sql
SELECT COUNT(*)
FROM purchases
WHERE status = 'completed';
```

The result-page query may return only 20 rows, but the count query must determine how many rows in the entire filtered set qualify. If it runs on every page request, the database repeats that work on every page request. Page 2, page 3, and page 4 all ask the same existential question: “How many are there, exactly?”

## Why this can become expensive

Without a useful index for the filter, the database must examine every purchase row:

```sql
EXPLAIN QUERY PLAN
SELECT COUNT(*)
FROM purchases
WHERE status = 'completed';
```

Typical SQLite plan output resembles:

```text
SCAN purchases
```

```text
purchases table

[pending][completed][failed][completed][pending][completed] ...
   check      check      check       check      check      check

                         count the matching rows
```

The query cannot know a row's status without looking at it. On a large table, doing this repeatedly can consume meaningful CPU and I/O even though the displayed page contains only a handful of rows.

## First: make the exact query as efficient as possible

An index on the filtering column can make an exact count cheaper:

```sql
CREATE INDEX idx_purchases_status
ON purchases(status);
```

```sql
EXPLAIN QUERY PLAN
SELECT COUNT(*)
FROM purchases
WHERE status = 'completed';
```

The plan may now resemble:

```text
SEARCH purchases USING COVERING INDEX idx_purchases_status (status=?)
```

The database can seek to the `completed` portion of the index and count entries there. This is usually better than scanning full table rows, especially if the index is covering.

However, an index does not make a count magically constant-time. If 8 million purchases have `status = 'completed'`, an exact answer still needs work proportional to a very large qualifying set. The database may count index entries rather than wide table rows, but it must still count them.

For multi-column filters, use an index that matches the query shape:

```sql
SELECT COUNT(*)
FROM purchases
WHERE customer_id = 42
  AND status = 'completed';
```

```sql
CREATE INDEX idx_purchases_customer_status
ON purchases(customer_id, status);
```

Always inspect the actual plan for the real query. Index usefulness depends on selectivity, column order, database engine, and the rest of the `WHERE` clause.

## Why pagination multiplies the cost

Suppose a result page is fetched with:

```sql
SELECT *
FROM purchases
WHERE status = 'completed'
ORDER BY purchased_at DESC
LIMIT 20 OFFSET 40;
```

The interface may also execute the count query:

```sql
SELECT COUNT(*)
FROM purchases
WHERE status = 'completed';
```

```text
One page request

1. Find 20 rows for the requested page
2. Count every matching row to display the total

Next page request

1. Find 20 different rows
2. Count the same matching set again
```

Even if page retrieval is fast, the repeated count can become the dominant cost. This is especially common when the count is exact, the filter is broad, and many users browse or refresh the same view.

## Strategy 1: cache an exact count

If the same filter is requested repeatedly and a slightly stale value is acceptable, cache the computed count:

```text
cache key: purchases:count:status=completed
value:     2,418,372
expires:   60 seconds
```

```text
Request arrives
       |
       v
Is a cached count available and fresh?
   | yes                      | no
   v                          v
return cached total       run exact COUNT(*)
                             |
                             v
                         store in cache
```

This changes the common path from “count all matching purchases” to “read one cached value.” The tradeoff is freshness: a user may briefly see a total that is a few seconds old.

### Cache invalidation choices

There are two common approaches:

| Approach             | Behavior                                                            | Tradeoff                                            |
| -------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| Time-to-live (TTL)   | Recompute after a fixed interval, such as 60 seconds                | Simple; count can be stale until expiration         |
| Invalidate on writes | Remove or update affected cached counts whenever a purchase changes | Fresher; considerably more complex for many filters |

Caching works best for a small, predictable set of filters—for example, counts by a fixed set of statuses. Caching every possible combination of customer, date range, product, status, region, and thirteen other dropdowns can create a cache-key collection with its own postal code.

## Strategy 2: maintain a counter or summary table

For common predefined categories, store the count as data that is updated when purchases change.

```sql
CREATE TABLE purchase_status_counts (
  status TEXT PRIMARY KEY,
  purchase_count INTEGER NOT NULL
);
```

Then reading the total is inexpensive:

```sql
SELECT purchase_count
FROM purchase_status_counts
WHERE status = 'completed';
```

The write path must update the summary correctly. When a purchase moves from `pending` to `completed`, decrement one counter and increment the other in the same transaction as the purchase update.

```text
Purchase status changes: pending → completed

pending count     - 1
completed count   + 1
```

This can provide an exact, fast total, but it moves complexity from reads to writes. Concurrent updates, failures, backfills, and repair jobs must be designed carefully. Periodically validating or rebuilding summaries is sensible; counters are small objects with a surprising talent for finding edge cases.

Summary tables are most suitable when the totals correspond to stable, well-defined groupings. They are less suitable for arbitrary ad hoc filters such as “completed purchases by customers in these 37 cities during a user-selected time range.”

## Strategy 3: show an approximate count

Sometimes the interface does not need an exact total. Search engines and large catalog interfaces often use language such as:

```text
About 2.4 million results
More than 10,000 results
10,000+ results
```

An approximate count can come from database statistics, a periodically refreshed aggregate, a sampled estimate, or a separate analytics/search system. The key benefit is that the application avoids performing an expensive exact count at request time.

```text
Exact count:       2,418,372
Displayed estimate: about 2.4 million
```

Approximate counts are a strong fit when users primarily need to know the scale of a result set, not the final digit. They are a poor fit for billing, compliance, quota enforcement, or any place where “approximately correct” would produce an approximately unhappy auditor.

In SQLite specifically, `ANALYZE` populates planner statistics such as `sqlite_stat1`, but those values are estimates for query planning—not a general, exact per-filter count API. Treat planner statistics as implementation details unless the application deliberately accepts their approximation limits.

## Strategy 4: avoid showing a total

For an infinite-scroll or cursor-based interface, it may be enough to return a page plus a signal indicating whether another page exists:

```sql
SELECT *
FROM purchases
WHERE status = 'completed'
ORDER BY purchased_at DESC, id DESC
LIMIT 21;
```

Return 20 rows to the client. If a 21st row exists, show “Load more.” This avoids calculating the total entirely.

```text
20 rows returned and another exists  → show “Load more”
Fewer than 21 rows returned          → no next page
```

This design works naturally with keyset pagination. It trades a precise “Page 3 of 121” for a responsive “More results are available.”

## Comparing the options

| Approach                      | Read cost                                 | Freshness                             | Best use                                    |
| ----------------------------- | ----------------------------------------- | ------------------------------------- | ------------------------------------------- |
| Exact `COUNT(*)`              | Can be high for broad filters             | Exact at query time                   | Small datasets or infrequent totals         |
| Exact count with a good index | Lower, but still depends on matching rows | Exact at query time                   | Selective or moderately sized filtered sets |
| Cached exact count            | Usually very low                          | Slightly stale until refreshed        | Repeated, predictable filters               |
| Maintained summary counter    | Very low                                  | Exact if write maintenance is correct | Stable categories and high read volume      |
| Approximate count             | Very low                                  | Intentionally approximate             | Search, catalogs, and exploratory browsing  |
| No displayed total            | Very low                                  | Not applicable                        | Infinite scroll and cursor-based navigation |

## Timing and plan comparison

In the SQLite command-line shell, enable timing:

```text
.timer on
```

Then compare the exact count before and after adding a relevant index:

```sql
SELECT COUNT(*)
FROM purchases
WHERE status = 'completed';
```

Run each version multiple times and inspect `EXPLAIN QUERY PLAN`. The first run may include disk I/O, while later runs may benefit from cache warming. Measure a representative dataset and filter; a count of three rows is not a stress test, no matter how dramatically it is timed.

## Summary

> **An exact filtered count answers a question about the entire result set, not just the current page.**

First, index the filter appropriately and verify the plan. Then decide whether the product truly needs an exact, live total. If it does not, a cached count, maintained summary, approximate display, or “Load more” interface can remove a repeated full-scan—or large index-scan—from the request path.
