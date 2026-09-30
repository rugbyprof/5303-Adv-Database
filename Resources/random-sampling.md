<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture07_random
name: SubLecture07_random
title: "Random Sampling Without ORDER BY random()"
description: ""
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Random Sampling Without `ORDER BY random()`

A common request is “show 10 random products” or “select 10 random purchases.” The most obvious SQL is:

```sql
SELECT *
FROM products
ORDER BY random()
LIMIT 10;
```

It is concise, correct for a simple random sample, and often expensive on a large table.

The problem is not the `LIMIT 10`. The database must usually assign a random value to **every candidate row** and sort all candidates by those values before it knows which 10 are first.

## What `ORDER BY random()` asks the database to do

Conceptually, the query does this:

```text
1. Read every eligible product.
2. Generate one random value for every product.
3. Sort every product by its generated value.
4. Return the first 10.
```

```text
products

id    generated random value
---   ----------------------
1     0.719
2     0.032
3     0.841
4     0.116
...   ...

sort all rows by random value
              ↓
return the first 10
```

In SQLite, inspect the plan:

```sql
EXPLAIN QUERY PLAN
SELECT *
FROM products
ORDER BY random()
LIMIT 10;
```

Typical output resembles:

```text
SCAN products
USE TEMP B-TREE FOR ORDER BY
```

The exact wording varies, but the important signals are a scan of the candidate set and temporary sorting work. `random()` is calculated at query time; there is no ordinary B-tree index already ordered by “the random number this row will receive right now.”

## Why `LIMIT 10` does not fix it

For an ordinary indexed ordering, `LIMIT` can be very cheap:

```sql
SELECT *
FROM products
ORDER BY id
LIMIT 10;
```

The database reads the first 10 entries from an existing index order and stops.

For `ORDER BY random()`, it cannot know whether a row belongs in the smallest 10 random values until it compares that row with the rest of the candidate set. The output is small, but the work depends on the full candidate population.

In simplified terms:

```text
ORDER BY id LIMIT 10
    approximately O(10), after finding the start of the index

ORDER BY random() LIMIT 10
    generate a value for N rows, plus broad ordering work
    commonly O(N) to inspect rows and roughly O(N log N) sort work
```

Database engines may use a bounded top-`K` sort rather than a full sort in some cases, so the exact complexity and memory use vary. The essential point remains: the engine still examines the full eligible set and cannot use a normal index to jump to 10 newly random rows.

## Filtered samples have the same issue

Adding a filter reduces the candidate set, which may help, but it does not change the basic pattern:

```sql
SELECT *
FROM products
WHERE department = 'Electronics'
ORDER BY random()
LIMIT 10;
```

An index on `department` may help locate Electronics products. SQLite still has to randomize and order all matching Electronics rows to return an unbiased sample using this approach.

```text
Index helps find the candidate rows.
It does not pre-sort them by a random value generated for this request.
```

## Option 1: store a random sampling key

For frequent random sampling, assign every product a persistent random key when it is created:

```sql
ALTER TABLE products
ADD COLUMN sample_key REAL;

-- Backfill existing rows once.
UPDATE products
SET sample_key = (random() & 0x7fffffffffffffff) / 9223372036854775808.0;

CREATE INDEX idx_products_sample_key
ON products(sample_key);
```

When inserting new products, assign a uniformly distributed key between 0 and 1 in application code or in the insert statement.

To sample, choose a random cutoff `:cutoff` between 0 and 1:

```sql
SELECT *
FROM products
WHERE sample_key >= :cutoff
ORDER BY sample_key
LIMIT 10;
```

The index can seek directly to `:cutoff` and read 10 consecutive index entries:

```text
sample_key index

0.02   0.11   0.29   0.57 | 0.58   0.61   0.66   0.71 ...
                           ↑
                       random cutoff
                           └──── return next 10 ────┘
```

The plan should resemble an index-backed range search rather than an all-row random sort:

```sql
EXPLAIN QUERY PLAN
SELECT *
FROM products
WHERE sample_key >= :cutoff
ORDER BY sample_key
LIMIT 10;
```

```text
SEARCH products USING INDEX idx_products_sample_key (sample_key>?)
```

### Handle the end of the key range

If the cutoff falls near 1.0, fewer than 10 rows may remain. Query again from the beginning of the key range for the remainder:

```sql
-- First segment
SELECT *
FROM products
WHERE sample_key >= :cutoff
ORDER BY sample_key
LIMIT 10;

-- If needed, take the remaining rows from this segment.
SELECT *
FROM products
WHERE sample_key < :cutoff
ORDER BY sample_key
LIMIT :remaining;
```

The two segments act like a circular walk around the random-key index. Deduplicate by product ID if application logic combines results defensively.

### Important tradeoff

The selected rows are random because their stored keys are random. If the keys stay fixed forever, repeated requests can still be statistically fair, but nearby keys will often appear together in a single sample. Periodically regenerating keys, or using several independent sampling keys, may be appropriate when visible variety matters more than purely independent draws.

For a filtered sample, use a composite index that matches the filter and traversal order:

```sql
CREATE INDEX idx_products_department_sample_key
ON products(department, sample_key);
```

```sql
SELECT *
FROM products
WHERE department = 'Electronics'
  AND sample_key >= :cutoff
ORDER BY sample_key
LIMIT 10;
```

## Option 2: random row-ID lookups

If row IDs are dense, repeatedly choose a random candidate ID and look it up:

```sql
SELECT *
FROM products
WHERE id = :random_id;
```

Each primary-key lookup is fast. Repeat until 10 distinct existing rows have been collected.

```text
generate random ID → primary-key lookup → keep if row exists and qualifies
                         │
                         └─ retry for missing IDs, duplicates, or failed filters
```

This can work well for a dense, mostly static table. It becomes less attractive when IDs have large gaps, rows are heavily filtered, or the implementation needs many retries.

Do not use a simplistic “find the first ID at or above a random threshold” approach without understanding its bias. If IDs have gaps, the row immediately after a large gap can receive more probability mass than other rows.

## Option 3: application-side reservoir sampling

When a query already needs to stream every eligible row—for example, a scheduled data job—**reservoir sampling** can choose a uniform sample of `K` rows in one pass without sorting all rows.

```text
Keep the first K rows.
For the nth later row, keep it with probability K / n.
If kept, replace one random reservoir row.
```

Reservoir sampling still reads every eligible row, so it is not a shortcut for an interactive request. Its advantage is avoiding an expensive random sort while using only `O(K)` memory.

## Option 4: use a separate sample or recommendation source

For home-page product discovery, a random SQL sample may not be the product goal at all. A periodically refreshed “featured products” table, a recommendation service, or an analytics-generated candidate set can offer better relevance and predictable request cost.

This is a design change rather than a query trick, but it often answers the real question: “Which varied products should a customer see?” Randomness is one possible ingredient, not always the main course.

## Comparing approaches

| Approach                         | Request-time work                     | Sample quality                          | Main limitation                                        |
| -------------------------------- | ------------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| `ORDER BY random() LIMIT 10`     | Scan and broad ordering of candidates | Simple, unbiased sample                 | Expensive on large candidate sets                      |
| Stored random key + indexed seek | Small index range read                | Good when keys are uniformly assigned   | Requires schema/write maintenance and wraparound logic |
| Random primary-key lookups       | Several point lookups                 | Good with dense IDs and careful retries | Gaps and filters can cause retries or bias             |
| Reservoir sampling               | One streaming pass                    | Uniform sample                          | Still reads every candidate; better for batch work     |
| Precomputed candidate set        | Small lookup                          | Depends on generation method            | Requires a refresh process                             |

## Timing and plan comparison

In the SQLite command-line shell, enable timing:

```text
.timer on
```

Compare the naïve query:

```sql
SELECT *
FROM products
ORDER BY random()
LIMIT 10;
```

with the stored-key query on a representative table size. Inspect both with `EXPLAIN QUERY PLAN`, and run each several times. The first run may include disk I/O, while later runs may be warmed by cache.

Also measure the filter combinations that the application truly uses. A brilliant sampling query for all products is not automatically brilliant for “10 in-stock Electronics products available in Illinois.”

## Summary

> **`ORDER BY random()` makes every candidate participate before it can select a few.**

It is fine for small tables, ad hoc queries, and occasional administrative use. For frequent sampling from large tables, store an indexed random key, use carefully designed ID sampling, precompute candidates, or move the full scan to a background job. The best alternative depends on whether the priority is statistical purity, visible variety, simple maintenance, or low request latency.
