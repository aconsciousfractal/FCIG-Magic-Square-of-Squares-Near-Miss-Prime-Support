# Pre-publication red-team report

## Final verdict

The mathematical package is internally consistent and publishable as a
preprint artifact. No global Parker theorem or priority claim is made.

## Resolved blocking findings

- corrected the degree-four witness attribution from Bremner 1999 to
  Bremner 2001 and explained that adjoining `sqrt(133)` is the present
  degree-four completion of Bremner's eight-square display;
- made the fixed-shadow quotient replay perform the actual substitution
  `x=1/t^2` on the elliptic cubic, with denominators cleared, rather than
  comparing two manually expanded copies of one factorization;
- linked the elliptic cubic, transcript model coefficients and finite-field
  counts inside the verifier;
- corrected the height census to enumerate all five raw partial
  progressions and then reject the two that violate nine-way distinctness;
- aligned the packaged least-shift census with its actual range `n=1..6`;
- labelled every theorem depending on an external rank or point-list record
  as computer-assisted;
- corrected two cell coordinates in the normal-form remark and added a
  published Lutz-Nagell reference;
- normalized `.gp` files to LF and included every shipped source in the
  manifest;
- removed references to private paths, hidden notes and nonexistent task
  matrices from the public paper and repository.
- source-locked Houston's 2016 ownership of the classical seven-line normal
  form and related elliptic construction;
- independently certified the integral line-sum Smith form from exact minors
  and modular ranks, and the fixed-orbit density formula from Haar measure;
- full-text audited Coumbe's published proof, recorded the literal
  `120+120=240` repeated-summand defect, and kept both the possible repair and
  final exclusion explicitly undecided;
- cited Cowan's published density formulation and marked the
  Harrison--Mudgal--Schmidt result as an unrefereed complementary preprint;
- corrected the final independent-review attribution drift in the exact
  quartic witness (`BRE99` to the source-locked `BRE01`) and added a
  regression assertion for that source identifier;
- fixed the missing LaTeX `corollary` environment and froze
  `SOURCE_DATE_EPOCH`, with two byte-identical Tectonic builds.

After that review, one expository remark was added after the orbit-density
corollary. It derives the universal `Beta(1/4,1/2)` push-forward of Haar
probability on `E_d(R)^0`, records the even/odd-component caveat, and cites
DLMF only for the classical lemniscatic integral. It adds no headline or
arithmetic claim and was included in the final build, manifest, leak scan and
boundary-test replay.

## Final pre-push adjudication

A last external consistency pass was checked against the release tree. It
produced the following corrections and explicit dispositions:

- the three still-open specialist claim-use reviews are now stated in the
  public boundary document, consistently with the reviewer quickstart;
- retired certificate names and legacy-path commentary were removed, the
  centre-841 transcript now names its shipped input path, and both Selmer
  transcripts carry an in-band Magma version record; all affected bytes were
  re-frozen and the verifier digest was updated;
- the independent census script no longer describes itself as the first
  public implementation, and the degree-90 dossier separates certified
  reductions from bounded negative search evidence;
- the reproducibility appendix now distinguishes the checked deterministic
  Tectonic build from the supported `pdflatex` route;
- release version/date metadata and temporary-build exclusions were added;
- the LMFDB basis record now has an explicit citation and bibliography item.

Two proposed bibliography restorations were not made: the dropped
Bruin--Stoll/Fisher items are not invoked by the manuscript, while the
Gardner/LaBar history remains explicitly attributed through the cited Bremner
source. Adding decorative references would weaken rather than improve the
claim-to-source map.

## Verification boundary

The verifier fails closed when a frozen certificate is absent or its bytes
change. Its output digest authenticates computed values, while the source
manifest authenticates the verifier logic itself. External Magma and
PARI/GP records are not re-executed by the standard-library replay.

## Remaining non-blocking release choices

The compiled PDF is reproducible from pinned source but is intentionally not
part of the source manifest. Commit signing, release tagging and repository
account metadata are owner-controlled publication choices.

## Final release checks

- normal and optimized verifier replays: `PASS`;
- certificate digest:
  `283DB3886199A93F0C510799AC70973C705F809EFDBA1ABFA2121100747CF1B6`;
- both PARI/GP 2.17.4 inputs reproduce their frozen transcripts exactly;
- quotient-map mutation `(23,65) -> (7,11)` fails at the intended check;
- a fresh Git clone with `core.autocrlf=true` verifies all 56 manifest rows;
- scans of public source, filenames and extracted PDF text find no private
  path, hidden-document reference or project codename;
- the 28-page PDF has no overfull box, undefined citation or unresolved
  reference; SHA-256
  `DA3D8AC5B45F90C35BC8657EB23D72F5CE75E3014FAC2AC72E4A9272954072AE`.
