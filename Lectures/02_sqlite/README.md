# 02 — SQLite

Taking one flat, spreadsheet-shaped CSV ([`../example_data.csv`](../example_data.csv),
1,000 purchase rows), deciding how it *should* be organized, building a
normalized schema for it in SQLite, loading the data, and querying it.

The lecture covers: data types, primary/foreign keys and relationships, `CHECK`
constraints, normalization vs. deliberate denormalization, loading CSV via a
staging table, and reads — `SELECT *`, joins, subqueries, aggregates, and
date-range queries. It builds on the
[Data Modeling Glossary](../01_overview/README.md).

## Quick start

```bash
cd Lectures/02_sqlite
rm -f store.db
sqlite3 store.db ".read rebuild.sql"      # build the whole database from the CSV
sqlite3 store.db ".read sql/03_queries.sql"   # run the worked query examples
```

New to the `sqlite3` command line? Start with
[running_sqlite.md](running_sqlite.md).

## Files

### Read these

| File | What it is |
| :--- | :--- |
| [sqlite_walkthrough.md](sqlite_walkthrough.md) | **The lecture.** Step-by-step: inspect the raw data, find its functional dependencies, design the 8-table schema (with an ER diagram), build it, and query it. Start here. |
| [running_sqlite.md](running_sqlite.md) | Orientation for the `sqlite3` shell — how to run `.sql` files, every `.` (dot) command used here, `PRAGMA` vs. dot commands, and how `sqlite3 store.db < script.sql` redirection works. |
| [encryption_and_passwords.md](encryption_and_passwords.md) | SQLite ships no encryption or password hashing — it is all application-side. Worked Python examples: Argon2id / bcrypt / scrypt password hashing, Fernet and AES-256-GCM field encryption, blind-index search over encrypted columns, and whole-file SQLCipher. |

### Run these

| File | What it does | Depends on |
| :--- | :--- | :--- |
| [rebuild.sql](rebuild.sql) | One entry point. Drops and recreates every object, loads the CSV, and verifies (foreign-key check + row/revenue round-trip). Safe to re-run. | `sql/01_schema.sql`, `sql/02_load.sql` |
| [sql/01_schema.sql](sql/01_schema.sql) | `CREATE TABLE` ×8 + indexes + a `purchase_details` view. All data types, keys, and constraints, with the design rationale in comments. | — |
| [sql/02_load.sql](sql/02_load.sql) | Loads `../example_data.csv` into a text-only `staging_raw` table, then `INSERT … SELECT` transforms it into the normalized tables (parents first). Converts the `M/D/YYYY` dates to ISO. | `01_schema.sql` |
| [sql/03_queries.sql](sql/03_queries.sql) | Worked read examples grouped by topic: `SELECT *`, filtering, joins (inner / left / window), subqueries (scalar / `IN` / derived / correlated / `NOT EXISTS`), aggregates (`GROUP BY` / `HAVING`), date ranges, plus `CASE`, CTEs, and `EXPLAIN QUERY PLAN`. Run against a built database. | a built `store.db` |
| [sql/90_data_quality.sql](sql/90_data_quality.sql) | The functional-dependency checks that justify the schema. Run against a `staging_raw`-only database *before* designing — see [sqlite_walkthrough.md §2](sqlite_walkthrough.md#2-decide-the-schema-the-normalization-exercise). | a loaded `staging_raw` |

### Not in version control

`store.db`, `explore.db`, and any other `*.db` files are build artifacts —
regenerate them with `rebuild.sql`. They are covered by the repo
[.gitignore](../../.gitignore).

## The schema at a glance

```
states ─< zipcodes ─< customers ─< cards ─< purchases >─ products
                                    │                 │
                          card_types┘       departments┘
```

Eight tables. `purchases` is the fact table — one row per purchase event, every
descriptive attribute replaced by a foreign key, except `amount` (a point-in-time
snapshot of what was charged) and `purchase_date` (stored as ISO `TEXT`). Full
diagram and rationale in [sqlite_walkthrough.md](sqlite_walkthrough.md).
