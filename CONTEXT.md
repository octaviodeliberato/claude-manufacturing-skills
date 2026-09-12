# Chemical Manufacturing Skills for Claude

A collection of Claude Skills encoding process/manufacturing engineering practices, so Claude's diagrams and technical output hold up to a practicing engineer's review.

## Language

**Mineral Processing**:
The domain covered by the planned sibling skill to `pfd-generator`: crushing, grinding, sizing, separation, and dewatering of mined ore, per Iran Standard No. 508 (2010), *Standard Symbols for Mineral Processing Flowsheets*.
_Avoid_: Ore dressing (the standard's own Persian-language synonym, and the working branch name — keep it as a recognized trigger phrase in the skill's `description`, but don't use it as the canonical term in docs/prose).

**Equipment class code**:
The `XX-YY` two-letter-pair code (e.g. `ML-BA`, `CL-HY`) Iran Standard No. 508 uses to identify an equipment symbol in its Chapter 3 tables. Used internally in `mineral-processing-pfd` as the lookup key from code to drawing primitive — never surfaced on the drawing itself. Distinct from the standard's full equipment tag format (`NNLL-LL-LLNN`, Chapter 2), which this skill does not use at all — drawn equipment gets a plain name or a simple per-drawing tag instead, the same way `pfd-generator` labels vessels.

**Mill charge**:
What a grinding mill (SAG, ball) contains and tumbles: the grinding media plus, in a SAG mill, the ore itself. Drawn heaped along the bottom of the mill shell. "Grinding media" alone means only the steel balls/rods, which is the whole charge of a ball mill but only part of a SAG mill's — say *charge* when talking about what the mill symbol depicts.

**Trunnion**:
The hollow bearing journal at each end of a grinding mill through which feed enters and product discharges. On a flowsheet the trunnions are the mill's only connection points: feed at the left trunnion, discharge at the right.

**Deck**:
One screening surface (mesh) inside a vibrating screen. Every deck has its own **oversize** stream; only the bottom deck's throughput is the screen's **undersize**. A multi-deck screen therefore has *deck count + 1* product streams, and a flowsheet that shows fewer is wrong.

**Oversize / Undersize**:
Material retained on a screen deck (oversize) versus passing through it (undersize). In a closed crushing circuit every deck's oversize returns to the crusher; the undersize is the circuit product.
