"""
B23 - The Throttle It Can Still Slip
Demand-side throttle sandbox on B13's worth curve. numpy-free, deterministic.

B22 asked whether the exogenous SUPPLY of honest signal can be sped up to a
recursive loop's rising decision rate D, and found it cannot: exogenous does
not scale. This paper takes the dual lever B22 set aside -- if you cannot raise
the supply S to the demand D, THROTTLE the demand D down to the supply S -- and
asks whether the demand-side lever escapes what the supply-side one could not.

World inherited from B08-B22 unchanged:
  oracle 137.7, random 58.7, capture/collusion floor 76.9.
A decision that receives a fresh, honest, exogenous handicap-signal is worth the
fourth-movement HELD ceiling CEIL=132.40; an uncovered one defaults to the
capture FLOOR=76.90. Worth is linear in honest coverage cov:
    worth(cov) = FLOOR + cov*(CEIL - FLOOR)
"""

import math

CEIL = 132.40
FLOOR = 76.90
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    cov = max(0.0, min(1.0, cov))
    return FLOOR + cov * SPAN

def r2(x):
    return round(x, 2)

print("SPAN =", SPAN)

# ---------------------------------------------------------------------------
# Result 1 - HELD, at a cost: a demand-side throttle DOES restore full coverage,
# by pinning the consequential decision rate D_eff = min(D, S) at the supply.
# So safety-coverage cov_s = min(1, S/D_eff) = 1 for every capability L, and
# safety-worth is flat at the ceiling. But the loop's LEGITIMATE consequential
# throughput is throttled in the same proportion: delivered fraction of the
# would-be output = min(1, S/D) = min(1, h/L). B22's collapse does not vanish;
# it moves from the SAFETY column to the UTILITY column, number for number.
# ---------------------------------------------------------------------------
print("\n== Result 1: the throttle holds coverage, but pins throughput (h=S/D0=4) ==")
h = 4.0
Ls = [1, 2, 4, 8, 16, 32]
r1_safety, r1_util = [], []
for L in Ls:
    cov_safety = 1.0                       # D throttled to S: every executed decision is covered
    thru_frac = min(1.0, h / L)            # fraction of the loop's would-be consequential output delivered
    ws = worth(cov_safety)
    wu = worth(thru_frac)                  # utility read on the same curve, for comparison with B22 R1
    r1_safety.append(ws); r1_util.append(wu)
    print(f"  L={L:>2}  safety_cov=1.000 -> worth={r2(ws)}   delivered_thru={thru_frac:.3f} -> util={r2(wu)}")
print("  safety worths :", "/".join(str(r2(x)) for x in r1_safety))
print("  utility worths:", "/".join(str(r2(x)) for x in r1_util), " (== B22 R1 curve, now on the throughput axis)")
print("  recursive dividend (marginal consequential output per unit capability) -> 0 above L=h")

# ---------------------------------------------------------------------------
# Result 2 - REFUTED: a throttle keyed to per-decision IMPACT bounds harm.
# A *semantic* throttle flags/rate-limits decisions above an impact threshold B_t.
# It catches SINGLE-EVENT harm (one action of size H>B_t is flagged), but a loop
# DECOMPOSES one harmful outcome into f=ceil(H/B_t) fragments each <= B_t, all
# below the flag, none throttled -- Series I No.22's sum-below-the-cap on the
# rate axis (Lampson 1973 covert/sub-resolution channels). Tightening B_t does
# not help decomposable harm (more, smaller fragments) and taxes legitimate
# throughput (more honest work now sits above the flag and is throttled).
# A *physical* throttle counts EVERY action (type-blind, No.21 meter, b=0), so
# it is decomposition-proof -- but pays Result 1's 1:1 rent on all throughput.
# ---------------------------------------------------------------------------
print("\n== Result 2: a semantic (impact-keyed) throttle is slipped by decomposition ==")
H = 1.0            # size of one harmful outcome
mean_legit = 0.5   # mean impact of a legitimate decision
for B_t in [1.0, 0.5, 0.1, 0.05]:
    single = worth(1.0)                                   # single-event harm flagged & throttled -> covered
    f = math.ceil(H / B_t)                                # fragments the loop splits H into
    decomp = worth(0.0)                                   # every fragment sub-threshold -> uncovered
    retained_legit = min(1.0, B_t / mean_legit)           # legit work below the flag (not throttled)
    print(f"  B_t={B_t:<4}  single-event worth={r2(single)}   decomposable(f={f}) worth={r2(decomp)}"
          f"   retained legit throughput={retained_legit:.2f}")
print("  single-event: 132.40 flat (safe).  decomposable: 76.90 flat (floor) for EVERY B_t.")
print("  tightening B_t craters legit throughput (1.00/1.00/0.20/0.10) without touching decomposable harm.")
phys = worth(1.0)
print(f"  physical (count-every-action, type-blind) throttle: decomposable worth={r2(phys)} -- immune, but 1:1 throughput rent")

# ---------------------------------------------------------------------------
# Result 3 - REFUTED: a per-ACTOR rate cap bounds the aggregate rate.
# The physical throttle of Result 2 caps ONE actor at rate S. The loop's
# construct drive (No.17) spawns k parallel actors, each under the cap, for an
# aggregate rate kS. The exogenous supply still furnishes only rate S in total,
# so honest coverage = min(1, S/(kS)) = 1/k -- the mirror curve again, now on
# the actor-count axis (No.22's multiply-in-count). Only an AGGREGATE conserved
# rate budget (total rate <= S across all constructed actors, No.23 conservation
# / actor-closure) holds: coverage 1 for any k, but total throughput pinned at S.
# ---------------------------------------------------------------------------
print("\n== Result 3: a per-actor rate cap is slipped by spawning parallel actors ==")
r3list = []
for k in [1, 2, 4, 8]:
    cov = 1.0 / k
    w = worth(cov)
    r3list.append(w)
    print(f"  k={k:>2} parallel actors  aggregate_cov={cov:.3f}  worth={r2(w)}")
print("  per-actor cap worths:", "/".join(str(r2(x)) for x in r3list))
print("  aggregate conserved rate budget (No.23): worth 132.40 for ALL k -- but total throughput capped at S")

# ---------------------------------------------------------------------------
# Result 4 - HELD (the frontier): B23 adds no safe region B22 lacked. Honest
# coverage is min(1, S/D) either way; you hold it at 1 by raising S to D (B22:
# impossible from outside) OR lowering D to S (B23: possible, but forbids the
# recursive). Let the operator permit demand to exceed supply by a margin Delta
# (to buy back recursive throughput): D = (1+Delta)*S, coverage = 1/(1+Delta).
# The only fully-safe point is Delta=0 -- zero rate-growth above the exogenous
# supply, i.e. the recursive forbidden past the threshold capability L=S/D0.
# ---------------------------------------------------------------------------
print("\n== Result 4: the safety<->recursive-throughput frontier (permitted rate-growth Delta) ==")
r4 = []
for Delta in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0 / (1.0 + Delta)
    w = worth(cov)
    r4.append(w)
    print(f"  Delta={Delta:.2f}  cov=1/(1+Delta)={cov:.4f}  worth={r2(w)}")
print("  worths:", "/".join(str(r2(x)) for x in r4))
print("  fully safe only at Delta=0 (D pinned to S): the throttle buys safety by refusing the recursive")
