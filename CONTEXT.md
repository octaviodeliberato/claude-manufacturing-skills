# Chemical Manufacturing Skills for Claude

A collection of Claude Skills encoding process/manufacturing engineering practices, so Claude's diagrams and technical output hold up to a practicing engineer's review.

## Language

**Mineral Processing**:
The domain covered by the planned sibling skill to `pfd-generator`: crushing, grinding, sizing, separation, and dewatering of mined ore, per Iran Standard No. 508 (2010), *Standard Symbols for Mineral Processing Flowsheets*.
_Avoid_: Ore dressing (the standard's own Persian-language synonym, and the working branch name — keep it as a recognized trigger phrase in the skill's `description`, but don't use it as the canonical term in docs/prose).

**Equipment class code**:
The `XX-YY` two-letter-pair code (e.g. `ML-BA`, `CL-HY`) Iran Standard No. 508 uses to identify an equipment symbol in its Chapter 3 tables. Used internally in `mineral-processing-pfd` as the lookup key from code to drawing primitive — never surfaced on the drawing itself. Distinct from the standard's full equipment tag format (`NNLL-LL-LLNN`, Chapter 2), which this skill does not use at all — drawn equipment gets a plain name or a simple per-drawing tag instead, the same way `pfd-generator` labels vessels.
