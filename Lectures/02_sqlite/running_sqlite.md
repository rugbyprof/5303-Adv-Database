# How to Run These SQL Files (and what the `.` lines are)

A short orientation for the [SQLite walkthrough](sqlite_walkthrough.md) if you
have never driven SQLite from the command line.

---

## 1. The mental model

- **A database is one file.** `store.db` is a single binary file. There is no
  server, no "load the database" step, no import into a running process. You
  point the `sqlite3` program at a path; if the file exists it is opened, if not
  it is created on the first write.
- **`sqlite3` is a program (a REPL).** Run `sqlite3 store.db` and you get a
  `sqlite>` prompt. You type SQL, it answers. That is the whole tool.
- **Two kinds of lines** go into that prompt (and into `.sql` script files):
  1. **SQL statements** — `SELECT …`, `CREATE TABLE …`, `INSERT …`. End with a
     semicolon `;`. Standard-ish SQL; any SQLite driver in any language runs
     these.
  2. **Dot commands** — `.read`, `.mode`, `.import`, …. Start with a `.` in
     column 1, take the **whole line** (no trailing `;`, no trailing
     `-- comment`), one per line. These are features of the `sqlite3` *shell*,
     not SQL — a Python/Java/Go driver does **not** understand them.

---

## 2. Four ways to run a script against a database

All four do the same thing: feed SQL + dot commands to `sqlite3` with `store.db`
open. Pick whichever fits.

```bash
# (a) interactive: open the shell, then read a file into the session
sqlite3 store.db
sqlite> .read rebuild.sql
sqlite> .quit

# (b) one command as an argument, then exit
sqlite3 store.db ".read rebuild.sql"
sqlite3 store.db "SELECT count(*) FROM purchases;"

# (c) redirect a file onto sqlite3's standard input
sqlite3 store.db < rebuild.sql

# (d) heredoc (a script written inline in the shell)
sqlite3 store.db <<'EOF'
.mode box
SELECT * FROM departments;
EOF
```

Capture the output like any other command:

```bash
sqlite3 store.db < rebuild.sql > build.log 2>&1
sqlite3 store.db ".read sql/03_queries.sql" > query_results.txt
```

### Your specific question: `data.db < newinfo.sql`

That does **not** work, and it is worth understanding why. In the shell, `<`
connects a file to the **standard input of a program**. So the line needs to
name a program to run. `data.db` is not a program — it is a data file — so the
shell just reports "command not found" or "permission denied".

The correct form always names `sqlite3` and passes the database as its
**argument**:

```bash
sqlite3 data.db < newinfo.sql
#  ^program  ^arg (which db)  ^redirect the script onto sqlite3's stdin
```

Read it as: "run `sqlite3` with database `data.db`, and instead of me typing at
the prompt, take the keystrokes from `newinfo.sql`."

`sqlite3 data.db < newinfo.sql` and `sqlite3 data.db ".read newinfo.sql"` are
almost equivalent. The difference: with `<`, stdin *is* the script, so the
session cannot also read anything you type; with `.read` you can run it in the
middle of an interactive session and keep going afterward.

### Ephemeral database

```bash
sqlite3 :memory: < some.sql     # database lives in RAM, gone on exit
sqlite3 < some.sql              # same thing (no file arg = a temp db)
```

---

## 3. The dot commands used in this tutorial

| Command | What it does | Where it appears here |
| :--- | :--- | :--- |
| `.read FILE` | Execute `FILE` as a script (SQL **and** dot commands). Path is relative to the directory you launched `sqlite3` from. | [rebuild.sql](rebuild.sql) chains `sql/01_schema.sql` then `sql/02_load.sql` |
| `.mode MODE` | Output format for query results: `list` (default, `|`-separated), `box`, `table`, `column`, `csv`, `json`, `markdown`, `insert`, … | `.mode csv` before importing; `.mode box` in [sql/03_queries.sql](sql/03_queries.sql) for readable output |
| `.import [OPTS] FILE TABLE` | Read `FILE` into `TABLE`. `--csv` = CSV quoting rules; `--skip 1` = drop the header row. Path is relative to your working directory. | [sql/02_load.sql](sql/02_load.sql): `.import --skip 1 data/example_data.csv staging_raw` |
| `.headers on` / `off` | Show or hide column-name headers above results. | [sql/03_queries.sql](sql/03_queries.sql) |
| `.bail on` / `off` | `on` = stop at the first error instead of continuing. Essential for build scripts so a failure does not cascade. | [rebuild.sql](rebuild.sql) |
| `.echo on` / `off` | `on` = print each statement before running it. | [rebuild.sql](rebuild.sql) sets it `off` for quiet output |

### `PRAGMA` is different

`PRAGMA foreign_keys = ON;` looks like a setting but it **is SQL** (semicolon and
all) — a SQLite-specific statement, runnable from any driver. It is *not* a dot
command. It is needed once per connection because SQLite does not enforce foreign
keys by default. Every script here opens with it.

---

## 4. Other dot commands worth knowing

You will reach for these constantly while exploring:

| Command | Use |
| :--- | :--- |
| `.tables` | List tables and views. |
| `.schema ?NAME?` | Print the `CREATE` statements (all, or matching `NAME`). |
| `.indexes ?TABLE?` | List indexes. |
| `.quit` / `.exit` | Leave the shell (or press Ctrl-D). |
| `.open FILE` | Switch to a different database file without leaving the shell. |
| `.databases` | Show which file(s) are attached. |
| `.dump ?NAME?` | Emit SQL (schema + `INSERT`s) that would rebuild the database — the standard backup/export. `sqlite3 store.db .dump > backup.sql` |
| `.output FILE` / `.once FILE` | Send the next results (or all results) to a file instead of the screen. `.output` with no arg goes back to the screen. |
| `.nullvalue ␣NULL␣` | Choose how `NULL` prints (default is empty string — easy to miss). |
| `.timer on` | Print wall-clock time for each statement. |
| `.width 20 12` | Fixed column widths for `.mode column`. |
| `.help ?PATTERN?` | List dot commands, or those matching `PATTERN`. |
| `.show` | Dump the shell's current settings (mode, headers, separators, …). |

Useful `PRAGMA`s (these are SQL):

| Statement | Use |
| :--- | :--- |
| `PRAGMA table_info(purchases);` | Columns, types, PK flags for a table. |
| `PRAGMA foreign_key_list(purchases);` | The table's foreign keys. |
| `PRAGMA foreign_key_check;` | Report any row whose FK points nowhere. |
| `PRAGMA integrity_check;` | Verify the file is not corrupt. |

---

## 5. Gotchas this tutorial already ran into

- **No trailing comment on a dot command.** `.bail on  -- stop on error` fails
  with `Usage: .bail on|off` because `-- stop on error` is parsed as arguments.
  Put the comment on its own line.
- **Dot-command paths are relative to your shell's working directory**, not to
  the script doing the `.read`. That is why the tutorial says to `cd
  Lectures/02_sqlite` first — so `data/example_data.csv` in `.import` resolves.
- **`.read` runs dot commands too**, so a script can `.mode`, `.import`, and
  `.read` other scripts. That is how [rebuild.sql](rebuild.sql) is just a
  sequence of `.read`s.
- **`GLOB` vs `LIKE` wildcards** (SQL, not shell): in `LIKE`, `_` is "any one
  character"; in `GLOB`, the equivalent is `?` and `_` is literal.
- **Semicolons.** A SQL statement without its `;` leaves the shell showing a
  `...>` continuation prompt, waiting for you to finish it.

---

## 6. Try it now

```bash
cd Lectures/02_sqlite
rm -f store.db
sqlite3 store.db < rebuild.sql          # build it via stdin redirect
sqlite3 store.db ".tables"              # one command via argument
sqlite3 store.db                        # then explore interactively:
```
```
sqlite> .mode box
sqlite> .headers on
sqlite> .schema purchases
sqlite> SELECT department, count(*) FROM purchases GROUP BY department;
sqlite> .read sql/03_queries.sql
sqlite> .quit
```
