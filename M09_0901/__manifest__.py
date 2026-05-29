# -*- coding: utf-8 -*-
{
    'name': 'MKT 0901 - Marketing Project & Promotion Approval',
    'version': '19.0.1.3.0',
    'summary': 'Marketing Project / Promotion Approval Form Management',
    'description': """
M09_0901: Marketing PAF Management
==================================================
Digitalizes the proposed - evaluation - approval - implementation - evaluation workflow
of new projects / promotions (PAF - Project / Promotion Approval Form).

Covers Phase 0 and Phase 1 (Master Data Extension).
    """,
    'category': 'Marketing/PAF',
    'author': 'PSM',
    'license': 'OEEL-1',
    'icon': '/M09_0901/static/description/icon.png',
    # PIF integration: depends on M08_P0801 (canonical); RSG_0801 is superseded.
    'depends': [
        'base',
        'mail',
        'hr',
        'product',
        'mrp',
        'stock',
        'account',
        'approvals',
        'loyalty',
        'purchase',
        'point_of_sale',
        'M02_P0200',
        'M08_P0801',
    ],
    'data': [
        'security/res_groups.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/approval_category_data.xml',
        'data/m08_pif_category_patch.xml',
        'data/res_groups_implied.xml',
        'data/promotion_legal_data.xml',
        'data/banner_config_data.xml',
        'data/mail_template_data.xml',
        'data/cron_data.xml',
        'reports/mkt_paf_valuation_report.xml',
        'views/actions.xml',
        'views/product_template_views.xml',
        'views/mkt_paf_banner_views.xml',
        'views/mkt_paf_request_views.xml',
        'views/mkt_paf_template_views.xml',
        'views/mkt_paf_evaluation_line_views.xml',
        'views/approval_request_views.xml',
        'views/mkt_paf_wizard_views.xml',
        'views/menus.xml',
        'views/mkt_paf_pspd_views.xml',
        'views/mkt_paf_valuation_report_views.xml',
        'views/mkt_paf_kanban_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
