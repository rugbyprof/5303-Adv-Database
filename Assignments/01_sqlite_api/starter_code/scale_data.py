"""
scale_data.py -- build and populate the Assignment 01 database at any size.

Reuses the schema from Lectures/02_sqlite/sql/01_schema.sql, then generates
customers, cards, products, zipcodes, and (a lot of) purchases.

Examples
--------
    # lecture-sized
    python scale_data.py --db store.db --purchases 1000

    # something that will make Phase 3 hurt
    python scale_data.py --db store.db \
        --customers 50000 --products 5000 --purchases 1000000 --skew

Only the standard library is used.
"""

from __future__ import annotations

import argparse
import datetime as dt
import random
import sqlite3
import string
import sys
import time
from pathlib import Path

DEFAULT_SCHEMA = (
    Path(__file__).resolve().parents[3]
    / "Lectures" / "02_sqlite" / "sql" / "01_schema.sql"
)

STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO",
    "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
]
CARD_TYPES = [
    "visa", "mastercard", "americanexpress", "discover", "jcb", "maestro",
    "solo", "switch", "bankcard", "china-unionpay", "diners-club-international",
    "instapayment", "laser",
]
DEPARTMENTS = [
    "Automotive", "Baby", "Beauty", "Books", "Clothing", "Computers",
    "Electronics", "Games", "Garden", "Grocery", "Health", "Home", "Industrial",
    "Jewelry", "Kids", "Movies", "Music", "Outdoors", "Shoes", "Sports",
    "Tools", "Toys",
]
FIRST_NAMES = "Ada Grace Linus Alan Edsger Barbara Donald Ken Dennis Margaret " \
    "Radia Leslie Katherine Guido Bjarne Anita Shafi Frances Tim Vint".split()
LAST_NAMES = "Lovelace Hopper Torvalds Turing Dijkstra Liskov Knuth Thompson " \
    "Ritchie Hamilton Perlman Lamport Johnson Rossum Stroustrup Borg Goldwasser " \
    "Allen Berners Cerf".split()
ADJECTIVES = "Portable Wireless Compact Deluxe Rugged Smart Classic Premium " \
    "Foldable Insulated Adjustable Ergonomic Stainless Ceramic Bamboo".split()
NOUNS = "Charger Blender Backpack Lamp Speaker Kettle Skillet Notebook Tripod " \
    "Scooter Mixer Heater Organizer Toolkit Bottle Planter Keyboard Monitor".split()


def _apply_schema(con: sqlite3.Connection, schema_path: Path) -> None:
    if not schema_path.exists():
        sys.exit(
            f"schema not found: {schema_path}\n"
            "Pass --schema pointing at Lectures/02_sqlite/sql/01_schema.sql "
            "(or your own copy)."
        )
    con.executescript(schema_path.read_text())


def build(
    db_path: str,
    *,
    schema_path: Path = DEFAULT_SCHEMA,
    customers: int = 1_000,
    products: int = 800,
    zipcodes: int = 700,
    purchases: int = 1_000,
    max_cards: int = 2,
    skew: bool = False,
    start_date: str = "2024-01-01",
    end_date: str = "2026-08-31",
    seed: int = 1234,
) -> None:
    rng = random.Random(seed)
    t0 = time.perf_counter()

    Path(db_path).unlink(missing_ok=True)
    for sidecar in ("-wal", "-shm"):
        Path(db_path + sidecar).unlink(missing_ok=True)

    con = sqlite3.connect(db_path)
    _apply_schema(con, schema_path)

    # Load fast: this is disposable generated data.
    con.execute("PRAGMA foreign_keys = OFF")
    con.execute("PRAGMA journal_mode = OFF")
    con.execute("PRAGMA synchronous = OFF")

    cur = con.cursor()
    cur.execute("BEGIN")

    cur.executemany("INSERT INTO states(state_code) VALUES (?)",
                    [(s,) for s in STATES])
    cur.executemany("INSERT INTO card_types(card_type) VALUES (?)",
                    [(c,) for c in CARD_TYPES])
    cur.executemany("INSERT INTO departments(department) VALUES (?)",
                    [(d,) for d in DEPARTMENTS])

    # zipcodes -> one state each (a real functional dependency)
    zips: list[str] = []
    seen_zip: set[str] = set()
    while len(zips) < zipcodes:
        z = f"{rng.randint(1, 99999):05d}"
        if z not in seen_zip:
            seen_zip.add(z)
            zips.append(z)
    cur.executemany(
        "INSERT INTO zipcodes(zipcode, state_code) VALUES (?, ?)",
        [(z, rng.choice(STATES)) for z in zips],
    )

    # customers
    cust_rows = []
    for i in range(1, customers + 1):
        fn = rng.choice(FIRST_NAMES)
        ln = rng.choice(LAST_NAMES)
        email = f"{fn}.{ln}.{i}@example.com".lower()
        cust_rows.append((i, fn, ln, email, f"{rng.randint(1, 9999)} Main St",
                          rng.choice(zips)))
    _batched(cur,
             "INSERT INTO customers"
             "(customer_id, first_name, last_name, email, address, zipcode) "
             "VALUES (?, ?, ?, ?, ?, ?)", cust_rows)

    # cards: 1..max_cards per customer
    card_rows = []
    cards_by_customer: dict[int, list[int]] = {}
    card_id = 0
    for cid in range(1, customers + 1):
        for _ in range(rng.randint(1, max_cards)):
            card_id += 1
            card_rows.append((card_id, cid, rng.choice(CARD_TYPES),
                              f"{4_000_000_000_000_000 + card_id}"))
            cards_by_customer.setdefault(cid, []).append(card_id)
    _batched(cur,
             "INSERT INTO cards"
             "(card_id, customer_id, card_type, card_number) VALUES (?, ?, ?, ?)",
             card_rows)

    # products: name -> one price (functional dependency)
    prod_rows = []
    seen_name: set[str] = set()
    pid = 0
    while pid < products:
        name = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)} {pid}"
        if name in seen_name:
            continue
        seen_name.add(name)
        pid += 1
        prod_rows.append((pid, name, round(rng.uniform(0.79, 399.99), 2)))
    _batched(cur,
             "INSERT INTO products(product_id, product_name, unit_price) "
             "VALUES (?, ?, ?)", prod_rows)
    prices = {r[0]: r[2] for r in prod_rows}

    # purchases -- the big table
    start = dt.date.fromisoformat(start_date)
    span = (dt.date.fromisoformat(end_date) - start).days
    # fixed permutations so "hot" customers / "popular" products are arbitrary
    # but reproducible
    cust_order = list(range(1, customers + 1))
    prod_order = list(range(1, products + 1))
    rng.shuffle(cust_order)
    rng.shuffle(prod_order)
    exp = 3.0 if skew else 1.0
    # with --skew, some customers never buy and some products never sell, so the
    # LEFT JOIN / anti-join endpoints have real gaps to find
    active_cust = int(customers * 0.9) if skew else customers
    active_prod = int(products * 0.7) if skew else products

    def gen_purchases():
        for _ in range(purchases):
            cust = cust_order[int(active_cust * (rng.random() ** exp)) % active_cust]
            prod = prod_order[int(active_prod * (rng.random() ** exp)) % active_prod]
            yield (
                cust,
                rng.choice(cards_by_customer[cust]),
                prod,
                rng.choice(DEPARTMENTS),
                prices[prod],
                (start + dt.timedelta(days=rng.randint(0, span))).isoformat(),
            )

    _batched(cur,
             "INSERT INTO purchases"
             "(customer_id, card_id, product_id, department, amount, purchase_date) "
             "VALUES (?, ?, ?, ?, ?, ?)", gen_purchases(), total=purchases)

    con.commit()

    # back to safe settings for the API to use
    con.execute("PRAGMA journal_mode = WAL")
    con.execute("PRAGMA foreign_keys = ON")
    bad = con.execute("PRAGMA foreign_key_check").fetchall()
    if bad:
        sys.exit(f"foreign_key_check found {len(bad)} problem rows")
    con.execute("ANALYZE")
    con.commit()

    counts = {
        t: con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        for t in ("states", "zipcodes", "card_types", "departments",
                  "customers", "cards", "products", "purchases")
    }
    con.close()
    dt_s = time.perf_counter() - t0
    print(f"built {db_path} in {dt_s:,.1f}s")
    for t, n in counts.items():
        print(f"  {t:<12} {n:>12,}")


def _batched(cur, sql, rows, *, size=10_000, total=None):
    """executemany in chunks so a huge generator doesn't buffer in memory."""
    buf = []
    done = 0
    for row in rows:
        buf.append(row)
        if len(buf) >= size:
            cur.executemany(sql, buf)
            done += len(buf)
            buf.clear()
            if total:
                print(f"\r  ...{done:,}/{total:,}", end="", flush=True)
    if buf:
        cur.executemany(sql, buf)
        done += len(buf)
    if total:
        print(f"\r  {done:,} rows".ljust(30))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default="store.db")
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA,
                   help=f"path to 01_schema.sql (default: {DEFAULT_SCHEMA})")
    p.add_argument("--customers", type=int, default=1_000)
    p.add_argument("--products", type=int, default=800)
    p.add_argument("--zipcodes", type=int, default=700)
    p.add_argument("--purchases", type=int, default=1_000)
    p.add_argument("--max-cards", type=int, default=2)
    p.add_argument("--skew", action="store_true",
                   help="concentrate purchases on a few customers; leave some "
                        "products unsold")
    p.add_argument("--start-date", default="2024-01-01")
    p.add_argument("--end-date", default="2026-08-31")
    p.add_argument("--seed", type=int, default=1234)
    a = p.parse_args(argv)

    build(a.db, schema_path=a.schema, customers=a.customers, products=a.products,
          zipcodes=a.zipcodes, purchases=a.purchases, max_cards=a.max_cards,
          skew=a.skew, start_date=a.start_date, end_date=a.end_date, seed=a.seed)


if __name__ == "__main__":
    main()
