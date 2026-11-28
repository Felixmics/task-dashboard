#!/usr/bin/env python3 -I
"""
RODNEY Marks Master Register — zoning screen (step 10).

Reads the register (CSV export or Google Sheets JSON), performs a
point-in-polygon spatial join against GBRMPA Zoning Plan 2003 polygons
(Cairns corridor GeoJSON), and writes two outputs:

  1. zoning_results.csv   – every mark with zone, group, legal_screening
  2. zoning_summary.txt   – counts by zone type and flagged marks

The script does NOT write back to the Google Sheet.  Mick reviews the CSV
first; a separate apply step pushes approved results.

Usage:
    python3 -I 10_zoning_screen.py \
        --register marks_register.csv \
        --zoning   GBRMP_zoning_Cairns_corridor.geojson \
        --out      zoning_results.csv

If --register is omitted the script tries to read the sheet via the
Google Sheets CSV export URL (requires network).
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

try:
    from shapely.geometry import Point, shape
    from shapely.prepared import prep
except ImportError:
    sys.exit("shapely is required: pip install shapely")

# ---------------------------------------------------------------------------
# GBRMPA zoning classification for line fishing
# ---------------------------------------------------------------------------
FISHING_STATUS = {
    "General Use":               "LINE_FISHING_OK",
    "Habitat Protection":        "LINE_FISHING_OK",
    "Conservation Park":         "LIMITED_1_LINE_1_HOOK",
    "Marine National Park":      "NO_TAKE",
    "Scientific Research":       "NO_TAKE_NO_ENTRY",
    "Preservation":              "NO_TAKE_NO_ENTRY",
    "Commonwealth Islands (GBRMPA)": "SPECIAL_RULES",
    "Buffer":                    "NO_TAKE",
}

FISHING_ALLOWED = {"LINE_FISHING_OK", "LIMITED_1_LINE_1_HOOK"}


def load_zoning(path: str) -> list[dict]:
    """Load GBRMPA zoning GeoJSON and prepare geometries."""
    with open(path) as f:
        gj = json.load(f)
    zones = []
    for feat in gj["features"]:
        geom = shape(feat["geometry"])
        if not geom.is_valid:
            geom = geom.buffer(0)
        zones.append({
            "geom": prep(geom),
            "raw_geom": geom,
            "type": feat["properties"]["TYPE"],
            "group": feat["properties"]["GROUP_ID"],
            "name": feat["properties"]["NAME"],
            "desc": feat["properties"].get("PERMIT_DESC", ""),
            "alt_zone": feat["properties"].get("ALT_ZONE", ""),
        })
    return zones


def classify_point(lat: float, lon: float, zones: list[dict]) -> dict:
    """Return the zone a point falls in, or OUTSIDE_ZONING if none."""
    pt = Point(lon, lat)
    for z in zones:
        if z["geom"].contains(pt):
            zone_type = z["type"]
            return {
                "zone": zone_type,
                "zone_group": z["group"],
                "zone_name": z["name"],
                "zone_desc": z["desc"],
                "legal_screening": FISHING_STATUS.get(zone_type, "UNKNOWN"),
                "fishing_ok": FISHING_STATUS.get(zone_type, "UNKNOWN") in FISHING_ALLOWED,
            }
    return {
        "zone": "OUTSIDE_ZONING_POLYGONS",
        "zone_group": "",
        "zone_name": "",
        "zone_desc": "Not inside any named zone polygon — likely General Use or outside the marine park boundary",
        "legal_screening": "UNRESOLVED_CHECK_CHARTPLOTTER",
        "fishing_ok": None,
    }


def load_register_csv(path: str) -> list[dict]:
    """Load register from a local CSV file."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def run(register_path: str, zoning_path: str, out_path: str) -> None:
    print(f"Loading zoning polygons from {zoning_path} ...")
    zones = load_zoning(zoning_path)
    print(f"  {len(zones)} zone polygons loaded")

    print(f"Loading register from {register_path} ...")
    rows = load_register_csv(register_path)
    print(f"  {len(rows)} marks loaded")

    fieldnames = list(rows[0].keys()) if rows else []
    extra_fields = [
        "zone_result", "zone_group_result", "zone_name_result",
        "zone_desc_result", "legal_screening_result", "fishing_ok",
    ]

    results = []
    skipped = 0
    counts = {}
    no_take_marks = []

    for i, row in enumerate(rows):
        lat_s = row.get("lat", "").strip()
        lon_s = row.get("lon", "").strip()
        if not lat_s or not lon_s:
            skipped += 1
            row.update({f: "" for f in extra_fields})
            results.append(row)
            continue

        try:
            lat = float(lat_s)
            lon = float(lon_s)
        except ValueError:
            skipped += 1
            row.update({f: "" for f in extra_fields})
            results.append(row)
            continue

        cls = classify_point(lat, lon, zones)
        row["zone_result"] = cls["zone"]
        row["zone_group_result"] = cls["zone_group"]
        row["zone_name_result"] = cls["zone_name"]
        row["zone_desc_result"] = cls["zone_desc"]
        row["legal_screening_result"] = cls["legal_screening"]
        row["fishing_ok"] = "yes" if cls["fishing_ok"] else ("no" if cls["fishing_ok"] is False else "")

        zone_type = cls["zone"]
        counts[zone_type] = counts.get(zone_type, 0) + 1

        if cls["legal_screening"] in ("NO_TAKE", "NO_TAKE_NO_ENTRY"):
            no_take_marks.append({
                "id": row.get("id", f"row_{i+2}"),
                "lat": lat,
                "lon": lon,
                "reef": row.get("reef", ""),
                "species": row.get("species", ""),
                "zone": zone_type,
                "zone_name": cls["zone_name"],
            })

        results.append(row)

        if (i + 1) % 500 == 0:
            print(f"  ... {i+1}/{len(rows)} marks processed")

    # Write results CSV
    out_fields = fieldnames + extra_fields
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    print(f"\nResults written to {out_path}")

    # Write summary
    summary_path = out_path.replace(".csv", "_summary.txt")
    screened = len(rows) - skipped
    with open(summary_path, "w") as f:
        f.write("RODNEY Marks Master Register — Zoning Screen Summary\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Total marks:     {len(rows)}\n")
        f.write(f"Screened:        {screened}\n")
        f.write(f"Skipped (no coords): {skipped}\n\n")

        f.write("Zone breakdown:\n")
        for zone_type, count in sorted(counts.items(), key=lambda x: -x[1]):
            status = FISHING_STATUS.get(zone_type, "UNKNOWN")
            f.write(f"  {zone_type:35s}  {count:5d}  ({status})\n")

        no_take_count = len(no_take_marks)
        ok_count = sum(1 for r in results
                       if r.get("fishing_ok") == "yes")
        limited_count = sum(1 for r in results
                           if r.get("legal_screening_result") == "LIMITED_1_LINE_1_HOOK")
        outside_count = counts.get("OUTSIDE_ZONING", 0)

        f.write(f"\n--- Fishing status ---\n")
        f.write(f"  Line fishing OK:        {ok_count}\n")
        f.write(f"  Limited (1 line/hook):   {limited_count}\n")
        f.write(f"  NO TAKE:                {no_take_count}\n")
        f.write(f"  Outside corridor:       {outside_count}\n")
        f.write(f"  Skipped:                {skipped}\n")

        if no_take_marks:
            f.write(f"\n--- NO-TAKE marks (must be removed or flagged) ---\n")
            for m in no_take_marks:
                f.write(f"  {m['id']:15s}  {m['lat']:10.5f}  {m['lon']:10.5f}  "
                        f"{m['reef']:25s}  {m['species']:20s}  {m['zone']} ({m['zone_name']})\n")

    print(f"Summary written to {summary_path}")
    print(f"\nDone: {screened} screened, {no_take_count} NO-TAKE, "
          f"{ok_count} fishing OK, {outside_count} outside corridor")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RODNEY zoning screen")
    parser.add_argument("--register", required=True, help="Path to register CSV")
    parser.add_argument("--zoning", required=True,
                        help="Path to GBRMP_zoning_Cairns_corridor.geojson")
    parser.add_argument("--out", default="zoning_results.csv",
                        help="Output CSV path")
    args = parser.parse_args()
    run(args.register, args.zoning, args.out)
