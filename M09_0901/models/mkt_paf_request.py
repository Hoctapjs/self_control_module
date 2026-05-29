# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class PafRequest(models.Model):
    _name = 'mkt_paf.request'
    _description = 'PAF Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Identification & Meta
    name = fields.Char(
        string='Mã PAF',
        required=True,
        readonly=True,
        copy=False,
        default='New'
    )

    template_id = fields.Many2one(
        'mkt_paf.template',
        string='Template PAF',
        required=True,
        tracking=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company,
        required=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        store=True,
        string='Tiền tệ'
    )

    # Ownership / Creator
    creator_id = fields.Many2one(
        'res.users',
        string='Người tạo',
        default=lambda self: self.env.user,
        required=True,
        readonly=True
    )

    creator_department_id = fields.Many2one(
        'hr.department',
        string='Phòng ban người tạo',
        compute='_compute_creator_info',
        store=True
    )

    creator_job_id = fields.Many2one(
        'hr.job',
        string='Chức vụ người tạo',
        compute='_compute_creator_info',
        store=True
    )

    # State Machine
    state = fields.Selection([
        ('draft', 'Nháp (MKT Soạn)'),
        ('dept_evaluation', 'Đánh giá phòng ban'),
        ('head_approval', 'Duyệt cấp Trưởng phòng'),
        ('clevel_approval', 'Duyệt cấp C-Level'),
        ('approved', 'Đã phê duyệt'),
        ('pif_running', 'PIF Đang chạy'),
        ('valuation', 'Đang làm Valuation'),
        ('done', 'Đóng phiếu'),
        ('rejected', 'Bị từ chối'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft', required=True, tracking=True)

    # PAF Content
    description_html = fields.Html(
        string='Mô tả PAF'
    )

    product_ids = fields.Many2many(
        'product.template',
        'mkt_paf_request_product_rel',
        'request_id',
        'product_tmpl_id',
        string='Sản phẩm áp dụng',
        domain=[('paf_can_use', '=', True)]
    )

    bom_ids = fields.Many2many(
        'mrp.bom',
        'mkt_paf_request_bom_rel',
        'request_id',
        'bom_id',
        string='BOM/Công thức',
        domain=[('paf_can_use', '=', True)]
    )

    loyalty_program_id = fields.Many2one(
        'loyalty.program',
        string='Chương trình khuyến mãi (Scheme)'
    )

    promotion_type = fields.Selection([
        ('discount_direct', 'Giảm giá trực tiếp'),
        ('gift_attached', 'Tặng quà kèm'),
        ('lucky_draw', 'Bốc thăm trúng thưởng'),
    ], string='Hình thức khuyến mãi', default='gift_attached', required=True, tracking=True)

    promotion_legal_form = fields.Selection([
        ('notification', 'Thông báo'),
        ('registration', 'Đăng ký'),
    ], string='Hình thức hồ sơ pháp lý', default='notification', required=True, tracking=True)

    regulatory_authority = fields.Char(
        string='Cơ quan tiếp nhận'
    )

    regulatory_filing_code = fields.Char(
        string='Số văn bản phê duyệt'
    )

    total_promotion_value = fields.Monetary(
        string='Tổng giá trị khuyến mãi',
        compute='_compute_total_promotion_value',
        store=True,
        currency_field='currency_id',
        tracking=True
    )

    gift_quantity = fields.Integer(
        string='Số lượng quà dự kiến',
        default=0,
        tracking=True
    )

    gift_unit_value = fields.Monetary(
        string='Giá trị 1 quà',
        default=0.0,
        currency_field='currency_id',
        tracking=True
    )

    gift_total_value = fields.Monetary(
        string='Tổng giá trị quà',
        compute='_compute_total_promotion_value',
        store=True,
        currency_field='currency_id'
    )

    discount_percent = fields.Float(
        string='% giảm giá',
        default=0.0,
        tracking=True
    )

    discount_total_estimate = fields.Monetary(
        string='Ước tính tổng giảm giá',
        default=0.0,
        currency_field='currency_id',
        tracking=True
    )

    allow_holiday_100 = fields.Boolean(
        string='Cho phép quà 100% mùa lễ',
        default=False,
        tracking=True
    )

    allow_extended_duration = fields.Boolean(
        string='Cho phép vượt 90 ngày',
        default=False,
        tracking=True
    )

    planned_start_date = fields.Date(
        string='Ngày bắt đầu dự kiến',
        tracking=True
    )

    planned_end_date = fields.Date(
        string='Ngày kết thúc dự kiến',
        tracking=True
    )

    target_store_ids = fields.Many2many(
        'pos.config',
        'mkt_paf_request_pos_config_rel',
        'request_id',
        'pos_config_id',
        string='Cửa hàng áp dụng'
    )

    eligible_channel_ids = fields.Many2many(
        'x_psm_pif_platform',
        'mkt_paf_request_pif_platform_rel',
        'request_id',
        'platform_id',
        string='Kênh áp dụng'
    )

    max_uses_per_customer = fields.Integer(
        string='Số lượt tối đa/khách',
        default=0,
        tracking=True
    )

    time_window_start = fields.Float(
        string='Giờ bắt đầu áp dụng',
        default=0.0,
        tracking=True
    )

    time_window_end = fields.Float(
        string='Giờ kết thúc áp dụng',
        default=24.0,
        tracking=True
    )

    customer_eligibility_html = fields.Html(
        string='Điều kiện khách hàng'
    )

    food_safety_declaration_state = fields.Selection([
        ('not_required', 'Không yêu cầu'),
        ('pending', 'Đang chờ'),
        ('done', 'Đã hoàn tất'),
        ('expired', 'Hết hạn'),
    ], string='Tình trạng ATTP', compute='_compute_food_safety_summary', store=True)

    food_safety_summary = fields.Text(
        string='Tóm tắt ATTP',
        compute='_compute_food_safety_summary',
        store=True
    )

    food_safety_responsible_dept_id = fields.Many2one(
        'hr.department',
        string='Phòng phụ trách ATTP'
    )

    # ROI Summary
    total_raw_cost = fields.Monetary(
        string='Tổng chi phí NVL',
        compute='_compute_total_raw_cost',
        store=True,
        currency_field='currency_id'
    )

    forecast_revenue = fields.Monetary(
        string='Doanh thu dự báo',
        default=0.0,
        currency_field='currency_id'
    )

    roi_percent = fields.Float(
        string='Tỷ suất ROI (%)',
        compute='_compute_roi_percent',
        store=True
    )

    # Approval & Execution Links
    head_approval_request_id = fields.Many2one(
        'approval.request',
        string='Yêu cầu duyệt của Heads',
        readonly=True
    )

    clevel_approval_request_id = fields.Many2one(
        'approval.request',
        string='Yêu cầu duyệt C-Level',
        readonly=True
    )

    pif_object_id = fields.Many2one(
        'x_psm_pif_object',
        string='Đối tượng PIF liên quan',
        readonly=True
    )

    # SLA Info
    regulatory_sla_days = fields.Integer(
        string='Số ngày SLA Pháp lý',
        compute='_compute_sla_info',
        store=True
    )

    paf_effective_start_date = fields.Date(
        string='Ngày bắt đầu hiệu lực thực tế',
        compute='_compute_sla_info',
        store=True
    )

    # Evaluation Lines relation
    evaluation_line_ids = fields.One2many(
        'mkt_paf.evaluation.line',
        'paf_request_id',
        string='Chi tiết đánh giá các phòng ban'
    )

    banner_ids = fields.One2many(
        'mkt_paf.banner',
        'paf_request_id',
        string='Hình ảnh / Banner'
    )

    banner_count = fields.Integer(
        string='Số banner',
        compute='_compute_banner_stats'
    )

    banner_approved_count = fields.Integer(
        string='Banner OK',
        compute='_compute_banner_stats'
    )

    banner_completeness = fields.Float(
        string='Hoàn tất banner (%)',
        compute='_compute_banner_stats'
    )

    require_banner_before_submit = fields.Boolean(
        string='Yêu cầu banner trước khi submit',
        default=True,
        tracking=True
    )

    evaluation_progress = fields.Float(
        string='Tiến độ đánh giá (%)',
        compute='_compute_evaluation_progress',
        store=False
    )

    # UI Helpers
    can_submit_evaluation = fields.Boolean(
        compute='_compute_can_submit_evaluation',
        string='Có quyền nộp đánh giá'
    )

    can_head_approve = fields.Boolean(
        compute='_compute_can_approve',
        string='Có quyền duyệt Head'
    )

    can_clevel_approve = fields.Boolean(
        compute='_compute_can_approve',
        string='Có quyền duyệt C-Level'
    )

    @api.depends('creator_id')
    def _compute_creator_info(self):
        for rec in self:
            employee = self.env['hr.employee'].sudo().search([('user_id', '=', rec.creator_id.id)], limit=1)
            rec.creator_department_id = employee.department_id if employee else False
            rec.creator_job_id = employee.job_id if employee else False

    @api.depends('bom_ids.paf_total_raw_cost')
    def _compute_total_raw_cost(self):
        for rec in self:
            rec.total_raw_cost = sum(rec.bom_ids.mapped('paf_total_raw_cost'))

    @api.depends('total_raw_cost', 'forecast_revenue')
    def _compute_roi_percent(self):
        for rec in self:
            if rec.total_raw_cost:
                rec.roi_percent = (rec.forecast_revenue - rec.total_raw_cost) / rec.total_raw_cost * 100
            else:
                rec.roi_percent = 0.0

    @api.depends('gift_quantity', 'gift_unit_value', 'discount_total_estimate')
    def _compute_total_promotion_value(self):
        for rec in self:
            rec.gift_total_value = max(rec.gift_quantity or 0, 0) * (rec.gift_unit_value or 0.0)
            rec.total_promotion_value = rec.gift_total_value + (rec.discount_total_estimate or 0.0)

    @api.depends(
        'product_ids.food_safety_declaration_state',
        'product_ids.food_safety_declaration_no',
        'product_ids.food_safety_declaration_date',
    )
    def _compute_food_safety_summary(self):
        priority = {
            'pending': 4,
            'expired': 3,
            'done': 2,
            'not_required': 1,
            False: 0,
        }
        for rec in self:
            products = rec.product_ids
            if not products:
                rec.food_safety_declaration_state = 'not_required'
                rec.food_safety_summary = False
                continue
            state = max(products.mapped('food_safety_declaration_state') or ['not_required'], key=lambda value: priority.get(value, 0))
            rec.food_safety_declaration_state = state or 'not_required'
            lines = []
            for product in products:
                label = dict(product._fields['food_safety_declaration_state'].selection).get(product.food_safety_declaration_state)
                doc_no = product.food_safety_declaration_no or '-'
                doc_date = product.food_safety_declaration_date or '-'
                lines.append("%s: %s | %s | %s" % (product.display_name, label, doc_no, doc_date))
            rec.food_safety_summary = "\n".join(lines)

    @api.depends('evaluation_line_ids.regulatory_sla_days', 'planned_start_date')
    def _compute_sla_info(self):
        for rec in self:
            legal_lines = rec.evaluation_line_ids.filtered(lambda l: l.department_code == 'legal')
            sla_days = sum(legal_lines.mapped('regulatory_sla_days'))
            rec.regulatory_sla_days = sla_days
            if rec.planned_start_date:
                rec.paf_effective_start_date = rec.planned_start_date - timedelta(days=sla_days)
            else:
                rec.paf_effective_start_date = False

    @api.depends('evaluation_line_ids.status')
    def _compute_evaluation_progress(self):
        for rec in self:
            total = len(rec.evaluation_line_ids)
            if not total:
                rec.evaluation_progress = 0.0
            else:
                completed = len(rec.evaluation_line_ids.filtered(lambda l: l.status in ('done', 'failed')))
                rec.evaluation_progress = (completed / total) * 100.0

    @api.depends('banner_ids.status')
    def _compute_banner_stats(self):
        for rec in self:
            total = len(rec.banner_ids)
            approved = len(rec.banner_ids.filtered(lambda b: b.status == 'brand_approved'))
            rec.banner_count = total
            rec.banner_approved_count = approved
            rec.banner_completeness = (approved / total) * 100.0 if total else 0.0

    @api.depends('state', 'evaluation_line_ids.status', 'evaluation_line_ids.department_id')
    def _compute_can_submit_evaluation(self):
        for rec in self:
            if rec.state != 'dept_evaluation':
                rec.can_submit_evaluation = False
                continue
            user_depts = self.env.user.employee_ids.department_id
            pending_lines = rec.evaluation_line_ids.filtered(lambda l: l.status in ('pending', 'in_review') and l.department_id in user_depts)
            rec.can_submit_evaluation = bool(pending_lines)

    def _compute_can_approve(self):
        # Implementation skeleton, will be detailed in Phase 5
        for rec in self:
            rec.can_head_approve = False
            rec.can_clevel_approve = False

    def _notify_all_evaluations_complete(self):
        for rec in self:
            rec.message_post(body=_("Tất cả các đánh giá phòng ban đã hoàn thành. Tự động thu thập đánh giá."))
            rec.action_collect_evaluations()

    def _get_legal_param_int(self, key, default):
        value = self.env['ir.config_parameter'].sudo().get_param(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _get_legal_param_float(self, key, default):
        value = self.env['ir.config_parameter'].sudo().get_param(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @api.onchange('promotion_type')
    def _onchange_promotion_type(self):
        for rec in self:
            if rec.promotion_type == 'lucky_draw':
                rec.promotion_legal_form = 'registration'
            elif not rec.promotion_legal_form:
                rec.promotion_legal_form = 'notification'

    @api.onchange('product_ids')
    def _onchange_product_ids_food_safety(self):
        sc_dept = self.env.ref('M02_P0200.dept_rst_supply_chain', raise_if_not_found=False)
        for rec in self:
            if not rec.food_safety_responsible_dept_id and sc_dept:
                rec.food_safety_responsible_dept_id = sc_dept

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            description_parts = [self.template_id.description_html or '']
            if self.template_id.default_description_legal_html:
                description_parts.append(self.template_id.default_description_legal_html)
            self.description_html = ''.join(description_parts)
            self.loyalty_program_id = self.template_id.default_loyalty_program_id
            self.product_ids = [(6, 0, self.template_id.default_product_ids.ids)]
            self.promotion_type = self.template_id.default_promotion_type
            self.promotion_legal_form = self.template_id.default_promotion_legal_form
            self.eligible_channel_ids = [(6, 0, self.template_id.default_eligible_channel_ids.ids)]
            self.max_uses_per_customer = self.template_id.default_max_uses_per_customer
            self.time_window_start = self.template_id.default_time_window_start
            self.time_window_end = self.template_id.default_time_window_end
            self.food_safety_responsible_dept_id = self.template_id.default_food_safety_responsible_dept_id

    @api.constrains('planned_start_date', 'planned_end_date', 'allow_extended_duration')
    def _check_promotion_duration_limit(self):
        limit_days = self._get_legal_param_int(
            'm09_0901.promotion_duration_limit_days',
            90,
        )
        for rec in self:
            if not rec.planned_start_date or not rec.planned_end_date or rec.allow_extended_duration:
                continue
            delta = (rec.planned_end_date - rec.planned_start_date).days
            if delta > limit_days:
                raise ValidationError(_(
                    "Theo Nghị định 81/2018/NĐ-CP, chương trình khuyến mãi "
                    "giảm giá/tặng quà không được kéo dài quá %s ngày. "
                    "Hiện tại: %s ngày (Bắt đầu: %s, Kết thúc: %s)."
                ) % (limit_days, delta, rec.planned_start_date, rec.planned_end_date))

    @api.constrains('promotion_type', 'promotion_legal_form')
    def _check_lucky_draw_legal_form(self):
        for rec in self:
            if rec.promotion_type == 'lucky_draw' and rec.promotion_legal_form != 'registration':
                raise ValidationError(_("Bốc thăm trúng thưởng phải chọn hình thức hồ sơ pháp lý là Đăng ký."))

    @api.constrains('state', 'promotion_type', 'regulatory_filing_code', 'total_promotion_value')
    def _check_legal_required_before_submit(self):
        if self.env.context.get('module') == 'M09_0901':
            return
        active_states = {'dept_evaluation', 'head_approval', 'clevel_approval', 'approved', 'pif_running', 'valuation', 'done'}
        for rec in self:
            if rec.state not in active_states:
                continue
            if rec.total_promotion_value <= 0:
                raise ValidationError(_("Vui lòng khai báo Tổng giá trị khuyến mãi trước khi chuyển PAF ra khỏi Nháp."))
            if rec.promotion_type == 'lucky_draw' and not rec.regulatory_filing_code:
                raise ValidationError(_("PAF bốc thăm trúng thưởng cần có Số văn bản phê duyệt trước khi chuyển ra khỏi Nháp."))

    @api.constrains('eligible_channel_ids', 'state')
    def _check_eligible_channels_before_submit(self):
        if self.env.context.get('module') == 'M09_0901':
            return
        active_states = {'dept_evaluation', 'head_approval', 'clevel_approval', 'approved', 'pif_running', 'valuation', 'done'}
        for rec in self:
            if rec.state in active_states and not rec.eligible_channel_ids:
                raise ValidationError(_("Vui lòng chọn ít nhất một Kênh áp dụng trước khi chuyển PAF ra khỏi Nháp."))

    @api.constrains('time_window_start', 'time_window_end')
    def _check_time_window(self):
        for rec in self:
            if not (0 <= rec.time_window_start <= 24) or not (0 <= rec.time_window_end <= 24):
                raise ValidationError(_("Khung giờ áp dụng phải nằm trong khoảng 0 đến 24."))
            if rec.time_window_end and rec.time_window_start and rec.time_window_end <= rec.time_window_start:
                raise ValidationError(_("Giờ kết thúc áp dụng phải lớn hơn giờ bắt đầu."))

    @api.constrains('gift_total_value', 'forecast_revenue', 'allow_holiday_100')
    def _check_gift_value_ratio(self):
        ratio_limit = self._get_legal_param_float(
            'm09_0901.gift_value_ratio_limit',
            0.5,
        )
        for rec in self:
            if rec.allow_holiday_100 or rec.gift_total_value <= 0 or rec.forecast_revenue <= 0:
                continue
            if rec.gift_total_value > ratio_limit * rec.forecast_revenue:
                raise ValidationError(_(
                    "Tổng giá trị quà tặng không được vượt quá %s%% giá trị hàng hóa dự kiến. "
                    "Hiện tại: %s / %s."
                ) % (ratio_limit * 100, rec.gift_total_value, rec.forecast_revenue))

    # Action Methods
    def action_submit_to_evaluation(self):
        self.ensure_one()
        if self.state != 'draft':
            raise ValidationError(_("Chỉ có thể gửi đánh giá từ trạng thái Nháp."))
        if not self.planned_start_date or not self.planned_end_date:
            raise ValidationError(_("Vui lòng điền ngày bắt đầu và ngày kết thúc dự kiến."))
        if self.require_banner_before_submit and self.banner_approved_count == 0:
            raise ValidationError(_(
                "PAF chưa có banner nào được Brand duyệt. "
                "Phòng MKT phải upload và có ít nhất 1 banner Brand duyệt trước khi submit."
            ))

        # Create evaluation lines based on template
        self.evaluation_line_ids.unlink()
        eval_vals = []
        sequence = 10
        eval_line_model = self.env['mkt_paf.evaluation.line']
        for dept in self.template_id.required_dept_evaluation:
            dept_code = eval_line_model._get_dept_code_mapping(dept)
            line_vals = {
                'department_id': dept.id,
                'department_code': dept_code,
                'sequence': sequence,
                'status': 'pending',
            }
            if dept_code == 'legal':
                line_vals.update({
                    'legal_filing_type': self.promotion_legal_form,
                    'requires_government_approval': self.promotion_legal_form == 'registration',
                })
            elif dept_code == 'sc' and self.food_safety_declaration_state in ('pending', 'expired'):
                line_vals['food_safety_check_status'] = 'pending'
            eval_vals.append((0, 0, line_vals))
            sequence += 10

        self.write({
            'evaluation_line_ids': eval_vals,
            'state': 'dept_evaluation'
        })
        return True

    def action_collect_evaluations(self):
        self.ensure_one()
        if self.state != 'dept_evaluation':
            raise ValidationError(_("Trạng thái hiện tại không phải là Đang đánh giá."))
        if any(line.status != 'done' for line in self.evaluation_line_ids):
            raise ValidationError(_("Tất cả các phòng ban phải hoàn thành đánh giá trước khi gửi phê duyệt."))

        # Find Approval Category
        category = False
        if 'is_mkt_paf' in self.env['approval.category']._fields:
            category = self.env['approval.category'].search([('is_mkt_paf', '=', True), ('mkt_paf_stage', '=', 'head')], limit=1)
        if not category:
            category = self.env.ref('M09_0901.mkt_0901_approval_category_paf_head', raise_if_not_found=False)
        if not category:
            category = self.env['approval.category'].search([('name', 'ilike', 'PAF Head')], limit=1)

        if not category:
            raise ValidationError(_("Không tìm thấy Category duyệt '0901 - PAF Head Review'. Vui lòng cấu hình hệ thống."))

        # Create Approval Request
        approval_vals = {
            'name': _("Duyệt PAF Head: %s") % self.name,
            'category_id': category.id,
            'request_owner_id': self.creator_id.id,
            'x_psm_mkt_paf_request_id': self.id,
        }
        request = self.env['approval.request'].create(approval_vals)
        if hasattr(request, 'action_confirm'):
            request.action_confirm()

        self.write({
            'head_approval_request_id': request.id,
            'state': 'head_approval'
        })
        return True

    def action_request_clevel(self):
        self.ensure_one()
        category = False
        if 'is_mkt_paf' in self.env['approval.category']._fields:
            category = self.env['approval.category'].search([('is_mkt_paf', '=', True), ('mkt_paf_stage', '=', 'clevel')], limit=1)
        if not category:
            category = self.env.ref('M09_0901.mkt_0901_approval_category_paf_clevel', raise_if_not_found=False)
        if not category:
            category = self.env['approval.category'].search([('name', 'ilike', 'C-Level')], limit=1)

        if not category:
            raise ValidationError(_("Không tìm thấy Category duyệt '0901 - PAF C-Level'. Vui lòng cấu hình hệ thống."))

        approval_vals = {
            'name': _("Duyệt PAF C-Level: %s") % self.name,
            'category_id': category.id,
            'request_owner_id': self.creator_id.id,
            'x_psm_mkt_paf_request_id': self.id,
        }
        request = self.env['approval.request'].create(approval_vals)
        if hasattr(request, 'action_confirm'):
            request.action_confirm()

        self.write({
            'clevel_approval_request_id': request.id,
            'state': 'clevel_approval'
        })
        return True

    def action_mark_approved(self):
        self.ensure_one()
        self.write({'state': 'approved'})
        self._run_pif_workflow()
        return True

    def _run_pif_workflow(self):
        """Trigger M08_P0801 PIF workflow when PAF is C-Level approved.

        Marketing PIF requests are not fast-tracked in M08. RSG approves the
        approval.request manually, then M08 creates x_psm_pif_object and
        pif_object.py links it back to this PAF.
        """
        self.ensure_one()
        category = self.env.ref(
            'M08_P0801.approval_category_data_pif',
            raise_if_not_found=False,
        )
        if not category:
            category = self.env['approval.category'].search([('x_psm_0801_is_pif', '=', True)], limit=1)
        if not category:
            self.message_post(body=_(
                "Không tìm thấy approval category PIF của M08_P0801. "
                "PAF chuyển state pif_running nhưng KHÔNG tạo PIF request."
            ))
            self.write({'state': 'pif_running'})
            return True

        product_product = self.env['product.product']
        if self.product_ids:
            product_product = product_product.search(
                [('product_tmpl_id', '=', self.product_ids[0].id)],
                limit=1,
            )

        pif_vals = {
            'name': _("Yêu cầu PIF từ PAF: %s") % self.name,
            'category_id': category.id,
            'request_owner_id': self.creator_id.id or self.env.user.id,
            'x_psm_0801_pif_request_type': 'marketing',
            'x_psm_mkt_paf_request_id': self.id,
        }
        if product_product:
            pif_vals['x_psm_0801_pif_product_id'] = product_product.id

        pif_request = self.env['approval.request'].sudo().create(pif_vals)

        # M08 fast-tracks only digital/supply_chain on confirm. Marketing keeps
        # the standard approval flow so RSG can approve the PIF request manually.
        if hasattr(pif_request, 'action_confirm'):
            pif_request.action_confirm()

        if pif_request.x_psm_0801_pif_object_id:
            self._sync_banners_to_pif(pif_request.x_psm_0801_pif_object_id)

        self.write({'state': 'pif_running'})
        return True

    def _sync_banners_to_pif(self, pif_object):
        self.ensure_one()
        if not pif_object:
            return False

        purpose_map = {
            'pos_display': ('x_psm_img_pos', 'x_psm_img_pos_filename'),
            'sok_display': ('x_psm_img_sok', 'x_psm_img_sok_filename'),
            'dt_menu': ('x_psm_img_dmb', 'x_psm_img_dmb_filename'),
            'mop_app': ('x_psm_img_mop', 'x_psm_img_mop_filename'),
        }
        attachments = self.env['ir.attachment'].sudo()
        vals = {}
        for purpose, (image_field, filename_field) in purpose_map.items():
            banner = self.banner_ids.filtered(
                lambda b: b.status == 'brand_approved' and b.purpose == purpose and b.image
            ).sorted('sequence')[:1]
            if not banner:
                continue
            filename = banner.image_filename or ("%s.png" % banner.name)
            vals[image_field] = banner.image
            vals[filename_field] = filename
            attachments.create({
                'name': filename,
                'type': 'binary',
                'datas': banner.image,
                'res_model': pif_object._name,
                'res_id': pif_object.id,
                'mimetype': 'image/png',
            })
        if vals:
            pif_object.sudo().write(vals)
        return bool(vals)

    def action_reject(self, reason):
        self.ensure_one()
        self.message_post(body=_("PAF bị từ chối. Lý do: %s") % reason)
        self.write({
            'state': 'draft',
            'head_approval_request_id': False,
            'clevel_approval_request_id': False,
        })
        return True

    def action_open_valuation(self):
        self.ensure_one()
        if self.state != 'pif_running':
            raise ValidationError(_("Chỉ có thể mở Valuation khi PIF đang chạy."))

        report = self.env['mkt_paf.valuation.report'].create({
            'paf_request_id': self.id,
            'status': 'draft',
        })
        self.write({'state': 'valuation'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Báo cáo đánh giá PAF'),
            'res_model': 'mkt_paf.valuation.report',
            'res_id': report.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_pspd_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Phân bổ PSPD'),
            'res_model': 'mkt_paf.pspd.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_paf_request_id': self.id,
            },
        }

    def action_view_banners(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hình ảnh / Banner'),
            'res_model': 'mkt_paf.banner',
            'view_mode': 'kanban,list,form',
            'domain': [('paf_request_id', '=', self.id)],
            'context': {'default_paf_request_id': self.id},
        }

    def action_close(self):
        self.ensure_one()
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise ValidationError(_("Không thể hủy phiếu đã hoàn thành."))
        self.write({'state': 'cancelled'})
        return True

    # Overrides
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('mkt.paf.request') or 'New'
            if vals.get('promotion_type') == 'lucky_draw':
                vals['promotion_legal_form'] = 'registration'
        return super(PafRequest, self).create(vals_list)

    def write(self, vals):
        if vals.get('promotion_type') == 'lucky_draw':
            vals = dict(vals, promotion_legal_form='registration')
        return super(PafRequest, self).write(vals)

    def unlink(self):
        for rec in self:
            if not (self.env.is_superuser() or self.env.user.has_group('base.group_system')):
                raise ValidationError(_("Chỉ quản trị viên hệ thống mới có quyền xóa PAF Request. Người dùng thông thường vui lòng sử dụng chức năng Hủy."))
        return super(PafRequest, self).unlink()
