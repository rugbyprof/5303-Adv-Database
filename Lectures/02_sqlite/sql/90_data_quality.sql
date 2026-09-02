-- =============================================================================
-- 90_data_quality.sql  --  The checks that justify the schema in 01_schema.sql
-- =============================================================================
-- Run these against a STAGING copy of the raw data BEFORE you design the schema.
-- Each query answers "is this a real functional dependency, or wishful thinking?"
--
-- To use them, load the CSV into staging_raw only (steps A + B of 02_load.sql)
-- and stop before the transforms:
--
--     cd Lectures/02_sqlite
--     sqlite3 explore.db
--     sqlite> CREATE TABLE staging_raw ( ... );      -- from 02_load.sql step A
--     sqlite> .mode csv
--     sqlite> .import --skip 1 data/example_data.csv staging_raw
--     sqlite> .read sql/90_data_quality.sql
-- =============================================================================

.mode box
.headers on

-- 1. Is every source id unique? (Can it be a primary key?)
SELECT count(*) AS rows, count(DISTINCT id) AS distinct_ids FROM staging_raw;

-- 2. Is email one-per-person? Any email attached to more than one name?
SELECT email, count(*) AS rows, count(DISTINCT first_name || '|' || last_name) AS names
FROM staging_raw
GROUP BY email
HAVING names > 1;
-- (no rows) => email identifies a person => customers keyed by email is safe

-- 3. zipcode -> state : does any zipcode map to more than one state?
SELECT zipcode, count(DISTINCT state) AS distinct_states
FROM staging_raw
GROUP BY zipcode
HAVING distinct_states > 1;
-- (no rows) => clean dependency => a zipcodes(zipcode PK, state) table is valid

-- 4. cc_number -> cc_type : does any card number carry two different types?
SELECT cc_number, count(DISTINCT cc_type) AS distinct_types
FROM staging_raw
GROUP BY cc_number
HAVING distinct_types > 1;
-- (no rows) => card_type belongs on the card, not on every purchase

-- 5. cc_number shared by more than one person?
SELECT cc_number, count(DISTINCT email) AS people
FROM staging_raw
GROUP BY cc_number
HAVING people > 1;
-- (no rows) => each card belongs to exactly one customer (1:N customer->cards)

-- 6. prod_name -> purchase_amount : does any product appear at two prices?
SELECT prod_name, count(DISTINCT purchase_amount) AS distinct_prices
FROM staging_raw
GROUP BY prod_name
HAVING distinct_prices > 1;
-- (no rows) => a product has ONE unit_price => products.unit_price is valid

-- 7. prod_name -> purchase_dept : does a product appear in multiple departments?
SELECT count(*) AS products_in_multiple_departments FROM (
    SELECT prod_name
    FROM staging_raw
    GROUP BY prod_name
    HAVING count(DISTINCT purchase_dept) > 1
);
-- (181!) => department is NOT a function of the product.
--           It is an attribute of the PURCHASE. That is why 01_schema.sql puts
--           `department` on `purchases` and not on `products`.

-- 8. What do the date strings actually look like? (format assumptions)
SELECT purchase_data, count(*) AS n
FROM staging_raw
WHERE purchase_data NOT GLOB '*/*/????'      -- anything not M.../D.../YYYY
GROUP BY purchase_data;
-- (no rows) => every value is 'M/D/YYYY'; the split-on-slash parse is safe

-- 9. Any NULLs / blanks in columns we intend to make NOT NULL?
SELECT
    sum(id              IS NULL OR id              = '') AS bad_id,
    sum(email           IS NULL OR email           = '') AS bad_email,
    sum(zipcode         IS NULL OR zipcode         = '') AS bad_zipcode,
    sum(state           IS NULL OR state           = '') AS bad_state,
    sum(cc_number       IS NULL OR cc_number       = '') AS bad_cc_number,
    sum(prod_name       IS NULL OR prod_name       = '') AS bad_prod_name,
    sum(purchase_amount IS NULL OR purchase_amount = '') AS bad_amount,
    sum(purchase_dept   IS NULL OR purchase_dept   = '') AS bad_dept,
    sum(purchase_data   IS NULL OR purchase_data   = '') AS bad_date
FROM staging_raw;
-- (all zero) => the NOT NULL constraints in 01_schema.sql will not reject anything
