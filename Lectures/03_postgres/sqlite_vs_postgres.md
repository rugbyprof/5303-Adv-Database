# SQLite vs. PostgreSQL: Same SQL, Different Machines

In [Assignment 01](../../Assignments/01_sqlite_api/) you put SQLite behind an API, watched indexes turn 1-second queries into 1-millisecond ones, and then watched `database is locked` show up as soon as several clients tried to write at once. Next you'll build the same API on PostgreSQL. Most of your SQL will carry over unchanged. Almost everything **underneath** the SQL will change.

This tutorial covers what changes and why, using the store schema and the 15 queries from [QUERIES.md](../../Assignments/01_sqlite_api/QUERIES.md). Read it before you port anything.

**The one-sentence version:**

> SQLite is a **library** that your program uses to read and write a file. PostgreSQL is a **server**: a separate program that owns the data, and your program sends it requests over a network connection.

Nearly every difference below follows from that sentence.

| Section | Topic |
| :--- | :--- |
| [1](#1-architecture-library-vs-server) | Architecture: library vs. server |
| [2](#2-our-setup-your-laptop-and-the-class-server) | Our setup: your laptop and the class server |
| [3](#3-types-and-strictness) | Types and strictness |
| [4](#4-porting-the-15-queries) | Porting the 15 queries |
| [5](#5-the-planner-and-explain) | The planner and `EXPLAIN` |
| [6](#6-indexes) | Indexes |
| [7](#7-storage-mvcc-and-vacuum) | Storage, MVCC, and `VACUUM` |
| [8](#8-concurrency-and-transactions) | **Concurrency and transactions** (the big one) |
| [9](#9-code-inside-the-database-functions-procedures-triggers) | Code inside the database: functions, procedures, triggers |
| [10](#10-security-operations-and-configuration) | Security, operations, and configuration |
| [11](#11-features-one-has-and-the-other-doesnt) | Features one has and the other doesn't |
| [12](#12-measuring-fairly) | Measuring fairly |
| [13](#13-which-one-when) | Which one, when |
| [14](#14-cheat-sheet) | Cheat sheet |
| [15](#15-check-your-understanding) | Check your understanding |

---

## 1. Architecture: library vs. server

### SQLite: the database is a file, the engine is in your process

```
┌──────────────────────── your Python process ────────────────────────┐
│                                                                     │
│   FastAPI route ──► sqlite3 module ──► SQLite engine (C library)    │
│                                              │                      │
└──────────────────────────────────────────────┼──────────────────────┘
                                               │ ordinary file reads/writes
                                               ▼
                           data/idx_1m.db   (+ -wal, -shm in WAL mode)
```

- There is no server. `sqlite3.connect("idx_1m.db")` opens a file. A "query" is a function call inside your process, so a primary-key lookup takes microseconds.
- Every process that opens the file has its own copy of the engine. They coordinate through **file locks** on that one file. That is why SQLite has one writer for the whole database: the lock covers the whole file.
- Nothing runs while no program has the file open. No background jobs, no scheduler, no one checking passwords.

### PostgreSQL: a server process owns the data

```
 your laptop / API server                         PostgreSQL server machine
┌──────────────────────────┐                ┌──────────────────────────────────────────┐
│ FastAPI worker 1 ──conn──┼──── TCP 5432 ──┼──► backend process (one per connection) │
│ FastAPI worker 2 ──conn──┼────────────────┼──► backend process                      │
│ psql             ──conn──┼────────────────┼──► backend process                      │
└──────────────────────────┘                │          │  share:                       │
                                            │          ▼                               │
                                            │   shared buffers (page cache in RAM)    │
                                            │   lock manager (row & table locks)      │
                                            │   WAL writer · checkpointer ·           │
                                            │   autovacuum · background writer        │
                                            │          │                               │
                                            │          ▼                               │
                                            │   data directory: many files per table  │
                                            └──────────────────────────────────────────┘
```

- **A connection is a process.** When a client connects, the server forks a new **backend process** for it. That process lives until the client disconnects. Opening a connection costs a few milliseconds (more with SSL over the internet), and each one uses several MB of server memory.
- **The server is the only thing that touches the files.** Clients never open data files. Because one program coordinates every client, it can lock **individual rows** instead of the whole database.
- **The server runs work in the background:** writing dirty pages to disk, cleaning up old row versions (autovacuum), refreshing planner statistics. That's where its extra features come from, and it's why there's more to configure.

### What that means in practice

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Install | Nothing (the library is built into Python) | A server: Docker, Postgres.app, or an installer |
| "Connect" means | open a file | TCP handshake, authenticate, server forks a process |
| Cost of a trivial query | microseconds (a function call) | at least one network round trip: about 0.1 ms locally, **20–80 ms to a cloud server** |
| Who enforces access | the operating system's file permissions | the server: roles, passwords, `GRANT`, SSL |
| Concurrency control | file locks: many readers, **one writer for the whole file** | lock manager + MVCC: **row-level** write locks, readers never block writers |
| Background work | none | autovacuum, checkpoints, statistics, scheduled jobs (`pg_cron`) |
| Back up | copy the file (carefully; see the [WAL handout](../../Assignments/01_sqlite_api/handouts/wal_mode.md#8-caveats)) | `pg_dump`, or continuous WAL archiving for point-in-time recovery |
| Server-side code | triggers only | functions, procedures, triggers, in PL/pgSQL, SQL, Python, and more |

> **The network is now part of every query.** In Assignment 01, `elapsed_ms` measured only the time spent inside SQLite. Against a cloud server, a query that runs in 0.2 ms inside PostgreSQL might take 40 ms from your laptop, and almost all of that is the trip there and back. A route that runs 10 small queries one after another (the "N+1" pattern) costs 10 round trips. SQLite never charged you for that pattern. PostgreSQL over the internet makes you pay for it every time.

---

## 2. Our setup: your laptop and the class server

You will use PostgreSQL in two places:

| | Your local server | The class server |
| :--- | :--- | :--- |
| Where | Your laptop ([setup guide](postgres_setup.md)) | A cloud VM run by the instructor |
| Who uses it | Only you | Everyone in the class at once |
| Used for | Porting the API, building the databases, running the index experiments | **Concurrency experiments**: everyone hammers it at the same time |
| Network distance | Loopback, about 0.1 ms | The internet, tens of milliseconds |
| You are | Superuser: you can do anything | An ordinary role with limited rights and a **connection limit** |
| Connection string | `postgresql://student:student@localhost:5432/course` | `postgresql://<your_user>:<password>@<class-host>:5432/<db>?sslmode=require` (details in class) |

Why the split? Index and query-plan experiments need a quiet machine. If 30 people share the server while you time a query, you're measuring their load, not your index. Concurrency experiments need the opposite: one server and many clients, which is something SQLite can't do at all. (Thirty laptops can't share one SQLite file. Remember from the [WAL handout](../../Assignments/01_sqlite_api/handouts/wal_mode.md#8-caveats) that WAL mode doesn't even work over a network drive.)

Things that are different on the class server:

- **Connection limits are real.** A PostgreSQL server accepts a fixed number of connections (`max_connections`, 100 by default), and the class server gives each role its own smaller limit. If you start `uvicorn --workers 4` and every worker opens a 10-connection pool, that's 40 connections from one student. When you exceed your limit you get:

  ```
  FATAL:  too many connections for role "your_user"
  ```

  This failure is new in this assignment. SQLite had no connections to run out of.

- **SSL is required.** Your password crosses the internet, so add `sslmode=require` to the connection string.
- **You can't change server settings or install extensions.** You can `SET` per-session settings such as `work_mem`, `statement_timeout`, and `lock_timeout`, but not `max_connections` or `shared_buffers`.
- **Your data lives next to everyone else's data.** You'll work in your own schema or database (instructions in class). `DROP TABLE` affects only what you own, but a runaway query uses CPU that everyone shares. Set `statement_timeout` on every connection to the class server.

---

## 3. Types and strictness

### SQLite: column types are suggestions

SQLite uses **type affinity**. The declared type is a preference, not a rule. Try this in the `sqlite3` shell:

```sql
CREATE TABLE t (i INTEGER, n NUMERIC, d TEXT);
INSERT INTO t VALUES ('abc', 9.99, 'not a date');   -- succeeds
SELECT typeof(i), typeof(n) FROM t;                  -- text | real
```

The string `'abc'` went into an `INTEGER` column. `9.99` in a `NUMERIC` column is stored as a **floating-point** `real`. That's why the [triggers handout](../../Assignments/01_sqlite_api/handouts/triggers_and_procedures.md) has to `ROUND` revenue before comparing it: `0.1 + 0.2` comes out as `0.30000000000000004`. That's also why our schema needs `CHECK (purchase_date GLOB '????-??-??')`. SQLite has no date type, so a CHECK constraint is the only guard.

(SQLite 3.37 added `STRICT` tables, which reject wrong types. Our assignment schema doesn't use them.)

### PostgreSQL: column types are enforced

```sql
CREATE TABLE t (i integer, n numeric(10,2), d date);
INSERT INTO t VALUES ('abc', 9.99, 'not a date');
-- ERROR:  invalid input syntax for type integer: "abc"
```

The types that matter most for our schema:

| Our column | SQLite | PostgreSQL | Why it matters |
| :--- | :--- | :--- | :--- |
| `purchase_id INTEGER PRIMARY KEY` | an alias for the internal `rowid` | `bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY` | See "identity gotcha" below |
| `amount NUMERIC` | stored as a float (`real`) | `numeric(10,2)`: **exact** decimal | Money arithmetic is exact; no rounding leftovers |
| `purchase_date TEXT` + `GLOB` check | ISO text; string order equals date order | `date` | Real date arithmetic, `date_trunc`, and invalid dates are rejected |
| `state_code TEXT CHECK (...)` | text | `text` or `char(2)` | Same idea |
| booleans | `0` / `1` integers | `boolean` (`true` / `false`) | |

### Other strictness differences that will bite you

| Behavior | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Foreign keys | **off** unless each connection runs `PRAGMA foreign_keys = ON` | always enforced |
| Indexes on FK columns | not automatic | **also not automatic**. You still create `idx_purchases_customer` yourself |
| `'Games' LIKE 'games'` | true (ASCII is case-insensitive) | **false**. Use `ILIKE` or `lower(...)` |
| `"Games"` (double quotes) | treated as a string if no such column exists | always an **identifier**: `column "Games" does not exist` |
| Unquoted identifiers | case preserved | folded to **lowercase**. `CREATE TABLE Purchases` creates `purchases` |
| Non-aggregated column in `GROUP BY` query | allowed; picks a value from some row | error, unless that column depends on the grouped primary key |
| `round(x, 2)` on a float | works | `round(double precision, integer)` doesn't exist; cast to `numeric` first |
| `ALTER TABLE` | limited (no changing a column's type) | almost anything, and it's **transactional**: DDL can be rolled back |

> **The identity gotcha.** If you load rows with explicit ids (copying `purchase_id` from SQLite), the identity sequence doesn't know about them. It still starts at 1, and your first `POST /purchases` fails with `duplicate key value violates unique constraint "purchases_pkey"`. After every bulk load with explicit ids, run:
>
> ```sql
> SELECT setval(pg_get_serial_sequence('purchases', 'purchase_id'), max(purchase_id))
> FROM purchases;
> ```

---

## 4. Porting the 15 queries

Most of [QUERIES.md](../../Assignments/01_sqlite_api/QUERIES.md) runs on PostgreSQL unchanged. The changes cluster around dates and around the Python driver.

### The driver: `sqlite3` → `psycopg`

| | `sqlite3` | `psycopg` (version 3) |
| :--- | :--- | :--- |
| Connect | `sqlite3.connect("data/idx_1m.db")` | `psycopg.connect("postgresql://...")` |
| Named parameter | `:customer_id` | `%(customer_id)s` |
| Positional parameter | `?` | `%s` |
| A literal `%` in SQL that has parameters | `'%'` | `'%%'` (it's a format character now) |
| Rows as dicts | `con.row_factory = sqlite3.Row` | `psycopg.connect(..., row_factory=dict_row)` |
| Transaction | `with con:` | `with con.transaction():` (`with con:` also commits, but then **closes** the connection) |
| Connection per request | cheap; fine | expensive; use a pool (`psycopg_pool.ConnectionPool`) |
| "Locked" error | `sqlite3.OperationalError: database is locked` | several kinds, see [§8](#8-concurrency-and-transactions) |

The placeholder change touches every query, so do it with care. `WHERE customer_id = :customer_id` becomes `WHERE customer_id = %(customer_id)s`.

### Query by query

| Query | Changes for PostgreSQL |
| :--- | :--- |
| Q01–Q05 | Placeholders only |
| **Q06** streaks | `julianday(day)` doesn't exist. With a real `date` column, subtract an integer instead: `day - (ROW_NUMBER() OVER (ORDER BY day))::int AS grp`. The cast is required, because `date - bigint` has no operator. |
| Q07, Q08, Q09 | Placeholders only |
| Q10 | Runs as written. `pr.product_name` is allowed with `GROUP BY pr.product_id` because `product_id` is the primary key of `products`, so the name is determined by it. Group by a non-key column and PostgreSQL rejects the query; SQLite would silently pick a value. |
| Q11 | Placeholders only. `OFFSET` is just as expensive in PostgreSQL. |
| Q12 | `ORDER BY random()` works and is just as slow. The fast version still works, but sequences in PostgreSQL skip values whenever an insert rolls back, so the "ids have no big gaps" assumption is weaker. PostgreSQL also offers `TABLESAMPLE` (see [§11](#11-features-one-has-and-the-other-doesnt)). |
| **Q13** by month | `substr(purchase_date, 1, 7)` fails on a `date`: `function substr(date, integer, integer) does not exist`. Use `to_char(purchase_date, 'YYYY-MM')` (text) or `date_trunc('month', purchase_date)::date` (a date, which sorts and indexes better). |
| **Q14** cube | Same `substr` change. The CTE named `cube` runs, but `CUBE` is a keyword in PostgreSQL (`GROUP BY CUBE (...)`, see [§11](#11-features-one-has-and-the-other-doesnt)), so a name like `grid` avoids confusion. |
| Q15 insert | `RETURNING` works in both. Remember the identity gotcha from [§3](#3-types-and-strictness). |

For example, Q06 in PostgreSQL:

```sql
WITH days AS (
    SELECT DISTINCT purchase_date AS day
    FROM purchases
    WHERE customer_id = %(customer_id)s
),
islands AS (
    SELECT day,
           day - (ROW_NUMBER() OVER (ORDER BY day))::int AS grp
    FROM days
)
SELECT MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM islands
GROUP BY grp
HAVING COUNT(*) >= 2
ORDER BY days DESC, streak_start
LIMIT 10
```

> **Dates as parameters.** `purchase_date >= %(start)s` works when you pass the string `'2025-03-01'`, because PostgreSQL converts it to a `date`. Passing a Python `datetime.date` is cleaner, and FastAPI parses it for you if you annotate the route parameter as `start: date`.

---

## 5. The planner and `EXPLAIN`

Both databases use a **cost-based planner**: it estimates the cost of several plans from table statistics and runs the cheapest one. PostgreSQL's planner has more ways to run a query, so the **same missing index can hurt much less**.

### Reading plans: `EXPLAIN QUERY PLAN` → `EXPLAIN ANALYZE`

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Show the plan | `EXPLAIN QUERY PLAN SELECT ...` | `EXPLAIN SELECT ...` (estimates only, doesn't run it) |
| Run it and show actual numbers | `.eqp on` + `.timer on` in the shell | `EXPLAIN (ANALYZE) SELECT ...`: actual rows, time per step, buffer hits |
| Output | a few lines of text | a tree. Read it **from the most indented line outward** |

`EXPLAIN ANALYZE` **runs** the query. On an `INSERT` or `DELETE` it really changes data, so wrap it in `BEGIN; ... ROLLBACK;`.

### Translating the plan vocabulary

| SQLite says | PostgreSQL says | Meaning |
| :--- | :--- | :--- |
| `SCAN purchases` | `Seq Scan on purchases` | read every row |
| — | `Parallel Seq Scan` under `Gather` | read every row, split across several worker processes |
| `SEARCH ... USING INDEX idx_x (col=?)` | `Index Scan using idx_x` | walk the index, fetch each matching row |
| — | `Bitmap Index Scan` + `Bitmap Heap Scan` | collect the matching row locations first, sort them by position on disk, then read each table page once. For "a few thousand rows" this beats both an index scan and a full scan. |
| `USING COVERING INDEX idx_x` | `Index Only Scan using idx_x` | answer from the index alone (see the visibility-map caveat in [§7](#7-storage-mvcc-and-vacuum)) |
| `SEARCH ... USING INTEGER PRIMARY KEY` | `Index Scan using purchases_pkey` | **not** the same thing; see [§7](#7-storage-mvcc-and-vacuum) |
| `USE TEMP B-TREE FOR ORDER BY` | `Sort` (watch `Sort Method: external merge Disk`) | sort first. "Disk" means it didn't fit in `work_mem` |
| `USE TEMP B-TREE FOR GROUP BY` | `HashAggregate` or `Sort` + `GroupAggregate` | group first |
| `CORRELATED SCALAR SUBQUERY` | `SubPlan` | inner query runs once per outer row |
| (nested loop, the only join SQLite has) | `Nested Loop`, `Hash Join`, `Merge Join` | three join algorithms; see below |
| `NOT EXISTS` as a correlated subquery | `Hash Anti Join` / `Nested Loop Anti Join` | anti-join done as a join |

### Why PostgreSQL survives a missing index better

SQLite joins tables one way: a **nested loop**. For each row of the outer table, it searches the inner table. If the inner search has an index, that's fast. If it doesn't, SQLite scans the inner table once **per outer row**. That's why Q08 had the biggest index win in Assignment 01: without `idx_purchases_product`, SQLite re-scanned purchases for each of 5,000 products. (SQLite sometimes builds a temporary "automatic index" to soften this; it shows up in plans as `AUTOMATIC COVERING INDEX`.)

PostgreSQL can also do a **hash join**: read one side once into an in-memory hash table, then stream the other side past it once. Here's Q08 on PostgreSQL with **no secondary indexes at all** (300k purchases, `EXPLAIN (ANALYZE, COSTS OFF)`, trimmed):

```
Hash Right Anti Join
  Hash Cond: (pu.product_id = pr.product_id)
  ->  Hash Join
        Hash Cond: (pu.customer_id = c.customer_id)
        ->  Seq Scan on purchases pu            ← purchases read ONCE
        ->  Hash
              ->  Hash Join  (customers ⋈ zipcodes WHERE state_code = 'TX')
  ->  Hash
        ->  Seq Scan on products pr
Execution Time: 27.9 ms
```

Purchases is read **once**, not once per product. Expect the `noidx` vs. `idx` gap for Q08 to be **far smaller** on PostgreSQL than on SQLite. The index still helps, but its absence is no longer a disaster. When you compare your two results tables, this is the kind of difference to look for and explain.

Two more planner features SQLite lacks:

- **Parallel query.** A big `Seq Scan` or aggregate can be split across worker processes (`Workers Launched: 2`). On the `noidx` databases this makes full scans faster than you might expect.
- **Richer statistics.** `ANALYZE` (run automatically by autovacuum) stores histograms and most-common values per column in `pg_stats`. That helps with skewed data, such as our few heavy-buying customers. In SQLite, statistics are refreshed only when you run `ANALYZE` yourself, which is why `make_dbs.py` calls it.

---

## 6. Indexes

The B-tree index you know from SQLite is also PostgreSQL's default, and `CREATE INDEX idx_purchases_date ON purchases(purchase_date)` is identical in both. PostgreSQL adds more index **types** and options:

| Feature | SQLite | PostgreSQL | Where it would help us |
| :--- | :---: | :---: | :--- |
| B-tree | ✅ | ✅ | everything in Assignment 01 |
| Composite (multi-column) | ✅ | ✅ | `(customer_id, amount)` |
| Partial: `... WHERE state = 'active'` | ✅ | ✅ | index only the rows a hot query touches |
| Expression: `ON purchases (lower(email))` | ✅ | ✅ | case-insensitive lookups |
| `INCLUDE` columns | — | ✅ | `ON purchases (customer_id) INCLUDE (amount)`: covering without making `amount` part of the key |
| **BRIN** (block range) | — | ✅ | `purchase_date` on a table that's inserted in date order: a tiny index (kilobytes) that skips whole ranges of pages |
| **GIN** | — | ✅ | full-text search (`tsvector`), `jsonb`, arrays; with `pg_trgm`, `LIKE '%term%'` |
| **GiST** | — | ✅ | **PostGIS** geometry ("what's near this point?"). This is why the course moves to PostgreSQL |
| Hash | — | ✅ | equality-only lookups |
| Build without blocking writes | — | `CREATE INDEX CONCURRENTLY` | add an index to a live, busy table |

Full-text search shows the difference in approach. SQLite's answer is a separate **FTS5 virtual table** that you keep in sync with triggers (see the [FTS5 handout](../../Assignments/01_sqlite_api/handouts/lead_wildcard-vs-fts5.md)). PostgreSQL's answer is an index on the existing table:

```sql
-- Full-text search: words
CREATE INDEX idx_products_fts ON products
    USING gin (to_tsvector('english', product_name));
SELECT * FROM products
WHERE to_tsvector('english', product_name) @@ plainto_tsquery('english', 'wireless mouse');

-- Substring search: makes the "leading wildcard" LIKE indexable
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_trgm ON products USING gin (product_name gin_trgm_ops);
SELECT * FROM products WHERE product_name ILIKE '%mouse%';     -- can use the index
```

---

## 7. Storage, MVCC, and `VACUUM`

### Where the rows live

- **SQLite** stores each table as a B-tree **keyed by `rowid`**. With `INTEGER PRIMARY KEY`, the primary key *is* the `rowid`, so a primary-key lookup lands directly on the row. The table is **clustered** on its primary key. Q01 and the Q11 keyset query were fast in `noidx_*` for that reason.
- **PostgreSQL** stores each table as a **heap**: rows sit wherever there was free space, in no particular order. **Every** index, including the primary key, is a separate structure that points into the heap. A primary-key lookup is "search the `purchases_pkey` index, then fetch the heap page". It's still fast, but it's two steps, the same as any other index.

### MVCC: why PostgreSQL keeps old row versions

PostgreSQL uses **multi-version concurrency control**. An `UPDATE` never overwrites a row in place. It writes a **new version** of the row and marks the old one as expired. Each transaction sees the versions that were committed when its snapshot was taken. That's how readers and writers avoid blocking each other ([§8](#8-concurrency-and-transactions)).

The cost is **dead row versions**. Every `UPDATE` and `DELETE` leaves one behind. A background process, **autovacuum**, later reclaims their space and updates the **visibility map**, a per-page note that says "every row on this page is visible to everyone".

SQLite in WAL mode also gives readers a snapshot, but it does it with the `-wal` file, at the level of the whole database and with a single writer. It never has dead rows to clean up. SQLite's `VACUUM` means something else: it rebuilds the whole file to reclaim free space.

### Consequences you'll see

**Index-only scans depend on `VACUUM`.** The index doesn't know whether a row version is visible to your transaction. PostgreSQL can skip the heap only for pages that the visibility map marks all-visible. Right after a bulk load, nothing is marked yet. Here's the same query, before and after `VACUUM`, with the covering index `(customer_id, amount)`:

```
-- just loaded, never vacuumed
HashAggregate
  ->  Bitmap Heap Scan on purchases               ← reads the table anyway
        ->  Bitmap Index Scan on idx_purchases_cust_amount

-- after:  VACUUM purchases;
GroupAggregate
  ->  Index Only Scan using idx_purchases_cust_amount on purchases
        Heap Fetches: 5                           ← only 5 rows needed the table
```

So after you load your Postgres databases, run `VACUUM ANALYZE;` before you time anything, just as `make_dbs.py` runs `ANALYZE` for SQLite. Otherwise your "covering index" results will be wrong.

**`COUNT(*)` is still not free.** Because visibility is per transaction, PostgreSQL can't keep a single row count. It has to count visible rows. The tricks from the [counting handout](../../Assignments/01_sqlite_api/handouts/cached-vs-approximate_counts.md) still apply, and PostgreSQL gives you a free estimate: `SELECT reltuples::bigint FROM pg_class WHERE relname = 'purchases';`

**Update-heavy tables bloat.** A summary row that's updated 100,000 times leaves 100,000 dead versions until autovacuum catches up. Keep that in mind when [§9](#9-code-inside-the-database-functions-procedures-triggers) proposes a trigger that updates `monthly_sales` on every insert.

---

## 8. Concurrency and transactions

This is where the two databases differ most, and it's what the class-server experiment tests.

### SQLite: one writer for the whole file

You measured this in Phase 4:

- Any number of readers (in WAL mode, readers don't block the writer).
- **One** writer at a time for the **entire database**. Two clients inserting unrelated rows into different tables still take turns.
- A second writer waits up to `busy_timeout`, then fails with `database is locked`.
- More processes (`--workers 4`) meant more competitors for the same lock, not more write capacity.

### PostgreSQL: row-level locks and MVCC

- **Readers never block writers, and writers never block readers.** A `SELECT` reads the row versions in its snapshot and takes no row locks.
- **Writers lock only the rows they change.** Two transactions inserting different purchases don't wait for each other at all. Two transactions updating the *same* row do: the second **waits** until the first commits or rolls back.
- By default it waits **indefinitely** (`lock_timeout = 0`). Requests don't fail the way SQLite's did. They queue. If you'd rather fail fast, set a timeout:

  ```sql
  SET lock_timeout = '500ms';
  UPDATE counter SET n = n + 1 WHERE id = 1;
  -- ERROR:  canceling statement due to lock timeout
  ```

- **Deadlocks are detected.** If transaction A waits on B while B waits on A, PostgreSQL notices within about a second (`deadlock_timeout`) and aborts one of them with `deadlock detected`. SQLite has only one lock to wait for, so the nearest it gets is two transactions that both try to upgrade from reading to writing. It refuses one immediately with `database is locked` instead of letting them wait on each other.

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Unit of write locking | the whole database | a row |
| Readers vs. writers | WAL mode: don't block | never block (MVCC) |
| Two writers, different rows | take turns | run at the same time |
| Two writers, same row | take turns | second one waits for the first to commit |
| Waiting forever? | no: `busy_timeout`, then `database is locked` | yes, by default; set `lock_timeout` or `statement_timeout` |
| Default isolation | serializable (there's only ever one writer) | **read committed** |
| Deadlocks | avoided: a would-be deadlock fails at once with `database is locked` | detected; one transaction is aborted |

### Isolation levels: the new thing to understand

SQLite transactions are effectively **serializable**: only one writer exists, so no two writes can interleave. PostgreSQL lets writes interleave, and the **isolation level** decides what a transaction can see while others commit around it:

| Level | What a transaction sees | What can go wrong |
| :--- | :--- | :--- |
| `READ COMMITTED` (**default**) | each **statement** sees everything committed before *that statement* started | read-modify-write in application code can lose updates |
| `REPEATABLE READ` | the whole **transaction** sees one snapshot, taken at its first statement | conflicting updates fail with a serialization error, and you retry |
| `SERIALIZABLE` | as if transactions ran one at a time | more serialization errors, and you retry |

**The lost update.** This is the classic bug that SQLite's single writer hid from you. Two API requests each add one purchase to a counter by reading it in Python and writing it back:

```
 time   request A                           request B
 ────   ─────────────────────────────────   ─────────────────────────────────
  1     SELECT n FROM counter;  -- 10
  2                                         SELECT n FROM counter;  -- 10
  3     UPDATE counter SET n = 11;
  4     COMMIT;
  5                                         UPDATE counter SET n = 11;
  6                                         COMMIT;                -- n = 11, not 12
```

Two fixes:

1. **Let the database do the arithmetic:** `UPDATE counter SET n = n + 1`. B's `UPDATE` waits for A's lock, then re-reads the committed value 11 and writes 12. This is also how the trigger in [§9](#9-code-inside-the-database-functions-procedures-triggers) works.
2. **Lock the row when you read it:** `SELECT n FROM counter WHERE id = 1 FOR UPDATE;` B's `SELECT` waits until A commits.

Under `REPEATABLE READ`, step 5 doesn't silently overwrite. It fails:

```
ERROR:  could not serialize access due to concurrent update
```

That's correct behavior. Your code must **catch it and retry the transaction** (SQLSTATE `40001`). Code that runs at `REPEATABLE READ` or `SERIALIZABLE` without a retry loop has a bug, even if it hasn't shown up yet.

### Hot rows: rebuilding SQLite's bottleneck by accident

Row-level locking helps only if writers touch **different** rows. `loadtest.py` posts the **same** purchase every time (`customer_id 1`, `department 'Games'`, `2026-01-15`). Plain inserts of that purchase don't conflict, because each one is a new row. Now add the trigger from [§9](#9-code-inside-the-database-functions-procedures-triggers) that keeps `monthly_sales` up to date: every insert updates the **same** summary row (`2026-01`, that customer's state, `Games`). Every transaction has to wait for the row lock that the previous one holds until it commits. You've rebuilt a single-writer bottleneck, this time on one row instead of the whole file.

On a laptop with 16 concurrent clients (`pgbench`, local, so no network):

| Workload | Relative throughput | Failures |
| :--- | :--- | :--- |
| Plain `INSERT INTO purchases` | 1.0× | none |
| `INSERT` + per-row trigger updating one `monthly_sales` row | about 0.3× | none, they wait |

PostgreSQL doesn't fail here. It queues, and throughput drops. Your measurements will differ; look for the pattern. Ways around a hot row: batch the updates (a statement-level trigger, [§9](#9-code-inside-the-database-functions-procedures-triggers)), spread the load across several rows and sum them when you read, or refresh the summary on a schedule instead of on every write.

### What limits throughput on the class server

With SQLite the limit was obvious: one write lock. On the shared PostgreSQL server, expect these limits instead, roughly in the order you'll hit them:

1. **Network round trips.** Each request is at least one round trip over the internet, plus `BEGIN`/`COMMIT` round trips if your driver sends them separately. A single connection doing one insert per round trip at 40 ms can't exceed about 25 inserts per second, however fast the server is. Concurrency (several connections at once) is how you get past that.
2. **Connection limits.** Your role's limit and the server's `max_connections`. Exceed them and you get `too many connections for role "..."` or `sorry, too many clients already`. This is the closest equivalent to `database is locked`, but it means "no free connection slot", not "no free write lock".
3. **Hot rows and lock waits**, as described above.
4. **Commit flushes.** By default every commit waits for its WAL record to reach disk (`synchronous_commit = on`). PostgreSQL batches the flushes of commits that arrive at the same moment ("group commit"), which is one reason many concurrent writers do better than one.
5. **Server CPU and disk.** These are shared by the whole class, so your numbers will depend on what everyone else is doing at that moment.

### Errors to catch in the API

| Situation | SQLite | PostgreSQL (`psycopg` exception, SQLSTATE) |
| :--- | :--- | :--- |
| Couldn't get a write lock in time | `OperationalError: database is locked` | `LockNotAvailable` (`55P03`), only if `lock_timeout` is set |
| Statement ran too long | — | `QueryCanceled` (`57014`), if `statement_timeout` is set |
| Concurrent update conflict | — | `SerializationFailure` (`40001`): **retry** |
| Deadlock | — | `DeadlockDetected` (`40P01`): **retry** |
| No connection slot | — | `OperationalError` at connect: `too many connections ...` (`53300`) |
| Foreign key violated | only if `foreign_keys = ON` | `ForeignKeyViolation` (`23503`): a client error, return `400`/`422` |

---

## 9. Code inside the database: functions, procedures, triggers

You found the gap in the [triggers and procedures handout](../../Assignments/01_sqlite_api/handouts/triggers_and_procedures.md): SQLite has **no stored procedures**. It has no `CREATE PROCEDURE`, no variables, no `IF`, and no `CALL`. Its only server-side code is triggers, and because SQLite has no server, your Python code plays the "procedure" role.

PostgreSQL has a full procedural layer:

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Functions usable in SQL | Only ones your app registers (`con.create_function`), running **in your app** | `CREATE FUNCTION` in SQL, **PL/pgSQL**, PL/Python, and others, running **in the server** |
| Procedures | none | `CREATE PROCEDURE` + `CALL`; can `COMMIT` partway through (PostgreSQL 11+) |
| Triggers | `FOR EACH ROW`; the body is SQL statements | `FOR EACH ROW` **or** `FOR EACH STATEMENT`; the body is a function, so it can use logic, loops, and error handling |
| Batch triggers | — | Statement triggers with **transition tables** see every row the statement inserted |
| Materialized views | — (build a table by hand) | `CREATE MATERIALIZED VIEW` + `REFRESH ... CONCURRENTLY` |
| Scheduling | none; needs cron or your app | `pg_cron` extension (available on most managed cloud providers) |
| Notifications | — | `LISTEN` / `NOTIFY` to push events to connected clients |

Here's the `monthly_sales` problem from the handout, solved in PostgreSQL each way. (All of these were tested on PostgreSQL 18; `monthly_sales.month` is a `date` holding the first day of the month.)

### A procedure: rebuild on demand

```sql
CREATE OR REPLACE PROCEDURE refresh_monthly_sales()
LANGUAGE plpgsql AS $$
BEGIN
    TRUNCATE monthly_sales;
    INSERT INTO monthly_sales
    SELECT date_trunc('month', pu.purchase_date)::date, z.state_code, pu.department,
           COUNT(*), SUM(pu.amount)
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    GROUP BY 1, 2, 3;
    RAISE NOTICE 'monthly_sales rebuilt: % rows', (SELECT COUNT(*) FROM monthly_sales);
END $$;

CALL refresh_monthly_sales();
```

Any client can now call it: `psql`, your API, a scheduler. The logic lives in one place, inside the database. (`TRUNCATE` takes an exclusive lock, so readers wait for the rebuild to finish instead of seeing an empty table.)

### A row trigger: keep it fresh on every insert

```sql
CREATE OR REPLACE FUNCTION monthly_sales_add() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO monthly_sales AS ms (month, state_code, department, num_purchases, revenue)
    SELECT date_trunc('month', NEW.purchase_date)::date, z.state_code, NEW.department,
           1, NEW.amount
    FROM customers c JOIN zipcodes z ON z.zipcode = c.zipcode
    WHERE c.customer_id = NEW.customer_id
    ON CONFLICT (month, state_code, department) DO UPDATE
        SET num_purchases = ms.num_purchases + EXCLUDED.num_purchases,
            revenue       = ms.revenue       + EXCLUDED.revenue;
    RETURN NULL;   -- AFTER trigger: the return value is ignored
END $$;

CREATE TRIGGER purchases_after_insert
AFTER INSERT ON purchases
FOR EACH ROW EXECUTE FUNCTION monthly_sales_add();
```

`INSERT ... ON CONFLICT DO UPDATE` (an "upsert") creates the summary row for a new month or adds to an existing one in a single statement. SQLite has the same syntax. The difference is what happens under concurrency: in SQLite the whole file is already locked, while in PostgreSQL this is the **hot row** from [§8](#8-concurrency-and-transactions).

### A statement trigger: one update per batch

```sql
CREATE OR REPLACE FUNCTION monthly_sales_add_batch() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO monthly_sales AS ms (month, state_code, department, num_purchases, revenue)
    SELECT date_trunc('month', n.purchase_date)::date, z.state_code, n.department,
           COUNT(*), SUM(n.amount)
    FROM new_rows n
    JOIN customers c ON c.customer_id = n.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    GROUP BY 1, 2, 3
    ON CONFLICT (month, state_code, department) DO UPDATE
        SET num_purchases = ms.num_purchases + EXCLUDED.num_purchases,
            revenue       = ms.revenue       + EXCLUDED.revenue;
    RETURN NULL;
END $$;

CREATE TRIGGER purchases_after_insert_batch
AFTER INSERT ON purchases
REFERENCING NEW TABLE AS new_rows
FOR EACH STATEMENT EXECUTE FUNCTION monthly_sales_add_batch();
```

An `INSERT` of 1,000 rows now touches each summary row **once**, not 1,000 times. SQLite can't express this, because its triggers are always per row.

### A materialized view: the summary table, managed by the server

```sql
CREATE MATERIALIZED VIEW monthly_sales_mv AS
SELECT date_trunc('month', pu.purchase_date)::date AS month, z.state_code, pu.department,
       COUNT(*) AS num_purchases, SUM(pu.amount) AS revenue
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY 1, 2, 3;

CREATE UNIQUE INDEX ON monthly_sales_mv (month, state_code, department);

REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_mv;   -- readers keep reading during the refresh
```

This is exactly what `sql/summary_tables.sql` did by hand: a stored snapshot of a query. It's still stale between refreshes, just as in Phase 3. `CONCURRENTLY` requires a unique index on the view. In exchange, readers never wait while it refreshes.

### Scheduling it

With the `pg_cron` extension, the schedule lives in the database too:

```sql
SELECT cron.schedule('refresh-monthly-sales', '*/10 * * * *',
                     'REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_mv');
```

This resolves the handout's question "can you schedule a procedure?" In SQLite the answer was "only from outside". In PostgreSQL it's "yes, if `pg_cron` is installed". `pg_cron` isn't in the course Docker image, so locally you'd still use cron or your app, just as before.

### A function you can use in a query

```sql
CREATE OR REPLACE FUNCTION customer_total(p_customer_id bigint) RETURNS numeric
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(SUM(amount), 0) FROM purchases WHERE customer_id = p_customer_id
$$;

SELECT customer_id, customer_total(customer_id) FROM customers LIMIT 5;
```

`STABLE` tells the planner the function doesn't modify data and returns the same result within a single statement. Be careful: calling this for every customer is a correlated subquery in disguise, and it shows up in the plan the same way.

> **When should logic live in the database?** Server-side code is shared by every client, sits next to the data (no round trips), and can enforce rules that no client can bypass. It's also harder to version, test, and debug than your Python code. A reasonable default: keep **data integrity** in the database (constraints, triggers that maintain derived data) and **business logic** in the application.

---

## 10. Security, operations, and configuration

### Who is allowed to do what

SQLite has no users. Anyone who can read the file can read every row, and anyone who can write the file can change it. (That's why Assignment 01 checks API keys in FastAPI: the API is the only gatekeeper.)

PostgreSQL has **roles** and **privileges**:

```sql
CREATE ROLE api_reader LOGIN PASSWORD '...' CONNECTION LIMIT 10;
GRANT CONNECT ON DATABASE course TO api_reader;
GRANT USAGE ON SCHEMA public TO api_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO api_reader;   -- read-only
```

A sensible API setup gives the read routes a read-only role, so even an SQL-injection bug in a `GET` route can't modify data. PostgreSQL also has **row-level security** (policies such as "a user sees only their own rows"), SSL, and `pg_hba.conf`, which controls which hosts may connect and how they authenticate. The class server uses these to give each of you your own account with a limited number of connections.

### Configuration: per-connection `PRAGMA` vs. server settings

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Where | `PRAGMA`s, mostly **per connection**, which is why `experiment.py` sets them on every request | `postgresql.conf` / `ALTER SYSTEM` for the server; `SET` for one session |
| Examples | `journal_mode`, `foreign_keys`, `busy_timeout`, `synchronous` | `shared_buffers`, `work_mem`, `max_connections`, `statement_timeout`, `lock_timeout`, `synchronous_commit` |
| Durability trade-off | `synchronous = NORMAL` | `synchronous_commit = off`: commits return before the WAL is flushed. A crash can lose the last few commits but never corrupts data. Same trade-off. |
| Sort/hash memory | `cache_size`, `temp_store` | `work_mem`, **per sort or hash, per query**. Too small, and you'll see `external merge Disk` in Q07/Q12 plans. |

### Watching the server

The server knows what every connection is doing. On the class server these views show the hammering as it happens:

```sql
-- who is connected, and what are they running or waiting on?
SELECT usename, state, wait_event_type, wait_event, now() - query_start AS running_for, query
FROM pg_stat_activity
WHERE datname = current_database();

-- who is blocked, and by whom?
SELECT pid, usename, pg_blocking_pids(pid) AS blocked_by, query
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;

-- dead row versions waiting for autovacuum
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables;
```

With the `pg_stat_statements` extension, `SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC` lists the server's most expensive queries across all clients. SQLite has no equivalent, because no single process sees all the clients.

### Backups

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| Logical copy | `.dump` | `pg_dump` / `pg_restore` |
| Online copy | `.backup copy.db` | `pg_basebackup` |
| Point-in-time recovery ("restore to 2:14 pm yesterday") | — | WAL archiving |

---

## 11. Features one has and the other doesn't

### PostgreSQL has, SQLite doesn't

| Feature | Example | Relevance |
| :--- | :--- | :--- |
| `GROUP BY ROLLUP / CUBE / GROUPING SETS` | `GROUP BY ROLLUP (state_code, department)` adds subtotal and grand-total rows | Q14's "cube" in one query. The SQLite lecture had to fake rollups with `UNION ALL`. |
| `DISTINCT ON` | `SELECT DISTINCT ON (customer_id) ... ORDER BY customer_id, amount DESC` | each customer's single biggest purchase, without a window function |
| `LATERAL` joins | `JOIN LATERAL (SELECT ... WHERE pu.customer_id = c.customer_id ORDER BY amount DESC LIMIT 3) ...` | "top 3 per group" |
| `TABLESAMPLE` | `FROM purchases TABLESAMPLE SYSTEM (1)` | Q12-style sampling: picks about 1% of **pages**, so it's fast but clumpy. `BERNOULLI` samples rows: slower, more even. |
| `generate_series` | `generate_series('2025-01-01'::date, '2025-12-31', '1 day')` | build a calendar to find days with **zero** sales (gaps-and-islands) |
| Rich types | `jsonb`, arrays, ranges (`daterange`), `enum`, `uuid`, `interval`, `inet` | |
| Schemas (namespaces) | `course.purchases`, `alice.purchases` | separate workspaces inside one database; SQLite uses `ATTACH` for something similar |
| `COPY` | `COPY purchases FROM STDIN (FORMAT csv)` | bulk loading, much faster than row-by-row `INSERT` |
| Table partitioning | `PARTITION BY RANGE (purchase_date)` | split one huge table into monthly pieces |
| Extensions | `postgis`, `pg_trgm`, `pg_stat_statements`, `pg_cron` | **PostGIS is why this course switches databases** |
| Transactional DDL | `BEGIN; ALTER TABLE ...; ROLLBACK;` | schema changes can be undone |

Example: Q14's state × department report with subtotals, run against the summary table:

```sql
SELECT state_code, department, SUM(num_purchases) AS num_purchases, SUM(revenue) AS revenue
FROM monthly_sales
GROUP BY ROLLUP (state_code, department)
ORDER BY state_code NULLS LAST, department NULLS LAST;
-- rows with department NULL are state subtotals; the row with both NULL is the grand total
```

### SQLite has, PostgreSQL doesn't (or does worse)

| Strength | Why it matters |
| :--- | :--- |
| No server, no setup, no administrator | `pip install` and go; nothing to keep running or patch |
| The database is one file | email it, check it into a test fixture, ship it inside an app |
| No network | single-user point lookups are **faster** than any client/server database, because there's no round trip |
| `:memory:` databases | a brand-new database for each test in microseconds |
| Tiny footprint | runs on phones, browsers (WASM), embedded devices |
| Flexible typing | handy for messy imports; dangerous everywhere else |

---

## 12. Measuring fairly

When you repeat Assignment 01 on PostgreSQL, you'll be tempted to put the two results tables side by side. Read them with care:

1. **Time the same thing.** Assignment 01's `elapsed_ms` timed `execute + fetchall` in Python. With SQLite that's almost pure engine time. With PostgreSQL it includes a network round trip and moving the rows to Python. For engine-to-engine comparisons, also record PostgreSQL's server-side `Execution Time` from `EXPLAIN (ANALYZE)`.
2. **Warm the cache.** The first run reads from disk; later runs hit `shared_buffers` and the OS cache. The driver's median-of-5 helps. Treat the first run as a warm-up.
3. **`VACUUM ANALYZE` after loading,** or the planner works from missing statistics and index-only scans won't happen ([§7](#7-storage-mvcc-and-vacuum)).
4. **Match the hardware.** Your laptop vs. a cloud VM is not a database comparison. Run the local experiments on your laptop for both databases.
5. **`EXPLAIN ANALYZE` adds overhead,** because it times every step. Use it to understand a plan, not as the official time.
6. **Look for patterns, not winners.** For a single-row lookup, SQLite should win (no round trip). For a big join without indexes, PostgreSQL should close much of the gap (hash joins, parallel workers). For concurrent writers, the comparison isn't close. If your numbers don't fit these patterns, look at the plans until you can explain why.

---

## 13. Which one, when

The Phase 5 scenarios again, with PostgreSQL as the alternative:

| Scenario | Better fit | Why |
| :--- | :--- | :--- |
| Internal read-only dashboard, ~10 analysts | either | SQLite handles concurrent readers well. Choose PostgreSQL if the data already lives on a server or needs real accounts. |
| Mobile app's offline local storage | **SQLite** | embedded, one file, no server, one user |
| Thousands of events per second from many servers | **PostgreSQL** | many writers, row-level locks, network clients, group commit |
| A fresh throwaway database for each automated test | **SQLite** (unless production is PostgreSQL) | `:memory:` is instant. If production runs PostgreSQL, test against PostgreSQL too, because the type and SQL differences in §3–§4 will bite you. |
| A web API with many users who write | **PostgreSQL** | the Phase 4 bottleneck goes away (until you create a hot row) |
| Geospatial queries ("airports within 50 km of this earthquake") | **PostgreSQL + PostGIS** | GiST indexes and hundreds of `ST_*` functions. SQLite's SpatiaLite exists but is far less common. |
| A desktop app's document format | **SQLite** | the file *is* the document |
| Several applications sharing one database, with different permissions | **PostgreSQL** | roles, `GRANT`, row-level security |

A rule of thumb: **SQLite competes with `fopen()`, PostgreSQL competes with other database servers.** If the data belongs to one program on one machine, start with SQLite. If many clients, users, or machines share it, start with PostgreSQL.

---

## 14. Cheat sheet

### SQL and schema

| SQLite | PostgreSQL |
| :--- | :--- |
| `INTEGER PRIMARY KEY` | `bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY` |
| `NUMERIC` (stored as a float) | `numeric(10,2)` (exact) |
| `TEXT` date + `GLOB '????-??-??'` | `date` |
| `substr(d, 1, 7)` | `to_char(d, 'YYYY-MM')` or `date_trunc('month', d)` |
| `julianday(a) - julianday(b)` | `a - b` (two dates give an integer number of days) |
| `date('now')` | `current_date` |
| `strftime('%Y', d)` | `extract(year FROM d)` |
| `x LIKE 'abc%'` (case-insensitive) | `x ILIKE 'abc%'` |
| `GROUP_CONCAT(x, ',')` | `string_agg(x, ',')` |
| `IFNULL(a, b)` | `COALESCE(a, b)` (works in both) |
| `INSERT OR IGNORE` | `INSERT ... ON CONFLICT DO NOTHING` |
| `INSERT OR REPLACE` | `INSERT ... ON CONFLICT (...) DO UPDATE SET ...` |
| `PRAGMA foreign_keys = ON` | (always on) |
| `EXPLAIN QUERY PLAN` | `EXPLAIN (ANALYZE)` |
| `ANALYZE` | `VACUUM ANALYZE` (also done automatically) |
| FTS5 virtual table | `tsvector` + GIN index; `pg_trgm` for substrings |
| (no procedures) | `CREATE PROCEDURE` / `CREATE FUNCTION ... LANGUAGE plpgsql` |

### Python

| `sqlite3` | `psycopg` 3 |
| :--- | :--- |
| `:name`, `?` | `%(name)s`, `%s` |
| `sqlite3.Row` | `psycopg.rows.dict_row` |
| new connection per request | `psycopg_pool.ConnectionPool`, opened once at startup |
| `except sqlite3.OperationalError` | `except psycopg.errors.SerializationFailure`, `LockNotAvailable`, `QueryCanceled`, ... |

### Shell

The `psql` equivalents of `.tables`, `.schema`, `.timer`, and friends are in the [psql cheat sheet](postgres_setup.md#psql-cheat-sheet) in the setup guide.

---

## 15. Check your understanding

1. Assignment 01's Q01 took about 0.05 ms in SQLite. You run it from your laptop against the class server and the API reports 45 ms. The server's `EXPLAIN ANALYZE` says `Execution Time: 0.06 ms`. Where did the other 44.9 ms go, and why doesn't an index fix it?
2. Q08 was the biggest index win on SQLite. Predict whether the `noidx`/`idx` gap will be larger or smaller on PostgreSQL, and name the plan node that explains your prediction.
3. You load `purchases` into PostgreSQL, create the covering index `(customer_id, amount)`, and run Q09 straight away. The plan shows `Bitmap Heap Scan`, not `Index Only Scan`. What's missing, and why does PostgreSQL need it when SQLite didn't?
4. In SQLite, Phase 4's run A failed with `database is locked`. Thirty students run the same load test against the class server. Give two failures that **can** happen there and one that **can't**.
5. Two requests run `SELECT n FROM counter` in Python, add 1, and write the result back with `UPDATE counter SET n = :new`. Why did SQLite never lose an update this way, while PostgreSQL at its default isolation level can? Give two fixes.
6. Your trigger keeps `monthly_sales` perfectly in sync, but write throughput on the class server dropped sharply once you added it. Using the phrase "hot row", explain why. Then suggest two changes.
7. SQLite has no stored procedures. Name three things PostgreSQL's procedures and functions can do that a Python function in your API can't, or can't do as well.
8. Your teammate wants to run the API's unit tests against an in-memory SQLite database even though production uses PostgreSQL. Name two differences from §3–§4 that could let a test pass on SQLite but fail in production.
