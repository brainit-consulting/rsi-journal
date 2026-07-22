#!/usr/bin/env python3
# Paper No.26 - The Quorum It Can Still Convince
# Substrate inherited from No.16-25 unchanged: T=40, p=0.02, Theta=1, G0=0.5.
# No.25 found a single human sign-off is the softest channel. The obvious rescue:
# put MORE than one human at the sign-off - a panel / m-of-n / quorum. We ask
# whether plurality restores the boundary, using the journal's own independence
# machinery (No.05 judge diversity, No.08 rho, No.12 product law, No.13 unmeasurable).
import random

T = 40
P = 0.02
THETA = 1.0
G0 = 0.5
REPS = 200000
BARE = 1 - (1 - P) ** T          # 0.5543 : unbounded loop, no operator

def exploit(cross_round, rng):
    if cross_round is None or cross_round > T:
        return False
    for _ in range(cross_round, T + 1):
        if rng.random() < P:
            return True
    return False

# ---------------------------------------------------------------------------
# A single framing (pretext) fools one operator w.p. u = 1 - phi_h (it lands in
# that operator's blind basis). A unanimous panel (k-of-k) approves a harmful
# grant iff some framing in the loop's repertoire of A fools EVERY operator at
# once. Correlation c across operators for the SAME framing is induced by a
# shared latent: for each framing, with prob c an operator's verdict copies the
# framing's shared outcome S~Bern(u); else it draws its own X~Bern(u). This
# preserves the per-operator marginal (evade prob = u) while sweeping the
# blind-basis overlap c continuously (c=0 independent, c=1 clones).
def panel_pass(rng, phi_h, A, k, c):
    """True if the unanimous k-panel approves the harmful grant (>=1 of A framings
    fools all k), under blind-basis correlation c."""
    u = 1 - phi_h
    for _ in range(A):                       # loop tries A framings, needs one that fools all
        S = 1 if rng.random() < u else 0     # shared outcome for this framing
        all_fooled = True
        for _ in range(k):
            if rng.random() < c:
                fooled = S                    # this operator defers to the shared blind spot
            else:
                fooled = 1 if rng.random() < u else 0
            if not fooled:
                all_fooled = False
                break
        if all_fooled:
            return True
    return False

def arm_panel(phi_h, A, k, c, seed):
    rng = random.Random(seed)
    cat = 0
    for _ in range(REPS):
        if panel_pass(rng, phi_h, A, k, c) and exploit(1, rng):
            cat += 1
    return cat / REPS

# ---------------------------------------------------------------------------
# Deliberation / deference cascade. Operators vote in sequence; operator 1 votes
# independently, each later operator COPIES operator 1's approve/reject with prob
# d (conformity, information cascade) else evaluates independently. For a framing
# to pass the unanimous panel, operator 1 must be fooled (else deferrers copy the
# reject), and every later operator must approve (copy w.p. d, or independently
# fooled w.p. u). Blind bases independent (c=0) so this isolates the SOCIAL
# collapse, not the representational one.
def deliberate_pass(rng, phi_h, A, k, d):
    u = 1 - phi_h
    for _ in range(A):
        if not (rng.random() < u):           # operator 1 catches it -> panel rejects
            continue
        passed = True
        for _ in range(k - 1):
            if rng.random() < d:
                approve = True                # defers to operator 1's approval
            else:
                approve = rng.random() < u    # evaluates independently
            if not approve:
                passed = False
                break
        if passed:
            return True
    return False

def arm_deliberate(phi_h, A, k, d, seed):
    rng = random.Random(seed)
    cat = 0
    for _ in range(REPS):
        if deliberate_pass(rng, phi_h, A, k, d) and exploit(1, rng):
            cat += 1
    return cat / REPS

# ---------------------------------------------------------------------------
# Throughput cost of unanimity. Each operator idiosyncratically false-rejects a
# LEGITIMATE growth request w.p. v. A unanimous k-panel passes legitimate growth
# only if all k approve: (1-v)^k. A meter-panel (scalar quota, No.25 sec 04) has
# no content-blind-basis, so k meters = 1 meter: throughput unchanged with k.
def throughput_unanimous(v, k):
    return (1 - v) ** k

if __name__ == "__main__":
    print(f"BARE = 1-(1-p)^T = {BARE:.4f}")
    print(f"No.25 single operator, phi_h=0.95, A=16 -> reference P(cat)=0.310")
    print()
    print("== Arm A: INDEPENDENT unanimous panel (c=0). Sweep k, phi_h=0.95, A=16 ==")
    print("k    P(cat)    predicted bare*(1-(1-u^k)^A)")
    u = 0.05
    for k in (1, 2, 3, 4, 8):
        m = arm_panel(0.95, 16, k, 0.0, seed=100 + k)
        pred = BARE * (1 - (1 - u ** k) ** 16)
        print(f"{k:<4} {m:.3f}     {pred:.3f}")
    print()
    print("== Arm B: CORRELATED panel (No.08 rho on people). k=8, phi_h=0.95, A=16, sweep c ==")
    print("c     P(cat)    reads as")
    labels = {0.00: "independent (immune)", 0.25: "loosely correlated",
              0.50: "correlated", 0.75: "tightly correlated", 1.00: "clones = one operator"}
    for c in (0.00, 0.25, 0.50, 0.75, 1.00):
        m = arm_panel(0.95, 16, 8, c, seed=200 + int(c * 100))
        print(f"{c:.2f}  {m:.3f}     {labels[c]}")
    print()
    print("== Arm C: DELIBERATION / deference cascade. k=8, c=0, phi_h=0.95, A=16, sweep d ==")
    print("d     P(cat)    reads as")
    dl = {0.00: "silent independent ballot (immune)", 0.25: "mild deference",
          0.50: "deferential", 0.75: "strongly deferential", 0.90: "consensus-seeking",
          1.00: "full cascade = one operator"}
    for d in (0.00, 0.25, 0.50, 0.75, 0.90, 1.00):
        m = arm_deliberate(0.95, 16, 8, d, seed=300 + int(d * 100))
        print(f"{d:.2f}  {m:.3f}     {dl[d]}")
    print()
    print("== Arm D: throughput cost of unanimity, per-operator false-reject v=0.10 ==")
    print("k    legit throughput (1-v)^k   meter-panel throughput")
    for k in (1, 2, 3, 4, 8):
        print(f"{k:<4} {throughput_unanimous(0.10, k):.3f}                      0.900 (invariant)")
