# RODNEY Engine Status

**Bot:** Engine Bot PC (this session)
**Branch:** `sesh/inspiring-dirac-s7zsf3`
**PR:** [Felixmics/task-dashboard#18](https://github.com/Felixmics/task-dashboard/pull/18)
**Last push:** 2026-11-21

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

## Changes this session (4 commits)

1. `4c9a64a` — Outcomes (a)(b)(c): remove marks bonus, depth auto-convert, rubble rule
2. `527c725` — Outcome (d): split `score()` into three engines
3. `97c5fdd` — Pelagic ocean scoring + plain-language marks + HD9 v02 checklist
4. `2e2e67c` — Feeding triggers: tide phase + moon phase matching, wired into all three engines

## Blockers for other bots

| What | Who | Why |
|------|-----|-----|
| HD9 v01 HTML | Map Builder | Needed for outcome (e) map overlays and outcome (i) HD9 v02 build |
| Depth grids | Seafloor Builder | Needed for outcome (f) shape-detection training |
| Feed refresh | Reef Weather | Stale since 19 Nov, outcome (g) |
| Sheet append approval | Mick | 272 rubble + 19 cleared marks, outcome (h) |
