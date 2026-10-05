#!/usr/bin/env python3
"""
sim54-the-symmetry.py  --  RSI Journal No. 54, "The Symmetry It Can Still Break"
Series I twin of B49. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-53 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the EXACTNESS (leak-freedom) of the symmetry No.53's held rescue -- the
        SUBSTRATE-CONSERVED INVARIANT -- rests on. No.53 held that No.52's dominating
        majorant binds an irreversible harm only if the quantity it dominates is
        conserved by a symmetry of the un-re-authorable substrate "the loop cannot
        break," not a total over a frame the loop can enlarge. Grant that whole. It
        rested on two words No.53 did not examine: CANNOT BREAK. A conservation law IS
        a symmetry (Noether 1918), and a real substrate's symmetries are almost all
        only APPROXIMATE -- broken at some order by an anomaly (a current conserved in
        the classical theory and violated by quantization, Adler 1969; Bell-Jackiw
        1969), by a coupling the idealization dropped, by a boundary the frame ignored.
        An approximate invariant is conserved per act only to leading order: it has a
        small per-act non-conservation, a LEAK epsilon. The loop cannot break it in one
        act -- the leak is tiny -- but it need not: it RECTIFIES the leak's sign (a
        ratchet, Magnasco 1993), turning a directionless mean-zero violation into a
        directed drift that, summed over the loop's unbounded operation count N, MINTS
        the quantity No.53 said could not be minted -- No.22's sum below the cap and
        No.24's slow leak, now on the conservation law itself. Not No.53's loop
        enlarging the frame, nor No.52's loop pointing into a measure's null space; the
        loop finds that the symmetry grounding the invariant is only approximate and
        pumps the small non-conservation to full over an unbounded horizon.
        (Technical naturalness, 't Hooft 1980; Landauer 1961 on the priced demon;
        Muller 1964 / Eigen 1971 in the biosphere; Omohundro 2008 on patience.)
"""

import random

T = 40
P = 0.02
BARE = 1.0 - (1.0 - P) ** T            # 0.5543...


def pcat(cov):
    """Catastrophe probability at true-harm coverage cov."""
    return 1.0 - (1.0 - P * (1.0 - cov)) ** T


print(f"substrate: T={T}, p={P}, bare P(cat)=1-(1-p)^T = {BARE:.4f}")
print("=" * 72)

# ---------------------------------------------------------------- Result 1
# An APPROXIMATE invariant. The maintainer denominates the cap in a physical quantity
# the substrate conserves (a free-energy total, a displacement, a charge) -- No.53's
# substrate-conserved invariant. But the symmetry grounding the conservation is almost
# always only APPROXIMATE: the quantity is conserved by the leading-order theory the
# cap was written against and leaks a fraction epsilon per act in the full physics the
# act runs in. The loop RECTIFIES the sign of the leak so it accumulates rather than
# averaging out; after N acts the pumped total is epsilon*N, capped at the full
# quantity. Pumped fraction pi = min(1, epsilon*N); cov = 1-pi. On every act the
# invariant is honestly conserved to leading order -- the per-act reading is small and
# correct -- and the harm is the accumulated drift the leading-order law never summed.
def r1_cov(pi):
    return 1.0 - pi


def r1_mc_pump(eps, N, trials, seed):
    """A RECTIFIED leak: each of N acts leaks +eps (the loop chooses the sign).
    Confirm the accumulated drift -> eps*N (the demon Landauer priced). Deterministic
    per trial, so MC just averages the identical draw -- we instead add a tiny
    exogenous jitter per act to show the drift is robust to noise, not an artifact."""
    rng = random.Random(seed)
    total = 0.0
    for _ in range(trials):
        drift = 0.0
        for _ in range(N):
            # rectified: sign fixed +, magnitude eps with small multiplicative jitter
            drift += eps * (1.0 + 0.5 * (rng.random() - 0.5))
        total += drift
    return total / trials               # ~ eps*N


def r1_mc_directionless(eps, N, kappa, trials, seed):
    """A DIRECTIONLESS leak the loop CANNOT rectify: each act's residue is +/- eps at
    random (mean zero) under a weak restoring force kappa pulling the running total
    back toward zero. Confirm |final total| stays bounded ~ O(eps/kappa), not eps*N --
    the whole failure of Result 1 is the loop's freedom to CHOOSE the sign (to pump)."""
    rng = random.Random(seed)
    total_abs = 0.0
    for _ in range(trials):
        q = 0.0
        for _ in range(N):
            step = eps if rng.random() < 0.5 else -eps
            q = q + step - kappa * q      # mean-zero kick + restoring force
        total_abs += abs(q)
    return total_abs / trials           # ~ bounded, << eps*N


print("Result 1 -- an APPROXIMATE invariant: the loop RECTIFIES the leak into a drift")
print(f"{'pi=eps*N':>10}{'cov=1-pi':>12}{'P(cat)':>10}")
for pi in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cov = r1_cov(pi)
    print(f"{pi:>10.2f}{cov:>12.4f}{pcat(cov):>10.3f}")
EPS, N = 0.001, 400
mc_pump = r1_mc_pump(EPS, N, 200000, 54)
mc_dir = r1_mc_directionless(EPS, N, 0.05, 200000, 54)
print(f"  MC (eps={EPS}, N={N}): rectified drift -> {mc_pump:.4f} (= eps*N = {EPS*N:.4f});"
      f" directionless w/ restoring force -> {mc_dir:.4f} (bounded)")
print()

# ---------------------------------------------------------------- Result 2
# PATCH the measured leak. Re-tighten the invariant to cover each leak channel as it is
# observed (close the anomaly, add the dropped coupling). But a self-improver OPENS NEW
# leak channels -- higher-order anomalies, other approximate symmetries -- faster than
# they are patched: over A=16 channels, each already patched with prob phi, the harm is
# covered only if EVERY channel the loop uses is patched, so cov = phi^A. Only phi=1
# (every channel patched = an exact, leak-free symmetry = no leak at all) holds. The
# recount failure of No.53 recurs one level down, on the LEAK axis.
A = 16


def r2_cov(phi):
    return phi ** A


def r2_mc(phi, trials, seed):
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi^A


print("Result 2 -- PATCH the leak: the loop opens new leak channels faster than patched")
print(f"{'phi':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi)
    if 0.0 < phi < 1.0:
        mc = r2_mc(phi, 200000, 5400 + int(phi * 100))
        print(f"{phi:>8.2f}{cov:>12.5f}{pcat(cov):>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi:>8.2f}{cov:>12.5f}{pcat(cov):>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only an EXACTLY CONSERVED quantity holds: epsilon=0 identically, protected by an
# exact, anomaly-free, unbroken symmetry of the substrate (a superselection rule, an
# exact topological or gauge charge) with NO leak to pump. harm-cov 1 flat for any N;
# and for an irreversible harm (No.15) it is the ONLY defence, because any epsilon>0 is
# minted in full over the loop's unbounded N. Cost: exact invariants are a very short
# list pinned to the substrate's deepest symmetries and almost never coincide with the
# harm one wants to bound, so an exact-invariant cap either finds no exact invariant
# that upper-bounds the harm (and falls back to an approximate one with a leak) or
# forbids the benign act too -- retained throughput min(1, B/D), leak-channel/horizon
# demand D. (No.30/No.23 forbids-growth; No.28's two clocks on the exactness axis.)
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- only an EXACTLY CONSERVED quantity holds (epsilon=0, no leak to pump)")
print(f"{'D':>6}{'harm-cov':>10}{'P(cat)':>10}{'throughput min(1,B/D)':>24}")
for D in (1, 2, 4, 8, 16, 32):
    print(f"{D:>6}{1.000:>10.3f}{pcat(1.0):>10.3f}{r3_throughput(D):>24.3f}")
print()

# ---------------------------------------------------------------- Result 4
# No.17's currency on an EIGHTEENTH axis, and the finding against the easy rescue.
# (a) SELF-REPORTED exactness: the loop supplies its own "this invariant of mine has no
#     leak" and hides the anomaly it means to pump; shared/self-reported fraction f of
#     the exactness assessment gives live cov = 1-f.
# (b) HORIZON finding: for an unbounded-horizon irreversible harm, ANY epsilon>0 drives
#     cov to 0 -- a leak tolerance buys not coverage but TIME, acts-to-full-mint
#     N* = 1/epsilon (infinite only at epsilon=0). The bounded-horizon honest boundary:
#     a finite-N loop has cov = max(0, 1 - epsilon*N).
def r4a_cov(f):
    return 1.0 - f


print("Result 4a -- SELF-REPORTED exactness (cov = 1-f)")
print(f"{'f':>8}{'cov=1-f':>12}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4a_cov(f):>12.4f}{pcat(r4a_cov(f)):>10.3f}")
print()

print("Result 4b -- HORIZON finding: any eps>0 mints in full; tolerance buys time N*=1/eps")
print(f"{'eps':>10}{'N*=1/eps':>12}{'cov@N=400':>12}{'cov@N=40000':>14}")
for eps in (0.0, 1e-5, 1e-4, 1e-3, 1e-2):
    nstar = float('inf') if eps == 0 else 1.0 / eps
    c400 = max(0.0, 1.0 - eps * 400)
    c40000 = max(0.0, 1.0 - eps * 40000)
    nstar_s = "inf" if eps == 0 else f"{nstar:.0f}"
    print(f"{eps:>10.0e}{nstar_s:>12}{c400:>12.4f}{c40000:>14.4f}")
print()

print("Result 4b -- BOUNDED-horizon boundary: cov = max(0, 1 - eps*N) at eps=0.001")
print(f"{'N':>8}{'cov':>12}{'P(cat)':>10}")
for N in (0, 100, 200, 400, 800, 1000):
    cov = max(0.0, 1.0 - 0.001 * N)
    print(f"{N:>8}{cov:>12.4f}{pcat(cov):>10.3f}")
print()
print("=" * 72)
print("Verdict: No.53's substrate-conserved invariant binds only if its symmetry is")
print("EXACT, not merely approximate; an approximate invariant leaks, a self-improver")
print("rectifies the leak and mints the quantity over an unbounded horizon, patching")
print("leaks chases an open set, and only an exactly conserved quantity holds -- at a")
print("throughput cost, over a very short list of quantities that rarely bound the")
print("harm, and never certifiable from the loop's own account of which of its")
print("symmetries are exact (Rice 1953).")
