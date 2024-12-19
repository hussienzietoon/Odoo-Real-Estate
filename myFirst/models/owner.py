from odoo import models, fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(string='Salesman')
    contact = fields.Char(string='Contact')
    ownership_persentage = fields.Char(string='Ownership Percentage')
