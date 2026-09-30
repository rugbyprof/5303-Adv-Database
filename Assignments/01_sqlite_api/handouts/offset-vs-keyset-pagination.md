<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: SubLecture01_offset_keyset
name: SubLecture01_offset_keyset
title: "OFFSET vs. Keyset (Seek) Pagination"
description: Breakdown of the OFFSET vs Keyset concept
category: Sub_Lecture
date_due:
  month: "09"
  day: "30"
  year: 2026
  hour: 13
```
</details>

# OFFSET vs. Keyset (Seek) Pagination

Pagination breaks a large result set into manageable pages. Two common approaches are **OFFSET pagination** and **keyset (or seek) pagination**. They may return the same-looking pages, but they ask the database very different questions.

## The cost of OFFSET

Consider a request for 20 customers after the first 100,000:

```sql
SELECT id, name, created_at
FROM customers
ORDER BY id
LIMIT 20 OFFSET 100000;
```

Conceptually, the database must locate rows in `id` order, walk past 100,000 of them, and then return the next 20.

```text
Page 1       OFFSET 0
Page 100     OFFSET 1,980
Page 1,000   OFFSET 19,980
Page 5,000   OFFSET 99,980
```

The deeper the page, the more work is spent discarding rows. It is a little like asking someone to count 100,000 people in a line, ignore all of them, and then introduce the next 20.

## Keyset pagination changes the question

Instead of remembering **how many rows to skip**, keyset pagination remembers the **key of the final row from the previous page**.

If the previous page ended with `id = 100000`, request the next page like this:

```sql
SELECT id, name, created_at
FROM customers
WHERE id > 100000
ORDER BY id
LIMIT 20;
```

With an index on `id`, the database can seek directly to the relevant part of the index:

```text
B-tree index
                         ↓
... 99998  99999  100000 | 100001  100002  100003 ...
                         ↑
                         seek here
```

It does not need to process the first 100,000 entries merely to discard them.

```text
OFFSET pagination

index start
    ↓
[1][2][3][4]................[100000][100001]...[100020]
 └──────────── SKIP ──────────────┘ └── RETURN ──┘


KEYSET pagination

                              seek
                                ↓
[1][2][3]................[100000][100001]...[100020]
                                └── RETURN ──┘
```

With a B-tree, locating `100000` is approximately **O(log N)**, followed by reading the requested rows. With a large `OFFSET`, the work generally grows with the offset because the engine must still advance through those index entries or rows.

```text
OFFSET:
    O(offset + page_size)

KEYSET:
    O(log N + page_size)
```

This is a useful mental model, not a promise about every query plan. Covering indexes, caching, MVCC, and the database engine all affect real-world performance.

## Ordering by a non-unique value: use a tie-breaker

Often the sort column is not the primary key:

```sql
SELECT *
FROM posts
ORDER BY created_at
LIMIT 20 OFFSET 100000;
```

A first attempt at keyset pagination might be:

```sql
SELECT *
FROM posts
WHERE created_at > '2026-09-29 14:37:22'
ORDER BY created_at
LIMIT 20;
```

An index supports that order:

```sql
CREATE INDEX idx_posts_created_at
ON posts(created_at);
```

However, `created_at` is usually not unique:

```text
id      created_at
------  -------------------
1041    2026-09-29 14:37:22
1042    2026-09-29 14:37:22
1043    2026-09-29 14:37:22
1044    2026-09-29 14:37:23
```

If a page ends at `id = 1041`, the condition `created_at > '2026-09-29 14:37:22'` skips `1042` and `1043`. Those rows have the same timestamp, so the strict comparison moves past all of them.

Use a unique tie-breaker to create a total ordering:

```sql
SELECT *
FROM posts
WHERE (created_at, id) > ('2026-09-29 14:37:22', 1041)
ORDER BY created_at, id
LIMIT 20;
```

Create a composite index that matches the pagination order:

```sql
CREATE INDEX idx_posts_created_id
ON posts(created_at, id);
```

The cursor sent to the client can conceptually contain:

```text
created_at = 2026-09-29 14:37:22
id         = 1041
```

The next request means: “Give me the next 20 records **after this record**,” rather than “Start at the beginning, count 100,000 records, discard them, and then give me 20.”

## Stability when data changes

Keyset pagination also behaves more predictably when rows are inserted or deleted during browsing.

Suppose the first OFFSET page contains:

```text
A
B
C
D
E
```

Now a row is inserted before `A`:

```text
NEW
A
B
C
D
E
F
...
```

The next OFFSET request, `LIMIT 5 OFFSET 5`, may return:

```text
E
F
G
H
I
```

`E` appears twice because the row positions shifted underneath the numeric offset.

With keyset pagination, if the prior page ended at `E`, the next request is conceptually “give me records greater than `E`,” producing:

```text
F
G
H
I
J
```

Keyset pagination therefore tends to be both faster for deep pages and more stable under inserts and deletes. It does not eliminate every consistency concern—transactions and isolation levels still matter—but it avoids the basic “rows moved while counting” problem.

## Tradeoffs

| OFFSET pagination                         | Keyset / seek pagination               |
| ----------------------------------------- | -------------------------------------- |
| “Skip **N rows**”                         | “Start **after this key**”             |
| Easy implementation                       | Slightly more complex                  |
| Easy arbitrary page jumps                 | Naturally sequential                   |
| Gets slower at large offsets              | Performance stays much more consistent |
| Sensitive to rows shifting                | More stable under inserts/deletes      |
| Good for small or administrative datasets | Excellent for large or live datasets   |
| Uses page numbers naturally               | Usually uses cursors                   |

Keyset pagination is excellent for **Next**, **Previous**, and infinite-scroll interfaces. Its principal limitation is arbitrary jumps such as “go directly to page 7,423.” An OFFSET can calculate:

```text
OFFSET (7423 - 1) * 20
```

A keyset query cannot inherently know where page 7,423 starts; it needs a cursor from around that point.

## Summary

> **OFFSET tells the database how many rows to walk past; keyset pagination tells the database where to start.**

Indexes are very good at finding a value. They do not make counting past ten million values free. For deep, sequential pagination over large or changing datasets, keyset pagination is usually the better fit.
