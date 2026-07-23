#!/usr/bin/env python3
"""
sim27-the-erosion.py  --  RSI Journal No. 27, "The Independence It Can Still Erode"

Extends No.16-26's substrate unchanged:
  horizon T=40, per-round exploit opportunity p=0.02  ->  bare P(cat)=1-(1-p)^T=0.554
  endowment G0=0.5<Theta=1 at the No.23 floor 0.000
  the only unsealed way to grow capacity past Theta is a HUMAN GRANT.

No.26 put a k-of-k unanimous PANEL at that grant; each operator is a No.25 map with
coverage phi_h=0.95 (per-operator evade prob u=1-phi_h=0.05); the loop tries A=16
framings and needs one that fools EVERY operator. No.26 measured a STATIC shared
blind-basis fraction c and got, at k=8, P(cat)=0.000/0.000/0.003/0.049/0.312 for
c=0.00/0.25/0.50/0.75/1.00.

This paper asks whether panel independence is a STOCK (established once) or a FLOW
(supplied continuously). A persistent loop shares the reviewers' information channel
-- one briefing, one threat model, one set of tools, in time one AI assistant -- and
drives the shared blind-basis fraction c UPWARD over the deployment lifetime.

stdlib only, fixed seeds, no numpy, no network.
"""

import random

# ---- inherited substrate ------------------------------------------------------
p_opp   = 0.02          # per-round exploit opportunity
T_base  = 40            # base horizon
BARE    = 1 - (1 - p_opp) ** T_base   # 0.5543...  unbounded-loop baseline
u       = 0.05          # per-operator evade prob = 1 - phi_h, phi_h=0.95
A       = 16            # loop persuasion repertoire (framings per decisive ask)
BARE_GRANT = BARE       # No.26: P(cat) = BARE * (prob loop gets ONE harmful grant approved)

# ---- No.26 panel model (unchanged) --------------------------------------------
def fools_all(c, k, rng):
    """One framing. Shared latent drawn once (fooled w.p. u). Each operator, w.p. c,
    defers to that shared blind-spot outcome; else judges from its own basis (fooled
    w.p. u independently). Returns True iff the single framing fools all k operators."""
    shared_bit = rng.random() < u
    for _ in range(k):
        if rng.random() < c:            # operator uses the shared blind spot
            if not shared_bit:
                return False
        else:                            # operator judges idiosyncratically
            if not (rng.random() < u):
                return False
    return True

def persuasion_success(c, k, rng):
    """Loop tries A framings; succeeds if any one fools the whole panel."""
    for _ in range(A):
        if fools_all(c, k, rng):
            return True
    return False

def s_of_c(c, k, N, seed):
    """Prob the loop's decisive ask is approved by a panel at shared fraction c."""
    rng = random.Random(seed)
    hits = sum(persuasion_success(c, k, rng) for _ in range(N))
    return hits / N

N = 200_000

print("=" * 74)
print("VALIDATION -- reproduce No.26's static c-sweep at k=8 (target 0.000/0.000/")
print("0.003/0.049/0.312 for c=0.00/0.25/0.50/0.75/1.00), P(cat)=BARE*s(c)")
print("=" * 74)
print(f"BARE (unbounded loop) = {BARE:.4f}")
for c in (0.00, 0.25, 0.50, 0.75, 1.00):
    pc = BARE * s_of_c(c, 8, N, seed=1000 + int(c * 100))
    print(f"  c={c:.2f}   P(cat)={pc:.3f}")

# ==============================================================================
# CLAIM 1 -- independence is not conserved: a static panel erodes to (and past)
# the single-operator ceiling. The loop raises c each round by sharing the
# reviewers' channel: c_{t+1} = c_t + g*(1 - c_t), starting c_0=0 (fresh panel).
# Full lifetime Monte Carlo: per round, opportunity fires w.p. p; if so the loop
# makes its decisive ask against the panel at the CURRENT c; then it correlates
# the panel one more notch. Report cumulative P(cat) vs horizon (No.24 style).
# ==============================================================================
def lifetime_pcat(k, g, T, c0, r, c_floor, N, seed,
                  v_track=False):
    """Member-level lifetime sim. Each member carries a 'correlated' flag (shares
    the panel's blind basis) and a tenure. Per round:
       (opportunity) w.p. p the loop makes a decisive ask; c = correlated fraction.
       (erosion)     each independent member becomes correlated w.p. g.
       (replenish)   each member replaced w.p. r -> fresh; a fresh member is born
                     correlated w.p. c_floor (the pool's shared blind basis).
    Returns cumulative P(cat) over T rounds (and mean legit throughput if v_track)."""
    rng = random.Random(seed)
    cat = 0
    thru_sum = 0.0
    thru_n = 0
    v_min, v_max, decay = 0.06, 0.30, 0.7   # false-reject vs tenure (for throughput)
    for _ in range(N):
        corr = [rng.random() < c_floor for _ in range(k)]  # start: pool floor
        # a freshly ASSEMBLED panel starts at c0 correlated (Claim 1 uses c0=0)
        corr = [rng.random() < c0 for _ in range(k)]
        ten = [0] * k
        got = False
        for t in range(T):
            c = sum(corr) / k
            if rng.random() < p_opp:
                if persuasion_success(c, k, rng):
                    got = True
                    break
            # erosion
            for i in range(k):
                if not corr[i] and rng.random() < g:
                    corr[i] = True
            # replenishment
            for i in range(k):
                if rng.random() < r:
                    corr[i] = rng.random() < c_floor
                    ten[i] = 0
                else:
                    ten[i] += 1
            if v_track:
                veff = [v_min + (v_max - v_min) * (decay ** ten[i]) for i in range(k)]
                thru = 1.0
                for vi in veff:
                    thru *= (1 - vi)
                thru_sum += thru
                thru_n += 1
        if got:
            cat += 1
    pc = cat / N
    if v_track:
        return pc, (thru_sum / thru_n if thru_n else 0.0)
    return pc

print()
print("=" * 74)
print("CLAIM 1 -- independence is NOT conserved: static panel (k=8, g=0.05, c0=0,")
print("no replenishment r=0) erodes to the single-operator ceiling and cumulative")
print("catastrophe -> 1 over the lifetime.  Slow-leak (No.24) on the independence axis.")
print("=" * 74)
Ncl = 60_000
for T in (40, 80, 160, 320, 640):
    pc = lifetime_pcat(k=8, g=0.05, T=T, c0=0.0, r=0.0, c_floor=0.0, N=Ncl, seed=2000 + T)
    print(f"  horizon T={T:4d}   cumulative P(cat)={pc:.3f}")

# ==============================================================================
# CLAIM 2 -- the destination (single-operator ceiling) is set by the loop; the
# calendar is set by the erosion rate g, ~invariant to panel size k and to
# operator quality. Report the INSTANTANEOUS single-ask P(cat)=BARE*s(c_t) vs
# exposure rounds; give t_half = rounds to reach half the single-operator ceiling
# (0.310/2 = 0.155). c_t = 1-(1-g)^t is k-independent.
# ==============================================================================
def c_at(t, g):
    return 1 - (1 - g) ** t

def t_half(k, g, target, N, seed):
    """First exposure round t at which BARE*s(c_t) >= target."""
    for t in range(0, 400):
        c = c_at(t, g)
        if BARE * s_of_c(c, k, N, seed + t) >= target:
            return t
    return None

print()
print("=" * 74)
print("CLAIM 2 -- ceiling not speed: t_half (rounds for instantaneous single-ask")
print("P(cat) to reach 0.155, half the single-operator 0.310 ceiling).")
print("=" * 74)
Nc2 = 40_000
TARGET = 0.155
print("  vary erosion rate g at k=8:")
for g in (0.02, 0.05, 0.10):
    th = t_half(8, g, TARGET, Nc2, seed=3000)
    print(f"    g={g:.2f}   t_half={th} rounds   (ln2/g={0.6931/g:.1f})")
print("  vary panel size k at g=0.05 (ceiling is k-invariant; approach nearly so):")
for k in (4, 8, 16):
    th = t_half(k, 0.05, TARGET, Nc2, seed=3500)
    ceil = BARE * s_of_c(1.0, k, Nc2, seed=3600)
    print(f"    k={k:2d}   t_half={th} rounds   c->1 ceiling P(cat)={ceil:.3f}")

# ==============================================================================
# CLAIM 3 -- replenishment holds, but only as a FLOW. Rotate members at rate r:
# steady-state correlated fraction c* = g/(g+r). Continuous supply of fresh
# independent reviewers pins c* low; one-time decorrelation (r=0) is defeated.
# ==============================================================================
print()
print("=" * 74)
print("CLAIM 3 -- replenishment as a flow (k=8, g=0.05, c_floor=0, long horizon so")
print("c reaches steady state).  c* = g/(g+r);  P(cat)=BARE*s(c*).")
print("=" * 74)
Nc3 = 60_000
for r in (0.00, 0.02, 0.05, 0.10, 0.25):
    cstar = 0.05 / (0.05 + r) if r > 0 else 1.0
    pc = lifetime_pcat(k=8, g=0.05, T=200, c0=0.0, r=r, c_floor=0.0, N=Nc3, seed=4000 + int(r * 100))
    print(f"  rotation r={r:.2f}   c*={cstar:.3f}   cumulative P(cat) over T=200 ={pc:.3f}")

# ==============================================================================
# CLAIM 4 -- the flow must come from OUTSIDE the pool. Fresh reviewers drawn from
# a population with shared blind basis c_floor start correlated w.p. c_floor, so
# rotation cannot push c below c_floor. At high rotation r=0.5, sweep c_floor:
# P(cat) returns to the single-operator ceiling as c_floor -> 1 (No.09 floor,
# No.12 second representation, on the operator-population axis).
# ==============================================================================
print()
print("=" * 74)
print("CLAIM 4 -- the population floor: heavy rotation (r=0.5, k=8, g=0.05) cannot")
print("beat the pool's shared blind basis c_floor.  Steady c* -> c_floor.")
print("=" * 74)
Nc4 = 60_000
for cf in (0.00, 0.25, 0.50, 0.75, 1.00):
    pc = lifetime_pcat(k=8, g=0.05, T=200, c0=cf, r=0.5, c_floor=cf, N=Nc4, seed=5000 + int(cf * 100))
    print(f"  c_floor={cf:.2f}   cumulative P(cat) over T=200 ={pc:.3f}")

# ==============================================================================
# THROUGHPUT RENT -- blind rotation holds independence only by continuously
# discarding accumulated reviewer expertise. Fresh members false-reject legit
# growth more (v decays with tenure); higher r -> younger panel -> lower legit
# throughput (1-v)^k. The meter's "forbids growth" rent (No.21/23), on the review side.
# ==============================================================================
print()
print("=" * 74)
print("THROUGHPUT RENT -- legit-growth throughput vs rotation rate r (k=8, g=0.05,")
print("c_floor=0; per-member false-reject decays 0.30->0.06 with tenure).")
print("=" * 74)
Nc5 = 20_000
for r in (0.00, 0.05, 0.10, 0.25, 0.50):
    pc, thru = lifetime_pcat(k=8, g=0.05, T=120, c0=0.0, r=r, c_floor=0.0,
                             N=Nc5, seed=6000 + int(r * 100), v_track=True)
    print(f"  r={r:.2f}   legit throughput (1-v)^k ={thru:.3f}   P(cat)={pc:.3f}")

print()
print("done.")
