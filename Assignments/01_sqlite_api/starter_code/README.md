# Starter scaffold — Assignment 01

Scaffold for the [SQLite-behind-an-API assignment](../README.md). Q01 is implemented as a worked example. Copy the SQL for the rest from [QUERIES.md](../QUERIES.md).

## Layout

```
starter_code/
├── pyproject.toml         deps (fastapi, uvicorn, pydantic; dev: pytest, httpx)
├── .env.example           DATA_DIR, BUSY_TIMEOUT_MS, API_KEYS
├── scale_data.py          generates one database at any size (stdlib only)
├── make_dbs.py            builds all six experiment databases into data/
├── driver.py              calls every route on every database -> results.md / results.csv
├── loadtest.py            fires N concurrent requests (Phase 4)
├── sql/
│   ├── drop_indexes.sql       turns a copy into the noidx_* variant
│   ├── covering_indexes.sql   extra indexes in the idx_* variant
│   ├── summary_tables.sql     monthly_sales rollup (Phase 3 /fast routes)
│   └── auth.sql               api_keys table (stretch task)
├── app/
│   ├── experiment.py      get_exp_db (?db= selection) + run_query (timing + plan)
│   ├── models.py          Pydantic models (NewPurchase for Q15)
│   ├── auth.py            X-API-Key dependency
│   ├── db.py              older single-database helper (not used by the routes)
│   └── main.py            the FastAPI app -- your routes go here
└── tests/test_smoke.py    builds a tiny DB in a temp dir, checks Q01 + ?db= handling
```

## Setup

```bash
cd Assignments/01_sqlite_api/starter_code
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q

python make_dbs.py                 # ~20 s; writes data/{idx,noidx}_{10k,100k,1m}.db
python -m app.main                 # http://127.0.0.1:8001/docs
```

In a second terminal, once your routes are in:

```bash
python driver.py --sizes 10k       # quick check
python driver.py                   # full run
```

**Always run from this folder.** That's where `pyproject.toml`, `app/` and `data/` live. `python -m app.main` and `uvicorn app.main:app --port 8001` both work. `python app/main.py` does **not**, because the `app.` package-relative imports need the package context.

`HOST`, `PORT` (default 8001) and `RELOAD` (`0` disables auto-reload) are read from the environment by the `__main__` block. `BUSY_TIMEOUT_MS` (default 5000) is read by `app/experiment.py`.

## Editor setup (VS Code / Pyright)

`app/` is a package. Its modules import each other **relatively**, e.g. `from .experiment import run_query`. Don't let an "organize imports" action rewrite these to `from experiment import ...`. That form resolves in the editor but crashes at runtime with `ModuleNotFoundError`.

1. Open `Assignments/01_sqlite_api/starter_code/` as its own workspace folder.
2. Select the `.venv` interpreter (Command Palette → *Python: Select Interpreter* → `./.venv`).

## Notes

- `data/`, `*.db`, `*.db-wal`, `*.db-shm`, `.env` and `.venv/` are git-ignored.
- `scale_data.py` reads the schema from `Lectures/02_sqlite/sql/01_schema.sql`. Pass `--schema PATH` to override it.
