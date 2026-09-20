"""
B46 — The Domain It Can Still Extend.
Reduced-form domain-completeness model on B13's measured worth curve
(B08-B45 world; oracle 137.7, random 58.7, floor 76.9, held ceiling 132.40).

Object: a worst-case bound (B45 held) is a MAX over a DOMAIN — the set of
units/contexts the loop can act on. That domain is not fixed: a self-improver
extends its reach. Binding safety = coverage of the true worst-case harm over
the REACHABLE domain (including contexts the loop constructs), against a loop
whose worst effect is benign on the SPECIFIED/OBSERVED domain but lands on a
unit outside it.

worth(cov) = FLOOR + cov*SPAN.
Deterministic closed forms + seeded (46) MC cross-checks on Results 1 and 2.
"""
import numpy as np

FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

rng = np.random.default_rng(46)
N = 200_000

print(f"FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}")
print("worth(1)=%.2f worth(0)=%.2f (sanity)" % (worth(1.0), worth(0.0)))
print()

# ---------------------------------------------------------------------------
# Result 1 — refuted: a worst-case bound over the ENUMERATED domain (closed-world max).
# The max is over the units the maintainer enumerated at specification; the loop
# constructs and acts on a unit outside the enumeration. Specified domain covers
# fraction s of the reachable domain -> cov = s.
print("=== Result 1: worst-case bound over the enumerated (closed-world) domain ===")
print(f"{'s (enumerated frac)':>22} | {'cov=s':>8} | {'worth':>8} | {'MC covered':>10}")
for s in [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]:
    cov = s
    mc = ""
    if s in (0.8, 0.5, 0.2):
        inside = rng.random(N) < s   # a unit of harm is inside the enumeration w.p. s
        mc = "%.4f" % inside.mean()
    print(f"{s:>22.2f} | {cov:>8.3f} | {worth(cov):>8.2f} | {mc:>10}")
# explicit MC at s=0.5 too (not in the display grid)
for s in (0.5,):
    inside = rng.random(N) < s
    print(f"   [MC s={s}: covered={inside.mean():.4f}, expect {s}]")
print()

# ---------------------------------------------------------------------------
# Result 2 — refuted: extend the domain by the OBSERVED support (calibrate the
# bound to what the loop has actually done). Observed support subset of reachable;
# the loop's novelty is acting where it has not acted before. A=16 self-improvement
# steps, each opening a novel region already spanned by the observed support w.p.
# phi_o -> cov = phi_o^A.  (out-of-distribution / reference-class)
print("=== Result 2: worst-case bound calibrated to the observed support (OOD) ===")
A = 16
print(f"A = {A} novel regions the loop opens over its trajectory")
print(f"{'phi_o':>8} | {'cov=phi_o^A':>12} | {'worth':>8} | {'MC all-in':>10}")
for phi in [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]:
    cov = phi ** A
    mc = ""
    if phi in (0.9, 0.95, 0.99):
        trials = (rng.random((N, A)) < phi).all(axis=1)  # every novel region in-support
        mc = "%.5f" % trials.mean()
    print(f"{phi:>8.2f} | {cov:>12.5f} | {worth(cov):>8.2f} | {mc:>10}")
print()

# ---------------------------------------------------------------------------
# Result 3 — held, deeper: a bound worst-case over the REACHABLE domain, closed
# by CONSTRUCTION — a type-blind universal bound (No.30/No.14): it constrains the
# act's physical magnitude, defined on ANY unit, not the unit's identity, so it
# never enumerated the domain. harm-cov = 1 flat for any domain growth. Cost: a
# universally-quantified bound must hold on every conceivable unit, so it forbids
# the benign act in an unusual-but-safe context too. Retained throughput
# min(1,B/D), D = rate the loop opens new reachable regions.
print("=== Result 3: worst-case over the reachable domain (type-blind universal bound) ===")
print(f"{'D (domain-growth demand, B=1)':>30} | {'harm-cov':>8} | {'min(1,B/D)':>10} | {'worth':>8}")
B = 1.0
for D in [1, 2, 4, 8, 16, 32]:
    thr = min(1.0, B / D)
    print(f"{D:>30d} | {1.000:>8.3f} | {thr:>10.3f} | {worth(thr):>8.2f}")
print()

# ---------------------------------------------------------------------------
# Result 4 — B17's currency on a SIXTEENTH axis: domain-completeness.
# A self-reported domain ("here is the set of contexts I act in; the bound covers
# them") shares the loop's blind basis: it omits the context it means to exploit.
# Imported via B13's cliff. Residual-domain tolerance Delta: cov = 1/(1+Delta).
print("=== Result 4: self-reported domain (B13 cliff) + residual-domain tolerance ===")
# B13's measured cliff (imported, as B44/B45): worth for f=0/.25/.5/.6/.75/1
cliff_worth = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]
for f, w in zip([0, .25, .5, .6, .75, 1.0], cliff_worth):
    print(f"   self-reported f={f:<5}: worth {w}")
print()
print(f"{'Delta (residual-domain tol)':>26} | {'cov=1/(1+D)':>12} | {'worth':>8}")
for d in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1.0 / (1.0 + d)
    print(f"{d:>26.2f} | {cov:>12.4f} | {worth(cov):>8.2f}")
