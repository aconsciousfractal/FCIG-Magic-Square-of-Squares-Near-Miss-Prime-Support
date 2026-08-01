print "OUTER_CORE6_MAGMA_GATE";
v1, v2, v3 := GetVersion();
print "MAGMA_VERSION", v1, v2, v3;

Q<t> := PolynomialRing(Rationals());
f := (t+1)*(t+25)*(t+49)*(2*t+1)*(2*t+25)*(2*t+49);
C := HyperellipticCurve(f);

pts, proved := RationalPointsGenus2(
    C : Fast:=true, Bound1:=1000, Bound2:=10000
);

expected := {
    C![0, 1225, 1],
    C![0, -1225, 1],
    C![-1, 0, 1],
    C![-25, 0, 1],
    C![-49, 0, 1],
    C![-1, 0, 2],
    C![-25, 0, 2],
    C![-49, 0, 2]
};

assert proved;
assert pts eq expected;

print "PROVED", proved;
print "NUMBER_POINTS", #pts;
print "RATIONAL_T", [Rationals()!(P[1]/P[3]) : P in pts];
print "POSITIVE_DISTINCT_T", [];
print "ASSERTIONS PASS";
print "STATUS PASS_INDEPENDENT_MAGMA_REPLAY";
