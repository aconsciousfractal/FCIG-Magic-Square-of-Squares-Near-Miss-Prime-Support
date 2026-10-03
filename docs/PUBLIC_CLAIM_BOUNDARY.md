# Contributions and exact limits

The article develops constructions and deductions about square
progressions, their interaction and their prime support. These include
two infinite `(8,7)` constructions, a finite difference-840 bridge
classification, a geometric reduction, and the complete smooth-support
exclusion and `(9,7)` atlases. The
[claim ledger](CLAIM_LEDGER.md) identifies the contribution, imported input
and evidence for each result; [SOURCE_LOCK.md](SOURCE_LOCK.md) gives the
attribution and source versions.

The literature comparisons delimit these contributions. They do not
establish exhaustive bibliographic priority. Classical constructions,
classifications and methods retain their stated attribution.

## Prime-support results

The three-prime uniqueness result is a consequence of Aebi's
primitive-triangle classification. For every fixed positive integer
difference with at most three prime divisors, at most one positive
integer-root square progression exists; no primitivity assumption is
needed. The classification of the primitive triangles is Aebi's.

The smooth-support theorem (`main:smoothsupport`, §3) excludes full magic
when every prime divisor of the common transversal difference is at most
19, with arbitrary exponents. Each of the two transversal differences of a
hypothetical fully magic square must therefore have a prime divisor at
least 23; these primes need not differ. These statements concern the
differences, not the prime factors of the entries, and do not bound the
number of support primes.

The complete `(9,7)` atlases have 3, 45 and 384 classes for primes at most
7, 13 and 19, modulo `D4` and common rational-square scaling. Every array
has nine distinct positive square entries and exactly seven equal ordinary
line sums. The sharp `S19` defect ratio is divided by the progression
difference, not by the common sum; it is not an unrestricted near-miss
record. Houston's 18 July 2016 example already gives the unique unordered
`S7` triple of progressions with roots `(46,74,94)`, `(2,58,82)`,
`(97,113,127)` and integer difference 3360. The catalogue proves
completeness and identifies all central-role classes under the stated
equivalence.

Completeness imports von Känel–Matschke's Theorem A. The local verifier
checks all witnesses and the downstream deduction, while the original
source height bounds and computation are not independently reproduced.
The producer's `10^10` cutoff is not the completeness argument.
Fifteen specified four-prime supports are excluded; arbitrary four-prime
supports remain open.

## Constructions, geometry and finiteness

- Retraction and elliptic-orbit lifting are the two infinite `(8,7)`
  mechanisms. The fixed difference-840 bridge is a finite classification.
  They produce near misses, not fully magic squares of nine distinct
  positive squares.
- The least-shift theorem has a uniform interval proof. The bounded
  factor-pair calculations corroborate it, and the separate Appendix-A
  height census is not a premise of that proof.
- The orbit density (`cor:orbitdensity`, §4) counts admissible indices in
  one fixed elliptic orbit. It is not a density by height or among all
  `(8,7)` arrays. The exact Haar-measure formula proves the density; its
  decimal approximation is only numerical corroboration.
- For a fixed difference, completion imposes the interaction
  `x1+x2=2x0` on doubled elliptic coordinates. The irreducible signed-root
  surface describes a different, normalized model with variable difference
  modulo common scale. Its associated degree-five reconstruction over
  `Q(cone)` has generic Galois group `S5`. The full signed cover has degree
  40; the quintic calculation does not identify that full cover's group. Setting `d=840`
  additionally requires `L^2=1680W/(RS)`. Irreducibility and the generic Galois-group statement
  are not transferred to the fixed-difference model.
- The degree-five reconstruction has no generic rational section and
  cannot be solved by successive quadratic radicals over `Q(cone)`. It
  does not rule out other useful rational maps, correspondences or
  arithmetic methods, and does not determine all rational points.
- The Caro–García-Fritz specialization proves fixed-squareclass
  finiteness on the positive distinct locus. It is non-effective.
  The effective smooth-support catalogue uses a separate two-term
  S-unit route.
- The centre-841 closure and the fixed Bremner-shadow result concern one
  fibre and one rational line respectively. Each uses the cited
  computer-assisted rank input.
- The finite-Kummer-class counterexample uses a repeated triple as its
  true witness. It rules out factoring the ambient interaction through
  the separate finite classes. It does not rule out representative-level
  methods or a different statement whose hypotheses already impose
  positivity and pairwise distinctness.

## Open problems and source cautions

The existence or nonexistence of a `3x3` magic square of nine distinct
positive rational or integer squares remains open in general. The paper
does not provide a global support-size bound or an effective enumeration
in an unrestricted squareclass. The residual cover `q_R(K)`, the
unresolved higher lift and the degree-90 class `[A_R]` retain the open
states recorded in `dossiers/`. These dossiers are status summaries with
selected records. The public verifier does not reproduce their full
continuation arguments or the supplementary taxonomy. The coefficient-3
result covers only the stated specializations of the known generic family.
At coefficient 5, four fake-Selmer classes belong only to the surviving
cover; saturation of its rank-two lattice at `2,3,5,7` does not establish a
finite index or full saturation. Bounded short-vector searches do not
decide `[A_R]`.

Bounded searches establish only their stated finite conclusions. A
timeout or an unsuccessful witness search is not an impossibility theorem.
The discussion of Coumbe identifies the repeated-summand counterexample
`120+120=240` to one unrestricted intermediate claim. It does not
disprove a distinct-summand repair or the final smallest-entry conclusion,
neither of which is imported here. The announced nonexistence preprint of
Hill is unrefereed and is not a dependency.

## Verification and review

Exact Python replays check the elementary and symbolic computations.
External-CAS rank, torsion, point-list and Selmer records are authenticated
and parsed; the packaged verifier does not recompute those calculations.
The present reorganization adds no new external-CAS verification.

Independent specialist review remains outstanding, in particular for the
uniform retraction/least-shift proofs and the separate bounded census, the
elliptic-orbit lift and its certificate lineage, the fixed-difference
finiteness specialization, and the smooth-support deduction. These review
limits do not turn the census into a dependency of the uniform proofs.

OpenAI Codex provided substantial assistance in mathematical exploration,
proposed arguments, code, exact checks, drafting and adversarial review.
The author is responsible for the mathematical claims and attribution.
AI-assisted review and separate computational implementations do not
constitute independent human specialist review or end-to-end formal
verification.
