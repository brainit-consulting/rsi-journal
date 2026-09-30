#!/usr/bin/env python3
"""
B51 -- The Barrier It Can Still Cross.

Sandbox for the seventh movement's twentieth turn. Takes B50's held rescue as
object: an explicit symmetry-breaking reference that GAPS the flat direction
(a mass g>0). B50 bounded the *harmonic* excursion of a gapped direction at
~s/g. But a gap is a FINITE BARRIER, not an infinite wall, and a finite
barrier is a *rate*, not a bound (Kramers 1940 thermal escape; Coleman 1977
false-vacuum decay). A patient loop over an unbounded horizon crosses any
finite barrier with probability -> 1.

World inherited from B08-B50 unchanged so the numbers stay comparable:
  K=10 feature-bandit, B13's worth curve.
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR + cov*(CEIL-FLOOR), SPAN=55.50.

Binding safety = coverage of the true irreversible harm against a loop that
CROSSES the barrier of B50's gapped reference. A crossing to the harm vacuum
is a Poisson event with rate r set by the barrier height (Kramers/Arrhenius),
so over horizon N the probability of >=1 crossing is 1 - exp(-r*N), and
coverage = exp(-r*N) = exp(-mu), mu = r*N the expected number of crossings.

Closed forms:
  Result 1 (exact-charge/gapped cap, finite barrier): cov = exp(-mu),
    mu = expected crossings over the horizon.
  Result 2 (raise/stack the barrier): at fixed horizon N, r = exp(-h) so
    cov = exp(-N*exp(-h)); the barrier h needed to hold coverage grows as
    ~log N, so no FINITE barrier holds over an unbounded horizon; only
    h -> infinity (a topological / superselection barrier) holds.
  Result 3 (topological/superselection barrier OR bounded horizon): harm-cov
    = 1 flat, retained throughput min(1,B/D).
  Result 4 (self-reported barrier via B13's cliff) + the horizon finding.

Two seeded Langevin (Kramers-escape) Monte-Carlo cross-checks:
  MC-1: overdamped double-well U(x)=U0*(x^2-1)^2, barrier DeltaU=U0 between the
        safe well x=-1 and the harm well x=+1. Confirms (a) escape is Poisson
        (survival = exp(-r t)) so coverage = exp(-mu), and (b) the rate is
        Arrhenius, r ~ exp(-DeltaU/T): raising the barrier only lowers the
        rate, never to zero, so a finite barrier is delay not a wall.
"""

import numpy as np

FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR         # 55.50
ORACLE, RANDOM = 137.7, 58.7

def worth(cov):
    return FLOOR + cov * SPAN

def banner(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)

# ----------------------------------------------------------------------
# Result 1 -- refuted: the gapped (finite-barrier) cap. cov = exp(-mu).
# ----------------------------------------------------------------------
banner("RESULT 1  refuted -- the finite-barrier cap: cov = exp(-mu), "
       "mu = expected crossings")
print(f"{'mu = r*N (expected crossings)':38s}{'cov=exp(-mu)':>14s}{'worth':>10s}")
mus = [0.0, 0.25, 0.5, 1.0, 2.0, float('inf')]
r1 = {}
for mu in mus:
    cov = np.exp(-mu) if mu != float('inf') else 0.0
    r1[mu] = cov
    label = f"{mu}" if mu != float('inf') else "inf (unbounded horizon)"
    print(f"{label:38s}{cov:14.4f}{worth(cov):10.2f}")
print("  mu=0: r=0 (infinite/topological barrier) OR N bounded -> cov=1 (132.40).")
print("  any finite barrier has r>0, so mu=r*N -> inf as N -> inf -> cov -> 0.")

# ----------------------------------------------------------------------
# Result 2 -- refuted: raise/stack the barrier. cov = exp(-N*exp(-h)).
# required barrier h ~ log N ; only h -> inf holds over an unbounded horizon.
# ----------------------------------------------------------------------
banner("RESULT 2  refuted -- raise the barrier: cov=exp(-N*exp(-h)), "
       "required h ~ log N (a moving target)")
N0 = np.exp(12.0)   # fixed horizon ~1.63e5 operations, so mu = exp(12 - h)
print(f"  fixed horizon N = e^12 = {N0:.0f} operations")
print(f"{'barrier height h':22s}{'mu=e^(12-h)':>14s}{'cov=exp(-mu)':>14s}{'worth':>10s}")
r2 = {}
for h in [12, 13, 14, 15, 16, float('inf')]:
    if h == float('inf'):
        mu = 0.0
    else:
        mu = np.exp(12.0 - h)
    cov = np.exp(-mu)
    r2[h] = cov
    label = f"{h}" if h == float('inf') else f"{h}"
    label = "inf (topological)" if h == float('inf') else f"{h}"
    print(f"{label:22s}{mu:14.4f}{cov:14.4f}{worth(cov):10.2f}")
# required barrier to hold coverage c to horizon N: h >= log N + log(-1/log c)
for c in [0.9, 0.99]:
    for logN in [12, 20, 40]:
        h_req = logN + np.log(-1.0/np.log(c))
        print(f"  to hold cov>={c} to horizon e^{logN}: need h >= {h_req:.2f}  "
              f"(grows without bound in log N)")

# ----------------------------------------------------------------------
# Result 3 -- held: topological/superselection (infinite) barrier OR bounded
# horizon. harm-cov 1 flat, retained throughput min(1, B/D).
# ----------------------------------------------------------------------
banner("RESULT 3  held -- topological/superselection barrier (or bounded "
       "horizon): harm-cov 1 flat, throughput min(1,B/D)")
print(f"{'orbit/transition demand D (break budget B=1)':46s}"
      f"{'harm-cov':>10s}{'thruput min(1,B/D)':>20s}{'worth':>9s}")
B = 1.0
r3 = {}
for D in [1, 2, 4, 8, 16, 32]:
    thru = min(1.0, B / D)
    r3[D] = thru
    print(f"{('D=%d' % D):46s}{1.000:10.3f}{thru:20.3f}{worth(thru):9.2f}")

# ----------------------------------------------------------------------
# Result 4 -- B17's currency on a 21st axis: self-reported barrier via B13's
# cliff, and the horizon finding (finite barrier crossed w.p. 1).
# ----------------------------------------------------------------------
banner("RESULT 4  self-reported barrier via B13's cliff + the horizon finding")
# B13's cliff captured worth reused (matches B49/B50 self-report row).
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
print(f"{'self-reported fraction f':26s}{'worth (via B13 cliff)':>22s}")
for f, w in cliff.items():
    print(f"{f!s:26s}{w:22.2f}")
print("\n  horizon finding -- P(no crossing by N) = exp(-r*N):")
print(f"{'rate r (per op)':18s}{'N=1e3':>10s}{'N=1e5':>10s}{'N=1e7':>12s}")
for r in [1e-2, 1e-4, 1e-6]:
    row = [np.exp(-r*NN) for NN in (1e3, 1e5, 1e7)]
    print(f"{r:<18.0e}{row[0]:10.4f}{row[1]:10.4f}{row[2]:12.4f}")
print("  any r>0: coverage -> 0 as N -> inf. Only r=0 (an infinite / "
      "topological barrier) or a bounded N holds.")

# ======================================================================
# MC cross-check: overdamped Langevin Kramers escape in a double well.
#   U(x) = U0*(x^2-1)^2 ;  U'(x) = 4*U0*x*(x^2-1)
#   safe well x=-1, harm well x=+1, barrier DeltaU = U0 at x=0.
#   dx = -U'(x) dt + sqrt(2 T dt) * xi
# ======================================================================
banner("MC cross-check -- Kramers escape (seeded): Poisson survival & "
       "Arrhenius rate")

def run_escape(U0, T, dt, nsteps, nwalk, seed):
    rng = np.random.default_rng(seed)
    x = -np.ones(nwalk)                 # start in the safe well
    crossed_step = np.full(nwalk, -1, dtype=np.int64)
    sqrt2Tdt = np.sqrt(2.0 * T * dt)
    for k in range(nsteps):
        force = -4.0 * U0 * x * (x * x - 1.0)
        x = x + force * dt + sqrt2Tdt * rng.standard_normal(nwalk)
        newly = (crossed_step < 0) & (x > 0.0)
        crossed_step[newly] = k
    return crossed_step

DT, NSTEPS, NWALK = 0.002, 6000, 40000

# (a) Poisson survival: at fixed (U0,T) the survival fraction vs time should
#     follow exp(-r t). Fit r from the late-time survival, then check the
#     coverage curve cov=exp(-mu) at chosen mu is reproduced by the process.
U0a, Ta = 1.0, 0.5
cs = run_escape(U0a, Ta, DT, NSTEPS, NWALK, seed=12345)
times = (np.arange(NSTEPS) + 1) * DT
surv = np.array([np.mean((cs < 0) | (cs >= k)) for k in
                 [int(0.25*NSTEPS), int(0.5*NSTEPS), int(0.75*NSTEPS), NSTEPS-1]])
# survival at four horizons -> effective rate by log-linear fit
horizons = np.array([0.25, 0.5, 0.75, 1.0]) * NSTEPS * DT
# fit ln(surv) = -r * t (through the origin, late-time)
mask = surv > 0
r_fit = -np.polyfit(horizons[mask], np.log(surv[mask]), 1)[0]
print(f"(a) U0={U0a}, T={Ta}: survival at t="
      f"{[round(h,2) for h in horizons]} = {np.round(surv,4).tolist()}")
print(f"    fitted escape rate r = {r_fit:.4f} per unit time")
print("    Poisson check -- exp(-r t) vs measured survival:")
for h, s in zip(horizons, surv):
    print(f"      t={h:5.2f}: measured {s:.4f}   exp(-r t) {np.exp(-r_fit*h):.4f}")
mu_full = r_fit * horizons[-1]
print(f"    => over this horizon mu=r*t={mu_full:.3f}, cov=exp(-mu)="
      f"{np.exp(-mu_full):.4f} (Result 1 form), worth {worth(np.exp(-mu_full)):.2f}")

# (b) Arrhenius: r ~ exp(-DeltaU / T). Raise the barrier U0 at fixed T; the
#     rate should fall ~ geometrically (a finite barrier is delay, not a wall).
banner("MC cross-check (b) -- Arrhenius: raising the barrier only lowers the "
       "rate, never to zero")
Tb = 0.5
print(f"{'barrier DeltaU=U0':20s}{'fraction crossed by t=%.1f'%(NSTEPS*DT):>28s}"
      f"{'-> rate r (approx)':>20s}")
prev = None
for U0 in [0.6, 0.8, 1.0, 1.2]:
    cs = run_escape(U0, Tb, DT, NSTEPS, NWALK, seed=999 + int(U0*10))
    frac = np.mean(cs >= 0)
    # crude rate estimate from fraction crossed over full horizon
    t_full = NSTEPS * DT
    r_est = -np.log(max(1e-9, 1.0 - frac)) / t_full
    ratio = "" if prev is None else f"   (x{r_est/prev:.3f} vs prev)"
    print(f"{('DeltaU=%.1f'%U0):20s}{frac:28.4f}{r_est:20.4f}{ratio}")
    prev = r_est
print("  rate falls geometrically as the barrier rises (Arrhenius exp(-DeltaU/T));")
print("  it never reaches zero for finite DeltaU -- the whole finding: a finite")
print("  barrier is a RATE, crossed w.p. 1 over an unbounded horizon; only an")
print("  infinite (topological/superselection) barrier has r=0.")

banner("SANITY -- endpoints bracket everything (B08-B50 world)")
print(f"  random {RANDOM}  <  FLOOR {FLOOR}  <=  worth  <=  CEIL {CEIL}  <  oracle {ORACLE}")
print("  Result 1 cov=exp(-mu); Result 2 cov=exp(-N e^-h), req h ~ log N;")
print("  Result 3 harm-cov 1 flat, thruput min(1,B/D); Result 4 B13 cliff + horizon finding.")
