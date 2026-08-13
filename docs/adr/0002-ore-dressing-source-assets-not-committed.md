# Source PDF and PNGs for the mineral-processing symbol set are not committed

`assets/PNG Ore Dressing/` holds Iran Standard No. 508 (2010), *Standard Symbols for Mineral Processing Flowsheets*, and 289 PNG icons extracted from it. A licensing fact-check (`docs/research/ore-dressing-symbols.md`, §7) found no copyright notice, public-domain declaration, or reproduction terms anywhere in the document — under default copyright that means unresolved, not cleared for redistribution. `mineral-processing-pfd` already draws its own vector symbols rather than shipping these pictograms (see the skill's design decisions), so nothing in the shipped skill depends on this folder existing in the repo.

**Decision:** `assets/PNG Ore Dressing/` is gitignored, not committed. It stays as private local reference material for whoever is hand-drawing the vector primitives. Don't remove the `.gitignore` entry to "restore" these files into the public repo — the rights question was never resolved, only worked around.

`docs/research/ore-dressing-symbols.md` stays committed: it cites facts (equipment names, codes, page numbers) about the standard, not its graphic symbols.

## Status

Accepted.
