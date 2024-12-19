from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Offer(models.Model):
    _name = 'offer'
    _description = 'Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    prop_id = fields.Many2one('prop', string='Property', required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                create_date_as_date = offer.create_date.date()
                delta = (offer.date_deadline - create_date_as_date).days
                offer.validity = max(0, delta)

    def accept_button(self):
        for record in self:
            if record.status == 'refused':
                raise ValidationError("Refused offer cannot be accepted.")
            record.status = 'accepted'
             # record.prop_id.buyer_id = record.partner_id
            record.prop_id.selling_price = record.price
            record.prop_id.status='rented'


    def refuse_button(self):
        for record in self:
            if record.status == 'accepted':
                raise ValidationError("Accepted offer cannot be refused.")
            record.status = 'refused'



    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.model
    def create(self, vals):
        # Access the property using the prop_id
        prop_id = self.env['prop'].browse(vals['prop_id'])



        # Ensure no offer is lower than an existing offer
        if prop_id.offer_id and vals['price'] <= max(prop_id.offer_id.mapped('price')):
            raise ValidationError("The offer price must be higher than any existing offer.")

        # Update the property state to 'offer_received'

        # Create the offer
        return super(Offer, self).create(vals)
