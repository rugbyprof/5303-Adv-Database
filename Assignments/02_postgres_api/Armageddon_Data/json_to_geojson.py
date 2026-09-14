#!/usr/bin/env python3
"""
Generic script to convert JSON files with geo data to GeoJSON format.
Handles both newline-delimited JSON (NDJSON) and JSON arrays.

Usage:
    python json_to_geojson.py input.json output.geojson [options]

Customize by modifying the FIELD_MAPPINGS dictionary for your data structure.
"""

import json
import sys
from pathlib import Path


# ============================================================================
# CONFIGURATION - Customize this for each dataset
# ============================================================================

FIELD_MAPPINGS = {
    # Maps common field names for latitude/longitude to standardized names
    "latitude_fields": ["latitude", "lat", "reclat", "Latitude", "LAT"],
    "longitude_fields": ["longitude", "lon", "reclong", "Longitude", "LON"],
}

# Optional: Map property field names if you want to rename them
# Leave empty {} to keep all fields as-is
PROPERTY_RENAMES = {
    # 'old_name': 'new_name',
}

# Fields to exclude from GeoJSON properties (keep coordinates separate)
EXCLUDE_PROPERTIES = {
    "latitude",
    "lat",
    "reclat",
    "Latitude",
    "LAT",
    "longitude",
    "lon",
    "reclong",
    "Longitude",
    "LON",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def find_lat_long_fields(record):
    """
    Detect latitude and longitude field names in a record.
    Returns tuple (lat_field, lon_field) or (None, None) if not found.
    """
    lat_field = None
    lon_field = None

    for field in FIELD_MAPPINGS["latitude_fields"]:
        if field in record:
            lat_field = field
            break

    for field in FIELD_MAPPINGS["longitude_fields"]:
        if field in record:
            lon_field = field
            break

    return lat_field, lon_field


def record_to_feature(record, lat_field, lon_field):
    """
    Convert a single record to a GeoJSON Feature.
    """
    try:
        lat = float(record[lat_field])
        lon = float(record[lon_field])

        # Skip records with missing/zero coordinates
        if lat == 0 and lon == 0:
            return None

        # Build properties, excluding coordinate fields
        properties = {}
        for key, value in record.items():
            if key not in EXCLUDE_PROPERTIES:
                # Apply field renames if configured
                new_key = PROPERTY_RENAMES.get(key, key)
                properties[new_key] = value

        # Create GeoJSON Feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],  # GeoJSON uses [lon, lat]
            },
            "properties": properties,
        }
        return feature

    except (ValueError, KeyError, TypeError):
        return None


def load_json_file(filepath):
    """
    Load JSON file, handling both NDJSON and JSON array formats.
    Returns list of records.
    """
    records = []
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Try NDJSON format (one JSON object per line)
    if content and not content.startswith("["):
        for line in content.split("\n"):
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON line: {e}", file=sys.stderr)
    else:
        # Try JSON array format
        try:
            data = json.loads(content)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                # Might be a FeatureCollection or single object
                if "features" in data:
                    records = data["features"]
                else:
                    records = [data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Could not parse JSON: {e}")

    return records


def is_valid_json_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, ValueError):
        return False


def convert_dict_to_records(data):
    records = []
    for key, val in data.items():
        print(key, val)
        records.append(val)

    if isinstance(records[0], list):
        newrecords = []
        for zone in records:
            newrecords.extend(zone)
            return newrecords
    return records


def json_to_geojson(input_file, output_file, verbose=True):
    """
    Main conversion function.
    """

    valid_json = is_valid_json_file(input_file)

    if isinstance(valid_json, dict):
        records = convert_dict_to_records(valid_json)
        backup_file = input_file.replace(".json", "_tmp.json")
        with open(backup_file, "w") as f:
            json.dump(records, f)

        input_file = backup_file

    # Load input data
    records = load_json_file(input_file)

    if not records:
        print("Error: No records found in input file", file=sys.stderr)
        return False

    if verbose:
        print(f"Loaded {len(records)} records from {input_file}")

    # Detect coordinate fields from first record
    lat_field, lon_field = find_lat_long_fields(records[0])

    if not lat_field or not lon_field:
        print(f"Error: Could not find latitude/longitude fields", file=sys.stderr)
        print(f"First record keys: {list(records[0].keys())}", file=sys.stderr)
        return False

    if verbose:
        print(f"Using fields: {lat_field} (latitude), {lon_field} (longitude)")

    # Convert records to GeoJSON features
    features = []
    skipped = 0

    for i, record in enumerate(records):
        feature = record_to_feature(record, lat_field, lon_field)
        if feature:
            features.append(feature)
        else:
            skipped += 1

    if verbose:
        print(f"Converted {len(features)} records to features ({skipped} skipped)")

    # Create GeoJSON FeatureCollection
    geojson = {"type": "FeatureCollection", "features": features}

    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    if verbose:
        print(f"Wrote GeoJSON to {output_file}")

    return True


# ============================================================================
# CLI
# ============================================================================


def main():
    if len(sys.argv) < 3:
        print("Usage: python json_to_geojson.py input.json output.geojson")
        print()
        print("Options:")
        print("  --quiet          Suppress verbose output")
        print("  --help           Show this message")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    verbose = "--quiet" not in sys.argv

    try:
        success = json_to_geojson(input_file, output_file, verbose=verbose)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
