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
