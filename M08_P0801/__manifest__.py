{
    'name': "RSG PIF Management (0801)",
    'summary': "RSG Department - Product Initiation Forms Management",
    'description': """
        RSG PIF Management Module.

        Base module for PIF Implementation workflow:
        - PIF Implementation workflow (RSG → IT → Master Data → Lab Test → Pilot)
        - Finished Good WRIN generation
        - Future: Other PIF types (Marketing, S&I, Digital, Supply Chain)

        IMPORTANT: Do NOT install together with RSG_0801_pif_management.
        Both modules define the same models (pif.object, etc.) with conflicting
        selection values. M08_P0801 is the canonical version; RSG_0801_pif_management
        is superseded. SC_0402_supplier_management depends on RSG_0801 and runs
        as a separate stack.
    """,
    'author': "MongTuyen",
    'version': '0.2',
    'category': 'Supply Chain/RSG',
    'depends': ['base', 'mail', 'product', 'mrp', 'approvals', 'hr'],
    'external_dependencies': {
        'python': ['openpyxl'],
    },
    'data': [
        'security/pif_groups.xml',
        'security/ir.model.access.csv',
        'data/pif_sequence.xml',
        'data/pif_data.xml',
        'report/pif_report_action.xml',
        'report/pif_valuation_report.xml',
        'views/pif_views.xml',
    ],
    'installable': True,
    'application': False, 
}
