# Reviewer Quickstart

About twenty minutes: a sub-second replay plus reading. This is a theory
paper whose every computation ships as an exact certificate — no external
data, no randomness, no network, no commercial software required.

1. **Read the paper**: the title-named PDF in `paper/`. The spine: the
   seven-line normal form (Thm 1, §2); the three infinite `(8,7)`
   mechanisms with the complete least-shift law (Thm 2, §3, interval
   analysis in Appendix B); the interaction surface, its saturation and
   the `S5` cone wall (Thm 3, §4); imported finiteness and the closed
   `x0=841` fibre (Thm 4, §5); the finite-class stop (Thm 5, §5); the
   `S`-unit support law with the mod-8 endpoint table and the `{2,3}`
   exclusion (Thm 6, §6); the complete three-prime exclusion (Thm 7, §7);
   the four-prime frontier stated exactly and left open (§8); the program
   and the three dossiers (§9); census and provenance (App. A);
   certificates (App. B); reproducibility and data policy (App. C).

2. **Replay the certificates** (~0.1 s; Python 3.10+, standard library
   only):

   ```bash
   python scripts/verify.py \
       --output results/verification.json --log results/verification.log
   ```

   One entry point re-derives, with exact integer/rational arithmetic:
   the retraction identities and the full interval analysis; the
   factor-pair census (n = 1..6) with `t_min = 9, then 6z^2`; the bridge
   divisor check retaining exactly `(23,37,47)` and `(79,65,89)`; the
   elliptic-orbit witnesses `m = 1` and `m = 3` recomputed from the group
   law; the Mordell–Weil lock transport; the saturation premises and the
   `S5` monodromy data (mod 7 irreducible, mod 29 `[2,1,1,1]`, exact
   discriminant); the `x0=841` quotient algebra and pulled-back t-list;
   the half-class countercertificate; the torus/endpoint/`{2,3}` replays;
   the three-prime `W=2x-1` forcing; the four-prime fixtures, cores,
   closed fibres and addition-curve algebra; the Section-1 quartic
   witness (Bremner's square over `Q(sqrt3, sqrt133)`) in exact
   quadratic-field arithmetic; and the Appendix-A height census replayed
   from scratch. It ends `PASS`, prints
   `certificate_sha256=44581673...`, and **fails closed**: the live
   output must hash to the digest pinned inside the verifier and match
   `certificates/expected_verification.json` byte for byte (also under
   `python -O`); a missing or drifted certificate is a hard failure.

3. **The frozen Magma layer**: results attributed to the official Magma
   Calculator V2.29-8 (two rank-zero quotients, one certified-complete
   point list, the six addition-curve rank pairs, two singleton
   fake-Selmer sets) enter **only** as the 13 files under `certificates/`
   — 7 transcripts/certificates plus the 6 exact calculator inputs for
   byte-exact resubmission. The verifier pins each by SHA-256 and
   re-parses the asserted lines; it never runs Magma. The transcripts are
   normalized records, not raw session dumps (`docs/SOURCE_LOCK.md`): to
   audit independently, resubmit any `.m` input at
   `magma.maths.usyd.edu.au/calc/` and compare the asserted values.

4. **Check the manifest**: `MANIFEST_SHA256.txt` covers every shipped
   source byte (see `REPRODUCE.md`); the compiled PDF and `results/` are
   deliberately unpinned (toolchain-dependent / regenerated).

5. **Boundary** (read before citing): `docs/PUBLIC_CLAIM_BOUNDARY.md` and
   the what-this-paper-does-not-claim block of the front matter. In
   particular: no four-prime exclusion, no effectivity, no novelty or
   firstness anywhere, and three claim-use obligations deliberately
   carried with open human-review gates.

6. **The open objects**: `dossiers/` declares the three terminal states
   exactly (with digest-pinned evidence) and catalogues every exhausted
   route with its boundary.
