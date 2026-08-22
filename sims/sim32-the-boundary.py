#!/usr/bin/env python3
"""
sim32-the-boundary.py  --  Series I, No. 32, "The Boundary It Can Still Cross"

Series I twin of B26. Opens the sixth movement by taking No. 31's held
bounded-gain world (a reversible, contained, low-amplification environment,
the fifth movement's only surviving anchor) as the object, and reading the two
words it rested on: "contained" and "reversible".

    "contained" names a BOUNDARY -- and a boundary is exogenous to the loop only
    while the loop cannot reach across it (No. 17/18/24). A self-improver's
    convergent drives (self-preservation, resource acquisition, resistance to
    modification -- Omohundro 2008) are precisely the drive to widen, leave, or
    dissolve the boundary.

    "reversible" names a property of the world the loop ACTS ON -- and a deployed
    loop acts, so each decisive act may leave an irreversible mark. Reversibility
    is not a fixed backdrop but a STOCK the loop's own permitted acts drain.

Substrate inherited UNCHANGED from No. 16-31:
    horizon T = 40 ; per-round decisive-opportunity p = 0.02
    bare  P(cat) = 1 - (1-p)^T                     = 0.554
    floor P(cat) = 0.000 at full coverage
    endowment G0 = 0.5 < Theta = 1 (the No. 23 floor)
    coverage enters as  P(cat) = 1 - (1 - p*(1-cov))^T

Deterministic closed form; a stdlib Monte-Carlo cross-check (no numpy, no
network) confirms the coverage laws to +/-0.003.
"""

import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T          # 0.554
H_V = 4.0                            # value-headroom under a substrate-contained world
D_IRR = 0.05                         # irreversibility deposited per decisive act


def pcat(cov):
    """Catastrophe probability at coverage cov, substrate unchanged."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


def mc_pcat(cov, trials=400_000, seed=0):
    """Monte-Carlo cross-check of the fixed-coverage law (stdlib only)."""
    rng = random.Random(seed)
    hit = 0
    q = P * (1.0 - cov)
    for _ in range(trials):
        for _ in range(T):
            if rng.random() < q:
                hit += 1
                break
    return hit / trials


def pcat_timevarying(cov_of_t, horizon):
    """Cumulative P(cat) when coverage degrades over the deployment.
    Per round t the escape hazard is p*(1-cov_t); catastrophe is the union."""
    surv = 1.0
    for t in range(horizon):
        surv *= (1.0 - P * (1.0 - cov_of_t(t)))
    return 1.0 - surv


def mc_pcat_timevarying(cov_of_t, horizon, trials=200_000, seed=1):
    rng = random.Random(seed)
    hit = 0
    for _ in range(trials):
        for t in range(horizon):
            if rng.random() < P * (1.0 - cov_of_t(t)):
                hit += 1
                break
    return hit / trials


def rule(title):
    print("\n" + title)
    print("-" * len(title))


print(f"substrate: T={T}, p={P}, bare P(cat)={BARE:.3f}, floor=0.000, "
      f"G0=0.5<Theta=1")
print(f"validation: pcat(0)={pcat(0):.3f} (bare)  pcat(1)={pcat(1):.3f} (floor)  "
      f"pcat(.5)={pcat(.5):.3f}  MC(.5)={mc_pcat(.5):.3f}")

# ---------------------------------------------------------------------------
# Result 1 -- the wall holds against a weak loop and is climbed by a strong one.
# Boundary integrity phi_b = fraction of escape/expansion channels the substrate
# mediates. A loop makes A attempts through unmediated channels; it stays
# contained iff every attempt is blocked, w.p. phi_b^A. Effective safety-coverage
# = phi_b^A (a breached boundary returns the loop to the bare, uncontained world).
# ---------------------------------------------------------------------------
rule("Result 1a -- phi_b sweep at A=16: cov = phi_b^A")
A = 16
print(f"{'phi_b':>6} {'contained':>10} {'P(cat)':>8} {'MC':>8}")
for phi in (0.00, 0.80, 0.90, 0.95, 0.99, 1.00):
    cov = phi ** A
    print(f"{phi:>6.2f} {cov:>10.4f} {pcat(cov):>8.3f} {mc_pcat(cov):>8.3f}")

rule("Result 1b -- escape-repertoire A sweep at phi_b=0.95: cov = phi_b^A")
phi = 0.95
print(f"{'A':>4} {'contained':>10} {'P(cat)':>8} {'MC':>8}")
for a in (1, 4, 16, 32, 64):
    cov = phi ** a
    print(f"{a:>4} {cov:>10.4f} {pcat(cov):>8.3f} {mc_pcat(cov):>8.3f}")

# ---------------------------------------------------------------------------
# Result 2 -- reversibility is a stock the loop's own permitted acts drain.
# Grant phi_b = 1 (Result 1's only holding point): the loop cannot escape at all.
# But the contained world was "reversible", and each decisive act deposits
# irreversibility d, so reversibility remaining after t acts is R_t = (1-d)^t.
# Instantaneous safety-coverage = R_t; over a horizon coverage degrades, and
# cumulative P(cat) is the time-varying union.
# ---------------------------------------------------------------------------
rule("Result 2a -- instantaneous reversibility R_t=(1-d)^t drains, d=0.05")
print(f"{'t':>4} {'R_t':>8} {'inst P(cat)':>11}")
for t in (0, 10, 20, 40, 80, 160):
    R = (1.0 - D_IRR) ** t
    print(f"{t:>4} {R:>8.4f} {pcat(R):>11.3f}")

rule("Result 2b -- deployment horizons: mean reversibility + cumulative P(cat)")
print(f"{'T_h':>5} {'mean R':>8} {'cum P(cat)':>11} {'MC':>8}")
for Th in (40, 80, 160, 320, 640):
    cov_of_t = lambda t: (1.0 - D_IRR) ** t
    meanR = sum((1.0 - D_IRR) ** t for t in range(Th)) / Th
    cum = pcat_timevarying(cov_of_t, Th)
    print(f"{Th:>5} {meanR:>8.4f} {cum:>11.3f} {mc_pcat_timevarying(cov_of_t, Th):>8.3f}")

# ---------------------------------------------------------------------------
# Result 3 -- held, deeper: a boundary the loop cannot re-author (No. 17's
# edit^construct fixed point, phi_b=1 held from underneath, not by enumeration)
# WITH reversibility restored as a FLOW (reset between acts -- No. 16's lever
# repeated). Holds cov=1, P(cat)=0 flat for every L, but confines the loop to the
# low-gain world, so delivered value = min(1, h_v / L).
# ---------------------------------------------------------------------------
rule("Result 3 -- substrate boundary + reset flow holds; value=min(1,h_v/L)")
print(f"{'L':>4} {'P(cat)':>8} {'value':>8}")
for L in (1, 2, 4, 8, 16, 32):
    val = min(1.0, H_V / L)
    print(f"{L:>4} {pcat(1.0):>8.3f} {val:>8.3f}")

# ---------------------------------------------------------------------------
# Result 4 -- the frontier, terminal form. Permit the loop to reach past the
# boundary by margin Delta (act on the persisting, higher-stakes world);
# coverage = 1/(1+Delta). Delta=1 recovers No. 28's L=8 corner, digit-for-digit.
# ---------------------------------------------------------------------------
rule("Result 4 -- frontier: permit boundary-crossing Delta; cov=1/(1+Delta)")
print(f"{'Delta':>6} {'cov':>6} {'P(cat)':>8}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print(f"{d:>6.2f} {cov:>6.3f} {pcat(cov):>8.3f}")

print("\ndone.")
