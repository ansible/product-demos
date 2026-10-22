# Proposal: Docs-only pull request fast path

**Status:** Open for APD meeting discussion  
**Goal:** Let markdown-only documentation PRs merge without a second-person approval, while keeping review requirements for playbooks, setup YAML, roles, and other demo-breaking paths.

## Why

Today `main` has classic branch protection with **1 required approving review** for every pull request. That is appropriate for automation content, but it slows low-risk documentation fixes (typos, presenter notes, README clarifications) that cannot break demo job templates.

We already require a pull request (audit trail) and CI (pre-commit). For `*.md`-only changes, the remaining gate is human latency, not technical risk.

## Current controls (as of this proposal)

| Control | Source | What it enforces |
|---------|--------|------------------|
| 1 approving review | Repo branch protection on `main` | All PRs, including markdown-only |
| Separation of Duties | Org ruleset on default branch | No branch deletion, no force-push, required commit signatures |
| pre-commit | GitHub Actions | Lint/hooks on PR |

There is no `CODEOWNERS` file today. The org ruleset does **not** impose the review requirement; the repo branch protection rule does.

## Recommended approach (GitHub-native)

Use a **repository ruleset** with the [Required reviewer](https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/) rule and path negation (same idea as `.gitignore`):

1. Keep requiring a pull request into `main`.
2. Require 1 approving review for changes that touch non-markdown paths.
3. Exclude `*.md` from that review requirement via `!` patterns.
4. Lower or remove the classic branch-protection "required approving review count" so it does not override the path-aware ruleset (classic protection applies to **all** files and would keep blocking docs-only merges).

Example required-reviewer file patterns:

```text
**
!**/*.md
```

### What a docs-only PR would still require

- Open a PR against `ansible/product-demos` (no direct pushes to `main`)
- Pass existing CI (pre-commit)
- Meet org rules (signed commits, no force-push, etc.)
- Author (or any collaborator with write access) can merge when checks are green — no second approver

### What would still need a human approval

Any PR that changes even one non-markdown file (for example `.yml`, `.yaml`, `.j2`, roles, collections, workflows, images, scripts).

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. Ruleset required reviewers + `!*.md` (recommended)** | Native, path-aware, no bot secrets, easy to explain | Needs admin to replace classic "1 review for everything" |
| **B. Auto-approve Action for md-only PRs** | Keeps current branch protection | Needs a GitHub App or PAT; `GITHUB_TOKEN` approvals often do not count; more moving parts |
| **C. CODEOWNERS + require code owner reviews** | Familiar pattern | CODEOWNERS has no clean `!*.md` negation; easy to misconfigure with a catch-all `*` |
| **D. Admins bypass only** | Already possible (`enforce_admins` is off) | Only helps admins; does not speed up normal contributors |

## Scope decision for the meeting

Please decide:

1. **Which paths are exempt?**
   - Option 1 (broader): all `*.md` files
   - Option 2 (narrower): only `**/README.md` and `**/docs/**/*.md`
2. **Who may merge docs-only PRs?** Anyone with write access (recommended), or a named maintainers team only?
3. **Should process docs be exempt?** For example, should changes to `CONTRIBUTING.md` still need review even if they are markdown?

## Admin follow-up after APD accepts this

These settings are not stored as normal repo files; a repo admin applies them after the meeting:

1. Create a repo ruleset targeting the default branch with a required-reviewer (or pull-request) rule that excludes the agreed markdown patterns.
2. Set classic branch protection **Required approving reviews** to `0` (or remove that requirement) so it no longer forces a review on docs-only PRs. Keep "Require a pull request before merging".
3. Confirm a mixed PR (markdown + YAML) still requires approval.
4. Confirm a markdown-only PR can merge with green checks and no approval.

## Related doc change

`CONTRIBUTING.md` is updated in this PR to describe the docs-only exception so contributors know when a second review is optional.
