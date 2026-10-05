"""Helpers for the experiment routes (see ../QUERIES.md).

Every experiment route takes a ``?db=`` query parameter that picks one of the
databases ``make_dbs.py`` built in ``data/``, and returns the same envelope:

    {"elapsed_ms": 0.42, "row_count": 10, "plan": ["SEARCH ..."], "rows": [...]}

Usage in main.py:

    from .experiment import get_exp_db, run_query

    @app.get("/customers/{customer_id}")
    def q01_customer(customer_id: int, db: sqlite3.Connection = Depends(get_exp_db)):
        return run_query(db, Q01_SQL, {"customer_id": customer_id})
"""

from __future__ import annotations

import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterator

from fastapi import HTTPException, Query

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))

# Phase 4 sets this to 0 to watch "database is locked" happen.
BUSY_TIMEOUT_MS = int(os.environ.get("BUSY_TIMEOUT_MS", "5000"))

# idx_10k, noidx_1m, ... plus the scratch copy Phase 4 writes into
DB_NAME_PATTERN = r"^((idx|noidx)_(10k|100k|1m)|writes)$"


def get_exp_db(
    db: str = Query("idx_100k", pattern=DB_NAME_PATTERN,
                    description="which database in data/ to query, e.g. noidx_1m"),
) -> Iterator[sqlite3.Connection]:
    path = DATA_DIR / f"{db}.db"
    if not path.exists():
        raise HTTPException(404, f"{path.name} not found -- run  python make_dbs.py")
    # journal_mode=WAL is already stored in the file by make_dbs.py
    con = sqlite3.connect(path, check_same_thread=False, timeout=BUSY_TIMEOUT_MS / 1000)
    con.row_factory = sqlite3.Row
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
        con.execute("PRAGMA synchronous = NORMAL")
    except sqlite3.OperationalError as exc:   # can be "database is locked" under load
        con.close()
        raise HTTPException(503, f"database error: {exc}") from exc
    try:
        yield con
    finally:
        con.close()


def run_query(con: sqlite3.Connection, sql: str, params: dict[str, Any] | None = None) -> dict:
    """Run one SELECT and return its rows, its query plan, and how long it took.

    elapsed_ms times only execute + fetchall -- the database work -- not the
    HTTP round trip, JSON encoding, or the EXPLAIN itself.
    """
    params = params or {}
    plan = [r["detail"] for r in con.execute("EXPLAIN QUERY PLAN " + sql, params)]

    t0 = time.perf_counter()
    rows = con.execute(sql, params).fetchall()
    elapsed_ms = (time.perf_counter() - t0) * 1000

    return {
        "elapsed_ms": round(elapsed_ms, 3),
        "row_count": len(rows),
        "plan": plan,
        "rows": [dict(r) for r in rows],
    }
