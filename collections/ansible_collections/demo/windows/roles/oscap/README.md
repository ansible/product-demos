# Ansible Role: demo.windows.oscap

This role installs and configures OpenSCAP on Windows systems, including all required dependencies (Visual C++ Redistributable), and copies SCAP content files to the target system.

## Requirements

- Windows Server 2019 or later
- WinRM configured for Ansible connectivity
- Internet access (for downloading OpenSCAP and VC++ redistributable if not already installed)

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# OpenSCAP Windows installer URL
openscap_installer_url: "https://github.com/OpenSCAP/openscap/releases/download/1.3.4/OpenSCAP-1.3.4-win32.msi"
openscap_installer_path: "C:\\Windows\\Temp\\OpenSCAP.msi"

# OpenSCAP executable path
oscap_exe_path: "C:\\Program Files (x86)\\OpenSCAP 1.3.4\\oscap.exe"

# SCAP content file from repository
scap_content_file: "winserv2019-stig-scap-benchmark.xml"

# Directory on target system where SCAP content will be copied
scap_content_dir: "C:\\oscap-content"

# Source directory for SCAP content (relative to role or playbook)
scap_content_source_dir: "{{ role_path }}/files"

# Directory for OpenSCAP reports (used by setup_web_server.yml task file)
oscap_report_dir: "C:\\oscap-reports"
```

## Task Files

The role includes multiple task files that can be used independently:

### `main.yml` (default)
Installs OpenSCAP and dependencies, copies SCAP content files.

```yaml
- name: Install and configure OpenSCAP
  ansible.builtin.include_role:
    name: demo.windows.oscap
```

### `setup_web_server.yml` (optional)
Sets up IIS web server to serve OpenSCAP reports via HTTP. This is useful when you want to view HTML reports in a web browser.

```yaml
- name: Setup IIS web server for report viewing
  ansible.builtin.include_role:
    name: demo.windows.oscap
    tasks_from: setup_web_server
  vars:
    oscap_report_dir: "C:\\oscap-reports"
```

This task file will:
- Install IIS with management tools
- Configure firewall rules for HTTP
- Create virtual directory for reports
- Enable directory browsing
- Detect and display the server's public IP address (AWS-aware)

## Dependencies

- `ansible.windows` collection
- `chocolatey.chocolatey` collection (optional - used if Chocolatey is available on target)
- `community.windows` collection

## Example Playbook

### Basic OpenSCAP Setup

```yaml
---
- name: Setup OpenSCAP on Windows
  hosts: windows_servers
  gather_facts: true
  
  tasks:
    - name: Install and configure OpenSCAP
      ansible.builtin.include_role:
        name: demo.windows.oscap
```

### Generate Reports with Web Server

```yaml
---
- name: Generate OpenSCAP compliance report with web access
  hosts: windows_servers
  gather_facts: true
  
  vars:
    compliance_profile: xccdf_mil.disa.stig_profile_MAC-1_Sensitive
  
  tasks:
    - name: Install and configure OpenSCAP
      ansible.builtin.include_role:
        name: demo.windows.oscap
    
    - name: Generate compliance report
      ansible.windows.win_command: >
        "{{ oscap_exe_path }}" xccdf eval
        --profile "{{ compliance_profile }}"
        --report "{{ oscap_report_dir }}\\report.html"
        "{{ scap_content_dir }}\\{{ scap_content_file }}"
      register: oscap_result
      failed_when: false
    
    - name: Setup IIS web server for report viewing
      ansible.builtin.include_role:
        name: demo.windows.oscap
        tasks_from: setup_web_server
```

### Override Default Variables

```yaml
---
- name: Setup OpenSCAP with custom settings
  hosts: windows_servers
  gather_facts: true
  
  vars:
    scap_content_file: "custom-benchmark.xml"
    scap_content_dir: "C:\\custom-oscap"
    oscap_report_dir: "C:\\custom-reports"
  
  tasks:
    - name: Install and configure OpenSCAP
      ansible.builtin.include_role:
        name: demo.windows.oscap
```

## What This Role Does

1. Checks disk space availability
2. Downloads and installs Visual C++ 2015-2022 Redistributable (x86) if not already present
3. Installs OpenSCAP using Chocolatey (if available) or via MSI installer
4. Verifies OpenSCAP installation
5. Creates SCAP content directory on target system
6. Copies SCAP benchmark file to target system
7. Verifies SCAP content was successfully copied

## Files Included

The role includes a Windows Server 2019 STIG SCAP benchmark file in the `files/` directory:
- `winserv2019-stig-scap-benchmark.xml`

You can add your own SCAP content files to the `files/` directory and reference them via the `scap_content_file` variable.

## License

MIT

## Author Information

This role was created for Ansible Product Demos.
