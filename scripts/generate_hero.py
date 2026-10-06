"""assets/hero.svg: pixel-art scene, played in a loop.

Davi opens the door, waves, walks to the desk and sits down; the PC turns on and code
gets typed next to a steaming coffee. After a while the PC turns off, Davi walks back,
waves goodbye and leaves. The room stays empty for a moment and the story restarts.

The scene is drawn on a grid (1 unit = PX screen pixels). Sprites are strings where each
character is a palette color and "." is transparent. Every moving part follows a CSS
keyframe track over the same CYCLE, so the whole story loops in sync.
"""
from svg import THEME, document, esc, load_content, rect, save, spans, text

W, H = 900, 360
PX = 5                      # screen pixels per grid unit
GW, GH = W // PX, H // PX   # 180 x 72 grid
FLOOR = 64
CYCLE = 28.0                # seconds for the whole story

# story timeline (seconds)
DOOR_OPEN_IN = (0.6, 3.6)
WAVE_IN = (1.0, 3.2)
HELLO = (1.2, 3.2)
WALK_IN = (3.2, 6.2)
SEATED = (6.2, 19.0)
PC_ON = (6.6, 18.6)
WALK_OUT = (19.0, 22.0)
DOOR_OPEN_OUT = (21.6, 24.2)
WAVE_OUT = (22.0, 23.6)
BYE = (22.2, 23.6)

DOOR_X = 158   # where Davi enters and leaves
SEAT_X = 104   # where the walk ends, next to the chair

PALETTE = {
    "H": "#0e0e10", "h": "#3a3a44",   # black hair, highlight / rim light
    "S": "#f0c9b0", "s": "#d9a88e",   # light skin, shade
    "E": "#1a1412", "M": "#8a4a3c",   # eyes, mouth
    "T": "#3d4250", "t": "#2d313b",   # dark grey t-shirt
    "P": "#2b3a55", "B": "#d0d7de",   # jeans, sneakers
    "G": "#8fb573", "O": "#b08a5a", "o": "#8a6a42",   # Grogu: skin, robe
    "K": "#111111",                                   # Grogu's eyes
}

FRONT = [
    "......hhhhhh......",
    ".....HHHHHHHH.....",
    "....HHHHHHHHHH....",
    "....HHHHHHHHHH....",
    "....HSSSSSSSSH....",
    "....SSSSSSSSSS....",
    "...sSSESSSSESSs...",
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
# raised left arm (on the open side of the door) and two hand positions
WAVE_ARM = [(15, 3, "T"), (14, 3, "T"), (14, 2, "T"), (13, 2, "S"), (12, 2, "S"), (12, 1, "S"),
            (11, 1, "S"), (10, 1, "S")]
WAVE_HAND = {
    "a": [(9, 1), (9, 0), (8, 1), (8, 0), (7, 1), (7, 0)],
    "b": [(9, 2), (9, 1), (8, 2), (8, 3), (7, 3), (7, 2)],
}

SIDE = [  # facing right
    "....hhhhh.....",
    "...HHHHHHHH...",
    "..HHHHHHHHHH..",
    "..HHHHHHHHHH..",
    "..HHHHHSSSSS..",
    "..HHHSSSSSES..",
    "..HsSSSSSSSSS.",
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
    ".....hhhhhh.....",  # rim-lit outline keeps the black hair visible against the screen
    "....hHHHHHHh....",
    "...hHHHHHHHHh...",
    "...hHHHHHHHHh...",
    "...hHHHHHHHHh...",
    "..ShHHHHHHHHhS..",
    "...hHHHHHHHHh...",
    "....hHHHHHHh....",
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
CODE_LOOP = 6.0


# ---- drawing helpers -------------------------------------------------------

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
            ch, run = row[c], 1
            while c + run < len(row) and row[c + run] == ch:
                run += 1
            if ch != ".":
                out.append(rect(x + c, y + r, run, 1, fill=PALETTE[ch]))
            c += run
    return "".join(out)


def g(children, cls=None, style=None, transform=None) -> str:
    a = "".join(f' {k}="{esc(v)}"' for k, v in (("class", cls), ("style", style), ("transform", transform)) if v)
    return f"<g{a}>{''.join(children)}</g>"


def pct(t: float) -> str:
    return f"{t / CYCLE * 100:.2f}%"


class Tracks:
    """Collects CSS keyframes that all loop over CYCLE."""

    def __init__(self):
        self.css = []

    def visible(self, name, *windows) -> str:
        """Opacity 1 inside the (start, end) windows, 0 elsewhere."""
        frames = ["0%{opacity:0}"]
        for start, end in windows:
            frames += [f"{pct(start)}{{opacity:1}}", f"{pct(end)}{{opacity:0}}"]
        frames.append("100%{opacity:0}")
        self.css.append(f"@keyframes {name}{{{''.join(frames)}}}")
        return f"animation:{name} {CYCLE}s step-end infinite"

    def move(self, name, start, end, dx) -> str:
        """translateX from 0 to dx between start and end."""
        self.css.append(
            f"@keyframes {name}{{0%,{pct(start)}{{transform:translateX(0)}}"
            f"{pct(end)},100%{{transform:translateX({dx}px)}}}}"
        )
        return f"animation:{name} {CYCLE}s linear infinite"


# ---- scene parts -----------------------------------------------------------

def room() -> list[str]:
    t, f = THEME, FLOOR
    shelf = bookshelf(6, f)
    return [
        rect(0, 0, GW, f, fill="#121821"),
        rect(0, f, GW, GH - f, fill="#0b0f15"),
        rect(0, f, GW, 1, fill=t["border"]),
        *shelf,
        # neon circuit sign (like the one on the wall in the photo)
        g([
            rect(160, 8, 1, 7, fill=t["accent2"]), rect(160, 8, 8, 1, fill=t["accent2"]),
            rect(167, 8, 1, 4, fill=t["accent2"]), rect(164, 11, 1, 6, fill=t["accent2"]),
            rect(164, 16, 9, 1, fill=t["accent2"]), rect(172, 12, 1, 5, fill=t["accent2"]),
            rect(159, 14, 3, 3, fill=t["accent2"]), rect(166, 11, 3, 3, fill=t["accent2"]),
            rect(171, 11, 3, 3, fill=t["accent2"]),
        ], cls="neon"),
        *lightsaber(101, 16),  # on the wall above the monitor
        # plant
        rect(77, f - 6, 7, 6, fill="#5a3b2e"), rect(76, f - 7, 9, 1, fill="#6e4a3a"),
        rect(80, f - 15, 1, 8, fill="#2f6b3a"), rect(77, f - 13, 3, 2, fill="#3fb950"),
        rect(81, f - 12, 3, 2, fill="#2ea043"), rect(78, f - 10, 2, 2, fill="#2ea043"),
        rect(81, f - 16, 2, 2, fill="#3fb950"), rect(82, f - 9, 2, 2, fill="#3fb950"),
        # desk
        rect(89, f - 16, 64, 2, fill="#3a3f4a"), rect(89, f - 14, 64, 1, fill="#262b33"),
        rect(91, f - 13, 2, 13, fill="#262b33"), rect(149, f - 13, 2, 13, fill="#262b33"),
        # monitor (off screen) and laptop
        rect(97, f - 41, 38, 23, fill=t["border"]), rect(98, f - 40, 36, 21, fill="#090c10"),
        rect(114, f - 18, 4, 2, fill=t["border"]), rect(110, f - 17, 12, 1, fill=t["border"]),
        rect(138, f - 26, 11, 9, fill="#8b949e"), rect(139, f - 25, 9, 7, fill=t["panel"]),
        rect(136, f - 17, 15, 1, fill="#8b949e"),
    ]


GROGU = [
    "GG.....GG",
    ".GGGGGGG.",
    "..GKGKG..",
    "...GGG...",
    "..oOOOo..",
    "..OOOOO..",
    "..OOOOO..",
]
MANGA_COLORS = ["#e5534b", "#f0b72f", "#3fb950", "#79c0ff", "#d2a8ff", "#f778ba", "#ffa657"]
TECH_BOOKS = [  # (title, width, spine, text), top to bottom
    ("CLEAN CODE", 20, "#3d444d", "#e6edf3"),
    ("CLEAN ARCHITECTURE", 23, "#2d333b", "#f0b72f"),
    ("DOMAIN-DRIVEN DESIGN", 25, "#1d4f91", "#e6edf3"),
]


def label(x, y, s, size, color, width) -> str:
    """Small sans-serif title squeezed to an exact width (fonts differ between visitors)."""
    return (f'<text x="{x}" y="{y}" textLength="{width}" lengthAdjust="spacingAndGlyphs" '
            f'style="font-family:Arial,Helvetica,sans-serif;font-size:{size}px;font-weight:700;fill:{color}">'
            f"{esc(s)}</text>")


def pokeball(cx, cy, r) -> str:
    """Drawn with vector shapes: at this size pixels can't make the band and button read."""
    return (
        f'<g style="shape-rendering:auto">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e6edf3"/>'
        f'<path d="M{cx - r} {cy}a{r} {r} 0 0 1 {2 * r} 0z" fill="#e5534b"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0b0f15" stroke-width=".35"/>'
        f'<rect x="{cx - r}" y="{cy - 0.25}" width="{2 * r}" height=".5" fill="#0b0f15"/>'
        f'<circle cx="{cx}" cy="{cy}" r=".85" fill="#e6edf3" stroke="#0b0f15" stroke-width=".35"/>'
        "</g>"
    )


def bookshelf(x, f) -> list[str]:
    """Three shelves: manga + Grogu, engineering books + Rubik's cube, Catan + Pokéball."""
    out = [rect(x, f - 26, 40, 26, fill="#1c222b"), rect(x + 1, f - 25, 38, 24, fill="#151a22"),
           rect(x, f - 17, 40, 1, fill="#2a313c"), rect(x, f - 8, 40, 1, fill="#2a313c")]

    # top: a manga collection, same design on every spine, then Grogu
    for i in range(11):
        mx = x + 2 + i * 2
        out += [rect(mx, f - 24, 1.7, 7, fill="#dfe3e8"), rect(mx, f - 24, 1.7, 2, fill=MANGA_COLORS[i % 7]),
                rect(mx + 0.4, f - 19, 0.9, 0.6, fill="#30363d")]  # volume number
    out.append(sprite(GROGU, x + 28, f - 24))

    # middle: the engineering books lying down, titles readable, and a Rubik's cube
    y = f - 15.8
    for title, w, spine, ink in TECH_BOOKS:
        bx = x + 2 + (25 - w) // 2
        out += [rect(bx, y, w, 2.5, fill=spine), rect(bx, y + 2.4, w, 0.1, fill="#0b0f15"),
                label(bx + 1, y + 1.85, title, 1.7, ink, w - 2)]
        y += 2.6
    cube = [["#e5534b", "#f0b72f", "#3fb950"], ["#79c0ff", "#e6edf3", "#ffa657"], ["#3fb950", "#e5534b", "#79c0ff"]]
    cx, cy = x + 29, f - 13
    out.append(rect(cx, cy, 5, 5, fill="#0b0f15"))
    out += [rect(cx + 0.5 + c * 1.4, cy + 0.5 + r * 1.4, 1.2, 1.2, fill=cube[r][c]) for r in range(3) for c in range(3)]
    out += [rect(x + 35, f - 15, 2, 7, fill="#2f6b3a"), rect(x + 37, f - 14, 2, 6, fill="#6e4a3a")]

    # bottom: Catan, a Pokéball and a few more books
    out += catan(x + 2, f - 5)
    out.append(pokeball(x + 22, f - 3.6, 2.6))
    out += [rect(x + 26, f - 7, 3, 6, fill="#4a3b35"), rect(x + 29, f - 6, 3, 5, fill="#2b3a55"),
            rect(x + 32, f - 7, 3, 6, fill="#3d4250"), rect(x + 35, f - 6, 3, 5, fill="#5a3b2e")]
    return out


def catan(x, y) -> list[str]:
    """The Catan box lying on the shelf, book-sized, spine facing out: red, yellow serif title."""
    return [
        rect(x, y, 15, 4, fill="#b3261e"),
        rect(x, y, 15, 0.6, fill="#d0453a"),              # lit top edge
        rect(x, y + 3.4, 15, 0.6, fill="#5e8c3a"),        # hills from the cover art
        # inline style: the global `text` CSS rule would otherwise win over attributes
        f'<text x="{x + 7.5}" y="{y + 2.9}" text-anchor="middle" style="font-family:Georgia,\'Times New Roman\',serif;'
        f'font-size:3px;font-weight:700;letter-spacing:.1px;fill:#f6c945;stroke:#3a1a0a;stroke-width:.25px;'
        f'paint-order:stroke">CATAN</text>',
    ]


def lightsaber(x, y) -> list[str]:
    """A lightsaber on a wall mount, blade glowing."""
    t = THEME
    return [
        rect(x + 1, y + 1, 2, 2, fill="#30363d"), rect(x + 26, y + 1, 2, 2, fill="#30363d"),  # brackets
        rect(x, y, 7, 2, fill="#8b949e"), rect(x + 1, y, 1, 2, fill="#30363d"),               # hilt
        rect(x + 3, y, 1, 2, fill="#30363d"), rect(x + 5, y, 1, 1, fill="#f85149"),
        rect(x + 7, y, 2, 2, fill="#c9d1d9"),                                                  # emitter
        g([rect(x + 9, y, 22, 2, fill=t["accent2"]), rect(x + 9, y + 0.5, 21.5, 1, fill="#e6f3ff")],
          cls="saber"),
    ]


def coffee() -> list[str]:
    f = FLOOR
    mug = [rect(92, f - 21, 4, 5, fill="#d0d7de"), rect(93, f - 21, 2, 1, fill="#6f4e37"),
           rect(91, f - 20, 1, 3, fill="#d0d7de")]
    # wisps rising from the cup, each a tiny zig-zag starting at a different moment
    steam = [
        g([rect(x, f - 23, 1, 1, fill="#c9d1d9"), rect(x + 1, f - 24, 1, 1, fill="#c9d1d9"),
           rect(x, f - 25, 1, 1, fill="#c9d1d9")], cls="steam", style=f"animation-delay:{d}s")
        for x, d in ((92, 0), (94, 0.8), (93, 1.6))
    ]
    return mug + steam


def screen(tracks: Tracks) -> str:
    """Monitor and laptop contents, visible only while the PC is on."""
    x0, y0 = 100, FLOOR - 38
    parts, f = [], FLOOR
    for i, (indent, segs) in enumerate(CODE):
        x, bars = x0 + indent, []
        for w, color in segs:
            bars.append(rect(x, y0 + i * 2, w, 1, fill=CODE_COLORS[color]))
            x += w + 1
        a = i * 0.5 / CODE_LOOP * 100
        b = (i * 0.5 + 0.35) / CODE_LOOP * 100
        tracks.css.append(f"@keyframes l{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{b:.1f}%,92%{{transform:scaleX(1)}}"
                          f"96%,100%{{transform:scaleX(0)}}}}")
        parts.append(g(bars, cls="ln", style=f"animation:l{i} {CODE_LOOP}s linear infinite both"))
    parts.append(rect(x0, y0 + len(CODE) * 2, 2, 1, fill=THEME["text"], class_="blink"))
    parts += [
        rect(133, f - 19, 1, 1, fill=THEME["accent"]),  # power led
        rect(140, f - 24, 5, 1, fill=THEME["accent2"]), rect(142, f - 22, 5, 1, fill=THEME["muted"]),
        rect(140, f - 20, 4, 1, fill=THEME["accent2"]),
    ]
    return g(parts, cls="pc", style=tracks.visible("pc", PC_ON))


def door(tracks: Tracks) -> list[str]:
    f, x = FLOOR, DOOR_X
    frame = rect(x - 1, f - 35, 21, 35, fill="#1c222b")
    closed = g([
        rect(x, f - 34, 19, 34, fill="#2a2f38"),
        rect(x + 2, f - 32, 15, 13, fill="#242931"), rect(x + 2, f - 16, 15, 14, fill="#242931"),
        rect(x + 3, f - 18, 2, 2, fill="#d29922"),
    ])
    opened = g([
        rect(x, f - 34, 19, 34, fill="#06080b"),
        rect(x + 16, f - 34, 3, 34, fill="#2a2f38"), rect(x + 16, f - 18, 1, 2, fill="#d29922"),
    ], cls="door-open", style=tracks.visible("door", DOOR_OPEN_IN, DOOR_OPEN_OUT))
    return [frame, closed, opened]


def front_wave(tracks: Tracks, name, window) -> str:
    base = put(FRONT, [(r, c, ".") for r in (17, 18, 19) for c in (3, 4)])
    base = put(base, WAVE_ARM)
    frames = [g([sprite(put(base, WAVE_HAND[k], "S"))], cls=f"f{k}", style="animation-duration:.6s")
              for k in ("a", "b")]
    return g([g(frames, transform=f"translate({DOOR_X} {FLOOR - 27})")], cls="away",
             style=tracks.visible(name, window))


def walk(tracks: Tracks, name, window, x_from, x_to) -> str:
    facing_left = x_to < x_from
    frames = []
    for k in ("a", "b"):
        rows = put(SIDE + SIDE_LEGS[k], SIDE_ARM[k])
        frames.append(g([sprite(rows)], cls=f"f{k}", style="animation-duration:.4s"))
    body = g(frames, transform="translate(14 0) scale(-1 1)" if facing_left else None)
    mover = g([body], style=tracks.move(f"{name}m", *window, x_to - x_from))
    return g([g([mover], transform=f"translate({x_from} {FLOOR - 26})")], cls="away",
             style=tracks.visible(name, window))


def seated(tracks: Tracks) -> str:
    f = FLOOR
    arms = [g([sprite(put(["." * 16] * 15, BACK_ARMS[k], "S"))], cls=f"tap{k}") for k in ("l", "r")]
    person = g([sprite(BACK)] + arms, transform=f"translate(108 {f - 28})")
    return g([person], cls="seated", style=tracks.visible("seated", SEATED))


def chair() -> list[str]:
    f = FLOOR
    return [
        rect(110, f - 16, 12, 10, fill="#1f242c"), rect(111, f - 15, 10, 8, fill="#2a303a"),
        rect(107, f - 8, 18, 2, fill="#1f242c"), rect(115, f - 6, 2, 3, fill="#1f242c"),
        rect(109, f - 3, 14, 1, fill="#1f242c"),
        rect(109, f - 2, 2, 2, fill=THEME["dim"]), rect(121, f - 2, 2, 2, fill=THEME["dim"]),
    ]


def bubble(tracks: Tracks, name, window, msg) -> str:
    """Speech bubble above the doorway, tail pointing down at the head."""
    t = THEME
    w = len(msg) * 13 * 0.6 + 22
    x, y = W - 18 - w, (FLOOR - 27) * PX - 42
    tail_x = (DOOR_X + 9) * PX
    return g([
        f'<path d="M{tail_x - 6} {y + 27}l2 10l8 -10z" fill="{t["panel"]}" stroke="{t["accent"]}"/>',
        rect(x, y, w, 28, rx=4, fill=t["panel"], stroke=t["accent"]),
        rect(tail_x - 5, y + 26, 8, 3, fill=t["panel"]),
        text(x + 11, y + 19, msg, "a", font_size=13),
    ], cls="bubble", style=tracks.visible(name, window))


def build(content: dict) -> str:
    ident = content["identity"]
    tr = Tracks()
    scene = g(
        room() + coffee() + [screen(tr)] + door(tr) + [
            front_wave(tr, "hi", WAVE_IN),
            walk(tr, "win", WALK_IN, DOOR_X + 2, SEAT_X),
            seated(tr),
            walk(tr, "wout", WALK_OUT, SEAT_X, DOOR_X + 2),
            front_wave(tr, "bye", WAVE_OUT),
        ] + chair(),
        transform=f"scale({PX})",
    )

    head = f"{ident['user']}@{ident['host']}"
    overlay = [
        spans(32, 44, [(head, "a"), (":", "m"), ("~", "b"), ("$ ", "m"), ("./profile", None)], font_size=14),
        text(32, 92, ident["name"].upper(), font_size=32, font_weight=700, letter_spacing=1),
        rect(32, 106, 64, 3, fill=THEME["accent"]),
        *(text(32, 138 + i * 22, line, "m", font_size=15) for i, line in enumerate(ident["headline"])),
        bubble(tr, "hello", HELLO, "hello, world!"),
        bubble(tr, "seeyou", BYE, "see you!"),
    ]

    css = f"""
svg{{shape-rendering:crispEdges}}
.fa{{animation:fa .6s step-end infinite}}.fb{{animation:fb .6s step-end infinite}}
@keyframes fa{{50%{{opacity:0}}}}@keyframes fb{{0%{{opacity:0}}50%{{opacity:1}}}}
.tapl{{animation:tap .32s step-end infinite}}.tapr{{animation:tap .32s step-end -.16s infinite}}
@keyframes tap{{50%{{transform:translateY(-1px)}}}}
.ln{{transform-box:fill-box;transform-origin:left}}
.saber{{filter:drop-shadow(0 0 1px {THEME['accent2']}) drop-shadow(0 0 2px #1f6feb);animation:hum 1.8s steps(6) infinite}}
@keyframes hum{{0%,100%{{opacity:1}}40%{{opacity:.85}}55%{{opacity:1}}80%{{opacity:.92}}}}
.neon{{filter:drop-shadow(0 0 1.2px {THEME['accent2']});animation:pulse 3s ease-in-out infinite}}
.steam{{animation:steam 2.4s ease-out infinite both}}
@keyframes steam{{0%{{transform:translateY(0);opacity:0}}25%{{opacity:.9}}100%{{transform:translateY(-7px);opacity:0}}}}
{''.join(tr.css)}
@media (prefers-reduced-motion:reduce){{.away,.bubble,.door-open,.fb{{display:none}}}}
"""
    return document(
        W, H,
        title=f"{ident['name']} — {ident['headline'][0]}",
        desc=(f"Pixel-art scene in a loop: {ident['name']} opens the door, waves saying \"hello, world!\", "
              "walks to the desk and codes next to a steaming coffee, then turns the PC off, "
              "waves \"see you!\" and leaves. " + " · ".join(ident["headline"])),
        body=f'<clipPath id="frame">{rect(0, 0, W, H, rx=10)}</clipPath>'
             + f'<g clip-path="url(#frame)">{scene}{"".join(overlay)}</g>'
             + rect(0.5, 0.5, W - 1, H - 1, rx=10, fill="none", stroke=THEME["border"]),
        css=css,
    )


if __name__ == "__main__":
    save("hero.svg", build(load_content()))
