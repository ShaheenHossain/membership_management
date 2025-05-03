
from odoo import models, fields, api
import random

class Partner(models.Model):
    _inherit = 'res.partner'


    card_purchased = fields.Boolean(string='Card Purchased', default=False)
    last_contribution_date = fields.Date(string='Last Contribution Date')

    # Additional personal fields
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')

    date_of_birth = fields.Date(string='Date of Birth')
    place_of_birth = fields.Char(string='Place of Birth')
    nationality = fields.Many2one('res.country', string='Nationality')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status')

    profession = fields.Char(string='Profession')

    type = fields.Selection([
        ('invoice', 'Invoice Address'),
        ('delivery', 'Delivery Address'),
        ('other', 'Other Address'),
    ], string='Address Type', default='other', required=True)



    member_type = fields.Selection([
        ('individual', 'Individual'),
        ('organization', 'Organization')
    ], string='Member Type', default='individual')


    membership_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Membership Status', compute='_compute_membership_status', store=True)

    status = fields.Selection([
        ('new', 'New'),
        ('verified', 'Verified'),
        ('exited', 'Exited')
    ], string='Status', default='new')

    join_date = fields.Date(string='Join Date', default=fields.Date.today)

    exit_reason = fields.Selection([
        ('death', 'Death'),
        ('expelled', 'Expelled'),
        ('resigned', 'Resigned')
    ], string='Exit Reason')

    communication_preference_ids = fields.One2many('membership.communication.preference', 'member_id', string='Communication Preferences')

    role = fields.Selection([
        ('supporter', 'Supporter'),
        ('active', 'Active Member'),
        ('volunteer', 'Volunteer'),
        ('executive', 'Executive')
    ], string='Role', default='supporter')

    reference = fields.Many2one('res.partner', string='Reference')
    member_category_id = fields.Many2one('membership.member.category', string='Member Category')
    id_number = fields.Char(string='ID Number')
    membership_number_auto = fields.Char(string='Membership Number', readonly=True, copy=False, index=True)

    @api.model
    def create(self, vals):
        if not vals.get('membership_number_auto'):
            vals['membership_number_auto'] = self._generate_membership_number()
        return super().create(vals)

    def _generate_membership_number(self):
        """Generate a unique 10-digit membership number"""
        while True:
            number = str(random.randint(1000000000, 9999999999))
            if not self.search([('membership_number_auto', '=', number)], limit=1):
                return number

    @api.depends('card_purchased', 'last_contribution_date')
    def _compute_membership_status(self):
        today = fields.Date.today()
        for rec in self:
            if rec.card_purchased and rec.last_contribution_date:
                delta = (today - rec.last_contribution_date).days
                rec.membership_status = 'active' if delta <= 90 else 'inactive'
            else:
                rec.membership_status = 'inactive'