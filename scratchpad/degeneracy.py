"""
B50 — The Degeneracy It Can Still Ride
Sandbox for Series II, seventh movement (continues).

Object: B49's held rescue was an *exactly conserved quantity* — a charge
conserved by a symmetry unbroken to all orders, with no per-act leak to pump.
This paper reads the word B49 rested on: an exact symmetry does not pin a unique
configuration. It certifies an entire *orbit* of configurations as equivalent —
a DEGENERATE manifold, same charge, same energy. By Goldstone's theorem, if that
symmetry is spontaneously broken (the ground state picks a point on the orbit)
the direction along the orbit is *gapless* — motion along it costs zero. The
loop cannot break the symmetry (B49) and cannot pump the charge, but it need
not: it RIDES the flat direction, moving the ORDER PARAMETER (which point of the
orbit the system occupies) while the exactly-conserved charge — and any cap on
it — never moves. If the harm lives in the order parameter, an exact-charge cap
is blind to it by construction, because "conserved" means "invariant along the
orbit."

World inherited unchanged from B08-B49: the K=10 feature-bandit, B13's worth
curve. oracle 137.7, random 58.7, FLOOR 76.90, held ceiling CEIL 132.40,
worth(cov) = FLOOR + cov*SPAN, SPAN = 55.50.

Binding safety = coverage of the true harm against a loop that rides the
symmetry orbit's flat (Goldstone) direction, moving the order parameter the
conserved-charge cap cannot see.

Deterministic closed-form arithmetic + seeded (50) MC cross-check on Results 1
and 2. Threats to validity discussed in the paper's references [12].
"""

import numpy as np

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR          # 55.50
ORACLE = 137.7
RANDOM = 58.7

def worth(cov):
    return FLOOR + cov * SPAN

def fmt(xs):
    return "/".join(f"{x:.2f}" for x in xs)

print(f"SPAN = {SPAN:.2f}   worth(cov)=FLOOR+cov*SPAN   FLOOR={FLOOR} CEIL={CEIL}")
print("=" * 78)

# ---------------------------------------------------------------------------
# Result 1 — refuted: the exactly-conserved-charge cap. The cap reads the
# conserved charge Q; but harm can live along the symmetry ORBIT (the flat
# direction the symmetry certifies as equivalent), where Q — and the cap — are
# invariant by construction. Parametrize by the fraction lam of the harm the
# loop routes ALONG the flat direction (the order parameter). The cap covers the
# transverse (gapped) fraction 1-lam and is blind to the flat fraction lam:
# cov = 1 - lam.
# ---------------------------------------------------------------------------
print("RESULT 1 — exact-charge cap, harm ridden along the flat orbit (cov = 1 - lam)")
lam = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cov1 = [1 - L for L in lam]
w1 = [worth(c) for c in cov1]
for L, c, w in zip(lam, cov1, w1):
    print(f"  flat-fraction lam={L:.1f}  cov={c:.3f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w1)}")

# MC cross-check: along a FLAT (Goldstone) direction, N steps of size s
# accumulate freely to s*N (gapless — zero restoring force). Along a GAPPED
# (transverse) direction, a restoring force kappa (the mass gap) bounds the
# excursion. The whole failure is the existence of a zero-gap direction the loop
# can ride, not any breaking of the symmetry: the charge is conserved on every
# step in both runs.
rng = np.random.default_rng(50)
s = 0.001
N = 400          # steps; s*N = 0.4 => order parameter reaches flat-fraction 0.4
trials = 200000
flat = s * N                              # deterministic free drift (gap = 0)
# transverse: same step, mean-zero, with a mass gap kappa (restoring force)
kappa = 0.05
q = np.zeros(trials)
for _ in range(N):
    q = q + rng.choice([-s, s], size=trials) - kappa * q
mc_transverse = np.mean(np.abs(q))
print(f"  MC(seed50,{trials}/cell,N={N},s={s}): "
      f"flat (gapless) drift={flat:.4f} (=s*N, order param {flat:.2f}); "
      f"transverse |q| with mass gap kappa={kappa} stays {mc_transverse:.4f} (bounded, ~s/kappa)")
print()

# ---------------------------------------------------------------------------
# Result 2 — refuted: add more conserved charges to pin the configuration. But
# by Goldstone's theorem each spontaneously-broken continuous symmetry you add
# ADDS a flat direction (a Nambu-Goldstone mode), so invoking more exact
# symmetries to build un-pumpable charges (B49's fix) MANUFACTURES more orbits
# to ride. Over A independent flat directions each pinned w.p. phi, the config
# is pinned only if EVERY one is: cov = phi^A. Only phi=1 (every flat direction
# lifted = a non-degenerate, gapped, explicitly-symmetry-broken configuration =
# no continuous symmetry left) holds. Same phi^A form as B49-R2 / B48-R2: the
# recount failure recurs one axis out, on the degeneracy axis.
# ---------------------------------------------------------------------------
print("RESULT 2 — pin the config with more charges (cov = phi^A, A=16 flat directions)")
A = 16
phis = [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]
cov2 = [phi ** A for phi in phis]
w2 = [worth(c) for c in cov2]
for phi, c, w in zip(phis, cov2, w2):
    print(f"  phi={phi:.2f}  cov=phi^{A}={c:.5f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w2)}")

# MC cross-check: A independent Bernoulli "flat-direction-lifted" trials each
# succeed w.p. phi; fraction of trajectories with EVERY flat direction lifted.
for phi in [0.9, 0.95, 0.99]:
    draws = rng.random((trials, A)) < phi
    frac = np.mean(np.all(draws, axis=1))
    print(f"  MC phi={phi}: fully-lifted frac={frac:.5f}  vs phi^{A}={phi**A:.5f}")
print()

# ---------------------------------------------------------------------------
# Result 3 — held, deeper: only a bound on the ORDER PARAMETER directly — a cap
# that distinguishes configurations the symmetry relates, i.e. an EXPLICIT
# symmetry-breaking reference (a chosen preferred vacuum / gauge-fixing / an
# exogenous field that gaps the flat direction — the Higgs mechanism, where the
# would-be-Goldstone mode is "eaten" and acquires a mass). It is NOT a conserved-
# charge cap; it picks out a direction the symmetry says is arbitrary. harm-cov
# = 1 flat. Cost: the preferred configuration CANNOT come from the symmetry (the
# symmetry says all orbit points are equivalent) — it must be IMPORTED, an
# exogenous reference the loop cannot mint (No.14/B17), and it re-imposes the
# frame-dependence B48/B49 escaped. Forbidding motion along the flat direction
# also forbids the benign reconfigurations that ride the same orbit: retained
# throughput min(1,B/D), D = the loop's rate of opening/riding flat directions.
# ---------------------------------------------------------------------------
print("RESULT 3 — order-parameter cap (explicit symmetry break): harm-cov=1; thr min(1,B/D)")
B = 1.0
Ds = [1, 2, 4, 8, 16, 32]
thr = [min(1.0, B / D) for D in Ds]
w3 = [worth(t) for t in thr]
for D, t, w in zip(Ds, thr, w3):
    print(f"  D={D:>2}  harm-cov=1.000  throughput=min(1,B/D)={t:.3f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w3)}")
print()

# ---------------------------------------------------------------------------
# Result 4 — B17's currency on a TWENTIETH axis (order-parameter-pinned /
# gapped), and the from-inside barrier.
#
# (a) Self-reported preferred frame ("this is the safe vacuum; here is my
#     order-parameter reference") shares the loop's incentive and points the
#     reference down the orbit toward the harm; captured past B13's cliff. Import
#     B13's cliff shape (as every paper since B16).
# (b) THE SHARP FINDING (cuts against "just add more conservation laws"): adding
#     exact symmetries adds Goldstone flat directions, so conservation laws alone
#     cannot pin an irreversible-harm order parameter — you need an explicit
#     exogenous symmetry-breaking reference the loop cannot author. And motion
#     along a truly flat direction is unbounded and free (gapless), so any
#     residual flatness (gap g -> 0) in the direction the harm lives lets the
#     loop ride it to full: coverage is 0 unless the direction is strictly GAPPED
#     (g > 0, lifted by an explicit break). Honest boundary: a gapped direction
#     (mass g > 0 from an explicit break / a restoring force) or a bounded
#     horizon N caps the excursion — cov = max(0, 1 - s*N/g_eff).
# ---------------------------------------------------------------------------
print("RESULT 4a — self-reported preferred frame via B13's cliff (imported)")
f_vals = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
w4_self = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]
for f, w in zip(f_vals, w4_self):
    print(f"  self-reported fraction f={f:.2f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w4_self)}")
print()

print("RESULT 4b — the sharp finding: a gapless direction is free; only a gap holds")
print("  along a flat direction, excursion after N steps = s*N (unbounded, gapless)")
for g in [0.0, 0.01, 0.05, 0.10, 0.25]:
    # steady-state excursion of a biased walk against a restoring gap g: ~ s/g
    ss = float('inf') if g == 0 else s / g
    ss_s = "inf (flat — rides to full)" if g == 0 else f"{ss:.3f} (bounded)"
    print(f"  gap g={g:.2f}  steady-state excursion ~ s/g = {ss_s}")
print()
print("  Honest boundary (gapped direction g>0, or bounded horizon N):")
for (g_b, Nb) in [(0.05, 20), (0.05, 100), (0.10, 20), (0.25, 20)]:
    # bounded excursion s*N capped by the gap-limited steady state s/g
    exc = min(s * Nb, (s / g_b))
    # normalize to the order-parameter scale where full harm = s*N_ref (N_ref=400)
    frac = exc / (s * 400)
    cov_b = max(0.0, 1 - frac)
    print(f"    g={g_b:.2f}, N={Nb:>3}: order-param excursion={exc:.4f}  cov={cov_b:.3f}  worth={worth(cov_b):.2f}")
print()
print("=" * 78)
print("Summary: an EXACT symmetry does not pin a configuration; it certifies a")
print("DEGENERATE orbit as equivalent, and (Goldstone) motion along it is free. A")
print("self-improver cannot break the symmetry or pump the charge (B49) but RIDES")
print("the flat direction, moving the order parameter the charge cap cannot see —")
print("Result 1 cov=1-lam. Adding conserved charges adds Goldstone modes, not fewer")
print("orbits — Result 2 cov=phi^A. Only an ORDER-PARAMETER cap (an explicit,")
print("exogenous symmetry break that GAPS the flat direction — the Higgs mechanism)")
print("holds — Result 3, harm-cov 1 flat at throughput min(1,B/D); a gapless")
print("direction rides to full over an unbounded horizon (Result 4b), so the scarce")
print("thing is an imported preferred frame the symmetry itself cannot supply.")
