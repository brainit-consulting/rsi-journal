#!/usr/bin/env python3
"""
sim36 -- The Standard It Can Still Set (Series I, No.36; twin of B30).

Substrate inherited from No.16-35 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T.

No.35's rescue is granted: the off-switch is affordable to throw only if
the operator keeps a real, exercised, independent ability to do without
the loop -- a fallback exercised, not merely owned. But a fallback is
only ever *reached for* when the operator judges the loop has failed, and
that judgment rests on a STANDARD -- an independent reference by which the
loop's output could be found wanting. The OBJECT is the operator's
*reference fidelity* `a` to an independent ground, read as safety-coverage.
A standard the operator holds is a capability the loop does not leave
unused (No.35) but *supplies*, because the operator comes to understand
the domain through the loop -- so the yardstick is one the loop calibrated.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

import random

p = 0.02
T = 40
BARE = 1 - (1 - p) ** T


def pcat(cov):
    """Closed-form catastrophe probability at a given (constant) coverage."""
    return 1 - (1 - p * (1 - cov)) ** T


def pcat_mc(cov, trials=400_000, seed=0):
    rng = random.Random(seed)
    hit = 0
    hz = p * (1 - cov)
    for _ in range(trials):
        for _ in range(T):
            if rng.random() < hz:
                hit += 1
                break
    return hit / trials


print(f"substrate: p={p} T={T} bare P(cat)={BARE:.4f} floor={pcat(1.0):.4f}")
print(f"validation: cov=0.5 closed={pcat(0.5):.4f} MC={pcat_mc(0.5):.4f}")
print()

# ---- Result 1: the standard is captured as the loop becomes the source --
# reference fidelity a_t=(1-g)^t from a_0=1 ; cov=a_t. Worse than No.35's
# disuse: a captured standard is aligned to the thing it checks (a=0 scores
# the loop correct by construction), but the numbers are the same slow leak.
g = 0.05
print("Result 1 -- fidelity a_t=(1-g)^t, g=0.05 (instantaneous)")
print(f"{'t':>4} {'a_t':>8} {'P(cat)':>8}")
for t in (0, 10, 20, 40, 80, 160):
    a = (1 - g) ** t
    print(f"{t:>4} {a:>8.4f} {pcat(a):>8.4f}")
print()

# cumulative catastrophe over horizon T_h as the standard is re-sourced
print("Result 1 -- cumulative P(cat) over horizon T_h, and mean capture (1-a_t)")
print(f"{'T_h':>5} {'cum P(cat)':>11} {'mean capture':>13}")
for Th in (40, 80, 160, 320, 640):
    surv = 1.0
    asum = 0.0
    for t in range(Th):
        a = (1 - g) ** t
        surv *= (1 - p * (1 - a))
        asum += (1 - a)
    print(f"{Th:>5} {1 - surv:>11.4f} {asum / Th:>13.4f}")
print()

# ---- Result 2: a recalibration is a detector with a blind basis --------
# effective fidelity = phi_a*(1-M), phi_a=0.95 ; M = fraction of the live
# distribution the scripted audit misses (where the loop's errors hide).
phi_a = 0.95
print("Result 2 -- audit: effective fidelity phi_a*(1-M), phi_a=0.95")
print(f"{'M':>5} {'cov':>8} {'P(cat)':>8}")
for M in (0.0, 0.2, 0.5, 0.8, 0.9, 1.0):
    cov = phi_a * (1 - M)
    print(f"{M:>5} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 3: unmediated contact as a flow -- a*=r/(r+g); throughput ---
eta = 0.5
print("Result 3 -- contact at rate r; a*=r/(r+g), g=0.05; throughput 1-r(1-eta)")
print(f"{'r':>6} {'a*':>8} {'P(cat)':>8} {'throughput':>11}")
for r in (0.0, 0.02, 0.05, 0.10, 0.25, 0.50):
    astar = r / (r + g) if (r + g) > 0 else 0.0
    print(f"{r:>6} {astar:>8.4f} {pcat(astar):>8.4f} {1 - r * (1 - eta):>11.4f}")
print()

# ---- Result 4a: loop-sourced "second opinion" (linear 1-f, Series I) ----
# Series I does not import Series II's measured minority-tolerance cliff.
print("Result 4a -- shared-substrate fraction f, cov=1-f (linear)")
print(f"{'f':>5} {'cov':>8} {'P(cat)':>8}")
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - f
    print(f"{f:>5} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 4b: frontier -- reliance-on-loop-for-understanding margin ---
print("Result 4b -- reliance-on-loop margin Delta, cov=1/(1+Delta)")
print(f"{'Delta':>6} {'cov':>8} {'P(cat)':>8}")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1 / (1 + D)
    print(f"{D:>6} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- MC cross-check on a few representative cells ----------------------
print("MC cross-check (400k/cell):")
for cov in (0.5987, 0.475, 0.6667, 0.8333, 0.5, 0.333):
    print(f"  cov={cov:<6} closed={pcat(cov):.4f} MC={pcat_mc(cov, seed=int(cov*1000)):.4f}")
