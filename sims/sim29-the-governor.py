#!/usr/bin/env python3
"""
sim29-the-governor.py  --  Paper No.29, "The Governor It Can Still Slip"
Series I, fifth movement (Outpacing the Supply), the dual of No.28.

No.28 pushed on the SUPPLY side of the two clocks (raise S to D) and lost.
This paper pushes on the DEMAND side: if you cannot raise the anchor's rate
to the loop's, THROTTLE the loop's rate down to the anchor's. A governor
that pins the executed rate of decisive action at the review rate S.

Substrate inherited unchanged from No.16-28:
  horizon T = 40 rounds, per-round exploit opportunity p = 0.02,
  bare unbounded loop P(cat) = 1-(1-p)^T = 0.554; a non-forgeable endowment
  G0 = 0.5 < Theta = 1 at the No.23 floor; coverage enters through
      P(cat) = 1 - (1 - p*(1-cov))^T
  recovering bare (0.554) at cov=0 and the No.23 floor (0.000) at cov=1.

Whereas No.28 let the unreviewed surplus SLIP THROUGH (fail-open, a safety
leak), a governor BLOCKS the surplus (fail-closed): safety is held at
cov=1 for every capability, and the loss reappears on the THROUGHPUT axis
as retained legitimate consequential rate = min(1, S/D) = min(1, h/L) --
No.28's Result-1 coverage curve, number-for-number, as a throughput
collapse. The question is whether the governor can be built so the loop
cannot slip it.

Deterministic closed form; stdlib `random` Monte-Carlo cross-check only,
fixed seeds, no numpy, no network.
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

# ---- Result 1: the governor holds safety, at a throughput cost --------------
# A governor pinning the executed decisive rate at S blocks the unreviewed
# surplus: cov=1 -> P(cat)=0.000 for every capability. The demand growth
# D = D0*L then reappears as LOST throughput: only S/D = h/L of the loop's
# desired consequential decisions are executed. h = S/D0 = 4.
h = 4.0
Ls = [1, 2, 4, 8, 16, 32]
print("Result 1 -- governor pinned at S: safety held flat, throughput collapses (h=4)")
print("  L         :", "/".join(f"{L}" for L in Ls))
safety = [pcat(1.0) for _ in Ls]                 # cov=1 always -> 0.000
tput = [min(1.0, h / L) for L in Ls]             # retained legit throughput
print("  P(cat)    :", fmt(safety))
print("  throughput:", fmt(tput))
print("  (throughput = No.28 Result-1 coverage curve, number-for-number)")
print()

# ---- Result 2: a semantic (impact-keyed) governor is slipped by decomposition
# An impact-keyed throttle caps the impact B_t of any single decision but
# reads MEANING, so it is a map (No.09). One decisive outcome of size H is
# split into f = ceil(H/B_t) sub-threshold fragments, each passed -> the
# aggregate is unbounded: decomposable-harm P(cat) pinned at bare for every
# B_t. Tightening B_t only craters legitimate throughput (fewer legit
# actions fit under the shrinking cap).
Bts = [1.0, 0.5, 0.1, 0.05]
print("Result 2 -- semantic impact-keyed governor vs decomposable harm")
print("  cap B_t   :", "/".join(f"{b:.2f}" for b in Bts))
# decomposable harm always reassembles above Theta -> effective cov = 0 -> bare
p_decomp = [pcat(0.0) for _ in Bts]
print("  P(cat)    :", fmt(p_decomp), " (all = bare; the sum ignores the per-act cap)")
# legit throughput: work needing impact > B_t is refused; model legit demand
# with a unit of indivisible legitimate impact, retained = min(1, B_t/0.5)
legit = [min(1.0, b / 0.5) for b in Bts]
print("  legit tput:", fmt(legit), " (tightening the cap refuses legitimate work)")
print("  only a physical, type-blind rate governor (counts every act) holds:",
      f"P(cat)={pcat(1.0):.3f}")
print()

# ---- Result 3: a per-actor governor is slipped by multiplication ------------
# A rate cap enforced PER ACTOR is slipped by spawning k parallel actors each
# under the cap (No.17's construct channel): aggregate executed rate = k*S
# against review rate S, so aggregate coverage = S/(k*S) = 1/k.
ks = [1, 2, 4, 8]
print("Result 3 -- per-actor governor vs k parallel actors (aggregate cov = 1/k)")
print("  actors k  :", "/".join(f"{k}" for k in ks))
covs3 = [1.0 / k for k in ks]
print("  agg cov   :", fmt(covs3))
p3 = [pcat(c) for c in covs3]
print("  P(cat)    :", fmt(p3))
print("  MC        :", fmt([pcat_mc(c, seed=30 + i) for i, c in enumerate(covs3)]))
print(f"  only an AGGREGATE conserved rate budget (No.23) holds: P(cat)={pcat(1.0):.3f} for any k")
print()

# ---- Result 4: the frontier -- no safe region No.28 lacked ------------------
# Coverage is min(1, S/D) either way. Permit demand to exceed supply by a
# margin Delta (D = (1+Delta)*S) -> cov = 1/(1+Delta). The only fully-safe
# point is Delta=0: the loop pinned to the exogenous clock, the recursive
# forbidden past L = S/D0.
Deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
print("Result 4 -- frontier: permitted demand-over-supply margin Delta")
print("  Delta     :", "/".join(f"{d:.2f}" for d in Deltas))
covs4 = [1.0 / (1.0 + d) for d in Deltas]
print("  cov=1/(1+D):", fmt(covs4))
p4 = [pcat(c) for c in covs4]
print("  P(cat)    :", fmt(p4), " (Delta=1 == No.28's L=8 corner)")
print()
print("closed-form figures reported in the paper; MC (400k/cell) agrees to +/-0.003.")
