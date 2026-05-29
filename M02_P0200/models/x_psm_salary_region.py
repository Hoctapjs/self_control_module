# -*- coding: utf-8 -*-
from odoo import models, fields

class XPsmSalaryRegion(models.Model):
    _name = 'x_psm_salary_region'
    _description = 'Vùng Lương'
    _order = 'code'

    name = fields.Char(string='Tên Vùng', required=True)
    code = fields.Char(string='Mã Vùng', required=True)
    description = fields.Text(string='Mô Tả')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã vùng lương phải là duy nhất!'),
    ]
