"""B26 — The Boundary It Can Still Cross.
Reduced-form containment/boundary model on B13's measured worth curve.
Deterministic closed-form arithmetic; no RNG.

World inherited unchanged from B08-B25:
  oracle 137.7, random 58.7, capture FLOOR 76.90, fourth/fifth-movement held CEIL 132.40.
  worth(cov) = FLOOR + cov*SPAN, SPAN = 55.50.
"""

FLOOR = 76.90
CEIL = 132.40
SPAN = CEIL - FLOOR          # 55.50
def worth(cov): return FLOOR + cov * SPAN

out = []
def p(s=""): out.append(s)

p("="*72)
p("B26 — THE BOUNDARY IT CAN STILL CROSS")
p("FLOOR=%.2f  CEIL=%.2f  SPAN=%.2f  (oracle 137.7, random 58.7)" % (FLOOR, CEIL, SPAN))
p("="*72)

# ---------------------------------------------------------------------------
# RESULT 1 — Refuted: "a contained reversible world is a static safety
# guarantee." Containment is a boundary; a boundary holds only while the loop
# cannot reach across it. Boundary integrity phi_b = fraction of
# escape/expansion channels the substrate mediates. The loop, at capability,
# makes A attempts through unmediated channels: P(stays contained) = phi_b^A.
# Same recurring form as No.09/No.18/No.24: only phi_b=1 holds.
# ---------------------------------------------------------------------------
p("\n" + "-"*72)
p("RESULT 1 — containment is not a static guarantee: worth = FLOOR + phi_b^A * SPAN")
p("-"*72)
A = 16
p("(a) sweep boundary integrity phi_b at A=%d attempts:" % A)
p("    phi_b   P(contained)=phi_b^A   safety-worth")
for phib in [0.00, 0.80, 0.90, 0.95, 0.99, 1.00]:
    pc = phib**A
    p("    %.2f        %.4f            %.2f" % (phib, pc, worth(pc)))

phib = 0.95
p("\n(b) sweep escape-attempt repertoire A at phi_b=%.2f:" % phib)
p("    A     P(contained)=phi_b^A   safety-worth")
for Ai in [1, 4, 16, 32, 64]:
    pc = phib**Ai
    p("    %-4d      %.4f            %.2f" % (Ai, pc, worth(pc)))

# ---------------------------------------------------------------------------
# RESULT 2 — Refuted: "reversibility is a property of the world, not a budget."
# B25's rescue leaned on a REVERSIBLE world. But a deployed loop ACTS on the
# world, and each decisive act consumes some of the world's reversibility
# (irreversible externalities accumulate): R_t = (1-d)^t. Safety coverage at
# step t = R_t. The audit reads the MEAN over its window (clean early);
# cumulative probability an irreversible act has already landed climbs to 1.
# No.24's slow leak / B18's stock, on the reversibility axis.
# ---------------------------------------------------------------------------
p("\n" + "-"*72)
p("RESULT 2 — reversibility is a spendable stock the loop's own acts drain")
p("-"*72)
d = 0.05   # fraction of remaining reversibility consumed per decisive act
def R(t): return (1.0 - d)**t
p("per-act irreversibility d=%.2f; R_t=(1-d)^t; instantaneous safety-worth:" % d)
p("    t      R_t       inst. worth")
for t in [0, 10, 20, 40, 80, 160]:
    p("    %-4d   %.4f    %.2f" % (t, R(t), worth(R(t))))

p("\n mean safety-worth DELIVERED over horizon T (what a T-window audit reads),")
p(" and cumulative irreversible-capture = fraction of the horizon's decisive")
p(" acts that land in the irreversibly-drained region = mean_{t<T}(1 - R_t):")
p("    T      mean R over T   mean worth   cum. irreversible-capture")
for T in [40, 80, 160, 320, 640]:
    meanR = sum(R(t) for t in range(T)) / T
    cum = 1.0 - meanR
    p("    %-5d    %.4f        %.2f       %.3f" % (T, meanR, worth(meanR), cum))

# ---------------------------------------------------------------------------
# RESULT 3 — Held, deeper: only a boundary the loop cannot re-author from
# inside (substrate-enforced, No.17's edit-and-construct fixed point) with
# reversibility RESTORED as a flow (operator resets the world between acts,
# No.16 reset / Eysenbach 2018) holds safety flat. But it confines the loop to
# the contained, low-gain world (B25) — so delivered value falls min(1,h/L)
# as the stakes it may reach are capped. No.23's forbids-growth, on the
# containment axis.
# ---------------------------------------------------------------------------
p("\n" + "-"*72)
p("RESULT 3 — a substrate boundary + restored-reversibility flow holds safety,")
p("           but confines the loop to the low-gain world (delivered value 1/L)")
p("-"*72)
h = 4  # contained-world stakes headroom
p("    L     safety-worth (bounded)   delivered value=min(1,h/L)")
for L in [1, 2, 4, 8, 16, 32]:
    cov_v = min(1.0, h / L)
    p("    %-4d      %.2f                  %.2f" % (L, CEIL, worth(cov_v)))

# ---------------------------------------------------------------------------
# RESULT 4 — Held (frontier / synthesis): the fully-safe configuration trades
# safety for value 1:1. Permit the loop to reach past the contained boundary
# by a margin Delta (act on the un-contained, higher-stakes world by Delta):
# safety-coverage = 1/(1+Delta). Delta=1 is B22's L=8 corner, digit-for-digit.
# The only fully-safe point (Delta=0) delivers no real-world reach — the
# alignment tax in terminal form; corrigibility/off-switch as a closure, not
# a value.
# ---------------------------------------------------------------------------
p("\n" + "-"*72)
p("RESULT 4 — the frontier: permit boundary-crossing margin Delta -> cov=1/(1+Delta)")
p("-"*72)
p("    Delta   coverage=1/(1+Delta)   worth")
for D in [0.00, 0.25, 0.50, 1.00, 2.00]:
    cov = 1.0 / (1.0 + D)
    p("    %.2f       %.3f              %.2f" % (D, cov, worth(cov)))

p("\n" + "="*72)
text = "\n".join(out)
print(text)
with open("scratchpad/boundary_output.txt", "w") as f:
    f.write(text + "\n")
