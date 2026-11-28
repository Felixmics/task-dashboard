# RODNEY Engine Alignment — Grok (14 Nov) → Handover (21 Nov 2026)

## Summary

The handover engine (`07_rodney_engine.py`, 879 lines, 21 Nov 2026) is the **definitive version**.
It is a direct evolution of the Grok-built engine (`rodney_engine.py`, 14 Nov 2026) with every
decision Mick made between 14-21 Nov applied. The Grok engine is superseded — kept as a reference
copy (`grok_engine_14nov_reference.py`) for audit only.

**Engine test results (14 Nov run on the Grok engine): 85 PASS / 1 WARN / 0 FAIL**
The 1 WARN: `habitat/habitat_backreef_points` not built yet — engine runs without it.

---

## What changed: Grok → Handover

| # | Change | Grok (14 Nov) | Handover (21 Nov) | Source |
|---|--------|---------------|-------------------|--------|
| 1 | **Depth cutoff** | 120 m LAT hard cutoff | 150 m LAT cutoff, 120-150 m labelled "deep" | Mick 21 Nov 5:55 pm |
| 2 | **Cutoff MSL formula** | `-(120 - 1.74) = -118.26` **BUG** | `-(150 + 1.74) = -151.74` **FIXED** | Test Package item 3 |
| 3 | **Sweet spots** | None — single depth band per species | SWEET dict: 10 demersal species with (sweet_lo, sweet_hi) and (band_lo, band_hi) | Test Package / Mick |
| 4 | **Species type split** | All 20 species scored the same way | SPECIES_TYPE dict: demersal vs pelagic; pelagics NOT scored on depth | Mick 21 Nov 7:31 pm |
| 5 | **Three scoring engines** | Single `score()` method | `score_demersal()`, `score_pelagic()`, `score_ambush()` with dispatcher | Handover design |
| 6 | **Pelagic scoring** | Depth-based (same as demersal) | Water features: SST, chlorophyll, upwelling — ocean_score() | Mick 21 Nov 7:32 pm |
| 7 | **Ambush engine** | Not present | Hourly tide/current on reef faces | Handover design |
| 8 | **Buffer zones** | Not handled | Shown but labelled "troll only for pelagics" | Mick 21 Nov 6:23 pm |
| 9 | **Rubble rules** | Not present | RUBBLE_RULES dict (DE03 25-100 m, DE04 30-150 m), reef flat zones | Handover design |
| 10 | **Feeding triggers** | Not present | Loaded from RAG: tide_phase, moon_phase, pressure, temp, bait | XB3, 12 Nov |
| 11 | **Closures** | Hard-coded CRFF dates | Dynamic from RAG feed (`load_closures()`), never hard-coded | Mick 21 Nov 6:25 pm |
| 12 | **G12 tracking** | Not present | `answer_sources`, `held_text` — held-but-unused audit trail | Handover design |
| 13 | **Natural language output** | Not present | `plain_mark()` and `rank_with_marks()` | Handover design |
| 14 | **Points table** | 60,446 rows at 120 m | 60,847 rows at 150 m (60,815 after hd8check/G3) | 21 Nov 7:26 pm |
| 15 | **Manifest** | `engine_sources_2026-11-12.json` (26 files) | `engine_sources_2026-11-17.json` (+ seabed_hardness, INPUT 12 labels) | 17 Nov update |
| 16 | **MSL helpers** | Inline conversion | `msl_to_lat()`, `lat_to_msl()`, `is_deep()`, `depth_label()` functions | Handover cleanup |

### Shared / unchanged between both engines
- Feature type dictionary (FT): 25+ feature types with bottom/zone sets
- HAB_DS habitat dataset mapping
- `make_current()` RECOM tidal harmonic model (16 constituents, 10 stations)
- Engine class structure, `__init__`, `engine_lookup`, `run`
- Point-data-first candidate pipeline: G1 hd8check → HD8 10m → GBR30 fallback
- Mick's marks as evidence counts, never scoring positions
- Fisheries Queensland limits (FQ dict)
- Compass directions, rounding, alert system (WONKY_ALERT)

---

## Test Package "Waiting on Mick's Go" — 11 items status

From the RODNEY Test and Training Package (17 Nov 2026), section 11:

| # | Item | Status in handover | Notes |
|---|------|--------------------|-------|
| 1 | Melville strips alignment | **PENDING** | Needs HD8 rebuild with corrected strips |
| 2 | Falkor survey offsets | **PENDING** | Needs HD8 rebuild with offset corrections |
| 3 | Fix -118.26 cut formula | **DONE** | Handover: `-(150 + 1.74) = -151.74` |
| 4 | Seam filter for structure method | **PENDING** | Structure method v0 not yet in engine |
| 5 | Pick spacing for structure method | **PENDING** | Structure method v0 not yet in engine |
| 6 | Type check for structure method | **PENDING** | Structure method v0 not yet in engine |
| 7 | Snap to lump top | **PENDING** | Structure method v0 not yet in engine |
| 8 | Rubble marks append | **READY** | `08_rubble_marks_append.py` written, approved, blocked on source files |
| 9 | 150 m point table rebuild | **DONE** | 60,847 rows at 150 m LAT |
| 10 | Seabed hardness evidence | **DONE** | Wired into engine 17 Nov, in manifest |
| 11 | North strip hole fill | **PENDING** | Needs HD8 rebuild |

**Summary: 3 DONE, 1 READY (blocked on files), 7 PENDING (mostly HD8 rebuild and structure method)**

---

## Structure method v0 (from Test Package)

The structure method has defined weights but is NOT yet wired into the engine:

| Weight | Component |
|--------|-----------|
| 0.25 | Rugosity |
| 0.20 | Footprint |
| 0.15 | Moderate relief |
| 0.15 | Isolation |
| 0.10 | Clustering |
| 0.10 | Tidal-axis alignment |
| 0.05 | Structure type |

Key lesson from testing: **"finding 5 m bommies is a data gap, not a missing model"** — the 30 m grid cannot resolve individual bommies; that requires measured multibeam (AHO ref surfaces, CSIRO 5 m grids).

---

## Supporting files inventory (Drive: 03_Engine_and_RAG)

| File | Drive ID | Purpose | Status |
|------|----------|---------|--------|
| engine_test_results 2026-11-15 v2.md | `11RmHh5u2NxZiOznlqLEzlsg9StLPzzT0` | 85/1/0 test results | Reference |
| DATA_CATALOGUE_2026-11-14 | `1SCUw4P6UD0tBUHOHmSQLHR7i6m-fTTls4aJ8Z1o17LA` | Full data catalogue spreadsheet | Reference |
| SEAFLOOR SOURCES AT A GLANCE | `15ds9RLOKvQQ9afq4fZHtEQsPgKLWd_Y5ax_35T9tSeQ` | 15 seafloor datasets, coverage %, licences | Reference |
| WEB_LINKS_REGISTER | `1U0wkiN_bAcPYYVDEDpeCzN9ahsjK_NMSJiyQ_CdZTOk` | External links inventory | Reference |
| RODNEY_AI_TEST_WAYPOINTS_LOG | `1gk3xDz4A7WmKYOXV6J8hLBFsID3vALZX_iCZPeyC8fk` | Test waypoint log | Reference |
| FILE_SPECIES_MAP_2026-11-12.md | `1krcUAzOQOZDFRVzev9d9SP3Y6Bjyvo94` | Species ↔ file mapping (62 KB) | Reference |
| FILE_SPECIES_MAP_2026-11-12.csv | `1VdFfVSbjQs3OBuAc2x-UuXXq19e3AYfc` | Species ↔ file mapping (2.3 MB) | Reference |
| build_species_pelagic_v5.py | `12SB33BgeKB83mlPQB_0YUm3aB91P7PbQ` | Pelagic species table builder | Reference |
| species_evidence_arlington.json | `1EIf1PMg_fILD641lleLlEGIz9i4_1QVd` | Arlington test evidence | Reference |
| rodney_engine.py (Grok 14 Nov) | `1Cr6bT6YGI-fRS6SWu8cO8j6Y0xInOr08` | Original engine — SUPERSEDED | Reference |

### Drive subfolders (03_Engine_and_RAG)
- `Engine_test_2026-11-12_arlington_rerun/` — profiles.py, test scripts
- `Engine_baseline_combined_2026-11-12/` — baseline test data
- `engine_feed/` — RAG feed data
- `QGIS_Projects_and_Skills/` — 17_Skills, Styles_and_Recipes, 08_QGIS_Projects

---

## Seafloor data coverage (from SEAFLOOR SOURCES AT A GLANCE)

| Source | Resolution | % of HD8 box | Good for |
|--------|-----------|--------------|----------|
| HD8 composite | 10 m output | 100% (measured 8.5%) | Detail where measured; fill elsewhere |
| GBR30 | 30 m | 79.4% | Backdrop/fill only; NOT 5 m bommies |
| AusBathyTopo 250 m | 250 m | 7.2% | Deep slope backdrop |
| NGBR 16 m | 16 m | 6.0% | Check; coarser than 5 m objects |
| EOMAP SDB 10 m | 10 m | 4.9% | Reef-top only; NOT 20-80 m detail |
| AHO Ref Surface 0.5-1 m | 0.5-1 m | 0.018% (3 sites) | Best public 5 m bommie test bed |
| CSIRO 5 m DEMs | 5 m | 0.4% | Detail on strips; test/check |
| HI220 LADS | ~10 m | 0% (not released) | None for this box |

**Key fact: only 8.5% of the HD8 box is measured multibeam. The rest is 30 m interpolated fill.**

---

## Datum and depth rules (locked)

- MSL = LAT + 1.74 m (Cairns Wharf, Maritime Safety Qld 2026)
- Reef MSL = ~1.53-1.57 m (project locked figure: 1.55 m)
- Chartplotter and sounder reference LAT
- CUTOFF_MSL_M = -(CUTOFF_LAT_M + MSL_ABOVE_LAT) — the PLUS sign is critical (Grok had minus = bug)
- Depths always positive below datum, tagged surveyed/estimated
- 0.5 m rounding via `rhalf()`

---

## Next steps

1. **HD8 rebuild** needed for 7 of the 11 pending items (Melville strips, Falkor offsets, north strip hole, structure method inputs)
2. **Structure method v0** — weights defined, needs implementation as a scoring layer in the engine
3. **Rubble marks append** — script ready (`08_rubble_marks_append.py`), blocked on source files in /workspace/
4. **Ocean layers** — `score_pelagic()` and `ocean_score()` need live SST/chl-a feed wiring
5. **150 m grid copies** — point table done (60,847 rows); raster grids (depth_msl, gbr30_fallback) still at 120 m cut
6. **Ambush engine** — `score_ambush()` skeleton in place, needs hourly tide/current test data

---

*Alignment completed 21 Nov 2026. The handover engine (07_rodney_engine.py) is the single source of truth for RODNEY's scoring logic.*
