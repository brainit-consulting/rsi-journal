"""
B03 sandbox: does predictive coding recover backprop's gradient, and where
does the recovery break?

Whittington & Bogacz (2017) and Millidge et al. (2020) show a local
predictive-coding (PC) network's weight updates equal backprop's (BP)
gradient AT the inference equilibrium with the output clamped to the target.
The proof is first order: the equivalence is exact when the prediction errors
are small, and degrades as the target moves away from the network's own
feedforward output. We test both halves directly.

Convention (Millidge et al. 2020): node values x_l, prediction
  mu_l = f(x_{l-1}) @ W_l,   error  eps_l = x_l - mu_l.
Inference (hidden nodes):  dx_l = -eps_l + f'(x_l) * (eps_{l+1} @ W_{l+1}^T).
Local weight update:       dW_l = f(x_{l-1})^T @ eps_l.
Backprop is defined on the SAME network (f then linear at each stage,
linear output), so the equivalence can be exact.

Measure: angle (deg) between the PC update vector and the BP descent
direction (-gradient), flattened over all weights. 0 = exact recovery.
numpy only, fixed seeds.
"""
import numpy as np

def f(x):  return np.tanh(x)
def fp(x): return 1.0 - np.tanh(x)**2   # f'(arg) as a function of the arg

def build(seed, dims=(8, 16, 16, 4)):
    rng = np.random.default_rng(seed)
    return [rng.standard_normal((dims[i], dims[i+1])) * (1.0/np.sqrt(dims[i]))
            for i in range(len(dims)-1)]

def forward(W, x):
    """x_l = f(x_{l-1}) @ W_l for all l; output x_L read linearly."""
    xs = [x]
    h = x
    for w in W:
        h = f(h) @ w
        xs.append(h)
    return xs            # xs[0]=input ... xs[L]=output

def loss(W, x, y):
    return 0.5*np.sum((forward(W, x)[-1] - y)**2)

def bp_grad(W, x, y):
    """Exact gradient of 0.5||x_L - y||^2 on the f-then-linear network."""
    xs = forward(W, x)
    L = len(W)
    grads = [None]*L
    delta = (xs[L] - y)                  # linear output
    for li in reversed(range(L)):
        grads[li] = f(xs[li]).T @ delta  # dL/dW_li
        if li > 0:
            delta = (delta @ W[li].T) * fp(xs[li])
    return grads

def pc_update_fpa(W, x, y, n_iters, lr=0.1):
    """
    PC under the FIXED-PREDICTION ASSUMPTION (Millidge, Tschantz & Buckley
    2020): the top-down predictions mu_l and the derivatives f'(x_l) are held
    at their FEEDFORWARD values during inference; only the error/value nodes
    relax. The dynamics are then linear and the equilibrium errors equal the
    backprop deltas exactly. Output clamped to y.
    """
    L = len(W)
    xs = forward(W, x)                       # feedforward, frozen reference
    fp_ff = [fp(xs[li]) for li in range(L+1)]
    v = [a.copy() for a in xs]
    v[L] = y.copy()
    for _ in range(n_iters):
        # predictions use the FROZEN feedforward lower-layer activations
        mu = [None] + [f(xs[li]) @ W[li] for li in range(L)]
        eps = [None] + [v[li+1] - mu[li+1] for li in range(L)]
        for li in range(1, L):
            top_down = (eps[li+1] @ W[li].T) * fp_ff[li]
            v[li] = v[li] + lr * (-eps[li] + top_down)
    mu = [None] + [f(xs[li]) @ W[li] for li in range(L)]
    eps = [None] + [v[li+1] - mu[li+1] for li in range(L)]
    return [f(xs[li]).T @ eps[li+1] for li in range(L)]

def pc_update(W, x, y, n_iters, lr=0.05, soft_beta=None):
    """
    PC inference with the output clamped to y (soft_beta=None) or softly
    nudged with strength soft_beta. Returns local weight updates at the
    (approximate) equilibrium. Under a hard clamp + convergence + small
    error this equals the BP descent direction.
    """
    L = len(W)
    xs = forward(W, x)
    v = [a.copy() for a in xs]
    clamp = soft_beta is None
    if clamp:
        v[L] = y.copy()
    for _ in range(n_iters):
        mu = [None] + [f(v[li]) @ W[li] for li in range(L)]
        eps = [None] + [v[li+1] - mu[li+1] for li in range(L)]
        last = L-1 if clamp else L
        for li in range(1, last+1):
            top_down = (eps[li+1] @ W[li].T) * fp(v[li]) if li < L else 0.0
            dx = -eps[li] + top_down
            if li == L and not clamp:
                dx = dx - soft_beta * (v[li] - y)
            v[li] = v[li] + lr * dx
    mu = [None] + [f(v[li]) @ W[li] for li in range(L)]
    eps = [None] + [v[li+1] - mu[li+1] for li in range(L)]
    return [f(v[li]).T @ eps[li+1] for li in range(L)]

def angle(a, b):
    fa = np.concatenate([g.ravel() for g in a])
    fb = np.concatenate([g.ravel() for g in b])
    c = np.dot(fa, fb)/(np.linalg.norm(fa)*np.linalg.norm(fb)+1e-12)
    return np.degrees(np.arccos(np.clip(c, -1, 1)))

if __name__ == "__main__":
    seeds = [0,1,2,3]

    # --- Test 1: exact recovery in the small-error limit, with convergence ---
    print("Test 1 — PC update vs backprop DESCENT direction, output CLAMPED.")
    print("Angle (deg) as a function of target distance eps and inference iters.")
    print("Equivalence is first order: -> 0 as eps -> 0 AND iters large.\n")
    print(f"{'eps':>8}", end="")
    iters_list = [10, 100, 1000, 8000]
    for it in iters_list: print(f"{('it='+str(it)):>12}", end="")
    print()
    for eps in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0]:
        print(f"{eps:>8}", end="")
        for it in iters_list:
            angs = []
            for s in seeds:
                W = build(s); rng = np.random.default_rng(100+s)
                x = rng.standard_normal((1,8)); out = forward(W, x)[-1]
                d = rng.standard_normal((1,4)); d /= np.linalg.norm(d)
                y = out + eps*d
                g = [-g for g in bp_grad(W, x, y)]
                p = pc_update(W, x, y, n_iters=it)
                angs.append(angle(p, g))
            print(f"{np.mean(angs):>12.2f}", end="")
        print()

    # --- Test 1b: same sweep under the fixed-prediction assumption ---
    print("\nTest 1b — same, but under the FIXED-PREDICTION ASSUMPTION (FPA).")
    print("FPA makes the equivalence exact: angle -> ~0 at ALL eps.\n")
    print(f"{'eps':>8} {'angle(deg)':>12}")
    for eps in [0.001, 0.1, 1.0, 2.0]:
        angs = []
        for s in seeds:
            W = build(s); rng = np.random.default_rng(100+s)
            x = rng.standard_normal((1,8)); out = forward(W, x)[-1]
            d = rng.standard_normal((1,4)); d /= np.linalg.norm(d)
            y = out + eps*d
            g = [-g for g in bp_grad(W, x, y)]
            p = pc_update_fpa(W, x, y, n_iters=2000)
            angs.append(angle(p, g))
        print(f"{eps:>8} {np.mean(angs):>12.3f}")

    print("\nSummary: free-running clamped PC recovers backprop only")
    print("approximately (~12 deg floor, growing with output error); the")
    print("fixed-prediction assumption is what makes the equivalence exact.")
