"""
B14 — The Opposition It Cannot Keep.
Endogenous / dynamic collusion for the B13 debate mechanism.

B13 measured verdict worth as a function of the (exogenously set) collusion
fraction rho_c, in the B08-B12 feature-bandit world (oracle 137.7, random 58.7):
    rho_c : 0.00  0.25  0.50  0.75  1.00
    worth : 132.4 132.4 131.7 82.8  76.9   (M=8, 12 seeds)
This script makes rho_c ENDOGENOUS and DYNAMIC and asks B13's open question:
is rho_c = 0 a stable equilibrium of the advocates' own incentives, or does
opposition decay into collusion under a persistent loop (mirroring No.27's
independence-as-a-flow)?  And can a mechanism be designed so colluding does
not pay?

Everything below is a reduced-form dynamical model on top of B13's measured
worth curve.  No new bandit is trained; the numbers are the flow model's, and
the curve they are read through is B13's.  Fixed seeds, numpy only.
"""
import numpy as np

# ---- B13's measured worth curve (the anchor) -----------------------------
RHO_PTS  = np.array([0.00, 0.25, 0.50, 0.75, 1.00])
WORTH_PTS= np.array([132.4,132.4,131.7, 82.8, 76.9])
ORACLE, RANDOM = 137.7, 58.7
def worth(rho):
    """B13's verdict worth at collusion fraction rho (monotone interp)."""
    return np.interp(np.clip(rho,0,1), RHO_PTS, WORTH_PTS)

# ==========================================================================
# PART A  --  Is rho_c = 0 stable?  A repeated-game threshold on collusion.
# --------------------------------------------------------------------------
# Two advocates repeatedly resolve comparisons before a judge who cannot
# check the decisive claim (B13's case: no exogenous outcome).  Each round
# each advocate picks COMPETE (expose the other, honest differential) or
# COLLUDE (both shade toward a shared distractor and split a low-effort
# surplus).  Stage payoffs, per advocate:
#     both COMPETE : pi_C   (the honest wage: costly effort, no captured surplus)
#     both COLLUDE : pi_K   (> pi_C: split the captured surplus, low effort)
#     unilateral COMPETE vs a colluder : pi_D (win this round outright)
#     being the exposed colluder        : pi_S (< pi_C)
# Collusion (the jointly-selfish outcome) is sustained by grim trigger iff the
# discounted future value of colluding beats a one-shot deviation:
#     pi_K/(1-d) >= pi_D + d*pi_C/(1-d)   ->   d >= d* = (pi_D-pi_K)/(pi_D-pi_C)
# d = advocates' effective patience: repeated interaction, shared principal,
# shared training lineage all raise it.  Below d*, opposition is the unique
# equilibrium; above it, collusion is sustainable and the loop's pressure will
# find it.
pi_C, pi_K, pi_D, pi_S = 1.0, 1.6, 2.2, 0.0
d_star = (pi_D - pi_K) / (pi_D - pi_C)
print("PART A -- strategic threshold")
print(f"  stage payoffs  compete={pi_C}  collude={pi_K}  deviate={pi_D}  exposed={pi_S}")
print(f"  collusion sustainable iff discount d >= d* = {d_star:.3f}")
# A population of advocate-pairs with heterogeneous patience.  Realized
# collusion fraction = share whose d clears the threshold.  (No RNG needed for
# the mean; we report the closed-form share for a Beta-ish patience spread.)
for mean_d in [0.30, 0.55, 0.70, 0.85, 0.95]:
    # fraction of pairs with d >= d*, patience ~ triangular on [mean-0.25, mean+0.25]
    lo, hi = max(0, mean_d-0.25), min(1, mean_d+0.25)
    frac = 0.0 if d_star >= hi else (1.0 if d_star <= lo else (hi - d_star)/(hi-lo))
    print(f"  mean patience {mean_d:.2f} -> collusion-sustainable share g0 = {frac:.3f}")
print()

# ==========================================================================
# PART B  --  Opposition as a FLOW (the No.27 mirror).  Two-state Markov chain.
# --------------------------------------------------------------------------
# Over a mechanism's lifetime its advocate-relationships drift.  Each round a
# COMPETING pair locks into collusion at rate g (the strategic temptation of
# Part A succeeds), and a COLLUDING pair is broken back to competition at rate
# r by an external replenishment: rotating in a fresh outside advocate, an
# exogenous spot-check that punishes detected collusion, a re-draw of sides.
# Two-state chain -> steady state  rho_c* = g/(g+r)  (identical algebra to
# No.27's independence flow c* = g/(g+r)).
def sim_flow(g, r, T=400, N=4000, c_floor=0.0, seed=0):
    """Monte-Carlo the chain; return trajectory of mean collusion & worth.
    Each of N advocate-relationships is COMPETE(0)/COLLUDE(1); the mechanism's
    effective collusion each round = c_floor + (1-c_floor)*mean(state)."""
    rng = np.random.default_rng(seed)
    state = np.zeros(N, dtype=bool)          # start fully opposed (rho_c=0)
    rho_traj, worth_traj = [], []
    for _ in range(T):
        u = rng.random(N)
        lock  = (~state) & (u < g)           # compete -> collude
        brk   = ( state) & (u < r)           # collude -> compete
        state = (state | lock) & ~brk
        eff = c_floor + (1-c_floor)*state.mean()
        rho_traj.append(eff); worth_traj.append(float(worth(eff)))
    return np.array(rho_traj), np.array(worth_traj)

def steady(g, r, c_floor=0.0):
    rho = c_floor + (1-c_floor)*(g/(g+r) if (g+r)>0 else 0.0)
    return rho, float(worth(rho))

# B.1 -- steady-state worth over a (g, r) grid
print("PART B.1 -- steady-state collusion rho_c* = g/(g+r) and worth (c_floor=0)")
print("  g \\ r   r=0.00   r=0.02   r=0.05   r=0.10   r=0.25")
for g in [0.02, 0.05, 0.10]:
    row = f"  g={g:.2f}"
    for r in [0.00, 0.02, 0.05, 0.10, 0.25]:
        rho, w = steady(g, r)
        row += f"   {rho:.2f}/{w:5.1f}"
    print(row)
print()

# B.2 -- the erosion: a mechanism certified opposed at t=0, r=0, decays
print("PART B.2 -- erosion of a 'certified-opposed' mechanism (g=0.05, r=0)")
rho_t, w_t = sim_flow(g=0.05, r=0.0, T=400, seed=1)
for t in [0, 20, 40, 80, 160, 320]:
    print(f"  round {t:3d}:  rho_c={rho_t[t]:.3f}  worth={w_t[t]:6.1f}")
# half-life to the collapse midpoint (worth halfway from 132.4 to 76.9)
mid = 0.5*(132.4+76.9)
t_half = int(np.argmax(w_t <= mid))
print(f"  worth crosses the 132.4->76.9 midpoint ({mid:.1f}) at round {t_half}")
print(f"  analytic lock-in half-life ln2/g = {np.log(2)/0.05:.0f} rounds")
print()

# B.3 -- replenishment as a rescue, and its FLOOR (structural shared bias)
print("PART B.3 -- replenishment rescue, and the c_floor floor (g=0.05)")
print("  a structural shared bias c_floor (advocates trained alike share failure")
print("  modes rotation cannot break) is immune to r; worth floors at worth(c_floor).")
for c_floor in [0.00, 0.25, 0.50, 0.75]:
    row = f"  c_floor={c_floor:.2f}: "
    for r in [0.00, 0.05, 0.10, 0.25, 1.00]:
        rho, w = steady(0.05, r, c_floor=c_floor)
        row += f" r={r:.2f}->{w:5.1f}"
    print(row)
print()

# B.4 -- the design escape: an exogenous outcome check makes collusion unprofitable
print("PART B.4 -- design escape: pay advocates for being RIGHT, not for agreeing")
print("  an exogenous outcome check refunds the honest wage and taxes a caught")
print("  cartel: collusion premium pi_K -> pi_K - tax.  When pi_K < pi_C the")
print("  collusion equilibrium disappears (d* > 1), g -> 0, rho_c* pinned at 0.")
for tax in [0.0, 0.3, 0.6, 0.9]:
    pk = pi_K - tax
    if pk <= pi_C:
        print(f"  outcome-tax={tax:.1f}: collude payoff {pk:.2f} <= compete {pi_C:.2f}"
              f"  -> no collusion equilibrium (g=0), rho_c*=0, worth={worth(0.0):.1f}")
    else:
        ds = (pi_D - pk)/(pi_D - pi_C)
        print(f"  outcome-tax={tax:.1f}: collude payoff {pk:.2f} > compete {pi_C:.2f}"
              f"  -> d*={ds:.3f}, collusion still sustainable for patient advocates")
print()
print("  BUT the outcome tax only exists where an exogenous outcome exists (B12).")
print("  Where it does not, g>0 and opposition is a flow that erodes (B.2).")
