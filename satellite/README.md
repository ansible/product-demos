# Satellite Demos

## Table of Contents
- [Satellite Demos](#satellite-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
    - [Inventory](#inventory)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of linux operations and management with Ansible Automation Platform and Red Hat Satellite Server. The list of demos can be found below. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Workflows

| Workflow | Description |
|----------|-------------|
| [**Patch Dev Workflow**](docs/satellite-patch-dev.md) | End-to-end patching workflow for the Dev environment: sync Satellite inventory, publish content view, check for updates, and apply patches with approval gate. |

### Jobs

| Job Template | Description |
|--------------|-------------|
| [**Register with Satellite**](docs/satellite-register.md) | Register a RHEL server with Red Hat Satellite using an activation key in the format RHEL<version>_<environment>. |
| [**Compliance Scan with Satellite**](docs/satellite-compliance-scan.md) | Run an OpenSCAP compliance scan and report results back to Red Hat Satellite. |
| [**Publish Content View Version**](docs/satellite-publish-content-view.md) | Publish a new version of a Satellite content view to begin the patching promotion lifecycle. |
| [**Promote Content View Version**](docs/satellite-promote-content-view.md) | Promote a content view version from one lifecycle environment to the next (e.g. Dev → QA → Prod). |

## Suggested Usage
**Linux / Register with Satellite** - Register a server with Red Hat Satellite using an activation key in the format `RHEL<major version>_<environment>`.

**SATELLITE / Publish Content View Version** - Publish a new version of a content view to start a patching process. By default this will publish the version and promote to the 'Dev' environment.
