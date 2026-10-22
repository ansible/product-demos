"""Normalize whitelisted network facts for the static APD device report.

Resource data describes configuration. Legacy interface facts and LLDP RPC output
provide operational observations; neither implies routing protocol session health.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping

SENSITIVE = re.compile(
    r"password|secret|community|authentication|private.?key|token", re.I
)
RESOURCE_TITLES = {
    "interfaces": "Interface configuration",
    "l2_interfaces": "Access ports and trunks",
    "l3_interfaces": "IP addressing",
    "vlans": "VLANs",
    "lldp_global": "LLDP global configuration",
    "lldp_interfaces": "LLDP interface configuration",
    "lag_interfaces": "Link aggregation groups",
    "lacp_interfaces": "LACP interface configuration",
    "static_routes": "Static routes",
    "bgp_global": "BGP configuration",
    "bgp_address_family": "BGP address families",
    "ospfv2": "OSPF configuration",
    "ospf_interfaces": "OSPF interfaces",
    "ntp_global": "NTP configuration",
}


def _clean(value, secrets=()):
    if isinstance(value, Mapping):
        return {
            str(k): "[redacted]" if SENSITIVE.search(str(k)) else _clean(v, secrets)
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_clean(v, secrets) for v in value]
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(str(secret), "[redacted]")
        return value
    return value


def _failed(result):
    return bool(result.get("failed") or result.get("unreachable"))


def _error(result, secrets):
    # Messages can echo device commands; exclude raw exceptions and module args.
    message = str(result.get("msg", "Collection failed"))
    message = re.sub(
        r"(?i)\b(password|secret|community|token)\s*[:= ]\s*\S+",
        r"\1 [redacted]",
        message,
    )
    return _clean(message[:1000], secrets)


def _rows(data):
    if isinstance(data, Mapping):
        return [dict(data)] if data else []
    if isinstance(data, list):
        return [dict(v) if isinstance(v, Mapping) else {"value": v} for v in data]
    return [{"value": data}] if data is not None else []


def _columns(rows):
    return list(dict.fromkeys(k for row in rows for k in row))


def _junos_neighbors(value):
    """Read Junos JSON RPC's list-of-objects representation without fixed indexes."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            return []
    found = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key == "lldp-neighbor-information":
                for entry in child if isinstance(child, list) else [child]:

                    def text(name):
                        v = entry.get(name, [])
                        if isinstance(v, list):
                            return v[0].get("data", "Unknown") if v else "Unknown"
                        return v

                    found.append(
                        {
                            "local_interface": text("lldp-local-interface"),
                            "neighbor": text("lldp-remote-system-name"),
                            "remote_port": text("lldp-remote-port-id"),
                            "source": "LLDP",
                        }
                    )
            else:
                found.extend(_junos_neighbors(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_junos_neighbors(child))
    return found


def network_report_device(
    name,
    address,
    port,
    network_os,
    connection,
    platform,
    base,
    legacy,
    resource_results,
    neighbor_result,
    requested_resources,
    secrets=(),
):
    """Only export report data, never hostvars or a complete running config."""
    base = base or {}
    facts = dict(base.get("ansible_facts", {}))
    errors = []
    if _failed(base):
        errors.append({"section": "Identity", "message": _error(base, secrets)})
    successful_legacy = set()
    for result in (legacy or {}).get("results", []):
        if result.get("skipped"):
            continue
        if _failed(result):
            errors.append(
                {"section": result["item"], "message": _error(result, secrets)}
            )
        else:
            successful_legacy.add(result["item"])
            facts.update(result.get("ansible_facts", {}))
    resources = {
        r["item"]: r
        for r in (resource_results or {}).get("results", [])
        if not r.get("skipped")
    }
    supported = base.get("ansible_facts", {}).get("available_network_resources", [])
    sections = []
    configured_interfaces = {}
    for resource in requested_resources:
        result = resources.get(resource)
        data = []
        if not platform:
            status = "unsupported"
        elif _failed(base) or not base:
            status = "not collected"
        elif resource not in supported:
            status = "unsupported"
        elif result is None:
            status = "not collected"
        elif _failed(result):
            status = "failed"
            errors.append({"section": resource, "message": _error(result, secrets)})
        else:
            raw = result.get("ansible_facts", {}).get("ansible_network_resources")
            # Several vendor collectors omit empty resource keys. An explicit
            # empty resource mapping is a successful, unconfigured section.
            if raw == {}:
                status = "not configured"
            elif not isinstance(raw, dict) or resource not in raw:
                status = "not collected"
            else:
                data = _clean(raw[resource], secrets)
                status = "collected" if data else "not configured"
                if resource == "interfaces":
                    configured_interfaces = {
                        r["name"]: r for r in _rows(data) if "name" in r
                    }
        if status == "not collected" and platform and not _failed(base) and base:
            errors.append(
                {
                    "section": resource,
                    "message": "The supported resource did not return data in this run.",
                }
            )
        rows = _rows(data)
        sections.append(
            {
                "name": resource,
                "title": RESOURCE_TITLES.get(resource, resource),
                "status": status,
                "rows": rows,
                "columns": _columns(rows),
            }
        )
    live_interfaces = []
    for ifname, values in sorted((facts.get("ansible_net_interfaces") or {}).items()):
        values = values or {}
        live_interfaces.append(
            {
                "name": ifname,
                "description": values.get(
                    "description",
                    configured_interfaces.get(ifname, {}).get("description", ""),
                ),
                "operational": values.get(
                    "oper-status",
                    values.get(
                        "operstatus",
                        values.get(
                            "lineprotocol",
                            values.get("state", values.get("linkstatus", "Unknown")),
                        ),
                    ),
                ),
                "admin": values.get(
                    "admin-status",
                    values.get("admin_state", values.get("enabled", "Unknown")),
                ),
                "mtu": values.get("mtu", "Unknown"),
                "speed": values.get("speed", values.get("bandwidth", "Unknown")),
                "mac": values.get("macaddress", "Unknown"),
                "addresses": values.get("ipv4", values.get("ipv4addresses", [])),
            }
        )
    neighbors = []
    for local_interface, entries in (facts.get("ansible_net_neighbors") or {}).items():
        for entry in entries if isinstance(entries, list) else [entries]:
            if isinstance(entry, Mapping):
                neighbors.append(
                    {
                        "local_interface": local_interface,
                        "neighbor": entry.get("host", entry.get("sysname", "Unknown")),
                        "remote_port": entry.get("port", "Unknown"),
                        "source": "Device neighbor facts (LLDP/CDP)",
                    }
                )
    neighbor_result = neighbor_result or {}
    neighbor_status = (
        "collected"
        if "interfaces" in successful_legacy and network_os != "juniper.device.junos"
        else "not collected"
    )
    if (
        network_os == "juniper.device.junos"
        and not neighbor_result.get("skipped")
        and neighbor_result
    ):
        if _failed(neighbor_result):
            neighbor_status = "failed"
            errors.append(
                {
                    "section": "LLDP neighbors",
                    "message": _error(neighbor_result, secrets),
                }
            )
        else:
            neighbor_status = "collected"
            neighbors = _junos_neighbors(
                neighbor_result.get("output", neighbor_result.get("stdout", []))
            )
    status = (
        "unsupported"
        if not platform
        else (
            "failed"
            if _failed(base) or not base
            else "partial" if errors else "collected"
        )
    )
    return _clean(
        {
            "name": name,
            "hostname": facts.get("ansible_net_hostname", name),
            "vendor": platform.get("vendor", "Unknown"),
            "os": platform.get("os", network_os),
            "network_os": network_os,
            "address": address,
            "port": port,
            "transport": connection,
            "facts_module": platform.get("facts_module", "Unavailable"),
            "version": facts.get("ansible_net_version", "Unknown"),
            "model": facts.get("ansible_net_model", "Unknown"),
            "serial": facts.get("ansible_net_serialnum", "Unknown"),
            "memory_total_mb": facts.get("ansible_net_memtotal_mb", "Unknown"),
            "memory_free_mb": facts.get("ansible_net_memfree_mb", "Unknown"),
            "status": status,
            "interfaces": live_interfaces,
            "interface_status": (
                "collected" if "interfaces" in successful_legacy else "not collected"
            ),
            "neighbors": neighbors,
            "neighbor_status": neighbor_status,
            "sections": sections,
            "errors": errors,
        },
        secrets,
    )


def network_report_document(hostvars, selected_hosts, generated_at):
    devices = []
    for name in sorted(set(selected_hosts)):
        device = hostvars[name].get("network_report_device")
        if device is None:
            device = network_report_device(
                name, "Unknown", 0, "unknown", "unknown", {}, {}, {}, {}, {}, []
            )
            device["status"] = "not collected"
        devices.append(device)
    return {
        "generated_at": generated_at,
        "devices": devices,
        "vendor_count": len({d["vendor"] for d in devices if d["vendor"] != "Unknown"}),
        "complete_count": sum(d["status"] == "collected" for d in devices),
        "issue_count": sum(d["status"] != "collected" for d in devices),
    }


def network_report_cell(value):
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
    return str(value) if value is not None else "Unknown"


class FilterModule:
    def filters(self):
        return {
            "network_report_device": network_report_device,
            "network_report_document": network_report_document,
            "network_report_cell": network_report_cell,
        }
