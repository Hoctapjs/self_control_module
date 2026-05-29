# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    request_status = fields.Selection(
        selection_add=[
            ("done", "Done"),
        ],
        ondelete={"done": "set default"},
    )

    _GROUP_0214_RST_READ = (
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_S",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0214_REMINDER = _GROUP_0214_RST_READ
    _GROUP_0214_SURVEY_RESULTS = _GROUP_0214_RST_READ
    _GROUP_0214_HR_PROCESS = (
        "M02_P0200.GDH_RST_HR_ADMIN_S",
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0214_DONE = (
        "M02_P0200.GDH_RST_HR_ADMIN_M",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )
    _GROUP_0214_SUBORDINATE_REPORT = (
        "M02_P0200.GDH_RST_HR_HRBP_S",
        "M02_P0200.GDH_RST_HR_HRBP_M",
        "M02_P0200.GDH_RST_HR_HEAD_M",
        "M02_P0200.GDH_RST_SYSTEM_ST_M",
    )

    @api.model
    def _get_resignation_category(self):
        return self.env.ref(
            "M02_P0214.approval_category_resignation",
            raise_if_not_found=False,
        )

    def _get_0214_company(self):
        self.ensure_one()
        company = False
        if "company_id" in self._fields and self.company_id:
            company = self.company_id
        elif self.x_psm_0214_employee_id and self.x_psm_0214_employee_id.company_id:
            company = self.x_psm_0214_employee_id.company_id
        elif self.request_owner_id and self.request_owner_id.company_id:
            company = self.request_owner_id.company_id
        return company or self.env.company

    def _get_0214_reminder_overdue_days(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0214_reminder_overdue_days', '0')
        return int(param_val or 0)

    def _get_0214_reminder_extension_days(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0214_reminder_extension_days', '4')
        return int(param_val or 4)

    def _get_0214_exit_survey_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_exit_survey_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_exit_survey",
            raise_if_not_found=False,
        )

    def _get_0214_adecco_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_adecco_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_adecco_notification",
            raise_if_not_found=False,
        )

    def _get_0214_social_insurance_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_social_insurance_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_social_insurance",
            raise_if_not_found=False,
        )

    def _get_0214_offboarding_completion_template(self):
        self.ensure_one()
        company_template = (
            self._get_0214_company().x_psm_0214_offboarding_completion_template_id
        )
        return company_template or self.env.ref(
            "M02_P0214.email_template_offboarding_completion",
            raise_if_not_found=False,
        )

    def _get_0214_employee_reminder_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_employee_reminder_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_offboarding_reminder",
            raise_if_not_found=False,
        )

    def _get_0214_department_reminder_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_department_reminder_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_dept_offboarding_reminder",
            raise_if_not_found=False,
        )

    def _get_0214_manager_approval_reminder_template(self):
        self.ensure_one()
        company_template = (
            self._get_0214_company().x_psm_0214_manager_approval_reminder_template_id
        )
        return company_template or self.env.ref(
            "M02_P0214.email_template_manager_approval_reminder",
            raise_if_not_found=False,
        )

    def _get_0214_employee_approved_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_employee_approved_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_employee_approved_notification",
            raise_if_not_found=False,
        )

    def _get_0214_dept_assignment_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_dept_assignment_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_dept_offboarding_assignment",
            raise_if_not_found=False,
        )

    def _get_0214_dept_confirm_done_template(self):
        self.ensure_one()
        return self.env.ref(
            "M02_P0214.email_template_dept_confirm_done",
            raise_if_not_found=False,
        )

    def _get_0214_salary_settlement_template(self):
        self.ensure_one()
        company_template = self._get_0214_company().x_psm_0214_salary_settlement_template_id
        return company_template or self.env.ref(
            "M02_P0214.email_template_salary_settlement",
            raise_if_not_found=False,
        )

    def _get_0214_reminder_interval_days(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0214_reminder_interval_days', '3')
        return int(param_val or 3)

    def _get_0214_reminder_max_count(self):
        self.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0214_reminder_max_count', '2')
        return int(param_val or 2)

    def _get_0214_request_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return "%s/web#id=%s&model=approval.request&view_type=form" % (
            (base_url or "").rstrip("/"),
            self.id,
        )

    def _get_0214_portal_offboarding_url(self):
        return self._get_0214_portal_activities_url()

    def _get_0214_portal_activities_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return "%s/my/activities" % (base_url or "").rstrip("/")

    def _get_0214_portal_resignation_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return "%s/my/resignation/rst" % (base_url or "").rstrip("/")

    def _get_0214_al_leave_types(self):
        company = self[:1]._get_0214_company() if self else self.env.company
        leave_types = company.x_psm_0214_al_leave_type_ids
        if not leave_types:
            leave_types = self.env["hr.leave.type"].sudo().search(
                [("requires_allocation", "=", True)]
            )
        return leave_types

    def _get_0214_remaining_al(self, employee):
        if not employee:
            return 0.0

        leave_types = self._get_0214_al_leave_types()
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

    def _get_0214_employee_email_list(self):
        self.ensure_one()
        emails = []
        employee = self.x_psm_0214_employee_id
        if employee and employee.work_email:
            emails.append(employee.work_email)
        if self.x_psm_0214_employee_personal_email:
            emails.append(self.x_psm_0214_employee_personal_email)
        return list(dict.fromkeys(email for email in emails if email))

    def _get_0214_default_role_user(self, role):
        self.ensure_one()
        company = self._get_0214_company()
        if role == "it":
            return company.x_psm_0214_default_it_user_id
        if role == "admin":
            return company.x_psm_0214_default_admin_user_id
        if role == "hr":
            return company.x_psm_0214_default_hr_user_id
        return self.env["res.users"]

    def _check_0214_group_access(self, action_label, allowed_groups):
        if self.env.su or self.env.context.get("bypass_0214_group_check"):
            return

        if not self:
            if any(self.env.user.has_group(group_xmlid) for group_xmlid in allowed_groups):
                return
            raise AccessError(
                _("You do not have permission to perform: %s.")
                % action_label
            )

        rst_requests = self.filtered(lambda request: request._is_0214_offboarding_request())
        if not rst_requests:
            return

        if any(self.env.user.has_group(group_xmlid) for group_xmlid in allowed_groups):
            return

        raise AccessError(
            _("You do not have permission to perform: %s.") % action_label
        )

    @api.model
    def _get_exit_survey(self):
        survey = self.env.ref(
            "M02_P0214.survey_exit_interview",
            raise_if_not_found=False,
        )
        return survey.sudo() if survey else self.env["survey.survey"]

    def _is_0214_offboarding_request(self):
        self.ensure_one()
        rst_category = self._get_resignation_category()
        return bool(rst_category and self.category_id == rst_category)

    @api.model
    def _find_rst_employee(self, partner=None, user=None, email=None):
        employee_model = self.env["hr.employee"].sudo()
        employee = employee_model.browse()

        if partner:
            employee = employee_model.search(
                [("work_contact_id", "=", partner.id)],
                limit=1,
            )
            if employee:
                return employee

            if not user:
                user = self.env["res.users"].sudo().search(
                    [("partner_id", "=", partner.id)],
                    limit=1,
                )

        if user:
            employee = employee_model.search([("user_id", "=", user.id)], limit=1)
            if employee:
                return employee

        if email:
            employee = employee_model.search([("work_email", "=", email)], limit=1)

        return employee

    @api.model
    def _get_or_create_rst_survey_user_input(
        self,
        partner,
        resignation_request=None,
        create_if_missing=False,
    ):
        survey = self._get_exit_survey()
        if not survey or not partner:
            return self.env["survey.user_input"].sudo().browse()

        user_input = self.env["survey.user_input"].sudo().browse()
        if resignation_request and resignation_request.x_psm_0214_exit_survey_user_input_id:
            stored_user_input = resignation_request.x_psm_0214_exit_survey_user_input_id.sudo()
            if self._is_matching_0214_survey_user_input(
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
                lambda candidate: self._is_matching_0214_survey_user_input(
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
            and not resignation_request.x_psm_0214_exit_survey_user_input_id
        ):
            resignation_request.sudo().write(
                {"x_psm_0214_exit_survey_user_input_id": user_input.id}
            )

        return user_input

    @api.model
    def _is_matching_0214_survey_user_input(
        self,
        user_input,
        partner=None,
        resignation_request=None,
        done_only=False,
    ):
        if not user_input:
            return False

        survey = self._get_exit_survey()
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

        if resignation_request and not resignation_request._is_0214_offboarding_request():
            return False

        return True

    def _get_0214_exit_survey_user_inputs(self, done_only=False):
        self.ensure_one()
        survey = self._get_exit_survey()
        if not survey or not self._is_0214_offboarding_request() or not self.request_owner_id:
            return self.env["survey.user_input"].sudo().browse()

        partner = self.request_owner_id.partner_id
        user_inputs = self.env["survey.user_input"].sudo().browse()
        if self.x_psm_0214_exit_survey_user_input_id:
            stored_user_input = self.x_psm_0214_exit_survey_user_input_id.sudo()
            if self._is_matching_0214_survey_user_input(
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
            lambda candidate: self._is_matching_0214_survey_user_input(
                candidate,
                partner=partner,
                resignation_request=self,
                done_only=done_only,
            )
        )
        return user_inputs

    @api.model
    def _build_rst_notification_action(
        self,
        title,
        message,
        message_type="info",
        sticky=False,
    ):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": message_type,
                "sticky": sticky,
            },
        }

    @api.model
    def _build_rst_activity_domain(
        self,
        request=None,
        request_id=None,
        employee_id=None,
        active_only=None,
        deadline_before=None,
    ):
        if request:
            request_id = request.id
            employee_id = (
                request.x_psm_0214_employee_id.id
                if request.x_psm_0214_employee_id
                else False
            )

        domain = []
        if active_only is not None:
            domain.append(("active", "=", active_only))
        if deadline_before is not None:
            domain.append(("date_deadline", "<", deadline_before))

        domain.extend(
            [
                "|",
                "&",
                ("res_model", "=", "approval.request"),
                ("res_id", "=", request_id or 0),
                "&",
                ("res_model", "=", "hr.employee"),
                ("res_id", "=", employee_id or 0),
            ]
        )
        return domain

    @api.model
    def _build_rst_activity_domain_for_requests(
        self,
        requests,
        active_only=None,
        deadline_before=None,
    ):
        requests = requests.filtered(lambda req: req.x_psm_0214_employee_id)
        request_ids = requests.ids or [0]
        employee_ids = requests.mapped("x_psm_0214_employee_id").ids or [0]

        domain = []
        if active_only is not None:
            domain.append(("active", "=", active_only))
        if deadline_before is not None:
            domain.append(("date_deadline", "<", deadline_before))

        domain.extend(
            [
                "|",
                "&",
                ("res_model", "=", "approval.request"),
                ("res_id", "in", request_ids),
                "&",
                ("res_model", "=", "hr.employee"),
                ("res_id", "in", employee_ids),
            ]
        )
        return domain

    @api.model
    def _get_overdue_activities_by_request(self, requests, today=None):
        activities_by_request = {}
        if not requests:
            return activities_by_request

        today = today or fields.Date.today()
        requests = requests.filtered(lambda req: req.x_psm_0214_employee_id)
        if not requests:
            return activities_by_request

        all_activities = self.env["mail.activity"].sudo().search(
            self._build_rst_activity_domain_for_requests(
                requests,
                active_only=True,
                deadline_before=today,
            )
        )

        requests_by_id = {req.id: req for req in requests}
        requests_by_employee_id = {
            req.x_psm_0214_employee_id.id: req
            for req in requests
            if req.x_psm_0214_employee_id
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

        activity_model = self.env["mail.activity"].sudo()
        for req in requests:
            overdue_days = req._get_0214_reminder_overdue_days()
            activities = activity_model.browse(grouped_ids.get(req.id, []))
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

        activity_model = self.env["mail.activity"].sudo()
        return {
            user_id: activity_model.browse(activity_ids)
            for user_id, activity_ids in grouped_ids.items()
        }

    employee_id = fields.Many2one(
        "hr.employee",
        string="Resigning Employee (Request Owner)",
        compute="_compute_rst_employee_id",
        store=True,
        readonly=False,
    )
    x_psm_0214_employee_id = fields.Many2one(
        "hr.employee",
        related="employee_id",
        string="Resigning Employee",
        store=True,
        readonly=False,
    )
    resignation_employee_name = fields.Char(
        related="employee_id.name",
        string="Employee Name",
        readonly=True,
    )
    x_psm_0214_resignation_employee_name = fields.Char(
        related="resignation_employee_name",
        string="Employee Name",
        readonly=True,
    )
    resignation_manager_name = fields.Char(
        related="employee_id.parent_id.name",
        string="Line Manager",
        readonly=True,
    )
    x_psm_0214_resignation_manager_name = fields.Char(
        related="resignation_manager_name",
        string="Line Manager",
        readonly=True,
    )
    resignation_department = fields.Char(
        related="employee_id.department_id.name",
        string="Department",
        readonly=True,
    )
    x_psm_0214_resignation_department = fields.Char(
        related="resignation_department",
        string="Department",
        readonly=True,
    )
    job_id = fields.Many2one(
        related="employee_id.job_id",
        string="Job Position",
        readonly=True,
    )
    x_psm_0214_job_id = fields.Many2one(
        related="job_id",
        string="Job Position",
        readonly=True,
        store=True,
    )
    type_contract = fields.Char(
        related="x_psm_0213_type_contract",
        string="Contract Type",
        readonly=True,
    )
    x_psm_0214_type_contract = fields.Char(
        related="type_contract",
        string="Contract Type",
        readonly=True,
        store=True,
    )
    resignation_owner_email = fields.Char(
        related="request_owner_id.email",
        string="Requester Email",
        readonly=True,
    )
    x_psm_0214_resignation_owner_email = fields.Char(
        related="resignation_owner_email",
        string="Requester Email",
        readonly=True,
        store=True,
    )
    x_psm_0214_employee_personal_email = fields.Char(
        string="Employee Personal Email",
        help="Personal email of the resigning employee, used for post-departure communications.",
    )
    x_psm_0200_remaining_al_days = fields.Float(
        string="Remaining Annual Leave Days",
        compute="_compute_psm_0200_remaining_al_days",
        readonly=True,
        help=(
            "Số phép năm hiện tại của nhân viên (đọc từ hr.employee). "
            "Lưu ý: KHÔNG phải snapshot lịch sử của đơn — giá trị thay đổi "
            "theo trạng thái phép hiện tại của nhân viên."
        ),
    )
    x_psm_0214_al_advance_days = fields.Float(
        string="Advance Annual Leave Days",
        compute="_compute_0214_al_advance",
        store=True,
        help="So ngay phep nam da ung truoc (phan am cua so du phep). Se bi quy doi va tru vao luong quyet toan.",
    )
    x_psm_0214_al_has_advance = fields.Boolean(
        string="Has Advance Annual Leave",
        compute="_compute_0214_al_advance",
        store=True,
    )
    x_psm_0214_al_deduction_currency_id = fields.Many2one(
        "res.currency",
        string="AL Deduction Currency",
        compute="_compute_0214_al_deduction_currency",
        store=True,
    )
    x_psm_0214_al_deduction_rate = fields.Monetary(
        string="AL Deduction Rate (per day)",
        currency_field="x_psm_0214_al_deduction_currency_id",
        copy=False,
        help="Don gia moi ngay phep am. Finance/HR nhap tay.",
    )
    x_psm_0214_al_deduction_amount = fields.Monetary(
        string="AL Deduction Amount",
        currency_field="x_psm_0214_al_deduction_currency_id",
        copy=False,
        help="Tong tien tru luong cho phep ung truoc. Goi y = so ngay am x don gia; cho phep sua tay.",
    )
    x_psm_0214_al_deduction_note = fields.Text(
        string="AL Deduction Note",
        copy=False,
    )
    x_psm_0214_al_settled = fields.Boolean(
        string="Advance AL Settled",
        default=False,
        copy=False,
        readonly=True,
        help="Danh dau phan phep ung truoc da duoc Finance chot quy doi.",
    )
    x_psm_0214_manager_approval_reminder_count = fields.Integer(
        string="Manager Approval Reminders Sent",
        default=0,
        copy=False,
        readonly=True,
    )
    x_psm_0214_manager_approval_reminder_sent_at = fields.Datetime(
        string="Last Manager Reminder Email Sent At",
        copy=False,
        readonly=True,
    )
    x_psm_0214_signed_resignation_file = fields.Binary(
        string="Signed Resignation Letter (PDF)",
        attachment=True,
        copy=False,
    )
    x_psm_0214_signed_resignation_filename = fields.Char(
        string="Signed Resignation Filename",
        copy=False,
    )
    x_psm_0214_signed_resignation_hash = fields.Char(
        string="Checksum (SHA-256)",
        readonly=True,
        copy=False,
    )
    x_psm_0214_signed_locked = fields.Boolean(
        string="Signed Letter Locked",
        readonly=True,
        default=False,
        copy=False,
    )
    x_psm_0214_can_view_signed_resignation = fields.Boolean(
        string="Can View Signed Letter",
        compute="_compute_0214_can_view_signed_resignation",
        compute_sudo=False,
    )
    x_psm_0214_salary_settlement_file = fields.Binary(
        string="Salary Settlement File (PDF)",
        attachment=True,
        copy=False,
    )
    x_psm_0214_salary_settlement_filename = fields.Char(
        string="Salary Settlement Filename",
        copy=False,
    )
    x_psm_0214_signed_settlement_file = fields.Binary(
        string="Signed Settlement Copy",
        attachment=True,
        copy=False,
    )
    x_psm_0214_signed_settlement_filename = fields.Char(
        string="Signed Settlement Filename",
        copy=False,
    )
    x_psm_0214_settlement_sent = fields.Boolean(
        string="Salary Settlement Sent",
        default=False,
        copy=False,
        readonly=True,
    )
    x_psm_0214_settlement_sent_date = fields.Datetime(
        string="Salary Settlement Sent Date",
        copy=False,
        readonly=True,
    )
    x_psm_0214_settlement_reminder_sent_at = fields.Datetime(
        string="Last Settlement Reminder Sent At",
        copy=False,
        readonly=True,
    )
    x_psm_0214_settlement_signed = fields.Boolean(
        string="Signed Settlement Submitted",
        compute="_compute_0214_settlement_signed",
    )
    x_psm_0214_can_view_salary_settlement = fields.Boolean(
        string="Can View Salary Settlement",
        compute="_compute_0214_can_view_salary_settlement",
        compute_sudo=False,
    )
    x_psm_0214_finance_check_state = fields.Selection(
        [
            ("pending", "Pending"),
            ("blocked", "Blocked"),
            ("passed", "Passed"),
            ("overridden", "Overridden"),
        ],
        string="Accounting Check Status",
        default="pending",
        copy=False,
        readonly=True,
    )
    x_psm_0214_finance_pending_items_summary = fields.Text(
        string="Pending Items Summary",
        copy=False,
        readonly=True,
    )
    x_psm_0214_finance_override_reason = fields.Text(
        string="Accounting Override Reason",
        copy=False,
        readonly=True,
    )
    x_psm_0214_finance_override_user_id = fields.Many2one(
        "res.users",
        string="Accounting Override By",
        copy=False,
        readonly=True,
    )
    x_psm_0214_finance_checked_date = fields.Datetime(
        string="Accounting Check Date",
        copy=False,
        readonly=True,
    )
    exit_survey_completed = fields.Boolean(
        string="Survey Completed",
        compute="_compute_rst_exit_survey_completed",
        store=False,
        compute_sudo=True,
    )
    x_psm_0214_exit_survey_completed = fields.Boolean(
        related="exit_survey_completed",
        string="Survey Completed",
        readonly=True,
    )
    all_activities_completed = fields.Boolean(
        string="All Activities Completed",
        compute="_compute_rst_all_activities_completed",
        store=False,
    )
    x_psm_0214_all_activities_completed = fields.Boolean(
        related="all_activities_completed",
        string="All Activities Completed",
        readonly=True,
    )
    is_plan_launched = fields.Boolean(
        string="Plan Launched",
        default=False,
        copy=False,
    )
    x_psm_0214_is_plan_launched = fields.Boolean(
        related="is_plan_launched",
        string="Plan Launched",
        store=True,
        readonly=False,
    )
    exit_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Exit Survey User Input",
        copy=False,
    )
    x_psm_0214_exit_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        related="exit_survey_user_input_id",
        string="Exit Survey User Input",
        store=True,
        readonly=False,
    )
    resignation_date = fields.Date(string="Expected/Official Resignation Date")
    x_psm_0214_resignation_date = fields.Date(
        related="resignation_date",
        string="Expected/Official Resignation Date",
        store=True,
        readonly=False,
    )
    official_resignation_date = fields.Date(
        string="Official Resignation Date",
        compute="_compute_rst_official_resignation_date",
        store=True,
        readonly=False,
        copy=False,
    )
    x_psm_0214_official_resignation_date = fields.Date(
        related="official_resignation_date",
        string="Official Resignation Date",
        store=True,
        readonly=False,
    )
    resignation_date_formatted = fields.Char(
        string="Expected Resignation Date",
        compute="_compute_resignation_date_formatted",
        store=False,
    )
    x_psm_0214_resignation_date_formatted = fields.Char(
        related="resignation_date_formatted",
        string="Expected Resignation Date",
        readonly=True,
    )
    resignation_type_id = fields.Many2one(
        "x_psm_resignation_type",
        string="Resignation Type (Legacy)",
        readonly=True,
    )
    x_psm_0214_resignation_type_id = fields.Many2one(
        "x_psm_resignation_type",
        related="resignation_type_id",
        string="Resignation Type (Legacy)",
        store=True,
        readonly=False,
    )
    resignation_reason_id = fields.Many2one(
        "hr.departure.reason",
        string="Resignation Type",
    )
    x_psm_0214_resignation_reason_id = fields.Many2one(
        "hr.departure.reason",
        related="resignation_reason_id",
        string="Resignation Type",
        store=True,
        readonly=False,
    )
    resignation_reason = fields.Text(string="Resignation Reason")
    x_psm_0214_resignation_reason = fields.Text(
        related="resignation_reason",
        string="Resignation Reason",
        readonly=False,
    )
    social_insurance_email_sent = fields.Boolean(
        string="Social Insurance Email Sent",
        default=False,
        help="Marks that the Social-Insurance guidance email has been sent automatically.",
    )
    x_psm_0214_social_insurance_email_sent = fields.Boolean(
        related="social_insurance_email_sent",
        string="Social Insurance Email Sent",
        store=True,
        readonly=False,
    )
    owner_related_activity_ids = fields.Many2many(
        "mail.activity",
        compute="_compute_owner_related_activity_ids",
        string="Related Activities (Res Name)",
    )
    x_psm_0214_owner_related_activity_ids = fields.Many2many(
        "mail.activity",
        related="owner_related_activity_ids",
        string="Related Activities (Res Name)",
        readonly=True,
    )
    rst_checklist_activity_ids = fields.Many2many(
        "mail.activity",
        compute="_compute_rst_checklist_activity_ids",
        string="Resignation Checklist (RST)",
        compute_sudo=True,
        context={"active_test": False},
    )
    x_psm_0214_rst_checklist_activity_ids = fields.Many2many(
        "mail.activity",
        related="rst_checklist_activity_ids",
        string="Resignation Checklist (RST)",
        readonly=True,
        context={"active_test": False},
    )

    @api.depends("x_psm_0214_resignation_date")
    def _compute_resignation_date_formatted(self):
        for request in self:
            if request.x_psm_0214_resignation_date:
                request.resignation_date_formatted = (
                    request.x_psm_0214_resignation_date.strftime("%d/%m/%Y")
                )
            else:
                request.resignation_date_formatted = ""

    @api.depends(
        "category_id",
        "employee_id.x_psm_0200_remaining_al_days",
        "x_psm_0213_employee_id.x_psm_0200_remaining_al_days",
        "x_psm_0214_employee_id.x_psm_0200_remaining_al_days",
    )
    def _compute_psm_0200_remaining_al_days(self):
        for request in self:
            employee = request.x_psm_0214_employee_id
            if not request._is_0214_offboarding_request():
                employee = request.x_psm_0213_employee_id or request.employee_id
            request.x_psm_0200_remaining_al_days = (
                employee.x_psm_0200_remaining_al_days if employee else 0.0
            )

    @api.depends("resignation_date")
    def _compute_rst_official_resignation_date(self):
        """Mac dinh = ngay nghi du kien, khong ghi de gia tri HR da sua."""
        for request in self:
            if not request.official_resignation_date:
                request.official_resignation_date = request.resignation_date

    def _check_0214_official_resignation_date(self):
        """Chan duyet neu ngay nghi chinh thuc som hon ngay bat dau hop dong."""
        for request in self:
            if not request._is_0214_offboarding_request():
                continue
            employee = request.x_psm_0214_employee_id
            official_date = request.x_psm_0214_official_resignation_date
            if not employee or not official_date:
                continue
            version = employee.sudo().version_id
            if version.contract_date_start and version.contract_date_start > official_date:
                raise UserError(_(
                    "Official resignation date (%(date)s) cannot be earlier than the contract "
                    "start date of employee %(name)s.",
                    date=official_date,
                    name=employee.name,
                ))

    def _push_0214_contract_end_date(self):
        """Ghi ngay nghi viec chinh thuc vao contract_date_end cua version hien tai."""
        for request in self:
            if not request._is_0214_offboarding_request():
                continue
            employee = request.x_psm_0214_employee_id
            official_date = request.x_psm_0214_official_resignation_date
            request._write_0214_contract_date_end(employee, official_date)

    def _write_0214_contract_date_end(self, employee, official_date):
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

    def _apply_0214_native_departure(self):
        """Ghi nhan nghi viec theo co che native va archive ho so nhan vien."""
        for request in self:
            if not request._is_0214_offboarding_request():
                continue
            employee = request.x_psm_0214_employee_id
            if not employee:
                continue
            official_date = request.x_psm_0214_official_resignation_date
            departure_vals = {}
            if official_date:
                departure_vals["departure_date"] = official_date
            if request.x_psm_0214_resignation_reason_id:
                departure_vals["departure_reason_id"] = (
                    request.x_psm_0214_resignation_reason_id.id
                )
            if departure_vals:
                employee.sudo().write(departure_vals)
            request._write_0214_contract_date_end(employee, official_date)
            if employee.active:
                employee.sudo().with_context(no_wizard=True).action_archive()

    def _check_0214_signed_lock_write(self, vals):
        if self.env.context.get("bypass_0214_signed_lock"):
            return

        protected_fields = {
            "employee_id",
            "x_psm_0214_employee_id",
            "x_psm_0214_employee_personal_email",
            "resignation_date",
            "x_psm_0214_resignation_date",
            "official_resignation_date",
            "x_psm_0214_official_resignation_date",
            "resignation_reason",
            "x_psm_0214_resignation_reason",
            "resignation_reason_id",
            "x_psm_0214_resignation_reason_id",
            "x_psm_0214_signed_resignation_file",
            "x_psm_0214_signed_resignation_filename",
            "x_psm_0214_signed_resignation_hash",
            "x_psm_0214_signed_locked",
        }
        if not protected_fields.intersection(vals):
            return

        locked_requests = self.filtered(
            lambda request: request._is_0214_offboarding_request()
            and request.x_psm_0214_signed_locked
        )
        if locked_requests:
            raise UserError(
                _(
                    "The resignation letter has been signed and locked. To make changes, please cancel and create a new request."
                )
            )

    def write(self, vals):
        self._check_0214_signed_lock_write(vals)
        res = super().write(vals)
        if {
            "official_resignation_date",
            "x_psm_0214_official_resignation_date",
        } & set(vals):
            self.filtered(
                lambda request: request.request_status in ("approved", "done")
            )._push_0214_contract_end_date()
        if {
            "x_psm_0214_salary_settlement_file",
            "x_psm_0214_salary_settlement_filename",
        } & set(vals):
            self.filtered(
                lambda request: request._is_0214_offboarding_request()
                and request.request_status == "approved"
                and not request.x_psm_0214_settlement_sent
            )._check_and_send_salary_settlement()
        return res

    @api.depends("x_psm_0214_employee_id.x_psm_0200_remaining_al_days")
    def _compute_0214_al_advance(self):
        for request in self:
            advance = -(request.x_psm_0214_employee_id.x_psm_0200_remaining_al_days or 0.0)
            request.x_psm_0214_al_advance_days = advance if advance > 0 else 0.0
            request.x_psm_0214_al_has_advance = advance > 0

    @api.depends("company_id")
    def _compute_0214_al_deduction_currency(self):
        for request in self:
            company = request._get_0214_company() if request else self.env.company
            request.x_psm_0214_al_deduction_currency_id = (
                company.currency_id.id if company else self.env.company.currency_id.id
            )

    @api.onchange("x_psm_0214_al_deduction_rate", "x_psm_0214_al_advance_days")
    def _onchange_0214_al_deduction_amount(self):
        for request in self:
            if request.x_psm_0214_al_deduction_rate and request.x_psm_0214_al_advance_days:
                request.x_psm_0214_al_deduction_amount = (
                    request.x_psm_0214_al_advance_days
                    * request.x_psm_0214_al_deduction_rate
                )

    @api.depends("x_psm_0214_signed_settlement_file")
    def _compute_0214_settlement_signed(self):
        for request in self:
            request.x_psm_0214_settlement_signed = bool(
                request.x_psm_0214_signed_settlement_file
            )

    def _compute_0214_can_view_signed_resignation(self):
        current_user = self.env.user
        for request in self:
            employee_user = (
                request.x_psm_0214_employee_id.user_id or request.request_owner_id
            )
            manager_user = request.x_psm_0214_employee_id.parent_id.user_id
            allowed_users = employee_user | manager_user
            request.x_psm_0214_can_view_signed_resignation = bool(
                self.env.su or current_user in allowed_users
            )

    def _compute_0214_can_view_salary_settlement(self):
        current_user = self.env.user
        hr_groups = self._GROUP_0214_HR_PROCESS + self._GROUP_0214_DONE
        has_hr_access = any(current_user.has_group(group_xmlid) for group_xmlid in hr_groups)
        for request in self:
            employee_user = (
                request.x_psm_0214_employee_id.user_id or request.request_owner_id
            )
            manager_user = request.x_psm_0214_employee_id.parent_id.user_id
            allowed_users = employee_user | manager_user
            request.x_psm_0214_can_view_salary_settlement = bool(
                self.env.su or has_hr_access or current_user in allowed_users
            )

    @api.depends("x_psm_0214_employee_id")
    def _compute_owner_related_activity_ids(self):
        activity_sudo = self.env["mail.activity"].sudo().with_context(active_test=False)
        for request in self:
            activities = activity_sudo.browse([])
            if request.x_psm_0214_employee_id:
                activity_ids = activity_sudo.search(
                    self._build_rst_activity_domain(request=request)
                ).ids
                activities = activity_sudo.browse(activity_ids)
            request.owner_related_activity_ids = activities

    @api.depends("x_psm_0214_employee_id")
    def _compute_rst_checklist_activity_ids(self):
        activity_sudo = self.env["mail.activity"].sudo().with_context(active_test=False)
        for request in self:
            if not request.id or isinstance(request.id, str) and not request.id.isdigit():
                request.rst_checklist_activity_ids = activity_sudo.browse([])
                continue
            if not request.x_psm_0214_employee_id:
                request.rst_checklist_activity_ids = activity_sudo.browse([])
                continue

            activities = activity_sudo.search(
                self._build_rst_activity_domain(request=request)
            )
            request.rst_checklist_activity_ids = activities.with_context(active_test=False)

    @api.depends("x_psm_0214_employee_id", "x_psm_0214_is_plan_launched")
    def _compute_rst_all_activities_completed(self):
        for request in self:
            if not request.x_psm_0214_is_plan_launched:
                request.all_activities_completed = False
                continue

            pending_count = self.env["mail.activity"].sudo().search_count(
                self._build_rst_activity_domain(request=request, active_only=True)
            )
            request.all_activities_completed = pending_count == 0

    @api.depends("request_owner_id", "partner_id")
    def _compute_rst_employee_id(self):
        for request in self:
            if request.employee_id or request.x_psm_0214_employee_id:
                continue

            employee = request._find_rst_employee(
                partner=request.partner_id,
                user=request.request_owner_id,
            )
            request.employee_id = employee.id if employee else False

