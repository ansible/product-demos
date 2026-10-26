# Detailed multi-vendor network report

`network/report.yml` collects Cisco IOS-XE, Cisco NX-OS, Juniper Junos, and Arista EOS devices and publishes a standalone HTML report on the containerlab hypervisor. The report remains available after the AAP job finishes.

## Run the demo

1. Build and select the updated **Product Demos EE** using the definitions in `execution_environments/`. Sync the project and rerun Network setup to update inventory groups and job credentials.
2. Run **NETWORK | Deploy Containerlab Stack** and choose `product_demos` for the original two Cisco devices or `multi-vendor` for Junos and EOS. Deploy both topologies on the same hypervisor to report on all four platforms. Existing hypervisors can use **NETWORK | Containerlab | Deploy Topology**, which also refreshes security group ports. Redeploying reconfigures the lab and resets device configuration to its bootstrap.
3. Run **NETWORK | Containerlab | Configure Devices** to populate the deployed devices with interfaces, VLANs, trunks, loopbacks, NTP, and addressing through network resource modules.
4. For `multi-vendor`, run **NETWORK | Containerlab | Validate Devices** to validate Juniper on EC2. Its default target is `clab_junos`; the data-path check requires the neighboring Arista device to be configured too. This validation is still required: image availability and offline checks do not establish EC2 compatibility.
5. Run **NETWORK | Report**, select all devices or one platform, and open the `network_report_url` from the job output or AAP artifacts.

The default report URL is `http://<hypervisor>:8088/network/`. `report.json` provides the same sanitized data for download. The stable URL shows the most recently published report; concurrent runs may replace it.

## What the report includes

- Inventory identity, vendor, OS, model, serial, version, management endpoint, transport, and memory observations.
- Live interface observations and discovered neighbors. Cisco neighbor facts may include both LLDP and CDP; the report labels the source accordingly. Junos LLDP neighbors are collected separately over NETCONF.
- Detailed resource configuration: interfaces, switching, addressing, VLANs, LLDP, LAG/LACP, static routes, BGP, OSPF, and NTP where supported by the platform facts module.
- Independent collection status for every resource: collected, not configured, unsupported, failed, or not collected.
- Search, vendor filtering, expandable tables, and local CSS/JavaScript without CDN dependencies.

**Configuration and operational observations are separate.** BGP and OSPF configuration does not demonstrate adjacency health. This version does not collect routing protocol operational state.

Failed devices remain visible, successful sections survive individual parser failures, and only hosts selected in the current job are published. A successful publishing job can contain collection failures; check `network_report_devices_with_issues` in artifacts and the errors on each device card.

The report exports an explicit set of fields rather than hostvars or running configuration. Sensitive resource keys and credential values in errors are redacted. Device strings are HTML escaped. The site contains detailed lab information and is served over HTTP; use `clab_access_cidr` to restrict reachability to the execution nodes and presenters.

## Inventory and credentials

| Selection | Platform | Connection |
|---|---|---|
| `containerlab` | All enabled devices in the selected topology | Per-platform settings |
| `clab_ios` | Cisco IOS-XE | `ansible.netcommon.network_cli` |
| `clab_nxos` | Cisco NX-OS | `ansible.netcommon.network_cli` |
| `clab_junos` | Juniper Junos | `ansible.netcommon.netconf` |
| `clab_eos` | Arista EOS | `ansible.netcommon.network_cli` |

The `_hosts` survey controls device selection. `_report_server` defaults to the AWS inventory group `clab_containerlab`. Keep the hypervisor outside the `containerlab` device group. Use the survey instead of a job-wide limit that would exclude the publishing host.

The report job uses **Containerlab Device Access** for devices and **Containerlab SSH** for the hypervisor. Bootstrap defaults match the existing `admin` / `admin@123` demo credential. Override `clab_device_username` and `clab_device_password` together with that AAP credential when changing device access.

## Content and validation

Current Red Hat Hub content was located with `hub-search` on 2026-10-22. The EE definitions pin `ansible.netcommon` 8.7.1, `cisco.ios` 11.6.0, `cisco.nxos` 13.0.0, `arista.eos` 12.3.0, and `juniper.device` 2.0.1. Juniper uses the current `juniper.device.junos_*` resource modules rather than the compatibility redirects in `junipernetworks.junos`.

The toolkit's older report supplied the section concept. Collection, normalization, and hosting are implemented locally with current content. See the [collection tests](../../collections/ansible_collections/demo/network/tests/README.md) for offline rendering and failure-handling checks. Live device validation, second-run idempotence, reboot stability, and the existing Cisco backup/staging/upgrade demos still require an APD environment.
