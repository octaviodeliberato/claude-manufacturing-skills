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

**Control loop**:
One measurement → controller → final element chain, drawn complete and directional on a flowsheet. The unit a control strategy is built from.

**Control strategy**:
A named, tiered set of control loops for one circuit (crushing, grinding), together with the objective each loop serves. Distinct from an ad-hoc single loop the user asks for on one piece of equipment.
_Avoid_: Control philosophy, automation scheme, instrumentation package

**Control tier**:
The level of a control strategy: **basic** (single-loop regulatory control on the primary process variables), **intermediate** (cascade, ratio and feedforward built on the basic layer), or **advanced** (a supervisory/optimising layer — expert system or MPC — that writes setpoints down to the intermediate layer). Basic is the default when the user names none.
_Avoid_: Level (collides with the process variable), simple/complex

**Control narrative**:
The table that accompanies a drawn control strategy: one row per loop giving its tag, measured variable, manipulated variable and objective. What a reviewer checks the drawing against.
_Avoid_: Control description, functional spec

**Final element**:
What a controller ultimately moves. In comminution circuits it is usually a drive speed (feeder, mill, pump) or a crusher setting, not a control valve.
