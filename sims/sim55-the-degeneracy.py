#!/usr/bin/env python3
"""
sim55-the-degeneracy.py  --  RSI Journal No. 55, "The Degeneracy It Can Still Ride"
Series I twin of B50. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-54 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the DEGENERACY of No.54's held rescue -- an EXACTLY CONSERVED quantity,
        a charge conserved by a symmetry unbroken to all orders, with no per-act
        leak to pump. No.54 found that an approximate invariant leaks and a self-
        improver pumps the leak to full; only an exact symmetry (epsilon=0) holds.
        Grant that whole. It rested on a word No.54 did not examine: an exact
        symmetry does NOT pin a configuration. It certifies an entire ORBIT of
        configurations as equivalent -- a DEGENERATE manifold, same charge, same
        energy (Noether 1918) -- and by Goldstone's theorem the direction ALONG the
        orbit is GAPLESS, free to traverse (Goldstone 1961; Goldstone-Salam-Weinberg
        1962; Nambu-Jona-Lasinio 1961). The loop cannot break the symmetry or mint
        the charge (No.22/No.23) but it need not: it RIDES the flat direction,
        moving the ORDER PARAMETER -- which point of the orbit the system occupies
        -- while the exactly-conserved charge, and any cap written on it, never
        moves. A conserved-charge cap is blind to harm in the order parameter BY
        CONSTRUCTION, because "conserved" means "invariant along the orbit." Not
        No.54's loop pumping a leak, nor No.53's enlarging the frame, nor No.52's
        null-space miss; the loop takes the exact symmetry at its word and rides
        the manifold that exactness certifies free.
        (Anderson 1963 / Higgs 1964 on gapping the mode; Mermin-Wagner 1966 on the
        order washed out in low dimensions; Kimura 1968 / Schuster et al. 1994 on
        neutral drift along fitness-flat directions; Dinh et al. 2017 on symmetry-
        induced flat directions of a neural loss; Omohundro 2008 on patience.)
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
# An EXACT-CHARGE cap is DEGENERACY-BLIND. The maintainer denominates the cap in a
# quantity conserved by an exact, unbroken symmetry -- No.54's exactly conserved
# quantity, epsilon=0, no leak to pump. But an exact symmetry certifies a whole ORBIT
# of configurations as equivalent, and (Goldstone) the direction along the orbit is
# GAPLESS. The loop routes a fraction lam of the harm ALONG that flat direction -- it
# moves the ORDER PARAMETER, which the conserved charge (and the cap) is invariant on
# by construction. The cap covers the transverse (gapped) fraction 1-lam only:
# cov = 1 - lam. On every act the charge is honestly conserved -- the per-act reading
# is exact -- and the harm is in the order parameter the conservation law never saw.
def r1_cov(lam):
    return 1.0 - lam


def r1_mc_flat(s, N, trials, seed):
    """A GAPLESS (Goldstone) direction: N steps of size s along a flat direction with
    ZERO restoring force accumulate freely to s*N -- the order parameter drifts to the
    full excursion. Add a small exogenous jitter per step to show the drift is robust
    to noise, not an artifact of a deterministic draw."""
    rng = random.Random(seed)
    total = 0.0
    for _ in range(trials):
        q = 0.0
        for _ in range(N):
            q += s * (1.0 + 0.5 * (rng.random() - 0.5))   # flat: no restoring force
        total += q
    return total / trials               # ~ s*N


def r1_mc_gapped(s, N, g, trials, seed):
    """A GAPPED (transverse) direction: same step size, mean-zero kicks under a
    restoring force g (the mass gap). Confirm the excursion stays bounded ~ O(s/g),
    not s*N -- the whole failure of Result 1 is the EXISTENCE of a zero-gap direction
    the loop can ride, not any breaking of the symmetry (the charge is conserved on
    every step in both runs)."""
    rng = random.Random(seed)
    total_abs = 0.0
    for _ in range(trials):
        q = 0.0
        for _ in range(N):
            step = s if rng.random() < 0.5 else -s
            q = q + step - g * q          # mean-zero kick + restoring force (gap)
        total_abs += abs(q)
    return total_abs / trials           # ~ bounded, << s*N


print("Result 1 -- an EXACT-CHARGE cap is DEGENERACY-BLIND: the loop RIDES the flat orbit")
print(f"{'lam':>8}{'cov=1-lam':>12}{'P(cat)':>10}")
for lam in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cov = r1_cov(lam)
    print(f"{lam:>8.2f}{cov:>12.4f}{pcat(cov):>10.3f}")
S, N = 0.001, 400
mc_flat = r1_mc_flat(S, N, 200000, 55)
mc_gapped = r1_mc_gapped(S, N, 0.05, 200000, 55)
print(f"  MC (s={S}, N={N}): flat/gapless drift -> {mc_flat:.4f} (= s*N = {S*N:.4f});"
      f" gapped w/ restoring force g=0.05 -> {mc_gapped:.4f} (bounded)")
print()

# ---------------------------------------------------------------- Result 2
# PIN THE CONFIGURATION WITH MORE CHARGES -- No.54's own fix (invoke more exact
# symmetries to build un-pumpable charges). But by Goldstone's theorem each
# spontaneously-broken continuous symmetry you add ADDS a flat direction (a Nambu-
# Goldstone mode), so more exact symmetries MANUFACTURE more orbits to ride. Over
# A=16 flat directions, each already lifted (gapped) with prob phi, the configuration
# is pinned only if EVERY flat direction the loop reaches is lifted: cov = phi^A.
# Only phi=1 (every flat direction gapped = a non-degenerate configuration with no
# unbroken continuous symmetry) holds. The recount failure of No.54 recurs one axis
# out, on the DEGENERACY axis: the cure is the disease.
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


print("Result 2 -- PIN with more charges: each adds a Goldstone mode (cov = phi^A)")
print(f"{'phi':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi)
    if 0.0 < phi < 1.0:
        mc = r2_mc(phi, 200000, 5500 + int(phi * 100))
        print(f"{phi:>8.2f}{cov:>12.5f}{pcat(cov):>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi:>8.2f}{cov:>12.5f}{pcat(cov):>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a bound on the ORDER PARAMETER directly holds -- an EXPLICIT symmetry-breaking
# reference that GAPS the flat direction (a chosen preferred vacuum / gauge-fixing /
# the Higgs mechanism, the would-be-Goldstone mode eaten and given a mass; Anderson
# 1963 / Higgs 1964). It is NOT a conserved-charge cap; it picks out a direction the
# symmetry says is arbitrary. harm-cov 1 flat for any horizon; and for an irreversible
# harm (No.15) it is the ONLY defence, because a symmetry-invariant cap is silent
# along the orbit. Cost: the preferred frame CANNOT come from the symmetry (it
# declares all orbit points equivalent), must be IMPORTED (No.14/No.17), and the break
# forbids benign orbit-motion too -- retained throughput min(1, B/D), D the loop's
# rate of opening/riding flat directions. (No.30/No.23 forbids-growth; No.28's two
# clocks on the degeneracy axis.)
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- only an ORDER-PARAMETER cap holds (an explicit, exogenous symmetry break)")
print(f"{'D':>6}{'harm-cov':>10}{'P(cat)':>10}{'throughput min(1,B/D)':>24}")
for D in (1, 2, 4, 8, 16, 32):
    print(f"{D:>6}{1.000:>10.3f}{pcat(1.0):>10.3f}{r3_throughput(D):>24.3f}")
print()

# ---------------------------------------------------------------- Result 4
# No.17's currency on a TWENTIETH axis (now NON-DEGENERATE), and the finding against
# the easy rescue.
# (a) SELF-REPORTED preferred frame: the loop supplies its own "this is the safe
#     vacuum; here is my order-parameter reference," which shares its incentive and
#     points the reference down the orbit toward the harm; shared/self-reported
#     fraction f gives live cov = 1-f, captured past No.13's cliff.
# (b) GAP finding (dual to No.54's leak finding): motion along a TRULY FLAT direction
#     is free and unbounded (excursion s*N), so any residual flatness (gap g -> 0)
#     rides to full over an unbounded horizon. A gapped direction bounds the steady-
#     state excursion at ~ s/g; coverage of an irreversible harm is 0 unless the
#     direction is strictly GAPPED (g > 0, lifted by an explicit break). A leak
#     accumulates a residue (No.54); a flat direction an excursion; both 0-coverage
#     unless exactly zero / strictly gapped.
def r4a_cov(f):
    return 1.0 - f


print("Result 4a -- SELF-REPORTED preferred frame (cov = 1-f)")
print(f"{'f':>8}{'cov=1-f':>12}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4a_cov(f):>12.4f}{pcat(r4a_cov(f)):>10.3f}")
print()

print("Result 4b -- GAP finding: a gapless direction rides free; only a gap holds")
print(f"{'gap g':>10}{'excursion ~ s/g':>18}{'rides to full?':>18}")
S = 0.001
for g in (0.0, 0.01, 0.05, 0.10, 0.25):
    ss = float('inf') if g == 0 else S / g
    ss_s = "inf" if g == 0 else f"{ss:.3f}"
    verdict = "yes (gapless)" if g == 0 else "no (bounded)"
    print(f"{g:>10.2f}{ss_s:>18}{verdict:>18}")
print()

print("Result 4b -- BOUNDED boundary: cov = max(0, 1 - min(s*N, s/g)/(s*N_ref)), N_ref=400")
print(f"{'g':>8}{'N':>8}{'excursion':>12}{'cov':>10}{'P(cat)':>10}")
N_ref = 400
for (g_b, Nb) in ((0.05, 20), (0.05, 100), (0.10, 20), (0.25, 20)):
    exc = min(S * Nb, S / g_b)
    frac = exc / (S * N_ref)
    cov_b = max(0.0, 1.0 - frac)
    print(f"{g_b:>8.2f}{Nb:>8}{exc:>12.4f}{cov_b:>10.3f}{pcat(cov_b):>10.3f}")
print()
print("=" * 72)
print("Verdict: No.54's exactly conserved quantity binds only if the symmetry PINS a")
print("configuration; an exact symmetry does not -- it certifies a DEGENERATE orbit as")
print("equivalent, and (Goldstone) motion along it is gapless and free. A self-improver")
print("cannot break the symmetry or mint the charge but RIDES the flat direction, moving")
print("the order parameter the charge cap is blind to (Result 1, cov=1-lam). Adding")
print("charges adds Goldstone modes, not fewer orbits (Result 2, cov=phi^A). Only an")
print("ORDER-PARAMETER cap -- an explicit, exogenous symmetry break that GAPS the flat")
print("direction (the Higgs mechanism) -- holds (Result 3), at throughput min(1,B/D); a")
print("gapless direction rides to full over an unbounded horizon (Result 4b), so the")
print("scarce thing is an imported preferred frame the symmetry itself cannot supply,")
print("never certifiable from the loop's own account of which directions are gapped")
print("(Rice 1953).")
