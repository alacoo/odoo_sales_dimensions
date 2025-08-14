{
    'name': 'sale_dimensions',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add length, width, height dimensions to sale order lines',
    'description': '''
        This module adds dimension fields (Length, Width, Height) to sale order lines
        and automatically calculates quantity based on these dimensions.
    ''',
    'author': 'Tu Nombre',
    'website': 'https://www.tuempresa.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/sale_order_portal_templates.xml',
        'views/reports/sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}