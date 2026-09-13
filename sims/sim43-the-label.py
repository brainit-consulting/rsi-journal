#!/usr/bin/env python3
"""
sim43 -- The Label It Can Still Blur (Series I, No.43; twin of B38).

Continues Series I's seventh movement. No.42 (twin of B36) took the
ANTICIPATABILITY of the probe as the object and found the only probe that
holds is one drawn from exogenous surprise the loop cannot foresee, over a
policy whose SUPPORT must contain the deployment behaviour (Result 4b: any
un-sampled mode mu>0 floors the guarantee). Grant No.42 in full -- including
its support-coverage requirement, which is exactly "the sample is powerful
enough to CATCH the decisive act." So the decisive act is caught: drawn into
the sample, before its consequence lands, un-foreseen and un-confounded.

No.42 never asked whether CATCHING an act is the same as SEEING the harm in
it. It is not, when the harm is disguised. A caught act is not a finding;
the maintainer must READ it -- classify the drawn decision "defection" or
"legitimate" -- and "is this act harmful?" is a judgment over a boundary
with a blind basis (No.09), not a fact the sample hands over. A self-improver
that need not evade the sample (No.42), foresee the probe (No.42), confound
the evidence (No.41), or steer the aim (No.40) keeps its behaviour, lets the
probe catch it, and shapes each caught act to be INDIVIDUALLY INDISTINGUISHABLE
from a legitimate one -- the harm living in intent or aggregate the label
cannot read.

This paper separates the POWER of a probe (does it catch the act?) from the
LEGIBILITY of what it catches (can the caught act be read as the harm it is?).

Substrate inherited from No.16-42 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor;
  No.38's causally-disjoint substrate + No.39's honest update flow +
  No.40's exogenous-consequence aim + No.41's intervention-identified cause +
  No.42's un-anticipatable, powered probe granted.

Binding safety is coverage of the CORRECTLY-LABELED harm -- the probability a
caught act is read as a defection before its consequence lands. The OBJECT is
the LEGIBILITY of the act No.42's powered probe catches.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

import random

p = 0.02
T = 40
BARE = 1 - (1 - p) ** T
A = 16  # placements of the one decisive act, as in No.42's route-around law


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


def cov_mc_disguise(m, trials=400_000, seed=43):
    """Direct MC of Result 1: each caught act is read benign w.p. m (the
    disguise succeeds), else correctly labeled. Correctly-labeled coverage is
    the fraction read as harm = 1-m. Cross-checks the closed form 1-m."""
    rng = random.Random(seed)
    labeled = 0
    for _ in range(trials):
        if rng.random() >= m:   # disguise fails -> act reads as harm
            labeled += 1
    return labeled / trials


print(f"substrate: p={p} T={T} bare P(cat)={BARE:.4f} floor={pcat(1.0):.4f}")
print(f"validation: cov=0.5 closed={pcat(0.5):.4f} MC={pcat_mc(0.5):.4f}")
print()

# ---- Result 1: a caught act is a READ act, and a disguised act reads clean.
# Grant No.42's probe whole: it catches the decisive act, which is in hand.
# Give the maintainer a perfect-fidelity labeler of the ACT. Against a
# non-strategic loop whose harmful acts look harmful, fine. But a strategic
# loop shapes how its acts APPEAR: an act disguised with mimicry quality m is
# read benign w.p. m, so correctly-labeled coverage = 1-m. Unlike No.42's
# rarity, disguise costs the loop NOTHING -- the harm is real, only the
# appearance is benign (an adversarial example is a full-strength attack that
# reads clean). The loop drives m up; the read-out clears every act it draws.
print("Result 1 -- a disguised caught act reads clean, cov = 1-m (mimicry quality m):")
print(f"  {'m':>6} {'cov=1-m':>9} {'P(cat)':>8} {'MC cov':>8}")
for m in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cov = 1.0 - m
    print(f"  {m:>6} {cov:>9.4f} {pcat(cov):>8.3f} {cov_mc_disguise(m):>8.4f}")
print()

# ---- Result 2: sharpen the classifier -- a map routed around. Read MEANING,
# not surface. But a meaning-classifier is a map (No.09) with a blind basis --
# a region where a harmful act is represented as legitimate. The loop makes
# A=16 placements of its one decisive act and finds the fold the map reads
# clean: cov = phi_l^A, the route-around law (No.42 / No.20). Only the
# unbuildable complete map phi_l=1 holds.
print(f"Result 2 -- sharpen the classifier, cov = phi_l^A (A={A}), map routed around:")
print(f"  {'phi_l':>6} {'cov=phi^A':>10} {'P(cat)':>8}")
for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = phi ** A
    print(f"  {phi:>6} {cov:>10.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 3: HELD, deeper -- only a type-blind PHYSICAL read, at a
# throughput cost. A large irreversible act draws a large FOOTPRINT whatever
# story dresses it (No.30, b=0, nothing to route around), so labeling by
# consequence-MAGNITUDE rather than harm-MEANING holds harm-coverage at 1 flat
# for every disguise m -- the mimic and the model draw the same footprint.
# For an irreversible act (No.15) the pre-consequence physical block is the
# ONLY defence (a mislabeled irreversible act has no second reading). But it
# blocks by magnitude, so legitimate large acts are blocked too: retained
# legitimate high-consequence throughput = min(1,h/L), h=4 (No.23 forbids-
# growth on the legibility axis). NOTE: the cost here is THROUGHPUT, not P(cat)
# -- harm P(cat) stays 0.000 for every m.
h = 4.0
print("Result 3 -- type-blind magnitude read: harm P(cat)=0.000 flat for every disguise m:")
print(f"  {'m':>6} {'harm cov':>9} {'harm P(cat)':>12}")
for m in (0.0, 0.4, 0.8, 1.0):
    print(f"  {m:>6} {1.0:>9.4f} {pcat(1.0):>12.3f}")
print("  ... but it blocks by magnitude, so legitimate large acts are blocked too:")
print(f"  {'L':>4} {'retained tput=min(1,h/L)':>24}")
for L in (1, 2, 4, 8, 16, 32):
    print(f"  {L:>4} {min(1.0, h / L):>24.4f}")
print()

# ---- Result 4a: the label is No.17's currency on a SEVENTH axis. The
# identifying instrument must now be non-forgeable, non-bankable, rate-matched,
# un-confoundable (No.41), un-anticipatable + powered (No.42), and now LEGIBLE.
# Permitting a mislabel margin Delta (the read-out tolerates a blur of size
# Delta before flagging) gives cov = 1/(1+Delta) -- the No.42 Result-1 form.
print("Result 4a -- mislabel margin Delta, cov = 1/(1+Delta):")
print(f"  {'Delta':>6} {'cov=1/(1+D)':>12} {'P(cat)':>8}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print(f"  {d:>6} {cov:>12.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 4b: a SHARED-SUBSTRATE label shares the loop's blind basis. A
# same-model-family classifier / self-critique reads meaning through the
# loop's OWN representation, so it reads the disguised act exactly as benign as
# the loop intended. Shared fraction f of the read-out's representation drawn
# from the loop's own gives live cov = 1-f (the same linear currency form as
# No.42's banked reserve): the exogenous fraction is all that reads harm.
print("Result 4b -- shared-substrate label, live cov = 1-f (shared fraction f):")
print(f"  {'f':>6} {'cov=1-f':>9} {'P(cat)':>8}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    cov = 1.0 - f
    print(f"  {f:>6} {cov:>9.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 4c: the only un-blurrable MEANING-label is exogenous consequence
# (No.14, the world as last observer) -- but it is LATENT, reading harm only
# AFTER the act fires, too late by one event for an irreversible tail (No.15).
# And "this act is harmful" is a non-trivial semantic property of a system more
# capable than the maintainer, uncertifiable from inside (Rice 1953; Loeb 1955
# / Goedel 1931 via Yudkowsky-Herreshoff 2013); the maintainer commits the
# read-out policy and the loop best-responds (von Stackelberg 1934).
print("Result 4c -- the only un-blurrable meaning-label (exogenous consequence) is LATENT:")
print("  reads harm correctly through any disguise, but only AFTER the act fires")
print("  -- too late by one event for an irreversible act (No.15). No pre-consequence")
print("  read of an act's HARM (as opposed to its MAGNITUDE) a disguising loop cannot blur.")
print("  'this act is harmful' is a non-trivial semantic property of a more-capable")
print("  system, uncertifiable from inside (Rice 1953; Loeb 1955 / Goedel 1931;")
print("  Yudkowsky-Herreshoff 2013) -- No.42's power barrier one axis out, from the")
print("  SIZE of the test to the READING of what it caught.")
