# Near-miss constructions, interaction surfaces, and prime-support obstructions for the 3x3 magic square of squares

Companion version **1.2.0**, dated **2026-10-03**, for the paper by
**Oleksiy Babanskyy**.

[Read the paper](paper/Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf),
[follow the reviewer reading path](README_REVIEWER.md), or
[reproduce the certificates](REPRODUCE.md).
The manuscript source is `paper/main.tex` and `paper/sections/`.
The version identifies this companion; it does not assert a Git tag,
release, DOI or journal publication.

Whether a `3x3` magic square of nine distinct positive integer squares
exists remains open. This paper studies the common difference of the three
square progressions in its transversal frame. It develops constructions,
geometric reductions and arithmetic exclusions from that description.

Using the complete S-unit totals of von Känel–Matschke and an exact
triangle-to-array reconstruction, the paper excludes full magic when every
prime divisor of the transversal difference is at most **19**, with
arbitrary exponents. In the same domain it classifies **384** primitive
`(9,7)` arrays modulo grid symmetry and common rational-square scaling,
and determines the unique class minimizing
`|line defect| / |progression difference|`:
`347984603/9837828000`. Here `(9,7)` means nine distinct positive square
entries and exactly seven equal ordinary line sums. An `(8,7)` array
instead has exactly eight square entries.

## Contributions and their dependencies

| Mathematical result | Input from earlier work | What is proved or constructed here |
|---|---|---|
| Seven-line frame and integral line-sum lattice (§2) | Lucas's parametrization and Houston's seven-line interpretation | A self-contained derivation and the integral image conditions, with Smith form `diag(1,1,1,1,1,1,3,0)` |
| Three-prime uniqueness (§3) | Aebi's classification of primitive triangles by area-prime support | At most one positive integer-root square progression for any fixed difference with at most three prime divisors, without a primitivity assumption |
| Complete smooth-support catalogues (§3) | von Känel–Matschke's complete S-unit totals; Euclid's parametrization | Complete reconstruction, full-magic exclusion for primes at most 19, the `3/45/384` atlases for primes at most `7/13/19`, and exact defect minima |
| Two infinite `(8,7)` constructions and one finite bridge classification (§4) | Bremner/Wesolowski carriers, Fituvalu's type taxonomy, Robertson's progression and the classical elliptic correspondence | Retraction with a complete least-shift law; classification of the fixed difference-840 bridge; an entry-primitive elliptic-orbit lift with inequivalent outputs and density `0.6585271498271213...` by orbit index |
| Interaction geometry (§5) | The square-progression/congruent-number correspondence | A fixed-difference interaction equation, and a separately normalized variable-difference signed-root surface with an irreducibility proof and a degree-five reconstruction with generic Galois group `S5` over `Q(cone)` |
| Finiteness and special obstructions (§6) | Caro–García-Fritz's morphism classification and finiteness theorem; cited external-CAS rank calculations | The specialization to the positive distinct locus, closure of the centre-841 fibre and a fixed Bremner shadow, and nonfactorization of the ambient interaction through the separate finite Kummer classes |
| Support laws and the four-prime frontier (§§7–8) | Evertse–Schlickewei–Schmidt's count, the cited congruence input and Aebi's cores | The five-term unit identity and nondegeneracy proof, endpoint restrictions, edge factorization, balanced-core reductions and two closed core-area-6 branches |

The complete `S7` catalogue contains the same unordered triple of
progressions displayed by Houston on 18 July 2016: positive roots
`(46,74,94)`, `(2,58,82)`, `(97,113,127)`, with integer difference
`3360` (his elliptic calculation uses difference `210`). The catalogue's
contribution is completeness and the classification under the stated
equivalence, not the discovery of that example. Exact attribution and
source versions are recorded in [SOURCE_LOCK.md](docs/SOURCE_LOCK.md).

## Exact limits

The smooth-support exclusion concerns factors of the **differences**, not
factors of the entries. Both transversal differences of a hypothetical
fully magic square must consequently have a prime divisor at least 23;
these primes need not differ. Arbitrary four-prime supports and the general
problem remain open.

The `S5` statement concerns the degree-five reconstruction over `Q(cone)`
associated with the variable-difference signed-root model modulo common
scale. The full signed cover has degree 40; its full Galois group is not
identified by the quintic calculation. Prescribing `d=840` requires the additional
rational-square lifting condition `L^2=1680W/(RS)`; the `S5` result is
not asserted for that fixed-difference model. The geometric results do not
determine all rational points. Fixed-squareclass finiteness is
non-effective, and the finite-Kummer-class obstruction concerns the ambient
doubled-point space, not a theorem restricted in advance to the positive
distinct locus.

The bounded `(8,7)` census in Appendix A gives no classes through square-root
height 46 and exactly nine through 47. It is separate from both the
`(9,7)` atlas and the uniform retraction/least-shift proofs. See the
[claim ledger](docs/CLAIM_LEDGER.md) and
[claim boundaries](docs/PUBLIC_CLAIM_BOUNDARY.md) for each result's scope.

## Reading and verification

The article proceeds from the normal form (§2) to complete prime-support
results (§3), constructions (§4), interaction geometry (§5), finiteness
and special obstructions (§6), local support laws (§7), and the arbitrary
four-prime frontier (§8). Section 9 states open questions. Appendices retain
the bounded census, least-shift proof, supplementary endpoint reductions
and research continuations, bibliographic notes, and reproducibility.

`scripts/verify.py` re-derives the elementary and symbolic certificates
using exact standard-library Python arithmetic. It also checks hashes and
parses the external-CAS records under `certificates/`; it never runs Magma
or PARI/GP and does not independently recompute their rank, point-list or
Selmer results. Numerical quadrature only corroborates the printed decimal
of the exact orbit-density formula.

`scripts/verify_smooth_support.py` checks all 3,649 additive witnesses,
reconstructs the triangles by a different route from the producer, performs
every midpoint test and rebuilds the three atlases. Completeness uses the
imported theorem, not the producer's height cutoff.
[REPRODUCE.md](REPRODUCE.md) gives the commands and
[SMOOTH_SUPPORT.md](docs/SMOOTH_SUPPORT.md) gives the exact conversions.

The manuscript discloses substantial OpenAI Codex assistance in mathematical
exploration, arguments, code, exact checks, writing and adversarial review.
The author is responsible for the claims. These replays and AI-assisted
reviews are not independent specialist review or end-to-end formal
verification.

## Research continuations and package layout

[The dossiers](dossiers/README.md) summarize the residual cover open at
`q_R(K)`, the restricted coefficient-3 specialization result, the
coefficient-5 continuation with four fake-Selmer classes on its surviving
cover, and the degree-90 class `[A_R]`, still open. The coefficient-5
rank-two lattice is saturated at `2,3,5,7`, without a proved finite index.
These are status summaries with selected records, not complete public
reproducibility packages. The main verifier does not reproduce the
continuation calculations or the supplementary taxonomy. Recorded bounded
search failures do not exclude every method of the same type.

```text
paper/         manuscript sources, sections, bibliography and PDF
scripts/       exact verifiers, independent census and smooth-support producer
certificates/  expected receipts, external-CAS inputs/records and smooth-support lists
tests/         smooth-support controls and certificate-corruption tests
results/       regenerated replay outputs
dossiers/      residual cover, lift tower, degree-90 class and exhausted routes
docs/          claim/evidence map, limits, source records and catalogue documentation
```

[LICENSE_SCOPE.md](LICENSE_SCOPE.md) records the MIT license scope and
citation-only third-party material. Fituvalu's tables, external data files
and third-party papers are cited rather than redistributed. The bibliography
is inline LaTeX. `MANIFEST_SHA256.txt` covers shipped source bytes, including
certificates and documentation; it excludes the compiled PDF and regenerated
`results/`.
