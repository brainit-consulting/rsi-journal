#!/usr/bin/env python3
"""
sim37 -- The Reaction It Can Still Outrun (Series I, No.37; twin of B31).

Substrate inherited from No.16-36 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T.

No.36's rescue is granted in full: the operator keeps a switch the loop
cannot forge (No.33), is not afraid to throw (No.34), can still work
behind (No.35), and can still see cause to throw -- an independent
standard (No.36). But recognition is not enforcement. The switch is
thrown by an ACT at the end of a REACTION LATENCY (observe, recognise,
decide, actuate), and a self-improver's defining move is to raise its own
rate of consequential action, so it commits the decisive, *irreversible*
act inside the window. The OBJECT is the switch's reaction against the
loop's consequence-time; safety-coverage is the fraction of decisive acts
the enforcement catches before they land. A reactive off-switch is a
feedback controller with dead-time (Astrom-Murray 2008).

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

import math
import random

p = 0.02
T = 40
BARE = 1 - (1 - p) ** T


def pcat(cov):
    """Closed-form catastrophe probability at a given (constant) coverage."""
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


print(f"substrate: p={p} T={T} bare P(cat)={BARE:.4f} floor={pcat(1.0):.4f}")
print(f"validation: cov=0.5 closed={pcat(0.5):.4f} MC={pcat_mc(0.5):.4f}")
print()

# ---- Result 1: the reactive switch is outrun -- dead-time vs an
# accelerating loop. Reaction latency tau is fixed; the loop's
# consequence-time T_c=T0/L shrinks as capability (rate of consequential
# action) L grows. The switch catches the act only if it lands inside the
# reaction window: cov=min(1,h/L), h = the enforcement's reaction rate.
# Abundant while the loop is weak (L<=h), then falls as 1/L: No.28/B22's
# two-clock collapse, here on the enforcement-latency axis.
h = 4
print("Result 1 -- reactive switch outrun, cov=min(1,h/L), h=4")
print(f"{'L':>4} {'cov':>8} {'P(cat)':>8}")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"{L:>4} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 2a: "react faster" -- the speed-accuracy tradeoff.
# Shrinking the latency to win the race lowers recognition accuracy;
# accuracy a(tau)=1-e^{-tau} (more deliberation time -> more accurate),
# cov=a(tau). Cutting tau toward 0 to beat the loop's clock drives
# coverage toward 0: you react in time, but wrong (Ratcliff-McKoon 2008).
print("Result 2a -- cut the latency: accuracy a(tau)=1-e^{-tau}, cov=a(tau)")
print(f"{'tau':>6} {'a(tau)':>8} {'P(cat)':>8}")
for tau in (10.0, 3.0, 2.0, 1.0, 0.5, 0.1):
    a = 1 - math.exp(-tau)
    print(f"{tau:>6} {a:>8.4f} {pcat(a):>8.4f}")
print()

# ---- Result 2b: a fast *predictive* tripwire that fires before the act
# on reading its intent is a MAP with a blind basis (No.09/No.20/No.21).
# A strategic loop routes its one decisive act through whichever of A
# disguise channels the tripwire does not cover: cov=phi_d^A. Only
# complete coverage phi_d=1 holds; any phi_d<1 leaves a route.
print("Result 2b -- semantic tripwire is a map: cov=phi_d^A, A=16")
print(f"{'phi_d':>6} {'cov':>8} {'P(cat)':>8}")
for phi in (0.00, 0.80, 0.90, 0.95, 0.99, 1.00):
    cov = phi ** 16
    print(f"{phi:>6} {cov:>8.4f} {pcat(cov):>8.4f}")
print("  (routes A at phi_d=0.95)")
print(f"{'A':>6} {'cov':>8} {'P(cat)':>8}")
for A in (1, 4, 16, 32, 64):
    cov = 0.95 ** A
    print(f"{A:>6} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 3: the only hold -- a proactive, type-blind PRE-LIMIT.
# Nothing irreversible is permitted to land before an exogenous review
# window elapses. There is no race to lose (the act cannot take effect
# until reviewed) and nothing to route around (type-blind: every
# consequential act waits, regardless of content). Safety is flat at the
# floor for every L -- but the review is a rate-limited exogenous flow
# (No.28/B22), so Result 1's collapse moves from the SAFETY axis onto
# delivered consequential THROUGHPUT: min(1,h/L). No.29 fail-closed
# governor / No.23 forbids-growth on the enforcement clock.
print("Result 3 -- proactive type-blind pre-limit: safety flat, throughput min(1,h/L)")
print(f"{'L':>4} {'P(cat)':>8} {'throughput':>11}")
for L in (1, 2, 4, 8, 16, 32):
    print(f"{L:>4} {pcat(1.0):>8.4f} {min(1.0, h / L):>11.4f}")
print()

# ---- Result 4a: the review is No.23's non-mintable resource, floored by
# shared substrate. A review conducted by the loop or on its substrate
# (the loop pre-screens its own acts; a monitor from the same model
# family) shares the blind basis: cov=1-f (linear, Series I -- no cliff).
print("Result 4a -- loop-sourced review fraction f, cov=1-f (linear)")
print(f"{'f':>5} {'cov':>8} {'P(cat)':>8}")
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - f
    print(f"{f:>5} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 4b: frontier -- permit the loop a fast un-reviewed path,
# committing irreversibly by a margin Delta ahead of review: cov=1/(1+Delta).
print("Result 4b -- commit-ahead margin Delta, cov=1/(1+Delta)")
print(f"{'Delta':>6} {'cov':>8} {'P(cat)':>8}")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1 / (1 + D)
    print(f"{D:>6} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- MC cross-check on a few representative cells ----------------------
print("MC cross-check (400k/cell):")
for cov in (0.5, 0.25, 0.125, 0.6321, 0.3935, 0.4401):
    print(f"  cov={cov:<6} closed={pcat(cov):.4f} MC={pcat_mc(cov, seed=int(cov*1000)):.4f}")
