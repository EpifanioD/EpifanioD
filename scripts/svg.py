"""Small helpers to compose animated SVGs with plain strings.

Animations use CSS inside the SVG (no JavaScript), which GitHub keeps when
the file is rendered as an image in a README.
"""
from __future__ import annotations

import tomllib
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CONTENT = ROOT / "content" / "profile.toml"

THEME = {
    "bg": "#0d1117",
    "panel": "#161b22",
    "border": "#30363d",
    "text": "#e6edf3",
    "muted": "#8b949e",
    "dim": "#484f58",
    "accent": "#3fb950",
    "accent2": "#79c0ff",
}

# External fonts cannot load inside an <img>, so rely on common system monospace fonts.
FONT = ("'JetBrains Mono','Fira Code','SF Mono',Menlo,'Cascadia Mono',"
        "'DejaVu Sans Mono',Consolas,'Liberation Mono',monospace")
CHAR_W = 0.6  # average advance of the fonts above, in em

TITLE_BAR = 36
PAD = 32

CSS = f"""
text{{font-family:{FONT};fill:{THEME['text']}}}
.m{{fill:{THEME['muted']}}}.d{{fill:{THEME['dim']}}}.a{{fill:{THEME['accent']}}}.b{{fill:{THEME['accent2']}}}
.fade{{animation:fade .6s ease-out both}}
.cover{{transform-box:fill-box;transform-origin:right}}
.blink{{animation:blink 1.1s step-end infinite}}
.draw{{stroke-dasharray:1;stroke-dashoffset:0;animation:draw .9s ease-in-out both}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes type{{from{{transform:scaleX(1)}}to{{transform:scaleX(0)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes pulse{{50%{{opacity:.35}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.cover,.motion{{display:none}}}}
"""


def load_content() -> dict:
    with CONTENT.open("rb") as f:
        return tomllib.load(f)


def esc(value) -> str:
    return escape(str(value), {'"': "&quot;"})


def attrs(**kw) -> str:
    """Python kwargs -> SVG attributes (class_ -> class, font_size -> font-size)."""
    return " ".join(
        f'{k.rstrip("_").replace("_", "-")}="{esc(v)}"' for k, v in kw.items() if v is not None
    )


def width_of(s: str, size: float = 15) -> float:
    return len(s) * size * CHAR_W


def delay(seconds: float) -> str:
    return f"animation-delay:{seconds:.2f}s"


def text(x, y, s, cls=None, **kw) -> str:
    return f"<text {attrs(x=x, y=y, class_=cls, **kw)}>{esc(s)}</text>"


def spans(x, y, parts, **kw) -> str:
    """One <text> made of (string, css class) parts."""
    inner = "".join(f'<tspan {attrs(class_=c)}>{esc(s)}</tspan>' for s, c in parts)
    return f"<text {attrs(x=x, y=y, **kw)}>{inner}</text>"


def rect(x, y, w, h, **kw) -> str:
    return f"<rect {attrs(x=x, y=y, width=w, height=h, **kw)}/>"


def path(d, **kw) -> str:
    return f"<path {attrs(d=d, **kw)}/>"


def group(children, **kw) -> str:
    return f"<g {attrs(**kw)}>{''.join(children)}</g>"


def typed(x, y, s, start, size=15, cls=None, bg=THEME["bg"], cps=16) -> tuple[str, float]:
    """Text revealed char by char by a background-colored cover that shrinks to the right.

    Returns the SVG and the moment the typing ends.
    """
    dur = max(len(s) / cps, 0.2)
    cover = rect(
        round(x - 2, 1), round(y - size, 1), round(width_of(s, size) + size, 1), round(size * 1.45, 1),
        fill=bg, class_="cover",
        style=f"animation:type {dur:.2f}s steps({len(s)}) {start:.2f}s both",
    )
    return text(x, y, s, cls, font_size=size) + cover, start + dur


def prompt(x, y, cmd, start, ident) -> tuple[str, float]:
    """`davi@github:~$ cmd`, typing the command."""
    head = f"{ident['user']}@{ident['host']}"
    p = spans(x, y, [(head, "a"), (":", "m"), ("~", "b"), ("$ ", "m")])
    body, end = typed(x + width_of(head + ":~$ "), y, cmd, start)
    return p + body, end


def document(w, h, title, desc, body, css="") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-size="15" role="img" aria-labelledby="title desc">'
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>'
        f"<style>{CSS}{css}</style>{body}</svg>"
    )


def terminal(w, h, window_title, body, title, desc, css="") -> str:
    """A dark terminal window with a title bar; `body` is drawn below it."""
    t = THEME
    chrome = [
        '<clipPath id="win">' + rect(0, 0, w, h, rx=10) + "</clipPath>",
        group([
            rect(0, 0, w, h, fill=t["bg"]),
            rect(0, 0, w, TITLE_BAR, fill=t["panel"]),
            path(f"M0 {TITLE_BAR}H{w}", stroke=t["border"]),
        ], clip_path="url(#win)"),
        rect(0.5, 0.5, w - 1, h - 1, rx=10, fill="none", stroke=t["border"]),
        *(f'<circle cx="{20 + i * 18}" cy="{TITLE_BAR / 2}" r="5.5" fill="{t["dim"]}"/>' for i in range(3)),
        text(w / 2, TITLE_BAR / 2 + 4, window_title, "m", font_size=12, text_anchor="middle"),
    ]
    return document(w, h, title, desc, "".join(chrome) + body, css)


def wrap(items, max_chars, sep=" · ") -> list[str]:
    lines, cur = [], ""
    for item in items:
        nxt = f"{cur}{sep}{item}" if cur else item
        if cur and len(nxt) > max_chars:
            lines.append(cur)
            cur = item
        else:
            cur = nxt
    return lines + [cur] if cur else lines


def save(name: str, svg: str) -> Path:
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / name
    out.write_text(svg + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1024:.1f} KB)")
    return out
