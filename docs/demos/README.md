# Demo Detail Pages

This directory contains generated content for the GitHub Pages site.

**Source of truth:** Each demo's documentation lives next to its playbook in
`<section>/docs/<slug>.md` (e.g. `cloud/docs/patch-cloud-stack.md`).

During the GitHub Actions build, the `build-demo-pages.py` script copies each
README into `docs/demos/<slug>/index.md` for Jekyll to render.

To preview locally:

```bash
python3 docs/_scripts/build-demo-pages.py
cd docs && bundle exec jekyll serve
```
