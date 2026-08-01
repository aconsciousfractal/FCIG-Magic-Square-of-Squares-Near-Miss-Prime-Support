// Independent Magma gate for the centre-841 bielliptic fibre.
//
// Replayed on the official University of Sydney Magma Calculator:
// https://magma.maths.usyd.edu.au/calc/
// Magma V2.29-8, 2026-07-26.

Q := Rationals();
E := EllipticCurve([
    Q |
    0,
    -1998610598883,
    0,
    7061164703720084163,
    -3994430203629571309037281
]);

print "CENTRE841_BIELLIPTIC_MAGMA_GATE";
vmaj, vmin, vpatch := GetVersion();
print "MAGMA_VERSION", vmaj, vmin, vpatch;
print "CURVE", E;

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
print "TORSION_ORDER", #T;
print "TORSION_INVARIANTS", inv;
pts := [phi(t) : t in T];
print "TORSION_POINTS", pts;
xs := Sort(Setseq({
    Integers()!p[1] : p in pts | not IsIdentity(p)
}));
print "NONZERO_TORSION_X", xs;

epsilon := RootNumber(E);
print "ROOT_NUMBER", epsilon;

assert N eq 222693537175200;
assert rl eq 0 and ru eq 0;
assert r eq 0 and proved;
assert #T eq 4 and inv eq [2, 2];
assert xs eq [707281, 2825761, 1998607065841];
assert epsilon eq 1;

print "ASSERTIONS PASS";
print "STATUS PASS_INDEPENDENT_MAGMA_REPLAY";
