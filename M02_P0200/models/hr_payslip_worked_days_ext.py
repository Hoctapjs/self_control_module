# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    # Biến version_id thành trường lưu trữ để có thể giữ thông tin hợp đồng riêng cho từng dòng ngày công.
    # Thêm compute để Odoo tự động điền và lưu giá trị khi Save.
    version_id = fields.Many2one('hr.version', string='Contract', related=False, store=True, 
                                 compute='_compute_version_id', readonly=False)

    @api.depends('payslip_id.version_id')
    def _compute_version_id(self):
        for wd in self:
            if not wd.version_id:
                wd.version_id = wd.payslip_id.version_id

    @api.depends('is_paid', 'number_of_hours', 'payslip_id', 'version_id.wage', 'version_id.hourly_wage', 
                 'payslip_id.sum_worked_hours', 'work_entry_type_id.amount_rate', 'work_entry_type_id.is_extra_hours')
    def _compute_amount(self):
        """
        Ghi đè hàm tính tiền để sử dụng mức lương của version_id TRÊN DÒNG NÀY, 
        thay vì dùng verson_id của phiếu lương (header).
        """
        for worked_days in self:
            if worked_days.payslip_id.edited or worked_days.payslip_id.state != 'draft':
                continue
            if not worked_days.version_id or worked_days.code == 'OUT':
                worked_days.amount = 0
                continue
            
            # ĐIỂM THAY ĐỔI: Sử dụng version của chính dòng này
            version = worked_days.version_id
            
            amount_rate = worked_days.work_entry_type_id.amount_rate
            if worked_days.payslip_id.wage_type == "hourly":
                hourly_rate = version.hourly_wage
            else:
                # Tính toán tỷ lệ dựa trên tổng giờ làm việc trong kỳ của phiếu lương
                attendance_hours = sum(
                    wd.number_of_hours for wd in worked_days.payslip_id.worked_days_line_ids
                    if not wd.work_entry_type_id.is_extra_hours
                ) or 1
                hourly_rate = version.contract_wage / attendance_hours
            
            worked_days.amount = hourly_rate * worked_days.number_of_hours * amount_rate if worked_days.is_paid else 0
