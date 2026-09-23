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
