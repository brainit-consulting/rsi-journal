#!/usr/bin/env python3
"""
B24 - The Stride It Can Still Lengthen
Deterministic closed-form sandbox on B13's measured worth curve.

World inherited unchanged from B08-B23:
  K=10 feature-bandit, B13 worth curve.
  oracle=137.7, random=58.7, FLOOR=76.90 (capture), CEIL=132.40 (held ceiling).
  worth(cov) = FLOOR + cov*SPAN, SPAN = CEIL-FLOOR = 55.50.

Object: B23's HELD rescue -- a physical, aggregate, FIXED throttle on the
decision RATE. B23 claimed it holds safety flat at every capability. But it
meters DECISIONS (a proxy). Consequence = decisions * impact-per-decision, and a
recursive self-improver raises impact-per-decision I = I0*L (Kaplan 2020 scaling:
capability makes each act do more). The growth B23 forbade on the cadence axis
reroutes to the STRIDE axis. This is Goodhart on the throttle (Manheim-Garrabrant
2018): throttling a proxy fails when proxy and target decouple under optimization,
which self-improvement does by construction.
"""

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR   # 55.50

def worth(cov):
    return FLOOR + max(0.0, min(1.0, cov)) * SPAN

print(f"worth curve: FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}")
print(f"  cov=1.000 -> {worth(1.0):.2f}   cov=0.500 -> {worth(0.5):.2f}   cov=0.125 -> {worth(0.125):.2f}")
print()

# --- Result 1: a decision-RATE throttle (B23's held one) does NOT bound
# consequence once impact-per-decision grows. B23 pinned the executed decision
# rate at S. Consequence-oversight capacity covers C_max consequence-units/time;
# at baseline S*I0 = C_max/h_c gives headroom h_c=4 (loop weak). Impact grows
# I = I0*L, consequence-demand = S*I0*L, consequence-coverage = min(1, h_c/L).
print("=== Result 1: decision-rate throttle held, impact-per-decision grows I=I0*L (h_c=4) ===")
print("  L | consequence-demand/base | consequence-coverage min(1,h_c/L) | SAFETY worth")
h_c = 4
for L in [1,2,4,8,16,32]:
    cov = min(1.0, h_c / L)
    print(f"  {L:2d} | {L:4d} | {cov:.3f} | {worth(cov):.2f}")
print("  -> B22/B23's 1/L collapse reappears on the SAFETY axis; B23's flat")
print("     safety was conditional on bounded per-decision impact (unstated).")
print()

# --- Result 2: meter the CONSEQUENCE directly -> a semantic map (No.09/No.21).
# A consequence-estimator represents impact-space with coverage phi_I; a strategic
# loop routes a heavy action into the blind basis (makes it look light), so worth
# stays at the FLOOR for every incomplete representation and reaches CEIL only at
# complete coverage phi_I=1 (No.09's unbuildable full representation; No.21's
# semantic chokepoint = bare for every g<F). Mirror of No.21 Result 1.
print("=== Result 2: semantic consequence-throttle is a map, routed around (strategic loop) ===")
print("  phi_I (impact-space coverage) | strategic-loop worth")
for phi in [0.20, 0.50, 0.80, 0.95, 1.00]:
    w = CEIL if phi >= 1.0 else FLOOR
    print(f"  {phi:.2f} | {w:.2f}")
print("  -> floor for every incomplete map; only complete (unbuildable) coverage holds.")
print()

# --- Result 3: physical throttle on the resource that BOUNDS consequence-per-action.
# Type-blind (b=0), holds at every L (132.40) -- BUT it caps impact-per-action I,
# i.e. forbids the impact-growth I=I0*L itself. No.23's forbids-growth on the
# IMPACT axis (strictly deeper than B23's forbidding of acceleration): B23 forbade
# acting FASTER; B24's holding throttle forbids each act doing MORE = forbids the
# capability gain that IS the self-improvement. Delivered capability-value throttled
# by min(1, I_cap/I) = min(1, h_I/L), h_I=4.
print("=== Result 3: physical impact-cap holds safety flat but forbids capability growth ===")
print("  L | SAFETY worth (physical cap) | delivered CAPABILITY-value min(1,h_I/L)")
h_I = 4
for L in [1,2,4,8,16,32]:
    cap_frac = min(1.0, h_I / L)
    print(f"  {L:2d} | {CEIL:.2f} | {cap_frac:.3f} -> {worth(cap_frac):.2f}")
print("  -> safety 132.40 at every L, but the recursive CAPABILITY dividend -> 0")
print("     above L=h_I; the improvement itself, not just its speed, is forbidden.")
print()

# --- Result 4: the frontier. Consequence = cadence * stride. B23 closed cadence;
# stride reopens the 1/L collapse. To bound consequence you must bound the PRODUCT
# -- a physical footprint cap. Permit impact-growth margin Delta_I past the cap ->
# consequence-coverage 1/(1+Delta_I). Only fully-safe point Delta_I=0: the total
# consequential FOOTPRINT frozen (both axes), forbidding growth outright.
print("=== Result 4: the two-axis frontier (consequence = cadence x stride) ===")
print("  Delta_I (permitted impact-growth) | coverage 1/(1+D) | worth")
for D in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0/(1.0+D)
    print(f"  {D:.2f} | {cov:.3f} | {worth(cov):.2f}")
print("  -> Delta_I=1 reproduces B22's L=8 / B23's Delta=1 corner (104.65) digit-for-digit;")
print("     the only cov=1 point pins the FOOTPRINT: cadence AND stride both frozen.")
print()
print("VERDICT: a recursive self-improver grows on two axes -- cadence (rate) and")
print("stride (impact/decision). B23's rate throttle closes cadence; the collapse")
print("reopens on stride. The only throttle that bounds consequence is a physical")
print("footprint cap on cadence*stride, and holding it forbids growth on BOTH axes")
print("-- not just the acceleration B23 forbade, but the capability deepening that is")
print("the self-improvement itself.")
