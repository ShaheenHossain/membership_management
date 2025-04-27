from odoo import models, fields

class CommunicationPreference(models.Model):
    _name = 'membership.communication.preference'
    _description = 'Communication Preference'

    member_id = fields.Many2one('membership.member', string='Member')
    preference_type = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('call', 'Call')
    ], string='Preference Type')
