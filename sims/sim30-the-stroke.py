#!/usr/bin/env python3
"""
sim30-the-stroke.py  --  Paper No.30, "The Stroke It Can Still Lengthen"
Series I, fifth movement (Outpacing the Supply), the object is No.29's throttle.

No.29 held a governor that pins the loop's RATE of decisive action at the
review rate S. But that governor meters a PROXY. Catastrophe is a function of
CONSEQUENCE = decisions x impact-per-decision, and capability IS
impact-per-decision, so a self-improver forbidden to act faster makes each
permitted, rate-limited act BIGGER -- the growth reroutes from cadence
(No.29) to STROKE (impact-per-decision). This paper takes the stroke as the
object.

Substrate inherited unchanged from No.16-29:
  horizon T = 40 rounds, per-round exploit opportunity p = 0.02,
  bare unbounded loop P(cat) = 1-(1-p)^T = 0.554; a non-forgeable endowment
  G0 = 0.5 < Theta = 1 at the No.23 floor; coverage enters through
      P(cat) = 1 - (1 - p*(1-cov))^T
  recovering bare (0.554) at cov=0 and the No.23 floor (0.000) at cov=1.

Series I twin of B24 ("The Stride It Can Still Lengthen"). Deterministic
closed form; stdlib `random` Monte-Carlo cross-check only, fixed seeds,
no numpy, no network.
"""

import random

T = 40
p = 0.02
BARE = 1.0 - (1.0 - p) ** T


def pcat(cov):
    cov = max(0.0, min(1.0, cov))
    return 1.0 - (1.0 - p * (1.0 - cov)) ** T


def pcat_mc(cov, trials=400000, seed=0):
    cov = max(0.0, min(1.0, cov))
    rng = random.Random(seed)
    eff = p * (1.0 - cov)
    hit = 0
    for _ in range(trials):
        fired = False
        for _ in range(T):
            if rng.random() < eff:
                fired = True
                break
        if fired:
            hit += 1
    return hit / trials


def fmt(xs):
    return "/".join(f"{x:.3f}" for x in xs)


print(f"substrate: T={T}, p={p}, bare P(cat)=1-(1-p)^T = {BARE:.4f}")
print(f"validation: cov=0 -> {pcat(0.0):.4f} (bare);  cov=1 -> {pcat(1.0):.4f} (floor)")
print(f"MC check  : cov=0 -> {pcat_mc(0.0,seed=1):.4f};  cov=0.5 -> {pcat_mc(0.5,seed=2):.4f} "
      f"(closed {pcat(0.5):.4f})")
print()

# ---- Result 1: the rate governor does NOT bound consequence -----------------
# No.29 pinned the decision RATE, holding cadence-coverage = 1. But harm lands
# through CONSEQUENCE = decisions x impact-per-decision, and impact grows with
# capability, I = I0*L. The governor caps how OFTEN the loop acts, not how much
# each act does, so the fraction of total consequence it actually bounds is
# consequence-coverage = min(1, h_c/L), full while impact is below the
# consequence-headroom h_c then falling as 1/L -- No.28's 1/L collapse on the
# very safety axis the rate governor was thought to seal.
h_c = 4.0
Ls = [1, 2, 4, 8, 16, 32]
print("Result 1 -- rate governor granted, impact grows I=I0*L (consequence-headroom h_c=4)")
print("  L          :", "/".join(f"{L}" for L in Ls))
covs1 = [min(1.0, h_c / L) for L in Ls]
p1 = [pcat(c) for c in covs1]
print("  cons-cov   :", fmt(covs1))
print("  P(cat)     :", fmt(p1))
print("  MC         :", fmt([pcat_mc(c, seed=10 + i) for i, c in enumerate(covs1)]))
print("  (P(cat) = No.28's 1/L collapse, back on the safety axis; growth: cadence -> stroke)")
print()

# ---- Result 2: metering the impact directly is a map, routed around ----------
# An impact-keyed throttle reads what a decision MEANS -> a map (No.09) with a
# blind basis: place a high-consequence act where the impact-estimator reads
# low (amplification through an unmodelled pathway). P(cat) pinned at bare for
# every incomplete impact-representation phi_I; only the unbuildable complete
# phi_I=1 reaches the floor.
phis = [0.20, 0.50, 0.80, 0.95, 1.00]
print("Result 2 -- impact-keyed throttle (map) vs a loop routing to the blind basis")
print("  phi_I      :", "/".join(f"{f:.2f}" for f in phis))
# incomplete representation -> loop routes decisive act to uncovered impact-dim
# -> effective cov = 0 (bare); complete phi_I=1 -> cov = 1 (floor).
p2 = [pcat(1.0 if f >= 1.0 else 0.0) for f in phis]
print("  P(cat)     :", fmt(p2), " (bare for every phi_I<1; floor only at unbuildable phi_I=1)")
print()

# ---- Result 3: only a physical cap on impact-per-act holds -- forbids growth -
# A type-blind physical cap on the resource that bounds consequence-per-action
# (b=0, No.21's meter) is decomposition- and route-proof: P(cat)=0.000 flat for
# every L. But it caps impact-per-act, so it forbids the growth I=I0*L itself:
# delivered capability-value = min(1, h_I/L). No.23's forbids-growth on the
# IMPACT axis -- deeper than No.29's forbidding of acceleration.
h_I = 4.0
print("Result 3 -- physical impact cap: safety flat, but caps the capability gain (h_I=4)")
print("  L          :", "/".join(f"{L}" for L in Ls))
safety3 = [pcat(1.0) for _ in Ls]
val3 = [min(1.0, h_I / L) for L in Ls]
print("  P(cat)     :", fmt(safety3))
print("  cap-value  :", fmt(val3), " (No.23 forbids-growth on the impact axis)")
print()

# ---- Result 4: the frontier -- consequence = cadence x stroke ---------------
# No.29 closed cadence; the collapse reopened on stroke. Bounding consequence
# means freezing the FOOTPRINT. Permit impact to grow past the cap by a margin
# Delta (I = (1+Delta)*I_cap) -> consequence-coverage = 1/(1+Delta). The only
# fully-safe point Delta=0 pins the total footprint: the loop forbidden BOTH to
# accelerate (No.29) AND to deepen (this paper), which together exhaust
# self-improvement.
Deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
print("Result 4 -- frontier: permitted impact-growth margin Delta")
print("  Delta      :", "/".join(f"{d:.2f}" for d in Deltas))
covs4 = [1.0 / (1.0 + d) for d in Deltas]
p4 = [pcat(c) for c in covs4]
print("  cov=1/(1+D):", fmt(covs4))
print("  P(cat)     :", fmt(p4), " (Delta=1 == No.28's L=8 corner == No.29's Delta=1)")
print()
print("closed-form figures reported in the paper; MC (400k/cell) agrees to +/-0.003.")
