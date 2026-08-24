# demo.satellite.register_host

Register a RHEL host with Red Hat Satellite using an activation key, replacing any RHUI repos, enabling the Satellite-managed RHSM repos for the host's OS release, and enabling Satellite remote execution (SSH key from the Satellite/Capsule).

```yaml
- name: Register host to Satellite
  hosts: "{{ _hosts | default(omit) }}"
  become: true
  vars:
    satellite_url: "{{ lookup('ansible.builtin.env', 'SATELLITE_SERVER') }}"
  roles:
    - demo.satellite.register_host
```

The activation key defaults to `RHEL<major version>_<env>` (for example `RHEL8_dev`), so the target host's Satellite organization must have a matching activation key. RHSM repos are chosen per OS release from `vars/RedHat7.yml` / `vars/RedHat8.yml`. RHEL 9 is not supported today: `tasks/main.yml` asserts major version is `7` or `8`, and no `vars/RedHat9.yml` is shipped.

Repo playbook: [`satellite/server_register.yml`](../../../../../../satellite/server_register.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL 7 or 8 host reachable over SSH with `become` (RHEL 9 is asserted out)
- `community.general` collection (`redhat_subscription`, `rhsm_repository`)
- `ansible.posix` collection (`authorized_key`)
- Network access from the target host to the Satellite server (`satellite_url`) and a valid activation key for the host's org

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `instance_name` | `{{ inventory_hostname | regex_replace('_', '-') }}` | Consumer name registered in Satellite (underscores replaced with hyphens) |
| `activation_key` | `RHEL<major_version>_<env>` | Activation key used for `redhat_subscription`; requires `env` to be set by the caller |
| `rex_user` | `root` | User account that receives the Satellite remote execution SSH public key |
| `force_register` | `true` | Passed to `community.general.redhat_subscription` as `force_register` |
| `satellite_url` | required (caller-supplied) | Base URL of the Satellite server; used for the Katello CA RPM, remote execution pubkey, and (via `capsule_server`, in `scap_client`) other Satellite APIs |
| `org_id` | `Default_Organization` | Passed to `redhat_subscription`; override for non-default orgs |
| `rhsm_enabled_repos` | OS-specific (`vars/RedHat7.yml`, `vars/RedHat8.yml`) | List of repos enabled via `rhsm_repository`; selected by `include_vars` on `ansible_distribution + ansible_distribution_major_version` |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Verify RHEL 7/8, set hostname, remove RHUI client packages/repos, install the Katello CA RPM, register via activation key, enable OS-specific RHSM repos, install `katello-host-tools`, and authorize the Satellite remote execution SSH key. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.satellite`](../../README.md) for the Satellite registration demos in this repository.
