# Exhausted routes — every closed route, with its exact boundary

Scope: the difference-side program of the main paper and its three dossiers.
Each entry names a route that was run to its recorded stop, states the exact
boundary of what the stop establishes, and points to the record. A stop is
never an impossibility statement: upgrading any entry beyond its stated
boundary is forbidden. Negatives are never deleted; if a later run
contradicts one, both records stay and the contradiction is adjudicated in
the project log. The earlier, pre-consolidation negatives of the wider lane
(bounded pattern scans, selector channels and near-miss atlases outside this
paper's scope) remain in the project's `NEGATIVE_RESULTS.md` and are not
restated here.

## A. Stops recorded in the paper itself

| # | route | stop and exact boundary | record |
|---|---|---|---|
| A1 | rank-3 bielliptic quotient of the `x0 = 841` fibre | the quotient by `(t,w) -> (-t,w)` has rank 3 and **decides nothing**; the naive "compute the rank, then elliptic Chabauty" plan was under-specified. The complementary rank-0 quotient closed the fibre — one fibre only. | paper §5.2 |
| A2 | resolving the interaction cone by radicals or a generic section | the specialized monodromy is the full `S5`: no generic rational section, no quadratic-radical tower. Says nothing about other rational maps, height-decreasing correspondences, or further structure on the surface. | paper §4.3 |
| A3 | pure finite Kummer/2-Selmer class obstructions | neither `P -> x(P)` nor the interaction factors through the finite class triples, for any level `n`. Representative-level methods (covering curves, heights, valuations, a Mordell–Weil sieve) are **not** excluded. | paper §5.3 |
| A4 | ordinary genus-two Chabauty on the six addition curves `H_{n,a}` | blocked: the proved Jacobian ranks 2,2,3,3,4,5 are never below the genus. Two-cover descent still applies and leaves singleton fake two-Selmer sets for areas 30/60 — a target, not a result. | paper §8; `../certificates/` |

## B. J458

| # | route | stop and exact boundary | record |
|---|---|---|---|
| B1 | four Magma shortcuts | software stops, **not mathematical evidence**: `TwoDescendantsOverTwoIsogenyDescendant` raised an internal number-field error; `qCoverPartialDescent` raised an internal bad-argument error; full `qCoverDescent` exceeded the calculator time limit and requested conditional class-group data; `HasPointsEverywhereLocally` timed out on the surviving `(1,1)` block. Each was replaced by explicit local certificates (complete bad-place support, direct 2-adic point, odd-prime Hensel/square certificates, real checks, Hasse–Hensel at good reduction). None is used as evidence anywhere. | `E-P41-039`; project `NEGATIVE_RESULTS.md` |
| B2 | selected-channel rank computation | both selected channels stop at a rank-two bound (`T`); rank 1 versus 2 stays open on both. | `docs/SELECTED_CHANNEL_RANK_STOP.md` |
| B3 | filtered-Selmer pairing descent | the filtration stabilizes: `Theta_4 = 0` and **all later pairings vanish** (`AE`), so no further finite Fisher pairing can decide the chain. The open dichotomy is exactly rank 1 + nontrivial divisible Sha versus rank 2 + `q_R(K)` nonempty. | `docs/J458_FILTERED_SELMER_STABILIZATION_THEOREM.md` |

## C. The lift tower

| # | route | stop and exact boundary | record |
|---|---|---|---|
| C1 | fake two-Selmer descent on `D+` (`n = 5`) | the complete fake two-Selmer set has **four classes and eliminates none**: fake descent on `D+` is exhausted. It proves four everywhere-locally-soluble fake classes; it does not produce a rational point on any nonidentity cover. | `AX`; transcript pinned in `PO111A_N5/README.md` |
| C2 | real/local sieve on `D-` and the live branch | `D-` is empty on the live real branch `T >= 2`, and the projective sieve at `p = 3, 7` forces the identity cover; **no complete rational-`T` list follows** from the sieve. | `AW` |
| C3 | the `n = 3` stratification stage | at the `AQ` stage the Magma point list carried `complete = false`; superseded by the certified-complete lists of `AR`, which close `n = 3` only. | `AQ`, `AR` |
| C4 | uniformizing the odd family | the reciprocal structure persists for all odd `n`, but the genus of the terminal quotients grows on the order of `n^2/4`: the `n = 3` mechanism does not persist, and the specialized-odd family is an infinite non-uniformized ladder. Opens `ODD-ARITHMETIC`; **no bounded search is admitted** on it. | `AS` |
| C5 | automatic Mordell–Weil control over the degree-30 pair field | the automatic pseudo-Mordell–Weil and point-order computations timed out and were **discarded as evidence**; the recorded blocker is finite-index Mordell–Weil control, and the conditional elliptic-Chabauty gates wait on it. | `C130`/`C131` gates; project log 2026-07-28 |

## D. The degree-90 toolchain

| # | route | stop and exact boundary | record |
|---|---|---|---|
| D1 | twisted monomial characters in the `S6` normal closure | the twisted monomial-character space is **zero**: only the trivial character splits at all 26 primes above 72559. Excludes rank-one monomial characters only; the true dual object (a character of `Cl_S(F90)[2]`) remains open. | `E-P41-131` |
| D2 | pure pair rows of the `K5` compression layer | the ten pure-pair directions span an even-weight image (rank 4) while the marked vector has odd weight: **no pure-pair row can ever certify `[A_R] = 0`**. Retained as a compression layer only. | `E-P41-133` |
| D3 | descent images as a supply of new directions | the 2-descent map is a homomorphism, so the whole infinite subgroup `<H, R>` yields four squareclasses and, modulo the `S`-unit `x(H) - theta`, exactly one — `[A_R]` itself. Descent supply is exhausted at rank one; conditional on `<H, R>` being all of Mordell–Weil. | `E-P41-140`, `E-P41-152` |
| D4 | elementary `S`-unit families | fifteen structurally motivated candidates: three hits, all previously known or multiplicatively derived; the misses fail the factorization-free filter by residues of 228–465 digits against 1. The shift/elementary-value family at `theta` is closed. | `E-P41-151` |
| D5 | generalized norm relations with odd denominator | every odd-order subgroup of `S6` has order at most 9, whose fixed field has degree 160 over `Q` against the 90 of `F90`: any odd-denominator norm relation costs more than the problem. Lane closed. | `E-P41-141` |
| D6 | reciprocity on local data alone | withdrawn: `x(R) - theta` is a global element and satisfies every relation valid for global elements, so no functional built from the exhibited local data can separate it. The separator must be a nontrivial character of `Cl_S(F90)[2]`. | `F-CODEX-03`; `docs/RED_TEAM_AUDIT_CODEX_B7D_ANALYSIS_2026_07_30.md` |
| D7 | direct class-group computation in degree 90 | `bnfinit` on the absolute field produces nothing inside a governed 900 s / 6 GB window, and the standard smoothness estimate puts the relation hunt near `4 x 10^12` tests at Minkowski scale (heuristic `L_D[1/2, sqrt(2)] ~ 4 x 10^30`). **Cost evidence, not an arithmetic fact**; the sanctioned path is the relative route (32 relative units + 17 principal lifts with an index certificate), never a monolithic degree-90 `bnfinit`. | `E-P41-142`, `E-P41-153`; finding `F2` |
| D8 | the short-vector (lattice) lever | eleven `idealmin` directions on the reduced structure: no positive witness; target-to-calibration gap inside the noise. Two findings bound the route: flag-4 (unreduced) structures are useless for lattice work, and **the shortest element of a principal ideal need not generate it**, so a lattice miss can never be read as a negative — here or in any future lattice gate. Sensitivity measured: covolume `10^122.4`, `lambda_1 ~ 52.5`, LLL at `~74`, trivial-`S`-part generator threshold `>= 22.0`; PARI exposes no BKZ. The lever is spent. | `E-P41-156` |
| D9 | the outer-pentad coordinate route | the canonical outer-pentad lift is principal by an exact degree-12 computation (`B6G`), and importing its relation leaves the rank at 9/25 with the marked vector surviving (`B6G-D90`): the pentad neither decides `[A_R]` nor enlarges the usable relation space. No exhaustivity among twisted lifts is claimed. | `B6G`, `B6G-D90` |
| D10 | bounded selector and benchmark scouts | the governed scouts of the `B3`/`B4`/`B5` blocks (short-vector selectors, relative-squareclass and root-difference character windows, the degree-40 `bnf` benchmark) are bounded no-hits or cost measurements, each recorded with its exact window in the experiment ledger; none is a theorem and none closes a mathematical route by itself. | `E-P41-136`–`E-P41-151` ledger addenda |

## What remains live

For completeness of orientation only (each with its own gate in the
dossiers): the decision `q_R(K)` (J458); `ODD-ARITHMETIC` and the
finite-index Mordell–Weil gate (lift tower); the arithmetic dual character
and the positive-witness search on the compressed representative, plus the
degree-30 half of the `d90` splitting (degree-90 toolchain). Nothing on
this list carries any claim.
