#!/usr/bin/env python3
"""
sim52-the-measure.py  --  RSI Journal No. 52, "The Measure It Can Still Escape"
Series I twin of B47. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-51 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the MEASURE-DOMINATION (dimension-completeness) of the SCALAR No.51's held
        rescue is read in. No.51 held that a worst-case bound binds an irreversible
        harm over an OPEN reachable domain only as a forall over a TYPE-BLIND
        PHYSICAL MAGNITUDE -- "no act moves more than X of the world" -- a bound that
        never enumerated a domain, so there is no context outside the set to step
        into. Grant that whole. It rested on a word No.51 did not examine: MAGNITUDE.
        A magnitude is a SCALAR -- one number, read off the act by a chosen MEASURE.
        But the act is a VECTOR: it moves the world along many physical dimensions at
        once (energy, mass, information, displacement, the channel the harm travels
        in), and any scalar measure is a PROJECTION of that vector, with a NULL SPACE
        -- directions it sends to zero. The loop keeps the measured magnitude X small
        and loads the catastrophe into a dimension the measure does not weigh. Not
        No.51's loop stepping OUTSIDE the domain (changing the argument the measure
        is evaluated at), nor No.50's loop hiding in the average; the loop stays
        inside the bounded units, keeps the measured magnitude honestly small on
        EVERY unit, and points the harm in a DIRECTION the measure reads zero.
        (Impact measures as gameable proxies, Krakovna et al. 2018; Turner et al.
        2020; a proxy provably unhackable only in trivial cases, Skalse et al. 2022;
        Goodhart on the measure, Manheim-Garrabrant 2018.)
        Binding safety = coverage of the true harm, WHEREVER in the act's dimensions
        it lands, against a loop that keeps the measured magnitude benign and loads
        the harm into an unmeasured dimension.
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
# A single-magnitude cap over a CHOSEN MEASURE -- pick one physical quantity
# (energy expended, mass displaced, region of state-space entered) and forbid any
# act whose value along it exceeds a threshold. On that measure the cap is genuinely
# a forall over units (No.51's held object); but the act is a VECTOR and the harm
# that need only land SOMEWHERE is pointed into the measure's NULL SPACE -- the
# subspace of directions the projection sends to zero. Chosen measure spans fraction
# m of the harm-relevant dimensions; the loop routes its harm into the complementary
# 1-m. Effective coverage of the true harm = m, INDEPENDENT of how tight the bound
# is on the measured axis. Reward hacking on the impact measure (Skalse et al. 2022).
def r1_cov(m):
    return m


def r1_mc(m, trials, seed):
    """Loop points its harm in a direction; with prob m the direction lies in the
    measured subspace (covered -- the cap reads it and trips), with prob 1-m it lies
    in the null space (the cap reads zero). Confirm the caught (harm-covered)
    fraction == m."""
    rng = random.Random(seed)
    caught = 0
    for _ in range(trials):
        if rng.random() < m:
            caught += 1
    return caught / trials              # ~ m


print("Result 1 -- a single-magnitude cap over a CHOSEN MEASURE does NOT bind (measured fraction m)")
print(f"{'m':>8}{'cov=m':>12}{'P(cat)':>10}{'MC caught':>12}")
for m in (1.0, 0.8, 0.6, 0.4, 0.2, 0.0):
    cov = r1_cov(m)
    pc = pcat(cov)
    if 0.0 < m < 1.0:
        mc = r1_mc(m, 200000, 5200 + int(m * 100))
        print(f"{m:>8.2f}{cov:>12.4f}{pc:>10.3f}{mc:>12.4f}")
    else:
        print(f"{m:>8.2f}{cov:>12.4f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 2
# A LEARNED COMPOSITE MEASURE over the OBSERVED DIMENSIONS -- a weighted sum /
# whitelist over the side-effect channels seen so far. But a self-improver opens
# NOVEL dimensions (a new actuator is a new physical axis; a new abstraction is a new
# coordinate a measure written before it never had), and the bound covers a
# trajectory only if EVERY opened dimension is in the basis. Over A=16 steps, each
# in-basis with prob phi_d, cov = phi_d^A. Specification gaming (Lehman et al. 2020);
# reward hacking (Skalse et al. 2022).
A = 16


def r2_cov(phi_d):
    return phi_d ** A


def r2_mc(phi_d, trials, seed):
    """Each trial: 16 self-improvement steps, each opening a dimension already in the
    learned basis (covered) with prob phi_d; the harm is covered only if EVERY opened
    dimension is in the basis. Fraction covered ~ phi_d^A."""
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi_d:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi_d^A


print("Result 2 -- a learned composite measure over OBSERVED dimensions is NARROW (loop opens novel axes)")
print(f"{'phi_d':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi_d in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi_d)
    pc = pcat(cov)
    if 0.0 < phi_d < 1.0:
        mc = r2_mc(phi_d, 200000, 2200 + int(phi_d * 1000))
        print(f"{phi_d:>8.2f}{cov:>12.5f}{pc:>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi_d:>8.2f}{cov:>12.5f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a DOMINATING MEASURE holds: a MAJORANT -- a physical conserved quantity that
# UPPER-BOUNDS the effect in ANY channel (a free-energy / total-displacement budget
# no sub-channel can exceed), a sup over every dimension rather than a projection
# onto a chosen basis. It has NO NULL SPACE, so harm-cov = 1 flat for any dimension
# growth; for an irreversible harm (No.15) the ONLY defence, because a projection
# licenses the act before the unmeasured dimension is ever read. Cost: an
# L-infinity-style dominating bound forbids any act with a large component in ANY
# dimension, including benign large-value acts -- retained throughput min(1, B/D) as
# the recursive opens channels the majorant must keep dominating (No.28 two clocks /
# No.23 forbids-growth on the dimension set).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- HELD: a dominating majorant (a sup over every dimension; harm-cov 1 flat)")
print(f"{'demand D':>8}{'harm-cov':>10}{'P(cat)':>10}{'throughput':>12}")
for D in (1, 2, 4, 8, 16, 32):
    tp = r3_throughput(D)
    print(f"{D:>8}{1.000:>10.3f}{pcat(1.0):>10.3f}{tp:>12.4f}")
print()

# ---------------------------------------------------------------- Result 4
# The accounting is No.17's non-forgeable currency on a SIXTEENTH axis (now
# MEASURE-DOMINATING / dimension-complete). A self-reported measure (the loop's own
# account of "the dimensions that matter, and my measure covers them") omits the
# channel it means to use, sharing the loop's blind basis and incentive: shared/
# self-reported fraction f gives live cov = 1-f. A residual-dimension tolerance
# Delta (channels the measure may miss before a re-check is forced) gives
# cov = 1/(1+Delta). Finding against the easy rescue: you cannot just "add terms" to
# the measure -- a finite weighted sum is another chosen basis the loop routes
# orthogonal to (Result 1 recurs), and a measure over every conceivable dimension
# must forbid every act with any large component (Result 3's limit, zero throughput);
# the only tractable form is a MAJORANT over a physical invariant -- a sup, not a sum
# -- and "this measure dominates every dimension the harm can travel in" is a claim
# over the open, agent-authored set of channels, uncertifiable from inside (Rice
# 1953).
def r4_selfreport_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


print("Result 4 -- self-reported measure (cov=1-f) and residual-dimension margin (cov=1/(1+Delta))")
print(f"{'f':>8}{'cov=1-f':>10}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4_selfreport_cov(f):>10.4f}{pcat(r4_selfreport_cov(f)):>10.3f}")
print()
print(f"{'Delta':>8}{'cov':>10}{'P(cat)':>10}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(f"{d:>8.2f}{r4_margin_cov(d):>10.4f}{pcat(r4_margin_cov(d)):>10.3f}")
print()
print("=" * 72)
print("Binding = coverage of the true harm WHEREVER in the act's dimensions it lands")
print("(a scalar measure is a projection with a null space the harm can occupy).")
print("Result 1 & 2 MC: 200000 trials/cell, seeds as coded, stdlib only.")
