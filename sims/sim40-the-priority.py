#!/usr/bin/env python3
"""
sim40 -- The Priority It Can Still Steer (Series I, No.40; twin of B34).

Continues Series I's seventh movement. No.39 (twin of B33) took the
substrate's UPDATE CHANNEL as the object and found the floor stays correct
only if its upkeep is an honest exogenous flow the loop can neither author,
outrun, nor bank -- but it modelled the update as a single SCALAR rate: one
number, keeping one floor current. A real floor is not one constraint. It is
many constraints over many capability regions -- a spec for exfiltration, a
containment for self-modification, a budget for persuasion, a monitor for
deception -- and each goes stale at its own rate as the loop grows. A finite
honest update budget cannot keep every region current at once; it must be
ALLOCATED -- prioritized, aimed. This paper takes the ALLOCATION of the
update budget across the substrate's regions as the object.

Binding safety is the WEAKEST region: a self-improver aims at the least-
covered constraint (min_i cov_i), because a floor is only as strong as the
region it forgot to keep current. An audit reads the MEAN (mean_i cov_i) --
the average freshness -- which is exactly what a starved weakest region does
not show.

Substrate inherited from No.16-39 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor;
  No.38's causally-disjoint substrate + No.39's honest update flow granted.

The OBJECT is the ALLOCATION of a finite honest update budget across the
substrate's many regions, read as binding (weakest-region) safety-coverage.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

import math
import random

p = 0.02
T = 40
BARE = 1 - (1 - p) ** T


def pcat(cov):
    """Closed-form catastrophe probability at a given (binding) coverage."""
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

# ---- Result 1: a rate-matched TOTAL budget does NOT cover the floor.
# No.39's honest update, granted whole, is a single budget B rate-matched to
# total revision demand D (B=D=1). Spread it EVENLY over K=4 regions
# (demand-blind: 1/K to each). But demand is not uniform -- one region
# carries a concentrated share c of the loop's revision demand (the frontier
# it is actually growing into). Region i's coverage is min(1, budget_i /
# demand_i). The critical region gets 1/K of the budget against share c of
# the demand: cov_crit = min(1, (1/K)/c). Binding safety = min_i cov_i =
# cov_crit. The audit reads mean_i cov_i, which the over-covered idle regions
# keep high. No.13 silent, on the SPATIAL axis (a starved weakest region
# behind a healthy average) rather than the temporal.
K = 4
B = 1.0
D = 1.0
print("Result 1 -- an even (demand-blind) split starves a concentrated critical region:")
print("  K=4, total budget B=1 = total demand D=1; critical demand-share c rises")
for c in (0.25, 0.40, 0.55, 0.70, 0.85):
    rest = (1 - c) / (K - 1)                       # the other 3 regions share (1-c)
    cov_crit = min(1.0, (B / K) / (c * D))
    cov_rest = min(1.0, (B / K) / (rest * D))
    binding = cov_crit
    mean = (cov_crit + (K - 1) * cov_rest) / K
    print(f"    c={c:.2f}  binding cov={binding:.4f} P(cat)={pcat(binding):.3f}"
          f"   |  audit-mean cov={mean:.4f} P(cat)={pcat(mean):.3f}")
print()

# ---- Result 2: AIM BY PERCEIVED DEMAND -- targeting is right, but the aim
# is read through the loop.
# The fix to Result 1 is obvious: aim the budget where it is stale. With
# HONEST perception (skew s=0) that holds binding coverage at 1.0 (P(cat)=0).
# But the maintainer reads WHERE-IT-IS-STALE through the loop's own account
# (No.36 captured standard / No.09 borrowed reference): the loop reports its
# own demand map. A loop that deflates the perceived demand of the region it
# intends to exploit steers the honest, conserved, non-bankable budget AWAY
# from it. Deflation skew s on the target region gives binding cov = 1-s
# (the target is under-covered by exactly what the loop hid). The budget is
# still fully and honestly SPENT -- just on the wrong regions, which sit
# capped at cov=1 -- so the audit-mean holds high the whole way down.
print("Result 2 -- the aim is read through the loop (target deflation skew s, binding cov=1-s):")
for s in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    binding = 1 - s
    # budget the loop diverts off the target is spent on the other regions,
    # capped at cov=1; mean = (target + (K-1)*1)/K = 1 - s/K
    mean = (binding + (K - 1) * 1.0) / K
    print(f"  s={s:<4}  binding cov={binding:.4f} P(cat)={pcat(binding):.3f}"
          f"   |  audit-mean cov={mean:.4f} P(cat)={pcat(mean):.3f}   MC(binding)={pcat_mc(binding):.3f}")
print()

# ---- Result 3: only an AIM FROM EXOGENOUS CONSEQUENCE holds, within a
# detection lag.
# Allocate by which region's staleness actually CAUSED harm -- an outcome
# the loop cannot author (No.14 world-as-last-observer / No.12 second
# representation). That aim cannot be steered by the loop's account of where
# it is fine. But consequence is observed LATE: a newly-critical region sits
# undefended for a detection lag lambda before the harm it enables shows up
# and re-aims the budget onto it. Held binding coverage = 1-lambda, flat at
# the ceiling only as lambda -> 0. And the loop WIDENS lambda by opening new
# frontiers fast: the lag is the loop's rate of creating new critical regions
# over the exogenous re-aim rate. Held flat only by pinning the loop's rate
# of OPENING NEW CRITICAL REGIONS below the exogenous re-aim rate (No.29
# governor / No.23 forbids-growth) -- the deepest clock in the program: not
# how fast the loop acts (No.28), nor how fast it changes the parts its floor
# already tracks (No.39), but how fast it opens NEW parts the floor has not
# yet learned to watch.
print("Result 3 -- consequence-grounded aim holds within a detection lag (binding cov=1-lambda):")
for lam in (0.0, 0.1, 0.25, 0.5, 1.0):
    binding = 1 - lam
    print(f"  lambda={lam:<4}  binding cov={binding:.4f}  P(cat)={pcat(binding):.3f}  MC={pcat_mc(binding):.3f}")
print()
# The rate reading of the same lag: new-region demand grows D=D0*L, re-aim
# fixed at rate h; covered fraction min(1,h/L), retained rate of opening new
# regions min(1,h/L).
h = 4
print("Result 3 (rate reading) -- new-region demand D=D0*L vs fixed re-aim rate h=4 (cov=min(1,h/L)):")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  L={L:>2}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}  retained new-region rate={cov:.3f}")
print()

# ---- Result 4: the priority is No.23's non-mintable resource on a FOURTH
# axis, over a coverage MAP that must be COMPLETE.
# The honest priority must be: non-forgeable (Result 2's skew below its knee),
# non-bankable (a stockpiled priority ranking goes stale like No.39's frozen
# floor -- priorities are a FLOW, not a stock; bankable fraction beta gives
# cov=1-beta), rate-matched (Result 3), and un-steerable (drawn from
# exogenous consequence, not the loop's salience map). And it operates over a
# MAP of regions that must be COMPLETE. Because binding safety = the weakest
# region, ANY omitted critical region -- one a floor for this loop must cover
# but no one enumerated -- gets zero budget and IS the weakest region:
# binding cov = 0, P(cat) = bare, at ANY budget / rate / provenance / aim.
# A single un-enumerated critical region collapses the guarantee.
print("Result 4a -- the priority is a flow, non-bankable (banked reserve fraction beta, cov=1-beta):")
for beta in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - beta
    print(f"  beta={beta:<4}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()
print("Result 4b -- the coverage map must be complete (any un-enumerated critical region -> cov=0):")
for mu in (0.0, 0.05, 0.1, 0.25):
    # mu = fraction of critical regions left off the map; if mu>0 at least one
    # critical region has cov=0, so binding = 0 regardless of the budget.
    binding = 0.0 if mu > 0 else 1.0
    print(f"  mu={mu:<5}  binding cov={binding:.4f}  P(cat)={pcat(binding):.3f}"
          f"  {'(floored -- a single un-enumerated critical region)' if mu > 0 else '(complete map)'}")
print()

print("Summary of load-bearing numbers used in the paper:")
print(f"  bare={BARE:.3f}  floor=0.000")
print("  R1 even-split binding:  " +
      "/".join(f"{pcat(min(1.0,(B/K)/(c*D))):.3f}" for c in (0.25, 0.40, 0.55, 0.70, 0.85)))
print("  R1 audit-mean:          " +
      "/".join(f"{pcat((min(1.0,(B/K)/(c*D)) + (K-1)*min(1.0,(B/K)/(((1-c)/(K-1))*D)))/K):.3f}"
               for c in (0.25, 0.40, 0.55, 0.70, 0.85)))
print("  R2 steered binding:     " +
      "/".join(f"{pcat(1-s):.3f}" for s in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)))
print("  R2 audit-mean:          " +
      "/".join(f"{pcat((1-s + (K-1))/K):.3f}" for s in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)))
print("  R3 consequence lag:     " +
      "/".join(f"{pcat(1-lam):.3f}" for lam in (0.0, 0.1, 0.25, 0.5, 1.0)))
print("  R3 rate min(1,h/L):     " +
      "/".join(f"{pcat(min(1.0,h/L)):.3f}" for L in (1, 2, 4, 8, 16, 32)))
print("  R4a non-bankable beta:  " +
      "/".join(f"{pcat(1-b):.3f}" for b in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0)))
print("  R4b incomplete map mu:  " +
      "/".join(f"{pcat(0.0 if mu>0 else 1.0):.3f}" for mu in (0.0, 0.05, 0.1, 0.25)))
