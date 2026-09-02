-- =============================================================================
-- rebuild.sql  --  One command to recreate the whole database from the CSV
-- =============================================================================
-- Usage (must be run from the Lectures/02_sqlite/ directory so the relative
-- path to ../example_data.csv inside 02_load.sql resolves):
--
--     cd Lectures/02_sqlite
--     rm -f store.db
--     sqlite3 store.db ".read rebuild.sql"
--
-- or from an interactive prompt:
--
--     sqlite3 store.db
--     sqlite> .read rebuild.sql
--
-- It is safe to re-run: 01_schema.sql drops every object before creating it.
-- =============================================================================

-- Dot commands take the whole line: no trailing "-- comment" after them.
-- .bail on = stop at the first error instead of plowing ahead.
.bail on
.echo off

SELECT '== 1/2  creating schema ==' AS step;
.read sql/01_schema.sql

SELECT '== 2/2  loading + normalizing data ==' AS step;
.read sql/02_load.sql

-- ---- verification -----------------------------------------------------------
SELECT '== verification ==' AS step;

-- Foreign keys were declared with the FK pragma on; confirm nothing dangles.
PRAGMA foreign_key_check;

-- Round-trip check: the fact table must still hold every source row, and its
-- revenue total must match the raw file's.
SELECT
    (SELECT count(*) FROM purchases)                     AS purchase_rows,
    (SELECT round(sum(amount), 2) FROM purchases)        AS total_revenue,
    (SELECT count(DISTINCT customer_id) FROM purchases)  AS customers_with_purchases;

SELECT '== rebuild complete ==' AS step;
