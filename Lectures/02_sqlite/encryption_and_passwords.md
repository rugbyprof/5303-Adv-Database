# SQLite Security: Encryption, Hashing, and Passwords (with Python)

Supplement to the [SQLite walkthrough](sqlite_walkthrough.md). Where the
walkthrough's [example_data.csv](../example_data.csv) stores raw `cc_number`
values — fine for synthetic teaching data, never in production — this file shows
what you would actually do instead.

All code was run against Python 3.13 with `cryptography` 50.0 and the standard
library. `argon2-cffi`, `bcrypt`, and `sqlcipher3` snippets are marked with the
`pip install` they need.

---

## 1. What SQLite gives you: essentially nothing

| Concern | Built into stock SQLite? |
| :--- | :--- |
| File encryption at rest | **No.** The `.db` file is plaintext. |
| Connection password / user accounts | **No.** File access = full access. |
| Password-hashing SQL functions (bcrypt, argon2, PBKDF2) | **No.** |
| General hash SQL functions (`md5()`, `sha256()`) | **No** in the library. The `sqlite3` **CLI shell** compiles in `sha3()` / `sha3_query()` and `.sha3sum` — checksums, *not* password hashing. |
| Encryption extensions | Hooks exist; implementations are third-party (SEE, SQLCipher, …). |

So every technique below is **application-side**: your Python code does the
crypto and hands SQLite plain bytes to store in a `BLOB` or `TEXT` column.

Third-party at-rest encryption options, for reference:

| Option | License | Crypto |
| :--- | :--- | :--- |
| **SEE** (SQLite Encryption Extension) | Commercial, from the SQLite authors | AES-128/256 |
| **SQLCipher** (Zetetic) | Open source (BSD-style) | AES-256-CBC + HMAC-SHA-512, PBKDF2 |
| **SQLite3 Multiple Ciphers** (utelle) | Open source | Multiple, incl. SQLCipher-compatible, ChaCha20 |
| **SQLeet** | Public domain | ChaCha20-Poly1305 |

`PRAGMA key = '…'` is a SQLCipher/SEE convention, **not** vanilla SQLite.

---

## 2. Storing user passwords: hash, never encrypt

You **hash** passwords (one-way, verify by re-hashing). You do **not** encrypt
them — an encrypted password can be decrypted, which is exactly what you don't
want.

**Rules**

1. Use a slow, salted, memory-hard KDF: **Argon2id** (first choice), **scrypt**,
   or **bcrypt**. Fall back to **PBKDF2-HMAC-SHA-256** only when you cannot add a
   dependency.
2. Never use bare `md5()` / `sha1()` / `sha256()` on a password — they are
   GPU-fast and trivially brute-forced.
3. Store the algorithm and its parameters *with* the hash, so you can raise the
   cost later without locking users out.
4. Compare with a constant-time function (`hmac.compare_digest`), and let the KDF
   library do it when it offers a `verify()`.

### 2a. Argon2id — recommended  `pip install argon2-cffi`

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

# Defaults are sane (Argon2id, 64 MiB, 3 passes). Tune for ~0.25-0.5 s on your
# server hardware.
ph = PasswordHasher(time_cost=3, memory_cost=64 * 1024, parallelism=4)

def hash_password(plaintext: str) -> str:
    # Returns a self-describing string, e.g.
    # "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$aGFzaGJ5dGVz"
    return ph.hash(plaintext)

def verify_password(stored_hash: str, plaintext: str) -> bool:
    try:
        ph.verify(stored_hash, plaintext)
    except (VerifyMismatchError, InvalidHashError):
        return False
    return True

def needs_upgrade(stored_hash: str) -> bool:
    # True when the hash was made with weaker parameters than current defaults.
    return ph.check_needs_rehash(stored_hash)
```

Login flow, with transparent cost upgrades:

```python
import sqlite3

def login(con: sqlite3.Connection, email: str, password: str) -> bool:
    row = con.execute(
        "SELECT id, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    if row is None:
        # Hash anyway so a missing user and a wrong password take the same time.
        ph.hash(password)
        return False

    user_id, stored = row
    if not verify_password(stored, password):
        return False

    if needs_upgrade(stored):
        con.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(password), user_id),
        )
        con.commit()
    return True
```

### 2b. bcrypt  `pip install bcrypt`

```python
import bcrypt

def hash_password(plaintext: str) -> bytes:
    # bcrypt silently ignores bytes past 72; hash first if you must allow longer.
    return bcrypt.hashpw(plaintext.encode("utf-8"), bcrypt.gensalt(rounds=12))

def verify_password(stored_hash: bytes, plaintext: str) -> bool:
    return bcrypt.checkpw(plaintext.encode("utf-8"), stored_hash)
```

Store the `bytes` in a `BLOB` column, or `.decode("ascii")` it into `TEXT`
(bcrypt output is ASCII).

### 2c. Standard library only — scrypt or PBKDF2

No dependency. `hashlib.scrypt` needs an explicit `maxmem` because OpenSSL's
default 32 MiB cap is *exactly* what `n=2**15, r=8` requires.

```python
import base64, hashlib, hmac, os

def hash_password(plaintext: str, *, n=2**15, r=8, p=1) -> str:
    salt = os.urandom(16)
    dk = hashlib.scrypt(
        plaintext.encode("utf-8"),
        salt=salt, n=n, r=r, p=p, dklen=32,
        maxmem=128 * n * r * 2,          # headroom above the 128*n*r requirement
    )
    return "$".join([
        "scrypt", str(n), str(r), str(p),
        base64.b64encode(salt).decode(), base64.b64encode(dk).decode(),
    ])

def verify_password(stored: str, plaintext: str) -> bool:
    scheme, n, r, p, salt_b64, dk_b64 = stored.split("$")
    if scheme != "scrypt":
        raise ValueError(f"unexpected scheme {scheme!r}")
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(dk_b64)
    n, r, p = int(n), int(r), int(p)
    dk = hashlib.scrypt(
        plaintext.encode("utf-8"),
        salt=salt, n=n, r=r, p=p, dklen=len(expected),
        maxmem=128 * n * r * 2,
    )
    return hmac.compare_digest(dk, expected)
```

PBKDF2 variant (use ~600,000 iterations for SHA-256, per current OWASP guidance):

```python
salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac("sha256", plaintext.encode("utf-8"), salt, 600_000, dklen=32)
# store: "pbkdf2_sha256$600000$<b64 salt>$<b64 dk>", verify by re-deriving
```

### 2d. The schema, and what NOT to do

```sql
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,           -- self-describing: algo + params + salt + digest
    created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
```

```python
# DO NOT DO THIS. Fast hash, and here not even salted.
bad = hashlib.sha256(password.encode()).hexdigest()
```

A single GPU tries billions of SHA-256 guesses per second; a leak of that column
is a leak of every weak password within hours.

---

## 3. Encrypting individual column values

For data you must be able to read back but want unreadable in a file/backup
leak: card numbers, SSNs, tokens, notes.

**Cost you are accepting:** an encrypted column cannot be range-queried, sorted,
`LIKE`-searched, or (with proper randomized encryption) equality-matched. If you
need equality lookup, add a **blind index** (§3d).

**Key management** — the whole game:

- The key lives **outside** the database: an environment variable, a file with
  `600` perms, a KMS/Secrets Manager, an HSM. Never in a column, never in the
  repo.
- Commit neither keys nor real encrypted data. The tutorial's
  [.gitignore](../../.gitignore) already excludes `*.db`.
- Plan for rotation: keep a key id alongside each ciphertext.

### 3a. Fernet — the easy, safe default  `pip install cryptography`

Fernet = AES-128-CBC + HMAC-SHA-256, timestamped, URL-safe base64 output.

```python
import os, sqlite3
from cryptography.fernet import Fernet, InvalidToken

# Generate once, then load from the environment on every run:
#   export APP_FERNET_KEY="$(python -c 'from cryptography.fernet import Fernet;
#                                       print(Fernet.generate_key().decode())')"
fernet = Fernet(os.environ["APP_FERNET_KEY"].encode())

def encrypt(value: str) -> bytes:
    return fernet.encrypt(value.encode("utf-8"))          # store as BLOB

def decrypt(token: bytes) -> str:
    try:
        return fernet.decrypt(token).decode("utf-8")
    except InvalidToken:
        raise ValueError("ciphertext failed authentication (wrong key or tampered)")

con = sqlite3.connect("store.db")
con.execute("""
    CREATE TABLE IF NOT EXISTS payment_cards (
        id          INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
        card_ct     BLOB NOT NULL,        -- encrypted PAN
        last4       TEXT NOT NULL         -- kept in clear for display; not sensitive
    )
""")
con.execute(
    "INSERT INTO payment_cards (customer_id, card_ct, last4) VALUES (?, ?, ?)",
    (42, encrypt("6011000990139424"), "9424"),
)
con.commit()

(ct, last4) = con.execute(
    "SELECT card_ct, last4 FROM payment_cards WHERE customer_id = 42"
).fetchone()
print(decrypt(ct), last4)      # -> 6011000990139424 9424
```

### 3b. AES-256-GCM with associated data — more control

Authenticated encryption with a per-row random 96-bit nonce, plus **associated
data (AAD)** that is authenticated but not encrypted. Binding the row's identity
into the AAD stops an attacker with write access from swapping one row's
ciphertext into another row.

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = bytes.fromhex(os.environ["APP_AES_KEY_HEX"])   # 64 hex chars = 32 bytes
aes = AESGCM(key)

def encrypt_field(plaintext: str, *, table: str, column: str, row_id: int):
    nonce = os.urandom(12)
    aad = f"{table}.{column}:{row_id}".encode("utf-8")
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), aad)   # ct includes the 16-byte tag
    return nonce, ct

def decrypt_field(nonce: bytes, ct: bytes, *, table: str, column: str, row_id: int) -> str:
    aad = f"{table}.{column}:{row_id}".encode("utf-8")
    return aes.decrypt(nonce, ct, aad).decode("utf-8")        # raises InvalidTag on any mismatch
```

```sql
CREATE TABLE customer_ssn (
    customer_id INTEGER PRIMARY KEY REFERENCES customers(customer_id),
    ssn_nonce   BLOB NOT NULL,
    ssn_ct      BLOB NOT NULL,
    key_id      TEXT NOT NULL DEFAULT 'k1'   -- so a future rotation can tell rows apart
);
```

Store `ssn_nonce` and `ssn_ct` from `encrypt_field(...)`; pass the row's
`customer_id` as `row_id` on the way back out.

### 3c. Deriving the key from a passphrase

When the key must come from something a human types (e.g. a CLI tool), stretch it
with a KDF and store only the salt.

```python
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def derive_key(passphrase: str, salt: bytes) -> bytes:
    return Scrypt(salt=salt, length=32, n=2**15, r=8, p=1).derive(passphrase.encode("utf-8"))

salt = os.urandom(16)                 # persist this (a config table or a sidecar file)
key = derive_key("correct horse battery staple", salt)
aes = AESGCM(key)
```

### 3d. Searchable equality: the blind index

To support `WHERE email = ?` on an encrypted `email`, store a **keyed hash**
(HMAC) of the normalized value in a second column and query *that*. It reveals
only equality (which values are identical), never the plaintext, and only to
someone who also holds the HMAC key.

```python
import hmac, hashlib, os

BIDX_KEY = bytes.fromhex(os.environ["APP_BIDX_KEY_HEX"])   # separate from the encryption key

def blind_index(value: str) -> bytes:
    normalized = value.strip().lower().encode("utf-8")      # normalize BEFORE hashing
    return hmac.new(BIDX_KEY, normalized, hashlib.sha256).digest()
```

```sql
CREATE TABLE contacts (
    id         INTEGER PRIMARY KEY,
    email_ct   BLOB NOT NULL,           -- Fernet/GCM ciphertext of the address
    email_bidx BLOB NOT NULL            -- HMAC-SHA-256 of lower(trim(address))
);
CREATE INDEX idx_contacts_email_bidx ON contacts(email_bidx);
```

```python
# insert
con.execute(
    "INSERT INTO contacts (email_ct, email_bidx) VALUES (?, ?)",
    (encrypt("Foo@Bar.com"), blind_index("Foo@Bar.com")),
)
# look up  -- input case/whitespace does not matter, normalization handles it
row = con.execute(
    "SELECT id, email_ct FROM contacts WHERE email_bidx = ?",
    (blind_index("  foo@bar.com "),),
).fetchone()
```

Still impossible: `LIKE`, `ORDER BY`, range queries, `>`/`<`. Those need
plaintext or a specialized scheme.

---

## 4. Encrypting the whole database file: SQLCipher from Python

If you want *everything* — every table, index, and the schema itself —
transparently encrypted on disk, use a SQLCipher build instead of app-side
column crypto.

`pip install sqlcipher3-binary`  (bundles SQLCipher; drop-in DB-API module)

```python
import sqlcipher3 as sqlite3        # same API as the stdlib sqlite3

con = sqlite3.connect("secret.db")
con.execute("PRAGMA key = 'a strong passphrase or hex key'")   # MUST be first
# Optional hardening / compatibility knobs:
con.execute("PRAGMA cipher_page_size = 4096")
con.execute("PRAGMA kdf_iter = 256000")

# The key is only checked on first use — force it now so a wrong key fails loudly:
con.execute("SELECT count(*) FROM sqlite_master")

con.execute("CREATE TABLE IF NOT EXISTS secrets(id INTEGER PRIMARY KEY, note TEXT)")
con.execute("INSERT INTO secrets(note) VALUES ('only readable with the key')")
con.commit()
```

Raw-key form (no KDF, exactly 32 bytes as 64 hex chars) — note the required
`x'...'` quoting:

```python
con.execute("PRAGMA key = \"x'"
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
            "'\"")
```

Change the passphrase on an open database:

```python
con.execute("PRAGMA rekey = 'the new passphrase'")
```

Encrypt an existing plaintext database (run in the `sqlcipher` CLI, or via
`ATTACH` from Python):

```sql
ATTACH DATABASE 'encrypted.db' AS enc KEY 'passphrase';
SELECT sqlcipher_export('enc');
DETACH DATABASE enc;
```

**Trade-offs vs. column encryption**

| | Whole-file (SQLCipher) | Per-column (app-side) |
| :--- | :--- | :--- |
| Protects schema + indexes + all columns | yes | no |
| Queries/indexes work normally on protected data | yes (DB decrypts in memory) | no (ciphertext is opaque) |
| Data exposed while the DB is open in a process | yes (in RAM) | only the fields you decrypt |
| Granular keys (per user / per field) | no | yes |
| Extra build dependency | yes | just `cryptography` |

They compose: SQLCipher for the file **and** column encryption for the few
fields that warrant a second, separately-managed key.

Alternatives to `sqlcipher3-binary`: `pysqlcipher3`, or `apsw` built against
"SQLite3 Multiple Ciphers".

---

## 5. Putting it together

One schema with hashed passwords (§2a) and an encrypted, searchable email (§3a +
§3d). Runnable with `argon2-cffi` and `cryptography` installed and the three env
vars set.

```python
import os, sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from cryptography.fernet import Fernet
import hmac, hashlib

ph = PasswordHasher()
fernet = Fernet(os.environ["APP_FERNET_KEY"].encode())
BIDX_KEY = bytes.fromhex(os.environ["APP_BIDX_KEY_HEX"])

def blind_index(value: str) -> bytes:
    return hmac.new(BIDX_KEY, value.strip().lower().encode(), hashlib.sha256).digest()

con = sqlite3.connect("accounts.db")
con.execute("PRAGMA foreign_keys = ON")
con.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY,
        email_ct      BLOB NOT NULL,
        email_bidx    BLOB NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
    );
""")

def register(email: str, password: str) -> int:
    cur = con.execute(
        "INSERT INTO users (email_ct, email_bidx, password_hash) VALUES (?, ?, ?)",
        (fernet.encrypt(email.encode()), blind_index(email), ph.hash(password)),
    )
    con.commit()
    return cur.lastrowid

def authenticate(email: str, password: str) -> int | None:
    row = con.execute(
        "SELECT id, password_hash FROM users WHERE email_bidx = ?", (blind_index(email),)
    ).fetchone()
    if row is None:
        ph.hash(password)                 # equalize timing
        return None
    user_id, stored = row
    try:
        ph.verify(stored, password)
    except (VerifyMismatchError, InvalidHashError):
        return None
    if ph.check_needs_rehash(stored):
        con.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                    (ph.hash(password), user_id))
        con.commit()
    return user_id

uid = register("Ada@example.com", "correct horse battery staple")
assert authenticate("  ada@example.com ", "correct horse battery staple") == uid
assert authenticate("ada@example.com", "wrong") is None
```

---

## 6. Checklist

- [ ] Passwords: Argon2id / scrypt / bcrypt, salted, parameters stored with the
      hash. Never a bare fast hash.
- [ ] Constant-time comparison (`hmac.compare_digest` or the library `verify()`).
- [ ] Same code path and timing for "no such user" and "wrong password".
- [ ] Sensitive columns: authenticated encryption (Fernet or AES-GCM), key from
      env/KMS, `key_id` stored per row.
- [ ] Need to search an encrypted column? Blind index with a *separate* HMAC key;
      accept that only equality works.
- [ ] Whole-file secrecy (schema, indexes): SQLCipher, key checked on open.
- [ ] Keys and `*.db` files are git-ignored. Real card numbers (PANs) are not
      stored at all — see PCI-DSS.
- [ ] A rotation plan exists before the first row is written.

### Further reading

- OWASP Password Storage Cheat Sheet
- OWASP Cryptographic Storage Cheat Sheet
- `cryptography` docs: Fernet, `AESGCM`, `Scrypt`
- SQLCipher documentation (`PRAGMA key`, `rekey`, `cipher_*`)
- SQLite: "Is the database encrypted?" (<https://www.sqlite.org/faq.html>) and
  the SEE product page
