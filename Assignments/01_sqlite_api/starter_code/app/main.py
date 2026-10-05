"""
Assignment 01 -- SQLite behind a FastAPI service.

Run it from the starter folder, either way:
    python -m app.main                   # uses the __main__ block below (port 8001)
    uvicorn app.main:app --port 8001     # equivalent

Then open http://127.0.0.1:8001/docs

(Do NOT run `python app/main.py` -- the package-relative imports need the
`app.` package context, which only `-m app.main` / uvicorn provide.)

Q01 below is a worked example. Add Q02-Q15 the same way, copying the SQL from
../QUERIES.md. Every experiment route takes ?db=<name> (e.g. ?db=noidx_1m).
"""

from __future__ import annotations

import random  # noqa: F401  -- you need this for Q12 /fast
import sqlite3

from fastapi import Depends, FastAPI, HTTPException  # noqa: F401
from fastapi.responses import RedirectResponse

from .auth import require_api_key
from .experiment import get_exp_db, run_query
from .models import NewPurchase  # noqa: F401  -- you need this for Q15

app = FastAPI(title="SQLite API -- Assignment 01")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Bare host -> the Swagger UI."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


# --------------------------------------------------------------------------- #
# SQL -- copied from ../QUERIES.md
# --------------------------------------------------------------------------- #

Q01_SQL = """
SELECT c.customer_id, c.first_name, c.last_name, c.email, c.zipcode, z.state_code
FROM customers c
JOIN zipcodes z ON z.zipcode = c.zipcode
WHERE c.customer_id = :customer_id
"""

# TODO: Q02_SQL ... Q14_FAST_SQL


# --------------------------------------------------------------------------- #
# Routes
#
# FastAPI matches top to bottom, so keep the fixed paths (/purchases/page,
# /purchases/sample, .../fast) above anything shaped like /purchases/{x}.
# --------------------------------------------------------------------------- #

# Phase 1 ------------------------------------------------------------------- #

@app.get("/customers/{customer_id}", dependencies=[Depends(require_api_key)])
def q01_customer(customer_id: int, db: sqlite3.Connection = Depends(get_exp_db)):
    return run_query(db, Q01_SQL, {"customer_id": customer_id})


# TODO Q02  GET /products?limit=&offset=
# TODO Q03  GET /purchases?start=&end=

# Phase 2 ------------------------------------------------------------------- #

# TODO Q04  GET /customers/{customer_id}/purchases
# TODO Q05  GET /stats/department-count?department=
# TODO Q06  GET /customers/{customer_id}/streaks
# TODO Q07  GET /stats/leaderboard?start=&end=
# TODO Q08  GET /products/dead?state=
# TODO Q09  GET /stats/revenue-by-state
# TODO Q10  GET /products/top

# Phase 3 -- each has a slow route and a /fast route ------------------------ #

# TODO Q11  GET /purchases/page?offset=        GET /purchases/page/fast?after_id=
# TODO Q12  GET /purchases/sample              GET /purchases/sample/fast
# TODO Q13  GET /stats/revenue-by-month        GET /stats/revenue-by-month/fast
# TODO Q14  GET /reports/cube?start=&end=&min_purchases=
#                                              GET /reports/cube/fast?(same)

# Phase 4 ------------------------------------------------------------------- #

# TODO Q15  POST /purchases   (the full code is in QUERIES.md)


# --------------------------------------------------------------------------- #
# Dev entrypoint:  python -m app.main   (run from the starter folder)
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
