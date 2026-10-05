"""
make_dbs.py -- build every database the experiments need, in data/.

For each size it writes two files with identical rows:

    data/idx_<size>.db     schema indexes + covering indexes
    data/noidx_<size>.db   PRIMARY KEY / UNIQUE only (secondary indexes dropped)

Both get the monthly_sales summary table. Run from the starter folder:

    python make_dbs.py                  # 10k, 100k, 1m
    python make_dbs.py --sizes 10k      # just one size, for a quick test

Only the standard library is used.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
from pathlib import Path

from scale_data import build

HERE = Path(__file__).resolve().parent
SQL = HERE / "sql"
DATA = HERE / "data"

SIZES = {"10k": 10_000, "100k": 100_000, "1m": 1_000_000}


def run_sql(db: Path, *files: str, vacuum: bool = False) -> None:
    con = sqlite3.connect(db)
    for f in files:
        con.executescript((SQL / f).read_text())
    con.execute("ANALYZE")      # refresh planner statistics after index changes
    con.commit()
    if vacuum:
        con.execute("VACUUM")   # reclaim the space the dropped indexes used
    con.close()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sizes", nargs="+", default=list(SIZES), choices=list(SIZES))
    a = p.parse_args(argv)

    DATA.mkdir(exist_ok=True)
    for label in a.sizes:
        n = SIZES[label]
        idx = DATA / f"idx_{label}.db"
        noidx = DATA / f"noidx_{label}.db"
        print(f"== {label}: {n:,} purchases")

        build(str(idx), customers=max(n // 20, 500), products=max(n // 200, 100),
              purchases=n, skew=True, seed=1234)
        run_sql(idx, "summary_tables.sql")

        shutil.copy(idx, noidx)
        run_sql(idx, "covering_indexes.sql")
        run_sql(noidx, "drop_indexes.sql", vacuum=True)
        print(f"   wrote {idx.name} and {noidx.name}")


if __name__ == "__main__":
    main()
