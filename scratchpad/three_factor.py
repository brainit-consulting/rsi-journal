"""
B04 sandbox: is a scalar-neuromodulated local rule the same thing as backprop?

The brain's demonstrably-real machinery is a LOCAL synaptic rule (LTP/LTD,
eligibility trace) GATED BY A SCALAR neuromodulator (dopamine ~ reward
prediction error). The "three-factor" rule:  dW = pre x post-eligibility x M,
where M is ONE global scalar. The popular gloss reads this as "the brain does
gradient descent." This script measures the gap.

Canonical mapping: a reward-modulated three-factor rule with node-level
exploration noise IS node perturbation (Williams REINFORCE / Fiete-Seung).
It is an UNBIASED estimate of the true gradient -- but a scalar third factor
cannot carry a per-synapse error VECTOR, so the single-shot estimate is high
variance, and the variance grows with the number of units N
(Werfel, Xie & Seung 2005: node perturbation is ~N times slower than backprop).

We measure, at a fixed weight configuration:
  (a) is the three-factor update unbiased? (mean cosine -> +1 as samples grow)
  (b) single-shot fidelity: cosine of one estimate to the true gradient
  (c) how (b) and the samples-to-align scale with hidden width N.

numpy only, fixed seeds. Backprop reference finite-difference-checked.
"""
import numpy as np

def net_init(n_in, n_hid, n_out, rng):
    # small random net, tanh hidden, linear output, MSE loss
    W = rng.standard_normal((n_in, n_hid)) / np.sqrt(n_in)
    V = rng.standard_normal((n_hid, n_out)) / np.sqrt(n_hid)
    return W, V

def forward(x, W, V):
    h_pre = x @ W
    h = np.tanh(h_pre)
    y = h @ V
    return h_pre, h, y

def loss(y, t):
    return 0.5 * np.sum((y - t) ** 2)

def true_grad(x, t, W, V):
    h_pre, h, y = forward(x, W, V)
    dy = (y - t)                       # dL/dy
    dV = np.outer(h, dy)
    dh = dy @ V.T                      # dL/dh
    dhpre = dh * (1 - h ** 2)          # through tanh
    dW = np.outer(x, dhpre)
    return dW, dV

def fd_check(x, t, W, V, eps=1e-6):
    """finite-difference check of the backprop gradient on W."""
    dW, _ = true_grad(x, t, W, V)
    g = np.zeros_like(W)
    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            Wp = W.copy(); Wp[i, j] += eps
            Wm = W.copy(); Wm[i, j] -= eps
            _, _, yp = forward(x, Wp, V)
            _, _, ym = forward(x, Wm, V)
            g[i, j] = (loss(yp, t) - loss(ym, t)) / (2 * eps)
    return np.max(np.abs(g - dW))

def node_perturbation_sample(x, t, W, V, sigma):
    """ONE three-factor / node-perturbation update of the HIDDEN->? path.

    Perturb hidden-unit activities with noise xi (the exploratory 'post'
    fluctuation an eligibility trace records). The third factor is the SCALAR
    reward-prediction-error M = -(L_perturbed - L_baseline) -- one number, the
    dopamine-style global signal. Local synaptic update on W:
        dW_ij ∝ x_i * xi_j * M       (pre x local-noise x global scalar)
    This is an unbiased estimate of -dL/dh_pre folded onto W (Fiete-Seung).
    Returns an estimate of the DESCENT direction on W.
    """
    h_pre, h, y = forward(x, W, V)
    L0 = loss(y, t)
    xi = sigma * np.random.standard_normal(h_pre.shape)   # exploratory noise on hidden pre-activations
    h_pert = np.tanh(h_pre + xi)
    y_pert = h_pert @ V
    Lp = loss(y_pert, t)
    M = -(Lp - L0) / (sigma ** 2)        # scalar reward-prediction-error (normalised)
    # eligibility on W is pre-synaptic activity x the local exploratory fluctuation
    est_descent_W = np.outer(x, xi) * M
    return est_descent_W

def cosine(a, b):
    a = a.ravel(); b = b.ravel()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def run_width(n_hid, seeds=4, sigma=1e-3, batches=(1, 10, 100, 1000)):
    """Return single-shot cosine and averaged-cosine vs true gradient,
    plus angle, for a given hidden width, averaged over seeds + inputs."""
    out = {b: [] for b in batches}
    single = []
    for s in range(seeds):
        rng = np.random.default_rng(100 + s)
        np.random.seed(100 + s)
        n_in, n_out = 8, 3
        W, V = net_init(n_in, n_hid, n_out, rng)
        x = rng.standard_normal(n_in)
        t = rng.standard_normal(n_out)
        dW_true, _ = true_grad(x, t, W, V)
        descent_true = -dW_true            # backprop descent direction
        # draw a big pool of single-shot estimates
        pool = np.stack([node_perturbation_sample(x, t, W, V, sigma)
                         for _ in range(max(batches))])
        single.append(cosine(pool[0], descent_true))
        for b in batches:
            avg = pool[:b].mean(axis=0)
            out[b].append(cosine(avg, descent_true))
    res = {b: float(np.mean(out[b])) for b in batches}
    return float(np.mean(single)), res

if __name__ == "__main__":
    # 0) finite-difference sanity check on backprop
    rng = np.random.default_rng(0)
    W, V = net_init(8, 16, 3, rng)
    x = rng.standard_normal(8); t = rng.standard_normal(3)
    print("backprop FD-check max|err| on W:", fd_check(x, t, W, V))
    print()

    # 1) unbiasedness + variance: averaged cosine should climb toward 1 with more samples
    print("Three-factor (node-perturbation) update vs true backprop gradient")
    print("cosine(avg of B estimates, true descent dir), mean over 4 seeds")
    print(f"{'width N':>8} | {'B=1':>7} {'B=10':>7} {'B=100':>7} {'B=1000':>7} | {'angle@B=1':>9}")
    for n_hid in (4, 16, 64, 256):
        single, res = run_width(n_hid)
        ang = np.degrees(np.arccos(np.clip(single, -1, 1)))
        print(f"{n_hid:>8} | {res[1]:7.3f} {res[10]:7.3f} {res[100]:7.3f} {res[1000]:7.3f} | {ang:8.1f}°")

    # 2) samples-to-align: how many estimates to reach cosine>=0.9 vs width
    print()
    print("samples B needed for cosine(avg,true) >= 0.9  (mean over 4 seeds)")
    for n_hid in (4, 16, 64, 256):
        needed = []
        for s in range(4):
            rng = np.random.default_rng(100 + s); np.random.seed(100 + s)
            W, V = net_init(8, n_hid, 3, rng)
            x = rng.standard_normal(8); t = rng.standard_normal(3)
            descent_true = -true_grad(x, t, W, V)[0]
            acc = np.zeros_like(W); b = 0; hit = None
            for k in range(1, 20001):
                acc += node_perturbation_sample(x, t, W, V, 1e-3); b += 1
                if cosine(acc, descent_true) >= 0.9:
                    hit = b; break
            needed.append(hit if hit else 20000)
        print(f"  N={n_hid:>4}:  B ~ {int(np.mean(needed)):>6}   (params in W = {8*n_hid})")
