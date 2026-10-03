# Research-continuation summaries

Appendix C of the paper records three unresolved arithmetic directions;
Section 9 states the main open questions. These dossiers summarize the
research state and identify selected supporting records. They are not
self-contained reproducibility packages for the full continuation proofs.

| Dossier | Exact mathematical boundary |
|---|---|
| [Residual cover](residual_cover/README.md) | One residual covering class over `Q(sqrt(218))`; neither a rational point nor emptiness is proved |
| [Odd lift](odd_lift_n5/README.md) | At coefficient 3, the known generic family's nondegenerate rational specializations satisfying both base reconstructions are excluded; this does not classify all specialized Mordell–Weil points. At coefficient 5, one genus-two cover over `Q(sqrt(2))` is empty on the required real component and the other retains four fake two-Selmer classes |
| [Degree-90 class](degree90_sclass/README.md) | A marked class `[A_R]` in a degree-90 `S`-class group remains undecided; the bounded short-vector search supplies no impossibility theorem |

The rank-two lattice used in the coefficient-5 continuation is saturated
at the tested primes `2,3,5,7`. No rank upper bound, finite index in the
full Mordell–Weil group or full saturation is established by that
calculation. Complete rational-point lists with the required rational
coordinate and a uniform theorem for larger odd coefficients remain open.

The public `scripts/verify.py` checks the main article's support identities
and the area-30/60 singleton fake-Selmer records. It does not reproduce
the residual-cover descent, the higher-lift lattice, the degree-90
calculations or the supplementary support taxonomy.

[EXHAUSTED_ROUTES.md](EXHAUSTED_ROUTES.md) records attempted methods and
their stated computational limits. “Exhausted” refers to those recorded
attempts and domains; it does not exclude every algorithm of the same type.
None of these summaries settles the general magic-square problem.
