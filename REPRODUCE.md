# Reproducing the certificates

## Requirements

- Python 3.10+ — **standard library only** (see `requirements.txt`; there
  is nothing to install).
- No external data, no network, no randomness, no commercial software.

## Run

```bash
python scripts/verify.py \
    --output results/verification.json --log results/verification.log
```

## Expected result

The run prints one progress line per certificate family and ends in `PASS`
(~0.1 s). It verifies, with exact integer and rational arithmetic:

1. the digest layer: all 13 frozen files under `certificates/` match their
   pinned SHA-256 and byte counts;
2. family 2 (§3 + App. B): the retraction identities as polynomial
   identities modulo the family invariant, the complete interval-analysis
   identity set, the factor-pair census for `n = 1..6` against the frozen
   table (`t_min = 9`, then `6z^2`), the `(23,37,47)`/`(79,65,89)` bridge
   divisor check with the 9291-sum array, and the elliptic-orbit witnesses
   `m = 1` and `m = 3` recomputed from the group law with denominator
   clearing;
3. family 3 (§4): the transversal interaction equation, the LMFDB
   Mordell–Weil lock transport, the saturation premises (including
   `p_C - 2 p_A = -N_B` as an exact identity and the 30 saturated
   factors), and the `S5` monodromy certificate (irreducible mod 7,
   pattern `[2,1,1,1]` mod 29, discriminant `-24364389070416096000`);
4. families 4–5 (§5): the `x0 = 841` bielliptic quotient identity, the
   pulled-back t-list `{0, ±1, ±841, ±1681}`, the parsed rank-zero
   transcript, and the half-class countercertificate
   `delta(Q + 2^n R) = delta(Q) = (7,10,70)` against distinct doubled
   centres;
5. families 6–7 (§§6–7): the torus identity (abstract and on-surface), the
   14-subsum table, the endpoint pigeonhole to `e = 12`, the mod-8 table
   from quadratic residues, the `{2,3}` exclusion replay, the three-block
   and one-interior identities, and the `W = 2x-1` forcing whose only
   cubic hit is `(x, W) = (2, 3)`;
6. family 8 (§8): the edge-factorization identity, both fixtures (area
   210, mixed 30600), the seven balanced cores with their sextic/quotient
   identities and frozen integer models, both closed core-6 fibres with
   their parsed transcripts, the generic secant addition identity, and the
   six `H_{n,a}` curves whose parsed proved rank pairs sum to
   `2,2,3,3,4,5`, with the two singleton fake-Selmer sets.

plus, as family 1, the Section-1 rationality-filter witness — Bremner's
fully magic square of nine distinct squares over `Q(sqrt3, sqrt133)`
(centre `532 = (2 sqrt133)^2`, all eight lines summing 1596), replayed in
exact quadratic-field arithmetic with a biquadratic degree certificate —
and, as family 9, the Appendix-A height census replayed from scratch as a
second independent enumerator (12/13 full progressions at heights 46/47,
unique doubled difference 840, three partial progressions, 18 arrays = 9
exact `D4` classes with 2 centre-nonsquare, and the nine canonical
representatives frozen in the expected output).

The output JSON is byte-identical across runs and under `python -O`. The
run **fails closed**: it requires the live output to hash to the digest
pinned inside the verifier, requires
`certificates/expected_verification.json` to be present, and requires
byte-identity against it — any drift, and any missing certificate, is a
hard failure. The certificate SHA-256 is

```
44581673EF938253410621324A6A5BE946B0C8AE224A11FB51AA0D918B24440C
```

## What is imported rather than replayed

- **Frozen Magma evidence.** The rank/torsion/point-list computations
  attributed in the paper to the official Magma Calculator V2.29-8 ship as
  the transcripts under `certificates/`, together with the exact submitted
  `.m` inputs. The verifier checks digests and re-parses the asserted
  lines; it never executes Magma. The transcripts are **normalized
  records**, not raw session dumps (see `docs/SOURCE_LOCK.md`), so an
  independent audit resubmits the `.m` files at
  `https://magma.maths.usyd.edu.au/calc/` byte-exact and compares the
  **asserted values** (ranks, torsion, point lists, Selmer sets) rather
  than raw transcript bytes.
- **Imported theorems.** The Caro–García-Fritz finiteness core (Thm 4),
  the Evertse–Schlickewei–Schmidt subspace-theorem count (Thm 6), the
  Pinter–Tengely–Zakariás `1 mod 24` input, and Aebi's equal-area triangle
  classification (Thm 7) are cited, never re-proved; see
  `docs/SOURCE_LOCK.md`.
- **Third-party data.** Nothing is bundled. Fituvalu's tables are
  referenced by locator and digest in the paper's appendix; the entry-side
  PDFs (Rabern, Woll, Labruna, Weisenberg) are cited with their public
  locators and were verified against the primaries in the project record.

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
`paper/sections/00..12` plus the inline bibliography (`99_references.tex`
— **no `bibtex`/`biber` pass**). Two `pdflatex` passes resolve the
cross-references and table of contents. `main.tex` sets
`\pdfinfoomitdate=1`, `\pdfsuppressptexinfo=-1` and `\pdftrailerid{}`, so
the build is timestamp-free and byte-stable on a fixed TeX distribution.
Rebuild from `paper/` with the title-named job target:

```bash
cd paper
job="Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares"
pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" main.tex
```
