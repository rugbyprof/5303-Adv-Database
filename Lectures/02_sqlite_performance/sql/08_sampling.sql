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
