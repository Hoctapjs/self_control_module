# -*- coding: utf-8 -*-
from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    code = fields.Char(string='Mã Viết Tắt')
    name_ll = fields.Char(string='Tên Tiếng Việt', help='Tên vị trí bằng tiếng Việt')
    level_id = fields.Many2one('hr.job.level', string='Level')
    job_default_id = fields.Many2one('hr.job.position.default', string='Vị Trí Mặc Định', readonly=True)
    x_psm_0200_is_manager = fields.Boolean(
        related='job_default_id.x_psm_is_manager',
        string='Is Manager',
        store=True,
        readonly=True,
        help='Dùng để tính lương',
    )
    x_psm_0200_scale = fields.Integer(
        related='job_default_id.x_psm_scale',
        string='Scale',
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        ('code_dept_contract_unique', 'unique(code, department_id, company_id, contract_type_id)',
         'Mã viết tắt phải là duy nhất trong mỗi phòng ban!'),
    ]

