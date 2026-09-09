# Naming Conventions: SQL, MongoDB, and Redis

A reference on identifier naming — for use alongside `dbscope`, or on its own. None of what follows is enforced by any database engine; a table, column, or key name is just a string as far as SQLite, PostgreSQL, MongoDB, or Redis is concerned. Consistent naming is a habit you build for the humans reading the schema later, not a rule the database checks for you. (`dbscope` will reformat your SQL syntax on request — uppercase keywords, one clause per line — but it won't rename your tables. That part's on you.)

## SQL: tables and columns

Common convention, not a standard:

- **Casing** — `snake_case`, all lowercase, is the dominant convention in the PostgreSQL/MySQL/SQLite world. PascalCase shows up more in SQL Server / .NET-adjacent shops. Pick one and hold it across the *entire* schema — mixing styles is worse than consistently picking the "wrong" one.
- **Table names** — plural (`employees`, `orders`): a table holds a collection of rows. Singular has defenders (it names "one entity type"), but plural is more common. Consistency matters more than which one you choose.
- **Primary keys** — just `id`.
- **Foreign keys** — `<singular_table>_id`. A row in `orders` referencing `customers` gets a `customer_id` column. This keeps joins self-documenting: `JOIN customers ON orders.customer_id = customers.id`.
- **Junction / join tables** — combine both table names: `student_course`.
- **Booleans** — verb-prefixed: `is_active`, `has_paid`, `can_edit`.
- **Timestamps and dates** — `_at` suffix for timestamps (`created_at`, `updated_at`); `_date` suffix for dates-only (`birth_date`).
- **Avoid reserved words as identifiers** — `order`, `group`, `select`, `table` are legal column/table names, but every reference then needs quoting, and the quote character differs by engine: double quotes in PostgreSQL and standard SQL, backticks in MySQL, square brackets in SQL Server.
- **Avoid abbreviations** unless they're universally understood, and avoid spaces or special characters — both force quoting on every reference.

### The cross-engine gotcha: case folding

This is the one most likely to bite when the same query is run against two different backends — which is the whole point of `dbscope`:

| Engine | Unquoted identifier behavior |
|---|---|
| PostgreSQL | Folded to lowercase. `CREATE TABLE Users (...)` silently creates `users`. |
| MySQL | Depends on the OS/filesystem the server runs on — case-sensitive on Linux, case-insensitive by default on macOS/Windows. |
| SQLite | Stored exactly as typed. Comparisons are effectively case-insensitive for ASCII in practice, but don't rely on that holding everywhere. |

Create the same table with mixed-case naming on SQLite and PostgreSQL, then run the same `SELECT` against both — the divergence (or lack of one) is a good five-minute lesson on its own.

## MongoDB naming quirks

- **No enforced schema, at all.** Nothing stops one document in a collection from having `email` while another has `emailAddress`. Naming consistency is pure self-discipline — contrast this with SQL, where the table's `CREATE TABLE` statement locks column names in place.
- **Field names can't start with `$`** (reserved for query operators like `$gt`, `$in`) **and can't contain a literal `.`** (dot notation is how queries address nested/embedded fields).
- **`_id` is reserved** and auto-generated as an `ObjectId` if a document doesn't supply one.
- **Collection and field names are case-sensitive** — no PostgreSQL-style folding here.
- **No keyword-collision problem.** Fields are just quoted JSON keys, so a field literally named `"select"` causes zero issues.

## Redis naming quirks

- **No tables or collections** — just a flat namespace of keys. The idiomatic (unenforced) convention is colon-delimited pseudo-hierarchy that mimics `table:row:field`: `user:1000:profile`, `session:abc123`.
- **Keys are case-sensitive** and technically binary-safe — spaces and newlines are legal in a key name, but avoid that in practice; it makes the CLI and debugging miserable.
- **Commands are a separate, fixed vocabulary from key names.** `GET`, `SET`, `HGETALL`, and friends are reserved the way SQL keywords are reserved — but your *key names* aren't restricted the same way. Don't conflate the two.

## Quick reference

| | Case sensitivity | Reserved-word escaping |
|---|---|---|
| SQLite | Effectively insensitive (don't rely on it) | Double quotes: `"name"` |
| PostgreSQL | Unquoted identifiers folded to lowercase | Double quotes: `"name"` |
| MongoDB | Case-sensitive | Not applicable — field names are JSON keys |
| Redis | Case-sensitive | Not applicable — key names are data, not identifiers |

---

*Written to sit alongside `dbscope`. Suitable as a course repo reference doc, or as an in-app help topic — Textual's built-in `Markdown` widget can render this file directly without any conversion.*
