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
