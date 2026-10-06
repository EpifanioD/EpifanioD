# Profile generator

The SVGs in `assets/` are rendered by these scripts. Python 3.11+ only, no dependencies.

```text
content/profile.toml        what is shown (text, stack, architecture)
scripts/svg.py              theme, fonts, CSS animations and drawing helpers
scripts/generate_*.py       one script per SVG
assets/*.svg                output, embedded by README.md
```

## Run locally

```bash
python scripts/generate_all.py            # everything
python scripts/generate_hero.py           # or a single SVG
```

Open the files in `assets/` in a browser to watch the animations.

## Automation

`.github/workflows/update-profile.yml` runs on manual dispatch and whenever `content/` or
`scripts/` change on `main`. It regenerates every SVG and commits only if something changed.
The contribution snake comes from `snake.yml` (Platane/snk), published to the `output` branch.

## The hero scene

`generate_hero.py` draws a pixel-art room on a 180×72 grid (5 px per unit). Sprites are
lists of strings, one character per pixel (`H` hair, `S` skin, `T` t-shirt, `.` transparent);
colors were sampled from the GitHub avatar. The story (door opens, wave, walk in, code
next to a steaming coffee, PC off, walk out, wave goodbye) is a timeline at the top of the
file; every group follows a CSS keyframe track over the same cycle, so it loops in sync.

## Notes

- Animations are CSS inside each SVG (`fade`, `type`, `blink`, `draw`, `pulse`) plus one SMIL
  `animateMotion`. No JavaScript, which GitHub would strip.
- Fonts can't be loaded inside an `<img>`, so text uses the visitor's system monospace font.
  Layout assumes ~0.6em per character.
- Visitors with *reduced motion* enabled get the final, static frame (seated, coding, PC on).
- `profile.svg` and `stack.svg` are half-width panes shown side by side; `generate_all.py`
  gives both the height of the taller one.
