"""Regenerate every SVG in assets/. Pass --offline to reuse cached contribution data."""
import sys

import generate_architecture
import generate_contributions
import generate_hero
import generate_profile
import generate_stack
from svg import load_content, save

content = load_content()
save("hero.svg", generate_hero.build(content))
save("profile.svg", generate_profile.build(content))
save("stack.svg", generate_stack.build(content))
save("architecture.svg", generate_architecture.build(content))
data = generate_contributions.load(content["identity"]["github"], offline="--offline" in sys.argv)
save("contributions.svg", generate_contributions.build(content, data))
