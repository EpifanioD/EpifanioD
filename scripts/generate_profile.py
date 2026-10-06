"""assets/profile.svg: `whoami` as key/value rows, then `cat focus.md`.

Narrow pane, meant to sit next to stack.svg in the README.
"""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, prompt, save, terminal, text, width_of, wrap

W = 440
SIZE = 14
ROW = 23
COLON_X = 112
VALUE_X = 126


def rows(entries) -> list[tuple[str, str]]:
    """Flatten entries to (key, line) pairs; the key only on the first line."""
    max_chars = int((W - VALUE_X - 20) / width_of("x", SIZE))
    out = []
    for e in entries:
        v = e["value"]
        items = v.split(" · ") if isinstance(v, str) else v
        lines = wrap(items, max_chars) if isinstance(v, str) or e.get("inline") else items
        out += [(e["key"] if i == 0 else "", line) for i, line in enumerate(lines)]
    return out


def layout(content: dict) -> tuple[list[str], int]:
    ident = content["identity"]
    lines = rows(content["whoami"])
    y = TITLE_BAR + 36
    cmd, t = prompt(PAD, y, "whoami", 0.3, ident)
    body = [cmd]
    t += 0.3
    y += 36
    for i, (key, value) in enumerate(lines + [("status", "")]):
        d = delay(t + i * 0.1)
        if key:
            body.append(text(PAD, y, key, "b fade", font_size=SIZE, style=d))
            body.append(text(COLON_X, y, ":", "d fade", font_size=SIZE, style=d))
        if key == "status":
            body.append(
                f'<g class="fade" style="{d}">'
                f'<circle class="pulse" cx="{VALUE_X + 5}" cy="{y - 5}" r="5" fill="{THEME["accent"]}"/>'
                + text(VALUE_X + 18, y, "online", "a", font_size=SIZE) + "</g>"
            )
        else:
            body.append(text(VALUE_X, y, value, "fade", font_size=SIZE, style=d))
        y += ROW
    t += (len(lines) + 1) * 0.1 + 0.3

    y += 22
    cmd, t = prompt(PAD, y, "cat focus.md", t, ident)
    body.append(cmd)
    y += 34
    indent = width_of("▸ ", SIZE)
    max_chars = int((W - PAD - indent - 20) / width_of("x", SIZE))
    for i, item in enumerate(content["focus"]["items"]):
        d = delay(t + 0.2 + i * 0.12)
        body.append(text(PAD, y, "▸", "a fade", font_size=SIZE, style=d))
        for line in wrap(item.split(" "), max_chars, sep=" "):
            body.append(text(PAD + indent, y, line, "fade", font_size=SIZE, style=d))
            y += ROW - 2
        y += 4
    return body, y + 14


def build(content: dict, min_h: int = 0) -> str:
    body, h = layout(content)
    ident = content["identity"]
    lines = rows(content["whoami"])
    return terminal(
        W, max(h, min_h), "whoami", "".join(body),
        title=f"whoami — {ident['name']}",
        desc="; ".join(f"{k}: {v}" for k, v in lines if k) + "; status: online. Current focus: "
             + "; ".join(content["focus"]["items"]) + ".",
    )


if __name__ == "__main__":
    import generate_stack
    c = load_content()
    save("profile.svg", build(c, generate_stack.layout(c)[1]))
