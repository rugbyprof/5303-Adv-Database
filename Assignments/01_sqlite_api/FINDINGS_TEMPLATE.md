# FINDINGS — Assignment 01

> Copy this to `starter_classroom/FINDINGS.md` and fill it in. Keep answers
> short: one to three sentences each, and every answer should point at a
> **number** from `results.md` or a **plan line** from `results.csv`.

## Environment

- SQLite version (`sqlite3 --version`):
- Python version (`python --version`):
- Machine (CPU, RAM, SSD or spinning disk):
- Row counts (copy from the `make_dbs.py` output):

| Size | purchases | customers | products |
| :--- | --------: | --------: | -------: |
| 10k  |           |           |          |
| 100k |           |           |          |
| 1m   |           |           |          |

- Indexes in `idx_1m.db` (paste the output of `sqlite3 data/idx_1m.db ".indexes"`):

```
```

## Results

Paste your whole `results.md` here. All times are median milliseconds.

| Query | noidx_10k | idx_10k | noidx_100k | idx_100k | noidx_1m | idx_1m |
| :---- | --------: | ------: | ---------: | -------: | -------: | -----: |
| Q01   |           |         |            |          |          |        |

---

## Phase 1 — Simple reads (Q01–Q03)

| Query | Plan summary in `noidx_1m` | Plan summary in `idx_1m` |
| :---- | :------------------------- | :----------------------- |
| Q01   |                            |                          |
| Q03   |                            |                          |

*A plan summary is the one or two `SCAN` / `SEARCH` lines that matter, e.g. `SCAN purchases + TEMP B-TREE FOR ORDER BY`.*

1. Why is Q01 fast even in `noidx_*`?

2. What does SQLite do differently for Q03 in the two databases?

## Phase 2 — Where indexes matter (Q04–Q10)

| Query | `noidx_1m` ms | `idx_1m` ms | Speedup (noidx ÷ idx) |
| :---- | ------------: | ----------: | --------------------: |
| Q04   |               |             |                       |
| Q05   |               |             |                       |
| Q06   |               |             |                       |
| Q07   |               |             |                       |
| Q08   |               |             |                       |
| Q09   |               |             |                       |
| Q10   |               |             |                       |

1. Which query had the largest speedup? Quote its two plan summaries and explain the difference.

2. Q09 reads every purchase in both databases. Which word in its `idx_1m` plan explains why it's still faster?

3. Why did Q07 only get about 2× faster?

## Phase 3 — When an index can't save you (Q11–Q14)

| Query                          | slow, `noidx_1m` | slow, `idx_1m` | `/fast`, `idx_1m` |
| :----------------------------- | ---------------: | -------------: | ----------------: |
| Q11 offset → keyset            |                  |                |                   |
| Q12 random sort → random ids   |                  |                |                   |
| Q13 revenue by month → summary |                  |                |                   |
| Q14 cube → summary             |                  |                |                   |

For each, write one or two sentences: **why the slow version is slow** (point at the plan) and **what the rewrite gives up**.

- **Q11:**
- **Q12:**
- **Q13:**
- **Q14:** (also: why is the slow version slower in `idx_1m` than in `noidx_1m`?)

## Phase 4 — Write concurrency (Q15)

| Run  | busy_timeout | workers |    n | succeeded (201) | failed (503) | seconds | writes/sec |
| :--- | -----------: | ------: | ---: | --------------: | -----------: | ------: | ---------: |
| A    |            0 |       1 |  200 |                 |              |         |            |
| A    |            0 |       1 |  500 |                 |              |         |            |
| B    |         5000 |       1 |  200 |                 |              |         |            |
| B    |         5000 |       1 |  500 |                 |              |         |            |
| C    |            0 |       4 |  200 |                 |              |         |            |
| C    |            0 |       4 |  500 |                 |              |         |            |
| D    |         5000 |       4 |  200 |                 |              |         |            |
| D    |         5000 |       4 |  500 |                 |              |         |            |

Exact error text from a failed request:

```
```

Summary-table check (`COUNT(*) FROM purchases` vs. `SUM(num_purchases) FROM monthly_sales`):

```
```

1. What does `busy_timeout` do, and why did B succeed where A failed?

2. Did 4 worker processes make SQLite write faster? Why or why not?

3. Why don't the two summary-check numbers match? What does that cost the `/fast` routes from Phase 3?

## Phase 5 — Conclusions

For each scenario: **SQLite yes or no**, 1–2 sentences, and one number from your results.

1. Internal read-only dashboard, ~10 analysts:
2. Mobile app offline local storage:
3. Thousands of events per second from many servers:
4. Fresh throwaway database per automated test:
