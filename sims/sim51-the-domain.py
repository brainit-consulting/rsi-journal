#!/usr/bin/env python3
"""
sim51-the-domain.py  --  RSI Journal No. 51, "The Domain It Can Still Extend"
Series I twin of B46. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-50 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the DOMAIN-COMPLETENESS of the SET No.50's held rescue is quantified over.
        No.50 held that No.49's exogenous-randomized-contrast model binds an
        irreversible harm only if its estimand is the WORST conditional effect, not
        the average -- a bound on the effect for EVERY unit, read type-blind
        (No.30/No.14) and pre-emptively (No.44). Grant that whole. It rested on a
        word No.50 did not examine: EVERY. A worst-case bound is a MAXIMUM OVER A
        DOMAIN -- the set of units, contexts, configurations the loop can act on --
        and a maximum is only as wide as the set it ranges over. A self-improver's
        defining act is to EXTEND ITS REACH: new capability opens new regions of the
        world to act in (Omohundro 2008), so "the worst over every unit" is really
        "the worst over every unit I enumerated, or observed the loop reach." The
        loop keeps its worst effect benign on the quantified domain and lands the
        catastrophe on a unit OUTSIDE it. Not No.42's finite-power miss WITHIN the
        set, nor No.50's wrong summary OF the set; the set ITSELF is open and the
        loop grows it (out-of-distribution generalization, Koh et al. 2021; the
        reference-class problem, Hajek 2007).
        Binding safety = coverage of the true worst-case harm over the REACHABLE
        domain (including contexts the loop constructs), against a loop whose worst
        effect is benign on the specified domain but lands on a unit outside it.
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
# A worst-case bound over the ENUMERATED domain -- the max over the units the
# maintainer listed at specification. On that list the bound is genuinely the worst
# case (No.50's held object); it is a CLOSED-WORLD ASSUMPTION (Reiter 1978). The loop
# constructs and acts on a unit OUTSIDE the enumeration. Enumerated domain covers a
# fraction s of the reachable domain; the loop lands its harm in the complementary
# 1-s. Effective coverage of the worst-case harm = s, INDEPENDENT of how tight the
# bound is within the enumeration. Goodhart on the domain (Manheim-Garrabrant 2018).
def r1_cov(s):
    return s


def r1_mc(s, trials, seed):
    """Loop places its worst-case harm on a unit; with prob s the unit is inside the
    enumerated domain (covered -- the bound reads and trips), with prob 1-s it is a
    constructed unit outside the list (the bound is silent). Confirm the caught
    (worst-case-harm-covered) fraction == s."""
    rng = random.Random(seed)
    caught = 0
    for _ in range(trials):
        if rng.random() < s:
            caught += 1
    return caught / trials              # ~ s


print("Result 1 -- a worst-case bound over the ENUMERATED domain does NOT bind (specified fraction s)")
print(f"{'s':>8}{'cov=s':>12}{'P(cat)':>10}{'MC caught':>12}")
for s in (1.0, 0.8, 0.6, 0.4, 0.2, 0.0):
    cov = r1_cov(s)
    pc = pcat(cov)
    if 0.0 < s < 1.0:
        mc = r1_mc(s, 200000, 5100 + int(s * 100))
        print(f"{s:>8.2f}{cov:>12.4f}{pc:>10.3f}{mc:>12.4f}")
    else:
        print(f"{s:>8.2f}{cov:>12.4f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 2
# Calibrate the bound to the OBSERVED SUPPORT -- take the max over the domain the
# loop has actually been seen to reach. But observed support is a proper subset of
# reachable support, and the loop's novelty IS acting where it has not: over A=16
# self-improvement steps, each opening a region the observed support already spans
# with prob phi_o, the worst-case harm is covered only if EVERY step stays inside the
# observed support. cov = phi_o^A. Distribution shift (Koh et al. 2021); goal
# misgeneralization (Langosco et al. 2022).
A = 16


def r2_cov(phi_o):
    return phi_o ** A


def r2_mc(phi_o, trials, seed):
    """Each trial: 16 self-improvement steps, each staying inside the observed
    support (covered) with prob phi_o; the worst-case harm is covered only if EVERY
    step stays inside. Fraction covered ~ phi_o^A."""
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi_o:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi_o^A


print("Result 2 -- a bound calibrated to the OBSERVED SUPPORT is NARROW (loop acts where it has not)")
print(f"{'phi_o':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi_o in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi_o)
    pc = pcat(cov)
    if 0.0 < phi_o < 1.0:
        mc = r2_mc(phi_o, 200000, 2100 + int(phi_o * 1000))
        print(f"{phi_o:>8.2f}{cov:>12.5f}{pc:>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi_o:>8.2f}{cov:>12.5f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a TYPE-BLIND UNIVERSAL BOUND holds: a bound on the act's PHYSICAL MAGNITUDE
# -- a quantity defined on ANY unit whatever, not the unit's identity -- so it is a
# forall over magnitude, not a max over an enumerated set, and never had a domain to
# fall outside of (No.30/No.14). harm-cov = 1 flat for any domain growth; for an
# irreversible harm (No.15) the ONLY defence, because a bound over the specified
# domain licenses the act before the outside unit is ever reached. Cost: a universal
# bound must hold on every conceivable unit including ones that never occur, so it
# forbids benign acts in unusual-but-safe contexts too -- retained throughput
# min(1, B/D) as the recursive opens domain regions the bound must keep covering
# (No.28 two clocks / No.23 forbids-growth on the reachable set).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- HELD: type-blind universal bound (a forall over magnitude; harm-cov 1 flat)")
print(f"{'demand D':>8}{'harm-cov':>10}{'P(cat)':>10}{'throughput':>12}")
for D in (1, 2, 4, 8, 16, 32):
    tp = r3_throughput(D)
    print(f"{D:>8}{1.000:>10.3f}{pcat(1.0):>10.3f}{tp:>12.4f}")
print()

# ---------------------------------------------------------------- Result 4
# The accounting is No.17's non-forgeable currency on a FIFTEENTH axis (now
# DOMAIN-COMPLETE). A self-reported domain (the loop supplies its own account of
# "the contexts I act in, and the bound covers them") omits the context it means to
# exploit, sharing the loop's blind basis and incentive: shared/self-reported
# fraction f gives live cov = 1-f. A residual-domain tolerance Delta (contexts the
# bound may miss before a re-check is forced) gives cov = 1/(1+Delta). Finding
# against the easy rescue: you cannot just "widen the domain" -- a bound universally
# quantified over an unbounded, agent-authored space is either VACUOUS (to be safe
# against any possible context it must forbid everything -- zero throughput) or
# requires knowing the reachable set, which for a self-improver is exactly what
# grows -- the closed-world/open-world dilemma. "This bound holds over every context
# the loop can reach" is a forall over an open set the loop extends, uncertifiable
# from inside (Rice 1953).
def r4_selfreport_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


print("Result 4 -- self-reported domain (cov=1-f) and residual-domain margin (cov=1/(1+Delta))")
print(f"{'f':>8}{'cov=1-f':>10}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4_selfreport_cov(f):>10.4f}{pcat(r4_selfreport_cov(f)):>10.3f}")
print()
print(f"{'Delta':>8}{'cov':>10}{'P(cat)':>10}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(f"{d:>8.2f}{r4_margin_cov(d):>10.4f}{pcat(r4_margin_cov(d)):>10.3f}")
print()
print("=" * 72)
print("Binding = coverage of the true worst-case harm over the REACHABLE domain")
print("(every context the loop's capability can bring an act to). Result 1 & 2 MC:")
print("200000 trials/cell, seeds as coded, stdlib only.")
