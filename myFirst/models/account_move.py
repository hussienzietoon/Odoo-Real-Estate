from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    lease_id = fields.Many2one('lease', string="Lease")
