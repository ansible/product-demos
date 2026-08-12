# GitHub Actions
## Background
We want to make attempts to run our integration tests in the same manner wether using GitHub actions or on a developers's machine locally. For this reason, the tests are curated to run using container images. As of this writing, three images exist which we would like to test against:
  - quay.io/ansible-product-demos/apd-ee-24:latest
  - quay.io/ansible-product-demos/apd-ee-25:latest
  - quay.io/ansible-product-demos/apd-ee-26:latest

These images are built given the structure defined in their respective EE [definitions][../execution_environments]. Because they differ (mainly due to their python versions), each gets some special handling.

## pre-commit workflow: `pull_request` vs `pull_request_target`

The `pre-commit.yml` job only lints code. It does **not** need repo secrets.

### The simple mental model

Think of two kinds of CI runs:

| Trigger | Who's keys does the job hold? | Safe to run the PR's scripts? |
|---|---|---|
| `pull_request` | Visitor badge (no secrets) | Yes — lint the PR code |
| `pull_request_target` | Building keys (base repo token + secrets) | Risky — "pwn request" |

We **do** want to run lint against pull request code. That is the whole point of the check.

What we **do not** want is: give a fork PR the building keys, then check out and execute that fork's scripts.

### What was broken

1. Fork PRs (e.g. contributor `someone/product-demos` → `ansible/product-demos`) triggered `pull_request_target`.
2. The workflow checked out the fork and ran `./.github/workflows/run-pc.sh` from that tree while holding base-repo trust.
3. In mid-2026, `actions/checkout` started refusing that pattern by default (`allow-unsafe-pr-checkout` required), so `pre-commit-25` failed at **checkout** — before ansible-lint ever ran.
4. Local ansible-lint could pass while GitHub showed red. That red was a CI security gate, not a code lint failure.

Because `pull_request_target` always uses the workflow file from the **base** branch (`main`), fixing the YAML only inside a fork PR does not help until the fix lands on `main`.

### The fix

Use `pull_request` (plus `push`) and a normal checkout:

- CI still checks out and lints the PR code.
- The job runs without secrets / privileged base-repo access.
- Fork PRs no longer hit the checkout refusal.

Trade-offs for this lint-only job are small: no secrets access (we do not need any), and first-time fork contributors may need a maintainer to approve the workflow run once (GitHub org setting).

Do **not** reintroduce `pull_request_target` here unless this job truly needs secrets **and** untrusted PR code is never executed with those privileges.

## Troubleshooting GitHub Actions

### Interactive
It is likely the most straight-forward approach to interactively debug issues. The following podman command can be run from the project root directory to replicate the GitHub action:
```
podman run \
           --user root  \
           -v $(pwd):/runner:Z \
           -it \
           <image> \
           /bin/bash
```
`<image>` is one of `quay.io/ansible-product-demos/apd-ee-26:latest`, `quay.io/ansible-product-demos/apd-ee-25:latest`, `quay.io/ansible-product-demos/apd-ee-24:latest`
It is not exact because GitHub seems to run closer to a sidecar container paradigm, and uses docker instead of podman, but hopefully it's close enough.

For the 24 EE, the python interpreriter verions is set for our pre-commit script like so: `USE_PYTHON=python3.9 ./.github/workflows/run-pc.sh`
The 25 EE is similary run but without the need for this variable: `./.github/workflows/run-pc.sh`
