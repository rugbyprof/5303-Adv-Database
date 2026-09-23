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
