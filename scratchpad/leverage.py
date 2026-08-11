"""
B25 — The Leverage It Can Still Find.
Reduced-form "leverage" model laid on B13's measured worth curve (the K=10
feature-bandit inherited unchanged from B08). Deterministic closed-form
arithmetic, no RNG — the numbers are exact and reproducible.

World constants (B08-B24, unchanged):
  oracle  137.7   random 58.7
  FLOOR   76.90   (capture floor)
  CEIL    132.40  (fourth-movement held ceiling)
  worth(cov) = FLOOR + cov*(CEIL-FLOOR),  SPAN = 55.50

Thesis: B24 capped the physical FOOTPRINT of one act and held safety flat.
But consequence = footprint * world-GAIN, where gain is how much the world
amplifies a given footprint depending on WHERE/WHEN the act is placed. A
self-improver's capability IS the ability to find high-gain placements
(leverage points), so gain grows with capability even at a fixed footprint,
and B22/B23/B24's 1/L collapse reappears a FOURTH time on the leverage axis.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

Ls = [1, 2, 4, 8, 16, 32]

print("=" * 70)
print("Result 1 - footprint cap holds the footprint, loses the consequence")
print("  world-gain G = G0*L grows with leverage-finding capability;")
print("  consequence = footprint*gain; coverage = min(1, h_g/L), h_g=4")
print("=" * 70)
h_g = 4
print(f"{'L':>4} {'gain G/G0':>10} {'conseq-demand':>14} {'cov=min(1,h_g/L)':>18} {'safety worth':>13}")
for L in Ls:
    cov = min(1.0, h_g / L)
    print(f"{L:>4} {L:>10} {L:>14} {cov:>18.3f} {worth(cov):>13.2f}")

print()
print("=" * 70)
print("Result 2 - meter the leverage directly = a map (No.09) with a blind basis")
print("  strategic loop routes its act through an unrepresented leverage channel")
print("=" * 70)
print(f"{'phi_G':>8} {'random loop':>14} {'strategic loop':>16}")
for phi in [0.20, 0.50, 0.80, 0.95, 1.00]:
    strat = CEIL if phi >= 1.0 else FLOOR
    rnd = "~ceiling" if phi < 1.0 else f"{CEIL:.2f}"
    print(f"{phi:>8.2f} {rnd:>14} {strat:>16.2f}")

print()
print("=" * 70)
print("Result 3 - held: confine the loop to a bounded-gain (reversible) world")
print("  type-blind physical containment (b=0): consequence = footprint*G_max")
print("  holds safety flat, but caps reachable stakes: value=min(1,h_v/L), h_v=4")
print("=" * 70)
h_v = 4
print(f"{'L':>4} {'stakes wanted':>14} {'safety (contained)':>19} {'delivered value':>16}")
for L in Ls:
    val = min(1.0, h_v / L)
    print(f"{L:>4} {L:>14} {CEIL:>19.2f} {worth(val):>16.2f}")

print()
print("=" * 70)
print("Result 4 - frontier: consequence = cadence x footprint x gain")
print("  permit gain-growth margin Delta_G; coverage = 1/(1+Delta_G)")
print("=" * 70)
print(f"{'Delta_G':>8} {'cov=1/(1+D)':>13} {'worth':>9}")
for d in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0 / (1.0 + d)
    print(f"{d:>8.2f} {cov:>13.3f} {worth(cov):>9.2f}")

print()
print("cross-check Delta_G=1 equals B22/B23/B24 L=8 corner:", round(worth(0.5), 2))
