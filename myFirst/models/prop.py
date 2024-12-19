from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare

class Prop(models.Model):
    _name = 'prop'
    _description = 'Prop'
    _order = 'id desc'

    name = fields.Char(default='', required=True)
    address = fields.Char(string='Address')
    type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ], string='Type', required=True)
    size = fields.Float(string='Size')
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Float(string='Living Area')
    garden_area = fields.Float(string='Garden Area', default=10)
    active = fields.Boolean(default=True)
    total_area = fields.Float("Total Area", compute='_compute_total_area', store=True)
    owner_id = fields.Many2one('owner')
    tenant_id = fields.Many2one('buyer', string='Buyer')
    tag_id = fields.Many2many('tag', string='Cozy')
    property_media_ids= fields.One2many( 'property_media','prop_id', string='Property Media')
    offer_id = fields.One2many('offer', 'prop_id', string='Offers')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer', store=True)
    maintenance_ids = fields.One2many('maintenance', 'prop_id', string='Maintenance')
    maintenance_count = fields.Integer(string='Maintenance Count', compute='_compute_maintenance_count')
    lease_ids = fields.One2many('lease', 'prop_id', string="Leases")
    documents = fields.One2many('document', 'property_id', string="Documents")
    availability_ids = fields.One2many('property_availability', 'property_id', string='Availability')
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('under_maintenance', 'Under Maintenance'),
    ], default='available', required=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')

    @api.depends("offer_id.price")
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = max(rec.offer_id.mapped('price'), default=0)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    def under_maintenance_button(self):
        for record in self:
            if record.status == 'rented':
                raise ValidationError("You cannot maintenance a property that has already been rented.")
            record.status = 'under_maintenance'

    def rented_button(self):
        for record in self:
            if record.status == 'under_maintenance':
                raise ValidationError("You cannot rent a property that is under maintenance.")
            record.status = 'rented'

    def available_button(self):
        for record in self:
            record.status = 'available'

    _sql_constraints = [
        ('expected_price_positive', 'CHECK (expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price_non_negative', 'CHECK(selling_price>=0)', 'The selling price must be positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            if float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_rounding=0.01
            ) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for record in self:
            if record.status not in ['new', 'cancel']:
                raise ValidationError("You can only delete properties that are in 'New' or 'Canceled' status.")

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        if self._context.get('search_default_location'):
            args.append(('address', 'ilike', self._context['search_default_location']))
        return super(Prop, self).search(args, offset=offset, limit=limit, order=order)

    @api.depends('maintenance_ids')
    def _compute_maintenance_count(self):
        for rec in self:
            rec.maintenance_count = len(rec.maintenance_ids)
