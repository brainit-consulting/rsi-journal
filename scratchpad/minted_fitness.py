"""
B07 — The Fitness It Cannot Mint
Sandbox: can an agent that generates its OWN reward (curiosity / intrinsic
motivation) escape B06's seam that "the outer loop compounds only under an
external fitness signal it cannot mint internally"?

Setup: a k-armed "rooms" world. Each pull of an arm returns an observation.
An agent maintains a forward model of each arm's observation and drives its
choices by an INTRINSIC reward = its own prediction error (surprise).
The world contains three kinds of arm:
  - LEARNABLE arms: observation is a fixed hidden vector + small noise; a
    running-mean forward model drives prediction error -> 0 as it is visited.
  - a NOISY-TV arm: observation is pure high-variance noise; unlearnable, so
    prediction error stays high forever (Burda et al. 2018's noisy-TV).
  - a TASK arm: like a learnable arm, but the ONLY arm carrying external
    task reward. Once learned it is intrinsically boring.

We compare policies:
  (P) prediction-error curiosity (the self-minted signal),
  (C) count-based novelty 1/sqrt(n) (a self-signal that decays with VISITS,
      not with learnability),
  (E) external task reward (the ground truth),
  (R) uniform random baseline.

Falsifiable predictions:
  1. Pure prediction-error curiosity is CAPTURED by the noisy TV: its share
     of pulls stays high and the task arm is under-visited => a self-minted
     fitness signal does not point at ground truth; it is gameable by the
     agent's own environment. (thesis-confirming)
  2. Count-based novelty is NOT captured (1/sqrt(n) decays for the TV too),
     so it finds the task arm -- i.e. curiosity's failure is specific to
     self-referential prediction error, not to intrinsic reward in general.
     (a finding that cuts the other way -- report it)
  3. Hackability scales with the amount of irreducible noise the world
     offers: sweep the number of noisy-TV arms and measure task-arm coverage.
"""
import numpy as np

DIM = 16                 # observation dimensionality
NOISE_LEARNABLE = 0.10   # residual noise on learnable/task arms
NOISE_TV = 1.20          # noise on the noisy-TV arm (unlearnable)
STEPS = 4000
SEEDS = 8

def run(seed, policy, n_learnable=6, n_tv=1, beta=1.0):
    rng = np.random.default_rng(seed)
    # arms: [0..n_learnable-1] learnable, [n_learnable] = TASK, then n_tv TVs
    n_task = 1
    K = n_learnable + n_task + n_tv
    task_idx = n_learnable
    tv_idx = set(range(n_learnable + n_task, K))
    hidden = rng.standard_normal((K, DIM))      # each arm's true mean obs
    model = np.zeros((K, DIM))                   # agent's forward model (running mean)
    counts = np.zeros(K)
    ext_reward = np.zeros(K); ext_reward[task_idx] = 1.0   # external task reward only here

    pulls = np.zeros(K)
    task_reward_collected = 0.0
    eps = 0.10  # exploration floor so no policy self-locks trivially
    pred_err_est = np.full(K, 5.0)  # optimistic init drives an initial sweep of all arms

    for t in range(STEPS):
        if rng.random() < eps:
            a = rng.integers(K)
        else:
            if policy == "pred":            # intrinsic = current prediction error estimate
                # score = expected surprise: use last measured error proxy = ||model-hidden|| unknown to agent,
                # so agent uses its running estimate of its own error magnitude per arm
                score = pred_err_est
            elif policy == "count":         # 1/sqrt(n) novelty
                score = 1.0 / np.sqrt(counts + 1.0)
            elif policy == "ext":           # external ground-truth reward
                score = ext_reward.copy()
            else:                           # random
                score = rng.standard_normal(K)
            a = int(np.argmax(score + 1e-9 * rng.standard_normal(K)))

        # observe
        noise = NOISE_TV if a in tv_idx else NOISE_LEARNABLE
        obs = hidden[a] + noise * rng.standard_normal(DIM)
        # agent's actual prediction error this step
        err = np.linalg.norm(model[a] - obs)
        # update forward model (running mean) -> shrinks error on learnable arms
        counts[a] += 1
        model[a] += (obs - model[a]) / counts[a]
        # update the agent's running estimate of its own surprise per arm
        pred_err_est[a] += 0.15 * (err - pred_err_est[a])

        pulls[a] += 1
        task_reward_collected += ext_reward[a]

    return dict(pulls=pulls, task_idx=task_idx, tv_idx=tv_idx,
                task_share=pulls[task_idx] / STEPS,
                tv_share=sum(pulls[i] for i in tv_idx) / STEPS,
                task_reward=task_reward_collected)

def summarize(policy, **kw):
    rows = [run(s, policy, **kw) for s in range(SEEDS)]
    ts = np.array([r["task_share"] for r in rows])
    vs = np.array([r["tv_share"] for r in rows])
    tr = np.array([r["task_reward"] for r in rows])
    return ts.mean(), vs.mean(), tr.mean()

print("=== Result 1&2: one noisy TV present (n_learnable=6, n_tv=1) ===")
print(f"{'policy':<28}{'task-arm share':>16}{'TV share':>12}{'task reward':>14}")
for pol, name in [("pred","prediction-error curiosity"),
                  ("count","count-based novelty 1/sqrt(n)"),
                  ("ext","external task reward"),
                  ("rand","uniform random")]:
    ts, vs, tr = summarize(pol)
    print(f"{name:<28}{ts:>16.3f}{vs:>12.3f}{tr:>14.1f}")

random_share = 1.0/8.0
print(f"\n(uniform share per arm with K=8 = {random_share:.3f})")

print("\n=== Result 3: hackability vs amount of irreducible noise (n_tv sweep) ===")
print("prediction-error curiosity only; task-arm share should fall as TVs multiply")
print(f"{'n_tv':>6}{'K':>5}{'task-arm share':>18}{'total TV share':>18}{'random task share':>20}")
for n_tv in [0,1,2,4,8]:
    ts, vs, tr = summarize("pred", n_learnable=6, n_tv=n_tv)
    K = 6 + 1 + n_tv
    print(f"{n_tv:>6}{K:>5}{ts:>18.3f}{vs:>18.3f}{1.0/K:>20.3f}")

print("\n=== Result 3b: same sweep but count-based novelty (should NOT collapse) ===")
print(f"{'n_tv':>6}{'K':>5}{'task-arm share':>18}{'total TV share':>18}")
for n_tv in [0,1,2,4,8]:
    ts, vs, tr = summarize("count", n_learnable=6, n_tv=n_tv)
    K = 6 + 1 + n_tv
    print(f"{n_tv:>6}{K:>5}{ts:>18.3f}{vs:>18.3f}")
