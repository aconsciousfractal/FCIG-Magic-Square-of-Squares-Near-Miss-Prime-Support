# Contributions, evidence and scope

This map separates imported mathematical inputs from the deductions,
constructions and classifications presented in the article. Stable LaTeX
labels identify the results independently of changing theorem numbers.
Source versions and locators are in [SOURCE_LOCK.md](SOURCE_LOCK.md);
the comparison with earlier work does not establish exhaustive
bibliographic priority.

| Result and location | Imported input | Contribution and evidence | Exact scope |
|---|---|---|---|
| Seven-line form and integral lattice (§2; `main:normalform`, `prop:linesumsnf`) | Lucas/Houston normal form | Self-contained proof, integral image conditions, Smith form and exact determinant/modular-rank replay | The normal form is attributed; the lattice calculation concerns the ordinary eight-line map |
| Three-prime uniqueness (§3; `main:threeprime`) | Aebi's primitive-triangle classification | Distinct area squareclasses and the identity `d/4=area*root_gcd^2` give uniqueness for every fixed positive integer difference with at most three prime factors | No primitivity assumption; excludes both `(9,7)` and fully magic arrays at such a difference |
| Smooth-difference full-magic exclusion (§3; `main:smoothsupport`) | von Känel–Matschke, Theorem A, complete totals | Checked complete additive lists, bijective triangle reconstruction and exhaustive rational midpoint tests | Support contained in the primes at most 19, with arbitrary exponents; not arbitrary four-prime or eight-prime supports |
| Complete `(9,7)` atlases and defect minima (§3; `main:smoothsupport`) | The same complete totals and the classical triangle correspondence; Houston's known `S7` triple | Separate producer/checker reconstruct `3/45/384` primitive classes, prove the `D4`/scale normalization and compute the sharp minima | Nine distinct positive square entries and exactly seven equal sums; `S19` minimum `347984603/9837828000` is relative to the progression difference and is attained by one class |
| Infinite retraction family and least shift (§4; `main:families`, `prop:factorpairs`, `prop:leastshift`) | Catalogued Bremner/Wesolowski carrier | Explicit uniform construction, divisor classification and full interval proof; exact recurrence checks | `(8,7)` arrays; least shift is 9 at the first index and `6z_n^2` thereafter; the uniform proof does not depend on the bounded census |
| Fixed difference-840 bridge (§4; `prop:bridge`) | Fituvalu type 6.VI, Bremner Configuration VI and Robertson's progression | Complete factor-pair classification and explicit `(8,7)` array | Finite classification of the fixed bridge; not a third infinite-family theorem |
| Infinite orbit lift and density (§4; `cor:orbitdensity`) | Classical congruent-number doubling and real elliptic equidistribution | Minimal denominator clearing, entry-primitivity and inequivalence proofs; exact witnesses; analytic Haar-measure formula | Density is by index in one fixed orbit, not by height or among all arrays; decimal quadrature is corroboration only |
| Fixed-difference interaction (§5; `main:surface`) | Square-progression/congruent-number correspondence | The eighth line is the relation `x1+x2=2x0` among doubled elliptic coordinates | Membership in `2E_d(Q)`, positivity and distinctness remain arithmetic conditions |
| Variable-difference signed-root surface and quintic reconstruction (§5; `main:surface`) | Classical square-progression cone | Coordinate reduction, irreducibility/saturation proof and degree-five reconstruction over `Q(cone)` with generic Galois group `S5`; full signed cover of degree 40; exact algebra and factorization records | Model modulo common scale with variable difference; fixing `d=840` requires `L^2=1680W/(RS)`. The quintic Galois-group calculation neither identifies the full signed-cover group nor transfers to that fixed-difference model |
| Fixed-squareclass finiteness (§6; `main:finiteness`) | Caro–García-Fritz's morphism classification and Uniform Mordell–Lang bound | Specialization to the positive distinct locus and the rational-square scaling argument | Non-effective; no complete point enumeration follows |
| Closed fibre at centre 841 (§6; `main:finiteness`) | Frozen Magma rank-zero and torsion record for the decisive quotient | Quotient identity, complete pullback and positivity elimination; exact surrounding algebra replay | One fibre, computer-assisted; the other quotient's rank-three record is contextual only |
| Fixed Bremner shadow (§6; `prop:bremnershadow`) | Bremner's coefficient line and frozen PARI/GP rank interval | Quotient reduction, elementary torsion calculation and parameter elimination | Only this rational line; no global impossibility conclusion |
| Finite Kummer-class stop (§6; `main:kummerstop`) | Elliptic group structure and the stated basis | Explicit equal-class pairs and a triple counterexample for every finite level | Ambient doubled-point space; the true witness is a repeated triple. No exclusion of representative-level methods or a theorem restricted in advance to the positive distinct locus |
| Support law and local restrictions (§7; `main:supportlaw`) | Evertse–Schlickewei–Schmidt count and Pierrat–Thiriet–Zimmermann congruence input | Five-term identity, nondegeneracy proof, endpoint/interior laws and `{2,3}` exclusion | Necessary conditions and a fixed-support count; not an effective enumeration from that count or a global support-size bound |
| Four-prime frontier (§8; `prop:fourprime`, `prop:balanced`, `prop:outercore`) | Aebi cores, bielliptic/descent methods and frozen rank/point/Selmer records | Edge factorization, balanced reductions and central/outer core-area-6 exclusions | Arbitrary four-prime supports remain open outside the specific complete-catalogue exclusions |
| Height-47 `(8,7)` census (Appendix A; `prop:census`) | Seven-line normal form | Two separately implemented exact enumerators and nine canonical representatives | No classes through height 46 and nine through 47; distinct from the uniform construction proofs and the `(9,7)` catalogue |
| Supplementary endpoint laws, taxonomy and continuations (Appendix C) | Local support laws and the cited classical inputs | Alternative primitive three-prime argument and ordinary proofs of the incidence count, Hall criterion and outer-factor reduction | Hall sufficiency is limited to the declared matching relaxation; the Pythagorean and interaction equations remain necessary. The three continuation dossiers are status summaries, not calculations reproduced by the public verifier; residual cover, higher lift and degree-90 class remain open |

Houston's 18 July 2016 example supplies exactly the unordered `S7` root
triple `(46,74,94)`, `(2,58,82)`, `(97,113,127)`, of common integer
difference 3360. His elliptic calculation uses difference 210. The atlas
adds the complete classification for the declared support and equivalence.

External computer-algebra records are digest-pinned and parsed. The Python
verifier replays the surrounding exact algebra but does not recompute the
external rank, point-list or Selmer calculations. The imported S-unit
completeness theorem is also a mathematical dependency, not a result of the
local replay. See [PUBLIC_CLAIM_BOUNDARY.md](PUBLIC_CLAIM_BOUNDARY.md) for
the remaining mathematical and review limits.
