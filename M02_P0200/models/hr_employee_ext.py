# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    job_grade_id = fields.Many2one('hr.job.grade', string='Job Grade', groups='hr.group_hr_user')
    job_level_id = fields.Many2one('hr.job.level', string='Job Level', groups='hr.group_hr_user')
    contract_kind_id = fields.Many2one('hr.contract.kind', string='Contract Kind', 
        compute='_compute_contract_kind_id', inverse='_inverse_contract_kind_id', store=True, groups='hr.group_hr_user')
    allowance_responsibility = fields.Monetary(related="version_id.allowance_responsibility", readonly=False, string='Gross Responsibility allowance', groups='hr.group_hr_user')
    allowance_transportation = fields.Monetary(related="version_id.allowance_transportation", readonly=False, string='Gross Transportation allowance', groups='hr.group_hr_user')
    allowance_other = fields.Monetary(related="version_id.allowance_other", readonly=False, string='Gross Other allowance', groups='hr.group_hr_user')
    first_working_day = fields.Date(string='First Working Day', groups='hr.group_hr_user')
    
    # New fields for MCD
    x_psm_employee_code = fields.Char(string='Employee Code', groups='hr.group_hr_user', tracking=True, copy=False)
    x_psm_0200_is_non_packing = fields.Boolean(string='Is Non Packing', groups='hr.group_hr_user', default=False)
    x_psm_0200_remaining_al_days = fields.Float(
        string='Remaining Annual Leave Days',
        copy=False,
        groups='hr.group_hr_user',
        help=(
            'So ngay phep nam con lai cua nhan vien. Duong = con phep, '
            'am = da ung truoc. Field dung chung cho cac quy trinh PSM '
            'nhu 0213/0214 khi tinh khau tru AL luc nghi viec.'
        ),
    )

    _sql_constraints = [
        ('x_psm_employee_code_unique', 'unique(x_psm_employee_code)', 'Mã nhân viên đã tồn tại trong hệ thống!'),
    ]
    
    # Versioned Allowances (Related to version_id)
    x_psm_monthly_allowance = fields.Monetary(related="version_id.x_psm_monthly_allowance", readonly=False, string='Monthly Allowance', groups='hr.group_hr_user')
    x_psm_attendance_allowance = fields.Monetary(related="version_id.x_psm_attendance_allowance", readonly=False, string='Attendance Allowance', groups='hr.group_hr_user')
    x_psm_housing_allowance = fields.Monetary(related="version_id.x_psm_housing_allowance", readonly=False, string='Housing Allowance', groups='hr.group_hr_user')
    x_psm_hardshift_allowance = fields.Monetary(related="version_id.x_psm_hardshift_allowance", readonly=False, string='Hardshift Allowance', groups='hr.group_hr_user')
    x_psm_attraction_allowance = fields.Monetary(related="version_id.x_psm_attraction_allowance", readonly=False, string='Attraction Allowance', groups='hr.group_hr_user')

    @api.depends('version_id.contract_kind_id')
    def _compute_contract_kind_id(self):
        for emp in self:
            emp.contract_kind_id = emp.version_id.contract_kind_id

    def _inverse_contract_kind_id(self):
        for emp in self:
            if emp.version_id:
                emp.version_id.contract_kind_id = emp.contract_kind_id


    @api.onchange('job_level_id')
    def _onchange_job_level_id(self):
        if self.job_level_id:
            self.job_grade_id = self.job_level_id.grade_id

    @api.onchange('contract_type_id')
    def _onchange_contract_type_id(self):
        self.contract_kind_id = False
        return {
            'domain': {
                'contract_kind_id': [('contract_type_id', '=', self.contract_type_id.id)]
            }
        }

    @api.onchange('contract_kind_id', 'contract_date_start')
    def _onchange_contract_kind_id_mcd(self):
        if self.contract_kind_id and self.contract_date_start:
            from dateutil.relativedelta import relativedelta
            duration = self.contract_kind_id.duration
            unit = self.contract_kind_id.duration_unit
            
            start_date = fields.Date.from_string(self.contract_date_start)
            end_date = start_date
            
            if unit == 'days':
                end_date = start_date + relativedelta(days=duration)
            elif unit == 'months':
                end_date = start_date + relativedelta(months=duration)
            elif unit == 'years':
                end_date = start_date + relativedelta(years=duration)
            
            # Trừ đi 1 ngày để tròn kỳ (Ví dụ: 1 tháng từ 01/04 là đến 30/04)
            if end_date > start_date:
                self.contract_date_end = fields.Date.to_string(end_date - relativedelta(days=1))
