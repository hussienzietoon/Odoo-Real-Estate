from odoo import models, fields,api

class Maintenance(models.Model):
    _name = 'maintenance'

    name = fields.Char(string='Task Disciption')
    prop_id = fields.Many2one('prop', string='Property')
    tenant_id = fields.Many2one('buyer', string="Tenant", required=True)
    work_order_ids = fields.One2many('work_order', 'maintenance_id', string="Work Orders")
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today, required=True)
    completion_date = fields.Date(string='Completion Date')
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='new', required=True)
    # New field for multilingual support
    is_frontend_multilang = fields.Boolean(
        string='Is Frontend Multilingual',
        default=False
    )
    @api.constrains('completion_date', 'request_date')
    def _check_dates(self):
        for record in self:
            if record.completion_date and record.completion_date < record.request_date:
                raise ValidationError("Completion Date cannot be earlier than Request Date.")

    @api.model
    def create(self, vals):
        maintenance = super(Maintenance, self).create(vals)

        if maintenance.prop_id:
            maintenance.prop_id.status = 'under_maintenance'

        return maintenance