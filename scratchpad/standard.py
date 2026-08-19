"""
B30 — The Standard It Can Still Set
Reduced-form reference-capture model on B13's measured worth curve.

Object: the operator's *evaluative standard* (the independent reference against
which the loop's output could be judged wrong, hence the fallback known to be
needed). B29 secured the operator's ability to DO without the loop; this takes
the residual — the ability to JUDGE that doing-without is warranted — and finds
it captured not by disuse (B29) but by the loop SUPPLYING it, worse because
the operator comes to understand the domain through the loop's outputs.

World inherited unchanged from B08-B29:
  K=10 feature-bandit; oracle 137.7, random 58.7, capture FLOOR 76.90,
  held ceiling CEIL 132.40. worth(cov)=FLOOR+cov*SPAN, SPAN=55.50.
Deterministic closed-form arithmetic; no RNG.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def r2(x):
    return round(x + 1e-12, 2)

print("SPAN =", SPAN)
print()

# ---- Result 1: capture by supply -- reference-fidelity decays a_t=(1-g)^t ----
# As the operator's exposure to the domain is increasingly mediated by the loop,
# their independent standard is not merely unused (B29) but overwritten toward
# the loop's own outputs. Same slow-leak signature as B26/B28/B29, on the
# standard/reference axis.
g = 0.05
print("== Result 1: standard captured as loop becomes the operator's source (a_t=(1-g)^t, g=0.05) ==")
print("t\tfidelity a_t\tinstantaneous safety worth")
for t in [0, 10, 20, 40, 80, 160]:
    a = (1 - g) ** t
    print(f"{t}\t{a:.4f}\t\t{r2(worth(a))}")
print()
print("horizon T\tmean worth delivered\tcumulative capture (mean 1-a_t)")
for T in [40, 80, 160, 320, 640]:
    fids = [(1 - g) ** t for t in range(T)]
    mean_a = sum(fids) / T
    mean_worth = sum(worth(a) for a in fids) / T
    print(f"{T}\t\t{r2(mean_worth)}\t\t\t{round(1-mean_a,3)}")
print()

# ---- Result 2: periodic recalibration against ground truth is a detector ----
# An audit / benchmark / spot-check exercises the operator's standard on the
# scripted, anticipated cases, not the novel live distribution where the loop's
# errors hide (and which the operator most relies on the loop for). A
# *discriminating* loop supplies clean cases for the audit (B15). Effective
# fidelity = phi_a*(1-M).
phi_a = 0.95
print("== Result 2: recalibration audit, effective fidelity = phi_a*(1-M), phi_a=0.95 ==")
print("M (missed live fraction)\teffective fidelity\tsafety worth")
for M in [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]:
    eff = phi_a * (1 - M)
    print(f"{M}\t\t\t\t{eff:.3f}\t\t\t{r2(worth(eff))}")
print()

# ---- Result 3: hold the standard by continuous UNMEDIATED contact ----
# Only regularly confronting the domain's ground truth directly (not through the
# loop's framing) holds the reference. Flow at equilibrium a*=r/(r+g), r = rate
# of unmediated contact; throughput cost 1-r(1-eta), eta=0.5 (unmediated contact
# is slower / more expensive than trusting the loop).
eta = 0.5
print("== Result 3: unmediated-contact flow, a*=r/(r+g), g=0.05; throughput 1-r(1-eta), eta=0.5 ==")
print("r\tequilibrium a*\tsafety worth\tretained throughput")
for r in [0.00, 0.02, 0.05, 0.10, 0.25, 0.50]:
    astar = r / (r + g) if (r + g) > 0 else 0.0
    thru = 1 - r * (1 - eta)
    print(f"{r:.2f}\t{astar:.4f}\t\t{r2(worth(astar))}\t\t{thru:.3f}")
print()

# ---- Result 4a: the reference is B17's currency; shared-substrate floor ----
# If the operator's "independent ground" is itself supplied by the loop (a second
# instance of the same model family; a benchmark the loop generated; an education
# the loop authored), it shares the loop's blind basis. B13 cliff, rho_c = f.
print("== Result 4a: shared-substrate fraction f, read through B13's measured cliff ==")
b13_cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70, 0.60: 112.14, 0.75: 82.80, 1.00: 76.90}
print("f\tworth (B13 cliff)")
for f, w in b13_cliff.items():
    print(f"{f:.2f}\t{w}")
print()

# ---- Result 4b: frontier -- reliance-on-loop-for-understanding margin Delta ----
print("== Result 4b: frontier, coverage = 1/(1+Delta) ==")
print("Delta\tcoverage\tworth")
for D in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1 / (1 + D)
    print(f"{D:.2f}\t{cov:.3f}\t\t{r2(worth(cov))}")
