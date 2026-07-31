# Dossier PO111A_N5 — the lift tower (`n >= 3`)

## Scope

This dossier records the reconstruction covers of the transversal frame —
the lift tower entered from the outer-primitive double cover summarized in
Section 9 of the paper. The tower stratifies the two-primitive-AP outer
branch by the first vertical coefficient `n`; its skeleton is a `D8` action
with a Kummer quotient and genus-five fibres, and its arithmetic descends
through explicit elliptic and genus-three characters to specialized
genus-two curves.

## Terminal state (declared exactly)

- **`n = 3` is closed completely in this dossier**: the first vertical
  coefficient `n = 3` admits no nondegenerate lift, by certified-complete
  rational-point lists on both genus-two quotients (`AR`).
- **`n = 5` is developed, not closed**: over `K = Q(sqrt(2))` the branch
  reduces to two genus-two covers `D+` and `D-`; the complete fake
  two-Selmer set of `D+` has **four classes, none eliminated** (`AX`), and
  `D-` is empty on the live real branch `T >= 2` (`AW`). The pair-field
  lattice is saturated of rank two (`C132`), and the elliptic-Chabauty
  gates (`BA`, `C130`, `C131`) are conditional on finite-index Mordell–Weil
  control over the absolute degree-30 field — the sole active blocker.
- **No statement is made for odd `n >= 5`** beyond the structural ladder
  (`AS`): the reciprocal structure persists but the genus grows, and the
  `n = 3` mechanism does not.

## The chain (21 labels)

Compressed one-line reminders from the frozen statement inventory; the full
statements live in the named controlling documents of the project, and on
any divergence the frozen lock wins.

| label | statement (compressed) | role | controlling document |
|---|---|---|---|
| `AJ` | PO-111A branch/symmetry/fibration skeleton: D8 action, Kummer quotient, genus-5 fibres | supporting | `docs/PARKER_PO111A_BRANCH_QUOTIENT_THEOREM.md` |
| `AK` | F2 elliptic character: minimal model, 6I4+4I0*, E(Q(u))=Z+(Z/2)^2 | supporting | `docs/PARKER_PO111A_FIBRE_E1_THEOREM.md` |
| `AL` | F1F2 genus-three character: V4, three elliptic quotients, degree-8 isogeny, 4I4+4I2 | supporting | `docs/PARKER_PO111A_FIBRE_G3_THEOREM.md` |
| `AM` | primitive quotient sections; explicit (Z/2)^3 kernel; live linkage equations | supporting | `docs/PARKER_PO111A_LIFT_KERNEL_THEOREM.md` |
| `AN` | F2/Kummer compatibility R^2=2X_b; complete MW coset (2k+1)P_b+eps*tau_b | supporting | `docs/PARKER_PO111A_LIFT_F2_COMPATIBILITY_THEOREM.md` |
| `AO` | reconstruction-cover closure on the original-coordinate lane | supporting | `docs/PARKER_PO111A_LIFT_RECONSTRUCTION_THEOREM.md` |
| `AP` | generic odd-coset nonduplicate obstruction: n=+-1 only (division polynomials) | supporting | `docs/PARKER_PO111A_LIFT_NONDUPLICATE_GENERIC_THEOREM.md` |
| `AQ` | specialized-fibre stratification; n=3 obstruction descends to rank-one genus-one curve | supporting | `docs/PARKER_PO111A_SPECIALIZED_FIBRE_STRATIFICATION.md` |
| `AR` | COMPLETE exclusion of the first vertical coefficient (n=3): certified-complete point lists | headline | `docs/PARKER_PO111A_SPECIALIZED_N3_COMPLETE.md` |
| `AS` | all-odd reciprocal structure: F_n reciprocal, terminal quotients K_{n,+-}; n=5 genus 6 | supporting | `docs/PARKER_PO111A_SPECIALIZED_ODD_UNIFORM_STRUCTURE.md` |
| `AT` | n=5 character-Jacobian simplicity: dims 5,6,6,6; no quotient below genus 5 | supporting | `docs/PARKER_PO111A_N5_CHARACTER_JACOBIANS.md` |
| `AU` | n=5 quadratic descent: resultant -2^203, only delta=+-1, two K-simple torsion-free G2 covers | supporting | `docs/PARKER_PO111A_N5_QUADRATIC_DESCENT.md` |
| `AV` | 2-Selmer (Z/2)^3 on both covers; rank intervals [1,3] and [2,3] | supporting | `docs/PARKER_PO111A_N5_G2_SELMER_RANK.md` |
| `AW` | live branch: D_- real-empty on T>=2; projective sieve {2,inf} at p=3,7; genus-23 pullback | supporting | `docs/PARKER_PO111A_N5_LIVE_BRANCH_SIEVE.md` |
| `AX` | complete fake two-Selmer set of D_+: four classes, none eliminated | route-stop | `docs/PARKER_PO111A_N5_DPLUS_FAKE_SELMER_SET.md` |
| `AY` | identity fake-cover reduction: local images leave only the identity cover; sextic S6 | supporting | `docs/PARKER_PO111A_N5_IDENTITY_FAKE_COVER_SIEVE.md` |
| `AZ` | canonical kernel c=S_3; 2<=rank<=3; Cassels-Tate pairing zero | supporting | `docs/PARKER_PO111A_N5_CANONICAL_KERNEL_RANK.md` |
| `BA` | pair-field quartic gate: degree-15 field, factors [2,4], genus-one quartic + Jacobian | computational-gate | `docs/PARKER_PO111A_N5_PAIRFIELD_FACTOR_GATE.md` |
| `C130` | identity pair-field untwisting: d=1, single untwisted quartic w^2=q4(T) | supporting | `docs/PARKER_PO111A_N5_IDENTITY_PAIRFIELD_UNTWISTED_GATE.md` |
| `C131` | explicit elliptic original-T map on the C130 quartic | supporting | `docs/PARKER_PO111A_N5_EXPLICIT_ELLIPTIC_T_MAP.md` |
| `C132` | saturated rank-two pair-field lattice: P+Q=R, P=2H, <H,R> ell-saturated for 2,3,5,7 | supporting | `docs/PARKER_PO111A_N5_PRIMITIVE_MW_LATTICE.md` |

## Frozen official-CAS evidence (digest-pinned)

Every Magma-attributed statement above enters the record only as a frozen
transcript of the official Magma Calculator V2.29-8, pinned here by SHA-256
and byte count (project path `results/`):

| transcript | sha256 | bytes | backs |
|---|---|---|---|
| `parker_po111a_fibre_e1_magma_v2_29_8.txt` | `c81b3efd2f96499d203b4c19c8a9947d4b20245e558bb63abf2f166f5ac5cd0b` | 491 | `AK` |
| `parker_po111a_fibre_g3_magma_v2_29_8.txt` | `015c0c5afdb3707bbfa388eb8c42dca68af3e0fe03292a9bafc2add13106f28b` | 616 | `AL` |
| `parker_po111a_specialized_n3_complete_magma_v2_29_8.txt` | `da50ae651aac114a738ab3022fa9263a8f9d2cb3f25f98ee8cc4c0d496d7d825` | 1161 | `AR` |
| `parker_po111a_n5_g2_selmer_rank_magma_v2_29_8.txt` | `3efce7c1622be289ba91ac8d382d7ccbce5223f49cc234a76a342327af21dde7` | 880 | `AV` |
| `parker_po111a_n5_dplus_fake_selmer_set_magma_v2_29_8.txt` | `d3bbe14a5e464749f28889f57f26095369634f23f6ec2cb258753a6bae5f41a9` | 1824 | `AX` |
| `parker_po111a_n5_pairfield_factor_gate_magma_v2_29_8.txt` | `3df46fcd50fad8c389ab702f793eeac949b1a8e053df3e5e377681b4e85879e5` | 760 | `BA` |
| `parker_po111a_n5_identity_pairfield_untwisted_gate_magma_v2_29_8.txt` | `98df274ffc1466ea1c023075077e734e1c37a06929431f96ec42075c13469511` | 1041 | `C130` |
| `parker_po111a_n5_explicit_elliptic_t_map_gate_magma_v2_29_8.txt` | `5c4706be04d791c8bdd024e006e0c0827df6fc5d5d34b53543956b45f54cdce2` | 1304 | `C131` |
| `parker_po111a_n5_primitive_mw_lattice_gate_magma_v2_29_8.txt` | `22771160534754df421c5cb7f5405ba7af2a18c9d197c73a2538967ed0022cce` | 1504 | `C132` |

The `AX` transcript is explicitly collated from three independently
completed calculator blocks; its byte-stable certificate is part of the
project record.

## Open gates

- `ODD-ARITHMETIC` — any statement for odd `n >= 5`; opened by `AS`, with
  no bounded search admitted.
- Exact ranks on the `n = 5` covers and the rank-three case of `AZ`,
  conditional on finiteness of the relevant Tate–Shafarevich groups.
- Finite-index Mordell–Weil control over the absolute degree-30 pair field
  — the sole active blocker for the conditional elliptic-Chabauty gates
  (`C130`/`C131`/`C132`); recorded timeouts of the automatic routes are in
  the exhausted-routes catalogue.
- No identity-cover emptiness is claimed (`AY`), and no surjectivity back
  to the full cover is claimed (`C130`).

## Boundary

The `n = 3` closure is exactly the exclusion of one vertical coefficient on
one branch; it is not a Parker statement. Nothing here claims a complete
rational-point list on any `n = 5` object, and no priority is asserted for
the classical machinery (division polynomials, quadratic descent,
Bruin–Stoll fake descent, quartic-to-Weierstrass transformations) attributed
in the controlling documents. This dossier declares a developed open state.
