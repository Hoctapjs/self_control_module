# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PafEvaluationLine(models.Model):
    _name = 'mkt_paf.evaluation.line'
    _description = 'PAF Evaluation Line'
    _inherit = ['mail.thread']
    _order = 'paf_request_id, sequence, id'

    paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='PAF Request',
        required=True,
        ondelete='cascade'
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Phòng ban',
        required=True
    )

    department_code = fields.Selection([
        ('si', 'Strategy & Insights'),
        ('ops', 'Operations'),
        ('finance', 'Finance'),
        ('sc', 'Supply Chain'),
        ('legal', 'Legal')
    ], string='Mã phòng ban', compute='_compute_department_code', store=True)

    sequence = fields.Integer(
        string='Thứ tự',
        default=10
    )

    evaluator_id = fields.Many2one(
        'res.users',
        string='Người đánh giá',
        tracking=True
    )

    status = fields.Selection([
        ('pending', 'Chờ đánh giá'),
        ('in_review', 'Đang đánh giá'),
        ('done', 'Đã đánh giá'),
        ('failed', 'Từ chối')
    ], string='Trạng thái', default='pending', tracking=True)

    comment_html = fields.Html(
        string='Nhận xét',
        tracking=True
    )

    submitted_date = fields.Datetime(
        string='Ngày nộp',
        tracking=True
    )

    # Department-specific fields
    # S&I
    forecast_demand = fields.Float(
        string='Nhu cầu dự báo (S&I)',
        tracking=True
    )
    confidence_score = fields.Float(
        string='Điểm tin cậy (S&I)',
        tracking=True
    )

    # OPS
    pilot_capacity_score = fields.Selection([
        ('low', 'Thấp (Low)'),
        ('medium', 'Trung bình (Medium)'),
        ('high', 'Cao (High)')
    ], string='Đánh giá năng lực vận hành (OPS)', tracking=True)
    bottleneck_note = fields.Text(
        string='Ghi chú nghẽn cổ chai (OPS)',
        tracking=True
    )

    # Finance
    roi_estimated_percent = fields.Float(
        string='Tỷ suất ROI ước tính (%)',
        tracking=True
    )
    gross_margin_estimated = fields.Monetary(
        string='Lợi nhuận gộp ước tính',
        currency_field='currency_id',
        tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='paf_request_id.currency_id',
        string='Tiền tệ'
    )

    # SC
    supply_risk_level = fields.Selection([
        ('low', 'Thấp (Low)'),
        ('medium', 'Trung bình (Medium)'),
        ('high', 'Cao (High)')
    ], string='Rủi ro cung ứng (SC)', tracking=True)
    lead_time_days = fields.Integer(
        string='Thời gian cung ứng (SC - ngày)',
        tracking=True
    )
    food_safety_check_status = fields.Selection([
        ('not_required', 'Không yêu cầu'),
        ('verified', 'Đã xác minh'),
        ('pending', 'Đang chờ'),
    ], string='Kiểm tra ATTP (SC)', default='not_required', tracking=True)

    # Legal
    regulatory_sla_days = fields.Integer(
        string='SLA Pháp lý (ngày)',
        default=0,
        tracking=True
    )
    requires_government_approval = fields.Boolean(
        string='Cần xin phép cơ quan nhà nước',
        tracking=True
    )
    scheme_compliant = fields.Boolean(
        string='Scheme hợp lệ pháp lý',
        default=True,
        tracking=True
    )
    legal_filing_type = fields.Selection([
        ('notification', 'Thông báo'),
        ('registration', 'Đăng ký'),
    ], string='Loại hồ sơ Legal', tracking=True)
    legal_50_percent_check = fields.Boolean(
        string='Đã kiểm tra ngưỡng 50%',
        tracking=True
    )

    def _get_legal_param_int(self, key, default):
        value = self.env['ir.config_parameter'].sudo().get_param(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @api.depends('department_id')
    def _compute_department_code(self):
        for rec in self:
            rec.department_code = rec._get_dept_code_mapping(rec.department_id)

    def _get_dept_code_mapping(self, department):
        if not department:
            return False
        xmlid_mapping = {
            'M02_P0200.dept_rst_strategy_insights': 'si',
            'M02_P0200.dept_rst_operation': 'ops',
            'M02_P0200.dept_rst_finance': 'finance',
            'M02_P0200.dept_rst_supply_chain': 'sc',
            'M02_P0200.dept_rst_legal': 'legal',
        }
        for xmlid, code in xmlid_mapping.items():
            if department == self.env.ref(xmlid, raise_if_not_found=False):
                return code
        name = (department.name or '').lower()
        if 'operation' in name or 'ops' in name or 'vận hành' in name:
            return 'ops'
        elif 'finance' in name or 'tài chính' in name:
            return 'finance'
        elif 'supply' in name or 'cung ứng' in name or 'sc' in name:
            return 'sc'
        elif 'legal' in name or 'pháp lý' in name:
            return 'legal'
        return 'si'  # Default to S&I

    def action_start_review(self):
        self.ensure_one()
        if self.status != 'pending':
            raise ValidationError(_("Chỉ có thể bắt đầu đánh giá khi đang ở trạng thái Chờ đánh giá."))
        self.write({
            'status': 'in_review',
            'evaluator_id': self.env.user.id
        })
        return True

    def action_submit_done(self):
        self.ensure_one()
        if self.status != 'in_review':
            raise ValidationError(_("Chỉ có thể hoàn thành đánh giá khi đang ở trạng thái Đang đánh giá."))

        # Validation per department
        if self.department_code == 'si':
            if self.forecast_demand <= 0:
                raise ValidationError(_("Nhu cầu dự báo (S&I) phải lớn hơn 0."))
            if not (0 <= self.confidence_score <= 1):
                raise ValidationError(_("Điểm tin cậy (S&I) phải nằm trong khoảng từ 0 đến 1."))
        elif self.department_code == 'ops':
            if not self.pilot_capacity_score:
                raise ValidationError(_("Vui lòng chọn Điểm đánh giá năng lực vận hành (OPS)."))
        elif self.department_code == 'finance':
            if not self.roi_estimated_percent:
                raise ValidationError(_("Vui lòng nhập Tỷ suất ROI ước tính (Finance)."))
            if not self.gross_margin_estimated:
                raise ValidationError(_("Vui lòng nhập Lợi nhuận gộp ước tính (Finance)."))
        elif self.department_code == 'sc':
            if not self.supply_risk_level:
                raise ValidationError(_("Vui lòng chọn Mức độ rủi ro cung ứng (SC)."))
            if self.lead_time_days < 0:
                raise ValidationError(_("Thời gian cung ứng (SC) không được âm."))
            if self.paf_request_id.food_safety_declaration_state == 'pending' and self.food_safety_check_status != 'pending':
                raise ValidationError(_("ATTP của PAF đang chờ xử lý, SC cần chọn trạng thái kiểm tra ATTP là Đang chờ."))
        elif self.department_code == 'legal':
            if self.regulatory_sla_days < 0:
                raise ValidationError(_("SLA Pháp lý (Legal) không được âm."))
            if self.legal_filing_type and self.legal_filing_type != self.paf_request_id.promotion_legal_form:
                raise ValidationError(_("Loại hồ sơ Legal phải khớp với Hình thức hồ sơ pháp lý trên PAF."))
            if self.paf_request_id.promotion_type == 'lucky_draw':
                min_sla_days = self._get_legal_param_int('m09_0901.lucky_draw_min_sla_days', 30)
                if self.regulatory_sla_days < min_sla_days:
                    raise ValidationError(_("PAF bốc thăm trúng thưởng cần SLA Legal tối thiểu %s ngày.") % min_sla_days)
            if self.paf_request_id.gift_total_value > 0 and not self.legal_50_percent_check:
                raise ValidationError(_("Legal cần xác nhận kiểm tra ngưỡng quà tặng 50% trước khi hoàn thành đánh giá."))

        self.write({
            'status': 'done',
            'submitted_date': fields.Datetime.now(),
            'evaluator_id': self.env.user.id
        })

        # Check if all other lines are done
        paf = self.paf_request_id
        if all(line.status == 'done' for line in paf.evaluation_line_ids):
            paf._notify_all_evaluations_complete()

        return True

    def action_submit_failed(self, reason=None):
        self.ensure_one()
        if self.status != 'in_review':
            raise ValidationError(_("Chỉ có thể từ chối đánh giá khi đang ở trạng thái Đang đánh giá."))
        
        if not reason:
            if not self.comment_html or len(self.comment_html.strip()) < 10:
                raise ValidationError(_("Vui lòng nhập nhận xét/lý do từ chối (ít nhất 10 ký tự) trước khi chọn Từ chối."))
            reason = self.comment_html

        self.write({
            'status': 'failed',
            'submitted_date': fields.Datetime.now(),
            'evaluator_id': self.env.user.id
        })

        # Reject the parent request
        self.paf_request_id.action_reject(reason)
        return True
