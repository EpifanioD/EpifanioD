"""assets/hero.svg: pixel-art scene. Davi waves, walks to the desk, sits down and codes.

The scene is drawn on a grid (1 unit = PX screen pixels). Sprites are strings where
each character is a palette color and "." is transparent. States (waving, walking,
seated) are separate groups switched on and off by CSS animations over a timeline.
"""
from svg import THEME, document, esc, load_content, rect, save, spans, text

W, H = 900, 360
PX = 5                      # screen pixels per grid unit
GW, GH = W // PX, H // PX   # 180 x 72 grid
FLOOR = 64

PALETTE = {
    "H": "#241c1a", "h": "#3b2e29",   # hair, highlight
    "S": "#c58c74", "s": "#a8725c",   # skin, shade (sampled from the avatar)
    "E": "#1a1412", "M": "#6b3a2e",   # eyes, mouth
    "W": "#e6edf3",                   # earbuds
    "T": "#3d4250", "t": "#2d313b",   # dark grey t-shirt
    "P": "#2b3a55", "B": "#d0d7de",   # jeans, sneakers
}

FRONT = [
    "......HHHHHH......",
    ".....HHhHHhHH.....",
    "....HHHHHHHHHH....",
    "....HHHHHHHHHH....",
    "....HSSSSSSSSH....",
    "....SSSSSSSSSS....",
    "...WSSESSSSESSs...",
    "....SSSSSSSSSS....",
    "....SSSSssSSSS....",
    "....SSSMMMMSSS....",
    ".....SSSSSSSS.....",
    "......ssSSss......",
    ".......SSSS.......",
    ".....TTTTTTTT.....",
    "....TTTTTTTTTT....",
    "...TTTTTTTTTTTT...",
    "...TTTtTTTTtTTT...",
    "...SSTTTTTTTTSS...",
    "...SSTTTTTTTTSS...",
    "...SSTTTTTTTTSS...",
    ".....TTTTTTTT.....",
    ".....PPPPPPPP.....",
    ".....PPPPPPPP.....",
    ".....PPP..PPP.....",
    ".....PPP..PPP.....",
    ".....PPP..PPP.....",
    "....BBBB..BBBB....",
]

# raised right arm for the wave, two hand positions
WAVE_ARM = [(15, 14, "T"), (14, 14, "T"), (14, 15, "T"), (13, 15, "S"), (12, 15, "S"), (12, 16, "S"),
            (11, 16, "S"), (10, 16, "S")]
WAVE_HAND = {
    "a": [(9, 16), (9, 17), (8, 16), (8, 17), (7, 16), (7, 17)],
    "b": [(9, 15), (9, 16), (8, 15), (8, 14), (7, 14), (7, 15)],
}

SIDE = [
    "....HHHHH.....",
    "...HHhHHHHH...",
    "..HHHHHHHHHH..",
    "..HHHHHHHHHH..",
    "..HHHHHSSSSS..",
    "..HHHSSSSSES..",
    "..HWSSSSSSSSS.",
    "..HSSSSSSSSS..",
    "...SSSSSSSSs..",
    "...SSSSSSMM...",
    "....SSSSSSS...",
    ".....sSSSs....",
    "......SSS.....",
    "....TTTTTT....",
    "...TTTTTTTT...",
    "...TTTTTTTT...",
    "...TTTTTTTT...",
    "...TTTTTTTT...",
    "...TTTTTTTT...",
    "....TTTTTT....",
    "....PPPPPP....",
]
SIDE_LEGS = {
    "a": ["...PPP..PPP...", "..PPP....PPP..", "..PP......PP..", "..PP......PP..", ".BBB......BBBB"],
    "b": [".....PPPP.....", ".....PPPP.....", ".....PPPP.....", ".....PPPP.....", "....BBBBBB...."],
}
SIDE_ARM = {
    "a": [(14, 8, "t"), (15, 8, "t"), (16, 9, "S"), (17, 9, "S"), (17, 10, "S"), (18, 10, "S")],
    "b": [(14, 5, "t"), (15, 5, "t"), (16, 4, "S"), (17, 4, "S"), (17, 3, "S"), (18, 3, "S")],
}

BACK = [
    ".....HHHHHH.....",
    "....HHhHHhHH....",
    "...HHHHHHHHHH...",
    "...HHHHHHHHHH...",
    "...HHHHHHhHHH...",
    "..WHHHHHHHHHHS..",
    "...HHHHHHHHHH...",
    "....HHHHHHHH....",
    ".....SSSSSS.....",
    "...TTTTTTTTTT...",
    "..TTTTTTTTTTTT..",
    ".TTTTTTTTTTTTTT.",
    ".TTTtTTTTTTtTTT.",
    "..TTTTTTTTTTTT..",
    "...TTTTTTTTTT...",
]
BACK_ARMS = {"l": [(12, 0), (13, 0), (13, 1), (14, 1)], "r": [(12, 15), (13, 15), (13, 14), (14, 14)]}

# code on the monitor: (indent, [(width, color class)]) in grid units
CODE = [
    (0, [(5, "kw"), (8, "id"), (1, "pn")]),
    (2, [(4, "kw"), (6, "id"), (3, "pn")]),
    (4, [(6, "id"), (1, "pn"), (11, "st"), (1, "pn")]),
    (4, [(3, "kw"), (5, "id"), (2, "pn"), (7, "st")]),
    (2, [(1, "pn")]),
    (2, [(5, "kw"), (9, "id"), (2, "pn")]),
    (4, [(6, "kw"), (12, "id"), (1, "pn")]),
    (2, [(1, "pn")]),
    (0, [(1, "pn")]),
]
CODE_COLORS = {"kw": THEME["accent2"], "id": THEME["text"], "st": THEME["accent"], "pn": THEME["muted"]}

# timeline (seconds)
T_WAVE_END = 3.0
T_WALK_END = 5.8
T_CODE = 6.1
CODE_CYCLE = 7.0

START_X = 40   # where Davi waves
DESK_X = 112   # where the walk ends


def put(grid_rows, pixels, char=None):
    rows = [list(r) for r in grid_rows]
    for p in pixels:
        r, c, ch = p if len(p) == 3 else (*p, char)
        rows[r][c] = ch
    return ["".join(r) for r in rows]


def sprite(rows, x=0, y=0) -> str:
    """Pixel rows -> rects, merging horizontal runs of the same color."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            run = 1
            while c + run < len(row) and row[c + run] == ch:
                run += 1
            if ch != ".":
                out.append(rect(x + c, y + r, run, 1, fill=PALETTE[ch]))
            c += run
    return "".join(out)


def g(children, cls=None, style=None, transform=None) -> str:
    a = "".join(f' {k}="{esc(v)}"' for k, v in (("class", cls), ("style", style), ("transform", transform)) if v)
    return f"<g{a}>{''.join(children)}</g>"


def window(t_on=None, t_off=None) -> str:
    """CSS that shows a group only between t_on and t_off."""
    parts = []
    if t_on is not None:
        parts.append(f"on .01s {t_on:.2f}s both")
    if t_off is not None:
        parts.append(f"off .01s {t_off:.2f}s forwards")
    return "animation:" + ",".join(parts)


def room() -> list[str]:
    t, f = THEME, FLOOR
    out = [
        rect(0, 0, GW, f, fill="#121821"),
        rect(0, f, GW, GH - f, fill="#0b0f15"),
        rect(0, f, GW, 1, fill=t["border"]),
        # neon circuit sign (like the one on the wall in the photo)
        g([
            rect(160, 8, 1, 7, fill=t["accent2"]), rect(160, 8, 8, 1, fill=t["accent2"]),
            rect(167, 8, 1, 4, fill=t["accent2"]), rect(164, 11, 1, 6, fill=t["accent2"]),
            rect(164, 16, 9, 1, fill=t["accent2"]), rect(172, 12, 1, 5, fill=t["accent2"]),
            rect(159, 14, 3, 3, fill=t["accent2"]), rect(166, 11, 3, 3, fill=t["accent2"]),
            rect(171, 11, 3, 3, fill=t["accent2"]),
        ], cls="neon"),
        # plant
        rect(99, f - 6, 7, 6, fill="#5a3b2e"), rect(98, f - 7, 9, 1, fill="#6e4a3a"),
        rect(102, f - 15, 1, 8, fill="#2f6b3a"), rect(99, f - 13, 3, 2, fill="#3fb950"),
        rect(103, f - 12, 3, 2, fill="#2ea043"), rect(100, f - 10, 2, 2, fill="#2ea043"),
        rect(103, f - 16, 2, 2, fill="#3fb950"), rect(104, f - 9, 2, 2, fill="#3fb950"),
        # desk
        rect(108, f - 16, 66, 2, fill="#3a3f4a"), rect(108, f - 14, 66, 1, fill="#262b33"),
        rect(110, f - 13, 2, 13, fill="#262b33"), rect(170, f - 13, 2, 13, fill="#262b33"),
        # monitor
        rect(116, f - 41, 38, 23, fill=t["border"]),
        rect(117, f - 40, 36, 21, fill="#090c10"),
        rect(133, f - 18, 4, 2, fill=t["border"]), rect(129, f - 17, 12, 1, fill=t["border"]),
        # laptop
        rect(158, f - 26, 11, 9, fill="#8b949e"), rect(159, f - 25, 9, 7, fill=t["panel"]),
        rect(156, f - 17, 15, 1, fill="#8b949e"),
        g([rect(160, f - 24, 5, 1, fill=t["accent2"]), rect(162, f - 22, 5, 1, fill=t["muted"]),
           rect(160, f - 20, 4, 1, fill=t["accent2"])], cls="chat"),
    ]
    return out


def code_screen() -> tuple[list[str], str]:
    """Code lines typed on the monitor in a loop; returns elements and their keyframes."""
    x0, y0 = 119, FLOOR - 38
    out, css = [], []
    n = len(CODE)
    for i, (indent, segs) in enumerate(CODE):
        x = x0 + indent
        bars = []
        for w, color in segs:
            bars.append(rect(x, y0 + i * 2, w, 1, fill=CODE_COLORS[color]))
            x += w + 1
        a = i * 0.55 / CODE_CYCLE * 100
        b = (i * 0.55 + 0.4) / CODE_CYCLE * 100
        css.append(f"@keyframes l{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{b:.1f}%,92%{{transform:scaleX(1)}}"
                   f"96%,100%{{transform:scaleX(0)}}}}")
        out.append(g(bars, cls="ln", style=f"animation:l{i} {CODE_CYCLE}s linear {T_CODE}s infinite both"))
    cursor_y = y0 + n * 2
    out.append(rect(x0, cursor_y, 2, 1, fill=THEME["text"], class_="blink"))
    return out, "".join(css)


def waving() -> str:
    base = put(FRONT, [(r, c, ".") for r in (17, 18, 19) for c in (13, 14)])
    base = put(base, WAVE_ARM)
    frames = [g([sprite(put(base, WAVE_HAND[k], "S"))], cls=f"f{k}", style="animation-duration:.6s")
              for k in ("a", "b")]
    return g(frames, cls="st-wave", style=window(None, T_WAVE_END), transform=f"translate({START_X} {FLOOR - 27})")


def walking() -> tuple[str, str]:
    frames = []
    for k in ("a", "b"):
        rows = put(SIDE + SIDE_LEGS[k], SIDE_ARM[k])
        frames.append(g([sprite(rows)], cls=f"f{k}", style="animation-duration:.4s"))
    dist = DESK_X - START_X
    inner = g(frames, style=f"animation:walk {T_WALK_END - T_WAVE_END:.2f}s linear {T_WAVE_END:.2f}s both")
    css_walk = f"@keyframes walk{{from{{transform:translateX(0)}}to{{transform:translateX({dist}px)}}}}"
    return g([inner], cls="st-walk", style=window(T_WAVE_END, T_WALK_END),
             transform=f"translate({START_X + 2} {FLOOR - 26})"), css_walk


def seated() -> str:
    f = FLOOR
    arms = [g([sprite(put(["." * 16] * 15, BACK_ARMS[k], "S"))], cls=f"tap{k}") for k in ("l", "r")]
    person = g([sprite(BACK)] + arms, transform=f"translate(127 {f - 28})")
    chair = [
        rect(129, f - 16, 12, 10, fill="#1f242c"), rect(130, f - 15, 10, 8, fill="#2a303a"),
        rect(126, f - 8, 18, 2, fill="#1f242c"), rect(134, f - 6, 2, 3, fill="#1f242c"),
        rect(128, f - 3, 14, 1, fill="#1f242c"),
        rect(128, f - 2, 2, 2, fill=THEME["dim"]), rect(140, f - 2, 2, 2, fill=THEME["dim"]),
    ]
    return g([person] + chair, cls="st-sit", style=window(T_WALK_END, None))


def bubble() -> str:
    # to the right of the head, tail pointing back at it
    x, y = (START_X + 20) * PX, (FLOOR - 27) * PX - 4
    msg = "hello, world!"
    w = len(msg) * 13 * 0.6 + 22
    t = THEME
    return g([
        f'<path d="M{x} {y + 9}l-9 6l9 3z" fill="{t["panel"]}" stroke="{t["accent"]}"/>',
        rect(x, y, w, 28, rx=4, fill=t["panel"], stroke=t["accent"]),
        rect(x - 0.5, y + 10, 2, 7, fill=t["panel"]),
        text(x + 11, y + 19, msg, "a", font_size=13),
    ], cls="bubble", style=window(0.6, T_WAVE_END - 0.3))


def build(content: dict) -> str:
    ident = content["identity"]
    screen, code_css = code_screen()
    walk, walk_css = walking()
    scene = g(room() + screen + [waving(), walk, seated()], transform=f"scale({PX})")

    head = f"{ident['user']}@{ident['host']}"
    overlay = [
        spans(32, 44, [(head, "a"), (":", "m"), ("~", "b"), ("$ ", "m"), ("./profile", None)], font_size=14),
        text(32, 92, ident["name"].upper(), font_size=32, font_weight=700, letter_spacing=1),
        rect(32, 106, 64, 3, fill=THEME["accent"]),
        *(text(32, 138 + i * 22, line, "m", font_size=15) for i, line in enumerate(ident["headline"])),
        bubble(),
    ]

    css = f"""
svg{{shape-rendering:crispEdges}}text{{shape-rendering:auto}}
@keyframes on{{from{{opacity:0}}to{{opacity:1}}}}@keyframes off{{from,to{{opacity:0}}}}
.fa{{animation:fa .6s step-end infinite}}.fb{{animation:fb .6s step-end infinite}}
@keyframes fa{{50%{{opacity:0}}}}@keyframes fb{{0%{{opacity:0}}50%{{opacity:1}}}}
.tapl{{animation:tap .32s step-end infinite}}.tapr{{animation:tap .32s step-end -.16s infinite}}
@keyframes tap{{50%{{transform:translateY(-1px)}}}}
.ln{{transform-box:fill-box;transform-origin:left}}
.neon{{filter:drop-shadow(0 0 1.2px {THEME['accent2']});animation:pulse 3s ease-in-out infinite}}
.chat{{animation:pulse 2s ease-in-out infinite}}
{walk_css}{code_css}
@media (prefers-reduced-motion:reduce){{.st-wave,.st-walk,.bubble,.fb{{display:none}}}}
"""
    return document(
        W, H,
        title=f"{ident['name']} — {ident['headline'][0]}",
        desc=(f"Pixel-art scene: {ident['name']} waves saying \"hello, world!\", walks to the desk, "
              "sits in front of the monitor and laptop and starts coding. " + " · ".join(ident["headline"])),
        body=f'<clipPath id="frame">{rect(0, 0, W, H, rx=10)}</clipPath>'
             + f'<g clip-path="url(#frame)">{scene}{"".join(overlay)}</g>'
             + rect(0.5, 0.5, W - 1, H - 1, rx=10, fill="none", stroke=THEME["border"]),
        css=css,
    )


if __name__ == "__main__":
    save("hero.svg", build(load_content()))
