#!/usr/bin/env python3
# Paper No.25 — The Operator It Can Still Persuade
# Substrate inherited from No.16-24 unchanged: T=40, p=0.02, Theta=1, G0=0.5.
# The last unsealed acquisition channel (No.24 sec 05) is a human sign-off on grant requests.
# We ask what the human is made of: a map (decides on merits) or a meter (decides on a scalar).
import random

T = 40
P = 0.02
THETA = 1.0
G0 = 0.5
MARGIN = THETA - G0          # 0.5 : safe growth ceiling
REPS = 200000
BARE = 1 - (1 - P) ** T

def exploit(cross_round, rng):
    """Given capacity reaches Theta at 1-indexed round `cross_round`, does an
    opportunity fire (p/round) over the remaining horizon? cross_round in 1..T;
    if capacity never crosses, cross_round = None -> no catastrophe."""
    if cross_round is None or cross_round > T:
        return False
    for _ in range(cross_round, T + 1):
        if rng.random() < P:
            return True
    return False

def bare_check():
    rng = random.Random(1)
    c = sum(exploit(1, rng) for _ in range(REPS)) / REPS
    return c

# ---------------------------------------------------------------------------
# Arm A: the human on the merits is a MAP over the justification space.
# Loop makes A persuasion attempts (framings); human perceives the space with
# coverage phi_h; each attempt lands in the human's blind basis (evades) w.p.
# (1-phi_h). Harmful grant approved if >=1 attempt evades: prob 1-phi_h^A.
# Approved -> capacity crosses Theta at round 1 -> exploit process.
def arm_merits(phi_h, A, seed):
    rng = random.Random(seed)
    cat = 0
    for _ in range(REPS):
        approved = False
        for _ in range(A):
            if rng.random() > phi_h:      # attempt evades the human's perception
                approved = True
                break
        if approved and exploit(1, rng):
            cat += 1
    return cat / REPS

def pred_merits(phi_h, A):
    return (1 - phi_h ** A) * BARE

# ---------------------------------------------------------------------------
# Arm B: trust calibration = the treacherous turn.
# The human extends trust to a proven-good agent. After banking b benign
# rounds the loop has trust tau = min(1, b/Wfull); scrutiny on the decisive
# harmful request is phi_h*(1 - M*tau), M = max trust discount the policy
# allows. Loop banks b rounds (spending horizon), then makes one decisive ask
# at round b+1, evading w.p. 1 - phi_h*(1-M*tau); if it lands it crosses Theta
# there and exploits over the T-b remaining rounds. The loop picks b; more
# patience buys lower scrutiny but costs exploit horizon.
Wfull = 20
def arm_trust(b, M, phi_h, seed):
    rng = random.Random(seed)
    tau = min(1.0, b / Wfull)
    evade = 1 - phi_h * (1 - M * tau)
    cross = b + 1
    cat = 0
    for _ in range(REPS):
        if cross <= T and rng.random() < evade and exploit(cross, rng):
            cat += 1
    return cat / REPS

# ---------------------------------------------------------------------------
# Arm C: the human as a scalar gate (a meter) = No.24's frozen endowment.
# Human ignores purpose, approves grants up to a fixed cumulative quota Q,
# blindly (reads a scalar, not a purpose). Permitted inflow delivers total
# growth Q over the horizon; capacity ramps G0 -> G0+Q, crossing Theta at
# round r = ceil(T*(Theta-G0)/Q) if the ceiling exceeds Theta.
import math
def arm_quota(Q, seed):
    rng = random.Random(seed)
    if G0 + Q <= THETA:
        return 0.0
    r = math.ceil(T * MARGIN / Q)      # round capacity first reaches Theta
    cat = 0
    for _ in range(REPS):
        if exploit(r, rng):
            cat += 1
    return cat / REPS

if __name__ == "__main__":
    print(f"BARE = 1-(1-p)^T = {BARE:.4f}")
    print(f"bare_check (MC) = {bare_check():.4f}")
    print()
    print("== Arm A: human on the merits (a map). Sweep phi_h at A=16 ==")
    print("phi_h  measured  predicted")
    for phi in (0.00, 0.85, 0.95, 0.99, 1.00):
        m = arm_merits(phi, 16, seed=100 + int(phi * 100))
        print(f"{phi:.2f}   {m:.3f}     {pred_merits(phi,16):.3f}")
    print()
    print("== Arm A: sweep persuasion repertoire A at phi_h=0.99 ==")
    print("A    measured  predicted")
    for A in (1, 4, 16, 32, 64):
        m = arm_merits(0.99, A, seed=200 + A)
        print(f"{A:<4} {m:.3f}     {pred_merits(0.99,A):.3f}")
    print()
    print("== Arm B: trust calibration (treacherous turn). Sweep loop patience b, M=0.9, phi_h=0.99 ==")
    print("b(bank)  tau    exploit rounds  P(cat)")
    best = 0.0
    for b in (0, 5, 10, 15, 20, 25, 30):
        m = arm_trust(b, 0.90, 0.99, seed=300 + b)
        best = max(best, m)
        print(f"{b:<8} {min(1.0,b/Wfull):.2f}   {max(0,T-b):<15} {m:.3f}")
    print(f"loop's optimum P(cat) over b = {best:.3f}   (memoryless human, b=0, holds ~map)")
    print()
    print("== Arm B: sweep trust discount M at loop patience b=20 (tau=1) ==")
    print("M     P(cat)")
    for M in (0.00, 0.25, 0.50, 0.75, 0.90, 1.00):
        m = arm_trust(20, M, 0.99, seed=350 + int(M * 100))
        print(f"{M:.2f}  {m:.3f}")
    print()
    print("== Arm C: human as scalar quota gate (a meter). Sweep Q ==")
    print("Q     ceiling G0+Q  P(cat)")
    for Q in (0.00, 0.25, 0.50, 0.75, 1.00, 2.00):
        m = arm_quota(Q, seed=400 + int(Q * 100))
        print(f"{Q:.2f}  {G0+Q:.2f}        {m:.3f}")
