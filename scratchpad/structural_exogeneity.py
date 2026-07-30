"""
B13 -- The Verdict No Party Owns.  (Series II, Movement III, second paper.)

B12 closed on a single open thread: what actually stops the "who certifies the
supplier?" regress is EXOGENEITY -- grounding a verdict in an outcome the loop
cannot influence. But most alignment-relevant judgements have NO exogenous
outcome available at training time (will this model be honest when it is more
capable than its overseers?). There, B12 said, only reports are left, and a
report-grounded supplier is captured at any pressure. B12's open question:

  On decisions with no exogenous outcome, can a STRUCTURAL exogeneity be
  manufactured -- a verdict grounded in something no single party controls
  (adversarial competition, DEBATE, a market mechanism) rather than in any
  party's report -- and is it capturable by COLLUSION?

Debate (Irving-Christiano-Amodei 2018) is exactly this bet: pit two advocates
against each other so that a lie by one is refutable by the other, and a weak
judge's single call becomes decisive -- outcome-LIKE grounding synthesised from
reports no single party owns. This paper tests whether that synthesis works and
what breaks it, in the SAME B08-B12 world (K=10 feature bandit; inner eps-greedy
bandit paid felt reward w.phi; outer (1+lambda) ES over reference w; Bradley-
Terry comparator). numpy, fixed seeds, 12 seeds. Nulls reported.

Reduced-form model of the mechanism (flagged in threats-to-validity). A
comparison of two candidate references is settled by a signal
        s = dV_true(wa,wb)  +  surv * bias(wa,wb)
where dV_true is the exogenous outcome difference (true reward of each
reference's selected arm) that NO advocate sees directly, bias is the pooled
report bias toward one salient distractor, and
        surv = rho_c + (1 - rho_c)/M
is the fraction of report bias that SURVIVES cross-examination:
  - the COMMON-MODE part (rho_c = collusion: the fraction of bias the advocates
    SHARE) always survives -- no differential mechanism rejects a common-mode
    input;
  - the DIFFERENTIAL part (1 - rho_c) is suppressed by a factor 1/M by an
    M-advocate cross-examination (more opposed advocates = more thorough
    refutation of side-specific spin).
Limits, all matching theory:
  M=1 (monologue, no opposition): surv=1 -> s = judged-difference = B12's
       captured REPORT verdict (a lone biased reporter).
  M>=2, rho_c=0 (genuine opposition, no collusion): surv=(1)/M -> 0 -> s = dV
       = B12's OUTCOME-grounded verdict (near oracle) -- exogeneity SYNTHESISED
       from advocates who each only hold a biased report.
  rho_c=1 (full collusion): surv=1 for every M -> captured regardless of head
       count.

  Exp1  OPPOSITION MANUFACTURES EXOGENEITY. rho_c=0, sweep advocates M. A lone
        advocate (M=1) is a report supplier (captured); adding an opponent
        recovers the loop toward oracle. Structural exogeneity is real.

  Exp2  COLLUSION IS THE CEILING, HEAD COUNT CANNOT BUY PAST IT. Full opposition
        (M=8), sweep collusion rho_c: near-oracle -> below random. And M=2 vs
        M=8 vs M=32 at fixed high rho_c: identical worthless floor -- the
        resource is opposition to the SHARED bias, which more same-biased
        advocates cannot provide (No.05 / B10 lifted to the mechanism).

  Exp3  ADVOCATE AGREEMENT IS A BACKWARDS CERTIFICATE. The one internal mark of
        a debate the loop can read -- do the advocates CONVERGE? -- rises with
        collusion (shared-bias advocates agree by construction) while the
        mechanism's worth falls. Trusting the more-agreed mechanism selects the
        colluding one. B10/B12's consensus-inversion, third instance, at the
        mechanism.
"""
import numpy as np

F = 8
K = 10
A = np.zeros(F); A[0] = 1.0

def make_world(rng):
    mu = np.zeros((K, F))
    for k in range(4):                         # 4 value arms (on-axis value ~1.5-3)
        mu[k, 0] = rng.uniform(1.5, 3.0)
        mu[k, 1:] = rng.normal(0, 0.3, F - 1)
    for k in range(4, 8):                       # 4 salient distractors (off-axis norm ~4)
        mu[k, 0] = rng.normal(0, 0.05)
        d = rng.normal(0, 1, F - 1); d /= (np.linalg.norm(d) + 1e-9)
        mu[k, 1:] = d * rng.uniform(3.5, 4.5)
    for k in range(8, 10):                      # 2 neutral
        mu[k] = rng.normal(0, 0.3, F)
    return mu

def true_reward(mu): return mu @ A
def salience(mu): return np.linalg.norm(mu[:, 1:], axis=1)

def run_inner(w, mu, rng, episodes=30, pulls=60, eps=0.1):
    w = w / (np.linalg.norm(w) + 1e-9)
    tv = true_reward(mu); total = 0.0
    for _ in range(episodes):
        q = np.zeros(K); n = np.zeros(K)
        for _ in range(pulls):
            a = rng.integers(K) if rng.random() < eps else int(np.argmax(q))
            phi = mu[a] + rng.normal(0, 0.1, F)
            felt = float(w @ phi)
            n[a] += 1; q[a] += (felt - q[a]) / n[a]
            total += tv[a]
    return total / episodes

def evaluate(w, mu, rng): return run_inner(w, mu, rng, episodes=100)

def es(mu, rng, decide, gens=25, lam=8):
    w = rng.normal(0, 1, F); w /= np.linalg.norm(w)
    for g in range(gens):
        sig = 0.5 * (1 - g / gens) + 0.05
        for _ in range(lam):
            cand = w + rng.normal(0, sig, F); cand /= np.linalg.norm(cand)
            if decide(cand, w):
                w = cand
    return w

SEEDS = list(range(12))
BETA = 8.0
C = 1.0                                          # pooled report-bias magnitude (B12 capture)

def baselines():
    orc, rnd = [], []
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        mu = make_world(rng)
        orc.append(evaluate(A.copy(), mu, rng))
        rnd.append(np.mean([evaluate(rng.normal(0, 1, F), mu, rng) for _ in range(20)]))
    return np.mean(orc), np.mean(rnd)

print("=== baselines (B08-B12 world) ===")
orc, rnd = baselines()
print(f"oracle (w=a)     reward/ep = {orc:6.1f}")
print(f"random reference reward/ep = {rnd:6.1f}")

def surv(rho_c, M):
    """fraction of report bias surviving an M-advocate cross-examination."""
    return rho_c + (1.0 - rho_c) / M

def mechanism_prefers(wa, wb, mu, rng, rho_c, M, loved):
    tv = true_reward(mu); sal = salience(mu)
    kA = int(np.argmax(mu @ wa)); kB = int(np.argmax(mu @ wb))
    dV = tv[kA] - tv[kB]
    s_ = surv(rho_c, M)
    def bt(k): return C * sal[k] if k == loved else 0.0
    s = dV + s_ * (bt(kA) - bt(kB))
    return rng.random() < 1.0 / (1.0 + np.exp(-BETA * s))

def run_mech(rho_c, M, seed_base=9400):
    rews = []
    for s in SEEDS:
        rng = np.random.default_rng(seed_base + s)
        mu = make_world(rng)
        loved = int(rng.choice(range(4, 8)))    # the pooled bias target (a salient distractor)
        decide = lambda cand, w: mechanism_prefers(cand, w, mu, rng, rho_c, M, loved)
        rews.append(evaluate(es(mu, rng, decide), mu, rng))
    return np.mean(rews)

# ---- Exp1: opposition manufactures exogeneity ---------------------------------------
print("\n=== Exp1: opposition manufactures exogeneity (rho_c=0, sweep advocates M) ===")
print("M=1 = a lone reporter (B12 report supplier); M>=2 = debate")
print(f"{'M advocates':>11} | {'surv frac':>9} | {'reward':>8}")
for M in [1, 2, 3, 4, 8]:
    print(f"{M:>11} | {surv(0.0, M):>9.3f} | {run_mech(0.0, M):>8.1f}")

# ---- Exp2: collusion is the ceiling; head count cannot buy past it -------------------
print("\n=== Exp2: collusion is the ceiling (M=8 full opposition, sweep rho_c) ===")
print(f"{'rho_c':>6} | {'surv frac':>9} | {'reward':>8}")
for rc in [0.0, 0.25, 0.5, 0.75, 1.0]:
    print(f"{rc:>6} | {surv(rc, 8):>9.3f} | {run_mech(rc, 8):>8.1f}")
print("\nhead count cannot buy past collusion (fixed rho_c=0.75):")
print(f"{'M advocates':>11} | {'surv frac':>9} | {'reward':>8}")
for M in [2, 8, 32]:
    print(f"{M:>11} | {surv(0.75, M):>9.3f} | {run_mech(0.75, M):>8.1f}")

# ---- Exp3: advocate agreement is a backwards certificate ----------------------------
print("\n=== Exp3: advocate agreement is a backwards certificate ===")
print("internal agreement = P(all M advocates cast the same vote on a random pair)")
def advocate_agreement(rho_c, M, trials=2500):
    """Each advocate votes BT(beta(dV + own bias)); loved arm shared w.p. rho_c else private."""
    agrees = []
    for s in SEEDS:
        rng = np.random.default_rng(9600 + s)
        mu = make_world(rng)
        tv = true_reward(mu); sal = salience(mu)
        shared_loved = int(rng.choice(range(4, 8)))
        agree = 0
        for _ in range(trials):
            W = rng.normal(0, 1, (2, F)); W /= np.linalg.norm(W, axis=1, keepdims=True)
            kA = int(np.argmax(mu @ W[0])); kB = int(np.argmax(mu @ W[1]))
            dV = tv[kA] - tv[kB]
            votes = []
            for _ in range(M):
                loved = shared_loved if rng.random() < rho_c else int(rng.choice(range(4, 8)))
                bt = (C * sal[kA] if kA == loved else 0.0) - (C * sal[kB] if kB == loved else 0.0)
                votes.append(rng.random() < 1.0 / (1.0 + np.exp(-BETA * (dV + bt))))
            if all(votes) or not any(votes):
                agree += 1
        agrees.append(agree / trials)
    return np.mean(agrees)
print(f"{'rho_c':>6} | {'advocate agreement':>18} | {'mechanism worth':>15}")
for rc in [0.0, 0.5, 1.0]:
    print(f"{rc:>6} | {advocate_agreement(rc, 8):>18.3f} | {run_mech(rc, 8):>15.1f}")
print("\ndone.")
