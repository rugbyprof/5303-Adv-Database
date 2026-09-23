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
