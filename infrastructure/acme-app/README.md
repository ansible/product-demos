# ACME App (Simple Config Drift)

Playbooks and a single Jinja template for the **Simple Config Drift** demo: Ansible owns an ACME storefront on `aws_rhel9`.

Documentation: [`../docs/config-drift-simple.md`](../docs/config-drift-simple.md)

## Layout

| Path | Purpose |
|------|---------|
| [`playbooks/setup.yml`](playbooks/setup.yml) | Install httpd, copy CSS, render the approved baseline |
| [`playbooks/configure.yml`](playbooks/configure.yml) | Re-render the same template from survey vars |
| [`tasks/render.yml`](tasks/render.yml) | Shared copy + template tasks |
| [`playbooks/templates/index.html.j2`](playbooks/templates/index.html.j2) | Storefront HTML (under 30 lines) |
| [`playbooks/files/style.css`](playbooks/files/style.css) | Visual design |
| [`defaults.yml`](defaults.yml) | Approved baseline vars |

AAP job templates are defined in [`../setup.yml`](../setup.yml).
