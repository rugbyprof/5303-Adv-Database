#!/usr/bin/env python3
"""
Load the Armageddon data into PostgreSQL/PostGIS -- one raw table per file.

Reads straight from the .zip archives in this folder (no need to unzip first):

    world-earthquakes.zip  ->  table  world_earthquakes   (geom geometry(Point, 4326))
    usa-state_counties.zip ->  table  usa_state_counties  (geom geometry(MultiPolygon, 4326))
    world-country_codes.zip -> table  world_country_codes (no geometry -- plain JSON)

Every table gets a surrogate key `gid`, one column per property (renamed to
snake_case), and -- for GeoJSON -- a `geom` column in SRID 4326 (lon/lat) with a
GiST index. Values are loaded *as-is*: strings like 'NA' or '10/10/1949 21:00'
stay text. Cleaning types and designing the real schema is your job; treat these
as staging tables.

Usage (from this folder):
    pip install "psycopg[binary]"
    python load_postgis.py                          # load every file
    python load_postgis.py world-earthquakes usa-state_counties   # just these
    python load_postgis.py --dsn postgresql://user:pw@host:5432/db

The connection string comes from --dsn, else $DATABASE_URL, else the course
default below. Re-running is safe: each table is dropped and recreated.
"""

import argparse
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path

import psycopg
from psycopg import sql

DEFAULT_DSN = "postgresql://student:student@localhost:5432/course"
HERE = Path(__file__).resolve().parent


# ============================================================================
# READING
# ============================================================================


def read_json_from_zip(zip_path):
    """Return (member_name, parsed JSON) for the single .json/.geojson in a zip."""
    with zipfile.ZipFile(zip_path) as zf:
        member = next(
            n for n in zf.namelist() if n.endswith((".json", ".geojson"))
        )
        text = zf.read(member).decode("utf-8-sig")
    try:
        return member, json.loads(text)
    except json.JSONDecodeError:
        # A few source files have trailing commas (`...},\n]`), which JSON forbids.
        return member, json.loads(re.sub(r",\s*([\]}])", r"\1", text))


# ============================================================================
# SCHEMA INFERENCE
# ============================================================================


def snake_case(name):
    """'duration (seconds)' -> 'duration_seconds', 'VolcanoID' -> 'volcano_id'."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(name))
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    if not s:
        s = "field"
    if s[0].isdigit():
        s = "c_" + s
    return s


def column_names(keys):
    """Map original property keys to unique snake_case column names."""
    taken = {"gid", "geom"}
    out = {}
    for key in keys:
        base = col = snake_case(key)
        n = 2
        while col in taken:
            col = f"{base}_{n}"
            n += 1
        taken.add(col)
        out[key] = col
    return out


def pg_type(values):
    """Pick the narrowest PostgreSQL type that holds every non-null value."""
    seen = {type(v) for v in values if v is not None}
    if not seen:
        return "text"
    if seen == {bool}:
        return "boolean"
    if seen == {int}:
        big = any(abs(v) > 2**31 - 1 for v in values if v is not None)
        return "bigint" if big else "integer"
    if seen <= {int, float}:
        return "double precision"
    if seen <= {dict, list}:
        return "jsonb"
    return "text"


# Mixed single/multi geometries are promoted to the Multi type so the column can
# be declared with one concrete type (and ST_Multi applied on insert).
PROMOTE = {
    frozenset({"Polygon", "MultiPolygon"}): "MultiPolygon",
    frozenset({"LineString", "MultiLineString"}): "MultiLineString",
    frozenset({"Point", "MultiPoint"}): "MultiPoint",
}


def geometry_type(features):
    kinds = {(f.get("geometry") or {}).get("type") for f in features} - {None}
    if len(kinds) == 1:
        return kinds.pop(), False
    if frozenset(kinds) in PROMOTE:
        return PROMOTE[frozenset(kinds)], True
    return "Geometry", False


# ============================================================================
# LOADING
# ============================================================================


def to_copy_value(v):
    if isinstance(v, (dict, list)):
        return json.dumps(v)
    return v


def load_table(conn, table, rows, geometries=None):
    """
    Create `table` from a list of property dicts and load it with COPY.
    `geometries` (same length as rows) are GeoJSON geometry dicts, or None for
    non-spatial files.
    """
    keys = list(dict.fromkeys(k for r in rows for k in r))  # union, first-seen order
    cols = column_names(keys)
    types = {k: pg_type([r.get(k) for r in rows]) for k in keys}

    col_defs = [sql.SQL("gid serial PRIMARY KEY")]
    col_defs += [
        sql.SQL("{} {}").format(sql.Identifier(cols[k]), sql.SQL(types[k]))
        for k in keys
    ]
    spatial = geometries is not None
    if spatial:
        gtype, promote = geometry_type([{"geometry": g} for g in geometries])
        col_defs.append(sql.SQL(f"geom geometry({gtype}, 4326)"))

    t = sql.Identifier(table)
    prop_cols = [sql.Identifier(cols[k]) for k in keys]

    with conn.cursor() as cur:
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(t))
        cur.execute(sql.SQL("CREATE TABLE {} ({})").format(t, sql.SQL(", ").join(col_defs)))

        if not spatial:
            copy = sql.SQL("COPY {} ({}) FROM STDIN").format(t, sql.SQL(", ").join(prop_cols))
            with cur.copy(copy) as cp:
                for r in rows:
                    cp.write_row([to_copy_value(r.get(k)) for k in keys])
            return len(rows), None

        # COPY into a temp table with the geometry as GeoJSON text, then convert
        # in one INSERT ... SELECT (COPY itself can't call ST_GeomFromGeoJSON).
        cur.execute(
            sql.SQL("CREATE TEMP TABLE _stage (LIKE {} INCLUDING DEFAULTS, geojson text) ON COMMIT DROP").format(t)
        )
        cur.execute("ALTER TABLE _stage DROP COLUMN geom")
        copy = sql.SQL("COPY _stage ({}, geojson) FROM STDIN").format(sql.SQL(", ").join(prop_cols))
        with cur.copy(copy) as cp:
            for r, g in zip(rows, geometries):
                cp.write_row(
                    [to_copy_value(r.get(k)) for k in keys] + [json.dumps(g) if g else None]
                )

        geom_expr = "ST_SetSRID(ST_GeomFromGeoJSON(geojson), 4326)"
        if promote:
            geom_expr = f"ST_Multi({geom_expr})"
        cur.execute(
            sql.SQL("INSERT INTO {t} ({cols}, geom) SELECT {cols}, " + geom_expr + " FROM _stage ORDER BY gid").format(
                t=t, cols=sql.SQL(", ").join(prop_cols)
            )
        )
        cur.execute(
            sql.SQL("CREATE INDEX {} ON {} USING gist (geom)").format(sql.Identifier(f"{table}_geom_idx"), t)
        )
        cur.execute(sql.SQL("SELECT count(*) FILTER (WHERE NOT ST_IsValid(geom)) FROM {}").format(t))
        invalid = cur.fetchone()[0]
        cur.execute(sql.SQL("ANALYZE {}").format(t))
    return len(rows), (gtype, invalid)


def load_file(conn, zip_path):
    member, data = read_json_from_zip(zip_path)
    table = snake_case(Path(member).stem)

    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        feats = data["features"]
        rows = [f.get("properties") or {} for f in feats]
        geoms = [f.get("geometry") for f in feats]
        return table, load_table(conn, table, rows, geoms)
    if isinstance(data, list) and all(isinstance(r, dict) for r in data):
        return table, load_table(conn, table, data)
    raise ValueError(f"{member}: not a FeatureCollection or a list of objects")


# ============================================================================
# CLI
# ============================================================================


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="zip names to load, e.g. world-earthquakes (default: all)")
    ap.add_argument("--dsn", default=os.environ.get("DATABASE_URL", DEFAULT_DSN))
    ap.add_argument("--dir", type=Path, default=HERE, help="folder with the .zip files")
    args = ap.parse_args()

    zips = sorted(args.dir.glob("*.zip"))
    if args.names:
        wanted = {n.removesuffix(".zip") for n in args.names}
        zips = [z for z in zips if z.stem in wanted]
        missing = wanted - {z.stem for z in zips}
        if missing:
            sys.exit(f"No zip for: {', '.join(sorted(missing))}")
    if not zips:
        sys.exit(f"No .zip files found in {args.dir}")

    try:
        conn = psycopg.connect(args.dsn)
    except psycopg.OperationalError as e:
        sys.exit(f"Could not connect to {args.dsn}\n{e}\nIs the server running?")

    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        conn.commit()

        failed = 0
        for z in zips:
            start = time.perf_counter()
            try:
                with conn.transaction():
                    table, (n, geo) = load_file(conn, z)
            except Exception as e:  # keep going; report at the end
                failed += 1
                print(f"  FAILED  {z.name}: {e}", file=sys.stderr)
                continue
            secs = time.perf_counter() - start
            if geo:
                gtype, invalid = geo
                note = f"  ({invalid} invalid -- see ST_MakeValid)" if invalid else ""
                print(f"  {table:<28} {n:>7,} rows  {gtype}{note}  {secs:.1f}s")
            else:
                print(f"  {table:<28} {n:>7,} rows  (no geometry)  {secs:.1f}s")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
