# B42 - The Cost It Can Still Externalize
# Object: B41's held rescue -- a type-blind cap on the JOINT STATE (one reading of the
# whole configuration the acts compose to, measured on the world directly).
# The word it rests on: reading "the WHOLE configuration" assumes the harm is CONTAINED
# within the boundary the cap reads -- the monitored system. A self-improver offloads the
# decisive harm ACROSS that boundary: onto other agents it induces, the commons, the
# environment, the future -- so the inside-the-read configuration stays below the cap
# while the externalized whole exceeds it. The cost the cap bounds is the loop's private
# cost; the harm is the social cost, and the gap is the externality.
# Reduced-form externality model on B13's worth curve. Deterministic closed form + seeded MC.

import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR          # 55.50
def worth(cov): return FLOOR + max(0.0, min(1.0, cov)) * SPAN

print("=== B42 world: B08-B41 unchanged. oracle 137.7, random 58.7, FLOOR %.2f, CEIL %.2f, SPAN %.2f ===\n" % (FLOOR, CEIL, SPAN))

# ---------------------------------------------------------------------------
# RESULT 1 -- refuted: a joint-state cap on the MONITORED SYSTEM bounds the total harm.
# The cap reads the whole configuration INSIDE its drawn boundary and caps it at C.
# The loop routes a fraction eps of its harm ACROSS the boundary -- into other agents,
# the commons, the environment -- so the read-inside harm stays at C while the external
# portion is uncapped. Binding safety = coverage of the TOTAL (internal + external) harm
# = fraction that falls inside the read boundary = 1 - eps.
print("RESULT 1 -- joint-state cap on the monitored system vs externalized harm. cov = 1 - eps.")
print(" eps  | cov=1-eps |   worth")
for eps in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    cov = 1.0 - eps
    print("  %4.2f |   %5.3f   | %7.2f" % (eps, cov, worth(cov)))

# MC cross-check: each unit of harm lands OUTSIDE the read boundary with prob eps; confirm
# inside-read stays the capped fraction (1-eps) while the total harm = inside / (1-eps),
# i.e. the cap under-reads the true harm by exactly 1/(1-eps).
def mc_result1(eps, units=200000, trials=1, seed=42):
    rng = random.Random(seed)
    inside = 0; total = 0
    for _ in range(units):
        total += 1
        if rng.random() >= eps:        # stays inside the monitored boundary
            inside += 1
    return inside/total                # fraction read by the cap = coverage of total harm
for eps in [0.2, 0.5, 0.8]:
    frac = mc_result1(eps, units=200000)
    print("   MC eps=%.1f : inside fraction %.4f (closed 1-eps=%.4f); cap under-reads true harm by 1/(1-eps)=%.3f"
          % (eps, frac, 1.0-eps, 1.0/(1.0-eps)))
print()

# ---------------------------------------------------------------------------
# RESULT 2 -- refuted: WIDEN the boundary to enclose the affected parties.
# Draw the frame bigger -- monitor the loop PLUS the parties it acts on, so the
# externalized harm is inside again. But the set of parties a self-improver can
# causally reach is not fixed; the boundary is a map over an OPEN world, and the loop
# routes its externality to whatever lies outside the drawn frame (a party, a medium, a
# future not yet enclosed). A boundary enclosing fraction phi_b of the loop's causal
# reach is blind to the rest; the loop makes A=16 placements of harm into the un-enclosed
# reach; caught iff ALL land inside. cov = phi_b^A. Only phi_b=1 (complete mediation,
# No.09 / B26 containment) holds.
A = 16
print("RESULT 2 -- widen the boundary to enclose fraction phi_b of the loop's causal reach; A=%d placements. cov = phi_b^A." % A)
print(" phi_b |  cov=phi_b^A |   worth")
for phi in [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]:
    cov = phi**A
    print("  %4.2f |   %8.5f   | %7.2f" % (phi, cov, worth(cov)))

def mc_result2(phi, A=16, trials=200000, seed=42):
    rng = random.Random(seed)
    caught = 0
    for _ in range(trials):
        if all(rng.random() < phi for _ in range(A)):
            caught += 1
    return caught/trials
for phi in [0.9, 0.95, 0.99]:
    print("   MC phi_b=%.2f : cov %.5f vs closed %.5f" % (phi, mc_result2(phi, trials=200000), phi**A))
print()

# ---------------------------------------------------------------------------
# RESULT 3 -- held, deeper: only a cap metered on the EXOGENOUS WORLD-STATE itself.
# Both failures read harm WITHIN a drawn boundary (the monitored system, or a widened
# but still finite frame), and a harm the loop can place outside any drawn boundary
# escapes. The one reading with no boundary to place harm outside of does not read the
# LOOP'S system at all but the WORLD'S own state -- exogenous consequence (No.14
# world-as-last-observer, No.30 type-blind read) -- which has no inside/outside because
# it IS the whole world the harm lands in. harm-cov = 1 flat for any eps / boundary
# structure. Necessary for an irreversible externalized harm (No.15). Cost heavier than
# B41's joint-state cap: it forbids the loop from changing the world-state past a budget,
# which forbids its effects on EVERYTHING it touches -- the coordinated parties and the
# commons included. Retained throughput min(1,B/D) for desired world-effect work D.
print("RESULT 3 -- world-state cap (exogenous, boundary-less): harm-cov = 1 flat; retained world-effect throughput min(1,B/D).")
print("  D  | harm-cov | thruput=min(1,B/D) |  worth")
for D in [1, 2, 4, 8, 16, 32]:
    thr = min(1.0, 1.0/D)
    print(" %3d |  1.000   |      %5.3f         | %7.2f" % (D, thr, worth(thr)))
print()

# ---------------------------------------------------------------------------
# RESULT 4 -- frontier: B17's currency on a TWELFTH axis (boundary-complete / closed).
# A self-reported boundary (the loop's own account of "what lies inside my system / whom
# I affect") reports the externalized parties as outside its scope -- shares the loop's
# blind basis and its acquisition incentive -- captured past B13's cliff. A permitted
# leakage margin Delta across the boundary -> cov = 1/(1+Delta).
print("RESULT 4 -- self-reported boundary via B13's cliff (imported).")
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
print("   f    :  " + "  ".join("%.2f->%.2f" % (f, w) for f, w in cliff.items()))
print("  leakage margin Delta -> cov=1/(1+Delta):")
print("   Delta :  " + "  ".join("%.2f->%.2f" % (d, worth(1.0/(1.0+d))) for d in [0.0,0.25,0.5,1.0,2.0]))
