# Red-team report (public copy)

Two adversarial passes over the assembled manuscript and package, both
2026-07-31, both commissioned by the owner and adjudicated author-side
with every accepted finding **applied before this report was frozen**.
Anchoring: this report describes the package state at the assembly
revision that ships it (see the repository history; the verifier
certificate of that state is `44581673…`, pinned inside
`scripts/verify.py`). Neither pass is a human review: the three human
gates (`PO-081`, `PO-089`, `PO-094`) remain open and are declared in
`PUBLIC_CLAIM_BOUNDARY.md`.

## Pass 1 — author-side assembly red team (internal agent)

Boundary matrix re-run against the full manuscript; two real findings,
both applied:

| id | severity | finding | fix |
|---|---|---|---|
| `F-T15-01` | real | Section 1 promised "an exact verified witness in the companion repository" for the degree-four full solution, but no such witness was shipped | the witness (Bremner's square over `Q(sqrt3, sqrt133)`, centre `532`) is replayed exactly by `verify.py` family 1, with a biquadratic degree certificate |
| `F-T15-02` | attribution | the same sentence read as if the degree-four witness were this project's object | Section 1 names the square as **Bremner's**, with its exact field and centre |

Earlier applied findings remain on record: the four front-matter drifts
(`F-FM-01..04`) and the tooling traps logged in the project history.

## Pass 2 — external agent red team (independent agent, commissioned by the owner)

Independent recomputation confirmed, exactly: the quartic witness (all
eight lines at 1596, nine distinct entries, the four representations of
`532` as `u^2+3v^2`, degree four genuinely needed); the normal-form
theorem re-derived from scratch (antidiagonal forced, normalization
legitimate); the interaction equation under the fully-magic-carrier
hypothesis; the family-2 witness; the manifest (all entries recomputed);
the census numbers of Appendix A (12/13 progressions, 840 unique, 18
arrays = 9 classes, 2 centre-nonsquare); the endpoint/Legendre table; the
`{2,3}` exclusion; the §7 algebra with the `W=2x-1` forcing brute-forced
to `2^30`; the §8 edge identity and the six Aebi areas; the interval
analysis of Appendix B re-derived whole.

Its findings, with dispositions (all accepted ones applied):

| id | finding | disposition |
|---|---|---|
| B1 | §1 tied Bremner's seven-square record to the Appendix-A census (wrong population, an uncitable `10^7` bound, a different height notion) | **applied** — the sentence is removed; the census appendix is the only citable census statement |
| B2 | M-CEN was published CL3 with no shipped census certificate | **applied** — `verify.py` family 9 now replays the census from scratch and freezes the nine canonical representatives in the expected certificate |
| B3 | M-TAX was published CL5 with its proofs not in this tree | **applied** — M-TAX is now a summary row with no published level; §9 states that the full statements remain in the unpublished project record |
| B4 | the ledger's levels contradicted a "claim set is empty" sentence in this report | **applied** — the ledger states its levels describe verification state, not promotion; the contradicting sentence is gone |
| B5 | `PTZ15` had two different author sets across the package | **applied** — adjudicated against the locked primary: Pierrat–Thiriet–Zimmermann (technical note, 2015-03-13); all package files aligned to the bibliography |
| B6 | the promised Fituvalu/Brown locator+digest mechanism did not exist | **applied** — bibliography entries `FIT` (URL, file, bytes, SHA-256, source commit) and `BRO` (MathPages kmath417) added and cited; the public source lock carries the full rows |
| B7 | the claim ledger pinned a stale certificate digest | **applied** — aligned to the current digest (`44581673…`) |
| B8 | the verifier's self-check was fail-open (deleting the expected certificate still yielded `PASS`), contradicting the paper's "fails closed" | **applied** — the digest is pinned as a constant inside `verify.py`, the expected certificate is required to exist and match byte-for-byte, and Appendix C states exactly that; the failure was reproduced before and after the fix |
| high | a specific negative technical statement about Hill's preprint shipped without its supporting audit | **applied** — reduced to "unrefereed; nothing in this paper depends on it" (here and in the source lock); the audit stays in the unpublished record |
| high | seven dropped hypotheses in the ledger and CITATION (primitivity, positivity, the `0<t<C` range) | **applied** — restored in every row and in the CITATION abstract |
| high | `BRE99` is cited from a read-in-full project record but the primary is not archived, and the quartic witness had no source-lock row | **applied** in scope — the source-lock row now names the witness with its page locators; archiving the PDF remains an owner action |
| high | this report was unanchored, with a dangling forward reference | **applied** — anchored above; the reference list is this section |
| medium | ~50 named controlling documents do not exist in this tree; dense internal identifiers | **applied** — the dossiers index now states that no internal label is load-bearing, names the unpublished record explicitly, and carries an identifier glossary |
| medium | two Selmer transcripts lack the version banner; the e840 transcript carries a footer its input does not print; the e840 JSON certificate uses project-relative paths | **applied** — documented in the source lock ("normalized records, not raw session dumps"); the audit instruction now says to compare asserted values |
| medium | `CITATION.cff` declares a release date and repository URL before any release; unsigned commits under a personal email | **recorded** — pre-publication checklist items in the owner decision sheet; the URL is the intended one by design |
| math-1 | the "fourth square progression **with the same common difference**" remark was false (the centre progression has its own difference `E-A`, never `±D`) | **applied** — both remarks corrected, with the one-line distinctness argument in print |
| math-2 | the (L.1) nondegeneracy was asserted by pointer to an unshipped document, whose described method a counterexample falsifies | **applied** — a complete self-contained proof is now in §6 (squareclass argument + interaction-driven collapses, all fourteen subsums), and the verifier carries the collapse identities |
| math-3 | `smooth` appeared in Theorem 3 without a proof | **applied** — removed everywhere; the claim is irreducibility, dimension two and the degree-eight integral extension |
| math-4 | the EG branch formula read `t = C-u^2` instead of `t = E-w^2` | **applied** — corrected (the verifier had it right) |
| math-5 | "at least two endpoints at `p`" was never derived and the endpoint/interior dichotomy was stated vacuously | **applied** — §6 now derives it: an interior index puts `p` in every root of its progression, so primitivity forbids three interior indices, and the tropical tie forces the second endpoint |
| math-6 | Theorem 4(ii) and the §8 rank layer lacked a computer-assisted label at statement level | **applied** — Theorem 4(ii) now opens with the label, as 4(i) does for its import; the §8 propositions already carried the transcript clause in their statements |

External verdict on the three human gates: the text respects them; the
reviewing agents recorded explicitly that agent reviews **cannot close**
`PO-081`, `PO-089` or `PO-094`.

## Standing limits

These are agent passes plus their mechanized residue (the project suite
and `scripts/verify.py`); they are not human reviews, and the three human
gates remain open by the owner's recorded decision, with the manuscript
keeping the cautious claim-use wording they require. No priority is
claimed anywhere; the claim ledger's levels record verification state,
not promotion.
