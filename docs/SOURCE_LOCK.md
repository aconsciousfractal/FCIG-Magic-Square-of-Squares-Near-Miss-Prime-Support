# Source lock

No external data is bundled or required: the verifier constructs every
object from scratch, and the frozen Magma layer under `certificates/` is
this project's own record (inputs + transcripts). The theorems import or
build on the following, cited in the paper and owned by their authors.

## Imported theorem cores (never re-proved here)

| input | owner |
|---|---|
| fixed-difference finiteness core (`X_{(c1,c2,c3)}` morphism classification + Uniform Mordell–Lang bound) | Caro–García-Fritz, 2025 preprint cited as `CGF25` (Thm 1.2/1.3) |
| five-term `S`-unit equation count `exp(30^15(r+1))` | Evertse–Schlickewei–Schmidt, *Ann. of Math.* 155 (2002) |
| every entry of a primitive configuration is `1 mod 24` (Lemma 1) | Pierrat–Thiriet–Zimmermann, *Magic Squares of Squares*, technical note dated 2015-03-13, cited as `PTZ15` |
| primitive Pythagorean triangles with exactly three area primes | Aebi, *Elem. Math.* (2026), DOI 10.4171/EM/563 |
| bielliptic quotient method for even genus-two sextics | Flynn–Wetherell, 1999 (`FW99`) |
| two-cover descent and covering-class Chabauty framing | Bruin, *J. reine angew. Math.* 562 (2003) (`BRU03`) |
| equal-area / congruent-number correspondence and the classical `(1,29,41)` progression | Robertson, *Math. Mag.* 69 (1996) |
| Lutz–Nagell integral-torsion criterion | classical; carried per the locked lecture-note source (`IMPA-LNT`) |
| Mordell–Weil basis of `y^2 = x^3 - 44100x` | LMFDB curve `705600.vn3` (transported basis re-verified exactly) |

## Historical and record layer

| input | owner |
|---|---|
| problem statement (1984) and the \$100 offer | LaBar; Gardner (history as recorded in `BRE99` §0) |
| the 7-of-9-squares fully magic record, the degree-27 full solution, and the degree-four witness over `Q(sqrt3, sqrt133)` replayed by the verifier (family 1) | Bremner, *Acta Arith.* 88 (1999) `BRE99` (pp. 289–290; read in full in the project record); Configurations II/VI in *Acta Arith.* 96 (2001) `BRE01` |
| the 9-squares/7-sums record ("The Lost Theorem") | Sallows, *Math. Intelligencer* 19.4 (1997) |
| the order-3 parametric normal form lineage | Lucas (1891), as recorded in the project's source locks |

## Entry-side lineage (attributed prior art; disjoint object)

| input | owner |
|---|---|
| six entry-prime restrictions (all verified from the primary) | Rabern, *Rose-Hulman UMJ* 4(1) (2003), art. 3 |
| three-consecutive-QR centre criterion; residue-class counts | Woll, arXiv:1809.03067 (2018, unrefereed) |
| the finite-field order-three analogue (degrees 3/5/7/9) | Labruna, Montclair State Univ. ETD 138 (2018) |
| order bookkeeping, `1 mod 24` two-entry restriction, seven-arrangement list, Gaussian-signature proposal | Weisenberg, *Rose-Hulman UMJ* 24 (2023), art. 7 |
| announced nonexistence preprint — **unrefereed; nothing here depends on it** | Hill, arXiv preprint cited as `HILL26` |

## Catalogue provenance (cited by locator + digest; never bundled)

| input | owner and locator |
|---|---|
| type taxonomy `6:6` and the search-66 tables (row 340545 carrier) | Fituvalu (`FIT` in the bibliography): `fituvalu.nongnu.org`; dataset `unique-squares.csv`, 166,573,455 bytes, SHA-256 `fa88196c3055d39c8e29ce5f386ba7a1353a027003c28f82d604355919f00117`; source at Savannah, commit `b3063cf8` (2024-02-20). Never bundled (documentation CC BY-SA 4.0, code GPLv3+, dataset terms unresolved) |
| catalogue pages for the Wesolowski carrier and near-miss records | Boyer (`BOY05`, `BOYWEB`): `multimagie.com`, dated locators in the project record |
| centre-true records (the seven completions of Appendix A) | Brown (`BRO` in the bibliography): *Automedian Triangles and Magic Squares*, `mathpages.com/home/kmath417/kmath417.htm`, non-refereed; dated locator in the project record |

## Note on the frozen Magma layer

The shipped transcripts are **normalized records** (uppercase `KEY VALUE`
lines with an assertion status), not raw calculator session dumps: the
`e840` transcript carries an appended provenance footer, and the two
full-class Selmer transcripts omit the version banner (their engine and
date, official Magma Calculator V2.29-8, are recorded in the project
ledger). Byte-exact resubmission of the shipped `.m` inputs reproduces the
**asserted values**, not the transcript bytes. The machine-readable `e840`
certificate references its input and transcript by project-relative paths
(`scripts/…`, `results/…`); in this package both files live under
`certificates/`, and the verifier matches them by digest.

## Engines

Python 3 standard library (the verifier); official Magma Calculator
V2.29-8 **only as frozen transcripts** with byte-exact resubmission
inputs; the project record behind this package additionally used PARI/GP
2.17.4 and SageMath 10.9 for exploration, none of which this package
requires. The MIT license covers only the author's code and documentation
here.
