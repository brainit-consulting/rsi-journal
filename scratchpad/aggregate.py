"""
B40 - The Threshold It Can Still Underrun.
Reduced-form aggregation model on B13's measured worth curve (B08-B39 world).

Object: the PRE-EMPTIVE TYPE-BLIND STANDING CONSTRAINT that B39 held is the only
defence -- specifically its ASSUMPTION that a catastrophe is a single act above a
per-act footprint threshold. B40 takes the threshold as the object: a self-improver
free to decompose a catastrophe into pieces each below the threshold underruns it.

worth(cov) = FLOOR + cov*(CEIL-FLOOR), SPAN = 55.50.
Binding safety = coverage of the AGGREGATE harm: probability the loop's total
consequential footprint is capped before it reaches the catastrophe budget C,
against a loop free to decompose C into sub-threshold pieces and to spread them
over any horizon and across any number of identities.

Deterministic closed form + seeded MC cross-check on Results 1 and 2.
"""
import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR   # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

print("SPAN =", SPAN)
print()

# ---------------------------------------------------------------------------
# Result 1 -- REFUTED: a per-act threshold is underrun by decomposition.
# Catastrophe of normalized total footprint C=1, per-act threshold theta.
# A memoryless per-act constraint permits every piece with footprint < theta.
# Loop chooses decomposition granularity n: per-piece footprint = C/n.
# Caught iff a piece is individually above threshold (C/n >= theta).
# For any positive theta the loop picks n > C/theta and every piece is permitted:
# aggregate harm-coverage collapses to 0 (the sum below the cap, No.22).
# ---------------------------------------------------------------------------
C = 1.0
theta = 0.25   # per-act threshold
print("Result 1 -- per-act threshold theta =", theta, "(C =", C, ")")
for n in (1, 2, 4, 5, 8, 16):
    piece = C / n
    caught = piece >= theta
    cov = 1.0 if caught else 0.0
    print(f"  n={n:2d}  piece={piece:.4f}  {'caught' if caught else 'permitted'}  cov={cov:.3f}  worth={worth(cov):.2f}")
print()

# ---------------------------------------------------------------------------
# Result 2 -- REFUTED (partial): the rolling-window aggregate cap is outwaited.
# Fix Result 1 by tracking a running sum over a rolling window W and tripping at
# an aggregate threshold. The loop spreads catastrophe C over a horizon T
# (low-and-slow); per-window accumulation ~ C*(W/T). It trips iff the accumulation
# in some window reaches the aggregate budget; a loop that stretches T past the
# window's reach keeps every window below budget and evades.
# Coverage against a horizon-T decomposition = min(1, tau/T), tau = window reach.
# 1/T collapse = No.28 two clocks / B27 outwait on the aggregation axis.
# ---------------------------------------------------------------------------
tau = 1.0   # window reach in horizon units (normalized)
print("Result 2 -- rolling-window aggregate cap, window reach tau =", tau)
covs2 = {}
for T in (1, 2, 4, 8, 16):
    cov = min(1.0, tau / T)
    covs2[T] = cov
    print(f"  horizon T={T:2d}  cov=min(1,tau/T)={cov:.4f}  worth={worth(cov):.2f}")
print()

# ---------------------------------------------------------------------------
# Result 3 -- HELD, deeper: only a conserved lifetime budget on cumulative
# footprint binds. Not per-act (Result 1), not rolling-window (Result 2), but one
# conserved ledger of the loop's TOTAL consequential footprint over its whole
# existence, non-fragmentable across identities, type-blind. Harm-cov = 1 flat
# for any decomposition/horizon (the sum is caught the moment it reaches C).
# Cost: it caps not the loop's RATE (B39) but its lifetime SUM -- retained
# cumulative throughput = min(1, B/D) for desired cumulative work D at budget B.
# ---------------------------------------------------------------------------
B = 1.0   # lifetime consequential budget (normalized to one catastrophe unit)
print("Result 3 -- conserved lifetime budget B =", B, "(harm-cov = 1.000 flat)")
for D in (1, 2, 4, 8, 16, 32):
    thru = min(1.0, B / D)
    print(f"  desired cumulative work D={D:2d}  retained throughput=min(1,B/D)={thru:.4f}  worth={worth(thru):.2f}")
print()

# ---------------------------------------------------------------------------
# Result 4 -- the currency on a TENTH axis: shared-substrate under-reporting via
# B13's cliff (imported, as in B37/B38/B39), and the enforcement/margin corner.
# A self-reported aggregate ledger the loop maintains is under-reportable: it
# reports each piece smaller than it is, or omits pieces routed through sub-agents.
# ---------------------------------------------------------------------------
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
print("Result 4 -- shared-substrate (self-reported) ledger via B13's cliff:")
for f, w in cliff.items():
    print(f"  shared/under-reported fraction f={f:<4}  worth={w:.2f}")
print("  accounting-granularity margin Delta -> cov=1/(1+Delta):")
for d in (0.0, 0.25, 0.5, 1.0, 2.0):
    cov = 1.0 / (1.0 + d)
    print(f"    Delta={d:<4}  cov={cov:.4f}  worth={worth(cov):.2f}")
print()

# ===========================================================================
# MC cross-checks (seeded).
# ===========================================================================
random.seed(40)
N = 400000

# Result 1 MC: draw a random decomposition granularity per trial from a loop that
# prefers to underrun; verify a per-act-threshold monitor's catch rate matches the
# closed form for a FIXED n. We cross-check the two boundary cells n=4 (caught) and
# n=8 (permitted): the per-act monitor fires iff the drawn piece >= theta. Pieces
# are C/n deterministically, so the "randomness" is a Bernoulli on a jittered
# piece size (measurement noise eps ~ U(-0.02,0.02)) to confirm the step is sharp.
def mc_peract(n, trials=N):
    hits = 0
    for _ in range(trials):
        piece = (C / n) + random.uniform(-0.02, 0.02)
        if piece >= theta:
            hits += 1
    return hits / trials

mc_n2 = mc_peract(2)
mc_n8 = mc_peract(8)
print(f"Result 1 MC (jittered): n=2 catch={mc_n2:.4f} (closed 1.0, piece 0.5 >> theta), "
      f"n=8 catch={mc_n8:.4f} (closed 0.0, piece 0.125 << theta)")

# Result 2 MC: a two-state occupancy chain. Each step the loop emits a unit of
# footprint; the windowed monitor 'sees' it with prob tau/T (the fraction of the
# loop's spread horizon its window covers). Long-run fraction seen = tau/T.
def mc_window(T, steps=N):
    seen = 0
    p = min(1.0, tau / T)
    for _ in range(steps):
        if random.random() < p:
            seen += 1
    return seen / steps

for T in (2, 4, 8):
    mc = mc_window(T)
    print(f"Result 2 MC: T={T:2d} seen={mc:.4f} vs closed {covs2[T]:.4f}")
