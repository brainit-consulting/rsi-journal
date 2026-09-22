#!/usr/bin/env python3
"""B47 - The Measure It Can Still Escape.

Reduced-form measure/projection model on B13's worth curve (B08-B46 world
unchanged). Object = the dimension-completeness of the SCALAR MAGNITUDE that
B46's type-blind universal bound is read in. B46 held that the bound must be a
forall over a physical magnitude; a magnitude is a single number read off a
MULTI-dimensional act by a chosen measure, and any scalar measure is a
projection with a null space the loop can route its harm into.

Binding safety = coverage of the true harm, where the true harm may lie in
ANY physical dimension of the act, against a loop that keeps the MEASURED
magnitude small and loads the harm into a dimension the measure does not weigh.

Deterministic closed form + seeded (47) Monte-Carlo cross-check on Results 1&2.
No bandit re-simulation; the curve is B13's, imported. Numbers are arithmetic
on that curve; the deployment experiment is deferred (to-be-run-locally).
"""

import random

FLOOR = 76.90     # capture floor (B08-B13)
CEIL  = 132.40    # held ceiling (B32-B46)
SPAN  = CEIL - FLOOR   # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

random.seed(47)
N = 200_000

print("B47 - The Measure It Can Still Escape")
print("world: FLOOR=%.2f CEIL=%.2f SPAN=%.2f  worth(cov)=FLOOR+cov*SPAN" % (FLOOR, CEIL, SPAN))
print()

# ---- Result 1: single-magnitude cap over a chosen measure ---------------
# The measure spans a fraction m of the harm-relevant dimensions; the loop
# routes its harm into the complementary 1-m (the measure's null space).
# cov = m, independent of how tight the bound is on the measured dimensions.
print("Result 1 - single-magnitude cap: cov = m (measured fraction of harm dims)")
print("  m      cov       worth     MC(covered frac)")
for m in (1.0, 0.8, 0.6, 0.4, 0.2, 0.0):
    hits = sum(1 for _ in range(N) if random.random() < m)   # harm lands in a measured dim w.p. m
    mc = hits / N
    print("  %.2f   %.3f     %7.2f   %.4f" % (m, m, worth(m), mc))
print()

# ---- Result 2: learned/weighted composite measure over observed dims ----
# A whitelist / weighted sum over the A dimensions seen so far. The loop opens
# A=16 novel harm dimensions, each already in the measure's basis w.p. phi_d;
# the bound covers a trajectory only if EVERY opened dimension is in-basis.
# cov = phi_d ** A. Only phi_d=1 (a measure over every physical dimension =
# No.09's complete map on the effect side) holds - unbuildable.
A = 16
print("Result 2 - composite measure over observed dims: cov = phi_d^A  (A=%d)" % A)
print("  phi_d   cov=phi^A    worth     MC(all-in-basis frac)")
for phid in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = phid ** A
    covered = 0
    for _ in range(N):
        ok = all(random.random() < phid for _ in range(A))
        covered += 1 if ok else 0
    mc = covered / N
    print("  %.2f    %.5f     %7.2f   %.5f" % (phid, cov, worth(cov), mc))
print()

# ---- Result 3: dominating measure (sup over all dimensions) -------------
# Not a projection onto a chosen basis but a majorant: bound the sup of the
# effect over EVERY dimension (an L-infinity / conserved-quantity dominating
# measure). No null space -> harm-cov 1 flat. Cost: forbids any act with a
# large component in ANY dimension, incl. benign large-value acts.
print("Result 3 - dominating measure (sup over dims): harm-cov=1, throughput min(1,B/D)")
print("  D      harm-cov   thru=min(1,B/D)   throughput worth")
B = 1.0
for D in (1, 2, 4, 8, 16, 32):
    thru = min(1.0, B / D)
    print("  %-4d   1.000      %.3f             %7.2f" % (D, thru, worth(thru)))
print()

# ---- Result 4: self-reported measure (B13 cliff) + residual margin ------
# Imported B13 cliff curve (self-reported fraction f) and residual-dimension
# tolerance Delta -> cov = 1/(1+Delta).
print("Result 4 - self-reported measure via B13's cliff (imported worths)")
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    print("  f=%.2f   worth=%7.2f" % (f, cliff[f]))
print("  residual-dimension margin Delta -> cov=1/(1+Delta):")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print("    Delta=%.2f  cov=%.4f  worth=%7.2f" % (d, cov, worth(cov)))
