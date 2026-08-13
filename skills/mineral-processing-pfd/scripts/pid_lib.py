# -*- coding: utf-8 -*-
"""
pid_lib - primitives for hand-authored mineral-processing flowsheet SVGs.

Forked from pfd-generator/scripts/pid_lib.py (see
docs/adr/0001-mineral-processing-pfd-forks-primitives.md for why this is a
fork, not a shared import: skills are zipped and distributed one at a time,
so a runtime cross-skill import isn't viable). The generic drawing
primitives below (palette, markers, pipe/sig/bubble/cvalve/legend/vessel/
agitator, PID scaffold) are unchanged from that fork point. Everything from
"mineral-processing equipment" onward is new.

Usage:
    from pid_lib import PID
    d = PID(1400, 940)
    d.title("COPPER CONCENTRATOR - COMMINUTION", "Crush-grind-classify | MVP flowsheet")
    d.crusher_jaw(200, 120, 260)
    d.pipe("M 200,260 L 200,340", d.ORE, arrow=True)
    d.mill_sag(320, 300, 520, 380)
    d.legend([("Ore / slurry", d.ORE, False), ("Process water", d.BLUE, False),
              ("DCS signal", d.SIG, True)])
    d.save("out.svg")

All coordinates are absolute in viewBox units. Draw order: vessel/equipment
bodies+fills -> external pipes -> equipment internals -> balloons and valves
last (white fill hides pipes behind tags).

Equipment primitives draw ONLY the body/internals, never their own inlet or
outlet pipe stubs - same convention as vessel() in the pfd-generator fork
point. The composing script always draws every connecting pipe itself with
pipe(), starting exactly at the coordinates it needs, so nozzle placement
never fights the surrounding layout. Each primitive's docstring gives the
coordinates of its notable connection points (feed, discharge, overflow...).
"""
import math
import random

BLUE = "#1d4e89"    # process / wash water
RUST = "#a34a28"    # steam / condensate
CYAN = "#2a7f8f"    # cooling water
GREEN = "#3f7a4d"   # gas / air (flotation sparge)
ORE = "#7a5230"     # ore slurry / pulp
SOLIDS = "#9c8552"  # dry ore / rock (conveyed, not slurried)
SIG = "#50565f"     # instrument signal
EQ = "#343a46"       # equipment outline
INK = "#111418"
SUB = "#5a6472"
HAIR = "#b8bec7"
LIQ = "#dce8f5"
SHELL = "#f7f8fa"
RED = "#b02418"
FONTS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

_ARROW_COLORS = {BLUE: "aBlue", RUST: "aRust", CYAN: "aCyan", GREEN: "aGreen",
                  ORE: "aOre", SOLIDS: "aSolids"}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text_width(s, size, bold=False):
    """Rough width estimate. Verify by rendering; this only catches gross errors."""
    return len(s) * size * (0.60 if bold else 0.55)


class PID:
    BLUE, RUST, CYAN, GREEN, ORE, SOLIDS, SIG, EQ = BLUE, RUST, CYAN, GREEN, ORE, SOLIDS, SIG, EQ
    INK, SUB, LIQ, SHELL, RED, HAIR = INK, SUB, LIQ, SHELL, RED, HAIR

    def __init__(self, w=1400, h=940, border=True):
        self.w, self.h = w, h
        self.o = []
        self.o.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONTS}">')
        self.o.append('<defs>')
        for name, col in (("aBlue", BLUE), ("aRust", RUST), ("aSig", SIG),
                          ("aCyan", CYAN), ("aGreen", GREEN),
                          ("aOre", ORE), ("aSolids", SOLIDS)):
            self.o.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 0,0 L 10,5 L 0,10 z" fill="{col}"/></marker>')
        self.o.append('</defs>')
        self.o.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
        if border:
            self.o.append(f'<rect x="20" y="20" width="{w-40}" height="{h-40}" '
                          f'fill="none" stroke="{HAIR}" stroke-width="1"/>')

    def add(self, s):
        self.o.append(s)

    # ---------------------------------------------------------------- text
    def txt(self, x, y, s, size=10, fill=INK, weight="normal",
            anchor="start", ls=0):
        extra = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>')

    def title(self, main, subtitle=None, stamp=True):
        self.txt(45, 60, esc(main), size=21, weight="bold")
        if subtitle:
            self.txt(45, 82, esc(subtitle), size=11.5, fill=SUB)
        if stamp:
            x = self.w - 222
            self.add(f'<rect x="{x}" y="42" width="177" height="24" fill="none" '
                     f'stroke="{RED}" stroke-width="1.4"/>')
            self.txt(x + 88, 59, "NOT FOR CONSTRUCTION", size=11, weight="bold",
                     fill=RED, anchor="middle", ls=0.4)

    # ---------------------------------------------------------------- lines
    def pipe(self, d, color=ORE, arrow=False, width=2.4):
        key = _ARROW_COLORS.get(color, "aOre")
        m = f' marker-end="url(#{key})"' if arrow else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                 f'stroke-linejoin="round"{m}/>')

    def sig(self, d, arrow=True):
        """Instrument signal. Arrow points INTO the receiving device."""
        m = ' marker-end="url(#aSig)"' if arrow else ''
        self.add(f'<path d="{d}" fill="none" stroke="{SIG}" stroke-width="1.35" '
                 f'stroke-dasharray="7,5.5"{m}/>')

    def lead(self, x1, y1, x2, y2):
        """Thin solid process/impulse connection from equipment wall to a balloon."""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{EQ}" stroke-width="1.2"/>')

    def line_jump(self, x, y, color=ORE, r=14):
        """Semicircular hop. Break the underlying pipe path either side of x."""
        self.add(f'<path d="M {x-r},{y} A {r} {r} 0 0 1 {x+r},{y}" fill="none" '
                 f'stroke="{color}" stroke-width="2.4"/>')

    # ---------------------------------------------------------------- instruments
    def bubble(self, cx, cy, top, bot, shared=False, panel=False, r=22):
        """shared=True -> DCS/shared display (circle in square).
           panel=True  -> panel mounted (chord line)."""
        if shared:
            self.add(f'<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" '
                     f'fill="#ffffff" stroke="{EQ}" stroke-width="1.4"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" '
                 f'stroke="{EQ}" stroke-width="1.4"/>')
        if panel:
            self.add(f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" '
                     f'stroke="{EQ}" stroke-width="1.1"/>')
        self.txt(cx, cy - 2, top, size=11.5, weight="bold", anchor="middle")
        self.txt(cx, cy + 12, bot, size=10, anchor="middle")

    def cvalve(self, cx, cy, tag, fail=None, actuator="below", tag_dy=45):
        """Control valve. actuator='above' or 'below' - put it on the side the
        signal arrives from, so the signal never crosses the process line."""
        for sx in (-18, 18):
            self.add(f'<path d="M {cx+sx},{cy-12} L {cx+sx},{cy+12} L {cx},{cy} Z" '
                     f'fill="#ffffff" stroke="{EQ}" stroke-width="1.6" '
                     f'stroke-linejoin="miter"/>')
        s = -1 if actuator == "above" else 1
        self.add(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+s*20}" '
                 f'stroke="{EQ}" stroke-width="1.4"/>')
        ry = cy + s * 32 - (6 if s > 0 else 6)
        self.add(f'<rect x="{cx-14}" y="{ry}" width="28" height="12" rx="6" '
                 f'fill="#ffffff" stroke="{EQ}" stroke-width="1.4"/>')
        label = f"{tag}  ({fail})" if fail else tag
        self.txt(cx, cy + tag_dy, label, size=10.5, weight="bold", anchor="middle")

    def manual_valve(self, cx, cy, tag=None):
        for sx in (-14, 14):
            self.add(f'<path d="M {cx+sx},{cy-10} L {cx+sx},{cy+10} L {cx},{cy} Z" '
                     f'fill="#ffffff" stroke="{EQ}" stroke-width="1.5"/>')
        if tag:
            self.txt(cx, cy + 32, tag, size=10, weight="bold", anchor="middle")

    # ---------------------------------------------------------------- generic vessel
    def vessel(self, x0, y0, x1, y1, r=26, level=None, level_label=None):
        """Rounded-rectangle vessel. Flat wall spans are x0+r..x1-r and y0+r..y1-r;
        put every nozzle inside those ranges."""
        self.add(f'<path d="M {x0+r},{y0} L {x1-r},{y0} Q {x1},{y0} {x1},{y0+r} '
                 f'L {x1},{y1-r} Q {x1},{y1} {x1-r},{y1} L {x0+r},{y1} '
                 f'Q {x0},{y1} {x0},{y1-r} L {x0},{y0+r} Q {x0},{y0} {x0+r},{y0} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="2.2" stroke-linejoin="miter"/>')
        if level is not None:
            self.add(f'<path d="M {x0},{level} L {x1},{level} L {x1},{y1-r} '
                     f'Q {x1},{y1} {x1-r},{y1} L {x0+r},{y1} Q {x0},{y1} {x0},{y1-r} Z" '
                     f'fill="{LIQ}"/>')
            self.add(f'<line x1="{x0+6}" y1="{level}" x2="{x1-6}" y2="{level}" '
                     f'stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="7,5"/>')
            if level_label:
                self.txt(x1 - 10, level - 8, level_label, size=8.5, fill=SUB,
                         anchor="end", ls=0.3)

    def agitator(self, cx, top, shaft_bottom, tag="AG-101"):
        self.add(f'<rect x="{cx-28}" y="{top-44}" width="56" height="44" '
                 f'fill="#ffffff" stroke="{EQ}" stroke-width="1.6"/>')
        self.txt(cx, top - 15, "M", size=15, weight="bold", anchor="middle")
        self.add(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{shaft_bottom}" '
                 f'stroke="{EQ}" stroke-width="2"/>')
        b = shaft_bottom
        self.add(f'<path d="M {cx-32},{b+4} L {cx-4},{b-14} L {cx-4},{b-5} '
                 f'L {cx-32},{b+13} Z" fill="{EQ}"/>')
        self.add(f'<path d="M {cx+32},{b+4} L {cx+4},{b-14} L {cx+4},{b-5} '
                 f'L {cx+32},{b+13} Z" fill="{EQ}"/>')
        self.txt(cx + 42, top - 18, tag, size=10.5, weight="bold")

    def equip_tag(self, cx, y, tag, service=None, detail=None):
        """Equipment identification. Place in dead space; check against any line
        dropping from the equipment bottom."""
        self.txt(cx, y, tag, size=14, weight="bold", anchor="middle")
        if service:
            self.txt(cx, y + 18, service, size=10, fill=SUB, anchor="middle", ls=0.4)
        if detail:
            self.txt(cx, y + 35, detail, size=9, fill=SUB, anchor="middle")

    # ---------------------------------------------------------------- comminution
    def rock_breaker(self, cx, top, tag=None, w=70):
        """Static grizzly with a pivoted hydraulic hammer boom. Feed drops onto the
        grizzly from above; oversize is broken in place, everything passes down
        through top+52 at cx."""
        x0, x1 = cx - w / 2, cx + w / 2
        y0, y1 = top + 22, top + 52
        self.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{y1-y0}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        for i in range(4):
            gx = x0 + 10 + i * (w - 20) / 3
            self.add(f'<line x1="{gx}" y1="{y0+3}" x2="{gx+10}" y2="{y1-3}" '
                     f'stroke="{EQ}" stroke-width="1.1"/>')
        px, py = x0 - 6, top - 6
        tipx, tipy = cx + 6, y0 + 4
        self.add(f'<circle cx="{px}" cy="{py}" r="4" fill="{EQ}"/>')
        self.add(f'<line x1="{px}" y1="{py}" x2="{tipx}" y2="{tipy}" '
                 f'stroke="{EQ}" stroke-width="3"/>')
        self.add(f'<path d="M {tipx-6},{tipy-8} L {tipx+6},{tipy-8} L {tipx},{tipy+4} Z" '
                 f'fill="{EQ}"/>')
        if tag:
            self.txt(cx, y1 + 22, tag, size=10.5, weight="bold", anchor="middle")

    def feeder_vibrating(self, x0, y0, x1, y1, tag=None):
        """Skewed pan with vibration ticks beneath. Feed enters top-left corner,
        discharges off the bottom-right edge."""
        skew = 14
        self.add(f'<path d="M {x0+skew},{y0} L {x1},{y0} L {x1-skew},{y1} L {x0},{y1} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        zy, n = y1 + 8, 5
        pts = [f"{x0 + (x1-x0)*i/n},{zy + (5 if i % 2 == 0 else 0)}" for i in range(n + 1)]
        self.add(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{EQ}" stroke-width="1.1"/>')
        if tag:
            self.txt((x0 + x1) / 2, y1 + 30, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_jaw(self, cx, top, bottom, tag=None, w=64):
        """Single/double toggle jaw crusher: a housing with two visibly converging
        jaw plates forming a narrow crushing throat, distinct from the funnel
        silhouette shared by bins/silos. Feed enters the top span (x0..x1, top);
        crushed product discharges the chute at (cx, bottom)."""
        x0, x1 = cx - w / 2, cx + w / 2
        chute_top = bottom - 22
        gap = 8
        self.add(f'<rect x="{x0}" y="{top}" width="{w}" height="{chute_top-top}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<path d="M {x0+6},{top+6} L {cx-gap},{chute_top}" '
                 f'stroke="{EQ}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        self.add(f'<path d="M {x1-6},{top+6} L {cx+gap},{chute_top}" '
                 f'stroke="{EQ}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        self.add(f'<path d="M {cx-gap},{chute_top} L {cx-10},{bottom} '
                 f'L {cx+10},{bottom} L {cx+gap},{chute_top} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_cone(self, cx, top, bottom, tag=None, w=76):
        """Cone crusher: bowl liner (outer) with a suspended mantle (inner cone) on
        a central spindle. Feed enters top span; product discharges at (cx, bottom)."""
        x0, x1 = cx - w / 2, cx + w / 2
        self.add(f'<path d="M {x0},{top} L {x1},{top} L {cx+16},{bottom} L {cx-16},{bottom} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        mtop = top + 10
        self.add(f'<line x1="{cx}" y1="{top-14}" x2="{cx}" y2="{mtop}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<path d="M {cx-18},{mtop} L {cx+18},{mtop} L {cx},{bottom-10} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.4"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_gyratory(self, cx, top, bottom, tag=None, w=70):
        """Gyratory crusher: fixed spider bar across a wide top feed opening, with
        a central spindle running down to the discharge. Feed enters top span;
        product discharges at (cx, bottom)."""
        x0, x1 = cx - w / 2, cx + w / 2
        self.add(f'<path d="M {x0},{top+10} L {x1},{top+10} L {cx+12},{bottom} L {cx-12},{bottom} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<line x1="{x0}" y1="{top+10}" x2="{x1}" y2="{top+10}" '
                 f'stroke="{EQ}" stroke-width="2.4"/>')
        self.add(f'<line x1="{cx}" y1="{top-14}" x2="{cx}" y2="{top+10}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<line x1="{cx}" y1="{top+10}" x2="{cx}" y2="{bottom-8}" '
                 f'stroke="{EQ}" stroke-width="1.4"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_vsi(self, cx, cy, tag=None, r=36):
        """Vertical shaft impactor (Barmac-type, rock-on-rock). Feed enters the
        top of the circular housing at (cx, cy-r); product discharges (cx, cy+r)."""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        for k in range(3):
            ang = math.radians(90 + k * 120)
            ex, ey = cx + (r - 6) * math.cos(ang), cy + (r - 6) * math.sin(ang)
            self.add(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" '
                     f'stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{EQ}"/>')
        if tag:
            self.txt(cx, cy + r + 20, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_impact(self, cx, cy, tag=None, w=76, h=56):
        """Horizontal shaft impactor: rectangular housing, rotor with radial hammer
        lines. Feed enters the top edge; product discharges the bottom edge."""
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
        self.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        rr = h / 2 - 8
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{EQ}" stroke-width="1.4"/>')
        for k in range(4):
            ang = math.radians(k * 90 + 20)
            ex, ey = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            self.add(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" '
                     f'stroke="{EQ}" stroke-width="1.2"/>')
        if tag:
            self.txt(cx, y1 + 20, tag, size=10.5, weight="bold", anchor="middle")

    def crusher_roll(self, cx, top, bottom, tag=None, r=24):
        """Twin counter-rotating rolls (roll crusher / HPGR stand-in - see
        references/mineral-processing-symbols.md for the HPGR caveat). Feed drops
        into the gap between the rolls from the top; product discharges below."""
        cy = top + r + 6 if bottom - top <= 2 * r else (top + bottom) / 2
        x1c, x2c = cx - r - 3, cx + r + 3
        self.add(f'<circle cx="{x1c}" cy="{cy}" r="{r}" fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<circle cx="{x2c}" cy="{cy}" r="{r}" fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<path d="M {x1c-8},{cy-r+6} A {r-8} {r-8} 0 0 1 {x1c+8},{cy-r+6}" '
                 f'fill="none" stroke="{EQ}" stroke-width="1"/>')
        self.add(f'<path d="M {x2c-8},{cy-r+6} A {r-8} {r-8} 0 0 0 {x2c+8},{cy-r+6}" '
                 f'fill="none" stroke="{EQ}" stroke-width="1"/>')
        if tag:
            self.txt(cx, cy + r + 20, tag, size=10.5, weight="bold", anchor="middle")

    def screen(self, x0, y0, x1, y1, deck_count=1, wet=False, tag=None):
        """Vibrating screen, 1-4 decks. Body spans (x0,y0)-(x1, y0 + 0.7*h); each
        deck's oversize outlet is at (x1, dy) for dy in the returned list; the
        final undersize outlet is at ((x0+x1)/2, y1). wet=True only changes the
        label - it does not draw a wash-water inlet; the composing script should
        route a BLUE pipe into the top span when wet=True. Distinct from SD-DW/
        SD-HY, which are separate pieces of equipment, not a wet mode of this one."""
        deck_count = max(1, min(4, deck_count))
        w, h = x1 - x0, y1 - y0
        body_bottom = y0 + h * 0.7
        self.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{body_bottom-y0}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        fx = (x0 + x1) / 2
        self.add(f'<path d="M {x0},{body_bottom} L {x1},{body_bottom} L {fx+10},{y1} '
                 f'L {fx-10},{y1} Z" fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        deck_ys = []
        for i in range(deck_count):
            dy = y0 + (body_bottom - y0) * (i + 1) / (deck_count + 1)
            deck_ys.append(dy)
            self.add(f'<line x1="{x0+4}" y1="{dy}" x2="{x1-4}" y2="{dy}" '
                     f'stroke="{EQ}" stroke-width="1.1" stroke-dasharray="4,3"/>')
        label = tag or ""
        if label:
            suffix = f" ({deck_count}-deck, {'wet' if wet else 'dry'})"
            self.txt((x0 + x1) / 2, y0 - 10, label + suffix, size=10, weight="bold", anchor="middle")
        return deck_ys

    def _mill(self, x0, y0, x1, y1, charge="balls", tag=None):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        self.add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        for ex in (x0, x1):
            self.add(f'<ellipse cx="{ex}" cy="{cy}" rx="{min(14, rx*0.3):.1f}" ry="{ry}" '
                     f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        rnd = random.Random(42)
        n, rmax = (5, 9) if charge == "sag" else (14, 4)
        for _ in range(n):
            px = rnd.uniform(x0 + 20, x1 - 20)
            py = rnd.uniform(cy - ry * 0.5, cy + ry * 0.5)
            self.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rmax}" '
                     f'fill="none" stroke="{EQ}" stroke-width="1"/>')
        if tag:
            self.txt(cx, y1 + 22, tag, size=10.5, weight="bold", anchor="middle")

    def mill_sag(self, x0, y0, x1, y1, tag=None):
        """SAG mill: horizontal drum with a few large ore/steel charge circles.
        Feed enters the left trunnion (x0, cy); product discharges the right
        trunnion (x1, cy)."""
        self._mill(x0, y0, x1, y1, charge="sag", tag=tag)

    def mill_ball(self, x0, y0, x1, y1, tag=None):
        """Ball mill: horizontal drum with many small steel-ball charge circles.
        Feed enters the left trunnion (x0, cy); product discharges the right
        trunnion (x1, cy)."""
        self._mill(x0, y0, x1, y1, charge="balls", tag=tag)

    # ------------------------------------------------------ classification/flotation
    def cyclone(self, cx, top, bottom, tag=None, r=30):
        """Hydrocyclone: cylindrical top, conical bottom. Tangential feed enters at
        (cx-r, top+14); overflow exits up at (cx, top-14); underflow (apex)
        discharges at (cx, bottom)."""
        neck = top + r
        self.add(f'<rect x="{cx-r}" y="{top}" width="{2*r}" height="{neck-top}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<path d="M {cx-r},{neck} L {cx+r},{neck} L {cx},{bottom} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        # tangential feed nozzle (short stub on the shell, feed pipe attaches here)
        self.add(f'<line x1="{cx-r-16}" y1="{top+14}" x2="{cx-r}" y2="{top+14}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        # overflow pipe stub up from the vortex finder
        self.add(f'<line x1="{cx}" y1="{top-14}" x2="{cx}" y2="{top}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def classifier_screw(self, x0, y0, x1, y1, tag=None):
        """Inclined trough with a screw conveyor. Fine overflow discharges the low
        end (x0, y1); coarse sand is screwed up and out the high end (x1, y0)."""
        self.add(f'<path d="M {x0},{y1-16} L {x0},{y1} L {x1},{y0} L {x1},{y0-16} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        n = 6
        for i in range(n):
            t0, t1 = i / n, (i + 0.5) / n
            hx0, hy0 = x0 + (x1 - x0) * t0, (y1 - 8) + (y0 - (y1 - 8)) * t0
            hx1, hy1 = x0 + (x1 - x0) * t1, (y1 - 8) + (y0 - (y1 - 8)) * t1
            self.add(f'<line x1="{hx0:.1f}" y1="{hy0:.1f}" x2="{hx1:.1f}" y2="{hy1:.1f}" '
                     f'stroke="{EQ}" stroke-width="1.3"/>')
        if tag:
            self.txt((x0 + x1) / 2, y0 - 20, tag, size=10.5, weight="bold", anchor="middle")

    def classifier_rake(self, x0, y0, x1, y1, tag=None):
        """Inclined trough with a reciprocating rake. Fine overflow discharges the
        low end (x0, y1); coarse sand is raked up and out the high end (x1, y0)."""
        self.add(f'<path d="M {x0},{y1-16} L {x0},{y1} L {x1},{y0} L {x1},{y0-16} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        n = 5
        for i in range(1, n):
            t = i / n
            bx, by = x0 + (x1 - x0) * t, (y1 - 8) + (y0 - (y1 - 8)) * t
            self.add(f'<path d="M {bx-6},{by+7} L {bx+6},{by+7} L {bx},{by-7} Z" '
                     f'fill="none" stroke="{EQ}" stroke-width="1.3"/>')
        if tag:
            self.txt((x0 + x1) / 2, y0 - 20, tag, size=10.5, weight="bold", anchor="middle")

    def flotation_cell(self, x0, y0, x1, y1, tag=None):
        """Mechanical flotation cell: tank with an impeller shaft and a froth
        overflow lip. Feed/air enter the bottom span; froth concentrate overflows
        the lip at (x1, y0); tailings discharge the bottom span."""
        lip = 10
        self.add(f'<path d="M {x0},{y0} L {x1-lip},{y0} L {x1-lip},{y0+lip} '
                 f'L {x1},{y0+lip} L {x1},{y1} L {x0},{y1} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        cx = (x0 + x1) / 2 - lip / 2
        self.add(f'<line x1="{cx}" y1="{y0-30}" x2="{cx}" y2="{y1-14}" '
                 f'stroke="{EQ}" stroke-width="2"/>')
        self.add(f'<rect x="{cx-18}" y="{y0-44}" width="36" height="18" '
                 f'fill="#ffffff" stroke="{EQ}" stroke-width="1.4"/>')
        self.txt(cx, y0 - 31, "M", size=11, weight="bold", anchor="middle")
        r = 14
        self.add(f'<circle cx="{cx}" cy="{y1-14}" r="{r}" fill="none" '
                 f'stroke="{EQ}" stroke-width="1.4"/>')
        self.add(f'<line x1="{cx-r}" y1="{y1-14}" x2="{cx+r}" y2="{y1-14}" '
                 f'stroke="{EQ}" stroke-width="1.1"/>')
        self.add(f'<line x1="{cx}" y1="{y1-14-r}" x2="{cx}" y2="{y1-14+r}" '
                 f'stroke="{EQ}" stroke-width="1.1"/>')
        if tag:
            self.txt((x0 + x1) / 2, y1 + 20, tag, size=10.5, weight="bold", anchor="middle")

    def flotation_column(self, cx, top, bottom, tag=None, r=28):
        """Column flotation: tall vertical cell, froth overflow lip at (cx-r, top),
        feed entering mid-height at (cx-r, midpoint), air sparger at the bottom
        (bubble ticks), tailings underflow at (cx, bottom)."""
        self.add(f'<rect x="{cx-r}" y="{top}" width="{2*r}" height="{bottom-top}" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<line x1="{cx-r-10}" y1="{top+6}" x2="{cx-r}" y2="{top+6}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        by = bottom - 16
        for i in range(5):
            bx = cx - r + 10 + i * (2 * r - 20) / 4
            self.add(f'<circle cx="{bx:.1f}" cy="{by}" r="2.2" fill="none" '
                     f'stroke="{EQ}" stroke-width="1"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    # ------------------------------------------------------ dewatering/transport/storage
    def thickener(self, cx, top, bottom, tag=None, r=90):
        """Conventional rake thickener, side elevation: shallow cone-bottomed tank
        with a center feed well and a peripheral overflow launder. Feed enters the
        center well from above (cx, top-20); overflow exits the launder at
        (cx+r, top+14); underflow discharges the apex (cx, bottom)."""
        wall_bottom = top + (bottom - top) * 0.55
        self.add(f'<path d="M {cx-r},{top} L {cx+r},{top} L {cx+r},{wall_bottom} '
                 f'L {cx},{bottom} L {cx-r},{wall_bottom} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<line x1="{cx-r}" y1="{top+14}" x2="{cx+r}" y2="{top+14}" '
                 f'stroke="{EQ}" stroke-width="1.1"/>')
        self.add(f'<rect x="{cx-16}" y="{top}" width="32" height="20" '
                 f'fill="#ffffff" stroke="{EQ}" stroke-width="1.4"/>')
        self.add(f'<line x1="{cx}" y1="{top+20}" x2="{cx}" y2="{wall_bottom}" '
                 f'stroke="{EQ}" stroke-width="1.4"/>')
        self.add(f'<line x1="{cx-r+10}" y1="{wall_bottom-4}" x2="{cx+r-10}" y2="{wall_bottom-4}" '
                 f'stroke="{EQ}" stroke-width="1.1"/>')
        if tag:
            self.txt(cx, bottom + 22, tag, size=10.5, weight="bold", anchor="middle")

    def filter_drum(self, cx, cy, tag=None, r=45):
        """Drum vacuum filter: circular drum partially submerged in a trough. Feed
        slurry enters the trough at (cx-r-14, cy+r*0.5); filtrate exits below at
        (cx, cy+r*0.7+18); cake discharges tangentially at (cx+r, cy-r*0.3)."""
        trough_top = cy + r * 0.35
        self.add(f'<path d="M {cx-r-10},{trough_top} L {cx+r+10},{trough_top} '
                 f'L {cx+r-6},{cy+r*0.7} L {cx-r+6},{cy+r*0.7} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r*0.7:.1f}" fill="none" '
                 f'stroke="{EQ}" stroke-width="1"/>')
        self.add(f'<line x1="{cx+r*0.7:.1f}" y1="{cy-r*0.3:.1f}" '
                 f'x2="{cx+r+18}" y2="{cy-r*0.3-10:.1f}" stroke="{EQ}" stroke-width="1.4"/>')
        if tag:
            self.txt(cx, cy + r + 22, tag, size=10.5, weight="bold", anchor="middle")

    def pump_centrifugal(self, cx, cy, tag=None, r=16):
        """Centrifugal pump: circle with a discharge triangle. Suction enters the
        left of the circle (cx-r, cy); discharge exits the triangle tip
        (cx+r+10, cy)."""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<path d="M {cx-6},{cy-9} L {cx-6},{cy+9} L {cx+9},{cy} Z" fill="{EQ}"/>')
        if tag:
            self.txt(cx, cy + r + 20, tag, size=10, weight="bold", anchor="middle")

    def pump_sump(self, cx, cy, tag=None, r=16):
        """Sump pump: centrifugal pump symbol seated over a sump/pit basin. Slurry
        enters the basin from above; discharge exits the pump tip (cx+r+10, cy)."""
        by = cy + r + 10
        self.add(f'<path d="M {cx-r-8},{by} L {cx+r+8},{by} L {cx+r-4},{by+18} '
                 f'L {cx-r+4},{by+18} Z" fill="{SHELL}" stroke="{EQ}" stroke-width="1.5"/>')
        self.pump_centrifugal(cx, cy, tag=None, r=r)
        if tag:
            self.txt(cx, by + 36, tag, size=10, weight="bold", anchor="middle")

    def feeder_apron(self, x0, y0, x1, y1, tag=None):
        """Apron feeder: flat pan built from overlapping plate segments. Feed
        enters the top-left corner; discharges the bottom-right edge."""
        skew = 10
        self.add(f'<path d="M {x0+skew},{y0} L {x1},{y0} L {x1-skew},{y1} L {x0},{y1} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        n = 6
        for i in range(1, n):
            t = i / n
            px = x0 + skew * (1 - t) + (x1 - skew * t - (x0 + skew)) * t
            self.add(f'<line x1="{x0+(x1-x0)*t:.1f}" y1="{y0}" '
                     f'x2="{x0+(x1-x0)*t - skew*(1-2*t)*0.3:.1f}" y2="{y1}" '
                     f'stroke="{EQ}" stroke-width="1"/>')
        if tag:
            self.txt((x0 + x1) / 2, y1 + 22, tag, size=10.5, weight="bold", anchor="middle")

    def conveyor(self, x0, y0, x1, y1, tag=None):
        """Belt conveyor: inclined double line with idler ticks and a direction
        arrowhead. Feed enters (x0, y0); discharges (x1, y1)."""
        self.add(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        offx, offy = 0, 10
        self.add(f'<line x1="{x0+offx}" y1="{y0+offy}" x2="{x1+offx}" y2="{y1+offy}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        n = 6
        for i in range(1, n):
            t = i / n
            ix, iy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            self.add(f'<line x1="{ix:.1f}" y1="{iy:.1f}" x2="{ix:.1f}" y2="{iy+offy:.1f}" '
                     f'stroke="{EQ}" stroke-width="1"/>')
        ang = math.atan2(y1 - y0, x1 - x0)
        ahx, ahy = (x0 + x1) / 2, (y0 + y1) / 2 + offy / 2
        self.add(f'<path d="M {ahx:.1f},{ahy:.1f} '
                 f'L {ahx-10*math.cos(ang-0.4):.1f},{ahy-10*math.sin(ang-0.4):.1f} '
                 f'L {ahx-10*math.cos(ang+0.4):.1f},{ahy-10*math.sin(ang+0.4):.1f} Z" fill="{EQ}"/>')
        if tag:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 12
            self.txt(mx, my, tag, size=10, weight="bold", anchor="middle")

    def ore_bin(self, cx, top, bottom, tag=None, w=80):
        """Ore bin/bunker: hopper narrowing to a spout. Feed enters the top span;
        discharges the spout at (cx, bottom)."""
        x0, x1 = cx - w / 2, cx + w / 2
        neck = bottom - 16
        self.add(f'<path d="M {x0},{top} L {x1},{top} L {x1},{neck-20} '
                 f'L {cx+10},{neck} L {cx+10},{bottom} L {cx-10},{bottom} '
                 f'L {cx-10},{neck} L {x0},{neck-20} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def stockpile(self, cx, base_y, tag=None, w=140, h=70):
        """Stockpile: conical pile cross-section sitting on a baseline centered at
        (cx, base_y)."""
        self.add(f'<path d="M {cx-w/2},{base_y} L {cx},{base_y-h} L {cx+w/2},{base_y} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<line x1="{cx-w/2}" y1="{base_y}" x2="{cx+w/2}" y2="{base_y}" '
                 f'stroke="{EQ}" stroke-width="1.6"/>')
        if tag:
            self.txt(cx, base_y + 20, tag, size=10.5, weight="bold", anchor="middle")

    def silo(self, cx, top, bottom, tag=None, w=70):
        """Silo: cylindrical shell with a coned bottom. Feed enters the top;
        discharges the cone apex at (cx, bottom)."""
        neck = bottom - 24
        self.add(f'<path d="M {cx-w/2},{top} L {cx+w/2},{top} L {cx+w/2},{neck} '
                 f'L {cx},{bottom} L {cx-w/2},{neck} Z" '
                 f'fill="{SHELL}" stroke="{EQ}" stroke-width="1.8"/>')
        if tag:
            self.txt(cx, bottom + 20, tag, size=10.5, weight="bold", anchor="middle")

    def tailings_dam(self, x0, base_y, tag=None, w=200, h=50):
        """Tailings dam: embankment cross-section with a pond surface line held
        behind it. Tailings slurry enters from the pond side (x0, base_y-h*0.6)."""
        x1 = x0 + w
        crest = base_y - h
        self.add(f'<path d="M {x0},{base_y} L {x0+w*0.3},{crest} L {x0+w*0.45},{crest} '
                 f'L {x1},{base_y} Z" fill="{SHELL}" stroke="{EQ}" stroke-width="1.6"/>')
        self.add(f'<line x1="{x0-40}" y1="{crest+10}" x2="{x0+w*0.3}" y2="{crest+10}" '
                 f'stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3,3"/>')
        if tag:
            self.txt(x0 + w / 2, base_y + 20, tag, size=10.5, weight="bold", anchor="middle")

    def splitter(self, cx, cy, n_outputs=2, tag=None, spread=40):
        """Stream splitter: just the junction node. Draws no lines of its own -
        the composing script draws the inbound pipe and all n_outputs (2 or 3)
        outbound pipes with pipe(), all starting exactly at (cx, cy), in the
        process-stream color. Kept as a separate primitive (rather than a bare
        circle) so a splitter reads as a deliberate symbol, not a stray dot."""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{EQ}"/>')
        if tag:
            self.txt(cx, cy - 14, tag, size=9.5, weight="bold", anchor="middle")

    # ---------------------------------------------------------------- sheet furniture
    def notes(self, x, y, heading, bullets, size=9.5):
        self.txt(x, y, heading, size=11, weight="bold", ls=0.4)
        for i, b in enumerate(bullets):
            self.txt(x, y + 24 + i * 18, "&#8226;  " + esc(b), size=size, fill=SUB)

    def design_basis(self, cx, y, text, size=9.5):
        self.txt(cx, y, esc(text), size=size, fill=SUB, anchor="middle")

    def legend(self, entries, y=886, x=60, gap=210, size=12):
        """entries: list of (label, color, dashed)."""
        cx = x
        for label, color, dashed in entries:
            dash = ' stroke-dasharray="7,5.5"' if dashed else ''
            wgt = 1.6 if dashed else 2.8
            self.add(f'<line x1="{cx}" y1="{y}" x2="{cx+45}" y2="{y}" '
                     f'stroke="{color}" stroke-width="{wgt}"{dash}/>')
            self.txt(cx + 55, y + 5, esc(label), size=size, fill=SUB)
            cx += max(gap, 55 + text_width(label, size) + 40)

    def revision(self, text, y=890):
        self.txt(self.w - 55, y, esc(text), size=9, fill=SUB, anchor="end")

    # ---------------------------------------------------------------- output
    def save(self, path):
        out = "\n".join(self.o + ["</svg>"])
        with open(path, "w") as f:
            f.write(out)
        return path


def render(svg_path, png_path, width=1680):
    import cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=width)
    return png_path


def zoom(png_path, out_path, box, src_width=3200, canvas_width=1400):
    """box = (x0, y0, x1, y1) in viewBox units. Render at src_width first."""
    from PIL import Image
    im = Image.open(png_path)
    s = src_width / float(canvas_width)
    im.crop(tuple(int(v * s) for v in box)).save(out_path)
    return out_path
