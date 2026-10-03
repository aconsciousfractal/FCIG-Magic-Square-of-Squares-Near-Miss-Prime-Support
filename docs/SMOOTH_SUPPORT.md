# Complete smooth-support certificates

Theorem 8 uses a complete S-unit catalogue to make an unbounded statement
about a specified set of support primes. The producer's height cutoff is
not its completeness argument.

## Dependencies and exact conversions

1. von Känel–Matschke, arXiv:1605.06079v1, Theorem A, printed p. 7:
   63, 545, 3649 symmetry classes of `x+y=1` for the first 4, 6, 8 primes.
   Each class is represented uniquely by coprime positive `a+b=c`,
   `a<=b<c`; this includes `(1,1,2)` once. See `SOURCE_LOCK.md`.
2. The producer supplies 3649 distinct valid ABC triples. The checker
   verifies every equation, type, sign, gcd and support. Matching the
   imported global cardinality proves that no additional row is missing.
   The producer's `c<=10^10` cutoff only finds the witnesses.
3. Primitive right triangles correspond to coprime `m>k>0` of opposite
   parity with `m,k,m-k,m+k` all supported. The producer starts with
   `k+(m-k)=m`; the checker starts with `k+m=m+k` and joins the other
   additive record. The algorithms do not import one another.
4. For primitive legs `a,b`, hypotenuse `c`, area `n*h^2` with squarefree
   `n`, normalized roots are `(|a-b|/h,c/h,(a+b)/h)`, with square
   difference `4n` and centre `sigma=c^2/h^2`. Equal-difference
   progressions have the same `n` and common scale. Full magic requires
   three distinct centres with one equal to the average of the other two.
5. Triples in one squareclass yield all candidate seven-line arrays.
   Positivity, nine distinct entries, squareness, root normalization and
   all eight line sums are checked. The producer and checker implement
   D4 differently. The failed diagonal and fixed central entry distinguish
   the three possible central roles, modulo symmetry and square scaling.

| Largest prime | ABC classes | Triangles | Squareclasses | Midpoint pairs | Hits | Primitive `(9,7)` D4 classes |
|---|---:|---:|---:|---:|---:|---:|
| 7 | 63 | 12 | 9 | 4 | 0 | 3 |
| 13 | 545 | 62 | 39 | 36 | 0 | 45 |
| 19 | 3649 | 232 | 133 | 180 | 0 | 384 |

The minimum of `|seven-line sum - failed sum| / |difference|` for the last
atlas is `347984603/9837828000`, attained by one class, already in the
prime-13 atlas. It is not a percentage error or an unrestricted record.
These arrays have nine squares; the original `(8,7)` census is different.

## Files and replay

- `certificates/smooth_support/abc_S19.json`: locally generated witnesses.
- `triangles_S*.json`: complete primitive triangle lists.
- `atlas_9_7_S*.json`: canonical primitive roots, differences, squareclasses
  and originating Euclid pairs.
- `expected_verification.json`: frozen expected receipt.
- `scripts/produce_smooth_support.py`: bounded witness producer.
- `scripts/verify_smooth_support.py`: independent reconstruction and strict
  receipt comparison; the default expected receipt is mandatory.
- `tests/test_smooth_support.py`: corruptions, positive controls and exact
  arithmetic of the Aebi squareclass consequence.

Run the commands in `REPRODUCE.md`. The checker uses integers and `Fraction`;
checks remain active under `-O`. ABC booleans and floats are rejected, JSON
duplicate keys fail, and derived files/receipts compare types as well as
values. `1`, `1.0` and `true` cannot substitute for one another.

On 2026-10-03 all 3649 regenerated witnesses also matched the primary
authors' data in a read-only comparison. Their data and code are not
redistributed. The mathematical input is their theorem; its original
height proof and computation are not independently reproduced here.

## Boundary

No full-magic interaction survives when all difference primes are at most
19, with arbitrary exponents. Both transversal differences of any
hypothetical fully magic square must therefore have a prime at least 23.
This does not concern entry factors or require two different large primes.
Fifteen specific four-prime supports are excluded; arbitrary four-prime
supports and the general problem remain open. The unrestricted
fixed-squareclass finiteness theorem is still non-effective. No novelty,
priority, independent specialist review or formal-proof status follows.
