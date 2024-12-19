from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Visitor(models.Model):
    _name = 'visitor'
    _description = 'Visitor Record'

    name = fields.Char(string="Visitor Name", required=True)
    contact_number = fields.Char(string="Contact Number", required=True)
    email = fields.Char(string="Email")
    property_id = fields.Many2one('prop', string="Property", required=True)
    purpose = fields.Text(string="Purpose", required=True)
    scheduled_time = fields.Datetime(string="Scheduled Visit Time", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ], string="Approval Status", default='pending', required=True)

    @api.constrains('scheduled_time')
    def _check_scheduled_time(self):
        for record in self:
            if record.scheduled_time < fields.Datetime.now():
                raise ValidationError("Scheduled visit time must be in the future.")

    @api.model
    def search_visitor(self, property_id=None, status=None):
        """
        Search visitors by property or approval status.
        """
        domain = []
        if property_id:
            domain.append(('property_id', '=', property_id))
        if status:
            domain.append(('status', '=', status))
        return self.search_read(domain, ['name', 'scheduled_time', 'purpose', 'status'])

    def action_approve(self):
        for record in self:
            record.status = 'approved'

    def action_deny(self):
        for record in self:
            record.status = 'denied'
