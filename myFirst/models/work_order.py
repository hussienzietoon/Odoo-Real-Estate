from odoo import models, fields, api, _

class WorkOrder(models.Model):
    _name = 'work_order'
    _description = 'Property Work Order'

    name = fields.Char(string="Work Order Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    prop_id = fields.Many2one('prop', string="Property", required=True)
    description = fields.Text(string="Issue Description")
    maintenance_id = fields.Many2one('maintenance', string="Maintenance Request")
    priority = fields.Selection(
        [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        string="Priority",
        default='medium'
    )
    assigned_personnel_id = fields.Many2one('res.users', string="Assigned Personnel")
    status = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        string="Status",
        default='draft'
    )
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    progress = fields.Float(string="Progress (%)", compute="_compute_progress", store=True)
    notes = fields.Text(string="Internal Notes")

    @api.depends('status')
    def _compute_progress(self):
        for record in self:
            if record.status == 'completed':
                record.progress = 100
            elif record.status == 'in_progress':
                record.progress = 50
            else:
                record.progress = 0

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work_order') or _('New')
        return super(WorkOrder, self).create(vals)

    def action_set_in_progress(self):
        self.status = 'in_progress'

    def action_set_completed(self):
        self.status = 'completed'

    def action_cancel(self):
        self.status = 'cancelled'
