# Residual-cover frontier

## Origin

For the area-30 and area-60 addition curves in Section 8, the shipped Magma
records leave one fake two-Selmer class on each curve. Further explicit
descent reduces the live arithmetic to a residual cover `q_R` over
`K = Q(sqrt(218))`.

## What is proved

- the relevant fake two-Selmer sets are singletons;
- the two descent channels share a common `D4` skeleton;
- the remaining rank is constrained to be either one or two;
- the residual obstruction is represented by one explicit squareclass.

The two load-bearing Magma records are shipped as
`certificates/area30_magma.txt` and
`certificates/area60_magma.txt`; their bytes are
pinned by the manifest and parsed by the verifier.

## Open boundary

No `K`-rational point on `q_R` is exhibited and emptiness is not proved. A
point would give rank two; emptiness would give rank one together with a
nontrivial divisible Tate-Shafarevich class. Nothing in this repository
chooses between those alternatives.
