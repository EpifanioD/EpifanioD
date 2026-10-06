"""assets/hero.svg: the profile "boots" in a terminal."""
from svg import PAD, THEME, TITLE_BAR, delay, load_content, prompt, rect, save, spans, terminal, text, width_of

W, H = 900, 340


def build(content: dict) -> str:
    ident = content["identity"]
    y = TITLE_BAR + 38
    cmd, t = prompt(PAD, y, "./profile", 0.4, ident)
    body = [cmd]

    t += 0.3
    body.append(text(PAD, y + 28, "initializing profile...", "m fade", style=delay(t)))

    # left column: name and headline
    t += 0.5
    body.append(text(PAD, 170, ident["name"].upper(), "fade", font_size=34, font_weight=700,
                     letter_spacing=1, style=delay(t)))
    body.append(rect(PAD, 186, 64, 3, fill=THEME["accent"], class_="fade", style=delay(t + 0.2)))
    for i, line in enumerate(ident["headline"]):
        body.append(text(PAD, 220 + i * 24, line, "m fade", font_size=16, style=delay(t + 0.4 + i * 0.2)))

    # right column: boot checklist
    col = 590
    for i, item in enumerate(ident["boot"]):
        body.append(spans(col, 128 + i * 24, [("[", "d"), ("✓", "a"), ("] ", "d"), (item, None)],
                          class_="fade", style=delay(t + 0.2 + i * 0.18)))
    t += 0.2 + len(ident["boot"]) * 0.18 + 0.2

    body.append(spans(PAD, 290, [("● ", "a"), ("system ready", "m")], class_="fade", style=delay(t)))

    # final prompt with blinking cursor
    t += 0.4
    head = f"{ident['user']}@{ident['host']}:~$ "
    last = spans(PAD, H - 20, [(f"{ident['user']}@{ident['host']}", "a"), (":", "m"), ("~", "b"), ("$ ", "m")])
    cursor = rect(PAD + width_of(head), H - 33, 9, 17, fill=THEME["text"], class_="blink")
    body.append(f'<g class="fade" style="{delay(t)}">{last}{cursor}</g>')

    return terminal(
        W, H, f"{ident['user']}@{ident['host']}: ~", "".join(body),
        title=f"{ident['name']} — {ident['headline'][0]}",
        desc=" · ".join(ident["headline"] + ident["boot"]),
    )


if __name__ == "__main__":
    save("hero.svg", build(load_content()))
