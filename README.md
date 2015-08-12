#This modules adds some improvements to the odoo portal. 
    
REQUIRED
    - Go to Settings->Technical->Security->Record Rules
    - Search for "Public product template"
    - Remove from groups, "Portal"
    - It allows generating a report using products

Functionalities:
    - email template when inviting user to signup.
    - sales: 
        - adds contract menuitem
        - users can see contract informations, see SLA rules and download the service report.
        - domain: 
            - standard users can only access to their resources
            - "keyuser" (new in res.partner) -> access to own, enterprise and contacts enterprise resources.
    - project issue: users can see the description, the worklogs and the SLA.

This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.