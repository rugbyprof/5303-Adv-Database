# Starter scaffold — Assignment 01

Skeleton for the [SQLite-behind-an-API assignment](../README.md). Phase 1
endpoints work; Phases 2–4 are `501` stubs.

## Layout

```
starter/
├── pyproject.toml         deps (fastapi, uvicorn, pydantic; dev: pytest, httpx)
├── .env.example           DB_PATH, API_KEYS
├── scale_data.py          build store.db at any size  (stdlib only)
├── loadtest.py            fire N concurrent requests (Phase 4)
├── sql/auth.sql           api_keys table for the auth task
├── app/
│   ├── db.py              connect() + pragmas + explain() helper
│   ├── models.py          Pydantic response models
│   ├── auth.py            X-API-Key dependency (env-var now; DB-backed = your task)
│   └── main.py            the FastAPI app
└── tests/test_smoke.py    session fixture builds a tiny DB, hits Phase 1
```

## Setup

```bash
cd Assignments/01_sqlite_api/starter
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# build a database (lecture-sized to start)
python scale_data.py --db store.db --purchases 1000

# run it
export API_KEYS=dev-key-123
uvicorn app.main:app --reload
open http://127.0.0.1:8000/docs
```

Call an endpoint:

```bash
curl -s -H "X-API-Key: dev-key-123" http://127.0.0.1:8000/customers/1 | python -m json.tool
```

## Scaling up

```bash
python scale_data.py --db store.db --customers 50000 --products 5000 --purchases 1000000 --skew
```

`--skew` concentrates purchases on ~10% of customers and ~70% of products, so
the LEFT JOIN / anti-join / leaderboard endpoints have real gaps and hot spots
to find. Re-run at 100k / 1M / 5M `--purchases` and keep the query plans.

## Tests

```bash
pytest -q
```

The fixture builds a 3k-row DB in a temp dir and points `DB_PATH` at it, so
tests don't touch your `store.db`.

## Notes

- `store.db`, `*.db-wal`, `*.db-shm`, `.env`, `.venv/` are git-ignored.
- `scale_data.py` reads the schema from `Lectures/02_sqlite/sql/01_schema.sql`
  by default; `--schema PATH` overrides it.
- `app/db.py:explain(con, sql, params)` returns the `EXPLAIN QUERY PLAN` lines —
  use it when writing `FINDINGS.md`.
