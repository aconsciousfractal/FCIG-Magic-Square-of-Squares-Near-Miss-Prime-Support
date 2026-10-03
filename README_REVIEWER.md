# Reviewer reading and verification guide

This guide accompanies version 1.2.0. Start with the
[paper](paper/Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf)
and its [contribution/evidence map](docs/CLAIM_LEDGER.md).
The replay checks exact finite evidence; mathematical review of the
uniform proofs and imported results remains a separate task.

## Reading path

| Location | Mathematical question and result |
|---|---|
| §1 | The problem, the two near-miss metrics and the contributions relative to earlier work |
| §2 | Seven-line normal form, full-magic interaction and integral line-sum lattice |
| §3 | Aebi-derived three-prime uniqueness; complete smooth-support exclusion, `3/45/384` atlases and exact defect minima |
| §4 | Infinite retraction and orbit-lift constructions, finite difference-840 bridge, least shift and orbit density |
| §5 | Fixed-difference interaction; the distinct variable-difference signed-root surface, saturation and the associated degree-five reconstruction |
| §6 | Imported finiteness and its specialization; centre-841 fibre, fixed Bremner shadow and finite-Kummer-class stop |
| §7 | Five-term S-unit law, fixed-support count and local endpoint restrictions |
| §8 | Arbitrary four-prime frontier, balanced cores and the two closed core-area-6 branches |
| §9 | Remaining mathematical questions |
| Appendix A | Exact bounded `(8,7)` census |
| Appendix B | Full least-shift interval proof and certificate map |
| Appendix C | Supplementary endpoint arguments, support taxonomy and research continuations |
| Appendix D | Bibliographic and related-construction notes |
| Appendix E | Reproducibility, data policy and AI assistance |

For the complete-support theorem, read von Känel–Matschke's Theorem A
alongside [SMOOTH_SUPPORT.md](docs/SMOOTH_SUPPORT.md) and the reconstruction
proof. The imported total, the bijection and the symmetry normalization
are distinct logical steps. Houston's 18 July 2016 example is the exact
unordered `S7` triple with integer difference 3360; the article's claim
there is the complete classification, not discovery of that triple.

For the geometric results, check the coordinate bridge in §5 and keep its
two arithmetic models separate. The degree-five reconstruction over `Q(cone)` has generic Galois group
`S5`; it belongs to the variable-difference model modulo scale. The full
signed cover has degree 40, and its group is not identified by the quintic
calculation. A lift with `d=840` additionally
requires `L^2=1680W/(RS)`; no fixed-difference Galois-group conclusion is
asserted.

## Exact local replay

Python 3.10+ and its standard library suffice. No external data,
randomness, network access or commercial software is needed for these
commands.

```bash
python scripts/verify.py \
    --output results/verification.json --log results/verification.log
python scripts/census_reference.py
python -B scripts/verify_smooth_support.py
python -B -O scripts/verify_smooth_support.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

The original verifier covers the line-sum lattice, recurrence and
least-shift identities, finite bridge, orbit witnesses, interaction and
variable-difference surface algebra, finite-class counterexample, support
identities and frontier calculations. It also checks the quartic witness
and reconstructs the bounded height census. High-precision quadrature
corroborates only the decimal of the exact orbit-density formula.
[REPRODUCE.md](REPRODUCE.md) maps the unchanged certificate-family numbers
to the reorganized manuscript.

The original replay ends in `PASS` only when its output matches
`certificates/expected_verification.json` byte for byte and has the
internally pinned digest. The independent census must report 0 classes
through height 46 and 9 through height 47, including 2 with nonsquare
centre. Its implementation scans centres and differences; the original
verifier constructs progressions from roots.

The smooth-support checker reconstructs all triangle and array lists and
performs every midpoint test. It must report 3649 additive witnesses,
12/62/232 primitive triangles, zero midpoint hits and 3/45/384 primitive
array classes. The expected receipt is mandatory; missing records,
duplicate keys, damaged witnesses and type/value drift are rejected.
These finite checks do not re-prove the imported completeness theorem.

Check `MANIFEST_SHA256.txt` using the commands in
[REPRODUCE.md](REPRODUCE.md). It covers the shipped source, certificates
and documentation; the compiled PDF and regenerated `results/` are
excluded.

## External computer-algebra dependencies

The official Magma Calculator V2.29-8 results enter as 13 of the 17
external-CAS files under `certificates/`: seven output records or
certificates and six exact calculator inputs. They supply the two
rank-zero quotients, a complete point list, the six addition-curve rank
pairs and two singleton fake-Selmer sets. The verifier checks hashes and
parses asserted values; it never runs Magma.

The records are normalized assertions, not raw session dumps.
To recompute a Magma-dependent result, resubmit its `.m` input at the
[official calculator](https://magma.maths.usyd.edu.au/calc/) and compare
the asserted values. Independent auditing requires Magma or a separate
implementation of those calculations.

The other four files are two PARI/GP 2.17.4 input/output pairs. One
corroborates the contextual rank-three quotient of the centre-841 fibre;
the other supplies the rank-zero interval for the fixed Bremner-shadow
proposition (`prop:bremnershadow`). The verifier authenticates and
parses both pairs but does not execute PARI/GP. No new external-CAS
computation is supplied by this reorganization.

## Scope and remaining review

Read [PUBLIC_CLAIM_BOUNDARY.md](docs/PUBLIC_CLAIM_BOUNDARY.md) with the
theorem being assessed. The principal distinctions are difference support
versus entry support, two infinite constructions versus the finite bridge,
the variable-difference surface versus a fixed-difference lift, and exact
finite replay versus imported global completeness or rank calculations.
The uniform least-shift proof does not rely on the bounded census.

[The research dossiers](dossiers/README.md) summarize the unresolved
residual-cover, higher-lift and degree-90 problems with selected records.
They are not complete reproducibility packages: the main verifier does not
reproduce their full calculations or the supplementary taxonomy. The
coefficient-3 statement concerns the specified generic-family
specializations; the coefficient-5 lattice has only the stated saturation
at `2,3,5,7`, without a proved finite index. Their broader open problems
remain unresolved.

The author used substantial AI assistance in mathematics, code, checks,
writing and adversarial review. The contribution/source map does not
certify exhaustive priority, and AI-assisted checks do not substitute for
the independent specialist review still outstanding for the manuscript.
