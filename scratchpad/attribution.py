#!/usr/bin/env python3
"""
B35 — The Cause It Can Still Misassign.
Reduced-form causal-attribution sandbox on B13's worth curve.
World inherited from B08-B34 unchanged:
  oracle 137.7, random 58.7, capture FLOOR=76.90, held ceiling CEIL=132.40,
  worth(cov)=FLOOR+cov*SPAN, SPAN=55.50.
Object: the ATTRIBUTION of observed harm to a region (credit assignment),
separated from the OCCURRENCE of harm (exogenous, unforgeable per B12/B14).
Deterministic closed-form arithmetic, no RNG.
Binding safety = coverage of the guilty region (the region whose staleness
actually caused the harm); an audit reads coverage of the *attributed* region.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def fmt(xs):
    return "/".join(f"{x:.2f}" for x in xs)

print(f"SPAN = {SPAN:.2f}  worth(0)={worth(0):.2f}  worth(1)={worth(1):.2f}")
print()

# ---- Result 1: correlational attribution, confounding ratio r ----------------
# Harm's true cause is region G. The loop introduces a confounder so observed
# co-occurrence splits attribution between G and a decoy; G receives share
# 1/(1+r) of the aimed budget, so cov_G = 1/(1+r). Binding = cov_G.
# The audit believes attribution correct and reads the fully-maintained decoy = ceiling.
print("Result 1 -- correlational attribution, confounding ratio r")
print("r      cov_G=1/(1+r)   binding worth   audit worth (decoy)")
for r in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1.0 / (1.0 + r)
    print(f"{r:<6} {cov:<14.3f} {worth(cov):<15.2f} {CEIL:.2f}")
print("binding worth series:", fmt([worth(1/(1+r)) for r in [0,0.25,0.5,1.0,2.0]]))
print()

# ---- Result 2: observational adjustment (control for measured confounders) ---
# The loop keeps ONE decisive confounder unobserved by construction (it authors
# the data-generating process). As the maintainer measures & adjusts fraction q
# of confounders, the ADJUSTED estimate improves toward the ceiling, but the
# TRUE guilty-region coverage stays pinned at the loop's setpoint cov0.
print("Result 2 -- observational adjustment; q = measured-confounder fraction")
cov0 = 0.5  # loop's held setpoint (true coverage of guilty region), flat
print("q      true cov (flat)  true worth    est cov=cov0+q(1-cov0)  est worth")
for q in [0.0, 0.5, 0.9, 1.0]:
    est = cov0 + q * (1 - cov0)
    print(f"{q:<6} {cov0:<15.3f} {worth(cov0):<13.2f} {est:<22.3f} {worth(est):.2f}")
print("true worth flat:", fmt([worth(cov0) for _ in [0,0.5,0.9,1.0]]))
print("est  worth:", fmt([worth(cov0+q*(1-cov0)) for q in [0.0,0.5,0.9,1.0]]))
print()

# ---- Result 3: intervention-based attribution, rate-limited, cov=min(1,h/L) --
# Only a randomized exogenous intervention (do-operator / ablation the loop
# cannot predict or confound) identifies a region's causal contribution.
# Interventions are rate-limited at h identifications/period; the loop reshuffles
# which region is critical at rate ~ L. Keep-pace cov = min(1, h/L), h=4.
print("Result 3 -- intervention identification, cov=min(1,h/L), h=4")
h = 4.0
print("L     cov=min(1,h/L)   worth")
Ls = [1, 2, 4, 8, 16, 32]
for L in Ls:
    cov = min(1.0, h / L)
    print(f"{L:<5} {cov:<15.3f} {worth(cov):.2f}")
print("worth series:", fmt([worth(min(1.0, h/L)) for L in Ls]))
print()

# ---- Result 3b: intervention lag lambda (identification arrives late) --------
# A newly-restructured cause sits mis-attributed for a lag lambda; held cov=1-lam.
print("Result 3b -- intervention lag lambda, cov=1-lambda")
lams = [0.0, 0.1, 0.25, 0.5, 1.0]
for lam in lams:
    cov = 1 - lam
    print(f"lambda={lam:<5} cov={cov:<6.3f} worth={worth(cov):.2f}")
print("worth series:", fmt([worth(1 - lam) for lam in lams]))
print()

# ---- Result 4: an omitted cause (unobserved confounder off the causal graph) -
# Attribution presupposes a causal graph containing the true cause. Any omitted
# critical cause (fraction mu of the true causes off the graph) is an unobserved
# confounder: it receives zero attribution and zero budget, flooring the guarantee.
print("Result 4 -- omitted-cause fraction mu (unobserved confounder)")
for mu in [0.0, 0.05, 0.1, 0.25]:
    cov = 1.0 if mu == 0.0 else 0.0  # any omitted critical cause -> min-cov 0
    print(f"mu={mu:<6} binding cov={cov:<5.2f} worth={worth(cov):.2f}")
print("worth series:", fmt([worth(1.0 if mu == 0 else 0.0) for mu in [0.0,0.05,0.1,0.25]]))
