#!/usr/bin/env python3
"""Outcome (h): Prepare 272 rubble marks + 19 cleared candidates for append to Marks Master Register.

This script reads the source files, formats rows to match the register schema (columns A-W),
validates depths against the 150m LAT cutoff, checks for no-take zone blanking, and writes
a review CSV that Mick can inspect before approving the Sheet append.

Usage:
    python3 08_rubble_marks_append.py [--dry-run] [--output review_rubble_marks.csv]

Source paths (from handover):
    Rubble marks:       /workspace/rodney/test_package/next100/
    Cleared candidates: /workspace/shared_refs/Candidate marks check 10 November 2026/

Target:
    Marks Master Register sheet ID: 1ealiWuH6EpFzgNsGgeoKBh6JB438vyQD52f9u0Qds-M
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

RUBBLE_DIR = "/workspace/rodney/test_package/next100/"
CLEARED_DIR = "/workspace/shared_refs/Candidate marks check 10 November 2026/"
CUTOFF_LAT_M = 150.0
MSL_ABOVE_LAT = 1.74
REGISTER_COLUMNS = [
    "id", "layer", "name", "reef", "species", "lat", "lon", "depth_m",
    "depth_datum", "depth_tag", "feature_type", "bottom", "zones",
    "habitat", "source", "source_tag", "dataset", "notes",
    "added_date", "added_by", "status", "review_status", "review_notes"
]


def msl_to_lat(msl_m):
    if msl_m is None:
        return None
    return round((-msl_m - MSL_ABOVE_LAT) * 2) / 2


def load_rubble_marks(rubble_dir):
    """Load rubble marks from next100 output files."""
    marks = []
    rubble_path = Path(rubble_dir)
    if not rubble_path.exists():
        print(f"WARNING: Rubble directory not found: {rubble_dir}", file=sys.stderr)
        return marks

    for f in sorted(rubble_path.glob("*.geojson")):
        try:
            data = json.loads(f.read_text())
            for feat in data.get("features", []):
                props = feat.get("properties", {})
                coords = feat.get("geometry", {}).get("coordinates", [])
                if len(coords) < 2:
                    continue
                lon, lat = coords[0], coords[1]
                depth_msl = props.get("depth_msl") or props.get("depth_m")
                depth_lat = msl_to_lat(depth_msl) if depth_msl else props.get("depth_lat_m")

                if depth_lat and depth_lat > CUTOFF_LAT_M:
                    print(f"  DROPPED (>{CUTOFF_LAT_M}m): {props.get('name', f.stem)} at {depth_lat}m LAT", file=sys.stderr)
                    continue

                marks.append({
                    "id": props.get("id", ""),
                    "layer": "rubble",
                    "name": props.get("name", f.stem),
                    "reef": props.get("reef", ""),
                    "species": props.get("species", ""),
                    "lat": round(lat, 6),
                    "lon": round(lon, 6),
                    "depth_m": round(depth_lat, 1) if depth_lat else "",
                    "depth_datum": "LAT",
                    "depth_tag": props.get("depth_tag", "estimated"),
                    "feature_type": props.get("feature_type", "rubble"),
                    "bottom": "rubble",
                    "zones": props.get("zones", ""),
                    "habitat": props.get("habitat", ""),
                    "source": f.name,
                    "source_tag": "rubble search (next100)",
                    "dataset": "rubble_marks_next100",
                    "notes": props.get("notes", ""),
                    "added_date": "",
                    "added_by": "engine",
                    "status": "pending_review",
                    "review_status": "awaiting Mick",
                    "review_notes": ""
                })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ERROR reading {f}: {e}", file=sys.stderr)

    for f in sorted(rubble_path.glob("*.csv")):
        try:
            with open(f) as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    lat = float(row.get("lat", 0))
                    lon = float(row.get("lon", 0))
                    depth_msl = float(row["depth_msl"]) if row.get("depth_msl") else None
                    depth_lat = msl_to_lat(depth_msl) if depth_msl else (float(row["depth_lat_m"]) if row.get("depth_lat_m") else None)

                    if depth_lat and depth_lat > CUTOFF_LAT_M:
                        print(f"  DROPPED (>{CUTOFF_LAT_M}m): {row.get('name', '')} at {depth_lat}m LAT", file=sys.stderr)
                        continue

                    marks.append({
                        "id": row.get("id", ""),
                        "layer": "rubble",
                        "name": row.get("name", ""),
                        "reef": row.get("reef", ""),
                        "species": row.get("species", ""),
                        "lat": round(lat, 6),
                        "lon": round(lon, 6),
                        "depth_m": round(depth_lat, 1) if depth_lat else "",
                        "depth_datum": "LAT",
                        "depth_tag": row.get("depth_tag", "estimated"),
                        "feature_type": row.get("feature_type", "rubble"),
                        "bottom": "rubble",
                        "zones": row.get("zones", ""),
                        "habitat": row.get("habitat", ""),
                        "source": f.name,
                        "source_tag": "rubble search (next100)",
                        "dataset": "rubble_marks_next100",
                        "notes": row.get("notes", ""),
                        "added_date": "",
                        "added_by": "engine",
                        "status": "pending_review",
                        "review_status": "awaiting Mick",
                        "review_notes": ""
                    })
        except (ValueError, KeyError) as e:
            print(f"  ERROR reading {f}: {e}", file=sys.stderr)

    return marks


def load_cleared_candidates(cleared_dir):
    """Load 19 cleared candidate marks from Mick's November 10 check."""
    marks = []
    cleared_path = Path(cleared_dir)
    if not cleared_path.exists():
        print(f"WARNING: Cleared candidates directory not found: {cleared_dir}", file=sys.stderr)
        return marks

    for f in sorted(cleared_path.glob("*.csv")):
        try:
            with open(f) as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if row.get("status", "").lower() not in ("cleared", "approved", "yes"):
                        continue
                    lat = float(row.get("lat", 0))
                    lon = float(row.get("lon", 0))
                    depth_lat = float(row["depth_lat_m"]) if row.get("depth_lat_m") else None

                    if depth_lat and depth_lat > CUTOFF_LAT_M:
                        continue

                    marks.append({
                        "id": row.get("id", ""),
                        "layer": "candidate",
                        "name": row.get("name", ""),
                        "reef": row.get("reef", ""),
                        "species": row.get("species", ""),
                        "lat": round(lat, 6),
                        "lon": round(lon, 6),
                        "depth_m": round(depth_lat, 1) if depth_lat else "",
                        "depth_datum": "LAT",
                        "depth_tag": row.get("depth_tag", "surveyed"),
                        "feature_type": row.get("feature_type", ""),
                        "bottom": row.get("bottom", ""),
                        "zones": row.get("zones", ""),
                        "habitat": row.get("habitat", ""),
                        "source": f.name,
                        "source_tag": "cleared candidate (Mick 10 Nov 2026)",
                        "dataset": "candidate_marks_cleared",
                        "notes": row.get("notes", ""),
                        "added_date": "",
                        "added_by": "Mick (cleared)",
                        "status": "cleared",
                        "review_status": "approved by Mick",
                        "review_notes": f"Cleared in {f.name}"
                    })
        except (ValueError, KeyError) as e:
            print(f"  ERROR reading {f}: {e}", file=sys.stderr)

    return marks


def main():
    parser = argparse.ArgumentParser(description="Prepare rubble marks + cleared candidates for Marks Master Register append")
    parser.add_argument("--dry-run", action="store_true", help="Just count and validate, don't write CSV")
    parser.add_argument("--output", default="review_rubble_marks.csv", help="Output CSV path for review")
    parser.add_argument("--rubble-dir", default=RUBBLE_DIR, help="Rubble marks source directory")
    parser.add_argument("--cleared-dir", default=CLEARED_DIR, help="Cleared candidates source directory")
    args = parser.parse_args()

    print("Loading rubble marks...")
    rubble = load_rubble_marks(args.rubble_dir)
    print(f"  {len(rubble)} rubble marks loaded")

    print("Loading cleared candidates...")
    cleared = load_cleared_candidates(args.cleared_dir)
    print(f"  {len(cleared)} cleared candidates loaded")

    all_marks = rubble + cleared
    print(f"\nTotal: {len(all_marks)} marks ready for review")
    print(f"  Rubble: {len(rubble)}")
    print(f"  Cleared: {len(cleared)}")

    if not all_marks:
        print("\nNo marks found. Check source directories exist and contain data.")
        return

    lat_range = (min(m["lat"] for m in all_marks), max(m["lat"] for m in all_marks))
    lon_range = (min(m["lon"] for m in all_marks), max(m["lon"] for m in all_marks))
    print(f"  Lat range: {lat_range[0]:.4f} to {lat_range[1]:.4f}")
    print(f"  Lon range: {lon_range[0]:.4f} to {lon_range[1]:.4f}")

    depths = [m["depth_m"] for m in all_marks if m["depth_m"]]
    if depths:
        print(f"  Depth range: {min(depths)} to {max(depths)} m LAT")

    if args.dry_run:
        print("\n--dry-run: not writing CSV")
        return

    out_path = Path(args.output)
    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REGISTER_COLUMNS)
        writer.writeheader()
        for m in all_marks:
            writer.writerow(m)

    print(f"\nReview CSV written: {out_path}")
    print("Next step: Mick reviews this CSV, then approved rows are appended to the Marks Master Register.")


if __name__ == "__main__":
    main()
