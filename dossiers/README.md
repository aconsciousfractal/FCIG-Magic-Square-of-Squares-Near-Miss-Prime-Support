# Dossiers — where the open objects live

Section 9 of the paper declares that the companion repository carries three
dossiers, each stating its terminal condition exactly, together with an
exhausted-routes catalogue. This directory is that record.

| dossier | terminal state (declared exactly in its README) |
|---|---|
| [`J458/`](J458/README.md) | the descent chain out of the area-30/60 covering classes, developed to a single residual class `q_R` over `Q(sqrt(218))`; **open at exactly the decision `q_R(K)`** — a point gives rank two, emptiness gives rank one with a nontrivial divisible Tate–Shafarevich class. `PO-105` is OPEN. |
| [`PO111A_N5/`](PO111A_N5/README.md) | the lift tower (reconstruction covers, `n >= 3`): the `n = 3` branch **closed completely** by certified-complete point lists; the `n = 5` branch developed to two genus-two covers over `Q(sqrt(2))` whose complete fake two-Selmer set has **four classes, none eliminated**, with a saturated rank-two pair-field lattice and conditional elliptic-Chabauty gates. No statement for odd `n >= 5`. |
| [`B7D_F90/`](B7D_F90/README.md) | the degree-90 toolchain: the class `[A_R]` of the marked half ideal in a degree-90 `S`-class group is **OPEN**; the field itself is now computable, the splitting `d90 = dim Cl_S(F30)[2] + dim ker(N)[2]` is proved, and the short-vector route is measured to exhaustion. |

[`EXHAUSTED_ROUTES.md`](EXHAUSTED_ROUTES.md) consolidates every closed route
of this program with its exact boundary, so that no successor re-runs a dead
end.

## Evidence discipline

The dossiers index the project record; they do not restate proofs. Their
label tables reproduce the compressed one-line reminders of the frozen
statement inventory — on any divergence the frozen lock wins, and the full
statements live in the named controlling documents of the project.

**No internal label or path is load-bearing for a reader of this
repository.** The controlling documents named in the tables
(`docs/J458_*`, `docs/PARKER_PO111A_*`, …) and the ledgers they cite live
in the **unpublished project record** behind this package, not in this
tree; the dossiers and the exhausted-routes catalogue are the citable
form of their terminal states. Identifier glossary: `E-P41-nnn` =
experiment ledger entry; `P41-Cnnn` / bare `Cnnn` = claim ledger entry;
`PO-nnn` = proof obligation (gate); letters `S`–`BA` = frozen statement
labels of the project's theorem lock; `F-…` = recorded finding. The
claim levels quoted here (CL3/CL4/CL5) are the taxonomy summarized in
`../docs/CLAIM_LEDGER.md`.

Every computation attributed to the official Magma Calculator V2.29-8 is
identified below by the **SHA-256 digest and byte count of its frozen
transcript**; the two singleton fake-two-Selmer transcripts used by Section 8
of the paper already ship in [`../certificates/`](../certificates/) and are
digest-checked by the verifier. The remaining dossier transcripts are pinned
here by digest; whether they are additionally bundled is an assembly
decision recorded in the repository manifest. The verifier entry point never
requires that software to run.

## Boundary

Nothing in this directory is promoted, and nothing here claims a result
beyond the recorded ones. The dossiers declare open states; the public claim
set of this package is empty.
