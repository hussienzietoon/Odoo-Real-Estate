from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PropertyAvailability(models.Model):
    _name = 'property_availability'
    _description = 'Property Availability'

    property_id = fields.Many2one('prop', string='Property', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    is_available = fields.Boolean('Available', default=True)
    min_stay = fields.Integer('Minimum Stay (days)', default=1)
    max_stay = fields.Integer('Maximum Stay (days)', default=30)
    blackout_date = fields.Boolean('Blackout Date', default=False)

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.start_date >= record.end_date:
                raise ValidationError("Start date must be before the end date.")
