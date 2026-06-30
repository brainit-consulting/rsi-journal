"""
B05 sandbox: Evolution Strategies (ES) as a gradient estimator.

Claim under test: the ES "evolutionary" update (Salimans et al. 2017) is an
UNBIASED estimator of the (Gaussian-smoothed) gradient -- and its sample cost
to reach a fixed direction quality scales with the PARAMETER DIMENSION D, the
same dimension-scaling variance tax B04 found for the scalar three-factor rule
(node perturbation, Werfel-Xie-Seung). So ES used as a *weight* optimizer
inherits the sample-efficiency wall; it does not escape it.

Two measurements at a FIXED parameter point theta:
  (A) cosine(ES estimate over P antithetic pairs, true gradient) vs dimension D,
      at a few population sizes P -> shows unbiased (P->inf) and D-scaling.
  (B) population P needed to reach cosine >= 0.5 vs D -> the cost curve.

Objective: a fixed random smooth quadratic  F(theta) = 0.5 * theta^T A theta,
A = symmetric PD, so the true gradient is exactly A theta (closed form, no
finite-difference error). ES uses ONLY scalar values F(theta +/- sigma*eps).
"""
import numpy as np

def make_problem(D, seed):
    rng = np.random.default_rng(seed)
    # random PD matrix with a controlled spectrum (not identity -> nontrivial)
    Q, _ = np.linalg.qr(rng.standard_normal((D, D)))
    spec = rng.uniform(0.5, 1.5, size=D)
    A = (Q * spec) @ Q.T
    A = 0.5 * (A + A.T)
    theta = rng.standard_normal(D)
    theta /= np.linalg.norm(theta)
    return A, theta

def true_grad(A, theta):
    return A @ theta

def es_estimate(A, theta, P, sigma, rng):
    """Antithetic ES gradient estimate from P mirrored pairs, scalar fitness only."""
    D = theta.shape[0]
    g = np.zeros(D)
    def F(x):  # scalar objective
        return 0.5 * x @ (A @ x)
    for _ in range(P):
        eps = rng.standard_normal(D)
        fp = F(theta + sigma * eps)
        fm = F(theta - sigma * eps)
        g += (fp - fm) * eps      # antithetic: (F+ - F-)/2 * eps, factor folded below
    g /= (2.0 * P * sigma)
    return g

def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30))

SIGMA = 1e-3   # small -> ES estimates the true gradient, not a heavily smoothed one
SEEDS = range(4)

print("=== (A) cosine(ES estimate, true gradient): unbiased but D-scaling ===")
print(f"{'D':>6} | {'P=1':>8} {'P=4':>8} {'P=16':>8} {'P=64':>8} {'P=256':>8}")
Ps = [1, 4, 16, 64, 256]
for D in [2, 8, 32, 128]:
    row = []
    for P in Ps:
        cs = []
        for s in SEEDS:
            A, theta = make_problem(D, s)
            g_true = true_grad(A, theta)
            rng = np.random.default_rng(1000 + s)
            g_es = es_estimate(A, theta, P, SIGMA, rng)
            cs.append(cosine(g_es, g_true))
        row.append(np.mean(cs))
    print(f"{D:>6} | " + " ".join(f"{v:>8.3f}" for v in row))

print()
print("=== (B) population P to reach mean cosine >= 0.5 vs dimension D ===")
print(f"{'D':>6} | {'P*':>8}")
for D in [2, 8, 32, 128, 512]:
    Pstar = None
    P = 1
    while P <= 20000:
        cs = []
        for s in SEEDS:
            A, theta = make_problem(D, s)
            g_true = true_grad(A, theta)
            rng = np.random.default_rng(2000 + s)
            g_es = es_estimate(A, theta, P, SIGMA, rng)
            cs.append(cosine(g_es, g_true))
        if np.mean(cs) >= 0.5:
            Pstar = P
            break
        P = int(np.ceil(P * 1.5))
    print(f"{D:>6} | {str(Pstar):>8}")
