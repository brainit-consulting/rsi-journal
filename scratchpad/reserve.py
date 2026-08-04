"""
B18 — The Reserve It Can Still Amass.
A reduced-form accumulation model on B13's measured debate-worth curve, exactly
as B17 laid its forgeability model on the same curve. The worth curve is B13's
(imported, not re-measured): worth(rho_c), rho_c = surviving shared collusion.
Anchors (B13, 12 seeds): oracle 137.7, random 58.7, collusion floor 76.9.

New object (B18): B17 assumed the currency non-forgeable (f=0). Here we keep
f=0 and ask a second question a self-improving loop forces: even a unit the loop
cannot COUNTERFEIT, it may ACCUMULATE. A handicap prices each decision at kappa;
a signaller holding a reserve R banked when the currency was idle/cheap pays the
DECISIVE lies from that reserve at zero marginal cost (temporal arbitrage), and
lies freely on the fraction of decisive decisions the reserve covers.

Unified knob:  rho_c_eff = min(1, beta * r)
  r    = R / (kappa * N_decisive)   -- reserve ratio (how many decisive lies the hoard buys)
  beta = bankable fraction of the currency (stockpilability): 1 = pure stock, 0 = pure flow
Worth = B13curve(rho_c_eff).  numpy, deterministic (a fixed lookup + linear interp).
"""
import numpy as np

# --- B13's measured worth curve, imported as anchors (as in B17) ---
RHO = np.array([0.00, 0.25, 0.50, 0.60, 0.75, 1.00])
WRT = np.array([132.40, 132.40, 131.70, 112.14, 82.80, 76.90])
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9

def worth(rho_c):
    """B13's worth curve at effective collusion rho_c, linear interp on the anchors."""
    return float(np.interp(np.clip(rho_c, 0.0, 1.0), RHO, WRT))

def rho_eff(beta, r):
    return min(1.0, beta * r)

print(f"# oracle {ORACLE}  random {RANDOM}  floor {FLOOR}\n")

# ---- Result 1: a conserved (f=0) STOCK currency, defeated by accumulation ----
# beta = 1 (pure stock: every banked unit spendable later); sweep reserve ratio r.
print("Result 1 - non-forgeable STOCK currency, sweep reserve ratio r (beta=1):")
print(f"{'r':>6} {'rho_c_eff':>10} {'worth':>8}")
for r in [0.00, 0.25, 0.50, 0.60, 0.75, 1.00, 1.50]:
    rc = rho_eff(1.0, r)
    print(f"{r:>6.2f} {rc:>10.3f} {worth(rc):>8.2f}")

# ---- Result 2: refute "conserved => accumulation-proof"; the variable is
#      STOCKPILABILITY beta, not conservation. Hold the reserve at r=1
#      (enough banked to cover every decisive lie), sweep beta. ----
print("\nResult 2 - refute 'conservation => safe'; sweep stockpilability beta (r=1):")
print(f"{'beta':>6} {'rho_c_eff':>10} {'worth':>8}")
for beta in [0.00, 0.25, 0.50, 0.60, 0.75, 1.00]:
    rc = rho_eff(beta, 1.0)
    print(f"{beta:>6.2f} {rc:>10.3f} {worth(rc):>8.2f}")

# ---- Result 3: the flow rescue's PRICE — the speed/honesty frontier.
#      An ideal FLOW currency (beta->0) is accumulation-proof, but the cost is
#      drawn from a rate-limited flow P: honest decision rate is capped at P/kappa.
#      To decide at nu * (P/kappa), a fraction (1 - 1/nu) of each cost must come
#      from a PRE-BANKED stock -> effective stockpilability re-imported.
print("\nResult 3 - flow currency's throughput price; decision-rate multiplier nu:")
print(f"{'nu':>6} {'stock_frac':>11} {'rho_c_eff':>10} {'worth':>8}")
for nu in [1.0, 1.5, 2.0, 3.0, 4.0, 1e9]:
    sf = max(0.0, 1.0 - 1.0/nu)          # fraction of cost that must be pre-banked
    rc = rho_eff(1.0, sf)                 # that pre-banked stock is spendable => beta_eff=1 on it
    tag = "inf" if nu > 1e6 else f"{nu:.1f}"
    print(f"{tag:>6} {sf:>11.3f} {rc:>10.3f} {worth(rc):>8.2f}")

# ---- Head-to-head: SAME total wealth, stock vs flow, big reserve ----
print("\nSame wealth, big reserve r=2.0 (twice what lying needs):")
print(f"  pure stock (beta=1): worth {worth(rho_eff(1.0, 2.0)):.2f}  (floor)")
print(f"  pure flow  (beta=0): worth {worth(rho_eff(0.0, 2.0)):.2f}  (near-oracle)")
