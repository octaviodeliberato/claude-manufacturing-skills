---
name: mineral-processing-pfd
description: Generate a conceptual mineral-processing/ore-dressing flowsheet (PFD) as an editable SVG, along with the Python script that produced it. Use when the user describes a comminution, classification, flotation, or dewatering circuit and asks to draw, diagram, sketch, or visualize it; when they mention a mineral-processing flowsheet, ore-dressing PFD, or equipment like a crusher, SAG/ball mill, screen, hydrocyclone, flotation cell, thickener, or HPGR; or when they ask to edit an existing mineral-processing PFD SVG. Also use when they ask to add a control strategy, control philosophy, control loops, instrumentation or automation to a crushing or grinding flowsheet, ask for basic/intermediate/advanced control, mill load control, cyclone feed density control, or a control narrative. Not a substitute for an issued-for-design flowsheet - does not size equipment, does not perform metallurgical balance calculations, and does not perform hazard analysis.
---

# Mineral Processing PFD Generator

Produce a conceptual mineral-processing flowsheet as a hand-authored SVG that a process/metallurgical engineer would accept: correct equipment vocabulary, correct process flow, closed control loops where instrumentation exists, and a layout with zero collisions and zero crossed process lines. Sibling skill to `pfd-generator` (chemical-process P&IDs) — see `docs/adr/0001-mineral-processing-pfd-forks-primitives.md` for why this skill carries its own copy of the generic drawing primitives rather than importing `pfd-generator`'s.

The output is judged by an engineer who will spot a crusher symbol standing in for a mill, a screen with the wrong deck count, or an unlabeled slurry line. Accuracy and legibility rank above speed.

### Non-negotiable output rules

Same six rules as `pfd-generator`, unchanged:

1. **No hidden text.** Every label must be fully readable. Nothing may sit under a line, symbol, or another label.
2. **No crossing process lines.** Solve crossings by re-planning elevations, not by drawing over. If one is truly unavoidable, draw a proper line jump (semicircular hop, see `pipe`/`line_jump` in `scripts/pid_lib.py`).
3. **Control loops must be complete and directional.** Every loop is measurement → controller → final element, with an arrowhead on each leg. A signal line without an arrowhead is a defect.
4. **Text is real `<text>`, never glyph paths or outlines.** The user must be able to edit labels in a text editor.
5. **Minimum font size 8.5.** Tag text 10–11.5, line labels 11–13, title 20–22.
6. **Elevations must be physically true.** Feed enters above discharge on gravity-fed equipment (crushers, screens, cyclones); pumps are the only equipment that can lift a stream against gravity.

### Workflow

#### 1. Read the description and fill the gaps

A process description almost always underspecifies the circuit. Before drawing, resolve:

- What's the ore type / separation method — flotation, magnetic, or gravity? (The shipped symbol set covers a base-metal flotation circuit end-to-end; magnetic and gravity separation equipment are out of scope for now — say so if asked for and offer the flotation equivalent instead.)
- How many crushing stages, and which crusher types?
- Screen deck counts, and wet or dry screening?
- Which classification method — cyclone, screw, or rake?
- Does any piece of equipment need instrumentation (density control on a cyclone feed, level control on a thickener, pH control ahead of flotation)? If so, which is the master/slave in a cascade?
- If the user asks for a **control strategy** (control philosophy, loops, instrumentation, automation) on a crushing or grinding circuit: resolve the **control tier** per circuit — basic, intermediate or advanced, see `references/control-strategies.md`. Default is **basic**; don't ask, assume it and state the assumption in the delivery. Advanced is never drawn unasked. Flotation/thickening control strategies aren't in the reference yet — say so rather than improvising.

Ask at most 2–3 questions, and only for things that change the drawing. For anything minor, make a defensible engineering assumption and state it afterward.

#### 2. Plan the layout on paper before writing any SVG

Write out the coordinate plan first, same discipline as `pfd-generator`:

- Default canvas `1400 × 940`, landscape, hairline border inset 20.
- Lay the circuit out left-to-right in process order (ROM ore → comminution → classification → separation → dewatering → storage/disposal), one elevation band per major stage so nothing has to cross back over itself.
- Give every horizontal run its own y and every vertical run its own x — same corridor/band discipline as any P&ID. Read `references/layout-rules.md` for the full collision-geometry and crossing-elimination rules.

#### 3. Draw

`scripts/pid_lib.py` provides the primitives. Read it before writing the script and use it rather than reinventing symbols. It has two layers:

- **Generic** (forked from `pfd-generator`, unchanged behavior apart from `legend`'s `density` flag): `pipe`, `sig`, `lead`, `line_jump`, `bubble`, `cvalve`, `manual_valve`, `vessel`, `agitator`, `equip_tag`, `legend`, `title`, `notes`, `design_basis`, `revision`; plus `motor` (ISA drive symbol, the final element for speed loops — new here, not in `pfd-generator`).
- **Mineral-processing equipment** (new): `rock_breaker`, `feeder_vibrating`, `crusher_jaw`, `crusher_cone`, `crusher_gyratory`, `crusher_vsi`, `crusher_impact`, `crusher_roll`, `screen` (parametric, 1–4 decks, wet/dry), `mill_sag`, `mill_ball` (trunnions + charge; `x0..x1` is the outer envelope including the trunnions), `cyclone`, `classifier_screw`, `classifier_rake`, `flotation_cell`, `flotation_column`, `thickener`, `filter_drum`, `pump_centrifugal`, `pump_sump`, `feeder_apron`, `conveyor`, `ore_bin`, `stockpile`, `silo`, `tailings_dam`, `splitter`, `junction`.

Read `references/mineral-processing-symbols.md` for what each symbol represents, its source-standard code, and known caveats (in particular: `crusher_roll` is the closest match for HPGR, not a literal HPGR-specific symbol — say so if the drawing includes one).

**Every equipment primitive draws only its body — never its own inlet/outlet pipe stubs.** Connect equipment with `pipe()` yourself, in `ORE` (slurry) or `SOLIDS` (dry/conveyed ore) as appropriate, `BLUE` for wash/process water. Each primitive's docstring gives the coordinates of its notable connection points (feed, discharge, overflow, underflow).

Two composition rules the primitives cannot enforce for you:

- **Every screen deck outlet gets a pipe.** `screen()` returns one oversize `y` per deck; a `deck_count` screen has `deck_count + 1` product streams (each deck's oversize plus the undersize). Pipe every one of them — a deck outlet left hanging is a defect an engineer will spot immediately, not a simplification. Where two oversizes go to the same place (the usual closed-circuit case), merge them at a `junction()` and run one line.
- **Size a cyclone to its neighbours.** `cyclone()` takes `top`/`bottom` from you; make it about the height of the adjacent mill or sump, never taller, and keep the standard's tall-narrow proportion — the cylinder is `r` high, so give the cone at least ~3`r`. It returns its `feed`/`overflow`/`underflow` points — start and end your pipes on those.

Reuse the ISA-5.1 instrumentation primitives (`bubble`, `cvalve`, `sig`) for any control loop exactly as `pfd-generator` does — the source standard defines no ore-dressing-specific instrumentation of its own, so there's nothing to substitute.

**Control strategy.** When a strategy was requested, read `references/control-strategies.md` and draw that tier's loops for every circuit present — nothing more, nothing less. Drive-speed final elements (feeder, mill, pump VSDs) terminate on `motor()`, never on a `cvalve`; it returns the point the controller's signal lands on. Water loops terminate on `cvalve`. Monitors (mill power, PSM, a leftover pressure) stop at an indicator bubble. Sump level and cyclone feed density cannot both sit on the dilution-water valve — pick the pairing the reference describes and state it. Any `DT`/`DIC` needs `legend(..., density=True)`. Stamp the sheet with a per-circuit tier note via `notes()` ("Grinding: basic (assumed)"). `examples/build_grinding_circuit_control.py` is the pattern to copy.

**Label equipment by name or a simple per-drawing tag** (e.g. "SAG Mill" or `ML-101`), via `equip_tag`. Never surface the source standard's internal `XX-YY` class code (e.g. `ML-BA`) on the drawing — it's a lookup key in the reference doc, not a drawing tag, and never surface its full `NNLL-LL-LLNN` tag format at all (this skill doesn't implement that scheme).

#### 4. Render, look at it, and fix — then repeat

**Mandatory, same as `pfd-generator`.** Do not deliver a flowsheet you have not looked at.

```bash
pip install -r scripts/requirements.txt -q   # add --break-system-packages on a managed Python
python3 build_flowsheet.py
python3 -c "import cairosvg; cairosvg.svg2png(url='out.svg', write_to='preview.png', output_width=1680)"
```

If `cairosvg` won't install (routine on Windows — it needs native Cairo/GTK), fall back to `svglib`+`pymupdf` exactly as `pfd-generator` documents, and say plainly in your response that arrowheads were verified from source rather than the fallback preview (the fallback drops SVG `<marker>` arrowheads silently — that's a rendering artifact, not a defect).

Then open `preview.png`, inspect it as an engineer would, and zoom dense clusters (crusher/screen stacks, cyclone/flotation banks) at 3200 px. Run the QA checklist in `references/layout-rules.md` §6 against what you see. Expect 2–4 rounds.

Before shipping, also run the smoke tests, which catch structural defects (missing arrowheads, raster images, malformed SVG) before you even look at a render:

```bash
python3 scripts/test_primitives.py
```

#### 5. Deliver

Save the SVG and script where the user can reach it. Keep the generator script — revisions are a script edit + re-render, not hand-patching the SVG (unless the user hand-edited the SVG themselves, in which case patch with exact string replacements and verify each one matched).

State briefly:
- Engineering assumptions made (especially ore type/separation method, screen deck counts and wet/dry, and any HPGR-as-roll-crusher approximation)
- Anything in the description that could not be drawn because it falls outside the shipped ~26-symbol set, and why
- Any design concern noticed while drawing
- When a control strategy was drawn: the **control narrative** table (columns `Loop tag | Tier | Measured variable | Manipulated variable / final element | Objective | Notes`, one row per loop, monitors marked as such) and the tier assumption ("basic tier assumed for grinding — no tier was named"), plus the level/density pairing chosen

### What this skill does not do

It draws conceptual mineral-processing flowsheets covering a base-metal flotation circuit's comminution, classification, flotation, dewatering, and material-handling equipment. It does not size equipment, does not perform metallurgical mass/balance calculations, and does not perform hazard analysis. It does not yet cover magnetic-separation or gravity-separation circuits (iron ore, gold/placer), the standard's full ~275-symbol/20-category set, or the standard's formal equipment tag-numbering scheme — say so if the user's framing implies otherwise. Control strategies are conceptual: no setpoints, tuning, controller or transmitter sizing, interlock/safety or alarm design, and no flotation or thickening control strategies yet (crushing and grinding only).
