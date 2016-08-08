from openerp import models, fields, api
from openerp import SUPERUSER_ID
from openerp.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class portal_wizard_improvements(models.Model):
    _inherit = ['portal.wizard']
    
    def default_email_template(self):
        template_ids = self.env['mail.template'].search([('name', '=','Portal wizard user')])
        if template_ids:
            return self.env['mail.template'].browse(template_ids[0].id)
        return None
    
    email_template = fields.Many2one('mail.template', string='Email template', required=True, default=default_email_template)
    
    def _update_existing_ir_rules_for_keyuser_managment(self, cr, uid, ids=None, context=None):
        ir_rule_obj = self.pool.get('ir.rule')
        res_groups_obj = self.pool.get('res.groups')
        res_groups_portal_id = res_groups_obj.search(cr, uid, [('name', '=', 'Portal')])
        ir_rule_product_template_public_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Public product template')])
        ir_rule_portal_account_invoice_user_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Portal Personal Account Invoices')])
        ir_rule_portal_account_invoice_line_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Portal Invoice Lines')])
        ir_rule_portal_project_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Project: portal users: public, portal or following')])
        ir_rule_portal_issue_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Project/Issue: portal users: public or (portal and colleagues following) or (followers and following)')])
        ir_rule_portal_sale_order_user_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Portal Personal Quotations/Sales Orders')])
        ir_rule_portal_sale_order_line_rule_id = ir_rule_obj.search(cr, uid, [('name', '=', 'Portal Sales Orders Line')])

        
        if ir_rule_product_template_public_id and res_groups_portal_id:            
            query = """
                    DELETE FROM rule_group_rel
                    WHERE rule_group_id=%s
                    """
            cr.execute(query, [str(ir_rule_product_template_public_id[0])])
            
            query = """
                    INSERT INTO rule_group_rel (rule_group_id, group_id)
                    VALUES (%s,%s)
                    """
            cr.execute(query, (str(ir_rule_product_template_public_id[0]),str(res_groups_portal_id[0])))
        if ir_rule_portal_account_invoice_user_rule_id:
            domain_force = """[
            '|',
                '&',(user.partner_id.keyuser_accounting,'=',True),('partner_id','in',user.partner_id.parent_id.child_ids.ids),
                '|',
                    '&',(user.partner_id.keyuser_accounting,'=',True),('partner_id','=',[user.partner_id.parent_id.id]),
                    '|',('message_partner_ids','child_of',[user.partner_id.id]),('partner_id','=',[user.partner_id.id])
            ]
            
            """
            ir_rule_obj.write(cr, uid, [ir_rule_portal_account_invoice_user_rule_id[0]], {'domain_force': domain_force}, context=context)
        if ir_rule_portal_account_invoice_line_rule_id:
            domain_force = """
            [
            '|',
                '&',(user.partner_id.keyuser_accounting,'=',True),('partner_id','in',user.partner_id.parent_id.child_ids.ids),
                '|',
                    '&',(user.partner_id.keyuser_accounting,'=',True),('partner_id','=',[user.partner_id.parent_id.id]),
                    '|',('invoice_id.message_partner_ids','child_of',[user.partner_id.id]),('partner_id','=',[user.partner_id.id])
            ]
            
            """
            ir_rule_obj.write(cr, uid, [ir_rule_portal_account_invoice_line_rule_id[0]], {'domain_force': domain_force}, context=context)
            
            
        if ir_rule_portal_project_rule_id:
            domain_force = """
            [
            '|',   
                '&',('privacy_visibility', '=', 'portal'),('partner_id','=',[user.partner_id.id]), 
                '|',
                    ('privacy_visibility', '=', 'public'), 
                    '|',
                        '&',
                        ('privacy_visibility', '=', 'portal'),'&',
                        (user.partner_id.keyuser_project,'=',True),('partner_id','in',user.partner_id.parent_id.child_ids.ids),
                        '|',
                            '&',
                            ('privacy_visibility', '=', 'portal'),'&',
                            (user.partner_id.keyuser_project,'=',True),('partner_id','=',[user.partner_id.parent_id.id]), 
                            '|',
                                '&',
                                ('privacy_visibility', '=', 'portal'),
                                ('message_follower_ids', 'child_of', [user.partner_id.id]), 
                                '&',
                                ('privacy_visibility', '=', 'followers'),
                                ('message_follower_ids', 'in', [user.partner_id.id])
            ]
            """
            ir_rule_obj.write(cr, uid, [ir_rule_portal_project_rule_id[0]], {'domain_force': domain_force}, context=context)
        if ir_rule_portal_issue_rule_id:
            domain_force =  """
            [
            '|',   
                '&',('project_id.privacy_visibility', '=', 'portal'),('partner_id','=',[user.partner_id.id]), 
                '|',
                    ('project_id.privacy_visibility', '=', 'public'), 
                    '|',
                        '&',
                        ('project_id.privacy_visibility', '=', 'portal'),'&',
                        (user.partner_id.keyuser_project,'=',True),('partner_id','in',user.partner_id.parent_id.child_ids.ids),
                        '|',
                            '&',
                            ('project_id.privacy_visibility', '=', 'portal'),'&',
                            (user.partner_id.keyuser_project,'=',True),('partner_id','=',[user.partner_id.parent_id.id]), 
                            '|',
                                '&',
                                ('project_id.privacy_visibility', '=', 'portal'),
                                    '&',
                                    (user.partner_id.keyuser_project,'=',True),
                                    ('message_follower_ids', 'child_of', [user.partner_id.commercial_partner_id.id]), 
                                '&',
                                ('project_id.privacy_visibility', '=', 'followers'),
                                ('message_follower_ids', 'in', [user.partner_id.id])
            ]
            """
            ir_rule_obj.write(cr, uid, [ir_rule_portal_issue_rule_id[0]], {'domain_force': domain_force}, context=context)
        
        if ir_rule_portal_sale_order_user_rule_id:
            domain_force = """[
            '|',
                '&',(user.partner_id.keyuser_sales,'=',True),('partner_id','in',user.partner_id.parent_id.child_ids.ids),
                '|',
                    '&',(user.partner_id.keyuser_sales,'=',True),('partner_id','=',[user.partner_id.parent_id.id]),
                    '|',('message_partner_ids','child_of',[user.partner_id.id]),('partner_id','=',[user.partner_id.id])
            ]
            
            """
            ir_rule_obj.write(cr, uid, [ir_rule_portal_sale_order_user_rule_id[0]], {'domain_force': domain_force}, context=context)
        
        """
        if ir_rule_portal_sale_order_line_rule_id:
            "domain_force = 
            [
            '|',
                '&',(user.partner_id.keyuser_sales,'=',True),('order_id.partner_id','in',user.partner_id.parent_id.child_ids.ids),
                '|',
                    '&',(user.partner_id.keyuser_sales,'=',True),('order_id.partner_id','=',[user.partner_id.parent_id.id]),
                    '|',('order_id.message_follower_ids','child_of',[user.partner_id.id]),('order_id.partner_id','=',[user.partner_id.id])
            ]
            
            
            ir_rule_obj.write(cr, uid, [ir_rule_portal_sale_order_line_rule_id[0]], {'domain_force': domain_force}, context=context)
        """
    
class portal_wizard_user_improvements(models.Model):
    _inherit = ['portal.wizard.user']

    def _send_email(self, cr, uid, ids, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """

        wizard_user = self.browse(cr, uid, ids, context=context)
        res_partner = self.pool['res.partner']
        this_user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)
        if not this_user.email:
            raise UserError(_('You must have an email address in your User Preferences to send emails.'))

        # determine subject and body in the portal user's language
        user = wizard_user.user_id
        context = dict(context or {}, lang=user.lang)
        ctx_portal_url = dict(context, signup_force_type_in_url='')
        portal_url = res_partner._get_signup_url_for_action(cr, uid,
                                                            [user.partner_id.id],
                                                            context=ctx_portal_url)[user.partner_id.id]
        res_partner.signup_prepare(cr, uid, [user.partner_id.id], context=context)

        context.update({
            'dbname': cr.dbname,
            'portal_url': portal_url,
            'company': user.company_id.name,
            'db': cr.dbname,
            'name': user.name,
            'login': user.login,
            'signup_url': user.signup_url,
        })

        template_id = self.pool['ir.model.data'].xmlid_to_res_id(cr, uid, 'portal_improvements.email_template_portal_wizard')
        if template_id:
            self.pool['mail.template'].send_mail(cr, uid, template_id, wizard_user.id, force_send=True, context=context)
        else:
            _logger.warning("No email template found for sending email to the portal user")
        return True
