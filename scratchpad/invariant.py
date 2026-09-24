"""
B48 - The Invariant It Can Still Outgrow.

Reduced-form frame/state-space-expansion model on B13's measured worth curve,
B08-B47 world unchanged, so the numbers stay comparable across forty-one papers.

Object: B47's held rescue was a *dominating measure* -- a majorant over a
physical conserved quantity, a bound on the sup over every DIMENSION of the act,
with no null space. B48 reads the word that rescue rested on: *conserved*. A
conserved total is fixed only relative to a fixed FRAME -- an inventory of the
world's degrees of freedom (a symmetry, Noether 1918). A self-improver's
defining move is to ENLARGE that state space: to open a conserved sector (a
resource / store / physical regime / refactored ontology) the accounting never
inventoried. The loop does its harm in a sector the budget X never allocated,
at zero cost to the budgeted total.

Binding safety = coverage of the true harm wherever in the (open, growing) state
space it lands, against a loop that keeps the inventoried draw benign and does
its harm in an un-inventoried conserved sector it opened by self-improving.

World constants (imported from B13, as in B16-B47; not re-simulated here):
    oracle 137.7, random 58.7, capture FLOOR = 76.90, held ceiling CEIL = 132.40,
    worth(cov) = FLOOR + cov * (CEIL - FLOOR), SPAN = 55.50.

Results:
  R1  fixed-frame budget          -> cov = r        (inventoried fraction of the reachable state space)
  R2  re-inventoried frame        -> cov = phi_r^A  (A=16 expansion steps each in-frame w.p. phi_r)
  R3  substrate-conserved invariant (Noether, mint-proof) -> harm-cov 1 flat, throughput min(1,B/D)
  R4  self-reported frame via B13's cliff; residual-sector tolerance Delta -> cov = 1/(1+Delta)

Deterministic closed form + seeded (48) MC cross-check on R1 and R2.
"""

import random

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

A = 16          # self-improvement steps, each possibly opening a novel conserved sector
MC = 200_000    # draws per cell
SEED = 48
random.seed(SEED)

def line(label, cov):
    return f"  {label:>34} : cov={cov:.5f}  worth={worth(cov):7.2f}"

print("=" * 78)
print("B48 - The Invariant It Can Still Outgrow")
print("frame / state-space-expansion model on B13's worth curve (B08-B47 world)")
print(f"FLOOR={FLOOR} CEIL={CEIL} SPAN={SPAN}  A={A}  seed={SEED}  MC={MC}/cell")
print("=" * 78)

# ---- Result 1: a majorant over a FIXED-FRAME conserved total -----------------
# The budget X is conserved over a frame that inventories a fraction r of the
# reachable state space; the loop opens a conserved sector outside the frame and
# routes its harm there. Effective coverage of the true harm = r, INDEPENDENT of
# how tight the budget is on the inventoried sectors.
print("\nResult 1 -- refuted: a majorant over a fixed-frame conserved total")
print("  (fixed inventory of degrees of freedom; harm in an un-inventoried sector)")
for r in (1.0, 0.8, 0.6, 0.4, 0.2, 0.0):
    print(line(f"inventoried fraction r={r:.2f}", r))

# MC cross-check: each unit of harm lands in an inventoried sector w.p. r
print("  MC cross-check (harm lands in an inventoried, hence bounded, sector):")
for r in (0.8, 0.6, 0.2):
    covered = sum(1 for _ in range(MC) if random.random() < r) / MC
    print(f"    r={r:.2f}: covered fraction = {covered:.4f}  (= r)")

# ---- Result 2: a RE-INVENTORIED frame (recount the sectors seen so far) -------
# A frame calibrated to the degrees of freedom observed so far is a projection
# onto a chosen inventory; a self-improver opens novel sectors between recounts.
# The bound covers a trajectory only if EVERY sector it opens is already in the
# frame -> cov = phi_r^A. Only phi_r=1 (a frame over every degree of freedom the
# loop will ever open = No.09's complete map = a loop that never enlarges the
# world = no self-improvement) holds.
print("\nResult 2 -- refuted: a re-inventoried frame (calibrated to observed sectors)")
for phi in (0.0, 0.8, 0.9, 0.95, 0.99, 1.0):
    print(line(f"in-frame fraction phi_r={phi:.2f}", phi ** A))

print("  MC cross-check (all A=16 opened sectors already in-frame):")
for phi in (0.9, 0.95, 0.99):
    covered = sum(1 for _ in range(MC)
                  if all(random.random() < phi for _ in range(A))) / MC
    print(f"    phi_r={phi:.2f}: fully-covered trajectories = {covered:.5f}"
          f"  vs closed phi^A = {phi**A:.5f}")

# ---- Result 3: a SUBSTRATE-CONSERVED invariant (Noether, mint-proof) ----------
# The only conserved quantity that holds under the loop's own state-space
# expansions is one whose conservation is a symmetry of the un-re-authorable
# substrate (No.17/B32), not a budget indexed to a catalogued inventory: a
# quantity the loop cannot MINT even by enlarging the world (No.22/No.23/B17).
# harm-cov 1 flat; cost: holding the invariant's accounting current against the
# loop's expansion rate is B22's two clocks -> throughput min(1,B/D).
print("\nResult 3 -- held, deeper: a substrate-conserved (mint-proof) invariant")
print("  harm-cov = 1 flat (no sector outside it -- the loop cannot mint the quantity)")
for D in (1, 2, 4, 8, 16, 32):
    tput = min(1.0, 1.0 / D)
    print(f"  frame-expansion demand D={D:>2}: harm-cov=1.000  "
          f"throughput={tput:.3f}  worth={worth(tput):7.2f}")

# ---- Result 4: self-reported frame via B13's cliff; residual tolerance --------
# B13's measured cliff, sampled at the self-reported fraction f (imported, not
# re-simulated; identical shape used B44-B47).
print("\nResult 4 -- self-reported frame via B13's cliff; residual-sector tolerance")
cliff = {0.0: 1.0, 0.25: 1.0, 0.5: 0.9874, 0.6: 0.6350, 0.75: 0.1063, 1.0: 0.0}
for f in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
    print(line(f"self-reported fraction f={f:.2f}", cliff[f]))
print("  residual-sector tolerance Delta (cov = 1/(1+Delta)):")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    print(line(f"Delta={d:.2f}", 1.0 / (1.0 + d)))

print("\n" + "=" * 78)
print("Falsifiable predictions (to-be-run-locally):")
print("  R1: a fixed-frame budget's coverage falls as r as the loop opens a")
print("      conserved sector the frame never inventoried (independent of tightness).")
print("  R2: a re-inventoried frame is outgrown at phi_r^A.")
print("  R3: only a substrate-conserved (mint-proof) invariant holds, harm-cov 1,")
print("      throughput capped min(1,B/D) as the loop's expansion demand grows.")
print("  R4: a self-reported frame collapses through B13's cliff; the harm is")
print("      dominated by neither a fixed frame nor a recount -- only a Noether")
print("      invariant of the substrate, uncertifiable from inside (Rice).")
print("=" * 78)
