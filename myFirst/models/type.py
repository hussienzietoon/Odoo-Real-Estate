
from odoo import models, fields

class Type(models.Model):
    _name = 'type'
    _description = 'Type'
    _order = ' sequence asc,name'
    name = fields.Char(string='Property Type')
    sequence = fields.Integer(string='Sequence', default=10)

    # prop_id=fields.One2many('prop','type_id',string='Properties')
    # _sql_constraints = [
    #     ('unique_type_name', 'unique(name)', 'Type Prop must be unique.')
    # ]
