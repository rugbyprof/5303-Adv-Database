<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture02_like_fts5
name: SubLecture02_like_fts5
title: "Leading-Wildcard LIKE vs. FTS5 Full-Text Search"
description: "How FTS5 virtual tables can speed up text search"
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# Leading-Wildcard `LIKE` vs. FTS5 Full-Text Search

Text searching has an important performance trap: a normal B-tree index can efficiently find values that **start with** known text, but it generally cannot seek directly to a value when the search begins with a wildcard.

This handout compares a leading-wildcard `LIKE` query with SQLite's **FTS5** full-text search, including query plans and a simple timing method.

## A note about this exact query

```sql
SELECT *
FROM products
WHERE product_name LIKE '%';
```

The pattern `'%'` matches every non-`NULL` string, so this query effectively asks for every product having a non-`NULL` `product_name`. There is no selective search term for an index to narrow down.

The more common leading-wildcard search is something like:

```sql
SELECT *
FROM products
WHERE product_name LIKE '%wireless%';
```

The leading `%` is the crucial feature: it means “the matching text may occur anywhere in the value.”

## Why a normal index cannot usually help

Suppose a normal index exists:

```sql
CREATE INDEX idx_products_name
ON products(product_name);
```

For a prefix search, the database can use the index to seek into a contiguous range:

```sql
SELECT *
FROM products
WHERE product_name LIKE 'wireless%';
```

```text
B-tree index ordered by product_name

... webcam  |  wireless charger  wireless mouse  wireless speaker  |  wrench ...
             └────────── matching range ──────────────────────────┘
             ↑
             seek to "wireless"
```

For `LIKE '%wireless%'`, however, matching values are not in one contiguous range. A product named `Premium Wireless Mouse` could appear anywhere in alphabetical order relative to other matching values.

```text
... cable  |  premium wireless mouse  |  wrench  |  wireless charger  |  zipper ...
                 match                              match
```

The B-tree cannot jump to one starting point and then read a single range. The engine must inspect candidate rows to determine whether each name contains `wireless`. That is generally a full scan.

## Inspecting the query plan

In SQLite, use `EXPLAIN QUERY PLAN`:

```sql
EXPLAIN QUERY PLAN
SELECT *
FROM products
WHERE product_name LIKE '%wireless%';
```

Typical output will include a plan resembling:

```text
SCAN products
```

This indicates that SQLite is scanning the table rather than seeking to a narrow range using `idx_products_name`.

For contrast, a suitable prefix search may show output resembling:

```sql
EXPLAIN QUERY PLAN
SELECT *
FROM products
WHERE product_name LIKE 'wireless%';
```

```text
SEARCH products USING INDEX idx_products_name (...)
```

Exact wording varies by SQLite version, schema, collation, and query shape. The important distinction is `SCAN` versus an index-backed `SEARCH`.

## FTS5: an index designed for text search

SQLite FTS5 builds an inverted index. Instead of ordering full product names alphabetically, it maps each indexed term to the documents (rows) containing that term.

```text
FTS5 inverted index

term       rows containing the term
---------  ------------------------
wireless   12, 81, 304, 901
mouse      81, 209, 901
charger    12, 617
```

Create an FTS5 table for product names:

```sql
CREATE VIRTUAL TABLE products_fts
USING fts5(product_name);
```

Load it from the existing table:

```sql
INSERT INTO products_fts(rowid, product_name)
SELECT id, product_name
FROM products;
```

Here, `products.id` is assumed to be the primary-key identifier. Reusing it as the FTS row ID makes it easy to join a search result back to the ordinary `products` table.

Search for a word with `MATCH`:

```sql
SELECT p.*
FROM products_fts AS f
JOIN products AS p ON p.id = f.rowid
WHERE f.product_name MATCH 'wireless';
```

Unlike `LIKE '%wireless%'`, this asks the FTS index for the postings associated with the term `wireless`.

## Comparing plans

The leading-wildcard `LIKE` version typically resembles:

```sql
EXPLAIN QUERY PLAN
SELECT *
FROM products
WHERE product_name LIKE '%wireless%';
```

```text
SCAN products
```

The FTS5 version typically resembles:

```sql
EXPLAIN QUERY PLAN
SELECT p.*
FROM products_fts AS f
JOIN products AS p ON p.id = f.rowid
WHERE f.product_name MATCH 'wireless';
```

```text
SCAN f VIRTUAL TABLE INDEX ...
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
```

The word `SCAN` in the FTS5 plan does **not** mean it is reading every product row. It refers to FTS5's virtual-table access method, which uses its own inverted index. The primary-key lookup then fetches each matching product.

## Measuring time fairly

In the SQLite command-line shell, enable timing:

```text
.timer on
```

Then run comparable queries several times:

```sql
-- Leading-wildcard substring search
SELECT count(*)
FROM products
WHERE product_name LIKE '%wireless%';

-- FTS5 token search
SELECT count(*)
FROM products_fts
WHERE product_name MATCH 'wireless';
```

Record elapsed time after the first run and across several subsequent runs. The first run may include disk I/O and cache warming, so one timing is a tiny anecdote, not a scientific paper wearing a lab coat.

Use the same dataset and a term with a comparable number of matches. On a large dataset, FTS5 should usually avoid the work of checking every product name and will often be much faster for selective term searches.

## Important semantic difference

FTS5 is not a drop-in replacement for every substring search.

| `LIKE '%wireless%'`                                   | FTS5 `MATCH 'wireless'`                                                      |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| Looks for a character substring                       | Looks for indexed tokens/terms                                               |
| May match `wirelessly` because it contains `wireless` | Usually matches the token `wireless`, not arbitrary character fragments      |
| Usually requires a scan with a leading wildcard       | Uses an inverted index for terms                                             |
| Can express arbitrary substring patterns              | Supports full-text query features such as terms, phrases, and prefix queries |

For example, a prefix query in FTS5 uses `*` inside the FTS expression:

```sql
SELECT p.*
FROM products_fts AS f
JOIN products AS p ON p.id = f.rowid
WHERE f.product_name MATCH 'wireless*';
```

That can match terms such as `wireless` and `wirelessly`, but it is still a **token prefix** search—not a general “find these characters anywhere” search.

If the application truly needs arbitrary substring search, consider whether the requirement can be narrowed to token or prefix search. Specialized n-gram/trigram indexing approaches may be appropriate when arbitrary substrings are essential, but a plain FTS5 tokenizer does not automatically provide that behavior.

## Keeping the FTS table current

The example above creates a separate FTS table and loads it once. New, updated, and deleted products must also update the FTS index. In a production design, this is commonly handled with application writes or SQLite triggers. A fast search index that is stale is still fast; it is simply fast at being wrong.

## Summary

> **A B-tree index can seek to a known prefix; it cannot usually seek to an unknown position inside every string.**

`LIKE '%term%'` generally requires inspecting many or all product names. FTS5 uses an inverted index to locate rows containing indexed terms, making it a strong fit for large-scale full-text search. Before switching, confirm that token-based FTS5 matching has the same semantics your application needs.
