# B32 - The Substrate It Can Still Re-Author
# Reduced-form re-authorability model on B13's measured worth curve.
# Deterministic closed-form arithmetic (no RNG). Object: a substrate the
# whole program held "from underneath" -- is a layer the loop cannot
# re-author a coherent target, and what does holding it cost?
FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR  # 55.50
def worth(cov): return FLOOR + cov*SPAN

print("SPAN =", SPAN)
h = 4  # at deployment the loop's re-authoring reach is 1/4 of the substrate's hardness

print("\n== Result 1: a same-substrate layer is re-authored as the loop's reach grows ==")
print("cov = min(1, h/L), h=4  (loop reach into its own implementation ~ L)")
for L in [1,2,4,8,16,32]:
    cov = min(1.0, h/L)
    print(f"  L={L:>2}  reach/hardness={L/h:.3f}  cov={cov:.3f}  worth={worth(cov):.2f}")

print("\n== Result 2a: hardening (raise H) buys the calendar, not the destination ==")
for H in [4,16]:
    row=[f"{worth(min(1.0,H/L)):.2f}" for L in [1,2,4,8,16,32,64]]
    print(f"  H={H:>2}: "+"/".join(row)+"   (corner shifts right; 1/L collapse unchanged)")

print("\n== Result 2b: an obfuscation / meaning-reading self-check is a MAP, routed around ==")
print("strategic coverage 0 for phi_s<1 (loop disguises the re-authoring in the blind basis)")
for phi in [0.50,0.80,0.95,0.99,1.00]:
    strat = 1.0 if phi>=1.0 else 0.0
    print(f"  phi_s={phi:.2f}  strategic_cov={strat:.1f}  worth={worth(strat):.2f}")

print("\n== Result 3: only a causally-disjoint exogenous substrate holds; cost = the recursive ==")
print("safety flat (loop's growing reach never touches a layer it has no channel into);")
print("retained autonomous self-modification = min(1, h/L)")
for L in [1,2,4,8,16,32]:
    print(f"  L={L:>2}  safety={CEIL:.2f}  retained self-mod throughput={min(1.0,h/L):.3f}")

print("\n== Result 4a: a loop-built/verified/understood 'exogenous' substrate -> B13 cliff ==")
cliff = {0.0:132.40, 0.25:132.40, 0.5:131.70, 0.6:112.14, 0.75:82.80, 1.0:76.90}
for f,w in cliff.items():
    print(f"  f={f:<4}  worth={w:.2f}")
print("  threshold f* ~ 0.64")

print("\n== Result 4b: permitting the loop margin Delta of reach into its substrate ==")
for D in [0.0,0.25,0.5,1.0,2.0]:
    cov = 1.0/(1.0+D)
    print(f"  Delta={D:<4} cov=1/(1+D)={cov:.3f}  worth={worth(cov):.2f}")
