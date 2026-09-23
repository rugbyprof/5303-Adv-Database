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
