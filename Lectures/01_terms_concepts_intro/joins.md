---
topic: "SQL Join Diagrams"
course: "Advanced Databases"
concepts:
  ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN", "CROSS JOIN"]
---

Here are some **row/table diagrams over the usual Venn diagrams**. Venn diagrams are decent mnemonics, but joins operate on rows according to a predicate—not on mystical overlapping circles.

Suppose we have these two tables:

```text
STUDENT                         MAJOR
+----+----------+----------+    +----------+------------------+
| id | name     | major_id |    | major_id | major_name       |
+----+----------+----------+    +----------+------------------+
|  1 | Alice    | 10       |    | 10       | Computer Science |
|  2 | Bob      | 20       |    | 20       | Mathematics      |
|  3 | Charlie  | NULL     |    | 30       | Biology          |
|  4 | Diana    | 10       |    | 40       | History          |
+----+----------+----------+    +----------+------------------+
```

The relationship we're joining on is:

```text
STUDENT.major_id = MAJOR.major_id
```

## 1. INNER JOIN — only matching rows

```sql
SELECT s.name, m.major_name
FROM student s
INNER JOIN major m
    ON s.major_id = m.major_id;
```

Think:

```text
STUDENT                         MAJOR

Alice   ─── 10 ───────────────► 10 ─── Computer Science
Bob     ─── 20 ───────────────► 20 ─── Mathematics
Charlie ─── NULL                 30 ─── Biology
Diana   ─── 10 ───────────────► 40 ─── History
```

Only rows with a successful match survive:

```text
+-------+------------------+
| name  | major_name       |
+-------+------------------+
| Alice | Computer Science |
| Bob   | Mathematics      |
| Diana | Computer Science |
+-------+------------------+
```

**INNER JOIN = "Give me matches."**

---

## 2. LEFT JOIN — everyone on the left survives

```sql
SELECT s.name, m.major_name
FROM student s
LEFT JOIN major m
    ON s.major_id = m.major_id;
```

```text
STUDENT                         MAJOR

Alice   ─── 10 ───────────────► 10 ─── Computer Science
Bob     ─── 20 ───────────────► 20 ─── Mathematics
Charlie ─── NULL ───────X        30 ─── Biology
Diana   ─── 10 ───────────────► 40 ─── History

▲
│
ALL THESE ROWS SURVIVE
```

Result:

```text
+---------+------------------+
| name    | major_name       |
+---------+------------------+
| Alice   | Computer Science |
| Bob     | Mathematics      |
| Charlie | NULL             |
| Diana   | Computer Science |
+---------+------------------+
```

Charlie's row survives because `STUDENT` is the **left table**. SQL fills the missing right-hand columns with `NULL`.

**LEFT JOIN = "Give me everybody on the left, plus whatever matches."**

This is probably the outer join students should understand best because it's enormously useful.

---

## 3. RIGHT JOIN — everyone on the right survives

Reverse the idea:

```sql
SELECT s.name, m.major_name
FROM student s
RIGHT JOIN major m
    ON s.major_id = m.major_id;
```

```text
STUDENT                         MAJOR

Alice   ─── 10 ───────────────► 10 ─── Computer Science
Bob     ─── 20 ───────────────► 20 ─── Mathematics
Charlie ─── NULL                 30 ─── Biology
Diana   ─── 10 ───────────────► 40 ─── History
                                  ▲
                                  │
                         ALL THESE ROWS SURVIVE
```

Result:

```text
+-------+------------------+
| name  | major_name       |
+-------+------------------+
| Alice | Computer Science |
| Diana | Computer Science |
| Bob   | Mathematics      |
| NULL  | Biology          |
| NULL  | History          |
+-------+------------------+
```

Biology and History don't have students, but they survive because `MAJOR` is on the **right**.

**RIGHT JOIN = "Give me everybody on the right, plus whatever matches."**

And pedagogically, once they understand `LEFT JOIN`, I'd spend about 37 seconds on `RIGHT JOIN`. You can usually rewrite it by swapping table order and using `LEFT JOIN`.

---

## 4. FULL OUTER JOIN — everybody survives

```sql
SELECT s.name, m.major_name
FROM student s
FULL OUTER JOIN major m
    ON s.major_id = m.major_id;
```

Conceptually:

```text
        KEEP EVERYTHING

STUDENT                         MAJOR

Alice   ─── 10 ───────────────► 10 ─── Computer Science
Bob     ─── 20 ───────────────► 20 ─── Mathematics
Charlie ─── NULL                 30 ─── Biology
Diana   ─── 10 ───────────────► 40 ─── History

  KEEP                            KEEP
```

Result:

```text
+---------+------------------+
| name    | major_name       |
+---------+------------------+
| Alice   | Computer Science |
| Diana   | Computer Science |
| Bob     | Mathematics      |
| Charlie | NULL             |
| NULL    | Biology          |
| NULL    | History          |
+---------+------------------+
```

**FULL OUTER JOIN = "Give me everybody from both sides; match them where possible."**

---

# The Four-JOIN Cheat Sheet

Here's the diagram I'd actually put on a lecture slide:

```text
                 INNER JOIN
              matching rows only

         LEFT                 RIGHT
          │                     │
          └─────── MATCH ───────┘
                  ▲
                  │
                KEEP


                 LEFT JOIN
          keep entire LEFT side

         LEFT                 RIGHT
          │                     │
          ├─────── MATCH ───────┤
          │
          ▼
        KEEP ALL


                 RIGHT JOIN
          keep entire RIGHT side

         LEFT                 RIGHT
          │                     │
          ├─────── MATCH ───────┤
                                │
                                ▼
                              KEEP ALL


              FULL OUTER JOIN
              keep BOTH sides

         LEFT                 RIGHT
          │                     │
          ├─────── MATCH ───────┤
          │                     │
          ▼                     ▼
        KEEP ALL              KEEP ALL
```

Or even more brutally simplified:

```text
INNER       = MATCH

LEFT        = LEFT  + MATCH

RIGHT       = MATCH + RIGHT

FULL OUTER  = LEFT  + MATCH + RIGHT
```

That's the mental model I'd want them leaving class with.

---

## 5. CROSS JOIN — everybody dates everybody

This one is fundamentally different.

```sql
SELECT s.name, m.major_name
FROM student s
CROSS JOIN major m;
```

There is **no matching condition**.

Every student is paired with every major:

```text
Alice ─────┬── Computer Science
           ├── Mathematics
           ├── Biology
           └── History

Bob ───────┬── Computer Science
           ├── Mathematics
           ├── Biology
           └── History

Charlie ───┬── Computer Science
           ├── Mathematics
           ├── Biology
           └── History

Diana ─────┬── Computer Science
           ├── Mathematics
           ├── Biology
           └── History
```

If:

```text
STUDENT = 4 rows
MAJOR   = 4 rows
```

then:

```text
CROSS JOIN = 4 × 4 = 16 rows
```

In general:

\[
|A \times B| = |A| \times |B|
\]

That's a nice place to connect SQL back to the **Cartesian product in relational algebra** without making the entire database course turn into a semester-long mathematical hostage situation.

---

# The Important Part Students Usually Miss

The **join type** tells SQL what to do with **unmatched rows**.

The `ON` clause tells SQL **what constitutes a match**.

Those are two separate ideas:

```sql
SELECT *
FROM student s
LEFT JOIN major m
    ON s.major_id = m.major_id;
```

```text
LEFT JOIN
    │
    └── What happens when rows DON'T match?
        Keep the left row.

ON s.major_id = m.major_id
    │
    └── How do we determine whether rows DO match?
```

That distinction becomes really useful once you introduce multi-column joins and conditions more complicated than `PK = FK`.

For your database course, I'd probably teach them in this order:

**INNER → LEFT → FULL OUTER → CROSS → RIGHT**

because `RIGHT JOIN` adds almost no conceptual value once they understand `LEFT JOIN`, while `CROSS JOIN` gives you a beautiful bridge into Cartesian products and relational algebra.
