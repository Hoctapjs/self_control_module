# -*- coding: utf-8 -*-
import pytz
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_worked_day_lines(self, domain=None, check_out_of_version=True):
        """
        Ghi đè để thu thập ngày công từ TẤT CẢ các hợp đồng (versions) của nhân viên trong kỳ.
        Vẫn giữ nguyên logic gom nhóm và tính toán của Odoo.
        """
        self.ensure_one()
        all_versions = self.env['hr.version'].search([
            ('employee_id', '=', self.employee_id.id),
            ('contract_date_start', '<=', self.date_to),
            '|', ('contract_date_end', '=', False), ('contract_date_end', '>=', self.date_from)
        ])
        
        # Nếu không có hợp đồng nào khác ngoài hợp đồng hiện tại (hoặc không có hợp đồng nào), dùng logic gốc
        if not all_versions or len(all_versions) <= 1:
            return super()._get_worked_day_lines(domain=domain, check_out_of_version=check_out_of_version)

        res = []
        covered_intervals = []

        for version in all_versions:
            # Xác định đoạn giao thoa giữa hợp đồng và kỳ lương
            v_start = max(self.date_from, version.contract_date_start)
            v_end = min(self.date_to, version.contract_date_end or date.max)
            
            if v_start > v_end:
                continue
                
            covered_intervals.append((v_start, v_end))
            
            # Gọi hàm lấy giờ làm việc cho đoạn này của hợp đồng này
            # Hàm get_work_hours trả về {work_entry_type_id: hours}
            work_hours = version.get_work_hours(v_start, v_end, domain=domain)
            hours_per_day = version.resource_calendar_id.hours_per_day or 8.0
            
            for work_entry_type_id, hours in work_hours.items():
                work_entry_type = self.env['hr.work.entry.type'].browse(work_entry_type_id)
                res.append({
                    'sequence': work_entry_type.sequence,
                    'work_entry_type_id': work_entry_type_id,
                    'number_of_days': hours / hours_per_day,
                    'number_of_hours': hours,
                    'version_id': version.id, # Gán hợp đồng cụ thể cho dòng này
                })

        if check_out_of_version:
            # Tính toán phần Out of Contract cho những ngày không có hợp đồng nào bao phủ trong kỳ lương
            covered_intervals.sort(key=lambda x: x[0])
            merged = []
            if covered_intervals:
                merged.append(list(covered_intervals[0]))
                for current in covered_intervals[1:]:
                    prev = merged[-1]
                    if current[0] <= prev[1]:
                        prev[1] = max(prev[1], current[1])
                    else:
                        merged.append(list(current))
            
            gaps = []
            cur = self.date_from
            for start, end in merged:
                if start > cur:
                    gaps.append((cur, start + relativedelta(days=-1)))
                cur = max(cur, end + relativedelta(days=1))
            if cur <= self.date_to:
                gaps.append((cur, self.date_to))
                
            out_days, out_hours = 0, 0
            ref_calendar = self.version_id.resource_calendar_id or self.employee_id.company_id.resource_calendar_id
            for g_start, g_end in gaps:
                st_dt = datetime.combine(g_start, time.min)
                en_dt = datetime.combine(g_end, time.max)
                out_time = ref_calendar.get_work_duration_data(st_dt, en_dt, compute_leaves=False, domain=['|', ('work_entry_type_id', '=', False), ('work_entry_type_id.is_leave', '=', False)])
                out_days += out_time['days']
                out_hours += out_time['hours']
            
            out_type = self.env.ref('hr_work_entry.hr_work_entry_type_out_of_contract', raise_if_not_found=False)
            if out_type and (out_days or out_hours):
                res.append({
                    'sequence': out_type.sequence,
                    'work_entry_type_id': out_type.id,
                    'number_of_days': out_days,
                    'number_of_hours': out_hours,
                    'version_id': self.version_id.id,
                })

        return res

    @api.depends('employee_id', 'version_id', 'struct_id', 'date_from', 'date_to')
    def _compute_worked_days_line_ids(self):
        """
        Đảm bảo các work entries được sinh ra cho tất cả các hợp đồng trong kỳ trước khi tính lương.
        """
        if not self or self.env.context.get('salary_simulation'):
            return
        
        valid_slips = self.filtered(lambda p: p.employee_id and p.date_from and p.date_to and p.version_id and p.struct_id and p.struct_id.use_worked_day_lines)
        if not valid_slips:
            return
            
        for slip in valid_slips:
            all_versions = self.env['hr.version'].search([
                ('employee_id', '=', slip.employee_id.id),
                ('contract_date_start', '<=', slip.date_to),
                '|', ('contract_date_end', '=', False), ('contract_date_end', '>=', slip.date_from)
            ])
            for v in all_versions:
                v_start = max(slip.date_from, v.contract_date_start)
                v_end = min(slip.date_to, v.contract_date_end or date.max)
                v.filtered('resource_calendar_id').generate_work_entries(v_start + relativedelta(days=-1), v_end + relativedelta(days=1))
        
        return super()._compute_worked_days_line_ids()
