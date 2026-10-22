# Network demo checks

Run from the repository root. Install the pinned network collections from an EE requirements file and use Python with `ncclient`, `passlib`, Jinja2, and Ansible available. Offline resource rendering does not connect to devices.

```bash
python -m unittest discover -s collections/ansible_collections/demo/network/tests -v
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/render_resources.yml
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/render_topology.yml
ansible-playbook -i localhost, collections/ansible_collections/demo/network/tests/collect_unsupported.yml
```

`render_resources.yml` invokes each planned vendor resource module with `state: rendered`, checks that commands were generated, and requires zero device changes. Unit tests cover Junos logical units and LLDP JSON, Cisco/EOS neighbors, independent resource failures, unreachable devices, inventory selection, redaction, and HTML escaping.

In an APD environment, also verify:

1. Deploy the exact vJunos-switch image on the chosen EC2 size; record boot time and stability alongside all four devices. The default four-device deployment uses `c8i.4xlarge` for additional memory headroom; resource usage has not yet been measured live. `c8i.2xlarge` remains selectable for comparison.
2. Run Configure Devices twice and confirm second-run idempotence.
3. Run `network/validate_containerlab.yml` (the Controller job initially targets Junos) to capture KVM, container resource usage, facts, and a data-path ping. For a full standalone run, use `_hosts=containerlab`.
4. Generate all-device and each platform-only report. Make one device unreachable and verify the report retains it with an error.
5. Verify HTTP access from the execution node and presenter browser, then reboot the hypervisor and verify device and report persistence.
6. Exercise Cisco Backup, Staging, Upgrade, and IOS-XE compliance. Destroy the topology and confirm its report is removed; destroy the stack and confirm AWS resources are gone.

A passing offline check is not evidence that vJunos-switch runs on EC2. Containerlab documents a nested-VM limitation; the supplied image is believed to have been exercised on Azure, and the APD EC2 runtime still needs validation.
