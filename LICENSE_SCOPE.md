# License scope

Everything authored in this repository is released under the single MIT
`LICENSE`:

| Paths | License |
|---|---|
| `paper/**`, `scripts/**`, `docs/**`, `dossiers/**`, `results/**` | MIT |
| `certificates/**` (verifier certificate, Magma inputs and transcripts authored here) | MIT |
| `README.md`, `README_REVIEWER.md`, `REPRODUCE.md`, `CITATION.cff` | MIT |
| `MANIFEST_SHA256.txt`, `requirements.txt`, `.gitignore`, `.gitattributes` | MIT |

Copyright (c) 2026 Oleksiy Babanskyy.

## Third-party boundary

This package embeds **no third-party source, data, or documents**:

- `scripts/verify.py` constructs every object from scratch with no
  external input; it needs only the Python standard library.
- The files under `certificates/` are this project's own artifacts: the
  frozen expected verifier output, the calculator input files written
  here, and the normalized transcripts of their runs on the official Magma
  Calculator V2.29-8. Magma itself is commercial software of the
  Computational Algebra Group (University of Sydney) and is neither
  included nor required — the verifier only checks digests and parses the
  frozen text.
- **Fituvalu's catalogue tables are not bundled** (license unresolved);
  the paper cites them by locator and digest with download instructions
  (Appendix A/C), per the standing never-bundle rule.
- The entry-side documents (Rabern; Woll; Labruna; Weisenberg), Boyer's
  catalogue pages and Brown's centre records are cited by public locator
  only; **no PDF is redistributed**.
- The classical theorems the paper builds on are used only by **citation**
  and remain the work of their respective authors (Bremner; Sallows;
  Robertson; Lucas; Gardner; LaBar; Caro–García-Fritz;
  Evertse–Schlickewei–Schmidt; Pierrat–Thiriet–Zimmermann; Aebi;
  Flynn–Wetherell; Bruin; Bruin–Stoll; Fisher; Rabern; Woll; Labruna;
  Weisenberg); see `docs/SOURCE_LOCK.md`.

The MIT grant above covers only the original code and prose of this
repository, not those cited results, catalogues, or the Magma software.
