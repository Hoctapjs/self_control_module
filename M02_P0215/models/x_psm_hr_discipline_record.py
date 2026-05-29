from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo import _
import base64
from odoo.exceptions import UserError


class HrDisciplineRecord(models.Model):
    _name = "x_psm.hr.discipline.record"
    _description = "Discipline Record"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _order = "x_psm_date desc, id desc"

    name = fields.Char(
        string="Reference", required=True, copy=False, readonly=True, default="New"
    )
    x_psm_employee_id = fields.Many2one(
        "hr.employee", string="Employee", required=True, tracking=True
    )
    x_psm_employee_name = fields.Char(
        related="x_psm_employee_id.name",
        string="Employee Name",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_employee_email = fields.Char(
        related="x_psm_employee_id.work_email",
        string="Employee Email",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_violation_type = fields.Char(string="Violation Type", tracking=True)
    x_psm_violation_category_id = fields.Many2one(
        "x_psm.hr.discipline.violation.category",
        string="Violation Category",
        required=True,
        tracking=True,
    )

    # Company Representative (Manager who creates the log)
    x_psm_company_rep_id = fields.Many2one(
        "hr.employee",
        string="Đại diện công ty",
        required=True,
        default=lambda self: self.env.user.employee_id,
        tracking=True,
    )
    x_psm_rep_department_id = fields.Many2one(
        "hr.department",
        related="x_psm_company_rep_id.department_id",
        string="Nhà hàng/Bộ phận (ĐD)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_rep_job_id = fields.Many2one(
        "hr.job",
        related="x_psm_company_rep_id.job_id",
        string="Vị trí làm việc (ĐD)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_rep_level = fields.Char(
        compute="_compute_x_psm_rep_level",
        string="Cấp bậc (ĐD)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )

    x_psm_employee_domain = fields.Char(
        compute="_compute_x_psm_employee_domain",
        string="Employee Domain",
        store=False,
    )

    @api.depends('x_psm_rep_department_id')
    def _compute_x_psm_employee_domain(self):
        is_oc = self.env.user.has_group('M02_P0200.GDH_RST_OPS_OC_S')
        for rec in self:
            if is_oc:
                rec.x_psm_employee_domain = "[('department_id.block_code', '=', 'OPS')]"
            else:
                rec.x_psm_employee_domain = f"[('department_id', '=', {rec.x_psm_rep_department_id.id or 0})]"

    # Employee Info Helpers (For printing/display)
    x_psm_emp_department_id = fields.Many2one(
        "hr.department",
        related="x_psm_employee_id.department_id",
        string="Nhà hàng/Bộ phận (NV)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_emp_job_id = fields.Many2one(
        "hr.job",
        related="x_psm_employee_id.job_id",
        string="Vị trí làm việc (NV)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_emp_level = fields.Char(
        compute="_compute_x_psm_emp_level",
        string="Cấp bậc (NV)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_emp_barcode = fields.Char(
        compute="_compute_x_psm_emp_barcode",
        string="Mã số nhân viên",
        store=True,
        compute_sudo=True,
    )
    
    @api.depends("x_psm_employee_id")
    def _compute_x_psm_emp_barcode(self):
        for rec in self:
            rec.x_psm_emp_barcode = str(rec.x_psm_employee_id.id) if rec.x_psm_employee_id else ""

    def _x_psm_get_employee_level_name(self, employee):
        if not employee:
            return False
        employee = employee.sudo()
        if "job_level_id" in employee._fields and employee.job_level_id:
            return employee.job_level_id.name

        job = employee.job_id
        if job and "level_id" in job._fields and job.level_id:
            return job.level_id.name
        return False

    @api.depends("x_psm_company_rep_id", "x_psm_company_rep_id.job_id")
    def _compute_x_psm_rep_level(self):
        for rec in self:
            rec.x_psm_rep_level = rec._x_psm_get_employee_level_name(
                rec.x_psm_company_rep_id
            )

    @api.depends("x_psm_employee_id", "x_psm_employee_id.job_id")
    def _compute_x_psm_emp_level(self):
        for rec in self:
            rec.x_psm_emp_level = rec._x_psm_get_employee_level_name(
                rec.x_psm_employee_id
            )

    @api.depends("x_psm_witness_id", "x_psm_witness_id.job_id")
    def _compute_x_psm_witness_level(self):
        for rec in self:
            rec.x_psm_witness_level = rec._x_psm_get_employee_level_name(
                rec.x_psm_witness_id
            )

    x_psm_discipline_purpose = fields.Selection(
        [
            ("discipline", "Discipline"),
            ("pip", "PIP"),
            ("counseling_1", "Counselling 1st"),
            ("counseling_2", "Counselling 2nd"),
        ],
        string="Mục đích",
        tracking=True,
        default="discipline",
    )
    x_psm_date = fields.Date(
        string="Date", required=True, default=fields.Date.context_today, tracking=True
    )

    # Portal / Explanation Fields
    x_psm_employee_explanation = fields.Text(
        string="Employee Explanation",
        tracking=True,
        help="Truong snapshot/cache de giu noi dung tuong trinh chinh cho report, mail va du lieu cu.",
    )
    x_psm_explanation_date = fields.Date(
        string="Explanation Date",
        help="Ngay snapshot tuong trinh duoc cap nhat tu survey hoac fallback legacy.",
    )

    # Detailed Explanation Sections (Matching MCD PDF Template)
    x_psm_section_i_description = fields.Text(
        string="I. Mô tả tình huống vi phạm",
        help="Truong nghiep vu goc. Sau refactor duoc giu lai de tuong thich report va du lieu cu.",
    )
    x_psm_section_ii_feedback = fields.Text(
        string="II. Phản hồi/ Ý kiến của nhân viên",
        help="Truong snapshot/cache. Noi dung co the duoc dong bo tu survey tuong trinh hoac fallback legacy.",
    )
    x_psm_section_iii_identification = fields.Text(
        string="III. Xác định hành vi vi phạm",
        help="Truong snapshot/cache. Noi dung co the duoc cap nhat tu quy trinh feedback survey.",
    )
    x_psm_section_iv_agreement = fields.Text(
        string="IV. Nội dung hai bên đồng ý",
        help="Truong snapshot/cache. Noi dung co the duoc cap nhat tu quy trinh feedback survey.",
    )

    # Attachments for Physical Explanations
    x_psm_explanation_image_ids = fields.Many2many(
        "ir.attachment",
        string="Hình ảnh bản tường trình",
        help="Hình ảnh bản tường trình giấy do quản lý chụp và tải lên",
    )

    # Signatures & Dates
    x_psm_manager_signature = fields.Binary(string="Chữ ký Đại diện công ty")
    x_psm_manager_signature_date = fields.Date(string="Ngày ký (Quản lý)")
    x_psm_employee_signature = fields.Binary(string="Chữ ký Người lao động")
    x_psm_employee_signature_date = fields.Date(string="Ngày ký (Nhân viên)")
    x_psm_witness_id = fields.Many2one("hr.employee", string="Người làm chứng")
    x_psm_witness_department_id = fields.Many2one(
        "hr.department",
        related="x_psm_witness_id.department_id",
        string="Nhà hàng/Bộ phận (Người làm chứng)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_witness_job_id = fields.Many2one(
        "hr.job",
        related="x_psm_witness_id.job_id",
        string="Vị trí làm việc (Người làm chứng)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_witness_level = fields.Char(
        compute="_compute_x_psm_witness_level",
        string="Cấp bậc (Người làm chứng)",
        readonly=True,
        store=True,
        compute_sudo=True,
    )
    x_psm_witness_signature = fields.Binary(string="Chữ ký Người làm chứng")
    x_psm_witness_signature_date = fields.Date(string="Ngày ký (Người làm chứng)")

    # Explanation History
    x_psm_explanation_ids = fields.One2many(
        "x_psm.hr.discipline.explanation",
        "x_psm_record_id",
        string="Lịch sử tường trình",
        help="Luu snapshot lich su de giu tuong thich du lieu cu. Khong xoa trong giai doan refactor.",
    )

    x_psm_active_explanation_id = fields.Many2one(
        "x_psm.hr.discipline.explanation",
        string="Tường trình hiện tại",
        compute="_compute_x_psm_active_explanation",
        store=True,
    )

    x_psm_explanation_count = fields.Integer(
        compute="_compute_x_psm_explanation_count", string="Số lần tường trình"
    )

    @api.depends("x_psm_explanation_ids", "x_psm_explanation_ids.state")
    def _compute_x_psm_active_explanation(self):
        for rec in self:
            active = rec.x_psm_explanation_ids.filtered(
                lambda e: e.state in ["submitted", "accepted"]
            )
            rec.x_psm_active_explanation_id = active[0] if active else False

    @api.depends("x_psm_explanation_ids")
    def _compute_x_psm_explanation_count(self):
        for rec in self:
            rec.x_psm_explanation_count = len(rec.x_psm_explanation_ids)

    x_psm_action_id = fields.Many2one(
        "x_psm.hr.discipline.action",
        string="Proposed Action",
        tracking=True,
        help="Automatically suggested by the system based on history.",
    )

    x_psm_portal_needs_attention = fields.Boolean(
        string="Portal: Cần chú ý",
        default=True,
        copy=False,
    )

    x_psm_explanation_survey_id = fields.Many2one(
        "survey.survey",
        string="Explanation Survey",
        default=lambda self: self._x_psm_get_default_explanation_survey(),
        readonly=True,
    )
    x_psm_explanation_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Explanation Survey Response",
        copy=False,
        readonly=True,
        tracking=True,
    )
    x_psm_explanation_survey_state = fields.Selection(
        related="x_psm_explanation_survey_user_input_id.state",
        string="Explanation Survey Status",
        store=True,
        readonly=True,
    )
    x_psm_explanation_rejection_reason = fields.Text(
        string="Explanation Rejection Reason",
        copy=False,
        readonly=True,
    )
    x_psm_skip_hearing_reason = fields.Text(
        string="Skip Hearing Reason",
        copy=False,
        readonly=True,
        tracking=True,
    )
    x_psm_feedback_survey_id = fields.Many2one(
        "survey.survey",
        string="Feedback Survey",
        default=lambda self: self._x_psm_get_default_feedback_survey(),
        readonly=True,
    )
    x_psm_feedback_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Feedback Survey Response",
        copy=False,
        readonly=True,
        tracking=True,
    )
    x_psm_feedback_survey_state = fields.Selection(
        related="x_psm_feedback_survey_user_input_id.state",
        string="Feedback Survey Status",
        store=True,
        readonly=True,
    )
    x_psm_feedback_completed_date = fields.Datetime(
        string="Feedback Completed Date",
        copy=False,
        readonly=True,
    )
    x_psm_migration_status = fields.Selection(
        [
            ("not_needed", "Not Needed"),
            ("pending", "Pending"),
            ("partial", "Partial"),
            ("done", "Done"),
            ("failed", "Failed"),
        ],
        string="Migration Status",
        copy=False,
        readonly=True,
        tracking=True,
    )
    x_psm_migration_date = fields.Datetime(
        string="Migration Date",
        copy=False,
        readonly=True,
    )
    x_psm_migration_note = fields.Text(
        string="Migration Note",
        copy=False,
        readonly=True,
    )

    x_psm_approval_request_id = fields.Many2one(
        "approval.request",
        string="Approval Request",
        copy=False,
        readonly=True,
        tracking=True,
    )
    x_psm_approval_status = fields.Selection(
        related="x_psm_approval_request_id.request_status",
        string="Approval Status",
        store=True,
        readonly=True,
    )
    x_psm_approval_requested_date = fields.Datetime(
        string="Approval Requested Date",
        copy=False,
        readonly=True,
    )
    x_psm_approval_completed_date = fields.Datetime(
        string="Approval Completed Date",
        copy=False,
        readonly=True,
    )
    x_psm_approval_refuse_reason = fields.Text(
        string="Approval Refuse Note",
        copy=False,
        readonly=True,
    )

    x_psm_previous_record_id = fields.Many2one(
        "x_psm.hr.discipline.record",
        string="Previous Offense Link",
        readonly=True,
        help="Linked to a previous offense if this is an escalation.",
    )

    state = fields.Selection(
        [
            ("draft", "Khởi tạo"),
            ("under_review", "Đang xem xét"),
            ("level_determination", "Xác định cấp xử lý"),
            ("investigation", "Xác minh nâng cao"),
            ("hearing", "Họp kỷ luật"),
            ("proposal", "Đề xuất kỷ luật"),
            ("issued", "Ban hành quyết định"),
            ("approval", "Phê duyệt"),
            ("notified", "Thông báo"),
            ("active", "Đang hiệu lực"),
            ("expired", "Hết hiệu lực"),
            ("cancel", "Đã hủy"),
        ],
        string="Status",
        default="draft",
        tracking=True,
        group_expand="_group_expand_states",
    )

    @api.model
    def _group_expand_states(self, states, domain, order=None):
        return [key for key, val in type(self).state.selection]

    def _x_psm_state_label(self, state):
        return dict(self._fields["state"].selection).get(state, state)

    def _x_psm_allowed_state_transitions(self):
        return {
            "draft": {"under_review", "cancel"},
            "under_review": {"proposal", "level_determination", "cancel"},
            "level_determination": {"proposal", "investigation", "cancel"},
            "investigation": {"hearing", "proposal", "cancel"},
            "hearing": {"proposal", "cancel"},
            "proposal": {"level_determination", "issued", "cancel"},
            "issued": {"approval", "notified", "investigation", "cancel"},
            "approval": {"notified", "issued", "proposal", "cancel"},
            "notified": {"active", "proposal", "investigation", "cancel"},
            "active": {"expired", "cancel"},
            "expired": set(),
            "cancel": set(),
        }

    def _x_psm_validate_state_transition(self, target_state):
        allowed_transitions = self._x_psm_allowed_state_transitions()
        for rec in self:
            if not rec.id or rec.state == target_state:
                continue
            if target_state not in allowed_transitions.get(rec.state, set()):
                raise UserError(
                    _(
                        "Không thể chuyển trạng thái từ %(source)s sang %(target)s "
                        "trong quy trình 0215."
                    )
                    % {
                        "source": rec._x_psm_state_label(rec.state),
                        "target": rec._x_psm_state_label(target_state),
                    }
                )

    def _x_psm_write_state(self, target_state, vals=None):
        write_vals = dict(vals or {})
        write_vals["state"] = target_state
        self.write(write_vals)

    def _x_psm_ensure_action_selected(self):
        for rec in self:
            if not rec.x_psm_action_id:
                raise UserError("Vui lòng chọn hình thức kỷ luật trước khi ban hành.")

    def _x_psm_ensure_discipline_level(self):
        for rec in self:
            if not rec.x_psm_discipline_level:
                raise UserError("Vui lòng xác định cấp xử lý Store Level hoặc Company Level.")

    x_psm_rgm_is_repeat = fields.Boolean(
        string="RGM xác nhận tái phạm", default=False, tracking=True
    )

    # --- Bước 9: Phản hồi của Nhân viên ---
    x_psm_is_accepted = fields.Boolean(
        string="Nhân viên chấp nhận hình thức KL", default=False, tracking=True
    )
    x_psm_has_ceo_refused = fields.Boolean(
        string="Has CEO Refused",
        compute="_compute_x_psm_has_ceo_refused",
    )
    x_psm_employee_response_date = fields.Date(string="Ngày phản hồi")
    x_psm_employee_response_note = fields.Text(string="Lý do từ chối (nếu có)")

    def _compute_x_psm_has_ceo_refused(self):
        for rec in self:
            refused_count = self.env["approval.request"].sudo().search_count([
                ("x_psm_discipline_record_id", "=", rec.id),
                ("request_status", "=", "refused"),
            ])
            rec.x_psm_has_ceo_refused = refused_count > 0

    # --- Bước 7: Ngày ban hành ---
    x_psm_issued_date = fields.Date(string="Ngày ban hành quyết định", tracking=True)
    x_psm_start_date = fields.Date(string="Ngày bắt đầu hiệu lực", tracking=True)
    x_psm_end_date = fields.Date(
        string="Ngày hết hiệu lực", compute="_compute_x_psm_end_date", store=True
    )

    # Discipline Level (Store vs Company)
    x_psm_discipline_level = fields.Selection(
        [
            ("store", "Store Level"),
            ("company", "Company Level"),
        ],
        string="Cấp độ xử lý",
        tracking=True,
    )

    # Repeat Offense Detection
    x_psm_is_repeat_offense = fields.Boolean(
        compute="_compute_x_psm_repeat_offense",
        store=True,
        string="Tái phạm",
    )
    x_psm_related_records_count = fields.Integer(
        compute="_compute_x_psm_repeat_offense",
        store=True,
        string="Số lần vi phạm trước",
    )

    x_psm_days_remaining = fields.Integer(
        compute="_compute_x_psm_days_remaining",
        string="Ngày hiệu lực còn lại",
    )

    @api.depends("x_psm_start_date", "x_psm_action_id")
    def _compute_x_psm_end_date(self):
        for rec in self:
            if rec.x_psm_start_date and rec.x_psm_action_id and rec.x_psm_action_id.x_psm_improvement_period:
                rec.x_psm_end_date = rec.x_psm_start_date + relativedelta(
                    days=rec.x_psm_action_id.x_psm_improvement_period
                )
            else:
                rec.x_psm_end_date = False

    @api.depends("state", "x_psm_end_date")
    def _compute_x_psm_days_remaining(self):
        for rec in self:
            if rec.state == "active" and rec.x_psm_end_date:
                today = fields.Date.today()
                delta = (rec.x_psm_end_date - today).days
                rec.x_psm_days_remaining = max(0, delta)
            else:
                rec.x_psm_days_remaining = 0

    # Meeting Integration
    x_psm_meeting_count = fields.Integer(compute="_compute_x_psm_meeting_count")

    def _x_psm_meeting_domain(self):
        self.ensure_one()
        return [("res_model", "=", self._name), ("res_id", "=", self.id)]

    def _compute_x_psm_meeting_count(self):
        for rec in self:
            rec.x_psm_meeting_count = self.env["calendar.event"].search_count(rec._x_psm_meeting_domain())

    def _x_psm_get_meeting_partner_ids(self):
        self.ensure_one()
        partners = self.env["res.partner"]
        record = self.sudo()
        employees = record.x_psm_employee_id | record.x_psm_company_rep_id | record.x_psm_employee_id.parent_id
        for employee in employees:
            if "work_contact_id" in employee._fields and employee.work_contact_id:
                partners |= employee.work_contact_id
            elif employee.user_id and employee.user_id.partner_id:
                partners |= employee.user_id.partner_id
        partners |= self.env.user.partner_id

        for xmlid in ("M02_P0200.GDH_RST_HR_HRBP_S", "M02_P0200.GDH_RST_OPS_OC_S"):
            group = self.env.ref(xmlid, raise_if_not_found=False)
            if group:
                partners |= group.sudo().all_user_ids.filtered(lambda user: not user.share).mapped("partner_id")

        return list(dict.fromkeys(partners.filtered(lambda partner: partner).ids))

    def _x_psm_meeting_context(self):
        self.ensure_one()
        partner_ids = self._x_psm_get_meeting_partner_ids()
        start = fields.Datetime.now()
        return {
            "default_name": _("Discipline hearing: %(employee)s")
            % {"employee": self.x_psm_employee_name or self.x_psm_employee_id.name or self.name},
            "default_res_model": self._name,
            "default_res_id": self.id,
            "default_start": start,
            "default_stop": start + relativedelta(hours=1),
            "default_partner_ids": [(6, 0, partner_ids)],
        }

    def _x_psm_open_meeting_action(self, view_mode="list,form,calendar"):
        self.ensure_one()
        return {
            "name": _("Discipline Meeting"),
            "type": "ir.actions.act_window",
            "res_model": "calendar.event",
            "view_mode": view_mode,
            "domain": self._x_psm_meeting_domain(),
            "context": self._x_psm_meeting_context(),
        }

    def action_psm_schedule_meeting(self):
        self.ensure_one()
        return self._x_psm_open_meeting_action()

    # Meeting Info (for Company Level)
    x_psm_latest_meeting_id = fields.Many2one(
        "calendar.event", string="Cuộc họp mới nhất", compute="_compute_x_psm_latest_meeting"
    )
    x_psm_meeting_date = fields.Datetime(
        string="Ngày họp", compute="_compute_x_psm_latest_meeting", store=True, readonly=False
    )
    x_psm_meeting_notes = fields.Text(string="Nội dung họp")
    x_psm_meeting_attachment = fields.Binary(string="Biên bản họp")
    x_psm_meeting_attachment_filename = fields.Char(string="Tên file biên bản")
    x_psm_meeting_attachment_ids = fields.Many2many(
        "ir.attachment",
        "x_psm_hr_discipline_meeting_minutes_rel",
        "record_id",
        "attachment_id",
        string="Biên bản họp kỷ luật (nhiều file)",
    )
    x_psm_compensation_minutes_ids = fields.Many2many(
        "ir.attachment",
        "x_psm_hr_discipline_comp_minutes_rel",
        "record_id",
        "attachment_id",
        string="Biên bản bồi thường (nhiều file)",
    )

    @api.depends("x_psm_meeting_count")  # Re-compute when meeting count changes
    def _compute_x_psm_latest_meeting(self):
        for rec in self:
            # Filter meetings linked SPECIFICALLY to this discipline record
            meeting = self.env["calendar.event"].search(
                [
                    ("res_model", "=", self._name),
                    ("res_id", "=", rec.id),
                ],
                order="start desc",
                limit=1,
            )
            rec.x_psm_latest_meeting_id = meeting
            
            if meeting:
                rec.x_psm_meeting_date = meeting.start

            elif not rec.x_psm_meeting_date:
                # Keep existing if manually set, or clear?
                # Let's clear if no meeting linked, but allow manual override if store=True/readonly=False logic permits.
                # Actually with compute+store, it only updates when dependencies change.
                pass

    # Compensation (Finance)
    x_psm_has_compensation = fields.Boolean(string="Có bồi thường", tracking=True)
    x_psm_compensation_amount = fields.Monetary(
        string="Giá trị bồi thường", currency_field="currency_id", tracking=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    # Decision Attachments
    x_psm_disciplinary_decision_attachment = fields.Binary(string="Quyết định xử lý kỷ luật")
    x_psm_disciplinary_decision_filename = fields.Char(string="Filename kỷ luật")

    x_psm_compensation_decision_attachment = fields.Binary(string="Quyết định đền bù")
    x_psm_compensation_decision_filename = fields.Char(string="Filename đền bù")

    @api.depends("x_psm_employee_id")
    def _compute_x_psm_repeat_offense(self):
        for rec in self:
            if not rec.x_psm_employee_id:
                rec.x_psm_is_repeat_offense = False
                rec.x_psm_related_records_count = 0
                continue

            related_count = self.search_count(
                [
                    ("x_psm_employee_id", "=", rec.x_psm_employee_id.id),
                    ("id", "!=", rec._origin.id or rec.id),
                    ("state", "in", ["active", "expired"]),
                ]
            )
            rec.x_psm_related_records_count = related_count
            rec.x_psm_is_repeat_offense = related_count > 0

    def _x_psm_resolve_effective_start_date(self):
        self.ensure_one()
        today = fields.Date.today()
        if not self.x_psm_rgm_is_repeat or not self.x_psm_employee_id:
            self.x_psm_previous_record_id = False
            return today

        previous = self.search(
            [
                ("x_psm_employee_id", "=", self.x_psm_employee_id.id),
                ("id", "!=", self.id),
                ("state", "in", ["active", "expired"]),
                ("x_psm_end_date", "!=", False),
            ],
            order="x_psm_end_date desc, id desc",
            limit=1,
        )
        if not previous:
            self.x_psm_previous_record_id = False
            return today

        self.x_psm_previous_record_id = previous.id
        if previous.x_psm_end_date >= today:
            return previous.x_psm_end_date + relativedelta(days=1)
        return today

    def action_psm_rgm_no_repeat(self):
        """RGM: Không tái phạm -> Bước 3 (Level Determination)"""
        self.ensure_one()
        self._x_psm_write_state(
            "level_determination",
            {
                "x_psm_rgm_is_repeat": False,
            },
        )

    def action_psm_rgm_repeat(self):
        """RGM: Có tái phạm → Bước 3 (Level Determination)"""
        self.ensure_one()
        self._x_psm_write_state(
            "level_determination", {"x_psm_rgm_is_repeat": True}
        )

    # --- SUGGESTED ACTION LOGIC ---
    @api.onchange("x_psm_employee_id", "x_psm_date")
    def _compute_x_psm_suggested_action(self):
        # RGM sẽ chọn thủ công tại stage proposal.
        pass

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            explanation_survey = self._x_psm_get_default_explanation_survey()
            self._x_psm_sync_signature_dates(vals)
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("x_psm.hr.discipline.record")
                    or "New"
                )
            vals.setdefault(
                "x_psm_explanation_survey_id",
                explanation_survey.id if explanation_survey else False,
            )
        records = super().create(vals_list)
        for rec in records:
            if rec.state == 'under_review':
                rec._x_psm_notify_rgm()
        return records

    @api.model
    def _x_psm_sync_signature_dates(self, vals):
        signature_date_fields = {
            "x_psm_manager_signature": "x_psm_manager_signature_date",
            "x_psm_employee_signature": "x_psm_employee_signature_date",
            "x_psm_witness_signature": "x_psm_witness_signature_date",
        }
        today = fields.Date.today()
        for signature_field, date_field in signature_date_fields.items():
            if signature_field not in vals or date_field in vals:
                continue
            vals[date_field] = today if vals.get(signature_field) else False

    # --- PORTAL ACTIONS ---
    @api.model
    def _x_psm_get_default_explanation_survey(self):
        return self.env.ref(
            "M02_P0215.survey_psm_explanation", raise_if_not_found=False
        )

    @api.model
    def _x_psm_get_default_feedback_survey(self):
        return self.env.ref("M02_P0215.survey_psm_feedback", raise_if_not_found=False)

    def _x_psm_get_explanation_partner(self):
        self.ensure_one()
        if self.x_psm_employee_id.user_id:
            return self.x_psm_employee_id.user_id.partner_id
        if "work_contact_id" in self.x_psm_employee_id._fields:
            return self.x_psm_employee_id.work_contact_id
        if "address_home_id" in self.x_psm_employee_id._fields:
            return self.x_psm_employee_id.address_home_id
        return self.env["res.partner"]

    def _x_psm_prepare_explanation_survey_user_input_vals(self):
        self.ensure_one()
        partner = self._x_psm_get_explanation_partner()
        return {
            "survey_id": self.x_psm_explanation_survey_id.id,
            "partner_id": partner.id if partner else False,
            "email": self.x_psm_employee_id.work_email or False,
            "deadline": False,
            "x_psm_0215_record_id": self.id,
            "x_psm_0215_flow_type": "explanation",
        }

    def _x_psm_get_or_create_explanation_survey_user_input(self, force_new=False):
        self.ensure_one()
        if not self.x_psm_explanation_survey_id:
            default_survey = self._x_psm_get_default_explanation_survey()
            if default_survey:
                self.write({"x_psm_explanation_survey_id": default_survey.id})
        if not self.x_psm_explanation_survey_id:
            raise UserError(_("Khong tim thay survey tuong trinh cho quy trinh 0215."))

        current_input = self.x_psm_explanation_survey_user_input_id.exists()
        if (
            current_input
            and not force_new
            and current_input.survey_id == self.x_psm_explanation_survey_id
            and current_input.state != "done"
        ):
            return current_input

        user_input = self.env["survey.user_input"].sudo().create(
            self._x_psm_prepare_explanation_survey_user_input_vals()
        )
        self.write(
            {
                "x_psm_explanation_survey_id": self.x_psm_explanation_survey_id.id,
                "x_psm_explanation_survey_user_input_id": user_input.id,
            }
        )
        return user_input

    def _x_psm_get_explanation_survey_url(self):
        self.ensure_one()
        user_input = self._x_psm_get_or_create_explanation_survey_user_input()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        return f"{base_url.rstrip('/')}{user_input.get_start_url()}"

    def _x_psm_prepare_feedback_survey_user_input_vals(self):
        self.ensure_one()
        partner = self.env.user.partner_id
        return {
            "survey_id": self.x_psm_feedback_survey_id.id,
            "partner_id": partner.id if partner else False,
            "email": self.env.user.email or self.x_psm_employee_id.work_email or False,
            "deadline": False,
            "x_psm_0215_record_id": self.id,
            "x_psm_0215_flow_type": "feedback",
        }

    def _x_psm_get_or_create_feedback_survey_user_input(self, force_new=False):
        self.ensure_one()
        if not self.x_psm_feedback_survey_id:
            default_survey = self._x_psm_get_default_feedback_survey()
            if default_survey:
                self.write({"x_psm_feedback_survey_id": default_survey.id})
        if not self.x_psm_feedback_survey_id:
            raise UserError(_("Khong tim thay survey feedback cho quy trinh 0215."))

        current_input = self.x_psm_feedback_survey_user_input_id.exists()
        if (
            current_input
            and not force_new
            and current_input.survey_id == self.x_psm_feedback_survey_id
            and current_input.state != "done"
        ):
            return current_input

        user_input = self.env["survey.user_input"].sudo().create(
            self._x_psm_prepare_feedback_survey_user_input_vals()
        )
        self.write(
            {
                "x_psm_feedback_survey_id": self.x_psm_feedback_survey_id.id,
                "x_psm_feedback_survey_user_input_id": user_input.id,
                "x_psm_feedback_completed_date": False,
            }
        )
        return user_input

    def _x_psm_get_feedback_survey_url(self):
        self.ensure_one()
        user_input = self._x_psm_get_or_create_feedback_survey_user_input()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        return f"{base_url.rstrip('/')}{user_input.get_start_url()}"

    def _x_psm_get_explanation_answer_value(self, user_input, xmlid):
        question = self.env.ref(xmlid, raise_if_not_found=False)
        if not question:
            return False
        lines = user_input.user_input_line_ids.filtered(
            lambda line: line.question_id == question and not line.skipped
        )
        if not lines:
            return False
        line = lines[0]
        if line.answer_type == "char_box":
            return line.value_char_box
        if line.answer_type == "text_box":
            return line.value_text_box
        if line.answer_type == "numerical_box":
            return line.value_numerical_box
        if line.answer_type == "date":
            return line.value_date
        if line.answer_type == "datetime":
            return line.value_datetime
        if line.answer_type == "scale":
            return line.value_scale
        if line.answer_type == "suggestion":
            return line.suggested_answer_id.value
        return False

    def _x_psm_create_explanation_snapshot(self, user_input, values):
        self.ensure_one()
        next_sequence = (max(self.x_psm_explanation_ids.mapped("sequence")) + 1) if self.x_psm_explanation_ids else 1
        existing = self.x_psm_explanation_ids.filtered(
            lambda explanation: explanation.x_psm_submitted_date
            and user_input.end_datetime
            and explanation.x_psm_submitted_date == user_input.end_datetime
        )[:1]
        snapshot_vals = {
            "x_psm_record_id": self.id,
            "sequence": existing.sequence if existing else next_sequence,
            "x_psm_incident_date_time": values.get("x_psm_incident_date_time"),
            "x_psm_incident_location": values.get("x_psm_incident_location"),
            "x_psm_witness_names": values.get("x_psm_witness_names"),
            "x_psm_explanation_content": values.get("x_psm_explanation_content"),
            "x_psm_explanation_reason": values.get("x_psm_explanation_reason"),
            "x_psm_explanation_commitment": values.get("x_psm_explanation_commitment"),
            "state": "submitted",
            "x_psm_submitted_date": user_input.end_datetime or fields.Datetime.now(),
        }
        if existing:
            existing.write(snapshot_vals)
        else:
            self.env["x_psm.hr.discipline.explanation"].create(snapshot_vals)

    def _x_psm_sync_explanation_from_survey_input(self, user_input):
        self.ensure_one()
        content = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_explanation_question_content"
        )
        reason = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_explanation_question_reason"
        )
        commitment = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_explanation_question_commitment"
        )
        confirmation = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_explanation_question_confirmation"
        )
        values = {
            "x_psm_incident_date_time": self._x_psm_get_explanation_answer_value(
                user_input, "M02_P0215.survey_psm_explanation_question_incident_datetime"
            ),
            "x_psm_incident_location": self._x_psm_get_explanation_answer_value(
                user_input, "M02_P0215.survey_psm_explanation_question_incident_location"
            ),
            "x_psm_witness_names": self._x_psm_get_explanation_answer_value(
                user_input, "M02_P0215.survey_psm_explanation_question_witness_names"
            ),
            "x_psm_explanation_content": content,
            "x_psm_explanation_reason": reason,
            "x_psm_explanation_commitment": commitment,
        }
        section_feedback_parts = [part for part in [content, reason, commitment, confirmation] if part]
        self.write(
            {
                "x_psm_employee_explanation": content,
                "x_psm_explanation_date": fields.Date.today(),
                "x_psm_section_ii_feedback": "\n\n".join(section_feedback_parts),
                "x_psm_explanation_survey_user_input_id": user_input.id,
                "x_psm_explanation_rejection_reason": False,
            }
        )
        self._x_psm_create_explanation_snapshot(user_input, values)

    def _x_psm_on_explanation_survey_done(self, user_input):
        self.ensure_one()
        self._x_psm_sync_explanation_from_survey_input(user_input)
        self.message_post(body="Nhan vien da hoan tat tuong trinh qua survey.")

    def _x_psm_sync_feedback_from_survey_input(self, user_input):
        self.ensure_one()
        issue = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_issue"
        )
        cause = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_cause"
        )
        guidance = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_guidance"
        )
        commitment = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_employee_commitment"
        )
        follow_up_period = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_follow_up_period"
        )
        follow_up_result = self._x_psm_get_explanation_answer_value(
            user_input, "M02_P0215.survey_psm_feedback_question_follow_up_result"
        )

        identification_parts = [part for part in [issue, cause] if part]
        agreement_parts = []
        if guidance:
            agreement_parts.append(f"Huong dan da trao doi:\n{guidance}")
        if commitment:
            agreement_parts.append(f"Cam ket cua nhan vien:\n{commitment}")
        if follow_up_period:
            agreement_parts.append(f"Thoi gian theo doi: {follow_up_period}")
        if follow_up_result:
            agreement_parts.append(f"Ket qua sau theo doi:\n{follow_up_result}")

        self.write(
            {
                "x_psm_section_iii_identification": "\n\n".join(identification_parts),
                "x_psm_section_iv_agreement": "\n\n".join(agreement_parts),
                "x_psm_feedback_survey_user_input_id": user_input.id,
                "x_psm_feedback_completed_date": fields.Datetime.now(),
            }
        )

    def _x_psm_on_feedback_survey_done(self, user_input):
        self.ensure_one()
        self._x_psm_sync_feedback_from_survey_input(user_input)
        self.write(
            {
                "x_psm_feedback_survey_user_input_id": user_input.id,
                "x_psm_feedback_completed_date": fields.Datetime.now(),
            }
        )
        self.message_post(body="Feedback cai thien ngay da duoc hoan tat qua survey.")

    def action_psm_open_explanation_survey_response(self):
        self.ensure_one()
        if not self.x_psm_explanation_survey_user_input_id:
            raise UserError(_("Ho so chua co phan hoi survey tuong trinh."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Explanation Survey Response"),
            "res_model": "survey.user_input",
            "res_id": self.x_psm_explanation_survey_user_input_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_psm_open_feedback_survey(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "name": _("Feedback Survey"),
            "target": "self",
            "url": self._x_psm_get_feedback_survey_url(),
        }

    def action_psm_open_feedback_survey_response(self):
        self.ensure_one()
        if not self.x_psm_feedback_survey_user_input_id:
            raise UserError(_("Ho so chua co phan hoi survey feedback."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Feedback Survey Response"),
            "res_model": "survey.user_input",
            "res_id": self.x_psm_feedback_survey_user_input_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def _x_psm_migration_mark(self, status, message):
        self.ensure_one()
        self.write(
            {
                "x_psm_migration_status": status,
                "x_psm_migration_date": fields.Datetime.now(),
                "x_psm_migration_note": message,
            }
        )

    def _x_psm_migrate_legacy_explanation_snapshot(self):
        self.ensure_one()
        if self.x_psm_explanation_ids:
            return "explanation_history_exists"
        if not any(
            [
                self.x_psm_employee_explanation,
                self.x_psm_section_ii_feedback,
                self.x_psm_employee_signature,
                self.x_psm_explanation_image_ids,
            ]
        ):
            return "no_legacy_explanation_data"

        explanation_vals = {
            "x_psm_record_id": self.id,
            "sequence": 1,
            "x_psm_incident_date_time": False,
            "x_psm_incident_location": False,
            "x_psm_witness_names": self.x_psm_witness_id.name if self.x_psm_witness_id else False,
            "x_psm_explanation_content": self.x_psm_employee_explanation
            or self.x_psm_section_ii_feedback,
            "x_psm_explanation_reason": False,
            "x_psm_explanation_commitment": False,
            "x_psm_employee_signature": self.x_psm_employee_signature,
            "state": "accepted" if self.state not in ("draft", "under_review") else "submitted",
            "x_psm_submitted_date": self.create_date or fields.Datetime.now(),
        }
        self.env["x_psm.hr.discipline.explanation"].create(explanation_vals)
        return "explanation_snapshot_created"

    def _x_psm_migrate_legacy_approval_bridge(self):
        self.ensure_one()
        if self.state != "approval":
            return "approval_not_applicable"
        if self.x_psm_approval_request_id:
            return "approval_request_exists"
        if self.x_psm_discipline_level != "company":
            return "approval_level_not_company"
        if not self.x_psm_action_id:
            return "approval_missing_action"
        self._x_psm_create_or_confirm_approval_request()
        return "approval_request_created"

    def _x_psm_migrate_legacy_feedback_policy(self):
        self.ensure_one()
        if not self.x_psm_action_id or self.x_psm_action_id.x_psm_form_code != "feedback":
            return "feedback_not_applicable"
        if self.x_psm_feedback_survey_user_input_id:
            return "feedback_response_exists"
        return "feedback_kept_legacy_only"

    def action_psm_migrate_legacy_bridge(self):
        summary = []
        final_status = "done"
        for rec in self:
            rec.ensure_one()
            steps = []
            try:
                explanation_result = rec._x_psm_migrate_legacy_explanation_snapshot()
                approval_result = rec._x_psm_migrate_legacy_approval_bridge()
                feedback_result = rec._x_psm_migrate_legacy_feedback_policy()
                steps.extend(
                    [
                        f"explanation={explanation_result}",
                        f"approval={approval_result}",
                        f"feedback={feedback_result}",
                    ]
                )

                meaningful_results = {
                    explanation_result,
                    approval_result,
                    feedback_result,
                }
                if meaningful_results <= {
                    "no_legacy_explanation_data",
                    "approval_not_applicable",
                    "feedback_not_applicable",
                }:
                    status = "not_needed"
                elif "approval_missing_action" in meaningful_results:
                    status = "failed"
                    final_status = "failed"
                elif any(
                    result in meaningful_results
                    for result in ["feedback_kept_legacy_only", "approval_level_not_company"]
                ):
                    status = "partial"
                    if final_status != "failed":
                        final_status = "partial"
                else:
                    status = "done"
                note = "; ".join(steps)
                rec._x_psm_migration_mark(status, note)
                summary.append(f"{rec.name}: {note}")
            except Exception as exc:
                final_status = "failed"
                message = f"migration_error={exc}"
                rec._x_psm_migration_mark("failed", message)
                summary.append(f"{rec.name}: {message}")

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Legacy migration completed"),
                "message": "\n".join(summary[:5]),
                "sticky": final_status == "failed",
                "type": "warning" if final_status in ("failed", "partial") else "success",
            },
        }

    def action_psm_send_to_employee(self):
        """Action for Manager to request explanation from Employee"""
        self.ensure_one()
        # State stays in 'draft'
        survey_user_input = self._x_psm_get_or_create_explanation_survey_user_input()

        # Send Email
        template = self.env.ref(
            "M02_P0215.email_template_psm_ask_explanation", raise_if_not_found=False
        )
        if template:
            template.sudo().send_mail(self.id, force_send=True)

        # Schedule Activity
        if self.x_psm_employee_id.user_id:
            self.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=self.x_psm_employee_id.user_id.id,
                summary="Action Required: Provide Explanation",
                note=_(
                    "Please submit your explanation via the survey form: %s"
                ) % self._x_psm_get_explanation_survey_url(),
            )

    def _get_portal_url(self):
        return f"/my/discipline/{self.id}"

    # --- WORKFLOW BUTTONS ---

    def action_psm_confirm(self):
        """Manager xác nhận → Gửi RGM xem xét (Bước 2)"""
        for rec in self:
            rec._x_psm_write_state("under_review")

    def action_psm_reject_explanation(self):
        """Reject current explanation and request a new one"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Lý do từ chối",
            "res_model": "x_psm.hr.discipline.reject.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_x_psm_record_id": self.id,
                "default_x_psm_mode": "explanation",
            },
        }

    def action_psm_rgm_store_level(self):
        """Bước 3: Store Level → Nhảy thẳng Bước 6 (Proposal)"""
        self._x_psm_write_state("proposal", {"x_psm_discipline_level": "store"})

    def action_psm_activate_store_discipline(self):
        """Legacy: Store Level đi qua issued/notified, không kích hoạt thẳng."""
        for rec in self:
            rec.action_psm_issue_decision()
            rec.action_psm_submit_for_approval()

    def _x_psm_notify_hr_oc_investigation(self):
        for rec in self:
            users = self.env["res.users"]
            for xmlid in ("M02_P0200.GDH_RST_HR_HRBP_S", "M02_P0200.GDH_RST_OPS_OC_S"):
                group = self.env.ref(xmlid, raise_if_not_found=False)
                if group:
                    users |= group.all_user_ids.filtered(lambda u: not u.share)
            for user in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=user.id,
                    summary=f"[Xác minh nâng cao] {rec.name}",
                    note=f"Hồ sơ kỷ luật NV {rec.x_psm_employee_name} cần xác minh nâng cao.",
                    date_deadline=fields.Date.today(),
                )

    def action_psm_rgm_company_level(self):
        """Bước 3: Company Level → Bước 4 (Investigation)"""
        self._x_psm_write_state("investigation", {"x_psm_discipline_level": "company"})
        self._x_psm_notify_hr_oc_investigation()

    def action_psm_schedule_hearing(self):
        """Bước 4: HR quyết định cần họp → Bước 5"""
        for rec in self:
            meeting_count = self.env["calendar.event"].sudo().search_count(rec._x_psm_meeting_domain())
            if not meeting_count:
                action = rec._x_psm_open_meeting_action(view_mode="form")
                action["target"] = "current"
                return action
            rec._x_psm_write_state("hearing")
        return True

    def action_psm_open_skip_hearing_wizard(self):
        """Open reason wizard before skipping hearing."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Skip Hearing Reason"),
            "res_model": "x_psm.hr.discipline.reject.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_x_psm_record_id": self.id,
                "default_x_psm_mode": "skip_hearing",
            },
        }

    def action_psm_skip_hearing(self):
        """Bước 4: HR quyết định không cần họp → Nhảy Bước 6"""
        self._x_psm_write_state("proposal")

    def action_psm_close_hearing(self):
        """Bước 5: Kết thúc họp → Bước 6 (Proposal)"""
        for rec in self:
            if rec.x_psm_discipline_level == "company":
                if not rec.x_psm_meeting_attachment_ids:
                    raise UserError(_("Vui lòng tải lên Biên bản xử lý kỷ luật trước khi kết thúc họp."))
                if rec.x_psm_has_compensation and not rec.x_psm_compensation_minutes_ids:
                    raise UserError(_("Vui lòng tải lên Biên bản xử lý bồi thường trước khi kết thúc họp."))
            rec._x_psm_write_state("proposal")

    def action_psm_rgm_recheck_level(self):
        """Company proposal → RGM rechecks Store/Company level."""
        for rec in self:
            rec._x_psm_write_state(
                "level_determination",
                {
                    "x_psm_action_id": False,
                    "x_psm_discipline_level": False,
                },
            )

    def action_psm_issue_decision(self):
        """Bước 6 → 7: Ban hành quyết định"""
        for rec in self:
            rec._x_psm_ensure_action_selected()
            rec._x_psm_ensure_discipline_level()
            rec._x_psm_write_state(
                "issued", {"x_psm_issued_date": fields.Date.today()}
            )

    def action_psm_submit_for_approval(self):
        """Bước 7 → 8 (Company) hoặc 7 → 9 (Store)"""
        for rec in self:
            rec._x_psm_ensure_action_selected()
            rec._x_psm_ensure_discipline_level()
            if rec.x_psm_discipline_level == "company":
                rec._x_psm_create_or_confirm_approval_request()
            else:
                rec._x_psm_write_state("notified")
                rec._x_psm_notify_employee()

    def action_psm_rehear(self):
        """CEO từ chối và RGM quyết định Cần họp lại → Quay lại Bước 4 (Xác minh nâng cao/Investigation)"""
        for rec in self:
            if rec.x_psm_discipline_level != "company":
                raise UserError(_("Nút này chỉ khả dụng cho hồ sơ thuộc cấp công ty (Company Level)."))
            rec._x_psm_write_state("investigation")
            rec._x_psm_notify_hr_oc_investigation()
            rec.message_post(
                body=_("Hồ sơ đã được RGM chuyển lại bước Xác minh nâng cao để tổ chức họp lại."),
                subject=_("Cần họp lại")
            )

    def _x_psm_get_approval_approver_users(self):
        self.ensure_one()
        approver_group = self.env.ref("hr.group_hr_manager", raise_if_not_found=False)
        if not approver_group:
            return self.env["res.users"]
        users = approver_group.all_user_ids.filtered(lambda user: not user.share)
        users = users.filtered(lambda user: self.env.company in user.company_ids)
        return self.env["res.users"].browse(list(dict.fromkeys(users.ids)))

    def _x_psm_prepare_approval_request_vals(self, category):
        self.ensure_one()
        reason = _(
            "<p>Hồ sơ kỷ luật %(record)s cần phê duyệt cấp công ty.</p>"
            "<ul>"
            "<li>Nhân viên: %(employee)s</li>"
            "<li>Hình thức đề xuất: %(action)s</li>"
            "<li>Ngày ban hành: %(issued_date)s</li>"
            "</ul>"
        ) % {
            "record": self.name,
            "employee": self.x_psm_employee_name or "",
            "action": self.x_psm_action_id.name or "",
            "issued_date": self.x_psm_issued_date or "",
        }
        existing_approvals_count = self.env["approval.request"].sudo().search_count([
            ("x_psm_discipline_record_id", "=", self.id)
        ])
        if existing_approvals_count > 0:
            name = _("Phê duyệt lại kỷ luật %(record)s (Lần %(count)d)") % {
                "record": self.name,
                "count": existing_approvals_count + 1
            }
        else:
            name = _("Phê duyệt kỷ luật %(record)s") % {"record": self.name}

        return {
            "name": name,
            "category_id": category.id,
            "request_owner_id": self.env.user.id,
            "date": fields.Datetime.now(),
            "reference": self.name,
            "amount": self.x_psm_compensation_amount if self.x_psm_has_compensation else 0.0,
            "reason": reason,
            "x_psm_discipline_record_id": self.id,
        }

    def _x_psm_create_or_confirm_approval_request(self):
        self.ensure_one()
        if self.x_psm_approval_request_id:
            if self.x_psm_approval_request_id.request_status == "approved":
                self._x_psm_on_approval_request_approved(self.x_psm_approval_request_id)
                return
            if self.x_psm_approval_request_id.request_status != "refused":
                self._x_psm_write_state("approval")
                return

        category = self.env.ref(
            "M02_P0215.approval_category_psm_discipline_company_level",
            raise_if_not_found=False,
        )
        if not category:
            raise UserError(_("Không tìm thấy cấu hình approval category cho quy trình 0215."))

        approver_users = self._x_psm_get_approval_approver_users()
        if not approver_users:
            raise UserError(_("Không tìm thấy người duyệt trong nhóm HR Manager để tạo approval request."))

        approval_request = self.env["approval.request"].sudo().create(
            self._x_psm_prepare_approval_request_vals(category)
        )
        existing_user_ids = set(approval_request.sudo().approver_ids.mapped("user_id").ids)
        approver_commands = [
            (
                0,
                0,
                {
                    "user_id": user.id,
                    "required": False,
                    "sequence": 10,
                },
            )
            for user in approver_users
            if user.id not in existing_user_ids
        ]
        if approver_commands:
            approval_request.sudo().write({"approver_ids": approver_commands})
        approval_request.sudo().action_confirm()
        
        # Create activities for approvers on the discipline record itself
        for user in approver_users:
            self.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=user.id,
                summary=_("Phê duyệt kỷ luật: %s") % self.name,
                note=_("Vui lòng xem xét và phê duyệt hồ sơ kỷ luật cho nhân viên %s.")
                % (self.x_psm_employee_name or self.x_psm_employee_id.name),
            )
        self._x_psm_write_state(
            "approval",
            {
                "x_psm_approval_request_id": approval_request.id,
                "x_psm_approval_requested_date": fields.Datetime.now(),
                "x_psm_approval_refuse_reason": False,
            },
        )

    def _x_psm_on_approval_request_approved(self, approval_request):
        for rec in self:
            if rec.state == "notified":
                continue
            rec._x_psm_write_state(
                "notified",
                {
                    "x_psm_approval_request_id": approval_request.id,
                    "x_psm_approval_completed_date": fields.Datetime.now(),
                    "x_psm_approval_refuse_reason": False,
                },
            )
            rec._x_psm_notify_employee()
            rec._x_psm_clear_approval_activities()

    def _x_psm_on_approval_request_refused(self, approval_request, reason=None):
        refuse_reason = reason or self.env.context.get("ceo_reject_reason") or _("Approval request đã bị từ chối.")
        for rec in self:
            if rec.state == "issued":
                continue
            rec._x_psm_write_state(
                "issued",
                {
                    "x_psm_approval_request_id": approval_request.id,
                    "x_psm_approval_completed_date": fields.Datetime.now(),
                    "x_psm_approval_refuse_reason": refuse_reason,
                },
            )
            rec._x_psm_notify_rejection("ceo", refuse_reason)
            rec._x_psm_clear_approval_activities()


    def _x_psm_clear_approval_activities(self):
        """Dọn dẹp các activity phê duyệt khi đã xử lý xong"""
        for rec in self:
            approver_users = rec._x_psm_get_approval_approver_users()
            activities = rec.activity_ids.filtered(
                lambda a: a.user_id in approver_users and _("Phê duyệt kỷ luật") in (a.summary or "")
            )
            if activities:
                activities.action_feedback(feedback=_("Đã xử lý phê duyệt."))

    def action_psm_open_approval_request(self):
        self.ensure_one()
        approvals = self.env["approval.request"].sudo().search([
            ("x_psm_discipline_record_id", "=", self.id)
        ])
        if not approvals:
            raise UserError(_("Hồ sơ chưa có approval request."))
        if len(approvals) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": _("Approval Request"),
                "res_model": "approval.request",
                "res_id": approvals[0].id,
                "view_mode": "form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": _("Lịch sử Phê duyệt"),
                "res_model": "approval.request",
                "domain": [("id", "in", approvals.ids)],
                "view_mode": "list,form",
                "target": "current",
            }

    def _x_psm_notify_employee(self):
        """Gửi email thông báo hình thức kỷ luật cho nhân viên"""
        template = self.env.ref(
            "M02_P0215.email_template_psm_discipline_notified", raise_if_not_found=False
        )
        if template:
            template.sudo().send_mail(self.id, force_send=True)

    def _x_psm_notify_employee_active(self):
        """Gửi email thông báo kỷ luật đã có hiệu lực cho nhân viên"""
        template = self.env.ref(
            "M02_P0215.email_template_psm_discipline_active_notified",
            raise_if_not_found=False,
        )
        if template:
            template.sudo().send_mail(self.id, force_send=True)

    def _x_psm_get_employee_reject_notify_users(self):
        self.ensure_one()
        users = self.env["res.users"]
        if self.x_psm_employee_id.parent_id.user_id:
            users |= self.x_psm_employee_id.parent_id.user_id

        for xmlid in ("M02_P0200.GDH_OPS_STORE_RGM_M", "hr.group_hr_manager"):
            group = self.env.ref(xmlid, raise_if_not_found=False)
            if group:
                users |= group.all_user_ids.filtered(lambda user: not user.share)

        return self.env["res.users"].browse(list(dict.fromkeys(users.ids)))

    def _x_psm_notify_rejection(self, rejection_type, reason=""):
        """Thông báo khi record bị từ chối (CEO hoặc NV)
        - Luôn notify RGM (cả Store và Company)
        - Company level: thêm notify HRBP & OC
        """
        for rec in self:
            users = self.env["res.users"]
            
            # 1. Luôn notify RGM (theo Department)
            rgm_group = self.env.ref('M02_P0200.GDH_OPS_STORE_RGM_M', raise_if_not_found=False)
            if rgm_group:
                rgm_users = rgm_group.all_user_ids.filtered(
                    lambda u: u.employee_id.department_id == rec.x_psm_employee_id.department_id
                )
                users |= rgm_users
            
            # 2. Company level: thêm HRBP & OC
            if rec.x_psm_discipline_level == "company":
                for xmlid in ("M02_P0200.GDH_RST_HR_HRBP_S", "M02_P0200.GDH_RST_OPS_OC_S"):
                    group = self.env.ref(xmlid, raise_if_not_found=False)
                    if group:
                        users |= group.all_user_ids.filtered(lambda u: not u.share)
            
            if not users:
                continue

            # 3. Tạo thông báo (Activity + Message)
            subject = _("CEO Từ chối phê duyệt") if rejection_type == "ceo" else _("Nhân viên từ chối kỷ luật")
            body = _(
                "<strong>%(subject)s</strong><br/>"
                "Hồ sơ: %(record)s<br/>"
                "Nhân viên: %(employee)s<br/>"
                "Hình thức kỷ luật: %(action)s<br/>"
                "Lý do: %(reason)s"
            ) % {
                "subject": subject,
                "record": rec.name,
                "employee": rec.x_psm_employee_name or rec.x_psm_employee_id.name or "",
                "action": rec.x_psm_action_id.name or "",
                "reason": reason or rec.x_psm_employee_response_note or "",
            }

            rec.message_post(
                body=body,
                subject=subject,
                partner_ids=users.mapped("partner_id").ids,
            )
            for user in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=user.id,
                    summary=f"{subject}: {rec.name}",
                    note=body,
                )

    def action_psm_employee_accept(self):
        """Bước 9: NV chấp nhận → Bước 10 (Active)"""
        for rec in self:
            rec._x_psm_write_state(
                "active",
                {
                    "x_psm_is_accepted": True,
                    "x_psm_employee_response_date": fields.Date.today(),
                    "x_psm_start_date": rec._x_psm_resolve_effective_start_date(),
                },
            )
            rec._x_psm_notify_employee_active()

    def action_psm_employee_reject(self, note=None):
        """Bước 9: NV từ chối → Quay lại Bước 6 (Proposal)"""
        for rec in self:
            target_state = "investigation" if rec.x_psm_discipline_level == "company" else "proposal"
            vals = {
                "x_psm_is_accepted": False,
                "x_psm_employee_response_date": fields.Date.today(),
                "x_psm_approval_request_id": False,
            }
            if note is not None:
                vals["x_psm_employee_response_note"] = note
            rec._x_psm_write_state(target_state, vals)
            rec._x_psm_notify_rejection("employee", note)

    def action_psm_open_rgm_manual_confirm_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("RGM Manual Confirmation"),
            "res_model": "x_psm.hr.discipline.manual.confirm.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_x_psm_record_id": self.id},
        }

    def action_psm_rgm_manual_confirm(self, start_date):
        for rec in self:
            if not self.env.user.has_group("M02_P0200.GDH_OPS_STORE_RGM_M"):
                raise UserError(_("Bạn không có quyền xác nhận hộ hồ sơ này."))
            rec._x_psm_write_state(
                "active",
                {
                    "x_psm_is_accepted": True,
                    "x_psm_employee_response_date": fields.Date.today(),
                    "x_psm_start_date": start_date,
                },
            )
            rec.message_post(
                body=_("RGM đã xác nhận hộ nhân viên. Ngày bắt đầu hiệu lực: %s") % start_date,
                subject=_("RGM Manual Confirmation"),
            )
            rec._x_psm_notify_employee_active()

    def action_psm_expire(self):
        """Bước 10 → 11: Hết hiệu lực"""
        self._x_psm_write_state("expired")

    def action_psm_store_confirm(self):
        """Legacy - không còn sử dụng, giữ lại để tương thích"""
        pass

    def _x_psm_get_report_by_name_strict(self, report_name):
        return self.env["ir.actions.report"].search(
            [("report_name", "=", report_name), ("model", "=", self._name)],
            order="id desc",
            limit=1,
        )

    def action_psm_generate_disciplinary_decision(self):
        self.ensure_one()
        report = self._x_psm_get_report_by_name_strict(
            "M02_P0215.report_disciplinary_decision_template"
        )

        if not report:
            raise UserError(
                "LỖI CẤU HÌNH: Không tìm thấy mẫu báo cáo 'Quyết định Xử lý kỷ luật'.\n"
                "Giải pháp: Hãy vào Settings -> Reports -> Tìm 'Quyết định Xử lý kỷ luật'.\n"
                "Nếu không thấy, hãy upgrade lại module."
            )

        # Render with list of IDs to be safe
        pdf_content, _ = report._render_qweb_pdf(report.id, [self.id])
        self.x_psm_disciplinary_decision_attachment = base64.b64encode(pdf_content)
        safe_name = self.name.replace("/", "_")
        self.x_psm_disciplinary_decision_filename = f"Quyết định xử lý kỷ luật - {safe_name}.pdf"

    def write(self, vals):
        self._x_psm_sync_signature_dates(vals)
        target_state = vals.get("state")
        notify_rgm_records = self.browse()
        if target_state:
            self._x_psm_validate_state_transition(target_state)
            if target_state == "under_review":
                notify_rgm_records = self.filtered(lambda rec: rec.state != "under_review")

            # Task 5: Portal notification state logic
            if target_state == "notified":
                vals["x_psm_portal_needs_attention"] = True
            elif target_state in ("active", "cancel"):
                vals["x_psm_portal_needs_attention"] = False

        result = super().write(vals)

        # Notify RGM when shifting to under_review
        for rec in notify_rgm_records:
            rec._x_psm_notify_rgm()
        return result

    def _x_psm_notify_rgm(self):
        """Find RGM of the employee's department and create activity"""
        self.ensure_one()
        if not self.x_psm_employee_id.department_id:
            return

        rgm_group = self.env.ref('M02_P0200.GDH_OPS_STORE_RGM_M', raise_if_not_found=False)
        if not rgm_group:
            return

        # Find users in RGM group (direct or implied) whose employee belongs to the same department
        rgm_users = rgm_group.all_user_ids.filtered(
            lambda u: u.employee_id.department_id == self.x_psm_employee_id.department_id
        )

        for user in rgm_users:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=user.id,
                summary='[Xử lý kỷ luật] Hồ sơ cần xem xét: %s' % self.name,
                note='Có hồ sơ vi phạm kỷ luật của nhân viên %s cần bạn xác định cấp xử lý.' % self.x_psm_employee_id.name,
                date_deadline=fields.Date.today()
            )

    def action_psm_generate_compensation_decision(self):
        self.ensure_one()
        report = self._x_psm_get_report_by_name_strict(
            "M02_P0215.report_compensation_decision_template"
        )

        if not report:
            raise UserError(
                "LỖI CẤU HÌNH: Không tìm thấy mẫu báo cáo 'Quyết định Bồi thường'.\n"
                "Giải pháp: Hãy vào Settings -> Reports -> Tìm 'Quyết định Bồi thường'.\n"
                "Nếu không thấy, hãy upgrade lại module."
            )

        # Render with list of IDs to be safe
        pdf_content, _ = report._render_qweb_pdf(report.id, [self.id])
        self.x_psm_compensation_decision_attachment = base64.b64encode(pdf_content)
        safe_name = self.name.replace("/", "_")
        self.x_psm_compensation_decision_filename = f"Quyết định xử lý bồi thường thiệt hại - {safe_name}.pdf"

    def action_psm_hr_submit_meeting(self):
        """Bước 7 → 8: Trình CEO duyệt (thay thế bằng action_psm_submit_for_approval)"""
        self.action_psm_submit_for_approval()

    def action_psm_ceo_approve(self):
        """Bước 8: CEO phê duyệt → Bước 9 (Thông báo)"""
        for rec in self:
            if rec.x_psm_approval_request_id:
                rec.x_psm_approval_request_id.action_approve()
            else:
                rec._x_psm_write_state("notified")
                rec._x_psm_notify_employee()

    def action_psm_open_ceo_reject_wizard(self):
        """Open reason wizard before CEO rejection."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("CEO Rejection Reason"),
            "res_model": "x_psm.hr.discipline.reject.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_x_psm_record_id": self.id,
                "default_x_psm_mode": "ceo_reject",
            },
        }

    def action_psm_ceo_reject(self):
        """Bước 8: CEO từ chối → mở wizard nhập lý do."""
        self.ensure_one()
        return self.action_psm_open_ceo_reject_wizard()

    def action_psm_complete_improvement(self):
        """Legacy: map sang action_psm_expire"""
        self.action_psm_expire()

    def action_psm_done(self):
        """Legacy: map sang action_psm_expire"""
        self.action_psm_expire()

    def action_psm_cancel(self):
        """Cancel the record"""
        self._x_psm_write_state("cancel")

    def _x_psm_cron_auto_expire(self):
        """Cron: Tự động chuyển sang Hết hiệu lực khi quá Ngày kết thúc"""
        today = fields.Date.today()
        records_to_expire = self.search(
            [("state", "=", "active"), ("x_psm_end_date", "<", today)]
        )
        for rec in records_to_expire:
            rec.action_psm_expire()

    def _cron_auto_complete_improvement(self):
        """Legacy alias cho _cron_auto_expire"""
        self._x_psm_cron_auto_expire()
