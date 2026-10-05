"""Database connection helper.

One connection per request (see ``get_db`` in main.py). SQLite is happy with
that as long as every connection sets the same pragmas.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

# Override with  DB_PATH=/some/where/store.db  in the environment.
DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).resolve().parent.parent / "store.db"))


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(
        DB_PATH,
        # FastAPI runs sync endpoints in a threadpool, so a connection may be
        # created on one thread and used on another within a request.
        check_same_thread=False,
        # wait up to 5s for a lock instead of failing immediately with
        # "database is locked" -- Phase 4 explores where this stops helping.
        timeout=5.0,
    )
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode = WAL")     # readers don't block the writer
    con.execute("PRAGMA foreign_keys = ON")      # not the default; per connection
    con.execute("PRAGMA busy_timeout = 5000")
    con.execute("PRAGMA synchronous = NORMAL")   # safe with WAL, faster than FULL
    return con


def explain(con: sqlite3.Connection, sql: str, params: tuple = ()) -> list[str]:
    """Return the EXPLAIN QUERY PLAN lines for a statement -- use this in your
    FINDINGS.md write-ups."""
    rows = con.execute(f"EXPLAIN QUERY PLAN {sql}", params).fetchall()
    return [r["detail"] for r in rows]
