# Repository Structure & Conventions

The rules this repo follows so it stays navigable as more lectures land.

```
5303-Adv-Database/
├── README.md              course overview / syllabus text
├── syllabus.pdf
├── STRUCTURE.md           this file
├── .gitignore
├── .vscode/settings.json  shared editor + SQLTools config
│
├── Lectures/
│   ├── README.md          index table of all lectures
│   ├── 01_terms_concepts_intro/
│   │   ├── README.md      what this lecture is + links to its files
│   │   ├── glossary.md    reference material
│   │   ├── sql_basics.md  the walkthrough
│   │   └── data/          input files this lecture uses
│   │       └── students.sql
│   └── 02_sqlite/
│       ├── README.md
│       ├── sqlite_walkthrough.md
│       ├── running_sqlite.md, requirements.md, encryption_and_passwords.md
│       ├── data/
│       │   └── example_data.csv
│       └── sql/           runnable scripts
│           ├── 01_schema.sql … 90_data_quality.sql
│           └── (rebuild.sql lives at the lecture root — it's the entry point)
│
├── Assignments/
│   └── README.md
└── Resources/
    └── README.md          index of cross-cutting reference material
```

## Naming

- **Folders:** lowercase, words joined by `_`, numeric lectures zero-padded and
  prefixed: `01_terms_concepts_intro`, `02_sqlite`.
  Lowercase is deliberate — a case-only rename (`02_Sqlite` → `02_sqlite`) is
  invisible on macOS but creates a *second* folder on Linux / GitHub Codespaces
  and breaks every path.
- **Files:** lowercase, `_`-separated, `.md` for prose, `.sql` for scripts.
  A lecture's main narrative can be `<topic>_walkthrough.md` or `<topic>_basics.md`;
  `README.md` is always the short index, not the lecture itself.

## Where things go

| Kind of file | Location |
| :--- | :--- |
| Lecture prose | `Lectures/<nn_name>/*.md` |
| SQL scripts for a lecture | `Lectures/<nn_name>/sql/` (entry-point script may sit at the lecture root) |
| **Input data** a lecture reads (`.csv`, `.json`, `.sql` dumps) | `Lectures/<nn_name>/data/` — co-located with the lecture that uses it |
| Data shared by **two or more** lectures | a top-level `datasets/` folder (create it when that first happens); reference it, don't copy |
| **Generated** databases (`.db`, `.sqlite`) | wherever the script builds them (usually the lecture root); **never committed** |
| Editor / tool scratch files (`*.session.sql`) | wherever the tool drops them; **never committed** |

## Git hygiene

- `.gitignore` already excludes `*.db`, `*.sqlite`, `*.sqlite3`, `*.session.sql`,
  and all dotfiles except itself.
- A database that is already tracked is **not** covered by `.gitignore`. Untrack
  it once: `git rm --cached path/to.db` (the file stays on disk).
- Regenerate databases from their scripts; don't rely on a committed copy.
  Each lecture with SQL has a rebuild script that recreates its database from the
  data files.

## Relative paths in scripts

Scripts assume you run `sqlite3` **from the lecture folder**, so paths are short
and stable: `.import data/example_data.csv`, `.read sql/01_schema.sql`. Each
lecture's `README.md` states the directory to run from.
