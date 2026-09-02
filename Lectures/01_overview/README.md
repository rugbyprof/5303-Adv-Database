# Data Modeling Glossary

A reference for the _Database Models and Data Modeling_ theme. Terms are grouped
by topic. Each entry gives a short definition followed by a concrete example.
Where a relational term has a document-model counterpart (or vice versa), the
entry says so.

---

## 1. Relations, Tables, Documents, Collections, Keys, and Values

### Relation

The formal (relational-algebra) term for a set of tuples that all share the same
attributes. A relation has no duplicate tuples and no inherent row order. In
practice "relation" and "table" are used interchangeably, though a table is the
concrete SQL object and may permit duplicate rows unless a key forbids them.

- **Example:** the mathematical set
  `{ (1, 'Ada'), (2, 'Grace'), (3, 'Linus') }` over attributes `(id, name)` is a
  relation of three tuples.

### Table

The relational storage structure: named columns with declared types, holding zero
or more rows. The unit of definition in SQL DDL.

- **Example:**
  ```sql
  CREATE TABLE author (
      id    INTEGER PRIMARY KEY,
      name  TEXT NOT NULL,
      born  DATE
  );
  ```

### Row (Tuple / Record)

A single entry in a table: one value for each column. Corresponds to a tuple in a
relation.

- **Example:** `(3, 'Linus', 1969-12-28)` is one row of `author`.

### Column (Attribute / Field)

A named, typed component that every row supplies a value for. "Attribute" is the
relational-theory term; "field" is common in document contexts.

- **Example:** `born DATE` is a column of `author`; every row has a `born` value
  (possibly `NULL`).

### Document

A self-contained record in a document database, typically stored as JSON/BSON. It
can hold scalars, arrays, and nested sub-objects, so one document may represent
what a relational design spreads across several tables. Documents in the same
collection need not have identical fields.

- **Example (MongoDB):**
  ```json
  {
    "_id": "a3",
    "name": "Linus",
    "born": "1969-12-28",
    "books": [{ "title": "Just for Fun", "year": 2001 }]
  }
  ```

### Collection

The document-model container that holds documents. Roughly the counterpart of a
table, but without an enforced column set by default. Indexes and (optional)
validation rules are defined per collection.

- **Example:** the `authors` collection contains one document per author; some
  documents have a `website` field and others do not.

### Key

A value (or combination of values) used to identify or locate data.

- In the **relational** model: an attribute set that uniquely identifies rows
  (see _candidate key_, _primary key_ in §2).
- In the **key-value** model: the opaque lookup string a client presents to get
  or set a value. The store does not interpret its structure.

- **Relational example:** `author.id` is the key that identifies an author row.
- **Key-value example:** `SET session:9f83a1 "{...}"` in Redis; `session:9f83a1`
  is the key, and the store only knows how to hash and match it.

### Value

The data associated with a key.

- In **key-value** stores the value is often opaque bytes (a blob, a serialized
  object) that the database does not query into.
- In the **relational** model, a "value" is the single datum sitting in one row
  and one column (a _cell_).

- **Key-value example:** the JSON string stored under `session:9f83a1`.
- **Relational example:** the value `'Linus'` in `author.name` for row `id = 3`.

### Scalar vs. Complex Value

A **scalar** value is atomic (a number, string, boolean, timestamp). A **complex**
value has internal structure (an array or an embedded object). Classic relational
design favors scalars per column (first normal form); document and JSONB columns
allow complex values.

- **Example:** `born = '1969-12-28'` is scalar; `books = [ {...}, {...} ]` is
  complex.

---

## 2. Keys, Relationships, Constraints, and Referential Integrity

### Candidate Key

A minimal set of columns whose values are unique across all rows. A table can
have several. "Minimal" means no column can be dropped and still stay unique.

- **Example:** in `user(id, email, username)`, both `email` and `username` may be
  candidate keys, in addition to `id`.

### Primary Key

The candidate key chosen as the row's canonical identifier. Implies `UNIQUE` and
`NOT NULL`. Other tables reference this key.

- **Example:** `id INTEGER PRIMARY KEY` in `author`.

### Natural Key vs. Surrogate Key

A **natural key** comes from real-world data (an ISBN, an email, a country code).
A **surrogate key** is a system-generated value with no business meaning (an
auto-increment integer, a UUID). Surrogates stay stable when business data
changes.

- **Natural:** `isbn` identifies a `book`.
- **Surrogate:** `book_id SERIAL` identifies the same book; the ISBN is kept as a
  `UNIQUE` column but is not the reference target.

### Composite Key

A key made of two or more columns together. Common in join tables.

- **Example:** `book_author(book_id, author_id)` with
  `PRIMARY KEY (book_id, author_id)` — neither column is unique alone.

### Foreign Key

A column (or set) in one table whose values must match an existing key value in
another (or the same) table. Encodes a relationship and is enforced by the
database.

- **Example:**
  ```sql
  CREATE TABLE book (
      id         INTEGER PRIMARY KEY,
      title      TEXT NOT NULL,
      author_id  INTEGER REFERENCES author(id)
  );
  ```

### Relationship (and Cardinality)

An association between entities, described by how many of each side may relate.

- **One-to-one (1:1):** a `user` has one `user_profile`. Model with a shared
  primary key or a `UNIQUE` foreign key.
- **One-to-many (1:N):** an `author` has many `book` rows; each `book` has one
  `author`. Put the foreign key on the "many" side (`book.author_id`).
- **Many-to-many (M:N):** a `book` has many authors and an `author` has many
  books. Model with a **junction/join table** `book_author(book_id, author_id)`.

### Constraint

A rule the database enforces on every write, rejecting data that violates it.

| Constraint    | Meaning                                  | Example                                |
| :------------ | :--------------------------------------- | :------------------------------------- |
| `NOT NULL`    | value required                           | `name TEXT NOT NULL`                   |
| `UNIQUE`      | no two rows share the value              | `email TEXT UNIQUE`                    |
| `PRIMARY KEY` | unique + not null, the identifier        | `id INTEGER PRIMARY KEY`               |
| `FOREIGN KEY` | must match a key in the referenced table | `author_id REFERENCES author(id)`      |
| `CHECK`       | arbitrary boolean test                   | `CHECK (price >= 0)`                   |
| `DEFAULT`     | value used when none supplied            | `created_at TIMESTAMPTZ DEFAULT now()` |

### Referential Integrity

The guarantee that every foreign key value points to a row that actually exists —
no "orphans." The database maintains it by rejecting or cascading changes.

- **Rejected write:** `INSERT INTO book (id, title, author_id) VALUES (10, 'X',
999);` fails if `author` has no row with `id = 999`.
- **Referential actions** control what happens when the referenced row changes:
  ```sql
  author_id INTEGER REFERENCES author(id)
      ON DELETE CASCADE      -- delete the books when the author is deleted
      ON UPDATE RESTRICT     -- forbid changing an author id that books point to
  ```
  Other options: `ON DELETE SET NULL`, `ON DELETE SET DEFAULT`, `NO ACTION`.

### Referential Integrity in Document / Key-Value Stores

Most document and key-value databases do **not** enforce cross-document
references. If a document stores `"author_id": "a3"` and the `authors` document
`a3` is deleted, the reference dangles. The application (or a background job) is
responsible for consistency. This is a deliberate tradeoff for write speed and
horizontal scaling.

- **Example:** deleting author `a3` in MongoDB leaves `books` documents with
  `"author_id": "a3"` still present and now dangling.

---

## 3. Normalization and Deliberate Denormalization

### Functional Dependency

`X → Y` means the value of `X` determines the value of `Y`. Normalization is
largely about removing dependencies on non-key columns.

- **Example:** `zip → city, state`. If a table stores `zip`, `city`, and `state`
  per customer, `city`/`state` depend on `zip`, not on the customer key.

### Normalization

Organizing columns and tables so that each fact is stored exactly once, reducing
update/insert/delete anomalies. Achieved by splitting tables along their
functional dependencies.

### First Normal Form (1NF)

Every column holds a single atomic value; no repeating groups or arrays.

- **Violation:** `book(id, title, authors)` where `authors = 'Ada; Grace'`.
- **Fix:** move authors into their own rows via a join table.

### Second Normal Form (2NF)

Already 1NF, and every non-key column depends on the **whole** composite key, not
just part of it.

- **Violation:** `book_author(book_id, author_id, author_name)` — `author_name`
  depends on `author_id` alone.
- **Fix:** keep `author_name` in an `author` table keyed by `author_id`.

### Third Normal Form (3NF)

Already 2NF, and no non-key column depends on another non-key column (no
transitive dependencies).

- **Violation:** `customer(id, zip, city, state)` — `city`/`state` depend on
  `zip`.
- **Fix:** `customer(id, zip)` plus `zip_code(zip, city, state)`.

### BCNF, 4NF, 5NF (briefly)

Stricter forms. **BCNF** tightens 3NF so that every determinant is a candidate
key. **4NF** removes independent multi-valued facts stored together. **5NF**
addresses join dependencies. Most application schemas target 3NF/BCNF and stop
there.

### Anomalies (what normalization prevents)

- **Update anomaly:** a fact stored in many rows; changing it means updating all
  copies, and missing one corrupts the data. _(e.g., an author renames and only
  some `book` rows get the new `author_name`.)_
- **Insertion anomaly:** you cannot record one fact without inventing another
  _(e.g., cannot add a new author until they have a book, because the only place
  author data lives is the `book` table)._
- **Deletion anomaly:** deleting one fact destroys an unrelated one _(e.g.,
  deleting the last book by an author also erases that the author existed)._

### Denormalization

Deliberately storing redundant or pre-joined data to make reads faster or
simpler, accepting the cost of keeping the copies in sync. A performance
decision, not a modeling mistake — it is "deliberate" precisely because you know
which normal form you are breaking and why.

- **Relational example:** add `book.author_name` alongside `book.author_id` so
  listing books needs no join. A trigger or application code must update
  `author_name` whenever `author.name` changes.
- **Aggregate example:** store `author.book_count` instead of running
  `COUNT(*)` on `book` for every profile view.
- **Document example:** embed the author's name and photo URL inside each `book`
  document so rendering a book page is a single read.

### When to Denormalize

- Read-heavy workload where the same join runs constantly.
- The duplicated data changes rarely (names, categories, labels).
- The join or aggregate is measurably a bottleneck.
- You have a reliable way to propagate updates (triggers, CDC, batch jobs,
  application transactions).

---

## 4. Embedded Documents versus References

### Embedded Document (Embedding)

Nesting related data directly inside its parent document. The related data is
stored, read, and written as part of one document.

- **Example (MongoDB):** an order with its line items embedded:
  ```json
  {
    "_id": "o-1001",
    "customer": "c-42",
    "placed_at": "2026-09-02T14:03:00Z",
    "items": [
      { "sku": "BK-01", "qty": 1, "price": 39.0 },
      { "sku": "PN-07", "qty": 3, "price": 2.5 }
    ],
    "total": 46.5
  }
  ```
- **Good when:** the child data is owned by exactly one parent, is loaded
  together with it, and does not grow without bound. "Contains" relationships.
- **Costs:** duplicated data if the same sub-object belongs to many parents; the
  document can hit the size limit (16 MB in MongoDB); updating a fact embedded in
  many documents touches all of them.

### Reference (Referencing / Linking)

Storing an identifier that points to a separate document, then resolving it with
a second query (or a `$lookup` / application-side join).

- **Example (MongoDB):**

  ```json
  // books collection
  { "_id": "bk-9", "title": "SICP", "author_id": "a-3" }

  // authors collection
  { "_id": "a-3", "name": "Gerald Jay Sussman" }
  ```

  Resolve with a second read on `authors`, or:

  ```js
  db.books.aggregate([
    { $match: { _id: "bk-9" } },
    {
      $lookup: {
        from: "authors",
        localField: "author_id",
        foreignField: "_id",
        as: "author",
      },
    },
  ]);
  ```

- **Good when:** the referenced entity is shared by many parents, is large, is
  queried on its own, or changes often.
- **Costs:** extra round trips or joins; no enforced referential integrity in
  most document stores.

### Rules of Thumb

| Question                                       | Lean embed | Lean reference |
| :--------------------------------------------- | :--------- | :------------- |
| Is the child owned by one parent?              | yes        | no, shared     |
| Do you always load them together?              | yes        | no             |
| Does the child change independently and often? | no         | yes            |
| Is the set bounded and small?                  | yes        | no, unbounded  |
| Is the child queried on its own?               | no         | yes            |

### Hybrid (Extended Reference)

Reference by id **and** copy the one or two fields you display most, to avoid the
join on the common path. A form of deliberate denormalization (§3).

- **Example:** `{ "author_id": "a-3", "author_name": "Sussman" }` inside each
  book document; full author data still lives in `authors`.

---

## 5. Schema Enforcement and Schema Flexibility

### Schema

The declared structure of the data: which fields exist, their types, which are
required, and how they relate.

### Schema-on-Write (Schema Enforcement)

The database validates data against the schema at write time and rejects
anything that does not conform. Typical of relational systems.

- **Example:** with `born DATE NOT NULL`, `INSERT ... (born) VALUES ('yesterday')`
  is rejected; the shape of every row is guaranteed on read.
- **Benefits:** strong guarantees, simpler application code, the schema is
  documentation, bad data cannot enter.
- **Costs:** every structural change is a migration; harder to store genuinely
  heterogeneous data.

### Schema-on-Read (Schema Flexibility)

The store accepts documents of varying shape; the application interprets
structure when it reads. Typical of document and key-value systems by default.

- **Example:** the `products` collection has clothing documents with `size` and
  book documents with `page_count`; nothing at write time objects.
- **Benefits:** fast iteration, easy to add fields, natural fit for sparse or
  evolving data and per-tenant variation.
- **Costs:** the application must tolerate missing/old-shaped fields; data-quality
  problems surface later and further from the cause; "schema" now lives implicitly
  in code.

### Optional / Partial Schema Validation

Middle ground: define validation rules but scope them.

- **MongoDB `$jsonSchema` validator:**
  ```js
  db.createCollection("authors", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["name"],
        properties: {
          name: { bsonType: "string" },
          born: { bsonType: ["string", "null"] },
        },
      },
    },
    validationLevel: "moderate", // only validate inserts + updates to valid docs
    validationAction: "warn", // log instead of reject
  });
  ```
- **PostgreSQL `JSONB` column:** the row is schema-enforced, but the `JSONB`
  payload inside it is flexible:
  ```sql
  CREATE TABLE event (
      id      BIGINT PRIMARY KEY,
      kind    TEXT NOT NULL,
      payload JSONB NOT NULL,
      CHECK (payload ? 'source')     -- require one key, ignore the rest
  );
  ```

### Schema Evolution / Migration

Changing the schema over time.

- **Relational:** explicit DDL migrations (`ALTER TABLE ADD COLUMN ...`), often
  with a backfill and a tool (Flyway, Alembic, Rails migrations).
- **Document:** frequently "lazy" — write new documents in the new shape, add a
  `schema_version` field, and upgrade old documents when they are next read or in
  a background sweep.

- **Versioned-document example:**
  ```json
  {
    "_id": "a-3",
    "schema_version": 2,
    "name": "Sussman",
    "name_given": "Gerald Jay",
    "name_family": "Sussman"
  }
  ```

---

## 6. Data Duplication and Consistency

### Data Duplication (Redundancy)

The same fact stored in more than one place: denormalized columns, embedded
copies, cached aggregates, read-model projections, or replicas. Sometimes
accidental, often deliberate (§3, §4).

- **Example:** `author.name` copied into every `book` document; the customer's
  address copied onto each historical `order` (here duplication is _correct_ —
  the order must keep the address as it was at purchase time).

### Consistency (two distinct meanings)

1. **Integrity consistency:** the data satisfies all its rules and copies agree
   with each other (no contradictions between `book.author_name` and
   `author.name`). This is the sense that matters for data modeling.
2. **Distributed consistency:** how up-to-date a read is relative to the latest
   write across replicas (the "C" in CAP; strong vs. eventual). Covered under the
   _Transactions, Concurrency, and Consistency_ theme.

### The Duplication / Consistency Tradeoff

Every copy you add makes some read faster or simpler and creates a new way for
the data to disagree with itself. The question is not "duplicate or not" but
"how will every copy be kept in agreement, and what happens in the window while
they disagree?"

### Keeping Copies Consistent

| Mechanism                  | How it works                                     | Example                                                    |
| :------------------------- | :----------------------------------------------- | :--------------------------------------------------------- |
| Transaction                | update all copies atomically in one unit         | update `author` and all `book` rows in one SQL transaction |
| Trigger / stored procedure | database propagates the change on write          | `AFTER UPDATE ON author` refreshes `book.author_name`      |
| Application logic          | app code writes every copy                       | service updates the `authors` doc, then all `books` docs   |
| Materialized view          | database maintains a derived table               | `CREATE MATERIALIZED VIEW book_counts ...; REFRESH ...`    |
| Change data capture (CDC)  | stream the write log to update downstream copies | Debezium feeds a search index                              |
| Background reconciliation  | periodic job re-syncs copies                     | nightly job fixes drifted `author_name` values             |

### Source of Truth

The one authoritative location for a fact. Every other copy is derived and must
be reproducible from it. Naming the source of truth explicitly is what keeps
duplication manageable.

- **Example:** the `authors` collection is the source of truth for an author's
  name; `book.author_name` is a derived copy that a rebuild job can regenerate.

### Eventual Consistency (in the duplication sense)

Copies are allowed to disagree briefly and are expected to converge once
propagation finishes.

- **Example:** an author is renamed at 12:00:00; the search index reflects it at
  12:00:03. For three seconds, searches show the old name. Acceptable for a
  catalog; not acceptable for an account balance.

### Immutable Copy (Point-in-Time Snapshot)

Duplication that is intentional and never resynced, because the copy must record
history.

- **Example:** `order_line.unit_price` is copied from `product.price` at checkout
  and must **not** change when the product is later repriced. This looks like a
  denormalization violation but is a correct model of the business fact.

---

## Quick Cross-Model Term Map

| Relational         | Document                       | Key-Value                       |
| :----------------- | :----------------------------- | :------------------------------ |
| database           | database                       | namespace / logical db          |
| table              | collection                     | keyspace (by prefix convention) |
| row / tuple        | document                       | one value                       |
| column / attribute | field                          | (n/a — value is opaque)         |
| primary key        | `_id`                          | the key                         |
| foreign key        | reference field (not enforced) | (n/a)                           |
| join               | `$lookup` / app-side join      | (n/a)                           |
| schema (enforced)  | optional validator             | (none)                          |
| `NULL`             | missing field or `null`        | (n/a)                           |
