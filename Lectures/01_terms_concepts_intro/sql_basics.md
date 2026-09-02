# SQL Basics — Week 01

A lecture walkthrough of relational SQL. Term definitions live in
[glossary.md](glossary.md); this file is the teaching flow and the runnable
examples. Sample data to run them against is
[data/students.sql](data/students.sql).

## 1. Relational database concepts


- Database, database management system, and RDBMS
- Tables as collections of related data
- Columns: named attributes with defined data types
- Rows: individual records
- Cells and values
- Schema: the database’s structure
- Tables versus spreadsheets
- Data types:
  - Character strings
  - Integers and decimals
  - Dates and timestamps
  - Boolean values
- `NULL`: unknown or missing, not zero or an empty string
- Constraints and data integrity
- Entity and relationship concepts
- One-to-one, one-to-many, and many-to-many relationships
- Junction/associative tables
- A light introduction to normalization:
  - One fact in one place
  - Avoid repeating groups
  - Avoid duplicated data
  - Separate entities into related tables

## 2. Keys and constraints

Each of these is defined with an example in [glossary.md §2](glossary.md#2-keys-relationships-constraints-and-referential-integrity); cover them here as talking points.

- Candidate key
- Natural key versus surrogate key
- Primary key
- Composite key
- Foreign key
- Unique constraint
- `NOT NULL`
- `CHECK`
- Default values
- Referential integrity
- What happens when a referenced row is updated or deleted
- Generated identity/auto-increment values

A small university example works well ([data/students.sql](data/students.sql)
provides the `students` table and 1,000 rows to query):

```sql
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    major VARCHAR(50),
    graduation_year INTEGER
);

CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_title VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE Enrollments (
    student_id INTEGER,
    course_id INTEGER,
    semester VARCHAR(20),
    grade VARCHAR(2),

    PRIMARY KEY (student_id, course_id, semester),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
```

This demonstrates entities, primary keys, foreign keys, a composite key, and a many-to-many relationship.

## 3. Reading data with `SELECT`

Start with the general query shape:

```sql
SELECT columns
FROM table
WHERE condition
ORDER BY columns;
```

### Retrieve all columns

```sql
SELECT *
FROM Students;
```

Explain why `SELECT *` is useful for exploration but explicit columns are usually preferable in production code.

### Retrieve selected columns

```sql
SELECT student_name, major
FROM Students;
```

### Rename output columns

```sql
SELECT student_name AS name,
       graduation_year AS grad_year
FROM Students;
```

### Compute a value

```sql
SELECT course_title,
       credits * 15 AS estimated_contact_hours
FROM Courses;
```

### Remove duplicate results

```sql
SELECT DISTINCT major
FROM Students;
```

## 4. Searching and filtering

### Equality and comparison

```sql
SELECT student_name, major
FROM Students
WHERE major = 'Computer Science';
```

```sql
SELECT student_name, graduation_year
FROM Students
WHERE graduation_year >= 2027;
```

Cover:

- `=`
- `<>` or `!=`
- `<`, `<=`, `>`, `>=`

### Multiple conditions

```sql
SELECT student_name, major, graduation_year
FROM Students
WHERE major = 'Computer Science'
  AND graduation_year = 2027;
```

```sql
SELECT student_name, major
FROM Students
WHERE major = 'Computer Science'
   OR major = 'Data Science';
```

Introduce parentheses when combining `AND` and `OR`.

### Search a set of values

```sql
SELECT student_name, major
FROM Students
WHERE major IN ('Computer Science', 'Data Science');
```

### Search a range

```sql
SELECT student_name, graduation_year
FROM Students
WHERE graduation_year BETWEEN 2026 AND 2028;
```

Mention that `BETWEEN` includes both endpoints.

### Pattern matching

```sql
SELECT student_name
FROM Students
WHERE student_name LIKE 'A%';
```

- `%`: zero or more characters
- `_`: exactly one character
- Case sensitivity varies among database systems

### Missing values

```sql
SELECT student_name
FROM Students
WHERE major IS NULL;
```

```sql
SELECT student_name
FROM Students
WHERE major IS NOT NULL;
```

Emphasize that `major = NULL` is not the correct test.

## 5. Sorting and limiting results

```sql
SELECT student_name, graduation_year
FROM Students
ORDER BY graduation_year, student_name;
```

```sql
SELECT course_title, credits
FROM Courses
ORDER BY credits DESC;
```

Limiting syntax varies:

```sql
SELECT course_title
FROM Courses
ORDER BY course_title
LIMIT 5;
```

Potential portability note:

- PostgreSQL, MySQL, and SQLite commonly use `LIMIT`
- SQL Server commonly uses `TOP` or `OFFSET … FETCH`
- Standard-style pagination uses `OFFSET … FETCH`

## 6. Aggregate queries

Introduce aggregates as calculations across several rows:

- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`

```sql
SELECT COUNT(*) AS student_count
FROM Students;
```

```sql
SELECT MIN(credits) AS minimum_credits,
       MAX(credits) AS maximum_credits,
       AVG(credits) AS average_credits
FROM Courses;
```

Explain the important distinction between `COUNT(*)` and `COUNT(column)`: the latter does not count `NULL` values.

### Grouping

```sql
SELECT major, COUNT(*) AS student_count
FROM Students
GROUP BY major;
```

### Filtering groups

```sql
SELECT major, COUNT(*) AS student_count
FROM Students
GROUP BY major
HAVING COUNT(*) >= 10;
```

A useful contrast:

- `WHERE` filters rows before grouping
- `HAVING` filters groups after aggregation

## 7. Connecting tables with joins

Begin with an inner join:

```sql
SELECT s.student_name,
       c.course_code,
       c.course_title,
       e.semester
FROM Enrollments AS e
JOIN Students AS s
    ON e.student_id = s.student_id
JOIN Courses AS c
    ON e.course_id = c.course_id;
```

Important points:

- The foreign key establishes the relationship
- `JOIN` combines related rows
- Aliases make queries shorter and clearer
- Qualifying columns avoids ambiguity

### Left join

```sql
SELECT s.student_name,
       e.course_id
FROM Students AS s
LEFT JOIN Enrollments AS e
    ON s.student_id = e.student_id;
```

Use this to find students with no enrollment:

```sql
SELECT s.student_id, s.student_name
FROM Students AS s
LEFT JOIN Enrollments AS e
    ON s.student_id = e.student_id
WHERE e.student_id IS NULL;
```

For an introduction, inner joins and left joins are usually sufficient. Other join types can be mentioned without spending much time on them.

## 8. Changing data

### Insert

```sql
INSERT INTO Students (
    student_id,
    student_name,
    major,
    graduation_year
)
VALUES (
    101,
    'Avery Chen',
    'Computer Science',
    2027
);
```

### Update

```sql
UPDATE Students
SET major = 'Data Science'
WHERE student_id = 101;
```

### Delete

```sql
DELETE FROM Students
WHERE student_id = 101;
```

Stress that `UPDATE` or `DELETE` without `WHERE` affects every row.

A good safety habit is to run the corresponding `SELECT` first:

```sql
SELECT *
FROM Students
WHERE student_id = 101;
```

## 9. Transactions

A short conceptual introduction is valuable:

- A transaction treats related changes as a unit
- `COMMIT` makes changes permanent
- `ROLLBACK` abandons uncommitted changes
- ACID can be introduced at a high level:
  - Atomicity
  - Consistency
  - Isolation
  - Durability

```sql
BEGIN;

UPDATE Courses
SET credits = 4
WHERE course_id = 200;

ROLLBACK;
```

Exact transaction syntax and behavior vary by database system.

## 10. Indexes and query performance

Keep the first treatment conceptual:

- A primary key is commonly indexed automatically
- An index helps the database locate rows
- Indexes speed many reads but consume storage and add write overhead
- Foreign-key and frequently searched columns are common candidates
- An index is not a substitute for a correct query
- Query plans show how the RDBMS intends to execute a query

```sql
CREATE INDEX idx_students_major
ON Students(major);
```

## 11. Useful SQL distinctions

These prevent common beginner confusion (see [glossary.md](glossary.md) for the
full definitions):

- SQL is a language; MySQL, PostgreSQL, SQLite, Oracle, and SQL Server are database systems
- SQL implementations use different dialects
- Tables do not have an inherent display order
- `ORDER BY` is needed when result order matters
- Primary keys identify rows; foreign keys reference rows
- `NULL` means missing or unknown
- Text values normally use single quotes
- SQL generally describes the desired result, not a row-by-row procedure
- Query results are tables, but they are not necessarily stored tables
- Constraints protect data even when applications make mistakes

## 12. Suggested lecture sequence

For a 60–75 minute session:

1. Database, RDBMS, table, row, column, schema
2. Data types and `NULL`
3. Primary and foreign keys
4. Relationships and the sample schema
5. `SELECT` and column projection
6. `WHERE`, comparison, Boolean conditions, and pattern matching
7. `ORDER BY` and limiting
8. Aggregation and `GROUP BY`
9. Inner and left joins
10. `INSERT`, `UPDATE`, and `DELETE`
11. Transactions, constraints, and indexes
12. Short practice exercise

## Practice prompts

- List every student’s name and major.
- Find students graduating in or after 2027.
- Find students whose names begin with `M`.
- List the distinct majors.
- Count students in each major.
- List courses from highest to lowest number of credits.
- Show each student’s enrolled courses.
- Find students who are not enrolled in any course.
- Count enrollments by course.
- Add a student, change the student’s major, and delete the student safely.
- Explain which columns are primary keys and which are foreign keys.
- Explain why `Enrollments` needs both student and course references.