"""assets/stack.svg: `cat stack.yml`, each technology as a chip.

Chips are deliberately all the same: no bars or percentages pretending to measure skill.
Narrow pane, meant to sit next to profile.svg in the README.
"""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, prompt, rect, save, spans, terminal, text, width_of

W = 440
CHIP_X = PAD + 12
CHIP_H = 24
CHIP_GAP = 6
CHIP_SIZE = 12
KEY_SIZE = 14


def layout(content: dict) -> tuple[list[str], int]:
    ident = content["identity"]
    y = TITLE_BAR + 36
    cmd, t = prompt(PAD, y, "cat stack.yml", 0.3, ident)
    body = [cmd]
    t += 0.3

    y += 22
    for group_i, (key, items) in enumerate(content["stack"].items()):
        start = t + group_i * 0.25
        y += 20
        body.append(spans(PAD, y, [(key, "b"), (":", "d")], class_="fade", font_size=KEY_SIZE,
                          style=delay(start)))
        y += 8
        x = CHIP_X
        for i, item in enumerate(items):
            w = width_of(item, CHIP_SIZE) + 18
            if x + w > W - 20:
                x = CHIP_X
                y += CHIP_H + CHIP_GAP
            body.append(
                f'<g class="fade" style="{delay(start + 0.1 + i * 0.04)}">'
                + rect(x, y, round(w, 1), CHIP_H, rx=6, fill=THEME["panel"], stroke=THEME["border"])
                + text(x + 9, y + 16.5, item, font_size=CHIP_SIZE)
                + "</g>"
            )
            x += w + CHIP_GAP
        y += CHIP_H + 6
    return body, y + 18


def build(content: dict, min_h: int = 0) -> str:
    body, h = layout(content)
    groups = content["stack"]
    return terminal(
        W, max(h, min_h), "stack.yml", "".join(body),
        title="Tech stack",
        desc="; ".join(f"{k}: {', '.join(v)}" for k, v in groups.items()),
    )


if __name__ == "__main__":
    import generate_profile
    c = load_content()
    save("stack.svg", build(c, generate_profile.layout(c)[1]))
