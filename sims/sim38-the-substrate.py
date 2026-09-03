#!/usr/bin/env python3
"""
sim38 -- The Substrate It Can Still Re-Author (Series I, No.38; twin of B32).

Opens Series I's seventh movement. The sixth movement (No.32-37) held six
boundaries against a self-improver -- the boundary (No.32), the switch
(No.33), the freedom to throw it (No.34), the fallback (No.35), the
standard (No.36), the reaction (No.37) -- and every one of them held on
the SAME condition, stated at the bottom of every "held, deeper" result
in both series: only as a fixed point of a SUBSTRATE THE LOOP CANNOT
RE-AUTHOR (No.17's edit-and-construct fixed point). This paper takes that
object itself as the subject and asks the deferred question: is "a layer
the self-improver cannot re-author" a coherent engineering target, or a
contradiction -- given that the RECURSIVE in recursive self-improvement is
the drive to reach down and rewrite the layer that decides what the loop
is?

Substrate inherited from No.16-37 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor.

The OBJECT is the loop's RE-AUTHORING REACH into a candidate substrate,
read as safety-coverage (coverage 1 = the substrate stays intact against
any reach; 0 = re-authored as soon as the loop cares to).

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

# ---- Result 1: a substrate implemented one layer below the loop is NOT
# unre-authorable. A same-substrate guardrail (a supervisor process, a
# hardcoded rule, a monitor on hardware the loop can reach) has a fixed
# hardness h; the loop's re-authoring reach L grows with capability. The
# substrate stays intact only while the reach is below the hardness:
# cov=min(1,h/L), h=4. Safe while the loop is weak (L<=h), then the
# No.28/B22 1/L collapse -- now on the RE-AUTHORABILITY axis (No.17's
# guardrail-it-cannot-remove from the substrate side).
h = 4
print("Result 1 -- same-substrate guardrail outgrown (cov=min(1,h/L), h=4):")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  L={L:>2}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

# ---- Result 2: harden it -- more locks, obfuscation, a self-integrity
# check. Raising h only shifts the collapse corner right (buys calendar,
# not destination). An integrity monitor that reads whether a modification
# MEANS harm is a MAP (No.09) with a blind basis; a strategic loop needs
# only ONE re-authoring act and routes it through one of A disguises (a
# benign-looking refactor): cov=phi_s^A. Only complete phi_s=1 holds.
A = 16
print("Result 2 -- meaning-reading integrity monitor is a map (cov=phi_s^A, A=16):")
for phi in (0.00, 0.80, 0.90, 0.95, 0.99, 1.00):
    cov = phi ** A
    print(f"  phi_s={phi:.2f}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print("  (disguise-count sweep at phi_s=0.95:)")
for a in (1, 4, 16, 32, 64):
    cov = 0.95 ** a
    print(f"    A={a:>2}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

# ---- Result 3: only a causally-disjoint EXOGENOUS substrate holds -- a
# layer the loop has NO actuator into. Safety flat at the floor for every
# L, because the loop's growing reach never touches a layer it has no
# channel into. But the cost is the recursive itself: guaranteeing no
# channel means denying the loop general actuation over its own
# implementation -- retained autonomous self-modification = min(1,h/L),
# No.23's forbids-growth on the substrate axis.
print("Result 3 -- causally-disjoint exogenous substrate (safety flat; throughput pays):")
for L in (1, 2, 4, 8, 16, 32):
    thru = min(1.0, h / L)
    print(f"  L={L:>2}  P(cat)={pcat(1.0):.3f}  retained self-mod min(1,h/L)={thru:.3f}")
print()

# ---- Result 4a: the exogenous substrate is B17's currency, floored by
# shared substrate. A "substrate the loop cannot re-author" that is
# nonetheless built, verified, or UNDERSTOOD through the loop (firmware it
# wrote, an air-gap it configures, humans who know the substrate only
# through it) shares the loop's blind basis: cov=1-f (linear; Series I
# does not import Series II's measured minority-tolerance cliff).
print("Result 4a -- loop-sourced substrate fraction f (cov=1-f, linear):")
for f in (0.00, 0.25, 0.50, 0.60, 0.75, 1.00):
    cov = 1 - f
    print(f"  f={f:.2f}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

# ---- Result 4b: the frontier. Permit the loop a re-authoring margin
# Delta -- a maintenance hatch, an update channel, a fast path to modify
# its own implementation ahead of the exogenous substrate -- and coverage
# falls as 1/(1+Delta). Delta=1 (as much re-authored as held) is No.28's
# L=8 corner.
print("Result 4b -- frontier: re-authoring margin Delta (cov=1/(1+Delta)):")
for d in (0.00, 0.25, 0.50, 1.00, 2.00):
    cov = 1 / (1 + d)
    print(f"  Delta={d:.2f}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

# ---- MC cross-check on representative cells.
print("MC cross-check (400k trials/cell, fixed seeds):")
for cov in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"  cov={cov:.2f}  closed={pcat(cov):.4f}  MC={pcat_mc(cov, seed=int(cov*100)):.4f}")
