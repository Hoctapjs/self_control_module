# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError
import logging
from datetime import timedelta

_logger = logging.getLogger(__name__)


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    x_psm_0213_is_offboarding = fields.Boolean(
        string='Is Offboarding',
        default=False,
        groups='approvals.group_approval_manager,base.group_system',
        help='Đánh dấu category này là yêu cầu nghỉ việc (offboarding)'
    )

    def _check_0213_offboarding_flag_access(self):
        if self.env.su:
            return
        if (
            self.env.user.has_group('base.group_system')
            or self.env.user.has_group('approvals.group_approval_manager')
        ):
            return
        raise AccessError(_("Bạn không có quyền thay đổi cấu hình Offboarding."))

    @api.model_create_multi
    def create(self, vals_list):
        if any(vals.get('x_psm_0213_is_offboarding') for vals in vals_list):
            self._check_0213_offboarding_flag_access()
        return super().create(vals_list)

    def write(self, vals):
        if 'x_psm_0213_is_offboarding' in vals:
            new_value = bool(vals.get('x_psm_0213_is_offboarding'))
            if any(category.x_psm_0213_is_offboarding != new_value for category in self):
                self._check_0213_offboarding_flag_access()
        return super().write(vals)


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    _GROUP_0213_OPS_SCOPE = (
        "M02_P0200.GDH_RST_OPS_OC_S",
        "M02_P0200.GDH_RST_OPS_OM_M",
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_S",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_SURVEY_RESULTS = (
        "M02_P0200.GDH_RST_OPS_OM_M",
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_S",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_REMINDER = (
        "M02_P0200.GDH_RST_OPS_OC_S",
        "M02_P0200.GDH_RST_OPS_OM_M",
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_S",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_HR_PROCESS = (
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_DONE = (
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_REHIRE = (
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0213_BLACKLIST = (
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )

    # === Resignation Fields ===
    x_psm_0213_resignation_reason = fields.Text(string="Lý do nghỉ việc")
    x_psm_0213_resignation_reason_id = fields.Many2one("hr.departure.reason", string="Loại nghỉ việc")
    x_psm_0213_resignation_date = fields.Date(string="Ngày nghỉ dự kiến")
    x_psm_0213_official_resignation_date = fields.Date(
        string="Ngày nghỉ việc chính thức",
        compute="_compute_0213_official_resignation_date",
        store=True,
        readonly=False,
        copy=False,
        help=(
            "Ngày làm việc cuối cùng chính thức. Mặc định = 'Ngày nghỉ dự kiến', "
            "HR sửa được. Khi duyệt đơn sẽ ghi vào contract_date_end của nhân viên "
            "để chấm công (work entry) tự dừng."
        ),
    )
    request_status = fields.Selection(
        selection_add=[
            ("done", "Done"),
        ],
        ondelete={"done": "set default"},
    )

    x_psm_0213_is_rehire = fields.Boolean(
        string="Tái tuyển",
        default=False,
        copy=False,
    )
    x_psm_0213_is_blacklisted = fields.Boolean(
        string="Blacklist",
        default=False,
        copy=False,
    )

    # Link to employee -> Standardized field
    x_psm_0213_employee_id = fields.Many2one(
        "hr.employee",
        string="Nhân viên yêu cầu nghỉ việc",
        compute="_compute_employee_id",
        store=True,
    )

    # Related fields for display
    # Related fields for display
    x_psm_0213_resignation_employee_name = fields.Char(
        related="x_psm_0213_employee_id.name", string="Họ tên nhân viên", readonly=True
    )
    x_psm_0213_resignation_manager_name = fields.Char(
        related="x_psm_0213_employee_id.parent_id.name",
        string="Line Manager",
        readonly=True,
    )
    x_psm_0213_resignation_department = fields.Char(
        related="x_psm_0213_employee_id.department_id.name",
        string="Phòng ban",
        readonly=True,
    )
    x_psm_0213_job_id = fields.Many2one(
        related="x_psm_0213_employee_id.job_id",
        string="Chức vụ",
        readonly=True,
    )

    # Employee activities (for offboarding tracking) - includes done activities
    x_psm_0213_employee_activity_ids = fields.Many2many(
        "mail.activity",
        compute="_compute_employee_activity_ids",
        string="Quá trình nghỉ việc",
        compute_sudo=True,
        context={'active_test': False},
    )

    # Check if employee has completed exit interview survey
    x_psm_0213_exit_survey_completed = fields.Boolean(
        string="Đã làm khảo sát",
        compute="_compute_0213_exit_survey_completed",
        store=False,
        compute_sudo=True,
    )

    x_psm_0213_all_activities_completed = fields.Boolean(
        string="Đã hoàn thành mọi công việc",
        compute="_compute_all_activities_completed",
        store=False,
    )

    x_psm_0213_type_contract = fields.Char(
        string="Loại hợp đồng", compute="_compute_type_contract", store=False
    )

    x_psm_0213_is_social_insurance_contract = fields.Boolean(
        string="Di luong BHXH",
        compute="_compute_is_social_insurance_contract",
        store=False,
    )

    x_psm_0213_resignation_owner_email = fields.Char(
        related="request_owner_id.email", string="Email người yêu cầu", readonly=True
    )
    x_psm_0213_is_plan_launched = fields.Boolean(
        string="Đã Launch Plan", default=False, copy=False
    )

    x_psm_0213_adecco_notification_sent = fields.Boolean(
        string="Đã gửi Adecco", default=False, copy=False
    )

    x_psm_0213_exit_survey_user_input_id = fields.Many2one(
        'survey.user_input',
        string='Exit Survey User Input',
        copy=False,
        help='Lưu user_input đã dùng để gửi email khảo sát nghỉ việc, portal sẽ dùng chính link này.',
    )
    x_psm_0200_remaining_al_days = fields.Float(
        related="x_psm_0213_employee_id.x_psm_0200_remaining_al_days",
        string="Remaining Annual Leave Days",
        readonly=True,
        help=(
            "Số phép năm hiện tại của nhân viên (đọc từ hr.employee). "
            "Lưu ý: KHÔNG phải snapshot lịch sử của đơn — giá trị thay đổi "
            "theo trạng thái phép hiện tại của nhân viên."
        ),
    )
    x_psm_0213_al_advance_days = fields.Float(
        string="Advance Annual Leave Days",
        compute="_compute_0213_al_advance",
        store=True,
        help="So ngay phep nam da ung truoc (phan am cua so du phep). Se bi quy doi va tru vao luong quyet toan.",
    )
    x_psm_0213_al_has_advance = fields.Boolean(
        string="Has Advance Annual Leave",
        compute="_compute_0213_al_advance",
        store=True,
    )
    x_psm_0213_al_deduction_currency_id = fields.Many2one(
        "res.currency",
        string="AL Deduction Currency",
        compute="_compute_0213_al_deduction_currency",
        store=True,
    )
    x_psm_0213_al_deduction_rate = fields.Monetary(
        string="AL Deduction Rate (per day)",
        currency_field="x_psm_0213_al_deduction_currency_id",
        copy=False,
        help="Don gia moi ngay phep am. Finance/HR nhap tay.",
    )
    x_psm_0213_al_deduction_amount = fields.Monetary(
        string="AL Deduction Amount",
        currency_field="x_psm_0213_al_deduction_currency_id",
        copy=False,
        help="Tong tien tru luong cho phep ung truoc. Goi y = so ngay am x don gia; cho phep sua tay.",
    )
    x_psm_0213_al_deduction_note = fields.Text(
        string="AL Deduction Note",
        copy=False,
    )
    x_psm_0213_al_settled = fields.Boolean(
        string="Advance AL Settled",
        default=False,
        copy=False,
        readonly=True,
        help="Danh dau phan phep ung truoc da duoc Finance/HR chot quy doi.",
    )

    def _get_0213_company(self):
        self.ensure_one()
        company = False
        if "company_id" in self._fields and self.company_id:
            company = self.company_id
        elif self.x_psm_0213_employee_id and self.x_psm_0213_employee_id.company_id:
            company = self.x_psm_0213_employee_id.company_id
        elif self.request_owner_id and self.request_owner_id.company_id:
            company = self.request_owner_id.company_id
        return company or self.env.company

    def _get_0213_social_insurance_contract_type_ids(self):
        self.ensure_one()
        return self._get_0213_company().x_psm_0213_social_insurance_contract_type_ids

    def _get_0213_al_leave_types(self):
        company = self[:1]._get_0213_company() if self else self.env.company
        leave_types = company.x_psm_0213_al_leave_type_ids
        if not leave_types:
            leave_types = self.env["hr.leave.type"].sudo().search(
                [("requires_allocation", "=", True)]
            )
        return leave_types

    def _get_0213_remaining_al(self, employee):
        if not employee:
            return 0.0

        leave_types = self._get_0213_al_leave_types()
        if not leave_types:
            return 0.0

        allocations = self.env["hr.leave.allocation"].sudo().search(
            [
                ("employee_id", "=", employee.id),
                ("state", "=", "validate"),
                ("holiday_status_id", "in", leave_types.ids),
            ]
        )
        remaining_days = (
            allocation.number_of_days - allocation.leaves_taken
            for allocation in allocations
        )
        return sum(remaining_days, 0.0)

    def _is_0213_social_insurance_contract(self):
        self.ensure_one()
        contract_types = self._get_0213_social_insurance_contract_type_ids()
        employee = self.x_psm_0213_employee_id.sudo()
        contract_type = False

        if employee:
            if (
                "contract_id" in employee._fields
                and employee.contract_id
                and "contract_type_id" in employee.contract_id._fields
            ):
                contract_type = employee.contract_id.contract_type_id
            if not contract_type and "contract_type_id" in employee._fields:
                contract_type = employee.contract_type_id

        if contract_types:
            return bool(contract_type and contract_type in contract_types)

        return self.x_psm_0213_type_contract == "Full-Time"

    def _get_0213_reminder_overdue_days(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0213_reminder_overdue_days', '0')
        return int(param_val or 0)

    def _get_0213_reminder_extension_days(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0213_reminder_extension_days', '4')
        return int(param_val or 4)

    def _get_0213_exit_survey_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_exit_survey_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_exit_survey",
            raise_if_not_found=False,
        )

    def _get_0213_adecco_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_adecco_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_adecco_notification",
            raise_if_not_found=False,
        )

    def _get_0213_social_insurance_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_social_insurance_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_social_insurance",
            raise_if_not_found=False,
        )

    def _get_0213_employee_reminder_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_employee_reminder_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_offboarding_reminder",
            raise_if_not_found=False,
        )

    def _get_0213_department_reminder_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_department_reminder_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_dept_offboarding_reminder",
            raise_if_not_found=False,
        )

    def _get_0213_completion_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_completion_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_offboarding_completion",
            raise_if_not_found=False,
        )

    def _get_0213_employee_approved_template(self):
        self.ensure_one()
        company_template = self._get_0213_company().x_psm_0213_employee_approved_template_id
        return company_template or self.env.ref(
            "M02_P0213.psm_0213_email_template_employee_approved_notification",
            raise_if_not_found=False,
        )

    @api.model
    def _get_0213_activity_template_summaries(self):
        plan = self.env.ref(
            "M02_P0213.psm_0213_offboarding_activity_plan",
            raise_if_not_found=False,
        )
        if not plan:
            return set()
        return set(summary for summary in plan.template_ids.mapped("summary") if summary)

    def _filter_0213_offboarding_activities(self, activities):
        self.ensure_one()
        template_summaries = self._get_0213_activity_template_summaries()
        employee_id = self.x_psm_0213_employee_id.id if self.x_psm_0213_employee_id else False

        return activities.filtered(
            lambda act: (
                act.res_model == "approval.request"
                and act.res_id == self.id
            )
            or (
                employee_id
                and act.res_model == "hr.employee"
                and act.res_id == employee_id
                and act.summary in template_summaries
            )
        )

    def _get_0213_default_responsible_user(self, template):
        self.ensure_one()
        company = self._get_0213_company()
        summary = (template.summary or "").strip().lower()
        note = (template.note or "").strip().lower()
        combined_text = " ".join(part for part in [summary, note] if part)

        it_keywords = (
            "email",
            "odoo",
            "erp",
            "ldap",
            "vpn",
            "active directory",
            "tài khoản email",
            "tai khoan email",
            "tài khoản hệ thống",
            "tai khoan he thong",
            "hệ thống",
            "he thong",
        )
        if any(keyword in combined_text for keyword in it_keywords):
            department = self.x_psm_0213_employee_id.sudo().department_id
            store_it = department.x_psm_0213_it_user_id if department else False
            return (
                store_it
                or company.x_psm_0213_default_it_user_id
                or company.x_psm_0213_default_on_demand_user_id
            )

        return company.x_psm_0213_default_on_demand_user_id

    @api.model
    def _get_0213_resignation_category(self):
        return self.env.ref(
            "M02_P0213.psm_0213_approval_category_resignation",
            raise_if_not_found=False,
        )

    @api.model
    def _get_0213_exit_survey(self):
        survey = self.env.ref(
            "M02_P0213.psm_0213_survey_exit_interview",
            raise_if_not_found=False,
        )
        return survey.sudo() if survey else self.env["survey.survey"]

    def _is_0213_offboarding_request(self):
        self.ensure_one()
        resignation_category = self._get_0213_resignation_category()
        return bool(
            resignation_category
            and self.category_id
            and self.category_id.id == resignation_category.id
        )

    def _ensure_0213_offboarding_request(self):
        self.ensure_one()
        if not self._is_0213_offboarding_request():
            raise UserError(_("Thao tác này chỉ áp dụng cho đơn nghỉ việc OPS 0213."))
        return True

    def _check_0213_official_resignation_date(self):
        """Chan duyet neu ngay nghi chinh thuc som hon ngay bat dau hop dong."""
        for request in self:
            if not request._is_0213_offboarding_request():
                continue
            employee = request.x_psm_0213_employee_id
            official_date = request.x_psm_0213_official_resignation_date
            if not employee or not official_date:
                continue
            version = employee.sudo().version_id
            if version.contract_date_start and version.contract_date_start > official_date:
                raise UserError(_(
                    "Ngày nghỉ việc chính thức (%(date)s) không được sớm hơn ngày bắt đầu "
                    "hợp đồng của nhân viên %(name)s.",
                    date=official_date,
                    name=employee.name,
                ))

    def _push_0213_contract_end_date(self):
        """Ghi ngay nghi viec chinh thuc vao contract_date_end cua version hien tai."""
        for request in self:
            if not request._is_0213_offboarding_request():
                continue
            employee = request.x_psm_0213_employee_id
            official_date = request.x_psm_0213_official_resignation_date
            request._write_0213_contract_date_end(employee, official_date)

    def _write_0213_contract_date_end(self, employee, official_date):
        if not employee or not official_date:
            return False

        employee_sudo = employee.sudo()
        version = employee_sudo.version_id
        if not version:
            return False

        if not version.contract_date_start:
            _logger.warning(
                "Skip writing contract_date_end for employee %s because current "
                "hr.version has no contract_date_start.",
                employee_sudo.id,
            )
            return False

        employee_sudo.write({"contract_date_end": official_date})
        return True

    def _apply_0213_native_departure(self):
        """Ghi nhan nghi viec theo co che native va archive ho so nhan vien."""
        for request in self:
            if not request._is_0213_offboarding_request():
                continue
            employee = request.x_psm_0213_employee_id
            if not employee:
                continue
            official_date = request.x_psm_0213_official_resignation_date
            departure_vals = {}
            if official_date:
                departure_vals["departure_date"] = official_date
            if request.x_psm_0213_resignation_reason_id:
                departure_vals["departure_reason_id"] = (
                    request.x_psm_0213_resignation_reason_id.id
                )
            if departure_vals:
                employee.sudo().write(departure_vals)
            request._write_0213_contract_date_end(employee, official_date)
            if employee.active:
                employee.sudo().with_context(no_wizard=True).action_archive()

    def _get_0213_employee_email(self, employee=None):
        self.ensure_one()
        employee = employee or self.x_psm_0213_employee_id
        if not employee:
            return False

        email_candidates = [
            employee.work_email,
            employee.private_email if "private_email" in employee._fields else False,
            employee.user_id.partner_id.email if employee.user_id else False,
            self.request_owner_id.partner_id.email if self.request_owner_id else False,
            self.request_owner_id.email if self.request_owner_id else False,
        ]
        return next((email for email in email_candidates if email), False)

    @api.model
    def _is_matching_0213_survey_user_input(
        self,
        user_input,
        partner=None,
        resignation_request=None,
        done_only=False,
    ):
        if not user_input:
            return False

        survey = self._get_0213_exit_survey()
        if not survey or user_input.survey_id != survey:
            return False

        if done_only and user_input.state != "done":
            return False

        if partner:
            matches_partner = bool(user_input.partner_id == partner)
            partner_email = (partner.email or "").strip().lower()
            user_input_email = (user_input.email or "").strip().lower()
            matches_email = bool(partner_email and user_input_email == partner_email)
            if not (matches_partner or matches_email):
                return False

        if resignation_request and not resignation_request._is_0213_offboarding_request():
            return False

        return True

    @api.model
    def _get_or_create_0213_survey_user_input(
        self,
        partner,
        resignation_request=None,
        create_if_missing=False,
    ):
        survey = self._get_0213_exit_survey()
        if not survey or not partner:
            return self.env["survey.user_input"].sudo().browse()

        user_input = self.env["survey.user_input"].sudo().browse()
        if resignation_request and resignation_request.x_psm_0213_exit_survey_user_input_id:
            stored_user_input = resignation_request.x_psm_0213_exit_survey_user_input_id.sudo()
            if self._is_matching_0213_survey_user_input(
                stored_user_input,
                partner=partner,
                resignation_request=resignation_request,
            ):
                user_input = stored_user_input

        if not user_input:
            candidates = self.env["survey.user_input"].sudo().search(
                [
                    ("survey_id", "=", survey.id),
                    "|",
                    ("partner_id", "=", partner.id),
                    ("email", "=", partner.email),
                ],
                order="create_date desc",
            )
            user_input = candidates.filtered(
                lambda candidate: self._is_matching_0213_survey_user_input(
                    candidate,
                    partner=partner,
                    resignation_request=resignation_request,
                )
            )[:1]

        if not user_input and create_if_missing:
            user_input = self.env["survey.user_input"].sudo().create(
                {
                    "survey_id": survey.id,
                    "partner_id": partner.id,
                    "email": partner.email,
                }
            )

        if (
            resignation_request
            and user_input
            and not resignation_request.x_psm_0213_exit_survey_user_input_id
        ):
            resignation_request.sudo().write(
                {"x_psm_0213_exit_survey_user_input_id": user_input.id}
            )

        return user_input

    def _get_0213_exit_survey_user_inputs(self, done_only=False):
        self.ensure_one()
        if not self._is_0213_offboarding_request():
            return self.env["survey.user_input"]

        survey = self._get_0213_exit_survey()
        if not survey or not self.request_owner_id:
            return self.env["survey.user_input"]

        partner = self.request_owner_id.partner_id
        user_inputs = self.env["survey.user_input"].sudo().browse()
        if self.x_psm_0213_exit_survey_user_input_id:
            stored_user_input = self.x_psm_0213_exit_survey_user_input_id.sudo()
            if self._is_matching_0213_survey_user_input(
                stored_user_input,
                partner=partner,
                resignation_request=self,
                done_only=done_only,
            ):
                user_inputs |= stored_user_input

        candidates = self.env["survey.user_input"].sudo().search(
            [
                ("survey_id", "=", survey.id),
                "|",
                ("partner_id", "=", partner.id),
                ("email", "=", self.request_owner_id.email),
            ],
            order="create_date desc",
        )
        user_inputs |= candidates.filtered(
            lambda candidate: self._is_matching_0213_survey_user_input(
                candidate,
                partner=partner,
                resignation_request=self,
                done_only=done_only,
            )
        )
        return user_inputs

    def _check_0213_group_access(self, action_label, allowed_groups):
        if self.env.su or self.env.context.get("bypass_0213_group_check"):
            return

        offboarding_requests = self.filtered(lambda req: req._is_0213_offboarding_request())
        if not offboarding_requests:
            return

        if any(self.env.user.has_group(group_xmlid) for group_xmlid in allowed_groups):
            return

        raise AccessError(
            _("Bạn không có quyền thực hiện thao tác: %s.") % action_label
        )

    @api.model
    def _get_overdue_activities_by_request(self, requests, today=None):
        activities_by_request = {}
        if not requests:
            return activities_by_request

        today = today or fields.Date.today()
        requests = requests.filtered(lambda req: req.x_psm_0213_employee_id)
        if not requests:
            return activities_by_request

        request_ids = requests.ids
        employee_ids = requests.mapped("x_psm_0213_employee_id").ids
        all_activities = self.env["mail.activity"].sudo().search([
            ("active", "=", True),
            ("date_deadline", "<", today),
            "|",
            "&", ("res_model", "=", "approval.request"), ("res_id", "in", request_ids),
            "&", ("res_model", "=", "hr.employee"), ("res_id", "in", employee_ids),
        ])

        requests_by_id = {req.id: req for req in requests}
        requests_by_employee_id = {
            req.x_psm_0213_employee_id.id: req
            for req in requests
            if req.x_psm_0213_employee_id
        }
        grouped_ids = {req.id: [] for req in requests}

        for activity in all_activities:
            related_request = False
            if activity.res_model == "approval.request":
                related_request = requests_by_id.get(activity.res_id)
            elif activity.res_model == "hr.employee":
                related_request = requests_by_employee_id.get(activity.res_id)

            if related_request:
                grouped_ids.setdefault(related_request.id, []).append(activity.id)

        Activity = self.env["mail.activity"].sudo()
        for req in requests:
            overdue_days = req._get_0213_reminder_overdue_days()
            activities = req._filter_0213_offboarding_activities(
                Activity.browse(grouped_ids.get(req.id, []))
            )
            filtered_activities = activities.filtered(
                lambda act: act.date_deadline
                and (today - act.date_deadline).days > overdue_days
            )
            activities_by_request[req.id] = filtered_activities
        return activities_by_request

    @api.model
    def _group_activities_by_user(self, activities):
        grouped_ids = {}
        for activity in activities:
            if activity.user_id:
                grouped_ids.setdefault(activity.user_id.id, []).append(activity.id)

        Activity = self.env["mail.activity"].sudo()
        return {
            user_id: Activity.browse(activity_ids)
            for user_id, activity_ids in grouped_ids.items()
        }

    def action_withdraw(self):
        """
        Override action_withdraw to prevent withdrawing Resignation requests
        after they have been approved or refused.
        """
        resignation_category = self._get_0213_resignation_category()
        for request in self:
            # Kiểm tra nếu Category là "Resignation" (hoặc ID cụ thể)
            # Và trạng thái đang là Approved hoặc Refused
            if (
                resignation_category
                and request.category_id
                and request.category_id.id == resignation_category.id
                and request.request_status in ["approved", "refused"]
            ):
                raise UserError(
                    _(
                        "Bạn không thể rút lại yêu cầu Thôi việc (Resignation) sau khi đã được Phê duyệt hoặc Từ chối."
                    )
                )

        # Nếu không thỏa điều kiện trên, chạy logic gốc của Odoo
        return super(ResignationRequest, self).action_withdraw()

    # Override action_cancel to block the Cancel button
    def action_cancel(self):
        resignation_category = self._get_0213_resignation_category()
        for request in self:
            if (
                resignation_category
                and request.category_id
                and request.category_id.id == resignation_category.id
                and request.request_status in ["approved", "refused"]
            ):
                raise UserError(
                    _("Không thể hủy yêu cầu này khi đã có kết quả cuối cùng.")
                )
        return super(ResignationRequest, self).action_cancel()

    def action_send_adecco_notification(self):
        self._check_0213_group_access(
            _("Gửi thông tin Adecco"), self._GROUP_0213_HR_PROCESS
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        if not self.x_psm_0213_employee_id:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Lỗi",
                    "message": "Không tìm thấy nhân viên gắn với đơn nghỉ việc.",
                    "type": "danger",
                },
            }
        if self.x_psm_0213_is_social_insurance_contract:
            raise UserError(
                _("Đơn này đang đi luồng BHXH, không áp dụng gửi thông tin Adecco.")
            )

        template = self._get_0213_adecco_template()
        email_to = self._get_0213_company().x_psm_0213_adecco_notification_email

        if template and email_to:
            template.sudo().send_mail(
                self.x_psm_0213_employee_id.id,
                force_send=True,
                email_values={"email_to": email_to},
            )
            self.sudo().write({'x_psm_0213_adecco_notification_sent': True})
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Thành công",
                    "message": "Đã gửi thông báo cho Adecco.",
                    "type": "success",
                    "next": {"type": "ir.actions.client", "tag": "soft_reload"},
                },
            }
        missing_parts = []
        if not template:
            missing_parts.append("Email Template Adecco")
        if not email_to:
            missing_parts.append("email Adecco trong cấu hình công ty")

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Lỗi",
                "message": "Thiếu cấu hình: %s." % ", ".join(missing_parts),
                "type": "danger",
            },
        }

    @api.depends("x_psm_0213_employee_id")
    def _compute_type_contract(self):
        for request in self:
            contract_name = ""
            employee = request.x_psm_0213_employee_id.sudo()
            if employee:
                contract_type = False
                employee_fields = employee._fields

                # Ưu tiên lấy từ contract_id nếu môi trường có module hr_contract.
                if "contract_id" in employee_fields:
                    contract = employee.contract_id.sudo()
                    if contract and "contract_type_id" in contract._fields:
                        contract_type = contract.contract_type_id

                # Fallback: lấy trực tiếp từ employee nếu field này tồn tại.
                if not contract_type and "contract_type_id" in employee_fields:
                    contract_type = employee.contract_type_id

                if contract_type:
                    contract_name = contract_type.name

            request.x_psm_0213_type_contract = contract_name

    @api.depends("x_psm_0213_employee_id", "x_psm_0213_type_contract")
    def _compute_is_social_insurance_contract(self):
        for request in self:
            request.x_psm_0213_is_social_insurance_contract = request._is_0213_social_insurance_contract()

    @api.depends("x_psm_0213_employee_id", "x_psm_0213_employee_activity_ids", "x_psm_0213_is_plan_launched")
    def _compute_all_activities_completed(self):
        for request in self:
            if not request.x_psm_0213_is_plan_launched:
                request.x_psm_0213_all_activities_completed = False
                continue

            # Đếm các activity còn active (chưa done) trên approval.request và hr.employee
            pending_activities = self.env["mail.activity"].sudo().search([
                ("active", "=", True),
                "|",
                "&", ("res_model", "=", "approval.request"), ("res_id", "=", request.id),
                "&", ("res_model", "=", "hr.employee"), ("res_id", "=", request.x_psm_0213_employee_id.id if request.x_psm_0213_employee_id else 0),
            ])
            pending_count = len(request._filter_0213_offboarding_activities(pending_activities))
            request.x_psm_0213_all_activities_completed = (pending_count == 0)

    def action_send_social_insurance(self):
        self._check_0213_group_access(
            _("Gửi thông tin bảo hiểm xã hội"), self._GROUP_0213_HR_PROCESS
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        if not self.x_psm_0213_employee_id:
            return
        if not self.x_psm_0213_is_social_insurance_contract:
            raise UserError(
                _("Đơn này không thuộc luồng BHXH theo cấu hình loại hợp đồng hiện tại.")
            )

        template = self._get_0213_social_insurance_template()
        email_to = self._get_0213_employee_email(self.x_psm_0213_employee_id)

        if not email_to:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Lỗi",
                    "message": "Không tìm thấy email của nhân viên.",
                    "type": "danger",
                },
            }

        if template and email_to:
            template.sudo().send_mail(
                self.x_psm_0213_employee_id.id,
                force_send=True,
                email_values={"email_to": email_to},
            )
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Thành công",
                    "message": "Đã gửi thông tin BHXH qua email.",
                    "type": "success",
                },
            }
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Lỗi",
                    "message": "Không tìm thấy Email Template BHXH.",
                    "type": "danger",
                },
            }

    @api.depends("request_owner_id")
    def _compute_0213_exit_survey_completed(self):
        """Check if request_owner has completed exit interview survey"""
        survey = self._get_0213_exit_survey()
        for request in self:
            completed = False
            if survey and request.request_owner_id and request._is_0213_offboarding_request():
                user_input = request._get_0213_exit_survey_user_inputs(done_only=True)[:1]
                completed = bool(user_input)
            request.x_psm_0213_exit_survey_completed = completed

    def action_view_survey_results(self):
        """
        Open the survey.user_input form for the completed exit survey.
        """
        self._check_0213_group_access(
            _("Xem kết quả khảo sát"), self._GROUP_0213_SURVEY_RESULTS
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()

        user_inputs = self._get_0213_exit_survey_user_inputs(done_only=True)

        if not user_inputs:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Thông báo",
                    "message": "Không tìm thấy kết quả khảo sát đã hoàn thành.",
                    "type": "warning",
                },
            }

        # If multiple, show list. If one, show form.
        action = {
            "name": "Kết quả khảo sát",
            "type": "ir.actions.act_window",
            "res_model": "survey.user_input",
            "context": {"create": False},
        }
        if len(user_inputs) == 1:
            action.update(
                {
                    "view_mode": "form",
                    "res_id": user_inputs.id,
                }
            )
        else:
            action.update(
                {
                    "view_mode": "list,form",
                    "domain": [("id", "in", user_inputs.ids)],
                }
            )
        return action

    # Danh sách activity có res_name trùng tên nhân viên/owner
    # Dùng Many2many cho list computed không có inverse field
    x_psm_0213_owner_related_activity_ids = fields.Many2many(
        "mail.activity",
        related="x_psm_0213_employee_activity_ids",
        string="Hoạt động liên quan (Res Name)",
        readonly=True,
    )

    @api.depends("x_psm_0213_employee_id")
    def _compute_owner_related_activity_ids(self):
        # Compute bằng cùng env để tránh lệch cache, đồng thời luôn fallback về rỗng nếu có lỗi.
        Activity = self.env["mail.activity"].with_context(active_test=False)
        empty_activities = Activity.browse([])
        for request in self:
            try:
                activities = empty_activities
                if request.x_psm_0213_employee_id:
                    activities = Activity.search(
                        [
                            ("res_model", "=", "hr.employee"),
                            ("res_id", "=", request.x_psm_0213_employee_id.id),
                            ("active", "in", [True, False]),
                        ]
                    )
                    _logger.debug(
                        "OWNER ACTIVITIES: Employee ID=%s, Found %s activity IDs: %s",
                        request.x_psm_0213_employee_id.id,
                        len(activities.ids),
                        activities.ids,
                    )
                request.x_psm_0213_owner_related_activity_ids = activities
            except Exception:
                _logger.exception(
                    "Failed computing x_psm_0213_owner_related_activity_ids for approval.request %s",
                    request.id,
                )
                request.x_psm_0213_owner_related_activity_ids = empty_activities

    @api.depends("x_psm_0213_employee_id")
    def _compute_employee_activity_ids(self):
        """Compute activities (active + done) on approval.request and hr.employee"""
        ActivitySudo = self.env["mail.activity"].sudo().with_context(active_test=False)
        for request in self:
            if not request.id or not request.x_psm_0213_employee_id:
                request.x_psm_0213_employee_activity_ids = ActivitySudo.browse([])
                continue

            # Dùng SQL để bypass mọi bộ lọc active=False của Odoo
            activities = ActivitySudo.search(
                [
                    "|",
                    "&", ("res_model", "=", "approval.request"), ("res_id", "=", request.id),
                    "&", ("res_model", "=", "hr.employee"), ("res_id", "=", request.x_psm_0213_employee_id.id),
                ]
            )
            request.x_psm_0213_employee_activity_ids = activities

    @api.depends('request_owner_id', 'partner_id')
    def _compute_employee_id(self):
        for request in self:
            employee = False
            # 1. Partner First
            if request.partner_id:
                employee = self.env["hr.employee"].search(
                    [
                        (
                            "work_contact_id",
                            "=",
                            request.partner_id.id,
                        )
                    ],
                    limit=1,
                )
            # 2. User Fallback
            if not employee and request.request_owner_id:
                employee = self.env["hr.employee"].search(
                    [("user_id", "=", request.request_owner_id.id)], limit=1
                )
            
            request.x_psm_0213_employee_id = employee.id if employee else False

    @api.depends("x_psm_0213_resignation_date")
    def _compute_0213_official_resignation_date(self):
        """Mac dinh = ngay nghi du kien, khong ghi de gia tri HR da sua."""
        for request in self:
            if not request.x_psm_0213_official_resignation_date:
                request.x_psm_0213_official_resignation_date = (
                    request.x_psm_0213_resignation_date
                )

    @api.depends("x_psm_0213_employee_id.x_psm_0200_remaining_al_days")
    def _compute_0213_al_advance(self):
        for request in self:
            advance = -(request.x_psm_0213_employee_id.x_psm_0200_remaining_al_days or 0.0)
            request.x_psm_0213_al_advance_days = advance if advance > 0 else 0.0
            request.x_psm_0213_al_has_advance = advance > 0

    @api.depends("company_id")
    def _compute_0213_al_deduction_currency(self):
        for request in self:
            company = request._get_0213_company() if request else self.env.company
            request.x_psm_0213_al_deduction_currency_id = (
                company.currency_id.id if company else self.env.company.currency_id.id
            )

    @api.onchange("x_psm_0213_al_deduction_rate", "x_psm_0213_al_advance_days")
    def _onchange_0213_al_deduction_amount(self):
        for request in self:
            if request.x_psm_0213_al_deduction_rate and request.x_psm_0213_al_advance_days:
                request.x_psm_0213_al_deduction_amount = (
                    request.x_psm_0213_al_advance_days
                    * request.x_psm_0213_al_deduction_rate
                )

    def write(self, vals):
        res = super().write(vals)
        if "x_psm_0213_official_resignation_date" in vals:
            self.filtered(
                lambda request: request.request_status in ("approved", "done")
            )._push_0213_contract_end_date()
        return res

    def action_approve(self, approver=None):
        """
        Override: Xử lý khi duyệt yêu cầu nghỉ việc
        """
        category_id = self.env.ref(
            "M02_P0213.psm_0213_approval_category_resignation",
            raise_if_not_found=False,
        )
        if category_id:
            self.filtered(
                lambda request: request.category_id
                and request.category_id.id == category_id.id
            )._check_0213_official_resignation_date()

        res = super(ResignationRequest, self).action_approve(approver)

        # Lấy plan offboarding
        plan = self.env.ref(
            "M02_P0213.psm_0213_offboarding_activity_plan",
            raise_if_not_found=False,
        )

        for request in self:
            if category_id and request.category_id and request.category_id.id == category_id.id:
                remaining_al = request._get_0213_remaining_al(
                    request.x_psm_0213_employee_id
                )
                if request.x_psm_0213_employee_id:
                    request.x_psm_0213_employee_id.sudo().write(
                        {"x_psm_0200_remaining_al_days": remaining_al}
                    )
                approved_template = request._get_0213_employee_approved_template()
                approved_email_to = (
                    request.request_owner_id.partner_id.email
                    or request.request_owner_id.email
                    or request.x_psm_0213_employee_id.work_email
                )
                if approved_template and approved_email_to:
                    try:
                        approved_template.sudo().send_mail(
                            request.id,
                            force_send=True,
                            email_values={"email_to": approved_email_to},
                        )
                        body_text = _("Hệ thống: Đã gửi email thông báo duyệt đơn nghỉ việc tới %s") % approved_email_to
                        request.message_post(
                            body=Markup(
                                "<div class='o_0213_success'><i class='fa fa-check-circle'></i> %s</div>"
                            ) % body_text
                        )
                    except Exception as e:
                        _logger.error(
                            f"OPS 0213: Failed to send employee approved email for request {request.id}: {str(e)}"
                        )
                request.action_send_exit_survey()
                request._push_0213_contract_end_date()

                # Schedule "To Do" activity for the request owner
                # if request.request_owner_id:
                #     request.activity_schedule(
                #         "mail.mail_activity_data_todo",
                #         user_id=request.request_owner_id.id,
                #         summary="Hoàn tất thủ tục nghỉ việc",
                #         note="Yêu cầu nghỉ việc đã được duyệt. Vui lòng thực hiện các công việc bàn giao và khảo sát.",
                #     )

                # Tự động launch offboarding plan
                if plan and request.x_psm_0213_employee_id:
                    request._schedule_offboarding_activities(plan)
                    request.sudo().write({'x_psm_0213_is_plan_launched': True})

        return res

    def _schedule_offboarding_activities(self, plan):
        """
        Tự động tạo activities từ offboarding plan khi Manager approve.
        """
        self.ensure_one()
        from dateutil.relativedelta import relativedelta

        employee = self.x_psm_0213_employee_id.sudo()
        employee_user = employee.user_id or self.request_owner_id
        manager_user = employee.parent_id.user_id
        date_today = fields.Date.today()

        for template in plan.template_ids:
            # Xác định người phụ trách
            if template.responsible_type == 'employee':
                responsible = employee_user
            elif template.responsible_type == 'manager':
                responsible = manager_user
            elif template.responsible_type == 'on_demand':
                responsible = (
                    template.responsible_id
                    or self._get_0213_default_responsible_user(template)
                    or self.env.user
                )
            else:
                responsible = self.env.user

            if not responsible:
                responsible = self.env.user

            # Tính deadline
            date_deadline = date_today
            if template.delay_count > 0:
                delta = (
                    relativedelta(days=template.delay_count) if template.delay_unit == 'days'
                    else relativedelta(weeks=template.delay_count) if template.delay_unit == 'weeks'
                    else relativedelta(months=template.delay_count)
                )
                date_deadline = date_today + delta

            try:
                self.env['mail.activity'].sudo().create({
                    'res_model_id': self.env['ir.model']._get_id('approval.request'),
                    'res_id': self.id,
                    'activity_type_id': template.activity_type_id.id,
                    'summary': template.summary,
                    'note': template.note,
                    'user_id': responsible.id,
                    'date_deadline': date_deadline,
                    'automated': True,
                    'active': True,
                })
            except Exception as e:
                _logger.error(
                    f"[OPS] Error creating offboarding activity from template {template.id}: {str(e)}",
                    exc_info=True,
                )

    def action_launch_plan(self):
        """
        Mở wizard Launch Plan với context là hr.employee
        """

        self.ensure_one()
        self._ensure_0213_offboarding_request()
        if not self.x_psm_0213_employee_id:
            return False
        self.x_psm_0213_is_plan_launched = True
        # Lấy action plan_wizard_action từ module hr
        action = self.env.ref("hr.plan_wizard_action").sudo().read()[0]

        # Thay đổi context để wizard nhận employee thay vì approval.request
        action["context"] = {
            "active_model": "hr.employee",
            "active_id": self.x_psm_0213_employee_id.id,
            "active_ids": [self.x_psm_0213_employee_id.id],
            "plan_mode": True,
        }

        return action

    def action_send_exit_survey(self):
        """
        Override: Gửi email chứa link khảo sát Exit Interview (Template M14)
        """
        self.ensure_one()

        # Lấy survey Exit Interview
        survey = self.env.ref(
            "M02_P0213.psm_0213_survey_exit_interview", raise_if_not_found=False
        )
        if not survey:
            return super().action_send_exit_survey() # Fallback or error

        # Lấy email của request owner
        partner = self.request_owner_id.partner_id
        if not partner or not partner.email:
             return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Lỗi",
                    "message": "Không tìm thấy email của người yêu cầu!",
                    "type": "danger",
                },
            }

        user_input = self._get_or_create_0213_survey_user_input(
            partner=partner,
            resignation_request=self,
            create_if_missing=True,
        )
        if not user_input:
            return super().action_send_exit_survey()

        # Lấy link survey
        survey_url = user_input.get_start_url()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        full_survey_url = base_url + survey_url

        # Lấy email template
        template = self._get_0213_exit_survey_template()

        if template:
            # Gửi email bằng template
            template.with_context(survey_url=full_survey_url).send_mail(
                self.id, force_send=True, email_values={"email_to": partner.email}
            )
        else:
            # Fallback to super logic (manual email) if template missing
            return super().action_send_exit_survey()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Thành công",
                "message": f"Đã gửi email khảo sát đến {partner.email}",
                "type": "success",
            },
        }

    def action_done(self):
        """
        Hoàn tất quy trình nghỉ việc:
        - Kiểm tra exit_survey_completed và all_activities_completed
        - Chuyển trạng thái sang 'done'
        - Vô hiệu hóa tài khoản portal/internal của nhân viên
        """
        offboarding_requests = self.filtered(lambda req: req._is_0213_offboarding_request())
        other_requests = self - offboarding_requests
        result = False
        if other_requests and hasattr(super(ResignationRequest, other_requests), "action_done"):
            result = super(ResignationRequest, other_requests).action_done()
        if not offboarding_requests:
            return result

        self._check_0213_group_access(
            _("Hoàn thành nghỉ việc"), self._GROUP_0213_DONE
        )
        for request in offboarding_requests:
            if not request.x_psm_0213_exit_survey_completed:
                raise UserError(
                    _("Vui lòng hoàn thành khảo sát Nghỉ việc trước khi Hoàn tất quy trình.")
                )
            if not request.x_psm_0213_all_activities_completed:
                raise UserError(
                    _("Vui lòng hoàn thành tất cả công việc Offboarding trước khi Hoàn tất quy trình.")
                )

        offboarding_requests.sudo().write({"request_status": "done"})

        for request in offboarding_requests:
            request_sudo = request.sudo()
            completion_template = request._get_0213_completion_template()
            completion_email_to = (
                request_sudo.request_owner_id.partner_id.email
                or request_sudo.request_owner_id.email
            )
            if completion_template and completion_email_to:
                try:
                    completion_template.sudo().send_mail(
                        request.id,
                        force_send=True,
                        email_values={"email_to": completion_email_to},
                    )
                    body_text = _("Hệ thống: Đã gửi email cảm ơn hoàn tất offboarding tới %s") % completion_email_to
                    request.message_post(
                        body=Markup(
                            "<div class='o_0213_success'><i class='fa fa-check-circle'></i> %s</div>"
                        ) % body_text
                    )
                except Exception as e:
                    _logger.error(
                        f"OPS 0213: Failed to send completion email for request {request.id}: {str(e)}"
                    )

            request._apply_0213_native_departure()

            # Tìm user cần vô hiệu hóa
            user_to_deactivate = False

            # Ưu tiên 1: employee.user_id
            if request_sudo.x_psm_0213_employee_id and request_sudo.x_psm_0213_employee_id.user_id:
                user_to_deactivate = request_sudo.x_psm_0213_employee_id.user_id

            # Ưu tiên 2: request_owner_id (portal user)
            if not user_to_deactivate and request_sudo.request_owner_id:
                user_to_deactivate = request_sudo.request_owner_id

            if user_to_deactivate and user_to_deactivate.active:
                is_portal = user_to_deactivate.has_group('base.group_portal')
                is_internal = user_to_deactivate.has_group('base.group_user')
                if (is_portal or is_internal) and not user_to_deactivate.has_group('base.group_system'):
                    try:
                        user_to_deactivate.write({'active': False})
                        body_text = _("Hệ thống: Đã vô hiệu hóa tài khoản Portal/User: %s (%s)") % (
                            user_to_deactivate.name,
                            user_to_deactivate.login,
                        )
                        request.message_post(
                            body=Markup(
                                "<div class='o_0213_success'><i class='fa fa-check-circle'></i> %s</div>"
                            ) % body_text
                        )
                    except Exception as e:
                        _logger.error(
                            f"OPS 0213: Failed to deactivate user {user_to_deactivate.id}: {str(e)}"
                        )

            # Tự động hoàn thành các activity To-Do còn lại của request_owner
            if request_sudo.request_owner_id:
                todo_type = self.env.ref(
                    "mail.mail_activity_data_todo", raise_if_not_found=False
                )
                domain = [
                    ("res_model", "=", "approval.request"),
                    ("res_id", "=", request.id),
                    ("user_id", "=", request_sudo.request_owner_id.id),
                ]
                if todo_type:
                    domain.append(("activity_type_id", "=", todo_type.id))
                activities = self.env["mail.activity"].search(domain)
                if activities:
                    activities.action_feedback(
                        feedback="Đã hoàn thành thủ tục nghỉ việc."
                    )
        return result

    def action_rehire(self):
        """Đánh dấu nhân viên được tái tuyển dụng."""
        self._check_0213_group_access(_("Tái tuyển"), self._GROUP_0213_REHIRE)
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        self.sudo().write({"x_psm_0213_is_rehire": True})
        subtype = self.env.ref(
            'M02_P0213.mail_mt_0213_notification',
            raise_if_not_found=False,
        )
        body = Markup(
            "<div class='o_0213_success'><i class='fa fa-check-circle'></i> %s</div>"
        ) % _("Thông báo hệ thống: Đã đánh dấu: Tái tuyển")
        post_kwargs = {
            'body': body,
        }
        if subtype:
            post_kwargs['subtype_id'] = subtype.id
        self.message_post(**post_kwargs)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Tái tuyển",
                "message": "Đã đánh dấu nhân viên đủ điều kiện tái tuyển.",
                "type": "success",
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }

    def action_blacklist(self):
        """Đánh dấu nhân viên vào danh sách đen."""
        self._check_0213_group_access(
            _("Đưa vào Blacklist"), self._GROUP_0213_BLACKLIST
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        self.sudo().write({"x_psm_0213_is_blacklisted": True})
        subtype = self.env.ref(
            'M02_P0213.mail_mt_0213_notification',
            raise_if_not_found=False,
        )
        body = Markup(
            "<div class='o_0213_error'><i class='fa fa-ban'></i> %s</div>"
        ) % _("Thông báo hệ thống: Đã đánh dấu: Blacklist")
        post_kwargs = {
            'body': body,
        }
        if subtype:
            post_kwargs['subtype_id'] = subtype.id
        self.message_post(**post_kwargs)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Blacklist",
                "message": "Đã đưa nhân viên vào danh sách đen.",
                "type": "warning",
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }

    def _action_settle_0213_advance_al(self):
        self._check_0213_group_access(
            _("Settle Advance Annual Leave"),
            self._GROUP_0213_HR_PROCESS,
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        if not self.x_psm_0213_al_has_advance:
            raise UserError(_("This request has no advance annual leave to deduct."))
        if self.x_psm_0213_al_deduction_amount <= 0:
            raise UserError(
                _("Please enter the advance annual leave deduction amount before settling.")
            )
        self.sudo().write({"x_psm_0213_al_settled": True})
        currency = self.x_psm_0213_al_deduction_currency_id
        amount = "%s %s" % (
            self.x_psm_0213_al_deduction_amount or 0.0,
            currency.name if currency else "",
        )
        self.message_post(
            body=_(
                "Advance annual leave deduction settled: %(days).2f day(s) = %(amount)s"
            )
            % {
                "days": self.x_psm_0213_al_advance_days,
                "amount": amount,
            }
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Advance annual leave deduction has been settled."),
                "type": "success",
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }

    def action_settle_advance_al(self):
        return self._action_settle_0213_advance_al()

    @api.model
    def _cron_send_offboarding_reminders(self):
        """
        RST Reminders & Automatic Deadline Extensions:
        1. Tìm các đơn RST trạng thái 'Approved'.
        2. Tìm các công việc (mail.activity) của đơn đó bị trễ hạn hơn 3 ngày.
        3. Phân loại người phụ trách:
           - Nếu là Nhân viên (Owner): Gửi template Employee.
           - Nếu là IT/Admin/HR/Manager: Gửi template Dept.
        4. Tự động cộng thêm 4 ngày vào Due Date cho các công việc này.
        """
        cron_self = self.sudo()
        rst_category = cron_self._get_0213_resignation_category()
        if not rst_category:
            return

        requests = cron_self.search([
            ("category_id", "=", rst_category.id),
            ("request_status", "=", "approved"),
        ])

        # Ngưỡng trễ hạn: Bất cứ công việc nào có hạn nhỏ hơn ngày hôm nay
        today = fields.Date.today()

        activities_by_request = cron_self._get_overdue_activities_by_request(requests, today=today)

        for req in requests:
            emp_template = req._get_0213_employee_reminder_template()
            dept_template = req._get_0213_department_reminder_template()
            pending_activities = activities_by_request.get(
                req.id, self.env["mail.activity"].sudo().browse([])
            )

            if not pending_activities:
                continue

            activities_by_user = self._group_activities_by_user(pending_activities)

            for user_id, user_acts in activities_by_user.items():
                user = user_acts[0].user_id
                email_to = user.partner_id.email or user.email
                if not email_to:
                    _logger.warning(f"OFFBOARDING CRON: Bỏ qua {user.name} vì không có email.")
                    continue

                try:
                    if user == req.request_owner_id:
                        # Nhắc nhở Nhân viên (áp dụng tương tự)
                        if emp_template:
                            emp_template.send_mail(
                                req.id,
                                force_send=True,
                                email_values={'email_to': email_to},
                            )
                    else:
                        # Nhắc nhở Phòng ban (IT, Admin, HR, Manager...)
                        if dept_template:
                            dept_template.send_mail(req.id, force_send=True, email_values={'email_to': email_to})

                    # 5. Logic gia hạn: Cộng thêm 4 ngày cho Due Date của các task này
                    extension_days = req._get_0213_reminder_extension_days()
                    if extension_days > 0:
                        for act in user_acts:
                            old_date = act.date_deadline
                            new_date = old_date + timedelta(days=extension_days)
                            act.write({'date_deadline': new_date})

                except Exception as e:
                    _logger.error(f"OFFBOARDING CRON ERROR: Lỗi xử lý cho {user.name}: {str(e)}")

    def action_manual_reminder_extension(self):
        """Kích hoạt thủ công việc nhắc nhở và gia hạn cho ĐƠN NÀY"""
        self._check_0213_group_access(
            _("Nhắc nhở và gia hạn thủ công"), self._GROUP_0213_REMINDER
        )
        self.ensure_one()
        self._ensure_0213_offboarding_request()
        if self.request_status != 'approved':
            raise UserError(_("Chỉ có thể nhắc nhở các đơn đang ở trạng thái Approved."))

        today = fields.Date.today()
        # Tìm các activity trễ hạn của đơn này
        pending_activities = self.env["mail.activity"].sudo().search([
            ('active', '=', True),
            '|',
            '&', ('res_model', '=', 'approval.request'), ('res_id', '=', self.id),
            '&', ('res_model', '=', 'hr.employee'), ('res_id', '=', self.x_psm_0213_employee_id.id if self.x_psm_0213_employee_id else 0),
        ])
        pending_activities = self._filter_0213_offboarding_activities(pending_activities)
        overdue_days = self._get_0213_reminder_overdue_days()
        pending_activities = pending_activities.filtered(
            lambda act: act.date_deadline
            and act.date_deadline < today
            and (today - act.date_deadline).days > overdue_days
        )

        if not pending_activities:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Thông báo'),
                    'message': _('Không có công việc nào bị trễ hạn để xử lý.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }

        emp_template = self._get_0213_employee_reminder_template()
        dept_template = self._get_0213_department_reminder_template()

        activities_by_user = self._group_activities_by_user(pending_activities)
        extension_days = self._get_0213_reminder_extension_days()
        for user_id, user_acts in activities_by_user.items():
            user = user_acts[0].user_id
            email_to = user.partner_id.email or user.email
            if not email_to: continue

            if user == self.request_owner_id:
                if emp_template: emp_template.send_mail(self.id, force_send=True, email_values={'email_to': email_to})
            else:
                if dept_template: dept_template.send_mail(self.id, force_send=True, email_values={'email_to': email_to})

            if extension_days > 0:
                for act in user_acts:
                    act.write({'date_deadline': act.date_deadline + timedelta(days=extension_days)})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _('Đã gửi nhắc nhở và gia hạn cho %s công việc trễ hạn.') % len(pending_activities),
                'type': 'success',
                'sticky': False,
            }
        }
