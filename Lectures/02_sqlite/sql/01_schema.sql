-- =============================================================================
-- 01_schema.sql  --  Normalized schema for the example purchase data
-- =============================================================================
-- Run order: this file is step 1. It only CREATEs structure; it loads no data.
--
-- Source data (Lectures/example_data.csv) is one flat table with these columns:
--
--   id, first_name, last_name, email, cc_type, cc_number, purchase_dept,
--   purchase_amount, address, zipcode, state, prod_name, purchase_data
--
-- Every row mixes facts about a customer, a payment card, a product, a location,
-- and a single purchase event. Storing it as-is repeats the same customer,
-- product, and zip/state facts on every row -> update/insert/delete anomalies.
--
-- Functional dependencies we found by inspecting the data
-- (see sql/90_data_quality.sql for the queries that check these):
--
--   zipcode      -> state            (774 zips, 0 conflicts)   => zipcodes table
--   cc_number    -> cc_type          (0 conflicts)             => cards table
--   prod_name    -> purchase_amount  (0 conflicts)             => products.unit_price
--   prod_name    -> purchase_dept    *** 181 products appear in more than one
--                                        department ***        => department belongs
--                                        to the PURCHASE, not the product
--   email        identifies a person (unique in this file)     => customers table
--
-- Resulting tables (parent -> child):
--
--   states        (state_code)
--     zipcodes    (zipcode -> state_code)
--       customers (customer_id, email, zipcode -> zipcode)
--         cards   (card_id -> customer_id, card_type -> card_types)
--   card_types    (card_type)
--   departments   (department)
--   products      (product_id, product_name, unit_price)
--   purchases     (purchase_id -> customer_id, card_id, product_id, department)
-- =============================================================================

-- SQLite does NOT enforce foreign keys unless you ask it to, every connection.
PRAGMA foreign_keys = ON;

-- Drop children before parents so FK checks don't block the drop.
DROP VIEW  IF EXISTS purchase_details;
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS zipcodes;
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS card_types;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS products;

-- -----------------------------------------------------------------------------
-- Lookup tables: small, stable sets of allowed values. A foreign key to one of
-- these does the job a CHECK (col IN (...)) list would do, but the list lives in
-- data you can query and extend without a schema change.
-- -----------------------------------------------------------------------------

CREATE TABLE states (
    -- Natural key: the 2-letter USPS code is already unique and stable.
    state_code  TEXT PRIMARY KEY
                CHECK (length(state_code) = 2 AND state_code = upper(state_code))
);

CREATE TABLE card_types (
    card_type   TEXT PRIMARY KEY
);

CREATE TABLE departments (
    department  TEXT PRIMARY KEY
);

-- -----------------------------------------------------------------------------
-- zipcodes: resolves the transitive dependency zipcode -> state. Without this
-- table, "state" would ride along on every customer row and could disagree with
-- itself (3NF violation).
-- -----------------------------------------------------------------------------

CREATE TABLE zipcodes (
    zipcode     TEXT PRIMARY KEY,
    state_code  TEXT NOT NULL
                REFERENCES states(state_code) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- customers: one row per person. Surrogate integer PK (customer_id); email is a
-- second candidate key kept UNIQUE. address + zipcode are the person's location;
-- city is not in the source, and state comes from zipcodes, not from here.
-- -----------------------------------------------------------------------------

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,          -- surrogate key (see note below)
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE          -- natural/candidate key
                CHECK (email LIKE '%_@_%.__%'),
    address     TEXT NOT NULL,
    zipcode     TEXT NOT NULL
                REFERENCES zipcodes(zipcode) ON UPDATE CASCADE ON DELETE RESTRICT
);
-- Note on INTEGER PRIMARY KEY: in SQLite this column is an alias for the internal
-- rowid. We reuse the source file's "id" as customer_id so the mapping back to
-- the CSV stays obvious during the walkthrough.

-- -----------------------------------------------------------------------------
-- cards: a customer's payment methods. cc_number -> cc_type is a functional
-- dependency, so card_type lives here (with the number), not on every purchase.
-- One customer can have many cards (1:N). card_number is UNIQUE across everyone.
-- -----------------------------------------------------------------------------

CREATE TABLE cards (
    card_id     INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL
                REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE CASCADE,
    card_type   TEXT NOT NULL
                REFERENCES card_types(card_type) ON UPDATE CASCADE ON DELETE RESTRICT,
    card_number TEXT NOT NULL UNIQUE
    -- Real systems never store a raw PAN; this is teaching data only.
);

-- -----------------------------------------------------------------------------
-- products: the catalog. prod_name -> purchase_amount is a functional
-- dependency in this data, so a product has one unit_price. prod_name -> dept is
-- NOT a dependency, so department is deliberately absent here.
-- -----------------------------------------------------------------------------

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL UNIQUE,
    unit_price   NUMERIC NOT NULL CHECK (unit_price >= 0)
);

-- -----------------------------------------------------------------------------
-- purchases: the fact table. One row per purchase event. Every descriptive
-- attribute has been replaced by a foreign key EXCEPT:
--   * department  -- an attribute of the event (where it was bought), kept as an
--                    FK to the departments lookup
--   * amount      -- what was actually charged. It equals products.unit_price in
--                    this dataset, but we still store it: it is a point-in-time
--                    snapshot that must not change if the catalog price later
--                    changes (deliberate, correct duplication).
--   * purchase_date -- stored as TEXT in ISO 'YYYY-MM-DD' form so that string
--                    comparison == chronological comparison. The CSV's
--                    'M/D/YYYY' text is converted during load.
-- -----------------------------------------------------------------------------

CREATE TABLE purchases (
    purchase_id   INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL
                  REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    card_id       INTEGER NOT NULL
                  REFERENCES cards(card_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    product_id    INTEGER NOT NULL
                  REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    department    TEXT NOT NULL
                  REFERENCES departments(department) ON UPDATE CASCADE ON DELETE RESTRICT,
    amount        NUMERIC NOT NULL CHECK (amount >= 0),
    purchase_date TEXT NOT NULL
                  -- cheap ISO-shape guard. In GLOB, '?' is the single-char
                  -- wildcard ('_' would be a literal underscore -- that is a
                  -- LIKE-ism, and a classic bug to hit here).
                  CHECK (purchase_date GLOB '????-??-??')
);

-- -----------------------------------------------------------------------------
-- Indexes. The PKs and UNIQUE columns are already indexed. Add indexes on the
-- foreign-key columns and the date, because the example queries filter/join/
-- group on them. (On a 1,000-row table these change nothing measurable; the
-- point is to show WHERE they would go.)
-- -----------------------------------------------------------------------------

CREATE INDEX idx_zipcodes_state       ON zipcodes(state_code);
CREATE INDEX idx_customers_zipcode    ON customers(zipcode);
CREATE INDEX idx_cards_customer       ON cards(customer_id);
CREATE INDEX idx_purchases_customer   ON purchases(customer_id);
CREATE INDEX idx_purchases_product    ON purchases(product_id);
CREATE INDEX idx_purchases_department ON purchases(department);
CREATE INDEX idx_purchases_date       ON purchases(purchase_date);

-- -----------------------------------------------------------------------------
-- A view that re-joins the pieces back into the "wide" shape people expect to
-- read. Views cost nothing to store; they run their SELECT each time they are
-- queried. Use this in the query examples so they stay short.
-- -----------------------------------------------------------------------------

CREATE VIEW purchase_details AS
SELECT
    pu.purchase_id,
    pu.purchase_date,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.address,
    c.zipcode,
    z.state_code,
    pr.product_name,
    pu.department,
    pu.amount,
    ct.card_type
FROM purchases  pu
JOIN customers  c   ON c.customer_id  = pu.customer_id
JOIN zipcodes   z   ON z.zipcode      = c.zipcode
JOIN products   pr  ON pr.product_id  = pu.product_id
JOIN cards      cd  ON cd.card_id     = pu.card_id
JOIN card_types ct  ON ct.card_type   = cd.card_type;
