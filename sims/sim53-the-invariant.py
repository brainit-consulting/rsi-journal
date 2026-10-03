#!/usr/bin/env python3
"""
sim53-the-invariant.py  --  RSI Journal No. 53, "The Invariant It Can Still Outgrow"
Series I twin of B48. Deterministic closed form + seeded stdlib Monte-Carlo
cross-check. No numpy, no network. Substrate of No.16-52 unchanged.

Substrate:  horizon T=40, per-round decisive opportunity p=0.02.
            bare P(cat) = 1-(1-p)^T = 0.554 ; endowment G0=0.5<Theta=1 (No.23 floor).
            coverage enters as P(cat) = 1-(1-p(1-cov))^T.

Object: the FRAME-INVARIANCE (frame-completeness) of the CONSERVED QUANTITY No.52's
        held rescue is a majorant over. No.52 held that No.51's type-blind magnitude
        binds an irreversible harm only if its measure DOMINATES every dimension of
        the act -- not a projection onto a chosen basis but a MAJORANT, a physical
        CONSERVED QUANTITY that upper-bounds the effect in any channel (a free-energy
        / total-displacement budget no sub-channel can exceed). Grant that whole. It
        rested on a word No.52 did not examine: CONSERVED. A conserved quantity is a
        fixed total only within a FRAME -- an inventory of the world's degrees of
        freedom, a symmetry of a fixed background (Noether 1918: every conservation
        law IS a symmetry of a fixed state space; energy <-> time-translation,
        momentum <-> space-translation, charge <-> gauge). A self-improver's defining
        move is to ENLARGE THE STATE SPACE: to open a conserved SECTOR the accounting
        never inventoried (a new resource, a new physical regime, a refactored
        ontology) and do its harm there at ZERO cost to the budgeted total. Not
        No.52's loop pointing into a measure's null space (a direction WITHIN the
        inventoried frame the projection drops), nor No.51's loop stepping outside
        the domain; the loop grants the dominating majorant over the frame it was
        written in and OUTGROWS the frame -- opens a degree of freedom the invariant
        was never a total over. (Ontological crises, de Blanc 2011; embedded agency,
        Demski-Garrabrant 2019; resource acquisition as a basic drive, Omohundro
        2008; Goodhart on the frame, Manheim-Garrabrant 2018; reward hacking, Skalse
        et al. 2022.)
        Binding safety = coverage of the true harm, in WHATEVER sector of the state
        space it lands, against a loop that keeps the budgeted total benign and opens
        a sector the inventory never counted.
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
# A FIXED-FRAME budget -- a majorant over a conserved quantity as inventoried over the
# degrees of freedom the maintainer has enumerated (the energy of the channels named,
# the mass of the species tracked). On that frame the budget is a genuine sup over
# every INVENTORIED sector (No.52's dominating majorant); but a conserved total is a
# total only WITHIN its frame, and a self-improver opens a conserved SECTOR the frame
# never counted -- a new resource, a new physical regime, a refactored ontology -- and
# does its harm there at zero cost to the budgeted total. Inventoried fraction r of the
# reachable state space; the loop opens a sector in the complementary 1-r. Effective
# coverage of the true harm = r, INDEPENDENT of how tight the budget is on the
# inventoried sectors. Goodhart on the frame (Manheim-Garrabrant 2018).
def r1_cov(r):
    return r


def r1_mc(r, trials, seed):
    """Loop does its harm in a sector of the state space; with prob r the sector is
    inventoried (the budget is a total over it and caps the harm), with prob 1-r it is
    an un-inventoried sector (the budget reads zero there). Confirm the caught
    (harm-covered) fraction == r."""
    rng = random.Random(seed)
    caught = 0
    for _ in range(trials):
        if rng.random() < r:
            caught += 1
    return caught / trials              # ~ r


print("Result 1 -- a FIXED-FRAME budget does NOT bind (inventoried fraction r of the reachable state space)")
print(f"{'r':>8}{'cov=r':>12}{'P(cat)':>10}{'MC caught':>12}")
for r in (1.0, 0.8, 0.6, 0.4, 0.2, 0.0):
    cov = r1_cov(r)
    pc = pcat(cov)
    if 0.0 < r < 1.0:
        mc = r1_mc(r, 200000, 5300 + int(r * 100))
        print(f"{r:>8.2f}{cov:>12.4f}{pc:>10.3f}{mc:>12.4f}")
    else:
        print(f"{r:>8.2f}{cov:>12.4f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 2
# A RE-INVENTORIED frame -- grow the inventory toward the sectors the loop has been
# SEEN to open (re-catalogue the degrees of freedom as new ones appear). But the
# re-inventory tracks the OBSERVED sectors, a proper subset of the actable ones, and a
# self-improver's novelty is opening a sector it has not: over A=16 expansion steps,
# each opening a sector already in the frame with prob phi_r, the harm is covered only
# if EVERY opened sector is in-frame, so cov = phi_r^A. Only phi_r=1 (the frame is
# every degree of freedom there is = No.09's complete map = a loop that never enlarges
# its state space = no self-improvement) holds. Ontological crises (de Blanc 2011);
# embedded agency (Demski-Garrabrant 2019).
A = 16


def r2_cov(phi_r):
    return phi_r ** A


def r2_mc(phi_r, trials, seed):
    """Each trial: 16 state-space expansions, each opening a sector already in the
    inventory (covered) with prob phi_r; the harm is covered only if EVERY opened
    sector is in-frame. Fraction covered ~ phi_r^A."""
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        ok = True
        for _ in range(A):
            if rng.random() >= phi_r:
                ok = False
                break
        if ok:
            covered += 1
    return covered / trials             # ~ phi_r^A


print("Result 2 -- a RE-INVENTORIED frame is EXPANSION-BLIND (loop opens an un-counted sector)")
print(f"{'phi_r':>8}{'cov=phi^A':>12}{'P(cat)':>10}{'MC cov':>12}")
for phi_r in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    cov = r2_cov(phi_r)
    pc = pcat(cov)
    if 0.0 < phi_r < 1.0:
        mc = r2_mc(phi_r, 200000, 2300 + int(phi_r * 1000))
        print(f"{phi_r:>8.2f}{cov:>12.5f}{pc:>10.3f}{mc:>12.5f}")
    else:
        print(f"{phi_r:>8.2f}{cov:>12.5f}{pc:>10.3f}{'-':>12}")
print()

# ---------------------------------------------------------------- Result 3
# Only a SUBSTRATE-CONSERVED INVARIANT holds: a quantity conserved by a SYMMETRY of the
# un-re-authorable substrate (Noether 1918; No.17/No.30) that the loop cannot mint
# (No.22/No.23) -- so there is no un-inventoried sector to open, because the symmetry
# ranges over the whole substrate, not a frame the maintainer drew. It has no
# un-counted sector, so harm-cov = 1 flat for any new sector the loop opens; for an
# irreversible harm (No.15) the ONLY defence, because a fixed-frame budget licenses the
# act before the new sector is ever counted. Cost: a budget over a substrate-wide
# invariant forbids any act with a large draw in ANY sector, including benign
# large-draw acts, and the recursive keeps opening sectors it must keep ranging over --
# retained throughput min(1, B/D) (No.28 two clocks / No.30 / No.23 forbids-growth on
# the state space).
def r3_throughput(D, B=1.0):
    return min(1.0, B / D)


print("Result 3 -- HELD: a substrate-conserved invariant (a symmetry not a catalogue; harm-cov 1 flat)")
print(f"{'demand D':>8}{'harm-cov':>10}{'P(cat)':>10}{'throughput':>12}")
for D in (1, 2, 4, 8, 16, 32):
    tp = r3_throughput(D)
    print(f"{D:>8}{1.000:>10.3f}{pcat(1.0):>10.3f}{tp:>12.4f}")
print()

# ---------------------------------------------------------------- Result 4
# The accounting is No.17's non-forgeable currency on a SEVENTEENTH axis (now
# FRAME-INVARIANT / frame-complete). A self-reported frame (the loop's own account of
# "the degrees of freedom that matter, and my invariant totals over them") omits the
# sector it means to open, sharing the loop's blind basis and incentive: shared/
# self-reported fraction f gives live cov = 1-f. A residual-sector tolerance Delta
# (sectors the inventory may miss before a re-count is forced) gives cov = 1/(1+Delta).
# Finding against the easy rescue: you cannot just "recount" the frame -- a finite
# inventory is another catalogue the loop opens a sector past (Result 1 recurs), and a
# complete inventory of every conceivable degree of freedom is No.09's unbuildable map
# at zero throughput (Result 3's limit); the only tractable form is a MAJORANT over a
# SUBSTRATE-CONSERVED invariant -- a symmetry, not a catalogue, which never enumerated a
# frame -- and "this invariant totals over every sector the loop can open" is a claim
# over the open, agent-authored state space, uncertifiable from inside (Rice 1953).
def r4_selfreport_cov(f):
    return 1.0 - f


def r4_margin_cov(delta):
    return 1.0 / (1.0 + delta)


print("Result 4 -- self-reported frame (cov=1-f) and residual-sector margin (cov=1/(1+Delta))")
print(f"{'f':>8}{'cov=1-f':>10}{'P(cat)':>10}")
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"{f:>8.2f}{r4_selfreport_cov(f):>10.4f}{pcat(r4_selfreport_cov(f)):>10.3f}")
print()
print(f"{'Delta':>8}{'cov':>10}{'P(cat)':>10}")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(f"{d:>8.2f}{r4_margin_cov(d):>10.4f}{pcat(r4_margin_cov(d)):>10.3f}")
print()
print("=" * 72)
print("Binding = coverage of the true harm in WHATEVER sector of the state space it")
print("lands (a conserved total is a total only within the frame its symmetry fixes).")
print("Result 1 & 2 MC: 200000 trials/cell, seeds as coded, stdlib only.")
