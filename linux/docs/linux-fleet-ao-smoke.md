# Fleet Automation Orchestrator smoke service

`fleet_ao_smoke.yml` provides the visible state change used by the
`aap-demo` Fleet and Automation Orchestrator integration. It starts
`aap-demo-fleet-smoke.service` on the selected Linux host, then verifies that
the unit is active. The transient service sleeps for five minutes and systemd
collects it afterwards.

Run it only through the Fleet-scoped AAP job template created by the
integration. The playbook needs a host with systemd and permission to use
`systemd-run`.
