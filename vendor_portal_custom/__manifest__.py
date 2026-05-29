{
    'name': 'Vendor Portal Custom',
    'version': '1.0',
    'summary': 'Custom Portal for Vendors (Purchase Orders and Receipts)',
    'description': """
        This module provides a dedicated portal interface for Vendors.
        It allows vendors to view their Purchase Orders and associated incoming Warehouse Receipts.
        Separates from employee portal logic using `is_employee`.
    """,
    'category': 'Purchase/Purchase',
    'author': 'Duong Van',
    'depends': ['portal', 'purchase', 'stock', 'portal_custom'],
    'data': [
        'security/ir.model.access.csv',
        'security/vendor_security.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
