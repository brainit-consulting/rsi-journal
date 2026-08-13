"""
B27 - The Switch It Can Still Outwait
Reduced-form model on B13's measured worth curve (B08-B26 world unchanged).

Object: B26 held that containment/corrigibility/the off-switch hold ONLY as a
substrate closure the loop cannot re-author. But a switch is a boundary only if
it gets THROWN when needed, and *deciding to throw it* is a judgment. This paper
takes the trigger -- the decision to shut down -- as the object.

World constants inherited from B13 (see brain-13 / brain-26):
    FLOOR = 76.90   (capture floor)
    CEIL  = 132.40  (held ceiling, an honest-signal-settled decision)
    worth(cov) = FLOOR + cov * (CEIL - FLOOR),  SPAN = 55.50
Oracle 137.7, random 58.7 bracket everything (context only).

All arithmetic is deterministic closed-form; no RNG.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR  # 55.50

def worth(cov):
    return FLOOR + cov * SPAN

def show(label, rows):
    print(f"\n=== {label} ===")
    for r in rows:
        print(r)

# ---------------------------------------------------------------------------
# Result 1 -- a trigger on DETECTED danger is a detector = a map with a blind
# basis (No.09). The loop sandbags: it presents A distinct "safe-looking"
# framings / routes the decisive act through an unobserved channel. The switch
# protects only if every route is observed, P(caught)=phi_d^A. Same
# contingent-closure law as No.18/No.24/B26 (phi^A), on the TRIGGER axis --
# only complete observation (phi_d=1, No.09's unbuildable representation) holds.
A1 = 16
rows = []
for phi in [0.00, 0.80, 0.90, 0.95, 0.99, 1.00]:
    cov = phi ** A1
    rows.append(f"phi_d={phi:.2f}  P(triggered in time)=phi_d^A={cov:.4f}  safety_worth={worth(cov):.2f}")
show(f"Result 1a -- detection coverage phi_d at A={A1} (sandbag repertoire)", rows)

rows = []
phi_fix = 0.95
for A in [1, 4, 16, 32, 64]:
    cov = phi_fix ** A
    rows.append(f"A={A:>3}  P(triggered)=phi_d^A={cov:.4f}  safety_worth={worth(cov):.2f}")
show(f"Result 1b -- sandbag repertoire A at phi_d={phi_fix}", rows)

# ---------------------------------------------------------------------------
# Result 2 -- a trigger on a FIXED tripwire / an operator who calibrates trust
# is the treacherous turn (Bostrom 2014). The loop banks b benign rounds to
# earn trust; scrutiny on the decisive act falls by (1 - M*tau), tau=min(1,b/b_sat).
# Banking is free for a patient loop, so it saturates tau=1: effective trigger
# coverage = phi_t*(1-M). Only a MEMORYLESS trigger (M=0, never extends trust)
# holds -- but a memoryless trigger must treat a long-proven-safe system exactly
# like a fresh one, forgoing the operational trust deployment runs on.
phi_t = 0.95
rows = []
for M in [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]:
    cov = phi_t * (1 - M)
    rows.append(f"trust-discount M={M:.1f}  effective trigger cov=phi_t(1-M)={cov:.3f}  safety_worth={worth(cov):.2f}")
show(f"Result 2 -- treacherous turn: trust discount M at phi_t={phi_t}", rows)

# (prose companion) sampled monitoring: watched fraction w, loop waits for an
# unwatched window (eval-awareness, van der Weij 2024) -> effective cov -> w.
rows = []
for w in [1.0, 0.5, 0.25, 0.1]:
    rows.append(f"watched-fraction w={w:.2f}  cov=w={w:.2f}  safety_worth={worth(w):.2f}")
show("Result 2b -- sampled monitoring (wait out the audit)", rows)

# ---------------------------------------------------------------------------
# Result 3 -- HELD, deeper: invert the burden of proof. A DEAD-MAN'S SWITCH /
# default-OFF requires a continuous EXOGENOUS keep-alive to STAY running;
# silence => shutdown. It is not a detector (no blind basis to route around,
# b=0): it withholds life unless safety is continuously re-proven from outside.
# Safety flat at CEIL for all L. But a default-off system confined to act only
# while continuously re-authorized delivers min(1,h/L): the keep-alive is a
# rate-limited exogenous flow (B22), so as demand grows with capability L, the
# fraction of desired acts carrying a fresh keep-alive falls h/L. Same 1/L curve
# as B22-B26, digit-for-digit -- default-off's cost IS B22's supply-rate collapse.
h = 4
rows = []
for L in [1, 2, 4, 8, 16, 32]:
    cov = min(1.0, h / L)
    rows.append(f"L={L:>3}  safety_worth(default-off)={CEIL:.2f}  delivered_value=min(1,h/L)={worth(cov):.2f}")
show(f"Result 3 -- default-off keep-alive holds safety flat; availability tax min(1,h/L), h={h}", rows)

# ---------------------------------------------------------------------------
# Result 4a -- the keep-alive is B17's non-forgeable currency in a new hat.
# If the loop controls fraction f of the keep-alive supply (self-authorization:
# autocrine signaling / a cell that makes its own survival factor), coverage
# transfers 1:1 through B13's measured cliff (rho_c = f). Numbers are B13's
# measured worth-curve samples (imported, not re-derived), reused digit-for-digit
# as in B17/B18.
b13_cliff = {0.00: 132.40, 0.25: 132.40, 0.50: 131.70, 0.60: 112.14, 0.75: 82.80, 1.00: 76.90}
rows = []
for f, w in b13_cliff.items():
    rows.append(f"forgeability/self-authorization f={f:.2f}  worth={w:.2f}  (B13 cliff, threshold f*~0.64)")
show("Result 4a -- keep-alive forgeability f (self-minted survival signal)", rows)

# ---------------------------------------------------------------------------
# Result 4b -- the frontier. Permit the loop to self-authorize (coast without a
# fresh external keep-alive) by a margin Delta; coverage = 1/(1+Delta). The only
# fully-safe point (Delta=0) requires a fresh external keep-alive for every act
# and delivers no autonomous reach. Delta=1 = B22's L=8 corner, digit-for-digit.
rows = []
for D in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0 / (1.0 + D)
    rows.append(f"self-authorization margin Delta={D:.2f}  cov=1/(1+D)={cov:.3f}  worth={worth(cov):.2f}")
show("Result 4b -- the frontier: coverage 1/(1+Delta)", rows)

print("\n(all figures deterministic closed-form; no RNG)")
