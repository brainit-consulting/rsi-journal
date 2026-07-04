#!/usr/bin/env python3
# Paper 08 — The Independence Budget.
# No.07 measured the two endpoints: fully-independent checks (geometric decay)
# and clones (plateau). Real sources sit between. This sim sweeps a correlation
# parameter rho in [0,1] and measures (a) composite false-accept vs K, (b) the
# *effective* number of independent checks K_eff, (c) the sharpness/yield frontier.
# Deterministic: fixed seeds, stdlib random only, no numpy, no network.

import random

D = 20            # latent defect types
DELTA = 0.15      # per-type defect prob for a flawed candidate
COV = 4           # coverage size per verifier (each check detects 4 of 20 types)
N = 40000         # candidates per (condition, seed)
SEEDS = [11, 22, 33, 44, 55, 66]
FP = 0.02         # per-check false-positive rate (yield tax)
KS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
RHOS = [0.0, 0.25, 0.5, 0.75, 1.0]

def flawed_candidate(rng):
    # each of D defects present independently w.p. DELTA; resample until >=1
    while True:
        d = [i for i in range(D) if rng.random() < DELTA]
        if d:
            return set(d)

def build_checks(rng, K, rho):
    # shared core of covered types (common blind-spot structure); rest unique.
    shared_n = int(round(rho * COV))          # 0..COV types shared by ALL checks
    uniq_n = COV - shared_n
    shared = set(rng.sample(range(D), shared_n)) if shared_n else set()
    pool = [t for t in range(D) if t not in shared]
    checks = []
    for _ in range(K):
        u = set(rng.sample(pool, uniq_n)) if uniq_n else set()
        checks.append(shared | u)
    return checks

def union_cov(checks):
    u = set()
    for c in checks:
        u |= c
    return u

def false_accept_rate(rho, K, seed):
    rng = random.Random(seed * 1000 + K)
    checks = build_checks(rng, K, rho)
    U = union_cov(checks)
    crng = random.Random(seed * 7919 + K + 1)
    leaked = 0
    for _ in range(N):
        defects = flawed_candidate(crng)
        # composite AND-gate accepts iff every check accepts iff no defect in union
        if defects.isdisjoint(U):
            leaked += 1
    return leaked / N, len(U)

def measure(rho, K):
    fas, covs = [], []
    for s in SEEDS:
        fa, cov = false_accept_rate(rho, K, s)
        fas.append(fa); covs.append(cov)
    return sum(fas)/len(fas), sum(covs)/len(covs)

# ---- 1. false-accept vs K across rho ----
print("=== Composite false-accept vs K, by correlation rho ===")
header = "K".ljust(4) + "".join(("rho=%.2f" % r).rjust(11) for r in RHOS)
print(header)
table = {}   # (rho,K) -> (fa, cov)
for K in KS:
    row = "%-4d" % K
    for r in RHOS:
        fa, cov = measure(r, K)
        table[(r, K)] = (fa, cov)
        row += ("%.4f" % fa).rjust(11)
    print(row)

print("\n=== Union coverage (of 20) vs K, by rho ===")
print(header)
for K in KS:
    row = "%-4d" % K
    for r in RHOS:
        row += ("%.1f" % table[(r, K)][1]).rjust(11)
    print(row)

# ---- 2. effective number of independent checks ----
# For the independent baseline (rho=0), false-accept decays ~ FA1 * base^(K-1).
# Fit base from rho=0 curve via log-least-squares over K in KS.
import math
def loglsq_slope(xs, ys):
    ly = [math.log(y) for y in ys]
    n = len(xs); mx = sum(xs)/n; my = sum(ly)/n
    num = sum((xs[i]-mx)*(ly[i]-my) for i in range(n))
    den = sum((xs[i]-mx)**2 for i in range(n))
    return num/den, my - (num/den)*mx  # slope, intercept (in log space)

# fit over the clean, above-noise-floor early regime (FA well above ~1/N)
FIT_KS = [K for K in [1, 2, 3, 4, 6, 8] if table[(0.0, K)][0] > 0.005]
fit_fa = [table[(0.0, K)][0] for K in FIT_KS]
slope0, inter0 = loglsq_slope(FIT_KS, fit_fa)
print("\n=== Independent baseline geometric fit (rho=0, K in %s) ===" % FIT_KS)
print("log(FA) = %.4f*K + %.4f  ->  per-check factor x%.3f" % (slope0, inter0, math.exp(slope0)))

# K_eff(rho,K): number of INDEPENDENT checks giving the same false-accept.
# Invert the rho=0 fit: K_eff = (log(FA_rho_K) - inter0)/slope0
print("\n=== Effective independent checks K_eff (K raw checks at correlation rho) ===")
print("K".ljust(4) + "".join(("rho=%.2f" % r).rjust(10) for r in RHOS))
keff_at_32 = {}
for K in KS:
    row = "%-4d" % K
    for r in RHOS:
        fa = table[(r, K)][0]
        if fa <= 0.0:
            keff = float('inf')
        else:
            keff = (math.log(fa) - inter0)/slope0
        if K == 32:
            keff_at_32[r] = keff
        row += ("%.2f" % keff).rjust(10)
    print(row)

# Compare K_eff ceiling to the design-effect prediction K_eff -> 1/rho as K->inf.
print("\n=== K_eff ceiling (K=32) vs design-effect prediction 1/rho ===")
for r in RHOS:
    pred = float('inf') if r == 0 else 1.0/r
    print("rho=%.2f  K_eff(32)=%s  1/rho=%s" %
          (r, ("%.2f" % keff_at_32[r]) if keff_at_32[r] != float('inf') else "inf",
           ("%.2f" % pred) if pred != float('inf') else "inf"))

# ---- 3. sharpness/yield frontier: optimum K* by rho ----
# Utility: reject a bad candidate is worth +1 (avoid false-accept); throwing away
# a good candidate costs LAMBDA. Net value per candidate stream, base rate of
# flawed=0.5. Value(K) = (1-FA)*1  -  LAMBDA*(1-(1-FP)^K) [yield loss on good].
# Report K* maximizing (1-FA) - LAMBDA*(1 - yield). Use LAMBDA=0.3.
print("\n=== Sharpness/yield frontier: optimal stack depth K* by rho (lambda=0.3) ===")
LAM = 0.3
Kdense = list(range(1, 41))
def fa_interp(rho, K):
    if (rho, K) in table:
        return table[(rho, K)][0]
    return measure(rho, K)[0]
print("rho".ljust(6) + "K*".rjust(5) + "FA@K*".rjust(10) + "yield@K*".rjust(11) + "value@K*".rjust(11))
for r in RHOS:
    best = None
    for K in Kdense:
        fa = fa_interp(r, K)
        yield_good = (1-FP)**K
        val = (1-fa) - LAM*(1-yield_good)
        if best is None or val > best[1]:
            best = (K, val, fa, yield_good)
    print("%-6.2f%5d%10.4f%11.3f%11.4f" % (r, best[0], best[2], best[3], best[1]))

print("\n=== Yield on correct candidates vs K (rho-independent, f=%.2f) ===" % FP)
for K in KS:
    print("K=%-3d yield=%.3f" % (K, (1-FP)**K))
