from odoo import http
from odoo.http import request

class RealEstatePortal(http.Controller):

    @http.route(['/my/leases'], type='http', auth="user", website=True)
    def portal_my_leases(self):
        tenant = request.env.user.partner_id
        leases = request.env['lease'].sudo().search([('tenant_id', '=', tenant.id)])
        return request.render('myFirst.portal_my_leases', {'leases': leases})

    @http.route(['/my/maintenance'], type='http', auth='user', website=True)
    def portal_maintenance_requests(self):
        tenant = request.env['buyer'].search([('user_id', '=', request.env.user.id)], limit=1)
        requests = request.env['maintenance'].search([('tenant_id', '=', tenant.id)])
        website = request.env['website'].get_current_website()
        return request.render('myFirst.portal_maintenance_requests', {
            'tenant': tenant,
            'requests': requests,
            'website': website,
        })

    @http.route(['/my/maintenance/new'], type='http', auth='user', website=True, csrf=False)
    def new_maintenance_request(self, **kwargs):
        if kwargs.get('submit'):
            tenant = request.env['buyer'].search([('user_id', '=', request.env.user.id)], limit=1)
            request.env['maintenance'].create({
                'name': kwargs.get('name'),
                'tenant_id': tenant.id,
                'prop_id': kwargs.get('prop_id'),
                'description': kwargs.get('description'),
            })
            return request.redirect('/my/maintenance')
        tenant = request.env['buyer'].search([('user_id', '=', request.env.user.id)], limit=1)
        properties = request.env['prop'].search([('tenant_id', '=', tenant.id)])
        website = request.env['website'].get_current_website()
        return request.render('myFirst.portal_new_maintenance_request', {
            'tenant': tenant,
            'properties': properties,
            'website': website,
        })

    @http.route('/my/survey', type='http', auth='user', website=True)
    def survey(self):
        # Get the tenant (buyer) based on the logged-in user
        tenant = request.env['buyer'].search([('user_id', '=', request.env.user.id)], limit=1)

        if not tenant:
            return request.render('myFirst.survey_not_available')  # Error page if no tenant found

        # Get the properties the tenant is associated with
        properties = request.env['prop'].search([('tenant_id', '=', tenant.id)])

        # Render the survey form for the tenant to fill out
        return request.render('myFirst.portal_survey_form', {
            'tenant': tenant,
            'properties': properties,
        })

    @http.route('/my/survey/submit', type='json', auth='user', website=True)
    def submit_survey(self, tenant_id, prop_id, rating, comments):
        # Check if all required fields are provided
        if not tenant_id or not prop_id or not rating:
            return {'status': 'error', 'message': 'Missing required fields'}

        # Create the survey record in the database
        request.env['survey'].create({
            'tenant_id': tenant_id,
            'prop_id': prop_id,
            'rating': rating,
            'comments': comments,
        })

        # Return a success response
        return {'status': 'success', 'message': 'Survey submitted successfully'}
