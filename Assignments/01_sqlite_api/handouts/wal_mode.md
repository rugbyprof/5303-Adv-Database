# WAL Mode: How SQLite Lets Readers and a Writer Work at Once

Every database in this assignment runs in **WAL mode**. You can see it in the code: `scale_data.py` sets it, `app/experiment.py` notes that *"journal_mode=WAL is already stored in the file"*, and Phase 4 is really a test of what WAL can and can't do for you.

This handout explains what WAL is, shows it working with two short scripts you can run, and lists the mistakes it makes easy.

**The short version:**

- WAL stands for **write-ahead log**. New data is appended to a separate `-wal` file instead of overwriting the database file in place.
- Because the main file isn't being changed underneath them, **readers keep working while a writer commits**, and a writer doesn't wait for readers.
- There is still **only one writer at a time**. WAL helps reads during writes, not writes during writes.

---

## 1. Why a database needs a journal at all

A commit may change dozens of pages (4 KB blocks) of the database file. If the power fails after half of them are written, the file holds a mix of old and new pages: corrupt. A **journal** is the extra file that makes a commit all-or-nothing, so a crash leaves either the old version or the new one, never a mix.

SQLite has two kinds of journal. You pick one with `PRAGMA journal_mode`.

## 2. The old way: rollback journal (`journal_mode = DELETE`)

This is SQLite's default for a new database:

```text
COMMIT:
  1. copy the ORIGINAL pages      store.db  ──► store.db-journal
  2. overwrite them in place      store.db  ◄── new pages
  3. delete the journal           (the commit is done)

after a crash:  copy the originals back from the journal (a "rollback")
```

The weakness is step 2. While the writer overwrites pages **in the real file**, a reader could see half-old, half-new data. So SQLite uses locks to keep them apart:

- A writer can't commit while **any** reader is mid-read. It waits for them all to finish.
- Readers can't start while a commit is being written.

A long-running report therefore stops every write, and a stream of writes holds up every read.

## 3. The WAL way (`journal_mode = WAL`)

WAL turns it around: **leave the original pages alone, and append the new ones somewhere else**.

```text
COMMIT:
  append the new pages, then a "commit" marker    store.db-wal  ◄── new pages
  (store.db is not touched)

READ a page:
  newest committed copy in store.db-wal?  yes ─► use it
                                          no  ─► read it from store.db
  (store.db-shm is a small shared-memory index of which pages are in the WAL)

CHECKPOINT (now and then):
  copy WAL pages back into store.db, then start the WAL over
```

Three files make up one database now:

| File | Holds |
|---|---|
| `store.db` | the database as of the last checkpoint |
| `store.db-wal` | every page committed since then |
| `store.db-shm` | an index into the WAL, shared between connections |

Because committed data is only ever *added* to the WAL, a reader can keep reading the version that existed when it started, even while a writer appends newer pages after it. Each reader works from a **snapshot**.

**Checkpoints** happen automatically when the WAL reaches 1,000 pages (`PRAGMA wal_autocheckpoint`), and when the last connection to the database closes. When that last connection closes, SQLite also deletes the `-wal` and `-shm` files.

---

## 4. Demo: a reader and a writer at the same time

Save as `wal_demo.py` in `starter_code/` and run it twice:

```python
"""wal_demo.py -- rollback journal vs. WAL, with a reader holding a transaction open."""
import os
import sqlite3
import sys

mode = sys.argv[1] if len(sys.argv) > 1 else "wal"          # "wal" or "delete"
path = f"demo_{mode}.db"
for f in (path, path + "-wal", path + "-shm", path + "-journal"):
    if os.path.exists(f):
        os.remove(f)

setup = sqlite3.connect(path)
setup.execute(f"PRAGMA journal_mode = {mode}")
setup.execute("CREATE TABLE purchases (purchase_id INTEGER PRIMARY KEY, amount NUMERIC)")
setup.executemany("INSERT INTO purchases (amount) VALUES (?)", [(9.99,)] * 1000)
setup.commit()
setup.close()

reader = sqlite3.connect(path, isolation_level=None)
writer = sqlite3.connect(path, isolation_level=None, timeout=1)   # wait up to 1 s for locks

reader.execute("BEGIN")                                            # a long-running report...
print("reader sees", reader.execute("SELECT COUNT(*) FROM purchases").fetchone()[0], "rows")

writer.execute("BEGIN IMMEDIATE")
writer.execute("INSERT INTO purchases (amount) VALUES (19.99)")
try:
    writer.execute("COMMIT")
    print("writer committed")
except sqlite3.OperationalError as e:
    print("writer COMMIT failed:", e)
    writer.execute("ROLLBACK")

print("reader still sees", reader.execute("SELECT COUNT(*) FROM purchases").fetchone()[0], "rows")
reader.execute("COMMIT")                                           # ...report finishes
print("reader, new transaction, sees", reader.execute("SELECT COUNT(*) FROM purchases").fetchone()[0], "rows")
```

```text
$ python wal_demo.py delete                 $ python wal_demo.py wal
reader sees 1000 rows                       reader sees 1000 rows
writer COMMIT failed: database is locked    writer committed
reader still sees 1000 rows                 reader still sees 1000 rows
reader, new transaction, sees 1000 rows     reader, new transaction, sees 1001 rows
```

Read the two columns line by line:

- **Rollback journal:** one open reader was enough to make the writer's `COMMIT` wait out its 1-second timeout and fail with `database is locked`. The new row was lost.
- **WAL:** the writer committed right away. The reader, still inside its transaction, kept seeing **1,000** rows: its snapshot. As soon as the reader started a new transaction, it saw 1,001.

That snapshot behavior is also why a plain `BEGIN` transaction that reads and *then* tries to write can fail instantly with `database is locked`. Its snapshot is out of date and waiting won't fix it. `BEGIN IMMEDIATE` avoids this by taking the write lock before reading anything.

---

## 5. Demo: watch the files

Save as `wal_files.py` and run it. It keeps one connection open the whole time so you can see the `-wal` file before SQLite cleans it up:

```python
"""wal_files.py -- watch the -wal file grow, get checkpointed, and bite a careless copy."""
import os
import shutil
import sqlite3

path = "files_demo.db"
for f in (path, path + "-wal", path + "-shm", "copy.db"):
    if os.path.exists(f):
        os.remove(f)

def sizes(label):
    parts = []
    for f in (path, path + "-wal", path + "-shm"):
        parts.append(f"{f.split('.')[-1]:>6}: {os.path.getsize(f) if os.path.exists(f) else '-':>8}")
    print(f"{label:<34}", "  ".join(parts))

con = sqlite3.connect(path, isolation_level=None)
print("journal_mode =", con.execute("PRAGMA journal_mode = WAL").fetchone()[0])
print("wal_autocheckpoint =", con.execute("PRAGMA wal_autocheckpoint").fetchone()[0], "pages")
con.execute("CREATE TABLE purchases (purchase_id INTEGER PRIMARY KEY, amount NUMERIC)")
sizes("after CREATE TABLE")

con.executemany("INSERT INTO purchases (amount) VALUES (?)", [(9.99,)] * 1000)
con.execute("PRAGMA wal_checkpoint(TRUNCATE)")    # first 1,000 rows -> main file
sizes("1,000 rows, checkpointed")

con.execute("BEGIN")
con.executemany("INSERT INTO purchases (amount) VALUES (?)", [(9.99,)] * 1000)
con.execute("COMMIT")                             # next 1,000 rows -> -wal only
sizes("+1,000 rows, committed")

shutil.copy(path, "copy.db")                      # the mistake: copy only the .db file
copy = sqlite3.connect("copy.db")
print("rows in original:", con.execute("SELECT COUNT(*) FROM purchases").fetchone()[0],
      "| rows in copy.db:", copy.execute("SELECT COUNT(*) FROM purchases").fetchone()[0])
copy.close()

con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
sizes("after wal_checkpoint(TRUNCATE)")

con.close()
sizes("after the last connection closes")
```

```text
journal_mode = wal
wal_autocheckpoint = 1000 pages
after CREATE TABLE                     db:     4096  db-wal:     8272  db-shm:    32768
1,000 rows, checkpointed               db:    24576  db-wal:        0  db-shm:    32768
+1,000 rows, committed                 db:    24576  db-wal:    28872  db-shm:    32768
rows in original: 2000 | rows in copy.db: 1000
after wal_checkpoint(TRUNCATE)         db:    40960  db-wal:        0  db-shm:    32768
after the last connection closes       db:    40960  db-wal:        -  db-shm:        -
```

What to notice:

1. **`PRAGMA journal_mode = WAL` returns the mode it ended up in.** If you see `delete` instead, the switch failed.
2. **Committing grew the `-wal`, not the `.db`.** The second 1,000 rows are committed and safe, yet `store.db` didn't change size: those rows live only in the WAL.
3. **The copy lost 1,000 committed rows.** `copy.db` got the main file without its WAL. Nothing warns you; the data is simply missing. (Try copying before the first checkpoint: the copy doesn't even have the `purchases` table, because the `CREATE TABLE` was still in the WAL.)
4. **A checkpoint moves the pages home.** After `wal_checkpoint(TRUNCATE)` the main file holds everything and the WAL is empty again.
5. **Closing the last connection cleans up.** The `-wal` and `-shm` files disappear, and `store.db` alone is a complete database.

---

## 6. Side by side

| | Rollback journal (`DELETE`) | WAL |
|---|---|---|
| Where a commit writes | into `store.db`, after saving the old pages | appended to `store.db-wal` |
| Readers during a commit | blocked | **keep going**, on their snapshot |
| A writer while readers are reading | waits for them (demo: failed) | **doesn't wait** (demo: committed) |
| Writers at the same time | one | **still one** |
| Files on disk | 1, plus a temporary journal | 3 while open, 1 after the last close |
| Commit cost | several scattered writes plus syncs | one sequential append |
| Works on a network drive | yes (with caveats) | **no**: every process must be on the same machine |

---

## 7. How this project uses it

- **The mode is stored in the file.** `journal_mode = WAL` is remembered in the database itself, so every later connection gets WAL without asking. Most other pragmas (`foreign_keys`, `busy_timeout`, `synchronous`) are **per connection**, which is why `experiment.py` sets them on every request.
- **`scale_data.py` loads with the journal off, then switches.** During generation it uses `journal_mode = OFF` and `synchronous = OFF`. That's fast and has no crash safety, which is fine for data you can regenerate. At the end it switches to `WAL` for the API to use.
- **`synchronous = NORMAL`.** In WAL mode this is the usual setting. The database can't be corrupted by a crash, but a power cut can lose the last few commits. `FULL` forces a disk flush on every commit and is noticeably slower.
- **`busy_timeout`** is how long a writer waits for the one write lock before giving up with `database is locked`. Phase 4 runs A and B compare `0` with `5000`.

Check any of the experiment databases yourself:

```bash
sqlite3 data/idx_100k.db "PRAGMA journal_mode;"      # wal
```

---

## 8. Caveats

1. **Still one writer.** WAL doesn't let two transactions write at once. In Phase 4, adding `--workers 4` adds processes competing for the **same** lock, not more write capacity.
2. **Copy a WAL database only when it's closed**, or copy all three files together, or run `PRAGMA wal_checkpoint(TRUNCATE)` first. The demo in section 5 shows what happens otherwise. For a live database, use `sqlite3 store.db ".backup copy.db"`, which is always safe. (`cp data/idx_100k.db data/writes.db` in Phase 4 is fine because nothing has `idx_100k.db` open at that point.)
3. **Same machine only.** The `-shm` file is shared memory, so WAL doesn't work on NFS or SMB network drives.
4. **Long-running readers make the WAL grow.** A checkpoint can't move past the oldest open snapshot, so a reader left open blocks it. A forgotten `BEGIN` in a `sqlite3` shell is a classic cause.
5. **Keep `data/` out of cloud-synced folders** (iCloud Drive, Dropbox, OneDrive, Google Drive). The sync client copies files one at a time while the database is open, which can upload a `.db` without the `-wal` it needs. That's the section 5 mistake, done automatically.
6. **Read-only media.** A WAL database needs to create the `-shm` file, so opening one from a read-only location can fail unless you open it with `?mode=ro&immutable=1`.

---

## 9. Cheat sheet

```sql
PRAGMA journal_mode;                  -- which mode is this file in?
PRAGMA journal_mode = WAL;            -- switch (stored in the file); returns the new mode
PRAGMA journal_mode = DELETE;         -- switch back to the rollback journal

PRAGMA wal_autocheckpoint;            -- pages before an automatic checkpoint (default 1000)
PRAGMA wal_checkpoint(TRUNCATE);      -- checkpoint now and empty the -wal file

PRAGMA synchronous = NORMAL;          -- per connection; the usual choice with WAL
PRAGMA busy_timeout = 5000;           -- per connection; ms to wait for the write lock
```

## 10. Check your understanding

1. In the section 4 demo, why did the WAL reader still see 1,000 rows *after* the writer committed? What made it see 1,001?
2. A teammate's Phase 4 runs C and D (`--workers 4`) were no faster than B. Using section 3, explain why WAL didn't help.
3. You email `data/writes.db` to a classmate while your API is still running, and they report fewer purchases than you have. What happened, and give two ways to send a complete copy.
4. Why is it safe for `scale_data.py` to use `journal_mode = OFF`, but not for the API?
