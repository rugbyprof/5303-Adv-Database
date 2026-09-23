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
