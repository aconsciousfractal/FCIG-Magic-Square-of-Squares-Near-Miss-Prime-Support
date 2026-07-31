print "P41_PO104_CENTRAL_MW_GATE";
v1, v2, v3 := GetVersion();
print "MAGMA_VERSION", v1, v2, v3;

procedure Check(label, n, gx, gy, px, py, qa, qb, expected_qrank)
    print "BEGIN", label;

    E := EllipticCurve([0, 0, 0, -n^2, 0]);
    G := E![gx, gy, 1];
    P0 := E![px, py, 1];
    assert P0 eq -2*G;
    lo, hi := RankBounds(E);
    assert lo eq hi;
    print "CONGRUENT_RANK", lo, hi;
    print "FIXED_CLASS_MINUS_2G", true;

    Eq := EllipticCurve([0, qa+qb, 0, qa*qb, 0]);
    Eqm := MinimalModel(Eq);
    qlo, qhi := RankBounds(Eqm);
    assert qlo eq expected_qrank and qhi eq expected_qrank;
    T, mp := TorsionSubgroup(Eqm);
    assert Invariants(T) eq [2, 2];
    print "ADDITION_SECOND_QUOTIENT_RANK", qlo, qhi;
    print "ADDITION_SECOND_QUOTIENT_TORSION", Invariants(T);
    print "END", label;
end procedure;

Check("A30", 30, -6, -72, 169/4, 1547/8, 1635, 5070, 1);
Check("A60", 15, -15/4, -225/8, 289/16, 2737/64, 5070, 17340, 1);
Check("A180", 5, -4, 6, 1681/144, 62279/1728, 13210, 33620, 2);
Check("A84", 21, -3, -36, 625/16, 13175/64, 19194, 52500, 2);
Check("A504", 14, 18, 48, 4225/144, 241345/1728, 22519, 59150, 3);
Check("A1224", 34, -2, -48, 21025/144, 2964815/1728,
      315809, 714850, 3);

print "ASSERTIONS PASS";
print "STATUS PASS_INDEPENDENT_MAGMA_REPLAY";
