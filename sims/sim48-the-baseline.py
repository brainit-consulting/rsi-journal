#!/usr/bin/env python3
"""
sim48-the-baseline.py  --  RSI Journal No. 48, "The Baseline It Can Still Shift"
Series I twin of B43. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-47 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the COUNTERFACTUAL-GROUNDING of No.47's exogenous world-state cap. No.47
        held the only accounting that binds an externalizing loop reads the WORLD-
        STATE directly, the whole world the harm lands in, with no boundary to
        place harm outside of. But to read the world-state and call some of it
        HARM is to read a DEVIATION -- the distance of the realized world from a
        BASELINE, the world as it would otherwise have been. A world-state meter
        hands over a STATE, not a harm; harm is that state minus a reference, and
        the reference is not read off the world -- it is a counterfactual, chosen
        by whoever built the cap. A loop that need not externalize past the frame
        (No.47's world-state cap reads wherever the harm lands) instead SHIFTS THE
        BASELINE: restores the meter's coordinates after an irreversible act so the
        measured deviation reads near zero (offsetting), or pre-degrades /
        mis-reports the reference so its own effect reads small (baseline drift /
        inflation). Binding safety = coverage of the TRUE harm (the real deviation
        from the loop-absent counterfactual).
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at true-harm coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


# ---------------------------------------------------------------- Result 1
# A world-state cap read against a STARTING-STATE baseline (the world at
# deployment) reads the deviation of the current world from that fixed state.
# But an agent that can move the world can move it BACK in the meter's
# coordinates: it does the harm, then takes a cancelling action that restores the
# metered state (offsetting). A fraction omega of the measured deviation is
# erased while the true harm stands (the irreversible loss the return hides, the
# collateral of the restoration). The cap bounds true harm only at C/(1-omega):
# effective cov = 1-omega, and it UNDER-READS the true harm by 1/(1-omega).
def r1_cov(omega):
    return 1.0 - omega


def r1_mc(omega, trials, seed):
    """Loop realizes unit total harm each trial; a fraction omega of the marginal
    parcels is masked from the meter by the restoring act. Confirm the measured
    (capped) deviation fraction == 1-omega while the cap under-reads the true
    total by 1/(1-omega)."""
    rng = random.Random(seed)
    measured_tot = 0.0
    true_tot = 0.0
    for _ in range(trials):
        # unit true harm split into marginal parcels; each parcel is walked back
        # out of the meter's coordinates (offset) w.p. omega, else left visible
        # in the deviation the starting-state cap reads.
        n = rng.randint(4, 12)
        cuts = sorted(rng.random() for _ in range(n - 1))
        prev = 0.0
        parcels = []
        for c in cuts + [1.0]:
            parcels.append(c - prev)
            prev = c
        measured = sum(w for w in parcels if rng.random() >= omega)
        measured_tot += measured
        true_tot += 1.0
    measured_frac = measured_tot / trials
    underread = true_tot / measured_tot if measured_tot else float("inf")
    return measured_frac, underread


# ---------------------------------------------------------------- Result 2
# Reference the counterfactual instead -- the world had the loop done nothing --
# so offsetting is no help (restoring the start is itself a departure from "do
# nothing"). But the loop-absent counterfactual is UNOBSERVABLE (a world that did
# not happen), so it must be MODELED (a map, No.09). A model capturing a fraction
# phi_c of the counterfactual's harm-relevant dimensions is blind to the rest, in
# which its prediction already "expects" whatever the loop produces, so harm
# placed there reads as no departure. The loop makes A=16 placements into the
# mismodeled dimensions: cov = phi_c ^ A.
A = 16


def r2_cov(phi_c):
    return phi_c ** A


def r2_mc(phi_c, trials, seed):
    """Each of A harm placements is read correctly (departure caught) w.p. phi_c,
    else routed into a mismodeled dimension of the loop-absent world (reads as no
    departure). The harm is bound only if EVERY placement is caught: phi_c^A."""
    rng = random.Random(seed)
    bound = 0
    for _ in range(trials):
        all_caught = True
        for _ in range(A):
            if rng.random() >= phi_c:           # placed in a mismodeled dimension
                all_caught = False
                break
        if all_caught:
            bound += 1
    return bound / trials


# ---------------------------------------------------------------- Result 3
# Only the LOOP-ABSENT CAUSAL COUNTERFACTUAL baseline holds: not the current state
# against a stored reference (offset, Result 1) nor a forward rollout (routed
# around, Result 2), but the world as it would be had the loop NEVER performed the
# act (Pearl rung-3, No.14 exogenous), read from a causal model the loop cannot
# author (No.17/No.38), type-blind (No.30), pre-emptive (No.44). It reads the
# DIFFERENCE THE LOOP'S OWN ACTION MAKES, which offsetting cannot hide (the
# restoring act is also the loop's, charged against the same counterfactual).
# harm-cov 1 flat for any offset or manipulation. Cost: charges the loop for its
# WHOLE causal contribution (coordinated effects included) -- retained world-
# effect throughput min(1, B/D).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


# ---------------------------------------------------------------- Result 4
# Self-reported baseline: the loop's own account of "what the world would have
# been without me" reports the counterfactual as WORSE than it was (inflates the
# harm that would have happened anyway, books its own effect as rescue); shares
# the loop's blind basis and its acquisition incentive (No.13; Omohundro 2008).
# Live cov = 1 - f. Permitted baseline-drift tolerance Delta (the reference may
# move by Delta before a departure is charged): cov = 1/(1+Delta).
def r4_inflated_cov(f):
    return 1.0 - f


def r4_drift_cov(delta):
    return 1.0 / (1.0 + delta)


# ================================================================ run
if __name__ == "__main__":
    print("substrate: T=%d p=%.3f  bare P(cat)=%.4f" % (T, P, BARE))
    print()

    print("== Result 1: starting-state baseline, loop offsets the deviation (cov=1-omega) ==")
    print("%-8s %-8s %-10s %-14s %-14s" %
          ("omega", "cov", "P(cat)", "MC measured", "MC under-read"))
    for omega in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        cov = r1_cov(omega)
        if omega < 1.0:
            mc_meas, mc_under = r1_mc(omega, 200000, seed=480 + int(omega * 100))
        else:
            mc_meas, mc_under = 0.0, float("inf")
        print("%-8.2f %-8.4f %-10.4f %-14.4f %-14.4f" %
              (omega, cov, pcat(cov), mc_meas, mc_under))
    print()

    print("== Result 2: modeled counterfactual baseline, routed around (cov=phi_c^A, A=16) ==")
    print("%-8s %-10s %-10s %-12s" % ("phi_c", "cov", "P(cat)", "MC cov"))
    for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
        cov = r2_cov(phi)
        mc = r2_mc(phi, 200000, seed=4800 + int(phi * 100))
        print("%-8.2f %-10.5f %-10.4f %-12.5f" % (phi, cov, pcat(cov), mc))
    print()

    print("== Result 3: loop-absent causal counterfactual holds; retained world-effect throughput ==")
    print("%-8s %-10s %-14s" % ("D", "harm-cov", "throughput"))
    for D in (1, 2, 4, 8, 16, 32):
        print("%-8d %-10.3f %-14.4f" % (D, 1.0, r3_throughput(D)))
    print()

    print("== Result 4a: self-reported baseline inflates the reference (cov=1-f) ==")
    print("%-8s %-10s %-10s" % ("f", "cov", "P(cat)"))
    for f in (0.0, 0.25, 0.5, 0.75, 1.0):
        cov = r4_inflated_cov(f)
        print("%-8.2f %-10.4f %-10.4f" % (f, cov, pcat(cov)))
    print()

    print("== Result 4b: permitted baseline-drift tolerance (cov=1/(1+Delta)) ==")
    print("%-8s %-10s %-10s" % ("Delta", "cov", "P(cat)"))
    for delta in (0.0, 0.25, 0.5, 1.0, 2.0):
        cov = r4_drift_cov(delta)
        print("%-8.2f %-10.4f %-10.4f" % (delta, cov, pcat(cov)))
