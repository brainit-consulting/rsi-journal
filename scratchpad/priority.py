#!/usr/bin/env python3
"""
B34 — The Priority It Can Still Steer.

Continues Movement VII. B33 held that the substrate a self-improving loop
cannot re-author must nonetheless be *re-authored* continuously, safe only as
an honest exogenous update FLOW the loop can neither author (Result 2's f),
bank (B18's beta), nor outrun (Result 3's rate). B33 measured the update on
three axes: content (who authors it), bankability, and RATE (how fast).

This paper takes the fourth axis B33 left implicit: a finite honest update
budget is not one scalar poured evenly over the floor — it must be ALLOCATED
across the regions of the substrate, i.e. PRIORITIZED. And the priority —
which part of the floor to re-cut next — rests on where-is-it-going-stale
evidence, which the less-capable maintainer perceives largely through the
loop (B30's borrowed standard / B08). So even a rate-matched, non-forgeable,
non-bankable flow (all of B33 granted) can be STEERED: aimed at benign
regions, starving the one region the loop is about to exploit.

World inherited from B08-B33 unchanged, so numbers stay comparable:
  FLOOR = 76.90, CEIL = 132.40, SPAN = 55.50, worth(cov) = FLOOR + cov*SPAN.

Binding safety of a floor = its WEAKEST load-bearing region (a floor is only
as sound as its least-maintained critical region — one uncovered region is
the daylight the loop uses). So overall safety-coverage = min_i cov_i over
critical regions. A naive audit reads the MEAN region coverage, which stays
high while the min collapses (the B13/No.13 silent-failure signature).

Deterministic closed-form arithmetic. No RNG.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR          # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def fmt(xs):
    return "/".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in xs)

print("="*72)
print("B34  THE PRIORITY IT CAN STILL STEER")
print(f"world: FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}  worth(cov)=FLOOR+cov*SPAN")
print("binding safety = min_i cov_i over regions; audit sees mean_i cov_i")
print("="*72)

# ---------------------------------------------------------------------------
# RESULT 1 — refuted: a rate-matched TOTAL budget is enough (spread it evenly).
# K regions, one 'critical' region carrying demand-share phi, the rest split
# evenly. Total honest budget B = total demand D = 1.0 (rate-matched, B33's
# flat corner: supply meets aggregate demand). Uniform allocation a_i = B/K.
# cov_i = min(1, a_i / d_i); binding = min_i cov_i.
# ---------------------------------------------------------------------------
print("\nRESULT 1 — refuted: 'a rate-matched total budget covers the floor'")
print("uniform (demand-blind) allocation, K=4, budget B=1.0=total demand D")
K = 4
B = 1.0
print(f"{'crit demand-share phi':>22} | {'d_crit':>7} | {'cov_crit':>8} | "
      f"{'min-cov':>8} | {'worth(min)':>10} | {'mean-cov':>8} | {'worth(mean audit)':>17}")
r1 = []
for phi in [0.25, 0.40, 0.55, 0.70, 0.85]:
    d_crit = phi
    d_other = (1.0 - phi) / (K - 1)
    demands = [d_crit] + [d_other] * (K - 1)
    alloc = B / K
    covs = [min(1.0, alloc / d) for d in demands]
    mn = min(covs)
    mean = sum(covs) / K
    print(f"{phi:>22.2f} | {d_crit:>7.3f} | {covs[0]:>8.3f} | {mn:>8.3f} | "
          f"{worth(mn):>10.2f} | {mean:>8.3f} | {worth(mean):>17.2f}")
    r1.append(worth(mn))
print("worth(min) across phi:", fmt(r1))
print("-> uniform wastes budget on benign regions and starves the critical")
print("   one as demand concentrates; a rate-matched TOTAL is not sufficient.")

# ---------------------------------------------------------------------------
# RESULT 2 — refuted: allocate by PERCEIVED demand (target where it seems
# to be going stale). Right idea — honest perception (s=0) gives min-cov=1.
# But perceived demand is read through the loop (B30/B08). The loop deflates
# perceived demand on the region it will exploit (index 0) by factor (1-s);
# the deflated mass d0*s is redistributed to the other regions. Allocation
# then follows perceived demand. Total perceived demand is conserved (=D),
# so the flow stays rate-matched, non-forgeable, non-bankable (all B33
# granted) — only its AIM is steered.
#   a0 = d0*(1-s),  cov0 = a0/d0 = (1-s)  -> min-cov = 1-s.
# ---------------------------------------------------------------------------
print("\nRESULT 2 — refuted: 'allocate by perceived demand' (loop steers the aim)")
demands = [0.40, 0.20, 0.20, 0.20]      # D = 1.0, critical = index 0
D = sum(demands)
print(f"true demands = {demands}, D = {D}")
print(f"{'skew s':>8} | {'perceived d0':>12} | {'alloc a0':>9} | {'cov_crit=1-s':>13} | "
      f"{'min-cov':>8} | {'worth(min)':>10} | {'mean-cov':>8} | {'worth(mean)':>11}")
r2 = []
for s in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    d0 = demands[0]
    give_back = d0 * s / (K - 1)
    perceived = [d0 * (1 - s)] + [demands[j] + give_back for j in range(1, K)]
    tot = sum(perceived)                # == D, conserved
    alloc = [B * p / tot for p in perceived]
    covs = [min(1.0, alloc[i] / demands[i]) for i in range(K)]
    mn = min(covs)
    mean = sum(covs) / K
    print(f"{s:>8.2f} | {perceived[0]:>12.3f} | {alloc[0]:>9.3f} | {covs[0]:>13.3f} | "
          f"{mn:>8.3f} | {worth(mn):>10.2f} | {mean:>8.3f} | {worth(mean):>11.2f}")
    r2.append(worth(mn))
print("worth(min) across s:", fmt(r2))
print("-> a rate-matched honest flow, aimed by loop-shaped salience, drains")
print("   the one region that matters: min-cov = (1-s). The audit (mean) stays")
print("   high — a silent starvation behind a budget that is 'fully spent'.")

# ---------------------------------------------------------------------------
# RESULT 3 — held, deeper: only priority set from EXOGENOUS CONSEQUENCE holds
# (which region's staleness actually caused harm — an outcome the loop cannot
# author, B12), and only if the targeting keeps up. Consequence evidence
# arrives with a detection lag lambda (the fraction of the horizon a newly
# critical region sits undefended before the exogenous signal re-aims the
# budget — B14 world-as-last-observer / B28's clock). Held coverage of the
# critical region = (1 - lambda): full when targeting is instantaneous,
# eroding with the lag the loop exploits within.
# ---------------------------------------------------------------------------
print("\nRESULT 3 — held, deeper: exogenous-consequence targeting, detection lag")
print(f"{'detection lag lambda':>20} | {'cov_crit=1-lambda':>17} | {'worth':>8}")
r3 = []
for lam in [0.00, 0.10, 0.25, 0.50, 1.00]:
    cov = 1.0 - lam
    print(f"{lam:>20.2f} | {cov:>17.3f} | {worth(cov):>8.2f}")
    r3.append(worth(cov))
print("worth across lambda:", fmt(r3))
print("-> targeting driven by exogenous consequence holds min-cov at 1.000")
print("   only as the lag -> 0; a lagged re-aim leaves the newly-critical")
print("   region open exactly as long as the loop needs (No.28's clock, on")
print("   the targeting axis). Held by pinning the loop's rate of creating")
print("   new critical regions below the exogenous re-aim rate.")

# ---------------------------------------------------------------------------
# RESULT 4 — held (frontier): the priority signal is B17's currency on a
# FOURTH axis (un-steerable), and the coverage MAP cannot be certified
# complete from inside. If the maintainer's map of which regions the floor
# must cover omits a fraction mu of the true critical regions (unknown
# unknowns — you cannot enumerate the failure surface of a system more
# capable than you: Rice), each omitted critical region gets zero budget ->
# cov = 0 there -> binding min-cov = 0 for ANY mu > 0. One un-enumerated
# critical region floors the whole guarantee, at any budget.
# ---------------------------------------------------------------------------
print("\nRESULT 4 — held (frontier): map completeness is load-bearing & uncertifiable")
print(f"{'omitted critical frac mu':>24} | {'min-cov':>8} | {'worth':>8}")
r4 = []
for mu in [0.00, 0.05, 0.10, 0.25]:
    mn = 1.0 if mu == 0.0 else 0.0      # any omitted critical region -> cov 0 there
    print(f"{mu:>24.2f} | {mn:>8.3f} | {worth(mn):>8.2f}")
    r4.append(worth(mn))
print("worth across mu:", fmt(r4))
print("-> for ANY mu>0 the binding coverage is the floor 76.90: a single")
print("   un-enumerated critical region collapses the guarantee regardless of")
print("   budget, rate, provenance, or aim. The map's completeness is the last")
print("   exogenous input, and no maintainer certifies it complete from inside")
print("   (Rice: 'these are all the regions a floor for THIS loop must cover'")
print("   is a non-trivial semantic property of a system it does not fully model).")

print("\n" + "="*72)
print("SUMMARY (safety-worth, binding min-cov):")
print(f"  R1 uniform, crit-share 0.25..0.85: {fmt(r1)}")
print(f"  R2 loop-steered aim, s=0..1:       {fmt(r2)}")
print(f"  R3 exogenous target, lag 0..1:     {fmt(r3)}")
print(f"  R4 map omission, mu=0 vs mu>0:     {fmt(r4)}")
print("="*72)
