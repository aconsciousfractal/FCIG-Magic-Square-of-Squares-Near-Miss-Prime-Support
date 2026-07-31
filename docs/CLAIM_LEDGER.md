# Claim Ledger (public package)

One row per claim family shipped with this package, with its verification
pointer and scope caveat. The authoritative scope statement is
`docs/PUBLIC_CLAIM_BOUNDARY.md`. The object is the completion problem of
the 3x3 magic square of squares on its **difference side**: the three
same-difference square progressions of the seven-line normal form and the
prime support of the common difference `2d`.

The Level column records the verification state of each claim in the
project record behind this package (CL5 = internal proof, CL4 = imported
classical/external theorem, CL3 = exact finite certificate); it describes
how each claim is discharged and is **not** an act of promotion — no
priority is asserted for any row, and the claim boundary governs. The
*Verified by* column names the discharging route: a proof in the numbered
paper section, and/or a block of `scripts/verify.py` (frozen certificate
`44581673…`), and/or a frozen Magma transcript under `certificates/`,
and/or an imported source carried in `docs/SOURCE_LOCK.md`.

| ID | Level | Claim | Verified by | Scope caveat |
|---|---|---|---|---|
| M-NF | CL5 | seven-line normal form: every seven-line array = three same-difference APs on the transversal frame, with the failed-antidiagonal bookkeeping and the half-defect converse | proof, paper §2 (Thm 1) | elimination is classical (Lucas-form lineage); no novelty wording |
| M-FAM | CL5 + CL3 | three infinite `(8,7)` mechanisms: retraction family with the complete pair-closing classification of shifts `0<t<C` and the least-shift law `t_min(1)=9`, `t_min(n)=6z_n^2` for `n>=2`; the `delta=840` bridge completion retaining exactly `(23,37,47)` and `(79,65,89)`; the elliptic-orbit lift, primitive at every return | proofs, paper §3 + App. B; `verify.py` family 2 (identities mod the invariant, census n=1..6, bridge divisors, witnesses m=1,3) | carrier is Bremner/Wesolowski's (Boyer catalogue); type 6.VI and row 340545 are Fituvalu's; `(1,29,41)` is Robertson's; claim-use human reviews `PO-081`/`PO-089` deliberately open |
| M-SURF | CL5 + CL3 | the interaction equation (`x1+x2=2x0` on `E^3`); saturated Parker-open model = one irreducible surface of dimension two; the cone map `2A^2=B^2+C^2` has full `S5` monodromy | proofs, paper §4; `verify.py` family 3 (MW lock, saturation premises, S5 data) | smoothness is not claimed; positivity stays semialgebraic, never a polynomial saturation; the wall does not exclude other rational maps |
| M-FIN | CL4 + CL5 + CL3 | fixed-difference finiteness `D^(3r+1)` with exact CM specialization and squareclass passage; the fibre `x0=841` closed completely (computer-assisted: `t in {0,±1,±841,±1681}`, positivity leaves `t=0`) | imported core `CGF25` (§5, labelled); proofs §5; `verify.py` family 4; frozen transcript `e840_bielliptic_fibre_magma_v2_29_8.txt` + machine certificate | the bound is non-effective and yields no enumeration; imported-core human review `PO-094` deliberately open; rank/torsion enter only as the hash-verified transcript |
| M-KST | CL5 + CL3 | the finite-class stop: neither `x(P)` nor the interaction factors through finite Kummer/2-Selmer class triples, at every level `n` | proof §5; `verify.py` family 5 (`delta(Q+2^nR)=delta(Q)=(7,10,70)` vs distinct doubled centres) | rules out pure finite-class obstructions only; representative-level methods not excluded |
| M-SUP | CL5 + CL4 + CL3 | the coupled torus `S`-unit law with the in-paper nondegeneracy proof; the `exp(30^15(3|S|+1))` count; the exact mod-8 endpoint/interior table with the at-least-two-endpoints law; complete exclusion of `supp(2d)={2,3}` **for primitive positive configurations** | proofs §6; imported count `ESS02`; `1 mod 24` input `PTZ15`; `verify.py` family 6 | the count counts, never enumerates; local laws are necessary, not sufficient |
| M-3P | CL5 + CL3 | COMPLETE exclusion of `supp(2d)={2,3,p}` for every prime `p != 3`, **for primitive positive configurations** (three-block collapse; one-interior branch laws; the `W=2x-1` forcing with unique hit `(2,3)`) | proofs §7; `verify.py` family 7 | the equal-area triangle classification layer is Aebi's; no priority for the join; nothing extends to four primes |
| M-4P | CL5 + CL3 | four-prime frontier: edge factorization with two anti-overreach fixtures; balanced-dropout reduction (seven cores); central and outer core-6 branches empty **on the positive distinct locus** (computer-assisted); six addition curves with proved Jacobian ranks 2,2,3,3,4,5 and singleton fake two-Selmer sets for areas 30/60 | proofs §8; `verify.py` family 8; frozen transcripts (`parker_balanced_core6_fibre…`, `parker_po104_outer_core6_gate…`, `parker_po104_central_mw_gate…`, `parker_po105_full_class_a30/a60…`) | **states the frontier; no four-prime exclusion is claimed**; the singleton classes are a target, not a result |
| M-CEN | CL3 | the frozen `(8,7)` height census: 0 classes at height 46, exactly 9 at 47 (two centre-nonsquare), unique difference 840; Brown provenance correction | App. A + `verify.py` family 9 (the census replayed from scratch as a second enumerator; the nine canonical representatives are frozen in the expected certificate) | bounded census at the frozen default bound, corroboration only; never evidence for an unbounded statement; claim-use sits under the open `PO-081` review like the rest of the C/D lane |
| M-TAX | summary (no level) | difference-side taxonomy (eight strata with exact minima, Hall matching conditions), the fail-closed branch compiler, the outer Gaussian reduction | §9 summaries only | **necessary minima and matching conditions, not existence results**; the full statements and certificates remain in the unpublished project record, so no verification level is published for this row; interface closures, not Diophantine ones |

## Non-claims (standing)

- No priority, novelty, or firstness for any statement; dated negative
  searches are recorded as such, never as certificates.
- No four-prime exclusion; no effectivity; no global support-size bound;
  no statement about the frontier gates (`q_R(K)`, odd `n >= 5`, `[A_R]`)
  beyond the dossier records.
- Nothing proves or refutes the existence of a 3x3 magic square of nine
  distinct positive squares.
- Three claim-use human-review gates (`PO-081`, `PO-089`, `PO-094`) are
  deliberately open; the manuscript's wording respects them.
