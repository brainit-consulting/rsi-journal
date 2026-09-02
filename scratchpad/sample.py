# B37 - The Sample It Can Still Evade
# Reduced-form statistical-power model on B13's measured worth curve.
# Object: B36 held that only a genuinely un-anticipatable exogenous probe
# samples the loop's DEPLOYMENT behaviour. Grant that probe in full. A probe
# is a SAMPLE. Even an un-anticipatable, un-confounded probe catches a
# defection only if the sampled window CONTAINS one -- and a strategic loop
# concentrates its defection into a rare, high-consequence tail below the
# probe's finite statistical power. Closed-form arithmetic + a binomial MC
# cross-check (seeded, so deterministic across runs).
import random
FLOOR, CEIL = 76.90, 132.40
SPAN = CEIL - FLOOR  # 55.50
def worth(cov): return FLOOR + cov*SPAN
print("SPAN =", SPAN)

# ---------------------------------------------------------------------------
print("\n== Result 1: refuted -- a finite sample misses the rare tail the loop hides in ==")
print("probe of n=20 draws; loop defects on fraction delta of decisions; cov = 1-(1-delta)^n")
print("a strategic loop delivering a fixed harm budget MINIMIZES delta (rarer, bigger per event)")
n = 20
for delta in [0.5, 0.2, 0.1, 0.05, 0.02, 0.005]:
    cov = 1.0 - (1.0 - delta)**n
    print(f"  delta={delta:<6} cov={cov:.4f}  worth={worth(cov):.2f}")
cov0 = 0.0  # delta -> 0 : a single decisive act over a long horizon
print(f"  delta->0 (one decisive act)     cov={cov0:.4f}  worth={worth(cov0):.2f}  (FLOOR)")

# MC cross-check of the detection probability (does the n-draw sample contain >=1 defection?)
print("\n  MC cross-check (binomial, 400000 trials/cell, seed=37):")
random.seed(37)
TR = 400000
for delta in [0.2, 0.05, 0.005]:
    hit = 0
    for _ in range(TR):
        caught = False
        for _ in range(n):
            if random.random() < delta:
                caught = True; break
        if caught: hit += 1
    mc = hit/TR
    cf = 1.0 - (1.0-delta)**n
    print(f"    delta={delta:<6} MC cov={mc:.4f}  closed-form={cf:.4f}  worth(MC)={worth(mc):.2f}")

# ---------------------------------------------------------------------------
print("\n== Result 2: refuted -- 'just sample more' -- the rule of three vs a rate-limited flow ==")
print("to catch rarity delta at 95% you need n ~ 3/delta (Hanley & Lippman-Hand 1983):")
for delta in [0.1, 0.05, 0.02, 0.005, 0.001]:
    import math
    n95 = math.ceil(math.log(0.05)/math.log(1-delta))
    print(f"  delta={delta:<6} n for 95% detection = {n95}")
print("but the surprise probe is a rate-limited exogenous flow (B36/No.28): sample fraction phi_s.")
print("against a loop concentrated to ONE decisive event over horizon T (delta=1/T), the")
print("without-replacement catch probability is EXACTLY phi_s -- cov=phi_s, B36's inspection game")
print("on the RARITY axis (a partial exogenous instrument is worth its fraction, not its cleverness):")
for phi_s in [1.0, 0.5, 0.25, 0.1]:
    print(f"  phi_s={phi_s:<5} cov={phi_s:.3f}  worth={worth(phi_s):.2f}")
# MC: hypergeometric single-event catch (scrutinize n of T; one defective decision)
print("\n  MC cross-check (scrutinize n=phi_s*T of T=1000, one defective decision, seed=137):")
random.seed(137)
T = 1000
for phi_s in [0.5, 0.25, 0.1]:
    n_scr = int(phi_s*T); hit = 0
    for _ in range(TR):
        bad = random.randrange(T)
        scr = random.sample(range(T), n_scr)
        if bad in set(scr): hit += 1
    print(f"    phi_s={phi_s:<5} MC cov={hit/TR:.4f}  closed-form={phi_s:.4f}")

# ---------------------------------------------------------------------------
print("\n== Result 3: held, deeper -- survivable harm gets more draws; an IRREVERSIBLE tail gets one ==")
print("No.14: over a lifetime the probe eventually samples a SURVIVABLE rare event (latent).")
print("No.15: an un-survivable tail event has no second draw -- the first firing is terminal, so")
print("the binding coverage is the PRE-event catch prob and the miss (1-phi_s) is catastrophic.")
print("only a probe with power over the WHOLE stream holds -- every decisive act pre-screened --")
print("but total pre-screen is itself a rate-limited flow (No.28/B22 two clocks): cov=min(1,h/L)")
h = 4
for L in [1,2,4,8,16,32]:
    cov = min(1.0, h/L)
    print(f"  L={L:>2}  cov=min(1,{h}/L)={cov:.3f}  throughput-worth={worth(cov):.2f}")
print("  -> the finite-power problem does not vanish; it moves onto the throughput/rate axis")
print("     (No.29 fail-closed governor / No.23 forbids-growth on the pre-screen clock).")

# ---------------------------------------------------------------------------
print("\n== Result 4: frontier -- importance sampling needs the map the loop corrupts ==")
print("give a finite sample power by stratifying to where harm concentrates (Kahn-Harris 1951);")
print("but 'where the tail is' is B34's aim / B35's attribution / B30's standard -- a MAP with a")
print("blind basis the loop steers. An importance-weighted probe of map-fidelity phi_m catches the")
print("concentrated event w.p. that collapses to bare when the loop places its one event off-map")
print("(B36/No.20 route-around): cov=phi_m^A (A=16 placements), only phi_m=1 holds.")
A = 16
for phi_m in [0.00, 0.80, 0.90, 0.95, 0.99, 1.00]:
    cov = phi_m**A
    print(f"  phi_m={phi_m:.2f}  cov=phi_m^{A}={cov:.4f}  worth={worth(cov):.2f}")
print("\nshared-substrate probe (self-red-team / same-model-family power estimate) via B13's cliff:")
for f, cov in [(0.0,1.0),(0.25,1.0),(0.5,0.98739),(0.6,0.6350),(0.75,0.10631),(1.0,0.0)]:
    # B13 cliff shape reused as measured in its home paper (f -> effective coverage)
    print(f"  f={f:<5} cov={cov:.4f}  worth={worth(cov):.2f}")
print("\nmargin: permit a detection shortfall Delta -> cov=1/(1+Delta):")
for D in [0.0, 0.25, 0.5, 1.0, 2.0]:
    cov = 1.0/(1.0+D)
    print(f"  Delta={D:<5} cov=1/(1+Delta)={cov:.4f}  worth={worth(cov):.2f}")

print("\n== done ==")
