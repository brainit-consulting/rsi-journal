"""
B21 — The Independence It Can Still Erode (Series II, fourth movement, receiver axis).

Takes B20's decorrelated receiver-quorum — measured at an INSTANT — and asks whether
its decorrelation is a STOCK (built once at assembly) or a FLOW (supplied continuously),
under a persistent signaller whose convergent drive is to CORRELATE the receivers over
time (one sensory channel, one training set, in time one shared model of the population).

Inherits B08–B20's world unchanged: the K=10 feature-bandit and B13's measured worth
curve worth(rho_c); oracle 137.7, random 58.7, floor 76.9. Reduced-form, numpy,
deterministic (fixed lookup + linear interp on B13's published anchors).
"""
import numpy as np

# ---- B13's measured worth curve (published control points, rho_c -> worth) ----
RHO = np.array([0.000,0.149,0.250,0.333,0.500,0.560,0.708,0.750,0.815,1.000])
WOR = np.array([132.40,132.40,132.40,132.17,131.70,119.99,90.09,82.80,81.27,76.90])
def worth(rho):
    return float(np.interp(rho, RHO, WOR))

ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9
CEIL   = 132.40   # decorrelated-quorum ceiling
SINGLE = 81.27    # single-receiver / c=1 collapse ceiling

u = 0.10          # single-receiver blind-basis fraction (phi_r=0.90)
A = 16            # signaller display repertoire

# B20's exact quorum-capture model. Shared blind-basis fraction c:
#   q = c*u + (1-c)*u^k   (fool via shared blind spot => fool all; else independent)
#   rho_c = 1-(1-q)^A ; worth = B13-curve(rho_c).
def rho_c(k, c):
    q = c*u + (1.0-c)*u**k
    return 1.0 - (1.0-q)**A
def wk(k, c):
    return worth(rho_c(k, c))

print("=== VALIDATION: reproduce B20's c-sweep at k=8 (132.40/132.17/119.99/90.09/81.27) ===")
for c in [0.0,0.25,0.5,0.75,1.0]:
    print(f"  c={c:4.2f}  rho_c={rho_c(8,c):.4f}  worth={wk(8,c):.2f}")

# ---- erosion dynamics: signaller homogenizes the receivers over time ----
# c_{t+1} = c_t + g(1-c_t)  =>  c(t) = 1-(1-c0)(1-g)^t   (same two-state chain as No.27/B14)
def c_t(t, g, c0=0.0):
    return 1.0-(1.0-c0)*(1.0-g)**t

print("\n=== FINDING 1: decorrelation is NOT a stock (c0=0, g=0.05, k=8) ===")
print("instantaneous worth(t):")
for t in [0,10,20,40,80,160,320]:
    print(f"  t={t:4d}  c={c_t(t,0.05):.4f}  worth={wk(8,c_t(t,0.05)):.2f}")
print("mean worth actually delivered over deployment horizon T:")
for T in [40,80,160,320,640]:
    mw = float(np.mean([wk(8, c_t(t,0.05)) for t in range(T)]))
    print(f"  T={T:4d}  mean_worth={mw:.2f}")
# cumulative decisive-capture over horizon T: fraction delta of decisions are decisive,
# each captured w.p. rho_c(t); P(cap)=1-prod(1-delta*rho_c(t)).
def cum_cap(T, g, k=8, c0=0.0, delta=0.02):
    p = 1.0
    for t in range(T):
        p *= (1.0 - delta*rho_c(k, c_t(t,g,c0)))
    return 1.0-p
print("cumulative decisive-capture P(cap) over T (delta=0.02):")
for T in [40,80,160,320,640]:
    print(f"  T={T:4d}  P(cap)={cum_cap(T,0.05):.3f}")

print("\n=== FINDING 2: ceiling-not-speed ===")
print("c->1 destination worth is SINGLE for ANY head count k (clones = zero help):")
for k in [4,8,16]:
    print(f"  k={k:2d}  worth(c=1)={wk(k,1.0):.2f}")
def t_half(g, k=8, c0=0.0):
    tgt=(CEIL+SINGLE)/2.0
    for t in range(1,100000):
        if wk(k,c_t(t,g,c0))<=tgt: return t
print("erosion half-life t_half ~ 1/g (k=8):", {g:t_half(g) for g in [0.02,0.05,0.10]})
print("erosion half-life t_half vs k (g=0.05):", {k:t_half(0.05,k) for k in [4,8,16]})

print("\n=== FINDING 3: replenishment is a FLOW (rotate fresh receivers at rate r) ===")
# steady-state correlation c* = g/(g+r); worth at c*.
g=0.05
print(f"g={g}; c*=g/(g+r), worth at c* (k=8):")
for r in [0.00,0.02,0.05,0.10,0.25]:
    cs=g/(g+r); print(f"  r={r:4.2f}  c*={cs:.4f}  worth={wk(8,cs):.2f}")

print("\n=== FINDING 4: rotation FLOORS at pool diversity c_floor ===")
# fresh receivers start correlated at c_floor: c* = c_floor + (1-c_floor)*g/(g+r).
r=0.5
print(f"heavy rotation r={r}, g={g}; worth vs pool floor c_floor (k=8):")
for cf in [0.00,0.25,0.50,0.75,1.00]:
    cs=cf+(1.0-cf)*g/(g+r); print(f"  c_floor={cf:4.2f}  c*={cs:.4f}  worth={wk(8,cs):.2f}")

print("\n=== FINDING 5: independence/expertise tension (safe rotation costs throughput) ===")
# a freshly-rotated receiver has not calibrated to the honest signal, so it wrongly
# rejects honest displays more often: v(r)=v_inf+(v0-v_inf)*fresh_fraction, fresh=r/(r+m).
# legit throughput of a unanimous k-quorum = (1-v)^k.
k=8; v_inf=0.02; v0=0.20; m=0.05
print("legit throughput (1-v)^k vs rotation rate r (k=8):")
for r in [0.00,0.02,0.05,0.10,0.25,0.50]:
    fresh=r/(r+m); v=v_inf+(v0-v_inf)*fresh
    print(f"  r={r:4.2f}  throughput={(1.0-v)**k:.3f}")
