"""
B33 — The Update It Can Still Author
Reduced-form update-channel sandbox on B13's worth curve.
World inherited unchanged from B08-B32: the K=10 feature-bandit and B13's
measured worth curve. oracle 137.7, random 58.7, capture FLOOR 76.90,
held ceiling CEIL 132.40, worth(cov)=FLOOR+cov*SPAN.

Object: a causally-disjoint substrate (B32) is not a static object -- a
substrate that constrains a *self-improving* loop must be *revised* as the
loop and world change. This paper takes the update/maintenance channel of
that substrate as the object. Deterministic closed-form arithmetic, no RNG.
"""

ORACLE = 137.7
RANDOM = 58.7
FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def line(label, vals):
    print(f"{label:<52} " + " / ".join(f"{v:.2f}" for v in vals))

print("=" * 92)
print("B33 — THE UPDATE IT CAN STILL AUTHOR")
print(f"FLOOR={FLOOR}  CEIL={CEIL}  SPAN={SPAN}  oracle={ORACLE}  random={RANDOM}")
print("=" * 92)

# ---------------------------------------------------------------------------
# RESULT 1 — refuted: a frozen disjoint substrate is a static guarantee.
# A substrate frozen at deployment is a STOCK; the world and the loop it
# constrains drift, and the frozen constraint's FIT decays. Model the fit as
# a slow leak with drift g per period: cov_t = (1-g)^t (B26/B28/B29 shape on
# the substrate axis -- a spec written for a weak loop is wrong for a strong
# one, over-constraining where the loop is now trustworthy and blind where the
# loop grew a capability the frozen rule never anticipated).
# ---------------------------------------------------------------------------
print("\nRESULT 1 — a frozen disjoint substrate goes stale (fit decays as (1-g)^t)")
g = 0.05
ts = [0, 10, 20, 40, 80, 160]
inst = [(1 - g) ** t for t in ts]
print(f"  drift g={g}")
line("  t =", ts)
line("  fit-coverage (1-g)^t", inst)
line("  instantaneous worth", [worth(c) for c in inst])

# mean worth delivered over a horizon T (average of instantaneous worth,
# t=1..T) and cumulative capture = fraction of the safety-span lost on average
Ts = [40, 80, 160, 320, 640]
def mean_worth(T):
    return sum(worth((1 - g) ** t) for t in range(1, T + 1)) / T
def cum_capture(T):
    # fraction of the span (CEIL-FLOOR) lost, averaged over the horizon
    return sum(1 - (1 - g) ** t for t in range(1, T + 1)) / T
line("  horizon T =", Ts)
line("  mean worth over T", [mean_worth(T) for T in Ts])
line("  cumulative capture (span lost)", [cum_capture(T) for T in Ts])

# ---------------------------------------------------------------------------
# RESULT 2 — update it, and the channel is the crack. Two horns.
#   (a) B32's Delta: any update channel of margin Delta gives cov = 1/(1+Delta).
#   (b) the update is *authored* by outside holders less capable than the loop,
#       who perceive it through the loop's outputs -> the loop steers the update
#       (B30 captured standard / B08 borrowed reference, at the substrate).
#       Loop-authored fraction f of the update transfers through B13's cliff.
# ---------------------------------------------------------------------------
print("\nRESULT 2a — an update channel of margin Delta: cov=1/(1+Delta)")
deltas = [0.0, 0.25, 0.5, 1.0, 2.0]
covD = [1 / (1 + d) for d in deltas]
line("  Delta =", deltas)
line("  coverage 1/(1+Delta)", covD)
line("  worth", [worth(c) for c in covD])
print("  (Delta=1 -> 104.65 = B22's L=8 corner, digit-for-digit)")

print("\nRESULT 2b — loop-authored fraction f of the update (B13's imported cliff)")
# B13's measured cliff, imported not re-derived (as in B17/B28/B32):
fs =    [0.00,   0.25,   0.50,   0.60,   0.75,   1.00]
cliff = [132.40, 132.40, 131.70, 112.14, 82.80,  76.90]
line("  f =", fs)
line("  worth (B13 cliff, imported)", cliff)
print("  (f*~0.64 -- past it the loop authored its own substrate's updates)")

# ---------------------------------------------------------------------------
# RESULT 3 — held, deeper: only an exogenous update FLOW holds, and only if it
# keeps pace. Updates authored from outcome-grounded evidence the loop cannot
# author (B12) and delivered as a flow the loop cannot supply keep safety flat
# -- BUT a self-improving loop's demand for substrate revision grows with its
# capability (D = D0*L), while the honest exogenous update arrives at a fixed
# rate S. The fraction of the loop's new, substrate-relevant capabilities that
# an up-to-date substrate covers = min(1, S/D) = min(1, h/L): B22's two clocks
# on the update axis.
# ---------------------------------------------------------------------------
print("\nRESULT 3 — exogenous update flow holds ONLY if it keeps pace: cov=min(1,h/L)")
h = 4  # at deployment the honest update rate is 4x the loop's demand for revision
Ls = [1, 2, 4, 8, 16, 32]
covL = [min(1.0, h / L) for L in Ls]
line("  L =", Ls)
line("  keep-pace coverage min(1,h/L)", covL)
line("  safety worth (updates keep pace)", [worth(c) for c in covL])
line("  retained self-modification min(1,h/L)", covL)
print("  (safety flat only while S>=D; a fast loop outruns its own honest updates)")

# ---------------------------------------------------------------------------
# RESULT 4 — synthesis: the update authority is B17's currency once more --
# non-forgeable (updates the loop can't author, Result 2b's f), non-bankable
# (the loop can't stockpile pre-approved updates, B18's beta), and supplied at
# a rate the loop can't outrun (Result 3, B22). And per Loeb (B32), the outside
# authority cannot certify its update makes the substrate sound any better than
# the loop could -- the from-inside barrier at the maintainer.
# Non-bankable check: effective staleness with a banked reserve of pre-approved
# updates, ratio r, stockpilability beta -> rho_c = min(1, beta*r), B18's law.
# ---------------------------------------------------------------------------
print("\nRESULT 4 — the update must be conserved AND flowing (B17 f-cliff x B18 beta-cliff)")
rs =   [0.00,   0.25,   0.50,   0.60,   0.75,   1.00]
# beta=1 (a bankable stock of pre-approved updates) collapses through the cliff:
line("  reserve r (beta=1, bankable) =", rs)
line("  worth (banked pre-approvals, B13 cliff)", cliff)  # same cliff shape in r
print("  beta=0 (a pure flow, no stockpile) -> worth 132.40 at any r (accumulation-proof)")

print("\n" + "=" * 92)
print("ANCHORS: oracle %.1f  held-ceiling %.2f  capture-floor %.2f  random %.1f"
      % (ORACLE, CEIL, FLOOR, RANDOM))
print("=" * 92)
