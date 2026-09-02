-- =============================================================================
-- 02_load.sql  --  Load the CSV into a staging table, then fan it out into the
--                  normalized tables from 01_schema.sql
-- =============================================================================
-- Run order: step 2. Assumes 01_schema.sql has already run in this database.
--
-- Working directory matters: the .import path below is resolved relative to the
-- directory you launched sqlite3 from. Run everything from Lectures/02_sqlite/
-- so that data/example_data.csv resolves. rebuild.sql does exactly that.
--
-- Strategy: never INSERT straight from a CSV into a constrained schema. Land the
-- raw text in a staging table with no rules, inspect/clean it, THEN transform.
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- Step A: staging table. Every column TEXT, no constraints. It should accept
-- the file no matter how dirty the file is.
-- -----------------------------------------------------------------------------

DROP TABLE IF EXISTS staging_raw;

CREATE TABLE staging_raw (
    id              TEXT,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT,
    cc_type         TEXT,
    cc_number       TEXT,
    purchase_dept   TEXT,
    purchase_amount TEXT,
    address         TEXT,
    zipcode         TEXT,
    state           TEXT,
    prod_name       TEXT,
    purchase_date   TEXT   -- CSV header is 'purchase_data' (a source typo);
                           -- .import maps columns by position, not name, so the
                           -- 13th field lands here. Value is a date, 'M/D/YYYY'.
);

-- Step B: import. --csv sets the delimiter/quoting rules; --skip 1 drops the
-- header row (our staging table already has the column names).
.mode csv
.import --skip 1 data/example_data.csv staging_raw

-- Quick sanity check echoed to the console during a rebuild.
SELECT 'staging_raw rows loaded: ' || count(*) FROM staging_raw;

-- -----------------------------------------------------------------------------
-- Step C: populate lookup / parent tables first, so the children's foreign keys
-- have something to point at. INSERT ... SELECT DISTINCT is the workhorse.
-- -----------------------------------------------------------------------------

INSERT INTO states (state_code)
SELECT DISTINCT state
FROM staging_raw
ORDER BY state;

INSERT INTO card_types (card_type)
SELECT DISTINCT cc_type
FROM staging_raw
ORDER BY cc_type;

INSERT INTO departments (department)
SELECT DISTINCT purchase_dept
FROM staging_raw
ORDER BY purchase_dept;

-- zipcode -> state is a functional dependency in this data, so one row per zip.
-- If it were NOT clean, this INSERT would still succeed (DISTINCT pair) and the
-- PRIMARY KEY on zipcode would then reject the second state for a zip -- which is
-- exactly the error you want to see.
INSERT INTO zipcodes (zipcode, state_code)
SELECT DISTINCT zipcode, state
FROM staging_raw;

-- -----------------------------------------------------------------------------
-- Step D: customers. One row per person. The source "id" becomes customer_id.
-- CAST the text to INTEGER so the column stores a number, not a numeral string.
-- -----------------------------------------------------------------------------

INSERT INTO customers (customer_id, first_name, last_name, email, address, zipcode)
SELECT CAST(id AS INTEGER), first_name, last_name, email, address, zipcode
FROM staging_raw;

-- -----------------------------------------------------------------------------
-- Step E: cards. Every staging row carries exactly one card. card_number is
-- unique in the source, so there is one card per customer here -- but the schema
-- allows many, which is the realistic model.
-- -----------------------------------------------------------------------------

INSERT INTO cards (customer_id, card_type, card_number)
SELECT CAST(s.id AS INTEGER), s.cc_type, s.cc_number
FROM staging_raw s;

-- -----------------------------------------------------------------------------
-- Step F: products. Collapse the repeated product rows to one per name. Because
-- prod_name -> purchase_amount is a clean dependency, MIN == MAX == the price;
-- MAX() is just a way to pick the single value inside a GROUP BY.
-- -----------------------------------------------------------------------------

INSERT INTO products (product_name, unit_price)
SELECT prod_name, MAX(CAST(purchase_amount AS NUMERIC))
FROM staging_raw
GROUP BY prod_name
ORDER BY prod_name;

-- -----------------------------------------------------------------------------
-- Step G: purchases -- the fact table. Join staging back to the parents on their
-- natural keys (email, card_number, product_name) to look up the surrogate ids.
--
-- The date arrives as 'M/D/YYYY' text (e.g. '3/9/2026'). The CTE splits it on
-- the two slashes; printf() zero-pads the parts into ISO 'YYYY-MM-DD'.
-- -----------------------------------------------------------------------------

INSERT INTO purchases
    (purchase_id, customer_id, card_id, product_id, department, amount, purchase_date)
WITH after_month AS (
    -- split off the month: 'M/D/YYYY' -> mm='M', tail='D/YYYY'
    SELECT
        s.*,
        substr(s.purchase_date, 1, instr(s.purchase_date, '/') - 1) AS mm,
        substr(s.purchase_date,    instr(s.purchase_date, '/') + 1) AS tail
    FROM staging_raw s
),
parsed AS (
    -- split the tail: 'D/YYYY' -> dd='D', yyyy='YYYY'
    SELECT
        a.*,
        substr(a.tail, 1, instr(a.tail, '/') - 1) AS dd,
        substr(a.tail,    instr(a.tail, '/') + 1) AS yyyy
    FROM after_month a
)
SELECT
    CAST(p.id AS INTEGER),
    c.customer_id,
    cd.card_id,
    pr.product_id,
    p.purchase_dept,
    CAST(p.purchase_amount AS NUMERIC),
    printf('%04d-%02d-%02d',
           CAST(p.yyyy AS INTEGER),
           CAST(p.mm   AS INTEGER),
           CAST(p.dd   AS INTEGER))
FROM parsed    p
JOIN customers c  ON c.email        = p.email
JOIN cards     cd ON cd.card_number = p.cc_number
JOIN products  pr ON pr.product_name = p.prod_name;

-- -----------------------------------------------------------------------------
-- Step H: drop staging. Keep it while learning if you want to compare; a real
-- pipeline discards it so nobody queries the un-normalized copy by accident.
-- -----------------------------------------------------------------------------

DROP TABLE staging_raw;

-- Row counts after load, for the rebuild console output.
SELECT 'states'      AS table_name, count(*) AS rows FROM states
UNION ALL SELECT 'zipcodes',    count(*) FROM zipcodes
UNION ALL SELECT 'card_types',  count(*) FROM card_types
UNION ALL SELECT 'departments', count(*) FROM departments
UNION ALL SELECT 'customers',   count(*) FROM customers
UNION ALL SELECT 'cards',       count(*) FROM cards
UNION ALL SELECT 'products',    count(*) FROM products
UNION ALL SELECT 'purchases',   count(*) FROM purchases;
