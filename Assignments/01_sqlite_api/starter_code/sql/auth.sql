-- Phase: replace the env-var check in app/auth.py with this table.
-- Apply once against your store.db:  sqlite3 store.db ".read sql/auth.sql"

CREATE TABLE IF NOT EXISTS api_keys (
    key_hash   TEXT PRIMARY KEY,          -- sha256(hex) or an Argon2 encoded hash
    label      TEXT NOT NULL,             -- who/what this key is for
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    revoked_at TEXT                       -- NULL = active
);

-- Example: register a key whose SHA-256 you computed elsewhere, e.g.
--   python -c "import hashlib;print(hashlib.sha256(b'dev-key-123').hexdigest())"
-- INSERT INTO api_keys(key_hash, label) VALUES
--   ('9f86d0818884...', 'dev');

-- Lookup shape your dependency should use:
--   SELECT label FROM api_keys
--   WHERE key_hash = :hash AND revoked_at IS NULL;
