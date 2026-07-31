// Independent Magma gate for P41-C089 / PO-103.
//
// Replayed on the official University of Sydney Magma Calculator:
// https://magma.maths.usyd.edu.au/calc/
// Magma V2.29-8, 2026-07-26.

Q := Rationals();
E := EllipticCurve([Q | 0, -93861, 0, 10406250, 0]);

print "P41_PO103_CORE6_MAGMA_GATE";
vmaj, vmin, vpatch := GetVersion();
print "MAGMA_VERSION", vmaj, vmin, vpatch;

Emin, iso := MinimalModel(E);
print "MINIMAL_MODEL", Emin;

N := Conductor(E);
print "CONDUCTOR", N;

rl, ru := RankBounds(E);
print "RANK_BOUNDS", rl, ru;
r, proved := Rank(E);
print "RANK", r;
print "RANK_PROVED", proved;

T, phi := TorsionSubgroup(E);
inv := AbelianInvariants(T);
print "TORSION_INVARIANTS", inv;
pts := [phi(t) : t in T];
print "TORSION_POINTS", pts;
xs := Sort(Setseq({
    Integers()!P[1] : P in pts | not IsIdentity(P)
}));
print "NONZERO_TORSION_X", xs;

assert N eq 4848480;
assert rl eq 0 and ru eq 0;
assert r eq 0 and proved;
assert #T eq 4 and inv eq [2, 2];
assert xs eq [0, 111, 93750];

print "ASSERTIONS PASS";
print "STATUS PASS_INDEPENDENT_MAGMA_REPLAY";
