from openerp import models, fields, api

class res_partner_portal(models.Model):
    _inherit = ['res.partner']
    keyuser = fields.Boolean(string="Keyuser", default=False)