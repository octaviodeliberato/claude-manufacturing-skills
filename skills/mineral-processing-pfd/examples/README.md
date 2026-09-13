# Examples

Sample output from the `mineral-processing-pfd` skill. Open the SVG in a browser or vector editor — all labels are real `<text>` elements, so tags and notes can be edited directly.

| File | Description |
|---|---|
| `base_metal_flotation_flowsheet.svg` | Copper concentrator: ROM ore through crushing, screening, SAG/ball mill grinding, cyclone classification, series rougher + column cleaner flotation, concentrate dewatering, and tailings thickening with a level-control loop. Conceptual, `NOT FOR CONSTRUCTION`. |

| `grinding_circuit_control.svg` | Primary/secondary crushing stage (gyratory → surge bin → 2-deck screen, cone crusher on the oversize) ahead of a SAG → ball mill → hydrocyclone closed circuit, **crushing at the basic control tier, grinding at the intermediate tier**. Crushing: crusher load, cavity level and bin level loops on feeder drives (`M`), the crusher-setting loop as a `ZIC` ending on the cone body, a belt-scale monitor. Grinding: the basic loops (feed rate and sump level on drives, inlet/dilution water on valves, mill load writing the feed setpoint, power/PSM monitors) plus the intermediate additions on top — load → feed cascade through a power-override low selector, water-to-ore ratio station, PSM → density cascade, density → dilution-water cascade with a level limiter, pump-pressure override — every master on an `SP` leg into its slave's setpoint port. Per-circuit tier note and the ISA "D = density" legend declaration. Built by `build_grinding_circuit_control.py`. Conceptual, `NOT FOR CONSTRUCTION`. |

`build_flowsheet.py` and `build_grinding_circuit_control.py` are the generator scripts — kept alongside the SVGs so a revision is a script edit + re-render, not hand-patching the output.

## Control narrative — `grinding_circuit_control`

Tiers: **Crushing: basic (assumed) | Grinding: intermediate** — the user named intermediate for
grinding only, so crushing takes the basic default. Tiers are cumulative (ADR 0004): every basic row
is still drawn; the intermediate rows add to it and never re-route it. Crusher setting is drawn in
setting mode; load mode is the alternative mode of the same `ZIC-103`, not a second loop. Pairing
chosen in grinding: sump level on the pump drive, cyclone feed density on the dilution water — which
is why the PSM cascade lands on the density controller and the pressure override on the pump. Every
row traces to `references/control-strategies.md` (Circuit 1 basic for the 100-series; Circuits 2 and
3 basic + intermediate for the 200-series).

| Loop tag | Tier | Measured variable | Manipulated variable / final element | Objective | Notes |
|---|---|---|---|---|---|
| JIC-101 | basic | Primary crusher CR-101 motor power, JT-101 | ROM-bin apron feeder FD-101 speed / drive (`M`) — DRIVE SPEED | Keep the primary crusher loaded without stalling | Becomes a constraint/override at intermediate |
| LIC-102 | basic | Cone crusher CR-102 cavity level, LT-102 | Crusher feeder FD-103 speed / drive (`M`) — DRIVE SPEED | Maintain choke feed (full cavity) | On the feeder that feeds this crusher, not the surge-bin feeder |
| ZIC-103 | basic | Cone crusher mainshaft position = CSS, ZT-103 | Hydroset / mantle position on the crusher body — CRUSHER SETTING | Hold constant CSS (setting mode) | One controller, two modes: load mode (PT/JT → ZIC) is the alternative, not a second loop; drawn as a `ZIC` whose output ends on the bowl, labelled "CSS" |
| LIC-104 | basic | Surge bin GE-102 level, LT-104 | Screen feeder FD-102 speed / drive (`M`) — DRIVE SPEED | Keep the bin in range, steady screen feed | — |
| WI-105 | basic | Product tonnage, belt scale WT-105 on CV-103 | — | Measure stage yield | **Monitor**; feedforward source at intermediate |
| WIC-201 | basic | Fresh feed tonnage, belt scale WT-201 on CV-201 | Reclaim feeder FD-201 speed / drive (`M`) — DRIVE SPEED | Hold SAG fresh feed at setpoint | **Slave** of the load cascade: its setpoint port takes the JY-204 output (`SP`) |
| FIC-202 | basic | SAG inlet water flow, FT-202 | FV-202 — VALVE | Hold inlet water at setpoint | **Slave** of the FFY-202 ratio station at this tier (`SP` on its top port) |
| WIC-203 | basic | SAG mill load, load cells WT-203 | Setpoint of WIC-201 → feeder drive — DRIVE SPEED | Keep mill load in its target range | **Master** of the load → feed cascade; at intermediate its output enters the JY-204 low selector rather than landing on WIC-201 directly |
| JIC-204 / JY-204 | intermediate | SAG mill power, JT-204 (same transmitter as the basic JI-204 monitor) | Setpoint of WIC-201 through the JY-204 low selector — DRIVE SPEED | Cut feed when power runs at its high limit | **Override master** = JIC-204; **slave** = WIC-201. The basic monitor became an indicating controller; JY-204 takes the WIC-203 and JIC-204 outputs, its output is the one `SP` leg into WIC-201 |
| FFY-202 | intermediate | Fresh feed tonnage WT-201 (second branch off the transmitter) | Setpoint of FIC-202 — VALVE (FV-202 through the slave) | Hold mill inlet water at a constant ratio to ore feed | **Ratio master** = FFY-202; **slave** = FIC-202. The WT-201 branch crosses the SAG feed chute once — no re-route exists |
| LIC-205 | basic | Cyclone feed sump level, LT-205 | Cyclone feed pump PU-201 speed / drive (`M`) — DRIVE SPEED | Keep the sump from overflowing or running dry | Pairing choice; alternative is level → dilution water. At intermediate its output reaches the motor through the PY-207 selector |
| PIC-207 / PY-207 | intermediate | Cyclone feed pressure, PT-207 (same transmitter as the basic PI-207 monitor) | Pump PU-201 speed through the PY-207 selector — DRIVE SPEED | Keep cyclone feed pressure in its operating band (no roping/choking) | **Override master** = PIC-207; **slave** = the pump drive. PY-207 takes the LIC-205 and PIC-207 outputs |
| DIC-206 | basic | Cyclone feed density, DT-206 on the pump discharge riser | FV-210 dilution water — VALVE, through the FIC-210 slave at this tier | Hold cyclone feed density at setpoint | ISA letter D declared on the legend (user's choice). **Master** of the dilution-water cascade and **slave** of the PSM cascade (`SP` on its right port from AIC-208) |
| LY-205 / FIC-210 | intermediate | Dilution water flow FT-210 (slave); sump level LT-205 (constraint, second branch off the transmitter) | FV-210 — VALVE | Stabilise cyclone feed density and sump level together | **Master** = DIC-206 through the LY-205 level limiter; **slave** = FIC-210 (`SP` on its top port). The basic DIC → valve leg gained the FIC slave; the valve is retagged FV-210 |
| AIC-208 | intermediate | Particle size, PSM AT-208 on cyclone overflow (same transmitter as the basic AI-208 monitor) | Setpoint of DIC-206 → dilution water — VALVE through the DIC/FIC chain | Hold the cyclone cut size / product grind | **Master** = AIC-208; **slave** = DIC-206. Its `SP` leg crosses the cyclone feed line once to reach the DIC inside the closed-circuit ring |
| JI-209 | basic | Ball mill power, JT-209 | — | Indication/alarm | **Monitor** |

Intermediate rows the reference lists that this sheet does **not** draw, and why: feedforward into
the load master (no pebble-recycle belt scale, ore-size analyser or VSD speed on this flowsheet),
ball addition ratio (no ball charging system drawn), downstream density → CFD setpoint cascade (the
sheet ends at the cyclone overflow, and the DIC-206 setpoint already has one master), ball-mill
water-to-ore ratio (SAG-fed ball mill with no separate water loop), and all crushing intermediate
rows (crushing is at basic).

Signal legs cross a process line in three places — the FFY-202 input over the SAG feed chute, the
AIC-208 setpoint leg over the cyclone feed line, the LIC-205 output over the pump riser. All three
are signal-over-process crossings on straight pipe runs (`layout-rules.md` §2 allows them); there
are no process-line crossings and no signal-to-signal crossings.

Conceptual only: no setpoints, tuning, controller or transmitter sizing, interlocks or alarm design.
