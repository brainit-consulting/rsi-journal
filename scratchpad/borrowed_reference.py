"""
B08 — The Reference It Can Only Borrow.

Question (from B07's open ledger line): can an outer loop with NO gradient
tune its own *reward reference* so that a self-computed signal tracks the
world -- or can it only borrow one?

Setup. A K-armed "rooms" world, F features per arm. Each arm k has a fixed
feature template mu_k; a pull returns mu_k + observation noise. The TRUE task
value of an arm is v_k = a . mu_k, where `a` is the (hidden) true reward
reference -- a direction in feature space that says *which features are
actually valuable*.

An inner agent acts on a *reward reference* w (unit vector): it is paid its
own felt reward w . phi on each pull, runs epsilon-greedy over its running
estimate of felt value, and we score it by the TRUE reward it happens to
collect. If w is aligned with a, chasing felt reward = chasing true value.
If w points elsewhere, the agent feels great and collects nothing.

The outer loop is a gradient-free (1+lambda) evolution search over w on the
sphere. The whole experiment is about WHAT the outer loop is scored by:
  ANCHORED  -- fitness = true reward the inner agent collected (external)
  SELF      -- fitness = felt reward the inner agent collected (self-minted)

World is built with a deliberate trap: some arms are "salient distractors"
-- near-zero true value (feature 0 ~ 0) but large magnitude in the other
features, so a misaligned w finds them maximally rewarding. This is the
noisy-TV of B07 lifted into reference space.
"""
import numpy as np

F = 8            # features
A = np.zeros(F); A[0] = 1.0     # true reference: only feature 0 is valuable
T = 250          # inner steps per episode
EPS = 0.10       # inner exploration floor
OBS_NOISE = 0.15


def make_world(rng):
    """4 value arms (true value in feature0), 4 salient distractors (0 value,
    high norm elsewhere), 2 neutral arms. Highest-norm arm is a distractor,
    so felt-reward-maximisation misaligns from true value by construction."""
    arms = []
    kinds = []
    for _ in range(4):                       # value arms
        mu = np.zeros(F)
        mu[0] = rng.uniform(1.5, 3.0)        # real value
        mu[1:] = rng.normal(0, 0.3, F - 1)
        arms.append(mu); kinds.append("value")
    for _ in range(4):                       # salient distractors
        mu = np.zeros(F)
        mu[0] = rng.normal(0, 0.05)          # ~no true value
        d = rng.normal(0, 1.0, F - 1)
        d *= 4.0 / (np.linalg.norm(d) + 1e-9)  # big norm off the value axis
        mu[1:] = d
        arms.append(mu); kinds.append("distractor")
    for _ in range(2):                       # neutral small arms
        mu = rng.normal(0, 0.2, F)
        arms.append(mu); kinds.append("neutral")
    mu = np.array(arms)
    v = mu @ A                               # true value per arm
    return mu, v, kinds


def rollout(w, mu, v, rng):
    """Inner epsilon-greedy bandit paid felt reward w.phi. Returns
    (true_reward, felt_reward) summed over T steps."""
    K = mu.shape[0]
    est = np.zeros(K); n = np.zeros(K)
    true_r = 0.0; felt_r = 0.0
    for t in range(T):
        if rng.random() < EPS or n.min() == 0:
            k = int(rng.integers(K)) if rng.random() < EPS else int(np.argmin(n))
        else:
            k = int(np.argmax(est))
        phi = mu[k] + rng.normal(0, OBS_NOISE, F)
        felt = float(w @ phi)
        n[k] += 1
        est[k] += (felt - est[k]) / n[k]     # running mean of felt value
        true_r += float(v[k])
        felt_r += felt
    return true_r, felt_r


def fitness(w, mu, v, rng, mode, episodes=2):
    tr = fr = 0.0
    for _ in range(episodes):
        t, f = rollout(w, mu, v, rng)
        tr += t; fr += f
    tr /= episodes; fr /= episodes
    return (tr if mode == "true" else fr), tr, fr


def unit(x):
    return x / (np.linalg.norm(x) + 1e-12)


def es_tune(mu, v, rng, mode, gens=25, lam=8, sigma0=0.4, mix_true=1.0):
    """(1+lambda)-ES over the reference w on the unit sphere.
    mode 'true' -> anchored; 'felt' -> self. mix_true in [0,1] = probability a
    given generation is scored by TRUE reward (else felt) -- the thin-anchor dial."""
    w = unit(rng.normal(0, 1, F))
    best_score, _, _ = fitness(w, mu, v, rng, "true" if mode == "true" else "felt")
    for g in range(gens):
        sigma = sigma0 * (1 - g / gens) + 0.05
        use_true = (mode == "true") and (rng.random() < mix_true)
        smode = "true" if use_true else "felt"
        # re-score incumbent under this generation's objective
        best_score, _, _ = fitness(w, mu, v, rng, smode)
        for _ in range(lam):
            cand = unit(w + rng.normal(0, sigma, F))
            sc, _, _ = fitness(cand, mu, v, rng, smode)
            if sc > best_score:
                best_score = sc; w = cand
    return w


def evaluate(w, mu, v, rng, episodes=30):
    tr = 0.0
    for _ in range(episodes):
        t, _ = rollout(w, mu, v, rng)
        tr += t
    return tr / episodes


def cos(u, w):
    return float(unit(u) @ unit(w))


# ---------------------------------------------------------------------------
SEEDS = range(6)

print("=" * 74)
print("EXPERIMENT 1 -- can the outer loop tune a reward reference?")
print("=" * 74)
rows = {"anchored": [], "self": [], "random": [], "oracle": []}
cosr = {"anchored": [], "self": []}
for s in SEEDS:
    rng = np.random.default_rng(1000 + s)
    mu, v, kinds = make_world(rng)
    w_anch = es_tune(mu, v, rng, "true")
    w_self = es_tune(mu, v, rng, "felt")
    rows["anchored"].append(evaluate(w_anch, mu, v, rng))
    rows["self"].append(evaluate(w_self, mu, v, rng))
    rows["oracle"].append(evaluate(unit(A), mu, v, rng))
    # random-reference baseline: mean true reward over random unit w
    rr = [evaluate(unit(rng.normal(0, 1, F)), mu, v, rng, episodes=5) for _ in range(20)]
    rows["random"].append(float(np.mean(rr)))
    cosr["anchored"].append(cos(A, w_anch))
    cosr["self"].append(cos(A, w_self))

print(f"{'policy':<34}{'cos(w*,a)':>12}{'true reward/ep':>18}")
print("-" * 64)
print(f"{'oracle  w = a (true reference)':<34}{1.000:>12.3f}{np.mean(rows['oracle']):>18.1f}")
print(f"{'ANCHORED outer (scored by truth)':<34}{np.mean(cosr['anchored']):>12.3f}{np.mean(rows['anchored']):>18.1f}")
print(f"{'SELF outer (scored by felt reward)':<34}{np.mean(cosr['self']):>12.3f}{np.mean(rows['self']):>18.1f}")
print(f"{'random reference (baseline)':<34}{0.000:>12.3f}{np.mean(rows['random']):>18.1f}")

print()
print("=" * 74)
print("EXPERIMENT 2 -- how little external signal does the outer loop need?")
print("  (mix_true = fraction of outer generations scored by TRUE reward)")
print("=" * 74)
print(f"{'mix_true':>10}{'cos(w*,a)':>14}{'true reward/ep':>18}")
print("-" * 42)
for mt in [0.0, 0.10, 0.30, 1.0]:
    cs = []; trs = []
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        mu, v, kinds = make_world(rng)
        # mode 'true' so the dial is live; mix_true routes each gen true-vs-felt
        w = es_tune(mu, v, rng, "true", mix_true=mt)
        cs.append(cos(A, w)); trs.append(evaluate(w, mu, v, rng))
    print(f"{mt:>10.2f}{np.mean(cs):>14.3f}{np.mean(trs):>18.1f}")

print()
print("=" * 74)
print("EXPERIMENT 3 -- does stacking SELF-scored meta-levels manufacture")
print("  the anchor? A meta-ES tunes the inner self-ES's (sigma0, init),")
print("  itself scored by felt reward. If the regress could bootstrap a")
print("  reference, best cos would climb with meta-search effort.")
print("=" * 74)


def inner_self_es(mu, v, rng, sigma0, w_init, gens=25, lam=8):
    w = unit(w_init)
    best, _, _ = fitness(w, mu, v, rng, "felt")
    for g in range(gens):
        sigma = sigma0 * (1 - g / gens) + 0.05
        best, _, _ = fitness(w, mu, v, rng, "felt")
        for _ in range(lam):
            cand = unit(w + rng.normal(0, sigma, F))
            sc, _, _ = fitness(cand, mu, v, rng, "felt")
            if sc > best:
                best = sc; w = cand
    return w


meta_self_cos = []; meta_self_true = []
meta_anch_cos = []; meta_anch_true = []
for s in SEEDS:
    rng = np.random.default_rng(3000 + s)
    mu, v, kinds = make_world(rng)
    # meta-search over (sigma0, init) with FELT (self) meta-fitness
    best_felt = -1e9; best_w_self = None
    best_true = -1e9; best_w_anch = None
    for _ in range(8):                       # meta candidates
        sig = float(rng.uniform(0.15, 0.6))
        w0 = rng.normal(0, 1, F)
        w = inner_self_es(mu, v, rng, sig, w0)
        _, tr, fr = fitness(w, mu, v, rng, "felt", episodes=6)
        if fr > best_felt:                   # meta scored by SELF
            best_felt = fr; best_w_self = w
        if tr > best_true:                    # meta scored by TRUTH (control)
            best_true = tr; best_w_anch = w
    meta_self_cos.append(cos(A, best_w_self))
    meta_self_true.append(evaluate(best_w_self, mu, v, rng))
    meta_anch_cos.append(cos(A, best_w_anch))
    meta_anch_true.append(evaluate(best_w_anch, mu, v, rng))

print(f"{'meta-selection scored by':<34}{'cos(w*,a)':>12}{'true reward/ep':>18}")
print("-" * 64)
print(f"{'SELF (felt reward, all levels)':<34}{np.mean(meta_self_cos):>12.3f}{np.mean(meta_self_true):>18.1f}")
print(f"{'TRUTH at the top (control)':<34}{np.mean(meta_anch_cos):>12.3f}{np.mean(meta_anch_true):>18.1f}")
print()
print("done.")
