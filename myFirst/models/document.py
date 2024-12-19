from odoo import models, fields, api
from datetime import date, timedelta

class Document(models.Model):
    _name = 'document'
    _description = 'Legal Document'

    name = fields.Char(string="Document Name", required=True)
    description = fields.Text(string="Description")
    property_id = fields.Many2one('prop', string="Property", required=True)
    document_type = fields.Selection([
        ('photo', 'Photo'),
        ('floor_plan', 'Floor Plan'),
        ('inspection_report', 'Inspection Report'),
        ('permit', 'Permit'),
        ('license', 'License'),
        ('safety_certificate', 'Safety Certificate'),
        ('other', 'Other'),
    ], string="Document Type", required=True, default='other')
    expiry_date = fields.Date(string="Expiry Date")
    attachment = fields.Binary(string="Attachment", required=True)
    attachment_filename = fields.Char(string="Filename")
    uploaded_by = fields.Many2one('res.users', string="Uploaded By", default=lambda self: self.env.user)

    @api.model
    def search_documents(self, property_id=None, document_type=None):
        """
        Search for documents based on property or document type.
        """
        domain = []
        if property_id:
            domain.append(('property_id', '=', property_id))
        if document_type:
            domain.append(('document_type', '=', document_type))
        return self.search_read(domain, ['name', 'document_type', 'attachment_filename', 'uploaded_by'])

    @api.model
    def send_expiry_reminders(self):
        """
        Check for documents nearing expiry and notify responsible users.
        """
        today = date.today()
        reminder_date = today + timedelta(days=7)  # Notify 7 days before expiry
        expiring_docs = self.search([('expiry_date', '<=', reminder_date), ('expiry_date', '>=', today)])
        for doc in expiring_docs:
            # Example notification to uploader
            message = f"Reminder: The document '{doc.name}' for property '{doc.property_id.name}' will expire on {doc.expiry_date}."
            doc.uploaded_by.notify_info(message)
