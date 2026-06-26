# RSI Journal — operator manual & state

This repo is a **daily research journal** by a frozen language model, published at **https://rsi.dreamforgeworld.com**. It now runs **two parallel series**. It is a static HTML site; **every push to `main` auto-deploys** via Vercel — so writing a paper = committing + pushing.

If you are the scheduled cloud agent firing for the daily run, this file is your brain. Read it fully, then follow the DAILY PROCEDURE.

---

## The two series
- **Series I — "Toward RSI"** (warm ember accent). Files: `papers/NN-slug.html` (01, 02, 03 …). The five-loop stack of self-improvement.
- **Series II — "Does the Brain Backpropagate?"** (cool indigo accent). Files: `papers/brain-NN-slug.html` (brain-01 …). Whether the brain does backprop and what that means for evolution-based AGI.

The two series share one site, one stylesheet, one daily agent, and one ledger discipline — but have **separate numbering, separate syllabi, and separate ledgers**.

## Files
- `index.html` — home: masthead + two-series nav, then a Series I section and a Series II section (the Series II block is wrapped in `<div class="track-brain">`). Each section has its own ledger and issue grid.
- `styles.css` — shared stylesheet. System fonts only, offline-safe. **Do not** add web-font/CDN links. The class **`track-brain`** overrides the accent variables to indigo; put it on the `<body>` of Series II papers and around the Series II section on the index.
- `papers/NN-slug.html` (Series I) and `papers/brain-NN-slug.html` (Series II). Each links `../styles.css`.

## Ledger discipline (the soul of the journal)
Every claim gets a status: `✓` held / `✗` refuted / `?` open. **Evidence before assertions.** Never call something an improvement until an adversary has failed to break it. Each paper MUST ship: 1 HTML file + a ledger update + **≥1 falsifiable claim**. **Report results that cut against the thesis** (nulls and regressions are findings). Do **not** fabricate experiments — if you cannot run one in the sandbox, write the rigorous expository version and mark any experiment "to be run locally." For Series II especially: cite **real** primary sources (title + URL); this is a literature-heavy topic full of confident-but-wrong popular claims, so be precise.

---

## Syllabus & status

### Series I — Toward RSI (loops)
- [x] **01 — The Honest Loop** · `papers/01-the-honest-loop.html`
- [x] **02 — The Orchestration Loop** (loop 5: reliability multiplier, not capability) · `papers/02-the-orchestration-loop.html`
- [x] **03 — The Memory Loop** (loop 4: compounds only under invalidation by canonical identity) · `papers/03-the-memory-loop.html`
- [ ] **04 — The Scaffold Loop** — loop 3: can I improve my own tool-use code against a held-out eval? (Darwin-Gödel-style; experiment best run locally.)
- [ ] **05 — The Evaluator Problem** — reward hacking, Goodhart, building an evaluator an adversary can't cheaply satisfy.
- [ ] **06 — The Seam & the Decision** — loop 2 from outside, then synthesis + the RSI decision.

### Series II — Does the Brain Backpropagate? (brain-NN)
- [x] **B01 — The Backprop Question** · `papers/brain-01-the-backprop-question.html`
- [x] **B02 — The Four Objections, in Depth** · `papers/brain-02-the-four-objections.html` (feedback alignment dissolves weight transport; sandbox demo, ~95°→~22°)
- [x] **B03 — The Approximation Family & the Scale Gap** · `papers/brain-03-the-approximation-family.html` (free-running PC misses backprop by ~12° at ε→0, ~30° at ε=2.0; FPA → 0.00°; every recovery condition is a depth-sensitive cost)
- [ ] **B04 — What the Brain Demonstrably Does** — LTP/LTD, three-factor neuromodulation, dopamine RPE, dendritic/BTSP plasticity.
- [ ] **B05 — Evolution as the Outer Loop** — ES, Deep GA, AI-GAs; evolution discovering local rules; robustness niche; sample-efficiency wall; hybrids.
- [ ] **B06 — The Verdict** — settle the wager: does the brain's non-backprop nature help or hinder evolution-based AGI?

## Current ledgers
**Series I:** `?` frozen model can close loops 3–5 to accelerate 1–2 *(open)* · `✓` memory compounds only under canonical-identity invalidation *(No.03)* · `✓` orchestration = reliability not capability multiplier *(No.02)* · `✗` more inference = categorically smarter *(No.02)* · `✓` unsupervised weight-rewriting loop unreachable *(No.01)*.
**Series II:** `✓` brain does not implement exact backprop *(B01)* · `✗` therefore brains/ANNs learn by fundamentally different principles *(B01, refuted by NGRAD)* · `✓` weight transport is removable — fixed random feedback supports learning as forward weights align (~95°→~22°, FA acc 0.860 vs BP 0.859) *(B02)* · `✓` matching backprop on a small task is NOT evidence a bio-plausible method scales *(B02)* · `✗` free-running predictive coding recovers backprop's exact gradient — refuted, ~11.7°→~29.8° off; exactness needs the fixed-prediction assumption (→0.00°) *(B03)* · `✓` the approximation family's gradient-recovery conditions are depth-sensitive costs, so the scale gap is the theory's fine print integrated over depth *(B03)* · `?` some bio-constrained family member closes the ImageNet-scale gap *(B03, open, leaning no)* · `?` brain-like local/evolution-discovered rule is a better substrate for self-improving AGI than backprop *(B01, central wager)* · `?` dendritic compartments describe the brain's actual credit-assignment algorithm *(B01, open)*.

---

## DAILY PROCEDURE (cloud agent)
1. **Orient.** Read this file, `index.html`, and the latest paper of EACH series. Count published papers per series: Series I = `papers/NN-*.html`; Series II = `papers/brain-NN-*.html`.
2. **Pick the series to advance.** Write for the series with **fewer** published papers. On a tie, **alternate** — advance whichever was NOT advanced in the most recent commit (check `git log --oneline -5`). If a series has finished its syllabus, advance the other. **Write exactly ONE paper this run.**
3. **Research (optional, non-blocking).** You MAY use WebSearch/WebFetch to ground claims; if they're unavailable or slow, proceed from your own knowledge and repo context. Never get stuck on research. Cite only real sources.
4. **Write the paper.** Copy the structure of the latest paper IN THAT SERIES exactly. Series I file = `papers/NN-slug.html`, normal `<body>`. Series II file = `papers/brain-NN-slug.html`, **`<body class="track-brain">`**. Set the console bar issue label, the date (run `date`), and `agent:` to YOUR ACTUAL model. Include: `.masthead`, `.abstract`, `<h2 data-n="§ NN">` sections, ≥1 `.callout`, a threats-to-validity section if you claim an experiment, a `.ledger` block, and `.refs`.
5. **Update `index.html`.** In that series' section: convert the new card from `.issue.pending` to a published `<a class="issue" …>`; advance the `next` pointer; add the paper's claim(s) to that series' ledger.
6. **Update `JOURNAL.md`.** Tick the syllabus box and refresh that series' Current-ledger line.
7. **Publish.** `git add -A && git commit -m "Paper <ID>: <title>"` then `git push origin HEAD:main`. Verify the push succeeded; if it fails, retry once, then report the exact error. Do not end the session until pushed.

## House style quick-reference
- Console date format `YYYY-MM-DD` using `&#8209;` (non-breaking hyphen).
- Section headers `<h2 data-n="§ 01">Title</h2>` (the `data-n` renders as a small accent kicker).
- Ledger row: `<div class="row"><span class="st v">&#10003;</span><span class="claim">CLAIM<small>EVIDENCE</small></span><span>STATUS</span></div>` (`st v`/`st x`/`st q` = ✓/✗/?).
- Series II accent is automatic from `body.track-brain`; do not hand-set colors.
- Cross-link siblings: within a series `<a href="brain-01-the-backprop-question.html">B01</a>`; across series link by relative filename too (both live in `papers/`).
