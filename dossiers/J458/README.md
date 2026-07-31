# Dossier J458 — the residual class `q_R` and the decision `q_R(K)`

## Scope

This dossier records the descent chain growing out of the area-30/60
covering classes of Section 8 of the paper. There, two-cover descent on the
integral models of the addition curves `H_{n,a}` for the Aebi core areas 30
and 60 leaves a **singleton** fake two-Selmer set on each (the untruncated
transcripts ship in [`../../certificates/`](../../certificates/) as
`parker_po105_full_class_a30_magma_v2_29_8.txt` and
`parker_po105_full_class_a60_magma_v2_29_8.txt`, digest-checked by the
verifier). The chain below develops those unique covering classes through
explicit higher descents — norm coverings, torsor Selmer cosets, an affine
Cassels–Tate reduction, explicit radical rows, and a common `D4` skeleton —
down to a single residual class `q_R` over `Q(sqrt(218))`.

## Terminal state (declared exactly)

**Open at exactly the decision `q_R(K)`, and nothing in this dossier decides
it:**

- a `K`-point on the residual cover gives **rank two**;
- emptiness gives **rank one with a nontrivial divisible element of the
  Tate–Shafarevich group**.

The controlling obligation `PO-105` is **OPEN**. The subsidiary obligation
`PO-109` (coordinate kernel and model isomorphisms behind the
256-presentations/64-classes count) is open. No rational point, no
emptiness proof, and no rank value is claimed.

## The chain (14 labels)

Compressed one-line reminders from the frozen statement inventory; the full
statements live in the named controlling documents of the project, and on
any divergence the frozen lock wins.

| label | statement (compressed) | role | controlling document |
|---|---|---|---|
| `S` | full Selmer norm-covering reduction: fake two-Selmer of area-30/60 curves is a singleton | supporting | `docs/FULL_SELMER_NORM_COVERING_REDUCTION.md` |
| `T` | selected-channel rank-two stop | route-stop | `docs/SELECTED_CHANNEL_RANK_STOP.md` |
| `U` | explicit alternative residual-cover frontier | open-frontier | `docs/ALTERNATIVE_RESIDUAL_COVER_FRONTIER.md` |
| `V` | J458 norm-fibre collapse 512->128 to one two-isogeny channel; Selmer 64/4 | supporting | `docs/J458_NORM_ISOGENY_FRONTIER.md` |
| `W` | unique everywhere-local J458 torsor Selmer coset (1,1) | supporting | `docs/J458_TORSOR_SELMER_COSET_THEOREM.md` |
| `X` | affine Cassels-Tate reduction to two radical rows (30/2 split) | supporting | `docs/J458_CASSELST_TATE_RESIDUAL_THEOREM.md` |
| `Y` | explicit identification of the two radical rows (q4/q85) | supporting | `docs/J458_EXPLICIT_RADICAL_ROWS_THEOREM.md` |
| `Z` | common D4 skeleton; CT kernel dim 3; rank in {1,2}; unique radical qR | supporting | `docs/J458_COMMON_D4_SKELETON_THEOREM.md` |
| `AA` | qR pushout squareclass 17; single model-4 reduction with two-way birational maps | supporting | `docs/J458_QR_PUSHOUT_MODEL4_THEOREM.md` |
| `AB` | normalized qR affine origin; exactly four surviving absolute twists | supporting | `docs/J458_QR_AFFINE_ORIGIN_THEOREM.md` |
| `AC` | complementary local survival: 64-class everywhere-locally-soluble fibre per twist | supporting | `docs/J458_QR_COMPLEMENTARY_PUSHOUT_THEOREM.md` |
| `AD` | literal phi-Selmer basis compatibility (64/4; rank-six matrices) | supporting | `docs/J458_QR_SELMER_BASIS_COMPATIBILITY_THEOREM.md` |
| `AE` | filtered-Selmer stabilization: Theta_4=0, all later pairings zero | supporting | `docs/J458_FILTERED_SELMER_STABILIZATION_THEOREM.md` |
| `AF` | ordinary Selmer-4 fibre cardinality: 256 presentations = 64 classes | supporting | `docs/J458_FILTERED_SELMER_STABILIZATION_THEOREM.md` |

`AE` and `AF` are exact internal candidates (exact Python computation of the
Fisher rectangular pairings); they carry no commercial-CAS transcript.

## Frozen official-CAS evidence (digest-pinned)

Every Magma-attributed statement above enters the record only as a frozen
transcript of the official Magma Calculator V2.29-8, pinned here by SHA-256
and byte count (project path `results/`):

| transcript | sha256 | bytes | backs |
|---|---|---|---|
| `parker_po105_a30_selected_exact_rank_magma_v2_29_8.txt` | `41c8dafae5545d68ee5db7294f424ecf4577c0da0280e0b643519179c28fe783` | 167 | `T` |
| `parker_po105_alternative_residual_covers_magma_v2_29_8.txt` | `d588703adcca5c4833a2fc7eb42410668ea352fe431bf960f0ec61f0c0f735be` | 997 | `U` |
| `parker_po105_j458_norm_selmer_magma_v2_29_8.txt` | `7600cc7607b5d117059e592ae8c3d6af0dc730b636975a104e14e7f9f14b8156` | 2295 | `V` |
| `parker_po105_j458_four_block_local_magma_v2_29_8.txt` | `7d5f172acf11a0f71c248b8794bc5817b164dde980a93be23c3dddaa2e3ae6a5` | 2968 | `W` |
| `parker_po105_j458_affine_cassels_tate_atomic_magma_v2_29_8.txt` | `f3e28a7c3fb3942db6847685c3a703c024bcf51832ca55fef0ce7715267246c7` | 1044 | `X` |
| `parker_po105_j458_explicit_radical_rows_atomic_magma_v2_29_8.txt` | `4e66544113d9b55e28b8baed6c713b6efb992b3b99d1a003d1f1f4f0ffe52bc2` | 1742 | `Y` |
| `parker_po105_j458_common_d4_atomic_magma_v2_29_8.txt` | `27e89e454fcf107d17757c2c14e46231a262cbee6dd1b2fcec3d6ab9fa5811da` | 1228 | `Z` |
| `parker_po105_j458_qr_pushout_model4_magma_v2_29_8.txt` | `d905b01df94648074388f6d7f23ea00c0a6de9a8e2eb93bf57f8c740d81973ef` | 1358 | `AA` |
| `parker_po105_j458_qr_affine_origin_magma_v2_29_8.txt` | `89d3fcbb74b05f588f113b9a17d18653975a5b05f92d6cc8379890359ea333a8` | 1195 | `AB` |
| `parker_po106_j458_selmer_basis_compatibility_magma_v2_29_8.txt` | `8385e118919e11eface792cd53f5dcf8690ab87a3cf15df83e11b52a5eb1676a` | 928 | `AD` |

`AC` is backed by four per-twist transcripts
(`parker_po105_j458_qr_complementary_pushout_{1,17,458,7786}_magma_v2_29_8.txt`),
each pinned in the project registry `registry/artifacts.yaml`; the four
Magma software stops that produced **no** evidence are recorded in the
exhausted-routes catalogue, not here.

## Open gates

- `PO-105` — the decision `q_R(K)` itself (rank two versus rank one with
  divisible Sha); open on both selected channels (`T`).
- `PO-109` — the coordinate kernel and model isomorphisms behind `AF`.
- `Sel_4` versus Mordell–Weil at the `Y` stage; rational solubility of the
  identified radical rows.

## Boundary

No rational point is exhibited, no emptiness is proved, no rank is decided,
and no priority is asserted for any layer of the chain; the classical
machinery used at every stage is attributed in the controlling documents.
This dossier declares an open state.
