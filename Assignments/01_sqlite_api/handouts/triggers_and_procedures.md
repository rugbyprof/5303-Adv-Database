# Keeping a Summary Table Fresh: Procedures, Triggers, and Schedules in SQLite

In Phase 3 the `/fast` versions of Q13 and Q14 read `monthly_sales`, a pre-aggregated table that `make_dbs.py` builds once from [`sql/summary_tables.sql`](../starter_code/sql/summary_tables.sql). In Phase 4 you inserted new purchases, and the summary check showed the damage:

```bash
sqlite3 data/writes.db "SELECT COUNT(*) FROM purchases; SELECT SUM(num_purchases) FROM monthly_sales;"
```

The two numbers disagree because nothing updates `monthly_sales` after it is built. This walkthrough shows four ways to fix that, using the store schema you already have:

| Approach                                                                             | Runs when                                   | Section                                                                            |
| :----------------------------------------------------------------------------------- | :------------------------------------------ | :--------------------------------------------------------------------------------- |
| A "procedure" you call by hand                                                       | whenever you run it                         | [1](#1-sqlite-has-no-stored-procedures), [2](#2-a-procedure-you-can-call-from-sql) |
| Triggers that update the summary on every write                                      | inside every `INSERT` / `UPDATE` / `DELETE` | [3](#3-triggers-keep-it-fresh-on-every-write)                                      |
| A scheduled job                                                                      | every N minutes                             | [4](#4-can-you-schedule-a-trigger-or-procedure)                                    |
| Triggers that only *mark* months as changed, plus a scheduled job that rebuilds them | both                                        | [5](#5-the-hybrid-mark-dirty-refresh-on-a-schedule)                                |

**The three short answers:**

1. **Stored procedure?** SQLite has none: there is no `CREATE PROCEDURE` and no `CALL`. You get the same effect with a SQL script, a function in your application, or a view-plus-trigger trick that lets you "call" it from SQL with a parameter.
2. **Run it with a trigger?** Yes. Triggers are SQLite's only server-side code, and they can maintain the summary row by row.
3. **Schedule a trigger or procedure?** You can't schedule a trigger in any database. Triggers fire on data changes, never on a clock. You can schedule a *procedure* in PostgreSQL (`pg_cron`) or MySQL (`CREATE EVENT`), but not in SQLite: SQLite is a library, not a server, so nothing runs while no program has the file open. The scheduler has to live outside: cron, Task Scheduler, or a loop inside your FastAPI app.

---

## 0. Setup

Run everything from `starter_code/`. Practice on a scratch copy so your experiment databases stay clean:

```bash
cp data/idx_100k.db data/practice.db        # Windows: copy data\idx_100k.db data\practice.db
```

### A test you will reuse: is the summary in sync?

Save this as `sql/check_monthly_sales.sql`. It rebuilds the aggregate from scratch and compares it with `monthly_sales` **in both directions**:

```sql
-- 0 | 0 means monthly_sales matches the purchases table exactly.
CREATE TEMP VIEW IF NOT EXISTS fresh_monthly_sales AS
SELECT substr(pu.purchase_date, 1, 7) AS month, z.state_code, pu.department,
       COUNT(*) AS num_purchases, ROUND(SUM(pu.amount), 2) AS revenue
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY 1, 2, 3;

SELECT
  (SELECT COUNT(*) FROM (SELECT month, state_code, department, num_purchases, ROUND(revenue, 2)
                         FROM monthly_sales
                         EXCEPT SELECT * FROM fresh_monthly_sales))  AS stale_or_extra,
  (SELECT COUNT(*) FROM (SELECT * FROM fresh_monthly_sales
                         EXCEPT SELECT month, state_code, department, num_purchases, ROUND(revenue, 2)
                         FROM monthly_sales))                        AS missing_or_wrong;
```

> **Why both directions?** `A EXCEPT B` only finds rows that are in A but missing from B. If you only check `monthly_sales EXCEPT fresh`, a brand-new month that is missing from the summary goes unnoticed, and the check happily reports 0. Revenue is rounded on both sides because adding and subtracting floating-point amounts leaves tiny leftovers (a total of `1234.5` might come back as `1234.4999999`).

Now break it on purpose:

```bash
sqlite3 data/practice.db "
  INSERT INTO purchases (customer_id, card_id, product_id, department, amount, purchase_date)
  SELECT customer_id, card_id, product_id, department, amount, '2025-03-31'
  FROM purchases LIMIT 50;" ".read sql/check_monthly_sales.sql"
```

You'll see non-zero numbers in both columns: 50 purchases exist that the summary doesn't know about.

---

## 1. SQLite has no stored procedures

In a client/server database the procedure lives **inside the server** and is written in the server's language:

```sql
-- PostgreSQL, for comparison. This does NOT run in SQLite.
CREATE PROCEDURE refresh_monthly_sales()
LANGUAGE plpgsql AS $$
BEGIN
    TRUNCATE monthly_sales;
    INSERT INTO monthly_sales SELECT ...;
END $$;

CALL refresh_monthly_sales();
```

SQLite runs **inside your program**, so the "procedure language" is just your program's language (Python, here). It has no `CREATE PROCEDURE`, no variables, no `IF`/`LOOP`, no `CALL`. That gives you two everyday substitutes.

### 1a. A SQL script as the procedure

Save as `sql/refresh_monthly_sales.sql`:

```sql
-- Rebuild monthly_sales from scratch, as one atomic step.
BEGIN IMMEDIATE;

DELETE FROM monthly_sales;

INSERT INTO monthly_sales (month, state_code, department, num_purchases, revenue)
SELECT substr(pu.purchase_date, 1, 7), z.state_code, pu.department,
       COUNT(*), SUM(pu.amount)
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY 1, 2, 3;

COMMIT;
```

Call it from the shell or from Python:

```bash
sqlite3 data/practice.db ".read sql/refresh_monthly_sales.sql" ".read sql/check_monthly_sales.sql"
# 0|0
```

```python
con.executescript(Path("sql/refresh_monthly_sales.sql").read_text())
```

Two details matter:

- **The transaction.** Without `BEGIN … COMMIT`, a reader that runs between the `DELETE` and the `INSERT` sees an empty summary table. Inside one transaction, readers in WAL mode keep seeing the old summary until the new one commits.
- **`IMMEDIATE`.** A plain `BEGIN` waits until the first write to take the write lock. `BEGIN IMMEDIATE` takes it right away, so if another writer holds the lock, the script waits (`busy_timeout`) at the start instead of failing halfway through.

How long it takes: about **1.5 s at 1M purchases** (measured on a laptop). That's fine for a nightly job, and far too slow to run on every request.

### 1b. A Python function as the procedure

In a real application this is the most common answer: the procedure is a function in your codebase, and you call it from an admin route, a CLI command, or a scheduler.

```python
def refresh_monthly_sales(con: sqlite3.Connection) -> None:
    con.executescript(Path("sql/refresh_monthly_sales.sql").read_text())
```

---

## 2. A procedure you can call from SQL

Here is a trick that gets you surprisingly close to `CALL refresh_monthly_sales('2025-03')` in pure SQLite. Two features combine:

- A **view** can't be inserted into, but
- an **`INSTEAD OF INSERT` trigger** on the view runs in place of the insert, and sees the inserted values as `NEW.<column>`.

So the view's columns become the procedure's **parameters**, and the trigger body becomes its **code**. Save as `sql/refresh_procedure.sql`:

```sql
DROP VIEW IF EXISTS refresh_monthly_sales;
CREATE VIEW refresh_monthly_sales AS
SELECT NULL AS month;     -- the view's columns are the procedure's parameters

-- "CALL refresh_monthly_sales()"          -->  INSERT INTO refresh_monthly_sales DEFAULT VALUES;
DROP TRIGGER IF EXISTS refresh_monthly_sales_all;
CREATE TRIGGER refresh_monthly_sales_all
INSTEAD OF INSERT ON refresh_monthly_sales
WHEN NEW.month IS NULL
BEGIN
    DELETE FROM monthly_sales;

    INSERT INTO monthly_sales (month, state_code, department, num_purchases, revenue)
    SELECT substr(pu.purchase_date, 1, 7), z.state_code, pu.department,
           COUNT(*), SUM(pu.amount)
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    GROUP BY 1, 2, 3;
END;

-- "CALL refresh_monthly_sales('2025-03')"  -->  INSERT INTO refresh_monthly_sales(month) VALUES ('2025-03');
DROP TRIGGER IF EXISTS refresh_monthly_sales_one;
CREATE TRIGGER refresh_monthly_sales_one
INSTEAD OF INSERT ON refresh_monthly_sales
WHEN NEW.month IS NOT NULL
BEGIN
    DELETE FROM monthly_sales WHERE month = NEW.month;

    INSERT INTO monthly_sales (month, state_code, department, num_purchases, revenue)
    SELECT substr(pu.purchase_date, 1, 7), z.state_code, pu.department,
           COUNT(*), SUM(pu.amount)
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    WHERE pu.purchase_date >= NEW.month || '-01'
      AND pu.purchase_date <  NEW.month || '-32'    -- '-32' sorts after every real day
    GROUP BY 1, 2, 3;
END;
```

Install it once, then call it:

```bash
sqlite3 data/practice.db ".read sql/refresh_procedure.sql"

# refresh one month
sqlite3 data/practice.db "INSERT INTO refresh_monthly_sales(month) VALUES ('2025-03');"

# refresh everything
sqlite3 data/practice.db "INSERT INTO refresh_monthly_sales DEFAULT VALUES;"
```

From Python, with a bound parameter like any other statement:

```python
con.execute("INSERT INTO refresh_monthly_sales(month) VALUES (?)", ("2025-03",))
con.commit()
```

### Why two triggers instead of one with an `OR`?

The obvious first attempt is a single trigger:

```sql
WHERE NEW.month IS NULL
   OR pu.purchase_date >= NEW.month || '-01' AND pu.purchase_date < NEW.month || '-32'
```

That's correct, but it's slow. SQLite plans the trigger's statements once, without knowing whether `NEW.month` will be NULL, so the `OR` stops it from using `idx_purchases_date` and it scans every purchase. Splitting the work into two triggers with `WHEN` clauses gives each statement a plain range condition the index can use:

| At 1M purchases    | One trigger with `OR` | Two triggers with `WHEN` |
| :----------------- | --------------------: | -----------------------: |
| Refresh one month  |                1.07 s |               **0.08 s** |
| Refresh everything |                1.55 s |                   1.53 s |

This is the same lesson as Phase 2: write the `WHERE` so the plan can `SEARCH`. Check it yourself with `EXPLAIN QUERY PLAN` on the inner `SELECT`.

### Limits of the trick

- No return value. To report something, write it to a table.
- No loops or `IF`. Use `WHEN` on the trigger, and `CASE`/`WHERE` inside the statements.
- **Statements inside a trigger can't use `WITH` (CTEs).** Inline the subqueries instead.
- Anyone who can write to the database can "call" it. Fine here; worth knowing.

---

## 3. Triggers: keep it fresh on every write

Instead of rebuilding, adjust **one summary row** every time a purchase changes. For this table that's easy, because `COUNT` and `SUM` can be updated incrementally: an insert adds 1 and the amount, and a delete subtracts them. (`AVG`, `MIN`, `MAX` and `COUNT(DISTINCT …)` are not this easy. Deleting the current `MAX` means rescanning.)

Save as `sql/monthly_sales_triggers.sql`:

```sql
-- INSERT: add the new purchase to its (month, state, department) row.
DROP TRIGGER IF EXISTS monthly_sales_ai;
CREATE TRIGGER monthly_sales_ai
AFTER INSERT ON purchases
BEGIN
    INSERT INTO monthly_sales (month, state_code, department, num_purchases, revenue)
    SELECT substr(NEW.purchase_date, 1, 7), z.state_code, NEW.department, 1, NEW.amount
    FROM customers c
    JOIN zipcodes  z ON z.zipcode = c.zipcode
    WHERE c.customer_id = NEW.customer_id
    ON CONFLICT (month, state_code, department) DO UPDATE SET
        num_purchases = num_purchases + 1,
        revenue       = revenue + excluded.revenue;
END;

-- DELETE: take it back out; drop the row if it reaches zero.
DROP TRIGGER IF EXISTS monthly_sales_ad;
CREATE TRIGGER monthly_sales_ad
AFTER DELETE ON purchases
BEGIN
    UPDATE monthly_sales
    SET num_purchases = num_purchases - 1,
        revenue       = revenue - OLD.amount
    WHERE month      = substr(OLD.purchase_date, 1, 7)
      AND department = OLD.department
      AND state_code = (SELECT z.state_code
                        FROM customers c JOIN zipcodes z ON z.zipcode = c.zipcode
                        WHERE c.customer_id = OLD.customer_id);

    DELETE FROM monthly_sales
    WHERE num_purchases = 0
      AND month      = substr(OLD.purchase_date, 1, 7)
      AND department = OLD.department;
END;

-- UPDATE: an update is a delete of the old row plus an insert of the new one.
DROP TRIGGER IF EXISTS monthly_sales_au;
CREATE TRIGGER monthly_sales_au
AFTER UPDATE OF customer_id, department, amount, purchase_date ON purchases
BEGIN
    UPDATE monthly_sales
    SET num_purchases = num_purchases - 1,
        revenue       = revenue - OLD.amount
    WHERE month      = substr(OLD.purchase_date, 1, 7)
      AND department = OLD.department
      AND state_code = (SELECT z.state_code
                        FROM customers c JOIN zipcodes z ON z.zipcode = c.zipcode
                        WHERE c.customer_id = OLD.customer_id);

    DELETE FROM monthly_sales
    WHERE num_purchases = 0
      AND month      = substr(OLD.purchase_date, 1, 7)
      AND department = OLD.department;

    INSERT INTO monthly_sales (month, state_code, department, num_purchases, revenue)
    SELECT substr(NEW.purchase_date, 1, 7), z.state_code, NEW.department, 1, NEW.amount
    FROM customers c
    JOIN zipcodes  z ON z.zipcode = c.zipcode
    WHERE c.customer_id = NEW.customer_id
    ON CONFLICT (month, state_code, department) DO UPDATE SET
        num_purchases = num_purchases + 1,
        revenue       = revenue + excluded.revenue;
END;
```

Install, then hammer it and check:

```bash
sqlite3 data/practice.db \
  ".read sql/refresh_procedure.sql" \
  "INSERT INTO refresh_monthly_sales DEFAULT VALUES;" \
  ".read sql/monthly_sales_triggers.sql" \
  "INSERT INTO purchases (customer_id, card_id, product_id, department, amount, purchase_date)
     SELECT customer_id, card_id, product_id, department, amount, '2026-09-15' FROM purchases LIMIT 50;" \
  "DELETE FROM purchases WHERE purchase_id % 97 = 0;" \
  "UPDATE purchases SET amount = amount + 1, department = 'Toys', purchase_date = '2024-02-29'
     WHERE purchase_id % 89 = 0;" \
  ".read sql/check_monthly_sales.sql"
# 0|0
```

Start in sync (the full refresh), then install the triggers. A trigger only tracks *changes*, so it can't repair a table that was already wrong.

### How it works, line by line

- **`NEW` and `OLD`** are the row after and before the change. `INSERT` has only `NEW`, `DELETE` only `OLD`, and `UPDATE` has both.
- **The state lookup.** `purchases` has no state. It comes from customer → zipcode → state, the same joins the summary uses.
- **The UPSERT.** `INSERT … ON CONFLICT (pk) DO UPDATE` creates the row the first time a (month, state, department) appears and increments it afterwards. `excluded.revenue` is the value the failed insert *would* have written (here, `NEW.amount`).
- **The UPSERT parsing trap.** With `INSERT … SELECT … ON CONFLICT`, SQLite can't tell whether `ON` begins the upsert or a join's `ON`. A `WHERE` clause on the `SELECT` removes the ambiguity. Ours has one already. If yours doesn't, add `WHERE true`.
- **Keyed cleanup.** `DELETE … WHERE num_purchases = 0` alone would scan the entire summary table on every delete. Adding the key columns makes it a primary-key lookup.
- **`AFTER UPDATE OF col, …`** fires only when one of those columns appears in the `UPDATE`'s `SET` list. Updating `card_id` can't change the summary, so it doesn't fire.

### The blind spot

The summary depends on **three** tables: `purchases`, `customers` (zipcode) and `zipcodes` (state). These triggers watch only `purchases`. Move one active customer to another state and see what happens:

```sql
UPDATE customers
SET zipcode = (SELECT zipcode FROM zipcodes WHERE state_code = 'AK' LIMIT 1)
WHERE customer_id = (SELECT customer_id FROM purchases
                     GROUP BY customer_id ORDER BY COUNT(*) DESC LIMIT 1);
```

On the 100k practice database this left more than **a thousand** summary rows wrong (`1359 | 1254`). Every past purchase by that customer now counts toward a different state, and no trigger fired. You could add triggers to `customers` and `zipcodes` too, but each one has to re-aggregate many rows. Section 5 shows a cheaper fix.

> **Design question:** is "the customer's *current* state" even the right answer for a sale made two years ago? A data warehouse would usually record the state *on the purchase* at the time of sale. This kind of history-tracking is called a "slowly changing dimension".

### What triggers cost

A trigger runs **inside** the writing transaction, so its time is added to every write, and it holds SQLite's single write lock while it runs.

| Measured on 20k purchases                      |     No triggers |          With triggers |
| :--------------------------------------------- | --------------: | ---------------------: |
| 3,000 inserts, one commit each (like the API)  | 26,152 writes/s | 22,375 writes/s (−15%) |
| 100,000 inserts in one transaction (bulk load) |          0.31 s |   3.19 s (~10× slower) |

When each request commits on its own, the cost of the commit dominates and the trigger costs about 15%. In a bulk load it's 10×. The standard practice is: **drop the triggers, bulk load, run the full refresh, then recreate the triggers.**

---

## 4. Can you schedule a trigger or procedure?

|                                | Trigger                                        | Stored procedure                                                                                             |
| :----------------------------- | :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| **What starts it**             | an `INSERT`, `UPDATE` or `DELETE` on its table | someone calls it                                                                                             |
| **Schedule it in SQLite?**     | No                                             | No (there are no procedures)                                                                                 |
| **Schedule it in PostgreSQL?** | No                                             | Yes, with the `pg_cron` extension: `SELECT cron.schedule('*/10 * * * *', 'CALL refresh_monthly_sales()');`   |
| **Schedule it in MySQL?**      | No                                             | Yes, with the event scheduler: `CREATE EVENT … ON SCHEDULE EVERY 10 MINUTE DO CALL refresh_monthly_sales();` |

Triggers are **event-driven** by definition. "Every 10 minutes" isn't a data change, so no database can put a trigger on a timer.

SQLite can't schedule anything for a more basic reason: **it isn't a running program**. It's a library your process links in. When no process has the file open, no SQLite code is running at all. So the clock must live outside the database. Three common places:

### 4a. The operating system scheduler (cron)

`crontab -e`, then add one line (use full paths: cron doesn't run in your project folder or virtualenv):

```cron
# every 10 minutes, rebuild the summary
*/10 * * * * cd /path/to/starter_code && sqlite3 data/practice.db ".read sql/refresh_monthly_sales.sql" >> refresh.log 2>&1
```

On Windows, Task Scheduler does the same. On macOS, cron works; `launchd` is the native option.

### 4b. Inside your FastAPI app

Start a background loop when the app starts, and stop it on shutdown:

```python
# app/main.py
import asyncio
from contextlib import asynccontextmanager

from refresh_job import refresh_dirty_months     # section 5


async def refresh_loop():
    while True:
        await asyncio.sleep(600)                                   # every 10 minutes
        await asyncio.to_thread(refresh_dirty_months, "data/practice.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(refresh_loop())
    yield
    task.cancel()


app = FastAPI(title="SQLite API -- Assignment 01", lifespan=lifespan)
```

`asyncio.to_thread` keeps the blocking SQLite work off the event loop, so requests are still served while it runs. One caveat: with `uvicorn --workers 4` you get **four** loops, one per process. Each refresh is atomic so that's still safe, just wasteful. That's why production systems usually prefer 4a, or a dedicated worker process.

### 4c. Scheduled job versus trigger

|                         | Triggers (section 3) | Scheduled full refresh (4a / 4b)            |
| :---------------------- | :------------------- | :------------------------------------------ |
| Freshness               | always exact         | up to N minutes stale                       |
| Cost per write          | +15% (more for bulk) | none                                        |
| Cost per refresh        | none                 | ~1.5 s at 1M rows, with the write lock held |
| Catches customer moves? | no                   | yes                                         |

Section 5 combines the two.

---

## 5. The hybrid: mark dirty, refresh on a schedule

Let the triggers do the **cheapest possible** thing, which is to remember *which months changed*. A scheduled job then rebuilds only those months with the procedure from section 2.

Save as `sql/monthly_sales_dirty.sql`. If you installed the section 3 triggers, drop them first, because you want one approach or the other:

```sql
DROP TRIGGER IF EXISTS monthly_sales_ai;
DROP TRIGGER IF EXISTS monthly_sales_ad;
DROP TRIGGER IF EXISTS monthly_sales_au;

CREATE TABLE IF NOT EXISTS monthly_sales_dirty (
    month     TEXT PRIMARY KEY,
    marked_at TEXT NOT NULL DEFAULT (datetime('now'))
);

DROP TRIGGER IF EXISTS purchases_mark_dirty_ai;
CREATE TRIGGER purchases_mark_dirty_ai AFTER INSERT ON purchases
BEGIN
    INSERT OR IGNORE INTO monthly_sales_dirty(month) VALUES (substr(NEW.purchase_date, 1, 7));
END;

DROP TRIGGER IF EXISTS purchases_mark_dirty_ad;
CREATE TRIGGER purchases_mark_dirty_ad AFTER DELETE ON purchases
BEGIN
    INSERT OR IGNORE INTO monthly_sales_dirty(month) VALUES (substr(OLD.purchase_date, 1, 7));
END;

DROP TRIGGER IF EXISTS purchases_mark_dirty_au;
CREATE TRIGGER purchases_mark_dirty_au AFTER UPDATE ON purchases
BEGIN
    INSERT OR IGNORE INTO monthly_sales_dirty(month) VALUES (substr(OLD.purchase_date, 1, 7));
    INSERT OR IGNORE INTO monthly_sales_dirty(month) VALUES (substr(NEW.purchase_date, 1, 7));
END;

-- A customer who moves changes the state of every purchase they ever made.
DROP TRIGGER IF EXISTS customers_mark_dirty_au;
CREATE TRIGGER customers_mark_dirty_au AFTER UPDATE OF zipcode ON customers
BEGIN
    INSERT OR IGNORE INTO monthly_sales_dirty(month)
    SELECT DISTINCT substr(purchase_date, 1, 7)
    FROM purchases
    WHERE customer_id = NEW.customer_id;
END;
```

`INSERT OR IGNORE` against the primary key means 500 inserts into March produce **one** dirty row, not 500.

The job, saved as `refresh_job.py`:

```python
"""refresh_job.py -- rebuild only the months that changed since the last run."""
import sqlite3
import sys


def refresh_dirty_months(db_path: str) -> list[str]:
    con = sqlite3.connect(db_path, timeout=10, isolation_level=None)   # we manage BEGIN/COMMIT
    try:
        con.execute("BEGIN IMMEDIATE")        # take the write lock now, not halfway through
        months = [m for (m,) in con.execute("SELECT month FROM monthly_sales_dirty ORDER BY month")]
        for m in months:
            con.execute("INSERT INTO refresh_monthly_sales(month) VALUES (?)", (m,))
        con.execute("DELETE FROM monthly_sales_dirty")
        con.execute("COMMIT")
        return months
    finally:
        con.close()


if __name__ == "__main__":
    months = refresh_dirty_months(sys.argv[1] if len(sys.argv) > 1 else "data/practice.db")
    print(f"refreshed {len(months)} month(s): {', '.join(months) or '-'}")
```

Try it:

```bash
sqlite3 data/practice.db ".read sql/refresh_procedure.sql" ".read sql/monthly_sales_dirty.sql"

sqlite3 data/practice.db \
  "INSERT INTO purchases (customer_id, card_id, product_id, department, amount, purchase_date)
     SELECT customer_id, card_id, product_id, department, amount, '2025-03-31' FROM purchases LIMIT 30;" \
  "DELETE FROM purchases WHERE purchase_id IN (5, 6);" \
  "SELECT * FROM monthly_sales_dirty;" \
  ".read sql/check_monthly_sales.sql"          # out of sync

python refresh_job.py data/practice.db         # refreshed 3 month(s): 2024-11, 2025-03, ...  (yours will differ)
sqlite3 data/practice.db ".read sql/check_monthly_sales.sql"   # 0|0
python refresh_job.py data/practice.db         # refreshed 0 month(s): -
```

Then schedule `python refresh_job.py data/practice.db` with cron (4a), or call `refresh_dirty_months` from the FastAPI loop (4b).

Why the job is safe:

- **Reading the queue and clearing it happen in one `IMMEDIATE` transaction.** No writer can slip a purchase in between "which months are dirty?" and "clear the list". If one did, that month would be cleared without being rebuilt.
- **It reuses the indexed one-month procedure** from section 2: about 0.08 s per dirty month at 1M rows, instead of 1.5 s for everything.
- **The customer-move blind spot is covered.** In testing, moving the busiest customer marked 32 months dirty, and one job run brought the summary back to `0|0`.

---

## 6. Which one should you use?

| Need                                                   | Use                                                                            |
| :----------------------------------------------------- | :----------------------------------------------------------------------------- |
| A one-off fix, or after a bulk load                    | the full refresh (section 1a or 2)                                             |
| Totals must be exact the moment a write commits        | incremental triggers (section 3), and accept the write cost and the blind spot |
| A few minutes stale is fine, and writes must stay fast | the hybrid (section 5) on a schedule                                           |
| The summary is cheap to compute anyway                 | no summary table: just run the query (Q13's slow route at 10k rows)            |

## 7. Try it

1. Re-run **Phase 4 Run B** against a `writes.db` that has the section 3 triggers installed. How did writes/sec change? Then do the same with the section 5 triggers. Which costs more per write, and why?
2. After the load test, run `sql/check_monthly_sales.sql` against `writes.db`, both with and without triggers. Use the result to answer FINDINGS Phase 4, question 3.
3. Run `EXPLAIN QUERY PLAN` on the inner `SELECT` of `refresh_monthly_sales_one`, with and without the `OR NEW.month IS NULL` version. Find the line that changes.
4. Write the `AFTER UPDATE OF state_code ON zipcodes` trigger that section 5 is still missing.

## Cleanup

```sql
DROP TRIGGER IF EXISTS monthly_sales_ai;
DROP TRIGGER IF EXISTS monthly_sales_ad;
DROP TRIGGER IF EXISTS monthly_sales_au;
DROP TRIGGER IF EXISTS purchases_mark_dirty_ai;
DROP TRIGGER IF EXISTS purchases_mark_dirty_ad;
DROP TRIGGER IF EXISTS purchases_mark_dirty_au;
DROP TRIGGER IF EXISTS customers_mark_dirty_au;
DROP TABLE   IF EXISTS monthly_sales_dirty;
DROP VIEW    IF EXISTS refresh_monthly_sales;     -- also drops its INSTEAD OF triggers
```

Or just `rm data/practice.db`.

---

*All timings were measured with SQLite 3.54 on an Apple-silicon laptop, using data from `scale_data.py`. Your numbers will differ; the ratios are what matter.*
