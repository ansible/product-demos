# Network demo checks

Run from the repository root with the rebuilt network EE. Offline rendering does not connect to devices.

```bash
python -m unittest discover -s collections/ansible_collections/demo/network/tests -v
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/render_resources.yml
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/render_topology.yml
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/collect_unsupported.yml
```

`render_topology.yml` renders the connected topology and all bootstrap files in a temporary directory. It checks the exact requested node names, vSRX image/kind, management IP uniqueness, ports, EOS CPU settings, and all three cross-vendor links. It also verifies discovery of legacy split-lab records for migration and of completed teardown records.

`render_resources.yml` invokes each planned vendor resource module with `state: rendered`, requires commands to be generated, and checks zero device changes. Unit tests cover vendor facts and neighbors, report host selection, unreachable devices, independent collection errors, redaction, and HTML escaping.

For live APD acceptance:

1. Deploy the connected topology on a KVM-capable EC2 hypervisor using the rebuilt EE. Confirm old split labs and retired inventory hosts are removed.
2. Run Configure Devices; check all four nodes and rerun when inspecting configuration drift.
3. Run Validate Devices for `containerlab`. It captures KVM/capacity evidence, collects structured resources, and tests multi-hop pings sourced from each node's loopback.
4. Run Report and verify four collected devices with no issues; inspect interface/neighbor observations and routes.
5. Run the IOS-XE backup demo. Exercise STIG, Staging, and Upgrade separately as required.
6. Test topology and stack teardown, including report removal and AWS cleanup.

`inspect_topology.yml` is a read-only live hypervisor check for the single topology record, exact five-container membership, running states, and all device management ports. Its AAP artifacts include container IDs and start times. Previous split-lab or vJunos-switch acceptance is not evidence for vSRX 23.2R2.21 or the new connected layout; validate this image and routed paths live.
