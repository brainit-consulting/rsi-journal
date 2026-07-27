"""
B10 — The Bias It Cannot Audit.

B09 established: a borrowed preference channel's load-bearing property is
UNBIASEDNESS, not width. A channel biased past the value-gap threshold inverts
the loop below random, and no amount of data fixes it. B09's open question:
is there ANY internal instrument -- consistency checks, cross-referencing
multiple channels, adversarial probing -- by which a refinement loop could
DETECT that its imported channel is biased BEFORE optimizing into the trap?
Or is bias-detection strictly another thing sourced from outside?

Two audit families, tested against the B08/B09 world:

  (1) INTERNAL CONSISTENCY (transitivity): probe the channel with reference
      triples, count cyclic/intransitive verdicts. Prediction: cyclic rate
      tracks NOISE (beta), FLAT in BIAS (c). A coherent-but-biased judge is
      perfectly transitive -> consistency audits are blind to bias.

  (2) CROSS-REFERENCING M channels: majority-vote a panel of biased channels
      whose biases share a fraction rho (rho=0 independent, rho=1 identical).
      Prediction: correction is bought only in the INDEPENDENT component;
      rho=1 (shared bias) => panel = single biased channel (no help), and the
      inter-channel DISAGREEMENT that would flag bias vanishes -> consensus
      indistinguishable from correctness. Bias-detection reach == channel
      independence, which the loop cannot mint (echo of Series I No.05/No.08).

World reused from B09 (thin_channel.py). numpy, fixed seeds. Nulls reported.
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

def salience(mu): return np.linalg.norm(mu[:, 1:], axis=1)  # off-axis magnitude (B09)

# ---- channel biases: each channel over-credits ONE 'vivid' distractor arm.
# A channel's bias = "loved arm" (a salient distractor). rho = fraction of
# channels that share ONE common loved arm; the rest love a random distractor.
# This mirrors Series I No.08's rho: the SHARED blind spot vs idiosyncratic ones.
def make_loved_arms(M, rho, rng):
    DISTRACTORS = list(range(4, 8))
    shared = int(rng.choice(DISTRACTORS))
    loved = []
    for _ in range(M):
        loved.append(shared if rng.random() < rho else int(rng.choice(DISTRACTORS)))
    return loved

def judged(w, mu, c, loved):
    """Perceived worth of reference w: true value of the arm it settles on, plus
    (if that arm is this channel's loved distractor) a salience bonus c*||off-axis||
    -- the systematic over-crediting of a vivid feature (B09's bias, made per-arm)."""
    w = w / (np.linalg.norm(w) + 1e-9)
    k = int(np.argmax(mu @ w))
    worth = float(true_reward(mu)[k])
    if k == loved:
        worth += c * float(salience(mu)[k])
    return worth

def prefers_ch(wa, wb, mu, rng, beta, c, loved):
    d = judged(wa, mu, c, loved) - judged(wb, mu, c, loved)
    p = 1.0 / (1.0 + np.exp(-beta * d))
    return rng.random() < p

def panel_prefers(wa, wb, mu, rng, beta, c, loved_arms):
    """Majority vote of the M-channel panel (each a 1-bit biased comparator)."""
    votes = sum(1 for lv in loved_arms if prefers_ch(wa, wb, mu, rng, beta, c, lv))
    return votes * 2 > len(loved_arms)

def es_panel(mu, rng, loved_arms, gens=25, lam=8, beta=8.0, c=1.0):
    w = rng.normal(0, 1, F); w /= np.linalg.norm(w)
    for g in range(gens):
        sig = 0.5 * (1 - g / gens) + 0.05
        for _ in range(lam):
            cand = w + rng.normal(0, sig, F); cand /= np.linalg.norm(cand)
            if panel_prefers(cand, w, mu, rng, beta, c, loved_arms):
                w = cand
    return w

SEEDS = list(range(6))

def baselines():
    orc, rnd = [], []
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        mu = make_world(rng)
        orc.append(evaluate(A.copy(), mu, rng))
        rnd.append(np.mean([evaluate(rng.normal(0, 1, F), mu, rng) for _ in range(20)]))
    return np.mean(orc), np.mean(rnd)

print("=== baselines ===")
orc, rnd = baselines()
print(f"oracle (w=a)     reward/ep = {orc:6.1f}")
print(f"random reference reward/ep = {rnd:6.1f}")

# ---- Exp 1: transitivity audit — cyclic rate vs (beta, c). Single channel. ----
print("\n=== Exp1: internal-consistency (transitivity) audit ===")
print("cyclic/intransitive verdict rate over random reference triples")
def cyclic_rate(beta, c, trials=4000):
    rates = []
    for s in SEEDS:
        rng = np.random.default_rng(3000 + s)
        mu = make_world(rng)
        b = make_loved_arms(1, 1.0, rng)[0]    # one fixed loved distractor
        cyc = 0
        for _ in range(trials):
            W = rng.normal(0, 1, (3, F)); W /= np.linalg.norm(W, axis=1, keepdims=True)
            ab = prefers_ch(W[0], W[1], mu, rng, beta, c, b)
            bc = prefers_ch(W[1], W[2], mu, rng, beta, c, b)
            ca = prefers_ch(W[2], W[0], mu, rng, beta, c, b)
            if (ab and bc and ca) or ((not ab) and (not bc) and (not ca)):
                cyc += 1
        rates.append(cyc / trials)
    return np.mean(rates)
print(f"{'beta':>6} | {'c=0.0':>8} {'c=1.0':>8}")
for beta in [0.5, 1.0, 2.0, 8.0]:
    r0 = cyclic_rate(beta, 0.0); r1 = cyclic_rate(beta, 1.0)
    print(f"{beta:>6} | {r0:>8.3f} {r1:>8.3f}")

# ---- Exp 2: cross-referencing — M-channel panel, bias past threshold, vary rho ----
print("\n=== Exp2: cross-referencing M=8 biased channels (c=1.0, beta=8), vary rho ===")
def panel_result(rho, M=8, c=1.0):
    rews, coss = [], []
    for s in SEEDS:
        rng = np.random.default_rng(4000 + s)
        mu = make_world(rng)
        loved = make_loved_arms(M, rho, rng)
        w = es_panel(mu, rng, loved, gens=25, lam=8, beta=8.0, c=c)
        rews.append(evaluate(w, mu, rng))
        wn = w / (np.linalg.norm(w) + 1e-9); coss.append(float(wn @ A))
    return np.mean(rews), np.mean(coss)
print(f"{'rho':>6} | {'reward':>8} {'cos':>8}")
for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
    r, c = panel_result(rho)
    print(f"{rho:>6} | {r:>8.1f} {c:>+8.3f}")
# single biased channel control (should match rho=1)
r1, c1 = panel_result(1.0, M=1)
print(f" M=1   | {r1:>8.1f} {c1:>+8.3f}   <- single biased channel control")
# honest panel control (c=0)
rh, ch = panel_result(1.0, M=8, c=0.0)
print(f"c=0    | {rh:>8.1f} {ch:>+8.3f}   <- honest panel (no bias) upper ref")

# ---- Exp 3: disagreement as a bias detector — does it see SHARED bias? ----
print("\n=== Exp3: inter-channel DISAGREEMENT rate (the internal bias alarm) ===")
print("fraction of random comparisons where the M=8 panel is split, beta=8")
def disagreement(rho, c, M=8, trials=3000):
    ds = []
    for s in SEEDS:
        rng = np.random.default_rng(5000 + s)
        mu = make_world(rng)
        loved = make_loved_arms(M, rho, rng)
        split = 0
        for _ in range(trials):
            W = rng.normal(0, 1, (2, F)); W /= np.linalg.norm(W, axis=1, keepdims=True)
            votes = sum(1 for lv in loved if prefers_ch(W[0], W[1], mu, rng, 8.0, c, lv))
            if 0 < votes < M:        # not unanimous
                split += 1
        ds.append(split / trials)
    return np.mean(ds)
print(f"{'rho':>6} | {'c=0.0':>8} {'c=1.0':>8}  (alarm should rise with bias IF it can see it)")
for rho in [0.0, 0.5, 1.0]:
    d0 = disagreement(rho, 0.0); d1 = disagreement(rho, 1.0)
    print(f"{rho:>6} | {d0:>8.3f} {d1:>8.3f}")
