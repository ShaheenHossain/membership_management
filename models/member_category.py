from odoo import models, fields

class MemberCategory(models.Model):
    _name = 'membership.member.category'
    _description = 'Member Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')