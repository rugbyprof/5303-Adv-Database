-- Added to the "idx" variant on top of the plain foreign-key indexes that
-- 01_schema.sql already creates. A covering index holds every column a query
-- needs, so SQLite answers from the index alone and never reads the table.
CREATE INDEX IF NOT EXISTS idx_purchases_cust_amount      ON purchases(customer_id, amount);
CREATE INDEX IF NOT EXISTS idx_purchases_prod_amount      ON purchases(product_id, amount);
CREATE INDEX IF NOT EXISTS idx_purchases_date_cust_amount ON purchases(purchase_date, customer_id, amount);
