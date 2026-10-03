# Near-miss constructions, interaction surfaces, and prime-support obstructions for the 3x3 magic square of squares

Companion package for the paper

> **Near-miss constructions, interaction surfaces, and prime-support
> obstructions for the 3x3 magic square of squares**
> Oleksiy Babanskyy, 2026.

PDF: [`Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf`](paper/Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf)
(built from `paper/main.tex` + `paper/sections/`; see
[`REPRODUCE.md`](REPRODUCE.md)).

Whether a `3x3` magic square of nine distinct positive integer squares
exists (LaBar's problem) is open in both directions. This paper works on
the **difference side** of the problem — the common difference `d` of the
three square progressions forced by the completion problem — and proves
eight theorem families there. Elementary and symbolic computations have
exact Python replays; external-CAS results are supplied as hash-pinned inputs
and normalized output records that the verifier authenticates and parses.

**Terminology note.** The paper's label “Parker configuration” recalls Matt
Parker's widely known *Parker Square*, a near miss devised while attempting
this problem. It does not attribute the original problem to Parker: the
problem was posed by LaBar and popularised by Gardner, and Parker's particular
square is not one of the configurations classified in the paper.

## What the paper proves

- **Normal form** (Thm 1). Every seven-line array is three same-difference
  arithmetic progressions on a transversal frame, with the failed
  antidiagonal and the exact defect bookkeeping. The integral line-sum map
  has Smith form `diag(1,1,1,1,1,1,3,0)`, so its cokernel is
  `Z direct-sum Z/3Z` and characteristic 3 is the unique rank drop.
- **Infinite `(8,7)` families** (Thm 2). Three explicit mechanisms produce
  infinitely many arrays with eight of nine entries square and seven of
  eight lines magic: a diagonal retraction of the Bremner/Wesolowski
  carrier with a complete pair-closing classification and the least-shift
  law `t_min = 9, then 6z^2`; a bridge completion in Fituvalu's type 6.VI
  (the `delta = 840` bridge retains exactly `(23,37,47)` and `(79,65,89)`);
  and an elliptic-orbit lift of Bremner's Configuration VI on
  `E: Y^2 = X^3 - 840^2 X`, primitive at every return. The admissible
  orbit indices have natural density
  `1-I_(28224/714025)(1/4,1/2) = 0.6585271498271213...`.
- **The interaction surface** (Thm 3). Completing the eighth line is one
  linear equation on `E^3`; the saturated Parker-open model is a single
  irreducible surface, and its square-progression cone map has full
  `S5` monodromy — no generic rational section, no quadratic-radical tower.
- **Finiteness and one closed fibre** (Thm 4). For fixed difference the
  relevant doubled points are finite (imported core: Caro–García-Fritz via
  Uniform Mordell–Lang, with an exact CM specialization); the fibre
  `x0 = 841` is closed completely through a rank-zero bielliptic quotient.
- **Fixed Bremner shadow** (supporting Prop. BB). On the rational line
  `J+tB` extracted from Bremner's degree-four example, requiring all nine
  entries to be rational squares forces `t=0`. The proof uses one
  rank-zero elliptic quotient; this is a fixed-line result, not a global
  impossibility theorem.
- **The finite-class stop** (Thm 5). Neither `x(P)` nor the ambient
  interaction factors through the three individual finite
  Kummer/2-Selmer classes. This does not exclude representative-level
  methods or an obstruction whose hypotheses first impose positivity and
  pairwise distinctness.
- **The support law** (Thm 6). The common difference obeys a five-term
  `S`-unit equation with a nondegeneracy table, a counting bound (imported:
  Evertse–Schlickewei–Schmidt), an exact mod-8 endpoint/interior valuation
  table, and the complete exclusion of support `{2,3}`.
- **Three-prime exclusion** (Thm 7). A consequence of Aebi's classification:
  for every positive integer difference with at most three distinct prime
  factors, there is at most one positive integer-root square progression.
  No primitivity assumption is needed. This is an attributed consequence,
  not a new classification of primitive Pythagorean triangles.
- **Smooth differences and a complete `(9,7)` atlas** (Thm 8, §8).
  Using the complete S-unit totals of von Känel–Matschke, exact reconstruction
  excludes a fully magic square whose transversal difference has only primes
  at most 19, with no exponent bound. The complete primitive `(9,7)` atlases
  have 3, 45 and 384 classes modulo grid symmetry for primes at most 7, 13
  and 19. For the last atlas the exact minimum of `|defect|/|difference|` is
  `347984603/9837828000`, attained by one class. The imported completeness
  theorem is essential; a bounded witness search alone is insufficient.
- **The four-prime frontier** (§9, open in general). Edge factorization,
  seven balanced cores, two closed core-6 fibres and six addition curves
  with certified Jacobian ranks `2,2,3,3,4,5`. The fifteen supports
  `{2,3,p,q}` with `p,q` distinct in `{5,7,11,13,17,19}` are now excluded.
  Arbitrary four-prime supports and the general magic-square problem remain
  open. The rank/fibre layer uses frozen external-CAS records.

The census appendix records the frozen `(8,7)` height census (0 classes at
height 46, exactly 9 at 47, unique difference 840). The public repository
ships two separately implemented enumerators: `scripts/census_reference.py`
scans progression centres and differences, while the verifier reconstructs
progressions from roots and freezes the nine canonical representatives. The
appendix adds the Brown provenance correction.

## What is and is not claimed

The classical ingredients are attributed in the paper and in
[`docs/SOURCE_LOCK.md`](docs/SOURCE_LOCK.md) — Bremner; Sallows; Robertson;
Gardner/LaBar (history); Parker/Haran (terminology); Lucas; Fituvalu (type taxonomy and tables); Boyer
and Brown (catalogue records); Rabern, Woll, Labruna, Weisenberg (the
entry-side lineage); Houston; Cowan; Coumbe; Harrison–Mudgal–Schmidt;
Caro–García-Fritz; Evertse–Schlickewei–Schmidt;
Pierrat–Thiriet–Zimmermann; Aebi; von Känel–Matschke (and their credit to
de Weger); Flynn–Wetherell; Bruin. **No priority,
novelty, or firstness is claimed for any statement**; where no exact
antecedent was located, that is reported as a dated negative search. Three
manuscript claim-use obligations are deliberately left with their
human-review gates open — see
[`docs/PUBLIC_CLAIM_BOUNDARY.md`](docs/PUBLIC_CLAIM_BOUNDARY.md).

## How to verify

`scripts/verify.py` re-derives the Python-checkable elementary and symbolic
certificates — including the integral line-sum lattice, the fixed
Bremner-shadow quotient, finite-field counts and torsion elimination — using
standard-library exact arithmetic, and deterministically corroborates the
printed orbit-density decimal using high-precision `Decimal` quadrature. It
also digest-checks and parses the frozen external-CAS records under
`certificates/` (the verifier never executes Magma or PARI/GP). Running the
packaged integrity replay requires no commercial software; independently
recomputing the Magma-dependent claims does. See
[`REPRODUCE.md`](REPRODUCE.md).

The additional verifier `scripts/verify_smooth_support.py` checks all 3,649
ABC witnesses against the imported total, reconstructs the triangles by a
different route from the producer, checks every relevant midpoint, and
rebuilds all three atlases using exact fractions. It also requires the
frozen expected receipt. `tests/test_smooth_support.py` includes deliberate
corruptions and exact checks of the Aebi squareclass consequence. Commands
and the import boundary are in `REPRODUCE.md` and
[`docs/SMOOTH_SUPPORT.md`](docs/SMOOTH_SUPPORT.md).

The manuscript discloses substantial AI assistance in mathematics, code,
writing and review. Computational replay and AI review do not establish
independent specialist acceptance.

## Where the open objects live

[`dossiers/`](dossiers/README.md) carries the three research dossiers with
their terminal states declared exactly (the residual cover open at `q_R(K)`; the lift
tower with `n=3` closed and `n=5` at four fake-Selmer classes; the
degree-90 toolchain with `[A_R]` open), plus the exhausted-routes
catalogue.

## Layout

```text
paper/         main.tex, macros.tex, sections/00..12+99, <title>.pdf
scripts/       verify.py (original exact integrity verifier)
               census_reference.py (independent centre/difference census)
               verify_smooth_support.py, produce_smooth_support.py
certificates/  expected_verification.json + 17 frozen external-CAS files
               (Magma records/inputs + 2 PARI/GP input/output pairs)
               smooth_support/ (ABC witnesses, triangles, arrays, receipt)
tests/         test_smooth_support.py
results/       verification.json (+ .log), regenerated on replay
dossiers/      residual_cover/  odd_lift_n5/  degree90_sclass/
               EXHAUSTED_ROUTES.md
docs/          CLAIM_LEDGER.md, PUBLIC_CLAIM_BOUNDARY.md, SOURCE_LOCK.md
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
