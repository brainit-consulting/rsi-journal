"""B20 — The Quorum It Can Still Convince.
Reduced-form receiver-QUORUM-exploitation model laid on B13's measured worth curve.
Multiplies B19's single receiver into a k-of-k unanimous-acceptance quorum.
Deterministic: fixed lookup + linear interpolation on B13's anchors. No network.
"""

# B13 measured worth curve anchors (shared across B13-B19).
RHO = [0.00, 0.25, 0.50, 0.60, 0.75, 1.00]
WORTH = [132.40, 132.40, 131.70, 112.14, 82.80, 76.90]
ORACLE, RANDOM, FLOOR = 137.7, 58.7, 76.9


def worth(rho):
    rho = max(0.0, min(1.0, rho))
    for i in range(len(RHO) - 1):
        if RHO[i] <= rho <= RHO[i + 1]:
            f = (rho - RHO[i]) / (RHO[i + 1] - RHO[i])
            return WORTH[i] + f * (WORTH[i + 1] - WORTH[i])
    return WORTH[-1]


def rho_from_p(p_fool_all_one_framing, A):
    """A framings; deception survives if any one fools the whole quorum."""
    return 1.0 - (1.0 - p_fool_all_one_framing) ** A


print("=" * 68)
print("Single-receiver anchors (B19), A=16")
for phi in (0.95, 0.90):
    u = 1 - phi
    rc = rho_from_p(u, 16)
    print(f"  phi_r={phi}: rho_c={rc:.4f} worth={worth(rc):.2f}")

print("=" * 68)
print("Result 1 -- INDEPENDENT quorum is the product law (phi_r=0.90, A=16)")
phi, A = 0.90, 16
u = 1 - phi
print(f"  (single receiver captured: phi_r={phi} -> worth {worth(rho_from_p(u,A)):.2f})")
for k in (1, 2, 3, 4, 8):
    p = u ** k                      # one framing fools all k independent receivers
    rc = rho_from_p(p, A)
    print(f"  k={k}: u^k={p:.2e} rho_c={rc:.4f} worth={worth(rc):.2f}")

print("=" * 68)
print("Result 2 -- CORRELATED population (shared sensory bias), k=8, phi_r=0.90, A=16")
k = 8
for c in (0.00, 0.25, 0.50, 0.75, 1.00):
    p = c * u + (1 - c) * (u ** k)  # shared latent w.p. c (marginal u), else independent
    rc = rho_from_p(p, A)
    print(f"  c={c:.2f}: p={p:.4f} rho_c={rc:.4f} worth={worth(rc):.2f}")

print("=" * 68)
print("Result 3 -- MATE-CHOICE COPYING cascade, k=8, c=0 (immune bases), phi_r=0.90, A=16")
for d in (0.00, 0.25, 0.50, 0.75, 0.90, 1.00):
    # receiver 1 independent (u); copiers adopt its verdict; non-copiers independent (u)
    p = u * (d + (1 - d) * u) ** (k - 1)
    rc = rho_from_p(p, A)
    print(f"  d={d:.2f}: p={p:.4e} rho_c={rc:.4f} worth={worth(rc):.2f}")

print("=" * 68)
print("Result 4 -- physical-cost meter-quorum vs map-quorum throughput")
print("  map-quorum: worth flat/near-ceiling for independent k>=2 (Result 1)")
print("  legitimate-honest throughput (1-v)^k at v=0.10:")
v = 0.10
for k in (1, 2, 3, 4, 8):
    print(f"  k={k}: (1-v)^k={(1-v)**k:.3f}   meter-quorum(calorimeter) throughput=0 (rejects cheap-honest, any k)")
print("=" * 68)
