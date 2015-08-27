from openerp import models, fields, api

class account_analytic_account_portal(models.Model):
    _inherit = ['account.analytic.account']
    
    sla_rule_ids = fields.One2many(comodel_name='project.sla.rule',inverse_name='sla_id', related='contract_type.sla_id.sla_rule_ids', string="SLA rules", store=False)