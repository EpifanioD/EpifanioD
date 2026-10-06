"""assets/contributions.svg: last year's contribution calendar, from real GitHub data.

Data comes from the public page https://github.com/users/<user>/contributions
(no token needed) and is cached in data/contributions.json. If the fetch fails,
the cached data is used so a network hiccup never wipes the graph.

    python scripts/generate_contributions.py            # fetch + render
    python scripts/generate_contributions.py --offline  # render from cache
"""
import json
import re
import sys
import urllib.request
from datetime import date, timedelta
from html.parser import HTMLParser

from svg import DATA, PAD, THEME, TITLE_BAR, delay, load_content, prompt, rect, save, spans, terminal, text

W = 900
CELL, GAP = 12, 3
STEP = CELL + GAP
GRID_X = PAD + 40
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CACHE = DATA / "contributions.json"


class CalendarParser(HTMLParser):
    """Collects day cells (date, level) and their tooltips (count)."""

    def __init__(self):
        super().__init__()
        self.cells, self.tips = {}, {}
        self._tip_for = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in (a.get("class") or "") and a.get("data-date"):
            self.cells[a["id"]] = (a["data-date"], int(a.get("data-level", 0)))
        elif tag == "tool-tip":
            self._tip_for = a.get("for")

    def handle_data(self, data):
        if self._tip_for:
            self.tips[self._tip_for] = self.tips.get(self._tip_for, "") + data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self._tip_for = None


def fetch(user: str) -> dict:
    req = urllib.request.Request(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "profile-readme-generator"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8")

    p = CalendarParser()
    p.feed(html)
    days = []
    for cell_id, (day, level) in p.cells.items():
        m = re.match(r"\s*([\d,]+) contribution", p.tips.get(cell_id, ""))
        days.append({"date": day, "level": level, "count": int(m.group(1).replace(",", "")) if m else 0})
    if not days:
        raise RuntimeError("no contribution cells found; the page markup may have changed")
    days.sort(key=lambda d: d["date"])

    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", " ".join(html.split()))
    return {
        "user": user,
        "total": int(total.group(1).replace(",", "")) if total else sum(d["count"] for d in days),
        "days": days,
    }


def load(user: str, offline: bool) -> dict:
    if not offline:
        try:
            data = fetch(user)
            DATA.mkdir(exist_ok=True)
            CACHE.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
            return data
        except Exception as e:  # keep the last good graph instead of failing the workflow
            print(f"warning: fetch failed ({e}); using cache", file=sys.stderr)
    return json.loads(CACHE.read_text(encoding="utf-8"))


def streaks(days: list[dict]) -> tuple[int, int]:
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    # today may still be empty; the current streak counts up to yesterday in that case
    current = 0
    for d in reversed(days[:-1] if days and not days[-1]["count"] else days):
        if not d["count"]:
            break
        current += 1
    return current, longest


def build(content: dict, data: dict) -> str:
    ident = content["identity"]
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub columns start on Sunday
    weeks = (len(days) + offset + 6) // 7

    top = TITLE_BAR + 38
    cmd, t = prompt(PAD, top, "git activity --last-year", 0.3, ident)
    body = [cmd]
    t += 0.2
    grid_y = top + 52

    # month labels, on the first column that starts a new month
    last_label, prev_month = -3, None
    for w in range(weeks):
        sunday = max(first + timedelta(days=w * 7 - offset), first)
        if sunday.month != prev_month and w - last_label >= 3:
            body.append(text(GRID_X + w * STEP, grid_y - 8, sunday.strftime("%b"), "m fade",
                             font_size=11, style=delay(t)))
            last_label = w
        prev_month = sunday.month
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(text(PAD, grid_y + row * STEP + 9, name, "m fade", font_size=11, style=delay(t)))

    # cells appear in a wave from left to right; one CSS class per column keeps the file small
    cells = []
    for i, d in enumerate(days):
        w, row = divmod(i + offset, 7)
        cells.append(rect(GRID_X + w * STEP, grid_y + row * STEP, CELL, CELL, rx=2,
                          fill=LEVELS[d["level"]], class_=f"c w{w}"))
    body.append("".join(cells))
    css = ".c{animation:fade .4s ease-out both}" + "".join(
        f".w{w}{{animation-delay:{t + 0.2 + w * 0.03:.2f}s}}" for w in range(weeks)
    )

    # legend
    legend_y = grid_y + 7 * STEP + 14
    lx = GRID_X + weeks * STEP - GAP - 5 * STEP - 76
    legend = [text(lx, legend_y + 9, "less", "m", font_size=11)]
    legend += [rect(lx + 36 + i * STEP, legend_y, CELL, CELL, rx=2, fill=c) for i, c in enumerate(LEVELS)]
    legend.append(text(lx + 36 + 5 * STEP + 6, legend_y + 9, "more", "m", font_size=11))
    t_end = t + 0.2 + weeks * 0.03
    body.append(f'<g class="fade" style="{delay(t_end)}">{"".join(legend)}</g>')

    # summary line
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"])
    active = sum(1 for d in days if d["count"])
    stats = [
        (f"{data['total']:,}", "contributions"),
        (str(active), "active days"),
        (f"{longest}d", "longest streak"),
        (f"{current}d", "current streak"),
        (str(best["count"]), f"best day ({date.fromisoformat(best['date']):%b %d})"),
    ]
    y = legend_y + 50
    x = PAD
    for i, (value, label) in enumerate(stats):
        body.append(spans(x, y, [(value, "a"), (" " + label, "m")], class_="fade", font_size=14,
                          style=delay(t_end + 0.2 + i * 0.15)))
        x += (len(value) + len(label) + 4) * 14 * 0.6
    body.append(text(W - PAD, y + 28, f"updated {days[-1]['date']}", "d", font_size=11, text_anchor="end"))

    h = y + 46
    return terminal(
        W, h, "git activity", "".join(body), css=css,
        title=f"{data['total']} contributions in the last year",
        desc=f"GitHub contribution calendar for {data['user']} from {days[0]['date']} to {days[-1]['date']}. "
             + ", ".join(f"{v} {l}" for v, l in stats) + ".",
    )


if __name__ == "__main__":
    content = load_content()
    data = load(content["identity"]["github"], offline="--offline" in sys.argv)
    save("contributions.svg", build(content, data))
