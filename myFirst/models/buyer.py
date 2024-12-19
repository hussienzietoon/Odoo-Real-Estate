from odoo import models, fields,api

class Buyer(models.Model):
    _name = 'buyer'
    name = fields.Char(string='Tenant')
    contact = fields.Char(string='Contact')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    rent = fields.Float(string='Rent')
    lease_ids = fields.One2many('lease', 'tenant_id', string="Leases")
    user_id = fields.Many2one('res.users', string="Related User", required=True)
