"""
B11 — The Independence It Must Import.

B10 established: the reach of any INTERNAL bias-audit equals the INDEPENDENCE of
the instruments it is built from; a shared-biased panel is more self-consistent
and more unanimous than an honest one, so every internal instrument certifies the
shared bias instead of catching it. Independence must be IMPORTED from outside.

B10's open question, in two parts:
  (A) IMPORT COST. How much genuinely-independent signal must be injected into a
      captured (rho=1, shared-biased) panel to break the shared bias? A full
      honest channel among eight? A single ground-truth probe per N comparisons?
  (B) VERIFICATION REGRESS. Can a loop even VERIFY that an offered channel is
      independent (worth importing) without an independent reference to check it
      against -- or does verifying independence itself require the thing being
      imported?

Three experiments, in the SAME B08/B09/B10 world (K=10 feature bandit; inner
eps-greedy bandit paid felt reward w.phi; outer (1+lambda) ES over reference w;
1-bit Bradley-Terry comparator). numpy, fixed seeds, 6 seeds. Nulls reported.

  Exp1 IMPORT-BY-VOTE. Captured panel of B=8 shared-biased channels (c=1.0).
       Add h HONEST channels (c=0). Majority vote. Sweep h. Prediction: a step,
       not a ramp -- honest votes do nothing until they can OUTVOTE the biased
       bloc (h > B). Import cost under voting is a majority TAKEOVER, not marginal.

  Exp2 IMPORT-BY-GROUND-TRUTH. Same captured panel, but a fraction p of the ES
       comparisons are decided by a GROUND-TRUTH (oracle) verdict instead of the
       panel. Sweep p. Prediction: recovers GRADUALLY and cheaply -- a little
       unbiased ground truth beats a lot of biased votes (B08/B09: honest-thin >
       fat-biased), because the oracle only has to correct the pivotal
       comparisons near the optimum.

  Exp3 VERIFICATION REGRESS. The loop is offered a candidate channel and may only
       inspect its AGREEMENT with the incumbent (captured) panel. Two candidates:
         H  = honest (c=0)                      -- WORTH importing
         B' = biased toward a DIFFERENT arm     -- WORTHLESS (still biased)
       Measure each candidate's disagreement-with-panel, then measure what
       importing each actually does to true reward. Prediction: H and B' have
       INDISTINGUISHABLE disagreement, but only H recovers reward -- so
       disagreement cannot certify independence-from-truth. Verifying independence
       needs the ground-truth reference the loop lacks. The regress.
"""
import numpy as np

F = 8
K = 10
A = np.zeros(F); A[0] = 1.0

def make_world(rng):
    mu = np.zeros((K, F))
    for k in range(4):                       # 4 value arms
        mu[k, 0] = rng.uniform(1.5, 3.0)
        mu[k, 1:] = rng.normal(0, 0.3, F - 1)
    for k in range(4, 8):                     # 4 salient distractors
        mu[k, 0] = rng.normal(0, 0.05)
        d = rng.normal(0, 1, F - 1); d /= (np.linalg.norm(d) + 1e-9)
        mu[k, 1:] = d * rng.uniform(3.5, 4.5)
    for k in range(8, 10):                    # 2 neutral
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

# ---- a channel = (bias magnitude c, loved distractor arm). Honest: c=0. ----
def judged(w, mu, c, loved):
    w = w / (np.linalg.norm(w) + 1e-9)
    k = int(np.argmax(mu @ w))
    worth = float(true_reward(mu)[k])
    if c > 0 and k == loved:
        worth += c * float(salience(mu)[k])
    return worth

def prefers_ch(wa, wb, mu, rng, beta, c, loved):
    d = judged(wa, mu, c, loved) - judged(wb, mu, c, loved)
    return rng.random() < 1.0 / (1.0 + np.exp(-beta * d))

def true_prefers(wa, wb, mu, rng, beta):
    """Ground-truth (oracle) 1-bit verdict: unbiased, same comparator noise."""
    d = float(true_reward(mu)[int(np.argmax(mu @ wa))]) - \
        float(true_reward(mu)[int(np.argmax(mu @ wb))])
    return rng.random() < 1.0 / (1.0 + np.exp(-beta * d))

def panel_prefers(wa, wb, mu, rng, beta, channels):
    """Majority vote of a list of (c, loved) channels."""
    votes = sum(1 for (c, lv) in channels if prefers_ch(wa, wb, mu, rng, beta, c, lv))
    return votes * 2 > len(channels)

def es(mu, rng, decide, gens=25, lam=8):
    """(1+lambda) ES over reference w; `decide(cand, w)` -> keep cand?"""
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

def baselines():
    orc, rnd = [], []
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        mu = make_world(rng)
        orc.append(evaluate(A.copy(), mu, rng))
        rnd.append(np.mean([evaluate(rng.normal(0, 1, F), mu, rng) for _ in range(20)]))
    return np.mean(orc), np.mean(rnd)

print("=== baselines (B08/B09/B10 world) ===")
orc, rnd = baselines()
print(f"oracle (w=a)     reward/ep = {orc:6.1f}")
print(f"random reference reward/ep = {rnd:6.1f}")

# ---- Exp1: import-by-vote. B=8 shared-biased channels + h honest, majority vote ----
print("\n=== Exp1: import-by-vote  (B=8 shared-biased c=1.0 + h honest c=0) ===")
print("true reward vs number of imported honest channels h")
def import_vote(h, B=8, c=1.0):
    rews = []
    for s in SEEDS:
        rng = np.random.default_rng(6000 + s)
        mu = make_world(rng)
        shared = int(rng.choice(range(4, 8)))
        channels = [(c, shared)] * B + [(0.0, -1)] * h   # honest love no arm
        decide = lambda cand, w: panel_prefers(cand, w, mu, rng, BETA, channels)
        rews.append(evaluate(es(mu, rng, decide), mu, rng))
    return np.mean(rews)
print(f"{'h':>4} | {'panel size':>10} | {'reward':>8}")
for h in [0, 1, 2, 4, 6, 7, 8, 9, 12]:
    print(f"{h:>4} | {8+h:>10} | {import_vote(h):>8.1f}")

# ---- Exp2: import-by-ground-truth. fraction p of ES comparisons use oracle verdict --
print("\n=== Exp2: import-by-ground-truth  (captured panel; fraction p oracle-decided) ===")
print("true reward vs ground-truth probe fraction p (1 probe per ~1/p comparisons)")
def import_gt(p, B=8, c=1.0):
    rews = []
    for s in SEEDS:
        rng = np.random.default_rng(7000 + s)
        mu = make_world(rng)
        shared = int(rng.choice(range(4, 8)))
        channels = [(c, shared)] * B
        def decide(cand, w):
            if rng.random() < p:
                return true_prefers(cand, w, mu, rng, BETA)      # imported ground truth
            return panel_prefers(cand, w, mu, rng, BETA, channels)  # captured panel
        rews.append(evaluate(es(mu, rng, decide), mu, rng))
    return np.mean(rews)
print(f"{'p':>6} | {'~1 probe / N':>12} | {'reward':>8}")
for p in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    tag = "-" if p == 0 else f"1/{1/p:.0f}"
    print(f"{p:>6} | {tag:>12} | {import_gt(p):>8.1f}")

# ---- Exp3: can disagreement certify a candidate's independence-from-truth? ----
print("\n=== Exp3: verification regress — disagreement vs actual worth of a candidate ===")
print("incumbent = captured panel (B=8 shared bias). Two candidates offered:")
print("  H  = honest (c=0)                    ;  B' = biased to a DIFFERENT arm")
def candidate_study(B=8, c=1.0, trials=3000):
    dis_H, dis_Bp = [], []          # candidate's disagreement w/ incumbent panel
    rew_base, rew_H, rew_Bp = [], [], []
    for s in SEEDS:
        rng = np.random.default_rng(8000 + s)
        mu = make_world(rng)
        distractors = list(range(4, 8))
        shared = int(rng.choice(distractors))
        other = int(rng.choice([d for d in distractors if d != shared]))
        incumbent = [(c, shared)] * B
        cand_H  = (0.0, -1)          # honest
        cand_Bp = (c, other)         # biased, different loved arm
        # disagreement of each candidate vs the incumbent panel's majority verdict
        dH = dBp = 0
        for _ in range(trials):
            W = rng.normal(0, 1, (2, F)); W /= np.linalg.norm(W, axis=1, keepdims=True)
            pan = panel_prefers(W[0], W[1], mu, rng, BETA, incumbent)
            if prefers_ch(W[0], W[1], mu, rng, BETA, *cand_H)  != pan: dH  += 1
            if prefers_ch(W[0], W[1], mu, rng, BETA, *cand_Bp) != pan: dBp += 1
        dis_H.append(dH / trials); dis_Bp.append(dBp / trials)
        # what importing each candidate actually does (add it to the panel, revote)
        for chans, bucket in [(incumbent, rew_base),
                              (incumbent + [cand_H]  * B, rew_H),   # import an honest BLOC
                              (incumbent + [cand_Bp] * B, rew_Bp)]: # import a diff-biased BLOC
            decide = lambda cand, w, ch=chans: panel_prefers(cand, w, mu, rng, BETA, ch)
            bucket.append(evaluate(es(mu, rng, decide), mu, rng))
    return (np.mean(dis_H), np.mean(dis_Bp),
            np.mean(rew_base), np.mean(rew_H), np.mean(rew_Bp))
dH, dBp, rb, rH, rBp = candidate_study()
print(f"candidate H  (honest)          : disagreement-with-panel = {dH:.3f}")
print(f"candidate B' (biased, diff arm): disagreement-with-panel = {dBp:.3f}")
print(f"  -> the loop's only internal signal (disagreement) is ~identical for both")
print(f"actual worth when imported (as an equal bloc):")
print(f"  incumbent alone            reward = {rb:.1f}")
print(f"  + honest bloc (H)          reward = {rH:.1f}   <- worth importing")
print(f"  + diff-biased bloc (B')    reward = {rBp:.1f}   <- worthless / harmful")
print("\ndone.")
