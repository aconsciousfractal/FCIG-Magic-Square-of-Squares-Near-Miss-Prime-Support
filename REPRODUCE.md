# Reproducing the certificates

## Requirements

- Python 3.10+ — **standard library only** (see `requirements.txt`; there
  is nothing to install).
- No external data, network, randomness or commercial software is needed
  for the packaged integrity replay. Independent recomputation of the
  Magma-dependent claims is a separate audit.

## Run

```bash
python scripts/verify.py \
    --output results/verification.json --log results/verification.log
```

## Expected result

The run prints one progress line per certificate family and ends in `PASS`.
It verifies, with exact integer and rational arithmetic:

1. the digest layer: all 17 frozen external-CAS files under `certificates/`
   match their
   pinned SHA-256 and byte counts;
2. family 0 (§2): the integral line-sum matrix, its primitive free relation,
   exceptional mod-3 relation, determinant witnesses `-1` and `-3`, Smith
   form `diag(1,1,1,1,1,1,3,0)`, and modular ranks;
3. family 2 (§4 and Appendix B): the retraction identities as polynomial
   identities modulo the family invariant, the complete interval-analysis
   identity set, the factor-pair census for `n = 1..6` against the frozen
   table (`t_min = 9`, then `6z^2`), the `(23,37,47)`/`(79,65,89)` bridge
   divisor check with the 9291-sum array, and the elliptic-orbit witnesses
   `m = 1` and `m = 3` recomputed from the group law with denominator
   clearing, together with deterministic high-precision `Decimal`
   corroboration of the printed orbit density `0.6585271498271213`;
4. family 3 (§5): the transversal interaction equation, the LMFDB
   Mordell–Weil basis transport, the variable-difference signed-root
   surface's saturation premises (including
   `p_C - 2 p_A = -N_B` as an exact identity and the 30 saturated
   factors), and the associated quintic's generic `S5` Galois-group
   certificate (irreducible mod 7,
   pattern `[2,1,1,1]` mod 29, discriminant `-24364389070416096000`);
5. families 4–5 (§6): the `x0 = 841` bielliptic quotient identity, the
   pulled-back t-list `{0, ±1, ±841, ±1681}`, the parsed rank-zero
   transcript; the fixed Bremner-shadow rank-zero quotient, finite-field
   counts, torsion-halving test and exact rejection of every nonzero
   parameter; and the half-class countercertificate
   `delta(Q + 2^n R) = delta(Q) = (7,10,70)` against distinct doubled
   centres;
6. families 6–7 (§7 and Appendix C): the torus identity (abstract and
   on-surface), the
   14-subsum table, the endpoint pigeonhole to `e = 12`, the mod-8 table
   from quadratic residues, the `{2,3}` exclusion replay, the three-block
   and one-interior identities, and the `W = 2x-1` forcing whose only
   cubic hit is `(x, W) = (2, 3)`;
7. family 8 (§8): the edge-factorization identity, both fixtures (area
   210, mixed 30600), the seven balanced cores with their sextic/quotient
   identities and frozen integer models, both closed core-6 fibres with
   their parsed transcripts, the generic secant addition identity, and the
   six `H_{n,a}` curves whose parsed proved rank pairs sum to
   `2,2,3,3,4,5`, with the two singleton fake-Selmer sets.

plus, as family 1, the quartic witness discussed in Appendix D — the
degree-four completion of Bremner's displayed array, giving a fully magic
square of nine distinct squares over `Q(sqrt3, sqrt133)`
(centre `532 = (2 sqrt133)^2`, all eight lines summing 1596), replayed in
exact quadratic-field arithmetic with a biquadratic degree certificate —
and, as family 9, the Appendix-A height census replayed from scratch as a
second independent enumerator (12/13 full progressions at heights 46/47,
unique doubled difference 840, three partial progressions, 18 arrays = 9
exact `D4` classes with 2 centre-nonsquare, and the nine canonical
representatives frozen in the expected output). The separately shipped
`scripts/census_reference.py` supplies the first, centre/difference-based
census implementation; it can be run independently in a few seconds.

Certificate-family identifiers and historical section numbers inside code
comments remain unchanged. The locations above refer to the reorganized
manuscript. The `S5` assertion concerns the degree-five reconstruction over
`Q(cone)`; the full signed cover has degree 40. Fixing `d=840` requires the
additional rational-square lift `L^2=1680W/(RS)`, and no Galois-group claim
for that fixed-difference model follows from the certificate.

The output JSON is byte-identical across runs and under `python -O`. The
run **fails closed**: it requires the live output to hash to the digest
pinned inside the verifier, requires
`certificates/expected_verification.json` to be present, and requires
byte-identity against it — any drift, and any missing certificate, is a
hard failure. The certificate SHA-256 is

```
283DB3886199A93F0C510799AC70973C705F809EFDBA1ABFA2121100747CF1B6
```

## What is imported rather than replayed

- **Frozen external-CAS evidence.** The load-bearing rank, torsion,
  point-list and Selmer computations
  attributed in the paper to the official Magma Calculator V2.29-8 ship as
  the transcripts under `certificates/`, together with the exact submitted
  `.m` inputs. The verifier checks digests and re-parses the asserted
  lines; it never executes Magma. The transcripts are **normalized
  records**, not raw session dumps (see `docs/SOURCE_LOCK.md`), so an
  independent audit resubmits the `.m` files at
  `https://magma.maths.usyd.edu.au/calc/` byte-exact and compares the
  **asserted values** (ranks, torsion, point lists, Selmer sets) rather
  than raw transcript bytes. One PARI/GP 2.17.4 input/output pair concerns
  only the contextual rank-three quotient in §6; it is reproducible with
  `gp -q -f certificates/centre841_first_quotient_pari.gp` and is not used to
  prove the fibre closure. The second pair is reproducible with
  `gp -q -f certificates/bremner_shadow_pair_quotients.gp` and supplies the
  unconditional rank interval used by the fixed Bremner-shadow proposition
  (`prop:bremnershadow`); all surrounding
  quotient, torsion and parameter-elimination steps are replayed in Python.
- **Imported theorems.** Cowan's natural-density formulation for real
  elliptic multiples, the Caro–García-Fritz finiteness core (§6),
  the Evertse–Schlickewei–Schmidt subspace-theorem count (§7), the
  Pierrat–Thiriet–Zimmermann `1 mod 24` input, and Aebi's equal-area triangle
  classification (§3) are cited, never re-proved; see
  `docs/SOURCE_LOCK.md`. The complete S-unit totals of von Känel–Matschke
  are an additional dependency of the smooth-support result below.
- **Third-party data.** Nothing is bundled. Fituvalu's tables are
  referenced by locator and digest in the paper's appendix; the entry-side
  PDFs (Rabern, Woll, Labruna, Weisenberg) are cited with their public
  locators and were verified against the cited primary sources.

The continuation dossiers are status summaries, not complete
reproducibility packages. Appendix C supplies ordinary proofs of the
incidence count, matching criterion and outer-factor reduction; these
are not computations checked by the public verifier. `scripts/verify.py` reaches the
main-paper support identities, fixed-core calculations and area-30/60
singleton fake-Selmer records; it does not reproduce the taxonomy,
residual `q_R`, higher-lift lattice or degree-90 calculations. No new
external-CAS calculation is supplied by this reorganization.

## Check the manifest

`MANIFEST_SHA256.txt` pins the environment-independent bytes of the
package: the LaTeX source, the verifier, the frozen certificates, the
dossiers and the documentation. It does **not** pin the compiled PDF (its
bytes depend on the TeX distribution) or `results/` (regenerated on
replay).

```bash
# Linux/macOS:
sha256sum -c MANIFEST_SHA256.txt
# or, cross-platform:
python -c "import hashlib; \
[print('OK' if hashlib.sha256(open(p.strip(),'rb').read()).hexdigest()==h.lower() else 'MISMATCH', p.strip()) \
 for h,p in (l.split(None,1) for l in open('MANIFEST_SHA256.txt') if l.strip() and not l.startswith('#'))]"
```

## Build the paper

Multi-file LaTeX: `paper/main.tex` inputs `paper/macros.tex` and
`paper/sections/` plus the inline bibliography (`99_references.tex`
— **no `bibtex`/`biber` pass**). Three `pdflatex` passes resolve the
cross-references. `main.tex` sets
`\pdfinfoomitdate=1`, `\pdfsuppressptexinfo=-1` and `\pdftrailerid{}`, so
the build uses the fixed `SOURCE_DATE_EPOCH` below and is byte-stable on a
fixed TeX distribution.
Rebuild from `paper/` with the title-named job target:

```bash
cd paper
job="Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares"
export SOURCE_DATE_EPOCH=1785542400
pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" main.tex
```

The three-pass route is supported by MiKTeX-pdfTeX 4.23 (MiKTeX 25.12).
A conforming Tectonic build can instead be produced and renamed to the
title target:

```bash
cd paper
export SOURCE_DATE_EPOCH=1785542400
tectonic --keep-logs main.tex
mv main.pdf Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf
```

`main.pdf` is only Tectonic's temporary default output and must not be retained;
the repository ships only the title-named PDF above.

The version-1.2.0 PDF has 34 pages and 412690 bytes.
Its SHA-256 is
`3f1ee5f4af8757b25ec4bd908ffca3224f87a84d4e546111519c714b195121f7`.

The PDF is not part of the source manifest because different conforming
TeX engines may produce different bytes.

## Complete smooth-support catalogue

Run both verifiers for the whole manuscript. The original command above
covers its original certificate families; the following covers the
smooth-support theorem (`main:smoothsupport`) in Section 3.

```bash
python -B scripts/verify_smooth_support.py
python -B -O scripts/verify_smooth_support.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

Expected: `PASS`; 3649 ABC witnesses; 12/62/232 primitive triangles;
9/39/133 area squareclasses; zero midpoint hits in 4/36/180 pair tests;
3/45/384 primitive D4 classes. The 22 tests include deliberate certificate
corruptions and the Aebi squareclass arithmetic. Normal and optimized modes
produce the same exact result. The default expected receipt under
`certificates/smooth_support/` is required; absence or type/value drift fails.

To regenerate every witness independently (about half a minute, machine
and Python dependent), use a separate output directory:

```bash
python -B scripts/produce_smooth_support.py --out <scratch-directory>
python -B scripts/verify_smooth_support.py --certificates <scratch-directory>
```

The producer and verifier use different triangle-enumeration directions
and different D4 implementations. No downloaded dataset or external CAS is
needed. Global completeness imports von Känel–Matschke, Theorem A, p. 7;
the `10^10` generation bound is not a global height proof. See
`docs/SMOOTH_SUPPORT.md` and `docs/SOURCE_LOCK.md` for the normalization and
source boundary. The exact finite replay does not repeat the source's
original sieve or constitute independent specialist review of the paper.
