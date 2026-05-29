# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    x_psm_region = fields.Selection([
        ('north', 'Bắc'),
        ('central', 'Trung'),
        ('south', 'Nam'),
    ], string='Vùng', help='Phân loại tỉnh/thành phố theo vùng miền địa lý.')
    x_psm_0200_salary_region_id = fields.Many2one('x_psm_salary_region', string='Vùng lương', help='Vùng lương để so sánh khi tính toán lương.')
