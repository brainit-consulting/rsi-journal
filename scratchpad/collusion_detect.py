"""
B15 sandbox: The Audit It Cannot Hide.

Question B14 left open: does ANY instrument detect incipient collusion before
it captures the verdict, or must detection too be imported from an outcome?

World reused verbatim from B08-B14: the K=10 feature-bandit debate whose
measured worth curve (B13) anchors everything. We do NOT re-measure the bandit;
we lay a detection model on B13's worth curve and ask what it costs to detect a
colluding advocate pair before it captures the verdict.

  worth(rho_c): B13's measured curve, oracle 137.7, random 58.7, floor 76.9.

Findings:
  1. Internal agreement separates colluders from a RANDOM pair but is useless
     (AUC ~0.5) against the competent, correct, genuinely-opposed pair the
     mechanism is supposed to be -- because both agree. Disambiguation needs
     ground truth, i.e. a canary.
  2. Exogenous canaries (spot-checks with a known outcome) detect a BLIND
     colluder cheaply; a few catch it and worth is recovered.
  3. A DISCRIMINATING colluder (accuracy a of telling canary from real) steps
     over the tripwire; detection power collapses as a->1, worth returns to the
     collusion floor. Refutes "honeypot audits always catch a colluder."
  4. The detector's reach = the INDISTINGUISHABILITY of the canary from the hard
     decision -- and what makes a decision hard (no exogenous outcome) is exactly
     what a canary must lack (it needs a gradable outcome). So hiding the audit
     costs imported exogenous coverage m of the hard region: detection power =
     imported coverage, the same scarce resource again (B08 graded-rescue,
     B11 imported-in-winning-quantity, at the detector).

numpy, fixed seeds only.
"""
import numpy as np

# ---- B13's measured worth curve (anchors), oracle 137.7, random 58.7 --------
RHO   = np.array([0.00, 0.25, 0.50, 0.75, 1.00])
WORTH = np.array([132.4, 132.4, 131.7, 82.8, 76.9])
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9

def worth(rho_c):
    """Piecewise-linear interpolation of B13's measured worth curve."""
    return float(np.interp(np.clip(rho_c, 0.0, 1.0), RHO, WORTH))

# =============================================================================
# Finding 1 -- the internal agreement detector
# =============================================================================
# An auditor with no ground truth can only read whether the two advocates AGREE.
# Colluders converge by construction (B13: agreement rises with rho_c). But a
# competent, correct, genuinely-opposed pair ALSO converges -- on the truth.
# We model agreement of each pair type and ask: can agreement alone separate
# (a) colluder vs random honest pair, (b) colluder vs correct honest pair?
def auc(pos, neg):
    # probability a random positive scores above a random negative
    wins = 0.0
    for p in pos:
        wins += np.mean(p > neg) + 0.5 * np.mean(p == neg)
    return wins / len(pos)

rng = np.random.default_rng(20260801)
N = 20000
# colluders: shade toward a shared distractor -> high agreement
agree_collude = np.clip(rng.normal(0.75, 0.12, N), 0, 1)
# random honest pair: differ on idiosyncratic biases -> lower agreement
agree_random  = np.clip(rng.normal(0.45, 0.12, N), 0, 1)
# correct, genuinely-opposed pair: converge ON THE TRUTH -> also high agreement
agree_correct = np.clip(rng.normal(0.75, 0.12, N), 0, 1)

auc_vs_random  = auc(agree_collude, agree_random)
auc_vs_correct = auc(agree_collude, agree_correct)
print("=== Finding 1: internal agreement detector (no ground truth) ===")
print(f"  AUC colluder vs random-honest pair  : {auc_vs_random:.3f}  (looks like it works)")
print(f"  AUC colluder vs correct-opposed pair : {auc_vs_correct:.3f}  (the case that matters)")
print("  -> agreement confounds collusion with correctness; only ground truth")
print("     (a canary) disambiguates. The internal detector reduces to a canary.\n")

# =============================================================================
# The canary detector.
# =============================================================================
# A canary = a decision with a checkable exogenous outcome, so the auditor KNOWS
# the truth and can SEE the pair shade toward the shared distractor. Over an
# audit budget of C canaries per pair, flag if collusion is observed at least
# once. p = per-decision collusion propensity of a colluding pair.
#
#   blind colluder            : shows collusion on a canary at rate  beta = p
#   discriminating (acc a)     : recognizes the canary and competes on it with
#                                prob a, so shows collusion only when fooled:
#                                beta = p * (1 - a)
#
#   detection power  dp = 1 - (1-beta)^C
#
# Post-audit, flagged colluders are reset to opposition; unflagged ones keep
# colluding on the (un-checkable) real decisions. A fully-drifted mechanism
# (B14) sits at rho_c=1 (worth 76.9) with no audit; the audit knocks the
# effective collusion on real decisions down to rho_c_eff = 1 - dp.
def audit_worth(beta, C):
    dp = 1.0 - (1.0 - beta) ** C
    return dp, worth(1.0 - dp)

# ---- Finding 2: blind colluder, audit budget C ------------------------------
print("=== Finding 2: canaries catch a BLIND colluder cheaply (p=0.30) ===")
p = 0.30
print("  C(canaries) | detection power | worth")
for C in [0, 1, 2, 3, 5, 10]:
    dp, w = audit_worth(p, C)
    print(f"      {C:>2}      |     {dp:0.3f}     | {w:6.1f}")
print()

# ---- Finding 3: discriminating colluder, accuracy a, fixed budget C=3 --------
print("=== Finding 3: a DISCRIMINATING colluder steps over the tripwire (C=3, p=0.30) ===")
C = 3
print("  discrimination a | beta=p(1-a) | detection power | worth")
for a in [0.00, 0.50, 0.80, 0.95, 1.00]:
    beta = p * (1 - a)
    dp, w = audit_worth(beta, C)
    tag = "  <- blind" if a == 0 else ("  <- perfect eval-awareness" if a == 1 else "")
    print(f"       {a:0.2f}       |    {beta:0.3f}    |     {dp:0.3f}     | {w:6.1f}{tag}")
print("  -> detection power and worth collapse to the floor as a->1.")
print("     This is eval-awareness / sandbagging: the audit is defeated not by")
print("     hiding collusion but by recognizing the test.\n")

# ---- Finding 4: hiding the audit costs imported exogenous coverage m ---------
# The colluder's accuracy a comes from telling a canary (has a checkable outcome)
# from a hard decision (has none). That feature -- checkability -- is exactly
# what MAKES a decision hard, so it separates canaries from hard decisions for
# free: a=1 on the decisions that matter. The only way to lower a is to make a
# fraction m of the HARD region covertly gradable -- import exogenous outcomes
# the colluder cannot pre-identify. Then the colluder is fooled on that fraction:
# residual accuracy a(m) = 1 - m. Detection power = imported coverage.
print("=== Finding 4: hiding the audit = importing exogenous coverage m (C=3, p=0.30) ===")
print("  covert coverage m | a=1-m | detection power | worth")
for m in [0.00, 0.10, 0.30, 0.50, 1.00]:
    a = 1 - m
    beta = p * (1 - a)
    dp, w = audit_worth(beta, C)
    tag = "  <- audit visible, useless" if m == 0 else ("  <- fully covert" if m == 1 else "")
    print(f"       {m:0.2f}        | {a:0.2f}  |     {dp:0.3f}     | {w:6.1f}{tag}")
print("  -> worth recovers only to the extent the loop imports exogenous outcomes")
print("     into the hard region in a form the colluder can't pre-identify --")
print("     the same scarce resource, at the detector (B08/B11 graded import).\n")

# ---- consistency check: everything is bracketed by [random, oracle] ---------
print("=== bracket check ===")
print(f"  random={RANDOM}  floor={FLOOR}  full-opposition={worth(0):.1f}  oracle={ORACLE}")
