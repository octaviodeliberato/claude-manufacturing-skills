# Examples

Sample output from the `mineral-processing-pfd` skill. Open the SVG in a browser or vector editor — all labels are real `<text>` elements, so tags and notes can be edited directly.

| File | Description |
|---|---|
| `base_metal_flotation_flowsheet.svg` | Copper concentrator: ROM ore through crushing, screening, SAG/ball mill grinding, cyclone classification, series rougher + column cleaner flotation, concentrate dewatering, and tailings thickening with a level-control loop. Conceptual, `NOT FOR CONSTRUCTION`. |

| `grinding_circuit_control.svg` | SAG → ball mill → hydrocyclone closed circuit with a **basic-tier control strategy**: feed-rate and sump-level loops terminating on a drive (`M`), inlet/dilution water on valves, mill load writing the feed setpoint, power/pressure/PSM monitors, the per-circuit tier note and the ISA "D = density" legend declaration. Built by `build_grinding_circuit_control.py`. Conceptual, `NOT FOR CONSTRUCTION`. |

`build_flowsheet.py` and `build_grinding_circuit_control.py` are the generator scripts — kept alongside the SVGs so a revision is a script edit + re-render, not hand-patching the output.

## Control narrative — `grinding_circuit_control`

Tier: **basic** for the grinding circuit (assumed — no tier was named). Pairing chosen: sump level on
the pump drive, cyclone feed density on the dilution water; cyclone feed pressure is therefore a
monitor at this tier. Every row traces to `references/control-strategies.md` (Circuits 2 and 3, basic).

| Loop tag | Tier | Measured variable | Manipulated variable / final element | Objective | Notes |
|---|---|---|---|---|---|
| WIC-201 | basic | Fresh feed tonnage, belt scale WT-201 on CV-201 | Reclaim feeder FD-201 speed / drive (`M`) — DRIVE SPEED | Hold SAG fresh feed at setpoint | Slave to WIC-203 |
| FIC-202 | basic | SAG inlet water flow, FT-202 | FV-202 — VALVE | Hold inlet water at setpoint | Becomes the slave of a water-to-ore ratio at the intermediate tier |
| WIC-203 | basic | SAG mill load, load cells WT-203 | Setpoint of WIC-201 → feeder drive — DRIVE SPEED | Keep mill load in its target range | Drawn as one "SP" landing on WIC-201; override/feedforward are intermediate additions |
| JI-204 | basic | SAG mill power, JT-204 | — | Do not exceed maximum power | **Monitor** — indication/high alarm only |
| LIC-205 | basic | Cyclone feed sump level, LT-205 | Cyclone feed pump PU-201 speed / drive (`M`) — DRIVE SPEED | Keep the sump from overflowing or running dry | Pairing choice; alternative is level → dilution water |
| DIC-206 | basic | Cyclone feed density, DT-206 on the pump discharge | DV-206 dilution water — VALVE | Hold cyclone feed density at setpoint | ISA letter D declared on the legend (user's choice) |
| PI-207 | basic | Cyclone feed pressure, PT-207 | — | Keep feed pressure in the cyclone's operating region | **Monitor** at this tier; pump-speed override at intermediate |
| AI-208 | basic | Particle size, PSM AT-208 on cyclone overflow | — | Measure product size | **Monitor**; master of a cascade at intermediate |
| JI-209 | basic | Ball mill power, JT-209 | — | Indication/alarm | **Monitor** |

Conceptual only: no setpoints, tuning, controller or transmitter sizing, interlocks or alarm design.
