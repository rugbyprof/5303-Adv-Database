# 01 — Terms, Concepts & SQL Basics

The vocabulary and the first hands-on SQL for the *Database Models and Data
Modeling* and *Querying and Data Access* themes. Two documents, different jobs:

## Files

| File | What it is |
| :--- | :--- |
| [glossary.md](glossary.md) | **Reference.** Every term in the data-modeling theme, grouped by topic, defined once with a concrete example — and, where it matters, the document / key-value counterpart. Look things up here; it is not meant to be read start to finish. Covers relations/tables/documents/collections, keys & referential integrity, normalization vs. deliberate denormalization, embedding vs. referencing, schema enforcement vs. flexibility, and data duplication vs. consistency. |
| [sql_basics.md](sql_basics.md) | **Lecture walkthrough.** A 60–75 minute path through relational SQL against a small `Students` / `Courses` / `Enrollments` schema: `SELECT`, `WHERE`, pattern matching, `NULL`, `ORDER BY` / `LIMIT`, aggregates & `GROUP BY` / `HAVING`, inner and left joins, `INSERT` / `UPDATE` / `DELETE`, and a conceptual pass over transactions, constraints, and indexes. Ends with a suggested sequence and practice prompts. |

Read `sql_basics.md` for the flow of the class; reach for `glossary.md` whenever a
term needs a precise definition. `sql_basics.md` links into the glossary at the
points where the two overlap.

## Data

| File | Use |
| :--- | :--- |
| [data/students.sql](data/students.sql) | `CREATE TABLE students` plus 1,000 sample rows. Load it to have real data behind the `sql_basics.md` examples: `sqlite3 week01.db ".read data/students.sql"` (run from this folder). |

`week01.db` and any other `*.db` you create here are build artifacts — not
committed (see the repo [.gitignore](../../.gitignore)).

## Next

[02_sqlite](../02_sqlite/) takes these concepts and builds a normalized,
multi-table database from a messy CSV.
