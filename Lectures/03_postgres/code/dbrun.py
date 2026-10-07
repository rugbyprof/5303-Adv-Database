"""One small interface for running SQL on SQLite or PostgreSQL.

Pick the database with a URL; write every query the SQLite way (``:name``
placeholders); get back a list of dicts either way.

    from dbrun import Database

    db = Database("sqlite:///data/idx_100k.db")              # a file
    db = Database("postgresql://student:student@localhost:5432/course")

    rows = db.query("SELECT * FROM customers WHERE customer_id = :id", {"id": 7})
    one  = db.query_one("SELECT COUNT(*) AS n FROM purchases")
    db.execute("UPDATE products SET price = price * 1.1 WHERE product_id = :id", {"id": 3})

    with db.transaction():                 # all or nothing, on both databases
        db.execute(...)
        db.execute(...)

Both drivers follow the same Python standard (DB-API 2.0, PEP 249), so most of
this class is plumbing. The real differences it hides are:

1. Placeholders. sqlite3 wants ``:name`` / ``?``; psycopg wants ``%(name)s`` /
   ``%s`` and treats every other ``%`` as special. ``to_pyformat`` rewrites them.
2. Rows as dicts. ``sqlite3.Row`` vs. psycopg's ``dict_row``.
3. Transactions. Both connections are opened in autocommit mode, so every
   statement commits on its own unless it's inside ``with db.transaction():``.
4. EXPLAIN. ``EXPLAIN QUERY PLAN`` vs. ``EXPLAIN``.

What it does NOT hide: SQL dialect differences (``substr`` on a date,
``julianday``, ``LIKE`` case rules, ...) and the Python types that come back
(``float``/``str`` from SQLite, ``Decimal``/``date`` from PostgreSQL). See
../python_sqlite_vs_postgres.md.
"""

from __future__ import annotations

import re
import sqlite3
import time
from contextlib import contextmanager
from collections.abc import Generator, Mapping, Sequence
from typing import Any

Params = Mapping[str, Any] | Sequence[Any] | None


# ---------------------------------------------------------------------------
# Placeholder translation:  :name -> %(name)s,  ? -> %s,  % -> %%
# ---------------------------------------------------------------------------

# Order matters: the first alternative that matches wins, so string literals,
# quoted identifiers, comments, and "::" casts are consumed before we look for
# placeholders. That keeps  WHERE note = ':not_a_param'  and  x::int  intact.
_TOKEN = re.compile(
    r"""
      (?P<literal> '(?:[^']|'')*'          # 'string literal'
                 | "(?:[^"]|"")*"          # "Quoted Identifier"
                 | --[^\n]*                # -- line comment
                 | /\*.*?\*/               # /* block comment */
                 | \$(?P<tag>\w*)\$.*?\$(?P=tag)\$   # $$ dollar quoted $$
      )
    | (?P<cast>  ::)                       # PostgreSQL cast, not a placeholder
    | :(?P<name> [A-Za-z_]\w*)             # :named placeholder
    | (?P<qmark> \?)                       # ? positional placeholder
    | (?P<pct>   %)                        # bare % (e.g. in a LIKE pattern)
    """,
    re.VERBOSE | re.DOTALL,
)


def to_pyformat(sql: str) -> str:
    """Rewrite SQLite-style placeholders into psycopg's style.

    >>> to_pyformat("SELECT * FROM t WHERE id = :id AND name LIKE 'a%' AND x::int > ?")
    "SELECT * FROM t WHERE id = %(id)s AND name LIKE 'a%%' AND x::int > %s"

    psycopg looks for % everywhere -- even inside string literals -- whenever
    parameters are passed, so every literal % must be doubled.
    """

    def swap(m: re.Match) -> str:
        if m.group("literal") is not None:
            return m.group("literal").replace("%", "%%")
        if m.group("cast"):
            return "::"
        if m.group("name"):
            return f"%({m.group('name')})s"
        if m.group("qmark"):
            return "%s"
        return "%%"

    return _TOKEN.sub(swap, sql)


# ---------------------------------------------------------------------------
# The Database class
# ---------------------------------------------------------------------------


class Database:
    """A connection to SQLite or PostgreSQL behind one interface.

    url examples
        sqlite:///relative/path.db      sqlite:////absolute/path.db
        sqlite:///:memory:              postgresql://user:pw@host:5432/dbname
    """

    # A sqlite3.Connection or a psycopg.Connection, decided at runtime by the
    # URL. The type checker can't follow self.kind, so we tell it "either".
    con: Any

    def __init__(self, url: str, *, timeout_s: float = 5.0) -> None:
        self.url = url
        if url.startswith("sqlite:///"):
            self.kind = "sqlite"
            self.driver = sqlite3
            self.con = sqlite3.connect(
                url.removeprefix("sqlite:///"),
                timeout=timeout_s,          # how long to wait for the write lock
                isolation_level=None,       # autocommit; we issue BEGIN ourselves
                check_same_thread=False,    # FastAPI may hop threads mid-request
            )
            self.con.row_factory = sqlite3.Row
            self.con.execute("PRAGMA foreign_keys = ON")   # off by default!
        elif url.startswith(("postgresql://", "postgres://")):
            # Imported here, not at the top, so SQLite works without psycopg.
            try:
                import psycopg
                from psycopg.rows import dict_row
            except ImportError as exc:
                raise ImportError('PostgreSQL needs psycopg:  pip install "psycopg[binary]"') from exc
            self.kind = "postgres"
            self.driver = psycopg
            self.con = psycopg.connect(
                url,
                autocommit=True,            # match SQLite: no hidden open transaction
                # psycopg 3.3's type hints reject dict_row under recent Pyright,
                # even in psycopg's own docs example. It works at runtime.
                row_factory=dict_row,  # pyright: ignore[reportArgumentType]
                connect_timeout=int(timeout_s),
            )
            # Never wait forever on a row lock or a runaway query.
            self.con.execute(f"SET lock_timeout = '{int(timeout_s * 1000)}ms'")
        else:
            raise ValueError(f"unknown database url: {url!r}")

        # Same exception names exist in both drivers (DB-API 2.0), so callers
        # can write   except db.IntegrityError:   without knowing which one.
        self.IntegrityError = self.driver.IntegrityError
        self.OperationalError = self.driver.OperationalError
        self.Error = self.driver.Error

    # -- the one place the two drivers really differ ------------------------

    def _run(self, sql: str, params: Params):
        """Execute one statement and return the driver's cursor."""
        if not params:
            # No params: send the SQL untouched (psycopg then leaves % alone).
            return self.con.execute(sql)
        if self.kind == "postgres":
            sql = to_pyformat(sql)
        return self.con.execute(sql, params)

    # -- public API ---------------------------------------------------------

    def query(self, sql: str, params: Params = None) -> list[dict[str, Any]]:
        """Run a SELECT (or anything with RETURNING); return every row as a dict."""
        return [dict(r) for r in self._run(sql, params).fetchall()]

    def query_one(self, sql: str, params: Params = None) -> dict[str, Any] | None:
        """First row as a dict, or None."""
        row = self._run(sql, params).fetchone()
        return dict(row) if row is not None else None

    def execute(self, sql: str, params: Params = None) -> int:
        """Run INSERT / UPDATE / DELETE / DDL; return the number of rows affected."""
        return self._run(sql, params).rowcount

    def execute_many(self, sql: str, rows: Sequence[Params]) -> None:
        """Run one statement once per parameter set, e.g. a bulk INSERT."""
        if self.kind == "postgres":
            sql = to_pyformat(sql)
            with self.con.cursor() as cur:
                cur.executemany(sql, rows)
        else:
            self.con.executemany(sql, rows)

    @contextmanager
    def transaction(self) -> Generator[None, None, None]:
        """COMMIT if the block finishes, ROLLBACK if it raises. Not nestable."""
        if self.kind == "postgres":
            with self.con.transaction():
                yield
            return
        # BEGIN IMMEDIATE takes SQLite's write lock up front, so two writers
        # queue at BEGIN instead of failing halfway through (see sqlite_vs_postgres §8).
        self.con.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.con.execute("ROLLBACK")
            raise
        self.con.execute("COMMIT")

    def explain(self, sql: str, params: Params = None) -> list[str]:
        """The query plan, one line per step (the query itself is NOT run)."""
        if self.kind == "postgres":
            return [r["QUERY PLAN"] for r in self.query("EXPLAIN " + sql, params)]
        return [r["detail"] for r in self.query("EXPLAIN QUERY PLAN " + sql, params)]

    def timed_query(self, sql: str, params: Params = None) -> dict[str, Any]:
        """Same envelope as Assignment 01's run_query: rows, plan, elapsed_ms."""
        plan = self.explain(sql, params)
        t0 = time.perf_counter()
        rows = self.query(sql, params)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "db": self.kind,
            "elapsed_ms": round(elapsed_ms, 3),
            "row_count": len(rows),
            "plan": plan,
            "rows": rows,
        }

    def close(self) -> None:
        self.con.close()

    def __enter__(self) -> Database:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Database({self.kind}: {self.url.split('@')[-1]})"  # hide the password
