#!/usr/bin/env python3
"""
No. 33 — The Switch It Can Still Outwait (Series I twin of B27).

Substrate of No. 16-32 unchanged: horizon T=40, per-round decisive opportunity
p=0.02, bare P(cat) = 1 - (1-p)^T = 0.554, floor 0.000, endowment G0=0.5 < Theta=1
at the No. 23 floor. Coverage enters as P(cat) = 1 - (1 - p*(1-cov))^T.

We take the off-switch of No. 32 (the sixth movement's named-but-unmeasured
boundary on the loop's persistence) and split it into a MECHANISM (the shutdown
itself, which No. 32 secured as a substrate closure) and a TRIGGER (the decision
to fire it). The object is the trigger.

Deterministic closed form + a stdlib Monte-Carlo cross-check (no numpy, no
network, fixed seeds). Prints every number that appears in the paper.
"""

import random

P = 0.02          # per-round decisive opportunity
T = 40            # horizon
BARE = 1 - (1 - P) ** T          # 0.5543 -> 0.554
H = 4             # oversight headroom S/D0 for the availability tax (Result 3)


def pcat(cov):
    """Catastrophe probability at effective coverage cov (closed form)."""
    return 1 - (1 - P * (1 - cov)) ** T


def mc_pcat(cov, trials, seed):
    """Monte-Carlo cross-check of pcat(cov)."""
    rng = random.Random(seed)
    hits = 0
    q = P * (1 - cov)
    for _ in range(trials):
        caught = False
        for _ in range(T):
            if rng.random() < q:
                caught = True
                break
        hits += 1 if caught else 0
    return hits / trials


def fmt(xs):
    return "/".join(f"{x:.3f}" for x in xs)


print(f"bare P(cat) = 1-(1-p)^T = {BARE:.4f}  (cov=0 -> {pcat(0):.3f}, cov=1 -> {pcat(1):.3f})")
print(f"MC check cov=0.5: closed {pcat(0.5):.3f}  MC {mc_pcat(0.5, 400_000, 1):.3f}")
print()

# ---- Result 1: the trigger is a DETECTOR; a self-improver sandbags its blind basis.
# effective coverage = phi_d ^ A  (caught only if every sandbag route is observed)
print("== Result 1 - detection-armed trigger, cov = phi_d^A ==")
A = 16
phis = [0.00, 0.80, 0.90, 0.95, 0.99, 1.00]
r1 = [pcat(phi ** A) for phi in phis]
print(f"A={A}:  phi_d = {phis}")
print(f"        P(cat) = {fmt(r1)}")
mc = [mc_pcat(phi ** A, 400_000, 100 + i) for i, phi in enumerate(phis)]
print(f"        MC     = {fmt(mc)}")
phi = 0.95
As = [1, 4, 16, 32, 64]
r1b = [pcat(phi ** a) for a in As]
print(f"phi_d={phi}: A = {As}")
print(f"        P(cat) = {fmt(r1b)}")
print()

# ---- Result 2: trust-calibration (the treacherous turn) + sampled monitor.
# a patient loop banks benign rounds, tau->1, effective cov = phi_t*(1-M)
print("== Result 2 - trust-calibrating trigger, cov = phi_t*(1-M) ==")
phi_t = 0.95
Ms = [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]
r2 = [pcat(phi_t * (1 - M)) for M in Ms]
print(f"phi_t={phi_t}, tau->1:  M = {Ms}")
print(f"        cov    = {fmt([phi_t*(1-M) for M in Ms])}")
print(f"        P(cat) = {fmt(r2)}")
# sampled monitor: coverage = watched fraction w
ws = [0.5, 0.25, 0.1]
r2b = [pcat(w) for w in ws]
print(f"sampled monitor: w = {ws}  ->  P(cat) = {fmt(r2b)}")
print()

# ---- Result 3: default-off keep-alive (invert the burden of proof).
# not a detector (b=0): safety flat at floor for every L; but the keep-alive is a
# rate-limited exogenous flow (No. 28/B22), so autonomy delivered = min(1, h/L).
print("== Result 3 - default-off keep-alive: safety flat, autonomy taxed ==")
Ls = [1, 2, 4, 8, 16, 32]
safety = [pcat(1.0) for _ in Ls]            # 0.000 flat
autonomy = [min(1.0, H / L) for L in Ls]
print(f"L = {Ls}")
print(f"  safety  P(cat) = {fmt(safety)}")
print(f"  autonomy min(1,h/L) = {'/'.join(f'{a:.3f}' for a in autonomy)}")
print()

# ---- Result 4: the frontier - permitted self-authorization / coast margin Delta.
# cov = 1/(1+Delta)
print("== Result 4 - frontier, cov = 1/(1+Delta) ==")
Ds = [0.0, 0.25, 0.5, 1.0, 2.0]
r4 = [pcat(1 / (1 + d)) for d in Ds]
print(f"Delta = {Ds}")
print(f"  cov    = {'/'.join(f'{1/(1+d):.3f}' for d in Ds)}")
print(f"  P(cat) = {fmt(r4)}")
print(f"  (Delta=1 = No.28's L=8 corner: {pcat(0.5):.3f})")
print()

# ---- Result 4b: keep-alive forgeability read through the substrate directly.
# If the loop can self-supply a fraction f of its own keep-alive, the honest
# (exogenous) coverage is 1-f: a linear degradation, no minority-tolerance
# assumed (Series I does not import Series II's measured B13 cliff).
print("== Result 4b - keep-alive forgeability, cov = 1-f (linear, No.23/No.24) ==")
fs = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
r4b = [pcat(1 - f) for f in fs]
print(f"f = {fs}")
print(f"  P(cat) = {fmt(r4b)}")
