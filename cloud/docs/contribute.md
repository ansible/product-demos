# Contribute a Demo

Have a demo idea? We welcome contributions from Red Hat associates, partners, and the community. This guide walks you through the process of adding a new demo to the Ansible Product Demos repository.

## Prerequisites

- A GitHub account with a fork of [ansible/product-demos](https://github.com/ansible/product-demos)
- Access to [demo.redhat.com](https://demo.redhat.com) for testing (Red Hat associates and partners)
- Familiarity with Ansible playbooks and AAP job templates

## How to contribute

1. **Fork and branch** -- Fork the repo and create a feature branch from `main`
2. **Add your playbook** -- Place it in the appropriate section directory (`cloud/`, `linux/`, `windows/`, `network/`, `openshift/`, `satellite/`)
3. **Add a setup.yml entry** -- Register your demo as a job template or workflow in the section's `setup.yml`
4. **Add documentation** -- Create a markdown file in `<section>/docs/` describing your demo
5. **Test on RHDP** -- Use demo.redhat.com to validate, specifying your branch in the project configuration
6. **Open a PR** -- Submit against `ansible/product-demos` with a descriptive title

## Pull request guidelines

| Guideline | Details |
| --- | --- |
| **Base branch** | Always target `main` on `ansible/product-demos` |
| **Scope** | PRs should not impact more than a single demo section |
| **Include setup.yml** | Every demo needs a corresponding entry in `<section>/setup.yml` |
| **Include docs** | Add a README in `<section>/docs/` for the demo catalog |
| **Rebase** | Rebase against `main` before submitting to avoid conflicts |
| **No external deps** | Don't rely on external infrastructure unless automated or documented in `user_message` |
| **Descriptive titles** | PR titles should describe the work, not reference issue numbers |

## Adding a job template entry

Copy an existing entry in your section's `setup.yml` and adjust the fields:

```yaml
- name: "Section | Your Demo Name"
  job_type: run
  inventory: "Ansible Product Demos Inventory"
  project: "Ansible Product Demos"
  playbook: "section/your_playbook.yml"
  credentials:
    - AAP Credential
  survey_enabled: true
  survey_spec:
    name: ""
    description: ""
    spec:
      - question_name: "Target hosts"
        variable: "_hosts"
        type: "text"
        required: true
        default: "all"
```

## Playbook standards

- Parameterize the target hosts:

```yaml
hosts: "{{ _hosts | default('linux') }}"
```

- Use fully qualified collection names (FQCN) for all modules
- Follow existing naming conventions: `Section | Subsection | Demo Name`
- Add any required roles or collections to `collections/requirements.yml`

## Testing

Pre-commit hooks run automatically on each commit. To set up locally:

```bash
pip install pre-commit
pre-commit install
```

You will need an Automation Hub token for ansible-lint. Get one from the [Red Hat Console](https://console.redhat.com/ansible/automation-hub/token) and export it:

```bash
export ANSIBLE_GALAXY_SERVER_AH_TOKEN=<your-token>
```

## Related demos

| Demo | Description |
| --- | --- |
| [Deploy Cloud Stack in AWS](./deploy-cloud-stack.md) | Provisions the full demo infrastructure for testing |
| [Patch Cloud Stack in AWS](./patch-cloud-stack.md) | Example of a complex workflow demo with multiple playbooks |
