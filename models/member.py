# from odoo import models, fields
#
# class Member(models.Model):
#     _name = 'membership.member'
#     _description = 'Membership Member'
#     _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
#
#     name = fields.Char(string='Name', required=True)
#     image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
#     avatar_128 = fields.Image("Avatar", related="image_1920", max_width=128, max_height=128, store=True)
#
#     member_type = fields.Selection([
#         ('individual', 'Individual'),
#         ('organization', 'Organization')
#     ], string='Member Type', default='individual')
#     id_number = fields.Char(string='ID Number')
#     email = fields.Char(string='Email')
#     phone = fields.Char(string='Phone')
#     location = fields.Char(string='Location')
#     role = fields.Selection([
#         ('supporter', 'Supporter'),
#         ('active', 'Active Member'),
#         ('volunteer', 'Volunteer'),
#         ('executive', 'Executive')
#     ], string='Role', default='supporter')
#     status = fields.Selection([
#         ('new', 'New'),
#         ('verified', 'Verified'),
#         ('resigned', 'Resigned'),
#         ('suspended', 'Suspended')
#     ], string='Status', default='new')
#     join_date = fields.Date(string='Join Date', default=fields.Date.today)
#     renewal_date = fields.Date(string='Renewal Date')
#     resignation_date = fields.Date(string='Resignation Date')
#     suspension_date = fields.Date(string='Suspension Date')
#     communication_preference_ids = fields.One2many('membership.communication.preference', 'member_id', string='Communication Preferences')
#
#     reference = fields.Many2one('membership.member', string='Reference')
#     member_category_id = fields.Many2one('membership.member.category', string='Member Category 02')
#
#
#     member_category = fields.Selection([
#         ('inter_federation', 'Inter-federation'),
#         ('federation', 'Federation'),
#         ('district', 'District'),
#         ('section', 'Section'),
#         ('cellule', 'Cellule'),
#         ('sous_cellule', 'Sous-cellule')
#     ], string='Member Category')

from odoo import models, fields, api
import random

class Member(models.Model):
    _name = 'membership.member'
    _description = 'Membership Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    image_1920 = fields.Image("Photo", help="Member's photo for the membership card")

    # Auto-generated unique 10-digit membership number
    membership_number = fields.Char(string='Membership Number', readonly=True, copy=False, index=True)

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

    # Simplified member status logic
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

    reference = fields.Many2one('membership.member', string='Reference')

    member_category_id = fields.Many2one('membership.member.category', string='Member Category')

    # member_category = fields.Selection([
    #     ('inter_federation', 'Inter-federation'),
    #     ('federation', 'Federation'),
    #     ('district', 'District'),
    #     ('section', 'Section'),
    #     ('cellule', 'Cellule'),
    #     ('sous_cellule', 'Sous-cellule')
    # ], string='Member Category')

    # --- Membership logic ---
    card_purchased = fields.Boolean(string='Card Purchased', default=False)
    last_contribution_date = fields.Date(string='Last Contribution Date')

    @api.model
    def create(self, vals):
        if not vals.get('membership_number'):
            vals['membership_number'] = self._generate_membership_number()
        return super().create(vals)

    def _generate_membership_number(self):
        """Generate a unique 10-digit membership number"""
        while True:
            number = str(random.randint(1000000000, 9999999999))
            if not self.search([('membership_number', '=', number)], limit=1):
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



class Partner(models.Model):
    _inherit = 'res.partner'


    card_purchased = fields.Boolean(string='Card Purchased', default=False)
    last_contribution_date = fields.Date(string='Last Contribution Date')

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