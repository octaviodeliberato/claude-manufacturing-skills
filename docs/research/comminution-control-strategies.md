# Comminution Circuit Control Strategies — Primary Source Extraction

> **Status:** Primary-source research notes, not a spec. This file collects what textbooks, peer-reviewed
> papers, vendor-published control philosophies and ISA-5.1-2009 say about automatic control of
> crushing, SAG and ball-mill/cyclone circuits, organised as three *cumulative* tiers so that a future
> design session can decide how `mineral-processing-pfd` (or a sibling skill) should draw control loops.
> It makes no design decisions. Every claim is cited; where a claim could only be reached through a
> search-engine snippet or a secondary summary, that is said explicitly in the text and in §6.
> Sources are abbreviated in square brackets and expanded in §6.

## Scope

Three circuits are covered: (1) primary/secondary crushing — gyratory or jaw primary, cone secondary,
vibrating screen in closed circuit, feeders and conveyors; (2) SAG mill — feed conveyor with
weightometer, mill water, mill load (bearing pressure or load cells), mill power, variable speed if
fitted, optional pebble crusher; (3) ball mill + hydrocyclone closed circuit — cyclone feed sump, pump,
dilution water, cyclone feed density and pressure, particle size monitor. For every loop the tables
give the measured variable, the manipulated variable and its final element class (**DRIVE SPEED** —
feeder/mill/pump VSD; **CRUSHER SETTING** — CSS/hydroset; **VALVE** — water), the objective, suggested
ISA-5.1-2009 letters, the tier, and master/slave role in a cascade. Vendor supervisory products are
summarised in §5 to justify drawing "advanced" as one supervisory block per circuit.

## 1. Tier definitions

The three-layer split used here is the one the peer-reviewed literature uses:

- **Regulatory layer (basic).** "The aim of the regulatory layer is to stabilize the plant. This is
  generally achieved by means of simple single-loop PID controllers." [LeRoux2019, p.36]. "The majority
  of industrial mineral processing plants make use of SISO PID controllers to achieve their control
  objectives" [LeRoux2019, p.38, citing Wei & Craig 2009 as its ref. 32]. Hodouin's 2011 review makes
  the same point — PID is "the most usual approach to feedback control found in mineral processing
  plants" — but only the abstract and secondary quotations of that paper could be reached (see §6).
- **Enhanced regulatory layer (intermediate).** "A typical simple approach is to use the traditional PID
  controllers, with traditional enhancements such as cascade control, feedforward control, ratio
  control, and so forth, that are available in plant distributed control systems (DCS)." [Forbes&Gough,
  p.2]. This tier adds cascade, ratio, feedforward and override/constraint loops *on top of* the basic
  loops; nothing from tier 1 is removed.
- **Supervisory layer (advanced).** "The supervisory control layer aims to control the primary economic
  controlled variables using the set-points to the regulatory layer as manipulated variables."
  [LeRoux2019, p.38]. Vendor systems say the same in product language: the Metso Grinding Optimizer
  "manipulates the setpoints of multiple regulatory controllers in the grinding circuit, such as mill
  feed rates, rotational speed, water additions, cyclone feed characteristics, etc." [MetsoGO, p.1].
  Above this sits a real-time optimisation layer that chooses the supervisory setpoints from economics
  or grind curves [LeRoux2019, pp.39–40]; it is out of scope for drawing and is folded into "advanced".

Two structural facts justify one supervisory block per circuit: the supervisory system runs as separate
software that exchanges data with the DCS ("software running on a PC that is frequently exchanging
information (receiving process data and sending control outputs) with the DCS" [Forbes&Gough, p.2]);
and it connects "using the OLE for Process Control (OPC) standard interface", with "a communications
watchdog scheme ... to ensure that the process control automatically reverts to the existing control
system in the event of any communication or hardware faults" [Gough, p.5]. Sandvik's ASRi crusher
regulator likewise ships "an OPC-server that allows seamless integration with superior control systems
such as SCADA and DCS" (search-snippet only, see §6 [ASRi]).

### ISA-5.1-2009 letters used in the tables

All letters below are from ANSI/ISA-5.1-2009 **Table 4.1 "Identification letters", p.30** [ISA51].
First letters: **A** Analysis; **F** Flow, Flow Rate; **I** Current; **J** Power; **L** Level; **P**
Pressure; **S** Speed, Frequency; **W** Weight, Force; **Z** Position, Dimension. Succeeding letters:
**C** Control; **I** Indicate; **T** Transmit; **Y** Auxiliary Devices (compute/relay); **Z** Driver,
Actuator, Unclassified final control element; **V** Valve. Column-2 modifier **F** = Ratio (so a
ratio-flow controller is FFC). Two caveats: (i) **D is "User's Choice"** as a first letter in Table 4.1
— density is the conventional user assignment, so DT/DIC must be declared on the drawing legend; (ii)
Table 4.1 lists "Speed, Frequency" for S but has no dedicated readout for "speed controller" — SC/SIC
is formed by the ordinary rules. The pages of ISA-5.1 retrieved (Tables 4.1, 5.1.1–5.4.4) do not
include the clause on drawing cascade loops, so master/slave *drawing* convention is not sourced here.

## 2. Circuit 1 — Primary / secondary crushing with closed-circuit screen

Sources for this circuit are thinner than for grinding: Hulthén's Chalmers PhD (which bundles the two
Hulthén & Evertsson *Minerals Engineering* papers) [Hulthen2010], Metso's *Crushing and Screening
Handbook* 7th ed. [MetsoCSH], and vendor crusher-automation pages. Neither Wills ch. 6 nor the SME
Handbook crusher chapters could be read (see §6).

What the sources establish: on cone crushers the measured variables are "CSS, hydraulic pressure, and
the load (power draw or amps)" [Hulthen2010, p.23]; the crusher control unit "controls the hydraulic
pump" and runs "in one of two possible modes where either the CSS or the hydraulic pressure is kept
constant" [Hulthen2010, p.23]; mining crushers "are often operated in the pressure, or power, limited
mode" [Hulthen2010, p.23]. Metso: "Crusher setting can be continuously adjusted under load based on
power draw or crushing force measurement. With automation, system mode can be selected between two
options: setting mode or load mode." [MetsoCSH, pp.66–67]. On feeding: "Full cavity is often called
choke feeding" [MetsoCSH, p.17]; "Feeder speeds are calculated by high efficiency control loops
according to all available process information such as crusher currents and levels, hopper and
stockpile levels, conveyor flows (if belt scale available)" [MetsoCSH, p.162]. Belt scales are the
process feedback: "By applying mass-flow sensors to the process, e.g. conveyor-belt scales, the crusher
result can be monitored and the result can be fed back to an operator or a computer" [Hulthen2010, p.i].

### 2.1 Basic tier — single-loop regulatory

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Primary crusher feed (apron feeder) | Crusher motor current/power [MetsoCSH p.162 "crusher currents"] | Apron/vibrating feeder speed → **DRIVE SPEED** | Keep primary crusher loaded without stalling | IT/IIC (or JT/JIC) → SC on feeder | Basic | — |
| Secondary crusher cavity level | Cavity/feed-hopper level (light beam, radar, ultrasonic) [Hulthen2010 p.23] | Feed conveyor / feeder speed → **DRIVE SPEED** | Maintain choke feed ("full cavity") [MetsoCSH p.17] | LT/LIC → SC | Basic | — |
| Cone crusher setting | Mainshaft position = CSS [Hulthen2010 p.6, p.23] | Hydroset pressure / mantle position → **CRUSHER SETTING** | Hold constant CSS ("setting mode") [MetsoCSH p.67] | ZT/ZIC → ZY/hydraulic | Basic | — |
| Cone crusher load (alternative mode) | Hydroset pressure or motor power [Hulthen2010 p.23] | CSS → **CRUSHER SETTING** | Hold constant pressure/power ("load mode") | PT/PIC or JT/JIC → CSS | Basic | — |
| Surge bin / screen feed level | Bin level | Bin discharge feeder speed → **DRIVE SPEED** | Keep bin in range, steady screen feed [MetsoCSH p.162 "hopper and stockpile levels"] | LT/LIC → SC | Basic | — |
| Product conveyor tonnage (monitor) | Belt scale mass flow [Hulthen2010 p.i] | — (indication/totalising) | Measure stage yield for the layers above | WT/WI, WQI | Basic | — |

Note: the two crusher-setting rows are *alternative modes of the same controller* (setting mode vs load
mode), not two loops that run at once [MetsoCSH p.67; Hulthen2010 p.23].

### 2.2 Intermediate tier — additions only

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Power/pressure override on the CSS controller | Motor power and hydroset pressure vs. limits | CSS setpoint of the basic ZIC → **CRUSHER SETTING** | Protect the crusher: open CSS when power/pressure high ("protects your crusher from overloading by automatically regulating based on preset operational values" [ASRi]) | JT/PT → override selector (JY/PY) → ZIC | Intermediate | Master over ZIC |
| Wear compensation of CSS | Calibrated mainshaft position drift | CSS reference → **CRUSHER SETTING** | "automatic liner wear compensation" [ASRi]; HP-type crushers adjust "after a specific period of time or when the power draw drops below a certain limit" [Hulthen2010 p.23] | ZY → ZIC | Intermediate | Master over ZIC |
| Level-to-feeder cascade with power constraint | Cavity level (primary CV) and crusher current/power (constraint) | Feeder speed setpoint → **DRIVE SPEED** | Feeder speed "calculated ... according to ... crusher currents and levels, hopper and stockpile levels, conveyor flows" [MetsoCSH p.162] | LIC master → SC slave; IT/JT as override | Intermediate | LIC master, SC slave |
| Feed-rate feedforward from belt scale | Belt-scale tonnage upstream | Feeder speed setpoint → **DRIVE SPEED** | Anticipate load changes ("conveyor flows (if belt scale available)" [MetsoCSH p.162]) | WT → FY → SC | Intermediate | Feedforward into slave |
| Eccentric-speed selection (if VSD fitted) | Belt-scale product yields | Crusher eccentric speed via frequency converter → **DRIVE SPEED** | "Frequency converters can potentially control the eccentric speed" [Hulthen2010 p.6]; speed setpoint chosen w.r.t. current CSS [Hulthen2010 abstract] | WT → SC (crusher motor) | Intermediate | — |

### 2.3 Advanced tier — supervisory block

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Crushing-stage real-time optimiser | Belt-scale mass flows of each product [Hulthen2010 p.i]; power and pressure as constraints ("limited power draw, which make the optimal operating point on the border of the constraint" [Hulthen2010 p.38]) | Setpoints of the CSS controller and of the eccentric-speed controller | "make set-point selections automatically using a computer system. This is defined as real-time optimization" [Hulthen2010 p.37]; +3.5 % yield vs fixed CSS, +4.2–6.9 % vs good fixed speed [Hulthen2010 p.i] | One block (e.g. UC/UY) writing to ZIC and SC | Advanced | Master over intermediate CSS and speed controllers |

Hulthén explicitly frames this as a setpoint-writing layer on top of the existing regulator: "the
algorithm was implemented in addition to the existing control system" [Hulthen2010 p.i], and "there is
no target set-point ... Thus, there is no obvious set-point. Due to the fact that the set-points are
unknown, classic control theory cannot be used" [Hulthen2010 p.38].

## 3. Circuit 2 — SAG mill (feed conveyor, water, load, power, speed, pebble crusher)

Primary sources: Le Roux & Craig 2019 (single-stage SAG circuit, University of Pretoria preprint of the
*I&EC Research* paper) [LeRoux2019]; Andritz's two vendor papers on SAG MPC [Forbes&Gough], [Gough];
Honeywell's SAG APC whitepaper [HoneywellSAG]; Metso Grinding Optimizer leaflet [MetsoGO].

Key statements. Feed control: "The mass feed rate of ore is measured on the feed belt and typically an
enhanced PID control strategy is used to control the ore feed rate. The PID controller gives a master
feeder speed output which, typically, is then applied to each individual feeder with a different scaling
so as to compensate for segregation of fine and course ore in the stockpile." [Forbes&Gough, p.7].
Load: "industrial plants primarily manipulate JT by adjusting MFO, otherwise by varying the mill speed
(φc) if a variable speed drive is fitted, or as a last option by manipulating MIW" [LeRoux2019, p.10].
"mill load was inferred either from a direct weight measurement or from bearing oil pressure"
[Forbes&Gough, p.7]. Water: "In general MIW is kept at a constant ratio of MFO to maintain ρQ within
reasonable bounds" [LeRoux2019, p.14]. Power: "the power draw of the mill must be monitored to avoid
exceeding the maximum power limit" [Forbes&Gough, p.6]. Two classic strategies: "gradually increase the
feed rate to the mill until a high limit for weight or power draw has been reached ... can result in a
'saw tooth' pattern", versus "adjust mill feed rate to maintain mill weight at a set target"
[Forbes&Gough, pp.6–7].

### 3.1 Basic tier — single-loop regulatory

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Fresh feed rate | Weightometer (belt scale) t/h [Forbes&Gough p.7] | Master feeder speed, scaled per feeder → **DRIVE SPEED** | Hold ore feed at setpoint | WT/WIC → SC (feeders) | Basic | Slave (when a load master exists) |
| Mill inlet water | Water flow m³/h | Water control valve → **VALVE** | Hold MIW at setpoint | FT/FIC → FV | Basic | Slave of ratio (tier 2) |
| Mill load (weight / bearing pressure) | Load cells or bearing oil pressure [Forbes&Gough p.7] | Feed-rate setpoint (or feeder speed directly) → **DRIVE SPEED** | Keep JT at target; "maintain the weight within a specific range" [Forbes&Gough p.6] | WT/WIC (load cells) or PT/PIC (bearing) | Basic | Master over WIC feed (see 3.2) |
| Mill power (monitor / limit) | kW [Forbes&Gough p.6] | — (alarm/limit) | Do not exceed max power | JT/JI, JAH | Basic | — |
| Mill speed (if VSD) | Fraction of critical speed φc | Mill VSD → **DRIVE SPEED** | "φc is set by the operator to achieve the desired TP" [LeRoux2019 p.37] | ST/SIC → mill drive | Basic | — |
| Pebble crusher (optional) | Crusher power / hydroset pressure [Hulthen2010 p.23] | CSS → **CRUSHER SETTING** | Run in "pressure, or power, limited mode" typical of mining duty [Hulthen2010 p.23] | JT/JIC or PT/PIC → ZIC | Basic | — |
| Pebble recycle tonnage (monitor) | Belt scale on pebble return | — | Measurement used as feedforward/DV above [Gough p.7; HoneywellSAG p.5] | WT/WI | Basic | — |

### 3.2 Intermediate tier — additions only

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Load → feed-rate cascade | Mill load (weight or bearing pressure) | Setpoint of the feed-rate WIC → **DRIVE SPEED** | Master "takes the load measurement and set point ... and sets the set point for the feed rate controller" [Forbes&Gough p.7] | WIC/PIC master → WIC slave → SC | Intermediate | Master = load; slave = feed |
| Water-to-ore ratio | Weightometer t/h and water flow | Water FIC setpoint → **VALVE** | MIW "kept at a constant ratio of MFO" [LeRoux2019 p.14]; regulatory "flow controllers (FC) manipulate MIW ... set as constant ratios of MFO" [LeRoux2019 pp.37–38] | WT → FFY/FFC → FIC → FV | Intermediate | Ratio master over FIC |
| Power / bearing-pressure override on feed | Mill power, bearing pressure vs high limits | Feed-rate setpoint → **DRIVE SPEED** | Cut feed "should a high limit be violated ... until mill operations return to acceptable limits" [Forbes&Gough p.6] | JT/PT → high selector (JY/PY) → WIC | Intermediate | Override master over feed WIC |
| Feedforward into load control | Pebble recycle rate, ore size (coarse fraction), mill speed [Forbes&Gough p.7, Fig. 2] | Feed-rate setpoint → **DRIVE SPEED** | Reject measured disturbances before load moves | WT (pebbles), AT (size), ST → WY → WIC | Intermediate | Feedforward into master |
| Ball addition ratio (if automated) | Fresh feed t/h | Ball feeder speed → **DRIVE SPEED** | "MFB is used to maintain a constant JB", "set as constant fraction of MFO" [LeRoux2019 p.37] | WT → FFC → SC | Intermediate | Ratio master |

### 3.3 Advanced tier — supervisory block

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| SAG supervisory (expert / MPC) | CVs: "SAG Load, Bearing Pressure, SAG Power, Generated Pebbles"; DVs: "Recirculated Pebbles, Feed Granulometry, Ore Composition" [HoneywellSAG, Fig. 2 p.5]; mill sound/acoustics [Gough p.6; Forbes&Gough p.7] | MVs: "Feed Rate, Mill Velocity, %Solids" [HoneywellSAG Fig. 2] — i.e. the setpoints of the WIC feed, SIC speed and water-ratio controllers | "Stabilize mill load and power ... Operate safely and consistently closer to constraints" [HoneywellSAG p.4]; Metso: CVs "primary mill charge level, power and weight", MVs are "setpoints of multiple regulatory controllers ... mill feed rates, rotational speed, water additions" [MetsoGO p.1] | One block (UC) → WIC, SIC, FFC | Advanced | Master over all tier-2 masters |

Results reported for this layer: MPC as master over the feed-rate PID gave "1.5 to 2 % increase in ore
throughput relative to mill throughput with expert system control alone" at Candelaria, Escondida
Laguna Seca and Los Pelambres [Forbes&Gough p.8, Table 1]; mill-weight standard deviation −84 % vs expert
control at Los Pelambres [Gough p.7, Table 2]. Honeywell claims "around 3-4 % reduced SEC" [HoneywellSAG
p.6]. The operator still owns the outer constraint: "The maximum feed rate of fresh ore is set by the
operator based on plant operating constraints" [Gough p.7].

## 4. Circuit 3 — Ball mill + hydrocyclone closed circuit

Primary sources: Le Roux & Craig 2019 (the sump/cyclone half of Fig. 2 applies unchanged to a ball-mill
circuit) [LeRoux2019]; Mintek's MillStar case study at a platinum concentrator [Mintek]; Metso Grinding
Optimizer [MetsoGO]. Le Roux & Craig's regulatory proposal: "SFW is used to control SVOL and to reject
disturbances in PSE. CFF is used to control PSE." — with SFW = sump feed water, SVOL = sump slurry
volume, CFF = cyclone feed flow (variable-speed pump), PSE = particle size estimate [LeRoux2019 p.37].
Industrial preference: "In industrial plants, SFW is used more frequently than CFF to control SVOL"
and, for cyclone feed density, "SFW, MFO, and MIW - is the order of preference for plants to control
CFD" [LeRoux2019 pp.11–12, both citing Wei & Craig 2009]. Pressure bounds the pump: "The capacity of
the cyclone provides an upper bound for CFF. The minimum cyclone inlet pressure necessary to keep the
cyclone within its operable region provides the lower bound for CFF." [LeRoux2019 p.13].

### 4.1 Basic tier — single-loop regulatory

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Ball mill fresh feed (if separately fed) | Weightometer t/h | Feeder speed → **DRIVE SPEED** | Hold feed at setpoint | WT/WIC → SC | Basic | Slave (tier 2/3 masters) |
| Mill inlet water | Water flow | Control valve → **VALVE** | Hold flow at setpoint | FT/FIC → FV | Basic | Slave of ratio |
| Sump level | Sump level / slurry volume [LeRoux2019 p.11] | Sump dilution water valve → **VALVE** (industrial preference) *or* pump VSD → **DRIVE SPEED** | "prevent the sump from overflowing or running dry" [LeRoux2019 p.11] | LT/LIC → FV (water) or → SC (pump) | Basic | — |
| Cyclone feed density | Nuclear/Coriolis density gauge | Dilution water valve → **VALVE** | Hold CFD at setpoint; MillStar objective "Controlling cyclone feed density to a tight setpoint" [Mintek p.1] | DT/DIC → FV (D = user's choice, declare on legend) | Basic | — |
| Cyclone feed pressure | Cyclone inlet manifold pressure | Pump speed → **DRIVE SPEED** | "Keep cyclone feed pressure in normal operating region" [Mintek p.1]; min pressure bounds CFF [LeRoux2019 p.13] | PT/PIC → SC (pump) | Basic | — |
| Mill power (monitor) | kW | — | Indication/alarm | JT/JI | Basic | — |
| Particle size (monitor) | On-line PSM / PSI on cyclone overflow ("PSI® particle size analyzer" [MetsoGO]) | — | Measure PSE for tier 2/3 | AT/AI | Basic | — |

Note: sump level via water and cyclone feed density via water cannot both run as independent
single loops on the same valve; a plant picks one pairing (level→water with density controlled by
pump, or level→pump with density→water). Le Roux & Craig: "the sump controller must manage the loop
interactions between SVOL at the sump and PSE at the cyclone ... This requires a multi-variable
controller capable of decoupling" [LeRoux2019 p.11].

### 4.2 Intermediate tier — additions only

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Particle size → cyclone feed flow (or density) cascade | PSE from analyser [LeRoux2019 p.38: "analyser controller (AC) for PSE manipulates CFF"] | Setpoint of pump-speed/pressure controller (or of density DIC) → **DRIVE SPEED** / **VALVE** | Hold cyclone cut size at target | AT/AIC master → PIC or SIC slave (or DIC slave) | Intermediate | Master = AIC; slave = PIC/DIC |
| Density → dilution-water cascade with level constraint | CFD (primary) and sump level (constraint) | Water FIC setpoint → **VALVE** | MillStar discharge controller "implemented to stabilise the cyclone feed density and the sump level, while keeping the cyclone feed pressure within the required operating band" [Mintek p.3] | DIC master → FIC slave → FV; LT as constraint | Intermediate | Master = DIC; slave = FIC |
| Downstream density → CFD setpoint cascade | Rougher (flotation) feed density | CFD setpoint of the DIC → **VALVE** | "A cascade controller was implemented between the rougher feed density and the cyclone feed density in order to change the cyclone feed density setpoint" [Mintek p.4] | DIC (float feed) master → DIC (CFD) slave | Intermediate | Master = downstream DIC |
| Water-to-ore ratio at mill inlet | Feed t/h, water flow | FIC setpoint → **VALVE** | Constant mill discharge density [LeRoux2019 p.14] | WT → FFC → FIC → FV | Intermediate | Ratio master |
| Pump-pressure override | Cyclone inlet pressure vs. low/high limits | Pump speed / water → **DRIVE SPEED** / **VALVE** | Prevent roping/choke: "cyclone density (to prevent pipeline chokes and pressure variations)" and "sump level (to prevent pump surging and spillage)" [Mintek, search snippet, see §6] | PT → PY (selector) → SC | Intermediate | Override master |

### 4.3 Advanced tier — supervisory block

| Loop | Measured variable | Manipulated variable → final element (class) | Objective | ISA tags | Tier | Cascade role |
|---|---|---|---|---|---|---|
| Grinding-circuit supervisory (expert / MPC) | PSE, CFD, sump level, cyclone pressure, mill power/load [Mintek pp.1–3; MetsoGO p.1] | Setpoints of feed WIC, water FFC/FIC, sump LIC, density DIC, pump SIC/PIC | "Controlled variables typically include final particle size after grinding, primary mill charge level, power and weight ... Grinding Optimizer manipulates the setpoints of multiple regulatory controllers" [MetsoGO p.1]; MillStar "StarCS MPC controller further ensures that ... cyclone feed pressure and sump level, is kept inside their operating limit" [Mintek p.2] | One block (UC) → WIC, FFC, LIC, DIC, PIC/SIC | Advanced | Master over tier-2 masters |

Le Roux & Craig describe the same block in MPC terms: with MFB and MIW ratioed, "the controller can
make use MFO, SFW, and CFF as manipulated variables to control the primary economic controlled variable
JT, as well as the variables SVOL and PSE" [LeRoux2019 p.39]. Two operating philosophies are named for
the supervisor to choose between: "Maintain PSE at setpoint, and maximize TP" or "Maintain TP at
setpoint, and push PSE towards an acceptable setpoint" [LeRoux2019 p.13].

## 5. Supervisory systems — how vendors describe the block

| System | Type (as described) | Setpoints written | Constraints honoured | Verification |
|---|---|---|---|---|
| Metso Outotec **Grinding Optimizer** (ACT platform; RockSense, MillSense, PSI, CycloneSense inputs) | "a multivariable, model-based controller" | "setpoints of multiple regulatory controllers ... mill feed rates, rotational speed, water additions, cyclone feed characteristics" | CVs "final particle size after grinding, primary mill charge level, power and weight and other customer specific targets" | Vendor leaflet read in full [MetsoGO] |
| Metso Outotec **OCS-4D** | — | — | — | **Not verified.** No Metso page describing OCS-4D for grinding was reachable; search snippets only say it is Metso Outotec's "Optimising Control System" and show it in pelletizing contexts. Treat as an alias of the ACT/Grinding Optimizer family until a primary page is found. |
| Andritz **BrainWave** (Laguerre adaptive MPC) | Adaptive MPC "as a master controller over the feed rate controller" | Feed-rate PID setpoint; also belt weight and mill sound loops | Operator max feed rate; weight/power high limits; feedforwards from pebbles, ore size, speed | Two vendor papers read in full [Forbes&Gough], [Gough] |
| Honeywell **Profit Controller** (Profit Suite APC) | MPC | MVs "Feed Rate, Mill Velocity, %Solids" | CVs "SAG Load, Bearing Pressure, SAG Power, Generated Pebbles"; DVs pebbles, granulometry, ore composition | Vendor whitepaper read in full [HoneywellSAG] |
| Mintek **MillStar** (Solids Feed Controller + StarCS MPC discharge controller) | MPC with constraint handling | Cyclone feed density SP, sump level, feed rate; cascade from flotation feed density | Sump level limits, cyclone feed pressure band; "plant control scheme has no constraint handling capabilities" | Mintek case study read in full [Mintek] |
| FLSmidth **ECS/ProcessExpert** + **KnowledgeScape LoadIQ / GrindingExpert** | Rule-based/expert (search snippets); LoadIQ "sets the load target in real-time" | "feed rate, mill water addition, mill speed, cyclone feed density, pump speeds and circulating loads" | Measures "mill power consumption, load impacts, mill mass, sump levels, circuit flows, pump power, stream density, hydrocyclone pressure and product quality" | **Search snippets only** — the FLS product pages are script-rendered and returned no text; the kscape.com domain no longer hosts KnowledgeScape. |
| Sandvik **ASRi** (crusher) | Setting regulator with "Auto-CSS" and "Auto-load" modes | CSS; power/hydroset pressure setpoints | Overload protection; liner wear compensation; OPC to SCADA/DCS | Vendor page gives only marketing sentences; mode names from search snippet [ASRi] |
| Metso **IC70C / IC series** (crusher) | Crusher automation with "setting mode or load mode" | CSS; feeder speeds from "crusher currents and levels, hopper and stockpile levels, conveyor flows" | Power draw / crushing force; choke-feed level | Vendor handbook read in full [MetsoCSH] |

Common pattern across all rows: the supervisory product is a separate application (PC/server, OPC to
the DCS) whose outputs are *setpoints* of existing regulatory or enhanced-regulatory controllers, with
a watchdog fallback to DCS control — which is exactly the drawing model "one supervisory block per
circuit, signal lines to the tier-2 masters".

## 6. Sources

Read in full (text extracted from the linked file):

- **[ISA51]** ANSI/ISA-5.1-2009, *Instrumentation Symbols and Identification*, Table 4.1 "Identification
  letters", p.30 (plus Tables 5.1.1–5.4.4, pp.36–55). Excerpt PDF:
  https://banner9.icesi.edu.co/ic_contenidos_pdf/adjuntos/202210/202210_11459_12897.pdf
- **[LeRoux2019]** le Roux, J.D. & Craig, I.K., "A plant-wide control framework for a grinding mill
  circuit", *Ind. Eng. Chem. Res.* 58 (2019) 11585–11600, doi:10.1021/acs.iecr.8b06031. Page numbers
  above refer to the University of Pretoria author preprint:
  https://repository.up.ac.za/bitstream/handle/2263/72289/LeRoux_PlantWide_2019.pdf
- **[Forbes&Gough]** Forbes, M.G. & Gough, W.A., "Model predictive control of SAG mills and flotation
  circuits", ANDRITZ Automation paper P124, 12 pp.
  https://www.andritz.com/resource/blob/14766/39b32881f5cf79564ab492e33b47d549/aa-automation-mpc-sag-mills-flotation-circuits-data.pdf
- **[Gough]** Gough, W.A., "SAG mill optimization using model predictive control", ANDRITZ Automation, 8 pp.
  https://www.andritz.com/resource/blob/15118/a5556fa5e0ad15046e8059f9e1fb32c4/aa-sag-mill-optimization-using-model-predictive-control-data.pdf
- **[HoneywellSAG]** Honeywell Process Solutions, *Improving Operational Productivity in SAG Mills Using
  Advanced Process Control (APC)*, whitepaper, 9 pp. (undated; Fig. 2 "Common APC strategy", p.5).
  https://process.honeywell.com/content/dam/process/en/campaigns/hps/improving-operational-productivity-sag-mills/hon-ia-hp-whitepaper-sag-mills-mining.pdf
- **[Mintek]** Coetzee, L., Naidoo, A., Phillpotts, D. & client, "A complementary milling and flotation
  advanced process control system at a platinum concentrator", Mintek case study (4 pp.; full paper:
  Coetzee et al., *Precious Metals '12*, Cape Town, Nov. 2012).
  https://mintek.co.za/clusters/miningmaterialsautomation/measurement-and-control/mac-casestudies/a-complementary-milling-and-flotation-advanced-process-control-system-at-a-platinum-concentrator.pdf.pdf
- **[MetsoGO]** Metso Outotec, *Grinding Optimizer* leaflet (1 p., 2020).
  https://www.metso.com/globalassets/saleshub/documents---episerver/grinding-optimizer-leaflet-web.pdf
- **[MetsoCSH]** Metso, *Crushing and Screening Handbook*, 7th ed., © 2023 (216 pp.); pp.17, 66–67, 70,
  157–158, 162. https://www.metso.com/globalassets/insights/ebooks/metso-crushing-and-screening-handbook-edition7-en-web.pdf
- **[Hulthen2010]** Hulthén, E., *Real-Time Optimization of Cone Crushers*, PhD thesis, Chalmers
  University of Technology, Göteborg, Nov. 2010 (bundles Hulthén & Evertsson, *Minerals Engineering* 22
  (2009) 296–303, doi:10.1016/j.mineng.2008.08.007, and 24 (2011) 987–994, doi:10.1016/j.mineng.2011.04.007).
  https://publications.lib.chalmers.se/records/fulltext/128844.pdf

Cited only through abstracts, secondary quotation or search snippets — **treat as unverified**:

- Hodouin, D., "Methods for automatic control, observation, and optimization in mineral processing
  plants", *J. Process Control* 21 (2011) 211–225, doi:10.1016/j.jprocont.2010.10.016. Publisher page
  returned 403; the "PID ... most usual approach" statement comes from search-engine summaries and from
  its citation in [LeRoux2019] refs. 28–29, 48.
- Wei, D. & Craig, I.K., "Grinding mill circuits — A survey of control and economic concerns", *Int. J.
  Miner. Process.* 90 (2009) 56–66, doi:10.1016/j.minpro.2008.10.009 (also IFAC Proc. 41 (2008)
  1000–1005, doi:10.3182/20080706-5-kr-1001.00171). Full text unreachable; industrial-preference
  statements are taken as quoted in [LeRoux2019] (its ref. 32). The "68 responses" figure is from the
  abstract as shown in search results.
- Wills, B.A. & Finch, J.A., *Wills' Mineral Processing Technology*, 8th ed., Elsevier 2016 — Ch. 3
  "Sampling, Control, and Mass Balancing" (§3.5 "Automatic Control in Mineral Processing"), Ch. 6
  "Crushers", Ch. 7 "Grinding Mills" (pp.147–179). Only the table of contents was visible; O'Reilly and
  ScienceDirect chapter pages returned 403. **No claim above rests on Wills.**
- Dunne, R.C., Kawatra, S.K. & Young, C.A. (eds.), *SME Mineral Processing & Extractive Metallurgy
  Handbook*, SME 2019 — process-control chapters not reachable (Google Books search returned no
  snippets). **No claim above rests on it.**
- Napier-Munn, T.J., Morrell, S., Morrison, R.D. & Kojovic, T., *Mineral Comminution Circuits: Their
  Operation and Optimisation*, JKMRC 1996 — not reachable except via unauthorised copies, which were not
  used. **No claim above rests on it.**
- **[ASRi]** Sandvik Rock Processing, "ASRi — automation for optimized crusher performance",
  https://www.rockprocessing.sandvik/en/products/stationary-crushers/crusher-automation/asri/ — page
  yields only the three marketing sentences quoted in §2.2; "Auto-CSS"/"Auto-load" mode names and the
  OPC statement come from a search snippet of a Sandvik ASRi document that returned 403.
- FLSmidth ECS/ProcessExpert and KnowledgeScape (LoadIQ, GrindingExpert): fls.com product pages are
  script-rendered and returned no text; all statements in §5 are search snippets attributed to
  fls.com / E&MJ "Making the Most of a Mill" (e-mj.com, 403).
- Metso Outotec OCS-4D: no primary page found; see §5.
- Bouffard, S.C., "Benefits of process control systems in mineral processing grinding circuits",
  *Minerals Engineering* 79 (2015) 139–142, and Chen, X. et al., "Supervisory expert control for ball
  mill grinding circuits", *Expert Syst. Appl.* 34 (2008) 1877–1885 — located (DOIs resolved) but not
  read; listed as follow-up reading for the expert-system tier.
