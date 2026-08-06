# demo.patching.patch_windows

Scan installed packages and services (via the collection's `win_scan_packages` / `win_scan_services` modules), then install Windows Updates for the configured update categories.

```yaml
- name: Patch windows server
  ansible.builtin.include_role:
    name: demo.patching.patch_windows
```

The package/service scan populates fact data consumed later by `demo.patching.report_windows` / `demo.patching.report_windows_patching`. Reboots after patching are controlled by `allow_reboot`.

Repo playbook: [`windows/patching.yml`](../../../../../../windows/patching.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Windows host reachable over WinRM
- `ansible.windows` collection (`win_updates`)
- This collection's `win_scan_packages` and `win_scan_services` modules (`demo.patching`)

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `win_update_categories` | `Application`, `Connectors`, `CriticalUpdates`, `DefinitionUpdates`, `DeveloperKits`, `FeaturePacks Guidance`, `SecurityUpdates`, `ServicePacks`, `Tools`, `UpdateRollups`, `Updates` | Categories passed to `ansible.windows.win_updates` |
| `allow_reboot` | `true` | Passed as `win_updates`' `reboot` option |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Scan packages/services (`demo.patching.win_scan_packages`, `demo.patching.win_scan_services`), then install Windows Updates for `win_update_categories`. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Windows patching demos in this repository.
