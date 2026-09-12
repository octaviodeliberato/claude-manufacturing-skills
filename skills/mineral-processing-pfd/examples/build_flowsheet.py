# -*- coding: utf-8 -*-
"""Base-metal (copper/moly) flotation concentrator - conceptual flowsheet.
ROM ore -> crushing -> screening -> grinding -> cyclone classification ->
rougher/cleaner flotation -> concentrate dewatering, with tailings thickening
and disposal. Run from the examples/ directory."""
import sys
sys.path.insert(0, "../scripts")
from pid_lib import PID  # noqa: E402

d = PID(1900, 1380, border=True)
d.title("COPPER CONCENTRATOR - CONCEPTUAL FLOWSHEET",
         "Crushing - grinding - flotation - dewatering | Base-metal flotation MVP")

# ============================================================ Row 1: crushing
Y1 = 230
d.ore_bin(150, Y1 - 70, Y1 + 60, tag="ROM Ore Bin")
d.feeder_apron(230, Y1 - 15, 340, Y1 + 15, tag="FD-101")
d.crusher_jaw(430, Y1 - 60, Y1 + 60, tag="CR-101  Jaw Crusher")
d.conveyor(500, Y1 + 55, 610, Y1 - 10, tag="CV-101")
d.crusher_cone(680, Y1 - 60, Y1 + 60, tag="CR-102  Cone Crusher")
d.conveyor(750, Y1 + 55, 860, Y1 - 10, tag="CV-102")
screen_x0, screen_x1 = 900, 1060
deck_ys = d.screen(screen_x0, Y1 - 45, screen_x1, Y1 + 45, deck_count=2, wet=False, tag="SD-101")
d.conveyor(1130, Y1 + 55, 1240, Y1 - 10, tag="CV-103")
d.stockpile(1340, Y1 + 60, tag="GE-101  Crushed Ore Stockpile")

# feeder inlet / crusher discharge connections
d.pipe(f"M 150,{Y1+60} L 150,{Y1+90} L 230,{Y1+90} L 230,{Y1}", d.SOLIDS, arrow=True)
d.pipe(f"M 340,{Y1} L 400,{Y1-40} L 430,{Y1-40}", d.SOLIDS, arrow=True)
d.pipe(f"M 430,{Y1+60} L 430,{Y1+90} L 500,{Y1+90} L 500,{Y1+55}", d.SOLIDS, arrow=True)
d.pipe(f"M 610,{Y1-10} L 650,{Y1-40} L 680,{Y1-40}", d.SOLIDS, arrow=True)
d.pipe(f"M 680,{Y1+60} L 680,{Y1+90} L 750,{Y1+90} L 750,{Y1+55}", d.SOLIDS, arrow=True)
d.pipe(f"M 860,{Y1-10} L 890,{Y1-30} L {screen_x0},{Y1-30}", d.SOLIDS, arrow=True)
# screen undersize (final crushed product) to stockpile conveyor
fx = (screen_x0 + screen_x1) / 2
d.pipe(f"M {fx},{Y1+45+30} L {fx},{Y1+95} L 1130,{Y1+95} L 1130,{Y1+55}", d.SOLIDS, arrow=True)
d.pipe(f"M 1240,{Y1-10} L 1290,{Y1-40} L 1340,{Y1-40} L 1340,{Y1}", d.SOLIDS, arrow=True)
# screen oversize recycles back to the cone crusher feed - drawn as a loop above
# the row so it never crosses the main left-to-right flow. A 2-deck screen has
# TWO oversize streams (one per deck); the top deck only scalps to protect the
# bottom deck, so both are "too coarse" and both recycle: the bottom-deck line
# joins the top-deck line at a junction on the riser, then one loop carries both.
recycle_y = Y1 - 110
riser_x = screen_x1 + 40
d.pipe(f"M {screen_x1},{deck_ys[0]} L {riser_x},{deck_ys[0]} "
       f"L {riser_x},{recycle_y} L 680,{recycle_y} L 680,{Y1-60}", d.SOLIDS, arrow=True)
d.pipe(f"M {screen_x1},{deck_ys[1]} L {riser_x},{deck_ys[1]} L {riser_x},{deck_ys[0]}", d.SOLIDS)
d.junction(riser_x, deck_ys[0])
d.txt((screen_x1 + 680) / 2 + 40, recycle_y - 8, "Oversize recycle", size=9, fill=d.SUB, anchor="middle")

# ==================================================== Row 1->2 transfer corridor
# Stockpile reclaim feeds the start of the grinding row below-left, avoiding a
# single very long row - a standard elbow connector between flowsheet rows.
# Kept at its own elevation (350), clear of the cyclone-overflow run drawn
# later at 370 - two unrelated streams sharing a y-band would either read as
# one line or force an ambiguous crossing (layout-rules.md Sec. 2).
Y2 = 480
Y_TRANSFER = 350
d.pipe(f"M 1340,{Y1+90} L 1340,{Y_TRANSFER} L 150,{Y_TRANSFER} L 150,{Y2-15}", d.SOLIDS, arrow=True)

# ============================================================ Row 2: grinding
d.feeder_apron(90, Y2 - 15, 210, Y2 + 15, tag="FD-102  Reclaim Feeder")
d.mill_sag(280, Y2 - 55, 520, Y2 + 55, tag="ML-101  SAG Mill")
d.pump_sump(650, Y2 + 35, tag="PU-101  Sump Pump")
# sized level with the mills either side (SKILL.md: a cyclone is about the height
# of the adjacent mill, never taller); cyc holds its feed/overflow/underflow points
cyc = d.cyclone(780, Y2 - 55, Y2 + 55, tag="CL-101  Cyclone")
d.mill_ball(920, Y2 - 55, 1160, Y2 + 55, tag="ML-102  Ball Mill")

d.pipe(f"M 210,{Y2} L 280,{Y2}", d.SOLIDS, arrow=True)
d.pipe(f"M 520,{Y2} L 590,{Y2} L 590,{Y2+35} L 634,{Y2+35}", d.ORE, arrow=True)
d.txt(555, Y2 - 12, "+ water", size=8.5, fill=d.SUB, anchor="middle")
cfx, cfy = cyc["feed"]
d.pipe(f"M 666,{Y2+35} L 720,{Y2+35} L 720,{cfy} L {cfx},{cfy}", d.ORE, arrow=True)
# cyclone underflow -> ball mill feed trunnion at (920, Y2); the riser sits at 906,
# just clear of the cyclone tag, so the arrow lands on the trunnion face
ux, uy = cyc["underflow"]
d.pipe(f"M {ux},{uy} L {ux},{Y2+120} L 906,{Y2+120} L 906,{Y2} L 920,{Y2}", d.ORE, arrow=True)
d.pipe(f"M 1160,{Y2} L 1200,{Y2} L 1200,{Y2+160} L 650,{Y2+160} L 650,{Y2+67}", d.ORE, arrow=True)
d.txt(920, Y2 + 178, "Ball mill discharge to sump (closed circuit)", size=8.5, fill=d.SUB, anchor="middle")
# cyclone overflow (final grind product) up and over to flotation row - its own
# elevation (Y2-110), clear of the transfer corridor above at Y_TRANSFER (350)
Y3 = 700
ox, oy = cyc["overflow"]
d.pipe(f"M {ox},{oy} L {ox},{Y2-110} L 1450,{Y2-110} L 1450,{Y3-45}", d.ORE, arrow=True)
d.txt(1100, Y2 - 120, "Cyclone overflow to flotation", size=9, fill=d.SUB, anchor="middle")

# ================================================ Row 3: flotation + dewatering
d.flotation_cell(1370, Y3 - 45, 1530, Y3 + 60, tag="FL-101  Rougher 1")
d.flotation_cell(1580, Y3 - 45, 1740, Y3 + 60, tag="FL-102  Rougher 2")
d.flotation_column(1830, Y3 - 90, Y3 + 90, tag="FL-103  Cleaner Column")

# rougher bank runs in series: cell 1's tailings feed cell 2, not a parallel
# split - only the last cell's tailings are the final rougher tailings.
d.pipe(f"M 1450,{Y3+60} L 1450,{Y3+90} L 1660,{Y3+90} L 1660,{Y3-45}", d.ORE, arrow=True)
d.txt(1555, Y3 + 103, "Ro1 tails to Ro2", size=8.5, fill=d.SUB, anchor="middle")
# rougher 2 tailings -> final rougher tailings, down to the tailings thickener's
# feed well (thickener top 880, feed well entry at top-20 = 860 per its docstring)
d.pipe(f"M 1660,{Y3+60} L 1660,{Y3+120} L 900,{Y3+120} L 900,860", d.ORE, arrow=True)
d.txt(1280, Y3 + 133, "Rougher tailings", size=9, fill=d.SUB, anchor="middle")

# both cells' froth concentrate collect in a corridor above the row, into the
# cleaner column feed
conc_y = Y3 - 90
d.pipe(f"M 1520,{Y3-45+5} L 1520,{conc_y} L 1830,{conc_y} L 1830,{Y3-90+8}", d.ORE, arrow=True)
d.pipe(f"M 1730,{Y3-45+5} L 1730,{conc_y}", d.ORE)
d.txt(1625, conc_y - 8, "Ro1+Ro2 concentrate", size=8.5, fill=d.SUB, anchor="middle")

# cleaner concentrate -> concentrate thickener -> pump -> drum filter -> silo
d.thickener(1830, Y3 + 140, Y3 + 260, tag="TH-101  Conc. Thickener")
d.pipe(f"M 1830,{Y3+90} L 1830,{Y3+130}", d.ORE, arrow=True)
d.pump_centrifugal(1830, Y3 + 320, tag="PU-102")
d.pipe(f"M 1830,{Y3+260} L 1830,{Y3+304}", d.ORE, arrow=True)
d.filter_drum(1700, Y3 + 340, tag="FT-101  Drum Filter")
d.pipe(f"M 1814,{Y3+320} L 1745,{Y3+320} L 1745,{Y3+340}", d.ORE, arrow=True)
d.silo(1560, Y3 + 300, Y3 + 400, tag="GE-102  Concentrate Silo")
d.pipe(f"M 1655,{Y3+340} L 1600,{Y3+340} L 1600,{Y3+300}", d.SOLIDS, arrow=True)
d.txt(1560, Y3 + 448, "To market (truck/rail load-out)", size=9, fill=d.SUB, anchor="middle")

# ============================================================ Row 4: tailings
# Thickener shell: top 880, bottom (apex) 1000, shell right wall at cx+90=990.
d.thickener(900, 880, 1000, tag="TH-102  Tailings Thickener")

# Underflow leaves the apex (900,1000), drops to its own elevation (1050 -
# clear of the shell, which ends at 1000) and runs right through the level
# control valve to the splitter.
UF_Y = 1050
d.pipe(f"M 900,1000 L 900,{UF_Y}", d.ORE)
d.cvalve(1000, UF_Y, "LV-201", fail="FC", actuator="above", tag_dy=45)
d.pipe(f"M 1018,{UF_Y} L 1090,{UF_Y}", d.ORE, arrow=True)
d.splitter(1090, UF_Y, n_outputs=2, tag="OP-101")
d.pipe(f"M 1090,{UF_Y} L 1090,{UF_Y-20} L 1200,{UF_Y-20} L 1200,{UF_Y+5}", d.ORE, arrow=True)
d.txt(1200, UF_Y - 28, "To tailings dam", size=8.5, fill=d.SUB, anchor="middle")
d.tailings_dam(1220, UF_Y + 50, tag="GE-103  Tailings Dam")
# Routed below the dam's whole footprint (crest 1050 - base 1100), not through
# it - the dam is a filled shape, not a see-through symbol.
d.pipe(f"M 1090,{UF_Y} L 1090,{UF_Y+80} L 1300,{UF_Y+80}", d.BLUE, arrow=True)
d.txt(1300, UF_Y + 94, "Reclaim water", size=8.5, fill=d.SUB, anchor="start")
d.txt(1300, UF_Y + 108, "to process water tank", size=8.5, fill=d.SUB, anchor="start")

# Thickener level control: LT side-mounted on the shell -> LIC in clear space
# above the valve -> LV-201 on the underflow line. Same ISA-5.1 loop
# conventions pfd-generator uses (measurement -> controller -> final element).
# LT sits well clear of the x=1000 valve-signal corridor (offset to x=1090,
# not just past it) so the two loop legs land on separate LIC ports (right
# side for the incoming measurement, bottom for the outgoing control signal)
# instead of overlapping - two legs sharing one port reads as one tangled line.
d.bubble(1090, 950, "LT", "201", r=16)
d.lead(1074, 950, 990, 950)
d.bubble(1000, 860, "LIC", "201", shared=True, r=20)
d.sig("M 1090,934 L 1090,860 L 1020,860")
d.sig(f"M 1000,880 L 1000,{UF_Y-32}")

# =============================================================== sheet furniture
d.notes(60, 1220, "DESIGN BASIS / ASSUMPTIONS", [
    "Base-metal (Cu/Mo) sulphide ore, single-stage flotation train, conceptual only",
    "CR-RR (roll crusher) not used here; it's the symbol set's closest match for HPGR duty",
    "Screen SD-101: 2-deck, dry duty - deck count is illustrative, not sized",
    "Not for construction - no equipment sizing, mass balance, or hazard review",
])

d.legend([
    ("Ore / dry solids (conveyed)", d.SOLIDS, False),
    ("Ore slurry / pulp", d.ORE, False),
    ("Process / reclaim water", d.BLUE, False),
    ("DCS signal", d.SIG, True),
], y=1340, x=60)
d.revision("Rev A | mineral-processing-pfd example", y=1340)

d.save("base_metal_flotation_flowsheet.svg")
print("wrote base_metal_flotation_flowsheet.svg")
