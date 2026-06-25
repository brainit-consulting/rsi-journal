import numpy as np

rng = np.random.default_rng(7)

# --- toy task: nonlinearly-separable 2D classification (XOR-of-blobs), 8 classes-> use 3-bit parity-ish target
N, D, H1, H2, O = 4000, 20, 64, 64, 1
X = rng.standard_normal((N, D))
# target from a random 2-layer TEACHER net -> guaranteed learnable by a 2-hidden-layer student
T1 = rng.standard_normal((D, 30)); T2 = rng.standard_normal((30, 1))
logits = np.tanh(X @ T1) @ T2
y = (logits > np.median(logits)).astype(np.float64)  # balanced by construction
ntr = 3000
Xtr, ytr, Xte, yte = X[:ntr], y[:ntr], X[ntr:], y[ntr:]

def tanh(z): return np.tanh(z)
def dtanh(a): return 1.0 - a*a
def sig(z): return 1.0/(1.0+np.exp(-z))

def init():
    s = lambda a,b: rng.standard_normal((a,b)) * np.sqrt(1.0/a)
    return [s(D,H1), s(H1,H2), s(H2,O)]

def feedback_matrices():
    # fixed random feedback for FA: B2 maps output-error -> H2, B1 maps H2-error -> H1
    return [rng.standard_normal((O,H2))*0.5, rng.standard_normal((H2,H1))*0.5]

def angle(u, v):
    u, v = u.ravel(), v.ravel()
    c = (u@v)/(np.linalg.norm(u)*np.linalg.norm(v)+1e-12)
    return np.degrees(np.arccos(np.clip(c,-1,1)))

def run(mode, epochs=60, lr=0.2, bs=64, track=False):
    W = init()
    B = feedback_matrices()
    align_hist = []
    for ep in range(epochs):
        idx = rng.permutation(ntr)
        for k in range(0, ntr, bs):
            b = idx[k:k+bs]
            xb, yb = Xtr[b], ytr[b]
            a1 = tanh(xb @ W[0]); a2 = tanh(a1 @ W[1]); o = sig(a2 @ W[2])
            e = (o - yb)                                   # output error (BCE+sigmoid grad)
            # --- credit assignment to hidden layers ---
            if mode == 'bp':
                d2 = (e @ W[2].T) * dtanh(a2)
                d1 = (d2 @ W[1].T) * dtanh(a1)
            else:  # feedback alignment: use FIXED RANDOM B instead of W.T
                d2 = (e @ B[0]) * dtanh(a2)
                d1 = (d2 @ B[1]) * dtanh(a1)
            if track and k == 0:
                # what BP *would* have said for this same forward pass:
                d2_bp = (e @ W[2].T) * dtanh(a2)
                align_hist.append(angle(d2, d2_bp))
            gW2 = a2.T @ e / len(b)
            gW1 = a1.T @ d2 / len(b)
            gW0 = xb.T @ d1 / len(b)
            W[2] -= lr*gW2; W[1] -= lr*gW1; W[0] -= lr*gW0
    # eval
    a1 = tanh(Xte @ W[0]); a2 = tanh(a1 @ W[1]); o = sig(a2 @ W[2])
    acc = float(((o>0.5)==yte).mean())
    return acc, align_hist

acc_bp, _ = run('bp')
acc_fa, ah = run('fa', track=True)
# chance baseline
chance = max(float(ytr.mean()), 1.0-float(ytr.mean()))
print(f"chance            : {chance:.3f}")
print(f"backprop test acc : {acc_bp:.3f}")
print(f"feedbk-align acc  : {acc_fa:.3f}")
print(f"FA->BP angle, layer2 hidden delta (degrees), first vs last 5 epochs:")
print(f"  start (ep0)     : {ah[0]:.1f}")
print(f"  early mean(1-5) : {np.mean(ah[1:6]):.1f}")
print(f"  late  mean(-5:) : {np.mean(ah[-5:]):.1f}")
print(f"  90deg = orthogonal (no alignment); ->0 = FA agrees with backprop")
