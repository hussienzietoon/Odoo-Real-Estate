from odoo import models, fields, api

class PropertyMedia(models.Model):
    _name = 'property_media'
    _description = 'Property Media'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    media_file = fields.Binary("Media File", attachment=True, required=True)
    media_type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video')
    ], string="Media Type", default='image')
    category_id = fields.Char( string="Category")
    tags = fields.Many2many('tag', string="Tags")
    prop_id = fields.Many2one('prop', string="Property", required=True)