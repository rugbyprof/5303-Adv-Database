-- Turns a copy of the database into the "noidx" variant: drops every
-- secondary index so only PRIMARY KEY / UNIQUE lookups remain.
DROP INDEX IF EXISTS idx_zipcodes_state;
DROP INDEX IF EXISTS idx_customers_zipcode;
DROP INDEX IF EXISTS idx_cards_customer;
DROP INDEX IF EXISTS idx_purchases_customer;
DROP INDEX IF EXISTS idx_purchases_product;
DROP INDEX IF EXISTS idx_purchases_department;
DROP INDEX IF EXISTS idx_purchases_date;
DROP INDEX IF EXISTS idx_purchases_cust_amount;
DROP INDEX IF EXISTS idx_purchases_prod_amount;
DROP INDEX IF EXISTS idx_purchases_date_cust_amount;
