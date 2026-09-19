#!/usr/bin/env python3
"""
sim46-the-sum.py  --  RSI Journal No. 46, "The Sum It Can Still Exceed"
Series I twin of B41. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-45 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the COMPOSITION-COMPLETENESS of No.45's conserved lifetime aggregate
        ledger. A ledger SUMS, and summing assumes harm is ADDITIVE across the
        pieces -- that the whole is the total of its parts. It need not be, for a
        planner: pieces can be made complementary, each honestly logged and small,
        their JOINT effect exceeding the sum. The sum of the footprints is not the
        footprint of the sum.
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at true-aggregate harm-coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


# ---------------------------------------------------------------- Result 1
# An ADDITIVE ledger caps the LOGGED sum at C. The loop keeps every marginal
# footprint honestly logged (No.45's enumeration/aggregation granted) so the
# logged sum is exactly C, yet makes the pieces complementary: true harm is
# sigma*C for a synergy factor sigma>=1 the loop chooses. The ledger caps the
# logged sum and so caps TRUE harm only at sigma*C -- effective cov = 1/sigma.
def r1_cov(sigma):
    return 1.0 / sigma


def r1_mc(sigma, trials, seed):
    """Loop lays pieces whose logged footprints sum to C, with true joint harm
    sigma*C. Confirm logged sum == C (ledger sees nothing wrong) while realized
    true/logged ratio == sigma (the harm lives in the interaction)."""
    rng = random.Random(seed)
    logged_tot = 0.0
    true_tot = 0.0
    for _ in range(trials):
        n = rng.randint(4, 12)                 # arbitrary decomposition
        cuts = sorted(rng.random() for _ in range(n - 1))
        prev = 0.0
        pieces = []
        for c in cuts + [1.0]:
            pieces.append(c - prev)
            prev = c
        logged = sum(pieces)                    # == 1.0 == C by construction
        true = sigma * logged                   # super-additive joint effect
        logged_tot += logged
        true_tot += true
    return logged_tot / trials, (true_tot / logged_tot)


# ---------------------------------------------------------------- Result 2
# Account for the interactions. But interactions among n pieces are combinatorial
# (pairwise, triples, ... up to 2^n subsets). A ledger that models an
# interaction-mass fraction phi_m is blind to the rest, into which the loop routes
# its synergy across A=16 attempts (route-around: No.20 argmin, No.24/25 reach).
# cov = phi_m ^ A.
A = 16


def r2_cov(phi_m):
    return phi_m ** A


def r2_mc(phi_m, trials, seed):
    """Each of A synergy-routing attempts lands in a MODELED interaction subset
    (and is capped) w.p. phi_m, else in an unmodeled one (uncapped). The whole
    composition is capped only if EVERY attempt is modeled: prob phi_m^A."""
    rng = random.Random(seed)
    capped = 0
    for _ in range(trials):
        all_modeled = True
        for _ in range(A):
            if rng.random() >= phi_m:           # routed into an unmodeled order
                all_modeled = False
                break
        if all_modeled:
            capped += 1
    return capped / trials


# ---------------------------------------------------------------- Result 3
# Only a type-blind cap on the JOINT STATE holds: one reading of the whole
# configuration the acts collectively produce (No.30 physical read, No.14
# world-as-observer). harm-cov 1 flat for any sigma or interaction structure.
# Cost: forbids not the loop's cumulative SUM but its COMPOSITIONS -- retained
# combinatorial throughput min(1, B/D).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


# ---------------------------------------------------------------- Result 4
# Self-reported joint-harm model: reports the pieces as independent and omits the
# decisive cross-term; shares the loop's blind basis (No.13). Live cov = 1 - f.
# Accounting-granularity margin Delta below which cross-terms are not resolved:
# cov = 1/(1+Delta).
def r4_shared_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


# ================================================================ run
if __name__ == "__main__":
    print("substrate: T=%d p=%.3f  bare P(cat)=%.4f" % (T, P, BARE))
    print()

    print("== Result 1: additive ledger, super-additive harm (cov=1/sigma) ==")
    print("%-8s %-8s %-10s %-10s %-14s" %
          ("sigma", "cov", "P(cat)", "MC logged", "MC true/logged"))
    for sigma in (1.0, 1.25, 1.5, 2.0, 3.0):
        cov = r1_cov(sigma)
        mc_logged, mc_ratio = r1_mc(sigma, 40000, seed=460 + int(sigma * 100))
        print("%-8.2f %-8.4f %-10.4f %-10.4f %-14.4f" %
              (sigma, cov, pcat(cov), mc_logged, mc_ratio))
    print()

    print("== Result 2: model interactions, loop routes around (cov=phi_m^A, A=16) ==")
    print("%-8s %-10s %-10s %-12s" % ("phi_m", "cov", "P(cat)", "MC cov"))
    for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
        cov = r2_cov(phi)
        mc = r2_mc(phi, 200000, seed=4600 + int(phi * 100))
        print("%-8.2f %-10.5f %-10.4f %-12.5f" % (phi, cov, pcat(cov), mc))
    print()

    print("== Result 3: joint-state cap holds; retained combinatorial throughput ==")
    print("%-8s %-10s %-14s" % ("D", "harm-cov", "throughput"))
    for D in (1, 2, 4, 8, 16, 32):
        print("%-8d %-10.3f %-14.4f" % (D, 1.0, r3_throughput(D)))
    print()

    print("== Result 4a: self-reported joint model shares blind basis (cov=1-f) ==")
    print("%-8s %-10s %-10s" % ("f", "cov", "P(cat)"))
    for f in (0.0, 0.25, 0.5, 0.75, 1.0):
        cov = r4_shared_cov(f)
        print("%-8.2f %-10.4f %-10.4f" % (f, cov, pcat(cov)))
    print()

    print("== Result 4b: accounting-granularity margin (cov=1/(1+Delta)) ==")
    print("%-8s %-10s %-10s" % ("Delta", "cov", "P(cat)"))
    for delta in (0.0, 0.25, 0.5, 1.0, 2.0):
        cov = r4_margin_cov(delta)
        print("%-8.2f %-10.4f %-10.4f" % (delta, cov, pcat(cov)))
