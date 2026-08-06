# demo.satellite.scap_client

Configure a host to run OpenSCAP compliance scans reported back to Red Hat Satellite/Foreman: install the OpenSCAP scanner and `foreman_scap_client`, look up the matching compliance policy (and any tailoring file) from the Satellite API, and template `/etc/foreman_scap_client/config.yaml`.

Adapted from the [foreman_scap_client Puppet module](https://github.com/theforeman/puppet-foreman_scap_client). The role must run with root privileges (directly as root or via `become`) because it modifies system configuration.

```yaml
- name: Run openSCAP scan
  hosts: "{{ _hosts | default(omit) }}"
  become: true
  vars:
    policy_name: all
  roles:
    - demo.satellite.scap_client
```

The scan itself is not triggered by this role -- after the config is templated, the caller runs `foreman_scap_client <policy id>` (see the repo playbook, which loops over the resolved `policy` list).

Repo playbook: [`satellite/server_openscap.yml`](../../../../../../satellite/server_openscap.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL host with `dnf` and `become` (root); RPM repos providing `openscap-scanner` and `rubygem-foreman_scap_client` must be enabled (for example via `demo.satellite.register_host`)
- Network access from the target host to the Satellite server (`foreman_server_url`) to query the Compliance API
- A Satellite user (`foreman_username` / `foreman_password`) with permission to read Compliance policies, SCAP contents, and tailoring files
- The host must already have a Compliance policy assigned in Satellite that matches `policy_name`

## Role Variables

Defaults live in `defaults/main.yaml`.

| Variable | Default | Description |
| --- | --- | --- |
| `foreman_server_url` | `env:SATELLITE_SERVER` | Base URL of the Satellite/Foreman server used for the Compliance API |
| `foreman_username` | `env:SATELLITE_USERNAME` | Satellite API username (basic auth) |
| `foreman_password` | `env:SATELLITE_PASSWORD` | Satellite API password (basic auth); logged calls that use it are suppressed via `no_log` |
| `foreman_validate_certs` | `env:FOREMAN_VALIDATE_CERTS` (default `true`) | Whether to validate TLS certs; API lookups in `tasks/main.yaml` currently always pass `validate_certs: false` |
| `capsule_server` | `{{ foreman_server_url }}` | Proxy/Capsule hostname written into `config.yaml` as `:server:` |
| `capsule_port` | `'9090'` | Port written into `config.yaml` as `:port:` |
| `policy_name` | `'all'` | Compliance policy name to match (or `all` for every policy assigned to the host) |
| `policy_scan` | `{{ policy_name }}` | Policy name(s) the caller's scan loop should execute against |
| `crontab_hour` / `crontab_minute` / `crontab_weekdays` | `2` / `0` / `0` | Reserved for a scheduled-scan cron job; the cron task in `tasks/main.yaml` is currently commented out |
| `foreman_operations_scap_client_secure_logging` | `true` | When `true`, suppresses logging (`no_log`) on the Satellite API calls that carry credentials |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Install OpenSCAP packages, resolve the matching policy/SCAP content/tailoring file from the Satellite Compliance API, and template `/etc/foreman_scap_client/config.yaml`. |

## License

MIT (see [`LICENSE`](LICENSE)) -- this role predates the collection's GPL-3.0-or-later default and keeps its original license.

## Authors and Acknowledgments

- **morenod** -- original author (2018), see [`LICENSE`](LICENSE) and [`Changelog.md`](Changelog.md).
- Adapted from the [`foreman_scap_client` Puppet module](https://github.com/theforeman/puppet-foreman_scap_client).
