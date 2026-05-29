# -*- coding: utf-8 -*-
import base64
import hashlib
import logging

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    def _compute_0214_file_hash(self, file_b64):
        if not file_b64:
            return False
        if isinstance(file_b64, str):
            file_b64 = file_b64.encode()
        return hashlib.sha256(base64.b64decode(file_b64)).hexdigest()

    def _get_0214_department_offboarding_activities(self):
        activity_sudo = self.env["mail.activity"].sudo().with_context(active_test=False)
        department_keywords = ("it:", "admin:", "hr:")
        activities_by_request = {}
        for request in self:
            activities = activity_sudo.search(request._build_rst_activity_domain(request=request))
            department_activities = activities.filtered(
                lambda activity: activity.res_model == "approval.request"
                and activity.summary
                and activity.summary.strip().lower().startswith(department_keywords)
            )
            activities_by_request[request.id] = department_activities
        return activities_by_request

    def _are_0214_department_activities_completed(self):
        self.ensure_one()
        activities = self._get_0214_department_offboarding_activities().get(
            self.id,
            self.env["mail.activity"].sudo().browse(),
        )
        return len(activities) >= 3 and not any(activity.active for activity in activities)

    def _send_settlement_with_attachment(self, request):
        template = request._get_0214_salary_settlement_template()
        emails = request._get_0214_employee_email_list()
        if not template or not emails:
            _logger.warning(
                "[RST] Skip salary settlement email for request %s because template/email is missing.",
                request.id,
            )
            return False

        attachment = self.env["ir.attachment"].sudo().create(
            {
                "name": request.x_psm_0214_salary_settlement_filename
                or "quyet_toan_luong.pdf",
                "datas": request.x_psm_0214_salary_settlement_file,
                "res_model": "approval.request",
                "res_id": request.id,
                "mimetype": "application/pdf",
            }
        )
        template.with_context(
            portal_url=request._get_0214_portal_resignation_url(),
            is_reminder=False,
        ).sudo().send_mail(
            request.id,
            force_send=True,
            email_values={
                "email_to": ",".join(emails),
                "attachment_ids": [(6, 0, [attachment.id])],
            },
        )
        return True

    def _check_and_send_salary_settlement(self):
        for request in self:
            if (
                not request._is_0214_offboarding_request()
                or request.x_psm_0214_settlement_sent
                or not request.x_psm_0214_salary_settlement_file
                or not request._are_0214_department_activities_completed()
            ):
                continue

            if request._send_settlement_with_attachment(request):
                request.sudo().write(
                    {
                        "x_psm_0214_settlement_sent": True,
                        "x_psm_0214_settlement_sent_date": fields.Datetime.now(),
                    }
                )

    def _find_configured_offboarding_responsible(self, request, template):
        employee_user = (
            request.x_psm_0214_employee_id.user_id or request.request_owner_id
        )
        manager_user = request.x_psm_0214_employee_id.parent_id.user_id

        if template.responsible_type == "employee":
            return employee_user or self.env.user
        if template.responsible_type == "manager":
            return manager_user or self.env.user

        summary = (template.summary or "").lower()
        if "it" in (template.summary or "") or "thiet bi" in summary:
            return request._get_0214_default_role_user("it")
        if "admin" in (template.summary or "") or "quan tri" in summary:
            return request._get_0214_default_role_user("admin")
        if "hr" in (template.summary or "") or "nhan su" in summary:
            return request._get_0214_default_role_user("hr")
        if template.responsible_type == "other" and template.responsible_id:
            return template.responsible_id
        return self.env["res.users"]

    def _find_offboarding_responsible(self, request, template):
        responsible = self._find_configured_offboarding_responsible(request, template)
        if responsible:
            return responsible
        return self.env.user

    def _get_0214_activity_deadline(self, request):
        request.ensure_one()
        param_val = self.env['x_psm_parameter'].get_param('x_psm_0214_activity_deadline_days', '7')
        deadline_days = int(param_val or 7)
        return fields.Date.today() + relativedelta(days=deadline_days)

    def _get_0214_email_cc_for_department_activity(self, request):
        emails = request._get_0214_employee_email_list()
        manager = request.x_psm_0214_employee_id.parent_id.user_id
        manager_email = manager.partner_id.email or manager.email
        if manager_email:
            emails.append(manager_email)
        return ",".join(dict.fromkeys(email for email in emails if email))

    def _notify_dept_assignment(self, activity, request, responsible, is_reminder=False):
        template = request._get_0214_dept_assignment_template()
        email_to = responsible.partner_id.email or responsible.email
        if not template or not email_to:
            _logger.warning(
                "[RST] Skip department assignment email for activity %s because template/email is missing.",
                activity.id,
            )
            return False

        template.with_context(
            portal_url=request._get_0214_portal_activities_url(),
            activity_summary=activity.summary,
            activity_deadline=activity.date_deadline,
            is_reminder=is_reminder,
            reminder_count=activity.x_psm_0214_reminder_count + 1,
        ).sudo().send_mail(
            request.id,
            force_send=True,
            email_values={
                "email_to": email_to,
                "email_cc": self._get_0214_email_cc_for_department_activity(request),
            },
        )
        return True

    def _notify_missing_pic(self, request, template):
        hr_manager = request._get_0214_default_role_user("hr")
        email_to = hr_manager.partner_id.email or hr_manager.email
        mail_template = request._get_0214_dept_assignment_template()
        if not mail_template or not email_to:
            _logger.warning(
                "[RST] Missing PIC for template %s, but HR manager/template email is not configured.",
                template.id,
            )
            request.message_post(
                body=_("Warning: No PIC configured for activity %s.")
                % (template.summary or template.display_name)
            )
            return False

        mail_template.with_context(
            missing_pic=True,
            missing_role=template.summary or template.display_name,
            portal_url=request._get_0214_request_url(),
            activity_summary=template.summary,
        ).sudo().send_mail(
            request.id,
            force_send=True,
            email_values={"email_to": email_to},
        )
        return True

    def _get_template_deadline(self, template):
        date_today = fields.Date.today()
        if template.delay_count <= 0:
            return date_today

        delta = (
            relativedelta(days=template.delay_count)
            if template.delay_unit == "days"
            else relativedelta(weeks=template.delay_count)
            if template.delay_unit == "weeks"
            else relativedelta(months=template.delay_count)
        )
        return date_today + delta

    def _schedule_offboarding_activity(self, request, plan):
        created_activities = []
        for template in plan.template_ids:
            responsible = self._find_configured_offboarding_responsible(request, template)
            if not responsible:
                self._notify_missing_pic(request, template)
                continue

            date_deadline = self._get_0214_activity_deadline(request)

            try:
                activity = self.env["mail.activity"].sudo().create(
                    {
                        "res_model_id": self.env["ir.model"]._get_id("approval.request"),
                        "res_id": request.id,
                        "activity_type_id": template.activity_type_id.id,
                        "summary": template.summary,
                        "note": template.note,
                        "user_id": responsible.id,
                        "date_deadline": date_deadline,
                        "automated": True,
                        "active": True,
                    }
                )
                created_activities.append(activity)
                self._notify_dept_assignment(activity, request, responsible)
            except Exception as exc:
                _logger.error(
                    "[RST] Error creating offboarding activity from template %s: %s",
                    template.id,
                    str(exc),
                    exc_info=True,
                )

        if created_activities:
            self.env.cr.commit()

    def action_checklist_completed(self):
        for request in self:
            message = _("The entire offboarding checklist has been completed.")

            survey_completed = bool(
                request._get_0214_exit_survey_user_inputs(done_only=True)
            )

            pending_count = self.env["mail.activity"].search_count(
                self._build_rst_activity_domain(request=request, active_only=True)
            )
            activities_completed = pending_count == 0

            if survey_completed and activities_completed:
                if request.x_psm_0214_social_insurance_email_sent:
                    message += _(" Social-Insurance email has been sent.")
                else:
                    message += _(" HR can send the Social-Insurance instructions from the button on the form.")
                request.message_post(body=message)
            else:
                missing = []
                if not survey_completed:
                    missing.append("Exit Interview")
                if not activities_completed:
                    missing.append("Offboarding Activities")
                message += _(" (Waiting on: %s)") % ", ".join(missing)
                request.message_post(body=message)

    def action_view_my_activities(self):
        self._check_0214_group_access(
            _("View My Activities"), self._GROUP_0214_RST_READ
        )
        return {
            "type": "ir.actions.act_window",
            "name": "My Activities",
            "res_model": "mail.activity",
            "view_mode": "list,kanban,calendar",
            "search_view_id": self.env.ref("mail.mail_activity_view_search").id,
            "context": {"search_default_filter_user_id_uid": 1},
            "domain": [("user_id", "=", self.env.uid)] + self._build_rst_activity_domain(request=self),
        }

    @api.model
    def action_pending_offboarding_subordinates(self):
        self._check_0214_group_access(
            _("View RST Offboarding Report"),
            self._GROUP_0214_SUBORDINATE_REPORT,
        )
        rst_category = self._get_resignation_category()
        if not rst_category:
            raise UserError(_("RST Resignation category not found."))

        resignation_requests = self.sudo().search(
            [
                ("category_id", "=", rst_category.id),
                ("request_status", "=", "approved"),
            ]
        )
        pending_requests = resignation_requests.filtered(
            lambda r: not r.x_psm_0214_exit_survey_completed
            or not r.x_psm_0214_all_activities_completed
        )

        if not pending_requests:
            return self._build_rst_notification_action(
                _("Notice"),
                _("No RST employees currently pending offboarding."),
            )

        return {
            "type": "ir.actions.act_window",
            "name": _("Offboarding Report - RST"),
            "res_model": "approval.request",
            "view_mode": "list,form",
            "views": [
                (self.env.ref("M02_P0214.view_psm_offboarding_report_tree").id, "list"),
                (False, "form"),
            ],
            "search_view_id": self.env.ref(
                "M02_P0214.view_psm_offboarding_report_search"
            ).id,
            "domain": [("id", "in", pending_requests.ids)],
            "context": {"create": False, "search_default_groupby_reason": 1},
        }
