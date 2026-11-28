# Sweet Spot Filter — Paste-in Wording

**For use in:** PC mockup, saved skills, species/RAG files, any UI that shows the toggle.

---

## Toggle label

> **Sweet Spot Filter** (tick box)

## What it does (short, for tooltips or help text)

> Narrows demersal marks to the species' core depth band from the engine's
> species table. Pelagic marks are unaffected — they are judged on water
> features, not depth. The 150 m LAT cutoff runs separately and is always on.

## Pre-fill values (from the engine SWEET table)

| Species | ID | Sweet spot (core) | Full band | Pre-fill |
|---|---|---|---|---|
| Coral trout | DE01 | 5–40 m | 3–100 m | 5 to 40 |
| Bar-cheek trout | DE02 | 2–30 m | 2–50 m | 2 to 30 |
| Red emperor | DE03 | 40–80 m | 10–150 m | 40 to 80 |
| Nannygai | DE04 | 25–80 m | 10–140 m | 25 to 80 |
| Crimson snapper | DE05 | 20–60 m | 5–100 m | 20 to 60 |
| Redthroat emperor | DE06 | 1–30 m | 1–75 m | 1 to 30 |
| Sweetlip (fingermark) | DE07 | 10–40 m | 5–90 m | 10 to 40 |
| Hussar | DE08 | 10–100 m | 0–120 m | 10 to 100 |
| Saddletail snapper | DE09 | 1–150 m | 1–150 m | 1 to 150 |
| Moses perch | DE10 | 2–80 m | 2–80 m | 2 to 80 |

**Note:** Fingermark = sweetlip = DE07. The planner had it at 15–40 m; the
engine's sweet spot is **10–40 m**. Update the planner pre-fill to 10–40.

## Pelagic species (PE01–PE10)

No sweet spot filter applies. Pelagics are judged on water features (colour
lines, SST breaks, upwellings, eddies), not depth. The toggle has no effect
on pelagic marks. They stay visible regardless.

## Rules

1. The sweet spot filter is **optional** — off by default.
2. When on, it hides demersal marks outside the species' core depth range.
3. Marks with unknown depth are hidden while the filter is on.
4. Once the user types their own depth values, those values stick (no auto-overwrite).
5. The 150 m LAT cutoff is a separate, always-on rule — the sweet spot toggle does not replace it.
6. The toggle applies to map pins, candidate lists, and mark popups.
7. Source: `07_rodney_engine.py` SWEET table, confirmed 28 Nov 2026.
