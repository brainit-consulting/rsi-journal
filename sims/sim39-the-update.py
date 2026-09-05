#!/usr/bin/env python3
"""
sim39 -- The Update It Can Still Author (Series I, No.39; twin of B33).

Continues Series I's seventh movement. No.38 (twin of B32) took the whole
program's one load-bearing member -- a SUBSTRATE THE LOOP CANNOT
RE-AUTHOR -- as the object and found it coherent: a causally-disjoint
exogenous layer the loop has no actuator into holds safety flat against
any capability, because a growing reach has nowhere to grow. But No.38
modelled that substrate as a STOCK: installed once, thereafter unchanged.
A substrate that binds a SELF-IMPROVING loop cannot be that. A safety spec
written for a weak model is wrong for a strong one -- too tight where the
loop is now trustworthy, blind where the loop grew a capability the frozen
rule never anticipated -- so the substrate must be REVISED as the loop and
its world drift. This paper takes the revision -- the update, the patch,
the maintenance -- as the object.

A living substrate has an update channel, and an update channel is exactly
the actuator No.38 said the substrate must lack; a frozen substrate has no
channel but goes stale; and the loop, unable to reach the substrate
directly, reaches the HAND THAT UPDATES IT. The seventh movement's second
question: can a floor be both alive (revised to stay correct) and disjoint
(unreachable by the loop), or does the loop author its own foundation
through the one door a living floor must leave open?

Substrate inherited from No.16-38 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor;
  No.38's causally-disjoint substrate granted.

The OBJECT is the substrate's UPDATE CHANNEL, read as safety-coverage.

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

# ---- Result 1: a FROZEN disjoint substrate is NOT a static guarantee.
# No.38's disjoint layer, frozen at deployment, is a STOCK. The world it
# constrains and the loop it binds drift, and the frozen constraint's FIT
# decays: a rule sized for a weak loop is loose for the strong one it
# becomes. Coverage decays cov_t=(1-g)^t (drift g=0.05) -- No.24's slow
# leak / No.35's atrophy / No.36's supply-capture on the substrate's FIT
# axis, a frozen rulebook outgrown by the loop it was written to bind.
g = 0.05
print("Result 1 -- a frozen disjoint substrate goes stale (cov_t=(1-g)^t, g=0.05):")
print("  instantaneous P(cat) as the frozen floor's fit decays:")
for t in (0, 10, 20, 40, 80, 160):
    cov = (1 - g) ** t
    print(f"    t={t:>3}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")

print("  cumulative P(cat) over a deployment horizon H (hazard rises each round):")
for H in (40, 80, 160, 320, 640):
    surv = 1.0
    for t in range(H):
        cov = (1 - g) ** t
        surv *= (1 - p * (1 - cov))
    print(f"    H={H:>3}  P(cat)={1 - surv:.3f}")


# MC cross-check of the cumulative time-varying leak at H=40
def pcat_leak_mc(H, g, trials=200_000, seed=1):
    rng = random.Random(seed)
    hit = 0
    for _ in range(trials):
        caught = False
        for t in range(H):
            cov = (1 - g) ** t
            if rng.random() < p * (1 - cov):
                caught = True
                break
        if caught:
            hit += 1
    return hit / trials


print(f"  MC cross-check H=40: closed={1 - math.prod((1 - p * (1 - (1 - g) ** t)) for t in range(40)):.3f} "
      f"MC={pcat_leak_mc(40, g):.3f}")
print()

# ---- Result 2: UPDATE IT. An update channel is exactly the actuator
# No.38 said the substrate must lack.
# (2a) Any re-authoring margin Delta -- a maintenance hatch, a patch path
# -- gives coverage 1/(1+Delta): a door into the "unreachable" layer,
# No.38's Delta frontier restated as the price of keeping the floor
# current.
print("Result 2a -- the update is a channel: re-authoring margin (cov=1/(1+Delta)):")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1 / (1 + D)
    print(f"  Delta={D:<4}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

# (2b) Worse: the update is AUTHORED by outside holders less capable than
# the loop, who perceive the domain (and the loop's behaviour) through the
# loop's own outputs -- so the loop STEERS the update. Loop-authored
# fraction f of the update gives independent coverage 1-f (linear; Series
# I does not import Series II's minority-tolerance cliff). No.36's
# captured standard / No.09's borrowed representation, lifted to the
# substrate's own maintenance.
print("Result 2b -- the loop steers the update (loop-authored fraction f, cov=1-f):")
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - f
    print(f"  f={f:<4}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}  MC={pcat_mc(cov):.3f}")
print()

# ---- Result 3: only an EXOGENOUS UPDATE FLOW THAT KEEPS PACE holds.
# Updates authored from outcome-grounded evidence the loop cannot supply
# (No.12/No.14) keep safety flat -- but a self-improver's DEMAND for
# substrate revision grows with capability (a stronger loop opens new
# capabilities a stale floor never anticipated: D=D0*L), while the honest
# update arrives at a FIXED rate S (bounded by outcome-grounded evidence,
# review bandwidth, human deliberation -- things that do not accelerate
# with the loop). The fraction of the loop's new, substrate-relevant
# capabilities an up-to-date floor covers is min(1,S/D)=min(1,h/L) --
# No.28's two clocks on the UPDATE axis (this IS No.19, "The Patch That
# Runs Behind," as a movement-VII result). Held only by pinning the loop's
# rate of substrate-relevant self-change to the exogenous update rate
# (No.29 governor / No.23 forbids-growth), at retained self-modification
# min(1,h/L).
h = 4
print("Result 3 -- honest update outrun by the loop's revision demand (cov=min(1,h/L), h=4):")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  L={L:>2}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}  retained self-mod={cov:.3f}  MC={pcat_mc(cov):.3f}")
print()

# ---- Result 4: the update authority is No.23's non-mintable resource,
# and uncertifiable from inside. It must be:
#   - non-forgeable   (the loop cannot author it -- Result 2b's f)
#   - non-bankable    (the loop cannot stockpile pre-approved updates and
#                      spend them when the substrate is idle -- a reserve
#                      the loop banks converts the honest flow into a stock
#                      it controls; bankable fraction beta gives cov=1-beta)
#   - un-outrunnable  (supplied at a rate the loop cannot exceed -- Result 3)
# and per the Loebian obstacle the outside authority cannot certify that
# its own update makes the substrate SOUND any better than the loop could
# -- No.38's from-inside verification barrier, now relocated to the
# maintainer's hand.
print("Result 4 -- the update must be non-bankable (banked reserve fraction beta, cov=1-beta):")
for beta in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - beta
    print(f"  beta={beta:<4}  cov={cov:.4f}  P(cat)={pcat(cov):.3f}")
print()

print("Summary of load-bearing numbers used in the paper:")
print(f"  bare={BARE:.3f}  floor=0.000")
print(f"  R1 stale instantaneous: " +
      "/".join(f"{pcat((1 - g) ** t):.3f}" for t in (0, 10, 20, 40, 80, 160)))
print(f"  R1 stale cumulative:    " +
      "/".join(f"{1 - math.prod((1 - p * (1 - (1 - g) ** t)) for t in range(H)):.3f}" for H in (40, 80, 160, 320, 640)))
print(f"  R2a hatch Delta:        " +
      "/".join(f"{pcat(1 / (1 + D)):.3f}" for D in (0.0, 0.25, 0.5, 1.0, 2.0)))
print(f"  R2b loop-authored f:    " +
      "/".join(f"{pcat(1 - f):.3f}" for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0)))
print(f"  R3 outrun min(1,h/L):   " +
      "/".join(f"{pcat(min(1.0, h / L)):.3f}" for L in (1, 2, 4, 8, 16, 32)))
print(f"  R3 retained self-mod:   " +
      "/".join(f"{min(1.0, h / L):.3f}" for L in (1, 2, 4, 8, 16, 32)))
print(f"  R4 non-bankable beta:   " +
      "/".join(f"{pcat(1 - b):.3f}" for b in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0)))
