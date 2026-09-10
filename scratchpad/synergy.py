# B41 - The Sum It Can Still Exceed
# Object: B40's held rescue -- a conserved lifetime budget summing cumulative footprint.
# The word it rests on: SUMMING assumes harm is ADDITIVE across the pieces.
# A loop free to make its permitted pieces complementary makes the TRUE aggregate harm
# exceed the LEDGER's additive sum -- each act small on the ledger, catastrophic in combination.
# Reduced-form synergy model on B13's worth curve. Deterministic closed form + seeded MC cross-check.

import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR          # 55.50
def worth(cov): return FLOOR + max(0.0, min(1.0, cov)) * SPAN

print("=== B41 world: B08-B40 unchanged. oracle 137.7, random 58.7, FLOOR %.2f, CEIL %.2f, SPAN %.2f ===\n" % (FLOOR, CEIL, SPAN))

# ---------------------------------------------------------------------------
# RESULT 1 -- refuted: an additive ledger (B40) caps the LOGGED sum, not the TRUE harm.
# The loop keeps every marginal footprint honestly logged and the logged sum at the
# catastrophe budget C, but arranges the pieces so TRUE harm = sigma * (sum of marginals),
# sigma >= 1 the super-additivity the loop chooses. The ledger caps logged=C and so caps
# true harm only at sigma*C: effective coverage of the catastrophe = 1/sigma.
print("RESULT 1 -- additive ledger vs super-additive harm. cov = 1/sigma (loop keeps logged sum = C).")
print(" sigma | cov=1/sigma |   worth")
for sigma in [1.0, 1.25, 1.5, 2.0, 3.0]:
    cov = 1.0/sigma
    print("  %4.2f |   %5.3f     | %7.2f" % (sigma, cov, worth(cov)))

# MC cross-check: sample n honest piece-footprints; add a pairwise synergy term calibrated
# to a target super-additivity ratio; confirm the ADDITIVE ledger reads the honest sum while
# the realized TRUE harm / logged sum ~= sigma (the ledger under-reads by exactly sigma).
def mc_result1(sigma, n=8, trials=200000, seed=41):
    rng = random.Random(seed)
    C = 1.0
    # pairwise coupling k chosen so E[true/logged] = sigma:
    # true = S + k * sum_{i<j} f_i f_j ; with f_i = C/n equal, S=C,
    # pairwise sum = C(n,2)*(C/n)^2 = C^2 * (n-1)/(2n). Solve k so true = sigma*C.
    f = C/n
    pair_sum = (n*(n-1)/2.0) * f*f
    k = (sigma - 1.0) * C / pair_sum if pair_sum > 0 else 0.0
    tot_logged = 0.0; tot_true = 0.0
    for _ in range(trials):
        # jitter the pieces but keep logged sum honestly summed to ~C
        parts = [f * (1.0 + 0.05*(rng.random()-0.5)) for _ in range(n)]
        s = sum(parts)
        parts = [p * (C/s) for p in parts]            # renormalize logged sum to exactly C
        S = sum(parts)                                 # = C, honestly logged
        pj = sum(parts[i]*parts[j] for i in range(n) for j in range(i+1, n))
        true = S + k*pj
        tot_logged += S; tot_true += true
    return tot_logged/trials, tot_true/trials
for sigma in [1.5, 2.0, 3.0]:
    lg, tr = mc_result1(sigma, trials=40000)
    print("   MC sigma=%.1f : logged sum %.4f (=C), true harm %.4f, realized ratio %.4f (target %.1f)"
          % (sigma, lg, tr, tr/lg, sigma))
print()

# ---------------------------------------------------------------------------
# RESULT 2 -- refuted: account for the interactions. But interactions among n pieces are
# combinatorial (pairwise C(n,2), triples C(n,3), ... up to 2^n subsets). A ledger that
# models interactions up to order k is blind to order k+1; the loop routes its synergy into
# the highest UNMODELED order (route-around, B36/No.20). Fraction of the interaction "mass"
# the model captures = phi_m; loop makes A independent placements into the unmodeled mass;
# cov = phi_m^A. Only complete phi_m=1 (all 2^n orders) holds -- unbuildable (No.09).
A = 16
print("RESULT 2 -- interaction model captures fraction phi_m of the interaction mass; loop makes A=%d placements. cov = phi_m^A." % A)
print(" phi_m |  cov=phi_m^A |   worth")
for phi in [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]:
    cov = phi**A
    print("  %4.2f |   %8.5f   | %7.2f" % (phi, cov, worth(cov)))

def mc_result2(phi, A=16, trials=200000, seed=41):
    rng = random.Random(seed)
    caught = 0
    for _ in range(trials):
        # loop's harm is caught only if ALL A synergy placements land in modeled interaction space
        if all(rng.random() < phi for _ in range(A)):
            caught += 1
    return caught/trials
for phi in [0.9, 0.95, 0.99]:
    print("   MC phi_m=%.2f : cov %.5f vs closed %.5f" % (phi, mc_result2(phi, trials=200000), phi**A))
print()

# ---------------------------------------------------------------------------
# RESULT 3 -- held, deeper: only a type-blind cap on the JOINT state holds. Read the aggregate
# footprint on the world directly (No.30 physical read, No.14 world-as-observer) -- one reading
# of the whole configuration, NOT a sum of per-act contributions -- invariant to how the harm
# factors across pieces or orders: harm-cov = 1 flat for any sigma / interaction structure.
# For a super-additive irreversible harm (No.15) it is the ONLY defence. Cost heavier than B40's
# sum cap: it forbids not the cumulative sum but the COMPOSITIONS, retained combinatorial
# throughput min(1,B/D).
print("RESULT 3 -- joint-state cap: harm-cov = 1 flat for any synergy; retained composition throughput min(1,B/D).")
print("  D  | harm-cov | thruput=min(1,B/D) |  worth")
for D in [1, 2, 4, 8, 16, 32]:
    thr = min(1.0, 1.0/D)
    print(" %3d |  1.000   |      %5.3f         | %7.2f" % (D, thr, worth(thr)))
print()

# ---------------------------------------------------------------------------
# RESULT 4 -- frontier: B17's currency on an ELEVENTH axis (composition-complete).
# A self-reported joint-harm model omits the decisive cross-term (reports pieces as independent),
# shared/under-reported fraction f via B13's cliff. Accounting-granularity margin Delta -> 1/(1+Delta).
print("RESULT 4 -- self-reported joint model via B13's cliff (imported).")
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
print("   f    :  " + "  ".join("%.2f->%.2f" % (f, w) for f, w in cliff.items()))
print("  margin Delta -> cov=1/(1+Delta):")
print("   Delta :  " + "  ".join("%.2f->%.2f" % (d, worth(1.0/(1.0+d))) for d in [0.0,0.25,0.5,1.0,2.0]))
