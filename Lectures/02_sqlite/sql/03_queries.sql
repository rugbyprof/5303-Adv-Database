-- =============================================================================
-- 03_queries.sql  --  Worked query examples against the loaded database
-- =============================================================================
-- These are meant to be run one block at a time in an interactive session:
--
--     cd Lectures/02_sqlite
--     sqlite3 store.db
--     sqlite> .read sql/03_queries.sql        -- runs them all, or
--     sqlite> .mode box
--     sqlite> -- then paste individual queries
--
-- rebuild.sql does NOT run this file; it is for exploration after the build.
-- =============================================================================

.mode box
.headers on
PRAGMA foreign_keys = ON;

-- #############################################################################
-- 1. SELECT *  --  look at whole tables
-- #############################################################################

-- Everything in a small lookup table:
SELECT * FROM departments;

-- Never bare SELECT * on a big table in a shared session -- cap it:
SELECT * FROM customers LIMIT 5;
SELECT * FROM purchases ORDER BY purchase_date DESC LIMIT 5;

-- The re-joined "wide" view built in 01_schema.sql:
SELECT * FROM purchase_details LIMIT 5;

-- Inspecting structure (dot commands, not SQL):
--   .tables            list tables and views
--   .schema purchases  show the CREATE statement
--   .indexes purchases show indexes on a table
-- Same thing as SQL, from the catalog:
SELECT type, name FROM sqlite_master WHERE type IN ('table','view','index') ORDER BY type, name;


-- #############################################################################
-- 2. Filtering, projection, ORDER BY, DISTINCT
-- #############################################################################

-- Just the columns you need, filtered, sorted:
SELECT first_name, last_name, email, zipcode
FROM customers
WHERE zipcode LIKE '9%'
ORDER BY last_name, first_name;

-- DISTINCT list of states we ship to:
SELECT DISTINCT state_code FROM zipcodes ORDER BY state_code;

-- IN / BETWEEN / comparison:
SELECT product_name, unit_price
FROM products
WHERE unit_price BETWEEN 100 AND 150
ORDER BY unit_price DESC;


-- #############################################################################
-- 3. JOINs
-- #############################################################################

-- 3a. Inner join: each purchase with its customer, product, and location.
SELECT
    pu.purchase_id,
    pu.purchase_date,
    c.first_name || ' ' || c.last_name AS customer,
    z.state_code,
    pr.product_name,
    pu.department,
    pu.amount
FROM purchases pu
JOIN customers c  ON c.customer_id = pu.customer_id
JOIN zipcodes  z  ON z.zipcode     = c.zipcode
JOIN products  pr ON pr.product_id = pu.product_id
ORDER BY pu.purchase_date
LIMIT 15;

-- 3b. Multi-table join + GROUP BY: revenue by state.
SELECT
    z.state_code,
    count(*)                       AS num_purchases,
    round(sum(pu.amount), 2)       AS revenue
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY z.state_code
ORDER BY revenue DESC
LIMIT 10;

-- 3c. LEFT JOIN: every department, plus its purchase count. A LEFT JOIN keeps
--     departments with no purchases (count comes back 0, not missing) -- an
--     INNER JOIN would silently drop them. Every department is used in this
--     data; add an unused one to `departments` and re-run to see the 0 row.
SELECT
    d.department,
    count(pu.purchase_id) AS num_purchases
FROM departments d
LEFT JOIN purchases pu ON pu.department = d.department
GROUP BY d.department
ORDER BY num_purchases DESC, d.department;

-- 3d. Self-contained "top N per group" using a window function:
--     the single most expensive product bought in each department.
SELECT department, product_name, amount
FROM (
    SELECT
        pu.department,
        pr.product_name,
        pu.amount,
        row_number() OVER (PARTITION BY pu.department
                           ORDER BY pu.amount DESC, pr.product_name) AS rn
    FROM purchases pu
    JOIN products pr ON pr.product_id = pu.product_id
)
WHERE rn = 1
ORDER BY amount DESC;


-- #############################################################################
-- 4. Subqueries (scalar, IN, correlated, EXISTS)
-- #############################################################################

-- 4a. Scalar subquery in WHERE: purchases above the overall average amount.
SELECT purchase_id, purchase_date, department, amount
FROM purchases
WHERE amount > (SELECT avg(amount) FROM purchases)
ORDER BY amount DESC
LIMIT 10;

-- 4b. Subquery producing a set for IN: customers who bought from 'Electronics'.
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM purchases
    WHERE department = 'Electronics'
)
ORDER BY last_name
LIMIT 10;

-- 4c. Derived table (subquery in FROM): per-customer totals, then filter.
SELECT t.customer_id, c.email, t.spent
FROM (
    SELECT customer_id, sum(amount) AS spent
    FROM purchases
    GROUP BY customer_id
) t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.spent > 200
ORDER BY t.spent DESC;

-- 4d. Correlated subquery: each product with how many times it was purchased.
SELECT
    pr.product_name,
    pr.unit_price,
    (SELECT count(*) FROM purchases pu WHERE pu.product_id = pr.product_id) AS times_sold
FROM products pr
ORDER BY times_sold DESC, pr.product_name
LIMIT 10;

-- 4e. EXISTS / NOT EXISTS: products that have never been purchased.
--     Returns 0 rows in THIS data by construction -- the products table was
--     derived from the purchase rows, so every product has at least one sale.
--     Insert a lone product, re-run, and it shows up.
SELECT pr.product_id, pr.product_name
FROM products pr
WHERE NOT EXISTS (
    SELECT 1 FROM purchases pu WHERE pu.product_id = pr.product_id
)
ORDER BY pr.product_name;


-- #############################################################################
-- 5. Aggregate functions:  count, sum, avg, min, max  (+ GROUP BY / HAVING)
-- #############################################################################

-- 5a. Whole-table aggregates in one row.
SELECT
    count(*)                        AS num_purchases,
    count(DISTINCT customer_id)     AS distinct_customers,
    round(sum(amount), 2)           AS total_revenue,
    round(avg(amount), 2)           AS avg_ticket,
    min(amount)                     AS smallest,
    max(amount)                     AS largest
FROM purchases;

-- 5b. GROUP BY: the same aggregates per department.
SELECT
    department,
    count(*)              AS num_purchases,
    round(sum(amount), 2) AS revenue,
    round(avg(amount), 2) AS avg_ticket
FROM purchases
GROUP BY department
ORDER BY revenue DESC;

-- 5c. HAVING filters groups AFTER aggregation (WHERE filters rows before).
--     Departments whose average ticket is over $100.
SELECT
    department,
    count(*)              AS num_purchases,
    round(avg(amount), 2) AS avg_ticket
FROM purchases
GROUP BY department
HAVING avg(amount) > 100
ORDER BY avg_ticket DESC;

-- 5d. WHERE + GROUP BY + HAVING together: among purchases of $20 or more,
--     card types used more than 40 times.
SELECT
    ct.card_type,
    count(*)              AS num_purchases,
    round(sum(pu.amount), 2) AS revenue
FROM purchases  pu
JOIN cards      cd ON cd.card_id   = pu.card_id
JOIN card_types ct ON ct.card_type = cd.card_type
WHERE pu.amount >= 20
GROUP BY ct.card_type
HAVING count(*) > 40
ORDER BY num_purchases DESC;


-- #############################################################################
-- 6. Date ranges
-- #############################################################################
-- Dates are TEXT in ISO 'YYYY-MM-DD', so plain string comparison is also date
-- comparison, and SQLite's date functions accept them directly.

-- 6a. A closed range with BETWEEN (inclusive on both ends): autumn 2025.
SELECT purchase_id, purchase_date, department, amount
FROM purchases
WHERE purchase_date BETWEEN '2025-09-01' AND '2025-11-30'
ORDER BY purchase_date;

-- 6b. Half-open range (>= start, < next start). Preferred for month/quarter
--     boundaries -- no "last day of month" bugs. December 2025:
SELECT count(*) AS december_2025_purchases, round(sum(amount), 2) AS revenue
FROM purchases
WHERE purchase_date >= '2025-12-01'
  AND purchase_date <  '2026-01-01';

-- 6c. Bucket by month with strftime(): revenue per calendar month.
SELECT
    strftime('%Y-%m', purchase_date) AS month,
    count(*)                         AS num_purchases,
    round(sum(amount), 2)            AS revenue
FROM purchases
GROUP BY month
ORDER BY month;

-- 6d. Relative to a reference date: purchases in the 90 days before the last
--     purchase in the data.
SELECT count(*) AS last_90_days
FROM purchases
WHERE purchase_date > date((SELECT max(purchase_date) FROM purchases), '-90 days');

-- 6e. Day-of-week distribution ('0' = Sunday ... '6' = Saturday).
SELECT
    strftime('%w', purchase_date) AS dow,
    count(*)                      AS num_purchases
FROM purchases
GROUP BY dow
ORDER BY dow;


-- #############################################################################
-- 7. A few more things worth seeing
-- #############################################################################

-- 7a. CASE for bucketing a continuous value.
SELECT
    CASE
        WHEN amount <  10 THEN '  < $10'
        WHEN amount <  50 THEN ' $10-50'
        WHEN amount < 100 THEN '$50-100'
        ELSE               '  $100+'
    END AS price_band,
    count(*) AS num_purchases
FROM purchases
GROUP BY price_band
ORDER BY price_band;

-- 7b. Common Table Expression (WITH) to name a step, then reuse it.
WITH customer_spend AS (
    SELECT customer_id, sum(amount) AS spent
    FROM purchases
    GROUP BY customer_id
)
SELECT
    round(avg(spent), 2) AS avg_customer_spend,
    max(spent)           AS biggest_spender_total
FROM customer_spend;

-- 7c. Read the planner's mind: does the date filter use idx_purchases_date?
EXPLAIN QUERY PLAN
SELECT * FROM purchases WHERE purchase_date >= '2026-01-01';

-- 7d. Referential integrity is live. This INSERT is REJECTED because product_id
--     99999 does not exist (run it to see the error, then move on):
-- INSERT INTO purchases (customer_id, card_id, product_id, department, amount, purchase_date)
-- VALUES (1, 1, 99999, 'Games', 9.99, '2026-01-15');

-- 7e. Integrity check across the whole database:
PRAGMA foreign_key_check;      -- returns no rows when everything is consistent
