-- =============================================================================
-- 03_search_fts5.sql  --  LIKE vs indexes, and full-text search with FTS5
-- =============================================================================
--     sqlite3 perf.db ".read sql/03_search_fts5.sql"
-- Examples search CUSTOMERS (50k rows). Creates two indexes and two FTS tables,
-- then drops them at the end so the script is re-runnable.
-- =============================================================================

.eqp on
.timer on
.mode box

-- ---------------------------------------------------------------------------
-- Part 1: when can LIKE use an index?
-- ---------------------------------------------------------------------------

-- 1a. Leading wildcard: no index can help -- a B-tree is sorted by the START
--     of the string. SQLite scans the smallest thing holding the column (here
--     the UNIQUE index on email) and tests every entry.
SELECT count(*) FROM customers WHERE email LIKE '%hopper%';

-- 1b. Prefix pattern -- surely THIS uses the email index? No:
--     LIKE is case-INsensitive in SQLite, but the index is sorted
--     case-sensitively (BINARY collation), so a range seek could miss 'Grace…'.
SELECT count(*) FROM customers WHERE email LIKE 'grace%';

-- 1c. Give LIKE an index whose collation matches it: NOCASE.
--     Now a prefix pattern becomes a range SEARCH (last_name>? AND last_name<?).
CREATE INDEX idx_customers_last_nocase ON customers(last_name COLLATE NOCASE);
SELECT count(*) FROM customers WHERE last_name LIKE 'Hop%';

--     ...but a leading wildcard still can't seek -- it just scans the smaller index.
SELECT count(*) FROM customers WHERE last_name LIKE '%per';

-- ---------------------------------------------------------------------------
-- Part 2: FTS5 -- an inverted index (token -> list of rowids)
-- ---------------------------------------------------------------------------

-- 2a. External-content FTS table: the index lives in customers_fts, the text
--     stays in customers (no second copy). content_rowid ties them together.
CREATE VIRTUAL TABLE customers_fts USING fts5(
    first_name, last_name, email,
    content = 'customers', content_rowid = 'customer_id'
);
-- Build the index from the existing rows (one-time cost).
INSERT INTO customers_fts(customers_fts) VALUES ('rebuild');

-- 2b. MATCH finds rows by TOKEN. The default tokenizer (unicode61) splits on
--     punctuation, so 'grace.hopper.45@example.com' becomes grace|hopper|45|example|com.
--     PLAN: SCAN customers_fts VIRTUAL TABLE INDEX 0:M… -- for a virtual table
--     "SCAN" just means "asked the FTS module"; the M means a MATCH lookup.
SELECT count(*) FROM customers_fts WHERE customers_fts MATCH 'hopper';

-- 2c. Boolean operators, prefix queries (hop*), column filters, and ranking.
--     Join back to the real table by rowid for the columns you want.
SELECT c.customer_id, c.first_name, c.last_name, c.email
FROM customers_fts f
JOIN customers c ON c.customer_id = f.rowid
WHERE customers_fts MATCH 'grace AND hop*'
ORDER BY f.rank                     -- bm25 relevance; lower = better
LIMIT 5;

SELECT rowid, highlight(customers_fts, 2, '[', ']') AS email
FROM customers_fts
WHERE customers_fts MATCH 'email:lovelace'
LIMIT 3;

-- 2d. Tokens are WHOLE words. 'ove' is not a token, so MATCH finds nothing,
--     while LIKE '%ove%' finds every "lovelace". FTS is not a substring index.
SELECT count(*) AS fts_hits  FROM customers_fts WHERE customers_fts MATCH 'ove';
SELECT count(*) AS like_hits FROM customers     WHERE email LIKE '%ove%';

-- 2e. Want substring search indexed? The trigram tokenizer indexes every
--     3-character slice, and then LIKE '%…%' itself can use the FTS index
--     (plan shows INDEX 0:L…). Bigger index; patterns shorter than 3 characters
--     fall back to scanning.
CREATE VIRTUAL TABLE customers_tri USING fts5(
    email, content = 'customers', content_rowid = 'customer_id', tokenize = 'trigram'
);
INSERT INTO customers_tri(customers_tri) VALUES ('rebuild');
SELECT count(*) FROM customers_tri WHERE email LIKE '%ove%';

-- ---------------------------------------------------------------------------
-- Part 3: keeping an external-content index in sync
-- ---------------------------------------------------------------------------
-- The FTS table does NOT watch customers by itself. Without these triggers,
-- new/changed customers are invisible to MATCH (and deletes leave ghosts).
CREATE TRIGGER customers_fts_ai AFTER INSERT ON customers BEGIN
    INSERT INTO customers_fts(rowid, first_name, last_name, email)
    VALUES (new.customer_id, new.first_name, new.last_name, new.email);
END;
CREATE TRIGGER customers_fts_ad AFTER DELETE ON customers BEGIN
    INSERT INTO customers_fts(customers_fts, rowid, first_name, last_name, email)
    VALUES ('delete', old.customer_id, old.first_name, old.last_name, old.email);
END;
CREATE TRIGGER customers_fts_au AFTER UPDATE ON customers BEGIN
    INSERT INTO customers_fts(customers_fts, rowid, first_name, last_name, email)
    VALUES ('delete', old.customer_id, old.first_name, old.last_name, old.email);
    INSERT INTO customers_fts(rowid, first_name, last_name, email)
    VALUES (new.customer_id, new.first_name, new.last_name, new.email);
END;

-- ---------------------------------------------------------------------------
-- Clean up so the script can be re-run.
-- ---------------------------------------------------------------------------
.eqp off
.timer off
DROP TRIGGER customers_fts_ai;
DROP TRIGGER customers_fts_ad;
DROP TRIGGER customers_fts_au;
DROP TABLE customers_fts;
DROP TABLE customers_tri;
DROP INDEX idx_customers_last_nocase;
