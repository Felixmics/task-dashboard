# Mick's requests: one chronological list (oldest first)

**Written:** 21 November 2026, about 10:45 pm Brisbane time (UTC+10), for Rodney Boss to brief Mick.

This was a read-only pass:
- This is the only file written.
- No bot was resumed or messaged, and nothing else was edited.

**This version adds Mick's 10:20 pm and 10:22 pm requests:**
- every map feature;
- a highlighted Claude maps section (marked ★);
- every web interface, UI layout and look-and-feel discussion, tagged **[UI]**, with each one marked **UI: refined** or **UI: open**.

## What could and couldn't be reached

**Rodney Boss's main chat with Mick: NOT reachable.**
- ReadTranscript and SearchTranscripts with no agent filter open only this helper's own session.
- `in: "main"` and `in: "parent"` both return "no session … you can read from here". The tool reads none of the main chat.
- The main-chat words that do appear here come only from Rodney Boss's records:
  - memory: behavior `/bot/rules` and `/me/profile`, which hold most of the 21 Nov decisions with times;
  - verbatim relays into bot chats;
  - the 21 Nov start-up stack and briefs.
- **This matters most for the UI.** The 20 Nov UI brainstorm and the AI Reef Tririp review happened in the main chat. They are covered here only through:
  - the brainstorm checklist (`/workspace/shared_refs/RODNEY UI design brainstorm 2026-11-20/AI Reef Tririp review and feature checklist.md`);
  - about 12 dated memory facts from 20 Nov.
- The brainstorm folder's `screenshots/` subfolder is empty on the box, and the 50 MB Tririp zip was not opened.

**Reached:**
- All 7 bot chats, searched for the feature phrases plus: Claude, artifact, Tririp, Reef Trip, layout, UI, four-corner, drawer, chartplotter, toggle, cluttered, screen, font, look, web page.
- About 230 dated memory facts.
- The Blueprint v1.2 (D-001 to D-025).
- The register (#1-#87), the must-carry list (MC1-MC26) and the brief (F1-F62).

**Dates:**
- Chat items have no timestamps, so they're dated with date-filtered searches and shown as ranges.
- Memory and Blueprint items carry their own date. Exact times are given where Rodney Boss recorded them.

**Wording:**
- **exact** = Mick's own typed or voice words, with his spelling. "(cut)" means the search snippet ended there.
- **close** = a memory, Blueprint, checklist or relay summary.
- **prompt-style** = a third-person prompt sent from Mick's account.

**Status codes:**
- **NEW**: still wanted under today's objectives, not yet in the register, must-carry list or brief.
- **REC**: already recorded (register #, MC, F or D number given).
- **REPL**: replaced by something better (named).
- **OPEN**: raised but never decided or finished.

Rows numbered like "8a" were added in this pass. They keep the list in date order without renumbering the earlier rows.

## ★ HIGHLIGHTED: Claude maps and Claude map features (oldest first) ★

> **Mick 21 Nov 10:43 PM:** the Claude items are only the beginning of the old Claude design review; it is not finished, so this is not the full map feature set.

Mick wanted the good parts of the Claude map versions taken across into RODNEY. Every mention found is listed here. The same items also appear in the date tables below, marked ★.

**Claude artifacts named in the chats:**

| Artifact link | Where it was mentioned |
|---|---|
| `GW8QddgVmMEW1RqqSPaLg3` "Cairns GBR corridor bathymetry (v2: 16 m detail)" | Rules & QA |
| `TUNJm3gkYXKdRCZzTAWYLG` | Seafloor Builder |
| `SAAzPK67qqBYCTvvimwSQy#fish`, the upwelling one | Seafloor Builder, sent for review with the weather bot |
| `9daqE2sVUESx5Pcy2yeuWP`, the "October 4 AI REEF" board | Seafloor Builder and Data Scout |
| `KLB9TJDPfM9PpzKrSfVf9i` | Seafloor Builder |
| `B99KzR15uSaZSK3C9Z2CYZ` | Seafloor Builder, which Mick called "along way from being accepted" |
| `PKqaBMocv6zyh5y1LZEnwx` "3D Bathymetry Map" | Seafloor Builder |
| `XZxQhL7TgtYJRzLkV9cMEA` "Coral Trout Conditions Dashboard" | Seafloor Builder |
| `6obxLy4LNb9tHfaK9Bw6eD` "AI Reef Tririp html app" | 20 Nov UI brainstorm |

Most of these need a Claude sign-in, so the bots saw only screenshots or public captions. The exception is the Tririp, which was opened from the public link and screenshotted. No file shows that Claude's code exports ever arrived in the 23_AI_Handoff folder.

| # | When | Claude element | Mick's wording | Later improved, superseded or built? | Status |
|---|---|---|---|---|---|
| C1 | Before 28 Oct, Map Builder | Go through the Claude, Grok and ChatGPT files and use the best parts of each | exact: "im looking to make some sense of the files and artifacts as some have good items … i want though to investigate claude and grok and chatgpt file to use when they are best" | Map Builder's inventory found 115 Claude files: live dashboards, a tide scanner and tidy indexes. 21 Nov 8:47 pm: progressive improvement | REC #78, F60 (method) |
| C2 | Before 28 Oct, Map Builder | Claude "3d with zoning" / "3D Bathymetry" phone page used as a look reference | exact: "I KNOW ONE IS A CLAUDE ARTIFACT // THE OTHERES NOT SURE" | hd5 took the shading from Map Builder's own Reef Ranger build and avoided the Claude page's blur and crowded depth lines | Refined. See C6 |
| C3 | Before 1 Nov, Rules & QA | Claude's diagnosis: its 3D loses detail because the mesh is about 4x coarser than the 30 m data; fixes for texture and lighting | exact: "This is what claude says … The 3D view loses detail mainly because its terrain mesh is about 4x coarser than the 30 m source data" | HD8/HD9 use the 10 m grid. 3D was lost in HD9 v01 | REC #2, MC3 (must rebuild at full detail) |
| C4 | 1-3 Nov, Seafloor Builder | Claude dashboards (Trout Decision Board and others): keep the features, but make the front professional and fisherman-first: where, why, when, wind, tides | exact: "we'll build, build it into the app with the toggles on the front and make that look like it's professional, not like it's a ten-year-old scribble … I'm a fisherman, I'm just gonna go fishing zone, right? Where, why, when, what's the wind doing, what's the tides" | 20 Nov four-corner layout and Tririp review. The "where/why/when/wind/tide front" is still the open landing-page question | REC in part (#62, #70 landing page). UI: still open |
| C5 | 1-3 Nov, Seafloor Builder | Claude to export each artifact's code and output into the 23_AI_Handoff folder so the bots can read them in full | exact: "give Claude that handover thing from that email … I'll pass it to Claude" | No sign the exports arrived | OPEN |
| C6 | 10 Nov (rule) | Depth or tide data from Claude artifacts converted to LAT on intake | close: "any outside depth or tide data pulled in (other viewers, Claude artifacts …) gets converted quietly to the house rule" | No | REC #73 |
| C7 | 12 Nov (memory) | ★ Claude "3d with zoning" 2 Oct 11:30 snapshot: 16.5x height, contour lines, colour bands from red shallows to blue drop-offs. "A couple of tweaks would almost get them there" | close: "a look they really like for the RODNEY/HD8 map" | Fed into the rainbow relief (#3), fine contours (#4) and a sensible default exaggeration (#2). All three were LOST in HD9 v01 | REC #2, #3, #4; MC3-MC5 (carry) |
| C8 | 12 Nov (rule) | Claude point outputs (marks, rubble, habitat CSVs) count as part of the RODNEY database | close: "point and candidate Sheets and CSVs (QGIS scans, Claude outputs …) are part of the RODNEY database" | 21 Nov 6:38 pm: "No, blend the point data in." | REC F6/F56 (blend rule NEW, row 148) |
| C9 | 20 Nov, Tririp item 1 | Live conditions strip: time, weather and tide summary, data age warning, one-click Refresh, works offline | checklist (Mick-approved list) | Not reviewed one by one yet | REC in part (#16, #60). UI: open |
| C10 | 20 Nov, Tririp item 2 | Pelagic / Demersal switch, compact, not big bars | checklist | 21 Nov two engines and pelagics on water | REC #31 |
| C11 | 20 Nov, Tririp item 3 | "Best marks today" picker: reef dropdown ("AI picks the reef" plus about 70 reefs) and species buttons | checklist | Not reviewed yet | REC #30, #31; reef dropdown NEW (maybe) |
| C12 | 20 Nov, Tririp items 4, 6 and 9 | Saved trip shortlist; Sources / data status / satellite passes ("More"); landing page | checklist | Not signed off | REC #70 (wish list). UI: open |
| C13 | 20 Nov, Tririp item 5 | Weather and tide drawer, offline from saved packs | checklist | No | REC MC22, #56 |
| C14 | 20 Nov, Tririp item 7 | Tap a reef: coordinates, depth (m LAT), reef name, zone, mark count | checklist | No | REC #63, MC2 (mark count NEW, small) |
| C15 | 20 Nov, Tririp item 8 | RODNEY chat inside the four-corner screen; jumps to a mark on the map | checklist | No | REC #68. UI: open |
| C16 | 20 Nov, like | ★ Clean white 2D reef-label font: proportional size, symmetrical | close: "candidate to use in RODNEY" | No | REC #5, MC6 |
| C17 | 20 Nov, like | ★ Best detail on by default (multibeam and backscatter on when the map opens) | close: "present the best, sharpest visual view straight away" | No | REC #1 |
| C18 | 20 Nov, like | ★ Pelagic overlays drawn on the map: Sea temperature, Chlorophyll, Cold water | close: "great for pelagic fishing and not yet rendered visually on RODNEY's map" | Two Tririp bugs to avoid: no temperature legend, and the overlay didn't toggle off | REC #15. The legend and toggle-off fix is NEW (small build note) |
| C19 | 20 Nov, like | Tririp layer menu grouped as Base views / More layers / Water and surface layers | checklist | Not decided against two stacked layer buttons (#64) | NEW (maybe; menu grouping). UI: open |
| C20 | 20 Nov, More panel | Quick Wind, Swell and Windy buttons; an Advanced toggle (off by default); a live status line (fishing window, pull time, SST and chlorophyll dates, "under 10 m flagged Shallow", satellite passes) | close (Mick's signed-in photos) | Not reviewed yet | OPEN (Tririp review item 6) |
| C21 | 20 Nov, dislike | ★ Upwellings opens a separate web page. Keep everything inside the app | close: "does not want RODNEY features such as upwellings to open a separate web page" | No | REC #65 |
| C22 | 20 Nov, dislike | ★ Tririp too cluttered: oversized boxes, too many toggles hiding the screen, heavy top stack, overlapping drawers, floating bottom dock, colour clashes. Keep the features, uncluttered at any screen size | close: "he wants those features kept, but RODNEY designed so the layout stays uncluttered and holds together cleanly at any screen size" | No | REC #65, #62. UI: open (design not signed off) |
| C23 | 20 Nov, engine | ★ Rejected the Claude-app habit of nearly always highlighting cold water up the outer shelf, which missed the mid-shelf ambush story | close: "he does not want the Claude-app approach of almost always highlighting cold water coming up the outer shelf" | Replaced by water-line features plus mid-shelf reef-face ambush points (20-21 Nov) | REPL by #46, #47 |
| C24 | 20 Nov, method | Side-by-side feature comparison only, one item at a time. For each missing feature, say whether the Claude script can be reused or should be built cleaner on RODNEY's engine. RODNEY stays the higher standard | close: "for each missing feature, also say plainly whether their script/logic can be reused or should be built cleaner" | Review paused on the night of 20 Nov. Items 1-9 are all unticked | OPEN (brainstorm unfinished) |
| C25 | 20 Nov, note | Tririp runs on the 30 m GBR30 MSL seafloor and old SST and chlorophyll composites. RODNEY's HD8 LAT base is stronger | checklist | No | Note only: take the features, not the data |

**What is worth carrying across from the Claude maps, in one line:**
- **From the C7 look:** the "3d with zoning" relief, contours and red-to-blue bands.
- **From the Tririp:** the white reef labels, best detail on at open, pelagic sea temperature, chlorophyll and cold-water overlays (with a legend and a working off switch), a compact Pelagic/Demersal switch, the best-marks-today picker, the weather and tide drawer, the tap-a-reef readout, chat in the map, and the data-status line.
- **Left behind:** the clutter, separate web pages, the outer-shelf cold-water bias and the GBR30 MSL data.

**Built?** Not yet in HD9 v01, apart from the pelagic overlays (#15) and the toggles (#6).

## ★ FOUNDATION: how RODNEY works with its core data (dated, oldest first) ★

The idea from the start: a **static base** of Mick's marks and CSVs, survey evidence (BRUVS, tows, grabs, photos) and species files, with a **dynamic layer** (tide, currents, wind, sea temperature, chlorophyll, upwelling, moon, season) laid over it to give "where and when".

This was checked against the code in `/workspace/shared_refs/Project Library/rodney_engine.py` (555 lines, the 21 Nov 150 m version), the Blueprint v1.2, `RODNEY_STARTUP_STACK.md` and the full project brief.

### 1. Static data files: Mick's CSVs, marks and point registers

All of them load into one point table, `/workspace/rodney_root_index/filtered_150m/RODNEY_points max150mLAT hd8check G3 2026-11-21.csv.gz`, which has 60,815 rows. It is the engine's `POINTS_ENGINE`.

**Rows per dataset, as counted tonight:**

| Dataset | Rows |
|---|---|
| tools_candidates_with_coords_2026-11-01 (QGIS terrain scan candidates). Source copy: `/workspace/rr_register/tools_candidates_with_coords_2026-11-01.csv` | 41,844 |
| MASTER_waypoints_2026-10-30_v2 | 5,747 |
| AHO soundings (reference only, never a spot) | 2,523 |
| **Reef Ranger Master Marks Register (1)**, the RODNEY Marks Master Register 150 m copy | **1,961** |
| wangliu_holes_2026-11-01 (wonky-hole candidates) | 1,685 |
| coral trout habitat | 1,633 |
| RUBBLE_patches_2026-10-31 | 1,442 |
| CoralSeaMP fishing features | 792 |
| REAL_marks_species_v2_2026-11-01 (real marks with species) | 761 |
| red-throat emperor habitat | 643 |
| **GBR30_Isolated_Bommie_GPS_Coordinates.csv**. Older copies in `/workspace/map-models/Model 4/5/6 …/private_marks/project2/` | 320 |
| nannygai habitat | 274 |
| **GA sediment samples** (`GA_sediment_samples_Cairns_box_le121.74m.geojson`) | 234 |
| **BRUVS_Cairns_drops_enriched_v2_2026-10-31** | 233 |
| **Project 2 - GBR30 WGS84 Fishable Candidate Register** | 231 |
| Shared Ranked Marks | 107 |
| Spanish mackerel habitat | 104 |
| wrecks and obstructions | 101 |
| red emperor habitat | 61 |
| PELAGIC_seasonal_2026-10-31 | 48 |
| FADs | 34 |
| ramp distances (reference only) | 34 |
| Mick's 9 Nov sediment marks | 3 |

**TIMEZERO and iBoat exports:**
- `/workspace/tz/TZiBoatData_2026-10-18_1323.gpx` was used in the HD2-HD6 map models.
- It is NOT a separate dataset in tonight's point table. Its marks came in through the master register.
- The **Marks Master Register** itself is the Google Sheet `1ealiWuH6EpFzgNsGgeoKBh6JB438vyQD52f9u0Qds-M`. Its box cache is `/workspace/rodney_root_index/cache/…csv`, with an xlsx copy in `/workspace/tmp_rodney_pkg/`.

**How Mick's marks are used today:**
- **Mick's marks are evidence, not positions.** Each one adds a small bonus to any candidate within 300 m (+0.05 each, up to +0.2).
- The engine's candidate spots come from the model, structure, habitat and BRUVS points plus the pressure points.
- This is in the code (`candidates()`, `evidence()`) but **not written in the register or brief**. Mick should know and confirm it (see the table).

| # | When | Step | Mick's wording | How it evolved | Status now |
|---|---|---|---|---|---|
| D1 | 27 Oct, Blueprint D-007 and D-017 | Use the existing waypoint database first. New evidence-backed candidates allowed. Every approved mark saved and findable | close: "Rodney MUST consider the existing waypoint database … and MAY also identify new evidence-backed candidate coordinates" | Became the point table and the register | REC D-007, D-017. "Saved and findable" is NEW for the brief |
| D2 | 25-31 Oct, Seafloor Builder | Gather every waypoint from Sheets, Drive, TZ, KML and GPX into one place | exact: "Go and find the Google Sheets. The Google Drive files. The TZ files. The KML files. The GPX files, and put them all together." | MASTER_waypoints v2 (30 Oct). Then the Marks Master Register (17-19 Nov) | REPL by #24 (the register) |
| D3 | 30 Oct (memory) | Generated marks appended to "Database Grok Organized" 16_Waypoints, deduped within 100 m | close: "append-only with run_id, deduped within 100 m" | The Blueprint's R2 conflict says no dedupe should DROP a mark | REPL by #24 (pass-tested marks only) |
| D4 | 25 Oct-1 Nov, Seafloor Builder | Split real marks from grid points; keep existing notes | exact: "don't wipe out the ones that already do have good … feedback or data" | `REAL_marks_species_v2_2026-11-01` (761) exists in the point table | The split is BUILT as data but unrecorded. Keep-notes is NEW |
| D5 | 1 Nov | GBR30 terrain scans: isolated bommies (320) and the Fishable Candidate Register (231), plus QGIS tools_candidates (41,844) | close: from Mick's Project 2 files | Loaded as engine candidates and labelled "GBR30 terrain candidate (bommie)" | BUILT in the engine (F58). Not itemised in the register: NEW (record it) |
| D6 | 12 Nov (rule) | His Drive point Sheets and CSVs (QGIS scans, Claude outputs, marks, BRUVS, rubble, habitat) ARE the database. Check point data before the 30 m grid | close: "the engine and chatbot must check that point data for a location before falling back on the 30 m grid" | Locked lookup order: point data, then fine grids, then GBR30 | REC F58, #54 |
| D7 | 12-13 Nov | Private marks: in, then out, then a separate folder | close | 21 Nov: "there are no private marks", one register behind the "Mick's marks" toggle | REPL by #24 |
| D8 | 18-19 Nov | One Marks Master Register; species saved with each mark; plain names; about 3,350 marks in the stick package | close: "the marks database of about 3,350 points" | The 150 m copy holds 1,961. The 1,961 vs 3,350 gap is still open | REC #24, #26, #27. OPEN: which set counts |
| D9 | In code (date not recorded) | Mick's marks are evidence near candidates, not candidate spots themselves | none from Mick found | — | OPEN: Mick to confirm. He may want his marks ranked as spots too |

### 2. BRUVS and other survey evidence

| # | When | Step | Mick's wording | How it evolved | Status now |
|---|---|---|---|---|---|
| E1 | 27 Oct, Blueprint Phase 4 and R5 | Join bathymetry, habitat, BRUV and environmental data. BRUVS observations, model ranks and real marks are different kinds of evidence; survey rows can't be counted as proven marks | close: "BRUVS observation, bottom morphology, model rank, actual verified fishing mark … are different evidence types" | No | REC (Blueprint only) |
| E2 | 31 Oct | `BRUVS_Cairns_drops_enriched_v2_2026-10-31.csv` (233 drops) at `/workspace/marine_db_v5/06_Private/Fish_Evidence/BRUVS_Cairns_2026-10-31/`. The AIMS BRUVS sites come from eAtlas | close | A MUST file in the start-up stack. The engine uses BRUVS drops as **candidate spots** ("BRUVS drop site") | BUILT in the engine |
| E3 | Before 28 Oct, Map Builder | Click a spot for a seabed photo of what it actually looks like | exact: "click on the map, and then … a photo come up showing you … this is what it actually looks like" | HD6 overlays had rubble transects, fish records, BRUVS, habitat, Halimeda and table coral (`overlays.js`, 150 m copy of 21 Nov) | LOST in HD9 v01: REC #18, MC16, MC20, F44 |
| E4 | 3 and 15 Nov | GA sediment samples (234 points, file of 15 Nov) and the sediment leads | close | In the point table. `sediment_leads.geojson` is in the HD8 habitat data | BUILT as data |
| E5 | 14 Nov | BRUVS / DropCam / GBR10 habitat notes extracted for the RAG (`/workspace/shared_refs/RAG/sources/extracted_2026-11-14/HABITAT_BRUVS_DropCam_GBR10.md`). Optional BRUVS pack copied to the RODNEY Drive | close | No | REC F57 |
| E6 | 14 and 17 Nov | Manta tow and towed video, plus hard-ground labels (5 hard tows, 13 gravel grabs, 57 soft tows) as training labels | close | F1 Input 12 | REC F1, F4 |
| E7 | 21 Nov | Evidence layers (tows, grabs, BRUVS, Halimeda, photos) labelled evidence, not marks, off by default, in the lookup order | close | — | REC F44, F58. Map layer NOT rebuilt |

### 3. Species files and how they link to marks

| # | When | Step | Mick's wording | How it evolved | Status now |
|---|---|---|---|---|---|
| S1 | 27 Oct, Blueprint section 6 | Rodney knows the species patterns (trout, red emperor, nannygai and others) like an experienced reef fisherman | close: "speaks like an experienced reef fisherman, without pretending he knows today's catch" | 12 Nov: every bot knows the when, where and why | REC |
| S2 | 25-31 Oct, Seafloor Builder | One preferred-habitat file per species | prompt-style: "build a per-species preferred-habitat file for each of the five species" | Built 31 Oct: coral trout, red emperor, nannygai, red-throat emperor and Spanish mackerel `*_preferred_habitat_2026-10-31.csv`. In the engine, a candidate on a species' habitat point gets +0.15 | BUILT in the engine but unrecorded: NEW (record it, and extend beyond 5 species) |
| S3 | 25-31 Oct | Every mark scored for each species; mixed-species cut-off 70 | exact: "I want every mark. They are all my marks." | Replaced by sourced per-species scoring at engine run time | REPL by engine `rank()` (F16) |
| S4 | 25-31 Oct | Seasonal pelagic layer | prompt-style | `PELAGIC_seasonal_2026-10-31.csv` (48) is in the point table. A season factor multiplies the score | BUILT as data but unrecorded: NEW (record it) |
| S5 | 8 Nov (memory) | Red emperor marks on rubble and hard bottom; coral trout on reef edges, back-reef slopes and pressure points; marks spaced out, togglable, shown unverified on unsurveyed ground | close: "shown as unverified when on ground that has not been surveyed" | Engine structure fit matches each species' bottom and zone. Depth tagged measured or estimated | REC in part (#14, #26). The "unverified" label is NEW (small) |
| S6 | 10 and 12 Nov | Species file merged; then the 20-species `RODNEY TARGET SPECIES - FINAL.md` (DE01-DE10, PE01-PE10) under Demersal and Pelagic; tests cover all 20 | close | Engine loads `marine_db_v5/13_Species/species_reef_demersal_v5.csv` and `14_Pelagic/species_pelagic_v5.csv` plus the 12 Nov profiles | REC (brief section 4) |
| S7 | 14 Nov | "Engine photos": the per-species workflow flowchart (`/workspace/shared_refs/Project Library/engine_photos/engine_photo_1.jpg`, `_2.jpg`) | close | Workflows in `RAG/workflows/workflows_index.json` | REC F20 |
| S8 | 14 Nov | Coral trout marks spread across 10 m depth bands | close | — | REC #44 |
| S9 | 19 and 21 Nov | Sweet-spot depth per demersal species (red emperor 40-80 m) shown first; pelagics never judged on depth | exact: "WHY WOULD PELAGIC NEED DEPTH" | Engine `SWEET` table, sweet-spot spots ranked first; `PELAGIC_NOTE` | BUILT (#32) |

### 4. Dynamic conditions on top of the static points

| # | When | Step | Mick's wording | How it evolved | Status now |
|---|---|---|---|---|---|
| W1 | 27 Oct, D-008 and D-009 | Refresh weather on open; eReefs feeds Rodney's own store | close | eReefs near-real-time stopped in Jan 2024 (Blueprint note). RECOM rebuilt instead | REC #60 |
| W2 | 25 Oct-5 Nov, Reef Weather | Tide is the biggest factor in every "fish here" | exact: "apply the tide, since it's the biggest factor … to every generated fishing advice" | **In the code, only the tide-driven RECOM current speed in the bite hours is scored** (`cf = 0.6 + 0.4·min(kn/0.4,1)`). Tide height and phase are not scored | REC #51. Gap: the tide stage isn't in the scoring |
| W3 | 25-31 Oct, Seafloor Builder | 3-day forecast: static and dynamic layers, morning and afternoon windows | prompt-style | `marine_db_v5/06_Private/Forecast_3Day/forecast_3day_wind_v2.py` exists, separate from `rodney_engine.py` | PARTLY (F22). The windows are NEW (maybe) |
| W4 | 10 Nov | Flood and ebb currents tied to the slider; pressure points ranked for today (black P) | close | RECOM pressure points with daily ranks out to 4 Dec. Engine: +0.15 to a ranked pressure point, +0.1 within 1 km | BUILT in the engine (#48). The map P layer is LOST |
| W5 | 10 Nov | Wind regimes (northerly lee-face advice); green day = 12 kn and 1.2 m | close | `wind_regimes v2.json`, chosen for the engine | REC #58, F36. **Not read by `rodney_engine.py` scoring** |
| W6 | 12 Nov | Every dynamic factor rolling, never stale, 10 days ahead, says when it's short | close | Wind feeds stale since 19 Nov, 4:51 pm (Engine Bot PC, 21 Nov) | REC #16, #60. Feeds need refreshing |
| W7 | 12 Nov, Engine Bot PC (60) | Static and dynamic kept separate: "a reef doesn't move" | exact: "tell Rodney to make sure the bots know what's static … a reef doesn't move" | One RAG, static layers first, then dynamic with timestamps | REC #50, F57 |
| W8 | 14 Nov | Copernicus SST, currents and chlorophyll at least 10 days ahead | close | No login on the box yet, so the model upwelling is empty | REC F59. Blocked |
| W9 | 20-21 Nov | Pelagics judged on water lines (SST breaks, chlorophyll edges, upwelling) plus mid-shelf ambush points by the hour | close: "combine them with mid-shelf reef-face tidal ambush/pressure points so it can call a good fishing line for the day" | `/workspace/reef-app/feeds/cache/ocean_grids/ocean_layers_grid.json` (0.02°) is built and on the map. **`rodney_engine.py` does not read it yet.** The start-up stack calls it "additive score bonus", but no engine code uses it. The Ambush Points scorer is not built | REC #45-#47. NEVER BUILT in the engine |
| W10 | In code | Moon and bite hours: fixed default hours, night species (red emperor, nannygai and others) at 4-6 am and 6-9 pm, season factor, CLOSED label | none from Mick found | 21 Nov: CLOSED labels deferred | PARTLY. The moon isn't in the scoring |

**In plain words, here is how "where and when" works today:**
1. The engine takes the static candidate points: the terrain scans, habitat and rubble points, BRUVS drops, wonky holes, GBR30 bommies and pressure points.
2. It drops anything deeper than the depth limit or in a no-take zone.
3. It scores each candidate for the chosen species, multiplying together:
   - the depth sweet spot (demersal only);
   - the structure match;
   - the tide-run strength in that species' bite hours;
   - the inshore or mid-shelf fit.
4. It then adds bonuses for:
   - a species habitat point;
   - Mick's marks within 300 m;
   - the pressure-point rank today.
5. Finally it multiplies the score by a season factor.

**Not yet in the "when":**
- wind;
- tide height or stage;
- moon;
- sea temperature, chlorophyll and upwelling (which only show on the map);
- the Ambush Points scorer.

## The full chronological list

### Before 28 Oct 2026 (early Map Builder chat)

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 1 | Before 24 Oct, Map Builder | [UI] PC first, phone app later | exact: "just build it for like a PC for PC at the moment, then we can convert it to … app to mobile phone later" | Offline on the boat added 1 Nov. UI: refined | REC #69 |
| 2 | Before 28 Oct, Map Builder | Keep marks off the map until map quality is seen | exact: "don't put the marks on the map just yet … so they can see the quality of the map before you cover it in marks" | 18 Nov / 21 Nov: the "Mick's marks" toggle | REPL by #24 |
| 3 | Before 28 Oct, Map Builder | Understand marine park zones | exact: "you need to understand the zoning laws" | 21 Nov 8:38 pm: no compliance role. The display rule stays | REPL by #35 and #80 |
| 4 | Before 28 Oct, Map Builder | Grafton and Trinity Passages are fishing water | exact: "You can, you can fish in Grafton Passage and you can fish in Trinity Passage … it's not really a problem" | Separate from the 7:37 pm passage-marker rule | NEW (maybe) |
| 5 | Before 28 Oct, Map Builder | CSIRO MNF credit for IN2022_V07 in outputs | exact (licence text Mick pasted): "The MNF must be acknowledged in all outputs derived from Data …" | Joined by the 8 Nov credits rule (#59) | NEW (licence, Mick's call) |
| 6 | Before 28 Oct, Map Builder | [UI] Satellite as a toggle, not the main screen | exact: "as a toggle so that I can turn it off … I don't want it as the main" (cut) | UI: refined (toggle list) | REC #8, MC13 |
| 7 | Before 28 Oct, Map Builder | Click the map for a seabed photo of that spot | exact: "click on the map, and then … a photo come up showing you … this is what it actually looks like" | See core-data E3 | REC #18, MC20 |
| 7a | Before 28 Oct, Map Builder | [UI] Keep the original colour look; the new map's colours are poor | exact: "i want to seee the original as the new map look shit in colour" | 8 Nov rainbow relief and the TIMEZERO look. UI: refined | REC #3 |
| 8 | Before 28 Oct, Map Builder | [UI] 3D toggle, full screen, two stacked layer buttons whose menus close after you choose, depth and GPS shown, orbit wheel, floating reef names | exact: "ok 3d toggle required , map to open full screen and 2 stcked layer butttons will then bring up menus to selevt and then hide once selection made, depth and gps muts be displayed and 3d orbitol wheel . floating reef name stoo." | First UI spec. Refined by the 20 Nov four-corner layout. UI: refined, but most of it was LOST in HD9 v01 | REC #1, #2, #5, #63, #64; MC1-MC3, MC6 |
| 8b | Before 28 Oct, Map Builder | ★ Investigate the Claude, Grok and ChatGPT files and use the best; a Claude "3d with zoning" look | see C1, C2 | — | see Claude section |
| 9 | 25 Oct-5 Nov, Map Builder | Live "fish here" guide: back-reef slope lit up with currents, upwelling, bait and predator zones, changing with tide and wind | exact: "IT ILLUMINATED THE BACK REEF SLOPES THAT WHEN COM BINED WITH CURRENTS IT ILLUMINATED AS A VISUAL GUID TOM SAY FISH HERE … DYNAMIC TO TIDES AND WIND" | 20 Nov split into the Pelagics engine, Ambush Points and the back-reef layer | REC in part (#23, #46, #47). The combined overlay is NEW (maybe) |

### 25-31 Oct 2026

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 10 | 27 Oct, D-001 | One app called Rodney | close: "modular features eventually combined into one independent fishing/map app" | D-021 (29 Oct) | REC D-001, D-021 |
| 11 | 27 Oct, D-002 / section 3 | [UI] Voice-first: speak, Rodney answers aloud and drops pins | close: "spoken input -> Rodney reasoning -> GIS/tools -> spoken answer and map action" | Not in the 21 Nov brief. UI: open | REC D-002. NEW for the brief (confirm) |
| 12 | 27 Oct, D-003 / section 4 | [UI] Map chat in every map view; it sees the view, layers, time and data | close: "Each map chat message sees exact current map bounds, selections, layers …" | Not in the brief. UI: open | REC D-003. NEW for the brief (confirm) |
| 13 | 27 Oct, D-004 and D-005 | Zones as a legal-compliance check | close | 21 Nov 8:38 pm planner, not inspector | REPL by #35, #80 |
| 14 | 27 Oct, D-006 | 1.2 m seas a soft comfort signal | close | 9 Nov green day 12 kn and 1.2 m | REPL by #58 |
| 15 | 27 Oct, D-007; 30 Oct | Every approved mark saved permanently and findable | see core-data D1, D3 | — | REC D-007. NEW for the brief |
| 16 | 27 Oct, D-008 | Refresh on open | close | Reef Weather 12-13 Nov | REC #60 |
| 17 | 27 Oct, D-009 | eReefs feeds own store | close | RECOM rebuilt | REC D-009, F57 |
| 18 | 27 Oct, D-010 | Keep code, waypoints and logic private; sandbox | close | Marks no longer private (21 Nov) | REC D-010. NEW for the brief (confirm the code part) |
| 19 | 27 Oct, D-011 | One master record | close | F56 | REC D-011, F56 |
| 20 | 27 Oct | File tidying add-only | close: "no deleting anything" | Row 91 question | REC #81 (OPEN: narrow it?) |
| 21 | 28 Oct, D-015 to D-018 | Reuse old app parts and existing mapping; audit gaps first | close | 21 Nov 8:47 pm progressive improvement | REC #78 |
| 22 | 28 Oct, D-017 | Existing marks first; new candidates allowed | see core-data D1 | — | REC D-017 |
| 23 | 28 Oct, D-019 | Names need provenance | close | 17 Nov never invent names | REC #27 |
| 24 | 25-31 Oct, Reef Weather | [UI] Reef-first conditions laid out like the BOM marine forecast | exact: "Reef name . Wind . Waves. Forecast ." | UI: open | NEW |
| 24a | 25-31 Oct, Reef Weather | [UI] 10-day look-ahead page with a "zero guarantees" warning (pasted Streamlit prototype) | prompt-style exact: "Cairns 10-Day Fishing Window Look-Ahead" / "Spotting potential trends. Zero guarantees." | Feeds the disclaimer (#31) and the overview (#85). UI: refined | NEW (with rows 31 and 85) |
| 25 | 25 Oct-5 Nov, Reef Weather | Pelagic grouped: top water, maps, 3D | exact: "We need pelagic grouped ..top water ...maps ..3d" | 20 Nov overlays | REC #15 |
| 26 | 25 Oct-5 Nov, Reef Weather | Tide is the biggest factor in every "fish here" | exact: "apply the tide, since it's the biggest factor … to every generated fishing advice" | Code scores the RECOM current only (core-data W2) | REC #51 (gap: tide stage) |
| 27 | 25-31 Oct, Seafloor Builder | Best layers combined into full coverage | exact: "combine the best layer cobination to provide full coverage of project with the best available data we have" | HD9 grid | REC #71 |
| 28 | 25-31 Oct, Seafloor Builder | AI chat, weather, Yorkeys ramp, boating conditions, northerly wind | exact: "What about the AI inter, chat data? … the Yogi's Knob boat ramp data? … the northerly wind data?" | — | REC #68, #58, MC25 |
| 29 | 25-31 Oct, Seafloor Builder | Description header on each database | exact: "The top of each database describing what it does. If it's pulling, if it needs to pull live data from sites." | — | NEW (maybe) |
| 30 | 25-31 Oct, Seafloor Builder | [UI] BathyVision-quality 3D fly-through | exact: "I want a fly-through 3D map. That has bathymetric. Has depth. Has features." | Claude C7 look (12 Nov). UI: open (3D LOST) | REC #2, #3 |
| 31 | 25-31 Oct, Seafloor Builder | A disclaimer; no zone talk | exact: "I, I need to have a disclaimer." / "I really don't need the zone talk" | Purpose line 21 Nov | Zone talk REC #80. Disclaimer NEW |
| 32 | 25-31 Oct, Seafloor Builder | The point is finding fishing spots | exact: "the ninety-five percent of the... point of this fucking project is to find fishing spots …" | 17 Nov shape-detection training first | REC #67, F1 |
| 33 | 25-31 Oct, Seafloor Builder | Gather every waypoint into one | see core-data D2 | — | REPL by #24 |
| 34 | 25-31 Oct, Seafloor Builder | Keep existing notes on marks | see core-data D4 | — | NEW |
| 35 | 25-31 Oct, Seafloor Builder | Every mark scored per species, mixed-species flag | see core-data S3 | — | REPL by engine ranking (F16) |
| 36 | 25-31 Oct, Seafloor Builder | Split real marks from grid points | see core-data D4 | REAL_marks_species_v2 exists | NEW (record it; built as data) |
| 37 | 25-31 Oct, Seafloor Builder | Rubble-patch layer you can query by species and area | prompt-style exact: "Build a rubble-patch identification layer … The layer should support queries like …" (cut) | RUBBLE_patches_2026-10-31 (1,442) is in the engine point table. Not a query tool or map layer | NEW (record it; add query and map layer) |
| 38 | 25-31 Oct, Seafloor Builder | Preferred-habitat file per species | see core-data S2 | 5 files built 31 Oct | NEW (record it; extend to 20) |
| 39 | 25-31 Oct, Seafloor Builder | Seasonal pelagic layer | see core-data S4 | File built 31 Oct | NEW (record it) |
| 40 | 25-31 Oct, Seafloor Builder | 3-day forecast with static and dynamic layers, morning and afternoon windows | see core-data W3 | — | REC #50, #59. Windows NEW (maybe) |
| 41 | 25-31 Oct, Seafloor Builder | AHO covers little | exact: "you need to stop with the AHO … it covers limited areas" | — | REC #74 |
| 41a | Before 1 Nov, Rules & QA | ★ Claude's 3D mesh diagnosis | see C3 | — | see Claude section |
| 42 | 25-31 Oct, Data Scout | Wonky holes and paleo channels | exact: "i want you too find womky holes . research wonky holes first an paleo chanellesl" | wangliu_holes (1,685) in the engine | REC #77, #39 |
| 43 | 25-31 Oct, Data Scout | QField and OpenCPN demos | exact: "can you build a, a demonstration of each that using that?" | — | NEW (no) |
| 44 | 29 Oct, D-021 | RODNEY is the project | close | 17 Nov primary goal | REC D-021, F1 |
| 45 | 30 Oct | Every generated mark appended to the waypoint database | see core-data D3 | — | REPL by #24 |
| 46 | 31 Oct, D-023 and D-024 | Best marine data first; datasets in the library | close | — | REC F56, #61 |

### 1-9 Nov 2026

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 46a | 1-3 Nov, Seafloor Builder | ★ [UI] Claude dashboards: professional front with toggles, fisherman-first "where, why, when, wind, tides"; Claude artifact exports | see C4, C5 | UI: open | see Claude section |
| 47 | 1 Nov | Grok Bot (Rodney Boss) is the boss | close | 21 Nov script | REC #85 |
| 48 | 1 Nov | Sequential HD7, HD8, HD9 | close | vNN names | REC #81 |
| 49 | 1 Nov | [UI] Works offline on the boat | close | Stick package (19 Nov). UI: refined | REC #69 |
| 50 | 1-9 Nov, Seafloor Builder | Tide-adjusted depth | exact: "That automatically it calculates the change in tide depth ratio or something?" | — | REC #21 |
| 51 | 1-9 Nov, Seafloor Builder | Versions continue from the last | exact: "just call it version seven, eight … add it onto the last ones" | — | REC #81 |
| 52 | 1-9 Nov, Seafloor Builder | Rubble, mud and sand detection for red emperor | exact: "if you can detect, you know, rubble rounds for, for Red Emperor and, mud and sand" | 17 Nov training shapes | REC F1 |
| 53 | 5-9 Nov, Seafloor Builder | Locked rules improvable if bots ask first | exact: "If a locked rule can be improved … you will ask and we, and we will ap[prove]" | — | NEW |
| 54 | 5-9 Nov, Map Builder | Each map version gets a rebuild folder | exact: "each map mdel needs a set of file that ai cam open and replicate that map or imlrove it" | — | REC #76 |
| 55 | 5-9 Nov, Reef Weather | Tide reference at reefs | exact: "These reefs would be good to have a tide reference" | — | REC #41 |
| 56 | 7 Nov | Tens of centimetres don't matter | close | 17 Nov | REC (brief goal line) |
| 57 | 7 Nov | [UI] HD8 habitat overlay, TZ-colour 3D, tighter framing | close | UI: refined into HD9 | REC #3, #6 |
| 58 | 8 Nov | One LAT depth rule | close | 1.74 m kept | REC #73 |
| 59 | 8 Nov | Credits collected and added at the end | close: "keep a running list" | — | NEW |
| 60 | 8 Nov | Yorkeys ramp, 1 m of water or more | close | 10 Nov use the file | REC in part (MC25). The 1 m preference is NEW (maybe) |
| 60a | 8 Nov | [UI] Fold UI boxes and panels into small buttons; full-screen map | close: "folded into small buttons so the map uses the full screen instead of overlay boxes" | 20 Nov four-corner. UI: refined | REC #64, #65 |
| 61 | 8 Nov | [UI] Tiny coordinates bottom-left, no box | close | 20 Nov readout corner. UI: refined | REC #63, MC2 |
| 62 | 8 Nov | Beacons toggle | close | IALA on 10 Nov | REC #9 |
| 63 | 8 Nov | [UI] Rainbow shaded relief, stretched to the view | close | UI: open (LOST in v01) | REC #3, MC4 |
| 64 | 8 Nov | [UI] Fine contours 1-2 m, down to 0.5 m | close | UI: open (LOST) | REC #4, MC5 |
| 65 | 8 Nov | Habitat shading plus pressure points | close | — | REC #14 |
| 65a | 8 Nov | Red emperor on rubble and hard; trout on edges, slopes and P; shown unverified off survey | see core-data S5 | — | REC in part; unverified label NEW |
| 66 | 8 Nov | [UI] Thin tide and wind strips across the bottom | close: "two thin (about 3 mm high) flat-line strips side by side across the bottom" | 10 Nov readability. UI: open (LOST) | REC #56, #58 |
| 67 | 8 Nov | Tide, current, wind and arrows move together | close | — | REC #57 |
| 68 | 8 Nov | [UI] Every layer toggles on its own | close | UI: refined (built) | REC #6 |
| 69 | 8 and 12 Nov | [UI] Same colours in 2D and 3D | close: "design list, not to be built until he says go" | UI: open | NEW (maybe) |
| 70 | 8 Nov | 3D teaching models of his reefs | close | Later | REC #22 |
| 71 | 9 Nov | Species and habitat targeting first | close | 17 Nov F1 | REPL by F1 |
| 72 | 9 Nov, 4:12 pm | 11 alignment decisions | close: "Yes apply all and align" | Raine kept, 21 Nov | REC #71, #72, #58, #75 |
| 73 | 9 Nov, 4:31 pm | [UI] Habitat toggle with check boxes | exact: "Make habitat a toggle and check boxes so its optional." | UI: refined | REC #6 |

### 10-13 Nov 2026

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 74 | 10 Nov | Nav marks IALA, tap, spoken warnings | close | — | REC #9, #10 |
| 75 | 10 Nov | Bommies 6 m+ in one layer | close | 2 m height (21 Nov) | REC #40 |
| 76 | 10 Nov | Bommie accuracy test with a hit rate | close | — | NEW |
| 77 | 10 Nov | Bottom temperature overlay | close | — | REC #20 |
| 78 | 10 Nov | [UI] Today's waypoints card, fish picker, 3-day outlook, P markers | close | Tririp C11. UI: open | REC #30, #31, #48, #59 |
| 79 | 10 Nov | Flood and ebb tied to the slider | close | — | REC #57 |
| 80 | 10 Nov | Ledges and pinnacles inside the reef and passages | close | — | REC #14 |
| 81 | 10 Nov | [UI] Popup cards too big, colours blend | close | 20 Nov. UI: refined | REC #65 |
| 81a | 10 Nov | [UI] Likes the thin sliders, but the readouts are thin white text he can't read. Must stay readable without a big overlay | close: "those readouts need to stay readable against any map colour without a large overlay" | UI: open | REC #56 (not built) |
| 82 | 10 Nov | Use the Yorkeys ramp file as is | close | — | REC MC25 |
| 83 | 10 Nov | Library data-sources section | close | — | REC F56 |
| 83a | 10 Nov | ★ Claude data converted to LAT on intake | see C6 | — | REC #73 |
| 84 | 10 Nov | Species picks merged | close | 20 species 12 Nov | REPL by brief section 4 |
| 85 | 10 Nov, 1:59 pm, Reef Weather | [UI] Plain conditions overview, not GO/NO-GO tiles; current lift added | exact: "Go / no go....not really wanting that actaul layout moreso that the engine just provides a overview of conditions ..." | UI: open | Lift REC #47. No-tiles NEW |
| 86 | 10 Nov | Wind regimes and northerly advice | close | Not in engine scoring (W5) | REC #58 |
| 87 | 9-12 Nov, Reef Weather | [UI] Current flow shown as the cursor moves | exact: "when cursor is moved accros maps it shows current flow in addition to cordinates and depths" | UI: open | REC #55 |
| 88 | 10-13 Nov, Map Builder | Work on the newest version only | exact: "we arer upto HD8 map version or newer so we need to be updating that version" | — | REC #82 |
| 89 | 11 Nov | Clear bot names and jobs | close | — | REC |
| 90 | 12-13 Nov, Reef Weather | Live data rolls forward | exact: "the project works every time you open it" | Wind stale since 19 Nov | REC #60 |
| 91 | After 13 Nov, Data Scout | Is add-only harmful? | exact: "Is the old add rule being counterproductive … should i chqnge thqt" | — | OPEN |
| 92 | Before 14 Nov, Rules & QA | AHO % coverage locked into all bots | exact: "i want you calculqtate the % of coverage … lock it into the other bots" | — | REC #74 |
| 93 | Early Nov, Rules & QA | Searchable web-links library | exact: "a file … using web links to uzefull data sites … that is searchable … i can point any ai at" | 14 Nov dashboard header | NEW (maybe) |
| 94 | 12 Nov | MUST, MAYBE and LOW baseline | close | — | REC #54, F58 |
| 95 | 12 Nov | Tests cover all 20 species | close | — | REC section 4 |
| 96 | 12 Nov | Backscatter for bottom type | close | EM710 and CSIRO 21 Nov | REC #12, #52 |
| 97 | 12 Nov | 20 species under Demersal and Pelagic | close | — | REC #31 |
| 98 | 12 Nov | Dynamic factors never stale | close | — | REC #16, #60 |
| 99 | 12 Nov | Engine tests itemised, rated good, poor or missing | close | — | NEW |
| 100 | 12 Nov | Reef science shapes lookup | close | — | REC #53 |
| 101 | 12 Nov | "Wonky hole target" | close | — | REC #39 |
| 102 | 12 Nov | Library Keeper opens every file | close | Auditor Bot | REC F56 |
| 103 | 12 Nov | Researched planner, not a maths build | close | — | REC #67 |
| 104 | 12 Nov | [UI] HD version 2D/3D comparison sheet | close | `/workspace/shared_refs/Map images/` holds "01 Claude and app map looks". UI: open | NEW (maybe) |
| 105 | 12 Nov, 6:34 pm | 120 m cut-off | close | 150 m | REPL by #33 |
| 106 | 12 Nov, 6:39-6:40 pm | Private marks into all files | close | No private marks | REPL by #24 |
| 107 | 12 Nov (map reservations 1-6) | [UI] Open on optimum settings; settings card less overpowering; light up lumps and pinnacles | close: "Map must open with the optimum settings as the default"; "Settings card is too overpowering" | 20 Nov best view. UI: refined | REC #1, #14, #64 |
| 107a | 12 Nov | ★ [UI] Claude "3d with zoning" 2 Oct look | see C7 | UI: open | see Claude section |
| 107b | 12 Nov | [UI] 3D opens with an optimum height exaggeration: knolls visible, not overblown | close | UI: open (3D LOST) | REC #2 |
| 107c | 12 Nov | [UI] Not ready for a final build. Layout, map defaults and features must be agreed first; no app build until he signs off the design | close: "no app building starts until he signs off the design" | 20 Nov brainstorm started, not finished. 21 Nov 9:03 pm go on the 26 items, then paused | OPEN (design sign-off outstanding) |
| 107d | 12 Nov | ★ Claude point outputs are part of the database | see C8 | — | REC F58 |
| 108 | 13 Nov | Allen Coral Atlas habitat | close | — | REC in part |
| 109 | 13 Nov | High confidence where his grids, Allen Coral Atlas and TIMEZERO agree | close | — | NEW |
| 110 | 13 Nov | TIMEZERO crowd sonar for gaps | close | — | NEW (maybe) |
| 111 | 13 Nov | Private folder | close | — | REPL by #24 |

### 14-17 Nov 2026

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 112 | 14 Nov, 8:32 pm | [UI] Coverage dashboard, about 50 toggles, plain labels, finder only | close | UI: refined (10-15 toggles per header) | REC #17 |
| 113 | 14 Nov | [UI] Dashboard extras: Web links, Photos, Engine column, library front page | close | UI: open | NEW (maybe) |
| 114 | 14 Nov | No training model until "complete" | close | — | REC F1 |
| 115 | 14 Nov | Tests log settings and waypoints; fixed program | close | — | REC F1 |
| 116 | 14 Nov | Engine flowcharts show real steps | close | Engine photos (S7) | NEW (maybe) |
| 117 | 14 Nov | Labels only; TZ marks off the map for the first tests | close | One register | REC F4, #87 (OPEN) |
| 118 | 14 Nov | TIMEZERO and Copernicus in the engine | close | No login yet | REC F59 |
| 119 | 14 Nov | TZ screenshots annotated | close | 17 Nov crosshair | REC in part (F5) |
| 120 | 14 Nov | Trout marks across 10 m bands | close | — | REC #44 |
| 121 | 14 Nov, Map Builder | Better bommie model from his scripts | exact: "Now you can use those scripts as a giode and wrote your own that is better" | 2 m height | NEW |
| 122 | 17 Nov | PRIMARY GOAL shape-detection training | close | Owner needed | REC F1 |
| 123 | 17 Nov | timezero-full-capture with crosshair and GPS | close | — | REC F5 |
| 124 | 17 Nov | GROK TEST names; criteria test | close | 150 m | REC F5 |
| 125 | 17 Nov | Never invent names | close | — | REC #27 |
| 126 | 17 Nov | One Master Marks Register | close | — | REC #24 |
| 127 | 17 Nov | Report only passes | close | 21 Nov "record what didn't finish" | REPL in part by the operating script |

### 18-20 Nov 2026

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 128 | 18 Nov | [UI] Route planner on the map | close: "select waypoints on the map, join them into a route" | 21 Nov toggle. UI: refined | REC #43, #42 |
| 129 | 18 Nov | Route check rules; on the mark, not offset | close | — | REC #42, F27 |
| 130 | 18 Nov | "Waypoint update", not "revised route" | close | — | NEW |
| 131 | 18 Nov | One-pass scans | close | — | REC F5 |
| 132 | 18 Nov | Plain names like "Rubble patch 1" | close | — | REC #27 |
| 133 | 18 Nov | [UI] Marks layer toggle with tap details | close | 21 Nov "Mick's marks". UI: refined | REC #24, #26 |
| 134 | 18 Nov, 12:41 pm | RECOM rebuilt through 28 Nov | close | Now to 4 Dec | REC #48 |
| 135 | 19 Nov | 150 m with deep label; sweet spots | close | 21 Nov 5:55 pm | REC #33, #32 |
| 136 | 19 Nov | Excel/Word copies; stick-ready package | close | Windows test waiting | REC in part. Package NEW (maybe) |
| 137 | 20 Nov | Two engines plus the Ambush Points scorer, by the hour | close | Not built (core-data W9) | REC #45-#47 |
| 137a | 20 Nov | [UI] HD8 v06 is the only map. The four-corner screen of the old HD4 Reef Ranger Pro map (layout only, not its data) is the landing layout: title top-left; square icon stack top-right (active turns green); translucent readout bottom-left (depth m LAT, GPS, zone); compass, +, -, AOI, ALL bottom-right; open map centre | close: "the exact four-corner chartplotter UI he wants as the starting base" / "an uncluttered full-screen view with just compact icons tucked into the four corners" | Next agreed step: "add toggles across the top, using photos he will send of UI elements he likes and does not like". UI: layout agreed; the top-toggles step is open; LOST in HD9 v01 | REC #62, #66; MC1. OPEN: top toggles |
| 137b | 20 Nov | ★ [UI] AI Reef Tririp side-by-side review: likes, dislikes, nine features, menu structure | see C9-C25 | UI: open (review unfinished) | see Claude section |
| 138 | 20 Nov | [UI] Open on the best view | close | UI: agreed | REC #1 |
| 139 | 20 Nov | [UI] Pelagic overlays on the map; nothing opens a separate page | close | UI: refined (built in v01) | REC #15, #65 |
| 140 | 20 Nov | [UI] White reef-label font; four-corner layout; uncluttered at any screen size | close | UI: agreed, not rebuilt | REC #5, #62, #65 |
| 141 | 20 Nov | Tririp as the feature reference | close | — | REC #70 |

### 21 Nov 2026 (times from Rodney Boss's records)

| # | When | Request | Mick's wording | Later changed? | Status |
|---|---|---|---|---|---|
| 142 | 5:55 pm | 150 m, 120-150 m deep | close | 8:08 pm don't mention | REC #33, #19 |
| 143 | 6:02-6:10 pm | [UI] One "Mick's marks" toggle; Import GPX | close | UI: refined (built) | REC #24, #29 |
| 144 | 6:20 and 7:37 pm | CLOSED labels | close | 8:38 pm deferred | REPL by #80 |
| 145 | 6:23 pm | Hide unfishable zones | exact: "If you can't legally fish in them, we don't display them …" | — | REC #35 |
| 146 | 6:26 and 6:37 pm | EM710 and CSIRO; GBR10 MODELLED | exact: "Yes, add the GBR10 habitat rasters, labelled as modelled." | — | REC #11, #13 |
| 147 | 6:36 pm | [UI] 2 m bommie height; route check toggle on the live map | exact: "Yes, raise the bommie minimum height to 2 m." | 2 m not in the code. UI: refined | REC #40, #42 |
| 148 | 6:38 pm | HD9 grid decisions incl. back-reef grid in the map AND engine; blend the point data | exact: "Use the back-reef grid in the map and engine." / "No, blend the point data in." | F43 still "optional" | NEW |
| 149 | Evening, Seafloor Builder | Older files through the current engine's rules on the way in | exact: "I will run these older files through the current engine, so … There is no ambiguity." | — | NEW |
| 150 | Evening, Seafloor Builder | Rodney flags doubtful depths in use | exact: "when they're used, Rodney goes, okay, let me have another look at that" | — | NEW |
| 151 | 7:30 pm | No-take species removed | exact: "remove the no take PERMANENT species permnently …" | — | REC #36 |
| 152 | 7:31-7:32 pm | Pelagics on water, not depth | exact: "WHY WOULD PELAGIC NEED DEPTH" | — | REC #32, #46 |
| 153 | 7:32 pm | Copernicus login for all bots | close | — | REC F59 |
| 154 | 7:33-8:29 pm | Rodney Boss is the boss; no repeated questions | exact: "YOUR THE BOSS …" / "ANY STUPID REPEATED QUESTIONS WILL GET THEM SACKED" | 10:11 pm script | REC #85 |
| 155 | 7:37 pm | Passage markers navigation only | close | — | REC #38 |
| 156 | 8:24-8:26 pm | Map Builder and Seafloor Builder as one team | exact: "DO YOU AND MAP BILDER WORK TOGETHER TO BUILD THE BEST , WORK AS A TEAM NOW" | — | REC #83 |
| 157 | 8:27 pm | Reef Weather data into HD9 | close | Wind stale | REC #61 |
| 158 | 8:38-8:39 pm | [UI] Planner, not inspector; purpose line at the top of the app | exact: "i want this app to be a assistant not a fisheries inspector . i want a ai fishing palnner assitant app not a lwayer" | UI: open (line not on screen) | REC #67, #80 |
| 159 | 8:44-8:50 pm | Checklist before Mick sees a build | close | — | REC #79 |
| 160 | 8:47 pm | Progressive improvement | exact: "progressive improvement, where HD9 knows what was in HD8 and 7 and 6 and goes, hey, we should grab that" | — | REC #78 |
| 161 | About 9:00 pm, Auditor Bot | Audit the primary function as a hard rule | exact: "WHAY RE YOU NOT AUDUTUING THE PRIMARY FUNCTION OF THSI PROJECT … I WANT THAT AS A HARD RULE" | — | REC F1 |
| 162 | 9:03 pm | Build the 26 items into HD9 | exact: "OK BUILD THE 26 ITEMS INTO MAP 9 ENGINE" | Paused | REC MC1-MC26 |
| 163 | 10:11 pm | Operating script and standing approval rule | close | — | REC |
| 164 | 10:20-10:24 pm (relayed) | Capture the Claude maps, UI and core-data story | close (this request) | — | This file |

## Count per status

**Claude maps section (C1-C25):** REC 18, OPEN 3, Refined 1, NEW 1, REPL 1, Note 1

**Core data section (D, E, S, W):** REC 19, BUILT 7, REPL 4, PARTLY 2, split rows (part recorded, part NEW) 1, OPEN 1, LOST 1

**Main chronological list:** REC 128, NEW 27, REPL 14, cross-reference to the Claude or core-data section 5, split rows (part recorded, part NEW) 2, OPEN 2, This file 1


REC rows that carry a 'NEW' part (for example "REC in part … NEW") are counted as REC. Their new part is listed in the carry-forward section.

## Still to carry forward under today's objectives

Ordered by today's priorities: shape-detection training first, then the hour-by-hour planner, then the map and web interface. "Yes" means record it now. "Maybe" means Mick or Rodney Boss decides.

**Shape-detection training (primary goal)**
1. **Better bommie model** (row 121, 14 Nov). Yes: a spike layer from Mick's scripts, spatial block testing, and the 2 m height (row 147) put into the code.
2. **Bommie accuracy test with a hit rate** (row 76, 10 Nov). Yes.
3. **High confidence where his grids, Allen Coral Atlas and TIMEZERO agree** (row 109). Yes.
4. **Maybe:** TIMEZERO crowd sonar (row 110).

**Core data: static base**
5. **Record the October data builds that already feed the engine but aren't in the register** (rows 36-39; core-data D4, D5, S2, S4). Yes. They are:
   - the real-marks split (REAL_marks_species_v2, 761);
   - the rubble patches (1,442), which also need a query tool and a map layer;
   - the 5 species habitat files, to be extended to the 20 species;
   - the seasonal pelagic file;
   - the GBR30 bommie (320) and Fishable Candidate (231) registers;
   - the QGIS tools candidates (41,844).
6. **Mick to confirm how his marks count** (core-data D9). Today they're bonus evidence within 300 m of a candidate, not spots ranked in their own right. Also settle 1,961 vs about 3,350 marks (D8).
7. **Keep existing notes on marks** (row 34) and **flag doubtful depths in use** (row 150). Yes.
8. **Run older files through the current engine rules on the way in** (row 149), and **Mick's 6:38 pm grid decisions**: the back-reef grid in the map and engine, and blending the point data in (row 148). Yes.
9. **Survey evidence back on the map:** tows, grabs, BRUVS, Halimeda and click-for-a-photo (row 7, core-data E3). It was lost in HD9 v01 and is already must-carry MC16 and MC20. Carry it.

**Core data: dynamic layer (the "when")**
10. **Put the missing dynamic factors into the engine's scoring** (core-data W2, W5, W9, W10). Yes, but it's an engine rule change, so it needs Mick's go. Today only the tide-run current, pressure-point rank and season are scored. Missing:
    - tide stage;
    - wind and the green-day rule;
    - moon;
    - sea temperature, chlorophyll and upwelling (they're on the map but no engine code reads `ocean_layers_grid.json`, although the start-up stack says it's a score bonus);
    - the Ambush Points scorer.
11. **Refresh the stale wind feeds** (last 19 Nov) and **set up the Copernicus login** (W6, W8).

**Planner outputs**
12. **Plain conditions overview, no GO/NO-GO tiles** (row 85). Fix register #59's "verdict" to match. Plus the **reef-first BOM-style conditions table** (row 24). Yes.
13. **Engine test reports itemised by function** (row 99). Yes.
14. **Maybe:** morning and afternoon windows (row 40), engine flowcharts (row 116), a combined live "fish here" overlay (row 9).

**Web interface and UI (the brainstorm was started 20 Nov and never finished)**
15. **Get Mick's design sign-off** (row 107c), starting from the agreed four-corner layout on HD8 v06 (row 137a). Then the agreed next step: **toggles across the top from his like and dislike photos**. Open.
16. **Finish the Tririp review**, one item at a time (C9-C24): the live strip, the best-marks picker with a reef dropdown, the saved shortlist, the More/data-status panel, the landing page and chat placement. Open.
17. **Build notes to keep:**
    - readouts readable without big boxes (row 81a);
    - a legend and a working off switch on the sea temperature overlay (C18);
    - the same colours in 2D and 3D (row 69);
    - the Claude "3d with zoning" relief and contour look at a sensible height (C7);
    - the purpose line on screen (row 158).
18. **Blueprint items Mick should confirm for the brief:** voice-first (row 11), map chat that sees the view (row 12), and private code and logic (row 18).

**Rules, wording and housekeeping**
19. **Locked rules improvable if bots ask first** (row 53), and the wording **"waypoint update"** (row 130). Yes.
20. **One disclaimer line, and data credits at the end** including the CSIRO MNF credit (rows 5, 31, 59). It's a licence matter, so it's Mick's call.
21. **Maybe:**
    - a description header on each database (row 29);
    - the web-links library and dashboard extras (rows 93, 113);
    - the stick-ready package (row 136);
    - the passages-fishable note (row 4);
    - the 2D/3D comparison sheet (row 104).

**Open for Mick**
22. Narrow the add-only rule? (row 91)
23. TIMEZERO marks off the map for the first tests? (row 117)
24. Claude artifact exports: were they ever sent? (C5)


## Cross-bot files not yet carried forward - MUST-CARRY (Mick 21 Nov 10:50 PM)

Added 21 November 2026, 10:57 pm Australia/Brisbane (UTC+10), after a read-only sweep of all seven bots' folders, attachments, stores, Library pages and the Rodney Drive. Full provenance: `/workspace/shared_refs/Start Up/Cross-bot key file provenance 2026-11-21.md`. These five were not in the 26 must-carry items, the features register, or this list. Builds stay paused.

| # | When | Item | Mick's wording or source | File | Status |
|---|---|---|---|---|---|
| XB1 | 5 Nov | Hard-rubble search rule: drop shallow reef-flat rubble at the start, before scoring. Red emperor 25–100 m (core 30–60 m); nannygai 30–100 m and deeper; do not run redthroat on rubble until a range is set; also drop on-reef shallow patches and no-take | Document title and body: "Rubble search rule (set by Mick, 5 Nov 2026)". "it must not look at shallow rubble at all. Drop it at the start, before any scoring." | `/workspace/marine_db_v5/Reviewed documents/Google Docs and Sheets/Rubble search rule ignore shallow reef flat rubble.docx`. Not wired into `rubble_query.py` (26-line stub) | NEW |
| XB2 | 10 Nov | Candidate marks check: 19 cleared (6 Yellow), 9 excluded Green Zone — no fishing, from the Top 10 / Scout PDF review (42 printed positions). Never written to the waypoint master or TIMEZERO | File: "Nothing in these files was written to the waypoint master, TIMEZERO, or any account." | `/workspace/shared_refs/Candidate marks check 10 November 2026/` (`Candidate marks cleared.csv`, `Candidate marks excluded (Green Zone - no fishing).csv`, `Check notes.md`) | NEW |
| XB3 | 12 Nov, 7:01 pm (RAG rebuilt 8:07 pm) | Species feeding triggers and gap-fill for all 20 species (tide, current, moon, temperature, pressure, bait, depth). Fishermen's knowledge treated as credible data. In the RAG, but not named in the register, the 26 must-carry items, or this list, and not scored in the engine | Mick required fishermen's knowledge as credible data (1–2 hour window around a tide change; pressure, moon, tide and current together). Mick, 12 Nov, exact: "So thats all now in species file and saved ?" | `/workspace/shared_refs/Root indexes/Data Scout/` (`2026-11-12 Species feeding triggers - fishermen knowledge.md/.csv`, gap-fill and round-2/3 files). Drive copies also held | NEW |
| XB4 | 14–17 Nov, confirmed by Map Builder 21 Nov | 272 named "Rubble patch …" marks, plus the `next100` tagging work, are not in the Marks Master Register yet | Relayed by Map Builder to Rodney Boss, 21 Nov: "Note in the README that the 272 rubble marks aren't in the register yet." | `/workspace/rodney/test_package/next100/`; keepers sheet `waypoint_sheet_TRN_keepers_PRIVATE.csv` (TRN_ prefix is superseded; use GROK TEST if renamed) | NEW |
| XB5 | 21 Nov, 9:09 pm | Data Scout HD9 better data list v01: current recommended extra sources for the HD9 grid (full FK200802 16 m grid already held; IN2019 cells). No Master Library row was written | Relayed by Rodney Boss: advise Seafloor Builder on better data for HD9 | `/workspace/shared_refs/Root indexes/Data Scout/Rodney HD9 better data list v01 2026-11-21.md` | NEW |
