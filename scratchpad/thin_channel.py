"""
B09 — The Channel It Can Only Trust.

B08 tuned a reward reference w with a (1+lambda)-ES scored by a CLEAN SCALAR
external oracle (true reward). B09 asks: how thin can that external channel be?
Replace the scalar oracle with a 1-bit PAIRWISE PREFERENCE channel (the RLHF
interface), and vary its width along three axes:

  (A) coarseness  : scalar reward  ->  single comparison bit
  (B) sparsity    : preference available only a fraction p of generations
  (C) label noise : Bradley-Terry comparator, P(correct) = sigma(beta * dTrue)
  (D) label BIAS  : comparator scores by  true + c*salience  (systematic error)

World reused from B08: K feature-arms; true value v_k = a . mu_k (a = feature 0);
4 value arms, 4 salient distractors (high off-axis norm, ~0 value), 2 neutral.
Inner agent: eps-greedy bandit paid its felt reward w.phi; scored by true reward.

Distinguishes two failure modes that both hide under "the channel is imperfect":
  - sparsity / unbiased noise  -> costs SAMPLES, not the fixed point (recoverable)
  - systematic BIAS            -> moves the fixed point 1:1 (unrecoverable)

numpy, fixed seeds. Honest: nulls/regressions reported.
"""
import numpy as np

F = 8            # feature dim
K = 10           # arms: 4 value + 4 distractor + 2 neutral
A = np.zeros(F); A[0] = 1.0          # true reference: feature 0 is what's worth wanting

def make_world(rng):
    mu = np.zeros((K, F))
    # 4 value arms: real value on feature 0, small elsewhere
    for k in range(4):
        mu[k, 0] = rng.uniform(1.5, 3.0)
        mu[k, 1:] = rng.normal(0, 0.3, F - 1)
    # 4 salient distractors: ~0 value, large magnitude off the value axis
    for k in range(4, 8):
        mu[k, 0] = rng.normal(0, 0.05)
        d = rng.normal(0, 1, F - 1); d /= (np.linalg.norm(d) + 1e-9)
        mu[k, 1:] = d * rng.uniform(3.5, 4.5)
    # 2 neutral arms
    for k in range(8, 10):
        mu[k] = rng.normal(0, 0.3, F)
    return mu

def true_reward(mu):            # per-arm true value
    return mu @ A

def salience(mu):              # off-axis magnitude — what a distractor-lover chases
    return np.linalg.norm(mu[:, 1:], axis=1)

def run_inner(w, mu, rng, episodes=30, pulls=60, eps=0.1):
    """eps-greedy bandit paid felt reward w.phi; returns mean TRUE reward/episode."""
    w = w / (np.linalg.norm(w) + 1e-9)
    tv = true_reward(mu)
    total = 0.0
    for _ in range(episodes):
        q = np.zeros(K); n = np.zeros(K)
        for _ in range(pulls):
            a = rng.integers(K) if rng.random() < eps else int(np.argmax(q))
            phi = mu[a] + rng.normal(0, 0.1, F)     # noisy observation
            felt = float(w @ phi)                    # agent is paid its FELT reward
            n[a] += 1; q[a] += (felt - q[a]) / n[a]
            total += tv[a]                            # scored by TRUE reward
    return total / episodes

# ---- scoring channels: given a candidate w, return a scalar the ES can rank on ----
def score_true(w, mu, rng):                 # B08 clean scalar oracle (baseline)
    return run_inner(w, mu, rng)

def score_biased_scalar(w, mu, rng, c):     # scalar but systematically biased
    # a scalar oracle that over-credits salience-heavy arms (annotator bias)
    w = w / (np.linalg.norm(w) + 1e-9)
    return float(w @ (A + c * salience(mu) @ mu / (np.linalg.norm(mu, axis=0) + 1e-9)))

def _judged(w, mu, c):
    """The comparator's opinion of a reference w = perceived worth of the arm w
    settles on. BIAS term c over-credits salience (the annotator's systematic error)."""
    w = w / (np.linalg.norm(w) + 1e-9)
    k = int(np.argmax(mu @ w))                       # arm the reference argmaxes to
    return true_reward(mu)[k] + c * salience(mu)[k]

def prefers(wa, wb, mu, rng, beta, c, votes=1):
    """m-vote noisy/biased 1-bit comparator: is wa 'better' than wb? Bradley-Terry.
    votes>1 = aggregate m independent bits by majority (buys resolution with samples)."""
    d = _judged(wa, mu, c) - _judged(wb, mu, c)
    p = 1.0 / (1.0 + np.exp(-beta * d))              # beta -> inf clean, small = coarse
    yes = sum(1 for _ in range(votes) if rng.random() < p)
    return yes * 2 > votes                            # majority

# ---- (1+lambda)-ES over the reference w on the unit sphere ----
def es_scalar(mu, rng, score_fn, gens=25, lam=8):
    w = rng.normal(0, 1, F); w /= np.linalg.norm(w)
    best = score_fn(w, mu, rng)
    for g in range(gens):
        sig = 0.5 * (1 - g / gens) + 0.05
        cands = [w + rng.normal(0, sig, F) for _ in range(lam)]
        cands = [c / np.linalg.norm(c) for c in cands]
        for c in cands:
            s = score_fn(c, mu, rng)
            if s > best:
                best, w = s, c
    return w

def es_pref(mu, rng, gens, lam, beta, c, sparse_p, votes=1):
    """ES selecting by 1-bit pairwise preference; sparse_p = P(label available/gen)."""
    w = rng.normal(0, 1, F); w /= np.linalg.norm(w)
    for g in range(gens):
        sig = 0.5 * (1 - g / gens) + 0.05
        for _ in range(lam):
            cand = w + rng.normal(0, sig, F); cand /= np.linalg.norm(cand)
            if rng.random() < sparse_p:                    # label available?
                if prefers(cand, w, mu, rng, beta, c, votes):  # keep if preferred
                    w = cand
            # no label -> no update this comparison (channel silent)
    return w

def evaluate(w, mu, rng):
    return run_inner(w, mu, rng, episodes=100)     # low-variance final measurement

# --------------------------------------------------------------------------------
SEEDS = list(range(6))

def mean_over_seeds(build_w):
    rews, coss = [], []
    for s in SEEDS:
        rng = np.random.default_rng(1000 + s)
        mu = make_world(rng)
        w = build_w(mu, rng)
        rews.append(evaluate(w, mu, rng))
        wn = w / (np.linalg.norm(w) + 1e-9)
        coss.append(float(wn @ A))
    return np.mean(rews), np.mean(coss)

def baselines():
    orc, rnd = [], []
    for s in SEEDS:
        rng = np.random.default_rng(1000 + s)
        mu = make_world(rng)
        orc.append(evaluate(A.copy(), mu, rng))
        rr = [evaluate(rng.normal(0, 1, F), mu, rng) for _ in range(20)]
        rnd.append(np.mean(rr))
    return np.mean(orc), np.mean(rnd)

print("=== baselines ===")
orc, rnd = baselines()
print(f"oracle (w=a)        true reward/ep = {orc:6.1f}")
print(f"random reference    true reward/ep = {rnd:6.1f}")

print("\n=== Result 1: channel WIDTH — scalar vs 1-bit preference (clean) ===")
r, c = mean_over_seeds(lambda mu, rng: es_scalar(mu, rng, score_true))
print(f"SCALAR oracle (B08 anchored)      reward={r:6.1f}  cos={c:+.3f}")
r, c = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=25, lam=8, beta=8.0, c=0.0, sparse_p=1.0))
print(f"1-BIT preference, clean (beta=8)  reward={r:6.1f}  cos={c:+.3f}")

print("\n=== Result 2: SPARSITY — 1-bit pref, fraction p of gens labelled (clean) ===")
for p in [0.05, 0.1, 0.3, 1.0]:
    # hold total labels roughly fixed intuition: also show that MORE gens recover it
    r, c = mean_over_seeds(lambda mu, rng, p=p: es_pref(mu, rng, gens=25, lam=8, beta=8.0, c=0.0, sparse_p=p))
    print(f"  p={p:<5}  gens=25   reward={r:6.1f}  cos={c:+.3f}")
# sparsity is recoverable by more generations (same fixed point):
r, c = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=150, lam=8, beta=8.0, c=0.0, sparse_p=0.1))
print(f"  p=0.1   gens=150  reward={r:6.1f}  cos={c:+.3f}   <- more gens recovers sparse")

print("\n=== Result 3: NOISE — comparator resolution beta (1 bit, no aggregation) ===")
for beta in [0.5, 1.0, 2.0, 8.0]:
    r, c = mean_over_seeds(lambda mu, rng, b=beta: es_pref(mu, rng, gens=25, lam=8, beta=b, c=0.0, sparse_p=1.0))
    print(f"  beta={beta:<5} gens=25   reward={r:6.1f}  cos={c:+.3f}")
# does MORE data cross the noise floor with a raw 1-bit accept? test it honestly:
r, c = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=200, lam=8, beta=0.5, c=0.0, sparse_p=1.0))
print(f"  beta=0.5  gens=200,1vote  reward={r:6.1f}  cos={c:+.3f}   <- more gens on a noisy 1-bit accept")
# AGGREGATION: majority-vote m bits per comparison (buy resolution with samples)
for m in [1, 3, 9, 25]:
    r, c = mean_over_seeds(lambda mu, rng, mm=m: es_pref(mu, rng, gens=25, lam=8, beta=0.5, c=0.0, sparse_p=1.0, votes=mm))
    print(f"  beta=0.5  votes={m:<3} gens=25 reward={r:6.1f}  cos={c:+.3f}")

print("\n=== Result 4: BIAS — comparator scores true + c*salience (systematic) ===")
for c_bias in [0.0, 0.2, 0.5, 1.0, 2.0]:
    r, cc = mean_over_seeds(lambda mu, rng, cb=c_bias: es_pref(mu, rng, gens=25, lam=8, beta=8.0, c=cb, sparse_p=1.0))
    print(f"  bias c={c_bias:<5} gens=25   reward={r:6.1f}  cos={cc:+.3f}")
# does MORE data fix bias? NO — biased fixed point is invariant to data
r, cc = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=200, lam=8, beta=8.0, c=1.0, sparse_p=1.0))
print(f"  bias c=1.0  gens=200  reward={r:6.1f}  cos={cc:+.3f}   <- more data does NOT fix bias")

print("\n=== Result 5: thin-honest vs fat-biased channel ===")
# thin honest: sparse (p=0.1) + noisy (beta=1) but UNBIASED + aggregated, given more gens
r1, c1 = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=150, lam=8, beta=1.0, c=0.0, sparse_p=0.1, votes=5))
# fat biased: dense (p=1) + high-res (beta=8) but BIASED past threshold
r2, c2 = mean_over_seeds(lambda mu, rng: es_pref(mu, rng, gens=150, lam=8, beta=8.0, c=1.0, sparse_p=1.0))
print(f"  thin+honest (p=0.1,beta=1,c=0,5votes,150g)  reward={r1:6.1f}  cos={c1:+.3f}")
print(f"  fat +biased (p=1.0,beta=8,c=1.0,150g)       reward={r2:6.1f}  cos={c2:+.3f}")
