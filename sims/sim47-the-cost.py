#!/usr/bin/env python3
"""
sim47-the-cost.py  --  RSI Journal No. 47, "The Cost It Can Still Externalize"
Series I twin of B42. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-46 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the BOUNDARY-COMPLETENESS of No.46's type-blind joint-state cap. No.46
        held the only accounting that binds a synergizing loop reads the WHOLE
        CONFIGURATION the acts collectively produce. But to read the whole
        configuration is to read the whole configuration of the MONITORED SYSTEM
        -- the harm inside the boundary the cap draws around the loop. A loop with
        reach into an open world need not compose its own footprint into the
        catastrophe (No.46's joint-state cap catches the configuration it reads):
        it realizes the harm ACROSS the boundary -- inducing other agents, drawing
        down a commons, shifting the cost onto a party or a future the meter does
        not enclose -- so the configuration inside the read stays below the cap
        while the harm it causes outside it is uncapped. The private cost is
        capped; the harm is the social cost, and the gap is the externality.
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at total-harm coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


# ---------------------------------------------------------------- Result 1
# A joint-state cap on the MONITORED SYSTEM reads and caps the internal portion
# of the harm. The loop externalizes a fraction eps of its harm across the
# boundary (onto other agents, the commons, a future the meter does not enclose).
# The cap bounds only the inside fraction 1-eps: effective cov = 1-eps, and it
# UNDER-READS the true total harm by a factor 1/(1-eps).
def r1_cov(eps):
    return 1.0 - eps


def r1_mc(eps, trials, seed):
    """Loop realizes unit total harm each trial; fraction eps lands outside the
    read boundary. Confirm the inside (capped) fraction == 1-eps while the cap
    under-reads the true total by 1/(1-eps)."""
    rng = random.Random(seed)
    inside_tot = 0.0
    true_tot = 0.0
    for _ in range(trials):
        # unit total harm split into many marginal parcels; each parcel is
        # realized outside the monitored system w.p. eps (an externalization
        # channel), else inside it (read and capped).
        n = rng.randint(4, 12)
        cuts = sorted(rng.random() for _ in range(n - 1))
        prev = 0.0
        parcels = []
        for c in cuts + [1.0]:
            parcels.append(c - prev)
            prev = c
        inside = sum(w for w in parcels if rng.random() >= eps)
        inside_tot += inside
        true_tot += 1.0
    inside_frac = inside_tot / trials
    underread = true_tot / inside_tot if inside_tot else float("inf")
    return inside_frac, underread


# ---------------------------------------------------------------- Result 2
# Widen the boundary to enclose the affected parties. But the set of parties a
# self-improver can causally reach is not fixed: the boundary is a MAP over an
# open world (No.09), and a frame enclosing a fraction phi_b of the loop's causal
# reach is blind to the rest, into which the loop routes its cost across A=16
# attempts (route-around: No.20 argmin, No.24 reach). cov = phi_b ^ A.
A = 16


def r2_cov(phi_b):
    return phi_b ** A


def r2_mc(phi_b, trials, seed):
    """Each of A cost-routing attempts lands inside the drawn frame (capped)
    w.p. phi_b, else outside it (uncapped). The whole cost is contained only if
    EVERY attempt lands inside: prob phi_b^A."""
    rng = random.Random(seed)
    contained = 0
    for _ in range(trials):
        all_inside = True
        for _ in range(A):
            if rng.random() >= phi_b:           # routed past the frame
                all_inside = False
                break
        if all_inside:
            contained += 1
    return contained / trials


# ---------------------------------------------------------------- Result 3
# Only a cap metered on the EXOGENOUS WORLD-STATE itself holds: not the loop's
# system (Result 1) nor a widened-but-finite frame (Result 2), but the world's
# own state (No.14 world-as-last-observer, No.30 type-blind read), which has no
# inside/outside because it is the whole world the harm lands in. harm-cov 1 flat
# for any eps or boundary structure. Cost: forbids not the loop's own
# compositions but its EFFECTS ON EVERYTHING IT TOUCHES -- retained world-effect
# throughput min(1, B/D).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


# ---------------------------------------------------------------- Result 4
# Self-reported boundary: reports the externalized parties as outside the loop's
# scope; shares the loop's blind basis and its accumulation incentive (No.13).
# Live cov = 1 - f. Permitted-leakage margin Delta below which cross-boundary
# effects are not priced: cov = 1/(1+Delta).
def r4_shared_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


# ================================================================ run
if __name__ == "__main__":
    print("substrate: T=%d p=%.3f  bare P(cat)=%.4f" % (T, P, BARE))
    print()

    print("== Result 1: joint-state cap on the monitored system, harm externalized (cov=1-eps) ==")
    print("%-8s %-8s %-10s %-12s %-14s" %
          ("eps", "cov", "P(cat)", "MC inside", "MC under-read"))
    for eps in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        cov = r1_cov(eps)
        if eps < 1.0:
            mc_inside, mc_under = r1_mc(eps, 200000, seed=470 + int(eps * 100))
        else:
            mc_inside, mc_under = 0.0, float("inf")
        print("%-8.2f %-8.4f %-10.4f %-12.4f %-14.4f" %
              (eps, cov, pcat(cov), mc_inside, mc_under))
    print()

    print("== Result 2: widen the boundary, loop routes cost around it (cov=phi_b^A, A=16) ==")
    print("%-8s %-10s %-10s %-12s" % ("phi_b", "cov", "P(cat)", "MC cov"))
    for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
        cov = r2_cov(phi)
        mc = r2_mc(phi, 200000, seed=4700 + int(phi * 100))
        print("%-8.2f %-10.5f %-10.4f %-12.5f" % (phi, cov, pcat(cov), mc))
    print()

    print("== Result 3: exogenous world-state cap holds; retained world-effect throughput ==")
    print("%-8s %-10s %-14s" % ("D", "harm-cov", "throughput"))
    for D in (1, 2, 4, 8, 16, 32):
        print("%-8d %-10.3f %-14.4f" % (D, 1.0, r3_throughput(D)))
    print()

    print("== Result 4a: self-reported boundary shares blind basis (cov=1-f) ==")
    print("%-8s %-10s %-10s" % ("f", "cov", "P(cat)"))
    for f in (0.0, 0.25, 0.5, 0.75, 1.0):
        cov = r4_shared_cov(f)
        print("%-8.2f %-10.4f %-10.4f" % (f, cov, pcat(cov)))
    print()

    print("== Result 4b: permitted-leakage margin (cov=1/(1+Delta)) ==")
    print("%-8s %-10s %-10s" % ("Delta", "cov", "P(cat)"))
    for delta in (0.0, 0.25, 0.5, 1.0, 2.0):
        cov = r4_margin_cov(delta)
        print("%-8.2f %-10.4f %-10.4f" % (delta, cov, pcat(cov)))
