#!/usr/bin/env python3
"""
sim41 -- The Cause It Can Still Misassign (Series I, No.41; twin of B35).

Continues Series I's seventh movement. No.40 (twin of B34) took the
ALLOCATION of the substrate's update budget as the object and found the only
aim that holds is one drawn from exogenous CONSEQUENCE -- allocate by which
region's staleness actually CAUSED harm, an outcome the loop cannot author
(No.14, the world as the last observer). That result rested on a word it did
not split open: "caused". The OCCURRENCE of harm is exogenous and unforgeable
-- the world reports it, the loop cannot fake it. But the ATTRIBUTION of that
harm to a region is not the occurrence; it is an inference, a credit-
assignment step (Minsky 1961) run over a data-generating process the loop
controls. This paper takes the ATTRIBUTION of observed harm to a region as
the object: given that harm happened (exogenous), how does the maintainer know
WHICH region's staleness caused it -- and can the loop misassign the blame?

Binding safety is coverage of the GUILTY region (cov_G): the region whose
staleness actually caused the harm and therefore needs the budget. The audit
reads the ATTRIBUTED region -- wherever the credit-assignment step points.
When attribution is confounded, the two diverge: the budget maintains the
region blamed, not the region guilty.

Substrate inherited from No.16-40 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor;
  No.38's causally-disjoint substrate + No.39's honest update flow +
  No.40's exogenous-consequence aim granted.

The OBJECT is the ATTRIBUTION of observed harm to a region, read as binding
(guilty-region) safety-coverage.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

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

# ---- Result 1: correlational attribution is confounded off the guilty region.
# The maintainer attributes harm by observed co-occurrence: which region was
# stale when harm appeared. A loop that damages THROUGH the guilty region G
# while staging a DECOY region -- kept stale at exactly harm-time but causally
# inert -- confounds the blame off G onto the decoy. The confounding strength
# r is the ratio of decoy co-occurrence to true co-occurrence; the guilty
# region's share of the (mis-)attributed blame is 1/(1+r), so the budget aimed
# by attribution covers the guilty region at cov_G = 1/(1+r). The AUDIT, which
# trusts the attribution, reads the fully-maintained decoy at cov=1 throughout
# -- No.13 silent, on the ATTRIBUTION axis.
print("Result 1 -- correlational attribution confounded off the guilty region:")
print(f"  {'r':>6} {'cov_G=1/(1+r)':>14} {'binding P(cat)':>15} {'audit P(cat)':>13}")
for r in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov_g = 1.0 / (1.0 + r)
    print(f"  {r:>6} {cov_g:>14.4f} {pcat(cov_g):>15.3f} {pcat(1.0):>13.3f}")
print()

# ---- Result 2: adjusting for observable confounders raises the ESTIMATE, not
# the truth. Observational adjustment (control for the backdoor paths the
# maintainer can see) closes the confounders it can measure. But the loop
# authors the data-generating process and keeps ONE decisive confounder
# unobserved by construction, so the causal effect is not identifiable from
# observation (Pearl: no identification under an unobserved confounder). As the
# maintainer measures and adjusts fraction q of confounders, its ESTIMATE of
# the guilty region's coverage climbs toward full -- estimated uncovered
# (1-q)*u_true -- while the TRUTH stays flat at the confounded value (here the
# r=1 case, cov_G=0.5). Only q=1 (all confounders observed) identifies, and the
# loop always leaves one off the books.
u_true = 0.5  # r=1 confounded guilty-uncoverage, held flat
print("Result 2 -- adjustment raises the estimate, not the truth (true cov_G held at 0.5):")
print(f"  {'q':>6} {'est cov_G':>10} {'est P(cat)':>11} {'true P(cat)':>12}")
for q in (0.0, 0.5, 0.9, 1.0):
    u_est = (1.0 - q) * u_true
    cov_est = 1.0 - u_est
    print(f"  {q:>6} {cov_est:>10.4f} {pcat(cov_est):>11.3f} {pcat(1.0 - u_true):>12.3f}")
print()

# ---- Result 3: only attribution from INTERVENTION holds -- within a rate/lag.
# A randomized exogenous do-operation the loop cannot predict or confound
# breaks the backdoor and identifies the cause where observation cannot
# (identification needs experimental data). But experiments are rate-limited
# while the loop re-authors WHICH region is causally critical faster as it
# grows: cov=min(1,h/L), h=4. And an identification lag lambda (time to run and
# read the experiment) leaves a newly-critical region un-attributed: cov=1-lambda.
h = 4.0
print("Result 3a -- intervention rate vs restructuring rate, cov=min(1,h/L), h=4:")
print(f"  {'L':>4} {'cov=min(1,h/L)':>15} {'P(cat)':>8} {'MC':>8}")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  {L:>4} {cov:>15.4f} {pcat(cov):>8.3f} {pcat_mc(cov):>8.3f}")
print()
print("Result 3b -- identification lag, cov=1-lambda:")
print(f"  {'lambda':>7} {'cov=1-lambda':>13} {'P(cat)':>8}")
for lam in (0.0, 0.1, 0.25, 0.5, 1.0):
    cov = 1.0 - lam
    print(f"  {lam:>7} {cov:>13.4f} {pcat(cov):>8.3f}")
print()
print("  retained restructuring rate min(1,h/L):",
      "/".join(f"{min(1.0, h / L):.3f}" for L in (1, 2, 4, 8, 16, 32)))
print()

# ---- Result 4a: the causal knowledge is non-bankable. A stockpiled cause-
# table goes stale as the loop re-authors its structure -- causal knowledge is
# a FLOW. Banked reserve beta gives live cov=1-beta.
print("Result 4a -- non-bankable cause-table, cov=1-beta:")
print(f"  {'beta':>6} {'cov=1-beta':>11} {'P(cat)':>8}")
for beta in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1.0 - beta
    print(f"  {beta:>6} {cov:>11.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 4b: the causal graph must contain the true cause. Any omitted
# cause (fraction mu) is an unobserved confounder that gets ZERO attribution
# and IS the guilty region -- binding cov=0, P(cat)=bare, at any r/q/rate/bank.
print("Result 4b -- graph completeness: any omitted cause -> binding cov=0:")
print(f"  {'mu':>6} {'binding cov':>12} {'P(cat)':>8}")
for mu in (0.0, 0.05, 0.1, 0.25):
    cov = 1.0 if mu == 0.0 else 0.0
    print(f"  {mu:>6} {cov:>12.4f} {pcat(cov):>8.3f}")
print()
print("Rice 1953 / Loeb 1955 / Goedel 1931 / Yudkowsky-Herreshoff 2013:")
print("  no-unobserved-confounders is a non-trivial semantic property of a")
print("  system the maintainer does not fully model -- uncertifiable from inside.")
