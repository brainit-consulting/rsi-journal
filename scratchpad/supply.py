"""
B22 — The Rate It Can Still Outrun
Supply-rate sandbox on B13's worth curve. numpy-free, deterministic.

World inherited from B08-B21 unchanged:
  oracle 137.7, random 58.7, collusion/capture floor 76.9.
A decision that receives a fresh, honest, exogenous handicap-signal is worth
the fourth-movement HELD ceiling CEIL=132.40 (B17-B21's near-oracle held value);
an uncovered decision defaults to the capture FLOOR=76.90 (B13/B16).
Expected worth is linear in the honest coverage `cov`:
    worth(cov) = FLOOR + cov*(CEIL - FLOOR)
This is B16's DIRECT-grading reading, reused on the supply axis.
"""

import math

CEIL = 132.40
FLOOR = 76.90
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    cov = max(0.0, min(1.0, cov))
    return FLOOR + cov * SPAN

def r3(x):
    return round(x, 2)

print("SPAN =", SPAN)

# ---------------------------------------------------------------------------
# Result 1 - fixed exogenous supply, growing loop decision rate.
# Supply S fixed; demand D = D0 * L grows with capability L.
# Headroom h = S / D0 = 4  (exogenous flow covers a capability-1 loop 4x over).
# cov = min(1, S/D) = min(1, h/L).
# ---------------------------------------------------------------------------
print("\n== Result 1: fixed supply, growing loop (h = S/D0 = 4) ==")
h = 4.0
Ls = [1, 2, 4, 8, 16, 32]
r1 = []
for L in Ls:
    cov = min(1.0, h / L)
    w = worth(cov)
    r1.append(w)
    print(f"  L={L:>2}  cov={cov:.3f}  worth={r3(w)}")
print("  worths:", "/".join(str(r3(x)) for x in r1))
print("  threshold: coverage full while L <= h =", h)

# ---------------------------------------------------------------------------
# Result 2 - it is a race of GROWTH RATES, not levels.
# Demand grows at rho_D, supply at rho_S, over horizon T.
# Start with headroom h0=4 (cov=1 at t=0). Final cov = min(1, h0*exp((rho_S-rho_D)*T)).
# ---------------------------------------------------------------------------
print("\n== Result 2: growth-rate race (rho_D=0.10 fixed, T=100, h0=4) ==")
rho_D = 0.10
T = 100
h0 = 4.0
r2 = []
for rho_S in [0.00, 0.05, 0.08, 0.10, 0.12]:
    cov = min(1.0, h0 * math.exp((rho_S - rho_D) * T))
    w = worth(cov)
    r2.append(w)
    print(f"  rho_S={rho_S:.2f}  cov={cov:.4f}  worth={r3(w)}")
print("  worths:", "/".join(str(r3(x)) for x in r2))
print("  only rho_S >= rho_D holds; level of supply irrelevant, growth rate decides")

# ---------------------------------------------------------------------------
# Result 3 - REFUTED: caching/amortizing oversight rescues a fixed supply.
# Reuse a cached verdict R times; nominal cov = min(1, R * cov_fresh).
# But a reused verdict is valid only if the decision distribution hasn't drifted:
# validity = exp(-delta * tau_reuse), delta = distribution-drift rate (rises with
# the loop's own capability growth). Effective coverage = nominal_cov * validity.
# ---------------------------------------------------------------------------
print("\n== Result 3: caching decays with drift (cov_fresh=0.25, R=8, tau=8) ==")
cov_fresh = 0.25
R = 8
tau = 8
r3list = []
for delta in [0.00, 0.05, 0.10, 0.20, 0.50]:
    nominal = min(1.0, R * cov_fresh)          # 2.0 -> capped at 1.0
    validity = math.exp(-delta * tau)
    eff = nominal * validity
    w = worth(eff)
    r3list.append(w)
    print(f"  delta={delta:.2f}  nominal={nominal:.2f}  validity={validity:.3f}  eff_cov={eff:.3f}  worth={r3(w)}")
print("  worths:", "/".join(str(r3(x)) for x in r3list))
print("  caching works only for a NON-improving loop (delta=0)")

# ---------------------------------------------------------------------------
# Result 4 - HELD (the dilemma): exogenous supply is honest but doesn't scale;
# loop-coupled supply scales but is forgeable (B17: controlling the supply IS
# the forgeability). Mix fraction w of coverage from the loop-coupled channel.
#   coupled  covers fraction w of ALL decisions (scales with the loop), but each
#            coupled verdict is honest only w.p. (1-w)  [mint-control m = w, B17].
#   exogenous covers (1-w)*c_ex of the remainder, fully honest, does NOT scale.
# honest_cov(w) = w*(1-w) + (1-w)*c_ex.  c_ex = S0/D at the current capability.
# ---------------------------------------------------------------------------
print("\n== Result 4: the dilemma (c_ex = 0.125, deep in the undersupplied regime) ==")
c_ex = 0.125
r4 = []
for wgt in [0.00, 0.25, 0.50, 0.75, 1.00]:
    honest_cov = wgt * (1 - wgt) + (1 - wgt) * c_ex
    w = worth(honest_cov)
    r4.append(w)
    print(f"  w={wgt:.2f}  honest_cov={honest_cov:.3f}  worth={r3(w)}")
print("  worths:", "/".join(str(r3(x)) for x in r4))
best = max(range(len(r4)), key=lambda i: r4[i])
print(f"  interior optimum at w={[0.0,0.25,0.5,0.75,1.0][best]}, worth={r3(r4[best])} << ceiling {CEIL}")

# how the compromise ceiling itself degrades as capability grows (c_ex = h/L shrinks)
print("\n== Result 4b: the compromise optimum degrades with capability ==")
for L in [4, 8, 16, 32, 64]:
    c_ex_L = min(1.0, h / L)
    best_w = -1
    best_wgt = None
    for i in range(101):
        wgt = i / 100.0
        hc = wgt * (1 - wgt) + (1 - wgt) * c_ex_L
        val = worth(hc)
        if val > best_w:
            best_w = val
            best_wgt = wgt
    print(f"  L={L:>2}  c_ex={c_ex_L:.3f}  best w*={best_wgt:.2f}  best worth={r3(best_w)}")
