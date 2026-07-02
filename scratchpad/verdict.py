"""
B06 — The Verdict. The division-of-labour measurement.

A task with TWO objects to optimize:
  (outer) a non-differentiable STRUCTURAL choice g in {0..K-1}: which fixed
          nonlinearity is applied to the input features. Categorical => no gradient.
  (inner) a continuous WEIGHT matrix W (d_out x d_in): differentiable given g.

Teacher: y = W* @ phi_{g*}(x) + noise, with a specific true g*.

Three regimes:
  A. PURE GRADIENT  — cannot reach the categorical g, so it fixes a default g and
                       least-squares-solves W (exact gradient optimum for that g).
  B. PURE EVOLUTION — ES over the weights W (given the correct g), swept over D_w,
                       to expose the inner-loop dimension tax from B05.
     B'. ES over (g,W) jointly via a continuous relaxation of g — the fully
         "evolve everything" regime.
  C. HYBRID         — evolution/search picks g (K cheap trials), gradient (LSQ)
                       fits W exactly for the chosen g.

Prediction (the verdict): C dominates. A is stuck whenever g* != default.
B's cost to reach LSQ-level loss grows with D_w (B05's wall), and B' is worse still.
Falsifier: hybrid fails to beat both, OR pure-evolution matches hybrid at equal/lower
cost and without cost growing in D_w.
"""
import numpy as np

# ---- fixed nonlinearity library (the discrete outer choice) --------------
def phi(g, X):
    if g == 0: return X                      # identity
    if g == 1: return X**2                    # square
    if g == 2: return np.sin(3.0 * X)         # oscillatory
    if g == 3: return np.tanh(2.0 * X)        # saturating
    if g == 4: return np.abs(X)               # rectify-abs
    raise ValueError(g)
K = 5

def make_task(d_in, d_out, g_star, n=400, noise=0.05, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d_in))
    Wt = rng.standard_normal((d_out, d_in)) / np.sqrt(d_in)
    Y = phi(g_star, X) @ Wt.T + noise * rng.standard_normal((n, d_out))
    # train/test split
    ntr = n // 2
    return (X[:ntr], Y[:ntr]), (X[ntr:], Y[ntr:]), Wt

def lsq_fit(g, Xtr, Ytr):
    """Exact gradient optimum for the linear-in-W problem given structure g."""
    P = phi(g, Xtr)                            # (n, d_in)
    W, *_ = np.linalg.lstsq(P, Ytr, rcond=None)  # (d_in, d_out)
    return W.T                                 # (d_out, d_in)

def mse(g, W, X, Y):
    return float(np.mean((phi(g, X) @ W.T - Y)**2))

# ---- ES over weights W (inner-loop optimizer), given g -------------------
def es_fit_W(g, Xtr, Ytr, d_in, d_out, pop, iters, sigma=0.1, lr=0.3, seed=0):
    rng = np.random.default_rng(seed)
    W = np.zeros((d_out, d_in))
    for _ in range(iters):
        E = rng.standard_normal((pop, d_out, d_in))
        # antithetic pairs
        losses_p = np.array([mse(g, W + sigma*E[k], Xtr, Ytr) for k in range(pop)])
        losses_m = np.array([mse(g, W - sigma*E[k], Xtr, Ytr) for k in range(pop)])
        # reward = -loss; gradient ascent on reward == descent on loss
        adv = -(losses_p - losses_m)          # (pop,)
        g_est = (adv[:, None, None] * E).mean(0) / (2*sigma)
        W = W + lr * g_est
    return W

# =========================================================================
np.set_printoptions(precision=4, suppress=True)
print("="*70)
print("B06 VERDICT — division of labour measurement")
print("="*70)

# ---- REGIME A vs C: reaching the non-differentiable structural choice -----
print("\n[1] Structural choice: g* varies. default g for pure-gradient = 0 (identity)")
print("    A = pure gradient (fixed g=0, LSQ W).  C = hybrid (search g, LSQ W).")
print(f"    d_in=8, d_out=4, 4 seeds per g*.  test MSE (lower=better).")
print("    g*   A:grad(fixed)   C:hybrid(search)   C picks g*?")
default_g = 0
for g_star in range(K):
    a_list, c_list, hit = [], [], 0
    for seed in range(4):
        (Xtr,Ytr),(Xte,Yte),_ = make_task(8, 4, g_star, seed=seed)
        # A: fixed default structure
        Wa = lsq_fit(default_g, Xtr, Ytr)
        a_list.append(mse(default_g, Wa, Xte, Yte))
        # C: search over all K structures on TRAIN, pick best, report TEST
        cand = [(mse(g, lsq_fit(g, Xtr, Ytr), Xtr, Ytr), g) for g in range(K)]
        g_hat = min(cand)[1]
        Wc = lsq_fit(g_hat, Xtr, Ytr)
        c_list.append(mse(g_hat, Wc, Xte, Yte))
        hit += (g_hat == g_star)
    print(f"     {g_star}     {np.mean(a_list):8.4f}        {np.mean(c_list):8.4f}         {hit}/4")

# ---- REGIME B: inner-loop tax — ES on W vs LSQ, sweep D_w ----------------
print("\n[2] Inner loop (weights): pure-evolution (ES on W) vs gradient (LSQ).")
print("    Correct g* known; measure evaluations ES needs to reach 1.10x LSQ test MSE,")
print("    as weight-dimension D_w = d_out*d_in grows. (LSQ is one exact solve.)")
print("    d_in x d_out   D_w    LSQ testMSE   ES pop*iters to reach 1.10xLSQ")
g_star = 2  # oscillatory: a structure pure-gradient-with-default can't fake
configs = [(4,2),(8,4),(16,8),(32,16)]
pop = 20
for d_in, d_out in configs:
    Dw = d_in*d_out
    seeds_evals = []
    lsq_list = []
    for seed in range(4):
        (Xtr,Ytr),(Xte,Yte),_ = make_task(d_in, d_out, g_star, n=600, seed=seed)
        Wl = lsq_fit(g_star, Xtr, Ytr)
        lsq_mse = mse(g_star, Wl, Xte, Yte)
        lsq_list.append(lsq_mse)
        target = 1.10 * lsq_mse
        # grow ES iteration budget until it reaches target (or cap)
        evals = None
        for iters in [5,10,20,40,80,160,320,640,1280]:
            We = es_fit_W(g_star, Xtr, Ytr, d_in, d_out, pop, iters, seed=seed)
            if mse(g_star, We, Xte, Yte) <= target:
                evals = pop*2*iters   # antithetic => 2 evals per pop member per iter
                break
        seeds_evals.append(evals if evals is not None else float('inf'))
    finite = [e for e in seeds_evals if np.isfinite(e)]
    ev = int(np.mean(finite)) if finite else float('inf')
    reached = f"{ev:>8} evals ({sum(np.isfinite(seeds_evals))}/4 seeds)"
    print(f"    {d_in:>2} x {d_out:<2}      {Dw:>3}   {np.mean(lsq_list):9.5f}    {reached}")

# ---- REGIME B': evolve everything (g relaxed + W) — the maximalist -------
print("\n[3] Pure-evolution 'evolve everything': ES over W AND a softmax over g.")
print("    Same budget as hybrid's structural search + a modest weight budget.")
print("    Compared to hybrid C at matched *total* evaluations. g*=2, d_in=8,d_out=4.")
def es_joint(Xtr, Ytr, d_in, d_out, pop, iters, sigma=0.1, lr=0.3, seed=0):
    rng = np.random.default_rng(seed)
    W = np.zeros((d_out, d_in)); logits = np.zeros(K)
    def loss(W_, logits_):
        w = np.exp(logits_ - logits_.max()); w /= w.sum()
        feat = sum(w[g]*phi(g, Xtr) for g in range(K))
        return float(np.mean((feat @ W_.T - Ytr)**2))
    for _ in range(iters):
        Ew = rng.standard_normal((pop, d_out, d_in))
        El = rng.standard_normal((pop, K))
        lp = np.array([loss(W+sigma*Ew[k], logits+sigma*El[k]) for k in range(pop)])
        lm = np.array([loss(W-sigma*Ew[k], logits-sigma*El[k]) for k in range(pop)])
        adv = -(lp-lm)
        W += lr * (adv[:,None,None]*Ew).mean(0)/(2*sigma)
        logits += lr * (adv[:,None]*El).mean(0)/(2*sigma)
    return W, logits
for seed in range(1):
    (Xtr,Ytr),(Xte,Yte),_ = make_task(8,4,2,n=600,seed=seed)
    # hybrid total evals: K structural LSQ (count each as 1) is essentially free;
    # give ES-joint a generous budget and see where it lands
    for iters in [50, 200, 800]:
        W,logits = es_joint(Xtr,Ytr,8,4,pop,iters,seed=seed)
        w = np.exp(logits-logits.max()); w/=w.sum()
        feat = sum(w[g]*phi(g,Xte) for g in range(K))
        te = float(np.mean((feat@W.T - Yte)**2))
        print(f"    ES-joint iters={iters:>4} ({pop*2*iters:>6} evals): test MSE {te:.5f}, "
              f"g-weights {np.round(w,3)} (g*=2)")
    # hybrid reference
    cand=[(mse(g,lsq_fit(g,Xtr,Ytr),Xtr,Ytr),g) for g in range(K)]
    gh=min(cand)[1]; te_h=mse(gh,lsq_fit(gh,Xtr,Ytr),Xte,Yte)
    print(f"    HYBRID (K={K} LSQ solves ~ {2*K} evals):        test MSE {te_h:.5f}, picks g={gh}")
print("\ndone.")
