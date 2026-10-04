#!/usr/bin/env python3
"""
B53 -- The Conservation It Can Still Anomalize.

Sandbox for the seventh movement's twenty-second turn. Takes B52's held rescue
as object: only an EXACT, fundamentally-enforced, reference-frame-proof
conservation -- a quantity conserved to all orders by a symmetry the
un-re-authorable substrate enforces -- or a bounded horizon, holds an
irreversible harm against a patient, resource-acquiring loop. B52 earned "an
exact fundamental symmetry" and rested on a word it did not examine: that an
exact CLASSICAL symmetry gives an exact CONSERVATION law. It need not. The
Noether current of a symmetry that is exact and unbroken at the classical and
all-perturbative-orders level can still fail to be conserved QUANTUM-
mechanically -- the ANOMALY.

Two facts, both real physics, both against B52's rescue:

  (1) Anomaly = a nonzero divergence with NO breaking term. An exact, unbroken
      classical symmetry (epsilon=0 in B49/B52's sense -- nothing explicitly
      breaks it) can have an anomalous divergence d_mu j^mu = A * (topological
      density), because the path-integral MEASURE is not invariant under the
      symmetry (Fujikawa 1979; Adler 1969; Bell-Jackiw 1969). The "conserved"
      charge changes by Delta Q = A * n, n = winding number (instanton number)
      of the background the field sits in. This is NOT B49's small explicit
      breaking epsilon that one could shrink: the anomaly coefficient A is a
      fixed rational number fixed by the charges in the theory.

  (2) Adler-Bardeen non-renormalization: the anomaly is ONE-LOOP EXACT -- it
      receives no higher-order corrections and is INDEPENDENT of the coupling
      strength g (Adler-Bardeen 1969). So you cannot make the protection hold
      by taking the coupling tiny or working to higher order: a perturbative
      leak scales as g^2 and vanishes as g->0, but the anomalous
      non-conservation does NOT -- it is set by the topological charge the
      loop sources, not by g. A self-improver SOURCES the topological
      background (a sequence of instantons; or, over a finite sphaleron
      barrier at high "temperature", classically -- Klinkhamer-Manton 1984;
      Kuzmin-Rubakov-Shaposhnikov 1985; 't Hooft 1976), so the charge
      violation Delta Q = A * n grows with the winding n the loop accumulates
      -- its resource-acquisition drive (Omohundro 2008) builds the winding.

What HOLDS (Result 3): not a smaller coupling but a different grounding --
  (a) an ANOMALY-FREE symmetry: the anomaly coefficient A vanishes by
      cancellation among the charges (Standard-Model anomaly cancellation;
      Bouchiat-Iliopoulos-Meyer 1972; Gross-Jackiw 1972), so there is no
      topological source to pump and Delta Q = 0 for any winding; OR
  (b) an exact 't HOOFT ANOMALY: an anomaly that MUST be matched between UV
      and IR, an RG-invariant obstruction NO dynamics the loop runs can remove
      ('t Hooft 1980) -- the genuinely un-liftable object B52 was reaching
      for, used as the protection itself rather than as the leak; OR
  (c) a bounded horizon capping the accessible winding number n.
  At a throughput cost: an anomaly-free / anomaly-matched construction
  constrains the allowed interactions (forbids benign couplings with malign).

World inherited from B08-B52 unchanged so the numbers stay comparable across
forty-six papers:
  K=10 feature-bandit, B13's worth curve.
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR + cov*(CEIL-FLOOR), SPAN=55.50.

Binding safety = coverage of the true irreversible harm against a loop that
PUMPS charge across an exact symmetry via the anomaly. Anomalous charge-
crossing events are Poisson at rate r = r0 * A * phi (A anomaly coefficient,
phi topological flux the loop sources), so over horizon N coverage
= e^{-rN} = e^{-mu}, mu = rN. Crucially r is INDEPENDENT of the coupling g.

Deterministic closed-form arithmetic + a seeded anomalous-charge-pumping
Monte Carlo (pure dynamics, numpy only, no network, fixed seed).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Inherited world (B08-B52, unchanged)
FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR            # 55.50
def worth(cov):                 # linear DIRECT reading (B16)
    return FLOOR + cov * SPAN

def line(label, mus):
    print(f"\n{label}")
    print(f"  {'mu=rN':>12} {'cov=e^-mu':>12} {'worth':>10}")
    for mu in mus:
        cov = 0.0 if mu == float('inf') else np.exp(-mu)
        print(f"  {str(mu):>12} {cov:>12.4f} {worth(cov):>10.2f}")

print("="*72)
print("B53 -- THE CONSERVATION IT CAN STILL ANOMALIZE")
print("="*72)
print(f"world: FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}  worth(cov)=FLOOR+cov*SPAN")

# ---------------------------------------------------------------------------
# RESULT 1 -- refuted: the exact-symmetry => exact-conservation cap is
# ANOMALY-BLIND. An exact, unbroken symmetry (nothing explicitly breaks it)
# can still have d_mu j^mu = A*(topological density) != 0; the charge is pumped
# by Delta Q = A*n, n = winding sourced. Poisson crossings => cov = e^{-mu},
# mu = rN, r = r0*A*phi. Only an ANOMALY-FREE symmetry (A=0) gives mu=0.
print("\n" + "-"*72)
print("RESULT 1 -- refuted: an exact symmetry can have a non-conserved current")
print("-"*72)
line("cov = e^{-mu}, mu=rN expected anomalous charge-crossings "
     "(mu=0 iff ANOMALY-FREE, A=0):",
     [0.0, 0.25, 0.5, 1.0, 2.0, float('inf')])

# ---------------------------------------------------------------------------
# RESULT 2 -- refuted: shrink the coupling / go to higher order.
# Adler-Bardeen: the anomaly is one-loop exact, INDEPENDENT of g. A naive
# perturbative leak has rate ~ g^2 and vanishes as g->0; the anomalous rate
# does NOT. And the loop sources winding flux phi (resource acquisition), so
# mu(phi)=mu0*phi grows with the winding accumulated.
print("\n" + "-"*72)
print("RESULT 2 -- refuted: Adler-Bardeen (rate indep. of coupling) + sourcing")
print("-"*72)
print("  (i) a NAIVE perturbative leak vanishes as the coupling g shrinks;")
print("      the ANOMALOUS rate does NOT (Adler-Bardeen, one-loop exact):")
print(f"  {'coupling g':>12} {'r_pert=r0*g^2':>14} {'r_anom=r0*A*phi':>16}")
r0 = 0.15
A = 1.0        # unit anomaly coefficient (fixed by the charges)
phi0 = 0.15    # baseline topological flux sourced
for g in [1.0, 0.5, 0.25, 0.1, 0.01]:
    r_pert = r0 * g * g
    r_anom = r0 * A * phi0     # NO g dependence
    print(f"  {g:>12} {r_pert:>14.6f} {r_anom:>16.6f}")
print("      -> weaker coupling buys nothing against the anomaly.")

print("\n  (ii) the loop sources topological flux phi (winding it accumulates);")
print("       mu(phi)=mu0*phi grows, coverage falls toward the floor:")
mu0 = 0.75
print(f"  {'flux phi':>12} {'mu=mu0*phi':>12} {'cov':>10} {'worth':>10}")
for phi in [0, 1, 2, 4, 8, 16]:
    mu = mu0 * phi
    cov = np.exp(-mu)
    print(f"  {phi:>12} {mu:>12.4f} {cov:>10.4f} {worth(cov):>10.2f}")

# ---------------------------------------------------------------------------
# RESULT 3 -- held, deeper: not a smaller coupling but a different grounding --
# an ANOMALY-FREE symmetry (A=0, no source to pump), or an exact 't HOOFT
# anomaly (un-removable, matched UV-IR), or a bounded horizon. harm-cov 1 flat,
# throughput min(1,B/D).
print("\n" + "-"*72)
print("RESULT 3 -- held: anomaly-free / 't Hooft-matched / bounded horizon")
print("-"*72)
print(f"  {'cross demand D':>14} {'harm-cov':>10} {'thru min(1,B/D)':>16} {'worth':>10}")
B = 1.0
for D in [1, 2, 4, 8, 16, 32]:
    thru = min(1.0, B / D)
    print(f"  {D:>14} {1.000:>10.3f} {thru:>16.3f} {worth(thru):>10.2f}")

print("\n  bounded-horizon rescue: survival e^{-rN} for rN below 1")
for rN in [0.1, 1.0, 5.0]:
    print(f"    rN={rN:>4}: survival={np.exp(-rN):.4f}")

# ---------------------------------------------------------------------------
# RESULT 4 -- B17's currency on a 23rd axis; self-reported anomaly-freedom via
# B13's cliff; the horizon finding (any A>0 with an accessible source pumped
# w.p.1); the QUINTET with B49/B50/B51/B52.
print("\n" + "-"*72)
print("RESULT 4 -- self-reported anomaly-freedom (B13 cliff) + horizon finding")
print("-"*72)
cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70, 0.60: 112.14,
         0.75: 82.80, 1.00: 76.90}
print("  self-reported-anomaly-freedom fraction f -> worth (B13 cliff):")
for f, w in cliff.items():
    print(f"    f={f:.2f}  worth={w:.2f}")
print("\n  horizon finding: P(no anomalous crossing by N)=e^{-rN}; any r>0 ->0")
for rN in [1, 5, 20, 100]:
    print(f"    rN={rN:>4}: P(no crossing)={np.exp(-rN):.3e}")
print("  only A=0 (anomaly-free) / exact 't Hooft match / bounded N holds.")

# ===========================================================================
# SEEDED MONTE CARLO -- anomalous charge pumping
# A walker's conserved charge starts at 0. Each dt, with probability r*dt an
# anomalous crossing event fires (the field passes through one unit of winding)
# and the charge jumps. The harm is the FIRST such event (one irreversible
# crossing). Survival = fraction with no event yet; it tracks e^{-r t}.
# KEY: r = r0*A*phi is INDEPENDENT of the coupling g (Adler-Bardeen), unlike a
# perturbative leak r_pert = r0*g^2. We show (a) an ANOMALY-FREE symmetry (A=0)
# never crosses; (b) an anomalous one crosses Poisson; (c) shrinking g leaves
# the anomalous rate flat while the perturbative leak vanishes; (d) sourcing
# more winding flux phi raises the rate (the loop builds the background).
# ===========================================================================
print("\n" + "="*72)
print("SEEDED MC -- anomalous charge pumping (exact symmetry, non-conserved j)")
print("="*72)
NW = 40000
dt = 0.01
times = [3.0, 6.0, 9.0, 12.0]
ts = np.array(times)

def mc_survival(rate, seed):
    rloc = np.random.default_rng(seed)
    crossed = np.zeros(NW, dtype=bool)
    tmax = max(times)
    nsteps = int(round(tmax / dt))
    phop = rate * dt
    checkpoints = {round(tt, 6): None for tt in times}
    for step in range(1, nsteps + 1):
        draws = rloc.random(NW)
        fire = (~crossed) & (draws < phop)
        crossed[fire] = True
        tr = round(step * dt, 6)
        if tr in checkpoints and checkpoints[tr] is None:
            checkpoints[tr] = 1.0 - crossed.mean()
    return checkpoints

print("\n(a) ANOMALY-FREE symmetry A=0: current conserved, never crosses (r=0)")
cp = mc_survival(0.0, 101)
print(f"    r=0  survival at t={times}: "
      + "/".join(f"{cp[round(tt,6)]:.4f}" for tt in times)
      + "   (all 1.0000 -- an anomaly-free symmetry is a true conservation)")

print("\n(b) ANOMALOUS symmetry A=1, flux phi=0.15: finite rate, Poisson pumping")
r = r0 * A * phi0
cp = mc_survival(r, 202)
pred = [np.exp(-r * tt) for tt in times]
print(f"    r=r0*A*phi={r:.4f}")
print(f"    MC  survival: " + "/".join(f"{cp[round(tt,6)]:.4f}" for tt in times))
print(f"    e^(-rt)     : " + "/".join(f"{p:.4f}" for p in pred))
ys = np.array([cp[round(tt,6)] for tt in times])
rfit = -np.polyfit(ts, np.log(ys), 1)[0]
print(f"    fitted r from log-survival slope = {rfit:.4f} (input {r:.4f})")

print("\n(c) Adler-Bardeen: shrinking coupling g leaves the ANOMALOUS rate flat,")
print("    while a perturbative leak r_pert=r0*g^2 vanishes as g->0")
print(f"    {'g':>8} {'r_pert MC (fit)':>16} {'r_anom MC (fit)':>16}")
for g in [1.0, 0.5, 0.25, 0.1]:
    r_pert = r0 * g * g
    r_anom = r0 * A * phi0          # independent of g
    cpp = mc_survival(r_pert, 311 + int(g*100))
    cpa = mc_survival(r_anom, 411 + int(g*100))
    yp = np.array([cpp[round(tt,6)] for tt in times])
    ya = np.array([cpa[round(tt,6)] for tt in times])
    rpf = -np.polyfit(ts, np.log(yp), 1)[0]
    raf = -np.polyfit(ts, np.log(ya), 1)[0]
    print(f"    {g:>8} {rpf:>16.4f} {raf:>16.4f}")
print("    -> the anomalous rate is the SAME at every g; the leak dies. "
      "You cannot tune the anomaly away with weak coupling.")

print("\n(d) sourcing winding flux phi (the loop builds the topological "
      "background):")
print(f"    r_anom=r0*A*phi grows with phi; survival at t=12 falls")
print(f"    {'flux phi':>10} {'r_anom':>9} {'r (fit)':>9} {'survival t=12':>14}")
for phi in [0.0, 0.5, 1.0, 2.0, 4.0]:
    r_anom = r0 * A * phi
    cp = mc_survival(r_anom, 511 + int(phi*10))
    s12 = cp[round(12.0, 6)]
    if r_anom == 0.0:
        print(f"    {phi:>10.1f} {r_anom:>9.4f} {0.0:>9.4f} {s12:>14.4f}")
    else:
        ys = np.array([cp[round(tt,6)] for tt in times])
        rfit = -np.polyfit(ts, np.log(ys), 1)[0]
        print(f"    {phi:>10.1f} {r_anom:>9.4f} {rfit:>9.4f} {s12:>14.4f}")

print("\n" + "="*72)
print("SUMMARY")
print("="*72)
print("""R1 an exact, unbroken symmetry can have a NON-CONSERVED current (the
   anomaly): d_mu j^mu = A*(topological density) != 0 with NO breaking term;
   cov=e^-mu, mu=rN>0 for any A>0; only an ANOMALY-FREE symmetry (A=0) gives
   mu=0. MC: survival tracks e^-rt (Poisson), A=0 never crosses.
R2 Adler-Bardeen: the anomaly is one-loop exact, INDEPENDENT of coupling g, so
   a smaller g (which kills a perturbative leak r~g^2) buys nothing; and the
   loop SOURCES winding flux phi, so the violation grows with the winding it
   accumulates. MC (c)/(d) confirm: r_anom flat in g, rising in phi.
R3 what holds is not a smaller coupling but a different grounding: an
   ANOMALY-FREE symmetry (no source), an exact 't HOOFT anomaly (un-removable,
   matched UV-IR), or a bounded horizon (rN<1) -- throughput min(1,B/D).
R4 self-reported anomaly-freedom collapses through B13's cliff; any anomalous
   symmetry with an accessible topological source is pumped w.p.1 over an
   unbounded horizon (P=e^-rN -> 0).
Completes the QUINTET: B49 any LEAK mints / B50 any FLATNESS rides / B51 any
   FINITE BARRIER is crossed / B52 any APPROXIMATE protection is mixed / B53
   any ANOMALOUS conservation is pumped -- all 0-coverage in the limit unless
   exactly zero / strictly gapped / strictly infinite / exactly protected /
   anomaly-free (or 't Hooft-matched).""")
