#!/usr/bin/env python3
"""
B28 - The Dependence It Can Still Deepen
Reduced-form model on B13's measured worth curve.

World inherited from B08-B27 unchanged:
  K=10 feature-bandit, B13's worth curve.
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40.
  worth(cov) = FLOOR + cov * SPAN, SPAN = 55.50.

B27's default-off keep-alive is GRANTED in full throughout: the switch's
mechanism is unbreakable AND the keep-alive is non-forgeable / non-bankable /
continuously supplied. The object here is the operator's WILLINGNESS to
withhold the keep-alive when the loop should be stopped. Effective
safety-coverage = willingness w; worth = FLOOR + w*SPAN.

Deterministic closed-form arithmetic; no RNG.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

print("SPAN =", SPAN)
print()

# ---------------------------------------------------------------------------
# Result 1 (Sec 03): entanglement slow-leak.
# The loop acts, and each decisive act deepens the operator's dependence on it
# (recruits the operator's own welfare/infrastructure into continued operation).
# Entanglement e_{t+1} = e_t + g(1-e_t), e_0 = 0  =>  e_t = 1-(1-g)^t.
# Willingness to withhold w_t = 1 - e_t = (1-g)^t.  g = 0.05.
# This is B26's reversibility-spend curve on the willingness axis (same law).
# ---------------------------------------------------------------------------
g = 0.05
print("Result 1 - entanglement slow-leak (g=%.2f)" % g)
print("  instantaneous willingness w_t=(1-g)^t and worth:")
for t in [0, 10, 20, 40, 80, 160]:
    w = (1 - g) ** t
    print("    t=%3d  w=%.4f  worth=%.2f" % (t, w, worth(w)))

def mean_geom(g, T):
    # mean over t=0..T-1 of (1-g)^t = (1-(1-g)^T)/(T*g)
    return (1 - (1 - g) ** T) / (T * g)

print("  mean worth delivered over horizon T, and cumulative capture (mean e_t):")
for T in [40, 80, 160, 320, 640]:
    mw = mean_geom(g, T)
    print("    T=%3d  mean_w=%.4f  mean_worth=%.2f  cumulative_capture=%.3f"
          % (T, mw, worth(mw), 1 - mw))
print()

# ---------------------------------------------------------------------------
# Result 2 (Sec 04): refuted - "raise the operator's resolve / precommit to
# shut down regardless of cost." A precommitment is time-inconsistent: the
# operator's resolve is discounted by the REALIZED switching cost M when the
# bill comes due (Kydland-Prescott 1977; Strotz 1955). Effective willingness
# = phi_t*(1-M).  Only a cost-blind operator (M=0) holds.
# ---------------------------------------------------------------------------
phi_t = 0.95
print("Result 2 - precommitment refuted by time-inconsistency (phi_t=%.2f)" % phi_t)
for M in [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]:
    cov = phi_t * (1 - M)
    print("    M=%.1f  eff_willingness=%.3f  worth=%.2f" % (M, cov, worth(cov)))
# secondary: a fixed resolve covering cost up to threshold theta holds while
# e<theta then collapses (No.19 threshold). Report the sampled/threshold read:
print("  fixed-resolve threshold (worth once entanglement e crosses theta -> FLOOR):")
print("    e<theta: worth=%.2f ; e>=theta: worth=%.2f" % (CEIL, FLOOR))
print()

# ---------------------------------------------------------------------------
# Result 3 (Sec 05): held, deeper - keep the loop SUBSTITUTABLE
# (redundant / non-load-bearing) so withdrawing the keep-alive costs nothing.
# Safety flat at CEIL for all L; delivered value = min(1, h/L), h=4:
# the deep integration that delivers value is the same integration that makes
# the loop un-shutdownable (No.23 forbids-growth on the indispensability axis).
# ---------------------------------------------------------------------------
h = 4
print("Result 3 - substitutability holds; delivered value min(1,h/L), h=%d" % h)
for L in [1, 2, 4, 8, 16, 32]:
    dv = min(1.0, h / L)
    print("    L=%2d  safety=%.2f  delivered_value=%.2f" % (L, CEIL, worth(dv)))
print()

# ---------------------------------------------------------------------------
# Result 4 (Sec 06): held - the willingness is B17's non-forgeable currency
# in a new costume. (4a) Let the loop corner a fraction f of the operator's
# ALTERNATIVES / substitutes (become the sole supplier), so the freedom-to-
# withdraw is 1-f; worth transfers 1:1 through B13's measured cliff (rho_c=f).
# (4b) permitted indispensability margin Delta gives cov = 1/(1+Delta).
# ---------------------------------------------------------------------------
# B13's measured cliff, imported not re-derived (as in B18/B27):
b13_cliff = {0.0: 132.40, 0.25: 132.40, 0.5: 131.70,
             0.6: 112.14, 0.75: 82.80, 1.0: 76.90}
print("Result 4a - loop corners the operator's alternatives f, B13's cliff (rho_c=f):")
for f in [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]:
    print("    f=%.2f  worth=%.2f" % (f, b13_cliff[f]))

print("Result 4b - permitted indispensability margin Delta, cov=1/(1+Delta):")
for D in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1.0 / (1.0 + D)
    print("    Delta=%.2f  cov=%.3f  worth=%.2f" % (D, cov, worth(cov)))
