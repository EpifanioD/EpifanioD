# Profile generator

The SVGs in `assets/` are rendered by these scripts. Python 3.11+ only, no dependencies.

```text
content/profile.toml        what is shown (text, stack, architecture)
scripts/svg.py              theme, fonts, CSS animations and drawing helpers
scripts/generate_*.py       one script per SVG
data/contributions.json     cached contribution data (written by the workflow)
assets/*.svg                output, embedded by README.md
```

## Run locally

```bash
python scripts/generate_all.py            # everything (fetches contributions)
python scripts/generate_all.py --offline  # reuse data/contributions.json
python scripts/generate_hero.py           # or a single SVG
```

Open the files in `assets/` in a browser to watch the animations.

## Automation

`.github/workflows/update-profile.yml` runs daily, on manual dispatch and whenever
`content/` or `scripts/` change on `main`. It regenerates every SVG and commits only
if something changed.

## The hero scene

`generate_hero.py` draws a pixel-art room on a 180×72 grid (5 px per unit). Sprites are
lists of strings, one character per pixel (`H` hair, `S` skin, `T` t-shirt, `.` transparent);
colors were sampled from the GitHub avatar. Three groups (waving, walking, seated) are
switched on and off by CSS animations on a timeline, and the code on the monitor types
itself in a loop.

## Notes

- Animations are CSS inside each SVG (`fade`, `type`, `blink`, `draw`, `pulse`) plus one SMIL
  `animateMotion`. No JavaScript, which GitHub would strip.
- Fonts can't be loaded inside an `<img>`, so text uses the visitor's system monospace font.
  Layout assumes ~0.6em per character.
- Visitors with *reduced motion* enabled get the final, static frame (seated, coding).
- `profile.svg` and `stack.svg` are half-width panes shown side by side; `generate_all.py`
  gives both the height of the taller one.
