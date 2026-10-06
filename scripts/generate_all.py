"""Regenerate every SVG in assets/ and point README.md at the new versions."""
import hashlib
import re

import generate_architecture
import generate_hero
import generate_profile
import generate_stack
from svg import ASSETS, ROOT, load_content, save

content = load_content()
save("hero.svg", generate_hero.build(content))

# side-by-side panes share the taller one's height
pane_h = max(generate_profile.layout(content)[1], generate_stack.layout(content)[1])
save("profile.svg", generate_profile.build(content, pane_h))
save("stack.svg", generate_stack.build(content, pane_h))

save("architecture.svg", generate_architecture.build(content))

# Browsers cache each image for a few minutes, so a changed SVG at the same URL shows up
# late. README links the absolute raw URL with a content hash: new content, new URL.
# (A relative path won't do: GitHub's redirect drops the query string.)
user = content["identity"]["github"]
raw = f"https://raw.githubusercontent.com/{user}/{user}/main/assets/"
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
for svg in sorted(ASSETS.glob("*.svg")):
    version = hashlib.sha1(svg.read_bytes()).hexdigest()[:8]
    pattern = rf'src="[^"]*assets/{re.escape(svg.name)}(\?v=[0-9a-f]+)?"'
    text = re.sub(pattern, f'src="{raw}{svg.name}?v={version}"', text)
readme.write_text(text, encoding="utf-8")
print("README.md image versions updated")
