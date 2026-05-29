# -*- coding: utf-8 -*-
from odoo import models, fields

class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    is_mkt_paf = fields.Boolean(
        string='Là quy trình PAF',
        default=False
    )

    mkt_paf_stage = fields.Selection([
        ('head', 'Head Review'),
        ('clevel', 'C-Level Review')
    ], string='Giai đoạn PAF')
