# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrContractKind(models.Model):
    _name = 'hr.contract.kind'
    _description = 'Contract Kind'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    duration = fields.Integer('Duration', help='Thời gian áp dụng', required=True)
    duration_unit = fields.Selection([
        ('days', 'Ngày'),
        ('months', 'Tháng'),
        ('years', 'Năm')
    ], string='Đơn vị áp dụng', default='days', required=True)
    kind_type = fields.Selection([
        ('definite', 'Definite'),
        ('in-definite', 'In-definite'),
        ('seasonal', 'Seasonal'),
        ('other', 'Other'),
        ('training', 'Training'),
        ('casual', 'Casual'),
        ('probation', 'Probation')
    ], string='Loại', default='definite', required=True)
    contract_type_id = fields.Many2one('hr.contract.type', string='Contract Type', required=True)
    description = fields.Html('Description')


