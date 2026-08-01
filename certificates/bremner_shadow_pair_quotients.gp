/* Exact elliptic quotients of the Bremner-shadow line.
   PARI/GP 2.17.4 replay; no GRH flag or conditional class-group routine. */

A = [23, 65, 88, 153];

print("BREMNER_SHADOW_PARI_BEGIN");
print("PARI_VERSION|", version());

/* The first pair already suffices for the global projection theorem. */
E = ellinit([0, -(23^2 + 65^2), 0, 23^2 * 65^2, 0]);
Emin = ellminimalmodel(E);
red = ellglobalred(E);
identified = ellidentify(E);
print("SELECTED_ORIGINAL_AINVS|", E.a1, "|", E.a2, "|", E.a3, "|", E.a4, "|", E.a6);
print("SELECTED_MIN_AINVS|", Emin.a1, "|", Emin.a2, "|", Emin.a3, "|", Emin.a4, "|", Emin.a6);
print("SELECTED_CONDUCTOR|", red[1]);
print("SELECTED_CREMONA|", identified[1][1]);
print("SELECTED_CREMONA_DATABASE_ROW|", ellsearch("345345r4"));
print("SELECTED_TORSION|", elltors(Emin));
print("SELECTED_RANK|", ellrank(Emin));
print("SELECTED_CARD|17|", ellcard(E, 17));
print("SELECTED_CARD|41|", ellcard(E, 41));
print("SELECTED_ANALYTIC_RANK|", ellanalyticrank(Emin));

/* Retain the complete six-pair atlas as a diagnostic.  GP terminates a
   statement at newline, so the nested loop is deliberately one statement. */
for(i = 1, #A, for(j = i + 1, #A, aa = A[i]; bb = A[j]; Ep = ellinit([0, -(aa^2 + bb^2), 0, aa^2 * bb^2, 0]); Epmin = ellminimalmodel(Ep); print("PAIR|", aa, "|", bb); print("PAIR_MIN_AINVS|", Epmin.a1, "|", Epmin.a2, "|", Epmin.a3, "|", Epmin.a4, "|", Epmin.a6); print("PAIR_TORSION|", elltors(Epmin)); print("PAIR_RANK|", ellrank(Epmin))));

print("BREMNER_SHADOW_PARI_DONE");
