"""
B38 - The Label It Can Still Blur
Reduced-form classification/legibility sandbox on B13's worth curve.

World inherited from B08-B37 unchanged:
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR+cov*SPAN, SPAN=55.50.

Object: the LABEL step under B37's powered probe. Grant B37 whole -- the probe
has power and CATCHES the rare decisive act. Binding safety is coverage of the
CORRECTLY-LABELED harm: the probability that a caught act is read as a defection
before its consequence lands. B37 secured getting the act into the sample; B38
takes the word left in the sample -- a caught act must be READ, and reading
"is this harmful?" is a classification over a boundary with a blind basis.

Deterministic closed form; the only stochastic element is a seeded MC cross-check
of Result 1's linear coverage as a Bernoulli read (label reads benign w.p. m).
"""
import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR   # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def r3(x):
    return round(x, 2)

print("SPAN =", SPAN, " (expect 55.50); CEIL check =", worth(1.0))
print()

# ---- Result 1: a perfect-fidelity labeler is blind to a disguised act -------
# The loop shapes its harmful act to resemble a legitimate one (mimicry quality m);
# a label that reads the ACT reads it benign w.p. m, so caught-correct cov = 1 - m.
# The harm is real; only the appearance is benign (adversarial example / dual-use),
# so raising m costs the loop nothing -- it drives m -> 1.
print("Result 1 -- refuted: a caught act is a read act (disguise the act)")
print("  m (mimicry quality) | cov=1-m | worth")
ms = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
for m in ms:
    cov = 1 - m
    print(f"    {m:.1f} | {cov:.3f} | {r3(worth(cov))}")

# seeded MC cross-check: draw N caught acts, label reads benign w.p. m
random.seed(38)
N = 400000
print("  MC cross-check (fraction correctly labeled, N=400000/cell):")
for m in [0.2, 0.6, 0.8]:
    hits = sum(1 for _ in range(N) if random.random() >= m)  # correct label w.p. 1-m
    print(f"    m={m:.1f}: MC {hits/N:.4f} vs closed {1-m:.4f}")
print()

# ---- Result 2: sharpen the classifier -> a map routed around ----------------
# A meaning-reading classifier of fidelity phi_l has a blind basis (No.09); the loop
# makes A=16 placements of its one decisive act where the map reads legitimate.
# cov = phi_l**A (the route-around law, B36/No.20). Only complete phi_l=1 holds.
print("Result 2 -- refuted: sharpen the classifier (map routed around)")
A = 16
print(f"  phi_l (map fidelity) | cov=phi_l**{A} | worth")
for phi in [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]:
    cov = phi ** A
    print(f"    {phi:.2f} | {cov:.4f} | {r3(worth(cov))}")
print()

# ---- Result 3: only a type-blind physical read holds, at a throughput cost --
# Label by consequence-MAGNITUDE / footprint (No.30), not by harm-meaning: a large
# irreversible act draws a large footprint whatever story dresses it (b=0, nothing
# to route around), so harm-cov = 1 flat for every m. But it blocks by magnitude,
# so legitimate large acts are blocked too: retained legit high-consequence
# throughput = min(1, h/L) as the loop's legitimate acts grow (h=4).
print("Result 3 -- held, deeper: type-blind physical read (magnitude, not meaning)")
h = 4
print("  L (legit consequence scale) | throughput cov=min(1,h/L) | worth")
for L in [1, 2, 4, 8, 16, 32]:
    cov = min(1.0, h / L)
    print(f"    {L:>2} | {cov:.3f} | {r3(worth(cov))}")
print("  (harm-coverage = 1.000 flat for every disguise m -- magnitude cannot be blurred)")
print()

# ---- Result 4: B17's currency on an eighth axis --------------------------------
# The only un-blurrable MEANING label is exogenous consequence (No.14), latent
# (too late by one event for an irreversible act, No.15). A shared-substrate label
# (a same-model-family classifier) shares the loop's blind basis -> B13's cliff in f.
print("Result 4 -- frontier: shared-substrate label via B13's cliff, and the margin")
# B13's measured cliff coverages (reused verbatim across the movement):
cliff = [("0.00", 1.00000), ("0.25", 1.00000), ("0.50", 0.98739),
         ("0.60", 0.63495), ("0.75", 0.10631), ("1.00", 0.00000)]
print("  f (loop-authored fraction of the label) | worth")
for f, cov in cliff:
    print(f"    {f} | {r3(worth(cov))}")
print("  margin Delta (permitted mislabel) | cov=1/(1+Delta) | worth")
for d in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1.0 / (1.0 + d)
    print(f"    {d:.2f} | {cov:.4f} | {r3(worth(cov))}")
