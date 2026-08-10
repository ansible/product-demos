#!/usr/bin/env python3
"""Copy demo READMEs from <section>/docs/ into docs/demos/<slug>/ for Jekyll.

Source files are pure markdown (no YAML frontmatter) so they read cleanly on
GitHub.  This script prepends the required Jekyll frontmatter during the copy.

Relative links are rewritten during copy:
  - Playbook refs  (../foo.yml)        → GitHub blob links
  - Same-dir docs  (./other-demo.md)   → ../other-demo/  (Jekyll structure)
  - Cross-section   (../../linux/docs/linux-foo.md) → ../linux-foo/

Run before `jekyll serve` for local preview. The GitHub Actions workflow runs
this automatically during CI/CD build.

Usage:
    python3 docs/_scripts/build-demo-pages.py
"""
import os
import re
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(REPO_ROOT)

GITHUB_BLOB = "https://github.com/ansible/product-demos/blob/main"
LINK_RE = re.compile(r"(\[[^\]]*\])\(([^)]+)\)")


def rewrite_links(body: str, readme_path: str) -> str:
    """Transform relative links from source-doc context to Jekyll site context."""
    src_dir = os.path.dirname(readme_path)

    def _replace(match: re.Match) -> str:
        label = match.group(1)
        url = match.group(2)

        if url.startswith(("http://", "https://", "#", "(")):
            return match.group(0)

        fragment = ""
        if "#" in url:
            url, fragment = url.split("#", 1)
            fragment = "#" + fragment

        if url.endswith((".yml", ".yaml", ".j2")):
            resolved = os.path.normpath(os.path.join(src_dir, url))
            return f"{label}({GITHUB_BLOB}/{resolved}{fragment})"

        if url.endswith(".md"):
            slug = os.path.splitext(os.path.basename(url))[0]
            return f"{label}(../{slug}/{fragment})"

        return match.group(0)

    return LINK_RE.sub(_replace, body)


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

    body = rewrite_links(body, readme)

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
