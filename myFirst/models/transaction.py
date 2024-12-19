from odoo import models, fields

class Transaction(models.Model):
    _name = 'transaction'
    date = fields.Datetime(string='Date')
    amount = fields.Float(string='Amount')
    prop_id = fields.Many2one('prop', string='Property')
    parties_involved=fields.Many2many('buyer', string='Parties')
