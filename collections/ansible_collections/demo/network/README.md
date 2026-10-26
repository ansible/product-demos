# demo.network

Local collection supporting the [Network demos](../../../../network/README.md). It is shipped inside this repository rather than published to Galaxy or Automation Hub.

| Role | Description |
|---|---|
| `containerlab` | Shared device catalog, infrastructure defaults, independent `product_demos` (Cisco) and `multi-vendor` (Juniper/Arista) topologies, bootstrap rendering, and active topology discovery. |
| `configure_lab` | Connected demo configuration using vendor network resource modules. |
| `gather_report` | Independent identity, operational, and structured-resource collection with partial-failure handling. |
| `report_server` | Persistent Apache hosting, SELinux port policy, and active firewalld configuration. |
| `build_report` | Static HTML and sanitized JSON publication with an AAP report URL artifact. |

The `network_report` filter plugin normalizes vendor facts, redacts sensitive values, and aggregates only hosts selected by the current job. The HTML uses native expandable sections and local assets. See [report documentation](../../../../network/docs/network-report.md) and [tests](tests/README.md).
