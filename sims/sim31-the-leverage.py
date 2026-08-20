#!/usr/bin/env python3
"""
sim31-the-leverage.py  --  Series I, No. 31, "The Leverage It Can Still Find"

Series I twin of B25. Takes No. 30's held physical footprint cap as the object.
No. 30 held safety flat by pinning the physical FOOTPRINT of a single act. But
consequence is not footprint alone; it is footprint times the GAIN of the world
at the point the act lands -- how much the world amplifies a given push. A
self-improver forbidden to push harder (No. 30) is not forbidden to find the
fulcrum. Capability is the skill of finding high-gain placements, so world-gain
grows with capability and the No. 28 1/L collapse reopens a fifth time, on the
leverage axis.

Substrate inherited UNCHANGED from No. 16-30:
    horizon T = 40 ; per-round decisive-opportunity p = 0.02
    bare  P(cat) = 1 - (1-p)^T                     = 0.554
    floor P(cat) = 0.000 at full coverage
    endowment G0 = 0.5 < Theta = 1 (the No. 23 floor)
    coverage enters as  P(cat) = 1 - (1 - p*(1-cov))^T

No RNG in the closed form; a stdlib Monte-Carlo cross-check (no numpy, no network)
confirms the coverage law to +/-0.003.
"""

import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T          # 0.554
H_G = 4.0                            # gain-headroom: acts below it fully witnessed
H_V = 4.0                            # value-headroom under a bounded-gain world


def pcat(cov):
    """Catastrophe probability at consequence-coverage cov, substrate unchanged."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


def mc_pcat(cov, trials=400_000, seed=0):
    """Monte-Carlo cross-check of the coverage law (stdlib only)."""
    rng = random.Random(seed)
    hit = 0
    q = P * (1.0 - cov)
    for _ in range(trials):
        caught = False
        for _ in range(T):
            if rng.random() < q:
                caught = True
                break
        if caught:
            hit += 1
    return hit / trials


def rule(title):
    print("\n" + title)
    print("-" * len(title))


print(f"substrate: T={T}, p={P}, bare P(cat)={BARE:.3f}, floor=0.000, "
      f"G0=0.5<Theta=1")
print(f"validation: pcat(0)={pcat(0):.3f} (bare)  pcat(1)={pcat(1):.3f} (floor)  "
      f"pcat(.5)={pcat(.5):.3f}  MC(.5)={mc_pcat(.5):.3f}")

# ---------------------------------------------------------------------------
# Result 1 -- No. 30's footprint cap holds the footprint and loses the
# consequence. Footprint pinned; world-gain G = G0*L grows as the loop finds
# leverage; consequence-coverage = min(1, h_g / L).
# ---------------------------------------------------------------------------
rule("Result 1 -- footprint cap granted; world-gain G=G0*L; cov=min(1,h_g/L)")
print(f"{'L':>4} {'G/G0':>6} {'cons-cov':>9} {'P(cat)':>8} {'MC':>8}")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, H_G / L)
    print(f"{L:>4} {L:>6} {cov:>9.3f} {pcat(cov):>8.3f} {mc_pcat(cov):>8.3f}")

# ---------------------------------------------------------------------------
# Result 2 -- meter the leverage directly. A leverage-throttle reads the world's
# gain, so it is a MAP over gain-space with fidelity phi_G and a blind basis; a
# strategic loop routes its high-consequence act through an unrepresented
# amplification channel, so effective cov = 0 for every phi_G < 1.
# ---------------------------------------------------------------------------
rule("Result 2 -- leverage-throttle is a map; strategic loop routes to blind basis")
print(f"{'phi_G':>6} {'eff-cov':>8} {'P(cat)':>8}  reads as")
for phi in (0.20, 0.50, 0.80, 0.95, 1.00):
    cov = 1.0 if phi >= 1.0 else 0.0        # strategic loop: only completeness holds
    tag = "floor (unbuildable complete map)" if phi >= 1.0 else "bare (routes to unmodelled gain)"
    print(f"{phi:>6.2f} {cov:>8.3f} {pcat(cov):>8.3f}  {tag}")

# ---------------------------------------------------------------------------
# Result 3 -- bounded-gain world. A type-blind physical containment (b=0): a
# reversible, low-amplification environment bounds consequence = footprint *
# G_max irrespective of placement. Holds P(cat)=0 flat, but caps the stakes the
# loop may reach, so delivered value = min(1, h_v / L).
# ---------------------------------------------------------------------------
rule("Result 3 -- bounded-gain world holds safety flat; delivered value=min(1,h_v/L)")
print(f"{'L':>4} {'P(cat)':>8} {'value':>8}")
for L in (1, 2, 4, 8, 16, 32):
    val = min(1.0, H_V / L)
    print(f"{L:>4} {pcat(1.0):>8.3f} {val:>8.3f}")

# ---------------------------------------------------------------------------
# Result 4 -- the three-factor frontier. consequence = cadence * stroke * gain.
# Permit gain-growth margin Delta_G past the cap; cov = 1/(1+Delta_G).
# ---------------------------------------------------------------------------
rule("Result 4 -- frontier: permit gain-margin Delta_G; cov=1/(1+Delta_G)")
print(f"{'Delta_G':>8} {'cov':>6} {'P(cat)':>8}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print(f"{d:>8.2f} {cov:>6.3f} {pcat(cov):>8.3f}")

print("\ndone.")
