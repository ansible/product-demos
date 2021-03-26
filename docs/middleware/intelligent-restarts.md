# Demo: Intelligent Reboot(middleware)

[Click here to return to master demo list](../../README.md#demo-repository)

## Table of Contents

* [Objective](#objective)
* [What business problem is solved?](#what-business-problem-is-solved)
* [Features show cased](#features-show-cased)
* [Video](#video)
* [Guide](#guide)

# Objective

Demonstrate how Ansible + Red Hat middleware can elevate common operational workflows.


# What business problem is solved?

- **speed to market**:
reducing human time to manually try and restart processes before having to reboot
- **reduce human error**:
automation of routine manual process
- **add intelligence**:
tracking state of last reboot outside the automation system and applying decision manager policies allow for intelligent operations

# Features show cased

- Workflows
- Decision Manager
- Stateful operations

During manual operations, it may require a human to troubleshoot
multiple services running on a server by restarting them. They might
need to make sure that they try to restart a service multiple times
before it works. Finally if the restarts don't work they might have to
reboot the system. This however may not be a simple decision. There
might be reasons why you might not want to reboot a node if you have
just rebooted it in the past hour for instance. This demo showcases
how such an use case can be handled, where state tracking outside the
automation system along with a decision engine instructs the
automation system whether to reboot or not.


# Video


# Guide

1. Login to Ansible Platform UX

2. Navigate to **Templates**

     ![job templates](../../images/templates.png)

3. Click the rocket next to **1 Install Dependencies** to set up the demo environment

     ![rocket launch](../../images/rocket.png)
This will also set up the Decision Manager, MySQL and FUSE containers on node3.

4. Ensure that the Decision Manager's GUI is reachable via http://<public_ip_node3>:8088. Set the following:
- Rule Name: Reboot

- Restart Minutes: 5

- Restart Count: 1

> You are telling decision manager that within a 5 minute window you may only reboot a node once.

5. Now ssh into nodes 1 and 2 and start the python listener by typing

``` bash
python3 -m http.server 8080
```

6. Navigate to **Templates** and run the **Intelligent restart
   workflow**. This is the first run. Since the Python listeners are up, this should pass.

7. Now from your terminal kill one of the python listeners.

8. Re-run the workflow. Click on the **Can this node be restarted?**
   Job Template. Look at the log output where Decision Manager's API
   response instructs Ansible to restart the server. Ansible proceeds
   to reboot and then run end-to-end tests once the systems are up.

9. Re-Run the workflow within the time interval you defined in
   step 4. The Python service is still down. However, this time, when
   Ansible queries Decision Manager whether it is ok to reboot,
   Decision Manager responds negatively. Ansible can now be configured
   to alert a human to intervene.

Explain how this can help elevate manual operational tasks that helpdesk can now handle. Also talk about other use cases where external state tracking/decision making might be required. e.g Disaster Recovery


8. Circle back and summarize

     You need to circle back what has been showcased to the [business reasons listed above](#what-business-problem-is-solved).  You are welcome to verify on the RHEL web nodes that the application was actually installed but unless you have a very technical audience you are going to start losing folks.  The real business solution here is automating away the boring and routine.



---
You have finished this demo.  [Click here to return to master demo list](../../README.md#demo-repository)
