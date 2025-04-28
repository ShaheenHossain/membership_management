from odoo import models, fields

class MembershipTier(models.Model):
    _name = 'membership.tier'
    _description = 'Membership Tier'

    name = fields.Char(string='Tier Name', required=True)
    description = fields.Text(string='Description')

