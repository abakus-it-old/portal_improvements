from openerp import models, fields, api

class res_partner_portal(models.Model):
    _inherit = ['res.partner']
    
    keyuser_sales = fields.Boolean(string="Portal Sales Keyuser", default=False)
    keyuser_project = fields.Boolean(string="Portal Project Keyuser", default=False)
    keyuser_accounting = fields.Boolean(string="Portal Accounting Keyuser", default=False)