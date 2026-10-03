# Source lock

No external data is bundled or required for the packaged integrity replay.
The verifier reconstructs the elementary and symbolic objects, and
authenticates and parses the frozen external-CAS records under
`certificates/`; it does not independently recompute the calculations in
those records. The theorems import or build on the following, cited in the
paper and owned by their authors.

## Imported theorem cores (never re-proved here)

| input | owner |
|---|---|
| fixed-difference finiteness core (`X_{(c1,c2,c3)}` morphism classification + Uniform Mordell–Lang bound) | Caro–García-Fritz, *J. Number Theory* 271 (2025), 109–121, DOI `10.1016/j.jnt.2024.11.003`, arXiv:2310.17592, Thms. 1.2/1.3; published primary and arXiv text read 2026-07-26 |
| five-term `S`-unit equation count `exp(30^15(r+1))` | Evertse–Schlickewei–Schmidt, *Ann. of Math.* 155 (2002) |
| natural density of multiples of a non-torsion real elliptic point in an open set | Cowan, *J. Number Theory* 211 (2020), 530–544, DOI `10.1016/j.jnt.2019.12.010`; published primary `https://www.sciencedirect.com/science/article/pii/S0022314X20300184`, arXiv:1901.10656 |
| every entry of a primitive configuration is `1 mod 24` (Lemma 1) | Paul Pierrat, François Thiriet and Paul Zimmermann, *Magic Squares of Squares*, technical note dated 2015-03-13, cited as `PTZ15`; primary PDF `https://members.loria.fr/PZimmermann/papers/squares.pdf`, accessed 2026-08-01 |
| primitive Pythagorean triangles with exactly three area primes | Aebi, *Elem. Math.* (2026), DOI 10.4171/EM/563 |
| bielliptic quotient method for even genus-two sextics | Flynn–Wetherell, 1999 (`FW99`) |
| two-cover descent and covering-class Chabauty framing | Bruin, *J. reine angew. Math.* 562 (2003) (`BRU03`) |
| equal-area / congruent-number correspondence and the classical `(1,29,41)` progression | Robertson, *Math. Mag.* 69 (1996) |
| Lutz-Nagell integral-torsion criterion | Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed. (2009), Chap. VII, Prop. 3.1, DOI `10.1007/978-0-387-09494-6` |
| Mordell–Weil basis of `y^2 = x^3 - 44100x` | LMFDB curve `705600.vn3` (transported basis re-verified exactly) |

## Historical and record layer

| input | owner |
|---|---|
| problem statement (1984) and the \$100 offer | LaBar; Gardner (history as recorded in `BRE99` §0) |
| “Parker” terminology used for this paper's common-difference configurations | The label recalls Matt Parker's widely known *Parker Square*, documented by Numberphile and Brady Haran at `https://www.numberphile.com/videos/the-parker-square` and `https://www.bradyharanblog.com/the-parker-square`, both accessed 2026-08-14. This is a naming/history source only: it does not transfer authorship of LaBar's problem to Parker and does not identify Parker's particular near miss with the configurations studied here. |
| the 7-of-9-squares fully magic record and degree-27 full solution | Bremner, *Acta Arith.* 88 (1999) `BRE99`, pp. 289–290 |
| degree-four witness over `Q(sqrt3,sqrt133)`, its rational/anti-invariant decomposition, and the fixed coefficient line used in the fixed Bremner-shadow proposition | Bremner, *Acta Arith.* 99 (2001) `BRE01`, display (2), p. 289 and equations (28)–(29), pp. 306–307; DOI `10.4064/aa99-3-6`; the displayed eight-square array over `Q(sqrt3)`, family and coefficient formulas are Bremner's. Adjoining `sqrt133` makes the centre square; the present article also proves the fixed-line deduction |
| elliptic quotient in the fixed Bremner-shadow proposition: `y^2=x(x-529)(x-4225)`, minimal label `345345r4`, rank interval `[0,0]` | Cremona elliptic-curve data, `https://johncremona.github.io/ecdata/`; PARI/GP 2.17.4 `ellsearch`, `ellrank`, `elltors`; catalogued data used as a rank dependency |
| the 9-squares/7-sums record ("The Lost Theorem") | Sallows, *Math. Intelligencer* 19.4 (1997) |
| the order-3 parametric normal form lineage | Lucas (1891), cited directly in the bibliography |
| the seven-line almost-magic normal form and its three-common-difference-AP interpretation | Houston, *Bosker Blog*, 13 and 18 July 2016, [Part I](https://bosker.wordpress.com/2016/07/13/magic-squares-of-squares/) and [Almost-magic squares of squares](https://bosker.wordpress.com/2016/07/18/almost-magic-squares-of-squares/); both read 2026-08-01. The article attributes this structure and supplies its self-contained proof and integral line-sum calculation. |
| the exact unordered triple of progressions in the complete `S7` atlas | Houston, *Almost-magic squares of squares*, 18 July 2016, `HOU16B`: roots `(46,74,94)`, `(2,58,82)`, `(97,113,127)` with common integer difference `3360`; the elliptic calculation uses difference `210`. The present catalogue establishes completeness, the three central-role classes modulo `D4` and common square scaling, and their relation to the larger `S13` and `S19` atlases. |
| classical lemniscatic integral and its Gamma evaluation | NIST Digital Library of Mathematical Functions, §19.20(i), Eq. (19.20.2), `https://dlmf.nist.gov/19.20`; terminology and evaluation only. The Beta push-forward of normalized Haar measure on `E_d(R)^0` is derived directly in the paper and is presented as an explanation of the orbit-density corollary |

## Entry-side lineage (attributed prior art; disjoint object)

| input | owner |
|---|---|
| six entry-prime restrictions (all verified from the primary) | Rabern, *Rose-Hulman UMJ* 4(1) (2003), art. 3 |
| three-consecutive-QR centre criterion; residue-class counts | Woll, arXiv:1809.03067 (2018, unrefereed) |
| the finite-field order-three analogue (degrees 3/5/7/9) | Labruna, Montclair State Univ. ETD 138 (2018) |
| order bookkeeping, `1 mod 24` two-entry restriction, seven-arrangement list, Gaussian-signature proposal | Weisenberg, *Rose-Hulman UMJ* 24 (2023), art. 7 |
| announced nonexistence preprint — **unrefereed; nothing here depends on it** | Hill, arXiv preprint cited as `HILL26` |
| Pell-transform approach and smallest-entry exclusion | The unity case is credited by Coumbe to Lee Morgenstern (2006); Coumbe owns the prime-square extension and the audited published statement: *JP J. Algebra Number Theory Appl.* 63(6) (2024), 587–614, DOI `10.17654/0972555524032`, primary PDF `https://pphmjopenaccess.com/jpjana/article/download/2332/1365/5024`. This paper does **not** import the exclusion because the unrestricted intermediate difference-set claim admits the literal repeated-summand instance `120+120=240`; this does not decide a distinct-summand repair or the final exclusion. The unity-case attribution to Morgenstern is preserved. |

## Recent adjacent work (cited, not imported)

| input | owner |
|---|---|
| uniform rank-dependent bounds for arithmetic/geometric progressions and consecutive squares inside one elliptic coordinate set | Harrison–Mudgal–Schmidt, `https://arxiv.org/abs/2603.06483v1` (submitted 2026-03-06), Theorem 1.1; **unrefereed preprint**, complementary to rather than a replacement for the three-coordinate interaction theorem |

## Catalogue provenance (cited by locator + digest; never bundled)

| input | owner and locator |
|---|---|
| type taxonomy `6:6` and the search-66 tables (row 340545 carrier) | Fituvalu (`FIT` in the bibliography): `fituvalu.nongnu.org`; dataset `unique-squares.csv`, 166,573,455 bytes, SHA-256 `fa88196c3055d39c8e29ce5f386ba7a1353a027003c28f82d604355919f00117`; source at Savannah, commit `b3063cf8` (2024-02-20). Never bundled (documentation CC BY-SA 4.0, code GPLv3+, dataset terms unresolved) |
| catalogue pages for the Wesolowski carrier and near-miss records | Boyer (`BOY05`, `BOYWEB`): `https://www.multimagie.com/English/SquaresOfSquares.htm` and `https://www.multimagie.com/English/SquaresOfSquaresSearch.htm`, accessed 2026-07-24; archival snapshots SHA-256 `2a2602ab68a9eb0ed4785eed34292ae5a151a00b5f4d593f7b53db8a217241df` (64,766 bytes) and `d753e84fbd81d04bfa104aff33bb82b83a05a2992d8948443b780399dd91343e` (105,400 bytes), not bundled |
| centre-true records (the seven completions discussed in Appendix D) | Brown (`BRO`): *Automedian Triangles and Magic Squares*, `https://www.mathpages.com/home/kmath417/kmath417.htm`, accessed 2026-07-24, non-refereed; archival HTML snapshot SHA-256 `17676ac268212fc856ac22d1209939a0030254d368c7806a0e62957f8518b383` (57,631 bytes), not bundled |

## Note on the frozen external-CAS layer

The shipped transcripts are **normalized records** (uppercase `KEY VALUE`
lines with an assertion status), not raw calculator session dumps. The
centre-841 transcript carries an appended provenance footer; the two
full-class Selmer transcripts now carry an in-band `MAGMA_VERSION 2 29 8`
record. Byte-exact resubmission of the shipped `.m` inputs reproduces the
**asserted values**, not the transcript bytes. The centre-841
machine-readable certificate references both its input and transcript by
their public `certificates/…` paths, and the verifier matches them by digest.
Two additional
PARI/GP 2.17.4 input/output pairs are shipped. The first independently
corroborates rank 3 for the first bielliptic quotient of the `x0=841` fibre;
that contextual rank is not used to close the fibre. The second supplies the
unconditional rank interval `[0,0]` and catalogue label used in the fixed Bremner-shadow proposition. The verifier authenticates and parses both pairs but does not execute
PARI/GP; for the fixed Bremner-shadow proposition it independently checks the quotient identity,
finite-field counts, torsion-halving obstruction and terminal parameter
elimination.

## Engines

Python 3 standard library (the verifier and both census implementations);
official Magma Calculator V2.29-8 **only as frozen records** with byte-exact
resubmission inputs; PARI/GP 2.17.4 as two reproducible input/output pairs,
one contextual and one rank-bearing for the fixed Bremner-shadow proposition. Neither external
system is required to run the packaged
integrity replay. Exploratory computations additionally used SageMath 10.9 for
exploration. The MIT license covers only the author's code and documentation
here.

## Smooth-support sources and conversions (source check 2026-10-03)

- **Aebi:** DOI `10.4171/EM/563`, *Elemente der Mathematik* 81 (2026),
  71–72, theorem and concluding remark, publisher full text read. The six
  primitive triangles with exactly three area primes have areas
  30, 60, 180, 84, 504, 1224; the sole triangle with fewer area primes is
  (3,4,5), area 6. The seven squarefree parts 6,30,15,5,21,14,34 are
  distinct. Our uniqueness statement is the squareclass consequence of
  this classification, with `d/4 = area * root_gcd^2`.
- **von Känel–Matschke:** [arXiv:1605.06079v1](https://arxiv.org/abs/1605.06079v1),
  Theorem A, printed p. 7; version dated 2016-05-19. The imported totals
  for the first 4, 6 and 8 primes are 63, 545 and 3649. These count symmetry
  orbits of rational `x+y=1`, not ordered signed solutions. The unique
  representative `0 < x <= 1/2` identifies each orbit with a primitive
  positive `a+b=c`, `a<=b`; (1,1,2) is counted once.
  The PDF SHA-256 read was
  `3890fe77150fd7ca94eb6e3dd36e1f648809e3684ac9a8ad5ec7e13e2f91f1c2`.
  Only these totals are imported. No unproved conjecture about all supports
  of a fixed cardinality is used. The earlier n<=6 computations are credited
  by the source to de Weger; we do not claim to repeat either original sieve.
- The [authors' data page](https://www.math.u-bordeaux.fr/~bmatschke/data/)
  confirms the same normalization and counts. Its S19 text file was compared
  read-only with our independently regenerated witnesses: all 3649 agree.
  That third-party file (CC BY-NC 3.0) is **not bundled**; its checked SHA-256
  is `e0a3e69866745312a6f891795156a197dabfc6abed3861a620d73cd3f89e9212`.
  Shipped certificates are locally produced exact integer witnesses and
  derived triangle/array catalogues, with no copied source implementation.

The import-to-target proof and all scale, parity and D4 conversions are in
Section 3 (`main:smoothsupport`) and `SMOOTH_SUPPORT.md`. The catalogue gives exclusions for
subsets of the first eight primes, not for arbitrary eight-prime supports.

The geometric source/evidence map distinguishes the fixed-difference
elliptic interaction from the variable-difference signed-root model modulo
scale. The latter carries the irreducibility statement and an associated
degree-five reconstruction over `Q(cone)` with generic Galois group `S5`.
The full signed cover has degree 40; its full group is not identified by
that quintic calculation. Fixing `d=840` additionally imposes `L^2=1680W/(RS)`;
the generic Galois-group statement is not transferred to that arithmetic lift. This
coordinate clarification uses the written algebra, not a new external-CAS
calculation.
