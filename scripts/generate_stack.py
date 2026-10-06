"""assets/stack.svg: `cat stack.yml`, each technology as a chip.

Chips are deliberately all the same: no bars or percentages pretending to measure skill.
"""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, prompt, rect, save, spans, terminal, text, width_of

W = 900
CHIP_X = 170
CHIP_H = 26
CHIP_GAP = 8
CHIP_SIZE = 13
ROW_GAP = 14


def build(content: dict) -> str:
    ident = content["identity"]
    top = TITLE_BAR + 38
    cmd, t = prompt(PAD, top, "cat stack.yml", 0.3, ident)
    body = [cmd]
    t += 0.3

    y = top + 30
    for group_i, (key, items) in enumerate(content["stack"].items()):
        start = t + group_i * 0.25
        body.append(spans(PAD, y + 18, [(key, "b"), (":", "d")], class_="fade", style=delay(start)))
        x = CHIP_X
        for i, item in enumerate(items):
            w = width_of(item, CHIP_SIZE) + 22
            if x + w > W - PAD:
                x = CHIP_X
                y += CHIP_H + CHIP_GAP
            body.append(
                f'<g class="fade" style="{delay(start + 0.1 + i * 0.04)}">'
                + rect(x, y, w, CHIP_H, rx=6, fill=THEME["panel"], stroke=THEME["border"])
                + text(x + 11, y + 17.5, item, font_size=CHIP_SIZE)
                + "</g>"
            )
            x += w + CHIP_GAP
        y += CHIP_H + ROW_GAP

    groups = content["stack"]
    return terminal(
        W, y + 16, "stack.yml", "".join(body),
        title="Tech stack",
        desc="; ".join(f"{k}: {', '.join(v)}" for k, v in groups.items()),
    )


if __name__ == "__main__":
    save("stack.svg", build(load_content()))
