# -*- coding: utf-8 -*-
{
    'name': 'M00_P9990_PSM_PARAMATER',
    'version': '1.0',
    'summary': 'Custom system parameters for PSM configuration',
    'category': 'Technical',
    'author': 'PSM',
    'description': """
M00_P9990_PSM_PARAMATER
=======================
A custom key-value parameter store, similar to Odoo's System Parameters (ir.config_parameter),
but independent and managed separately.

Use this module to declare and manage PSM-specific configuration parameters.
The menu is located under Settings > Technical > Parameters > PSM Parameters.
    """,
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/psm_parameter_views.xml',
        'data/psm_parameters_0213_0214_0215.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OEEL-1',
}
