from odoo import models, fields

class Member(models.Model):
    _name = 'membership.member'
    _description = 'Membership Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    member_type = fields.Selection([
        ('individual', 'Individual'),
        ('organization', 'Organization')
    ], string='Member Type', default='individual')
    id_number = fields.Char(string='ID Number')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    location = fields.Char(string='Location')
    role = fields.Selection([
        ('supporter', 'Supporter'),
        ('active', 'Active Member'),
        ('volunteer', 'Volunteer'),
        ('executive', 'Executive')
    ], string='Role', default='supporter')
    status = fields.Selection([
        ('new', 'New'),
        ('verified', 'Verified'),
        ('resigned', 'Resigned'),
        ('suspended', 'Suspended')
    ], string='Status', default='new')
    join_date = fields.Date(string='Join Date', default=fields.Date.today)
    renewal_date = fields.Date(string='Renewal Date')
    resignation_date = fields.Date(string='Resignation Date')
    suspension_date = fields.Date(string='Suspension Date')
    communication_preference_ids = fields.One2many('membership.communication.preference', 'member_id', string='Communication Preferences')


