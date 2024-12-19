from odoo import models, fields

class Tag(models.Model):
    _name = 'tag'
    _description = 'Tag'
    _order = 'name'
    name = fields.Char(string='Cozy')
    color = fields.Integer(string='Color')


    _sql_constraints = [
        ('unique_tag_name', 'unique(name)','Tag name must be unique.')
    ]