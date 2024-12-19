from odoo import models, fields, api, exceptions
from datetime import date

class RealEstateLease(models.Model):
    _name = 'lease'
    _description = 'Lease Agreement'

    name = fields.Char(string="Lease Name", required=True)
    tenant_id = fields.Many2one('buyer', string="Tenant", required=True)
    prop_id = fields.Many2one('prop', string="Property", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    rent_amount = fields.Float(string="Rent Amount", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], string="Status", default='draft', tracking=True)
    duration_days = fields.Integer(string="Lease Duration (Days)", compute="_compute_duration", store=True)
    notes = fields.Text(string="Additional Notes")

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """Calculate lease duration in days."""
        for record in self:
            if record.start_date and record.end_date:
                duration = (record.end_date - record.start_date).days
                record.duration_days = duration if duration > 0 else 0
            else:
                record.duration_days = 0

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Ensure start_date is before end_date."""
        for record in self:
            if record.start_date >= record.end_date:
                raise exceptions.ValidationError("The start date must be earlier than the end date.")

    def action_activate(self):
        """Set lease to active if in draft state and dates are valid."""
        for record in self:
            if record.state != 'draft':
                raise exceptions.UserError("Only leases in draft state can be activated.")
            if record.start_date <= date.today():
                record.state = 'active'
            else:
                raise exceptions.UserError("The lease cannot be activated before its start date.")

    def action_expire(self):
        """Manually expire a lease."""
        for record in self:
            if record.state == 'active':
                record.state = 'expired'
            else:
                raise exceptions.UserError("Only active leases can be expired.")
    def reset_action(self):
        for record in self:
            record.state = 'draft'
    @api.model
    def _auto_check_expired_leases(self):
        """Automated cron method to check and expire leases."""
        today = date.today()
        expired_leases = self.search([('end_date', '<', today), ('state', '=', 'active')])
        for lease in expired_leases:
            lease.state = 'expired'

    # invoice_ids = fields.One2many('account.move', 'lease_id', string="Invoices")  # Add this line to link invoices
    #
    # @api.model
    # def create(self, vals):
    #     lease = super(RealEstateLease, self).create(vals)
    #
    #     # Create invoice for the lease
    #     invoice_vals = {
    #         'partner_id': lease.tenant_id.id,
    #         'move_type': 'out_invoice',  # Customer invoice
    #         'invoice_date': fields.Date.context_today(self),
    #         'invoice_line_ids': [(0, 0, {
    #             'product_id': 1,  # Assuming a product "Rent" exists with ID 1
    #             'quantity': 1,
    #             'price_unit': lease.rent_amount,
    #         })],
    #     }
    #     invoice = self.env['account.move'].create(invoice_vals)
    #
    #     # Link invoice to lease (optional)
    #     lease.invoice_ids = [(4, invoice.id)]  # This links the invoice to the lease
    #
    #     return lease
