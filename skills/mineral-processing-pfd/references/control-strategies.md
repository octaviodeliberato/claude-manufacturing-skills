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
| **intermediate** | Enhanced regulatory: cascade, ratio, feedforward and override/constraint loops *added on top of* the basic loops. | Masters landing on the setpoint port of the slave controllers; ratio/override/feedforward functions as `Y` bubbles — see "Drawing a cascade, ratio or override" below |
| **advanced** | Supervisory/optimising layer (expert system or MPC) that writes setpoints down to the intermediate layer. Never drawn unless asked. | One `supervisory_block` per circuit + `softlink` signals to the controllers it drives *(primitives not yet shipped — later ticket)* |

Tiers are **cumulative**: a higher tier never removes or replaces a lower-tier loop, so each tier's
table lists only what that tier *adds*.

### Final-element classes

| Class | Meaning | Primitive the controller's signal terminates on |
|---|---|---|
| **DRIVE SPEED** | Feeder, mill or pump variable-speed drive | `motor()` — returns its signal landing point; controller letters `SC`/`SIC` or the process controller (`WIC`, `LIC`) writing to the drive directly |
| **VALVE** | Water (process, dilution, inlet) control valve | `cvalve()` |
| **CRUSHER SETTING** | Closed-side setting (CSS) / hydroset | `ZIC` bubble with a `sig` ending on the crusher body — no dedicated primitive; see "Drawing a crusher-setting loop" under Circuit 1 |
| **MONITOR** | Transmitter + indicator/alarm only; **no final element** | Indicator bubble (`JI`, `PI`, `AI`); the narrative must say "monitor", not oversell it as a loop |

### ISA-5.1 letters (research §1, "ISA-5.1-2009 letters")

A analysis · F flow · J power · L level · P pressure · S speed · W weight/force · Z position; succeeding
C control · I indicate · T transmit · V valve · Y compute/relay. **D is "user's choice"** in Table 4.1 —
density is the conventional assignment, so any drawing with a `DT`/`DIC` must carry the legend
declaration (`legend(..., density=True)`). `SC`/`SIC` is formed by the ordinary rules. Modifier
**F** in the second position = ratio, so a ratio station is `FFY` (computing) or `FFC` (controlling).
The retrieved pages of ISA-5.1 do not include the cascade-drawing clause, so master/slave drawing
follows the existing `pfd-generator` convention — see the next section.

### Drawing a cascade, ratio or override (intermediate tier)

The ISA-5.1 clause on drawing cascade loops could not be sourced (research §1: the retrieved pages
are Tables 4.1 and 5.1.1–5.4.4 only), so this skill follows the convention `pfd-generator` already
uses in its distillation example (`references/isa-conventions.md` §5 there) and that the shipped
grinding example applies:

- **A master's output lands on the slave's setpoint port.** The slave controller bubble has three
  connections — measurement in, setpoint in, output out — on three *different* ports (bottom /
  side / top or the other side), so the setpoint leg can never be mistaken for the measurement.
  Label the leg `SP` beside the arrowhead (`pfd-generator` writes "CASCADE SP" / "remote SP"; the short
  form is the same convention, chosen because comminution sheets carry several cascades in little room). The slave's own output still lands on the final element
  exactly as it did at the basic tier: a cascade adds a bubble and a leg, it never re-routes the
  regulatory loop.
- **Ratio, override and feedforward are `Y` bubbles, never implied by a line.** A ratio station is
  `FFY` (input: the wild-flow transmitter; output: the slave's setpoint), an override/constraint
  selector is `JY`/`PY`/`LY` (inputs: the constraint controller's output and the normal master's
  output; output: the slave's setpoint), a feedforward computer is `WY`/`AY`. Write the function
  beside the bubble in small text ("low select", "ratio", "feedforward") — the letters alone do
  not say which. The constraint's own controller (`JIC`, `PIC`) is an ordinary bubble upstream of
  the selector; if the basic tier drew that variable as a monitor (`JI`, `PI`), the transmitter
  stays and the indicator becomes an indicating controller — nothing is removed (ADR 0004).
- **Signal crossings.** A setpoint leg may cross a *process* line where no small re-route exists
  (`layout-rules.md` §2 — acceptable practice, no jump), and it commonly must: a closed grinding
  circuit is a ring of process lines (sump → pump → cyclone → mill → sump) and the density and
  dilution-water instruments sit inside it while the particle-size analyser sits outside. Signal
  legs may never cross *each other* — re-route, and never drop a loop to avoid a crossing.

### Loop tag numbering

100-series for crushing, 200-series for grinding (SAG and ball mill/cyclone share the 200 range),
matching the shipped examples' `LV-201` / `WIC-201` style. The `1xN` / `2xN` numbers in the tables
below are the shipped example's assignments; SAG and ball-mill/cyclone loops share one sequence, so
optional loops (mill speed, pebble crusher) take the next free number rather than a fixed one.

---

## Circuit 1 — Primary / secondary crushing with closed-circuit screen (research §2)

The circuit the rows assume: ROM bin → apron feeder → primary crusher (gyratory or jaw) → conveyor →
surge bin → bin feeder → screen; screen undersize is the stage product (belt scale on the product
conveyor); screen oversize goes to the secondary cone crusher through its own feeder, and the cone
product returns to the surge bin (forward closed circuit). Each feeder has exactly one controller
writing to it — the basic tier has no cascades.

### Basic tier

| Loop | Tag scheme | Measured variable (ISA letters) | Controller | Manipulated variable → final element (class) | Objective | Cascade role | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Primary crusher load | `JT/JIC-1x1` (power) or `IT/IIC` (current) | Primary crusher motor power/current (`JT`/`IT`) | `JIC` / `IIC` | Apron/vibrating feeder speed → feeder `motor` (**DRIVE SPEED**) | Keep the primary crusher loaded without stalling | Constraint/override at higher tiers | `JT` on a lead from the crusher body; `JIC` above it; one signal over to `motor(port="top")` on the ROM-bin feeder | §2.1 [MetsoCSH p.162 "crusher currents"] |
| Secondary crusher cavity level | `LT/LIC-1x2` | Cone crusher cavity / feed-hopper level (`LT`) | `LIC` | Crusher feeder (or feed conveyor) speed → feeder `motor` (**DRIVE SPEED**) | Maintain choke feed ("full cavity") | Master of the level-to-feeder cascade at intermediate | `LT` on a lead from the bowl near its top; `LIC` beside it; signal to the `motor` of the feeder that feeds *this* crusher — not the surge-bin feeder | §2.1 [Hulthen2010 p.23; MetsoCSH p.17] |
| Cone crusher setting (CSS) | `ZT/ZIC-1x3` — setting mode; `PT/PIC` or `JT/JIC` → `ZIC` as the *alternative* load mode | Mainshaft position = CSS (`ZT`); in load mode hydroset pressure (`PT`) or power (`JT`) | `ZIC` | Hydroset / mantle position → crusher body (**CRUSHER SETTING**) | Hold constant CSS ("setting mode") or constant pressure/power ("load mode") | Slave of the power/pressure override at intermediate | **One** controller, two selectable modes — never two loops. `ZT` on a lead from the bowl; `ZIC` beside it; its output `sig` ends on the crusher body low down (the hydroset end). Draw the mode the plant runs in and name it in the narrative; the other mode is a note, not a second bubble | §2.1 [Hulthen2010 p.23; MetsoCSH pp.66–67] |
| Surge bin / screen feed level | `LT/LIC-1x4` | Surge bin level (`LT`) | `LIC` | Bin discharge (screen feed) feeder speed → feeder `motor` (**DRIVE SPEED**) | Keep the bin in range, steady screen feed | — | `LT` on a lead from the bin wall; `LIC` beside it; signal to `motor(port="right")` on the bin feeder | §2.1 [MetsoCSH p.162 "hopper and stockpile levels"] |
| Product conveyor tonnage | `WT/WI-1x5` (`WQI` if totalised) | Belt-scale mass flow on the stage product conveyor (`WT`) | `WI` | — (**MONITOR**) | Measure stage yield; the measurement the intermediate feedforward and advanced optimiser use | — | `WT` on a lead from the conveyor belt, `WI` above it; no outgoing signal | §2.1 [Hulthen2010 p.i] |

Caveats for the crushing basic tier:

- **Setting mode and load mode are one controller.** The research file lists "cone crusher setting"
  and "cone crusher load" as two rows because they measure different things, but the crusher
  control unit runs "in one of two possible modes where either the CSS or the hydraulic pressure
  is kept constant" [Hulthen2010 p.23] — draw one `ZIC`, pick the mode, state it. Mining crushers
  are often run pressure/power-limited, so load mode is a defensible choice too; whichever is drawn,
  the *override* of one by the other is an intermediate addition, not a basic loop.
- **One feeder, one controller.** The cavity-level loop and the surge-bin-level loop must land on
  different feeders (the crusher feeder and the bin/screen feeder respectively). If the flowsheet
  has only one feeder between bin and crusher, the cavity-level loop takes it and the bin level is
  drawn as an indicator (`LI`) — say so in the narrative.
- **Belt scale is a monitor.** No final element at basic; it becomes the feedforward source at
  intermediate.

#### Drawing a crusher-setting loop

There is no CSS primitive and none is needed. Put a `ZT` bubble on a `lead` from the crusher bowl,
the `ZIC` beside or above it, and run the `ZIC`'s output `sig` so its arrowhead ends **on the
crusher body** — low on the bowl, where the hydroset sits — with a small "CSS" label at the landing.
The same convention serves the SAG pebble crusher (Circuit 2) and any tertiary crusher. Because the
signal ends on equipment rather than on a `cvalve` or `motor`, this is the one final-element class a
reader cannot identify from the symbol it lands on; the "CSS" label and the narrative row carry that.

### Intermediate tier — additions only (research §2.2)

| Loop | Tag scheme | Measured variable (ISA letters) | Controller / function | Manipulated variable → final element (class) | Objective | Master / slave | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Power/pressure override on the CSS controller | `JT/JIC-1x3` (power) or `PT/PIC-1x3` (hydroset pressure) → `JY`/`PY-1x3` | Cone crusher motor power (`JT`) or hydroset pressure (`PT`) against its limit | `JIC`/`PIC` (constraint controller) → `JY`/`PY` low selector | Setpoint of the basic `ZIC-1x3` → crusher body (**CRUSHER SETTING**) | Protect the crusher: open the CSS when power or pressure runs high | **Master** = `JIC`/`PIC` via the selector; **slave** = `ZIC-1x3` | `JT` on a lead from the crusher body (motor end), `JIC` above it, `JY` beside the `ZIC` on its setpoint side; `JY` output lands on the `ZIC` setpoint port marked `SP`; the `ZIC` output still ends on the crusher body at the hydroset end | §2.2 [ASRi (snippet); MetsoCSH pp.66–67] |
| Wear compensation of CSS | `ZY-1x3` | Calibrated mainshaft-position drift (no transmitter of its own — a periodic calibration in the crusher controller) | `ZY` computing function | Setpoint (CSS reference) of `ZIC-1x3` (**CRUSHER SETTING**) | Hold the true CSS as liners wear; HP-type crushers re-calibrate "after a specific period of time or when the power draw drops below a certain limit" | **Master** = `ZY`; **slave** = `ZIC-1x3` | One `ZY` bubble next to the `ZIC`, output into the same setpoint port (or into the `JY` selector when the override is also drawn, so the `ZIC` keeps one setpoint leg); label "wear comp."; say in the narrative that it is a controller-internal function (ASRi, IC70C), not a field loop | §2.2 [ASRi (snippet); Hulthen2010 p.23] |
| Level-to-feeder cascade with power constraint | `LIC-1x2` → `JY-1x2` → `SC-1x2` | Cavity level (`LT-1x2`, primary); crusher current/power (`IT`/`JT`, constraint); feeder speed feedback (`ST`) | `LIC` master, `SC` slave, `JIC`/`IIC` → `JY` low selector | Feeder speed setpoint → feeder `motor` (**DRIVE SPEED**) | Choke feed held by level while the crusher's power limit caps the feeder | **Master** = `LIC-1x2` (through `JY`); **slave** = `SC-1x2` | Adds a speed controller `SC` beside the feeder `motor` (its `ST` feedback is a short lead from the motor); the basic `LIC` output now lands on the `SC` setpoint port through the `JY`, marked `SP`; the `SC` output lands on the `motor`. Formalises the basic loop — draw it only once | §2.2 [MetsoCSH p.162] |
| Feed-rate feedforward from belt scale | `WT-1x5` (or an upstream belt scale) → `WY-1x5` | Belt-scale tonnage upstream of the feeder (`WT`) | `WY` feedforward computer | Trim on the feeder speed setpoint → feeder `motor` (**DRIVE SPEED**) | Anticipate load changes before the level or power moves | **Feedforward into the slave** `SC-1x2` (no setpoint of its own) | `WY` bubble beside the `SC`; a second branch off the `WT` signal into `WY`; `WY` output into the `JY` selector (or summed at the `SC` setpoint) on a leg labelled "FF" — a feedforward trim, never a second controller and never a second `SP` leg. Research §2.2 writes the computer as `FY`; `WY` is used here because its input is the weight transmitter (ISA first letter follows the measured variable) | §2.2 [MetsoCSH p.162] |
| Eccentric-speed selection *(only if a VSD is fitted)* | `WT-1x5` → `SIC-1x6` | Belt-scale product yield (`WT`) and crusher speed (`ST`) | `SIC` | Crusher eccentric speed via frequency converter → crusher drive `motor` (**DRIVE SPEED**) | Pick the eccentric speed that maximises yield at the current CSS | — (standalone at this tier; the advanced optimiser writes its setpoint) | `motor` on the crusher body at the drive end, `SIC` beside it; belt-scale branch into the `SIC`. Omit on a fixed-speed crusher and say so | §2.2 [Hulthen2010 p.6, abstract] |

Caveats for the crushing intermediate tier:

- **One setpoint leg per slave.** If both the override and the wear compensation are drawn, chain
  them (`ZY` → `JY` → `ZIC`) so the `ZIC` has one setpoint port in use; two masters writing the same
  setpoint is a drawing defect a reviewer will call out.
- **The cascade formalises the basic level loop, it does not add a second feeder loop.** The basic
  `LIC` → `motor` leg becomes `LIC` → `JY` → `SC` → `motor`; the `LT`, `LIC` and `motor` are the
  same bubbles as at basic.
- **No pebble/size/speed feedforward at crushing** — the only feedforward source in the research is
  the belt scale.

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
| Mill speed *(only if VSD)* | `ST/SIC` (next free 200-series number) | Fraction of critical speed (`ST`) | `SIC` | Mill drive VSD → mill `motor` (**DRIVE SPEED**) | Operator-set speed target | — | `motor` on the mill trunnion drive end; omit entirely on a fixed-speed mill and say so | §3.1 [LeRoux2019 p.37] |
| Pebble crusher *(optional)* | `JT/JIC` or `PT/PIC` → `ZIC` (next free number) | Crusher power or hydroset pressure | `JIC`/`PIC` → `ZIC` | CSS (**CRUSHER SETTING**) | Run in power/pressure-limited mode | — | `ZIC` with a `sig` ending on the crusher body | §3.1 [Hulthen2010 p.23] |
| Pebble recycle tonnage *(optional)* | `WT/WI` (next free number) | Belt scale on pebble return | `WI` | — (**MONITOR**) | Measurement for feedforward at higher tiers | — | Indicator only | §3.1 [Gough p.7; HoneywellSAG p.5] |

Caveats for the SAG basic tier:

- **One feeder drive, two loops.** Fresh feed rate and mill load both act on the feeder. At the
  basic tier draw the load controller's output landing on the feed-rate controller (the "adjust mill
  feed rate to maintain mill weight" strategy of research §3); the intermediate tier formalises it as
  a cascade and adds the power/bearing-pressure override and feedforward, so those rows go there.
- **Power is a monitor at the basic tier.** The high-limit *override* on feed is an intermediate
  addition — do not draw a `JIC` writing to the feed loop at basic.

### Intermediate tier — additions only (research §3.2)

| Loop | Tag scheme | Measured variable (ISA letters) | Controller / function | Manipulated variable → final element (class) | Objective | Master / slave | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Load → feed-rate cascade | `WIC-2x3` (or `PIC-2x3`) → `WIC-2x1` | Mill load (`WT` load cells / `PT` bearing pressure) | `WIC`/`PIC` master, `WIC-2x1` slave | Setpoint of the fresh-feed `WIC-2x1` → feeder `motor` (**DRIVE SPEED**) | The master "takes the load measurement and set point ... and sets the set point for the feed rate controller" | **Master** = load `WIC-2x3`; **slave** = feed `WIC-2x1` | The basic row already lands the load controller on the feed `WIC` setpoint port marked `SP` — this tier adds nothing to that leg except the override selector (next row) spliced into it. Do not redraw the landing | §3.2 [Forbes&Gough p.7] |
| Water-to-ore ratio | `WT-2x1` → `FFY-2x2` → `FIC-2x2` | Fresh-feed tonnage (`WT-2x1`, the wild flow) and inlet water flow (`FT-2x2`) | `FFY` ratio station | Setpoint of the inlet-water `FIC-2x2` → water valve (**VALVE**) | Mill inlet water "kept at a constant ratio" of ore feed — constant discharge density | **Master** = `FFY-2x2` (ratio); **slave** = `FIC-2x2` | `FFY` directly above the `FIC` so its output drops onto the `FIC` setpoint port (top) marked `SP`; the `WT-2x1` gets a second branch off its bubble into the `FFY`. That branch usually has to cross the feed conveyor or chute — acceptable (see the cascade section), no re-route exists because the weightometer is on the belt and the water header is below it | §3.2 [LeRoux2019 p.14, pp.37–38] |
| Power / bearing-pressure override on feed | `JT-2x4` → `JIC-2x4` → `JY-2x4` (or `PT/PIC/PY`) | Mill power (`JT-2x4`) or bearing pressure (`PT`) against its high limit | `JIC` high-limit controller → `JY` low selector | Setpoint of the fresh-feed `WIC-2x1` (**DRIVE SPEED**) | Cut feed "should a high limit be violated ... until mill operations return to acceptable limits" | **Override master** = `JIC-2x4` via `JY`; **slave** = `WIC-2x1` (the `JY` also takes the load master's output) | The basic `JI-2x4` monitor becomes `JIC-2x4` (same `JT`, same place); the `JY` sits on the `SP` leg between `WIC-2x3` and `WIC-2x1`, `JIC` output comes down into the `JY` from above; label "low select". Research §3.2 writes "high selector"; a feed *cut* means the selector passes the lower of the two feed-rate demands, so low select is the correct function for this sign convention — the source's word is not carried over | §3.2 [Forbes&Gough p.6] |
| Feedforward into load control | `WT` (pebble recycle) / `AT` (ore size) / `ST` (mill speed) → `WY-2x3` | Whichever of pebble recycle tonnage, feed coarse fraction, mill speed is measured on the flowsheet | `WY` feedforward computer | Trim on the load master's setpoint / output → feed `WIC-2x1` (**DRIVE SPEED**) | Reject measured disturbances before the load moves | **Feedforward into the master** `WIC-2x3` | `WY` beside `WIC-2x3` on its setpoint side, one leg per measured disturbance into the `WY`, `WY` output onto the `WIC-2x3` labelled "FF". Draw only for sources that exist on the drawing (a pebble-return belt scale, an ore-size analyser, a VSD `ST`); with none present, omit the row and say so | §3.2 [Forbes&Gough p.7, Fig. 2] |
| Ball addition ratio *(only if a ball charging system is on the flowsheet)* | `WT-2x1` → `FFC-2xN` | Fresh-feed tonnage (`WT-2x1`) | `FFC` ratio controller | Ball feeder speed → ball feeder `motor` (**DRIVE SPEED**) | Ball addition "set as constant fraction" of ore feed to hold ball filling | **Ratio master** = `FFC`; slave = the ball feeder drive | Ball feeder + `motor` beside the SAG feed chute, `FFC` above it with a branch off `WT-2x1`. Omit when no ball charging equipment is drawn and say so | §3.2 [LeRoux2019 p.37] |

Caveats for the SAG intermediate tier:

- **The `WIC-2x1` still has one setpoint leg.** Load master and power override meet in the `JY`;
  only the `JY` output lands on the feed controller.
- **Feedforward and ball-addition rows are conditional** on equipment/measurements that exist on the
  drawing — the narrative says which were omitted and why, rather than inventing a transmitter.

### Advanced tier — supervisory block

*Not yet written — one `supervisory_block` ("SAG MILL OPTIMISER (MPC)") with `softlink` to the feed
`WIC`, speed `SIC` and water-ratio `FFY`.*

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

### Intermediate tier — additions only (research §4.2)

| Loop | Tag scheme | Measured variable (ISA letters) | Controller / function | Manipulated variable → final element (class) | Objective | Master / slave | Drawing hint | Source |
|---|---|---|---|---|---|---|---|---|
| Particle size → cyclone feed cascade | `AT-2x8` → `AIC-2x8` → `DIC-2x6` (density) **or** → `PIC-2x7`/`SIC` (pump speed) | Cyclone overflow particle size, on-line PSM (`AT-2x8`) | `AIC` master | Setpoint of the density `DIC-2x6` → dilution water (**VALVE**), when the pump is level-owned; setpoint of the pump-speed/pressure controller → pump `motor` (**DRIVE SPEED**) when the pump is free | Hold the cyclone cut size ("analyser controller (AC) for PSE manipulates CFF") | **Master** = `AIC-2x8`; **slave** = `DIC-2x6` or `PIC-2x7`/`SIC` — one, not both | The basic `AI-2x8` monitor becomes `AIC-2x8` beside the `AT` on the overflow; its output lands on the slave's setpoint port marked `SP`. With the shipped pairing (level → pump) the slave is the `DIC`, which sits inside the closed-circuit ring, so this leg crosses the cyclone feed line once — acceptable, see the cascade section | §4.2 [LeRoux2019 p.38] |
| Density → dilution-water cascade with level constraint | `DIC-2x6` → `LY-2x5` → `FIC-2xN` / `FT-2xN` / `FV-2xN` | Cyclone feed density (`DT-2x6`, primary); dilution water flow (`FT`, slave); sump level (`LT-2x5`, constraint) | `DIC` master, `LY` limiter, `FIC` slave | Setpoint of the dilution-water `FIC` → `FV` (**VALVE**) | Stabilise cyclone feed density and sump level together while the pump holds level | **Master** = `DIC-2x6`; **slave** = `FIC-2xN`; **constraint** = `LT-2x5` into `LY-2x5` | Column `DIC` → `LY` → `FIC` → `FV`: the basic `DIC` → valve leg gains the `FIC` slave (valve retagged `FV`, `FT` on a lead from the water line) and the `LY` on the `SP` leg; the `LT-2x5` gets a second branch into the `LY` side port; label "level limit". Nothing basic is removed — the `LIC` → pump loop is untouched | §4.2 [Mintek p.3] |
| Downstream density → CFD setpoint cascade *(only if the flotation feed is on the flowsheet)* | rougher-feed `DT/DIC` → `DIC-2x6` | Rougher (flotation) feed density | Downstream `DIC` master | Setpoint of the cyclone-feed `DIC-2x6` (**VALVE** through the slave chain) | Change the cyclone feed density setpoint to hold flotation feed density | **Master** = flotation-feed `DIC`; **slave** = `DIC-2x6` | Only one master may write the `DIC-2x6` setpoint: if the PSM cascade is drawn, this one is a note in the narrative, not a second `SP` leg. Omit entirely when the drawing ends at the cyclone overflow | §4.2 [Mintek p.4] |
| Water-to-ore ratio at mill inlet *(only if the ball mill has its own feed and water loops)* | `WT` → `FFY` → `FIC` | Ball-mill feed tonnage and inlet water flow | `FFY` ratio station | Setpoint of the mill-water `FIC` → valve (**VALVE**) | Constant mill discharge density | **Master** = `FFY`; **slave** = `FIC` | As for the SAG ratio row. In a SAG-fed ball mill with no separate water loop, omit and say so | §4.2 [LeRoux2019 p.14] |
| Pump-pressure override | `PT-2x7` → `PIC-2x7` → `PY-2x7` | Cyclone inlet pressure (`PT-2x7`) against its low/high band | `PIC` constraint controller → `PY` selector | Pump speed → pump `motor` (**DRIVE SPEED**) (or dilution water when the pump is density-owned) | Keep the cyclones out of roping/choking: pressure inside its band overrides level | **Override master** = `PIC-2x7` via `PY`; **slave** = the pump drive (the `PY` also takes the `LIC-2x5` output) | The basic `PI-2x7` monitor becomes `PIC-2x7` (same `PT`); the `PY` sits on the `LIC` → `motor` leg just above the pump motor, `PIC` output comes into it from above; label "override" | §4.2 [Mintek (snippet)] |

Caveats for the ball-mill/cyclone intermediate tier:

- **The pairing chosen at basic decides the slaves.** With level → pump and density → water (the
  shipped example) the PSM cascade lands on the `DIC`, the pressure override on the pump. With the
  other pairing (level → water, density → pump) swap them. Never re-pair at a higher tier — tiers
  are cumulative.
- **One master per setpoint.** PSM cascade and downstream-density cascade both target the
  `DIC-2x6` setpoint — draw one, mention the other.
- **The ring crossing is expected.** The `DIC`, `LY`, `FIC` and dilution valve sit inside the
  closed-circuit ring (sump → pump → cyclone → mill → sump); the `AT`/`AIC` on the overflow and the
  `LIC` → pump loop sit outside it. Expect one signal-over-process crossing for the PSM `SP` leg
  and one for the level loop, place the crossings on straight pipe runs away from arrowheads and
  junctions, and never let two signals cross each other. `pump_sump(basin_w=...)` widens the pit so
  the level transmitter's rim lead and the dilution-water inlet both sit on the ring's inside, which
  is what keeps the count at two.

### Advanced tier — supervisory block

*Not yet written — one `supervisory_block` ("GRINDING CIRCUIT OPTIMISER (MPC)") with `softlink` to
the feed `WIC`, water `FFY`/`FIC`, sump `LIC`, density `DIC` and pump `SIC`/`PIC`.*

---

## Circuits not covered

Flotation, thickening, filtration and reagent-dosing control strategies are not in this reference.
If the user asks for control on one of those circuits, say that the skill does not yet know those
strategies rather than improvising loops; a single loop the user specifies explicitly on one piece
of equipment (e.g. the thickener level loop in the base-metal example) is still fine to draw.

## Per-circuit tier note

Because tiers can be mixed per circuit, the drawing must carry a note stating which tier each circuit
was drawn at. Format: one `CONTROL STRATEGY` notes block whose first bullet lists every circuit
present as `<Circuit>: <tier>`, separated by ` | `, with `(assumed)` after any tier the user did not
name — e.g.

```python
d.notes(x, y, "CONTROL STRATEGY", [
    "Crushing: basic (assumed) | Grinding: basic (assumed) - no tier was named",
    ...
])
```

The shipped example (`examples/build_grinding_circuit_control.py`) is the mixed case — the user
named intermediate for grinding only — and its note reads
`"Crushing: basic (assumed) | Grinding: intermediate"`.

The separator is ASCII on purpose: `pid_lib.save()` writes in the platform encoding, so a non-ASCII
`·` breaks the SVG on a managed Windows Python. This is the only place on the sheet that says what
the drawn loops represent (ADR 0004), and the end-to-end smoke test asserts the line.
