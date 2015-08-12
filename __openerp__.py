{
    'name': "AbAKUS portal improvements",
    'version': '1.0',
    'depends': ['account_analytic_analysis','account_analytic_account_improvements','sla', 'website_sale'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Contract',
    'description': 
    """
    This modules adds some improvements to the odoo portal. 
    
    REQUIRED
        - Go to Settings->Technical->Security->Record Rules
        - Search for "Public product template"
        - Remove from groups, "Portal" - it allows portal users to see products (ie.: generating report using products)
    
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
    """,
    'data': ['view/portal_wizard_view.xml',
             'view/portal_sale_view.xml',
             'view/portal_project_issue.xml',
             'view/res_partner_view.xml',
             'portal_wizard_user_email_template.xml',
             'security/portal_security.xml',
             'security/ir.model.access.csv',
            ],
}