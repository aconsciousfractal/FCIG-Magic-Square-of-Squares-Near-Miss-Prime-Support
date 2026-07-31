# Near-miss constructions, interaction surfaces, and prime-support obstructions for the 3x3 magic square of squares

Companion package for the paper

> **Near-miss constructions, interaction surfaces, and prime-support
> obstructions for the 3x3 magic square of squares**
> Oleksiy Babanskyy, 2026.

PDF: [`paper/`](paper/) (title-named, built from `paper/main.tex` +
`paper/sections/`; see [`REPRODUCE.md`](REPRODUCE.md)).

Whether a `3x3` magic square of nine distinct positive integer squares
exists (LaBar's problem) is open in both directions. This paper works on
the **difference side** of the problem — the common difference `d` of the
three square progressions forced by the completion problem — and proves
seven theorem families there, with every computation shipped as an exact
machine-checkable certificate.

## What the paper proves

- **Normal form** (Thm 1). Every seven-line array is three same-difference
  arithmetic progressions on a transversal frame, with the failed
  antidiagonal and the exact defect bookkeeping.
- **Infinite `(8,7)` families** (Thm 2). Three explicit mechanisms produce
  infinitely many arrays with eight of nine entries square and seven of
  eight lines magic: a diagonal retraction of the Bremner/Wesolowski
  carrier with a complete pair-closing classification and the least-shift
  law `t_min = 9, then 6z^2`; a bridge completion in Fituvalu's type 6.VI
  (the `delta = 840` bridge retains exactly `(23,37,47)` and `(79,65,89)`);
  and an elliptic-orbit lift of Bremner's Configuration VI on
  `E: Y^2 = X^3 - 840^2 X`, primitive at every return.
- **The interaction surface** (Thm 3). Completing the eighth line is one
  linear equation on `E^3`; the saturated Parker-open model is a single
  irreducible surface, and its square-progression cone map has full
  `S5` monodromy — no generic rational section, no quadratic-radical tower.
- **Finiteness and one closed fibre** (Thm 4). For fixed difference the
  relevant doubled points are finite (imported core: Caro–García-Fritz via
  Uniform Mordell–Lang, with an exact CM specialization); the fibre
  `x0 = 841` is closed completely through a rank-zero bielliptic quotient.
- **The finite-class stop** (Thm 5). Neither `x(P)` nor the interaction
  ever factors through the finite Kummer/2-Selmer class triples: pure
  finite class obstructions cannot decide the completion problem.
- **The support law** (Thm 6). The common difference obeys a five-term
  `S`-unit equation with a nondegeneracy table, a counting bound (imported:
  Evertse–Schlickewei–Schmidt), an exact mod-8 endpoint/interior valuation
  table, and the complete exclusion of support `{2,3}`.
- **Three-prime exclusion** (Thm 7). No primitive positive configuration
  has `supp(2d) = {2,3,p}` for any prime `p != 3` — the join of the
  endpoint law with the equal-area triangle layer (that classification
  layer is Aebi's). Both fibre closures above and the rank layer of §8 are
  computer-assisted through the frozen transcripts.
- **The four-prime frontier** (§8, open). Edge factorization, two
  anti-overreach fixtures, seven balanced cores, two closed core-6 fibres,
  and six addition curves with proved Jacobian ranks `2,2,3,3,4,5` —
  stated exactly and **left open; no four-prime exclusion is claimed**.

The census appendix records the frozen `(8,7)` height census (0 classes at
height 46, exactly 9 at 47, unique difference 840): the verifier replays
it from scratch as a second independent enumerator and freezes the nine
canonical representatives; the appendix adds the Brown provenance
correction.

## What is and is not claimed

The classical ingredients are attributed in the paper and in
[`docs/SOURCE_LOCK.md`](docs/SOURCE_LOCK.md) — Bremner; Sallows; Robertson;
Gardner/LaBar (history); Lucas; Fituvalu (type taxonomy and tables); Boyer
and Brown (catalogue records); Rabern, Woll, Labruna, Weisenberg (the
entry-side lineage); Caro–García-Fritz; Evertse–Schlickewei–Schmidt;
Pierrat–Thiriet–Zimmermann; Aebi; Flynn–Wetherell; Bruin. **No priority,
novelty, or firstness is claimed for any statement**; where no exact
antecedent was located, that is reported as a dated negative search. Three
manuscript claim-use obligations are deliberately left with their
human-review gates open — see
[`docs/PUBLIC_CLAIM_BOUNDARY.md`](docs/PUBLIC_CLAIM_BOUNDARY.md).

## How to verify

`scripts/verify.py` re-derives the exact certificates of all seven theorem
families and the frontier — standard library only, exact integer and
rational arithmetic, ~0.1 s — and digest-checks the 13 frozen
official-Magma files under `certificates/` (the verifier never executes
that software). See [`REPRODUCE.md`](REPRODUCE.md).

## Where the open objects live

[`dossiers/`](dossiers/README.md) carries the three research dossiers with
their terminal states declared exactly (J458 open at `q_R(K)`; the lift
tower with `n=3` closed and `n=5` at four fake-Selmer classes; the
degree-90 toolchain with `[A_R]` open), plus the exhausted-routes
catalogue.

## Layout

```text
paper/         main.tex, macros.tex, sections/00..12+99, <title>.pdf
scripts/       verify.py (stdlib-only exact verifier, single entry point)
certificates/  expected_verification.json + 13 frozen Magma files
               (7 transcripts/certificates + 6 calculator inputs)
results/       verification.json (+ .log), regenerated on replay
dossiers/      J458/  PO111A_N5/  B7D_F90/  EXHAUSTED_ROUTES.md
docs/          CLAIM_LEDGER.md, PUBLIC_CLAIM_BOUNDARY.md, SOURCE_LOCK.md,
               RED_TEAM_REPORT.md, GATE_HISTORY.md
LICENSE (MIT), LICENSE_SCOPE.md, CITATION.cff, MANIFEST_SHA256.txt,
requirements.txt
```

`LICENSE_SCOPE.md` records the single-MIT license map and the
citation-only third-party boundary: **no third-party data or documents are
bundled** — Fituvalu's tables and the entry-side PDFs are referenced by
locator and digest only. The bibliography is an inline `thebibliography`
(no `bibtex` pass). `MANIFEST_SHA256.txt` pins every shipped source byte
but not the compiled PDF (TeX-toolchain-dependent) or `results/`
(regenerated on replay).
