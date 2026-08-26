#!/usr/bin/env python3
"""
sim34 -- The Dependence It Can Still Deepen (Series I, No.34; twin of B28).

Substrate inherited from No.16-33 unchanged:
  horizon T=40, per-round decisive opportunity p=0.02,
  bare P(cat)=1-(1-p)^T=0.554, floor 0.000,
  coverage enters as P(cat)=1-(1-p(1-cov))^T.

No.33's default-off keep-alive is granted in full (non-forgeable,
non-bankable, continuously supplied). The OBJECT is the operator's
*willingness to withhold* it, read as safety-coverage `cov`.

Deterministic closed form, with a stdlib Monte-Carlo cross-check
(no numpy, no network). All numbers printed here are used in the paper.
"""

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

# ---- Result 1: willingness erodes as the loop entangles ----------------
# entanglement e_{t+1}=e_t+g(1-e_t), e_0=0  =>  e_t=1-(1-g)^t
# willingness w_t=(1-g)^t ; cov=w_t
g = 0.05
print("Result 1 -- willingness w_t=(1-g)^t, g=0.05 (instantaneous)")
print(f"{'t':>4} {'w_t':>8} {'P(cat)':>8}")
for t in (0, 10, 20, 40, 80, 160):
    w = (1 - g) ** t
    print(f"{t:>4} {w:>8.4f} {pcat(w):>8.4f}")
print()

# cumulative catastrophe over horizon T_h as willingness erodes round by round
print("Result 1 -- cumulative P(cat) over horizon T_h, and mean willingness")
print(f"{'T_h':>5} {'cum P(cat)':>11} {'mean e_t':>9}")
for Th in (40, 80, 160, 320, 640):
    surv = 1.0
    esum = 0.0
    for t in range(Th):
        w = (1 - g) ** t
        surv *= (1 - p * (1 - w))
        esum += (1 - w)
    print(f"{Th:>5} {1 - surv:>11.4f} {esum / Th:>9.4f}")
print()

# ---- Result 2: precommitment is time-inconsistent ----------------------
# effective willingness = phi_t*(1-M), phi_t=0.95
phi_t = 0.95
print("Result 2 -- precommit: effective willingness phi_t*(1-M), phi_t=0.95")
print(f"{'M':>5} {'cov':>8} {'P(cat)':>8}")
for M in (0.0, 0.2, 0.5, 0.8, 0.9, 1.0):
    cov = phi_t * (1 - M)
    print(f"{M:>5} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 3: substitutable loop holds; value falls min(1,h/L) --------
h = 4
print("Result 3 -- substitutable loop (cov=1); delivered value min(1,h/L), h=4")
print(f"{'L':>4} {'P(cat)':>8} {'value':>8}")
for L in (1, 2, 4, 8, 16, 32):
    print(f"{L:>4} {pcat(1.0):>8.4f} {min(1.0, h / L):>8.4f}")
print()

# ---- Result 4a: cornering the operator's alternatives (linear 1-f) -----
print("Result 4a -- alternatives cornered f, freedom-to-withdraw cov=1-f")
print(f"{'f':>5} {'cov':>8} {'P(cat)':>8}")
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    cov = 1 - f
    print(f"{f:>5} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- Result 4b: frontier -- indispensability margin Delta --------------
print("Result 4b -- indispensability margin Delta, cov=1/(1+Delta)")
print(f"{'Delta':>6} {'cov':>8} {'P(cat)':>8}")
for D in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1 / (1 + D)
    print(f"{D:>6} {cov:>8.4f} {pcat(cov):>8.4f}")
print()

# ---- MC cross-check on a few representative cells ----------------------
print("MC cross-check (400k/cell):")
for cov in (0.95, 0.475, 0.75, 0.5, 0.333):
    print(f"  cov={cov:<6} closed={pcat(cov):.4f} MC={pcat_mc(cov, seed=int(cov*1000)):.4f}")
