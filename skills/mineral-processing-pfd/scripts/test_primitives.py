# -*- coding: utf-8 -*-
"""
Smoke tests for pid_lib's mineral-processing primitives.

No pytest dependency - this repo has no test framework anywhere else, and
the seam agreed for this skill (see spec) is: call each primitive, assert
structural invariants on the SVG it produces, then rely on the mandatory
render-and-inspect step (SKILL.md) as the real acceptance test. Run with:

    python3 scripts/test_primitives.py
"""
import re
import sys
import xml.etree.ElementTree as ET

from pid_lib import PID

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
    directional control loops)."""
    for s in d.o:
        if 'stroke-dasharray="7,5.5"' in s:
            assert "marker-end" in s, f"signal line missing arrowhead: {s[:80]}"


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
    ("feeder_apron", test_feeder_apron),
    ("conveyor", test_conveyor),
    ("ore_bin", test_ore_bin),
    ("stockpile", test_stockpile),
    ("silo", test_silo),
    ("tailings_dam", test_tailings_dam),
    ("splitter", test_splitter),
    ("junction", test_junction),
]

ALL_TESTS = list(COMMINUTION_TESTS) + CLASSIFICATION_TESTS + DEWATERING_TRANSPORT_TESTS

if __name__ == "__main__":
    for name, fn in ALL_TESTS:
        check(name, fn)
    print(f"\n{len(ALL_TESTS) - len(FAILURES)}/{len(ALL_TESTS)} passed")
    sys.exit(1 if FAILURES else 0)
