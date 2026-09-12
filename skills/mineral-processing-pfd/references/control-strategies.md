# Control Strategies for Comminution Circuits

What to draw when the user asks for a **control strategy** on a crushing or grinding flowsheet.
Vocabulary follows `CONTEXT.md`: a *control loop* is one measurement → controller → final element
chain; a *control strategy* is the tiered set of loops for one circuit; the *control tier* is basic /
intermediate / advanced; the *control narrative* is the table delivered with the drawing; the *final
element* is what the controller moves — in comminution usually a drive speed or crusher setting, not
a valve.

Every row below is derived from `docs/research/comminution-control-strategies.md` (the primary-source
extraction; section references in the **Source** column point into it). Claims that file could only
reach through a search snippet are marked *(snippet)* there and are not relied on here.

## Tier definitions (research §1, ADR 0004)

| Tier | What it is | Drawn as |
|---|---|---|
| **basic** | Regulatory layer: single-loop PID on the primary process variables. The default when the user names no tier — assume it and say so. | Ordinary ISA-5.1 loops: transmitter → controller `bubble` → final element |
| **intermediate** | Enhanced regulatory: cascade, ratio, feedforward and override/constraint loops *added on top of* the basic loops. | Masters landing on the setpoint side of the slave controllers (`pfd-generator` cascade convention) |
| **advanced** | Supervisory/optimising layer (expert system or MPC) that writes setpoints down to the intermediate layer. Never drawn unless asked. | One `supervisory_block` per circuit + `softlink` signals to the controllers it drives *(primitives not yet shipped — later ticket)* |

Tiers are **cumulative**: a higher tier never removes or replaces a lower-tier loop, so each tier's
table lists only what that tier *adds*.

### Final-element classes

| Class | Meaning | Primitive the controller's signal terminates on |
|---|---|---|
| **DRIVE SPEED** | Feeder, mill or pump variable-speed drive | `motor()` — returns its signal landing point; controller letters `SC`/`SIC` or the process controller (`WIC`, `LIC`) writing to the drive directly |
| **VALVE** | Water (process, dilution, inlet) control valve | `cvalve()` |
| **CRUSHER SETTING** | Closed-side setting (CSS) / hydroset | `ZIC` bubble with a `sig` ending on the crusher body — no dedicated primitive *(crushing rows: later ticket)* |
| **MONITOR** | Transmitter + indicator/alarm only; **no final element** | Indicator bubble (`JI`, `PI`, `AI`); the narrative must say "monitor", not oversell it as a loop |

### ISA-5.1 letters (research §1, "ISA-5.1-2009 letters")

A analysis · F flow · J power · L level · P pressure · S speed · W weight/force · Z position; succeeding
C control · I indicate · T transmit · V valve · Y compute/relay. **D is "user's choice"** in Table 4.1 —
density is the conventional assignment, so any drawing with a `DT`/`DIC` must carry the legend
declaration (`legend(..., density=True)`). `SC`/`SIC` is formed by the ordinary rules. The retrieved
pages of ISA-5.1 do not include the cascade-drawing clause, so master/slave drawing follows the
existing `pfd-generator` convention (master signal lands on the slave controller, marked "SP").

### Loop tag numbering

100-series for crushing, 200-series for grinding (SAG and ball mill/cyclone share the 200 range),
matching the shipped examples' `LV-201` / `WIC-201` style.

---

## Circuit 1 — Primary / secondary crushing with closed-circuit screen (research §2)

### Basic tier

*Not yet written — a later ticket appends the rows here (crusher load → feeder speed, cavity level →
feeder speed, CSS in setting or load mode as **one** controller, surge-bin level, belt-scale monitor).*

### Intermediate tier — additions only

*Not yet written.*

### Advanced tier — supervisory block

*Not yet written.*

---

## Circuit 2 — SAG mill (research §3)

### Basic tier

| Loop | Tag scheme | Measured variable (ISA letters) | Controller | Manipulated variable → final element (class) | Objective | Cascade role | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Fresh feed rate | `WT/WIC-2x1` | Belt-scale tonnage on the mill feed conveyor (`WT`) | `WIC` | Feeder speed → feeder `motor` (**DRIVE SPEED**) | Hold ore feed at setpoint | Slave when a load master exists | `WT` on a lead from the conveyor belt; `WIC` above it; signal to `motor(port="top")` on the feeder | §3.1 [Forbes&Gough p.7] |
| Mill inlet water | `FT/FIC-2x2` | Water flow (`FT`) | `FIC` | Water control valve (**VALVE**) | Hold inlet water at setpoint | Slave of the water-to-ore ratio (intermediate) | Water header along the bottom, `cvalve(actuator="above")`, joins the feed chute at a `junction` | §3.1 [LeRoux2019 p.14] |
| Mill load | `WT/WIC-2x3` (load cells) or `PT/PIC-2x3` (bearing pressure) | Mill weight or bearing oil pressure | `WIC` / `PIC` | Feed-rate setpoint of the fresh-feed `WIC` → feeder `motor` through it (**DRIVE SPEED**) | Keep mill load in its target range | Master over the fresh-feed loop | Transmitter on a lead from the shell; controller beside the feed `WIC`; one horizontal signal landing on the feed `WIC`, marked "SP" | §3.1, §3 key statements [Forbes&Gough pp.6–7; LeRoux2019 p.10] |
| Mill power | `JT/JI-2x4` | Motor power kW (`JT`) | `JI` (+ high alarm) | — (**MONITOR**) | Do not exceed maximum power | — | `JT` on a lead from the shell, `JI` above it; no outgoing signal | §3.1 [Forbes&Gough p.6] |
| Mill speed *(only if VSD)* | `ST/SIC-2x5` | Fraction of critical speed (`ST`) | `SIC` | Mill drive VSD → mill `motor` (**DRIVE SPEED**) | Operator-set speed target | — | `motor` on the mill trunnion drive end; omit entirely on a fixed-speed mill and say so | §3.1 [LeRoux2019 p.37] |
| Pebble crusher *(optional)* | `JT/JIC` or `PT/PIC` → `ZIC-2x6` | Crusher power or hydroset pressure | `JIC`/`PIC` → `ZIC` | CSS (**CRUSHER SETTING**) | Run in power/pressure-limited mode | — | `ZIC` with a `sig` ending on the crusher body | §3.1 [Hulthen2010 p.23] |
| Pebble recycle tonnage *(optional)* | `WT/WI-2x7` | Belt scale on pebble return | `WI` | — (**MONITOR**) | Measurement for feedforward at higher tiers | — | Indicator only | §3.1 [Gough p.7; HoneywellSAG p.5] |

Caveats for the SAG basic tier:

- **One feeder drive, two loops.** Fresh feed rate and mill load both act on the feeder. At the
  basic tier draw the load controller's output landing on the feed-rate controller (the "adjust mill
  feed rate to maintain mill weight" strategy of research §3); the intermediate tier formalises it as
  a cascade and adds the power/bearing-pressure override and feedforward, so those rows go there.
- **Power is a monitor at the basic tier.** The high-limit *override* on feed is an intermediate
  addition — do not draw a `JIC` writing to the feed loop at basic.

### Intermediate tier — additions only

*Not yet written — later ticket (load → feed cascade formalised, water-to-ore ratio `FFC`,
power/bearing-pressure override on feed, feedforward from pebbles/size/speed, ball addition ratio).
Note when writing it: the basic row above already lands the load controller on the feed `WIC`
setpoint, so the cascade row should say what it adds (override, feedforward), not redraw the landing.*

### Advanced tier — supervisory block

*Not yet written — one `supervisory_block` ("SAG MILL OPTIMISER (MPC)") with `softlink` to the feed
`WIC`, speed `SIC` and water-ratio `FFC`.*

---

## Circuit 3 — Ball mill + hydrocyclone closed circuit (research §4)

### Basic tier

| Loop | Tag scheme | Measured variable (ISA letters) | Controller | Manipulated variable → final element (class) | Objective | Cascade role | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Ball mill fresh feed *(only if separately fed)* | `WT/WIC` | Belt-scale tonnage (`WT`) | `WIC` | Feeder speed → feeder `motor` (**DRIVE SPEED**) | Hold feed at setpoint | Slave at higher tiers | As for the SAG fresh-feed loop; omit in a SAG-fed circuit | §4.1 |
| Mill inlet water | `FT/FIC` | Water flow (`FT`) | `FIC` | Water valve (**VALVE**) | Hold flow at setpoint | Slave of ratio | As for the SAG inlet water | §4.1 |
| Sump level | `LT/LIC-2x5` | Cyclone feed sump level (`LT`) | `LIC` | **Either** sump dilution water valve (**VALVE**) **or** cyclone feed pump speed → pump `motor` (**DRIVE SPEED**) — see the pairing caveat | Keep the sump from overflowing or running dry | — | `LT` on a lead from the sump wall/rim; `LIC` above; signal to the pump `motor` or the water `cvalve` | §4.1 [LeRoux2019 p.11] |
| Cyclone feed density | `DT/DIC-2x6` | Nuclear/Coriolis density on the cyclone feed line (`DT`; **declare D on the legend**) | `DIC` | Dilution water valve (**VALVE**) | Hold cyclone feed density at setpoint | — | `DT` on a lead from the pump discharge riser; `DIC` beside it; signal down to `cvalve(actuator="above")` on the dilution water line; `legend(density=True)` | §4.1 [Mintek p.1] |
| Cyclone feed pressure | `PT/PIC-2x7` (or `PT/PI` as monitor) | Cyclone inlet manifold pressure (`PT`) | `PIC` → pump `motor`, **or** `PI` | Pump speed (**DRIVE SPEED**) when it owns the pump; otherwise — (**MONITOR**) | Keep cyclone feed pressure in its operating region | — | `PT` on a lead from the cyclone feed line near the inlet; if the pump is already taken by level, draw `PI` only | §4.1 [Mintek p.1; LeRoux2019 p.13] |
| Mill power | `JT/JI-2x9` | kW (`JT`) | `JI` | — (**MONITOR**) | Indication/alarm | — | Lead from the shell, indicator above | §4.1 |
| Particle size | `AT/AI-2x8` | On-line PSM on the cyclone overflow (`AT`) | `AI` | — (**MONITOR**) | Measure product size for the higher tiers | — | Lead from the overflow line, indicator beside it, small "PSM" note | §4.1 [MetsoGO] |

Caveats for the ball-mill/cyclone basic tier:

- **Sump level and cyclone feed density cannot both sit on the dilution-water valve** as independent
  single loops (research §4.1 note, [LeRoux2019 p.11]). The circuit has two final elements — the
  dilution water valve and the pump drive — and three candidate variables (level, density, pressure).
  Pick a pairing, draw it, and state it in the narrative and tier note. The shipped example uses
  **level → pump speed, density → dilution water, pressure as a monitor**; the alternative is
  level → dilution water with density held by pump speed, pressure again a monitor. Whichever
  variable is left over is drawn as an indicator at the basic tier and becomes an override or
  cascade at intermediate.
- **D = density must be declared** on the legend whenever a `DT`/`DIC` is drawn (`legend(density=True)`).
- **Monitors are indication only.** Mill power (`JI`), particle size (`AI`) and, in the pairing above,
  cyclone feed pressure (`PI`) have no final element; the narrative says "monitor" for each.

### Intermediate tier — additions only

*Not yet written — later ticket (PSM → pump-speed/density cascade, density → dilution cascade with
level constraint, downstream density cascade, water-to-ore ratio, pump-pressure override).*

### Advanced tier — supervisory block

*Not yet written — one `supervisory_block` ("GRINDING CIRCUIT OPTIMISER (MPC)") with `softlink` to
the feed `WIC`, water `FFC`/`FIC`, sump `LIC`, density `DIC` and pump `SIC`/`PIC`.*

---

## Circuits not covered

Flotation, thickening, filtration and reagent-dosing control strategies are not in this reference.
If the user asks for control on one of those circuits, say that the skill does not yet know those
strategies rather than improvising loops; a single loop the user specifies explicitly on one piece
of equipment (e.g. the thickener level loop in the base-metal example) is still fine to draw.

## Per-circuit tier note

Because tiers can be mixed per circuit, the drawing must carry a note stating which tier each circuit
was drawn at, e.g. `notes(..., "CONTROL STRATEGY", ["Crushing: basic", "Grinding: basic (assumed)"])`.
This is the only place on the sheet that says what the drawn loops represent (ADR 0004).
