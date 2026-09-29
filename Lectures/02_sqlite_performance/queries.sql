-- =============================================================================
-- 01_reading_plans.sql  --  SCAN vs SEARCH, covering indexes, temp B-trees
-- =============================================================================
-- Run from Lectures/02_sqlite_performance against the scaled database:
--     sqlite3 perf.db ".read sql/01_reading_plans.sql"
-- .eqp on prints each statement's query plan before its result;
-- .timer on prints wall time after it. Read the PLAN first, the TIME second.
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. Primary-key lookup: one B-tree descent. Cost does not grow with the table.
--    PLAN: SEARCH purchases USING INTEGER PRIMARY KEY (rowid=?)
SELECT * FROM purchases WHERE purchase_id = 500000;

-- 2. Range on an indexed column, and the index alone answers the query.
--    PLAN: SEARCH ... USING COVERING INDEX idx_purchases_date (purchase_date>?)
--    "COVERING" = never touched the table; every needed column is in the index
--    (purchase_date, plus the rowid that every SQLite index entry ends with).
SELECT count(*) FROM purchases WHERE purchase_date >= '2026-08-01';

-- 3. Same range, but now we want columns the index doesn't have.
--    PLAN: SEARCH ... USING INDEX idx_purchases_date   (no "COVERING")
--    Each index hit costs one extra lookup into the table by rowid.
SELECT purchase_id, amount FROM purchases WHERE purchase_date = '2026-08-01' LIMIT 5;

-- 4. Filter on a column with no index: read every row.
--    PLAN: SCAN purchases
SELECT count(*) FROM purchases WHERE amount > 395;

-- 5. Sort on a column with no index: read every row AND sort them.
--    PLAN: SCAN purchases + USE TEMP B-TREE FOR ORDER BY
--    LIMIT 5 does not save the scan -- the top 5 aren't known until all rows are seen.
SELECT purchase_id, amount FROM purchases ORDER BY amount DESC LIMIT 5;

-- 6. Group on an expression: no index can be in that order -> temp B-tree.
--    PLAN: SCAN ... + USE TEMP B-TREE FOR GROUP BY
SELECT strftime('%Y', purchase_date) AS yr, count(*) AS n
FROM purchases GROUP BY yr;

-- 7. A correlated subquery runs once per outer row.
--    PLAN: CORRELATED SCALAR SUBQUERY -- multiply its cost by the outer row count.
SELECT pr.product_id, pr.product_name,
       (SELECT count(*) FROM purchases pu WHERE pu.product_id = pr.product_id) AS times_sold
FROM products pr
WHERE pr.product_id <= 5;

-- 8. The planner can choose badly. Revenue per department for ONE month:
--    it walks idx_purchases_department (all 1M rows, in department order, each
--    with a table lookup) to avoid a sort -- instead of using the date index
--    to find the ~3% of rows that match.
SELECT department, round(sum(amount), 2) AS revenue
FROM purchases
WHERE purchase_date >= '2026-08-01'
GROUP BY department;

--    Unary + on the GROUP BY term tells the planner "don't use an index for
--    this term". Now it SEARCHes the date index and sorts ~30k rows instead.
SELECT department, round(sum(amount), 2) AS revenue
FROM purchases
WHERE purchase_date >= '2026-08-01'
GROUP BY +department;

-- 9. What the planner knows: row counts and average rows-per-key from ANALYZE.
--    "1000000 45455" = 1M rows, ~45k rows per department value.
SELECT tbl, idx, stat FROM sqlite_stat1 WHERE tbl = 'purchases';
-- =============================================================================
-- 02_pagination.sql  --  OFFSET vs keyset (seek) pagination
-- =============================================================================
--     sqlite3 perf.db ".read sql/02_pagination.sql"
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. Page 1 with OFFSET: fast.
SELECT pu.purchase_id, pu.purchase_date, pr.product_name, pu.amount
FROM purchases pu JOIN products pr ON pr.product_id = pu.product_id
ORDER BY pu.purchase_id
LIMIT 5 OFFSET 0;

-- 2. "Page 180,001" with OFFSET: same plan, same 5 rows out -- but SQLite must
--    produce and throw away 900,000 joined rows to get there. Cost grows with
--    the page number.
SELECT pu.purchase_id, pu.purchase_date, pr.product_name, pu.amount
FROM purchases pu JOIN products pr ON pr.product_id = pu.product_id
ORDER BY pu.purchase_id
LIMIT 5 OFFSET 900000;

-- 3. Keyset / seek: the client sends back the last key it saw ("cursor"), and
--    the query SEEKs straight to it in the B-tree. Cost is the same for page 1
--    and page 180,001.
--    PLAN: SEARCH pu USING INTEGER PRIMARY KEY (rowid>?)
SELECT pu.purchase_id, pu.purchase_date, pr.product_name, pu.amount
FROM purchases pu JOIN products pr ON pr.product_id = pu.product_id
WHERE pu.purchase_id > 900000          -- :cursor = last purchase_id of previous page
ORDER BY pu.purchase_id
LIMIT 5;

-- 4. Keyset on a NON-unique sort column (newest purchases first).
--    purchase_date alone isn't unique, so a cursor of just a date would skip or
--    repeat rows that share it. Add a unique tie-breaker and compare as a
--    row value: (date, id) < (:last_date, :last_id).
--    Every SQLite index entry already ends with the rowid, so
--    idx_purchases_date is really an index on (purchase_date, purchase_id) --
--    it serves this ORDER BY and seek with no sort.
SELECT purchase_id, purchase_date, amount
FROM purchases
ORDER BY purchase_date DESC, purchase_id DESC
LIMIT 5;

--    Next page: plug in the LAST row of the page above as the cursor.
SELECT purchase_id, purchase_date, amount
FROM purchases
WHERE (purchase_date, purchase_id) < ('2026-08-31', 998207)
ORDER BY purchase_date DESC, purchase_id DESC
LIMIT 5;

-- 5. What keyset gives up: "jump to page 50,000" is no longer a thing -- only
--    next/previous from a known row. For an API feed, that's usually fine.
-- =============================================================================
-- 03_search_fts5.sql  --  LIKE vs indexes, and full-text search with FTS5
-- =============================================================================
--     sqlite3 perf.db ".read sql/03_search_fts5.sql"
-- Examples search CUSTOMERS (50k rows). Creates two indexes and two FTS tables,
-- then drops them at the end so the script is re-runnable.
-- =============================================================================

.eqp on
.timer on
.mode box

-- ---------------------------------------------------------------------------
-- Part 1: when can LIKE use an index?
-- ---------------------------------------------------------------------------

-- 1a. Leading wildcard: no index can help -- a B-tree is sorted by the START
--     of the string. SQLite scans the smallest thing holding the column (here
--     the UNIQUE index on email) and tests every entry.
SELECT count(*) FROM customers WHERE email LIKE '%hopper%';

-- 1b. Prefix pattern -- surely THIS uses the email index? No:
--     LIKE is case-INsensitive in SQLite, but the index is sorted
--     case-sensitively (BINARY collation), so a range seek could miss 'Grace…'.
SELECT count(*) FROM customers WHERE email LIKE 'grace%';

-- 1c. Give LIKE an index whose collation matches it: NOCASE.
--     Now a prefix pattern becomes a range SEARCH (last_name>? AND last_name<?).
CREATE INDEX idx_customers_last_nocase ON customers(last_name COLLATE NOCASE);
SELECT count(*) FROM customers WHERE last_name LIKE 'Hop%';

--     ...but a leading wildcard still can't seek -- it just scans the smaller index.
SELECT count(*) FROM customers WHERE last_name LIKE '%per';

-- ---------------------------------------------------------------------------
-- Part 2: FTS5 -- an inverted index (token -> list of rowids)
-- ---------------------------------------------------------------------------

-- 2a. External-content FTS table: the index lives in customers_fts, the text
--     stays in customers (no second copy). content_rowid ties them together.
CREATE VIRTUAL TABLE customers_fts USING fts5(
    first_name, last_name, email,
    content = 'customers', content_rowid = 'customer_id'
);
-- Build the index from the existing rows (one-time cost).
INSERT INTO customers_fts(customers_fts) VALUES ('rebuild');

-- 2b. MATCH finds rows by TOKEN. The default tokenizer (unicode61) splits on
--     punctuation, so 'grace.hopper.45@example.com' becomes grace|hopper|45|example|com.
--     PLAN: SCAN customers_fts VIRTUAL TABLE INDEX 0:M… -- for a virtual table
--     "SCAN" just means "asked the FTS module"; the M means a MATCH lookup.
SELECT count(*) FROM customers_fts WHERE customers_fts MATCH 'hopper';

-- 2c. Boolean operators, prefix queries (hop*), column filters, and ranking.
--     Join back to the real table by rowid for the columns you want.
SELECT c.customer_id, c.first_name, c.last_name, c.email
FROM customers_fts f
JOIN customers c ON c.customer_id = f.rowid
WHERE customers_fts MATCH 'grace AND hop*'
ORDER BY f.rank                     -- bm25 relevance; lower = better
LIMIT 5;

SELECT rowid, highlight(customers_fts, 2, '[', ']') AS email
FROM customers_fts
WHERE customers_fts MATCH 'email:lovelace'
LIMIT 3;

-- 2d. Tokens are WHOLE words. 'ove' is not a token, so MATCH finds nothing,
--     while LIKE '%ove%' finds every "lovelace". FTS is not a substring index.
SELECT count(*) AS fts_hits  FROM customers_fts WHERE customers_fts MATCH 'ove';
SELECT count(*) AS like_hits FROM customers     WHERE email LIKE '%ove%';

-- 2e. Want substring search indexed? The trigram tokenizer indexes every
--     3-character slice, and then LIKE '%…%' itself can use the FTS index
--     (plan shows INDEX 0:L…). Bigger index; patterns shorter than 3 characters
--     fall back to scanning.
CREATE VIRTUAL TABLE customers_tri USING fts5(
    email, content = 'customers', content_rowid = 'customer_id', tokenize = 'trigram'
);
INSERT INTO customers_tri(customers_tri) VALUES ('rebuild');
SELECT count(*) FROM customers_tri WHERE email LIKE '%ove%';

-- ---------------------------------------------------------------------------
-- Part 3: keeping an external-content index in sync
-- ---------------------------------------------------------------------------
-- The FTS table does NOT watch customers by itself. Without these triggers,
-- new/changed customers are invisible to MATCH (and deletes leave ghosts).
CREATE TRIGGER customers_fts_ai AFTER INSERT ON customers BEGIN
    INSERT INTO customers_fts(rowid, first_name, last_name, email)
    VALUES (new.customer_id, new.first_name, new.last_name, new.email);
END;
CREATE TRIGGER customers_fts_ad AFTER DELETE ON customers BEGIN
    INSERT INTO customers_fts(customers_fts, rowid, first_name, last_name, email)
    VALUES ('delete', old.customer_id, old.first_name, old.last_name, old.email);
END;
CREATE TRIGGER customers_fts_au AFTER UPDATE ON customers BEGIN
    INSERT INTO customers_fts(customers_fts, rowid, first_name, last_name, email)
    VALUES ('delete', old.customer_id, old.first_name, old.last_name, old.email);
    INSERT INTO customers_fts(rowid, first_name, last_name, email)
    VALUES (new.customer_id, new.first_name, new.last_name, new.email);
END;

-- ---------------------------------------------------------------------------
-- Clean up so the script can be re-run.
-- ---------------------------------------------------------------------------
.eqp off
.timer off
DROP TRIGGER customers_fts_ai;
DROP TRIGGER customers_fts_ad;
DROP TRIGGER customers_fts_au;
DROP TABLE customers_fts;
DROP TABLE customers_tri;
DROP INDEX idx_customers_last_nocase;
-- =============================================================================
-- 04_counting.sql  --  what COUNT(*) really costs, and cheaper answers
-- =============================================================================
--     sqlite3 perf.db ".read sql/04_counting.sql"
-- SQLite keeps NO stored row count. Every count(*) walks something.
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. Whole table: SQLite walks the SMALLEST B-tree that has one entry per row
--    -- usually some index, not the table itself. Still O(rows), just fewer pages.
SELECT count(*) FROM purchases;

-- 2. Filter on an indexed column: count only the matching index range.
SELECT count(*) FROM purchases WHERE department = 'Books';

-- 3. Filter on an unindexed column: full table scan for one number.
SELECT count(*) FROM purchases WHERE amount BETWEEN 100 AND 200;

-- 4. A page of results + its total is TWO queries -- and the total is usually
--    the expensive one: the page stops after LIMIT rows, the count never stops early.
SELECT purchase_id, amount FROM purchases
WHERE amount BETWEEN 100 AND 200 ORDER BY purchase_id LIMIT 5;

-- ---------------------------------------------------------------------------
-- Cheaper alternatives
-- ---------------------------------------------------------------------------

-- 5. Capped count: "1,000+ results" is as useful to a human as 250,123,
--    and stops after 1,001 matches.
SELECT count(*) AS n FROM (
    SELECT 1 FROM purchases WHERE amount BETWEEN 100 AND 200 LIMIT 1001
);

-- 6. "Is there a next page?" -- fetch LIMIT + 1 rows; if you got 6, there's more.
SELECT purchase_id FROM purchases
WHERE amount BETWEEN 100 AND 200 AND purchase_id > 0
ORDER BY purchase_id LIMIT 6;

-- 7. Estimate from planner statistics (instant, can be stale -- refreshed by ANALYZE).
SELECT CAST(substr(stat, 1, instr(stat, ' ') - 1) AS INTEGER) AS approx_rows
FROM sqlite_stat1 WHERE tbl = 'purchases' LIMIT 1;

-- 8. Maintained counter: a tiny table kept exact by triggers. Reads are O(1);
--    every insert/delete pays a little extra write (and write contention on
--    one hot row -- remember that in Phase 4).
CREATE TABLE row_counts (tbl TEXT PRIMARY KEY, n INTEGER NOT NULL);
INSERT INTO row_counts SELECT 'purchases', count(*) FROM purchases;
CREATE TRIGGER purchases_count_ai AFTER INSERT ON purchases BEGIN
    UPDATE row_counts SET n = n + 1 WHERE tbl = 'purchases';
END;
CREATE TRIGGER purchases_count_ad AFTER DELETE ON purchases BEGIN
    UPDATE row_counts SET n = n - 1 WHERE tbl = 'purchases';
END;
SELECT n FROM row_counts WHERE tbl = 'purchases';

-- Clean up.
.eqp off
.timer off
DROP TRIGGER purchases_count_ai;
DROP TRIGGER purchases_count_ad;
DROP TABLE row_counts;
-- =============================================================================
-- 05_window_functions.sql  --  ranking, running totals, frames, and their cost
-- =============================================================================
--     sqlite3 perf.db ".read sql/05_window_functions.sql"
-- A window function computes a value for each row from a "window" of related
-- rows -- WITHOUT collapsing them the way GROUP BY does.
--     f(...) OVER (PARTITION BY <groups> ORDER BY <order> <frame>)
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. The three ranking functions differ only on ties.
--    row_number: 1,2,3,4   rank: 1,2,2,4   dense_rank: 1,2,2,3
WITH t(v) AS (VALUES (50), (40), (40), (10))
SELECT v, row_number() OVER w AS row_number, rank() OVER w AS rank,
       dense_rank() OVER w AS dense_rank
FROM t
WINDOW w AS (ORDER BY v DESC);

-- 2. Aggregate FIRST, window SECOND. Revenue per product for the last 30 days
--    of data, then rank products *within each department*. The GROUP BY shrinks
--    ~30k rows to a few thousand; the window then only sorts those.
WITH recent AS (
    SELECT department, product_id, sum(amount) AS revenue
    FROM purchases
    WHERE purchase_date > date((SELECT max(purchase_date) FROM purchases), '-30 days')
    GROUP BY department, product_id
),
ranked AS (
    SELECT department, product_id, round(revenue, 2) AS revenue,
           rank() OVER (PARTITION BY department ORDER BY revenue DESC) AS rnk
    FROM recent
)
SELECT * FROM ranked
WHERE rnk <= 2                      -- can't filter on a window in WHERE of the same SELECT
  AND department IN ('Books', 'Toys')
ORDER BY department, rnk;

-- 3. Running total for one customer: the frame "from the first row up to this one".
--    ROWS counts physical rows; ties in purchase_date are broken by purchase_id
--    so the order (and the total) is deterministic.
SELECT purchase_id, purchase_date, amount,
       round(sum(amount) OVER (ORDER BY purchase_date, purchase_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2)
           AS running_total
FROM purchases
WHERE customer_id = 1
ORDER BY purchase_date, purchase_id;

-- 4. Trailing TIME window: "spend in the 30 days ending on this purchase".
--    ROWS BETWEEN 29 PRECEDING would mean 29 *purchases* back, not 29 days.
--    RANGE measures distance in the ORDER BY value, which must be a number --
--    so order by the day number (julianday), not the ISO text.
SELECT purchase_id, purchase_date, amount,
       round(sum(amount) OVER (ORDER BY julianday(purchase_date)
                               RANGE BETWEEN 29 PRECEDING AND CURRENT ROW), 2)
           AS spend_last_30_days
FROM purchases
WHERE customer_id = 1
ORDER BY purchase_date, purchase_id;

-- 5. Same idea store-wide: daily revenue with a 7-day moving average.
--    Aggregate to ~970 days first, then the window is trivial.
WITH daily AS (
    SELECT purchase_date AS day, sum(amount) AS revenue
    FROM purchases GROUP BY purchase_date
)
SELECT day, round(revenue, 2) AS revenue,
       round(avg(revenue) OVER (ORDER BY julianday(day)
                                RANGE BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS avg_7d
FROM daily
ORDER BY day DESC
LIMIT 7;

-- 6. The expensive shape: a window partitioned over the WHOLE fact table.
--    "Each customer's single largest purchase." Every one of 1M rows must be
--    visited in (customer_id, amount) order before it can be numbered.
--    The plan walks idx_purchases_customer (with a table lookup per row, to get
--    amount) and then sorts each customer's rows: TEMP B-TREE FOR LAST TERM.
SELECT count(*) AS customers_with_a_top_purchase FROM (
    SELECT customer_id, amount,
           row_number() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn
    FROM purchases
)
WHERE rn = 1;

-- 7. For "top 1 per group" a plain GROUP BY answers the same question with no
--    sort. Windows are the general tool; check whether a simpler aggregate does.
SELECT count(*) FROM (
    SELECT customer_id, max(amount) FROM purchases GROUP BY customer_id
);

-- 8. Surprise: forbid the index and it gets FASTER. Walking a non-covering
--    index across the whole table means 1M *random* lookups into the table;
--    a straight SCAN reads the table in storage order and sorts in memory.
--    An index is a win when it lets you touch FEW rows -- not when you touch
--    all of them anyway.
SELECT count(*) FROM (
    SELECT customer_id, max(amount) FROM purchases NOT INDEXED GROUP BY customer_id
);

-- 9. What does help a whole-table pass: a COVERING index, already in the right
--    order, holding every column the query reads. No lookups, no sort.
CREATE INDEX idx_purchases_customer_amount ON purchases(customer_id, amount);

SELECT count(*) FROM (
    SELECT customer_id, max(amount) FROM purchases GROUP BY customer_id
);

.eqp off
.timer off
DROP INDEX idx_purchases_customer_amount;
-- =============================================================================
-- 06_gaps_islands.sql  --  finding runs of consecutive values
-- =============================================================================
--     sqlite3 perf.db ".read sql/06_gaps_islands.sql"
-- "Islands" are runs of consecutive values (days, months, ids); "gaps" are the
-- holes between them. Classic questions: longest streak, current streak,
-- missing ids, outages.
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. The trick, on data small enough to read. Number the values in order.
--    Inside a run, value and row_number both go up by 1, so their DIFFERENCE
--    stays constant -- and it changes at every gap. That difference is the
--    island id.
WITH v(n) AS (VALUES (1), (2), (3), (7), (8), (12), (13), (14), (15))
SELECT n,
       row_number() OVER (ORDER BY n)     AS rn,
       n - row_number() OVER (ORDER BY n) AS island
FROM v;

-- 2. Collapse each island to one row.
WITH v(n) AS (VALUES (1), (2), (3), (7), (8), (12), (13), (14), (15)),
     tagged AS (SELECT n, n - row_number() OVER (ORDER BY n) AS island FROM v)
SELECT min(n) AS run_start, max(n) AS run_end, count(*) AS run_length
FROM tagged
GROUP BY island
ORDER BY run_start;

-- 3. Real data: consecutive MONTHS in which customer 54 bought something.
--    Steps: (a) one row per distinct month, (b) turn the month into an integer
--    so "consecutive" means "+1", (c) subtract row_number, (d) group.
--    Duplicates must be removed first (DISTINCT) -- two purchases in the same
--    month would otherwise break the "+1 per row" arithmetic.
WITH months AS (
    SELECT DISTINCT
           CAST(strftime('%Y', purchase_date) AS INTEGER) * 12
         + CAST(strftime('%m', purchase_date) AS INTEGER) AS m
    FROM purchases
    WHERE customer_id = 54
),
tagged AS (
    SELECT m, m - row_number() OVER (ORDER BY m) AS island FROM months
)
SELECT printf('%d-%02d', (min(m) - 1) / 12, (min(m) - 1) % 12 + 1) AS first_month,
       printf('%d-%02d', (max(m) - 1) / 12, (max(m) - 1) % 12 + 1) AS last_month,
       count(*) AS months_in_a_row
FROM tagged
GROUP BY island
ORDER BY months_in_a_row DESC, first_month
LIMIT 5;

-- 4. Same question with LAG: flag a row that starts a new island (gap > 1 from
--    the previous value), then a running SUM of the flags numbers the islands.
--    Handy when "consecutive" isn't a simple +1 (e.g. "within 3 days").
WITH months AS (
    SELECT DISTINCT
           CAST(strftime('%Y', purchase_date) AS INTEGER) * 12
         + CAST(strftime('%m', purchase_date) AS INTEGER) AS m
    FROM purchases
    WHERE customer_id = 54
),
flagged AS (
    SELECT m, CASE WHEN m - lag(m) OVER (ORDER BY m) = 1 THEN 0 ELSE 1 END AS new_island
    FROM months
),
numbered AS (
    SELECT m, sum(new_island) OVER (ORDER BY m ROWS UNBOUNDED PRECEDING) AS island
    FROM flagged
)
SELECT island, count(*) AS months_in_a_row
FROM numbered GROUP BY island ORDER BY months_in_a_row DESC LIMIT 3;

-- 5. Why it scales badly: the same query for EVERY customer at once.
--    One customer = a SEARCH on idx_purchases_customer (a few dozen rows).
--    All customers = DISTINCT over 1M rows, then a PARTITIONed window sort,
--    then another GROUP BY -- several temp B-trees over the whole table.
WITH months AS (
    SELECT DISTINCT customer_id,
           CAST(strftime('%Y', purchase_date) AS INTEGER) * 12
         + CAST(strftime('%m', purchase_date) AS INTEGER) AS m
    FROM purchases
),
tagged AS (
    SELECT customer_id,
           m - row_number() OVER (PARTITION BY customer_id ORDER BY m) AS island
    FROM months
),
runs AS (
    SELECT customer_id, count(*) AS len FROM tagged GROUP BY customer_id, island
)
SELECT len AS longest_monthly_streak, count(*) AS customers
FROM (SELECT customer_id, max(len) AS len FROM runs GROUP BY customer_id)
GROUP BY len
ORDER BY len DESC
LIMIT 5;
-- =============================================================================
-- 07_ctes_aggregation.sql  --  multi-key GROUP BY, CTEs, and counting the scans
-- =============================================================================
--     sqlite3 perf.db ".read sql/07_ctes_aggregation.sql"
-- A CTE (WITH name AS (...)) names a step. It does NOT make anything faster by
-- itself: every CTE that reads purchases is potentially another pass over 1M rows.
-- The question to ask of any report query: HOW MANY TIMES does it read the big table?
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. Multi-key GROUP BY + HAVING: revenue by (department, card type, year),
--    keeping only big groups. One pass over purchases (+ a cards lookup per row)
--    and one temp B-tree to bring equal keys together.
SELECT pu.department, cd.card_type, strftime('%Y', pu.purchase_date) AS yr,
       count(*) AS n, round(sum(pu.amount), 2) AS revenue
FROM purchases pu
JOIN cards cd ON cd.card_id = pu.card_id
GROUP BY pu.department, cd.card_type, yr
HAVING count(*) > 4000
ORDER BY revenue DESC
LIMIT 5;

-- 2. "Each department's revenue by card type, AND that department's total so we
--    can show a share." Written naively as two CTEs, each reading purchases:
--    look for TWO scans of purchases in the plan.
WITH by_card AS (
    SELECT pu.department, cd.card_type, sum(pu.amount) AS revenue
    FROM purchases pu JOIN cards cd ON cd.card_id = pu.card_id
    GROUP BY pu.department, cd.card_type
),
by_dept AS (
    SELECT department, sum(amount) AS dept_revenue
    FROM purchases GROUP BY department
)
SELECT b.department, b.card_type,
       round(100.0 * b.revenue / d.dept_revenue, 2) AS pct_of_dept
FROM by_card b JOIN by_dept d USING (department)
ORDER BY pct_of_dept DESC
LIMIT 3;

-- 3. Same answer, ONE pass: aggregate at the finest grain once, then derive the
--    coarser total from that small result (286 rows) with a window.
WITH by_card AS (
    SELECT pu.department, cd.card_type, sum(pu.amount) AS revenue
    FROM purchases pu JOIN cards cd ON cd.card_id = pu.card_id
    GROUP BY pu.department, cd.card_type
)
SELECT department, card_type,
       round(100.0 * revenue / sum(revenue) OVER (PARTITION BY department), 2) AS pct_of_dept
FROM by_card
ORDER BY pct_of_dept DESC
LIMIT 3;

-- 4. SQLite has no GROUP BY ROLLUP / CUBE (PostgreSQL does). Subtotals are
--    built by UNION ALL-ing several groupings. Do it from ONE materialized
--    fine-grained CTE, not by re-reading purchases for each level.
--    AS MATERIALIZED = compute once, store in a temp table, reuse.
--    (NOT MATERIALIZED would inline it -- re-running it for each reference.)
WITH fine AS MATERIALIZED (
    SELECT department, strftime('%Y', purchase_date) AS yr, sum(amount) AS revenue
    FROM purchases
    GROUP BY department, yr
)
SELECT department, yr, round(revenue, 2) AS revenue FROM fine
WHERE department = 'Books'
UNION ALL
SELECT department, 'ALL', round(sum(revenue), 2) FROM fine
WHERE department = 'Books' GROUP BY department
UNION ALL
SELECT 'ALL', 'ALL', round(sum(revenue), 2) FROM fine;

-- 5. Making the one unavoidable pass cheaper: a COVERING index holding exactly
--    the columns the query touches, already in GROUP BY order.
--    Before: SCAN purchases + temp B-tree (or the department index + a table
--    lookup per row). After: SCAN ... USING COVERING INDEX, no temp B-tree.
SELECT department, round(sum(amount), 2) AS revenue
FROM purchases NOT INDEXED            -- force the plain scan for the "before"
GROUP BY department
ORDER BY revenue DESC LIMIT 3;

CREATE INDEX idx_purchases_dept_amount ON purchases(department, amount);

SELECT department, round(sum(amount), 2) AS revenue
FROM purchases
GROUP BY department
ORDER BY revenue DESC LIMIT 3;

--    The price: a bigger file and slower inserts (one more B-tree per write).
.eqp off
.timer off
DROP INDEX idx_purchases_dept_amount;
-- =============================================================================
-- 08_sampling.sql  --  random rows without sorting the whole table
-- =============================================================================
--     sqlite3 perf.db ".read sql/08_sampling.sql"
-- Examples sample CUSTOMERS; the same reasoning applies to any rowid table.
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. The naive way. random() is evaluated for EVERY row, then all rows are
--    sorted by it, then 5 are kept. PLAN: SCAN + USE TEMP B-TREE FOR ORDER BY.
--    Cost grows with the table, on every call. Try it on purchases too.
SELECT customer_id, email FROM customers ORDER BY random() LIMIT 5;

-- 2. Random probe by rowid: pick a random number in [1, max] and SEEK to the
--    first row at or after it. One B-tree descent, regardless of table size.
--    Caveat: if ids have gaps (deleted rows), a row just after a big gap is
--    picked more often -- the sample is not perfectly uniform.
SELECT customer_id, email FROM customers
WHERE customer_id >= (SELECT abs(random()) % (SELECT max(customer_id) FROM customers) + 1)
ORDER BY customer_id
LIMIT 1;

-- 3. Several random rows: generate N random ids (recursive CTE), then look each
--    up by primary key. Missing ids (gaps) just return fewer rows -- ask for a
--    few extra and trim. Duplicates are possible; DISTINCT removes them.
WITH RECURSIVE picks(i, id) AS (
    SELECT 1, abs(random()) % (SELECT max(customer_id) FROM customers) + 1
    UNION ALL
    SELECT i + 1, abs(random()) % (SELECT max(customer_id) FROM customers) + 1
    FROM picks WHERE i < 8
)
SELECT c.customer_id, c.email
FROM customers c
WHERE c.customer_id IN (SELECT DISTINCT id FROM picks)
LIMIT 5;

-- 4. Sampling a FILTERED set (e.g. random Books purchases) is harder: random
--    ids mostly miss the filter. Options: probe repeatedly until you have
--    enough; or keep a precomputed list of eligible ids in a small table;
--    or accept "random-ish" (random offset into an indexed range -- which is
--    OFFSET again, so only cheap when the filtered range is small).
-- =============================================================================
-- 09_anti_joins.sql  --  "rows with NO match": NOT EXISTS, LEFT JOIN, NOT IN
-- =============================================================================
--     sqlite3 perf.db ".read sql/09_anti_joins.sql"
-- An anti-join keeps outer rows that have no partner in another table. The cost
-- is (outer rows) x (cost of proving there's no partner). The whole game is
-- making that proof a cheap index seek.
-- =============================================================================

.eqp on
.timer on
.mode box

-- 1. Products never sold at all. For each of 5,000 products, one seek into
--    idx_purchases_product: "is there at least one entry?" Cheap.
SELECT count(*) AS never_sold
FROM products pr
WHERE NOT EXISTS (SELECT 1 FROM purchases pu WHERE pu.product_id = pr.product_id);

-- 2. The same question, three spellings. SQLite plans the first two alike;
--    NOT IN differs in meaning (see 3).
SELECT count(*) AS never_sold_left_join
FROM products pr
LEFT JOIN purchases pu ON pu.product_id = pr.product_id
WHERE pu.purchase_id IS NULL;

SELECT count(*) AS never_sold_not_in
FROM products
WHERE product_id NOT IN (SELECT product_id FROM purchases);

-- 3. The NOT IN trap: if the subquery returns even ONE NULL, "x NOT IN (...)"
--    is never TRUE (it's NULL), so you silently get zero rows.
--    purchases.product_id is NOT NULL, so it's safe above -- but prefer
--    NOT EXISTS, which has no such trap.
SELECT 3 NOT IN (1, 2)       AS no_null_in_list,     -- 1 (true)
       3 NOT IN (1, 2, NULL) AS null_in_list;        -- NULL, not true

-- 4. A harder anti-join: customers who have NEVER bought anything in 'Books'.
--    The probe seeks idx_purchases_customer, then must read EVERY purchase of
--    that customer from the table to check its department. Cheap for most
--    customers, terrible for the skewed ones (one customer has ~28k purchases).
SELECT count(*) AS never_bought_books
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM purchases pu
    WHERE pu.customer_id = c.customer_id
      AND pu.department  = 'Books'
);

-- 5. Give the probe an index on BOTH columns it tests. Now "does customer X
--    have a Books purchase?" is one seek to (X, 'Books') -- COVERING, no table
--    reads, no matter how many purchases the customer has.
CREATE INDEX idx_purchases_customer_dept ON purchases(customer_id, department);

SELECT count(*) AS never_bought_books
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM purchases pu
    WHERE pu.customer_id = c.customer_id
      AND pu.department  = 'Books'
);

-- 6. Column order matters. The same two columns in the other order,
--    (department, customer_id), also turns the probe into a single seek.
--    But (department) alone, or (customer_id) alone, would not.
--    Rule: equality columns of the probe, in the index, left to right.

-- 7. When the "partner" is several joins away (purchases -> customers ->
--    zipcodes -> states), the probe becomes a join inside NOT EXISTS.
--    States where product 7 has never been bought: 51 outer rows, and each
--    probe starts from product 7's purchases and walks to their states.
--    Read the plan: which table does the probe start from, and does each
--    step SEEK? Then ask what happens if the outer side is 5,000 rows instead.
SELECT s.state_code
FROM states s
WHERE NOT EXISTS (
    SELECT 1
    FROM purchases pu
    JOIN customers c ON c.customer_id = pu.customer_id
    JOIN zipcodes  z ON z.zipcode     = c.zipcode
    WHERE pu.product_id = 7
      AND z.state_code  = s.state_code
);

.eqp off
.timer off
DROP INDEX idx_purchases_customer_dept;
