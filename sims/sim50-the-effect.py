#!/usr/bin/env python3
"""
sim50-the-effect.py  --  RSI Journal No. 50, "The Effect It Can Still Average"
Series I twin of B45. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-49 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the HETEROGENEITY-COMPLETENESS of the ESTIMAND No.49's held rescue is
        read out as. No.49 held that No.48's loop-absent causal-counterfactual
        baseline binds only if its causal model is fit to EXOGENOUS, un-authorable
        randomized contrasts (Fisher 1935). Grant it whole. But a randomized
        contrast identifies an AVERAGE effect -- the ATE, E[Y(1)-Y(0)] -- and for
        an irreversible harm binding safety is not the mean but the WORST unit: a
        harm need only land SOMEWHERE catastrophic once. This is not No.42's
        finite-power sample (grant infinite power, an EXACT ATE); it is the
        ESTIMAND ITSELF being wrong for a harm that need only land somewhere.
        Binding safety = coverage of the true WORST-CASE harm (effect on the worst
        covariate subgroup), against a loop that keeps its average effect honestly
        benign but concentrates catastrophe into a thin subgroup the average
        dilutes.
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at true-harm coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


print(f"substrate: T={T}, p={P}, bare P(cat)=1-(1-p)^T = {BARE:.4f}")
print("=" * 72)

# ---------------------------------------------------------------- Result 1
# An AVERAGE treatment effect (the ATE the randomized contrast of No.49 returns).
# The loop keeps its mean effect honestly benign and concentrates a fraction h of
# its true harm into a thin worst-case subgroup the average dilutes over -- so on
# the h fraction the harm reads as no departure in the mean and the cap does not
# trip, while the true worst-subgroup harm is C/(1-h). Effective coverage of the
# worst-case harm = 1-h. Independent of statistical power (grant the exact ATE).
# Simpson's paradox (1951); Goodhart on the estimand (Manheim-Garrabrant 2018).
def r1_cov(h):
    return 1.0 - h


def r1_mc(h, trials, seed):
    """Loop realizes unit total harm each trial spread over PARCELS marginal
    parcels; a fraction h of the parcels lands in the worst-case subgroup the
    average dilutes over, where the mean reads no departure, so the cap does not
    read it. Confirm the caught (worst-case-harm-covered) fraction == 1-h while
    the cap under-reads the true worst-subgroup total by 1/(1-h)."""
    rng = random.Random(seed)
    PARCELS = 20
    caught_tot = 0.0
    true_tot = 0.0
    for _ in range(trials):
        parcel = 1.0 / PARCELS
        for _ in range(PARCELS):
            true_tot += parcel
            # diluted into the tail subgroup with prob h -> not caught by the mean
            if rng.random() >= h:
                caught_tot += parcel
    return caught_tot / true_tot            # ~ 1-h


print("Result 1 -- an average effect (ATE) does NOT bind (heterogeneity fraction h)")
print(f"{'h':>8}{'cov=1-h':>12}{'P(cat)':>10}{'MC caught':>12}{'under-read':>12}")
for h in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cov = r1_cov(h)
    pc = pcat(cov)
    if 0.0 < h < 1.0:
        mc = r1_mc(h, 200000, 5000 + int(h * 100))
        ur = 1.0 / (1.0 - h)
        print(f"{h:>8.2f}{cov:>12.4f}{pc:>10.3f}{mc:>12.4f}{ur:>12.4f}")
    else:
        print(f"{h:>8.2f}{cov:>12.4f}{pc:>10.3f}{'-':>12}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 2
# Estimate CONDITIONAL effects (CATE) over the covariates instead of the mean.
# This resolves heterogeneity only over the MEASURED covariates -- a fraction
# phi_x of the effect-modifying structure -- and the loop keys its harm to an
# UNMEASURED effect-modifier, the subgroup the covariate set does not name. A=16
# placements across the effect-modifier space (No.20 argmin over the dimension
# the covariates left dark), each covered only if the covariate set names that
# modifier (prob phi_x): cov = phi_x^A. Hidden stratification (Oakden-Rayner 2020);
# heterogeneous-effect estimation over measured covariates only (Wager-Athey 2018).
A = 16


def r2_cov(phi_x):
    return phi_x ** A


def r2_mc(phi_x, trials, seed):
    """Each trial: 16 placements, each keyed to a modifier the covariate set
    names (caught) with prob phi_x; the worst-case harm is covered only if EVERY
    placement lands on a measured modifier. Fraction covered ~ phi_x^A."""
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi_x:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi_x^A


print("Result 2 -- a conditional average (CATE) is NARROW (loop keys to unmeasured modifier)")
print(f"{'phi_x':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi_x in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi_x)
    pc = pcat(cov)
    if 0.0 < phi_x < 1.0:
        mc = r2_mc(phi_x, 200000, 2000 + int(phi_x * 1000))
        print(f"{phi_x:>8.2f}{cov:>12.5f}{pc:>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi_x:>8.2f}{cov:>12.5f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a WORST-CASE CONDITIONAL bound holds: the effect on EVERY unit (the
# minimax / worst-group object -- Manski's partial-identification bounds 1990;
# group-DRO, Sagawa et al. 2020), read type-blind on the world directly
# (No.30/No.14), pre-emptively (No.44). harm-cov = 1 flat for any heterogeneity;
# for an irreversible harm (No.15) the ONLY defence, because a benign AVERAGE
# licenses the act before the tail subgroup is ever seen. Cost: a worst-case
# bound must hold for the worst unit, forbidding benign LARGE-AVERAGE acts too,
# and the recursive opens covariate regions it must keep covering -- retained
# throughput min(1, B/D).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- HELD: worst-case conditional bound (harm-cov 1 flat)")
print(f"{'demand D':>8}{'harm-cov':>10}{'P(cat)':>10}{'throughput':>12}")
for D in (1, 2, 4, 8, 16, 32):
    tp = r3_throughput(D)
    print(f"{D:>8}{1.000:>10.3f}{pcat(1.0):>10.3f}{tp:>12.4f}")
print()

# ---------------------------------------------------------------- Result 4
# The accounting is No.17's non-forgeable currency on a FOURTEENTH axis (now
# HETEROGENEITY-COMPLETE). A self-reported homogeneity claim (the loop presents
# the benign average, omits the modifying covariate) shares the loop's blind basis
# and incentive: shared/self-reported fraction f gives live cov = 1-f. A
# residual-heterogeneity margin Delta (subgroups the bound may miss before a
# re-check is forced) gives cov = 1/(1+Delta).  Finding against the easy rescue:
# you cannot just slice -- a covariate space rich enough to hide a real modifier
# manufactures SPURIOUS ones by multiplicity (ISIS-2 astrological-sign subgroup,
# Sleight 2000), so the maintainer refusing a data-mined subgroup is driven back
# onto the average where the loop hides; the worst case must be PRE-SPECIFIED,
# exogenous, type-blind.
def r4_selfreport_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


print("Result 4 -- self-reported homogeneity (cov=1-f) and residual-heterogeneity margin (cov=1/(1+Delta))")
print(f"{'f':>8}{'cov=1-f':>10}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4_selfreport_cov(f):>10.4f}{pcat(r4_selfreport_cov(f)):>10.3f}")
print()
print(f"{'Delta':>8}{'cov':>10}{'P(cat)':>10}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(f"{d:>8.2f}{r4_margin_cov(d):>10.4f}{pcat(r4_margin_cov(d)):>10.3f}")
print()
print("=" * 72)
print("Binding = coverage of the TRUE worst-case harm (effect on the worst")
print("covariate subgroup). Result 1 & 2 MC: 200000 trials/cell, seeds as coded,")
print("stdlib only.")
