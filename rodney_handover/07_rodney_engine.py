#!/usr/bin/env python3
"""RODNEY point-data-first engine core (14 Nov 2026, Grok Bot, box only).
Shared by engine_test.py (v2) and the local planner server (/workspace/rodney/planner/planner_server.py).

Rules built in (Mick):
- DEPTH RULE (Mick, 21 Nov 2026 5:55 pm, replaces the 120 m hard cutoff): keep marks to 150 m LAT, label 120-150 m "deep",
  drop anything deeper, show each species' sweet-spot depth first. Checked on EVERY input: point table at load (own depth
  AND HD8 depth), pressure points at load, grids at lookup, species bands capped at 150 m, every candidate re-checked.
  Sweet spots = SWEET below, DEMERSAL only; pelagics have no depth sweet spot or depth ranking - judged on water features (Mick 21 Nov 7:32 pm).
  (was:) Sweet spots = SWEET below (same table as the package's rodney_depth_rule.py; red emperor 40-80 m).
  NOTE: the point table, pressure points and grids below are still the 12 Nov 120 m cut copies until their owners make
  150 m copies and they are switched in, so nothing deeper than 120 m can come out yet.
- LAT depths, MSL = LAT + 1.74 m, 0.5 m rounding, tagged surveyed / estimated.
- No-take blanking: GBRMPA MNP / Preservation / Scientific Research (+300 m margin) and Commonwealth Islands
  Buffer zones are NOT blanked (Mick 21 Nov 6:23 pm: legal with restrictions -> shown): labelled 'Buffer zone: troll only for pelagics';
  pelagic species only there (bottom fishing is not allowed in a Buffer zone)
  (zoning gpkg), GBRMPA no-take blank geojson, Qld state no-take geojson. Blank spots are never suggested.
- Point data first (G1 hd8check table, G3-corrected tags), then HD8 10 m cut grid, then GBR30 cut (estimated) last.
- 20 FINAL species (DE01-DE10, PE01-PE10) from the v5 tables + 12 Nov test profiles (Arlington rerun profiles.py).
Model only. Not for navigation. ITS A PREDICTING APP, INTENT. NO GUARANTEE IS ACCEPTED."""
import json, math, os, re, sys, importlib.util, datetime as dt
import numpy as np

W = "/workspace"
PL = f"{W}/shared_refs/Project Library"
CUTOFF_LAT_M = 150.0                   # Mick 21 Nov 2026: deeper than 150 m LAT is dropped (was a 120 m hard cutoff)
DEEP_LAT_M = 120.0                     # 120-150 m LAT kept, labelled "deep"
MSL_ABOVE_LAT = 1.74
CUTOFF_MSL_M = -(CUTOFF_LAT_M + MSL_ABOVE_LAT)  # -151.74 (150 m LAT = 151.74 m below MSL)
# species_id: (sweet_lo, sweet_hi), (band_lo, band_hi) - FINAL 20 species tables, capped at 150 m (= package rodney_depth_rule.SWEET)
SWEET = {
    "DE01": ((5, 40), (3, 100)), "DE02": ((2, 30), (2, 50)), "DE03": ((40, 80), (10, 150)), "DE04": ((25, 80), (10, 140)),
    "DE05": ((20, 60), (5, 100)), "DE06": ((1, 30), (1, 75)), "DE07": ((10, 40), (5, 90)), "DE08": ((10, 100), (0, 120)),
    "DE09": ((1, 150), (1, 150)), "DE10": ((2, 80), (2, 80)),
}
# Mick 21 Nov 2026 7:31-7:32 pm: "WHY WOULD PELAGIC NEED DEPTH" / "FIX THE LOGIC TO PELAGIC SO BOTS KNOW THE DIFFERENCE".
# Each species has a type. Depth sweet spots, depth bands and depth-based ranking apply to DEMERSAL species only.
# Pelagic species never get a depth sweet-spot score or label: they are judged on water features.
SPECIES_TYPE = {**{f"DE{i:02d}": "demersal" for i in range(1, 11)}, **{f"PE{i:02d}": "pelagic" for i in range(1, 11)}}
PELAGIC_NOTE = "pelagic: judged on water features (colour lines, temperature breaks, upwellings, eddies), not depth"
# FINAL table depth text for pelagics, kept for reference only - NEVER used for scoring or labels
PELAGIC_DEPTH_INFO = {"PE01": ((0, 70), (0, 70)), "PE02": ((0, 30), (0, 30)), "PE03": ((0, 25), (0, 25)), "PE04": ((0, 30), (0, 30)), "PE05": ((0, 150), (0, 150)), "PE06": ((0, 50), (0, 50)), "PE07": ((0, 20), (0, 150)), "PE08": ((0, 50), (0, 50)), "PE09": ((0, 150), (0, 150)), "PE10": ((0, 80), (0, 80))}
SHARK_NOTE = "deeper than the sweet spot: long way up, higher shark risk (Mick)"


def msl_to_lat(msl_m):
    """Convert MSL depth (negative = below surface) to LAT depth (positive = below LAT datum), rounded to 0.5 m."""
    if msl_m is None or not np.isfinite(msl_m):
        return None
    return rhalf(-msl_m - MSL_ABOVE_LAT)


def lat_to_msl(lat_m):
    """Convert LAT depth (positive = below LAT datum) to MSL depth (negative = below surface)."""
    if lat_m is None:
        return None
    return -(lat_m + MSL_ABOVE_LAT)


def is_deep(depth_lat):
    return depth_lat is not None and DEEP_LAT_M < depth_lat <= CUTOFF_LAT_M


def depth_label(depth_lat):
    if depth_lat is None:
        return ""
    if depth_lat > CUTOFF_LAT_M:
        return "too deep (over 150 m LAT, dropped)"
    return "deep (120-150 m LAT)" if depth_lat > DEEP_LAT_M else ""
MANIFEST = f"{PL}/engine_sources_2026-11-17.json"  # 17 Nov 2026: + seabed_hardness evidence + INPUT 12 labels; 12 Nov file kept
POINTS_CANONICAL = f"{W}/rodney_root_index/filtered_150m/RODNEY_points max150mLAT 2026-11-21.csv.gz"  # 21 Nov 7:26 pm: 150 m table (60,847 rows); 120 m copy kept: max120mLAT 2026-11-12
POINTS_HD8CHECK = f"{W}/rodney_root_index/RODNEY_points max120mLAT hd8check 2026-11-12.csv.gz"
POINTS_ENGINE = f"{W}/rodney_root_index/filtered_150m/RODNEY_points max150mLAT hd8check G3 2026-11-21.csv.gz"  # 21 Nov 7:26 pm: G1 + G3, 150 m (60,815 rows); 120 m copy kept: hd8check G3-corrected 2026-11-14
PROFILES_PY = f"{W}/engine_test_2026-11-12_arlington_rerun/profiles.py"
REEF_NAMES = f"{W}/library-sorted/07 Research & Science/JSON & GeoJSON/gbr_features_box.geojson"
BNE = dt.timezone(dt.timedelta(hours=10), "AEST")
MICK_MARK_DS = r"PRIVATE_MASTER|Master Marks|REAL_marks|Shared Ranked Marks"
WONKY_ALERT = ("DEPRESSION, not a structure. Look for a dip on the sounder, not a lump. Make several slow, precise passes; "
               "it's easy to miss and think there's nothing here.")
CARD = "N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW".split()
card = lambda d: CARD[int(round((d % 360) / 22.5)) % 16]
rhalf = lambda x: round(x * 2) / 2

# Fisheries Queensland limits (tidal), page updated 25 Sep 2026, read 10 Nov 2026 (old engine_test FQ table)
FQ = {"DE01": (38, 7), "DE03": (55, 5), "DE07": (38, 8), "DE05": (40, 9), "DE04": (40, 9), "DE10": (35, 5), "PE01": (75, 1)}
# Closures: read from the team's live closures feed (RAG dynamic/freshness.py -> closures cache refreshed from the DAF Qld
# tidal closures page), never hard-coded (Mick 21 Nov 2026 6:25 pm). If the feed cache is older than its max age or the page
# differs, CLOSURES_STATUS carries a dated warning; the dates still come from that dated cache.
BUFFER_RULE = "Buffer zone: troll only for pelagics"
RUBBLE_SHALLOW_CUTOFF = 25.0
RUBBLE_RULES = {
    "DE03": (25, 100),  # red emperor on rubble: 25-100 m (core 30-60 m)
    "DE04": (30, 150),  # nannygai on rubble: 30-100 m+ (capped at 150 m LAT limit)
    "DE06": None,       # redthroat emperor: do not run on rubble until a range is set
}
RUBBLE_REEF_FLAT_ZONES = {"Inner Reef Flat", "Outer Reef Flat", "Reef Crest", "Shallow Lagoon"}
# Feeding triggers (XB3, 12 Nov 2026): species-specific bite-window modifiers.
# Keys = species_id, values = dict with optional tide_phase, moon_phase, pressure, temp_range, bait conditions.
# Loaded from RAG at init when available; empty dict = no trigger data yet.
FEEDING_TRIGGERS_PATH = f"{W}/shared_refs/RAG/sources/extracted_2026-11-14/species_feeding_triggers.csv"
OCEAN_GRID_PATH = f"{W}/reef-app/feeds/cache/ocean_grids/ocean_layers_grid.json"
OCEAN_FRONTS_PATH = f"{W}/reef-app/feeds/cache/ocean_grids/ocean_fronts.geojson"


def load_closures():
    """-> ({species_id: [(start, end), ...]}, status dict). Source: RAG dynamic_sources.json 'closures' cache (live feed)."""
    ds_dir = f"{W}/shared_refs/RAG/dynamic"
    try:
        src = next(x for x in json.load(open(f"{ds_dir}/dynamic_sources.json"))["sources"] if x["id"] == "closures")
        cpath = src["cache"]
        if cpath.startswith("rodney_system/"): cpath = _rp(cpath) if "_rp" in globals() else cpath
        elif not cpath.startswith("/"): cpath = f"{W}/{cpath}"
        c = json.load(open(cpath))
        out = {}
        for sid in c.get("crff_species", []): out[sid] = [tuple(w) for w in c["coral_reef_fin_fish"]]
        for sid in c.get("spanish_species", []): out[sid] = [tuple(w) for w in c["spanish_mackerel_north"]]
        lc = dt.datetime.fromisoformat(c["last_checked"]); age_h = (dt.datetime.now(BNE) - lc).total_seconds() / 3600
        stale = age_h > float(src.get("max_age_hours", 168)) or bool(c.get("page_differs"))
        st = dict(source=cpath, feed_url=c.get("url"), last_checked=c["last_checked"], page_last_updated=c.get("page_last_updated"),
                  cache_age_h=round(age_h, 1), status="STALE" if stale else "OK", saved_on=c["last_checked"][:10],
                  # Mick 21 Nov 2026 7:37 pm: "Show seasonal CLOSED labels from a saved copy with the date it was saved and a
                  # 'may be out of date' warning until the live feed works." The DAF page blocks scripts (403), so this is always shown.
                  saved_copy_note=f"from a saved copy of the Qld closures page, saved {c['last_checked'][:10]} - may be out of date",
                  warning=(f"WARNING: closure dates from a saved copy saved {c['last_checked'][:10]} - may be out of date"
                           + (f" (older than {src.get('max_age_hours', 168)} h or page differs)" if stale else "") + " - check the DAF closures page"))
        return out, st
    except Exception as e:
        return {}, dict(source=None, status="MISSING", warning=f"WARNING: closures feed not readable ({str(e)[:120]}) - closures UNKNOWN, check the DAF closures page")


CLOSURES, CLOSURES_STATUS = load_closures()

# feature_type / dataset -> (bottom set, zone set, short label)
FT = {
    "lump_pinnacle": ({"hard", "coral"}, {"bommie"}, "scan lump/pinnacle"),
    "Pinnacle": ({"hard"}, {"bommie"}, "pinnacle"), "pinnacle": ({"hard"}, {"bommie"}, "pinnacle"),
    "bommie/patch reef": ({"coral", "hard"}, {"bommie"}, "bommie/patch reef"), "bommie/small reef": ({"coral", "hard"}, {"bommie"}, "bommie/patch reef"),
    "isolated bommie (GBR30)": ({"coral", "hard"}, {"bommie"}, "GBR30 terrain candidate (bommie)"),
    "isolated bommie candidate": ({"coral", "hard"}, {"bommie"}, "GBR30 terrain candidate (bommie)"),
    "ledge_dropoff": ({"hard"}, {"slope"}, "scan ledge/drop-off"), "Escarpment": ({"hard"}, {"slope"}, "escarpment"),
    "reef base / deep slope": ({"hard", "rubble"}, {"slope", "backreef"}, "reef base / deep slope"),
    "reef slope/edge": ({"coral", "hard"}, {"slope", "front"}, "reef slope/edge"),
    "shelf edge (deep hard ground)": ({"hard"}, {"outer", "slope"}, "shelf edge (deep hard ground)"),
    "rubble patch": ({"rubble"}, {"interreef"}, "rubble patch"), "inter-reef hard/rough ground": ({"rubble", "hard"}, {"interreef"}, "inter-reef hard ground"),
    "wonky hole candidate": ({"rubble", "sponge"}, {"interreef"}, "Wonky hole target"), "wonky hole": ({"rubble", "sponge"}, {"interreef"}, "Wonky hole target"),
    "WRECKS": ({"wreck", "hard"}, {"interreef"}, "wreck"), "OBSTRN": ({"wreck", "hard"}, {"interreef"}, "obstruction"),
    "inter-reef plain, flat": ({"sand"}, {"interreef", "lagoon"}, "inter-reef sand plain"),
    "Ridge": ({"hard"}, {"interreef", "slope"}, "ridge"), "Bank": ({"hard", "sand"}, {"interreef"}, "bank"), "Platform": ({"hard"}, {"interreef"}, "platform"),
    "reef scan mark": ({"hard"}, {"slope", "bommie"}, "reef scan mark"),
    "Surface FAD": (set(), {"front", "outer"}, "FAD"), "All-water FAD (submerged buoy)": (set(), {"front", "outer"}, "FAD"),
    "current_point": (set(), {"front"}, "current point"), "front": (set(), {"front"}, "front"), "shelf_break": ({"hard"}, {"outer", "front"}, "shelf break"),
}
HAB_DS = {"coral_trout_preferred_habitat_2026-10-31.csv": ("DE01", "DE02"), "red_emperor_preferred_habitat_2026-10-31.csv": ("DE03",),
          "nannygai_preferred_habitat_2026-10-31.csv": ("DE04", "DE05"), "red_throat_emperor_preferred_habitat_2026-10-31.csv": ("DE07",),
          "spanish_mackerel_preferred_habitat_2026-10-31.csv": ("PE01",)}
# bite hours (AEST) used when no live tide is supplied (old engine_test windows; field rule, unsourced weight)
DEFAULT_HOURS = {"DEMERSAL": [5, 6, 7, 8, 9, 10, 11, 16, 17, 18], "PELAGIC": [5, 6, 7, 16, 17, 18]}
NIGHT_SPECIES = {"DE03", "DE04", "DE05", "DE08"}


def parse_band(txt):
    """'10-140 m (commonly 25-80 m)' -> ext (10,140), core (25,80). Capped at 150 m LAT."""
    nums = [tuple(map(float, m)) for m in re.findall(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", str(txt))]
    m2 = re.search(r"[Ss]urface to (\d+)", str(txt))
    ext = nums[0] if nums else ((0.0, float(m2.group(1))) if m2 else None)
    core = nums[1] if len(nums) > 1 else ext
    cap = lambda b: (min(b[0], CUTOFF_LAT_M), min(b[1], CUTOFF_LAT_M)) if b else None
    return cap(core), cap(ext), (ext is not None and ext[1] > CUTOFF_LAT_M)


def load_species():
    """20 FINAL species: v5 tables (names, limits, depth text) + 12 Nov profiles (bands, bottoms, zones, season factor)."""
    import pandas as pd
    spec = importlib.util.spec_from_file_location("profiles", PROFILES_PY); prof = importlib.util.module_from_spec(spec); spec.loader.exec_module(prof)
    out = {}
    for f in (f"{W}/marine_db_v5/13_Species/species_reef_demersal_v5.csv", f"{W}/marine_db_v5/14_Pelagic/species_pelagic_v5.csv"):
        for r in pd.read_csv(f).to_dict("records"):
            sid = r["species_id"]; p = prof.P[sid]
            v5core, v5ext, v5deep = parse_band(r["depth_range"])
            if sid in SWEET:  # 21 Nov: sweet spot = core, FINAL table range = band, capped at 150 m
                core, ext = tuple(map(float, SWEET[sid][0])), tuple(map(float, SWEET[sid][1]))
            else:
                core = (min(p["core"][0], CUTOFF_LAT_M), min(p["core"][1], CUTOFF_LAT_M))
                ext = (min(p["ext"][0], CUTOFF_LAT_M), min(p["ext"][1], CUTOFF_LAT_M))
            out[sid] = dict(id=sid, group=p["g"], name=p["n"], v5_name=r["common_name"], sci=r["scientific_name"], core=core, ext=ext,
                            capped=(p["ext"][1] > CUTOFF_LAT_M or v5deep), v5_depth=r["depth_range"], bottom=p["bottom"], zones=p["zones"],
                            season=p["season"], season_txt=p["season_txt"], sand_ok=p.get("sand_ok", False), zone_note=p.get("zone_note"),
                            needs=p.get("needs", []), notake_species=p.get("notake", []), size=r["size_limit_qld"], possession=r["possession_limit_qld"],
                            closures_txt=r["closures_qld"], substrate=r["substrate_structure"], habitat=r["preferred_habitat"], source_file=f)
    return out


def closed_label(cl):
    """Seasonal CLOSED label with the saved-copy date and 'may be out of date' warning (dates from the feed cache, never literals)."""
    return f"CLOSED {cl[0]} to {cl[1]} (seasonal closure, {CLOSURES_STATUS.get('saved_copy_note') or 'closures feed not readable'})"


def closed_on(sid, day):
    for a, b in CLOSURES.get(sid, []):
        if a <= day <= b:
            return (a, b)
    return None


def load_manifest(path=MANIFEST):
    class EngineSourceMissing(RuntimeError):
        pass
    if not os.path.exists(path):
        raise FileNotFoundError(f"manifest not found: {path}")
    m = json.load(open(path)); bad = []
    for role, entries in m["roles"].items():
        for key, e in entries.items():
            if "box_path" not in e:  # note-only entry (e.g. other_pelagics removed 12 Nov), not a file
                e["available"] = None; e["note_only"] = True; continue
            p = e.get("box_path"); e["available"] = bool(p) and os.path.exists(p)
            if e.get("required", True) and not e["available"]:
                bad.append(f"{role}/{key}: {p or '(no file listed)'}")
    if bad:
        raise FileNotFoundError("chosen engine source(s) missing: " + "; ".join(bad))
    return m


def make_current(T):
    """Port of reef_current_lookup.js (RECOM harmonics)."""
    g = T["grid"]; cons = T["constituents"]; om = T["omega_deg_per_hour"]; Wt = T["water"]
    C = {q: {k: np.asarray(T["cells"][q][k], float) for k in ("u_re", "u_im", "v_re", "v_im")} for q in cons}
    def cell(k, dk, minute):
        if not Wt[k]:
            return None
        row = T["nodal_daily"]["table"].get(dk)
        if row is None:
            return None
        u = v = 0.0
        for qi, q in enumerate(cons):
            f = row[qi][0]; ph = math.radians(row[qi][1] + om[qi] * minute / 60); cs, sn = math.cos(ph), math.sin(ph); c = C[q]
            u += f * (c["u_re"][k] * cs - c["u_im"][k] * sn); v += f * (c["v_re"][k] * cs - c["v_im"][k] * sn)
        return u, v
    def at(lon, lat, dk, minute):
        fi = (g["lat_n"] - lat) / g["d"]; fj = (lon - g["lon_w"]) / g["d"]
        if fi < 0 or fj < 0 or fi > g["ny"] - 1 or fj > g["nx"] - 1:
            return None
        i0 = min(int(fi), g["ny"] - 2); j0 = min(int(fj), g["nx"] - 2); di = fi - i0; dj = fj - j0
        u = v = w = 0.0
        for ii, jj, ww in ((i0, j0, (1 - di) * (1 - dj)), (i0 + 1, j0, di * (1 - dj)), (i0, j0 + 1, (1 - di) * dj), (i0 + 1, j0 + 1, di * dj)):
            r = cell(ii * g["nx"] + jj, dk, minute)
            if r and ww > 0:
                u += r[0] * ww; v += r[1] * ww; w += ww
        if w < 0.25:
            return None
        u /= w; v /= w
        return {"kn": math.hypot(u, v) / 1000 * 1.943844, "dir_to": (math.degrees(math.atan2(u, v)) + 360) % 360}
    return at


class Engine:
    def __init__(self, manifest=MANIFEST, points=POINTS_ENGINE):
        import rasterio, pyogrio, pandas as pd
        from pyproj import Transformer
        from shapely.ops import unary_union
        from shapely.prepared import prep
        from shapely import STRtree
        self.m = load_manifest(manifest); self.manifest_path = manifest
        R = lambda role, key: self.m["roles"][role][key]["box_path"]
        self.used = []
        def use(p):
            if p and p not in self.used: self.used.append(p)
        self.use = use
        self.tr = Transformer.from_crs(4326, 32755, always_xy=True); self.back = Transformer.from_crs(32755, 4326, always_xy=True)
        self.r_depth = rasterio.open(R("depth", "depth_msl")); self.r_flag = rasterio.open(R("depth", "depth_measured_flag"))
        self.r_g30 = rasterio.open(R("depth", "gbr30_fallback")); self.r_zone = rasterio.open(R("habitat", "habitat_reef_zones"))
        for k in (("depth", "depth_msl"), ("depth", "depth_measured_flag"), ("depth", "gbr30_fallback"), ("habitat", "habitat_reef_zones")): use(R(*k))
        self.species = load_species(); use(f"{W}/marine_db_v5/13_Species/species_reef_demersal_v5.csv"); use(f"{W}/marine_db_v5/14_Pelagic/species_pelagic_v5.csv"); use(PROFILES_PY)
        self.feeding_triggers = self._load_feeding_triggers()
        self.ocean = self._load_ocean_layers()
        self.cur = make_current(json.load(open(R("current", "current_harmonics")))); use(R("current", "current_harmonics"))
        PP = json.load(open(R("current", "pressure_points"))); use(R("current", "pressure_points"))
        self.pp = []
        for f in PP["features"]:
            d = f["properties"].get("depth_lat_m")
            if d is not None and float(d) > CUTOFF_LAT_M:
                continue  # 150 m rule at load
            lo, la = f["geometry"]["coordinates"][:2]
            self.pp.append(dict(lat=la, lon=lo, xy=self.tr.transform(lo, la), props=f["properties"], days=json.loads(f["properties"]["days"])))
        Z = pyogrio.read_dataframe(R("zoning", "zoning"), layer="GBRMPA_GBRMP_Zoning_full_res_nd_2026"); use(R("zoning", "zoning"))
        nt = Z[Z.TYPE.str.startswith(("Marine National Park", "Preservation", "Scientific Research"))]  # Buffer shown, troll only (Mick 21 Nov)
        geoms = list(nt.geometry.buffer(300)) + list(Z[Z.TYPE.str.startswith("Commonwealth Islands")].geometry)
        for key in ("no_take_gbrmpa", "no_take_qld_state"):
            g = pyogrio.read_dataframe(R("zoning", key)).to_crs(32755); geoms += list(g.geometry); use(R("zoning", key))
        self.n_notake_polys = len(nt)
        bz = list(Z[Z.TYPE.str.startswith("Buffer")].geometry)
        bfe = self.m["roles"]["zoning"].get("buffer_troll_only", {})
        if bfe.get("box_path") and os.path.exists(_rp(bfe["box_path"]) if "_rp" in globals() else bfe["box_path"]):
            bp = _rp(bfe["box_path"]) if "_rp" in globals() else bfe["box_path"]
            bz += list(pyogrio.read_dataframe(bp).to_crs(32755).geometry); use(bp)
        self.n_buffer_polys = len(bz)
        self.buffer = prep(unary_union(bz)) if bz else None
        self.notake = prep(unary_union(geoms))
        names = pyogrio.read_dataframe(REEF_NAMES).to_crs(32755); names = names[names.FEAT_NAME.isin(["Reef", "Cay", "Rock"])].reset_index(drop=True)
        names["NAME"] = [l if not str(g).startswith("U/N") else "unnamed reef " + str(l).split("(")[-1].rstrip(")") for g, l in zip(names.GBR_NAME, names.LOC_NAME_S)]
        self.names = names; self.name_tree = STRtree(list(names.geometry))
        self.points_path = points
        P = pd.read_csv(points, low_memory=False); use(points)
        n0 = len(P)
        d_own = pd.to_numeric(P.depth_LAT_m, errors="coerce"); d_hd8 = pd.to_numeric(P.get("hd8_depth_LAT_m"), errors="coerce") if "hd8_depth_LAT_m" in P else d_own * np.nan
        P = P[~((d_own > CUTOFF_LAT_M) | (d_hd8 > CUTOFF_LAT_M))].copy()  # 150 m rule at load (own + HD8)
        self.points_dropped_120 = self.points_dropped_150 = n0 - len(P)
        P["is_mark"] = P.dataset.astype(str).str.contains(MICK_MARK_DS, regex=True) & (P.source_tag == "Mick mark")
        self.P = P
        xs, ys = self.tr.transform(P.lon.values, P.lat.values); self.P["x"] = xs; self.P["y"] = ys
        from scipy.spatial import cKDTree
        self.ptree = cKDTree(np.c_[xs, ys])
        self.held = []  # held-but-unused (G12)
        self.last_area = None; self.last_answer = None  # per-answer held-but-unused (G12, Mick 21 Nov 2026 6:37 pm)
        for role, v in self.m["roles"].items():
            for key, e in v.items():
                p = e.get("box_path")
                if e.get("note_only"):
                    self.held.append(dict(role=role, key=key, path=None, reason="note only: " + str(e.get("reason") or e.get("source")))); continue
                if p and p not in self.used:
                    why = "full original kept, not engine-facing (120 m cut copy used instead)" if "full_original" in key else \
                          ("not available on box" if not e.get("available") else "listed in manifest, not used by point-first scoring (map/RAG layer)")
                    self.held.append(dict(role=role, key=key, path=p, reason=why))
                elif not p:
                    self.held.append(dict(role=role, key=key, path=None, reason="no file listed (not built yet)"))

    # ---------- helpers
    def place(self, x, y):
        from shapely.geometry import Point
        p = Point(x, y); i = self.name_tree.nearest(p); g = self.names.geometry[i]; c = g.centroid; d = g.distance(p)
        brg = (math.degrees(math.atan2(x - c.x, y - c.y)) + 360) % 360
        return (f"{card(brg)} side of {self.names.NAME[i]}" if d < 1500 else f"{d/1000:.1f} km {card(brg)} of {self.names.NAME[i]}")

    def reef_outline(self, name):
        x = self.names[self.names.GBR_NAME.str.contains(name, case=False, na=False)]
        return x.geometry.iloc[0] if len(x) else None

    def is_notake(self, x, y):
        from shapely.geometry import Point
        return self.notake.contains(Point(x, y))

    def depth_at(self, x, y):
        """HD8 cut copy (nearest 10 m cell, unsmoothed), then GBR30 cut (estimated). None if no value or deeper than 150 m LAT."""
        def samp(r):
            b = r.bounds
            if not (b.left <= x <= b.right and b.bottom <= y <= b.top): return None
            v = float(list(r.sample([(x, y)]))[0][0]); nd = r.nodata
            if not np.isfinite(v) or (nd is not None and v == nd): return None
            return v
        z = samp(self.r_depth)
        if z is not None:
            if z < CUTOFF_MSL_M:
                return None, None, None  # deeper than 150 m LAT
            fl = samp(self.r_flag)
            return msl_to_lat(z), ("surveyed" if fl == 1 else "estimated"), "HD8 10 m (120 m cut)"
        z = samp(self.r_g30)
        if z is not None and z < 0:
            if z < CUTOFF_MSL_M:
                return None, None, None
            return msl_to_lat(z), "estimated", "GBR30 30 m (120 m cut, fallback)"
        return None, None, None

    GEO = {2: "Deep", 11: "Shallow Lagoon", 12: "Deep Lagoon", 13: "Inner Reef Flat", 14: "Outer Reef Flat", 15: "Reef Crest",
           21: "Sheltered Reef Slope", 22: "Reef Slope", 23: "Plateau", 24: "Back Reef Slope", 25: "Patch Reef"}

    def zone_at(self, x, y):
        b = self.r_zone.bounds
        if not (b.left <= x <= b.right and b.bottom <= y <= b.top): return None
        return self.GEO.get(int(list(self.r_zone.sample([(x, y)]))[0][0]))

    def cur_window(self, lon, lat, day, hours):
        best = None
        for h in hours:
            c = self.cur(lon, lat, day, h * 60)
            if c and (best is None or c["kn"] > best[0]["kn"]):
                best = (c, h)
        return best

    # ---------- candidates (point data first)
    def candidates(self, area_geom=None, center=None, radius_m=4000, dedupe_m=40):
        """Point-table candidates (model / structure / habitat points; Mick's marks are evidence, not positions) + pressure points.
        Area = outline buffered by radius_m, or a circle around center (lat, lon)."""
        from shapely.geometry import Point
        if area_geom is not None:
            A = area_geom.buffer(radius_m)
        else:
            cx, cy = self.tr.transform(center[1], center[0]); A = Point(cx, cy).buffer(radius_m)
        x0, y0, x1, y1 = A.bounds
        P = self.P[(self.P.x >= x0) & (self.P.x <= x1) & (self.P.y >= y0) & (self.P.y <= y1)]
        from shapely.prepared import prep
        Ap = prep(A)
        C, seen, stats = [], set(), dict(blank_notake=0, deeper_or_no_depth=0, dries=0)
        for r in P.itertuples():
            if r.is_mark or r.dataset in ("aho_enc_soundings.csv", "ramp_to_public_reefs_distance_bearing.csv"):
                continue
            ft = FT.get(r.feature_type)
            hab = HAB_DS.get(r.dataset)
            if not ft and not hab and r.dataset != "BRUVS_Cairns_drops_enriched_v2_2026-10-31.csv":
                continue
            if not Ap.contains(Point(r.x, r.y)):
                continue
            k = (round(r.x / dedupe_m), round(r.y / dedupe_m), r.feature_type)
            if k in seen: continue
            seen.add(k)
            C.append(dict(kind="point", x=r.x, y=r.y, lat=r.lat, lon=r.lon, feature=r.feature_type, dataset=r.dataset,
                          label=(ft[2] if ft else ("habitat point" if hab else "BRUVS drop site")), bottom=(ft[0] if ft else set()), zones=(ft[1] if ft else set()),
                          hab_species=hab or (), species_txt=str(r.species), own_depth=r.depth_LAT_m, source_tag=r.source_tag))
        for p in self.pp:
            if Ap.contains(Point(*p["xy"])):
                C.append(dict(kind="pressure_point", x=p["xy"][0], y=p["xy"][1], lat=p["lat"], lon=p["lon"], feature="pressure point", dataset="RECOM pressure points (120 m)",
                              label=f"pressure point {p['props']['id']} ({p['props']['phase']})", bottom={"hard"}, zones={"front", "slope"}, hab_species=(), species_txt=str(p["props"].get("species")),
                              own_depth=p["props"].get("depth_lat_m"), pp=p, source_tag="public model"))
        out = []
        for c in C:
            if self.is_notake(c["x"], c["y"]):
                stats["blank_notake"] += 1; continue
            if self.buffer is not None and self.buffer.contains(Point(c["x"], c["y"])):
                c["zone_rule"] = BUFFER_RULE; stats["buffer_troll_only"] = stats.get("buffer_troll_only", 0) + 1
            od = c["own_depth"]
            try: od = float(od)
            except (TypeError, ValueError): od = None
            if od is not None and np.isfinite(od):
                dl, tag, src = rhalf(od), "own depth", "point's own LAT depth"
            else:
                dl, tag, src = self.depth_at(c["x"], c["y"])
            if dl is None or dl > CUTOFF_LAT_M:
                stats["deeper_or_no_depth"] += 1; continue
            if dl <= 0:
                stats["dries"] += 1; continue
            c.update(depth_lat_m=dl, depth_tag=tag, depth_src=src, deep=is_deep(dl), depth_label=depth_label(dl))
            out.append(c)
        stats["legal_candidates"] = len(out)
        # G12: remember what data the engine holds inside this answer area, so the answer can list what it held but didn't use
        try:
            from shapely import contains_xy
            inA = P[contains_xy(A, P.x.values, P.y.values)]
        except Exception:
            inA = P
        ds_counts = {str(k): int(v) for k, v in inA.dataset.astype(str).value_counts().items()}
        n_pp = sum(1 for c in C if c["kind"] == "pressure_point")
        if n_pp: ds_counts["RECOM pressure points (120 m)"] = n_pp
        self.last_area = dict(datasets=ds_counts, cand_datasets=sorted({c["dataset"] for c in C}),
                              legal_datasets=sorted({c["dataset"] for c in out}), stats=dict(stats))
        return out, stats, A

    @staticmethod
    def _load_feeding_triggers():
        """Load species feeding triggers (tide phase, moon, pressure, temp, bait) from RAG extract. Returns {species_id: {...}} or {}."""
        import pandas as pd
        try:
            if not os.path.exists(FEEDING_TRIGGERS_PATH):
                return {}
            df = pd.read_csv(FEEDING_TRIGGERS_PATH)
            triggers = {}
            for _, r in df.iterrows():
                sid = r.get("species_id")
                if not sid:
                    continue
                triggers[sid] = {k: r[k] for k in df.columns if k != "species_id" and pd.notna(r[k])}
            return triggers
        except Exception:
            return {}

    def _tide_phase_at(self, lon, lat, day, hour):
        """Determine tide phase at a location/time by comparing RECOM current speed at adjacent hours.
        Returns 'run-in' (increasing), 'run-out' (decreasing), 'change' (at min/max), or None."""
        prev_h = (hour - 1) % 24
        next_h = (hour + 1) % 24
        c_now = self.cur(lon, lat, day, hour * 60)
        c_prev = self.cur(lon, lat, day, prev_h * 60)
        c_next = self.cur(lon, lat, day, next_h * 60)
        if not c_now:
            return None
        kn_now = c_now["kn"]
        kn_prev = c_prev["kn"] if c_prev else kn_now
        kn_next = c_next["kn"] if c_next else kn_now
        if kn_now >= kn_prev and kn_now >= kn_next:
            return "change"
        if kn_now <= kn_prev and kn_now <= kn_next:
            return "change"
        if kn_now > kn_prev:
            return "run-in"
        return "run-out"

    @staticmethod
    def _moon_phase(day):
        """Approximate moon phase from date string 'YYYY-MM-DD'. Returns one of: new, waxing_crescent,
        first_quarter, waxing_gibbous, full, waning_gibbous, last_quarter, waning_crescent."""
        d = dt.date.fromisoformat(str(day))
        ref = dt.date(2000, 1, 6)  # known new moon
        days_since = (d - ref).days
        cycle = days_since % 29.53059
        if cycle < 1.85: return "new"
        if cycle < 7.38: return "waxing_crescent"
        if cycle < 9.23: return "first_quarter"
        if cycle < 14.77: return "waxing_gibbous"
        if cycle < 16.61: return "full"
        if cycle < 22.15: return "waning_gibbous"
        if cycle < 24.0: return "last_quarter"
        return "waning_crescent"

    def feeding_bonus(self, sp, c, day, hour):
        """Score bonus from species feeding triggers (tide change, moon phase, pressure, temperature). Returns (bonus, reasons)."""
        ft = self.feeding_triggers.get(sp["id"])
        if not ft:
            return 0.0, []
        bonus, why = 0.0, []
        tide_phase = ft.get("tide_phase")
        if tide_phase and hour is not None:
            actual_phase = self._tide_phase_at(c["lon"], c["lat"], day, hour)
            if actual_phase:
                wanted = [p.strip().lower() for p in str(tide_phase).split(",")]
                if actual_phase in wanted:
                    bonus += 0.1
                    why.append(f"feeding trigger: tide {actual_phase} matches {sp['name']} preference")
        moon = ft.get("moon_phase")
        if moon:
            actual_moon = self._moon_phase(day)
            wanted_moon = [p.strip().lower().replace(" ", "_") for p in str(moon).split(",")]
            if actual_moon in wanted_moon:
                bonus += 0.1
                why.append(f"feeding trigger: moon {actual_moon.replace('_', ' ')} matches {sp['name']} preference")
        return bonus, why

    @staticmethod
    def _load_ocean_layers():
        """Load ocean grid (SST, chlorophyll, upwelling proxy, fronts) for pelagic scoring. Returns dict or {}."""
        out = {}
        try:
            if os.path.exists(OCEAN_GRID_PATH):
                og = json.load(open(OCEAN_GRID_PATH))
                out["grid"] = og
                out["built_at"] = og.get("built_at")
                out["sst"] = og.get("ocean_sst", {})
                out["sst_anom"] = og.get("ocean_sst_anom_clim", {})
                out["sst_front_grad"] = og.get("ocean_sst_front_grad", {})
                out["chl"] = og.get("ocean_chl", {})
                out["chl_edge"] = og.get("ocean_chl_edge_grad", {})
                out["upwelling"] = og.get("ocean_upwelling_proxy", {})
        except Exception:
            pass
        try:
            if os.path.exists(OCEAN_FRONTS_PATH):
                out["fronts"] = json.load(open(OCEAN_FRONTS_PATH))
        except Exception:
            pass
        return out

    def ocean_score(self, lon, lat):
        """Score pelagic water features at a point. Returns (bonus, reasons).
        Uses SST gradients (temperature breaks), chlorophyll edges (colour lines), and upwelling proxy."""
        if not self.ocean:
            return 0.0, ["ocean layers not loaded"]
        bonus, why = 0.0, []
        grid = self.ocean.get("grid", {})
        bbox = grid.get("bbox")
        if not bbox:
            return 0.0, ["ocean grid has no bbox"]
        res = grid.get("resolution_deg", 0.01)
        if not (bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]):
            return 0.0, ["outside ocean grid coverage"]
        col = int((lon - bbox[0]) / res)
        row = int((bbox[3] - lat) / res)
        nx = grid.get("nx", int((bbox[2] - bbox[0]) / res) + 1)

        def val(layer_key):
            layer = self.ocean.get(layer_key, {})
            data = layer.get("data") or layer.get("values")
            if not data:
                return None
            idx = row * nx + col
            if 0 <= idx < len(data):
                v = data[idx]
                return v if v is not None and np.isfinite(v) else None
            return None

        sst_grad = val("sst_front_grad")
        if sst_grad is not None:
            if sst_grad > 0.5:
                bonus += 0.2
                why.append(f"strong SST break ({sst_grad:.2f} C/km) - temperature front")
            elif sst_grad > 0.2:
                bonus += 0.1
                why.append(f"moderate SST gradient ({sst_grad:.2f} C/km)")

        chl_edge = val("chl_edge")
        if chl_edge is not None:
            if chl_edge > 0.3:
                bonus += 0.2
                why.append(f"strong colour line ({chl_edge:.2f} chl gradient) - blue/green edge")
            elif chl_edge > 0.1:
                bonus += 0.1
                why.append(f"moderate chlorophyll edge ({chl_edge:.2f})")

        upwell = val("upwelling")
        if upwell is not None:
            if upwell > 0.5:
                bonus += 0.15
                why.append(f"upwelling signal ({upwell:.2f}) - cold nutrient-rich water")
            elif upwell > 0.2:
                bonus += 0.05
                why.append(f"weak upwelling signal ({upwell:.2f})")

        sst = val("sst")
        if sst is not None:
            why.append(f"SST {sst:.1f} C")

        if self.ocean.get("built_at"):
            why.append(f"ocean data: {self.ocean['built_at']}")
        elif not why:
            why.append("ocean layer data not available at this location")

        return round(bonus, 3), why

    def _current_at(self, sp, c, day, hours=None, current_override=None):
        """Shared: resolve RECOM current for a candidate. Returns (current_window, current_kn, current_factor, reasons)."""
        lon, lat = c["lon"], c["lat"]
        if current_override is not None:
            cw = current_override
        else:
            hrs = hours or (([4, 5, 6, 18, 19, 20, 21]) if sp["id"] in NIGHT_SPECIES else DEFAULT_HOURS[sp["group"]])
            key = (round(lon / 0.005), round(lat / 0.005), day, tuple(hrs))
            if not hasattr(self, "_cw"): self._cw = {}
            if key not in self._cw: self._cw[key] = self.cur_window(lon, lat, day, hrs)
            cw = self._cw[key]
        ckn = cw[0]["kn"] if cw else 0.0
        cf = 0.6 + 0.4 * min(ckn / 0.4, 1)
        why = []
        if cw: why.append(f"tide run {ckn:.2f} kn toward {card(cw[0]['dir_to'])} at {cw[1]:02d}:00 (RECOM model)")
        return cw, ckn, cf, why

    def score_demersal(self, sp, c, day, hours=None, current_override=None):
        """Demersal engine: depth sweet spot first, then structure, current and season."""
        core, ext = sp["core"], sp["ext"]; dl = c["depth_lat_m"]
        if dl > CUTOFF_LAT_M:
            return 0.0, ["deeper than 150 m LAT - dropped"], {}
        sweet = core[0] <= dl <= core[1]
        df = 1.0 if sweet else (0.5 if ext[0] <= dl <= ext[1] else 0.0)
        if df == 0:
            return 0.0, [f"{dl} m LAT outside {sp['name']} band {ext[0]:g}-{ext[1]:g} m"], {}
        why = [f"{dl} m LAT ({c['depth_tag']}) " + (f"in the sweet spot {core[0]:g}-{core[1]:g} m" if sweet else
               f"OUTSIDE the sweet spot {core[0]:g}-{core[1]:g} m (band {ext[0]:g}-{ext[1]:g} m)" + (f" - {SHARK_NOTE}" if (sp["id"] == "DE03" and dl > core[1]) else ""))]
        if is_deep(dl):
            why.append("DEEP: 120-150 m LAT")
        if c.get("zone_rule") == BUFFER_RULE:
            return 0.0, [f"{BUFFER_RULE} - no bottom fishing for {sp['name']}"], {}
        # rubble search rule
        if "rubble" in c["bottom"]:
            geo = self.zone_at(c["x"], c["y"])
            if geo in RUBBLE_REEF_FLAT_ZONES and dl < RUBBLE_SHALLOW_CUTOFF:
                return 0.0, [f"shallow reef-flat rubble dropped ({dl} m LAT, {geo})"], {}
            if sp["id"] in RUBBLE_RULES:
                rr = RUBBLE_RULES[sp["id"]]
                if rr is None:
                    return 0.0, [f"rubble skipped for {sp['name']} (no rubble depth range set yet)"], {}
                if not (rr[0] <= dl <= rr[1]):
                    return 0.0, [f"rubble outside {sp['name']} rubble range {rr[0]}-{rr[1]} m ({dl} m LAT)"], {}
        # structure fit
        b = (sp["bottom"] or set()) & c["bottom"]; z = sp["zones"] & c["zones"]
        sf = 1.0 if (b and z) else (0.8 if (b or z) else 0.5)
        if c["bottom"] == {"sand"} and not sp["sand_ok"]: sf = 0.4
        why.append(f"structure: {c['label']}" + (f" (matches {', '.join(sorted(b | z))})" if (b or z) else " (weak match)"))
        bonus = 0.0
        if sp["id"] in c["hab_species"]:
            bonus += 0.15; why.append("species habitat point (10-31 habitat file)")
        if sp["name"].split(" (")[0].lower() in c["species_txt"].lower():
            bonus += 0.05
        cw, ckn, cf, cw_why = self._current_at(sp, c, day, hours, current_override)
        why.extend(cw_why)
        # pressure point proximity
        if c["kind"] == "pressure_point":
            dday = c["pp"]["days"].get(day)
            if dday:
                bonus += 0.15 / max(1, dday["rank"]) ** 0.2; why.append(f"pressure point rank {dday['rank']} on {day}, peak {dday['peak_kn']} kn at {dday['peak_time_aest']}")
        else:
            if "_near" not in c: c["_near"] = min(self.pp, key=lambda q: (q["xy"][0] - c["x"]) ** 2 + (q["xy"][1] - c["y"]) ** 2) if self.pp else None
            near = c["_near"]
            if near and math.dist(near["xy"], (c["x"], c["y"])) < 1000:
                bonus += 0.1; why.append(f"within 1 km of pressure point {near['props']['id']}")
        zf = 1.0
        if sp["zones"] == {"inshore"} and c["lon"] > 145.85:
            zf = 0.5; why.append("inshore species on a mid-shelf reef (lower likelihood)")
        if sp["id"] == "DE07" and c["lon"] < 145.9:
            zf *= 0.5
        if c["label"] == "Wonky hole target":
            why.append("SKIPPER ALERT: " + WONKY_ALERT)
        fb, fw = self.feeding_bonus(sp, c, day, cw[1] if cw else None)
        bonus += fb; why.extend(fw)
        s = (df * sf * cf * zf + bonus) * sp["season"]
        cl = closed_on(sp["id"], day)
        if cl: why.append(closed_label(cl))
        return round(s, 3), why, dict(current=cw, closed=cl, sweet=sweet, species_type="demersal", deep=is_deep(dl))

    def score_pelagic(self, sp, c, day, hours=None, current_override=None):
        """Pelagic engine: judged on water features (colour lines, SST breaks, upwellings, eddies), not depth."""
        dl = c["depth_lat_m"]
        if dl > CUTOFF_LAT_M:
            return 0.0, ["deeper than 150 m LAT - dropped"], {}
        why = [f"{dl} m LAT ({c['depth_tag']}) - {PELAGIC_NOTE}"]
        if c.get("zone_rule") == BUFFER_RULE:
            why.append(BUFFER_RULE)
        # pelagic structure: fronts, outer zones, FADs, current points
        z = sp["zones"] & c["zones"]; b = set()
        sf = 1.0 if z else 0.5
        why.append(f"structure: {c['label']}" + (f" (matches {', '.join(sorted(z))})" if z else " (weak match)"))
        bonus = 0.0
        if sp["id"] in c["hab_species"]:
            bonus += 0.15; why.append("species habitat point (10-31 habitat file)")
        if sp["name"].split(" (")[0].lower() in c["species_txt"].lower():
            bonus += 0.05
        # current is key for pelagics
        cw, ckn, cf, cw_why = self._current_at(sp, c, day, hours, current_override)
        why.extend(cw_why)
        # water feature scoring: SST breaks, colour lines, upwellings
        ob, owhy = self.ocean_score(c["lon"], c["lat"])
        bonus += ob
        why.extend(owhy)
        fb, fw = self.feeding_bonus(sp, c, day, cw[1] if cw else None)
        bonus += fb; why.extend(fw)
        zf = 1.0
        s = (1.0 * sf * cf * zf + bonus) * sp["season"]
        cl = closed_on(sp["id"], day)
        if cl: why.append(closed_label(cl))
        return round(s, 3), why, dict(current=cw, closed=cl, sweet=False, species_type="pelagic", deep=is_deep(dl))

    def score_ambush(self, sp, c, day, hours=None, current_override=None):
        """Ambush Points engine: hourly tide/current on reef faces, corners, lee eddies."""
        dl = c["depth_lat_m"]
        if dl > CUTOFF_LAT_M:
            return 0.0, ["deeper than 150 m LAT - dropped"], {}
        why = [f"{dl} m LAT ({c['depth_tag']})"]
        if c.get("zone_rule") == BUFFER_RULE:
            if sp["group"] != "PELAGIC":
                return 0.0, [f"{BUFFER_RULE} - no bottom fishing for {sp['name']}"], {}
            why.append(BUFFER_RULE)
        # ambush points are all about current timing
        cw, ckn, cf, cw_why = self._current_at(sp, c, day, hours, current_override)
        why.extend(cw_why)
        # pressure point scoring is the core of the ambush engine
        bonus = 0.0
        if c["kind"] == "pressure_point":
            dday = c["pp"]["days"].get(day)
            if dday:
                bonus += 0.25 / max(1, dday["rank"]) ** 0.2
                why.append(f"AMBUSH: pressure point rank {dday['rank']} on {day}, peak {dday['peak_kn']} kn at {dday['peak_time_aest']}")
                if dday.get("phase"):
                    why.append(f"tide phase: {dday['phase']}")
            else:
                why.append("pressure point (no data for this day)")
        else:
            if "_near" not in c: c["_near"] = min(self.pp, key=lambda q: (q["xy"][0] - c["x"]) ** 2 + (q["xy"][1] - c["y"]) ** 2) if self.pp else None
            near = c["_near"]
            if near and math.dist(near["xy"], (c["x"], c["y"])) < 1000:
                bonus += 0.15; why.append(f"within 1 km of pressure point {near['props']['id']} (ambush zone)")
        # reef face / corner / lee eddy classification
        geo = self.zone_at(c["x"], c["y"])
        if geo:
            why.append(f"geomorphic zone: {geo}")
            if geo in ("Reef Slope", "Sheltered Reef Slope", "Reef Crest", "Back Reef Slope"):
                bonus += 0.1; why.append("reef face/slope (ambush position)")
        fb, fw = self.feeding_bonus(sp, c, day, cw[1] if cw else None)
        bonus += fb; why.extend(fw)
        s = (cf + bonus) * sp.get("season", 1.0)
        cl = closed_on(sp["id"], day)
        if cl: why.append(closed_label(cl))
        return round(s, 3), why, dict(current=cw, closed=cl, sweet=False, species_type="ambush", deep=is_deep(dl))

    def score(self, sp, c, day, hours=None, current_override=None):
        """Dispatch to the right engine. Returns (score, reasons, details)."""
        if c["kind"] == "pressure_point":
            return self.score_ambush(sp, c, day, hours, current_override)
        if sp["group"] == "PELAGIC":
            return self.score_pelagic(sp, c, day, hours, current_override)
        return self.score_demersal(sp, c, day, hours, current_override)

    def answer_sources(self, sid, sc, pick, day=None, top=3):
        """G12 (Mick, 21 Nov 2026 6:37 pm: "Yes, add the held-but-unused list (G12) to the engine").
        Every answer lists the files used and the data the engine HOLDS for it but did NOT use, each with a reason.
        Rule (start-up stack): held-but-unused data is a fail, so it must always be visible."""
        A = self.last_area or {}
        pick_ds = {c["dataset"] for _, c, _, _ in pick}
        scored_ds = {c["dataset"] for _, c, _, _ in sc}
        legal_ds = set(A.get("legal_datasets", [])); cand_ds = set(A.get("cand_datasets", []))
        used, held = [], []
        for ds, n in sorted(A.get("datasets", {}).items(), key=lambda t: -t[1]):
            if ds in pick_ds:
                used.append(dict(dataset=ds, rows_in_area=n, how="a top pick came from it")); continue
            if re.search(MICK_MARK_DS, ds):
                held.append(dict(kind="point data in the answer area", dataset=ds, rows_in_area=int(n), reason="Mick's marks (reference layer, not scored)")); continue
            if ds in scored_ds: why = f"scored for {sid}, none made the top {top}"
            elif ds in legal_ds: why = f"legal spots here scored 0 for {sid} (depth band, structure fit or season)"
            elif ds in cand_ds: why = "every spot from it here was blanked (no-take zone, deeper than 150 m LAT, no depth, or dries)"
            elif ds in ("aho_enc_soundings.csv", "ramp_to_public_reefs_distance_bearing.csv"): why = "reference data, not a spot source (soundings / ramp distances)"
            else: why = "not a structure or habitat type the scorer reads (map / RAG layer)"
            held.append(dict(kind="point data in the answer area", dataset=ds, rows_in_area=int(n), reason=why))
        for h in self.held:
            held.append(dict(kind="engine source not used by this engine", dataset=f"{h['role']}/{h['key']}", path=h.get("path"), reason=h["reason"]))
        pel = self.species.get(sid, {}).get("group") == "PELAGIC"
        return dict(species=sid, species_type="pelagic" if pel else "demersal",
                    judged_on=(PELAGIC_NOTE if pel else "demersal: depth sweet spot first, then structure, current and season"), day=str(day) if day is not None else None, closures_feed=CLOSURES_STATUS, files_used=list(self.used),
                    area_data_used=used, held_but_unused=held)

    @staticmethod
    def held_text(ans, limit=None):
        """Plain lines for an answer: 'Held but not used: <data> (<reason>)'."""
        hb = (ans or {}).get("held_but_unused") or []
        lines = [f"- {h['dataset']}" + (f" ({h['rows_in_area']:,} rows here)" if h.get("rows_in_area") else "") + f": {h['reason']}" for h in hb]
        return ["Held but not used:"] + (lines[:limit] if limit else lines) + ([f"- ... and {len(lines) - limit} more"] if limit and len(lines) > limit else [])

    def rank(self, sid, cands, day, top=3, min_sep_m=500, hours=None):
        sp = self.species[sid]; sc = []
        for c in cands:
            s, why, det = self.score(sp, c, day, hours=hours)
            if s > 0:
                sc.append((s, c, why, det))
        if sp["group"] == "PELAGIC":  # 21 Nov 7:32 pm: no depth-based ranking for pelagics
            sc.sort(key=lambda t: -t[0])
        else:
            sc.sort(key=lambda t: (not t[3].get("sweet", False), -t[0]))  # demersal: sweet-spot spots first (Mick 21 Nov)
        pick = []
        for s, c, why, det in sc:
            if any(math.dist((c["x"], c["y"]), (q[1]["x"], q[1]["y"])) < min_sep_m for q in pick): continue
            pick.append((s, c, why, det))
            if len(pick) == top: break
        self.last_answer = self.answer_sources(sid, sc, pick, day, top)  # G12: every answer lists held-but-unused
        return sc, pick


    def plain_mark(self, sp, c, score, why, det):
        """Plain-language mark output with coordinates (delivery plan step 3).
        E.g. 'There's a lump that matches the engine requirements. Likely coral trout / red emperor.
        It matches the depths and the criteria. Here's a mark.'"""
        dl = c["depth_lat_m"]
        place = self.place(c["x"], c["y"])
        feature = c["label"]
        name = sp["name"]
        lat_s = f"{abs(c['lat']):.5f} S" if c["lat"] < 0 else f"{c['lat']:.5f} N"
        lon_s = f"{c['lon']:.5f} E"

        if det.get("species_type") == "pelagic":
            water_features = [w for w in why if any(k in w.lower() for k in ("sst", "colour", "chlorophyll", "upwelling", "front", "current", "tide run"))]
            water_desc = "; ".join(water_features[:3]) if water_features else "water features present"
            line = (f"Water feature mark at {place}. {water_desc}. "
                    f"Likely {name} area. GPS: {lat_s}, {lon_s}.")
        elif det.get("species_type") == "ambush":
            current_info = [w for w in why if "tide run" in w.lower() or "pressure point" in w.lower() or "AMBUSH" in w]
            cur_desc = "; ".join(current_info[:2]) if current_info else "current pushing onto structure"
            line = (f"Ambush point at {place}. {cur_desc}. "
                    f"Likely {name} holding here on the tide. GPS: {lat_s}, {lon_s}.")
        else:
            sweet = "in the sweet spot" if det.get("sweet") else "in the depth band"
            deep_note = " (DEEP: 120-150 m)" if det.get("deep") else ""
            line = (f"There's a {feature} at {place} that matches the engine requirements. "
                    f"Likely {name} in there. {dl} m LAT {sweet}{deep_note}, "
                    f"structure fits the criteria. Here's a mark: {lat_s}, {lon_s}.")
        return line

    def rank_with_marks(self, sid, cands, day, top=3, min_sep_m=500, hours=None):
        """Rank candidates and produce plain-language mark descriptions."""
        sc, pick = self.rank(sid, cands, day, top=top, min_sep_m=min_sep_m, hours=hours)
        sp = self.species[sid]
        marks = []
        for s, c, why, det in pick:
            marks.append(dict(
                score=s, lat=c["lat"], lon=c["lon"],
                depth_lat_m=c["depth_lat_m"], feature=c["label"],
                plain=self.plain_mark(sp, c, s, why, det),
                reasons=why, details=det
            ))
        return marks, sc, pick


def species_type(sid):
    """'demersal' | 'pelagic' | None (unknown / species not set)."""
    return SPECIES_TYPE.get(str(sid)[:4]) if sid else None


def is_pelagic(sid):
    return species_type(sid) == "pelagic"
