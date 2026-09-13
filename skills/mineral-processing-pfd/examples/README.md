# Examples

Sample output from the `mineral-processing-pfd` skill. Open the SVG in a browser or vector editor — all labels are real `<text>` elements, so tags and notes can be edited directly.

| File | Description |
|---|---|
| `base_metal_flotation_flowsheet.svg` | Copper concentrator: ROM ore through crushing, screening, SAG/ball mill grinding, cyclone classification, series rougher + column cleaner flotation, concentrate dewatering, and tailings thickening with a level-control loop. Conceptual, `NOT FOR CONSTRUCTION`. |

| `grinding_circuit_control.svg` | Primary/secondary crushing stage (gyratory → surge bin → 2-deck screen, cone crusher on the oversize) ahead of a SAG → ball mill → hydrocyclone closed circuit, both circuits at the **basic control tier**: crusher load, cavity level and bin level loops on feeder drives (`M`), the crusher-setting loop as a `ZIC` ending on the cone body, a belt-scale monitor; feed-rate and sump-level loops on drives, inlet/dilution water on valves, mill load writing the feed setpoint, power/pressure/PSM monitors; the per-circuit tier note and the ISA "D = density" legend declaration. Built by `build_grinding_circuit_control.py`. Conceptual, `NOT FOR CONSTRUCTION`. |

`build_flowsheet.py` and `build_grinding_circuit_control.py` are the generator scripts — kept alongside the SVGs so a revision is a script edit + re-render, not hand-patching the output.

## Control narrative — `grinding_circuit_control`

Tiers: **Crushing: basic (assumed) | Grinding: basic (assumed)** — no tier was named. Crusher setting is drawn in
setting mode; load mode is the alternative mode of the same `ZIC-103`, not a second loop. Pairing chosen
in grinding: sump level on the pump drive, cyclone feed density on the dilution water; cyclone feed
pressure is therefore a monitor at this tier. Every row traces to `references/control-strategies.md`
(Circuit 1 basic for the 100-series, Circuits 2 and 3 basic for the 200-series).

| Loop tag | Tier | Measured variable | Manipulated variable / final element | Objective | Notes |
|---|---|---|---|---|---|
| JIC-101 | basic | Primary crusher CR-101 motor power, JT-101 | ROM-bin apron feeder FD-101 speed / drive (`M`) — DRIVE SPEED | Keep the primary crusher loaded without stalling | Becomes a constraint/override at intermediate |
| LIC-102 | basic | Cone crusher CR-102 cavity level, LT-102 | Crusher feeder FD-103 speed / drive (`M`) — DRIVE SPEED | Maintain choke feed (full cavity) | On the feeder that feeds this crusher, not the surge-bin feeder |
| ZIC-103 | basic | Cone crusher mainshaft position = CSS, ZT-103 | Hydroset / mantle position on the crusher body — CRUSHER SETTING | Hold constant CSS (setting mode) | One controller, two modes: load mode (PT/JT → ZIC) is the alternative, not a second loop; drawn as a `ZIC` whose output ends on the bowl, labelled "CSS" |
| LIC-104 | basic | Surge bin GE-102 level, LT-104 | Screen feeder FD-102 speed / drive (`M`) — DRIVE SPEED | Keep the bin in range, steady screen feed | — |
| WI-105 | basic | Product tonnage, belt scale WT-105 on CV-103 | — | Measure stage yield | **Monitor**; feedforward source at intermediate |
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
