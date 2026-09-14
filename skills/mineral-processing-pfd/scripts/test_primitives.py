# -*- coding: utf-8 -*-
"""
Smoke tests for pid_lib's mineral-processing primitives.

No pytest dependency - this repo has no test framework anywhere else, and
the seam agreed for this skill (see spec) is: call each primitive, assert
structural invariants on the SVG it produces - plus one drawing-level test
per shipped control-strategy example, built through its build() and run
through the same invariants - then rely on the mandatory render-and-inspect
step (SKILL.md) as the real acceptance test. Run with:

    python3 scripts/test_primitives.py
"""
import importlib.util
import os
import re
import sys
import xml.etree.ElementTree as ET

from pid_lib import PID, ORE, SIG

FAILURES = []


def check(name, fn):
    try:
        fn()
    except Exception as e:
        FAILURES.append(f"{name}: {e}")
        print(f"FAIL {name}: {e}")
    else:
        print(f"ok   {name}")


def assert_valid_svg(d):
    """The accumulated elements plus the <svg>/<defs> wrapper must be well-formed XML."""
    svg = "\n".join(d.o + ["</svg>"])
    ET.fromstring(svg)


def assert_no_raster_images(d):
    for s in d.o:
        assert "<image" not in s, f"raster <image> element found: {s[:80]}"


def assert_signals_have_arrowheads(d):
    """Every dashed instrument-signal line must carry marker-end (Rule 3: complete,
    directional control loops). The legend's dashed sample line is marked
    class="swatch" and is the one dashed element that is not a signal."""
    for s in d.o:
        if 'stroke-dasharray="7,5.5"' in s and 'class="swatch"' not in s:
            assert "marker-end" in s, f"signal line missing arrowhead: {s[:80]}"


def assert_softlinks_have_arrowheads(d):
    """Every software/data link must carry marker-end. The electrical guard above
    keys on the dashed pattern and would silently skip a softlink, so this one
    keys on the class the primitive stamps on every link it draws."""
    for s in d.o:
        if 'class="softlink"' in s:
            assert "marker-end" in s, f"software link missing arrowhead: {s[:80]}"


def assert_no_bare_text_paths(d):
    """Rule 4: text must be real <text>, never <path>/<use> glyph outlines standing
    in for a label. We only ever emit <text>, so this just guards against a future
    regression where someone pastes in glyph-path output."""
    for s in d.o:
        assert "<use" not in s, f"glyph-path <use> reference found: {s[:80]}"


def standard_checks(d):
    assert_valid_svg(d)
    assert_no_raster_images(d)
    assert_signals_have_arrowheads(d)
    assert_softlinks_have_arrowheads(d)
    assert_no_bare_text_paths(d)


# ---------------------------------------------------------------- comminution

def test_rock_breaker():
    d = PID()
    d.rock_breaker(200, 80, tag="RB-101")
    standard_checks(d)


def test_feeder_vibrating():
    d = PID()
    d.feeder_vibrating(100, 100, 220, 140)
    standard_checks(d)


def test_crusher_jaw():
    d = PID()
    d.crusher_jaw(200, 100, 220, tag="CR-101")
    standard_checks(d)


def test_crusher_cone():
    d = PID()
    d.crusher_cone(200, 100, 240, tag="CR-102")
    standard_checks(d)


def test_crusher_gyratory():
    d = PID()
    d.crusher_gyratory(200, 100, 260, tag="CR-103")
    standard_checks(d)


def test_crusher_vsi():
    d = PID()
    d.crusher_vsi(200, 200, tag="CR-104")
    standard_checks(d)


def test_crusher_impact():
    d = PID()
    d.crusher_impact(200, 200, tag="CR-105")
    standard_checks(d)


def test_crusher_roll():
    d = PID()
    d.crusher_roll(200, 100, 220, tag="CR-106")
    standard_checks(d)


def test_screen_decks():
    for n in (1, 2, 3, 4):
        for wet in (False, True):
            d = PID()
            deck_ys = d.screen(150, 100, 350, 200, deck_count=n, wet=wet, tag=f"SD-{n}{'W' if wet else 'D'}")
            standard_checks(d)
            # one oversize outlet per deck, top deck first, all inside the body -
            # the composing script must pipe every one of them (deck count + 1 streams)
            assert len(deck_ys) == n, f"{n}-deck screen returned {len(deck_ys)} outlets"
            assert deck_ys == sorted(deck_ys), "deck outlets must be top-down"
            assert all(100 < y < 170 for y in deck_ys), f"outlet outside body: {deck_ys}"


def _elements(d, tag, cls):
    """Emitted `<tag ...>` elements carrying class="cls"."""
    return [s for s in d.o if s.startswith(f"<{tag}") and f'class="{cls}"' in s]


def _mill_charge(d):
    return _elements(d, "circle", "charge")


def _mill_trunnions(d):
    return _elements(d, "path", "trunnion")


def test_mill_sag():
    d = PID()
    d.mill_sag(200, 300, 420, 380, tag="ML-101")
    standard_checks(d)
    assert len(_mill_trunnions(d)) == 2, "SAG mill must draw a trunnion at each end"
    assert _mill_charge(d), "SAG mill must draw a charge"


def test_mill_ball():
    d = PID()
    d.mill_ball(200, 300, 420, 380, tag="ML-102")
    standard_checks(d)
    assert len(_mill_trunnions(d)) == 2, "ball mill must draw a trunnion at each end"
    assert _mill_charge(d), "ball mill must draw a charge"


def test_mill_charge_distinguishes_sag_from_ball():
    """The only visual difference between the two mills is the charge: a SAG mill
    shows a few large lumps, a ball mill many small balls (CONTEXT.md: mill charge)."""
    sag, ball = PID(), PID()
    sag.mill_sag(200, 300, 420, 380)
    ball.mill_ball(200, 300, 420, 380)
    assert len(_mill_charge(sag)) < len(_mill_charge(ball))


def test_mill_charge_sits_at_the_bottom():
    d = PID()
    d.mill_ball(200, 300, 420, 380)
    cys = [float(re.search(r'cy="([\d.]+)"', s).group(1)) for s in _mill_charge(d)]
    assert cys, "no charge drawn"
    assert all(cy > 340 for cy in cys), f"charge circles above the shell centreline: {cys}"


def test_mill_trunnions_reach_the_envelope():
    """x0..x1 is the OUTER envelope: the trunnion faces sit exactly at x0 and x1 so
    (x0, cy)/(x1, cy) remain the documented feed/discharge points."""
    d = PID()
    d.mill_sag(200, 300, 420, 380)
    joined = " ".join(_mill_trunnions(d))
    assert "M 200," in joined or "L 200," in joined, "left trunnion face must touch x0"
    assert "M 420," in joined or "L 420," in joined, "right trunnion face must touch x1"
    assert not any(s.startswith("<ellipse") for s in d.o), "flat elevation: no drum ellipses"


COMMINUTION_TESTS = [
    ("rock_breaker", test_rock_breaker),
    ("feeder_vibrating", test_feeder_vibrating),
    ("crusher_jaw", test_crusher_jaw),
    ("crusher_cone", test_crusher_cone),
    ("crusher_gyratory", test_crusher_gyratory),
    ("crusher_vsi", test_crusher_vsi),
    ("crusher_impact", test_crusher_impact),
    ("crusher_roll", test_crusher_roll),
    ("screen (1-4 deck, wet/dry)", test_screen_decks),
    ("mill_sag", test_mill_sag),
    ("mill_ball", test_mill_ball),
    ("mill charge: SAG < ball", test_mill_charge_distinguishes_sag_from_ball),
    ("mill charge at the bottom", test_mill_charge_sits_at_the_bottom),
    ("mill trunnions at x0/x1", test_mill_trunnions_reach_the_envelope),
]

# ---------------------------------------------------------- classification/flotation

def test_cyclone():
    d = PID()
    d.cyclone(200, 100, 220, tag="CL-101")
    standard_checks(d)


def test_cyclone_stubs_scale_with_r():
    """Feed and overflow stubs are proportional to r, so a small cyclone doesn't
    grow oversized nozzles. Stub length is read back from the emitted <line>s."""
    def stub_lengths(r):
        d = PID()
        d.cyclone(200, 100, 220, r=r)
        lens = []
        for s in d.o:
            if s.startswith("<line"):
                x1, y1, x2, y2 = (float(re.search(f'{k}="(-?[\\d.]+)"', s).group(1))
                                  for k in ("x1", "y1", "x2", "y2"))
                lens.append(abs(x2 - x1) + abs(y2 - y1))
        return lens
    small, big = stub_lengths(15), stub_lengths(30)
    assert len(small) == len(big) == 2
    assert all(a < b for a, b in zip(small, big)), f"stubs did not scale: {small} vs {big}"


def test_classifier_screw():
    d = PID()
    d.classifier_screw(100, 150, 320, 220, tag="CL-102")
    standard_checks(d)


def test_classifier_rake():
    d = PID()
    d.classifier_rake(100, 150, 320, 220, tag="CL-103")
    standard_checks(d)


def test_flotation_cell():
    d = PID()
    d.flotation_cell(100, 150, 260, 260, tag="FL-101")
    standard_checks(d)


def test_flotation_column():
    d = PID()
    d.flotation_column(200, 100, 320, tag="FL-102")
    standard_checks(d)


CLASSIFICATION_TESTS = [
    ("cyclone", test_cyclone),
    ("cyclone stubs scale with r", test_cyclone_stubs_scale_with_r),
    ("classifier_screw", test_classifier_screw),
    ("classifier_rake", test_classifier_rake),
    ("flotation_cell", test_flotation_cell),
    ("flotation_column", test_flotation_column),
]

# ------------------------------------------------------ dewatering/transport/storage

def test_thickener():
    d = PID()
    d.thickener(300, 100, 260, tag="TH-101")
    standard_checks(d)


def test_filter_drum():
    d = PID()
    d.filter_drum(200, 200, tag="FT-101")
    standard_checks(d)


def test_pump_centrifugal():
    d = PID()
    d.pump_centrifugal(200, 200, tag="PU-101")
    standard_checks(d)


def test_pump_sump():
    d = PID()
    d.pump_sump(200, 200, tag="PU-102")
    standard_checks(d)


def test_pump_sump_basin_w():
    """A sump that takes several inflows and carries a level transmitter on its
    rim needs a pit wider than the pump; basin_w widens it to the right of the
    pump and the returned rim span must say so. Default keeps the old width."""
    d = PID()
    rim = d.pump_sump(200, 200, basin_w=160)["rim"]
    standard_checks(d)
    x0, x1, y = rim
    assert x1 - x0 == 160, f"rim span {x1 - x0} != basin_w"
    assert x0 < 200 - 16 and x1 > 200 + 16, f"pump not seated over the rim: {rim}"
    assert y > 200 + 16, "rim must sit below the pump circle"
    default = PID().pump_sump(200, 200)["rim"]
    assert default[1] - default[0] == 2 * 16 + 16, f"default rim changed: {default}"


def test_feeder_apron():
    d = PID()
    d.feeder_apron(100, 150, 320, 200, tag="FD-101")
    standard_checks(d)


def test_conveyor():
    d = PID()
    d.conveyor(100, 200, 400, 120, tag="GE-101")
    standard_checks(d)


def test_ore_bin():
    d = PID()
    d.ore_bin(200, 100, 220, tag="GE-102")
    standard_checks(d)


def test_stockpile():
    d = PID()
    d.stockpile(200, 300, tag="GE-103")
    standard_checks(d)


def test_silo():
    d = PID()
    d.silo(200, 100, 260, tag="GE-104")
    standard_checks(d)


def test_tailings_dam():
    d = PID()
    d.tailings_dam(100, 300, tag="GE-105")
    standard_checks(d)


def test_junction():
    d = PID()
    d.junction(200, 200)
    standard_checks(d)
    assert sum(s.startswith("<circle") for s in d.o) == 1


def test_splitter():
    d = PID()
    d.splitter(200, 200, n_outputs=2, tag="OP-101")
    d2 = PID()
    d2.splitter(200, 200, n_outputs=3, tag="OP-102")
    standard_checks(d)
    standard_checks(d2)


DEWATERING_TRANSPORT_TESTS = [
    ("thickener", test_thickener),
    ("filter_drum", test_filter_drum),
    ("pump_centrifugal", test_pump_centrifugal),
    ("pump_sump", test_pump_sump),
    ("pump_sump basin_w", test_pump_sump_basin_w),
    ("feeder_apron", test_feeder_apron),
    ("conveyor", test_conveyor),
    ("ore_bin", test_ore_bin),
    ("stockpile", test_stockpile),
    ("silo", test_silo),
    ("tailings_dam", test_tailings_dam),
    ("splitter", test_splitter),
    ("junction", test_junction),
]

# ------------------------------------------------------------- control strategy

def test_motor():
    """motor() is the drawn final element for a DRIVE SPEED loop (CONTEXT.md:
    final element). It must return the coordinate the speed-controller signal
    lands on, and that point must lie on/within the drawn body so the arrowhead
    visibly touches the symbol."""
    d = PID()
    land = d.motor(300, 200, tag="M")
    standard_checks(d)
    circles = [s for s in d.o if s.startswith("<circle")]
    assert circles, "motor must draw an ISA 'M' circle"
    cx, cy, r = (float(re.search(k + r'="(-?[\d.]+)"', circles[0]).group(1)) for k in ("cx", "cy", "r"))
    x, y = land
    assert ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= r + 0.5, f"landing {land} outside the circle"
    assert any(">M<" in s for s in d.o), "motor must carry the letter M"


def test_legend_declares_density_letter():
    """ISA-5.1 Table 4.1 leaves first-letter D to the user; a drawing with a
    density loop must declare it on the legend, and one without must not."""
    entries = [("Ore slurry", ORE, False), ("DCS signal", SIG, True)]
    with_d, without_d = PID(), PID()
    with_d.legend(entries, density=True)
    without_d.legend(entries)
    standard_checks(with_d)
    assert any("D = density" in s for s in with_d.o), "legend must declare D = density"
    assert not any("D = density" in s for s in without_d.o), "no density loop, no declaration"


def test_legend_wraps_instead_of_overflowing():
    """A fifth entry plus the density declaration does not fit one row on the
    default 1400-wide sheet: the legend must wrap onto a second row rather than
    run past the border, and report the last row's y so the caller can place
    the revision line under it."""
    entries = [("Ore / dry solids (conveyed)", ORE, False), ("Ore slurry / pulp", ORE, False),
               ("Process / dilution water", SIG, False), ("DCS signal", SIG, True),
               ("Software link (setpoint)", SIG, "soft")]
    d = PID()
    last_y = d.legend(entries, y=886, density=True)
    standard_checks(d)
    xs = [float(re.search(r'x="(-?[\d.]+)"', s).group(1)) for s in d.o if s.startswith("<text")]
    assert max(xs) < d.w - 40, f"legend text starts at {max(xs)}, past the border"
    assert last_y > 886, "five entries + declaration must wrap to a second row"
    assert PID().legend(entries[:3]) == 886, "three short entries stay on one row"


def test_supervisory_block():
    """supervisory_block() is the drawn ADVANCED tier: one rounded rectangle per
    circuit (ADR 0004), body only. It must return at least one signal-port
    coordinate, every port must sit on the block's own outline, and the title
    must be real text."""
    d = PID()
    ports = d.supervisory_block(300, 100, 620, 160, "SAG MILL OPTIMISER (MPC)",
                                subtitle="expert system / MPC", n_ports=3)
    standard_checks(d)
    rects = [s for s in d.o if s.startswith("<rect") and 'class="supervisory"' in s]
    assert len(rects) == 1, "one rounded rectangle per block"
    assert 'rx="' in rects[0], "block must be a ROUNDED rectangle, not a vessel or a hexagon"
    assert ">SAG MILL OPTIMISER (MPC)<" in "\n".join(d.o), "title must be real <text>"
    assert ">expert system / MPC<" in "\n".join(d.o), "subtitle must be real <text>"
    flat = [pt for side in ports.values() for pt in side]
    assert flat, "block must return at least one port coordinate"
    assert len(ports["bottom"]) == 3, "n_ports ports per side"
    for x, y in flat:
        assert 300 <= x <= 620 and 100 <= y <= 160, f"port {x, y} outside the block bounds"
        assert x in (300, 620) or y in (100, 160), f"port {x, y} not on the outline"
    assert not any(s.startswith("<line") for s in d.o), "body only: no signal stubs"


def test_softlink_always_has_an_arrowhead():
    """softlink() is the ISA-5.1 software/data link: visually distinct from the
    dashed electrical sig() and ALWAYS arrowed - there is no arrow=False."""
    d = PID()
    d.softlink("M 100,100 L 200,100 L 200,220")
    standard_checks(d)
    links = [s for s in d.o if 'class="softlink"' in s]
    assert links, "softlink must stamp class=softlink so the guard can find it"
    assert all("marker-end" in s for s in links)
    assert not any('stroke-dasharray="7,5.5"' in s for s in d.o), \
        "a software link must not reuse the electrical dash pattern"
    assert any(s.startswith("<circle") for s in d.o), \
        "software link is a line with small circles along it (ISA-5.1)"
    # the guard is a real guard: strip the marker and it must fail
    stripped = PID()
    stripped.o = [s.replace(' marker-end="url(#aSig)"', "") for s in d.o]
    try:
        assert_softlinks_have_arrowheads(stripped)
    except AssertionError:
        pass
    else:
        raise AssertionError("softlink arrowhead guard did not catch a missing marker")


def test_legend_renders_software_link_entry():
    """The legend must know the third line style ('soft') and draw it as the
    link looks on the sheet, without stamping the swatch as a real softlink
    (a swatch has no arrowhead and must not trip the guard)."""
    d = PID()
    d.legend([("DCS signal", SIG, True), ("Software link (supervisory setpoint)", SIG, "soft")])
    standard_checks(d)
    text = "\n".join(d.o)
    assert ">Software link (supervisory setpoint)<" in text
    assert not any('class="softlink"' in s for s in d.o), "legend swatch is not a signal"
    swatches = [s for s in d.o if 'class="swatch"' in s]
    assert any(s.startswith("<circle") for s in swatches), "soft swatch must show the circles"


def _load_example(name):
    """Import examples/<name>.py as a module without running its __main__ save."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "examples", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_example_grinding_circuit_control():
    """Drawing-level: the shipped example (crushing at basic, grinding at
    intermediate) builds end to end, passes every structural invariant, carries
    the per-circuit tier note naming BOTH circuits (ADR 0004: tiers can be mixed
    per circuit, so the note must list each one), draws the crusher-setting
    loop as a ZIC, declares D on the legend because it draws a density loop,
    and draws the intermediate additions as the reference prescribes: a ratio
    station and override/limit selectors as Y bubbles, the PSM as a controller
    (AIC) rather than the basic-tier indicator, every master landing on a leg
    lettered SP."""
    d = _load_example("build_grinding_circuit_control").build()
    standard_checks(d)
    text = "\n".join(d.o)
    assert "Crushing: basic (assumed) | Grinding: intermediate" in text, \
        "per-circuit tier note must list every circuit in the documented format"
    assert ">ZIC<" in text, "crusher-setting (CSS) loop must be a ZIC controller"
    assert "D = density" in text, "density loop drawn but D not declared on the legend"
    assert any('class="motor"' in s for s in d.o), "drive-speed loops need a motor final element"
    # intermediate tier, cumulative on top of basic (control-strategies.md)
    for letters, role in (("FFY", "water-to-ore ratio station"), ("JY", "power override selector"),
                          ("PY", "pump-pressure override selector"), ("LY", "sump-level limiter"),
                          ("AIC", "PSM cascade master"), ("FIC", "dilution-water cascade slave")):
        assert f">{letters}<" in text, f"intermediate grinding tier must draw the {role} ({letters})"
    assert ">AI<" not in text, "the basic-tier PSM indicator must become the AIC, not sit beside it"
    assert text.count(">SP<") >= 4, "each cascade master must land on a leg lettered SP"


CONTROL_TESTS = [
    ("motor", test_motor),
    ("legend declares D = density", test_legend_declares_density_letter),
    ("legend wraps instead of overflowing", test_legend_wraps_instead_of_overflowing),
    ("supervisory_block", test_supervisory_block),
    ("softlink always arrowed", test_softlink_always_has_an_arrowhead),
    ("legend renders software-link entry", test_legend_renders_software_link_entry),
    ("example: grinding_circuit_control end-to-end", test_example_grinding_circuit_control),
]

ALL_TESTS = (list(COMMINUTION_TESTS) + CLASSIFICATION_TESTS + DEWATERING_TRANSPORT_TESTS
             + CONTROL_TESTS)

if __name__ == "__main__":
    for name, fn in ALL_TESTS:
        check(name, fn)
    print(f"\n{len(ALL_TESTS) - len(FAILURES)}/{len(ALL_TESTS)} passed")
    sys.exit(1 if FAILURES else 0)
