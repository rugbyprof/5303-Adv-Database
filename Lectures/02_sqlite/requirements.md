# Requirements & Optional Add-ons

What you actually need for this lecture is small. Everything else on this page is
optional — listed so you know what exists, what is already built in, and what the
course's later themes (full-text search, spatial, vector search, encryption) will
want.

---

## 1. Required for this lecture

| Tool | Version | Notes |
| :--- | :--- | :--- |
| **`sqlite3` CLI** | 3.37+ (tested on 3.51) | The command-line shell. 3.37 covers everything the tutorial files use (`.import --csv --skip`, `.mode box`, `STRICT`-era syntax, `GLOB` guards). |

That is the whole list. No extensions, no Python, no GUI.

### Getting the CLI

| Platform | Command |
| :--- | :--- |
| macOS | Ships at `/usr/bin/sqlite3` (often a bit old). Newer: `brew install sqlite` (installs "keg-only" as `$(brew --prefix)/opt/sqlite/bin/sqlite3`). |
| Debian / Ubuntu | `sudo apt install sqlite3` |
| Fedora | `sudo dnf install sqlite` |
| Windows | `winget install SQLite.SQLite`, or download the "sqlite-tools" bundle from <https://sqlite.org/download.html> |

### The library is a *separate* build from the CLI

Your programming language links its own copy of SQLite. They can be different
versions with different compile options. Always check both:

```bash
sqlite3 --version
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

---

## 2. Already built in — no install needed

These are commonly assumed to be add-ons. In the official sqlite.org binaries,
Homebrew's `sqlite`, and the copy bundled with CPython, they are compiled in and
on by default.

| Feature | Since | What you get |
| :--- | :--- | :--- |
| **JSON** | functions since 3.9 (2015); **on by default since 3.38**, 2022 | `json()`, `json_extract()`, `json_array()`, `json_object()`, `json_group_array()`, `json_each()` table-valued function, and the `->` / `->>` operators. Store JSON in a `TEXT` column and query into it. |
| **JSONB** (binary JSON) | 3.45 (Jan 2024) | `jsonb()`, `jsonb_extract()`, … — a more compact on-disk form; same semantics. |
| **BLOB** | always | A native storage class, not an add-on. Bind `bytes` directly. Helpers: `length()`, `substr()`, `hex()`, `unhex()` (3.41+), `zeroblob()`, `randomblob()`, `quote()`. Streaming I/O via the C API (`sqlite3_blob_open`), exposed in Python 3.11+ as `Connection.blobopen()` and fully in `apsw`. |
| **Math functions** | 3.35 (2021) | `sqrt`, `pow`/`power`, `exp`, `ln`, `log`, `log10`, trig, `pi()`, `floor`, `ceil`, `trunc`, `mod`. In the official builds; verify elsewhere (below). |
| **Window functions** | 3.25 (2018) | `row_number() OVER (…)`, `rank`, `lag`/`lead`, running sums. Used in `sql/03_queries.sql`. |
| **CTEs**, recursive `WITH` | 3.8.3 | Named subquery steps; graph/tree walks. |
| **UPSERT** / **RETURNING** / **generated columns** / **`STRICT` tables** | 3.24 / 3.35 / 3.31 / 3.37 | `INSERT … ON CONFLICT DO UPDATE`; `INSERT … RETURNING *`; computed columns; opt-in rigid typing. |
| **FTS5** full-text search | module, enabled in official + Homebrew + CPython builds | `CREATE VIRTUAL TABLE docs USING fts5(body);` with `MATCH`, `bm25()` ranking, prefix/phrase queries. (Relevant to the *Querying* theme, not this lecture.) |
| **R\*Tree** index | module, enabled in official builds | `CREATE VIRTUAL TABLE bbox USING rtree(id, minX,maxX, minY,maxY);` — bounding-box range queries. A lightweight alternative to SpatiaLite for pure "what's near here" work. |
| **geopoly** | 3.28, enabled in official builds | Simple polygon containment/overlap on top of R\*Tree. |
| **UTF-8 / UTF-16** text | always | Storage is Unicode. `length()`, `substr()`, `unicode()`, `char()`, `trim()` operate on Unicode code points, not bytes. |

### What "Unicode support" does **not** include by default

| Gap | Default behavior | Fix |
| :--- | :--- | :--- |
| `upper()` / `lower()` | Fold **ASCII only** (`'é'` stays `'é'`) | ICU extension, or `sqlean-unicode` |
| `LIKE` case-insensitivity | **ASCII only** | same |
| `REGEXP` operator | **Not implemented at all** (no function bound) | `sqlean-regexp`, ICU, or a user function |
| Locale-aware sorting / collation | Only `BINARY`, `NOCASE` (ASCII), `RTRIM` | ICU collations (`icu_load_collation`) |

---

## 3. Checking what *your* build actually has

```sql
SELECT sqlite_version();
SELECT * FROM pragma_compile_options;
```

Things worth grepping that output for:

| Token | Meaning |
| :--- | :--- |
| `ENABLE_FTS5` | full-text search available |
| `ENABLE_RTREE` | R\*Tree available |
| `ENABLE_GEOPOLY` | geopoly available |
| `ENABLE_MATH_FUNCTIONS` | `sqrt()` etc. available (absent → they're not) |
| `ENABLE_JSON1` | present on older builds; its *absence* on 3.38+ is fine — JSON is on unless `OMIT_JSON` |
| `ENABLE_ICU` | Unicode-aware `upper`/`lower`/`LIKE`/collations (**usually absent**) |
| `ENABLE_LOAD_EXTENSION` | `.load` / `load_extension()` works (needed for everything in §4–§7) |
| `OMIT_LOAD_EXTENSION` | extensions are **disabled** in this build |

In Python, loadable-extension support is often turned off in OS-vendored builds
(e.g. macOS system `/usr/bin/python3`). Test:

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.enable_load_extension(True)   # raises if the build disabled it
```

Homebrew Python and most `python.org` installers have it enabled; if yours does
not, use a Homebrew/pyenv Python or the `apsw` package.

---

## 4. Loadable extension bundles

Loadable extensions are `.so` / `.dylib` / `.dll` files you attach at runtime
with `.load ./name` (CLI) or `con.load_extension("name")` (Python). They work
with the **stock** SQLite — no rebuild.

### `sqlean` — the practical starting point

<https://github.com/nalgeon/sqlean> — a curated, well-maintained set:

| Module | Adds |
| :--- | :--- |
| `sqlean-unicode` | Unicode `upper`/`lower`/`like`/`unaccent` |
| `sqlean-regexp` | `regexp_like`, `regexp_substr`, `regexp_replace`, the `REGEXP` operator |
| `sqlean-crypto` | `md5`, `sha1`, `sha256`, `sha384`, `sha512`, `encode`/`decode` (base64/hex/url) |
| `sqlean-stats` | `median`, `percentile`, `stddev`, `variance` |
| `sqlean-math`, `sqlean-text`, `sqlean-time`, `sqlean-uuid`, `sqlean-fuzzy`, `sqlean-vsv` (CSV vtab), `sqlean-ipaddr` | as named |

Install options:

- Download the platform bundle from the releases page, then `.load ./unicode`.
- Python: `pip install sqlean.py` — a drop-in replacement for the `sqlite3`
  module with all sqlean modules preloaded (`import sqlean as sqlite3`).
- `sqlpkg` (<https://sqlpkg.org>) — a package manager for SQLite extensions
  (`sqlpkg install nalgeon/unicode`).

---

## 5. Encryption (see [encryption_and_passwords.md](encryption_and_passwords.md))

Encryption is **not** a loadable extension — you cannot `.load` it into a stock
`sqlite3`. It requires an alternate build of the library.

| Option | Install | License |
| :--- | :--- | :--- |
| **SQLCipher** | macOS `brew install sqlcipher` (adds a `sqlcipher` CLI); Debian/Ubuntu `apt install sqlcipher`; Python `pip install sqlcipher3-binary` or `pysqlcipher3` | Open source (BSD-style) |
| **SQLite3 Multiple Ciphers** | `pip install apsw` built against it, or DB Browser for SQLite (SQLCipher edition) | Open source |
| **SEE** (official SQLite Encryption Extension) | purchase from sqlite.org | Commercial |

For the password-hashing and field-encryption examples in this folder you only
need Python 3 plus:

```bash
pip install cryptography            # Fernet, AES-GCM, KDFs  (required for those examples)
pip install argon2-cffi bcrypt      # optional: nicer password hashing than stdlib scrypt
pip install sqlcipher3-binary       # optional: whole-file encryption demo
```

---

## 6. Spatial

| Option | What it is | Install |
| :--- | :--- | :--- |
| **R\*Tree** | Built-in (§2). Bounding-box indexing only — no geometry types, no projections. Enough for "rows within this lat/long box". | none |
| **geopoly** | Built-in (§2). Polygon containment/overlap, GeoJSON-ish. | none |
| **SpatiaLite** (`mod_spatialite`) | Full OGC geometry: `GEOMETRY` columns, `ST_*` functions, spatial indexes, coordinate-system transforms via PROJ, shapefile import. | macOS `brew install libspatialite` (+ `brew install spatialite-tools` for the `spatialite` CLI); Ubuntu `apt install libsqlite3-mod-spatialite spatialite-bin`. Then `.load mod_spatialite`. |

Python: load `mod_spatialite` through `sqlite3`/`apsw`, or use `geoalchemy2` with
the SpatiaLite dialect; the `spatialite` PyPI package bundles the binary.

---

## 7. Python libraries

| Package | Use | Install |
| :--- | :--- | :--- |
| **`sqlite3`** (stdlib) | Always present. DB-API driver. Note the loadable-extension caveat in §3. | built in |
| **`apsw`** | "Another Python SQLite Wrapper" — thin binding to the full C API. Best choice for loadable extensions, custom VFS, blob streaming, sessions/changesets. | `pip install apsw` |
| **`sqlite-utils`** | Build and reshape SQLite DBs from CSV/JSON, introspect schema, manage FTS — CLI + library. Excellent for coursework. | `pip install sqlite-utils` |
| **`datasette`** | Point it at a `.db` and get a browsable web UI + JSON API; large plugin ecosystem. | `pip install datasette` → `datasette serve store.db` |
| **`pandas`** / **`polars`** | `read_sql` / `to_sql`; quick analysis and plotting. | `pip install pandas` |
| **SQLAlchemy** | Core + ORM; SQLite dialect built in. Pairs with **`alembic`** for migrations. | `pip install sqlalchemy alembic` |
| **`sqlean.py`** | Drop-in `sqlite3` replacement with sqlean extensions preloaded (§4). | `pip install sqlean.py` |
| **`sqlite-vec`** | Vector search (`vec0` virtual table). Relevant to the course's vector-search theme. | `pip install sqlite-vec` |
| **`litecli`** | Nicer interactive shell: autocompletion, syntax highlighting, history search. | `pip install litecli` |
| **`harlequin`** | Full terminal SQL IDE (TUI) with a SQLite adapter. | `pip install harlequin` |
| **`yoyo-migrations`** | Lightweight SQL-file migrations without an ORM. | `pip install yoyo-migrations` |

---

## 8. Viewing & editing tools

### VS Code extensions

| Extension (Marketplace id) | What it does |
| :--- | :--- |
| **SQLite Viewer** (`qwtel.sqlite-viewer`) | Read-only. Double-click a `.db` file, browse tables in a tab. Zero config — the easiest way to eyeball `store.db`. |
| **SQLite** (`alexcvzz.vscode-sqlite`) | Run queries from the editor, results panel, DB explorer sidebar. Uses a bundled or system `sqlite3`. |
| **SQLTools** (`mtxr.sqltools`) + **SQLite driver** (`mtxr.sqltools-driver-sqlite`) | Multi-database query runner with saved connections; needs both the core and the driver. |
| **Database Client** (`cweijan.vscode-database-client2`) | GUI panels, data editing, generates ER diagrams. |
| **Rainbow CSV** (`mechatroner.rainbow-csv`) | Column-colors [`data/example_data.csv`](data/example_data.csv); adds an inline CSV query command. |
| **Markdown Preview Mermaid Support** (`bierner.markdown-mermaid`) | Renders the `erDiagram` in [sqlite_walkthrough.md](sqlite_walkthrough.md) in VS Code's Markdown preview. |

### Standalone GUIs

| Tool | Notes |
| :--- | :--- |
| **DB Browser for SQLite** (DB4S) | The standard free cross-platform GUI. `brew install --cask db-browser-for-sqlite`. A separate "SQLCipher" build opens encrypted databases. |
| **SQLiteStudio** | Free, portable, no install. |
| **Beekeeper Studio** | Free community edition, modern UI, also does Postgres/MySQL. |
| **DBeaver** (Community) | Java, heavyweight, supports every database; ER diagrams. |
| **Datasette** | Browser-based (see §7); best for exploring + sharing read-only. |
| **Harlequin** | Terminal UI (see §7); stays in your shell. |
| **DataGrip** / JetBrains DB tools | Commercial; bundled with PyCharm Professional. |

---

## 9. TL;DR for each stage of the course

| You are doing… | You need |
| :--- | :--- |
| **This SQLite lecture** | `sqlite3` 3.37+. Optionally a viewer (SQLite Viewer extension or DB4S). |
| The [encryption examples](encryption_and_passwords.md) | Python 3 + `pip install cryptography`; optionally `argon2-cffi`, `bcrypt`, `sqlcipher3-binary`. |
| Full-text search theme | Nothing extra — FTS5 is built in. Verify with `pragma_compile_options`. |
| Unicode-correct `upper`/`lower`/`LIKE`/`REGEXP` | `sqlean-unicode` + `sqlean-regexp`, or an ICU build. |
| Spatial theme | Start with built-in R\*Tree; add SpatiaLite (`mod_spatialite`) for real geometry. |
| Vector search theme | `pip install sqlite-vec`. |
| JSON / BLOB work | Nothing — both are native (JSON on by default since 3.38). |
