# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    paf_can_use = fields.Boolean(
        string='Cho phép dùng trong PAF',
        default=False,
        tracking=True
    )

    paf_last_cost = fields.Float(
        string='Giá NVL (cache)',
        compute='_compute_paf_last_cost',
        store=True
    )

    food_safety_declaration_state = fields.Selection([
        ('not_required', 'Không yêu cầu'),
        ('pending', 'Đang chờ'),
        ('done', 'Đã hoàn tất'),
        ('expired', 'Hết hạn'),
    ], string='Tình trạng tự công bố ATTP', default='not_required', tracking=True)

    food_safety_declaration_no = fields.Char(
        string='Số tự công bố ATTP',
        tracking=True
    )

    food_safety_declaration_date = fields.Date(
        string='Ngày tự công bố ATTP',
        tracking=True
    )

    food_safety_notes = fields.Text(
        string='Ghi chú ATTP',
        tracking=True
    )

    @api.depends('standard_price', 'seller_ids.price')
    def _compute_paf_last_cost(self):
        for template in self:
            cost = template.standard_price
            if not cost and template.seller_ids:
                sorted_sellers = template.seller_ids.sorted(key=lambda s: s.create_date or fields.Date.min, reverse=True)
                if sorted_sellers:
                    cost = sorted_sellers[0].price
            template.paf_last_cost = cost
