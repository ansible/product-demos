#!/usr/bin/env python3
"""Copy demo READMEs from <section>/docs/ into docs/demos/<slug>/ for Jekyll.

Source files are pure markdown (no YAML frontmatter) so they read cleanly on
GitHub.  This script prepends the required Jekyll frontmatter during the copy.

Run before `jekyll serve` for local preview. The GitHub Actions workflow runs
this automatically during CI/CD build.

Usage:
    python3 docs/_scripts/build-demo-pages.py
"""
import os
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(REPO_ROOT)

with open("docs/_data/demos.yml") as f:
    demos = yaml.safe_load(f)

copied = 0
for demo in demos:
    slug = demo.get("slug", "")
    readme = demo.get("readme_path", "")
    if not readme or not os.path.exists(readme):
        continue

    with open(readme) as f:
        body = f.read()

    # Build frontmatter from demos.yml metadata
    fm_lines = [
        "---",
        "layout: demo-detail",
        f"demo_slug: {slug}",
    ]
    if demo.get("special_thanks"):
        fm_lines.append(f'special_thanks: "{demo["special_thanks"]}"')
    fm_lines.append("---")

    content = "\n".join(fm_lines) + "\n" + body

    dest_dir = f"docs/demos/{slug}"
    os.makedirs(dest_dir, exist_ok=True)
    with open(f"{dest_dir}/index.md", "w") as f:
        f.write(content)
    copied += 1

print(f"Copied {copied} demo READMEs into docs/demos/")
