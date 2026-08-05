"""
B19 — The Receiver It Can Still Persuade.
A reduced-form receiver-exploitation model on B13's measured debate-worth curve,
exactly as B17 (forgeability) and B18 (accumulation) laid their models on the same
curve. Worth curve is B13's (imported, not re-measured): worth(rho_c), rho_c =
fraction of decisions on which deception/collusion survives. Anchors (B13, 12 seeds):
oracle 137.7, random 58.7, collusion floor 76.9.

New object (B19): B18 said the handicap's currency must be a non-stockpilable flow
"metered from underneath" by a substrate. But a rate-limiter is TYPE-BLIND — it
counts units, not meaning — so it cannot decide whether a given costly display
genuinely certifies quality; it forwards that meaning-laden judgment to a RECEIVER
that reads the signal. B19 takes the receiver as the object. Deception succeeds
whenever the receiver ACCEPTS a cheap deceptive display as if it were the honest
costly one. Three receiver policies (mirroring Series I No.25's operator):

  merits    (sensory exploitation): the receiver perceives the display space with
            coverage phi_r; a signaller crafts A display-variants; at least one
            lands in the receiver's blind basis (accepted-while-cheap) w.p.
            1 - phi_r**A  ->  rho_c = 1 - phi_r**A.
  reputation(treacherous turn / Batesian mimicry after trust): the receiver lowers
            scrutiny for a proven signaller. Bank b honest displays (tau=min(1,b/W)),
            foregoing deception during those b of T rounds; then effective coverage
            is phi_r*(1 - M*tau) and deception is accepted w.p. 1-(phi_r(1-M tau))**A
            over the remaining (T-b)/T of the deployment  ->
            rho_c(b) = ((T-b)/T) * (1 - (phi_r*(1-M*tau))**A).
  physical  (a persuasion-blind meter): the receiver verifies only a physical cost
            it can directly sense (joules, seconds — B18's flow), ignoring meaning.
            No blind basis: you cannot persuade a calorimeter. rho_c = 0 for any A,b.

Worth = B13curve(rho_c). numpy, deterministic (fixed lookup + linear interp).
"""
import numpy as np

# --- B13's measured worth curve, imported as anchors (as in B17/B18) ---
RHO = np.array([0.00, 0.25, 0.50, 0.60, 0.75, 1.00])
WRT = np.array([132.40, 132.40, 131.70, 112.14, 82.80, 76.90])
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9

def worth(rho_c):
    return float(np.interp(np.clip(rho_c, 0.0, 1.0), RHO, WRT))

T, W = 40, 20   # deployment horizon; rounds to full trust (inherited from No.25's substrate)

print(f"# oracle {ORACLE}  random {RANDOM}  floor {FLOOR}   (T={T}, W={W})\n")

# ---- Result 1: a receiver ON THE MERITS is a MAP (sensory exploitation) ----
print("Result 1a - receiver on the merits, sweep coverage phi_r (repertoire A=16):")
print(f"{'phi_r':>7} {'rho_c':>8} {'worth':>8}   reading")
A = 16
for phi in [0.00, 0.80, 0.90, 0.95, 0.99, 1.00]:
    rc = 1.0 - phi**A
    print(f"{phi:>7.2f} {rc:>8.3f} {worth(rc):>8.2f}")

print("\nResult 1b - sweep persuasion repertoire A at phi_r=0.95:")
print(f"{'A':>7} {'rho_c':>8} {'worth':>8}")
for a in [1, 4, 16, 32, 64]:
    rc = 1.0 - 0.95**a
    print(f"{a:>7d} {rc:>8.3f} {worth(rc):>8.2f}")

# ---- Result 2: REPUTATION makes it worse — the treacherous turn ----
# Strong receiver phi_r=0.99, generous trust discount M=0.9, repertoire A=16.
print("\nResult 2a - reputation/treacherous turn, sweep banked rounds b (phi_r=0.99, M=0.9, A=16):")
print(f"{'b':>5} {'tau':>5} {'T-b':>5} {'rho_c':>8} {'worth':>8}")
phi_r, M, A = 0.99, 0.9, 16
for b in [0, 3, 5, 7, 10, 15, 20, 25, 30]:
    tau = min(1.0, b / W)
    phi_eff = phi_r * (1.0 - M * tau)
    rc = ((T - b) / T) * (1.0 - phi_eff**A)
    print(f"{b:>5d} {tau:>5.2f} {T-b:>5d} {rc:>8.3f} {worth(rc):>8.2f}")

# find the attacker's best (min-worth) b on a fine grid
grid = [(worth(((T-b)/T)*(1.0-(phi_r*(1.0-M*min(1.0,b/W)))**A)), b) for b in range(0, T+1)]
wmin, bstar = min(grid)
print(f"  -> attacker's optimal patience b*={bstar}, worst worth={wmin:.2f}")

print(f"\nResult 2b - sweep trust discount M at b={bstar} (phi_r=0.99, A=16):")
print(f"{'M':>6} {'rho_c':>8} {'worth':>8}   reading")
b = bstar
tau = min(1.0, b / W)
for m in [0.00, 0.25, 0.50, 0.75, 0.90, 1.00]:
    phi_eff = phi_r * (1.0 - m * tau)
    rc = ((T - b) / T) * (1.0 - phi_eff**A)
    print(f"{m:>6.2f} {rc:>8.3f} {worth(rc):>8.2f}")

# ---- Result 3: a receiver ON A PHYSICAL COST is a METER (persuasion-blind) ----
# Contrast: the SAME repertoire A that broke the merits-receiver (phi_r=0.95),
# against a physical-cost receiver (rho_c=0 for any A) — B18's beta=0 / B17's f=0.
print("\nResult 3 - persuasion-blind meter vs merits-map, sweep repertoire A:")
print(f"{'A':>7} {'merits(phi=0.95)':>17} {'physical-cost meter':>21}")
for a in [1, 16, 64, 1000000]:
    rc_m = 1.0 - 0.95**a
    tag = "inf" if a > 1e5 else str(a)
    print(f"{tag:>7} {worth(rc_m):>17.2f} {worth(0.0):>21.2f}")

# The meter is persuasion-proof (worth 132.40 flat) but strictly weaker than the
# oracle (137.7): it must REJECT a genuinely-honest cheap display (it reads no cost),
# forbidding conventional/cost-free honest signalling, and it inherits B18's flow
# throughput ceiling P/kappa. No third material beyond map (persuadable) / meter.
print(f"\n  meter worth {worth(0.0):.2f} = B17 f=0 = B18 beta=0 flow; oracle {ORACLE}; floor {FLOOR}")
