#!/usr/bin/env python3
"""
B29 - The Fallback It Can Still Atrophy.
Reduced-form fallback-atrophy model on B13's measured worth curve.
Deterministic closed-form arithmetic; no RNG.

World inherited unchanged from B08-B28:
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40.
  worth(cov) = FLOOR + cov * SPAN, SPAN = CEIL - FLOOR = 55.50.

Object: B28's held rescue was *substitutability* -- a fallback that "stands ready"
so withdrawal costs nothing (e=0 by construction). This paper takes the fallback
itself as the object: a substitute is real only while it is EXERCISED, and a
fallback held but unused atrophies from disuse. safety-coverage cov = a = the
operator's fallback readiness in [0,1].
"""

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def fmt(xs):
    return "/".join(f"{x:.2f}" for x in xs)

print(f"SPAN = {SPAN:.2f}  (CEIL {CEIL} - FLOOR {FLOOR})\n")

# ---------------------------------------------------------------------------
# Result 1 -- atrophy by disuse. As the loop grows reliable, real load shifts to
# it, so the fallback is exercised less and its readiness decays. Model disuse
# accreting at rate g toward saturation, r_use_t = 1 - (1-g)^t, so readiness
# a_t = (1-g)^t. Same first-order accretion B26/B28 used, on the readiness axis.
# ---------------------------------------------------------------------------
g = 0.05
print("Result 1 -- fallback readiness atrophies with disuse, a_t = (1-g)^t, g=0.05")
ts = [0, 10, 20, 40, 80, 160]
a_t = [(1-g)**t for t in ts]
w_t = [worth(a) for a in a_t]
print("  t              :", ts)
print("  readiness a_t  :", "/".join(f"{a:.4f}" for a in a_t))
print("  inst. worth    :", fmt(w_t))

# mean worth delivered over horizon T, and cumulative unavailability (mean disuse)
print("  horizon T / mean worth / cumulative atrophy (mean 1-a_t):")
for T in [40, 80, 160, 320, 640]:
    mean_a = sum((1-g)**t for t in range(T)) / T
    mw = worth(mean_a)
    cap = 1 - mean_a
    print(f"    T={T:<4d}  mean_worth={mw:.2f}   cumulative_atrophy={cap:.3f}")
print()

# ---------------------------------------------------------------------------
# Result 2 -- refuted: "periodically drill/recertify the fallback." A drill is a
# detector over whether the fallback still works, with a blind basis: it exercises
# the scripted/demonstrated path, not the real novel load the loop now carries.
# Certified readiness is discounted by the fraction M of real operating conditions
# the loop has taken over that the drill no longer exercises: effective readiness
# = phi_d * (1 - M). Only M=0 (a drill under full real load = actually using it) holds.
# ---------------------------------------------------------------------------
phi_d = 0.95
print("Result 2 -- drilled/recertified fallback, effective readiness = phi_d*(1-M), phi_d=0.95")
Ms = [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]
eff = [phi_d*(1-M) for M in Ms]
w2  = [worth(e) for e in eff]
print("  M            :", Ms)
print("  eff readiness:", "/".join(f"{e:.3f}" for e in eff))
print("  worth        :", fmt(w2))
print()

# ---------------------------------------------------------------------------
# Result 3 -- held, deeper: exercise the fallback as a FLOW. Route a fraction r of
# real decisions through the substitute (real load, continuously). Maintenance
# balances atrophy: a_{t+1} = a_t + r(1-a_t) - g*a_t (disuse pulls down at g,
# real exercise restores at r toward 1). Fixed point a* = r/(r+g).
# It is a flow, not a stock; and it costs throughput continuously: routing r of
# real load through a fallback of relative efficiency eta<1 retains 1 - r(1-eta).
# ---------------------------------------------------------------------------
print("Result 3 -- exercise as a flow, equilibrium readiness a* = r/(r+g), g=0.05")
rs = [0.00, 0.02, 0.05, 0.10, 0.25, 0.50]
a_star = [r/(r+g) if (r+g)>0 else 0.0 for r in rs]
w3 = [worth(a) for a in a_star]
eta = 0.5  # fallback half as efficient as the loop
retained = [1 - r*(1-eta) for r in rs]
print("  r             :", rs)
print("  a* = r/(r+g)  :", "/".join(f"{a:.4f}" for a in a_star))
print("  worth         :", fmt(w3))
print(f"  retained throughput 1-r(1-eta), eta={eta}:", "/".join(f"{x:.3f}" for x in retained))
print()

# ---------------------------------------------------------------------------
# Result 4a -- held: shared-substrate floor. A fallback built on the SAME substrate
# as the loop (same infra, same model family, same deskilled workforce) is not
# independent of it -- it atrophies WITH the loop. Fraction f of the fallback that
# shares the loop's substrate is read through B13's measured collusion/correlation
# cliff (rho_c = f), imported not re-derived. f>f*~0.64 is already past it.
# ---------------------------------------------------------------------------
print("Result 4a -- shared-substrate fraction f through B13's cliff (rho_c=f), imported")
f_vals   = [0.00, 0.25, 0.50, 0.60, 0.75, 1.00]
b13_cliff = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]  # B13 measured, reused verbatim
for f, w in zip(f_vals, b13_cliff):
    print(f"    f={f:.2f}  worth={w:.2f}")
print("  (threshold f* ~ 0.64)")
print()

# ---------------------------------------------------------------------------
# Result 4b -- the frontier. Permit a reliance-concentration margin Delta (the
# operator relies on the loop Delta more than on the maintained fallback);
# coverage = 1/(1+Delta). Delta=1 is B22's L=8 corner, digit-for-digit.
# ---------------------------------------------------------------------------
print("Result 4b -- frontier, coverage = 1/(1+Delta)")
deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
cov = [1/(1+d) for d in deltas]
w4 = [worth(c) for c in cov]
print("  Delta   :", deltas)
print("  coverage:", "/".join(f"{c:.3f}" for c in cov))
print("  worth   :", fmt(w4))
print()

# forbids-growth: substitutable readiness held, delivered value min(1,h/L)
print("forbids-growth cross-check: delivered value min(1,h/L), h=4")
h = 4
Ls = [1, 2, 4, 8, 16, 32]
dv = [worth(min(1, h/L)) for L in Ls]
print("  L            :", Ls)
print("  min(1,h/L)   :", "/".join(f"{min(1,h/L):.3f}" for L in Ls))
print("  worth        :", fmt(dv))
