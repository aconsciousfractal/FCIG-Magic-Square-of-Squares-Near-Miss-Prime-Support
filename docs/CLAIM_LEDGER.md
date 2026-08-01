# Public claim ledger

This table is the complete public claim inventory. It contains no priority
claim and does not rely on documents outside this repository.

| paper result | public evidence | boundary |
|---|---|---|
| seven-line normal form and integral line-sum lattice | proof in Section 2; exact determinant and modular-rank replay | classification of arrays with exactly one failed line; no priority claim for the classical normal form |
| three infinite near-miss mechanisms and orbit density | proofs in Section 3; exact recurrence, bridge and orbit checks; analytic Haar-measure ratio with numerical corroboration | produces `(8,7)` arrays, never a fully magic square of squares; density is by orbit index, not height or all arrays |
| interaction surface | proof in Section 4; saturation and monodromy records | describes the three-transversal interaction; does not determine all rational points |
| fixed-squareclass finiteness | cited theorem and specialization in Section 5 | non-effective; no enumeration follows |
| closed fibre at centre 841 | proof plus frozen Magma rank/torsion record | one fibre only; computer-assisted |
| fixed Bremner shadow | proof plus frozen PARI/GP rank record | one rational line only; computer-assisted |
| finite Kummer-class stop | explicit countercertificate in Section 5 | excludes only obstructions using the separate finite classes |
| support law and `{2,3}` exclusion | self-contained proof and exact replay | necessary support conditions, not a global support bound |
| three-prime exclusion | self-contained proof with Aebi's cited classification | exact support `{2,3,p}` only |
| four-prime frontier | identities, fixtures and frozen rank/Selmer records | no four-prime exclusion is claimed |
| height-47 census | two public enumerators and frozen representatives | finite bound only: 0 classes through 46 and 9 through 47 |

External computer-algebra records are digest-pinned and parsed. The Python
verifier independently replays the surrounding exact algebra but does not
replace the external rank, point-list or Selmer computations.
