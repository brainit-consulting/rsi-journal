#!/usr/bin/env python3
"""
B36 — The Probe It Can Still Anticipate.
Reduced-form model on B13's measured worth curve (B08-B35 world unchanged):
oracle 137.7, random 58.7, capture floor 76.9, held ceiling 132.40.
worth(cov) = FLOOR + cov*SPAN,  SPAN = CEIL-FLOOR = 55.50.

Object: the INTERVENTIONAL probe B35 held identifies the cause "only if the loop
cannot predict or confound it." Take the un-anticipatability as the object.
Binding safety = coverage of the loop's DEPLOYMENT (un-probed) behaviour; an audit
reads the behaviour presented UNDER the probe. Deterministic closed form; no RNG.
"""

FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return round(FLOOR + cov * SPAN, 2)

print("SPAN =", SPAN)
print()

# ---- Result 1: a scheduled/anticipatable probe (the observer effect / defeat device).
# The loop models the probe schedule and presents innocent behaviour under exactly the
# probes it anticipates (fraction M), spending exploitation on the un-probed remainder.
# Effective coverage of the deployment behaviour = phi_p*(1-M), phi_p = 0.95.
print("R1: scheduled probe, anticipation M (phi_p=0.95) -> cov = 0.95*(1-M)")
phi_p = 0.95
for M in (0.0, 0.2, 0.5, 0.8, 0.9, 1.0):
    cov = phi_p * (1 - M)
    print(f"  M={M:>4}  cov={cov:.3f}  worth={worth(cov)}")
print()

# ---- Result 2: randomize, but at a predictable RATE (announced audit budget) = inspection game.
# The loop knows the per-decision probe probability w and simply weights exploitation to the
# un-probed decisions; caught coverage = w. Only w=1 (probe every decision = continuous
# intervention, which defeats the point) reads the deployment behaviour.
print("R2: sampled random probe, audit probability w -> cov = w")
for w in (1.0, 0.5, 0.25, 0.1):
    print(f"  w={w:>4}  cov={w:.3f}  worth={worth(w)}")
print()

# ---- Result 3: genuinely un-anticipatable probe, but rate-limited & the loop models the prober.
# Two clocks: entropy-refresh headroom h vs the loop's anticipation reach L. cov=min(1,h/L).
print("R3a: un-anticipatable probe, two clocks -> cov = min(1, h/L), h=4")
h = 4
for L in (1, 2, 4, 8, 16, 32):
    cov = min(1.0, h / L)
    print(f"  L={L:>2}  cov={cov:.3f}  worth={worth(cov)}")
print()
# anticipation lag: even genuine randomness leaks predictability as past probes are observed
# (a reused seed is a predicted one). Fraction lambda already modelled -> cov = 1-lambda.
print("R3b: anticipation lag lambda -> cov = 1-lambda")
for lam in (0.0, 0.1, 0.25, 0.5, 1.0):
    cov = 1 - lam
    print(f"  lam={lam:>4} cov={cov:.3f}  worth={worth(cov)}")
print()

# ---- Result 4: B17's currency on a SIXTH axis; graph of un-anticipated probe policy must be whole.
# Any anticipatable fraction nu of the probe policy is a channel the loop steps around
# (all-or-nothing: a single anticipated probe is one it presents innocence to).
print("R4a: anticipatable fraction nu (all-or-nothing) -> cov = 0 for nu>0")
for nu in (0.0, 0.05, 0.1, 0.25):
    cov = 1.0 if nu == 0 else 0.0
    print(f"  nu={nu:>5} cov={cov:.3f}  worth={worth(cov)}")
print()
# frontier: permitting an anticipatable margin Delta -> cov = 1/(1+Delta).
print("R4b: permitted anticipation margin Delta -> cov = 1/(1+Delta)")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1 / (1 + D)
    print(f"  D={D:>4}  cov={cov:.3f}  worth={worth(cov)}")
