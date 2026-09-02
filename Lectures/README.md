## Lectures

Each lecture is a self-contained folder: a `README.md` index, the lecture
material as Markdown, a `sql/` folder for scripts, and a `data/` folder for its
input files. Generated `*.db` files stay local and are git-ignored.

| Folder | Title | Description | Due |
| :----- | :---- | :---------- | :-- |
| [01_terms_concepts_intro](01_terms_concepts_intro/) | Terms, Concepts & SQL Basics | The vocabulary ([glossary.md](01_terms_concepts_intro/glossary.md) — relations/tables/documents/collections, keys & referential integrity, normalization vs. denormalization, embedding vs. referencing, schema enforcement vs. flexibility, duplication vs. consistency) plus a first SQL walkthrough ([sql_basics.md](01_terms_concepts_intro/sql_basics.md) — `SELECT`, `WHERE`, joins, aggregates, DML) against a `Students`/`Courses`/`Enrollments` schema. | — |
| [02_sqlite](02_sqlite/) | SQLite: From a Flat CSV to a Normalized Database | Walkthrough: inspect `data/example_data.csv`, find its functional dependencies, design an 8-table schema, build it with a rebuild script, and query it (joins, subqueries, aggregates, date ranges). Also covers the `sqlite3` shell, requirements/optional add-ons, and encryption/password hashing in Python. | — |
