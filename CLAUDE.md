# CLAUDE.md — RODNEY Project

## Who is Mick

Mick is a fisherman based in the Cairns region of the Great Barrier Reef (GBR), Queensland, Australia. He uses AI, satellite data, bathymetry, benthic surveys, geomorphic classifications, tidal harmonics, moon phases, chlorophyll maps, SST fronts, and currents to narrow down productive fishing areas. He is the domain expert — every scoring rule, depth cutoff, species behaviour note, and UI preference in RODNEY comes from Mick's direct experience or his explicit approval.

Mick's timezone: Australia/Brisbane (AEST, UTC+10).

## What is RODNEY

RODNEY is an AI-assisted reef fishing planner for the GBR Cairns region. It is **not** a fisheries inspector, lawyer, or navigation tool. It predicts where fish are likely to be based on sourced evidence — it never presents unsourced scores as catch fact.

**Standing rule:** "Model only. Not for navigation. It's a predicting app, intent. No guarantee is accepted."

### Architecture: Static Base + Dynamic Overlay

- **Static base:** Mick's marks, CSVs, survey evidence, depth grids, species profiles, habitat data (~60,815 rows in the canonical points table)
- **Dynamic overlay:** Tide, current, wind, SST, chlorophyll, upwelling proxy, moon phase, season, closures — read live with a 10-day rolling window, or dated + stale-warned

### Three Scoring Engines

All in `rodney_handover/07_rodney_engine.py`:

1. **`score_demersal()`** — Depth sweet spot first, then structure (hard/coral/rubble), current lift, season. Sweet spots from the SWEET table (e.g. red emperor DE03: 40–80 m core, 10–150 m band). Deeper than sweet spot = "long way up, higher shark risk."
2. **`score_pelagic()`** — Judged on water features (colour lines, SST breaks, upwellings, eddies), **not depth**. Mick: "WHY WOULD PELAGIC NEED DEPTH" / "FIX THE LOGIC TO PELAGIC SO BOTS KNOW THE DIFFERENCE."
3. **`score_ambush()`** — Hourly tide/current on reef faces, corners, lee eddies. Uses RECOM tidal harmonics (CSIRO eReefs, 14 constituents, Dec 2016–Apr 2017).

### Key Rules (all from Mick)

- **Depth rule (21 Nov 2026):** Keep marks to 150 m LAT. Label 120–150 m "deep." Drop anything deeper. Show each species' sweet-spot depth first (demersal only).
- **LAT depths:** MSL = LAT + 1.74 m. 0.5 m rounding. Tagged surveyed/estimated.
- **No-take blanking:** GBRMPA MNP / Preservation / Scientific Research (+300 m margin) + Commonwealth Islands. Buffer zones are NOT blanked — labelled "Buffer zone: troll only for pelagics."
- **Point data first:** G1 hd8check table → HD8 10 m cut grid → GBR30 cut (estimated) last.
- **Rubble rule:** Red emperor (DE03) on rubble 25–100 m; nannygai (DE04) 30–150 m; redthroat emperor (DE06) not until a range is set.
- **Closures:** Read from the live DAF feed, never hard-coded. Show with "saved copy" date and "may be out of date" warning.
- **Tide is #1 factor** for coral trout and red emperor in this box. Bite windows: first 1.5–2 h of run and last ~1.5 h into the next change.
- **Safety:** Go if wind ≤ 12 kn AND waves ≤ 1.2 m (not the Tririp 15 kn figure).
- **Wind:** A northerly of 10 kn+ is a CHANGE OF PLAN — fish the lee faces.

### 20 Final Species

- **Demersal (DE01–DE10):** Coral trout, bar-cheek trout, red emperor, nannygai, crimson snapper, redthroat emperor, sweetlip, hussar, saddletail snapper, moses perch
- **Pelagic (PE01–PE10):** Spanish mackerel, narrow-barred mackerel, wahoo, dogtooth tuna, yellowfin tuna, longtail tuna, queenfish, giant trevally, golden trevally, cobia

## Key References and Files

### Google Sheets

- **Marks Master Register:** `1ealiWuH6EpFzgNsGgeoKBh6JB438vyQD52f9u0Qds-M`
  - Contains all of Mick's marks (2,647 shown, 701 hidden in no-take zones as of Nov 2026)

### Workspace Paths (on the RODNEY workspace, not this repo)

| Path | What |
|---|---|
| `/workspace/rodney_root_index/filtered_150m/RODNEY_points max150mLAT hd8check G3 2026-11-21.csv.gz` | Canonical points table (60,815 rows) |
| `/workspace/shared_refs/Project Library/` | Project Library (engine sources, blueprints, READ FIRST) |
| `/workspace/shared_refs/RAG/` | RAG dynamic sources (closures, feeds, freshness) |
| `/workspace/reef-app/feeds/cache/ocean_grids/` | Reef Weather ocean layer cache (SST, chl, fronts) |
| `/workspace/marine_db_v5/` | Species tables (v5 demersal + pelagic CSVs) |
| `/workspace/Map Builder index/` | HD9 v01 map HTML + sidecar data |
| `/workspace/rodney-pc/hd6/` | HD6 (best historical UI reference) |
| `/workspace/RODNEY complete project/map/` | HD8 v06 map (four-corner layout reference) |
| `/workspace/rodney-library/` | Rodney library (source of truth, env scanner, Edge Finder, AIRS) |
| `/workspace/shared_refs/RODNEY UI design brainstorm 2026-11-20/` | Mick's UI wish list |

### Key Source Files (engine data)

| File | Purpose |
|---|---|
| `engine_sources_2026-11-17.json` | Engine manifest (all source paths + roles) |
| `profiles.py` (Arlington rerun 12 Nov) | Species depth/habitat/season profiles |
| `species_reef_demersal_v5.csv` | Demersal species table (names, limits, depth text) |
| `species_pelagic_v5.csv` | Pelagic species table |
| `species_feeding_triggers.csv` | Feeding triggers (XB3, bite-window modifiers) |
| `ocean_layers_grid.json` / `ocean_fronts.geojson` | Ocean layers for pelagic scoring |
| RECOM current harmonics JSON | Tidal current harmonics (14 constituents) |
| Pressure points GeoJSON | Current-lift pressure point candidates |

## Handover Files (in this repo)

| File | Contents |
|---|---|
| `rodney_handover/STATUS.md` | Engine Bot PC status, gate checks, blockers |
| `rodney_handover/HD9_v02_checklist.md` | HD9 v02 build checklist, outcomes (a)–(i), 26 must-carry items |
| `rodney_handover/05_mick_requests_chronological.md` | Complete chronological list of Mick's 164+ requests |
| `rodney_handover/06_hd6_hd8_carryover_audit.md` | Feature carry-over audit: every version HD–HD9, what's in, what's missing |
| `rodney_handover/07_rodney_engine.py` | The actual engine code (3 scoring paths, all rules) |
| `rodney_handover/08_rubble_marks_append.py` | Rubble marks append script (272 rubble + 19 cleared candidates) |

## HD9 v02 Build Status

### What's Done (outcomes a–d+)

- Removed the 300 m bonus
- Depth auto-convert (MSL → LAT)
- Rubble rule implemented
- Three scoring engines (demersal, pelagic, ambush)
- Ocean layer scoring for pelagics
- Plain-language marks with sweet-spot text

### What's Remaining (outcomes e–i)

- (e) Pelagic overlays on the map
- (f) Seafloor shape-detection
- (g) Weather feeds refresh
- (h) 272 rubble marks append to register
- (i) HD9 v02 full build

### 26 Must-Carry Items (MC1–MC26)

These are features that existed in older map versions but are **missing from HD9 v01**. The full list is in `rodney_handover/06_hd6_hd8_carryover_audit.md` and `rodney_handover/HD9_v02_checklist.md`. Key ones:

1. Four-corner chartplotter layout (HD8 v06 shell)
2. Live pointer readout (depth + GPS + zone on hover, not click)
3. 3D terrain with exaggeration and orbit
4. TIMEZERO / Sunset palettes and Mick's hillshades
5. Depth contours (5/10/20/50/100/200 m selector)
6. White reef and island name labels
7. Tide curve + 72 h LAT chart + bite-window advice
8. Wind forecast strip + northerly/lee-face guidance
9. RECOM flood/ebb currents on map
10. Marks search by name or ID
11. Best-marks-today picker + Demersal/Pelagic mode switch
12. Export GPX (Furuno-friendly)
13–26. Satellite basemap, beacons, survey evidence, pinnacles/ledges, hardness readout, zoning outlines, seabed photos, tide-adjusted depth, environmental snapshot, 3-day plan, Back Reef Slope, trip planner, bottom-temp overlay, freshness lines

## Bot Roles

RODNEY uses multiple specialised bots:

| Bot | Responsibility |
|---|---|
| **Engine Bot PC** | Scoring engine, species profiles, depth rules, current harmonics |
| **Map Builder** | HD9 HTML map, overlays, sidecar data, UI layout |
| **Seafloor Builder** | Depth grids, unsmoothed 10 m LAT tiles, contours |
| **Reef Weather** | Live feeds (SST, chl, wind, tide predictions), ocean layer cache |
| **Data Scout** | Source discovery, new datasets, survey evidence ingestion |
| **Rules & QA** | Mick's rules enforcement, checklist compliance, gate checks |
| **Auditor Bot** | Cross-version feature audit, carry-over tracking |

## Domain Terminology

| Term | Meaning |
|---|---|
| **LAT** | Lowest Astronomical Tide — the depth datum. MSL = LAT + 1.74 m in this region. |
| **Benthic** | Relating to the seafloor. Benthic surveys map coral, sand, rubble, etc. |
| **Geomorphic** | Seafloor shape categories (reef slope, reef flat, lagoon, inter-reef, etc.) |
| **GBR10** | 10 m resolution benthic/geomorphic classification (MODELLED, shallow reef only ~0–20 m) |
| **GBR30** | 30 m resolution bathymetry grid (GA/JCU). Coarser fallback when no multibeam. |
| **RECOM** | CSIRO eReefs Relocatable Coastal Ocean Model. Provides tidal current harmonics. |
| **Sweet spot** | The depth range where a demersal species is most likely found (core band). |
| **Wonky hole** | Depression in the seafloor (rubble/sponge habitat). "Look for a dip, not a lump." |
| **Pressure point** | Where current hits structure — creates uplift that concentrates baitfish. |
| **Rubble** | Broken coral substrate. Important habitat for red emperor, nannygai. |
| **SST** | Sea surface temperature. Fronts and breaks attract pelagics. |
| **Chlorophyll-a** | Phytoplankton indicator. Elevated near upwelling zones. |
| **Kd490** | Light attenuation / turbidity proxy from satellite. |
| **Upwelling** | Deep cold nutrient-rich water rising. Drives productivity. |
| **Back Reef Slope** | The slope behind the reef crest. 1,512 polygons from Allen Coral Atlas. |
| **EM710** | Kongsberg multibeam (10 m). Used for hardness/backscatter. |
| **CSIRO 2013 SF55** | Older 75 m hardness grid. Wider coverage than EM710. |
| **EM122** | Deep-water multibeam. REJECTED — do not bring back. |
| **Buffer zone** | GBRMPA zone where only trolling for pelagics is allowed (no bottom fishing). |
| **FAD** | Fish Aggregating Device (surface or submerged buoy). |

## This Repository (task-dashboard)

A React task-dashboard app that serves as a UI scaffold. Tech stack:

- **React 19** + **Vite 7** + **Tailwind 4**
- **Vitest 3** + React Testing Library for tests
- **Framer Motion** for animations
- **Heroicons** for icons

### Project Structure

```
src/
  App.jsx                          — Main app component
  context/
    TaskContext.jsx                 — Task state management
    MemoryContext.jsx               — Memory system React context (3-layer architecture)
  common/utils/
    MemorySystem.js                — Core memory module (Storage, Injection, Recall, Dreaming)
    MemorySystem.test.js           — 32 unit tests
  context/
    MemoryContext.test.jsx          — 9 integration tests
  features/tasks/components/
    TaskItem.jsx                   — Individual task component
rodney_handover/                   — RODNEY project handover files (see table above)
```

### Running Tests

```bash
npx vitest run          # all tests (100 passing)
npx vitest run --watch  # watch mode
```

### Memory System

A trial implementation of a 3-layer memory architecture:
1. **Storage** — saves every interaction (nothing filtered out)
2. **Injection** — curated ≤2000-char snapshot of important items
3. **Recall** — hybrid cosine similarity (60%) + keyword match (40%) with synonym expansion for domain terms (reef, benthic, substrate, current, tide, etc.)
4. **Dreaming** — merges duplicate/outdated snapshot items, keeps newer versions

The synonym map covers both general terms (pricing, payment, brand, task) and GBR fishing domain terms (reef, habitat, substrate, benthic, coral, current, tide, tidal, upwelling, flow, water, direction, knots, survey, dive).

## Important Conventions

- **Never present unsourced scores as catch fact.** Use "habitat cues" language, not "fish sightings."
- **Never hard-code closures dates.** Always read from the live feed with dated warnings.
- **Pelagics have no depth sweet spot.** They are judged on water features only.
- **EM122 is out.** Do not bring it back.
- **Features deeper than 150 m LAT are dropped.** No exceptions.
- **Point data first** (surveyed marks → HD8 10 m grid → GBR30 estimated fallback).
- **Mick's marks are the authority.** The register is the single source of truth for fishing marks.
- **Buffer zones are shown, not blanked** — labelled "troll only for pelagics."
- **Keep it honest:** label modelled data as MODELLED, label saved-copy dates, show source/quality.
