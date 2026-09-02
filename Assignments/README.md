## Assignments

Each assignment is a self-contained folder: a `README.md` spec, a `starter/`
scaffold where relevant, and any `data/` it needs. Generated databases and
`.venv/` stay local (git-ignored).

| Folder | Title | Description | Due |
| :----- | :---- | :---------- | :-- |
| [01_sqlite_api](01_sqlite_api/) | SQLite Behind an API: Where It Shines and Where It Breaks | Wrap the [Lecture 02](../Lectures/02_sqlite/) database in a **FastAPI** service, scale the data up, add progressively harder endpoints (simple reads → joins/aggregates → deep pagination, `LIKE` search, windows, anti-joins → write concurrency), and write a memo on **when to choose SQLite and when not to**. Includes a starter scaffold and a data generator. Foreshadows the token-auth lecture with a thin `X-API-Key` stub. | _TBD_ |
