{
    'name': 'myFirst',
    'version': '1.0',
    'summary': 'Training model',
    'description': """
        This is My first model.
    """,
    'author': 'HussienMohamed',
    'website': 'https://www.yourwebsite.com',
    'category': 'Tools',
    'depends': ['base', 'web', 'website', 'account'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/prop_view.xml',
        'views/owner_view.xml',
        'views/type_view.xml',
        'views/buyer_view.xml',
        'views/tag.xml',
        'views/offer_view.xml',
        'views/transaction_view.xml',
        'views/maintenance_view.xml',
        'views/portal_templates.xml',
        'views/lease_view.xml',
        'views/document_view.xml',
        'views/visitor_view.xml',
        'views/work_order_view.xml',
        'views/survey_view.xml',
        'views/property_availability.xml',
        'views/property_media.xml',
    ],

    'controllers': [
        'controllers/portal.py',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
