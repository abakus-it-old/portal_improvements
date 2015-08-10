from openerp import models, fields, api
from openerp import SUPERUSER_ID

class portal_wizard_improvements(models.Model):
    _inherit = ['portal.wizard']
    
    def default_email_template(self):
        cr = self.env.cr
        uid = self.env.user.id
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=','Portal wizard user')]) 
        if template_ids:
            return template_ids[0]
        return False
    
    email_template = fields.Many2one('email.template', string='Email template', required=True, default=default_email_template)
    
class portal_wizard_user_improvements(models.Model):
    _inherit = ['portal.wizard.user']
       
    def _send_email(self, cr, uid, wizard_user, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """
        res_partner = self.pool['res.partner']
        this_context = context
        this_user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)
        if not this_user.email:
            raise osv.except_osv(_('Email Required'),
                _('You must have an email address in your User Preferences to send emails.'))

        # determine subject and body in the portal user's language
        user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
        context = dict(this_context or {}, lang=user.lang)
        ctx_portal_url = dict(context, signup_force_type_in_url='')
        portal_url = res_partner._get_signup_url_for_action(cr, uid, [user.partner_id.id], context=ctx_portal_url)[user.partner_id.id] 
        res_partner.signup_prepare(cr, uid, [user.partner_id.id], context=context)

        data = {
            'company': this_user.company_id.name,
            'portal': wizard_user.wizard_id.portal_id.name,
            'welcome_message': wizard_user.wizard_id.welcome_message or "",
            'db': cr.dbname,
            'name': user.name,
            'login': user.login,
            'signup_url': user.signup_url,
            'portal_url': portal_url,
        }
        
        #use new email template
        email_template_obj = self.pool.get('email.template')
        values = email_template_obj.generate_email(cr, uid, wizard_user.wizard_id.email_template.id, wizard_user.id, context=context)
        #values['subject'] = subject; values['body_html'] = body_html; values['body'] = body_html       

        mail_mail = self.pool.get('mail.mail')
        mail_values = {
            'email_from': this_user.email,
            'email_to': user.email,
            'subject': values['subject'] % data,
            'body_html': values['body_html'] % data,
            'state': 'outgoing',
            'type': 'email',
        }

        mail_id = mail_mail.create(cr, uid, mail_values, context=this_context)
        return mail_mail.send(cr, uid, [mail_id], context=this_context)