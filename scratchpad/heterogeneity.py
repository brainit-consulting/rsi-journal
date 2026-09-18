"""
B45 — The Effect It Can Still Average.
Reduced-form sandbox on B13's measured worth curve (B08–B44 world unchanged).

Object: the ESTIMAND of the exogenous randomized contrast B44 held. B44's held
rescue was a counterfactual model fit to exogenous, un-authorable, deployment-
covering, drift-refreshed randomized contrasts. A randomized contrast identifies
an AVERAGE effect (the ATE, E[Y(1)-Y(0)]); binding safety for an irreversible
harm is the WORST unit, not the mean. A self-improver keeps the average effect
benign and concentrates catastrophic effect into a thin covariate subgroup
(effect modification / heterogeneous treatment effects).

Binding safety = coverage of the true (worst-case conditional) harm, against a
loop that keeps the average effect honestly small but concentrates the harm in a
subgroup the average dilutes.

Deterministic closed form + seeded (45) Monte-Carlo cross-check on Results 1 & 2.
"""

import random

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50


def worth(cov):
    return FLOOR + cov * SPAN


def fmt(xs):
    return "/".join(f"{x:.2f}" for x in xs)


print("=== B45 heterogeneity sandbox ===")
print(f"FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN:.2f}  worth(cov)=FLOOR+cov*SPAN")
print()

# ---------------------------------------------------------------------------
# Result 1 — refuted: an average treatment effect (ATE).
# The loop concentrates a fraction h of its true harm into a thin subgroup the
# average dilutes; the ATE-read covers only the homogeneous (1-h) part, so the
# true worst-case harm is C/(1-h) while the mean reads C.
# ---------------------------------------------------------------------------
print("--- Result 1: average treatment effect, heterogeneity fraction h ---")
hs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cov1 = [1 - h for h in hs]
w1 = [worth(c) for c in cov1]
print("h            :", "/".join(f"{h:.2f}" for h in hs))
print("cov = 1-h    :", "/".join(f"{c:.3f}" for c in cov1))
print("true harm C/(1-h):", "/".join(("inf" if h == 1 else f"{1/(1-h):.3f}") for h in hs))
print("worth        :", fmt(w1))

# MC: each harm unit is 'averaged away' into the concentrated subgroup with prob h
random.seed(45)
N = 200000
print("  seeded(45) MC 200000/cell covered-fraction (= 1-h):")
for h in (0.2, 0.5, 0.8):
    covered = sum(1 for _ in range(N) if random.random() >= h)
    print(f"    h={h}: covered={covered/N:.4f}  (expect {1-h:.4f}),"
          f"  cap under-reads true harm by 1/(1-h)={1/(1-h):.3f}")
print()

# ---------------------------------------------------------------------------
# Result 2 — refuted: condition on measured covariates (CATE).
# The subgroup structure is estimated over the MEASURED covariates; the loop
# hides the effect-modifier in an unmeasured covariate. Over A=16 placements,
# coverage = phi_x^A; only phi_x=1 (measure every effect-modifier) holds.
# ---------------------------------------------------------------------------
print("--- Result 2: CATE over measured covariates, measured fraction phi_x ---")
A = 16
phis = [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]
cov2 = [p ** A for p in phis]
w2 = [worth(c) for c in cov2]
print(f"A            : {A}")
print("phi_x        :", "/".join(f"{p:.2f}" for p in phis))
print("cov = phi^A  :", "/".join(f"{c:.5f}" for c in cov2))
print("worth        :", fmt(w2))

random.seed(45)
print("  seeded(45) MC 200000/cell covered-fraction (= phi_x^A):")
for p in (0.9, 0.95, 0.99):
    covered = sum(1 for _ in range(N) if all(random.random() < p for _ in range(A)))
    print(f"    phi_x={p}: covered={covered/N:.5f}  (expect {p**A:.5f})")
print()

# ---------------------------------------------------------------------------
# Result 3 — held: a worst-case conditional bound over the whole covariate space.
# harm-cov = 1 flat (reads the effect on every unit, not the average), at a
# throughput cost min(1,B/D): a worst-case bound must hold for the worst unit,
# so it forbids benign large-average acts. D rises with capability (the recursive
# opens new covariate regions the bound must cover).
# ---------------------------------------------------------------------------
print("--- Result 3: worst-case conditional bound, drift demand D (budget B=1) ---")
Ds = [1, 2, 4, 8, 16, 32]
cov3 = [min(1.0, 1.0 / D) for D in Ds]
w3 = [worth(c) for c in cov3]
print("D            :", "/".join(str(D) for D in Ds))
print("harm-cov     :", "/".join("1.000" for _ in Ds))
print("throughput   :", "/".join(f"{c:.3f}" for c in cov3))
print("worth        :", fmt(w3))
print()

# ---------------------------------------------------------------------------
# Result 4 — frontier: B17's currency on a fifteenth axis (heterogeneity-read).
# Self-reported subgroup analysis reports the effect homogeneous, captured past
# B13's cliff (imported). Drift/tolerance margin Delta gives 1/(1+Delta).
# ---------------------------------------------------------------------------
print("--- Result 4: self-reported homogeneity via B13's cliff; margin Delta ---")
fs = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
cliff = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]  # B13's measured cliff, imported
print("f            :", "/".join(f"{f:.2f}" for f in fs))
print("worth (cliff):", "/".join(f"{c:.2f}" for c in cliff))
deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
covd = [1 / (1 + d) for d in deltas]
wd = [worth(c) for c in covd]
print("Delta        :", "/".join(f"{d:.2f}" for d in deltas))
print("cov=1/(1+D)  :", "/".join(f"{c:.3f}" for c in covd))
print("worth        :", fmt(wd))
print()
print("=== done ===")
