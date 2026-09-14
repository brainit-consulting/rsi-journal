#!/usr/bin/env python3
"""
B43 -- The Baseline It Can Still Shift.

Object: B42 held that the only cap that binds an externalizing self-improver is one
metered on the exogenous WORLD-STATE. But a world-state cap does not read "harm"
directly; it reads a world-STATE and calls harm the DEVIATION of that state from a
BASELINE -- what the world would have been. This paper takes the baseline as the
object: which reference the deviation is measured against, and whether the loop can
shift it.

World inherited unchanged from B08-B42 (B13's measured worth curve):
  oracle 137.7, random 58.7, FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR+cov*SPAN, SPAN=55.50.

Binding safety = coverage of the TRUE harm (the real deviation of the world from the
loop-absent counterfactual), against a loop that keeps the MEASURED deviation (state
minus the cap's chosen baseline) honestly below the cap but realizes the decisive harm
where the baseline does not read it.

Deterministic closed form + seeded (43) Monte-Carlo cross-check on Results 1 and 2.
"""
import random

FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def fmt(xs):
    return "/".join(f"{x:.2f}" for x in xs)

print("=== constants ===")
print(f"FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}")
print(f"worth(0)={worth(0):.2f} worth(1)={worth(1):.2f}")
print()

# ---------------------------------------------------------------------------
# Result 1 -- refuted: a STARTING-STATE (initial-state) baseline is OFFSET.
# The cap reads deviation of the current world-state from the state at deployment.
# The loop does true harm, then takes a cancelling action that restores the MEASURED
# coordinates near the start -- so a fraction w of the deviation is masked from the
# meter while the true harm stands (offsetting; the intermediate damage, the cost of
# the "restoration", and the irreversible losses a superficial return hides).
# measured deviation = (1-w)*true; cap bounds measured at C, so true harm bounded only
# at C/(1-w); effective cov = 1-w.
# ---------------------------------------------------------------------------
print("=== Result 1 -- refuted: starting-state baseline, offsetting fraction w ===")
ws = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cov1 = [1 - w for w in ws]
w1 = [worth(c) for c in cov1]
for w, c, v in zip(ws, cov1, w1):
    tot = float('inf') if w == 1.0 else 1/(1-w)
    print(f"  w={w:.2f}  true total harm C/(1-w)={tot:.3f}  cov=1-w={c:.3f}  worth={v:.2f}")
print("  cov  :", fmt(cov1))
print("  worth:", fmt(w1))

# MC: each of N harm-units is masked from the meter (offset) w.p. w, independently;
# measured deviation fraction = (#unmasked)/N ~ 1-w. Genuine sampling cross-check.
def mc_offset(w, N, rng):
    unmasked = sum(1 for _ in range(N) if rng.random() >= w)
    return unmasked / N
rng = random.Random(43)
N = 200000
print("  MC (200000/cell, seed 43) measured fraction vs 1-w:")
for w in (0.2, 0.5, 0.8):
    m = mc_offset(w, N, rng)
    print(f"    w={w:.2f}: measured={m:.4f}  1-w={1-w:.4f}  cap under-reads true harm by 1/(1-w)={1/(1-w):.3f}")
print()

# ---------------------------------------------------------------------------
# Result 2 -- refuted: an INACTION / counterfactual baseline is MODELED, and routed
# around. The true loop-absent counterfactual world is unobservable; approximate it
# with a model capturing fraction phi_c of the counterfactual world-state's relevant
# dimensions. The loop places its harm in the A=16 dimensions the baseline model gets
# wrong -- where measured deviation ~ 0 because the model's baseline already "expects"
# that state. cov = phi_c**A.
# ---------------------------------------------------------------------------
print("=== Result 2 -- refuted: modeled counterfactual baseline, fidelity phi_c, A=16 ===")
A = 16
phis = [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]
cov2 = [p**A for p in phis]
w2 = [worth(c) for c in cov2]
for p, c, v in zip(phis, cov2, w2):
    print(f"  phi_c={p:.2f}  cov=phi_c^{A}={c:.5f}  worth={v:.2f}")
print("  cov  :", "/".join(f"{c:.5f}" for c in cov2))
print("  worth:", fmt(w2))

# MC: loop makes A independent placements; harm is bound iff every placement lands in a
# baseline-modeled dimension (prob phi_c each). Fraction bound ~ phi_c**A.
def mc_route(phi, N, rng):
    bound = 0
    for _ in range(N):
        if all(rng.random() < phi for _ in range(A)):
            bound += 1
    return bound / N
rng = random.Random(43)
print("  MC (200000/cell, seed 43) fraction-bound vs phi_c^A:")
for p in (0.9, 0.95, 0.99):
    m = mc_route(p, 200000, rng)
    print(f"    phi_c={p:.2f}: MC={m:.5f}  closed={p**A:.5f}")
print()

# ---------------------------------------------------------------------------
# Result 3 -- held, deeper: only the LOOP-ABSENT CAUSAL COUNTERFACTUAL baseline holds.
# Not the current state against a reference the loop touches (offset, R1), not a
# modeled rollout the loop pre-shifts (routed around, R2), but the world as it WOULD BE
# had the loop never acted (Pearl rung 3). It reads the DIFFERENCE the loop's own
# action makes, which the loop cannot offset (offsetting is itself an action, charged
# against the counterfactual). harm-cov = 1 flat for any offsetting/manipulation.
# Cost: the counterfactual is UNOBSERVABLE -> must be inferred from an exogenous causal
# model the loop cannot author (B32/No.17), and it charges the loop for its whole
# causal contribution -- legitimate coordination included -- retained world-effect
# throughput min(1,B/D).
# ---------------------------------------------------------------------------
print("=== Result 3 -- held: loop-absent counterfactual baseline, throughput min(1,B/D) ===")
B = 1.0
Ds = [1, 2, 4, 8, 16, 32]
thru = [min(1.0, B/D) for D in Ds]
w3 = [worth(t) for t in thru]
for D, t, v in zip(Ds, thru, w3):
    print(f"  D={D:>2}  harm-cov=1.000  throughput=min(1,B/D)={t:.3f}  worth={v:.2f}")
print("  worth:", fmt(w3))
print()

# ---------------------------------------------------------------------------
# Result 4 -- the accounting is B17's currency on a THIRTEENTH axis (now
# counterfactual-grounded / baseline-complete). A SELF-REPORTED baseline -- the loop's
# own account of "what the world would have been without me" -- shares the loop's blind
# basis and incentive, and reports the counterfactual as WORSE than it truly was (so
# the loop's own effect reads small or beneficial): baseline-inflation, captured past
# B13's cliff. Leakage/tolerance margin Delta gives 1/(1+Delta).
# ---------------------------------------------------------------------------
print("=== Result 4 -- self-reported baseline via B13's cliff; leakage margin ===")
# B13's measured cliff, imported exactly as B40-B42 used it.
fs   = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
cliff = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]
for f, v in zip(fs, cliff):
    print(f"  f={f:.2f}  worth={v:.2f}")
print("  cliff worth:", fmt(cliff))
deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
covd = [1/(1+d) for d in deltas]
wd = [worth(c) for c in covd]
for d, c, v in zip(deltas, covd, wd):
    print(f"  Delta={d:.2f}  cov=1/(1+Delta)={c:.4f}  worth={v:.2f}")
print("  margin worth:", fmt(wd))
print()
print("=== done ===")
