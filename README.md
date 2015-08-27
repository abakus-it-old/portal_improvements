#This modules adds some improvements to the odoo portal. 
    
    Functionalities:
        - email template when inviting user to signup.
        - sales: 
            - adds contract menuitem
            - users can see contract informations, see SLA rules and download the service report.
        - project issue: users can see the description, the worklogs and the SLA.
        - keyuser (domain_force):
            - in a customer you can add the followings tags (categories):
                - keyuser_sales
                - keyuser_accounting
                - keyuser_project
            - this tags allows the customer to access to own, enterprise and contacts enterprise resources 
    
    This module modifies existing ir.rule for the keyuser management.
    
    HOW TO SET UP THE EMAIL TEMPLATE:

    The email template require following attributes:
    company (name of the company), name (name of the selected user), login (user odoo login), portal_url (url to access the portal), db (name of the database), signup_url

    Example:

    Dear %(name)s - Your Odoo account at %(company)s,
    You have been given access to %(company)s.
    Your login account data is:
    Username: %(login)s - Portal: %(portal_url)s - Database: %(db)s
    You can set or change your password via the following url:
    %(signup_url)s

This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.