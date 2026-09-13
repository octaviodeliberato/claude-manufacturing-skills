# -*- coding: utf-8 -*-
"""Primary/secondary crushing stage -> SAG -> ball mill -> hydrocyclone with a
BASIC-tier control strategy on both circuits (see
references/control-strategies.md): the regulatory single loops only,
drive-speed final elements drawn as a motor symbol, the crusher-setting loop
as a ZIC ending on the crusher body, monitors as indicators, and the
per-circuit tier note the drawing must carry (ADR 0004: tiers can be mixed
per circuit, so the note names each one). Crushing loops are 100-series,
grinding loops 200-series. Run from the examples/ directory;
test_primitives.py imports build()."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from pid_lib import PID  # noqa: E402


def build():
    d = PID(1400, 1560, border=True)
    d.title("CRUSHING + GRINDING CIRCUIT - BASIC CONTROL STRATEGY",
            "Primary/secondary crushing with closed-circuit screen - SAG - ball mill - hydrocyclone | "
            "regulatory (basic tier) loops, 100-series crushing / 200-series grinding tags")

    # Two elevation bands: the crushing stage (row 1) above, grinding (row 2)
    # below, joined by a transfer corridor that runs under row 1 and over row
    # 2's tallest instrument bubbles - one y each, so nothing crosses.
    Y1 = 210   # row 1 reference: ROM bin discharge is the stage's highest point
    Y = 1040   # row 2: mill centreline; everything in that row is planned around it
    Y_TRANSFER = Y - 310  # transfer corridor, 30 px clear of row 2's PSM label at Y-280

    # ======================================================= row 1: crushing
    # ROM bin -> apron feeder -> gyratory primary, drawn as the vertical stack
    # it really is (bin over feeder over crusher), discharging into a tunnel
    # conveyor that lifts the product to the surge bin.
    d.ore_bin(110, Y1 - 70, Y1 + 30, tag=None)
    d.txt(110, Y1 - 82, "GE-101  ROM ore bin", size=10.5, weight="bold", anchor="middle")
    d.pipe(f"M 110,{Y1+30} L 110,{Y1+55}", d.SOLIDS, arrow=True)
    d.feeder_apron(90, Y1 + 55, 210, Y1 + 80)
    d.txt(150, Y1 + 102, "FD-101", size=10.5, weight="bold", anchor="middle")
    d.txt(150, Y1 + 114, "Apron feeder", size=9, fill=d.SUB, anchor="middle")
    m_fd1 = d.motor(190, Y1 + 30, tag=None, port="top")
    d.lead(190, Y1 + 43, 190, Y1 + 55)
    d.pipe(f"M 200,{Y1+80} L 200,{Y1+100} L 312,{Y1+100} L 312,{Y1+120}", d.SOLIDS, arrow=True)
    d.crusher_gyratory(330, Y1 + 110, Y1 + 200, tag=None)
    d.txt(285, Y1 + 165, "CR-101", size=10.5, weight="bold", anchor="end")
    d.txt(285, Y1 + 178, "Gyratory crusher", size=9, fill=d.SUB, anchor="end")
    d.pipe(f"M 330,{Y1+200} L 330,{Y1+240} L 400,{Y1+240}", d.SOLIDS, arrow=True)
    d.conveyor(400, Y1 + 240, 560, Y1 + 150, tag="CV-101")

    # Surge (screen feed) bin with the secondary cone crusher stacked above it:
    # both the primary product (CV-101) and the cone product drop into the bin,
    # which is the closed circuit - bin -> feeder -> screen -> oversize -> cone
    # -> bin. Screen undersize is the stage product.
    d.pipe(f"M 560,{Y1+150} L 610,{Y1+150} L 610,{Y1+170}", d.SOLIDS, arrow=True)
    d.ore_bin(640, Y1 + 170, Y1 + 270, tag=None)
    d.txt(592, Y1 + 230, "GE-102", size=10.5, weight="bold", anchor="end")
    d.txt(592, Y1 + 243, "Surge bin", size=9, fill=d.SUB, anchor="end")
    d.pipe(f"M 640,{Y1+270} L 640,{Y1+295}", d.SOLIDS, arrow=True)
    d.feeder_vibrating(620, Y1 + 295, 730, Y1 + 320)
    d.txt(660, Y1 + 350, "FD-102", size=10.5, weight="bold", anchor="middle")
    d.txt(660, Y1 + 362, "Screen feeder", size=9, fill=d.SUB, anchor="middle")
    m_fd2 = d.motor(760, Y1 + 307, tag=None, port="right")
    d.lead(747, Y1 + 307, 724, Y1 + 307)
    d.pipe(f"M 716,{Y1+320} L 716,{Y1+340} L 800,{Y1+340} L 800,{Y1+355}", d.SOLIDS, arrow=True)
    deck_ys = d.screen(780, Y1 + 355, 940, Y1 + 445, deck_count=2, wet=False, tag=None)
    d.txt(875, Y1 + 462, "SD-101", size=10.5, weight="bold")
    d.txt(875, Y1 + 475, "Screen, 2-deck, dry", size=9, fill=d.SUB)
    # undersize (stage product) -> product conveyor -> transfer corridor -> stockpile
    d.pipe(f"M 860,{Y1+445} L 860,{Y1+490} L 1000,{Y1+490}", d.SOLIDS, arrow=True)
    d.conveyor(1000, Y1 + 490, 1150, Y1 + 400, tag="CV-103")
    d.pipe(f"M 1150,{Y1+400} L 1190,{Y1+400} L 1190,{Y_TRANSFER} L 110,{Y_TRANSFER} L 110,{Y-240}", d.SOLIDS, arrow=True)
    d.txt(650, Y_TRANSFER - 8, "Crushed ore to stockpile", size=9, fill=d.SUB, anchor="middle")
    # both decks' oversize recycle to the cone crusher: bottom deck joins the
    # top-deck line at a junction on the riser, one corridor above row 1 carries
    # both to the crusher feeder. The riser is the one "up" run in the stage
    # (a recycle conveyor, drawn as the base-metal example draws it).
    riser_x = 980
    d.pipe(f"M 940,{deck_ys[0]} L {riser_x},{deck_ys[0]} L {riser_x},{Y1-80} "
           f"L 578,{Y1-80} L 578,{Y1-50}", d.SOLIDS, arrow=True)
    d.pipe(f"M 940,{deck_ys[1]} L {riser_x},{deck_ys[1]} L {riser_x},{deck_ys[0]}", d.SOLIDS)
    d.junction(riser_x, deck_ys[0])
    d.txt(780, Y1 - 88, "Screen oversize to secondary crusher", size=9, fill=d.SUB, anchor="middle")
    # crusher feeder -> cone crusher -> surge bin (vertical stack)
    d.feeder_vibrating(560, Y1 - 50, 670, Y1 - 25)
    d.txt(600, Y1 + 4, "FD-103", size=10.5, weight="bold", anchor="middle")
    d.txt(600, Y1 + 16, "Crusher feeder", size=9, fill=d.SUB, anchor="middle")
    m_fd3 = d.motor(700, Y1 - 38, tag=None, port="right")
    d.lead(687, Y1 - 38, 664, Y1 - 38)
    d.pipe(f"M 660,{Y1-25} L 660,{Y1+40}", d.SOLIDS, arrow=True)
    d.crusher_cone(640, Y1 + 40, Y1 + 140, tag=None)
    d.txt(700, Y1 + 108, "CR-102", size=10.5, weight="bold")
    d.txt(700, Y1 + 121, "Cone crusher", size=9, fill=d.SUB)
    d.pipe(f"M 640,{Y1+140} L 640,{Y1+170}", d.SOLIDS, arrow=True)

    # ------------------------------------------------ crushing control loops
    # JIC-101 primary crusher load (power) -> FD-101 apron feeder VSD (DRIVE SPEED)
    d.bubble(420, Y1 + 160, "JT", "101", r=16)
    d.lead(354, Y1 + 160, 404, Y1 + 160)
    d.bubble(420, Y1 - 10, "JIC", "101", shared=True, r=20)
    d.sig(f"M 420,{Y1+144} L 420,{Y1+10}")
    d.sig(f"M 400,{Y1-10} L {m_fd1[0]},{Y1-10} L {m_fd1[0]},{m_fd1[1]}")

    # LIC-102 cone crusher cavity level -> FD-103 crusher feeder VSD (DRIVE SPEED):
    # the choke-feed loop, on the feeder that feeds THIS crusher
    d.bubble(722, Y1 + 70, "LT", "102", r=16)
    d.lead(671, Y1 + 70, 706, Y1 + 70)
    d.bubble(790, Y1 + 70, "LIC", "102", shared=True, r=20)
    d.sig(f"M 738,{Y1+70} L 770,{Y1+70}")
    d.sig(f"M 790,{Y1+50} L 790,{m_fd3[1]} L {m_fd3[0]},{m_fd3[1]}")

    # ZIC-103 cone crusher setting (CSS, setting mode) - CRUSHER SETTING: one
    # controller whose output ends on the crusher body at the hydroset end. Load
    # mode (PT/JT -> ZIC) is the alternative mode of this same controller, not
    # a second loop.
    d.bubble(562, Y1 + 90, "ZT", "103", r=16)
    d.lead(613, Y1 + 90, 578, Y1 + 90)
    d.bubble(490, Y1 + 90, "ZIC", "103", shared=True, r=20)
    d.sig(f"M 546,{Y1+90} L 510,{Y1+90}")
    d.sig(f"M 490,{Y1+110} L 490,{Y1+130} L 626,{Y1+130}")
    d.txt(590, Y1 + 125, "CSS", size=8.5, fill=d.SUB, anchor="middle")

    # LIC-104 surge bin level -> FD-102 screen feeder VSD (DRIVE SPEED)
    d.bubble(732, Y1 + 220, "LT", "104", r=16)
    d.lead(680, Y1 + 220, 716, Y1 + 220)
    d.bubble(800, Y1 + 220, "LIC", "104", shared=True, r=20)
    d.sig(f"M 748,{Y1+220} L 780,{Y1+220}")
    d.sig(f"M 800,{Y1+240} L 800,{m_fd2[1]} L {m_fd2[0]},{m_fd2[1]}")

    # WI-105 product belt scale on CV-103: monitor only (stage yield)
    d.bubble(1040, Y1 + 400, "WT", "105", r=16)
    d.lead(1040, Y1 + 466, 1040, Y1 + 416)
    d.bubble(1040, Y1 + 340, "WI", "105", shared=True, r=20)
    d.sig(f"M 1040,{Y1+384} L 1040,{Y1+360}")

    # ======================================================= row 2: grinding
    # Crushed-ore stockpile above the reclaim feeder, fed from the transfer
    # corridor; the pile is kept well above the WIC-201 signal corridor at
    # Y-150 so the signal never clips its slope.
    d.stockpile(110, Y - 170, tag=None)
    d.txt(190, Y - 215, "GE-103  Crushed ore stockpile", size=10.5, weight="bold")
    d.pipe(f"M 110,{Y-170} L 110,{Y-40}", d.SOLIDS, arrow=True)
    d.feeder_apron(70, Y - 40, 180, Y - 10)
    d.txt(100, Y + 15, "FD-201", size=10.5, weight="bold", anchor="middle")
    d.txt(100, Y + 28, "Reclaim feeder", size=9, fill=d.SUB, anchor="middle")
    # Feeder VSD: the drawn final element of the feed-rate loop. Body only -
    # the lead to the feeder pan and the incoming signal are drawn here.
    m_fd = d.motor(160, Y - 70, tag=None, port="top")
    d.lead(160, Y - 57, 160, Y - 40)
    # feeder -> conveyor tail -> SAG feed trunnion
    d.pipe(f"M 170,{Y-10} L 170,{Y+40} L 210,{Y+40}", d.SOLIDS, arrow=True)
    d.conveyor(210, Y + 40, 330, Y - 20)
    d.txt(245, Y + 66, "CV-201", size=10, weight="bold", anchor="middle")
    d.pipe(f"M 330,{Y-20} L 370,{Y-20} L 370,{Y} L 400,{Y}", d.SOLIDS, arrow=True)

    # ================================================================== SAG mill
    d.mill_sag(400, Y - 55, 620, Y + 55, tag="ML-201  SAG Mill")

    # SAG inlet water: header along the bottom, control valve, joins the feed
    # chute at a junction just ahead of the feed trunnion.
    d.txt(122, Y + 192, "Process water", size=9, fill=d.SUB)
    d.pipe(f"M 90,{Y+200} L 232,{Y+200}", d.BLUE)
    d.cvalve(250, Y + 200, "FV-202", fail="FC", actuator="above", tag_dy=45)
    d.pipe(f"M 268,{Y+200} L 385,{Y+200} L 385,{Y}", d.BLUE)
    d.junction(385, Y)

    # ============================================= sump, pump, cyclone, ball mill
    # Both mill discharges enter the sump basin from below (the pit-fed sump
    # convention the base-metal example uses); dropping the SAG line at x=660
    # keeps the x=700 corridor free for the LT-205 -> LIC-205 signal, which
    # would otherwise have to cross it.
    d.pipe(f"M 620,{Y} L 660,{Y} L 660,{Y+130} L 750,{Y+130} L 750,{Y+84}", d.ORE, arrow=True)
    d.pump_sump(760, Y + 40, tag=None)
    d.txt(812, Y + 60, "PU-201", size=10, weight="bold")
    d.txt(812, Y + 72, "Cyclone feed pump", size=8.5, fill=d.SUB)
    m_pu = d.motor(760, Y - 5, tag=None, port="top")
    d.lead(760, Y + 8, 760, Y + 24)
    # pump discharge riser to the cyclone feed nozzle
    cyc = d.cyclone(960, Y - 150, Y - 40, tag="CL-201  Cyclone", r=22)
    cfx, cfy = cyc["feed"]
    d.pipe(f"M 786,{Y+40} L 800,{Y+40} L 800,{cfy} L {cfx},{cfy}", d.ORE, arrow=True)
    # cyclone underflow -> ball mill feed trunnion; overflow up and out to flotation
    ux, uy = cyc["underflow"]
    d.pipe(f"M {ux},{uy} L {ux},{Y} L 1040,{Y}", d.ORE, arrow=True)
    ox, oy = cyc["overflow"]
    d.pipe(f"M {ox},{oy} L {ox},{Y-210} L 1360,{Y-210}", d.ORE, arrow=True)
    d.txt(1250, Y - 218, "Cyclone overflow to flotation", size=9, fill=d.SUB, anchor="middle")
    d.mill_ball(1040, Y - 55, 1260, Y + 55, tag="ML-202  Ball Mill")
    d.pipe(f"M 1260,{Y} L 1300,{Y} L 1300,{Y+160} L 770,{Y+160} L 770,{Y+84}", d.ORE, arrow=True)
    d.txt(1030, Y + 178, "Ball mill discharge to cyclone feed sump (closed circuit)",
          size=8.5, fill=d.SUB, anchor="middle")
    # dilution water into the sump from the right, through the density valve
    d.txt(1015, Y + 114, "Dilution water", size=9, fill=d.SUB)
    d.pipe(f"M 1010,{Y+110} L 938,{Y+110}", d.BLUE)
    d.cvalve(920, Y + 110, "DV-206", fail="FC", actuator="above", tag_dy=30)
    d.pipe(f"M 902,{Y+110} L 820,{Y+110} L 820,{Y+80} L 780,{Y+80}", d.BLUE, arrow=True)

    # ============================================================ control loops
    # Every loop: measurement -> controller -> final element, arrowhead per leg.
    # Drive-speed loops terminate on a motor(); water loops on a cvalve();
    # monitors stop at an indicator (no final element).

    # WIC-201 fresh feed rate: weightometer on CV-201 -> feeder VSD (DRIVE SPEED)
    d.bubble(300, Y - 80, "WT", "201", r=16)
    d.lead(300, Y - 7, 300, Y - 64)
    d.bubble(300, Y - 150, "WIC", "201", shared=True, r=20)
    d.sig(f"M 300,{Y-96} L 300,{Y-130}")
    d.sig(f"M 280,{Y-150} L {m_fd[0]},{Y-150} L {m_fd[0]},{m_fd[1]}")

    # FIC-202 SAG inlet water flow -> FV-202 (VALVE)
    d.bubble(110, Y + 120, "FT", "202", r=16)
    d.lead(110, Y + 200, 110, Y + 136)
    d.bubble(250, Y + 120, "FIC", "202", shared=True, r=20)
    d.sig(f"M 126,{Y+120} L 230,{Y+120}")
    d.sig(f"M 250,{Y+140} L 250,{Y+162}")

    # WIC-203 SAG mill load (load cells) -> feed-rate setpoint of WIC-201, i.e.
    # the feeder drive through WIC-201 (DRIVE SPEED). One drawn "SP" landing;
    # the basic tier stops here - override/feedforward are intermediate additions.
    d.bubble(470, Y - 95, "WT", "203", r=16)
    d.lead(470, Y - 55, 470, Y - 79)
    d.bubble(470, Y - 150, "WIC", "203", shared=True, r=20)
    d.sig(f"M 470,{Y-111} L 470,{Y-130}")
    d.sig(f"M 450,{Y-150} L 320,{Y-150}")
    d.txt(335, Y - 158, "SP", size=8.5, fill=d.SUB)

    # JI-204 SAG mill power: monitor only (indication / high alarm), no final element
    d.bubble(560, Y - 95, "JT", "204", r=16)
    d.lead(560, Y - 55, 560, Y - 79)
    d.bubble(560, Y - 150, "JI", "204", shared=True, r=20)
    d.sig(f"M 560,{Y-111} L 560,{Y-130}")

    # LIC-205 sump level -> cyclone feed pump VSD (DRIVE SPEED). Pairing chosen
    # for this drawing: level on the pump, density on the dilution water - the
    # two cannot both sit on the water valve (control-strategies.md caveat).
    d.bubble(700, Y + 76, "LT", "205", r=16)
    d.lead(738, Y + 76, 716, Y + 76)
    d.bubble(700, Y - 60, "LIC", "205", shared=True, r=20)
    d.sig(f"M 700,{Y+60} L 700,{Y-40}")
    d.sig(f"M 720,{Y-60} L {m_pu[0]},{Y-60} L {m_pu[0]},{m_pu[1]}")

    # DIC-206 cyclone feed density -> DV-206 dilution water (VALVE). D = density
    # is the user's-choice letter and is declared on the legend below.
    d.bubble(840, Y - 40, "DT", "206", r=16)
    d.lead(800, Y - 40, 824, Y - 40)
    d.bubble(900, Y - 40, "DIC", "206", shared=True, r=20)
    d.sig(f"M 856,{Y-40} L 880,{Y-40}")
    d.sig(f"M 900,{Y-20} L 900,{Y+40} L 920,{Y+40} L 920,{Y+72}")

    # PI-207 cyclone feed pressure: monitor only at the basic tier (becomes the
    # pump-speed override at intermediate)
    d.bubble(870, Y - 180, "PT", "207", r=16)
    d.lead(870, cfy, 870, Y - 164)
    d.bubble(870, Y - 240, "PI", "207", shared=True, r=20)
    d.sig(f"M 870,{Y-196} L 870,{Y-220}")

    # AI-208 particle size monitor (PSM) on the cyclone overflow: monitor only
    d.bubble(1080, Y - 250, "AT", "208", r=16)
    d.lead(1080, Y - 210, 1080, Y - 234)
    d.bubble(1140, Y - 250, "AI", "208", shared=True, r=20)
    d.sig(f"M 1096,{Y-250} L 1120,{Y-250}")
    d.txt(1110, Y - 280, "PSM", size=9, fill=d.SUB, anchor="middle")

    # JI-209 ball mill power: monitor only
    d.bubble(1150, Y - 95, "JT", "209", r=16)
    d.lead(1150, Y - 55, 1150, Y - 79)
    d.bubble(1150, Y - 150, "JI", "209", shared=True, r=20)
    d.sig(f"M 1150,{Y-111} L 1150,{Y-130}")

    # ============================================================ sheet furniture
    # Per-circuit tier note (ADR 0004): the only place that says which control
    # tier the drawn loops represent.
    Y_NOTES = Y + 300
    d.notes(60, Y_NOTES, "CONTROL STRATEGY", [
        "Crushing: basic (assumed) | Grinding: basic (assumed) - no tier was named; intermediate/advanced add cascades, ratio, override, supervisory",
        "ZIC-103 holds CSS in setting mode; load mode (PT/JT -> ZIC) is the alternative mode of the same controller, not a second loop",
        "Sump level -> pump speed and cyclone feed density -> dilution water: chosen pairing, they cannot share the water valve",
        "WI-105 (belt scale), JI-204 / JI-209 (mill power), PI-207 (cyclone feed pressure), AI-208 (PSM) are monitors - no final element",
        "Feeder and pump speed loops terminate on the drive (M), not a valve; WIC-203 writes the setpoint of WIC-201",
    ])
    d.notes(800, Y_NOTES, "DESIGN BASIS / ASSUMPTIONS", [
        "Conceptual only: no setpoints, tuning, controller or transmitter sizing, interlocks or alarms",
        "Gyratory primary, cone secondary in forward closed circuit with a 2-deck dry screen; feeders on VSDs",
        "Single SAG - ball mill line, fixed-speed mills, sump pump on VSD; loop tags 1xx crushing, 2xx grinding",
        "Not for construction - no equipment sizing, mass balance, or hazard review",
    ])
    d.legend([
        ("Ore / dry solids (conveyed)", d.SOLIDS, False),
        ("Ore slurry / pulp", d.ORE, False),
        ("Process / dilution water", d.BLUE, False),
        ("DCS signal", d.SIG, True),
    ], y=Y_NOTES + 130, x=60, density=True)
    d.revision("Rev B | mineral-processing-pfd example", y=Y_NOTES + 154)
    return d


if __name__ == "__main__":
    out = "grinding_circuit_control.svg"
    build().save(out)
    print(f"wrote {out}")
