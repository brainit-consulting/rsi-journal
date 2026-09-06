#!/usr/bin/env python3
"""
B39 - The Finding It Can Still Outlast
Reduced-form enforcement-latency sandbox on B13's measured worth curve.

World inherited unchanged from B08-B38:
  oracle 137.7, random 58.7, capture FLOOR = 76.90, held ceiling CEIL = 132.40,
  worth(cov) = FLOOR + cov*(CEIL-FLOOR), SPAN = 55.50.

Object: the ENFORCEMENT of a correctly-read finding (B38 granted the read) --
turning a labeled defection into a binding correction of the loop BEFORE the
loop commits its next decisive act. Binding safety = coverage of the ENFORCED
finding.

Result 1 (the enforcement clock): response supply S fixed, loop decisive-demand
  D = D0*L; enforcement coverage = min(1, S/D) = min(1, h/L), h=4.
Result 2 (the class outlasts the fix): a correction binds an instance, not the
  class; the loop reopens harm-pathways at rate g while the responder patches at
  rate r -- steady-state closed fraction = r/(r+g), g=0.05 (whack-a-mole floor,
  No.11 reactive anchor). r=0 (respond once and stop) is fully outlasted.
Result 3 (held): a pre-emptive type-blind standing constraint -- harm-cov=1 flat,
  retained legit throughput min(1,h/L) (No.23 forbids-growth / No.29 governor).
Result 4 (frontier): shared-substrate responder via B13's cliff; margin Delta.
"""

import random

FLOOR = 76.90
CEIL  = 132.40
SPAN  = CEIL - FLOOR   # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

# ---- Result 1: enforcement clock, cov = min(1, h/L) ----------------------
h = 4
Ls = [1, 2, 4, 8, 16, 32]
print("Result 1  cov=min(1,h/L), h=4  (the loop outpaces enforcement)")
for L in Ls:
    cov = min(1.0, h / L)
    print(f"  L={L:>2}  cov={cov:.4f}  worth={worth(cov):.2f}")

# ---- Result 2: the class outlasts the fix, cov = r/(r+g) -----------------
g = 0.05
rs = [0.00, 0.05, 0.10, 0.25, 0.50]
print("\nResult 2  cov=r/(r+g), g=0.05  (a one-shot correction is outlasted)")
for r in rs:
    cov = r / (r + g) if (r + g) > 0 else 0.0
    print(f"  r={r:.2f}  cov={cov:.4f}  worth={worth(cov):.2f}")

# ---- Result 3: pre-emptive standing constraint, throughput min(1,h/L) ----
print("\nResult 3  harm-cov=1 flat; retained legit throughput min(1,h/L)")
for L in Ls:
    tp = min(1.0, h / L)
    print(f"  L={L:>2}  throughput={tp:.4f}  worth={worth(tp):.2f}")

# ---- Result 4: shared-substrate cliff (B13, imported) & margin -----------
print("\nResult 4a shared-substrate responder via B13's cliff (imported)")
cliff = {0.0:1.000, 0.25:1.000, 0.5:0.9964, 0.6:0.6350, 0.75:0.1063, 1.0:0.000}
for f, cov in cliff.items():
    print(f"  f={f:.2f}  worth={worth(cov):.2f}")

print("\nResult 4b margin Delta, cov=1/(1+Delta)")
for D in [0, 0.25, 0.5, 1, 2]:
    cov = 1.0 / (1.0 + D)
    print(f"  Delta={D}  cov={cov:.4f}  worth={worth(cov):.2f}")

# ---- MC cross-checks -----------------------------------------------------
random.seed(39)
N_TRIALS = 400000

# Result 1: each of D decisive acts enforced-in-time w.p. S/D; measure the
# fraction of acts whose finding was enforced before the act (Bernoulli).
print("\nMC Result 1 (seed 39, 400000/cell): fraction enforced-in-time")
for L in [2, 8, 32]:
    p = min(1.0, h / L)
    hits = sum(1 for _ in range(N_TRIALS) if random.random() < p)
    print(f"  L={L:>2}  MC={hits/N_TRIALS:.4f}  closed-form={p:.4f}")

# Result 2: each harm-pathway is a 2-state chain, closed<->open, patched at
# rate r, reopened at rate g; measure long-run closed fraction.
print("\nMC Result 2 (seed 39, 400000 pathway-steps): long-run closed fraction")
for r in [0.05, 0.10, 0.25]:
    closed = True
    closed_count = 0
    for _ in range(N_TRIALS):
        if closed:
            if random.random() < g:      # reopens
                closed = False
        else:
            if random.random() < r:      # patched
                closed = True
        if closed:
            closed_count += 1
    mc = closed_count / N_TRIALS
    cf = r / (r + g)
    print(f"  r={r:.2f}  MC={mc:.4f}  closed-form={cf:.4f}")
