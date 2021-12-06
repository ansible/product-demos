# Demo: Chocolatey Config

[Click here to return to master demo list](../../README.md#demo-repository)

## Table of Contents

- [Demo: Chocolatey Config](#demo-chocolatey-config)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [What business problem is solved?](#what-business-problem-is-solved)
  - [Features show cased](#features-show-cased)
  - [Guide](#guide)

## Objective

Demostrate how Anisble can be used not only to enable or disable Chocolatey configuration parameters but to set specifc values for those parameters

## What business problem is solved?

- **Operational Efficiency**:
  Ansible provides the ability to save dozen to hundreds of hours of reconfiguration work by systems admins through the configuration automation
- **Increase Compliance**:
  Ansible provides the means to get and stay in compliance throughout all your systems

## Features show cased

- Configuration as code
- Self Service IT - Surveys

For description of these and other features of the Red Hat Ansible Automation Platform please refer to the [features README](../features.md)

## Guide

1. Login to Ansible Platform UX

2. Navigate to **Templates**

     ![job templates](../images/templates.png)

3. Click the rocket next to **INFRASTRUCTURE / Chocolatey Features Config** to launch the Job

     ![rocket launch](../images/rocket.png)

4. The survey will prompt you with 3 questions. What Parameter you want to change, whether you want to make it present or absent in the config, and the value for that paramater.

     ![survey choice](../images/choco_config/choco_config_survey.jpeg)

5. Choose a parameter. Select if you want to make it present or absent in the config. Finally, add the value for that parameter and press **NEXT**
   Note: These are just a few of the parameters they can add to the list. For these 3 see below for correct format for response.

   - **proxyUser** single text line such as drojas or student25
   - **commandExecutionTimeoutSeconds** integer value. 0 is infinite, 2700 is default, recomendation is 14400
   - **cacheLocation** text of a path to location on windows node such as c:\chocolatey_temp2

   For more info on possible parameter see [Chocolatey Documentation](https://chocolatey.org/docs/chocolatey-configuration)

     ![survey preview](../images/choco_config/choco_config_survey_preview.jpeg)

     Explain to audience what is happening here depending on audience persona

    **Persona A**: Technical audience that has written Ansible Playbooks before:
    Surveys create variables that the Job can use within Ansible Playbooks. This gives you the ability to create one playbook that can be used to enable or disable and set configuration values instead of having to create or maintain many job templates. Again saving you time and effort to write seperate playbooks for each use case.  In the screenshot you will see the variables are named **config-item**, **state**, and **value**  with values of  **cacheLocation**, **present**, and **c:\chocolatey_temp2**. These will be treated as extra vars and as such overirde any variables from any other source such as the playbook itself

    **Persona B**: Decision maker audience, IT manager or above:
    reiterate business values above.  This allows a systems admin to automate the reconfiguration of Chocolatey in a low risk repeatable manner.  This will free up IT staff for larger more mission critical projects all while reducing risk to your production operations. In the event that your IT process does not allow the Red Hat Ansible Automation Platform to be the front end, it has a rich and powerful API that can work with existing workflows such as ServiceNow.

6. Execute the job by pressing the green **LAUNCH** button

7. Explain what is happening:

     - Job has started executed in the background.  The user can navigate off this page and the job will continue to execute.
     - On the left is the **Job Details Pane** labeled simply with **DETAILS**.  This information is logged and tells you who, what, when and how.
       - **who** - who launched the job, in this example is the admin user
       - **what** - the project and Ansible Playbook used, and which credential to login to the infrastructure
       - **when** - time stamps for start, end and duration of the job run.
       - **how** - the job status (pass, fail), enviornment and execution node
     - The larger window on the right is the **Standard Out Pane**.  This provides the same console output the user would be used to on the command-line for troubleshooting purposes.  Some important takeways to showcase are:
       - aggregate info is at the top including the amount of Plays, tasks, hosts and time duration.
       - this pane can be expanded to take up entire browser window
       - Ansible Playbook can be downloaded for troubleshooting purposes
       - **click on task output** to show them task-by-task JSON output that can be used for troubleshooting or just getting additional information
       ![task breakdown](../images/choco_config/choco_config_task_output.jpeg)

8. Circle back and summarize

     You need to circle back what has been showcased to the [business reasons listed above](#what-business-problem-is-solved).  You are welcome to verify on the Windows hosts that the configuration was actually changed but unless you have a very technical audience you are going to start losing folks.  The real business solution here is automating away the mundane and repetative.

---
You have finished this demo.  [Click here to return to master demo list](../../README.md#demo-repository)
