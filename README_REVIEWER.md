# Reviewer Quickstart

The quick integrity replay is sub-second; mathematical review of the
theory paper is a separate task. The replay uses no external data,
randomness, network access or commercial software. Independent auditing of
the Magma-dependent ranks, point lists and Selmer sets requires Magma or a
separate implementation of those calculations.

1. **Read the paper**: [`Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf`](paper/Near-Miss_Constructions_Interaction_Surfaces_and_Prime-Support_Obstructions_for_the_3x3_Magic_Square_of_Squares.pdf). The spine: the
   seven-line normal form and integral Smith form (Thm 1, §2); the three
   infinite `(8,7)` mechanisms with the complete least-shift law and the
   positive-density elliptic-orbit lift (Thm 2, §3, interval
   analysis in Appendix B); the interaction surface, its saturation and
   the `S5` cone wall (Thm 3, §4); imported finiteness and the closed
   `x0=841` fibre (Thm 4, §5); the fixed Bremner-shadow closure (supporting
   Prop. BB, §5); the finite-class stop (Thm 5, §5); the
   `S`-unit support law with the mod-8 endpoint table and the `{2,3}`
   exclusion (Thm 6, §6); the complete three-prime exclusion (Thm 7, §7);
   the complete smooth-support result and `(9,7)` atlas (Thm 8, §8);
   the arbitrary four-prime frontier (§9); the program
   and the three dossiers (§10); census and provenance (App. A);
   certificates (App. B); reproducibility and data policy (App. C).

2. **Replay the certificates** (Python 3.10+, standard library
   only):

   ```bash
   python scripts/verify.py \
       --output results/verification.json --log results/verification.log
   ```

   One entry point re-derives, with exact integer/rational arithmetic:
   the line-sum Smith data; the retraction identities and the full interval analysis; the
   factor-pair census (n = 1..6) with `t_min = 9, then 6z^2`; the bridge
   divisor check retaining exactly `(23,37,47)` and `(79,65,89)`; the
   elliptic-orbit witnesses `m = 1` and `m = 3` recomputed from the group
   law; and, as numerical corroboration only, the printed orbit-density
   decimal via high-precision `Decimal` quadrature; the Mordell–Weil lock
   transport; the saturation premises and the
   `S5` monodromy data (mod 7 irreducible, mod 29 `[2,1,1,1]`, exact
   discriminant); the `x0=841` quotient algebra and pulled-back t-list;
   the fixed Bremner-shadow quotient, finite-field counts, torsion bound
   and parameter elimination;
   the half-class countercertificate; the torus/endpoint/`{2,3}` replays;
   the three-prime `W=2x-1` forcing; the four-prime fixtures, cores,
   closed fibres and addition-curve algebra; the Section-1 quartic
   witness (Bremner's square over `Q(sqrt3, sqrt133)`) in exact
   quadratic-field arithmetic; and the Appendix-A height census replayed
   from scratch. It ends `PASS`, prints
   `certificate_sha256=283DB388...`, and **fails closed for certificate
   values**: the live
   output must hash to the digest pinned inside the verifier and match
   `certificates/expected_verification.json` byte for byte (also under
   `python -O`); a missing or drifted certificate is a hard failure. The
   source manifest separately authenticates the verifier logic itself.

3. **The frozen external-CAS layer**: results attributed to the official Magma
   Calculator V2.29-8 (two rank-zero quotients, one certified-complete
   point list, the six addition-curve rank pairs, two singleton
   fake-Selmer sets) enter as 13 of the 17 frozen files under `certificates/`
   — 7 output records/certificates plus the 6 exact calculator inputs for
   byte-exact resubmission. The verifier pins each by SHA-256 and
   re-parses the asserted lines; it never runs Magma. The transcripts are
   normalized records, not raw session dumps (`docs/SOURCE_LOCK.md`): to
   audit independently, resubmit any `.m` input at
   `magma.maths.usyd.edu.au/calc/` and compare the asserted values.
   The remaining four files are two reproducible PARI/GP 2.17.4 pairs:
   one corroborates the non-load-bearing rank-three quotient in §5; the
   other supplies the rank-zero interval for Proposition BB. The verifier
   authenticates and parses them but does not execute PARI/GP.

4. **Run the independent census implementation** (a few seconds):

   ```bash
   python scripts/census_reference.py
   ```

   It scans centres and differences, independently of the root-based census
   embedded in `verify.py`, and must report 0 classes at height 46 and 9 at
   height 47, including 2 with nonsquare centre.

5. **Check the manifest**: `MANIFEST_SHA256.txt` covers every shipped
   source byte (see `REPRODUCE.md`); the compiled PDF and `results/` are
   deliberately unpinned (toolchain-dependent / regenerated).

6. **Boundary** (read before citing): `docs/PUBLIC_CLAIM_BOUNDARY.md` and
   the what-this-paper-does-not-claim block of the front matter. In
   particular: the exclusion for primes at most 19 does not settle arbitrary
   four-prime supports; no novelty or firstness is asserted, and three claim-use obligations deliberately
   carried with open human-review gates.

7. **The open objects**: `dossiers/` declares the three terminal states
   exactly (with digest-pinned evidence) and catalogues every exhausted
   route with its boundary.

8. **Check the new complete-support deduction**:

   ```bash
   python -B scripts/verify_smooth_support.py
   python -B -O scripts/verify_smooth_support.py
   python -B -m unittest discover -s tests -v
   ```

   Read `docs/SMOOTH_SUPPORT.md` and the imported Theorem A alongside the
   proof. The checker reconstructs the three triangle/array lists and every
   midpoint test. It requires the frozen expected receipt, rejects damaged
   or incomplete ABC lists, and compares JSON types strictly. This exact
   finite replay does not re-prove the imported completeness theorem.
