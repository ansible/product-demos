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

### Jobs
- [**LINUX / Register with Satellite**](server_register.yml) - Register a RHEL server with Red Hat Satellite.
- [**LINUX / Compliance Scan with Satellite**](server_openscap.yml) - Run OpenSCAP scan and report to Satellite.
- [**SATELLITE / Publish Content View Version**](satellite_publish.yml) - Publish a new version of a content view.
- [**SATELLITE / Promote Content View Version**](satellite_promote.yml) - Promote a content view version to the next lifecycle environment.

### Inventory

A dymanic inventory is created to pull inventory hosts from Red Hat Satellite. Groups will automatically be created

## Suggested Usage
**Linux / Register with Satellite** - Register a server with Red Hat Satellite using an activation key in the format `RHEL<major version>_<environment>`.

**SATELLITE / Publish Content View Version** - Publish a new version of a content view to start a patching process. By default this will publish the version and promote to the 'Dev' environment.
