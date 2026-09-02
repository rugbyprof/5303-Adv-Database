"""
Assignment 01 -- SQLite behind a FastAPI service.

Run:
    uvicorn app.main:app --reload        # from the starter/ directory
    open http://127.0.0.1:8000/docs

Phase 1 endpoints below are worked examples. Phases 2-4 are stubs that return
501 -- implement them and remove the `raise`. See ../README.md for the spec.
"""

from __future__ import annotations

import sqlite3
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException, Query

from . import models
from .auth import require_api_key
from .db import connect

app = FastAPI(title="SQLite API -- Assignment 01")


def get_db() -> Iterator[sqlite3.Connection]:
    con = connect()
    try:
        yield con
    finally:
        con.close()


# --------------------------------------------------------------------------- #
# Phase 1 -- simple reads (worked examples)
# --------------------------------------------------------------------------- #

@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/customers/{customer_id}", response_model=models.Customer,
         dependencies=[Depends(require_api_key)])
def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        """
        SELECT c.customer_id, c.first_name, c.last_name, c.email,
               c.address, c.zipcode, z.state_code
        FROM customers c
        JOIN zipcodes z ON z.zipcode = c.zipcode
        WHERE c.customer_id = ?
        """,
        (customer_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(404, f"no customer {customer_id}")
    return dict(row)


@app.get("/departments", dependencies=[Depends(require_api_key)])
def list_departments(db: sqlite3.Connection = Depends(get_db)) -> list[str]:
    return [r["department"] for r in db.execute("SELECT department FROM departments ORDER BY 1")]


@app.get("/products", response_model=list[models.Product],
         dependencies=[Depends(require_api_key)])
def list_products(
    db: sqlite3.Connection = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    # NOTE: OFFSET pagination. Fine here; Phase 3 shows why it stops being fine.
    rows = db.execute(
        "SELECT product_id, product_name, unit_price FROM products "
        "ORDER BY product_id LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [dict(r) for r in rows]


@app.get("/purchases", response_model=list[models.Purchase],
         dependencies=[Depends(require_api_key)])
def list_purchases(
    db: sqlite3.Connection = Depends(get_db),
    start: str = Query(..., description="inclusive ISO date, e.g. 2025-01-01"),
    end: str = Query(..., description="exclusive ISO date"),
    limit: int = Query(100, ge=1, le=1000),
):
    rows = db.execute(
        """
        SELECT purchase_id, customer_id, product_id, department, amount, purchase_date
        FROM purchases
        WHERE purchase_date >= ? AND purchase_date < ?
        ORDER BY purchase_date
        LIMIT ?
        """,
        (start, end, limit),
    ).fetchall()
    return [dict(r) for r in rows]


# --------------------------------------------------------------------------- #
# Phase 2 -- joins & aggregates            (implement these)
# --------------------------------------------------------------------------- #

_TODO = "not implemented -- see Assignments/01_sqlite_api/README.md"


@app.get("/customers/{customer_id}/purchases",
         response_model=list[models.PurchaseDetail],
         dependencies=[Depends(require_api_key)])
def customer_purchases(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/stats/revenue-by-state", response_model=list[models.RevenueRow],
         dependencies=[Depends(require_api_key)])
def revenue_by_state(db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/stats/revenue-by-month", response_model=list[models.RevenueRow],
         dependencies=[Depends(require_api_key)])
def revenue_by_month(db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/products/top", response_model=list[models.RevenueRow],
         dependencies=[Depends(require_api_key)])
def top_products(
    db: sqlite3.Connection = Depends(get_db),
    by: str = Query("revenue", pattern="^(revenue|count)$"),
    limit: int = Query(10, ge=1, le=100),
):
    raise HTTPException(501, _TODO + " (Phase 2)")


# --------------------------------------------------------------------------- #
# Phase 3 -- gnarly queries                (implement all 8 + 2 of your own)
# --------------------------------------------------------------------------- #

@app.get("/products/search", dependencies=[Depends(require_api_key)])
def search_products(q: str, db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: LIKE '%q%' -> then FTS5)")


@app.get("/customers/leaderboard", dependencies=[Depends(require_api_key)])
def leaderboard(db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: 90-day trailing spend window)")


@app.get("/customers/{customer_id}/streaks", dependencies=[Depends(require_api_key)])
def streaks(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: gaps-and-islands)")


@app.get("/reports/cube", dependencies=[Depends(require_api_key)])
def cube(db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: state x department x month)")


@app.get("/purchases/sample", dependencies=[Depends(require_api_key)])
def sample(db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: ORDER BY random() LIMIT 10)")


@app.get("/products/dead", dependencies=[Depends(require_api_key)])
def dead_products(state: str, db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 3: anti-join / NOT EXISTS)")


# --------------------------------------------------------------------------- #
# Phase 4 -- writes & concurrency          (implement, then hammer it)
# --------------------------------------------------------------------------- #

@app.post("/purchases", status_code=201, dependencies=[Depends(require_api_key)])
def create_purchase(body: models.NewPurchase, db: sqlite3.Connection = Depends(get_db)):
    raise HTTPException(501, _TODO + " (Phase 4: INSERT in a transaction, return 201)")
