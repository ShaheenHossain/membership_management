from odoo import models, fields

class MemberProvince(models.Model):
    _name = 'membership.province'
    _description = 'Province'

    name = fields.Char(string='Province', required=True)


class MemberTerritory(models.Model):
    _name = 'membership.territory'
    _description = 'Territory'

    name = fields.Char(string='Territory', required=True)
    province_id = fields.Many2one('membership.province', string='Province', required=True)



class MemberInterfederation(models.Model):
    _name = 'membership.interfederation'
    _description = 'Inter-Federation'

    name = fields.Char(string='Inter-Federation', required=True)


class MemberFederation(models.Model):
    _name = 'membership.federation'
    _description = 'Federation'

    name = fields.Char(string='Federation', required=True)
    interfederation_id = fields.Many2one('membership.interfederation', string='Inter-federation', required=True)



class MemberDistrict(models.Model):
    _name = 'membership.district'
    _description = 'District'

    name = fields.Char(string='District', required=True)
    federation_id = fields.Many2one('membership.federation', string='Federation', required=True)



class MemberSection(models.Model):
    _name = 'membership.section'
    _description = 'Section'

    name = fields.Char(string='Section', required=True)
    district_id = fields.Many2one('membership.district', string='District', required=True)



class MemberCellule(models.Model):
    _name = 'membership.cellule'
    _description = 'Cellule'

    name = fields.Char(string='Cellule', required=True)
    section_id = fields.Many2one('membership.section', string='Section', required=True)


class MemberSouscellule(models.Model):
    _name = 'membership.souscellule'
    _description = 'Sous-Cellule'

    name = fields.Char(string='Sous-Cellule', required=True)
    cellule_id = fields.Many2one('membership.cellule', string='Cellule', required=True)

