# HD9 v02 Build Checklist

Built from: carry-over audit (26 must-carry), features register (87 items, 20 LOST + 9 NEVER), Mick's 16-line checklist, and delivery plan gates G1-G9.

## Engine changes done in this session (outcomes a-d)

| Done | Outcome | What changed |
|------|---------|-------------|
| YES | (a) Remove 300m bonus | `evidence()` deleted, `marks300` bonus removed from `score()`, Mick's marks moved to held-not-used |
| YES | (b) Depth auto-convert | `msl_to_lat()` and `lat_to_msl()` functions added, used in `depth_at()` |
| YES | (c) Rubble rule + feeding triggers | `RUBBLE_RULES` with species-specific ranges, shallow reef-flat drop, `_load_feeding_triggers()` scaffold |
| YES | (d) Three engines | `score_demersal()`, `score_pelagic()`, `score_ambush()` with dispatcher `score()` |
| YES | (d+) Ocean layer scoring | `ocean_score()` method reads SST gradients, chlorophyll edges, upwelling proxy for pelagic scoring |
| YES | (d+) Plain-language marks | `plain_mark()` and `rank_with_marks()` methods output marks as natural English with GPS |

## Delivery plan gate G4 check (step 3 Engine)

- [x] Code contains no bonus term (300m removed)
- [x] Rubble search holds real rules (species-specific depth ranges, not a stub)
- [x] Plain "matches the criteria, here's a mark" line (`plain_mark()` method)
- [ ] Sample run on known marks (needs workspace data files)

## Remaining outcomes (e-i) - what each needs

### (e) Pelagic overlays on the map

**Engine side: DONE** - `ocean_score()` reads `ocean_layers_grid.json` for SST, chlorophyll, upwelling.
**Map side: needs HD9 v01 HTML** - Reg #15 says these are IN HD9 v01 already (9 pelagic water layers). Check they still work.

### (f) Seafloor shape-detection training set

Needs depth grid files, bommie model outputs, TIMEZERO captures. This is Seafloor Builder's task (delivery plan step 1).
Files needed: depth rasters, GBR30 tiles, bommie_pipeline.py outputs.

### (g) Refresh weather/tide/current feeds

Needs API access to: Open-Meteo, BOM Cairns, Copernicus Marine, Qld Open Data CKAN.
This is Reef Weather's task (delivery plan step 4). Plan B source order documented in delivery plan.

### (h) Append 272 rubble marks + 19 cleared candidates

Source: `/workspace/rodney/test_package/next100/` (rubble marks), `/workspace/shared_refs/Candidate marks check 10 November 2026/` (cleared candidates).
Target: Marks Master Register sheet `1ealiWuH6EpFzgNsGgeoKBh6JB438vyQD52f9u0Qds-M`.
**Mick must approve edits to that sheet.**

### (i) Build HD9 v02 - MUST-CARRY items

#### From carry-over audit (26 items mapped to register #)

| # | Feature | Audit status | Register # | Owner | Action |
|---|---------|-------------|-----------|-------|--------|
| MC1 | Four-corner layout | LOST | 62,64,66 | Map Builder | Restore HD4 layout: title TL, icons TR, readout BL, compass/zoom BR |
| MC2 | Live pointer readout (depth, GPS, zone) | LOST | 63 | Map Builder | mousemove handler, not click-only |
| MC3 | 3D terrain toggle | LOST | 2 | Map Builder + Seafloor | 3D panel with orbit, exaggeration control |
| MC4 | TIMEZERO/Sunset palettes, hillshades | LOST | 3 | Seafloor + Map | Rainbow relief, palette picker, hillshade options |
| MC5 | Fine contours + spot depths | LOST | 4 | Seafloor + Map | 1/2/5/10/20/50/100/200m selector |
| MC6 | White reef/island names | LOST | 5 | Map Builder | Floating white labels from GBRMPA features |
| MC7 | Tide curve + 72h chart + bite windows | LOST | 56 | Reef Weather + Map | Time slider with LAT tide curve |
| MC8 | Wind strip + green day rule | LOST | 58 | Reef Weather + Map | 12kn wind AND 1.2m seas = green |
| MC9 | Flood/ebb currents on slider | LOST | 57 | Reef Weather + Map | Arrows move with time slider |
| MC10 | Marks search | LOST | 28 | Map Builder | Type name, zoom to mark |
| MC11 | Species picker Demersal/Pelagic | PARTLY | 31 | Map Builder | Mode switch, not just checkboxes |
| MC12 | Today's waypoints + GPX/KML export | LOST | 30 | Map + Engine | Ranked card with export |
| MC13 | Satellite photo toggle | LOST | 8 | Map Builder | Opacity control, off by default |
| MC14 | Beacons + IALA colours | LOST | 9 | Map Builder | IALA shapes, tap for meaning |
| MC15 | Survey coverage footprint | LOST | 17 | Seafloor + Map | Measured vs modelled legend |
| MC16 | Evidence layers (tow, grabs, BRUVS) | LOST | 18 | Map Builder | Off by default |
| MC17 | Good ground highlights | LOST | 14 | Seafloor + Engine + Map | Pinnacles, ledges, edges, rubble, inside passages |
| MC18 | Hardness click-to-read | LOST | 12 | Map Builder | Click returns hardness rank value |
| MC19 | Zoning outlines toggle | LOST | 7 | Map Builder | Quiet, off by default |
| MC20 | Survey evidence layers | LOST | 18 | Map Builder | Off by default, tap for details |
| MC21 | Tide-adjusted depth at chosen time | LOST | 21 | Seafloor + Reef Weather | Live-tide mode from 3D artifact |
| MC22 | Trip planner drawer | NEVER | - | Map Builder | Date, ramp, times, species, range |
| MC23 | 3-day fishing outlook on map | PARTLY | 59 | Engine + Map | Three dated days with verdict |
| MC24 | Back reef slope toggle | NEVER | 23 | Seafloor | Optional, labelled modelled |
| MC25 | Environment snapshot drawer | NEVER | - | Map Builder | Small conditions summary |
| MC26 | Bottom temperature layer | NEVER | 20 | Data Scout + Map | Off by default, "model estimate" or "not available" |

#### From register - NEVER BUILT items not in carry-over

| Register # | Feature | Owner |
|-----------|---------|-------|
| 46 | Pelagic engine on water features | Engine Bot PC | **ENGINE DONE** |
| 47 | Ambush Points scorer | Engine Bot PC | **ENGINE DONE** |
| 55 | Live current under pointer | Reef Weather + Map |
| 67 | App purpose line (Mick's 8:39pm words) | Map Builder |
| 10 | Spoken danger warnings | Map Builder (low priority) |
| 22 | 3D teaching models of regular reefs | Seafloor (low priority) |
| 68 | Built-in chat wired to map | Engine + Map |

## Mick's 16-line checklist status

1. [x] Planning assistant, not inspector - rule applied throughout
2. [ ] Opens on best detailed view - PARTLY (not full screen)
3. [x] Best depth grid, unsmoothed readouts - IN v01
4. [x] One "Mick's marks" toggle, plain names - IN v01 (names partly blank)
5. [x] Demersal sweet spot first, pelagic no depth - ENGINE DONE
6. [x] No-take removed, seasonal CLOSED short line - IN v01
7. [x] Zone display rules (Green hidden, Yellow one line, Buffer troll) - IN v01
8. [ ] Tides/currents by hour + ambush points - ENGINE DONE, map LOST
9. [x] Pelagic water overlays on map - IN v01 (9 layers)
10. [x] Hardness EM710 + CSIRO separate, GBR10 MODELLED - IN v01
11. [x] Route check toggle, passage markers excluded - IN v01
12. [ ] Clean layout any size - PARTLY (top bar + side panel)
13. [x] Sequential versions, backup first - IN v01
14. [x] No needless questions to Mick - rule applied
15. [ ] Progressive improvement from all earlier versions - LOST 20 items
16. [ ] No new version unless it beats previous - blocked by #15
