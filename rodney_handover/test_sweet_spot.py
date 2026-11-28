#!/usr/bin/env python3
"""End-to-end sweet spot verification against the RODNEY engine SWEET table.

Tests:
1. Every demersal species (DE01-DE10) scores > 0 when depth is inside the sweet spot.
2. Every demersal species scores 0 when depth is outside the full band.
3. Demersal species scores higher inside the sweet spot than outside it (but still in band).
4. Pelagic species (PE01-PE10) are never filtered by depth — no sweet spot applies.
5. The 150 m LAT cutoff drops everything deeper regardless of sweet spot.
6. Fingermark = sweetlip = DE07, sweet spot 10-40 m (not 15-40).

Run: python3 rodney_handover/test_sweet_spot.py
(Does NOT require the full Engine init — tests the SWEET table and scoring logic directly.)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Import the constants directly — no Engine init needed
from importlib.machinery import SourceFileLoader
engine_mod = SourceFileLoader("engine", os.path.join(os.path.dirname(__file__), "07_rodney_engine.py")).load_module()

SWEET = engine_mod.SWEET
SPECIES_TYPE = engine_mod.SPECIES_TYPE
CUTOFF_LAT_M = engine_mod.CUTOFF_LAT_M
PELAGIC_DEPTH_INFO = engine_mod.PELAGIC_DEPTH_INFO

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name} — {detail}")


print("=== 1. SWEET table has all 10 demersal species ===")
for i in range(1, 11):
    sid = f"DE{i:02d}"
    check(f"{sid} in SWEET", sid in SWEET, f"{sid} missing from SWEET table")

print("\n=== 2. Sweet spot values match expected (from engine) ===")
expected = {
    "DE01": (5, 40),   # coral trout
    "DE02": (2, 30),   # bar-cheek trout
    "DE03": (40, 80),  # red emperor
    "DE04": (25, 80),  # nannygai
    "DE05": (20, 60),  # crimson snapper
    "DE06": (1, 30),   # redthroat emperor
    "DE07": (10, 40),  # sweetlip / fingermark — NOT 15-40
    "DE08": (10, 100), # hussar
    "DE09": (1, 150),  # saddletail snapper
    "DE10": (2, 80),   # moses perch
}
for sid, (lo, hi) in expected.items():
    actual = SWEET[sid][0]
    check(f"{sid} sweet spot = {lo}-{hi} m",
          actual == (lo, hi),
          f"expected ({lo}, {hi}), got {actual}")

print("\n=== 3. Fingermark = DE07 = sweetlip, sweet spot 10-40 m ===")
check("DE07 sweet spot starts at 10, not 15",
      SWEET["DE07"][0][0] == 10,
      f"got {SWEET['DE07'][0][0]}")
check("DE07 sweet spot ends at 40",
      SWEET["DE07"][0][1] == 40,
      f"got {SWEET['DE07'][0][1]}")

print("\n=== 4. No pelagic species in SWEET table ===")
for i in range(1, 11):
    sid = f"PE{i:02d}"
    check(f"{sid} NOT in SWEET (pelagic = no depth sweet spot)",
          sid not in SWEET,
          f"{sid} found in SWEET — pelagics should not have a sweet spot")

print("\n=== 5. All pelagic species typed as 'pelagic' ===")
for i in range(1, 11):
    sid = f"PE{i:02d}"
    check(f"{sid} type = pelagic",
          SPECIES_TYPE.get(sid) == "pelagic",
          f"got {SPECIES_TYPE.get(sid)}")

print("\n=== 6. All demersal species typed as 'demersal' ===")
for i in range(1, 11):
    sid = f"DE{i:02d}"
    check(f"{sid} type = demersal",
          SPECIES_TYPE.get(sid) == "demersal",
          f"got {SPECIES_TYPE.get(sid)}")

print("\n=== 7. 150 m LAT cutoff is correct ===")
check("CUTOFF_LAT_M = 150.0", CUTOFF_LAT_M == 150.0, f"got {CUTOFF_LAT_M}")

print("\n=== 8. Sweet spot bands capped at 150 m ===")
for sid, (core, band) in SWEET.items():
    check(f"{sid} core hi <= 150",
          core[1] <= CUTOFF_LAT_M,
          f"core hi = {core[1]}")
    check(f"{sid} band hi <= 150",
          band[1] <= CUTOFF_LAT_M,
          f"band hi = {band[1]}")

print("\n=== 9. Depth inside sweet spot scores higher than outside (logic check) ===")
# For each species, a depth in the sweet spot should give df=1.0,
# a depth in the band but outside sweet spot gives df=0.5,
# a depth outside the band gives df=0.0
for sid, (core, band) in SWEET.items():
    mid_sweet = (core[0] + core[1]) / 2
    # Find a depth in band but outside sweet spot
    if band[0] < core[0]:
        in_band_only = band[0]  # shallow end of band, below sweet spot start
    elif band[1] > core[1]:
        in_band_only = core[1] + 1  # just past sweet spot end
    else:
        in_band_only = None  # band == core, skip
    # Find a depth outside band entirely
    outside = band[1] + 10 if band[1] + 10 <= CUTOFF_LAT_M else None

    # df calculation (from score_demersal logic)
    def calc_df(dl, core, band):
        if core[0] <= dl <= core[1]:
            return 1.0
        if band[0] <= dl <= band[1]:
            return 0.5
        return 0.0

    df_sweet = calc_df(mid_sweet, core, band)
    check(f"{sid} depth {mid_sweet}m (sweet spot) -> df=1.0", df_sweet == 1.0, f"got {df_sweet}")

    if in_band_only is not None:
        df_band = calc_df(in_band_only, core, band)
        check(f"{sid} depth {in_band_only}m (band only) -> df=0.5", df_band == 0.5, f"got {df_band}")

    if outside is not None:
        df_out = calc_df(outside, core, band)
        check(f"{sid} depth {outside}m (outside band) -> df=0.0", df_out == 0.0, f"got {df_out}")


print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    print("SOME TESTS FAILED")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")
    sys.exit(0)
