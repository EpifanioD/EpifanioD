"""assets/architecture.svg: a layered system diagram whose connections draw themselves."""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, path, prompt, rect, save, spans, terminal, text, wrap

W, H = 900, 470
CX = 296  # center of the diagram column
NODE_H = 52

# (center x, top y, width, label, subtitle, highlighted)
NODES = {
    "client": (CX, 96, 220, "SPA · Mobile", "clients", False),
    "api": (CX, 186, 220, "REST API", "interface · MVC", False),
    "app": (CX, 276, 220, "Application", "use cases", False),
    "domain": (131, 376, 150, "Domain", "DDD · entities", True),
    "data": (296, 376, 150, "Data", "repositories · SQL", False),
    "events": (461, 376, 150, "Events", "event-driven", False),
}
EDGES = [
    "M296 148V186",
    "M296 238V276",
    "M296 328V352H131V376",
    "M296 328V376",
    "M296 328V352H461V376",
]
BOUNDARY = (40, 172, 512, 270)
# packets travelling a request from the client down to the domain / events layers
PACKETS = [("M296 148V352H131V376", 4.2), ("M296 148V352H461V376", 5.8)]


def node(key, start) -> str:
    cx, y, w, label, sub, hot = NODES[key]
    t = THEME
    return (
        f'<g class="fade" style="{delay(start)}">'
        + rect(cx - w / 2, y, w, NODE_H, rx=8, fill=t["panel"], stroke=t["accent"] if hot else t["border"])
        + text(cx, y + 23, label, font_weight=700, text_anchor="middle")
        + text(cx, y + 41, sub, "m", font_size=12, text_anchor="middle")
        + "</g>"
    )


def edge(d, start) -> str:
    return path(d, pathLength=1, fill="none", stroke=THEME["muted"], stroke_width=1.5,
                class_="draw", style=delay(start))


def packet(d, begin) -> str:
    return (
        f'<circle class="motion" r="3.5" fill="{THEME["accent"]}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{begin}s"/>'
        f'<animateMotion path="{d}" dur="2.6s" begin="{begin}s" repeatCount="indefinite"/>'
        "</circle>"
    )


def bullet_list(x, y, heading, items, start) -> tuple[list[str], float]:
    out = [text(x, y, heading, "b fade", style=delay(start))]
    for i, item in enumerate(items):
        y += 26
        out.append(spans(x, y, [("▸ ", "a"), (item, None)], class_="fade", style=delay(start + 0.1 + i * 0.12)))
    return out, y


def build(content: dict) -> str:
    ident, arch = content["identity"], content["architecture"]
    top = TITLE_BAR + 38
    cmd, t = prompt(PAD, top, "./architecture --describe", 0.3, ident)

    # packets go first so the boxes hide them: they only show while on an edge
    body = [cmd] + [packet(d, b) for d, b in PACKETS]

    t += 0.2
    body.append(node("client", t))
    body.append(edge(EDGES[0], t + 0.3))
    body.append(node("api", t + 0.7))
    body.append(edge(EDGES[1], t + 1.0))
    body.append(node("app", t + 1.4))
    for e in EDGES[2:]:
        body.append(edge(e, t + 1.7))
    for i, key in enumerate(("domain", "data", "events")):
        body.append(node(key, t + 2.3 + i * 0.15))

    bx, by, bw, bh = BOUNDARY
    body.append(rect(bx, by, bw, bh, rx=12, fill="none", stroke=THEME["dim"], stroke_dasharray="4 5",
                     class_="fade", style=delay(t + 2.9)))
    body.append(text(bx + bw - 10, by - 8, "clean architecture", "m fade", font_size=12,
                     text_anchor="end", style=delay(t + 2.9)))

    # right column: how it ships and the principles behind it
    col = 610
    body.append(path(f"M580 {TITLE_BAR + 60}V{H - 30}", stroke=THEME["border"], class_="fade", style=delay(t)))
    styles, y = bullet_list(col, 120, "styles:", arch["styles"], t + 0.4)
    principles, y = bullet_list(col, y + 44, "principles:", arch["principles"], t + 1.2)
    body += styles + principles
    for i, line in enumerate(wrap(arch["motto"].split(" "), 26, sep=" ")):
        body.append(text(col, y + 50 + i * 20, ("# " if i == 0 else "  ") + line, "d fade",
                         font_size=13, style=delay(t + 3.2)))

    labels = [n[3] for n in NODES.values()]
    return terminal(
        W, H, "architecture", "".join(body),
        title="Software architecture",
        desc=("Layered diagram: " + " → ".join(labels) + ". Styles: " + ", ".join(arch["styles"])
              + ". Principles: " + ", ".join(arch["principles"]) + "."),
    )


if __name__ == "__main__":
    save("architecture.svg", build(load_content()))
