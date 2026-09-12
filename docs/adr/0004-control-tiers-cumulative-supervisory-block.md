# Control tiers are cumulative, and the advanced tier is drawn as one supervisory block per circuit

`mineral-processing-pfd` offers a **control strategy** (see `CONTEXT.md`) at three **control tiers** — basic, intermediate, advanced — for crushing and grinding circuits. Two decisions about how those tiers relate to each other and to the drawing are recorded here, because once examples and the reference table exist they are expensive to change.

**Tiers are cumulative.** Intermediate is the basic loops plus cascades/ratio/feedforward built on top of them; advanced is the intermediate layer plus a supervisory/optimising layer that writes setpoints *down to* the intermediate controllers. A higher tier never removes or replaces a lower-tier loop. This mirrors how plants are actually built (the regulatory layer stays in service and is the fallback when the optimiser is off) and lets `references/control-strategies.md` list, per tier, only what that tier *adds*. The alternative — each tier a self-contained scheme that may redraw the regulatory layer differently — was rejected as both less realistic and three times the reference to maintain.

**Advanced is one block, not many bubbles.** The supervisory layer is drawn as a single `supervisory_block` per circuit (rounded rectangle, e.g. "SAG MILL OPTIMISER (MPC)") connected to the setpoint port of each controller it drives by an ISA-5.1 *software/data link* signal style (`softlink`), which is distinct from the dashed electrical signal used by regulatory loops. The alternative — an ISA-5.1 computer-function hexagon on every loop the optimiser touches — was rejected because it multiplies symbols without adding information and makes "advanced" indistinguishable at a glance from a busy "intermediate" drawing. A reader expecting hexagons should look here for why they are absent.

**Consequences:** the drawing must carry a per-circuit tier note ("Crushing: basic · Grinding: intermediate"), because tiers can be mixed per circuit and the note is the only place that states which tier the drawn loops correspond to. The default tier when the user names none is basic, stated as an assumption in the delivery — advanced is never drawn unasked.

## Status

Accepted.
