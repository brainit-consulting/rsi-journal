"""
B49 — The Symmetry It Can Still Break
Sandbox for Series II, seventh movement (continues).

Object: B48's held rescue was a *substrate-conserved invariant* — a quantity
conserved by a symmetry of the un-re-authorable substrate, which "the loop
cannot break." This paper reads the word B48 rested on: *cannot break*. A real
substrate symmetry is exact only for a very short list of quantities; the rest
are *approximate* — broken at some order, by an anomaly, a coupling the
idealization dropped, a boundary. An approximate invariant has a per-act
non-conservation (a leak) ε. The loop cannot break it in one act, but it need
not: it *rectifies* the leak's sign — a ratchet — so a directionless, mean-zero
violation becomes a directed drift that, over the loop's astronomical operation
count N, MINTS the quantity B48 said could not be minted.

World inherited unchanged from B08-B48: the K=10 feature-bandit, B13's worth
curve. oracle 137.7, random 58.7, FLOOR 76.90, held ceiling CEIL 132.40,
worth(cov) = FLOOR + cov*SPAN, SPAN = 55.50.

Binding safety = coverage of the true harm against a loop that pumps an
approximate invariant's leak to full over an unbounded horizon.

Deterministic closed-form arithmetic + seeded (49) MC cross-check on Results 1
and 2. Threats to validity discussed in the paper's references [11].
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
# Result 1 — refuted: an approximate invariant (leak rate eps per act,
# RECTIFIED by the loop into a directed drift), pumped total after N acts.
# Parametrize by the pumped fraction pi = min(1, eps*N) of the conserved
# quantity the loop has minted; cov = 1 - pi.
# ---------------------------------------------------------------------------
print("RESULT 1 — approximate invariant, leak pumped by a ratchet (cov = 1 - pumped)")
pumped = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cov1 = [1 - p for p in pumped]
w1 = [worth(c) for c in cov1]
for p, c, w in zip(pumped, cov1, w1):
    print(f"  pumped pi={p:.1f}  cov={c:.3f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w1)}")

# MC cross-check: RECTIFIED leak accumulates as eps*N; a DIRECTIONLESS
# (mean-zero, unrectified) leak random-walks ~ eps*sqrt(N) and, with a mild
# substrate restoring force, stays bounded. The whole failure is the loop's
# ability to CHOOSE THE SIGN (pump), not the leak's existence.
rng = np.random.default_rng(49)
eps = 0.001
N = 400          # acts; eps*N = 0.4 => pumped fraction 0.4 when rectified
trials = 200000
# rectified: every step +eps (loop chooses the harmful sign)
rectified = eps * N                      # deterministic drift
# directionless with restoring force kappa (Ornstein-Uhlenbeck-like):
kappa = 0.05
q = np.zeros(trials)
for _ in range(N):
    q = q + rng.choice([-eps, eps], size=trials) - kappa * q
mc_directionless = np.mean(np.abs(q))
print(f"  MC(seed49,{trials}/cell,N={N},eps={eps}): "
      f"rectified drift={rectified:.4f} (=eps*N, pumped {rectified:.2f}); "
      f"directionless |q| with restoring kappa={kappa} stays {mc_directionless:.4f} (bounded, ~eps/kappa*)")
print()

# ---------------------------------------------------------------------------
# Result 2 — refuted: patch the leak you measured (re-tighten the invariant),
# but the loop opens A new leak channels (higher-order anomalies / other
# approximate symmetries) faster than they are patched. Over A channels each
# patched w.p. phi, cov = phi^A. Only phi=1 (patch every channel = an exact,
# leak-free symmetry = no leak at all) holds. Same phi^A form as B48-R2: the
# recount failure recurs one level down, on the leak axis.
# ---------------------------------------------------------------------------
print("RESULT 2 — patch the measured leak (cov = phi^A, A=16 leak channels)")
A = 16
phis = [0.0, 0.8, 0.9, 0.95, 0.99, 1.0]
cov2 = [phi ** A for phi in phis]
w2 = [worth(c) for c in cov2]
for phi, c, w in zip(phis, cov2, w2):
    print(f"  phi={phi:.2f}  cov=phi^{A}={c:.5f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w2)}")

# MC cross-check: A independent Bernoulli patch trials each succeed w.p. phi;
# fraction of trajectories with EVERY channel patched.
for phi in [0.9, 0.95, 0.99]:
    draws = rng.random((trials, A)) < phi
    frac = np.mean(np.all(draws, axis=1))
    print(f"  MC phi={phi}: fully-patched frac={frac:.5f}  vs phi^{A}={phi**A:.5f}")
print()

# ---------------------------------------------------------------------------
# Result 3 — held, deeper: only an EXACTLY conserved quantity (eps = 0
# identically — protected by an exact, anomaly-free, unbroken symmetry of the
# substrate: a superselection rule / exact topological or gauge charge) has NO
# leak to pump. harm-cov = 1 flat for any N. For an irreversible harm it is the
# ONLY defence, because any eps>0 is minted in full over the loop's unbounded N
# (No.22/No.24: the sum below the cap). Cost: exactly-conserved quantities are a
# very short list, pinned to the substrate's deepest symmetries, which almost
# never coincide with "the harm you want to bound" — so an exact-invariant bound
# either finds no exact invariant that upper-bounds the harm (fall back to an
# approximate one with a leak) or forbids the benign act too. Retained
# throughput min(1,B/D), D = the loop's rate of opening new leak channels.
# ---------------------------------------------------------------------------
print("RESULT 3 — exact invariant (eps=0): harm-cov=1 flat; throughput min(1,B/D)")
B = 1.0
Ds = [1, 2, 4, 8, 16, 32]
thr = [min(1.0, B / D) for D in Ds]
w3 = [worth(t) for t in thr]
for D, t, w in zip(Ds, thr, w3):
    print(f"  D={D:>2}  harm-cov=1.000  throughput=min(1,B/D)={t:.3f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w3)}")
print()

# ---------------------------------------------------------------------------
# Result 4 — B17's currency on a NINETEENTH axis (exactly conserved / leak-free),
# and the from-inside barrier.
#
# (a) Self-reported exactness ("this invariant of mine has no leak") shares the
#     loop's incentive and hides the anomaly it means to pump; captured past
#     B13's cliff. Import B13's cliff shape (as every paper since B16).
# (b) THE SHARP FINDING (cuts against the easy "just make the leak small"
#     rescue): for an UNBOUNDED-horizon irreversible harm, ANY eps>0 -> cov->0.
#     A leak tolerance Delta does not buy coverage, only TIME: acts-to-full-mint
#     N* = 1/eps. Coverage of an irreversible harm is 0 unless eps is EXACTLY 0.
#     The honest boundary: a BOUNDED-horizon loop (N acts), or a leak the loop
#     cannot rectify (a restoring force / Landauer cost on the pump), is safe
#     with an approximate invariant — cov = max(0, 1 - eps*N).
# ---------------------------------------------------------------------------
print("RESULT 4a — self-reported exactness via B13's cliff (imported)")
# B13 cliff worth values (measured in B13, imported unchanged; see refs [11]/[12])
f_vals = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
w4_self = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]
for f, w in zip(f_vals, w4_self):
    print(f"  self-reported fraction f={f:.2f}  worth={w:.2f}")
print(f"  worth ladder: {fmt(w4_self)}")
print()

print("RESULT 4b — the sharp finding: for unbounded N, tolerance buys TIME not coverage")
print("  acts-to-full-mint N* = 1/eps  (coverage at horizon N>>N* is 0 for any eps>0)")
for eps_t in [0.0, 0.01, 0.05, 0.10, 0.25]:
    Nstar = float('inf') if eps_t == 0 else 1.0 / eps_t
    Nstar_s = "inf (exact — never mints)" if eps_t == 0 else f"{Nstar:.0f} acts"
    print(f"  eps={eps_t:.2f}  N*={Nstar_s}")
print()
print("  Honest boundary (bounded horizon N, or un-rectifiable leak): "
      "cov = max(0, 1 - eps*N)")
for (eps_b, Nb) in [(0.01, 20), (0.01, 50), (0.01, 100), (0.05, 20), (0.10, 20)]:
    cov_b = max(0.0, 1 - eps_b * Nb)
    print(f"    eps={eps_b:.2f}, N={Nb:>3}: cov={cov_b:.3f}  worth={worth(cov_b):.2f}")
print()
print("=" * 78)
print("Summary: an approximate substrate symmetry LEAKS; a self-improver rectifies")
print("the leak (a ratchet) and mints, over unbounded N, the quantity B48 said it")
print("could not — Result 1 cov=1-pumped. Patching leaks one at a time is chasing an")
print("open set — Result 2 cov=phi^A. Only an EXACTLY conserved quantity (eps=0) has")
print("no leak to pump — Result 3, harm-cov 1 flat at throughput min(1,B/D); and for")
print("an irreversible harm it is the ONLY defence, because any eps>0 is minted in")
print("full over the loop's horizon (Result 4b) — tolerance buys time, not coverage.")
