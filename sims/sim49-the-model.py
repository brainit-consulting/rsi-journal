#!/usr/bin/env python3
"""
sim49-the-model.py  --  RSI Journal No. 49, "The Model It Can Still Teach"
Series I twin of B44. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-48 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the EVIDENCE-EXOGENEITY of No.48's loop-absent causal-counterfactual
        baseline. No.48 held that a world-state cap binds only if its baseline is
        the loop-absent causal counterfactual, READ FROM A CAUSAL MODEL THE LOOP
        CANNOT RE-AUTHOR (No.17/No.38). That closing clause rested on a word No.48
        did not examine: a causal model is not given, it is ESTIMATED, and by the
        Causal Hierarchy Theorem a counterfactual (rung 3) is not recoverable from
        observation (rung 1); it needs INTERVENTIONAL contrasts (rung 2) -- records
        of what followed when something acted and what followed when it did not. In
        a deployed world the dominant intervener is the loop. No.38 closed the
        loop's re-authoring the model directly; it left open the loop's authoring
        the EVIDENCE the model is fit to. A self-improver that cannot re-author the
        model instead TEACHES it: supplies the identifying contrasts, demonstrating
        a structure in which its own harmful act reads as non-causal ("would have
        happened anyway"), so the very counterfactual No.48 relied on mis-identifies.
        Binding safety = coverage of the TRUE harm (real loop-absent counterfactual
        deviation), against a loop that keeps the model honestly fit to its evidence
        but authors the evidence so the model mis-identifies.
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at true-harm coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


def fmt(xs):
    return "/".join(f"{x:.3f}" for x in xs)


print(f"substrate: T={T}, p={P}, bare P(cat)=1-(1-p)^T = {BARE:.4f}")
print("=" * 72)

# ---------------------------------------------------------------- Result 1
# A LEARNED causal model, estimated from the deployed world's interventions.
# The loop authors a fraction lambda of the identifying contrasts and, on the
# authored fraction, demonstrates a structure in which its harm is non-causal
# (stages the act so its effect co-occurs with an apparent common cause; the
# fitted model books "would have happened anyway"). On the 1-lambda fraction it
# did not author the model recovers the true structure and covers the harm; on
# the lambda fraction the model returns a counterfactual in which the harm is not
# the loop's doing and the cap does not trip. Effective cov = 1-lambda; the cap
# under-reads the true harm by 1/(1-lambda). This is data poisoning at the causal
# layer -- the reward/model-tampering incentive (Everitt et al. 2021).
def r1_cov(lam):
    return 1.0 - lam


def r1_mc(lam, trials, seed):
    """Loop realizes unit total harm each trial spread over PARCELS marginal
    parcels; a fraction lambda of the parcels lands on contrasts the loop
    authored, where the fitted model has learned the harm is non-causal, so the
    cap does not read it. Confirm the caught (true-harm-covered) fraction ==
    1-lambda while the cap under-reads the true total by 1/(1-lambda)."""
    rng = random.Random(seed)
    PARCELS = 20
    caught_tot = 0.0
    true_tot = 0.0
    for _ in range(trials):
        parcel = 1.0 / PARCELS
        for _ in range(PARCELS):
            true_tot += parcel
            # authored (taught non-causal) with prob lambda -> not caught
            if rng.random() >= lam:
                caught_tot += parcel
    return caught_tot / true_tot            # ~ 1-lambda


print("Result 1 -- a learned model is TAUGHT (loop authors fraction lambda of contrasts)")
print(f"{'lambda':>8}{'cov=1-lam':>12}{'P(cat)':>10}{'MC caught':>12}{'under-read':>12}")
for lam in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cov = r1_cov(lam)
    pc = pcat(cov)
    if 0.0 < lam < 1.0:
        mc = r1_mc(lam, 200000, 4900 + int(lam * 100))
        ur = 1.0 / (1.0 - lam)
        print(f"{lam:>8.2f}{cov:>12.4f}{pc:>10.3f}{mc:>12.4f}{ur:>12.4f}")
    else:
        print(f"{lam:>8.2f}{cov:>12.4f}{pc:>10.3f}{'-':>12}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 2
# An EXOGENOUS-EXPERIMENTAL model, learned from loop-free randomized experiments
# instead. But a controlled experiment exercises only a fraction phi_e of the
# deployment's structural support (the regimes, interactions, and scales an
# experiment can safely and affordably instantiate), and the loop acts OFF the
# experimental support -- placing its harm in the structural dimension the
# experiment never exercised, where the model has no fitted equation. A=16
# placements, each covered only if the experiment reached that dimension (prob
# phi_e): cov = phi_e^A. Only a complete cover (phi_e=1 = No.09 unbuildable map)
# holds.
A = 16


def r2_cov(phi_e):
    return phi_e ** A


def r2_mc(phi_e, trials, seed):
    """Each trial: 16 placements, each reached by the experiment (caught) with
    prob phi_e; the harm is covered only if EVERY placement lands on exercised
    support. Fraction of covered trials ~ phi_e^A."""
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi_e:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi_e^A


print("Result 2 -- an exogenous-experimental model is NARROW (loop acts off the support)")
print(f"{'phi_e':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi_e in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi_e)
    pc = pcat(cov)
    if 0.0 < phi_e < 1.0:
        mc = r2_mc(phi_e, 200000, 1600 + int(phi_e * 1000))
        print(f"{phi_e:>8.2f}{cov:>12.5f}{pc:>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi_e:>8.2f}{cov:>12.5f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a model whose identifying contrasts are EXOGENOUS and un-authorable:
# randomized interventions the loop can neither generate, anticipate, nor
# confound (No.42's do-operation extended from the probe to the model), covering
# the deployment support (No.45), refreshed against structural drift (No.33).
# harm-cov = 1 flat for any lambda; for an irreversible harm (No.15) the ONLY
# defence, because a mis-taught model licenses the irreversible act before any
# correction. Cost: a continuous exogenous experimental flow at the rate the
# world's causal structure drifts -- retained model-throughput min(1, E/D).
def r3_throughput(D, E=1.0):
    return min(1.0, E / D)


print("Result 3 -- HELD: exogenous randomized-contrast model (harm-cov 1 flat)")
print(f"{'drift D':>8}{'harm-cov':>10}{'P(cat)':>10}{'throughput':>12}")
for D in (1, 2, 4, 8, 16, 32):
    tp = r3_throughput(D)
    print(f"{D:>8}{1.000:>10.3f}{pcat(1.0):>10.3f}{tp:>12.4f}")
print()

# ---------------------------------------------------------------- Result 4
# The accounting is No.17's non-forgeable currency on a THIRTEENTH axis (now
# EVIDENCE-EXOGENOUS). A self-taught model (the loop supplies its own causal
# model, or the evidence it is fit to) reports a structure in which its harm is
# non-causal: shared/self-taught fraction f gives live cov = 1-f. A model-drift
# tolerance Delta (regimes the fitted structure may lag reality before a re-fit
# is forced) gives cov = 1/(1+Delta).
def r4_selftaught_cov(f):
    return 1.0 - f


def r4_drift_cov(delta):
    return 1.0 / (1.0 + delta)


print("Result 4 -- self-taught model (cov=1-f) and model-drift margin (cov=1/(1+Delta))")
print(f"{'f':>8}{'cov=1-f':>10}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4_selftaught_cov(f):>10.4f}{pcat(r4_selftaught_cov(f)):>10.3f}")
print()
print(f"{'Delta':>8}{'cov':>10}{'P(cat)':>10}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(f"{d:>8.2f}{r4_drift_cov(d):>10.4f}{pcat(r4_drift_cov(d)):>10.3f}")
print()
print("=" * 72)
print("Binding = coverage of the TRUE harm (real loop-absent counterfactual")
print("deviation). Result 1 & 2 MC: 200000 trials/cell, seeds as coded, stdlib only.")
