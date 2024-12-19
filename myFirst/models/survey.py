from odoo import models, fields, api, _


class TenantSurvey(models.Model):
    _name = 'survey'
    _description = 'Tenant Satisfaction Survey'

    tenant_id = fields.Many2one('buyer', string="Tenant", required=True)
    prop_id = fields.Many2one('prop', string="Property", required=True)
    rating = fields.Selection([
        ('1', '1 - Very Poor'),
        ('2', '2 - Poor'),
        ('3', '3 - Average'),
        ('4', '4 - Good'),
        ('5', '5 - Excellent'),
    ], string="Rating", required=True)
    comments = fields.Text(string="Comments")
    survey_date = fields.Datetime(string="Survey Date", default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if not vals.get('survey_date'):
            vals['survey_date'] = fields.Datetime.now()
        return super(TenantSurvey, self).create(vals)
