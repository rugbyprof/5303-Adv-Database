"""
driver.py -- run every read query against every database through the API.

Start the API first (python -m app.main), then from the starter folder:

    python driver.py                       # all sizes, both variants
    python driver.py --sizes 10k 100k      # skip 1m while you are debugging
    python driver.py --only Q08 Q09        # rerun a few queries

For each (query, database) it calls the route RUNS times and keeps the
median of the elapsed_ms values the API reports. Output:

    results.csv          one row per (query, database): time, rows, plan
    results.md           the same numbers as a table -- paste it into FINDINGS.md

Needs httpx (installed with the dev extra).
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import statistics
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RUNS = 5
SIZES = ["10k", "100k", "1m"]
VARIANTS = ["noidx", "idx"]

# (query id, route, query-string params)
# {whale} = the customer with the most purchases in that database
# {deep}  = a purchase_id 90% of the way through the table
JOBS = [
    # Phase 1 -- simple reads
    ("Q01", "/customers/{whale}", {}),
    ("Q02", "/products", {"limit": 50, "offset": 0}),
    ("Q03", "/purchases", {"start": "2025-03-01", "end": "2025-03-08"}),
    # Phase 2 -- indexes
    ("Q04", "/customers/{whale}/purchases", {}),
    ("Q05", "/stats/department-count", {"department": "Games"}),
    ("Q06", "/customers/{whale}/streaks", {}),
    ("Q07", "/stats/leaderboard", {"start": "2026-06-02", "end": "2026-09-01"}),
    ("Q08", "/products/dead", {"state": "TX"}),
    ("Q09", "/stats/revenue-by-state", {}),
    ("Q10", "/products/top", {}),
    # Phase 3 -- rewrites: slow version, then /fast version
    ("Q11", "/purchases/page", {"offset": "{deep}"}),
    ("Q11-fast", "/purchases/page/fast", {"after_id": "{deep}"}),
    ("Q12", "/purchases/sample", {}),
    ("Q12-fast", "/purchases/sample/fast", {}),
    ("Q13", "/stats/revenue-by-month", {}),
    ("Q13-fast", "/stats/revenue-by-month/fast", {}),
    ("Q14", "/reports/cube", {"start": "2025-01-01", "end": "2026-01-01", "min_purchases": 10}),
    ("Q14-fast", "/reports/cube/fast", {"start": "2025-01-01", "end": "2026-01-01", "min_purchases": 10}),
]


def facts(db_name: str) -> dict[str, int]:
    """Look up the per-database values the routes need (read-only)."""
    con = sqlite3.connect(f"file:{DATA / (db_name + '.db')}?mode=ro", uri=True)
    whale = con.execute(
        "SELECT customer_id FROM purchases GROUP BY customer_id "
        "ORDER BY COUNT(*) DESC LIMIT 1").fetchone()[0]
    max_id = con.execute("SELECT MAX(purchase_id) FROM purchases").fetchone()[0]
    con.close()
    return {"whale": whale, "deep": int(max_id * 0.9)}


def fill(value, f: dict[str, int]):
    return value.format(**f) if isinstance(value, str) else value


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", default="http://127.0.0.1:8001")
    p.add_argument("--key", default="dev-key-123", help="X-API-Key value")
    p.add_argument("--sizes", nargs="+", default=SIZES, choices=SIZES)
    p.add_argument("--only", nargs="+", help="query ids to run, e.g. Q08 Q11-fast")
    a = p.parse_args(argv)

    jobs = [j for j in JOBS if not a.only or j[0] in a.only]
    dbs = [f"{v}_{s}" for s in a.sizes for v in VARIANTS]
    results = []

    with httpx.Client(base_url=a.base, headers={"X-API-Key": a.key}, timeout=120) as client:
        for db in dbs:
            f = facts(db)
            for qid, route, params in jobs:
                url = fill(route, f)
                q = {k: fill(v, f) for k, v in params.items()} | {"db": db}
                times = []
                for _ in range(RUNS):
                    r = client.get(url, params=q)
                    r.raise_for_status()
                    body = r.json()
                    times.append(body["elapsed_ms"])
                ms = statistics.median(times)
                results.append({"query": qid, "db": db, "median_ms": ms,
                                "rows": body["row_count"], "plan": " | ".join(body["plan"])})
                print(f"{db:<11} {qid:<9} {ms:>10.2f} ms  {body['row_count']:>4} rows")

    with open(HERE / "results.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)

    # pivot: one row per query, one column per database
    ms = {(r["query"], r["db"]): r["median_ms"] for r in results}
    lines = ["| Query | " + " | ".join(dbs) + " |",
             "| :--- | " + " | ".join("---:" for _ in dbs) + " |"]
    for qid, _, _ in jobs:
        lines.append(f"| {qid} | " + " | ".join(f"{ms[(qid, d)]:.2f}" for d in dbs) + " |")
    (HERE / "results.md").write_text("\n".join(lines) + "\n")
    print("\nwrote results.csv and results.md")


if __name__ == "__main__":
    main()
