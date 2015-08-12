from openerp import models, fields, api

class account_analytic_account_portal(models.Model):
    _inherit = ['account.analytic.account']
    sla_rule_ids = fields.One2many(comodel_name='project.sla.rule',inverse_name='sla_id', related='contract_type.sla_id.sla_rule_ids', string="SLA rules", store=False)
    portal_access = fields.Boolean(string="Portal access", default=True)
    
    #If you want to check the keyuser with the res.partner.category
    """
    def _get_portal_category(self):
        cr = self.env.cr
        uid = self.env.user.id
        category_ids = self.pool.get('res.partner.category').search(cr, uid, [('name','=','keyuser')])
        if category_ids:
            return self.pool.get('res.partner.category').browse(cr, uid, category_ids[0])
        else:
            category_id = self.pool.get('res.partner.category').create(cr,uid,{'name' : 'keyuser',})
            return self.pool.get('res.partner.category').browse(cr, uid, category_id)
    
    portal_category_id = fields.Many2one(comodel_name='res.partner.category', string="Portal category", default=_get_portal_category)
    """