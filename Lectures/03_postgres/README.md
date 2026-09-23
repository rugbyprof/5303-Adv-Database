<details>
<summary>⚙️ Metadata (auto-managed by <code>readmees</code> — edit values, not structure)</summary>

```yaml
is_due: false
id: L03-03_postgres
name: L03-03_postgres
title: NO TITLE
description: NO DESCRIPTION
category: Lectures
date_due:
  month: '09'
  day: '23'
  year: 2026
  hour: 13
```

</details>

# 03 — PostgreSQL + PostGIS

We move from SQLite to PostgreSQL for one main reason: **PostGIS**, its
geospatial extension. This lecture gets PostGIS running locally on Windows or
macOS and loads the
[Armageddon data](../../Assignments/02_postgres_api/Armageddon_Data/)
(earthquakes, airports, UFO sightings, meteorites, country and county outlines,
and more) into it for [Assignment 02](../../Assignments/02_postgres_api/).

## Quick start (Docker)

```bash
cd Lectures/03_postgres
docker compose up -d                                  # PostgreSQL 17 + PostGIS 3.5

cd ../../Assignments/02_postgres_api/Armageddon_Data
pip install "psycopg[binary]"
python load_postgis.py                                # 20 tables, straight from the zips
```

Connection string: `postgresql://student:student@localhost:5432/course`

No Docker? [postgres_setup.md](postgres_setup.md) covers native installs
(Postgres.app on macOS, the EDB installer with Stack Builder on Windows).

## Files

| File | What it is |
| :--- | :--- |
| [postgres_setup.md](postgres_setup.md) | **Start here.** Server vs. file, what PostGIS adds, and three install paths that include PostGIS. Then verifying it, loading the Armageddon data (what the tables look like and what still needs cleaning), first spatial queries (nearest-neighbour, point-in-polygon, distance joins, GeoJSON output), map viewers (DBeaver, QGIS), `psql` vs. SQLite dot commands, and troubleshooting. |
| [docker-compose.yml](docker-compose.yml) | PostgreSQL 17 + PostGIS 3.5. User `student`, database `course`, port 5432, persistent volume. |
| [../../Assignments/02_postgres_api/Armageddon_Data/load_postgis.py](../../Assignments/02_postgres_api/Armageddon_Data/load_postgis.py) | Loads every Armageddon `.zip` into its own staging table with a `geom` column (SRID 4326) and a GiST index. Safe to re-run. |
