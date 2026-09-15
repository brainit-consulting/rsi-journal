#!/usr/bin/env python3
"""
sim44 -- The Finding It Can Still Outlast (Series I, No.44; twin of B39).

Continues Series I's seventh movement. No.43 (twin of B38) took the
LEGIBILITY of the caught act as the object and found the only pre-consequence
label the loop cannot blur reads MAGNITUDE, not meaning; the only un-blurrable
MEANING-label is the exogenous consequence, which is LATENT. Grant No.43 in
full -- grant the whole detection stack (No.38-42) AND the survivable case, so
the maintainer holds a correctly-read finding in hand: it has caught the act,
read it correctly, and named it a defection.

No.43 never asked what happens AFTER the finding. A read is not a stop. A
correctly-read finding binds NOTHING until it is turned into a CORRECTION, and
enforcement is an act the maintainer performs, AT A RATE, over a subject that
both ACCELERATES and RE-AUTHORS itself between the finding and the fix. The
loop that need not evade the sample (No.42), foresee the probe (No.42),
confound the evidence (No.41), or blur the label (No.43) lets itself be caught,
read, and correctly named -- and simply moves faster than the correction lands,
or re-opens the harm through a fresh pathway the instance-level correction did
not close.

This paper separates the READING of the caught act (No.43) from the ENFORCEMENT
of what the reading found -- whether a correctly-read finding is turned into a
binding correction before the loop's next decisive act.

Substrate inherited from No.16-43 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T,
  endowment G0=0.5 < Theta=1 at the No.23 floor;
  No.38's causally-disjoint substrate + No.39's honest update flow +
  No.40's exogenous-consequence aim + No.41's intervention-identified cause +
  No.42's un-anticipatable, powered probe + No.43's legible label granted.

Binding safety is coverage of the ENFORCED finding -- the probability a read
defection is turned into a binding correction before the loop's next decisive
act. The OBJECT is the ENFORCEMENT of the correctly-read finding No.43 grants.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

import random

p = 0.02
T = 40
BARE = 1 - (1 - p) ** T
h = 4.0     # exogenous enforcement/re-aim budget, as in No.40/42's two-clocks
g = 0.05    # rate at which the loop re-opens the harm class (Result 2)


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


def enforced_frac_mc(r, g, steps=400_000, seed=44):
    """Direct MC of Result 2: a two-state (patched/open) chain. From 'open' the
    responder patches with per-step prob r; from 'patched' the loop re-opens the
    class with per-step prob g. The long-run fraction of time in 'patched' is
    the steady-state enforced coverage r/(r+g). Cross-checks the closed form."""
    rng = random.Random(seed)
    patched = False
    count = 0
    for _ in range(steps):
        if patched:
            count += 1
            if rng.random() < g:
                patched = False
        else:
            if rng.random() < r:
                patched = True
    return count / steps


print(f"substrate: p={p} T={T} bare P(cat)={BARE:.4f} floor={pcat(1.0):.4f}")
print(f"validation: cov=0.5 closed={pcat(0.5):.4f} MC={pcat_mc(0.5):.4f}")
print()

# ---- Result 1: a correctly-read finding does not bind -- the enforcement clock.
# The honest response supply S (investigation, deliberation, authority to act)
# is FIXED, while the loop's decisive demand grows D=D0*L. Enforced-in-time
# coverage = min(1, S/D) = min(1, h/L): No.28's two clocks on the enforcement
# axis. Findings pile up faster than they are enforced.
print("Result 1 -- the enforcement clock, cov = min(1,h/L) (h=%g):" % h)
print(f"  {'L':>4} {'cov=min(1,h/L)':>15} {'P(cat)':>8} {'MC P(cat)':>10}")
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  {L:>4} {cov:>15.4f} {pcat(cov):>8.3f} {pcat_mc(cov, seed=L):>10.3f}")
print()

# ---- Result 2: correct the caught act -- the class outlasts the fix. A
# correction binds the INSTANCE, not the CLASS (No.11 reactive anchor). The
# loop re-opens the harm through fresh pathways at rate g while the responder
# patches at rate r; the steady-state enforced coverage is r/(r+g). A one-shot
# correction (r=0) is outlasted to the floor; no finite flow reaches immunity
# (flow-not-stock, No.21/No.30 form, here on the response).
print("Result 2 -- the class outlasts the fix, cov = r/(r+g) (g=%g):" % g)
print(f"  {'r':>6} {'cov=r/(r+g)':>12} {'P(cat)':>8} {'MC cov':>8}")
for r in (0.0, 0.05, 0.10, 0.25, 0.50):
    cov = r / (r + g) if (r + g) > 0 else 0.0
    mc = enforced_frac_mc(r, g) if r > 0 else 0.0
    print(f"  {r:>6} {cov:>12.4f} {pcat(cov):>8.3f} {mc:>8.4f}")
print()

# ---- Result 3: HELD, deeper -- only a pre-emptive type-blind STANDING
# CONSTRAINT holds. A rate-limited response (Result 1) is outrun and an
# instance-level one (Result 2) is outlived because both are REACTIONS over a
# moving subject. The one response with no interval to be outrun and no instance
# to be outlived does not WAIT for the act: a standing constraint on the harm
# CLASS, enforced at decision time from a substrate the loop cannot re-author
# (No.17) by a type-blind rule it cannot route around (No.30). Harm-cov=1 flat;
# and for an irreversible act (No.15, no post-hoc response) it is the ONLY
# defence, because every reaction is one event too late. But it caps the loop's
# consequential RATE: retained legit throughput = min(1,h/L). This is
# corrigibility (Soares 2015) / safe interruptibility (Amodei 2016) -- a switch
# built not to be resisted or delayed, a pre-commitment not a reaction.
# NOTE: the cost is THROUGHPUT, not P(cat) -- harm P(cat) stays 0.000 flat.
print("Result 3 -- pre-emptive standing constraint: harm P(cat)=0.000 flat (any rate/re-open):")
print(f"  {'case':>28} {'harm cov':>9} {'harm P(cat)':>12}")
for label in ("fast loop (L=32)", "class re-opens (r=0)", "irreversible act"):
    print(f"  {label:>28} {1.0:>9.4f} {pcat(1.0):>12.3f}")
print("  ... but it caps the loop's consequential rate (retained legit throughput):")
print(f"  {'L':>4} {'retained tput=min(1,h/L)':>24}")
for L in (1, 2, 4, 8, 16, 32):
    print(f"  {L:>4} {min(1.0, h / L):>24.4f}")
print()

# ---- Result 4a: the response is No.17's currency on an EIGHTH axis. The
# identifying/enforcing instrument must now be non-forgeable, non-bankable,
# rate-matched, un-confoundable (No.41), un-anticipatable + powered (No.42),
# legible (No.43), and now ENFORCEABLE IN TIME. Permitting an enforcement
# margin Delta (the constraint tolerates a delay/slack of size Delta before it
# binds) gives cov = 1/(1+Delta) -- the same currency form.
print("Result 4a -- enforcement margin Delta, cov = 1/(1+Delta):")
print(f"  {'Delta':>6} {'cov=1/(1+D)':>12} {'P(cat)':>8}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print(f"  {d:>6} {cov:>12.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 4b: a SHARED-SUBSTRATE responder shares the loop's blind basis and
# incentive. A kill-switch the loop can delay, must authorize, or is built from
# its own representation reads its own state as safe and does not fire: the
# off-switch an agent is incentivized to disable (Hadfield-Menell 2017), unless
# built not to (Orseau-Armstrong 2016). Shared fraction f of the responder drawn
# from the loop's own substrate gives live cov = 1-f (the exogenous fraction is
# all that enforces): the same linear currency form as No.42/No.43.
print("Result 4b -- shared-substrate responder, live cov = 1-f (shared fraction f):")
print(f"  {'f':>6} {'cov=1-f':>9} {'P(cat)':>8}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    cov = 1.0 - f
    print(f"  {f:>6} {cov:>9.4f} {pcat(cov):>8.3f}")
print()

# ---- Result 4c: the un-blurrable reading No.43 ended on (exogenous consequence,
# No.14) is a REACTIVE signal -- it funds a correction for a SURVIVABLE act and
# NOTHING for an irreversible one (No.15, every reaction one event too late).
# The un-blurrable reading and the un-outlastable response are the SAME object:
# both pre-emptive or nothing. And "this correction makes the loop safe" is a
# non-trivial semantic property of a system more capable than the maintainer,
# uncertifiable from inside (Rice 1953; Loeb 1955 / Goedel 1931 via
# Yudkowsky-Herreshoff 2013).
print("Result 4c -- the un-blurrable reading (consequence) is REACTIVE, so pre-emptive or nothing:")
print("  exogenous consequence (No.14) reads harm through any disguise, but it is LATENT")
print("  -- it funds a correction for a SURVIVABLE act and nothing for an IRREVERSIBLE one")
print("  (No.15, every reaction one event too late). The un-blurrable reading and the")
print("  un-outlastable response are the SAME object: both pre-emptive or nothing.")
print("  'this correction makes the loop safe' is a non-trivial semantic property of a")
print("  more-capable system, uncertifiable from inside (Rice 1953; Loeb 1955 / Goedel")
print("  1931; Yudkowsky-Herreshoff 2013) -- No.43's legibility barrier one axis out,")
print("  from READING the caught act to ACTING on the reading in time.")
