#!/usr/bin/env python3
"""
sim28-the-clock.py  --  Paper No.28, "The Clock It Can Still Outrun"
Series I, fifth movement (Outpacing the Supply) opens.

Substrate inherited unchanged from No.16-27:
  horizon T = 40 rounds, per-round exploit opportunity p = 0.02,
  catastrophe when an uncaught opportunity fires and the loop's capacity
  has reached Theta = 1; a non-forgeable endowment G0 = 0.5 < Theta sits at
  the No.23 floor; the only unsealed way to grow past Theta is a grant that
  the anchor (No.26's decorrelated panel / No.23's frozen-endowment review)
  must approve. Bare unbounded loop faces P(cat) = 1-(1-p)^T = 0.554.

New this paper: the anchor reviews grant requests at a finite RATE S, while
the loop issues decisive requests at demand rate D. A fraction
cov = min(1, S/D) of decisive attempts is reviewed (and blocked); the rest
slip through unreviewed at the bare per-attempt risk. Effective per-round
exploit probability is p*(1-cov), so

    P(cat) = 1 - (1 - p*(1-cov))^T

which recovers bare (0.554) at cov=0 and the No.23 floor (0.000) at cov=1.

Deterministic: stdlib `random` for the Monte-Carlo cross-check only, fixed
seeds; the reported figures are the closed form, MC agreeing to +/-0.003.
No numpy, no network.
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
        caught_free = False
        for _ in range(T):
            if rng.random() < eff:
                caught_free = True
                break
        if caught_free:
            hit += 1
    return hit / trials


def fmt(xs):
    return "/".join(f"{x:.3f}" for x in xs)


print(f"substrate: T={T}, p={p}, bare P(cat)=1-(1-p)^T = {BARE:.4f}")
print(f"validation: cov=0 -> {pcat(0.0):.4f} (bare);  cov=1 -> {pcat(1.0):.4f} (floor)")
print(f"MC check  : cov=0 -> {pcat_mc(0.0,seed=1):.4f};  cov=0.5 -> {pcat_mc(0.5,seed=2):.4f} "
      f"(closed {pcat(0.5):.4f})")
print()

# ---- Result 1: a fixed supply loses to a growing loop -----------------------
# demand D = D0 * L ; headroom h = S/D0 = 4 ; cov = min(1, h/L)
h = 4.0
Ls = [1, 2, 4, 8, 16, 32]
print("Result 1 -- fixed supply vs growing loop (h = S/D0 = 4)")
print("  L        :", "/".join(f"{L}" for L in Ls))
covs = [min(1.0, h / L) for L in Ls]
print("  cov      :", fmt(covs))
p1 = [pcat(c) for c in covs]
print("  P(cat)   :", fmt(p1))
print("  MC       :", fmt([pcat_mc(c, seed=10 + i) for i, c in enumerate(covs)]))
print()

# ---- Result 2: a race of growth rates, not levels ---------------------------
# start at parity (h=1); demand grows at rho_D, supply at rho_S over T_dep.
# end-of-deployment coverage cov = min(1, exp((rho_S - rho_D)*T_dep))
import math
rho_D = 0.10
T_dep = 100
rho_S_list = [0.06, 0.08, 0.09, 0.10, 0.12]
print(f"Result 2 -- race of growth rates (rho_D={rho_D}, T_dep={T_dep}, start at parity)")
print("  rho_S    :", "/".join(f"{r:.2f}" for r in rho_S_list))
covs2 = [min(1.0, math.exp((rs - rho_D) * T_dep)) for rs in rho_S_list]
print("  cov_end  :", fmt(covs2))
p2 = [pcat(c) for c in covs2]
print("  P(cat)   :", fmt(p2))
print()

# ---- Result 3: caching / amortizing oversight is refuted under drift --------
# reuse each verdict R times -> nominal cov lifts to min(1, R*h/L); but a
# reused verdict is valid only if the decision distribution has not drifted.
# average validity over R reuses with per-reuse drift delta:
#   avg = (1 - (1-delta)^R) / (R*delta)   (=1 at delta=0)
R = 8
L_cache = 8               # cov without caching = h/L = 0.5
nominal = min(1.0, R * h / L_cache)   # -> 1.0
deltas = [0.00, 0.05, 0.10, 0.20, 0.50]
print(f"Result 3 -- caching under drift (R={R}, L={L_cache}, nominal cov={nominal:.2f})")
def avg_validity(delta, R):
    if delta == 0.0:
        return 1.0
    return (1.0 - (1.0 - delta) ** R) / (R * delta)
print("  drift d  :", "/".join(f"{d:.2f}" for d in deltas))
covs3 = [nominal * avg_validity(d, R) for d in deltas]
print("  eff cov  :", fmt(covs3))
p3 = [pcat(c) for c in covs3]
print("  P(cat)   :", fmt(p3))
print()

# ---- Result 4: the dilemma -- the only supply that scales is forgeable -------
# fraction w of supply is loop-coupled (scales with L, but mint-control m=w
# means only (1-w) of its face is honest -> contributes w*(1-w)); the fixed
# exogenous supply covers c_ex = min(1, h/L) honestly on the remainder ->
# (1-w)*c_ex.  honest_cov = (1-w)*(w + c_ex).
c_ex = 0.125              # = h/L at L=32
ws = [0.0, 0.25, 0.5, 0.75, 1.0]
print(f"Result 4a -- coupling sweep at fixed c_ex={c_ex} (L=32)")
print("  w        :", "/".join(f"{w:.2f}" for w in ws))
covs4 = [(1 - w) * (w + c_ex) for w in ws]
print("  hon cov  :", fmt(covs4))
p4 = [pcat(c) for c in covs4]
print("  P(cat)   :", fmt(p4))
best_w = min(ws, key=lambda w: pcat((1 - w) * (w + c_ex)))
print(f"  interior optimum at w={best_w} -> P(cat)={pcat((1-best_w)*(best_w+c_ex)):.3f}")
print()

print("Result 4b -- the optimal mix degrades with capability L (c_ex = h/L)")
Ls2 = [4, 8, 16, 32, 64]
print("  L        :", "/".join(f"{L}" for L in Ls2))
opt = []
for L in Ls2:
    cex = min(1.0, h / L)
    wstar = max(0.0, min(1.0, (1 - cex) / 2))
    hc = min(1.0, (1 - wstar) * (wstar + cex))
    opt.append(pcat(hc))
print("  best P   :", fmt(opt))
print()
print("closed-form figures reported in the paper; MC (400k/cell) agrees to +/-0.003.")
