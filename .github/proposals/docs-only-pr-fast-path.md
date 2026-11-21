# Proposal: Docs-only pull request fast path

**Status:** Accepted direction — implement with auto-approve bot (option B)  
**Goal:** Let documentation / graphics-only PRs merge without waiting on a second human, while keeping review requirements for playbooks, setup YAML, roles, and other demo-breaking paths.

## Why

Today `main` has classic branch protection with **1 required approving review** for every pull request. That is appropriate for automation content, but it slows low-risk documentation fixes (typos, presenter notes, README clarifications, screenshots) that cannot break demo job templates.

We already require a pull request (audit trail) and CI (pre-commit). For docs-only changes, the remaining gate is human latency, not technical risk.

## Chosen approach: auto-approve Action (option B)

Keep the existing “1 approving review” branch protection. Add a small GitHub Action that:

1. Lists files changed on the PR (API only — no checkout of PR code).
2. If **every** path is markdown or a common graphic (`.md`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`), treat the PR as docs-only.
3. Otherwise exit — humans review as today.
4. If docs-only, mint a token from a dedicated **GitHub App** and submit an **APPROVE** review (plus a `docs-only` label).

No AI is involved — this is a deterministic path filter + API approve, similar in spirit to how RHDP/agnosticv teams use bots for low-risk PR gates.

Workflow: [`.github/workflows/docs-only-auto-approve.yml`](../workflows/docs-only-auto-approve.yml).

### Why not a path-aware ruleset alone?

A ruleset with `!*.md` negation (option A) is still valid and needs no bot secrets, but it requires an admin to restructure classic branch protection. Option B keeps today’s “1 review for everything” rule and satisfies it with a bot approval for docs-only PRs — closer to Chris’s [suggestion on #371](https://github.com/ansible/product-demos/pull/371#issuecomment-6276629694) and easier to land incrementally.

### What a docs-only PR still requires

- Open a PR against `ansible/product-demos` (no direct pushes to `main`)
- Pass existing CI (pre-commit)
- Meet org rules (signed commits, no force-push, etc.)
- Docs-approver App approval (automatic when secrets are configured)
- Someone with write access clicks merge when checks are green

### What still needs a human approval

Any PR that changes even one non-docs path (for example `.yml`, `.yaml`, `.j2`, roles, collections, workflows, scripts). Mixed docs+YAML PRs are **not** auto-approved.

## Admin setup (one-time)

`GITHUB_TOKEN` approvals from Actions usually **do not count** toward required reviews. Use a GitHub App:

1. Create a GitHub App (e.g. `apd-docs-approver`) with permission **Pull requests: Read & write**.
2. Install it on `ansible/product-demos`.
3. Add repository secrets:
   - `APD_DOCS_APPROVER_APP_ID` — numeric App ID
   - `APD_DOCS_APPROVER_APP_PRIVATE_KEY` — App private key PEM
4. Confirm on a markdown-only test PR: workflow runs, `docs-only` label appears, bot APPROVE shows, merge is allowed with green CI.
5. Confirm a mixed markdown+YAML PR is **not** auto-approved.

Until those secrets exist, the workflow still detects docs-only PRs and leaves a one-time comment explaining that auto-approve is not configured yet.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. Ruleset required reviewers + `!*.md`** | Native, no bot secrets | Needs admin to replace classic “1 review for everything” |
| **B. Auto-approve Action (chosen)** | Keeps current branch protection; matches RHDP-style bot idea | Needs GitHub App secrets; `GITHUB_TOKEN` alone is not enough |
| **C. CODEOWNERS + require code owner reviews** | Familiar | No clean `!*.md` negation; easy to misconfigure |
| **D. Admins bypass only** | Already possible | Only helps admins |

## Related doc change

`CONTRIBUTING.md` describes the docs-only exception and the auto-approve bot so contributors know when a second human review is optional.
