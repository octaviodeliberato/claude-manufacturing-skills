# Mineral Processing Symbols

Maps the shipped equipment vocabulary to its `scripts/pid_lib.py` primitive function. Equipment
names and the `XX-YY` class codes are grounded in **Iran Standard No. 508 (2010), *Standard
Symbols for Mineral Processing Flowsheets*** (see `docs/research/ore-dressing-symbols.md` for the
full primary-source extraction this skill was designed from). The source document's own artwork
is not reproduced — every symbol below is an original vector drawing, informed by the standard's
pictogram shapes, not a copy of them (see `docs/adr/0002-ore-dressing-source-assets-not-committed.md`).

**The `XX-YY` code is an internal lookup key only.** Never render it onto a drawing — label
equipment by name or a simple per-drawing tag instead (see `CONTEXT.md`, "Equipment class code").

## Comminution

| Code | Standard's title | Primitive | Notes |
|---|---|---|---|
| `RB-OO` | Rock Breaker | `rock_breaker(cx, top, tag=None)` | Static grizzly + hydraulic hammer boom |
| `FD-VF` | Vibrating Feeder | `feeder_vibrating(x0, y0, x1, y1, tag=None)` | |
| `CR-JS` | Single/Double Toggle Jaw Crusher | `crusher_jaw(cx, top, bottom, tag=None)` | |
| `CR-CS` | Standard Cone Crusher | `crusher_cone(cx, top, bottom, tag=None)` | Bowl liner + suspended mantle |
| `CR-GS` | Gyratory Crusher | `crusher_gyratory(cx, top, bottom, tag=None)` | Distinct from `CR-GF`/`CR-GP` (fixed/suspended spindle variants) — not shipped |
| `CR-VO` | VSI – Rock to Rock (Barmac Type) | `crusher_vsi(cx, cy, tag=None)` | Vertical shaft impactor |
| `CR-IO` | Impact Crusher | `crusher_impact(cx, cy, tag=None)` | Horizontal shaft impactor by elimination — the standard doesn't name "HSI" explicitly, but `CR-VO` is called out separately as the vertical-shaft type |
| `CR-RR` | Roll Crusher | `crusher_roll(cx, top, bottom, tag=None)` | **HPGR caveat**: this is the standard's closest match for a high-pressure grinding roll, not a literal HPGR-specific symbol. The 2010 standard predates HPGR's widespread adoption; its "Roll Crusher" entry reads as a conventional smooth-roll crusher. Say so explicitly whenever this symbol is used to represent HPGR. |
| *(none — new parametric symbol)* | Vibrating Screen | `screen(x0, y0, x1, y1, deck_count=1, wet=False, tag=None)` | The standard's `SD-VO`/`SD-DD` don't cleanly encode deck count as distinct icon geometry (both render with the same 3-outlet layout); this primitive draws `deck_count` (1–4) internal mesh lines instead, each with its own oversize outlet. `wet=True` only changes the label — the composing script draws the wash-water inlet pipe itself. Not `SD-DW`/`SD-HY`, which are separate, distinctly-coded equipment (a wash chute and a static hydro-strainer basket), not a wet mode of this screen. |
| `ML-SA` | Semi-Autogenous (SAG) Mill | `mill_sag(x0, y0, x1, y1, tag=None)` | Few large charge circles |
| `ML-BA` | Ball Mill | `mill_ball(x0, y0, x1, y1, tag=None)` | Many small charge circles |

## Classification / Separation

| Code | Standard's title | Primitive | Notes |
|---|---|---|---|
| `CL-HY` | Hydrocyclone | `cyclone(cx, top, bottom, tag=None)` | |
| `CL-SC` | Screw Classifier | `classifier_screw(x0, y0, x1, y1, tag=None)` | |
| `CL-RO` | Rake Classifier | `classifier_rake(x0, y0, x1, y1, tag=None)` | |
| `FL-MC` | Mechanical Flotation Cell with Agitator | `flotation_cell(x0, y0, x1, y1, tag=None)` | |
| `FL-CF` | Column Flotation | `flotation_column(cx, top, bottom, tag=None)` | |

## Dewatering

| Code | Standard's title | Primitive | Notes |
|---|---|---|---|
| `TH-CR` | Conventional Rake Thickener | `thickener(cx, top, bottom, tag=None)` | |
| `FT-DV` | Drum Vacuum Filter | `filter_drum(cx, cy, tag=None)` | |

## Transport / Storage

| Code | Standard's title | Primitive | Notes |
|---|---|---|---|
| `PU-CF` | Centrifugal Pump | `pump_centrifugal(cx, cy, tag=None)` | |
| `PU-SU` | Sump Pump | `pump_sump(cx, cy, tag=None)` | |
| `FD-AF` | Apron Feeder | `feeder_apron(x0, y0, x1, y1, tag=None)` | |
| `GE-CV` | Belt Conveyor | `conveyor(x0, y0, x1, y1, tag=None)` | |
| `GE-OB` | Ore Bin, Bunker | `ore_bin(cx, top, bottom, tag=None)` | |
| `GE-SP` | Stockpile | `stockpile(cx, base_y, tag=None)` | |
| `GE-SO` | Silo | `silo(cx, top, bottom, tag=None)` | |
| `GE-TD` | Downstream Tailings Dam | `tailings_dam(x0, base_y, tag=None)` | Distinct from `GE-TC`/`GE-TU` (centerline/upstream construction methods) — not shipped |
| `OP-SO` | Output Splitter | `splitter(cx, cy, n_outputs=2, tag=None)` | 2 or 3 outbound legs |

## Out of scope for this symbol set

The remaining ~249 codes across Electrostatic Separators (`ES`), Collectors (`CO`), Leaching
(`LE`), Washing (`SR`), most Gravity Separation (`GS`) and Magnetic Separation (`MS`) equipment,
most Filtration variants beyond the drum vacuum filter, and the rest of General Equipment (`GE`)
are documented in `docs/research/ore-dressing-symbols.md` but have no primitive yet. If a drawing
needs one of these, say so plainly rather than approximating with the nearest shipped symbol —
the two approximations already made and disclosed (`CR-RR` for HPGR, `CR-IO` for HSI) are
deliberate, reviewed decisions, not a general license to substitute.

`GS-JB` and `GS-JR` (each a genuine two-title collision in the source standard, not an extraction
artifact — see `docs/research/ore-dressing-symbols.md` §7) and the `CL`/`CO` prefix typo on the
standard's own pp.76-78 are noted here for anyone extending this symbol set later; neither affects
the codes actually shipped above.
