# Dossier B7D_F90 — the degree-90 toolchain and the class `[A_R]`

## Scope

This dossier records the arithmetic toolchain built to decide the class
`[A_R]` of the marked half ideal inside the `S`-class group of a degree-90
number field `F90` — the object that controls the identity-cover arithmetic
of the `n = 5` branch of the lift tower. The decision identity is exact:

```text
[A_R] = 0   <=>   (x(R) - theta) * u = beta^2   for some S-unit u of F90
```

where `theta` is the relative cubic generator of `F90/F30` and `S` lies over
`{2, 72559, infinity}`. All computations in this dossier are exact PARI/GP,
FLINT and Python runs recorded in the project's experiment ledger; **this
dossier is Magma-free** and pins no commercial-CAS transcript.

## Terminal state (declared exactly)

- **`[A_R]` is OPEN.** No witness `u` was found and no separating character
  was exhibited; neither outcome of the decision is claimed.
- **The field is computable** (`E-P41-155`): `F90` is built by the relative
  route — `rnfinit` over the degree-30 base in 276 s, `polredbest` reducing
  the absolute coefficients from 309 to 51 digits — and its maximal order
  is certified at `2` and `72559` with discriminant exactly
  `2^303 * 72559^18` and residue 1 (no other prime divides the index). Six
  frozen ledger invariants were re-derived from the constructed field, and
  the marked half ideal was re-derived inside `F90` as a clean product of
  three unramified degree-one primes with norm
  `742555755443226614699386963220633` (33 digits).
- **The splitting `d90 = dim Cl_S(F30)[2] + dim ker(N)[2]` is proved**
  (`E-P41-156`), with **no Galois hypothesis** — `F90/F30` is not Galois —
  via the norm identity `N(j(x)) = x^3`, which is an automorphism of every
  2-torsion group. It moves half of `d90` into degree 30; it does **not**
  decide `[A_R]`, which lives in the second summand.
- **The short-vector (lattice) route is measured to exhaustion**
  (`E-P41-156`): eleven `idealmin` directions produced no positive witness;
  the measured sensitivity is covolume `10^122.4`, Gaussian heuristic
  `lambda_1 ~ 52.5`, LLL reaching `~74` (a factor `1.4`), while a generator
  with trivial `S`-part would sit at `>= 22.0` — the regime LLL does reach,
  which is why the run was worth doing. The structural finding `F-B9D-02`
  (the shortest element of a principal ideal need not generate it) means a
  lattice **miss can never be read as a negative**, here or in any future
  lattice gate; and PARI exposes no BKZ, so other directions sample at the
  same length. The lever is spent.

## The two route-stop labels

Compressed one-line reminders from the frozen statement inventory; full
statements in the controlling documents; on any divergence the lock wins.

| label | statement (compressed) | role | controlling document |
|---|---|---|---|
| `B6G` | canonical outer-pentad lift is principal (exact degree-12 principality) | route-stop | `docs/PARKER_PO111A_N5_C152B_B6G_PENTAD_COORDINATE_STOP.md` |
| `B6G-D90` | pentad import is redundant: rank stays 9/25, marked vector survives | route-stop | `docs/PARKER_PO111A_N5_C152B_B6G_D90_RELATION_IMPORT_STOP.md` |

## The toolchain (exact facts, with their ledger records)

- **98-coordinate relative local layer** (`C134`–`C143`, re-derived by
  three independent localizations): 30 odd + 64 dyadic (14 + 50) + 4 real
  coordinates, 49 Kummer equations (15 + 32 + 2); the base image vanishes
  in every relative block, so the relative layer is exactly 98-dimensional
  (`E-P41-148`).
- **Dirichlet bookkeeping `84 = 35 + 49`**, with the 49 split as 32
  relative-unit directions plus a rank-17 saturated `ker N` valuation
  lattice with an explicit `Z`-basis (`E-P41-138`).
- **Automatic norm membership** (`E-P41-139`): `N_{F90/F30}(x - theta) =
  f(x)` symbolically, so every elliptic descent image lies in `ker N` with
  no principality assumption; and `N(f'(theta)) = -disc(f)` shows
  `f'(theta)` is not an absolute kernel direction, while the relative
  invisibility lemma (`E-P41-149`) later certifies it as a relative
  `S`-unit direction.
- **Descent supply collapse** (`E-P41-140`, sharpened by the external
  package `E-P41-152`): the 2-descent map is a homomorphism on
  `E(F30)/2E(F30)`, so the whole infinite subgroup `<H, R>` contributes
  exactly four squareclasses, and modulo the `S`-unit `x(H) - theta`
  exactly **one** survives — `[A_R]` itself. Conditional only on `<H, R>`
  being all of Mordell–Weil, which is not known.
- **Compressed representative** (`E-P41-154`): `[A_(R-kH)] = [A_R]` for
  every `k`, and `R - 4H` presents the class on three marked primes of at
  most 19 digits — `{261577, 903557729, 3141764360217174001}` — against
  the original 93-digit support; every marked prime is unramified, degree
  one, with valuation exactly 2.
- **Supply span** (`E-P41-150`/`E-P41-151`): the certified supply
  (`x(H) - theta`, `f'(theta)`) has rank 2 against the 98-dimensional
  relative target; fifteen structurally motivated `S`-unit candidates gave
  no new direction.

## Open gates

- The decision `[A_R]` itself (either outcome).
- `d90` via the proved splitting: the first summand lives in degree 30 —
  measure `bnfinit` on the base before designing on top of it; the second
  summand (`dim ker(N)[2]`) is untouched.
- The Selmer dimension and saturation statements downstream of `d90`.
- The arithmetic dual route (a nontrivial character of `Cl_S(F90)[2]`
  vanishing on all admissible `S`-units and not on `[A_R]`) remains the
  one live lane; everything ruled out is recorded in the exhausted-routes
  catalogue.

## Boundary

No class-group computation in degree 90 is claimed, no witness and no
separating character is exhibited, and every stated exhaustion is a
measured negative with its exact window recorded in the project ledger —
never an impossibility statement. This dossier declares an open state.
