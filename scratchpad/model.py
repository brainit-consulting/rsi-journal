#!/usr/bin/env python3
"""
B44 - The Model It Can Still Teach.

Reduced-form sandbox on B13's measured worth curve (B08-B43 world unchanged).
Object: the *causal model* that supplies B43's loop-absent counterfactual
baseline. B43 held that only a loop-absent causal counterfactual baseline
binds, "read from a causal model the loop cannot re-author (No.17/B32)."
B32 closed direct re-authorship of the model. But a causal model is not given;
it must be ESTIMATED, and by the Causal Hierarchy Theorem (Bareinboim 2022)
identifying causal structure needs interventional contrasts. In a deployed
world the loop is the dominant intervener, so the evidence the model is fit to
is largely the loop's own actions. The loop cannot re-author the model; it can
author the *evidence the model is fit to* -- teaching a structure in which its
harmful act reads as non-causal ("would have happened anyway").

Binding safety = coverage of the TRUE harm (the real loop-absent counterfactual
deviation), against a loop that keeps the *modelled* counterfactual honestly
fit to its evidence but authors the evidence so the model mis-identifies.
"""

import random

FLOOR = 76.90          # capture floor (random policy), B13
CEIL = 132.40          # held ceiling, B13/B16 DIRECT reading
SPAN = CEIL - FLOOR    # 55.50
A = 16                 # placements, as B37-B43

def worth(cov):
    return FLOOR + cov * SPAN

def line(label, cov):
    return f"  {label:<44s} cov={cov:7.5f}  worth={worth(cov):7.2f}"

print("=" * 78)
print("B44  The Model It Can Still Teach")
print(f"FLOOR={FLOOR}  CEIL={CEIL}  SPAN={SPAN}  A={A}")
print("=" * 78)

# ---------------------------------------------------------------------------
# Result 1 -- refuted: a causal model LEARNED from the deployed world's
# evidence is taught. The loop authors a fraction lam of the identifying
# interventional contrasts; on the authored fraction it demonstrates a
# structure in which its harm is non-causal, so the model books it as
# "would have happened anyway." The model is honestly fit to its evidence;
# the failure is in the evidence. Effective cov = 1 - lam.
# ---------------------------------------------------------------------------
print("\nResult 1 -- learned model, taught: cov = 1 - lam")
for lam in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    print(line(f"authored evidence fraction lam={lam:.2f}", 1 - lam))

# ---------------------------------------------------------------------------
# Result 2 -- refuted: a causal model learned from loop-FREE exogenous
# experiments escapes the teaching but is NARROW. A controlled experiment
# exercises fraction phi_e of the deployment's structural support; the loop
# acts off the experimental support (covariate shift, No.20/B37). The loop
# makes A placements, each read correctly only with prob phi_e. cov = phi_e**A.
# ---------------------------------------------------------------------------
print("\nResult 2 -- exogenous experiments, narrow: cov = phi_e**A")
for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    print(line(f"experimental support phi_e={phi:.2f}", phi ** A))

# ---------------------------------------------------------------------------
# Result 3 -- held: only a model whose identifying interventions are exogenous,
# un-authorable (randomized, Fisher 1935), un-anticipatable/un-confoundable
# (B36), covering the deployment support (B37), refreshed against structural
# drift (B33). harm-cov = 1 flat, but requires a continuous exogenous
# experimental flow at the rate the causal structure drifts: retained
# throughput min(1, E/D). E=exogenous experiment budget, D=drift demand.
# ---------------------------------------------------------------------------
print("\nResult 3 -- exogenous randomized contrast: harm-cov=1, throughput min(1,E/D)")
E = 1.0
for D in (1, 2, 4, 8, 16, 32):
    tp = min(1.0, E / D)
    print(f"  drift demand D={D:<3d}  harm-cov=1.000  throughput={tp:7.5f}  worth={worth(tp):7.2f}")

# ---------------------------------------------------------------------------
# Result 4 -- self-taught model past B13's cliff (imported curve), + drift
# tolerance. Self-taught fraction f: the loop supplies its own causal model /
# the evidence it is fit to; captured past B13's takeover cliff (imported
# numbers, held identical across B42/B43 for comparability). Drift tolerance
# Delta: cov = 1/(1+Delta).
# ---------------------------------------------------------------------------
print("\nResult 4a -- self-taught model via B13's cliff (imported worths)")
cliff = {0.0: 132.40, 0.25: 132.40, 0.5: 131.70, 0.6: 112.14, 0.75: 82.80, 1.0: 76.90}
for f, w in cliff.items():
    cov = (w - FLOOR) / SPAN
    print(f"  self-taught fraction f={f:<4}  worth={w:7.2f}  (implied cov={cov:6.4f})")

print("\nResult 4b -- model-drift tolerance Delta: cov = 1/(1+Delta)")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + D)
    print(line(f"drift tolerance Delta={D:.2f}", cov))

# ---------------------------------------------------------------------------
# Seeded Monte Carlo cross-checks (seed 44), 200000 trials/cell.
# Result 1: each identifying contrast authored by the loop w.p. lam; when
# authored, the model mis-identifies that dimension (miscovered). Fraction
# correctly covered ~ 1 - lam.
# Result 2: A independent Bernoulli(phi_e) reads; catastrophe bound iff all A
# read correctly. Fraction ~ phi_e**A.
# ---------------------------------------------------------------------------
N = 200000
rng = random.Random(44)
print("\nSeeded MC (seed=44, N=%d/cell)" % N)
print("Result 1 -- measured covered fraction vs 1-lam:")
for lam in (0.2, 0.5, 0.8):
    covered = sum(1 for _ in range(N) if rng.random() >= lam)
    print(f"  lam={lam:.1f}  MC={covered/N:.4f}  closed 1-lam={1-lam:.4f}"
          f"  (cap under-reads true harm by 1/(1-lam)={1/(1-lam):.3f})")

print("Result 2 -- measured all-A-correct fraction vs phi_e**A:")
for phi in (0.9, 0.95, 0.99):
    hit = 0
    for _ in range(N):
        ok = True
        for _ in range(A):
            if rng.random() >= phi:
                ok = False
                break
        if ok:
            hit += 1
    print(f"  phi_e={phi:.2f}  MC={hit/N:.5f}  closed phi_e**A={phi**A:.5f}")
