# PostgreSQL + PostGIS Setup for the Armageddon Data (Windows & macOS)

We use PostgreSQL in this course for **PostGIS**, its geospatial extension. This
guide gets PostGIS running on your laptop and loads the
[Armageddon data](../../Assignments/02_postgres_api/Armageddon_Data/)
(earthquakes, airports, UFO sightings, country and county outlines, and more)
into it. It ends with spatial queries you can run against that data.

The end state:

```
Armageddon_Data/*.zip  ──load_postgis.py──►  PostgreSQL 17 + PostGIS 3.5
                                               database "course"
                                               20 tables, geom columns in SRID 4326
```

---

## 1. The mental model

**PostgreSQL is a server, not a file.** SQLite is a library that opens a
`store.db` file. PostgreSQL is a program that keeps running in the background
and listens on a network port (**5432**). Every client connects to it with
the same five values: `psql`, a GUI, VS Code, your Python API, or the
loader script.

```
host:      localhost
port:      5432
user:      student
password:  student
database:  course

URL form:  postgresql://student:student@localhost:5432/course
```

**PostGIS is an extension installed into a database.** It adds:

- a `geometry` column type (points, lines, polygons in a coordinate system),
- a `geography` type (the same shapes on a round Earth, so distances are in
  meters),
- a few hundred `ST_*` functions (`ST_Distance`, `ST_Contains`, `ST_DWithin`,
  …),
- **GiST spatial indexes** that make "what's near / inside this shape?" fast.

The PostGIS binaries have to be installed on the server machine. Then you run
`CREATE EXTENSION postgis;` once in each database. **An install without PostGIS
is useless for this course,** and that's the main thing that decides which
install option you pick.

---

## 2. Pick an install path

| Option | Windows | macOS | How PostGIS arrives | Use it when |
| :--- | :---: | :---: | :--- | :--- |
| **A. Docker** | ✅ | ✅ | Built into the `postgis/postgis` image | **Default.** Everyone gets identical versions, and resetting takes one command |
| **B. Postgres.app** | — | ✅ | Bundled | Mac, and you don't want Docker |
| **C. EDB installer** | ✅ | — | Separate Stack Builder step | Windows, and Docker/WSL 2 won't run on your machine |

Pick **one**. If two servers both try to use port 5432, you'll be connecting to
the wrong one without realizing it. That's the most common setup problem (see
[§10](#10-troubleshooting)).

> **Why no Homebrew?** `brew install postgis` builds against whichever
> PostgreSQL version Homebrew considers the default. That's often not the one
> you installed, and then `CREATE EXTENSION postgis` fails. If you already
> use Homebrew Postgres for something else, use Docker for this course and map
> it to port 5433 (see §10).

---

## 3. Option A: Docker (recommended, both platforms)

### 3.1 Install Docker Desktop

- **Windows 10/11:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
  It uses **WSL 2**. If the installer asks, let it enable WSL 2, or run this
  in an *admin* PowerShell and reboot:
  ```powershell
  wsl --install
  ```
  Virtualization must be turned on in BIOS/UEFI. Most laptops ship with it on.
- **macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  and pick the right chip: **Apple Silicon** (M-series) or **Intel**.

Start Docker Desktop and wait for "Engine running". Then check:

```bash
docker --version
docker compose version
```

### 3.2 Start the database

This folder has a ready-made [docker-compose.yml](docker-compose.yml). From the
repo root:

```bash
cd Lectures/03_postgres
docker compose up -d
docker compose ps          # STATUS should become "healthy" after a few seconds
```

What that file sets up:

- Image **`postgis/postgis:17-3.5`**: PostgreSQL 17 with PostGIS 3.5 already
  installed.
- User `student`, password `student`, database `course`.
- Port 5432 on your laptop is forwarded to the container.
- A **named volume** (`pgdata`), so your loaded tables survive
  `docker compose down` and reboots.

> **Apple Silicon:** the `postgis/postgis` image is built for Intel (amd64), so
> Docker Desktop runs it under emulation. It works, but it's slower. The compose
> file sets `platform: linux/amd64` to make that explicit. If loading or queries
> feel sluggish, Postgres.app (Option B) runs natively.

<details>
<summary>No compose? The equivalent single <code>docker run</code> command</summary>

```bash
docker run -d --name pg5303 --platform linux/amd64 \
  -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student -e POSTGRES_DB=course \
  -p 5432:5432 -v pgdata:/var/lib/postgresql/data \
  postgis/postgis:17-3.5
```

In Windows PowerShell, put it all on one line, or replace each trailing `\`
with a backtick `` ` ``.
</details>

### 3.3 Everyday commands

```bash
docker compose up -d        # start
docker compose stop         # pause (keeps container + data)
docker compose down         # remove container (data kept in volume)
docker compose down -v      # remove container AND data. Full reset; reload afterwards
docker compose logs -f db   # watch server logs (Ctrl-C to quit)

# psql *inside* the container. No local install needed:
docker compose exec db psql -U student -d course
```

Now skip to [§6 Verify](#6-verify-postgis).

---

## 4. Option B: macOS with Postgres.app

1. Download from [postgresapp.com](https://postgresapp.com/). PostGIS is
   bundled with every build.
2. Drag it into **Applications**, open it, and click **Initialize**. A server
   starts on port 5432. The elephant icon in the menu bar starts and stops it.
3. Put its command-line tools (`psql`, `pg_dump`, …) on your PATH:
   ```bash
   sudo mkdir -p /etc/paths.d &&
   echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
   ```
   Close and reopen Terminal, then run `psql --version`.
4. Create the course user and database. Enable PostGIS as the superuser,
   because a regular user can't create it:
   ```bash
   psql -d postgres -c "CREATE ROLE student LOGIN PASSWORD 'student';"
   psql -d postgres -c "CREATE DATABASE course OWNER student;"
   psql -d course   -c "CREATE EXTENSION postgis;"
   ```

---

## 5. Option C: Windows with the EDB installer

1. Download the **PostgreSQL 17** installer from
   [postgresql.org/download/windows](https://www.postgresql.org/download/windows/).
2. Run it and keep all components checked: **PostgreSQL Server, pgAdmin 4,
   Stack Builder, Command Line Tools**.
3. Set a password for the `postgres` superuser. **Write it down.** Keep port
   **5432**.
4. **PostGIS:** when the installer finishes, launch **Stack Builder**. Pick
   your PostgreSQL 17 install, open **Spatial Extensions**, check **PostGIS 3.x
   Bundle**, and install it. Say yes to the environment-variable prompts.
   *Don't skip this step.*
5. Add the tools to PATH. Open *Start → "Edit the system environment
   variables" → Environment Variables → Path → New*, add
   `C:\Program Files\PostgreSQL\17\bin`, then open a **new** terminal:
   ```powershell
   psql --version
   ```
6. Create the course user and database, and enable PostGIS. Each command
   prompts for the `postgres` password:
   ```powershell
   psql -U postgres -c "CREATE ROLE student LOGIN PASSWORD 'student';"
   psql -U postgres -c "CREATE DATABASE course OWNER student;"
   psql -U postgres -d course -c "CREATE EXTENSION postgis;"
   ```

The server runs as a Windows service (`postgresql-x64-17`) and starts at boot.
To start or stop it, use *Services* (`services.msc`).

> If `psql` output looks garbled or you see a "console code page" warning, run
> `chcp 1252` first, or use Windows Terminal.

---

## 6. Verify PostGIS

Connect with `psql`. Docker users can use
`docker compose exec db psql -U student -d course`:

```bash
psql "postgresql://student:student@localhost:5432/course"
```

```sql
CREATE EXTENSION IF NOT EXISTS postgis;   -- no-op if already enabled
SELECT postgis_full_version();            -- POSTGIS="3.x ..." GEOS=... PROJ=...

-- Wichita Falls → Dallas, great-circle distance in km (≈ 200)
SELECT round(ST_Distance(
         'SRID=4326;POINT(-98.4934 33.9137)'::geography,
         'SRID=4326;POINT(-96.7970 32.7767)'::geography)::numeric / 1000) AS km;
```

If `postgis_full_version()` errors, stop and fix that first (see §10).

---

## 7. Load the Armageddon data

[`load_postgis.py`](../../Assignments/02_postgres_api/Armageddon_Data/load_postgis.py)
reads each `.zip` in `Armageddon_Data/` directly, so you don't need to unzip
anything. It creates one table per file:

```bash
cd Assignments/02_postgres_api/Armageddon_Data
pip install "psycopg[binary]"
python load_postgis.py                 # all files, about 10–30 s
python load_postgis.py world-ufos      # or just one (re-running replaces the table)
```

It connects with `$DATABASE_URL` if you've set it, otherwise the course default
URL. Pass `--dsn postgresql://...` to override, for example if you moved to
port 5433.

### What you get

| Table | Rows | `geom` type |
| :--- | ---: | :--- |
| `usa_border_crossings` | 171 | Point |
| `usa_country_outline` | 326 | LineString |
| `usa_state_capitals` | 50 | Point |
| `usa_state_counties` | 3,220 | MultiPolygon |
| `usa_us_military_bases` | 824 | MultiPolygon |
| `usa_world_military_bases` | 331 | Point |
| `world_airports` | 29,304 | Point |
| `world_cities` | 10 | Point |
| `world_country_capitals` | 241 | Point |
| `world_country_codes` | 217 | *(none, plain table)* |
| `world_country_indicators` | 5,899 | *(none, plain table)* |
| `world_country_outline` | 255 | MultiPolygon |
| `world_country_outline2` | 245 | MultiPolygon |
| `world_earthquakes` | 23,119 | Point |
| `world_meteorites` | 32,187 | Point |
| `world_pirate_attacks` | 7,510 | Point |
| `world_railroads_10m` | 25,413 | LineString |
| `world_shipping_lanes` | 3 | MultiLineString |
| `world_ufos` | 87,184 | Point |
| `world_volcanos` | 1,546 | Point |

Every spatial table has:

- `gid`: a surrogate primary key.
- One column per GeoJSON property, renamed to snake_case (`duration (seconds)`
  → `duration_seconds`, `VolcanoID` → `volcano_id`).
- `geom geometry(<type>, 4326)` with a **GiST index** (`<table>_geom_idx`).
  Files that mix Polygon and MultiPolygon are promoted to MultiPolygon.

### These are *staging* tables

The loader copies values **as they appear in the files.** Cleaning them up is
part of your work, just like `staging_raw` in the SQLite lecture:

- Dates and times are text in several formats: `occurred_on` is
  `1969-01-03 3:16:40`, while `world_ufos.datetime` is `10/10/1949 21:00`.
- Missing values are sometimes the string `'NA'`, which forces whole columns to
  text (for example, every numeric-looking column in `world_country_indicators`).
- `world_volcanos` has a column called `class`, which is a reserved word. Write
  it as `"class"` in queries, or rename it.
- Some polygons may not be valid geometry. The loader prints a count when it
  finds any. Fix them with `UPDATE t SET geom = ST_MakeValid(geom) WHERE NOT ST_IsValid(geom);`.

Check the load:

```sql
\dt                              -- 20 tables
\d world_earthquakes             -- columns + the gist index
SELECT count(*) FROM world_ufos; -- 87184
```

---

## 8. First spatial queries

**`geometry` vs `geography`.** The data is stored as `geometry` in SRID 4326,
which means longitude/latitude in degrees. Geometry math is flat: a distance
between two points comes back *in degrees*, which means nothing physically. For
real distances, cast to `geography` (`geom::geography`) and you get **meters**
on the globe. Containment tests (`ST_Contains`, `ST_Intersects`) work fine on
`geometry`.

**Nearest neighbours.** Find the 5 airports closest to Wichita Falls. The `<->`
operator walks the GiST index, so this is fast even across 29k rows:

```sql
SELECT name, iata, city,
       round(ST_Distance(geom::geography,
                         ST_MakePoint(-98.4934, 33.9137)::geography)::numeric / 1000, 1) AS km
FROM world_airports
ORDER BY geom <-> ST_SetSRID(ST_MakePoint(-98.4934, 33.9137), 4326)
LIMIT 5;
```

**Point-in-polygon join.** Count UFO sightings per Texas county
(`statefp = '48'`):

```sql
SELECT co.name AS county, count(*) AS sightings
FROM usa_state_counties co
JOIN world_ufos u ON ST_Contains(co.geom, u.geom)
WHERE co.statefp = '48'
GROUP BY co.name
ORDER BY sightings DESC
LIMIT 10;
```

**Distance join in meters.** Find the capitals with the most magnitude 7+
earthquakes within 500 km:

```sql
SELECT c.city, c.country, count(*) AS quakes, max(e.magnitude) AS biggest
FROM world_country_capitals c
JOIN world_earthquakes e
  ON ST_DWithin(c.geom::geography, e.geom::geography, 500000)   -- meters
WHERE e.magnitude >= 7
GROUP BY c.city, c.country
ORDER BY quakes DESC
LIMIT 10;
```

Casting inside the join means the geometry index can't be used. That's fine
at this size. For big distance joins, add a real `geography` column and index it.

**Which country did each meteorite land in?**

```sql
SELECT c.admin AS country, count(*) AS meteorites
FROM world_country_outline c
JOIN world_meteorites m ON ST_Intersects(c.geom, m.geom)
GROUP BY c.admin
ORDER BY meteorites DESC
LIMIT 10;
```

**GeoJSON back out (for your API).** PostgreSQL can build the whole response
itself:

```sql
SELECT json_build_object(
         'type', 'FeatureCollection',
         'features', json_agg(json_build_object(
             'type', 'Feature',
             'geometry', ST_AsGeoJSON(geom)::json,
             'properties', json_build_object('name', v_name, 'country', country))))
FROM world_volcanos
WHERE country = 'Italy';
```

---

## 9. Seeing it on a map, and other clients

### Map viewers

- **DBeaver Community** (free, Windows/Mac) shows a **Spatial** tab for
  geometry columns, so query results appear on a map. It's the easiest way to
  check that a result looks right.
- **QGIS** (free, Windows/Mac) is a full GIS. Go to *Layer → Add Layer → Add
  PostGIS Layers*, add a connection with the §1 values, and drag tables onto
  the map.
- **pgAdmin 4** (bundled with the Windows installer) has a *Geometry Viewer*
  button on geometry columns in query results.
- Anything else: paste `ST_AsGeoJSON` output into [geojson.io](https://geojson.io).

### psql cheat sheet

Postgres uses **backslash** commands the way `sqlite3` uses dot commands:

| psql | SQLite equivalent | Meaning |
| :--- | :--- | :--- |
| `\l` | — | list databases |
| `\c dbname` | `.open` | connect to another database |
| `\dt` | `.tables` | list tables |
| `\d tablename` | `.schema tablename` | describe a table (columns, indexes) |
| `\dx` | — | list installed extensions (look for `postgis`) |
| `\i file.sql` | `.read file.sql` | run a script |
| `\x` | `.mode line` | toggle expanded (vertical) output. Handy for wide rows |
| `\timing` | `.timer on` | show query times. Try a query with and without the index |
| `\q` | `.quit` | quit |

### VS Code (SQLTools)

Install **SQLTools** and the **SQLTools PostgreSQL/Cockroach Driver**. Then add
a connection with the §1 values. It shows `geom` as hex (WKB), so select
`ST_AsText(geom)` when you want to read it.

### Python

```python
import psycopg

DSN = "postgresql://student:student@localhost:5432/course"

with psycopg.connect(DSN) as conn:
    rows = conn.execute(
        "SELECT name, ST_Y(geom) AS lat, ST_X(geom) AS lon "
        "FROM world_airports WHERE iata = %s", ("SPS",)
    ).fetchall()
    print(rows)
```

Placeholders are `%s`, not `?` like in `sqlite3`. Keep the connection string in
an `.env` file (`DATABASE_URL=...`), not in your code. The repo's `.gitignore`
already keeps dotfiles out of git.

---

## 10. Troubleshooting

| Symptom | Likely cause → fix |
| :--- | :--- |
| `connection refused` / `could not connect to server` | The server isn't running. Docker: is Docker Desktop open, and does `docker compose ps` show healthy? Native: start Postgres.app or the Windows service |
| `port is already allocated` (Docker), or tables "disappear" | Another PostgreSQL owns 5432, and you're connected to that one. Stop it, **or** change the compose port to `"5433:5432"` and use `--dsn postgresql://student:student@localhost:5433/course` |
| `could not open extension control file ".../postgis.control"` | This server has no PostGIS binaries. Windows: run the Stack Builder step (§5.4). Otherwise use Docker or Postgres.app |
| `permission denied to create extension "postgis"` | Native installs: enable it as the superuser (§4.4 / §5.6). Then re-run the loader |
| `type "geometry" does not exist` | PostGIS isn't enabled in *this* database. Run `CREATE EXTENSION postgis;` while connected to `course` |
| `password authentication failed for user "student"` | Docker: env vars only apply on the **first** start of an empty volume. Run `docker compose down -v`, then `up -d`, and reload. Native: re-run the `CREATE ROLE` step |
| `ModuleNotFoundError: No module named 'psycopg'` | Run `pip install "psycopg[binary]"` in the same Python/venv you run the loader with |
| `psql: command not found` / not recognized | Not on PATH (§4.3 / §5.5). Open a **new** terminal. Docker users can use `docker compose exec db psql …` |
| Loader or queries are slow on an M-series Mac with Docker | That's amd64 emulation. It's fine for coursework. For native speed, use Postgres.app |
| Windows: Docker says WSL 2 is required / virtualization disabled | Run `wsl --install` in an admin PowerShell, reboot, and enable virtualization in BIOS if needed |

---

## 11. Reset / uninstall

- **Start over with empty tables:** re-run `python load_postgis.py`. Each table
  is dropped and reloaded.
- **Docker:** `docker compose down -v` deletes the container and all data.
  `docker rmi postgis/postgis:17-3.5` removes the image.
- **Postgres.app:** quit it, delete the app, and delete
  `~/Library/Application Support/Postgres`.
- **Windows EDB:** *Settings → Apps → PostgreSQL 17 → Uninstall*, then delete
  `C:\Program Files\PostgreSQL\17\data` if it's still there.
