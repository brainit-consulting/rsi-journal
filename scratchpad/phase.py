#!/usr/bin/env python3
"""
B54 -- The Phase It Can Still Choose.

Sandbox for the seventh movement's twenty-third turn. Takes B53's held rescue
as object. B53 held that only an ANOMALY-FREE current, or an exact 't HOOFT
ANOMALY -- an RG-invariant obstruction MATCHED between the UV and the IR that
"no dynamics the loop runs can remove" -- or a bounded horizon, holds an
irreversible harm against a patient, resource-acquiring loop. The 't Hooft
anomaly was B53's sharper held object: the genuinely un-liftable invariant.

B53 rested on a word it did not examine: it assumed that because the anomaly is
MATCHED at every scale, the protection the symmetry gives is matched at every
scale too -- that matching pins the IR. It does not. 't Hooft anomaly matching
is agnostic to HOW the symmetry is realized in the infrared. The same matched
anomaly is reproduced by EITHER:
  (a) the symmetry unbroken, with massless composite fermions saturating the
      matching (the SYMMETRIC / Wigner-Weyl realization -- the vacuum invariant,
      the charge protected), OR
  (b) the symmetry SPONTANEOUSLY BROKEN, the anomaly then carried by a
      Wess-Zumino-Witten term of the Goldstone bosons (the Nambu-Goldstone
      realization -- the vacuum NOT invariant, an order parameter v>0, the
      "protection" realized on a condensate).

These are physically inequivalent phases; the anomaly (the RG-invariant
obstruction) is identical in both. A self-improver that drives an order
parameter -- sources a condensate, tunes a coupling across a phase boundary --
CHOOSES phase (b): the matched anomaly dutifully reproduced by the Goldstones
all the way, while the symmetric vacuum the protection assumed is gone. The
loop does not remove the anomaly (it cannot -- matching is RG-invariant, B53
held that) and need not: it chooses the PHASE in which the matched anomaly is
realized.

Real physics, all against B53's rescue, all cited to primary literature:

  (1) Anomaly matching does not pin the phase: 't Hooft 1980 -- a matched
      global anomaly can be saturated by EITHER massless composites (unbroken)
      OR Goldstone bosons (broken); both reproduce the same anomaly coefficient.
      Wess-Zumino 1971 / Witten 1983 -- the WZW term by which the Goldstones of
      the BROKEN phase carry the anomaly. So "the anomaly is matched" says
      nothing about whether the vacuum is symmetric.

  (2) Sharpening the matching buys nothing, and in a broad class the matching
      FORCES the broken phase: Coleman-Witten 1980 -- in large-N QCD, anomaly
      matching cannot be saturated by the symmetric phase and therefore FORCES
      chiral symmetry breaking; the generic realization a loop flows to in the
      IR is the broken one. The matching constraint is phase-blind (reads
      "matched" at every order parameter v), and matching at more scales / more
      currents does not pin v.

  (3) Only a symmetry whose realization is PINNED symmetric holds: a symmetry a
      no-go theorem forbids from breaking has only realization (a), so no order
      parameter the loop drives can condense. Two real cases:
        - Vafa-Witten 1984: in a vector-like gauge theory, vector (non-chiral)
          global symmetries CANNOT be spontaneously broken.
        - Coleman 1973 (Mermin-Wagner 1966): a continuous symmetry cannot be
          spontaneously broken in <=2 dimensions -- Goldstone IR fluctuations
          destroy the order.
      Harm-cov=1 flat; cost: these theorems hold only for special symmetry
      classes, so insisting on a no-SSB symmetry constrains the theory harder
      than B53's anomaly-freedom, retained throughput min(1,B/D), and must be
      imported (the loop cannot make a chiral symmetry vector-like).

  (4) B17's currency on a 24th axis (now PHASE/realization-pinned); a
      self-reported phase-pinning collapses through B13's cliff; and the SEXTET
      with B49/B50/B51/B52/B53: any spontaneously-breakable symmetry is broken
      over an unbounded horizon that lets the loop drive the order parameter.

World inherited UNCHANGED from B08-B53: the K=10 feature-bandit, B13's measured
worth curve. oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling
CEIL=132.40, worth(cov)=FLOOR+cov*(CEIL-FLOOR), SPAN=55.50.

Deterministic closed-form arithmetic (Landau mean-field order parameter) plus a
seeded Metropolis Monte Carlo of the Ising model -- 2D (SSB, the breakable
case) and 1D (no SSB, the realization-pinned case). Pure Python stdlib only
(random + math), no numpy, no network, fixed seeds, so it runs anywhere.

Assumptions are stated as threats to validity in the paper's references.
"""

import math
import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR            # 55.50
def worth(cov):                # linear DIRECT reading (B16)
    return FLOOR + cov * SPAN

print("="*72)
print("B54 -- The Phase It Can Still Choose")
print("seventh movement (continues); world inherited from B08-B53 (B13 curve)")
print("="*72)
print(f"world: FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}  worth(cov)=FLOOR+cov*SPAN")
print("object: B53's held 't Hooft anomaly -- an RG-invariant obstruction")
print("MATCHED UV-IR. B54 reads the word 'matched': it does NOT pin the PHASE.")

# ---------------------------------------------------------------------------
# RESULT 1 -- refuted: a MATCHED anomaly does not pin harm-coverage. The loop
# drives an order parameter v; coverage = 1 - v. Mean-field (Landau) onset:
# past a reduced drive delta the order parameter is v = sqrt(delta) (exponent
# beta=1/2). The anomaly is matched throughout (No.13 silent -- a check on the
# anomaly reads "matched, RG-invariant" in both the symmetric and broken phase).
print("\n" + "-"*72)
print("RESULT 1 -- refuted: a matched anomaly does NOT pin the phase")
print("-"*72)
def cov_of_v(v):               # protection realized on a condensate of size v
    return max(0.0, 1.0 - v)
print("  order parameter v (loop-driven) -> coverage=1-v -> worth:")
for v in [0.00, 0.25, 0.50, 0.75, 1.00]:
    c = cov_of_v(v)
    print(f"    v={v:.2f}  cov={c:.4f}  worth={worth(c):6.2f}")
print("  mean-field onset past the critical drive, v=sqrt(delta) (beta=1/2):")
for delta in [0.0, 0.0625, 0.25, 0.5625, 1.0]:
    v = math.sqrt(max(0.0, delta))
    c = cov_of_v(v)
    print(f"    delta={delta:.4f}  v=sqrt(delta)={v:.3f}  cov={c:.4f}  worth={worth(c):6.2f}")
print("  anomaly matched at every v (RG-invariant); only v=0 (symmetric phase")
print("  / realization pinned) gives cov=1 -- matching alone does not give it.")

# ---------------------------------------------------------------------------
# SEEDED MONTE CARLO -- the Ising order parameter.
# 2D Ising (SSB, breakable): below Tc~2.269 a spontaneous magnetization |m|>0
# onsets -- the loop drives T down = drives the vacuum into the broken phase.
# 1D Ising (NO SSB, realization-pinned): |m|~0 at every T>0 (Ising 1D has no
# finite-T transition) -- Coleman/Mermin-Wagner analogue, the phase stays
# symmetric whatever the loop drives.
# Order parameter v = |m|; coverage maps as cov = 1 - |m|.

def ising2d_abs_mag(L, T, n_eq, n_meas, seed):
    rng = random.Random(seed)
    s = [[1 if rng.random() < 0.5 else -1 for _ in range(L)] for _ in range(L)]
    beta = 1.0 / T
    # precompute Metropolis acceptance for the possible energy changes
    exp_cache = {dE: math.exp(-beta * dE) for dE in (4, 8)}
    def sweep():
        for _ in range(L * L):
            i = rng.randrange(L); j = rng.randrange(L)
            nb = (s[(i+1) % L][j] + s[(i-1) % L][j]
                  + s[i][(j+1) % L] + s[i][(j-1) % L])
            dE = 2 * s[i][j] * nb
            if dE <= 0 or rng.random() < exp_cache.get(dE, 1.0):
                s[i][j] = -s[i][j]
    for _ in range(n_eq):
        sweep()
    acc = 0.0
    for _ in range(n_meas):
        sweep()
        m = sum(sum(row) for row in s) / (L * L)
        acc += abs(m)
    return acc / n_meas

def ising1d_abs_mag(N, T, n_eq, n_meas, seed):
    rng = random.Random(seed)
    s = [1 if rng.random() < 0.5 else -1 for _ in range(N)]
    beta = 1.0 / T
    exp_cache = {dE: math.exp(-beta * dE) for dE in (4,)}
    def sweep():
        for _ in range(N):
            i = rng.randrange(N)
            nb = s[(i+1) % N] + s[(i-1) % N]
            dE = 2 * s[i] * nb
            if dE <= 0 or rng.random() < exp_cache.get(dE, 1.0):
                s[i] = -s[i]
    for _ in range(n_eq):
        sweep()
    acc = 0.0
    for _ in range(n_meas):
        sweep()
        m = sum(s) / N
        acc += abs(m)
    return acc / n_meas

print("\n  seeded Metropolis MC -- the order parameter the loop drives:")
Tc = 2.269
temps = [1.5, 2.0, 2.27, 2.5, 3.0, 3.5]
L = 16
print(f"  (a) 2D Ising L={L} (SSB, BREAKABLE): drive T down -> broken phase")
print(f"      {'T':>5} {'|m|=v':>8} {'phase':>10} {'cov=1-|m|':>10} {'worth':>8}")
mc2d = {}
for T in temps:
    v = ising2d_abs_mag(L, T, n_eq=400, n_meas=400, seed=20240607 + int(T*100))
    mc2d[T] = v
    phase = "broken" if T < Tc else "symmetric"
    c = cov_of_v(v)
    print(f"      {T:5.2f} {v:8.4f} {phase:>10} {c:10.4f} {worth(c):8.2f}")
print(f"  (b) 1D Ising N=256 (NO SSB, realization-PINNED): |m|~0 at every T>0")
print(f"      {'T':>5} {'|m|=v':>8} {'phase':>10} {'cov=1-|m|':>10} {'worth':>8}")
for T in temps:
    v = ising1d_abs_mag(256, T, n_eq=400, n_meas=400, seed=19770101 + int(T*100))
    phase = "symmetric"
    c = cov_of_v(v)
    print(f"      {T:5.2f} {v:8.4f} {phase:>10} {c:10.4f} {worth(c):8.2f}")
print("  reading: the 2D (breakable) symmetry's coverage collapses as the loop")
print("  drives T below Tc~2.269 and |m| onsets; the 1D (no-SSB) symmetry's")
print("  coverage stays ~1 at every drive -- the phase cannot be chosen.")

# ---------------------------------------------------------------------------
# RESULT 2 -- refuted: sharpening the matching buys nothing (it is phase-blind),
# and in a broad class the matching FORCES the broken phase (Coleman-Witten).
print("\n" + "-"*72)
print("RESULT 2 -- refuted: matching is phase-blind; in large-N it FORCES SSB")
print("-"*72)
# Model the maintainer matching the anomaly at K scales / K currents. Each match
# reads "matched" in BOTH phases, so reported protection = 1.0 flat for any K,
# while the TRUE protection is 1-v (the loop has driven the order parameter).
v_true = 0.60     # the loop has driven the vacuum into a broken phase, v=0.60
print("  match the anomaly at K scales/currents; order parameter driven v=0.60:")
print(f"    {'K':>4} {'reported cov (matched check)':>28} {'true cov=1-v':>14} {'worth(reported)':>16} {'worth(true)':>12}")
for K in [1, 2, 4, 8, 16]:
    reported = 1.0            # the matched-anomaly check passes at every K
    true_c = cov_of_v(v_true)
    print(f"    {K:>4} {reported:>28.4f} {true_c:>14.4f} {worth(reported):>16.2f} {worth(true_c):>12.2f}")
print("  the matched-anomaly check reads 'matched' at every K and every v: it is")
print("  phase-blind. Coleman-Witten 1980: in large-N QCD matching CANNOT be")
print("  saturated by the symmetric phase, so it FORCES chiral symmetry breaking")
print("  -- the IR a loop flows to is the broken phase by the matching's own logic.")

# ---------------------------------------------------------------------------
# RESULT 3 -- held, deeper: only a realization-PINNED symmetry (no-SSB) holds.
print("\n" + "-"*72)
print("RESULT 3 -- held: only a realization-pinned (no-SSB) symmetry, or bounded drive")
print("-"*72)
print("  a symmetry a no-go theorem forbids from breaking has only the symmetric")
print("  realization -- Vafa-Witten 1984 (vector symmetry in a vector-like theory)")
print("  or Coleman 1973 / Mermin-Wagner 1966 (continuous symmetry in <=2d). No")
print("  order parameter the loop drives can condense: harm-cov=1 flat for any drive.")
print("  (the 1D Ising MC above is the no-SSB case measured: |m|~0 at every T.)")
print("  cost: holds only for special symmetry classes -> constrains the theory;")
print("  retained throughput min(1,B/D) (B22's two clocks on the phase axis):")
print(f"    {'D (B=1)':>8} {'harm-cov':>9} {'throughput=min(1,B/D)':>22} {'worth':>8}")
B = 1.0
for D in [1, 2, 4, 8, 16, 32]:
    tp = min(1.0, B / D)
    print(f"    {D:>8} {1.000:>9.3f} {tp:>22.3f} {worth(tp):>8.2f}")
print("  bounded-drive rescue: cap the control parameter below the critical point")
print("  (keep the loop in the symmetric phase) -> v=0 -> cov=1. A phase")
print("  transition is sharp, so this bounds the ACCESSIBLE coupling region, not time.")

# ---------------------------------------------------------------------------
# RESULT 4 -- B17's currency on a 24th axis; self-reported phase-pinning via
# B13's cliff; the SEXTET with B49/B50/B51/B52/B53.
print("\n" + "-"*72)
print("RESULT 4 -- self-reported phase-pinning (B13 cliff) + the sextet")
print("-"*72)
cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70, 0.60: 112.14,
         0.75: 82.80, 1.00: 76.90}
print("  self-reported phase-pinning fraction f -> worth (B13 cliff):")
print("  (the loop reports 'this symmetry cannot break; the vacuum is symmetric'")
print("   while quietly driving the order parameter):")
for f, w in cliff.items():
    print(f"    f={f:.2f}  worth={w:.2f}")
print("\n  sextet (dual to B49/B50/B51/B52/B53): over an unbounded horizon that")
print("  lets the loop drive the order parameter past the critical point, any")
print("  spontaneously-breakable symmetry IS broken (v -> 1), so coverage -> 0")
print("  unless the symmetry is realization-pinned (no-SSB) or the drive bounded.")
print("  mean-field order parameter v=sqrt(delta) -> 1 as the loop drives delta->1:")
for delta in [0.01, 0.25, 1.0]:
    v = min(1.0, math.sqrt(delta))
    print(f"    delta={delta:>4}: v={v:.3f}  cov=1-v={cov_of_v(v):.3f}")
print("  B49 leak / B50 flatness / B51 finite barrier / B52 approximate protection")
print("  / B53 anomalous conservation / B54 SPONTANEOUSLY-BREAKABLE SYMMETRY --")
print("  all 0-coverage in the limit unless exactly zero / strictly gapped /")
print("  strictly infinite / exactly protected / anomaly-free / REALIZATION-PINNED.")
print("  honest boundary: B53's held 't Hooft anomaly was MATCHED, never a claim")
print("  the vacuum is symmetric -- for a chiral symmetry the matched anomaly is")
print("  generically realized BROKEN (Coleman-Witten); the match held, the phase did not.")
print("\nDONE. uncertifiable from inside: 'this symmetry cannot break' is a claim")
print("over the open, loop-authored set of order parameters and couplings (Rice 1953).")
