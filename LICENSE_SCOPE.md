# License scope

Everything authored in this repository is released under the single MIT
`LICENSE`:

| Paths | License |
|---|---|
| `paper/**`, `scripts/**`, `docs/**`, `dossiers/**`, `results/**` | MIT |
| `certificates/**` (verifier certificate and authored Magma/PARI inputs and normalized transcripts) | MIT |
| `README.md`, `README_REVIEWER.md`, `REPRODUCE.md`, `CITATION.cff` | MIT |
| `MANIFEST_SHA256.txt`, `requirements.txt`, `.gitignore`, `.gitattributes` | MIT |

Copyright (c) 2026 Oleksiy Babanskyy.

## Third-party boundary

This package embeds **no third-party source, data, or documents**:

- `scripts/verify.py` constructs its exact arithmetic objects without network
  access and needs only the Python standard library.
- The files under `certificates/` are this project's own artifacts: the
  frozen expected verifier output, calculator inputs written here, and
  normalized transcripts from the official Magma Calculator V2.29-8 and
  PARI/GP 2.17.4. The external systems are neither included nor required for
  the packaged replay: the verifier checks digests and parses frozen text.
- **Fituvalu's catalogue tables are not bundled** (license unresolved). The
  bibliography and public source lock cite the relevant dataset by locator,
  byte count, source commit and digest.
- The entry-side documents, catalogue pages and historical sources are cited
  by public locator only; no third-party PDF is redistributed.
- Imported theorems are used only by citation and remain the work of their
  authors; see `docs/SOURCE_LOCK.md` for the public attribution table.

The MIT grant covers only the original code and prose in this repository,
not cited results, catalogues, Magma or PARI/GP.
