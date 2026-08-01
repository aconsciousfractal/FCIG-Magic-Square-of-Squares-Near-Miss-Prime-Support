\\ PARI/GP 2.17.4 corroboration for the non-load-bearing first quotient
\\ of the x0=841 bielliptic fibre. The fibre closure uses the complementary
\\ rank-zero quotient, not this computation.

E = ellinit([0, 3533043, 0, 1998610598883, 1998607065841]);
r = ellrank(E);
t = elltors(E);

if (r[1] != 3 || r[2] != 3, error("rank bounds are not [3,3]"));
if (t[1] != 4 || t[2] != [2, 2], error("torsion is not [4,[2,2]]"));

print("CENTRE841_FIRST_QUOTIENT_PARI_CORROBORATION");
print("PARI_VERSION ", version());
print("CURVE_A_INVARIANTS [0,3533043,0,1998610598883,1998607065841]");
print("RANK_RESULT ", r);
print("TORSION_RESULT ", t);
print("STATUS PASS_CORROBORATION_ONLY");
quit
