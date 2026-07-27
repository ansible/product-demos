#!/usr/bin/env python3
"""Copy demo READMEs from <section>/docs/ into docs/demos/<slug>/ for Jekyll.

Run before `jekyll serve` for local preview. The GitHub Actions workflow runs
this automatically during CI/CD build.

Usage:
    python3 docs/_scripts/build-demo-pages.py
"""
import os
import shutil
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
    dest_dir = f"docs/demos/{slug}"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(readme, f"{dest_dir}/index.md")
    copied += 1

print(f"Copied {copied} demo READMEs into docs/demos/")
