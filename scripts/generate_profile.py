"""assets/profile.svg: `whoami` as key/value rows."""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, prompt, save, terminal, text, width_of, wrap

W = 900
ROW = 26
VALUE_X = 140
COLON_X = 118


def rows(entries) -> list[tuple[str, str]]:
    """Flatten entries to (key, line) pairs; the key only on the first line."""
    max_chars = int((W - VALUE_X - PAD) / width_of("x")) - 6  # room for wider fonts
    out = []
    for e in entries:
        v = e["value"]
        if isinstance(v, str):
            lines = [v]
        elif e.get("inline"):
            lines = wrap(v, max_chars)
        else:
            lines = v
        out += [(e["key"] if i == 0 else "", line) for i, line in enumerate(lines)]
    return out


def build(content: dict) -> str:
    ident = content["identity"]
    lines = rows(content["whoami"])
    top = TITLE_BAR + 38
    h = top + 40 + (len(lines) + 1) * ROW + 24

    cmd, t = prompt(PAD, top, "whoami", 0.3, ident)
    body = [cmd]
    t += 0.3
    y = top + 40
    for i, (key, value) in enumerate(lines):
        if key:
            body.append(text(PAD, y, key, "b fade", style=delay(t + i * 0.12)))
            body.append(text(COLON_X, y, ":", "d fade", style=delay(t + i * 0.12)))
        body.append(text(VALUE_X, y, value, "fade", style=delay(t + i * 0.12)))
        y += ROW

    t += len(lines) * 0.12 + 0.2
    body.append(text(PAD, y, "status", "b fade", style=delay(t)))
    body.append(text(COLON_X, y, ":", "d fade", style=delay(t)))
    body.append(
        f'<g class="fade" style="{delay(t)}">'
        f'<circle class="pulse" cx="{VALUE_X + 5}" cy="{y - 5}" r="5" fill="{THEME["accent"]}"/>'
        + text(VALUE_X + 18, y, "online", "a") + "</g>"
    )

    return terminal(
        W, h, "whoami", "".join(body),
        title=f"whoami — {ident['name']}",
        desc="; ".join(f"{k}: {v}" for k, v in lines if k) + "; status: online",
    )


if __name__ == "__main__":
    save("profile.svg", build(load_content()))
