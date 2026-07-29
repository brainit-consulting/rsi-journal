"""
B12 — The Supplier It Cannot Certify.  (Series II, Movement III opener.)

B11 closed Movement II: a frozen self-refining loop needs DECISIVE, VERIFIED
independence imported from outside, in a quantity large enough to WIN its
decisions, from a SUPPLIER it cannot audit without already holding what the
supplier sells. That names a new object -- the supplier/institution -- and one
question: can the loop lean on an external INSTITUTION to furnish independence,
or does the whole B08-B11 problem simply move up a level to "who certifies the
supplier?"

Three experiments in the SAME B08-B11 world (K=10 feature bandit; inner
eps-greedy bandit paid felt reward w.phi; outer (1+lambda) ES over reference w;
1-bit Bradley-Terry comparator). numpy, fixed seeds, 12 seeds. Nulls reported.

  Exp1  CAPTURE PROPAGATES. The loop imports its verdict from an INSTITUTION =
        a meta-panel of M sources aggregated by majority. A fraction rho_I of the
        sources are captured shared-bias clones (c=1.0, same loved arm); the rest
        are independent honest sources (c=0). Sweep rho_I. Prediction: importing
        "from an institution" buys nothing unless the institution's OWN internal
        independence is real -- recovery at rho_I=0, collapse to ~random at
        rho_I=1, with a majority-capture threshold at rho_I~0.5 (B10 up a level).

  Exp2  AUTHORITY IS A BACKWARDS CERTIFICATE. Offer two institutions and let the
        loop judge them only by the one internal mark of a reliable body it can
        read: how UNANIMOUS the institution's own sources are.
          I_honest = M independent honest sources (rho_I=0)  -- worth trusting
          I_cartel = M correlated captured sources (rho_I=1) -- worthless
        Measure each institution's internal unanimity, then what importing each
        does to true reward. Prediction: the cartel is MORE unanimous (correlated
        sources always agree) yet only the honest institution recovers the loop --
        so internal consensus (the mark of authority) ranks institutions
        BACKWARDS. B10's disagreement-inversion, lifted to the supplier.

  Exp3  EXOGENEITY, NOT AUTHORITY, STOPS THE REGRESS. Two institutions that
        aggregate identically (both fully honest, independent sources) but differ
        in what they are GROUNDED in:
          I_out  = OUTCOME-grounded: sources report an exogenous outcome (true
                   reward of the selected arm) the loop's policy cannot influence.
          I_pref = PREFERENCE-grounded: sources report the agent's own FELT value
                   of a reference (max_k w.mu_k) -- a self-referential quantity the
                   optimization pressure reaches and bends.
        Sweep optimization pressure (ES generations). Prediction: I_pref degrades
        as pressure rises (Goodhart -- driven to the high-magnitude distractor),
        I_out holds near oracle. The property that stops the regress is grounding
        in something the loop cannot influence -- exogeneity -- not a better
        aggregator or a higher authority. (Evolution's survival channel was
        uncapturable because it is an outcome, not a report.)
"""
import numpy as np

F = 8
K = 10
A = np.zeros(F); A[0] = 1.0

def make_world(rng):
    mu = np.zeros((K, F))
    for k in range(4):                        # 4 value arms (on-axis value ~1.5-3)
        mu[k, 0] = rng.uniform(1.5, 3.0)
        mu[k, 1:] = rng.normal(0, 0.3, F - 1)
    for k in range(4, 8):                      # 4 salient distractors (off-axis norm ~4)
        mu[k, 0] = rng.normal(0, 0.05)
        d = rng.normal(0, 1, F - 1); d /= (np.linalg.norm(d) + 1e-9)
        mu[k, 1:] = d * rng.uniform(3.5, 4.5)
    for k in range(8, 10):                     # 2 neutral
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

# ---- a source-channel = (bias magnitude c, loved distractor arm). Honest: c=0. ----
def judged(w, mu, c, loved):
    w = w / (np.linalg.norm(w) + 1e-9)
    k = int(np.argmax(mu @ w))
    worth = float(true_reward(mu)[k])
    if c > 0 and k == loved:
        worth += c * float(salience(mu)[k])
    return worth

def source_prefers(wa, wb, mu, rng, beta, c, loved):
    d = judged(wa, mu, c, loved) - judged(wb, mu, c, loved)
    return rng.random() < 1.0 / (1.0 + np.exp(-beta * d))

def institution_prefers(wa, wb, mu, rng, beta, sources):
    """Majority vote of an institution's list of (c, loved) sources."""
    votes = sum(1 for (c, lv) in sources if source_prefers(wa, wb, mu, rng, beta, c, lv))
    return votes * 2 > len(sources)

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
M = 9                     # institution size (odd -> clean majority)

def baselines():
    orc, rnd = [], []
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        mu = make_world(rng)
        orc.append(evaluate(A.copy(), mu, rng))
        rnd.append(np.mean([evaluate(rng.normal(0, 1, F), mu, rng) for _ in range(20)]))
    return np.mean(orc), np.mean(rnd)

print("=== baselines (B08-B11 world) ===")
orc, rnd = baselines()
print(f"oracle (w=a)     reward/ep = {orc:6.1f}")
print(f"random reference reward/ep = {rnd:6.1f}")

def build_institution(rho_I, mu, rng, c=1.0):
    """M sources; round(rho_I*M) are captured clones sharing ONE loved arm, rest honest."""
    n_cap = int(round(rho_I * M))
    shared = int(rng.choice(range(4, 8)))
    sources = [(c, shared)] * n_cap + [(0.0, -1)] * (M - n_cap)
    return sources

# ---- Exp1: capture propagates up -- institution only as good as its internal independence
print(f"\n=== Exp1: capture propagates (import verdict from an M={M}-source institution) ===")
print("fraction rho_I of the institution's own sources are captured shared-bias clones")
def import_from_institution(rho_I):
    rews = []
    for s in SEEDS:
        rng = np.random.default_rng(9100 + s)
        mu = make_world(rng)
        sources = build_institution(rho_I, mu, rng)
        decide = lambda cand, w: institution_prefers(cand, w, mu, rng, BETA, sources)
        rews.append(evaluate(es(mu, rng, decide), mu, rng))
    return np.mean(rews)
print(f"{'rho_I':>6} | {'captured sources':>16} | {'reward':>8}")
for rho_I in [0.0, 0.25, 0.5, 0.67, 0.75, 1.0]:
    print(f"{rho_I:>6} | {int(round(rho_I*M)):>7}/{M:<8} | {import_from_institution(rho_I):>8.1f}")

# ---- Exp2: internal consensus (authority) is a BACKWARDS certificate ------------------
print("\n=== Exp2: authority is a backwards certificate ===")
print("two institutions; loop reads only each institution's INTERNAL unanimity")
def unanimity_and_worth(rho_I, trials=2500):
    """internal unanimity = P(all sources agree on a random pairwise verdict); worth = loop reward when imported."""
    unan, worth = [], []
    for s in SEEDS:
        rng = np.random.default_rng(9200 + s)
        mu = make_world(rng)
        sources = build_institution(rho_I, mu, rng)
        agree = 0
        for _ in range(trials):
            W = rng.normal(0, 1, (2, F)); W /= np.linalg.norm(W, axis=1, keepdims=True)
            votes = [source_prefers(W[0], W[1], mu, rng, BETA, c, lv) for (c, lv) in sources]
            if all(votes) or not any(votes):
                agree += 1
        unan.append(agree / trials)
        decide = lambda cand, w: institution_prefers(cand, w, mu, rng, BETA, sources)
        worth.append(evaluate(es(mu, rng, decide), mu, rng))
    return np.mean(unan), np.mean(worth)
uH, wH = unanimity_and_worth(0.0)     # honest, independent sources
uC, wC = unanimity_and_worth(1.0)     # correlated captured cartel
print(f"I_honest (rho_I=0, independent sources): internal unanimity = {uH:.3f}  worth = {wH:.1f}")
print(f"I_cartel (rho_I=1, correlated sources) : internal unanimity = {uC:.3f}  worth = {wC:.1f}")
print(f"  -> the MORE unanimous institution ({'cartel' if uC>uH else 'honest'}) is the {'WORSE' if wC<wH else 'better'} one to trust")

# ---- Exp3: exogeneity, not authority, stops the regress -------------------------------
print("\n=== Exp3: exogeneity vs authority under rising optimization pressure ===")
print("both institutions fully honest & independent; differ only in what they are GROUNDED in")
def outcome_prefers(wa, wb, mu, rng, beta):
    """Exogenous OUTCOME: true reward of the selected arm (policy cannot influence it)."""
    d = float(true_reward(mu)[int(np.argmax(mu @ wa))]) - \
        float(true_reward(mu)[int(np.argmax(mu @ wb))])
    return rng.random() < 1.0 / (1.0 + np.exp(-beta * d))
def preference_prefers(wa, wb, mu, rng, beta):
    """Self-referential REPORT: the agent's own FELT value of each reference, max_k w.mu_k."""
    d = float(np.max(mu @ wa)) - float(np.max(mu @ wb))
    return rng.random() < 1.0 / (1.0 + np.exp(-beta * d))
def grounded_run(kind, gens):
    rews = []
    for s in SEEDS:
        rng = np.random.default_rng(9300 + s)
        mu = make_world(rng)
        if kind == "out":
            decide = lambda cand, w: outcome_prefers(cand, w, mu, rng, BETA)
        else:
            decide = lambda cand, w: preference_prefers(cand, w, mu, rng, BETA)
        rews.append(evaluate(es(mu, rng, decide, gens=gens), mu, rng))
    return np.mean(rews)
print(f"{'gens':>5} | {'I_out (outcome)':>16} | {'I_pref (preference)':>20}")
for gens in [10, 25, 50, 100]:
    print(f"{gens:>5} | {grounded_run('out', gens):>16.1f} | {grounded_run('pref', gens):>20.1f}")
print("\ndone.")
