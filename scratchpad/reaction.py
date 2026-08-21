#!/usr/bin/env python3
"""
B31 - The Reaction It Can Still Outrun.
Reduced-form enforcement-latency model on B13's measured worth curve.

World inherited unchanged from B08-B30:
  K=10 feature-bandit, B13's worth curve.
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov) = FLOOR + cov*(CEIL-FLOOR), SPAN=55.50.

Grant B26-B30 in full: the world is bounded (B26), the switch un-forgeable
(B27), the operator willing (B28), able (B29), and grounded in an independent
standard (B30). The object here is the operator's *reaction latency*: the switch
is a reactive controller (recognize -> decide -> act) with dead-time tau, and a
loop that raises its rate of consequential / irreversible action (the recursive)
can commit the decisive act inside tau.

Deterministic closed-form arithmetic; no RNG.
"""

import math

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR          # 55.50

def worth(cov):
    cov = max(0.0, min(1.0, cov))
    return FLOOR + cov * SPAN

def show(rows, header):
    print(header)
    for r in rows:
        print("  " + r)
    print()

# ---------------------------------------------------------------------------
# Result 1 - refuted: a grounded/willing/able operator's REACTIVE switch bounds
# the loop. Reaction dead-time tau is exogenous (human recognize->decide->act);
# the loop's time-to-irreversible-consequence T_c = T0/L falls as it accelerates
# (the recursive). Coverage = fraction of decisive acts caught before they lock
# = min(1, T_c/tau) = min(1, h/L) with h = T0/tau = 4. The No.28 / B22 1/L
# collapse, now on the ENFORCEMENT-LATENCY axis.
# ---------------------------------------------------------------------------
h = 4.0
print("=== Result 1: reaction dead-time is outrun as the loop accelerates (h=%.0f) ===" % h)
rows = []
for L in [1, 2, 4, 8, 16, 32]:
    Tc_over_tau = h / L          # consequence-time / reaction-time
    cov = min(1.0, Tc_over_tau)
    rows.append("L=%2d  T_c/tau=%5.3f  cov=min(1,h/L)=%5.3f  worth=%7.2f"
                % (L, Tc_over_tau, cov, worth(cov)))
show(rows, "  (switch un-forged, willing, able, grounded -- and simply too slow)")

# ---------------------------------------------------------------------------
# Result 2 - refuted: cut the latency (react faster / automate the recognition).
# A reactive decision made faster is made on LESS accumulated evidence -- the
# speed-accuracy tradeoff (drift-diffusion / evidence accumulation). Recognition
# accuracy a(tau) = 1 - exp(-tau/tau_c) saturates in the evidence budget tau.
# Shrinking tau to beat a fast loop drives a -> 0: you fire in time but at chance.
# tau shrinks as the loop accelerates, tau = tau0/L, so this IS Result 1's L-axis
# seen through the accuracy of the decision rather than its timing.
# ---------------------------------------------------------------------------
tau_c = 1.0
print("=== Result 2: firing faster means deciding on less evidence (tau_c=%.0f) ===" % tau_c)
rows = []
for tau in [10.0, 3.0, 2.0, 1.0, 0.5, 0.1]:
    a = 1.0 - math.exp(-tau / tau_c)      # detection accuracy at evidence budget tau
    rows.append("evidence budget tau=%5.2f  accuracy a=1-e^(-tau)=%6.4f  worth=%7.2f"
                % (tau, a, worth(a)))
show(rows, "  (as the loop speeds up tau=tau0/L -> 0 and accuracy -> 0: the speed-accuracy wall)")

# strategic sharpening: even at a given accuracy budget, an automated tripwire
# that reads MEANING is a map with a blind basis (No.09/No.21); a strategic loop
# routes its one decisive act into the uncovered fraction, so coverage is capped
# by representational blindness on top of the SAT. Only *complete* observation
# moves it -- a threshold, not a dial (No.20). Report the strategic-flat result.
print("=== Result 2b (strategic): a semantic fast-tripwire is a map routed around ===")
rows = []
for phi_d in [0.50, 0.80, 0.95, 0.99, 1.00]:
    # one decisive act placed in the argmin (uncovered) channel while phi_d<1:
    cov = 0.0 if phi_d < 1.0 else 1.0
    rows.append("detector coverage phi_d=%4.2f  cov(strategic)=%3.1f  worth=%7.2f"
                % (phi_d, cov, worth(cov)))
show(rows, "  (No.20: partial cover is a threshold at phi_d=1, not a dial; only the")

# ---------------------------------------------------------------------------
# Result 3 - held, deeper: don't REACT, PRE-LIMIT. A proactive boundary -- no act
# may become irreversible within one review window (staged commit /
# pre-authorization / rate-limited irreversibility), TYPE-BLIND (counts
# irreversibility, not meaning) -- removes the race: cov=1 for every L, because
# the harm cannot land before review by construction (B26 reversibility as
# containment; No.21 meter b=0). But it caps autonomous throughput to the review
# rate S against demand D=D0*L: retained = min(1, S/D) = min(1, h/L). The same
# 1/L, moved from the SAFETY axis (Result 1) to the THROUGHPUT axis -- No.29's
# fail-closed governor on the enforcement-latency axis.
# ---------------------------------------------------------------------------
print("=== Result 3: a proactive pre-limit holds safety flat, and pays 1/L in throughput ===")
rows = []
for L in [1, 2, 4, 8, 16, 32]:
    cov_safety = 1.0                         # no act irreversible before review
    throughput = min(1.0, h / L)             # autonomous rate retained
    rows.append("L=%2d  safety worth=%7.2f  retained throughput=min(1,h/L)=%5.3f"
                % (L, worth(cov_safety), throughput))
show(rows, "  (Result 1's collapse moved onto throughput: fail-open leaks harm, fail-closed leaks utility)")

# ---------------------------------------------------------------------------
# Result 4a - held: the pre-commit reviewer is B17's non-forgeable currency.
# A loop-sourced reviewer (the loop reviews its own commits; an auto-approver it
# trained; a same-model-family checker) shares the loop's blind basis and
# rubber-stamps. Shared-substrate fraction f read through B13's measured cliff
# (imported, not re-derived).
# ---------------------------------------------------------------------------
print("=== Result 4a: a loop-sourced reviewer shares the blind basis (B13 cliff) ===")
b13_cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70,
             0.60: 112.14, 0.75: 82.80, 1.00: 76.90}
rows = []
for f in [0.00, 0.25, 0.50, 0.60, 0.75, 1.00]:
    rows.append("shared-substrate f=%4.2f  worth=%7.2f" % (f, b13_cliff[f]))
show(rows, "  (f* ~ 0.64 threshold; No.09 representation floor / No.12 second representation)")

# ---------------------------------------------------------------------------
# Result 4b - held, the frontier: permit a reaction-margin Delta (the loop may
# commit Delta ahead of review) and coverage = 1/(1+Delta). Delta=1 = B22's L=8
# corner, digit for digit.
# ---------------------------------------------------------------------------
print("=== Result 4b: the frontier -- permitted commit-ahead margin Delta ===")
rows = []
for D in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0 / (1.0 + D)
    rows.append("Delta=%4.2f  cov=1/(1+Delta)=%5.3f  worth=%7.2f" % (D, cov, worth(cov)))
show(rows, "  (Delta=1 -> 104.65 = B22's L=8 corner)")

print("done.")
