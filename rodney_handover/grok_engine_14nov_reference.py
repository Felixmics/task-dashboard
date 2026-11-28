#!/usr/bin/env python3
"""RODNEY point-data-first engine core (14 Nov 2026, Grok Bot, box only).
Shared by engine_test.py (v2) and the local planner server (/workspace/rodney/planner/planner_server.py).

Rules built in (Mick):
- 120 m LAT hard cutoff on EVERY input: cut rasters, point table filtered again at load (own depth AND HD8 depth),
  pressure points filtered at load, species depth bands capped at 120 m, every candidate re-checked before scoring.
- LAT depths, MSL = LAT + 1.74 m, 0.5 m rounding, tagged surveyed / estimated.
- No-take blanking: GBRMPA MNP / Preservation / Scientific Research / Buffer (+300 m margin) and Commonwealth Islands
  (zoning gpkg), GBRMPA no-take blank geojson, Qld state no-take geojson. Blank spots are never suggested.
- Point data first (G1 hd8check table, G3-corrected tags), then HD8 10 m cut grid, then GBR30 cut (estimated) last.
- 20 FINAL species (DE01-DE10, PE01-PE10) from the v5 tables + 12 Nov test profiles (Arlington rerun profiles.py).
Model only. Not for navigation. ITS A PREDICTING APP, INTENT. NO GUARANTEE IS ACCEPTED."""
import json, math, os, re, sys, importlib.util, datetime as dt
import numpy as np

W = "/workspace"
PL = f"{W}/shared_refs/Project Library"
CUTOFF_LAT_M = 120.0
MSL_ABOVE_LAT = 1.74
CUTOFF_MSL_M = -(CUTOFF_LAT_M - MSL_ABOVE_LAT)  # -118.26
MANIFEST = f"{PL}/engine_sources_2026-11-12.json"
POINTS_CANONICAL = f"{W}/rodney_root_index/RODNEY_points max120mLAT 2026-11-12.csv.gz"
POINTS_HD8CHECK = f"{W}/rodney_root_index/RODNEY_points max120mLAT hd8check 2026-11-12.csv.gz"
POINTS_ENGINE = f"{W}/rodney_root_index/RODNEY_points max120mLAT hd8check G3-corrected 2026-11-14.csv.gz"  # G1 + G3
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
# Closures from RODNEY TARGET SPECIES - FINAL.md / v5 tables (coral reef fin fish; Spanish mackerel north of 22 S)
CRFF = [("2026-10-08", "2026-10-12"), ("2026-11-06", "2026-11-10"), ("2027-10-26", "2027-10-30"), ("2027-11-25", "2027-11-29")]
CLOSURES = {**{s: CRFF for s in ("DE01", "DE02", "DE03", "DE04", "DE05", "DE06", "DE07", "DE09")},
            "PE01": [("2026-10-08", "2026-10-29"), ("2026-11-06", "2026-11-27")]}

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
    """'10-140 m (commonly 25-80 m)' -> ext (10,140), core (25,80). Capped at 120 m LAT."""
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
            core = (min(p["core"][0], CUTOFF_LAT_M), min(p["core"][1], CUTOFF_LAT_M))
            ext = (min(p["ext"][0], CUTOFF_LAT_M), min(p["ext"][1], CUTOFF_LAT_M))
            out[sid] = dict(id=sid, group=p["g"], name=p["n"], v5_name=r["common_name"], sci=r["scientific_name"], core=core, ext=ext,
                            capped=(p["ext"][1] > CUTOFF_LAT_M or v5deep), v5_depth=r["depth_range"], bottom=p["bottom"], zones=p["zones"],
                            season=p["season"], season_txt=p["season_txt"], sand_ok=p.get("sand_ok", False), zone_note=p.get("zone_note"),
                            needs=p.get("needs", []), notake_species=p.get("notake", []), size=r["size_limit_qld"], possession=r["possession_limit_qld"],
                            closures_txt=r["closures_qld"], substrate=r["substrate_structure"], habitat=r["preferred_habitat"], source_file=f)
    return out


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
        self.cur = make_current(json.load(open(R("current", "current_harmonics")))); use(R("current", "current_harmonics"))
        PP = json.load(open(R("current", "pressure_points"))); use(R("current", "pressure_points"))
        self.pp = []
        for f in PP["features"]:
            d = f["properties"].get("depth_lat_m")
            if d is not None and float(d) > CUTOFF_LAT_M:
                continue  # 120 m filter at load
            lo, la = f["geometry"]["coordinates"][:2]
            self.pp.append(dict(lat=la, lon=lo, xy=self.tr.transform(lo, la), props=f["properties"], days=json.loads(f["properties"]["days"])))
        Z = pyogrio.read_dataframe(R("zoning", "zoning"), layer="GBRMPA_GBRMP_Zoning_full_res_nd_2026"); use(R("zoning", "zoning"))
        nt = Z[Z.TYPE.str.startswith(("Marine National Park", "Preservation", "Scientific Research", "Buffer"))]
        geoms = list(nt.geometry.buffer(300)) + list(Z[Z.TYPE.str.startswith("Commonwealth Islands")].geometry)
        for key in ("no_take_gbrmpa", "no_take_qld_state"):
            g = pyogrio.read_dataframe(R("zoning", key)).to_crs(32755); geoms += list(g.geometry); use(R("zoning", key))
        self.n_notake_polys = len(nt)
        self.notake = prep(unary_union(geoms))
        names = pyogrio.read_dataframe(REEF_NAMES).to_crs(32755); names = names[names.FEAT_NAME.isin(["Reef", "Cay", "Rock"])].reset_index(drop=True)
        names["NAME"] = [l if not str(g).startswith("U/N") else "unnamed reef " + str(l).split("(")[-1].rstrip(")") for g, l in zip(names.GBR_NAME, names.LOC_NAME_S)]
        self.names = names; self.name_tree = STRtree(list(names.geometry))
        self.points_path = points
        P = pd.read_csv(points, low_memory=False); use(points)
        n0 = len(P)
        d_own = pd.to_numeric(P.depth_LAT_m, errors="coerce"); d_hd8 = pd.to_numeric(P.get("hd8_depth_LAT_m"), errors="coerce") if "hd8_depth_LAT_m" in P else d_own * np.nan
        P = P[~((d_own > CUTOFF_LAT_M) | (d_hd8 > CUTOFF_LAT_M))].copy()  # 120 m filter at load (own + HD8)
        self.points_dropped_120 = n0 - len(P)
        P["is_mark"] = P.dataset.astype(str).str.contains(MICK_MARK_DS, regex=True) & (P.source_tag == "Mick mark")
        self.P = P
        xs, ys = self.tr.transform(P.lon.values, P.lat.values); self.P["x"] = xs; self.P["y"] = ys
        from scipy.spatial import cKDTree
        self.ptree = cKDTree(np.c_[xs, ys])
        self.held = []  # held-but-unused (G12)
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
        """HD8 cut copy (nearest 10 m cell, unsmoothed), then GBR30 cut (estimated). None if no value or deeper than 120 m."""
        def samp(r):
            b = r.bounds
            if not (b.left <= x <= b.right and b.bottom <= y <= b.top): return None
            v = float(list(r.sample([(x, y)]))[0][0]); nd = r.nodata
            if not np.isfinite(v) or (nd is not None and v == nd): return None
            return v
        z = samp(self.r_depth)
        if z is not None:
            fl = samp(self.r_flag)
            return rhalf(-z - MSL_ABOVE_LAT), ("surveyed" if fl == 1 else "estimated"), "HD8 10 m (120 m cut)"
        z = samp(self.r_g30)
        if z is not None and z < 0:
            return rhalf(-z - MSL_ABOVE_LAT), "estimated", "GBR30 30 m (120 m cut, fallback)"
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
            c.update(depth_lat_m=dl, depth_tag=tag, depth_src=src)
            out.append(c)
        stats["legal_candidates"] = len(out)
        return out, stats, A

    def evidence(self, c, r_marks=300):
        idx = self.ptree.query_ball_point([c["x"], c["y"]], r_marks)
        sub = self.P.iloc[idx] if idx else self.P.iloc[[]]
        marks = sub[sub.is_mark]
        return dict(marks300=int(len(marks)), mark_species=" ".join(marks.species.astype(str).tolist())[:4000])

    def score(self, sp, c, day, hours=None, current_override=None):
        """Point-first score for one species at one candidate. Returns (score, reasons, details) or (0, ...) if out of band."""
        core, ext = sp["core"], sp["ext"]; dl = c["depth_lat_m"]
        if dl > CUTOFF_LAT_M:
            return 0.0, ["deeper than 120 m LAT - excluded"], {}
        df = 1.0 if core[0] <= dl <= core[1] else (0.5 if ext[0] <= dl <= ext[1] else 0.0)
        if df == 0:
            return 0.0, [f"{dl} m LAT outside {sp['name']} band"], {}
        why = [f"{dl} m LAT ({c['depth_tag']}) in {'core' if df == 1 else 'extended'} band {core[0]:g}-{core[1]:g} m"]
        # structure fit
        if sp["group"] == "DEMERSAL":
            b = (sp["bottom"] or set()) & c["bottom"]; z = sp["zones"] & c["zones"]
            sf = 1.0 if (b and z) else (0.8 if (b or z) else 0.5)
            if c["bottom"] == {"sand"} and not sp["sand_ok"]: sf = 0.4
        else:
            z = sp["zones"] & c["zones"]; b = set()
            sf = 1.0 if z else 0.5
        why.append(f"structure: {c['label']}" + (f" (matches {', '.join(sorted(b | z))})" if (b or z) else " (weak match)"))
        bonus = 0.0
        if sp["id"] in c["hab_species"]:
            bonus += 0.15; why.append("species habitat point (10-31 habitat file)")
        if sp["name"].split(" (")[0].lower() in c["species_txt"].lower():
            bonus += 0.05
        if "_ev" not in c: c["_ev"] = self.evidence(c)
        ev = c["_ev"]
        if ev["marks300"]:
            bonus += min(0.05 * ev["marks300"], 0.2); why.append(f"{ev['marks300']} of Mick's marks within 300 m")
        # current in the bite window (RECOM tide-driven current only)
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
        if cw: why.append(f"tide run {ckn:.2f} kn toward {card(cw[0]['dir_to'])} at {cw[1]:02d}:00 (RECOM model)")
        # pressure point
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
        s = (df * sf * cf * zf + bonus) * sp["season"]
        cl = closed_on(sp["id"], day)
        return round(s, 3), why, dict(current=cw, closed=cl, marks300=ev["marks300"])

    def rank(self, sid, cands, day, top=3, min_sep_m=500, hours=None):
        sp = self.species[sid]; sc = []
        for c in cands:
            s, why, det = self.score(sp, c, day, hours=hours)
            if s > 0:
                sc.append((s, c, why, det))
        sc.sort(key=lambda t: -t[0]); pick = []
        for s, c, why, det in sc:
            if any(math.dist((c["x"], c["y"]), (q[1]["x"], q[1]["y"])) < min_sep_m for q in pick): continue
            pick.append((s, c, why, det))
            if len(pick) == top: break
        return sc, pick
