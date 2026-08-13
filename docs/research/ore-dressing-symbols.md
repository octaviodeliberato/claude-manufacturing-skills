# Ore Dressing / Mineral Processing Symbol Standard — Primary Source Extraction

> **Status:** Primary-source research notes, not a spec. This file extracts and cross-references the
> content of `assets/PNG Ore Dressing/Standard Symbols for Mineral Processing-Code508.pdf` against the
> 289 PNG icons already sitting in `assets/PNG Ore Dressing/`. It exists to feed a future
> `/grill-with-docs` design session about extending `pfd-generator` (or a sibling skill) to draw
> ore-dressing / mineral-processing equipment. It makes no design decisions and defines no skill
> behavior — treat every claim below as "what the source document says," cited by page number, not as
> a recommendation.

## 0. Answering the open question: is the body text Arabic?

**No — it is Persian (Farsi), not Arabic**, despite being written in the Arabic script (Farsi is a
distinct language that borrows the Arabic alphabet, the way Portuguese and Italian share the Latin
alphabet). Evidence:

- The cover page reads "جمهوری اسلامی ایران" (Islamic Republic of Iran) and "وزارت صنایع و معادن"
  (Ministry of Industries and Mines) — p.1.
- Persian-specific grammar and vocabulary throughout (e.g., the Persian ezāfe construction "ی"،
  possessive/plural markers "ها", verbs like "می‌شود" that don't exist in Arabic) — pervasive, e.g. p.7–8.
- The publisher's back-cover credit reads "ﺳﺮﻛﺎر ﺧﺎﻧﻢ ﻣﻬﻨﺪس ﺑﻬﻨﺎز ﭘﻮرﺳﻴﺪ" and other Persian honorifics — p.7.
- The document's own year "1388" (p.1, p.7) is a Solar Hijri (Persian) calendar year, corresponding to
  ~March 2009–March 2010 — consistent with the PDF's embedded metadata `creationDate:
  2009-12-20 14:19:39 +03:30` and `modDate: 2010-04-26 09:57:30 +04:30`, both using Iran Standard
  Time UTC offsets.
- p.86 (the English-language title page near the back of the file) confirms this directly: **"Islamic
  Republic of Iran / Vice Presidency for Strategic Planning and Supervision"**, dated **2010**.

The user's guess that "tables are in English" is correct in spirit: table **headers** and equipment
**titles** are bilingual (Persian + English side by side, see §2), but the surrounding descriptive prose
and all front/back matter is Persian only.

## 1. Front matter (authority, provenance, scope)

| Field | Value | Page |
|---|---|---|
| English title | *Standard Symbols for Mineral Processing Flowsheets* | p.86 |
| Persian title | علائم استاندارد نقشه‌های فرآوری مواد معدنی (کانه آرایی) — "Standard symbols for mineral-processing (ore-dressing) drawings" | p.1 |
| Publication number | نشریه شماره ۵۰۸ / **No. 508** — matches the "Code508" in the PDF's own filename | p.1, p.86 |
| Publisher | Islamic Republic of Iran, Vice Presidency for Strategic Planning and Supervision (معاونت برنامه‌ریزی و نظارت راهبردی رئیس جمهور), Office of Deputy for Strategic Supervision, Bureau of Technical Execution System (دفتر نظام فنی اجرایی) | p.1, p.86 |
| Co-sponsor | Ministry of Industries and Mines (وزارت صنایع و معادن), Deputy Office of Mining Affairs and Mineral Industries, Office for Mining Exploitation and Supervision | p.1, p.86 |
| URLs (as printed, likely stale today) | http://tec.mporg.ir, http://www.mim.gov.ir | p.1, p.86 |
| Year | 1388 (Solar Hijri) = **2009–2010**; back-cover states **2010** | p.1, p.7, p.86 |
| PDF technical metadata | Created 2009-12-20, Distiller 7.0; Producer: Acrobat Distiller 7.0 (Windows); 88 pages total | (file metadata) |
| Authoring committee | Named mining/metallurgical engineers and geologists, several with PhDs from Amirkabir University of Technology (دانشگاه صنعتی امیرکبیر) | p.8 |
| Scope statement | Preface explains the standard exists to give Iran's mineral-processing-plant designers a **unified equipment-numbering system** (Ch. 2) and a **unified symbol set** (Ch. 3) for flowsheet (PFD) drawings, drawing on both international standards/associations and Iranian expert practice | p.7 |
| Bibliography | 20 numbered sources, mixing English mineral-processing textbooks (Wills' *Mineral Processing Technology*, SME handbooks, Mular & Bhappu, King's *Modeling & Simulation*, Coulson & Richardson) and Persian-language textbooks, plus "Microsoft Visio" (source #18) and "USIM PAC 3.0.7.4, BRGM" (source #2) | p.83 |

**Authority read:** this is a national (Iranian government) technical-standards publication from a
recognized ministry/planning-organization process (named authors, formal review workflow described on
p.5), not a vendor catalog or informal compilation. It is ~15–16 years old (2010) — current enough that
the equipment vocabulary (SAG mills, VERTIMILL®, flotation columns, HPGR-adjacent crushers, HIMS/LIMS
magnetic separators) is still standard mineral-processing terminology, but a design session should treat
it as **one input**, not the final word — ISA-5.1 (already used by `pfd-generator`) has no ore-dressing
equivalent, so this Iranian standard is filling a real gap rather than competing with an existing
convention already in the skill.

## 2. Document structure

The PDF has three chapters plus front/back matter (88 pages total):

- **Chapter 1** (p.11–18ish): types of process diagrams/drawings used in mineral processing (flowsheets, etc.)
- **Chapter 2** "Equipment and Document Numbering System" (فصل دوم، p.19–38): defines a **comprehensive
  equipment tag-numbering scheme**, format `LLNN-LL-NLLN` (area number, sub-area number, main equipment
  class code, subclass code, serial number) — p.21. Relevant detail: **the 2-letter "index" code seen in
  the table headers and PNG filenames (e.g. `CR-JS`) is explicitly the "main class" + "subclass" segment
  of this larger tag scheme**, not a standalone identifier (§2.2.5, p.21). Per that section: *"در مواردی
  که تجهیز فرعی وجود ندارد از حرف 'O' استفاده می‌شود"* — "where no subclass exists, the letter 'O' is
  used" — which is exactly why every category has an `XX-OO` header row (e.g. `RB-OO`, `CR-OO`, `ML-OO`).
- **Chapter 3** "Standard Symbols of Operational Units" (فصل سوم، p.39–82): **this is the symbol table** —
  20 equipment categories, each with a `رده اصلی` (main category) header row, then one row per specific
  equipment type giving Persian name, English title, graphic symbol, and a numeric source reference back
  to the bibliography (p.83).
- **Back matter** (p.83–88): bibliography (p.83), a closing note from the publisher (p.85, Persian), the
  **English-language title page** (p.86), and a one-paragraph Persian abstract/scope statement (p.88).

## 3. Table structure (Chapter 3, pp.39–82)

Every table page repeats this column header row (Persian, p.39 and every subsequent table page):

`شاخص` (Index/code) | `رده اصلی` (Main category) | `رده فرعی 1` (Subcategory 1) | `رده فرعی 2` (Subcategory 2) | `عنوان انگلیسی` (English title) | `نماد گرافیکی` (Graphic symbol) | `منبع` (Source reference #)

In practice, for each equipment row the extracted text yields: Persian equipment name → English title →
numeric source reference (pointing into the p.83 bibliography, e.g. "5" = Denver Sala Basic Selection
Guide) → the `XX-YY` code → a Persian description paragraph. The graphic-symbol column is an embedded
image in the PDF (not extracted as text) — **this is presumably the source of the 289 PNGs**, though this
research pass did not attempt to extract/compare the embedded raster images themselves, only cross-check
by filename/code (see §5).

### 3.1 The 20 categories found in Chapter 3

| Code prefix | Category (English, as printed in the doc) | Pages | # distinct codes |
|---|---|---:|---:|
| `RB` | Rock Breakers | 39 | 1 |
| `CR` | Crushers | 39–41 | 16 |
| `ML` | Mills | 42–45 | 22 |
| `SD` | Grain Size Distribution Equipment (screens/sizing) | 45–48 | 22 |
| `CL` | Classifiers | 49–53 | 27 |
| `MS` | Magnetic Separators | 53–56 | 20 |
| `ES` | Electrostatic Separators | 57 | 4 |
| `GS` | Gravity Separation Equipment (jigs, tables, spirals, HMS, concentrators) | 57–66 | 54 |
| `FL` | Flotation Machines | 66–67 | 8 |
| `TH` | Thickening | 67–68 | 8 |
| `FT` | Filtration | 68–71 | 16 |
| `PU` | Pumps | 71 | 6 |
| `CT` | Conditioners (Tanks) | 72 | 4 |
| `DR` | Dryers | 72–73 | 6 |
| `FD` | Feeders | 73–74 | 7 |
| `LE` | Leaching | 74–75 | 11 |
| `OP` | Output (product-stream symbols, e.g. "2-Output Splitter") | 76 | 2 |
| `CO` | Collectors (dust collection, recycling, land-fill, sorting — see §3.2 caveat) | 76–78 | 13 |
| `GE` | General Equipment (furnaces, conveyors, silos, chutes, tailings dams, mixers, stacks) | 78–82 | 26 |
| `SR` | Washing | 82 | 2 |

**Total: 275 distinct `XX-YY` codes with an attached English title in the extracted text**, across pages
39–82 (Chapter 3 body).

### 3.2 Extraction caveat: `CL` vs `CO` on pages 76–78 (important for anyone re-deriving this table)

The raw PDF text extraction (via PyMuPDF) renders every code on pages 76–78 as `CL-xx` (e.g. `CL-CO`,
`CL-TR`, `CL-AC`), which collides with the unrelated `CL` = Classifiers block on pages 49–53. This is
almost certainly a **font/glyph-substitution artifact** in this specific font subset (an old
Distiller-7-produced PDF), not a real reuse of the prefix in the standard:

- The category header itself literally spells out **"Collectors"** in English at the top of that block
  (p.76: `CL-OO ... Collectors`), so the intended prefix is `CO` (Collection), not `CL` (Classifier).
- The 13 PNG files actually shipped for this section are named `CO-CO.png`, `CO-CP.png`, `CO-TR.png`,
  `CO-CB.png`, `CO-CC.png`, `CO-CM.png`, `CO-CU.png`, `CO-LF.png`, `CO-RY.png`, `CO-ST.png`, `CO-AC.png`,
  `CO-EC.png`, `CO-EU.png` — **exactly** the 13 codes the extracted text shows as `CL-xx` on pp.76–78,
  with `CL`→`CO` substituted letter-for-letter.

This document treats those 13 codes as `CO-xx` throughout (corrected from the raw extraction) and notes
it here explicitly so a future re-extraction of the PDF doesn't get tripped up by the same artifact, and
so nobody concludes the standard reuses `CL` for two unrelated categories.

Two smaller, cosmetic extraction artifacts worth flagging (not corrected inline, just noted — verify
against the actual PDF/PNG if it matters for the design work):
- A few English titles picked up a stray leading `"("` or trailing single-letter fragment from an
  adjacent footnote/manufacturer-name callout during text extraction (e.g. `SD-GO` → "Grizzly" not "(
  Grizzly"; `CL-BY` → "Birtley Classifier"; `GS-JC` → "Hancock Jig"; `FT-CO` → "Cartridge Filter").
- `GS-JH`'s title extracted as "Hand Jig Hand" (word duplicated by a column-layout artifact); it's a
  **Hand Jig**.

## 4. Cross-reference against the 289 PNG files in the repo

`ls "assets/PNG Ore Dressing"/*.png` (careful: the directory name itself has spaces, so a plain `xargs
basename` over the glob will mis-split on those spaces — use a `for`/`ls`-in-directory approach) returns
exactly **289 files**. Stripping the `.png` extension and normalizing away numeric-variant suffixes
(`_1`/`_2`, `-1`/`-2`/`-3`) yields **275 distinct base codes**.

**Result: all 275 distinct PDF codes (§3.1) match all 275 distinct PNG base codes, 1:1. Zero orphans in
either direction** — no PDF table entry lacks a PNG, and no PNG lacks a PDF table entry with a matching
code (after applying the `CL`→`CO` correction in §3.2; without that correction, 13 PNGs and 13 PDF codes
would incorrectly show up as unmatched on both sides).

The 14 "extra" PNG files beyond the 275 base codes are **numbered icon variants of the same code** —
13 codes each ship 2 PNGs and one (`GE-FO`) ships 3:

| Base code | Variant files |
|---|---|
| `CL-SO` | `CL-SO.png`, `CL-SO-2.png` |
| `GE-CH` | `GE-CH.png`, `GE-CH-2.png` |
| `GE-FO` | `GE-FO-1.png`, `GE-FO-2.png`, `GE-FO-3.png` |
| `GE-MO` | `GE-MO-1.png`, `GE-MO-2.png` |
| `GE-SO` | `GE-SO.png`, `GE-SO-2.png` |
| `GS-JB` | `GS-JB.png`, `GS-JB-2.png` |
| `GS-JR` | `GS-JR.png`, `GS-JR-2.png` |
| `ML-AG` | `ML-AG_1.png`, `ML-AG_2.png` |
| `ML-BA` | `ML-BA_1.png`, `ML-BA_2.png` |
| `ML-PO` | `ML-PO_1.png`, `ML-PO_2.png` |
| `MS-HJ` | `MS-HJ-1.png`, `MS-HJ-2.png` |
| `OP-PO` | `OP-PO.png`, `OP-PO_2.png` |
| `OP-SO` | `OP-SO.png`, `OP-SO_2.png` |

Note the inconsistent naming convention for variants — some use `_1`/`_2` (underscore), others `-2`/`-3`
(hyphen, and the first variant is bare with no suffix). Neither the PDF text nor this pass determined
what distinguishes each numbered variant graphically (e.g. `OP-PO` vs `OP-PO_2` likely correspond to the
PDF's own "1-Output Plant" vs "2-Output Plant" sub-rows sharing the `OP-PO` code — see the `OP` codes in
§5 below — but this wasn't verified against the actual images in this pass).

**289 total PNGs = 275 unique codes + 14 extra numbered-variant files.** No PNG is unattributable to the
PDF table; no documented code is missing an icon.

## 5. Full code → title table (all 275 codes, with page citation)

Grouped by category (see §3.1 for category names/page ranges). Titles are the English titles as printed
in the PDF; source-reference numbers (the `منبع` column) are omitted here for brevity but are visible in
Chapter 3 next to each row and resolve against the p.83 bibliography.

### RB — Rock Breakers (p.39)
`RB-OO` Rock Breaker

### CR — Crushers (p.39–41)
`CR-JD` Double Toggle Jaw Crusher · `CR-JS` Single Toggle Jaw Crusher · `CR-JU` Universal Jaw Crusher ·
`CR-CG` Gyradisc Cone Crusher · `CR-CH` Short-head Cone Crusher · `CR-CS` Standard Cone Crusher ·
`CR-GF` Fixed Spindle Gyratory Crusher · `CR-GP` Suspended Spindle Gyratory Crusher · `CR-GS` Gyratory
Crusher · `CR-HO` Hammer Crusher · `CR-IO` Impact Crusher · `CR-PO` Pebble Crusher · `CR-RD` Double-roll
Sledging Crusher · `CR-RR` Roll Crusher · `CR-RS` Single-roll Sledging Crusher · `CR-VO` VSI – Rock to
Rock (Barmac Type)

### ML — Mills (p.42–45)
`ML-AA` Aerofall Autogenous Mill · `ML-AG` Autogenous (AG) Mill · `ML-AH` Hadsel Autogenous Mill ·
`ML-AR` Hardinge Autogenous Mill · `ML-BA` Ball Mill · `ML-SA` Semi-Autogenous (SAG) Mill · `ML-PO`
Pebble Mill · `ML-RL` Roller Mill · `ML-RO` Rod Mill · `ML-RR` Raymond Mill · `ML-TO` Tube Mill · `ML-VO`
Vibrating Mill · `ML-AO` Agitated Mill · `ML-AT` Attrition Mill · `ML-CB` Conical Ball Mill · `ML-CO`
Compartmented Ball Mill · `ML-HO` Hammer Mill · `ML-IO` Impact Mill · `ML-JP` Jet Pulverizer Mill ·
`ML-SR` Rubber Roller Mill (SRR) · `ML-TM` Tower Mill · `ML-VM` Stirred Mill (VERTIMILL®)

### SD — Grain Size Distribution Equipment / Screens (p.45–48)
`SD-FO` Flat Screen · `SD-GO` Grizzly · `SD-IO` Inclined Screen · `SD-BA` Bartles–CTS Screen · `SD-BE`
Sieve Bend · `SD-CO` Curve Screen · `SD-DD` Double Deck Screen · `SD-DS` DSM Screen · `SD-DW` Drain/Wash
Screen · `SD-GV` Vibrating Grizzly Screen · `SD-HU` Hukki Screen · `SD-HY` Hydro Screen · `SD-MO`
Mogensen Screen (Sizer) · `SD-RO` Rotating Screen · `SD-TR` Trommel Screen · `SD-CA` Canal Screen ·
`SD-DR` Drum Screen · `SD-GY` Gyratory Screen · `SD-RE` Reciprocating Screen · `SD-RS` Resonance Screen ·
`SD-SH` Shaking Screen · `SD-VO` Vibrating Screen

### CL — Classifiers (p.49–53)
`CL-CO` Cone Classifier · `CL-FO` Fahrenwald Classifier · `CL-RH` Rheax Classifier · `CL-RO` Rake
Classifier · `CL-SO` Stokes Classifier · `CL-SP` Spitzkasten Classifier · `CL-BO` Bowl Classifier ·
`CL-HR` Hydro Classifier · `CL-HS` Hydroscillator · `CL-HY` Hydrocyclone · `CL-HZ` Hydrosizer · `CL-TO`
Settling Cone Classifier · `CL-AL` Alpine Classifier · `CL-BY` Birtley Classifier · `CL-CF` Centrifuge
Classifier · `CL-DC` Dry (Air) Cyclone · `CL-HU` Hukki Classifier · `CL-SC` Screw Classifier · `CL-DS`
Dynamic Separator · `CL-DY` Dynamic Classifier · `CL-EP` Electrostatic Precipitator · `CL-MP` Microplex ·
`CL-SJ` Saint Jacques Cyclone · `CL-WO` Wizzer · `CL-DI` Distributor · `CL-EL` Elutriator · `CL-WB`
Willoughby Box

### MS — Magnetic Separators (p.53–56)
`MS-LD` Low Intensity Dry Magnetic Separator (LIMS) · `MS-LS` Low Intensity Dry Magnetic Separator with
Suspended Magnets (LIMS) · `MS-HD` High Intensity Dry Magnetic Separator (HIMS) · `MS-HI` High Intensity
Dry Magnetic Separator with Induced Roll Separator (HIMS) · `MS-HK` High Intensity Dry Magnetic Separator
with Disc Separator (HIMS) · `MS-HP` High Intensity Dry Magnetic Separator – Permroll (HIMS) · `MS-HS`
High Intensity Dry Magnetic Separator with Cross-belt Separator (HIMS) · `MS-LM` Low Intensity Dry
Magnetic Separator with Drum Separator (LIMS) · `MS-LW` Low Intensity Wet Magnetic Separator · `MS-HC`
High Intensity Wet Magnetic Separator – Carpco (HIMS) · `MS-HG` High Intensity Wet Magnetic Separator –
Gill Separator (HIMS) · `MS-HJ` High Intensity Wet Magnetic Separator – Jones Separator (HIMS) · `MS-HW`
High Intensity Wet Magnetic Separator (HIMS) · `MS-LC` Low Intensity Dry Magnetic Separator – Crockett
(LIMS) · `MS-HA` High Intensity Wet Magnetic Separator – Continuous Separator (Sala-Carousel) (HIMS) ·
`MS-HB` High Intensity Wet Magnetic Separator – Boxmag Separator (HIMS) · `MS-HE` High Intensity Wet
Magnetic Separator – Eriez Separator (HIMS) · `MS-HH` High Gradient Magnetic Separator (HIMS) · `MS-HN`
High Intensity Wet Magnetic Separator – Non-continuous Separator (HIMS) · `MS-HR` High Intensity Wet
Magnetic Separator – Krupp Sol Separator (HIMS)

### ES — Electrostatic Separators (p.57)
`ES-HT` High Tension Separator · `ES-IO` Induced Separator · `ES-PO` Plate Electrostatic Separator ·
`ES-RO` Roll Electrostatic Separator

### GS — Gravity Separation Equipment (p.57–66)
`GS-JH` Hand Jig · `GS-JZ` Harz Jig · `GS-JB` Bendelari Jig · `GS-JD` Denver Jig · `GS-JP` Pan-American
Placer Jig · `GS-JR` Russian Jig (a second `GS-JR` row on p.59 is titled "Richards Jig" — see note below)
· `GS-JT` Batac Jig · `GS-JU` Baum Jig · `GS-JC` Hancock Jig · `GS-JF` Feldspar Jig · `GS-JI` Radial
(IHC) Jig · `GS-JN` Pneumatic Jig · `GS-JY` Yuba Jig · `GS-TW` Wilfley Table · `GS-TB` Bartles-Mozley
Slime Table · `GS-TC` Bartles–Crossbelt Concentrator · `GS-TD` Deister Table · `GS-TK` Buckman Table ·
`GS-TL` Rand Leases Plane Table · `GS-TR` Revolving Round Table · `GS-TS` Slime Table · `GS-MG`
Multi-Gravity Separator (MGS) · `GS-TA` Air (Pneumatic) Table · `GS-TG` Shaking Grease Table · `GS-TH`
Shaking Table · `GS-TM` Campbell Bumping Table · `GS-TV` Vibrating Grease Table · `GS-TY` Corduroy Table
· `GS-BB` Bartless Belt Separator · `GS-BO` Blanket · `GS-DS` Drum Separator · `GS-HM` Cone Heavy Media
Separator · `GS-PA` Palong or Sluice · `GS-PS` Pinched Sluice · `GS-RC` Reichert Cone · `GS-CC` Chance
Cone Heavy Media Separator · `GS-DO` Cylindrical Media Separator · `GS-DW` Dyna Whirlpool Heavy Media
Separator · `GS-NH` Norwalt Heavy Media Separator · `GS-TF` Tri-Flo · `GS-VH` Vorsyl Heavy Media
Separator · `GS-WC` Wemco Cone Heavy Media Separator · `GS-DC` Dense Medium Cyclone · `GS-HD` HMS Drum or
Trough · `GS-HH` HMS Cyclone · `GS-HO` HMS Cone · `GS-KO` Knelson Heavy Media Separator · `GS-WO`
Water-only Cyclone · `GS-EB` Vanner or Endless Belt · `GS-GD` GEC Duplex Concentrator · `GS-SH` Humphreys
Spiral · `GS-SR` Richard Spiral · `GS-SV` VXS Spiral · `GS-CE` Centrifugal Concentrator

*(`GS-JB` similarly has two rows in the extracted text — "Bendelari Jig" on p.58 and "Johnson Barrel" on
p.65 — same likely cause as the `CL`/`CO` collision, i.e. two different table rows landed on the same
2-letter code during extraction; not resolved further in this pass. Flag for verification against the
PDF's embedded images if `GS-JB`/`GS-JR` matter to the design work.)*

### FL — Flotation Machines (p.66–67)
`FL-BC` Double Cylindrical Flotation Bank · `FL-BR` Triple Flotation Bank · `FL-CF` Column Flotation ·
`FL-MC` Mechanical Flotation Cell with Agitator · `FL-WF` Wemco Fagergren Cell · `FL-AF` Aero Flotation ·
`FL-EF` Electro Flotation · `FL-JC` Jemsson Flotation Cell

### TH — Thickening (p.67–68)
`TH-AG` Agitator · `TH-CR` Conventional Rake Thickener · `TH-HR` High-Rate Thickener · `TH-CL` Clarifier
· `TH-DN` Decanter · `TH-LO` Lamella Thickener · `TH-PO` Paste Thickener · `TH-SR` Scrubber

### FT — Filtration (p.68–71)
`FT-AO` Air Filter · `FT-BV` Belt Vacuum Filter · `FT-BW` Belt Vacuum Filter – Washer · `FT-CO`
Cartridge Filter · `FT-DV` Drum Vacuum Filter · `FT-LV` Leaf Vacuum Filter · `FT-PV` Plane Vacuum Filter
· `FT-UV` Disc Vacuum Filter · `FT-BF` Bag Filter · `FT-CW` Cartridge Filter – Washer · `FT-PC` Pressure
(Press) Filter with Compressed Chamber · `FT-PO` Pan Filter · `FT-PR` Pressure (Press) Filter · `FT-PS`
Pressure (Press) Filter with Sump · `FT-PW` Pressure (Press) Filter – Washer · `FT-BO` Belt Filter

### PU — Pumps (p.71)
`PU-BR` Bradel Pump · `PU-CF` Centrifugal Pump · `PU-CU` Clean-up Pump · `PU-MT` Metering Pump · `PU-PD`
Positive Displacement Pump · `PU-SU` Sump Pump

### CT — Conditioners / Tanks (p.72)
`CT-CO` Conditioner Tank · `CT-HO` Hutch · `CT-PA` Pachuca Tank · `CT-TO` Tank

### DR — Dryers (p.72–73)
`DR-CD` Conveyor Dryer · `DR-DO` Dryer · `DR-FD` Flash Dryer · `DR-RD` Rotary Dryer · `DR-FB` Fluid Bed
Dryer · `DR-SD` Spray Dryer

### FD — Feeders (p.73–74)
`FD-AF` Apron Feeder · `FD-CF` Chain Feeder · `FD-DF` Drum Feeder · `FD-VF` Vibrating Feeder · `FD-DS`
Double Scoop Feeder · `FD-SF` Screw Feeder · `FD-TF` Spout Feeder

### LE — Leaching (p.74–75)
`LE-AC` Autoclave · `LE-AD` Adsorption/Desorption Column · `LE-MS` Mixer-Settler · `LE-TO` Leaching Tank
· `LE-BA` Bioreactor with Addition · `LE-BG` Bioreactor (Addition & Gas) · `LE-CE` Cementation · `LE-EC`
Electrolysis Cell · `LE-EV` Evaporator · `LE-HP` Heap Leaching · `LE-RA` Reactor with Addition

### OP — Output / Product Streams (p.76)
`OP-PO` "1-Output Plant" / "2-Output Plant" (two sub-rows share this code) · `OP-SO` "2-Output Splitter"
/ "3-Output Splitter" (two sub-rows share this code)

### CO — Collectors (p.76–78) — *see §3.2, extracted as `CL-xx` in the raw text; corrected to `CO-xx` here*
`CO-CO` Collection · `CO-CP` Collection Point · `CO-TR` Transport · `CO-CB` Compositing BRS · `CO-CC`
Composting · `CO-CM` Composting *(duplicate title in source; distinct code from `CO-CC`)* · `CO-CU`
2-Output Compositing · `CO-LF` Land Fill · `CO-RY` Recycling · `CO-ST` Sorting · `CO-AC` Air Classifier ·
`CO-EC` Eddy Current Separator · `CO-EU` 3-Output Eddy Current Separator

### GE — General Equipment (p.78–82)
`GE-AF` Anode Furnace · `GE-CF` Convertor Furnace · `GE-FO` Furnace (generic) · `GE-IN` Incineration ·
`GE-CS` Covered Stockpile · `GE-OB` Ore Bin, Bunker · `GE-SG` Storage · `GE-SK` Stack · `GE-SO` Silo ·
`GE-SP` Stockpile · `GE-ST` Spray Tower · `GE-CH` Fixed Chute (2nd row: Wheeled Chute) · `GE-CV` Belt
Conveyor · `GE-CY` Cyclosizer · `GE-HB` Handpicking Belt · `GE-MO` Mixer · `GE-RW` Ropeway · `GE-WD`
Waste Dump · `GE-AT` Attritor · `GE-DR` Double Regulator · `GE-HP` Heap · `GE-SD` Sump–Distributor–
Regulator · `GE-SR` Sump Regulator · `GE-TD` Downstream Tailings Dam · `GE-TC` Centerline Tailings Dam ·
`GE-TU` Upstream Tailings Dam

### SR — Washing (p.82)
`SR-WB` Washing (Barrel) · `SR-WT` Washing Barrel with Trommel

## 6. Open items / things a design session should double-check

1. **The `CL`/`CO` prefix substitution (§3.2)** is inferred from cross-referencing the PNG filenames and
   the printed English category header, not from a clean text extraction — worth a visual sanity check
   against a couple of the actual table pages (76–78) if anyone wants to be fully sure before citing this
   file's `CO-xx` codes elsewhere.
2. **`GS-JB` and `GS-JR`** each show two different English titles at two different page locations for the
   same code (§5 notes) — not resolved; likely the same kind of extraction collision as `CL`/`CO`, but
   with a lower-confidence fix since there's no PNG-filename tiebreaker (there's exactly one `GS-JB.png` +
   `GS-JB-2.png` pair, so it's plausible the two titles correspond 1:1 to the two numbered variants —
   *not verified*).
3. **What distinguishes numbered icon variants** (`_1`/`_2`/`-2`/`-3` in §4) was not determined — this
   pass only confirmed the codes match; it did not open and compare the PNGs against the PDF's embedded
   symbol images.
4. **Graphic symbols themselves were not extracted or visually compared** — this file establishes that a
   PDF table entry and a PNG filename exist for the same code, not that the shipped PNG actually matches
   the symbol drawn in the PDF. Worth a spot-check before treating the PNGs as ground truth for icon
   geometry.
5. Chapter 1 (diagram/drawing types) and Chapter 2's full numbering-scheme tables (pp.11–38) were skimmed
   for structure but not fully transcribed here, since the immediate need was the equipment symbol table
   (Chapter 3). Revisit those chapters if the design session needs the full tag-numbering convention
   (`LLNN-LL-NLLN`) rather than just the 2-letter+2-letter equipment class code.

## 7. Follow-up verification pass

This section resolves the four items §6 flagged as unverified. It's a targeted re-read of specific pages
(rendered directly from the PDF to raster images via PyMuPDF, since the sandbox lacked `pdftoppm`/`pdftotext`
— text-layer extraction was cross-checked against the rendered images throughout, not trusted alone, given
§3.2's history of extraction surprises), not a new independent pass. Where a §6 item is confirmed or
overturned, that's stated explicitly.

### 7.1 Licensing / copyright status — no explicit statement found (item 1, §6 not previously covered)

Checked pp.1, 5, 7, 85, 86, 88 specifically for a copyright notice, rights statement, "all rights reserved,"
public-domain declaration, or reproduction/usage terms. **None of the six pages contain any such
statement** — not a copyright notice, not a permissive grant, not a public-domain declaration. Specifically:

| Page | Content | Rights/license language present? |
|---|---|---|
| p.1 | Persian cover page: title, publisher/co-sponsor names, publication number 508, year 1388 | None |
| p.5 | "اصلاح مدارک فنی" (Technical-document correction) — a reader-feedback page inviting readers to report errors (page/section, error summary, suggested fix, contact info) to the Bureau of Technical Execution System, with a mailing address, phone, and `tsb.dta@mporg.ir` | None — this is an errata-reporting invitation, not a rights notice |
| p.7 | Persian preface ("پیشگفتار") — explains the standard's legal basis: it was issued under **Cabinet Resolution No. 42339/T33497H, dated 1385/4/20** (~2006-07-11), approving the "Technical and Executive System of the Country" (نظام فنی و اجرایی کشور), which mandates unified numbering/symbol standards to control lifecycle costs of mineral-processing plant design; explains scope, chapter structure, and thanks named contributors | None — legal/administrative basis for the standard's *existence*, not a copyright or reproduction clause |
| p.85 | "خواننده‌ی گرامی" (Dear reader) — describes the Bureau of Technical Execution System's 30+ years of publishing ~500 numbered technical bulletins/standards and points to `http://tec.mporg.ir` for the full catalog | None |
| p.86 | English title page: title, publisher (Vice Presidency for Strategic Planning and Supervision), co-sponsor (Ministry of Industries and Mines), URLs, "No. 508," year 2010 | None |
| p.88 | "این نشریه" (This publication) — one-paragraph Persian abstract: standardizes symbols for mineral-processing flowsheets, provides a comprehensive equipment/document numbering system, and defines the terms used | None |

**Read on this:** this is a free Iranian-government technical bulletin (نشریه) with no attached
copyright/reproduction boilerplate anywhere in the front or back matter, which is common for this class of
government "نظام فنی" publication. But the absence of an explicit statement is not itself a license — it
should not be read as "therefore public domain" or "therefore free to redistribute." Under default copyright
rules (Iran's own framework, and more relevantly whatever law would govern a US-hosted, MIT-licensed GitHub
repo redistributing derivative or verbatim copies of the drawings), a work is protected unless it's
affirmatively placed in the public domain or licensed — silence defaults to "all rights reserved," not to
permission. **This finding only establishes that the primary source is silent on reproduction terms; it does
not clear the way to bundle or redistribute the symbol drawings themselves in the repo's downloadable skill
zips.** That remains an open legal question for whoever makes the later design decision this research file
was meant to feed — treat "no statement found" as "unresolved, needs a legal/policy call," not as tacit
permission.

### 7.2 The `CL`/`CO` prefix collision on pp.76–78 — CONFIRMED as a genuine primary-source defect; §3.2's "extraction artifact" theory is OVERTURNED

§3.2 guessed this was "almost certainly a font/glyph-substitution artifact" of PyMuPDF's text extraction. That
guess is wrong. Re-rendering pp.76–78 directly to high-resolution raster images (bypassing the text layer
entirely — this is pixel-level glyph shape, not decoded character codes) shows the same thing the text layer
showed: **the PDF itself, visually, prints "CL-OO", "CL-CO", "CL-TR", "CL-CP"** for the Collectors category
header and its first three rows on p.76, continuing as `CL-LF`, `CL-RY`, `CL-CC`, `CL-CB`, `CL-CM`, `CL-CU`,
`CL-ST` (p.77) and `CL-EC`, `CL-EU`, `CL-AC` (p.78). A tight crop of the "CL-CO" cell shows an unambiguous
`L` glyph (straight vertical stroke + right-angle foot) immediately next to a round `O` in the same cell
("CL-**O**O" above it) — there's no font-substitution ambiguity here; a human reading the physical PDF page
sees the same "CL" a machine text-extraction sees.

This means **the primary source itself has a genuine typo/copy-paste defect**, not a PDF-tooling artifact:
the Collectors category (pp.76–78) was typeset with the same "CL" prefix as the unrelated Classifiers
category (pp.49–53), confirmed via the PDF's own text layer word-boxes (`CL-OO`, `CL-CO`, `CL-TR`, `CL-CP` on
p.76; `CL-LF`…`CL-ST` on p.77; `CL-EC`, `CL-EU`, `CL-AC` on p.78 — 16 tokens total, matching all 13 Collector
rows plus the 3-page category header).

Stronger confirmation than §3.2 had: **Chapter 2's own equipment-class index (Table 2-3, p.23)** —
independent of both the PNG filenames and Chapter 3's own body text — explicitly and unambiguously lists
`CL` = CLASSIFIER (کلاسیفایر) and `CO` = COLLECTOR (کلکتور) as two *separate* defined 2-letter codes, in the
same alphabetical table as `CR`, `CT`, `CV`, `DR`, etc. So the standard's own numbering-system chapter
confirms Collectors is supposed to be `CO`, making the "CL" printed on pp.76–78 an internal inconsistency
against the *document's own Chapter 2 definition table*, not just against the PNG filenames used to infer it
in §3.2.

Bonus finding while re-checking the Classifiers block (pp.49–53) for "legitimate prefix reuse," per the
task's ask: no reuse of `CL` for anything other than Classifiers was found there, but there **is** a
same-category internal duplicate — `CL-SO` is used for both "Stokes Classifier" and "Spiral Classifier" (two
separate rows on p.49, confirmed by both the text layer word boxes and the rendered image, at
y≈290.8 and y≈733.2 respectively on that page). The existing §5 table only lists `CL-SO` = Stokes Classifier;
Spiral Classifier isn't listed separately because it collides with the same code. This wasn't asked for
explicitly but shows the standard's authors were generally loose about 2-letter-code uniqueness — the
CL/CO whole-category collision on pp.76–78 is the most consequential instance, but not the only one.

**Verdict:** the `CL`/`CO` collision is CONFIRMED as real (in the source, at the glyph level) — overturning
§3.2's "font/glyph-substitution artifact" explanation — but the practical conclusion this file already
reached (treat those 13 pp.76–78 codes as `CO-xx`, matching both the PNG filenames and Chapter 2's Table 2-3)
remains the correct call.

### 7.3 `GS-JB` and `GS-JR` duplicate titles — CONFIRMED as genuine duplicate rows (not extraction collisions); PNG variants matched to specific titles

Both codes are genuinely reused for two distinct table rows with two distinct graphic symbols in the primary
source — this is a different kind of duplication than CL/CO (isolated single-row collisions, not a
whole-category substitution), but it is equally real, not an artifact.

**`GS-JB`:**
- p.58: **Bendelari Jig** (بندلاری), main category جیگ (Jig), subcategory آبی (Wet), source ref. 14. Symbol:
  a tall rectangular body with three small inlet slots at the top and a diagonal/diaphragm-style converging
  taper to a round base at the bottom.
- p.65: **Johnson Barrel** (جاتسون), main category **بشکه (Barrel/Drum)** — a *different* main category from
  Jig — source ref. 3, described as "a separator made of a rotating cylinder, 3.6 m long, 0.75 m diameter,
  with a relatively shallow slope (2.5–5°)." Symbol: a circle with an internal V/chevron divider, arrow in at
  top, arrow out right, arrow out bottom.

**`GS-JR`:**
- p.58: **Russian Jig** (روسی), main category جیگ (Jig), subcategory آبی (Wet), source ref. 9. Symbol: a wide
  V-bottomed vessel with **two** diagonal inlet arrows entering from the upper-left, one outlet arrow to the
  right, dashed internal divider, **no** bottom outlet arrow.
- p.59: **Richards Jig** (ریچاردز), same main/subcategory, source ref. 9, described only as "a type of wet
  jig." Symbol: a narrower vessel with a raised chimney-neck **single** top inlet, dashed internal divider,
  outlet arrow to the right (double-chevron line style), **and** a bottom outlet arrow — visibly different
  from Russian Jig's symbol in inlet count and the presence of a bottom outlet.

Cross-referencing the two PNG variants per code against these two distinct PDF symbols gives a confident,
feature-based 1:1 match (compared inlet-arrow count, presence/absence of a bottom outlet, and overall vessel
shape — not just eyeballing similarity):

| PNG file | Matches |
|---|---|
| `GS-JB.png` | **Johnson Barrel** (p.65) — circle + internal V-chevron + in/right/down arrows |
| `GS-JB-2.png` | **Bendelari Jig** (p.58) — tall box, top inlet slots, diaphragm taper to round base |
| `GS-JR.png` | **Richards Jig** (p.59) — narrow chimney-neck single inlet + bottom outlet arrow |
| `GS-JR-2.png` | **Russian Jig** (p.58) — wide V-bottom, two diagonal inlets, no bottom outlet |

**Verdict:** this resolves §6 item 2's "not verified" flag — these are genuine duplicate-code rows in the
primary source (like CL/CO, a real defect, not a PDF-extraction glitch), and the PNG-variant-to-title mapping
above is now established with reasonable confidence from direct visual comparison of the symbol geometry.

### 7.4 Chapter 2's equipment tag-numbering scheme (item 4)

**Format correction.** The abstract format captured earlier in this file (`LLNN-LL-NLLN`) does not match what
the primary source actually prints. Re-reading p.21 directly (§2.2, "شماره‌گذاری تجهیزات" / Equipment
Numbering) — including decoding which 1–4-character span is set in a distinguishing (bold/underlined) font
for each of the six defined sub-fields, verified via the PDF's own text-layer word-boxes as well as the
rendered image — the actual format is:

**`NNLL-LL-LLNN`**, i.e. `[NN][LL]-[LL]-[LL][NN]`, where:

| Segment | Meaning | Source |
|---|---|---|
| 1st `N` | Main area number (1 digit, 0–9) | Table 2-1 (p.22), e.g. `4` = CONCENTRATOR |
| 2nd `N` | Sub-area number (combines with the 1st digit into a 2-digit code) | Table 2-2 (p.22), e.g. `41` = GRINDING (note the sub-area code's own first digit repeats the main-area digit) |
| 1st `LL` (chars 3–4, still inside the first dash-delimited block) | Main equipment class code | Table 2-3 (p.23) — **this is the same 2-letter prefix used throughout Chapter 3**, e.g. `CR`=CRUSHER, `ML`=MILL, `CL`=CLASSIFIER, `CO`=COLLECTOR |
| Middle `LL` (between the two dashes) | Sub equipment class code | referenced as "فهرست رده فرعی تجهیزات" (Sub equipment class list), no separately numbered table shown for this segment specifically |
| 3rd-block `LL` | Sub-equipment list code | Table 2-4 (pp.23–27) — a much longer, ~150-entry alphabetical list of generic plant-wide accessory/subsystem codes, e.g. `AB`=FLOTATION AIR BLOWER, `JB`=JUNCTION BOX, `MO`=MOTOR, `VA`=VALVES. **This is a different code list from Chapter 3's equipment codes** and explains why 2-letter combinations like `JB` show up in two unrelated contexts across this standard. |
| 3rd-block `NN` | Equipment serial number within its area | §2.2.6 (p.26): "این عدد دو رقمی به شماره‌ی سریال تجهیزات در هر ناحیه اشاره دارد" — "this two-digit number refers to the equipment's serial number within each area" |

**No worked example exists in the primary source.** Despite defining the format precisely, Chapter 2
(pp.19–38) never shows it instantiated with real values — there is no "e.g., tag `41ML-BA-XX01` = ..." style
illustration anywhere in the chapter. Confirmed by: (a) a full-text search across all 20 pages for Persian
words meaning "example"/"sample" (مثال، نمونه، مثلا، فرضی) — zero hits; (b) a regex search for any
digit+letter+dash token shaped like an instantiated tag — zero hits; (c) visually reviewing every page in the
chapter, which is entirely composed of the seven lookup tables (2-1 through 2-7, covering area numbers,
sub-area numbers, main/sub equipment class codes, document-usage numbers) plus one-paragraph section
definitions — no illustrative figure or worked instance appears. p.36, the last page of the chapter, is
blank. **This should be flagged for the design session**: the format's abstract shape is fully specified and
now correctly captured above, but nobody reading only this document sees it applied to a concrete example —
constructing one (e.g., "a Ball Mill in the Grinding sub-area, serial 01, would tag as `41ML-BA-??01`" — the
middle "sub equipment class" 2-letter segment is still unclear from the tables alone, since Table 2-3's
Mill entry doesn't cross-reference which "LL" values are valid subclasses for it) would require synthesis
this document doesn't provide.

**Chapter 1 instrumentation/control-loop content.** Chapter 1 (pp.11–18, "نمودارها و نقشه‌های متداول در
فرآوری مواد معدنی" — Diagrams and Drawings Common in Mineral Processing) is *not* purely about
equipment/stream topology — it explicitly requires instrumentation and control-loop information on certain
diagram types, though generically, with no ore-dressing-specific instrumentation symbol convention of its
own:

- §1.4 "معیارهای طراحی" (Design Criteria, p.13–14) lists **Instrumentation Design Criteria** (معیار طراحی
  ابزار دقیق, footnoted in English) as one of six required design-criteria categories a project must define
  (alongside Process Units, Mechanical, Electrical, Structural/Concrete, and Piping design criteria).
- §1.5.7 "نمودارهای لوله‌کشی و ابزار دقیق (P&IDs)" (Piping and Instrument Diagrams, pp.15–16) is the section
  that actually engages with control loops: it requires every P&ID line to carry, among an 11-item checklist,
  item (b) — "ابزار دقیق با همکنش‌گرهای لازم و حلقه‌های کنترلی" — **"instruments together with their
  necessary interconnection symbols and control loops."** Other required items: mechanical equipment ID (a);
  pipe connections/dimensions/specs (c); valves with specs (d); vents/drains/special connections/sampling
  lines/reducers (e); flow direction (f); each interconnector's off-page reference spec (g); interconnector
  inputs/outputs (h); plant-wide interlocks (i); a legend for symbols used (j); and a reference list (k).
- §1.5.5 "نمودارهای مداری" (Circuit Diagrams, p.15) separately covers hydraulic/pneumatic systems
  specifically, "to show control valves, pipeline control equipment, and hydraulic/pneumatic interface
  points."
- Nowhere in Chapter 1 does the document define its own bubble/tag-notation symbol set for instruments or
  control loops (nothing resembling ISA-5.1's circle-in-square instrument bubbles). It mandates *that* P&IDs
  and circuit diagrams carry this information, without specifying *how* to draw it — implicitly deferring to
  general engineering P&ID convention. Consistent with §3.1: Chapter 3's 20 symbol categories are all process
  equipment (crushers, mills, screens, jigs, etc.); there is no instrumentation/control-loop category among
  them, and this follow-up pass found nothing elsewhere in the document that fills that gap.
