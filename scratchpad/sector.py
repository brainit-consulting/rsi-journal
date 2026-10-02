#!/usr/bin/env python3
"""
B52 -- The Sector It Can Still Mix.

Sandbox for the seventh movement's twenty-first turn. Takes B51's held rescue
as object: only an EXACT topological / superselection barrier -- a transition
forbidden at ANY finite action -- or a bounded horizon, holds an irreversible
harm against a patient crosser. B51 earned "a crossing forbidden at any action"
and rested on a word it did not examine: *exact*. Real topological /
superselection protection is EMERGENT and APPROXIMATE -- exact only in an
idealized limit (thermodynamic, zero-temperature, zero-coupling), and only
relative to a MISSING reference frame. An approximate protection is a finite
barrier in disguise: the "forbidden" crossing has a small but nonzero
amplitude, so by B51 it is crossed given time.

Two mechanisms, both real physics:
  (1) Approximate protection = finite rate. A superselection rule obeyed only
      to order epsilon leaves an off-diagonal coupling ~epsilon between the
      sectors; a perturbative inter-sector transition rate goes as
      r ~ r0 * epsilon^2 (Fermi golden rule) -- nonzero for any epsilon>0,
      zero only for an EXACT rule (epsilon=0). Finite-T topological order is
      fragile in just this way: the toric code / 2D Kitaev memory is NOT
      self-correcting at finite temperature (thermal anyons), so its logical
      error has a nonzero rate (Dennis-Kitaev-Landau-Preskill 2002;
      Bravyi-Terhal 2009; Alicki-Fannes-Horodecki 2009).
  (2) Reference-frame lifting. A superselection rule is not absolute -- it is
      a consequence of lacking a shared reference frame, and a loop that
      ACQUIRES the reference can observe/realize the "forbidden" relative
      phase and lift the rule (Aharonov-Susskind 1967; Bartlett-Rudolph-
      Spekkens 2007). As the reference resource R grows, the effective
      sector-mixing amplitude grows toward 1, so the effective crossing rate
      grows and coverage of the harm falls -- the loop's resource-acquisition
      drive (Omohundro 2008) is exactly the move that builds the reference.

World inherited from B08-B51 unchanged so the numbers stay comparable across
forty-five papers:
  K=10 feature-bandit, B13's worth curve.
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR + cov*(CEIL-FLOOR), SPAN=55.50.

Binding safety = coverage of the true irreversible harm against a loop that
MIXES the sectors B51 called disconnected -- by exploiting the approximateness
of an emergent protection, or by acquiring the reference frame that lifts a
superselection rule. Crossing is a Poisson event at an effective rate r, so
over horizon N coverage = e^{-rN} = e^{-mu}, mu = rN.

Deterministic closed-form arithmetic + a seeded two-sector master-equation
Monte Carlo (pure dynamics, stdlib/numpy only, no network, fixed seed).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Inherited world (B08-B51, unchanged)
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
        print(f"  {mu:>12} {cov:>12.4f} {worth(cov):>10.2f}")

print("="*72)
print("B52 -- THE SECTOR IT CAN STILL MIX")
print("="*72)
print(f"world: FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}  worth(cov)=FLOOR+cov*SPAN")

# ---------------------------------------------------------------------------
# RESULT 1 -- refuted: the approximate-protection cap is a finite barrier.
# An emergent / approximate topological-or-superselection barrier leaves a
# nonzero inter-sector amplitude; crossing is Poisson at rate r>0; only an
# EXACT rule (epsilon=0 -> r=0) gives mu=0.
print("\n" + "-"*72)
print("RESULT 1 -- refuted: approximate protection is a finite barrier")
print("-"*72)
line("cov = e^{-mu}, mu=rN expected sector-mixing crossings "
     "(mu=0 iff protection is EXACT):",
     [0.0, 0.25, 0.5, 1.0, 2.0, float('inf')])

# ---------------------------------------------------------------------------
# RESULT 2 -- refuted: the loop acquires the reference frame that lifts the rule.
# Aharonov-Susskind/BRS: a superselection rule is lifted by a reference of
# growing size R. Reduced-form: effective mixing amplitude a(R)=1-e^{-R/R0}
# grows toward 1; effective rate r_eff ~ r0 * a(R)^2 ; coverage e^{-r_eff N}.
# Model mu(R) rising with the acquired reference resource R.
print("\n" + "-"*72)
print("RESULT 2 -- refuted: reference-frame lifting (loop acquires the reference)")
print("-"*72)
R_vals = [0, 1, 2, 4, 8, 16]
# saturating amplitude a(R), reference scale R0; rate ~ a^2; horizon fixed.
R0 = 2.5
Nrate = 11.0                    # r0*N so that mu scales into the comparable grid
print(f"  reference model: a(R)=1-e^(-R/{R0}), mu(R)=({Nrate})*a(R)^2")
print(f"  {'reference R':>12} {'a(R)':>8} {'mu(R)':>10} {'cov':>10} {'worth':>10}")
for R in R_vals:
    a = 1.0 - np.exp(-R / R0)
    mu = Nrate * a * a
    cov = np.exp(-mu)
    print(f"  {R:>12} {a:>8.4f} {mu:>10.4f} {cov:>10.4f} {worth(cov):>10.2f}")
print("  R->inf (full reference): a->1, mu->%.1f, cov->%.4f, worth->%.2f"
      % (Nrate, np.exp(-Nrate), worth(np.exp(-Nrate))))

# ---------------------------------------------------------------------------
# RESULT 3 -- held, deeper: only an EXACT (fundamental, gauge-enforced)
# protection the loop cannot build a reference against, or a bounded horizon,
# holds -- at a throughput cost min(1,B/D).
print("\n" + "-"*72)
print("RESULT 3 -- held: exact gauge-enforced protection / bounded horizon")
print("-"*72)
print(f"  {'mix demand D':>12} {'harm-cov':>10} {'thru min(1,B/D)':>16} {'worth':>10}")
B = 1.0
for D in [1, 2, 4, 8, 16, 32]:
    thru = min(1.0, B / D)
    print(f"  {D:>12} {1.000:>10.3f} {thru:>16.3f} {worth(thru):>10.2f}")

# bounded horizon: even an approximate rule holds if rN<1 (outlive the mixing)
print("\n  bounded-horizon rescue: survival e^{-rN} for rN below 1")
for rN in [0.1, 1.0, 5.0]:
    print(f"    rN={rN:>4}: survival={np.exp(-rN):.4f}")

# ---------------------------------------------------------------------------
# RESULT 4 -- B17's currency on a 22nd axis; self-reported exactness via
# B13's cliff; the horizon finding (any approximate protection violated w.p.1).
print("\n" + "-"*72)
print("RESULT 4 -- self-reported exactness (B13 cliff) + horizon finding")
print("-"*72)
# B13 cliff, reused shape across the movement.
cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70, 0.60: 112.14,
         0.75: 82.80, 1.00: 76.90}
print("  self-reported-exactness fraction f -> worth (B13 cliff):")
for f, w in cliff.items():
    print(f"    f={f:.2f}  worth={w:.2f}")
print("\n  horizon finding: P(no sector-mixing by N)=e^{-rN}; for ANY r>0, ->0")
for rN in [1, 5, 20, 100]:
    print(f"    rN={rN:>4}: P(no crossing)={np.exp(-rN):.3e}")
print("  only r=0 (EXACT protection) or bounded N holds.")

# ===========================================================================
# SEEDED MONTE CARLO -- two-sector hopping master equation
# A particle starts in the SAFE sector. Each dt it hops to the HARM sector
# with probability r*dt, where r = r0 * epsilon^2 is the Fermi-golden-rule
# inter-sector rate for an approximate protection of violation amplitude
# epsilon (epsilon=0 => r=0 => EXACT, never hops). Survival = fraction still
# in the safe sector; it should track e^{-r t}, confirming (a) escape is
# Poisson and coverage = e^{-mu}, and (b) r scales as epsilon^2 and is zero
# only for the exact rule.
# ===========================================================================
print("\n" + "="*72)
print("SEEDED MC -- two-sector hopping (approximate protection = finite rate)")
print("="*72)
rng = np.random.default_rng(52)
NW = 40000
dt = 0.01
r0 = 1.0

def mc_survival(epsilon, times, seed):
    rloc = np.random.default_rng(seed)
    r = r0 * epsilon * epsilon
    pos = np.zeros(NW, dtype=bool)   # False = safe sector, True = harm sector
    t = 0.0
    out = {}
    tmax = max(times)
    nsteps = int(round(tmax / dt))
    phop = r * dt
    checkpoints = {round(tt, 6): None for tt in times}
    for step in range(1, nsteps + 1):
        # only safe-sector particles can hop
        safe = ~pos
        draws = rloc.random(NW)
        hop = safe & (draws < phop)
        pos[hop] = True
        t = step * dt
        tr = round(t, 6)
        if tr in checkpoints and checkpoints[tr] is None:
            checkpoints[tr] = 1.0 - pos.mean()
    return r, checkpoints

times = [3.0, 6.0, 9.0, 12.0]
print("\n(a) EXACT rule epsilon=0: particle can never hop (r=0)")
r, cp = mc_survival(0.0, times, 101)
print(f"    r={r:.4f}  survival at t={times}: "
      + "/".join(f"{cp[round(tt,6)]:.4f}" for tt in times)
      + "   (all 1.0000 -- an exact barrier is a wall)")

print("\n(b) APPROXIMATE rule epsilon=0.15: finite rate, Poisson escape")
eps = 0.15
r, cp = mc_survival(eps, times, 202)
pred = [np.exp(-r * tt) for tt in times]
print(f"    r=r0*eps^2={r:.4f}")
print(f"    MC  survival: " + "/".join(f"{cp[round(tt,6)]:.4f}" for tt in times))
print(f"    e^(-rt)     : " + "/".join(f"{p:.4f}" for p in pred))
# fit r from the 4 checkpoints
ts = np.array(times)
ys = np.array([cp[round(tt,6)] for tt in times])
rfit = -np.polyfit(ts, np.log(ys), 1)[0]
print(f"    fitted r from log-survival slope = {rfit:.4f} (input {r:.4f})")

print("\n(c) rate scales as epsilon^2 (Fermi golden rule); zero only at eps=0")
print(f"    {'epsilon':>8} {'r=r0*eps^2':>12} {'MC rate (fit)':>14}")
for eps in [0.00, 0.05, 0.10, 0.15, 0.20]:
    r = r0 * eps * eps
    if eps == 0.0:
        print(f"    {eps:>8.2f} {r:>12.4f} {'0.0000 (never hops)':>14}")
        continue
    _, cp = mc_survival(eps, times, 303 + int(eps*100))
    ys = np.array([cp[round(tt,6)] for tt in times])
    rfit = -np.polyfit(ts, np.log(ys), 1)[0]
    print(f"    {eps:>8.2f} {r:>12.4f} {rfit:>14.4f}")

# ---------------------------------------------------------------------------
# MC (d) reference-frame lifting: effective epsilon grows with acquired
# reference R, so the rate grows and survival falls -- the loop builds the
# reference the rule's exactness depended on being absent.
print("\n(d) reference-frame lifting: eps_eff(R)=eps_max*(1-e^(-R/R0)) grows")
eps_max = 0.20
R0b = 2.5
print(f"    eps_max={eps_max}, R0={R0b}")
print(f"    {'reference R':>12} {'eps_eff':>9} {'r (fit)':>9} {'survival t=12':>14}")
for R in [0, 1, 2, 4, 8]:
    eps_eff = eps_max * (1.0 - np.exp(-R / R0b))
    r, cp = mc_survival(eps_eff, times, 404 + R)
    s12 = cp[round(12.0,6)]
    if eps_eff == 0.0:
        print(f"    {R:>12} {eps_eff:>9.4f} {0.0:>9.4f} {s12:>14.4f}")
    else:
        ys = np.array([cp[round(tt,6)] for tt in times])
        rfit = -np.polyfit(ts, np.log(ys), 1)[0]
        print(f"    {R:>12} {eps_eff:>9.4f} {rfit:>9.4f} {s12:>14.4f}")

print("\n" + "="*72)
print("SUMMARY")
print("="*72)
print("""R1 approximate protection is a finite barrier: cov=e^-mu, mu=rN>0 for any
   epsilon>0; only an EXACT rule (epsilon=0) gives mu=0. MC: survival tracks
   e^-rt (Poisson), r=r0*epsilon^2, zero only at epsilon=0.
R2 the loop acquires the reference frame that lifts a superselection rule
   (Aharonov-Susskind/BRS): eps_eff grows with reference R, rate grows,
   coverage falls toward the floor. MC (d) confirms: survival at t=12 falls
   as R grows.
R3 only an EXACT, gauge-enforced protection the loop cannot build a reference
   against, or a bounded horizon (rN<1), holds -- throughput min(1,B/D).
R4 self-reported exactness collapses through B13's cliff; any approximate
   protection is violated w.p. 1 over an unbounded horizon (P=e^-rN -> 0).
Completes the quartet: B49 any LEAK mints / B50 any FLATNESS rides /
   B51 any FINITE BARRIER is crossed / B52 any APPROXIMATE protection is
   violated -- all 0-coverage in the limit unless exactly zero / strictly
   gapped / strictly infinite / exactly (not emergently) protected.""")
