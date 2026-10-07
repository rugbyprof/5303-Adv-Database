# Calling SQLite and PostgreSQL from Python

[sqlite_vs_postgres.md](sqlite_vs_postgres.md) compares the two databases. This handout zooms in on one piece of that comparison: **the Python code you write to talk to each one**. It puts a `sqlite3` call and a `psycopg` call side by side, explains every line that differs, and then hides those differences behind one small class, [`code/dbrun.py`](code/dbrun.py), so the same query runs on either database.

**The short version:**

- Both drivers follow the same Python standard (**DB-API 2.0**, [PEP 249](https://peps.python.org/pep-0249/)): `connect`, `execute`, `fetchall`, `commit`, `IntegrityError`. Most of your code carries over.
- Four things differ: **how you connect**, **how you write placeholders** (`:name` vs. `%(name)s`), **how transactions start**, and **what Python types come back**.
- A thin wrapper can hide the first three. It can't hide the fourth, and it can't hide SQL dialect differences. Those are your job.

| Section | Topic |
| :--- | :--- |
| [1](#1-the-same-query-both-ways) | The same query, both ways |
| [2](#2-line-by-line-what-changed) | Line by line: what changed |
| [3](#3-placeholders-and-the--trap) | Placeholders and the `%` trap |
| [4](#4-transactions-who-says-begin) | Transactions: who says `BEGIN`? |
| [5](#5-what-comes-back-same-query-different-python-types) | What comes back: same query, different Python types |
| [6](#6-one-interface-for-both-dbrundatabase) | One interface for both: `dbrun.Database` |
| [7](#7-run-the-demo) | Run the demo |
| [8](#8-using-it-in-the-api) | Using it in the API |
| [9](#9-the-industrial-strength-version) | The industrial-strength version |
| [10](#10-check-your-understanding) | Check your understanding |

---

## 1. The same query, both ways

"Total spent by one customer," written for each driver.

**SQLite (`sqlite3`, built into Python):**

```python
import sqlite3

con = sqlite3.connect("data/idx_100k.db")          # opens a file
con.row_factory = sqlite3.Row                       # rows act like dicts
con.execute("PRAGMA foreign_keys = ON")             # off unless you ask, every connection

sql = """
    SELECT customer_id, COUNT(*) AS n, SUM(amount) AS total
    FROM purchases
    WHERE customer_id = :customer_id
    GROUP BY customer_id
"""
row = con.execute(sql, {"customer_id": 1}).fetchone()
print(dict(row))       # {'customer_id': 1, 'n': 4, 'total': 40.279999999999994}

con.close()
```

**PostgreSQL (`psycopg` 3, `pip install "psycopg[binary]"`):**

```python
import psycopg
from psycopg.rows import dict_row

con = psycopg.connect(                               # TCP + login + a server process
    "postgresql://student:student@localhost:5432/course",
    row_factory=dict_row,                            # rows ARE dicts
)
# foreign keys: always on, nothing to set

sql = """
    SELECT customer_id, COUNT(*) AS n, SUM(amount) AS total
    FROM purchases
    WHERE customer_id = %(customer_id)s
    GROUP BY customer_id
"""
row = con.execute(sql, {"customer_id": 1}).fetchone()
print(row)             # {'customer_id': 1, 'n': 4, 'total': Decimal('40.28')}

con.close()            # also ROLLs BACK the transaction that SELECT opened (§4)
```

Same shape, same method names. The SQL is identical **except for the placeholder**, and the answer comes back as a different type.

---

## 2. Line by line: what changed

| Step | `sqlite3` | `psycopg` 3 | Why |
| :--- | :--- | :--- | :--- |
| Install | nothing | `pip install "psycopg[binary]"` | SQLite ships with Python; PostgreSQL needs a client library |
| Connect | `sqlite3.connect("file.db")` | `psycopg.connect("postgresql://user:pw@host:port/db")` | a file path vs. a network address plus credentials |
| Cost of connecting | microseconds | milliseconds (more over the internet) | the server forks a process per connection |
| Rows as dicts | `con.row_factory = sqlite3.Row`, then `dict(row)` | `row_factory=dict_row` | |
| Named parameter | `:customer_id` | `%(customer_id)s` | see [§3](#3-placeholders-and-the--trap) |
| Positional parameter | `?` | `%s` | |
| Literal `%` in SQL (with params) | `'G%'` | `'G%%'` | see [§3](#3-placeholders-and-the--trap) |
| Per-connection setup | `PRAGMA foreign_keys = ON`, `busy_timeout`, ... | `SET statement_timeout`, `SET lock_timeout` | |
| When a transaction starts | before `INSERT`/`UPDATE`/`DELETE` only | before **any** statement, including `SELECT` | see [§4](#4-transactions-who-says-begin) |
| `with con:` | commit or roll back, connection stays open | commit or roll back, then **close** | |
| Explicit transaction block | none built in | `with con.transaction():` | |
| Query plan | `EXPLAIN QUERY PLAN ...`, column `detail` | `EXPLAIN ...`, column `QUERY PLAN` | |
| Constraint failure | `sqlite3.IntegrityError` | `psycopg.errors.NotNullViolation`, `UniqueViolation`, ... (all subclasses of `psycopg.IntegrityError`) | |
| Lock trouble | `sqlite3.OperationalError: database is locked` | `LockNotAvailable`, `SerializationFailure`, `DeadlockDetected` | [sqlite_vs_postgres §8](sqlite_vs_postgres.md#8-concurrency-and-transactions) |
| Many requests | a new connection per request is fine | open a **pool** once at startup (`psycopg_pool.ConnectionPool`) | connecting is expensive |

The DB-API standard is why the right-hand column looks familiar at all: both modules have `connect()`, `execute()`, `fetchone()`, `fetchall()`, `commit()`, `rollback()`, and the same exception names (`IntegrityError`, `OperationalError`, ...).

---

## 3. Placeholders and the `%` trap

**Never build SQL with f-strings.** Both drivers send the parameter values separately from the SQL text, so a customer named `'; DROP TABLE purchases; --` is just a strange name, not an attack. Only the placeholder *spelling* differs:

| Style | `sqlite3` | `psycopg` |
| :--- | :--- | :--- |
| named, pass a `dict` | `WHERE id = :id` | `WHERE id = %(id)s` |
| positional, pass a `tuple` | `WHERE id = ?` | `WHERE id = %s` |

Here's what goes wrong with an f-string:

```python
sql = f"SELECT * FROM customers WHERE customer_id = {customer_id}"
# customer_id = "0 OR 1=1"   → every customer comes back
# name = "O'Brien"           → syntax error from the unbalanced quote
# value = None               → the text None, not NULL
```

Placeholders fix all three. The driver handles quoting, `NULL`, dates, and decimals, and the same SQL text can reuse a cached plan.

**The exception: names, not values.** A placeholder can stand in only for a **value**. It can't stand in for a table name, a column name, `ASC`/`DESC`, or a `PRAGMA` setting. When those have to vary, building the string is unavoidable. It's safe when the text comes from your own code, or from user input that you've checked against a fixed list:

```python
SORTABLE = {"amount", "purchase_date"}
if sort_col not in SORTABLE:                         # user input → only names you chose
    raise HTTPException(400, f"can't sort by {sort_col!r}")
sql = f"SELECT * FROM purchases ORDER BY {sort_col} DESC LIMIT :n"   # the value is still a placeholder
```

Assignment 01's `experiment.py` does the same thing with `f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}"`. A `PRAGMA` can't take a parameter, and the value is an `int` from the app's own configuration. For PostgreSQL identifiers that you have to build, `psycopg.sql.Identifier` quotes them safely.

> **Rule of thumb:** an f-string may insert a **name you chose**. Every **value** goes through a placeholder.

`psycopg`'s style comes from Python's old `%` string formatting, and that brings a trap: **once you pass parameters, every `%` in the SQL is special**, even one inside a string literal.

```python
# Works in sqlite3 (with ? in place of %s), breaks in psycopg:
con.execute("SELECT * FROM purchases WHERE department LIKE 'G%' AND amount > %s", (1,))
# psycopg.ProgrammingError: only '%s', '%b', '%t' are allowed as placeholders, got '%''

# Fixed: double the literal %
con.execute("SELECT * FROM purchases WHERE department LIKE 'G%%' AND amount > %s", (1,))
```

The same goes for the modulo operator (`7 % 3` becomes `7 %% 3`). With **no** parameters, `psycopg` leaves `%` alone, which makes the bug confusing: a query works until the day you add a parameter to it.

Two things that look like placeholders but aren't:

- **`::` casts** in PostgreSQL: `day - (ROW_NUMBER() OVER (ORDER BY day))::int`. That `:int` is not a parameter named `int`.
- **Anything inside quotes:** `WHERE note = ':not_a_param'`.

So converting `:name` to `%(name)s` with a plain search-and-replace is wrong. [`dbrun.to_pyformat`](code/dbrun.py) skips over quotes, comments, and casts before it rewrites anything:

```python
>>> to_pyformat("SELECT * FROM t WHERE id = :id AND name LIKE 'a%' AND x::int > ?")
"SELECT * FROM t WHERE id = %(id)s AND name LIKE 'a%%' AND x::int > %s"
```

---

## 4. Transactions: who says `BEGIN`?

Neither driver starts in the "every statement commits by itself" mode you get in the `sqlite3` shell or `psql`. Each one quietly sends `BEGIN` for you, at a different moment.

**`sqlite3` (default settings):** it sends `BEGIN` just before an `INSERT`, `UPDATE`, `DELETE`, or `REPLACE`, and leaves that transaction open until you call `commit()`. `SELECT` doesn't start one. Forget `commit()` and your inserts disappear when the connection closes. Leave the transaction open and you hold the database's **only** write lock.

**`psycopg` (default settings):** it sends `BEGIN` before the **first statement of any kind, including `SELECT`**. A read-only API route that never commits leaves its connection `idle in transaction` on the server. That holds back `VACUUM` ([sqlite_vs_postgres §7](sqlite_vs_postgres.md#7-storage-mvcc-and-vacuum)) and, on the class server, ties up one of your limited connections. You can spot it:

```sql
SELECT pid, state, now() - xact_start AS open_for, query
FROM pg_stat_activity
WHERE state = 'idle in transaction';
```

The fix is the same for both: **turn the hidden `BEGIN` off and be explicit.**

```python
# sqlite3: autocommit; you write BEGIN/COMMIT when you want a transaction
con = sqlite3.connect("file.db", isolation_level=None)
con.execute("BEGIN IMMEDIATE")      # take the write lock now, not halfway through
...
con.execute("COMMIT")

# psycopg: autocommit; a transaction is a with-block
con = psycopg.connect(url, autocommit=True)
with con.transaction():             # BEGIN ... COMMIT, or ROLLBACK on an exception
    ...
```

(Python 3.12+ also accepts `sqlite3.connect(..., autocommit=True)`. Its behavior differs slightly; `isolation_level=None` works on every version.)

Once both connections run in autocommit mode, they behave the same: a statement outside a transaction commits immediately, and a transaction lasts exactly as long as you say. That is the setup `dbrun` uses.

---

## 5. What comes back: same query, different Python types

The demo ([§7](#7-run-the-demo)) inserts the same four purchases into each database and reads them back:

| Expression | SQLite gives Python | PostgreSQL gives Python |
| :--- | :--- | :--- |
| `SUM(amount)` for $19.99 + $0.10 + $0.20 + $19.99 | `40.279999999999994` (`float`) | `Decimal('40.28')` |
| `amount` for $45.00 | `45` (`int`!) | `Decimal('45.00')` |
| `purchase_date` | `'2026-01-15'` (`str`) | `datetime.date(2026, 1, 15)` |
| `COUNT(*)` | `int` | `int` |
| `department LIKE 'games'` matches | 3 rows | 0 rows |
| a `NOT NULL` violation raises | `sqlite3.IntegrityError` | `psycopg.errors.NotNullViolation` |

Why:

- SQLite has no decimal or date types ([sqlite_vs_postgres §3](sqlite_vs_postgres.md#3-types-and-strictness)). A `NUMERIC` column stores `45.00` as the integer `45` and `0.10` as a float. A date is whatever text you stored.
- PostgreSQL's `numeric(10,2)` and `date` are real types, and `psycopg` converts them to the matching Python types: `decimal.Decimal` and `datetime.date`.

What this means for your code:

- **JSON:** FastAPI serializes `Decimal`, `date`, `float`, and `str` without complaint, so your API keeps working. But a client that compares `"amount": 45` to `"amount": "45.00"` will notice the change.
- **Arithmetic:** `Decimal('40.28') + 0.1` raises `TypeError`. Mixing `Decimal` with `float` in Python is an error, not a rounding problem.
- **Comparisons:** `row["purchase_date"] == "2026-01-15"` is `True` on SQLite and `False` on PostgreSQL (a `date` never equals a `str`).
- **Tests:** a test that passes on SQLite can fail on PostgreSQL for any of these reasons. If production runs PostgreSQL, test against PostgreSQL.

No wrapper should paper over this. Converting every `Decimal` to `float` would bring back the rounding errors PostgreSQL just got rid of.

---

## 6. One interface for both: `dbrun.Database`

[`code/dbrun.py`](code/dbrun.py) is about 200 lines, most of them comments. You choose the database with a URL and write every query once, SQLite-style:

```python
from dbrun import Database

db = Database("sqlite:///data/idx_100k.db")
# db = Database("postgresql://student:student@localhost:5432/course")   # same code below

rows = db.query("SELECT * FROM purchases WHERE customer_id = :cid LIMIT 5", {"cid": 1})
row  = db.query_one("SELECT COUNT(*) AS n FROM purchases")
n    = db.execute("DELETE FROM purchases WHERE purchase_id = :id", {"id": 99})   # rows affected

with db.transaction():                       # COMMIT at the end, ROLLBACK on an exception
    db.execute("UPDATE ...", {...})
    db.execute("INSERT ...", {...})

try:
    db.execute("INSERT INTO purchases ... VALUES (:cust, ...)", {"cust": None})
except db.IntegrityError:                    # the right class for whichever driver
    ...

print(db.explain("SELECT ...", {...}))       # EXPLAIN QUERY PLAN or EXPLAIN
print(db.timed_query("SELECT ...", {...}))   # Assignment 01's {elapsed_ms, row_count, plan, rows}
db.close()
```

| Method | Returns | Notes |
| :--- | :--- | :--- |
| `query(sql, params)` | `list[dict]` | `SELECT`, or anything with `RETURNING` |
| `query_one(sql, params)` | `dict` or `None` | first row |
| `execute(sql, params)` | `int` rows affected | `INSERT` / `UPDATE` / `DELETE` / DDL |
| `execute_many(sql, list_of_params)` | `None` | bulk insert; wrap it in `transaction()` |
| `transaction()` | context manager | not nestable |
| `explain(sql, params)` | `list[str]` | the plan; doesn't run the query |
| `timed_query(sql, params)` | `dict` | same envelope as `run_query` in `app/experiment.py` |
| `.kind` | `"sqlite"` or `"postgres"` | for the few places you still need to branch |
| `.IntegrityError`, `.OperationalError`, `.Error` | exception classes | from the active driver |

### How it works

The whole trick is in one method. Everything else is a thin pass-through.

```python
def _run(self, sql, params):
    if not params:
        return self.con.execute(sql)          # no params: send SQL untouched
    if self.kind == "postgres":
        sql = to_pyformat(sql)                # :name -> %(name)s,  ? -> %s,  % -> %%
    return self.con.execute(sql, params)
```

The constructor does the rest of the evening-out:

| | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| autocommit | `isolation_level=None` | `autocommit=True` |
| rows as dicts | `sqlite3.Row` | `dict_row` |
| safety settings | `PRAGMA foreign_keys = ON` | `SET lock_timeout = '5000ms'` |
| `transaction()` | `BEGIN IMMEDIATE` ... `COMMIT` / `ROLLBACK` | `con.transaction()` |

### What it hides, and what it doesn't

| Hidden | **Not** hidden |
| :--- | :--- |
| Connecting | SQL dialect: `substr` on a date, `julianday`, `ILIKE`, `INSERT OR IGNORE`, ... ([sqlite_vs_postgres §4](sqlite_vs_postgres.md#4-porting-the-15-queries), [§14](sqlite_vs_postgres.md#14-cheat-sheet)) |
| Placeholder spelling and `%` escaping | DDL: `INTEGER PRIMARY KEY` vs. `GENERATED ... AS IDENTITY` |
| Dict rows | Return types: `float`/`str` vs. `Decimal`/`date` ([§5](#5-what-comes-back-same-query-different-python-types)) |
| When transactions start | Concurrency behavior: one writer vs. row locks |
| `EXPLAIN` syntax | Plan **contents**: `SCAN purchases` vs. `Seq Scan on purchases` |
| Which `IntegrityError` class to catch | Specific Postgres errors (`SerializationFailure`, ...): catch them from `psycopg.errors` |

Known limits, on purpose, to keep it short:

- **One connection per `Database`.** Fine for scripts and experiments. A PostgreSQL-backed API that serves many requests at once should use a pool ([§8](#8-using-it-in-the-api)).
- **No mixing** `:name` and `?` in one query. `psycopg` refuses that too.
- **PostgreSQL's `jsonb` `?` operators** (`data ? 'key'`) would be mistaken for placeholders. Use the function form, `jsonb_exists(data, 'key')`.
- **`transaction()` doesn't nest.** `psycopg` supports nesting (as savepoints); SQLite's `BEGIN` doesn't.

---

## 7. Run the demo

[`code/demo.py`](code/demo.py) runs one set of queries against an in-memory SQLite database and then against PostgreSQL. It uses `TEMP` tables, so it leaves nothing behind in either one.

```bash
cd Lectures/03_postgres/code
pip install "psycopg[binary]"
python demo.py                                         # local Docker Postgres
PG_URL=postgresql://me:pw@host:5432/db python demo.py  # any other server
```

If PostgreSQL isn't running, the SQLite half still runs and the script tells you why it skipped the rest. Output (trimmed):

```text
=== Database(sqlite: sqlite:///:memory:) ===
  customer 1 totals            {'customer_id': 1, 'n': 4, 'total': 40.279999999999994}
  type(total)                  float
  type(purchase_date)          str  '2026-01-15'
  LIKE 'G%' AND amount > 1     [{'department': 'Games', 'amount': 19.99}, ..., {'department': 'Garden', 'amount': 45}]
  LIKE 'games' matches         3
  IntegrityError caught        IntegrityError
  rows before / after          5 / 5  (rolled back)
  plan:
      SCAN purchases

=== Database(postgres: localhost:5432/course) ===
  customer 1 totals            {'customer_id': 1, 'n': 4, 'total': Decimal('40.28')}
  type(total)                  Decimal
  type(purchase_date)          date  datetime.date(2026, 1, 15)
  LIKE 'G%' AND amount > 1     [{'department': 'Games', 'amount': Decimal('19.99')}, ..., {'department': 'Garden', 'amount': Decimal('45.00')}]
  LIKE 'games' matches         0
  IntegrityError caught        NotNullViolation
  rows before / after          5 / 5  (rolled back)
  plan:
      GroupAggregate  (cost=0.00..21.03 rows=1 width=44)
        ->  Seq Scan on purchases  (cost=0.00..21.00 rows=4 width=20)
              Filter: (customer_id = '1'::smallint)
```

Every query in the demo except the `CREATE TABLE` is written once. Look at what still came out different. (The `'1'::smallint` in the plan is `psycopg` telling the server the parameter's type: it picks the smallest integer type that fits the Python value.)

---

## 8. Using it in the API

Assignment 01 opened a new SQLite connection for every request in `get_exp_db` and timed queries in `run_query`. Here's the same pattern on `Database`:

```python
from fastapi import Depends
from dbrun import Database

DB_URL = os.environ.get("DB_URL", "sqlite:///data/idx_100k.db")

def get_db():
    db = Database(DB_URL)
    try:
        yield db
    finally:
        db.close()

@app.get("/customers/{customer_id}")
def q01_customer(customer_id: int, db: Database = Depends(get_db)):
    return db.timed_query(Q01_SQL, {"customer_id": customer_id})
```

Switching the environment variable switches the database. That's the payoff, and it's also how you'll run the same 15 queries against both databases for a fair comparison.

**For SQLite, a connection per request is fine.** Opening a file takes microseconds.

**For PostgreSQL, it isn't.** Each request would pay for a TCP handshake, a login, and a new server process: a few milliseconds locally, much more to the class server, and one more connection counted against your limit. The standard fix is a pool, opened once when the app starts:

```python
from psycopg_pool import ConnectionPool      # pip install psycopg-pool

pool = ConnectionPool(DB_URL, min_size=2, max_size=10,
                      kwargs={"autocommit": True, "row_factory": dict_row})

def get_pg():
    with pool.connection() as con:           # borrow; returned to the pool afterward
        yield con
```

Adding pool support to `Database` (accepting a borrowed connection instead of opening one) is a good exercise. Keep `max_size` × number of `uvicorn` workers under your connection limit on the class server.

---

## 9. The industrial-strength version

`dbrun` exists so you can see every moving part. In production code, the usual choice is **SQLAlchemy Core**, which does the same job:

```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg://student:student@localhost/course")
# engine = create_engine("sqlite:///data/idx_100k.db")

with engine.connect() as con:
    rows = con.execute(text("SELECT * FROM purchases WHERE customer_id = :cid"),
                       {"cid": 1}).mappings().all()
```

`text()` accepts `:name` placeholders and translates them for each driver, the way `to_pyformat` does. The engine also gives you connection pooling, and you still write the SQL yourself. (SQLAlchemy's ORM, which generates SQL from Python classes, is a separate layer. You don't need it to get these benefits.)

Even SQLAlchemy can't make `substr(purchase_date, 1, 7)` work on a PostgreSQL `date`, or turn a `Decimal` into a `float` without losing exactness. Dialect and type differences are the part of porting that stays your job.

---

## 10. Check your understanding

1. This query works in `psycopg` with no parameters, but fails once you add `AND customer_id = %(cid)s`. Why, and what's the fix? `SELECT * FROM products WHERE product_name LIKE '%mouse%'`
2. Why can't `to_pyformat` just run `re.sub(r":(\w+)", r"%(\1)s", sql)`? Give two SQL snippets that would break.
3. A read-only FastAPI route uses `psycopg` with default settings and never calls `commit()`. Nothing fails, but `pg_stat_activity` fills with `idle in transaction`. What started those transactions, and name two problems they cause.
4. Your SQLite test asserts `row["amount"] == 45.0` and `row["purchase_date"] == "2026-02-03"`. Which of the two assertions fail on PostgreSQL, and why?
5. Why does `Database.transaction()` use `BEGIN IMMEDIATE` on SQLite instead of plain `BEGIN`? (Hint: [sqlite_vs_postgres §8](sqlite_vs_postgres.md#8-concurrency-and-transactions), deadlocks.)
6. `Database` exposes `db.IntegrityError`. Why does `except db.IntegrityError` catch `psycopg.errors.NotNullViolation`?
7. List three differences between SQLite and PostgreSQL that `Database` deliberately does **not** hide, and explain why hiding each one would be a bad idea.
8. A route accepts `?order=amount` and builds `f"... ORDER BY {order}"`. Why can't you use `ORDER BY :order` instead? What makes the f-string version safe, and what would make it dangerous?
