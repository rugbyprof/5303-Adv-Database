"""
Assignment 01 -- SQLite behind a FastAPI service.

Run it from the  starter/  directory, either way:
    python -m app.main                   # uses the __main__ block below
    uvicorn app.main:app --reload        # equivalent

Then open http://127.0.0.1:8001/docs

(Do NOT run `python app/main.py` -- the package-relative imports need the
`app.` package context, which only `-m app.main` / uvicorn provide.)

Phase 1 endpoints below are worked examples. Phases 2-4 are stubs that return
501 -- implement them and remove the `raise`. See ../README.md for the spec.
"""

from __future__ import annotations

import sqlite3
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from .auth import require_api_key
from .db import connect
from .models import (
    Customer,
    NewPurchase,
    Product,
    Purchase,
    PurchaseDetail,
    RevenueRow,
)

app = FastAPI(title="SQLite API -- Assignment 01")


# def get_db() -> Iterator[sqlite3.Connection]:
#     con = connect()
#     try:
#         yield con
#     finally:
#         con.close()

conn = connect()


def custom_response(**kwargs):
    """
    Packages a response from a sqlite query to give a bit of consistency to each result


    :param query: The query that was run
    :param result: The results of the query, if any
    :param offset: Integer specifying the number of rows to skip.
    :param limit: Integer specifying the maximum number of rows to return.
    :param error: Error if any
    :return: List of dictionary's with all the info listed above
    """

    result = kwargs.get("result",[])
    query = kwargs.get("query", None)
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit", 10)  # Assuming a default limit might be helpful
    error = kwargs.get("error",None)
    success = kwargs.get("success",None)
    
    query = " ".join(query.split())
    
    if not isinstance(result, list):
        result = [result]
    
    retDict = {
        "query": query,
        "offset":offset,
        "limit":limit,
        "result_size": len(result),
        "data": result,
        "error": error,
        "success":success
    }

    return retDict

# --------------------------------------------------------------------------- #
# Phase 1 -- simple reads (worked examples)
# --------------------------------------------------------------------------- #

@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Bare host -> the Swagger UI."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> dict:
    return custom_response(result=[{"ok": True}])


@app.get("/customers")
def get_customer(customer_id: int):
    success = True
    error = None
    query = f"""
            SELECT c.customer_id, c.first_name, c.last_name, c.email,
                   c.address, c.zipcode, z.state_code
            FROM customers c
            JOIN zipcodes z ON z.zipcode = c.zipcode
            WHERE c.customer_id = {customer_id}
            """
    row = conn.execute(query).fetchone()
    if row is None:
        success = False
        error = HTTPException(404, f"no customer {customer_id}")
    return custom_response(result=row,error=error,success=success,query=query)


@app.get("/departments")
def list_departments() -> dict:
    success = True
    error = None
    query = "SELECT department FROM departments ORDER BY 1"
    result = conn.execute(query).fetchall()
    rows = [r["department"] for r in result]
    return custom_response(result=rows,success=success,query=query,error=error)


@app.get("/products")
def list_products(limit: int = Query(50, ge=1, le=500),offset: int = Query(0, ge=0),
):
    # NOTE: OFFSET pagination. Fine here; Phase 3 shows why it stops being fine.
    query = f"""
        SELECT product_id, product_name, unit_price FROM products
        ORDER BY product_id LIMIT {limit} OFFSET {offset}
        """
    rows = conn.execute(query).fetchall()
    return custom_response(result=[dict(r) for r in rows],limit=limit,offset=offset,query=query)


@app.get("/purchases")
def list_purchases(
    
    start: str = Query(..., description="inclusive ISO date, e.g. 2025-01-01"),
    end: str = Query(..., description="exclusive ISO date"),
    limit: int = Query(100, ge=1, le=1000),
):
    rows = conn.execute(
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


@app.get("/customers/{customer_id}/purchases")
def customer_purchases(customer_id: int, ):
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/stats/revenue-by-state")
def revenue_by_state():
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/stats/revenue-by-month")
def revenue_by_month():
    raise HTTPException(501, _TODO + " (Phase 2)")


@app.get("/products/top")
def top_products(
    by: str = Query("revenue", pattern="^(revenue|count)$"),
    limit: int = Query(10, ge=1, le=100),
):
    raise HTTPException(501, _TODO + " (Phase 2)")


# --------------------------------------------------------------------------- #
# Phase 3 -- gnarly queries                (implement all 8 + 2 of your own)
# --------------------------------------------------------------------------- #

@app.get("/products/search", )
def search_products(q: str):
    raise HTTPException(501, _TODO + " (Phase 3: LIKE '%q%' -> then FTS5)")


@app.get("/customers/leaderboard", )
def leaderboard():
    raise HTTPException(501, _TODO + " (Phase 3: 90-day trailing spend window)")


@app.get("/customers/{customer_id}/streaks", )
def streaks(customer_id: int):
    raise HTTPException(501, _TODO + " (Phase 3: gaps-and-islands)")


@app.get("/reports/cube")
def cube():
    raise HTTPException(501, _TODO + " (Phase 3: state x department x month)")


@app.get("/purchases/sample")
def sample():
    raise HTTPException(501, _TODO + " (Phase 3: ORDER BY random() LIMIT 10)")


@app.get("/products/dead")
def dead_products(state: str):
    raise HTTPException(501, _TODO + " (Phase 3: anti-join / NOT EXISTS)")


# --------------------------------------------------------------------------- #
# Phase 4 -- writes & concurrency          (implement, then hammer it)
# --------------------------------------------------------------------------- #

@app.post("/purchases", status_code=201)
def create_purchase(body: NewPurchase):
    raise HTTPException(501, _TODO + " (Phase 4: INSERT in a transaction, return 201)")


# --------------------------------------------------------------------------- #
# Dev entrypoint:  python -m app.main   (run from the starter/ directory)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(
        "app.main:app",   # import string, so --reload can re-import on change
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8001")),
        reload=os.environ.get("RELOAD", "1") == "1",
    )
