# RODNEY Engine Status

**Bot:** Engine Bot PC (this session)
**Branch:** `sesh/inspiring-dirac-s7zsf3`
**PR:** [Felixmics/task-dashboard#19](https://github.com/Felixmics/task-dashboard/pull/19)
**Last push:** 2026-11-21
**Engine alignment:** COMPLETE — handover engine is the single source of truth

## Delivery plan step 3 (Engine) — gate G4

| Gate check | Status |
|-----------|--------|
| Code contains no 300m bonus term | PASS |
| Rubble search holds real rules | PASS |
| Plain-language mark output | PASS |
| Feeding triggers wired (tide + moon) | PASS |
| Sample run on known marks | BLOCKED (needs workspace data) |

## Engine file: `07_rodney_engine.py`

Zero TODOs remain. All scoring paths implemented:

- **Demersal** (`score_demersal`): depth sweet spot, structure fit, current, rubble rules, feeding triggers
- **Pelagic** (`score_pelagic`): water features (SST gradient, chlorophyll edge, upwelling proxy), current, feeding triggers
- **Ambush** (`score_ambush`): pressure point ranking, reef face/slope classification, current timing, feeding triggers

## Changes this session (5 commits)

1. `4c9a64a` — Outcomes (a)(b)(c): remove marks bonus, depth auto-convert, rubble rule
2. `527c725` — Outcome (d): split `score()` into three engines
3. `97c5fdd` — Pelagic ocean scoring + plain-language marks + HD9 v02 checklist
4. `2e2e67c` — Feeding triggers: tide phase + moon phase matching, wired into all three engines
5. (pending) — HD9 v02 HTML: restored MC2 mousemove, MC10 search, MC11 species mode, MC12 export, MC13 satellite, MC19 zoning

## Engine alignment (21 Nov 2026)

The handover engine (`07_rodney_engine.py`) supersedes the Grok-built original (`rodney_engine.py`, 14 Nov).
Full diff: `09_engine_alignment.md`. Grok reference copy: `grok_engine_14nov_reference.py`.

Key upgrades from Grok → handover:
- Cutoff: 120 m → 150 m LAT (120-150 m labelled "deep")
- Formula fix: `-(CUTOFF + MSL)` not `-(CUTOFF - MSL)` — the -118.26 bug is gone
- Three separate scoring engines (demersal/pelagic/ambush) replace single `score()`
- Pelagics scored on water features, NOT depth (Mick 21 Nov 7:32 pm)
- Sweet spots, buffer zones, rubble rules, feeding triggers, dynamic closures, G12 tracking
- Points: 60,847 rows at 150 m (was 60,446 at 120 m)
- Manifest: engine_sources_2026-11-17 (was 2026-11-12)

Test results on the Grok engine (14 Nov): **85 PASS / 1 WARN / 0 FAIL**

### Waiting on Mick's go (from Test Package)
- 3 of 11 items DONE (formula fix, 150 m table, seabed hardness)
- 1 READY but blocked (rubble marks append — needs source files)
- 7 PENDING (HD8 rebuild items + structure method v0)

## Zoning screen (24 Nov 2026)

`10_zoning_screen.py` performs point-in-polygon against GBRMPA Zoning Plan 2003 polygons
(`GBRMP_zoning_Cairns_corridor.geojson`, 38 zones, from Mick's Drive `gbrmpa_zoning` folder).

**Results on 3,350 marks:**
| Status | Count |
|--------|-------|
| Line fishing OK (General Use + Habitat Protection) | 1,727 |
| Limited (Conservation Park, 1 line 1 hook) | 344 |
| **NO TAKE (Marine National Park + Preservation)** | **337** |
| Special rules (Commonwealth Islands) | 1 |
| Outside zoning polygons (check chartplotter) | 941 |

**337 marks are in NO-TAKE zones** — these must be flagged or removed before the register is used.
Key reefs affected: Norman, Saxon, Hastings, Michaelmas (all MNP-16-1050), Moore, Milln, Euston, Briggs/Sudbury, Green Island, Scott, Low Islands.

Zoning results written to new Google Sheet: [RODNEY Mastermark 2026-11-25 (zoned)](https://docs.google.com/spreadsheets/d/14h0qNUnsFrNiBLn4Crxzm9YXax3ydb3TBtQrYsOidSY/edit)
Columns T (zone) and U (legal_screening) populated for all 3,350 marks. Original sheet unchanged.

## Blockers for other bots

| What | Who | Why |
|------|-----|-----|
| HD9 v01 HTML | Map Builder | DONE — downloaded, used as base for HD9 v02 |
| Depth grids | Seafloor Builder | Needed for outcome (f) shape-detection training |
| Feed refresh | Reef Weather | Stale since 19 Nov, outcome (g) |
| Sheet append approval | Mick | 272 rubble + 19 cleared marks, outcome (h) — APPROVED, needs source files |
| HD8 rebuild | Seafloor Builder | 7 pending items need updated HD8 (Melville, Falkor, north strip) |
| Structure method v0 | Engine Bot | Weights defined, not yet wired into engine |
| 150 m raster grids | Seafloor Builder | Point table done; depth_msl and gbr30 rasters still at 120 m cut |
