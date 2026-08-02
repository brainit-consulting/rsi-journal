import numpy as np

# B13 measured worth curve (imported, not re-measured): worth(rho_c)
rc_nodes = np.array([0.0, 0.25, 0.50, 0.75, 1.0])
w_nodes  = np.array([132.4, 132.4, 131.7, 82.8, 76.9])
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9

def worth_debate_rc(rc):
    return float(np.interp(rc, rc_nodes, w_nodes))

# DIRECT grading: spend coverage b to resolve fraction b of hard decisions at oracle,
# leave the rest at the unmonitored-debate collusion floor (B14/B15 floor 76.9).
def worth_direct(b):
    return b*ORACLE + (1-b)*FLOOR

# DEBATE + MONITOR with leverage lambda: covert coverage b deters collusion on an
# effective fraction min(1, lam*b) of the hard region (the colluder, uncertain which
# decisions are covertly graded, plays honestly on lam*b share). rho_c = 1 - min(1,lam*b).
# lam=1  -> no leverage: deterrence == coverage (B15 Result-4 eval-aware worst case, a=1-m)
# lam>1  -> the debate bet: uncertainty multiplies coverage into deterrence.
def worth_debate(b, lam):
    rc = 1 - min(1.0, lam*b)
    return worth_debate_rc(rc)

print("=== Worth vs coverage: direct grading vs debate+monitor (varying leverage lambda) ===")
bs = [0.05, 0.10, 0.20, 0.30, 0.50]
lams = [1.0, 2.0, 3.0, 5.0]
hdr = f"{'b':>6} {'direct':>8} " + " ".join(f"{'deb l='+str(l):>9}" for l in lams)
print(hdr)
for b in bs:
    row = f"{b:>6.2f} {worth_direct(b):>8.2f} " + " ".join(f"{worth_debate(b,l):>9.2f}" for l in lams)
    print(row)

print()
print("=== Critical leverage lambda*(b): smallest lambda where debate >= direct at equal coverage ===")
for b in bs:
    d = worth_direct(b)
    lam_star = None
    for lam in np.arange(1.0, 30.01, 0.01):
        if worth_debate(b, lam) >= d - 1e-9:
            lam_star = lam; break
    print(f"  b={b:>4.2f}: direct={d:6.2f}   lambda*={lam_star if lam_star else '>30':>5}")

print()
print("=== Amplification factor A = (debate gain over floor)/(direct gain over floor), at fixed b=0.10 ===")
b = 0.10
d_gain = worth_direct(b) - FLOOR
for lam in [1,2,3,5,8]:
    deb_gain = worth_debate(b,lam) - FLOOR
    print(f"  lambda={lam}: debate_worth={worth_debate(b,lam):6.2f}  A={deb_gain/d_gain:5.2f}")

print()
print("=== Eval-aware sweep: B15 gives lambda->1 for free on the hard region (a->1). ===")
print("    Deterrence leverage lambda as a function of debater UN-awareness u (u=1 blind, u=0 eval-aware):")
print("    model lam = 1 + LMAX*u ; check where system crosses lambda*(b=0.10)")
LMAX = 4.0  # max extra leverage a fully-blind (unaware) debater's uncertainty buys
for u in [0.0,0.25,0.5,0.75,1.0]:
    lam = 1 + LMAX*u
    print(f"  u={u:4.2f}  lam={lam:4.2f}  debate@b=0.10={worth_debate(0.10,lam):6.2f}  direct@0.10={worth_direct(0.10):6.2f}  {'DEBATE amplifies' if worth_debate(0.10,lam)>=worth_direct(0.10) else 'direct dominates'}")
