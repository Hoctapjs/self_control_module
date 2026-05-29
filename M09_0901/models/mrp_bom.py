# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    paf_can_use = fields.Boolean(
        string='Recipe sẵn sàng PAF',
        default=False,
        tracking=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        store=True,
        string='Currency'
    )

    paf_total_raw_cost = fields.Monetary(
        string='Tổng chi phí NVL',
        compute='_compute_paf_total_raw_cost',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('bom_line_ids.product_qty', 'bom_line_ids.product_id.standard_price')
    def _compute_paf_total_raw_cost(self):
        for bom in self:
            total = 0.0
            for line in bom.bom_line_ids:
                if line.product_id:
                    total += line.product_qty * line.product_id.standard_price
            bom.paf_total_raw_cost = total
