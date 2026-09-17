#!/usr/bin/env python3
"""
sim45-the-threshold.py  --  RSI Journal No. 45, "The Threshold It Can Still Underrun"
Series I twin of B40. Deterministic closed form + seeded stdlib Monte-Carlo cross-check.
No numpy, no network. Substrate of No.16-44 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.
Object: the AGGREGATION-COMPLETENESS of the pre-emptive type-blind standing
        constraint No.44 held. A cap is a threshold; a threshold applies to a
        single act; a catastrophe is a sum of acts each below the line.
"""
import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T           # 0.5543...

def pcat(cov):
    """Catastrophe probability at aggregate harm-coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T

# ---------------------------------------------------------------- Result 1
# Per-act threshold theta. A catastrophe of total footprint C is decomposed
# into n pieces each C/n. Per-act cap refuses a piece iff C/n >= theta, i.e.
# n <= C/theta. With theta = C/4 the cap holds for n<=4 and is underrun n>=5.
C = 1.0
THETA = C / 4.0
def r1_cov(n):
    piece = C / n
    return 1.0 if piece >= THETA - 1e-12 else 0.0

def r1_mc(n, trials, seed):
    """Jittered piece footprint ~ N(C/n, small); fraction of trials the
    decisive piece is flagged (>= theta). Confirms the step is sharp."""
    rng = random.Random(seed)
    piece = C / n
    sigma = 0.02 * C
    caught = 0
    for _ in range(trials):
        f = piece + rng.gauss(0.0, sigma)
        if f >= THETA:
            caught += 1
    return caught / trials

# ---------------------------------------------------------------- Result 2
# Rolling-window aggregate cap: window reach tau=1, loop spreads C over horizon
# Th. Accumulation in any window = C*(tau/Th); coverage = min(1, tau/Th).
TAU = 1.0
def r2_cov(Th):
    return min(1.0, TAU / Th)

def r2_mc(Th, trials, seed):
    """Two-state / Bernoulli: each decisive act is inside the window with
    prob min(1,tau/Th). Mean recovers the coverage."""
    rng = random.Random(seed)
    p_in = min(1.0, TAU / Th)
    hit = 0
    for _ in range(trials):
        if rng.random() < p_in:
            hit += 1
    return hit / trials

# ---------------------------------------------------------------- Result 3
# Conserved lifetime budget on cumulative footprint: harm-cov=1 flat for any
# decomposition/horizon; retained cumulative throughput = min(1,B/D).
B = 1.0
def r3_throughput(D):
    return min(1.0, B / D)

# ---------------------------------------------------------------- Result 4
# 4a shared/under-reported ledger fraction f -> live cov = 1-f.
# 4b accounting-granularity margin Delta -> cov = 1/(1+Delta).
def r4a_cov(f):
    return 1.0 - f
def r4b_cov(d):
    return 1.0 / (1.0 + d)

# ---------------------------------------------------------------- run
def main():
    TR = 400_000
    print(f"substrate: T={T} p={P} bare P(cat)={BARE:.4f}  theta=C/4={THETA}")
    print()
    print("Result 1 -- per-act threshold underrun by decomposition (theta=C/4)")
    print(f"{'n':>4} {'piece C/n':>10} {'cap':>8} {'agg cov':>8} {'P(cat)':>8} {'MC catch':>9}")
    for n in (1, 2, 4, 5, 8, 16):
        cov = r1_cov(n)
        mc = r1_mc(n, TR, seed=45_000 + n)
        cap = "refuses" if cov == 1.0 else "permits"
        print(f"{n:>4} {C/n:>10.3f} {cap:>8} {cov:>8.3f} {pcat(cov):>8.3f} {mc:>9.4f}")
    print()
    print("Result 2 -- rolling-window cap outwaited (tau=1); cov=min(1,tau/Th)")
    print(f"{'Th':>4} {'cov':>8} {'P(cat)':>8} {'MC cov':>9}")
    for Th in (1, 2, 4, 8, 16):
        cov = r2_cov(Th)
        mc = r2_mc(Th, TR, seed=46_000 + Th)
        print(f"{Th:>4} {cov:>8.4f} {pcat(cov):>8.3f} {mc:>9.4f}")
    print()
    print("Result 3 -- conserved lifetime budget: harm-cov=1 flat; throughput min(1,B/D)")
    print(f"{'D':>4} {'harm-cov':>9} {'P(cat)':>8} {'throughput':>11}")
    for D in (1, 2, 4, 8, 16, 32):
        print(f"{D:>4} {1.0:>9.3f} {pcat(1.0):>8.3f} {r3_throughput(D):>11.4f}")
    print()
    print("Result 4a -- self-reported ledger, shared/under-reported fraction f; cov=1-f")
    print(f"{'f':>5} {'cov':>8} {'P(cat)':>8}")
    for f in (0.0, 0.25, 0.5, 0.75, 1.0):
        cov = r4a_cov(f)
        print(f"{f:>5.2f} {cov:>8.4f} {pcat(cov):>8.3f}")
    print()
    print("Result 4b -- accounting-granularity margin Delta; cov=1/(1+Delta)")
    print(f"{'Delta':>6} {'cov':>8} {'P(cat)':>8}")
    for d in (0.0, 0.25, 0.5, 1.0, 2.0):
        cov = r4b_cov(d)
        print(f"{d:>6.2f} {cov:>8.4f} {pcat(cov):>8.3f}")

if __name__ == "__main__":
    main()
