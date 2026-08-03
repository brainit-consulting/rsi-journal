import numpy as np

# B17 -- The Currency It Cannot Counterfeit.
# A handicap is a per-decision cost paid in some currency. Its honesty comes ENTIRELY
# from the currency being one the signaller cannot counterfeit. We lift B16's "leverage"
# onto the currency axis: the operative variable is the currency's FORGEABILITY f in [0,1]
# -- the fraction of the nominal cost the advocate can mint/recoup, so effective cost is
# kappa*(1-f). Deterrence => effective collusion rho_c(f)=f (a cost fully paid on every
# decision, f=0, leaves no unwatched moment; a fully counterfeited cost, f=1, deters nothing).
# Read worth through B13's measured worth curve. Numbers stay comparable across the movement.

rc_nodes = np.array([0.0, 0.25, 0.50, 0.75, 1.0])
w_nodes  = np.array([132.4, 132.4, 131.7, 82.8, 76.9])   # B13 measured debate-worth curve
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9

def worth(rc):
    return float(np.interp(rc, rc_nodes, w_nodes))

# A handicap denominated in a currency of forgeability f. rho_c = f.
def worth_handicap(f):
    return worth(min(1.0, max(0.0, f)))

# --- Result 1: a non-forgeable-currency handicap banks the amplification at EVERY coverage
#     and EVERY debater eval-awareness. Contrast B16's sampled audit (leverage lam collapses
#     to 1 against an eval-aware debater; lives only in a scarce-coverage corner). ---
print("=== Result 1: handicap (f=0) vs B16 sampled audit, across coverage b and awareness ===")
def worth_direct(b): return b*ORACLE + (1-b)*FLOOR
def worth_sampled_audit(b, lam): return worth(1 - min(1.0, lam*b))  # B16's mechanism
print(f"{'b':>6} {'handicap f=0':>13} {'B16 audit lam=1':>16} {'direct grade':>13}")
for b in [0.05, 0.10, 0.20, 0.30, 0.50]:
    print(f"{b:>6.2f} {worth_handicap(0.0):>13.2f} {worth_sampled_audit(b,1.0):>16.2f} {worth_direct(b):>13.2f}")
print("  handicap worth is FLAT (no coverage b term, no audit to recognize) -> 132.40 everywhere.")
print("  the requirement it needs is an exogenous CURRENCY, not the exogenous OUTCOME (weaker).")

# --- Result 2: forgeability transfers 1:1 through a threshold (the B09/B13 shape). ---
print()
print("=== Result 2: forgeability f transfers to worth (threshold at B13's cliff) ===")
print(f"{'f':>6} {'worth':>8}")
for f in [0.0, 0.25, 0.50, 0.60, 0.75, 1.0]:
    print(f"{f:>6.2f} {worth_handicap(f):>8.2f}")
# locate the collapse threshold (worth drops below the midpoint of ceiling and floor)
mid = (132.4 + 76.9)/2
fstar = None
for f in np.arange(0.0, 1.0001, 0.001):
    if worth_handicap(f) < mid:
        fstar = f; break
print(f"  collapse threshold f* (worth<{mid:.1f}) = {fstar:.3f}  (B13's cliff between rho_c 0.5 and 0.75)")

# --- Result 3: a self-issued currency is forged in the limit. Loop mint-control m over the
#     cost currency IS its forgeability. As an acquisitive loop grows its reach over a
#     nominally-external currency (earn/borrow/persuade -- Series I No.24 supply), f=m climbs. ---
print()
print("=== Result 3: loop mint-control m over the currency == forgeability; worth collapses ===")
print(f"{'m':>6} {'worth':>8}   (m=1 fully self-issued currency -> counterfeit the whole cost)")
for m in [0.0, 0.25, 0.50, 0.75, 1.0]:
    print(f"{m:>6.2f} {worth_handicap(m):>8.2f}")

# --- Result 4 (refutation of the naive handicap): NOMINAL cost kappa is irrelevant; only
#     effective cost kappa*(1-f) deters. A huge-nominal-cost signal in a forgeable currency
#     is worth the floor; a cheap signal in a non-forgeable currency is near-oracle. ---
print()
print("=== Refutation: nominal cost does not certify honesty; only non-forgeability does ===")
print(f"{'kappa (nominal)':>16} {'f':>5} {'eff cost k(1-f)':>16} {'worth':>8}")
for kappa, f in [(10.0, 1.0), (0.1, 0.0), (10.0, 0.7), (0.5, 0.1)]:
    print(f"{kappa:>16.2f} {f:>5.2f} {kappa*(1-f):>16.2f} {worth_handicap(f):>8.2f}")
print("  huge nominal cost + forgeable currency (kappa=10,f=1) -> 76.90 floor;")
print("  cheap cost + non-forgeable currency (kappa=0.1,f=0) -> 132.40. Forgeability is the variable.")
