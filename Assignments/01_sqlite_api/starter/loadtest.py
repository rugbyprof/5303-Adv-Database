"""
Trigger contention, don't benchmark it.

Fires N concurrent requests at one endpoint and reports the status-code spread
plus any exceptions. Use it in Phase 4 against POST /purchases to make
"database is locked" show up, then again after each mitigation.

    python loadtest.py --n 200 --method POST --path /purchases
    python loadtest.py --n 200 --path /stats/revenue-by-state   # read side

Needs httpx (installed with the dev extra).
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import time

import httpx

SAMPLE_PURCHASE = {
    "customer_id": 1,
    "card_id": 1,
    "product_id": 1,
    "department": "Games",
    "amount": 9.99,
    "purchase_date": "2026-01-15",
}


async def _one(client: httpx.AsyncClient, method: str, url: str, key: str | None):
    headers = {"X-API-Key": key} if key else {}
    try:
        if method == "POST":
            r = await client.post(url, json=SAMPLE_PURCHASE, headers=headers)
        else:
            r = await client.get(url, headers=headers)
        return r.status_code, r.text[:200]
    except Exception as exc:  # noqa: BLE001 -- we want to see everything
        return "EXC", f"{type(exc).__name__}: {exc}"


async def main_async(a):
    url = a.base.rstrip("/") + a.path
    async with httpx.AsyncClient(timeout=30) as client:
        t0 = time.perf_counter()
        results = await asyncio.gather(
            *(_one(client, a.method, url, a.key) for _ in range(a.n))
        )
        elapsed = time.perf_counter() - t0

    codes = collections.Counter(code for code, _ in results)
    print(f"{a.method} {url}  x{a.n}  in {elapsed:.2f}s")
    for code, count in sorted(codes.items(), key=lambda kv: str(kv[0])):
        print(f"  {code}: {count}")
    # show one example body per non-2xx outcome
    seen = set()
    for code, body in results:
        if code not in seen and not (isinstance(code, int) and 200 <= code < 300):
            seen.add(code)
            print(f"  --- {code} ---\n  {body}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", default="http://127.0.0.1:8000")
    p.add_argument("--path", default="/purchases")
    p.add_argument("--method", default="GET", choices=["GET", "POST"])
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--key", default="dev-key-123", help="X-API-Key value")
    asyncio.run(main_async(p.parse_args()))


if __name__ == "__main__":
    main()
