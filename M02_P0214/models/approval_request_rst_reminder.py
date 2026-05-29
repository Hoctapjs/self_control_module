# -*- coding: utf-8 -*-
import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    def _get_rst_reminder_templates(self):
        self.ensure_one()
        return (
            self._get_0214_employee_reminder_template(),
            self._get_0214_department_reminder_template(),
        )

    def _send_rst_reminders_by_user(
        self,
        request,
        activities_by_user,
        employee_template,
        department_template,
    ):
        for activities in activities_by_user.values():
            user = activities[:1].user_id
            email_to = user.partner_id.email or user.email
            if not email_to:
                _logger.warning(
                    "OFFBOARDING REMINDER: Bo qua %s vi khong co email.",
                    user.name,
                )
                continue

            if user == request.request_owner_id:
                if employee_template:
                    employee_template.send_mail(request.id, force_send=True)
            elif department_template:
                department_template.send_mail(
                    request.id,
                    force_send=True,
                    email_values={"email_to": email_to},
                )

            extension_days = request._get_0214_reminder_extension_days()
            for activity in activities:
                activity.write(
                    {
                        "date_deadline": activity.date_deadline
                        + timedelta(days=extension_days)
                    }
                )

    @api.model
    def _cron_send_offboarding_reminders(self):
        rst_category = self._get_resignation_category()
        if not rst_category:
            return

        requests = self.search(
            [
                ("category_id", "=", rst_category.id),
                ("request_status", "=", "approved"),
            ]
        )
        today = fields.Date.today()
        activity_model = self.env["mail.activity"].sudo()
        pending_activities = activity_model.search(
            self._build_rst_activity_domain_for_requests(
                requests,
                active_only=True,
            )
        )

        for activity in pending_activities:
            related_requests = activity_model._get_related_rst_requests(
                activity,
                rst_category,
            ).filtered(lambda req: req.request_status == "approved")
            req = related_requests[:1]
            if not req or not activity_model._is_0214_department_activity(activity, req):
                continue

            interval_days = req._get_0214_reminder_interval_days()
            max_count = req._get_0214_reminder_max_count()
            if not interval_days or not max_count:
                continue
            if activity.x_psm_0214_reminder_count >= max_count:
                continue
            if not activity.create_date:
                continue

            create_date = fields.Date.to_date(activity.create_date)
            days_since = (today - create_date).days
            next_threshold = interval_days * (activity.x_psm_0214_reminder_count + 1)
            if days_since < next_threshold:
                continue

            try:
                req._notify_dept_assignment(
                    activity,
                    req,
                    activity.user_id,
                    is_reminder=True,
                )
                activity.write(
                    {
                        "x_psm_0214_reminder_count": (
                            activity.x_psm_0214_reminder_count + 1
                        )
                    }
                )
            except Exception as exc:
                _logger.error(
                    "OFFBOARDING CRON ERROR: Loi xu ly activity %s cua request %s: %s",
                    activity.id,
                    req.id,
                    str(exc),
                    exc_info=True,
                )

    @api.model
    def _cron_send_manager_approval_reminders(self):
        rst_category = self._get_resignation_category()
        if not rst_category:
            return

        now = fields.Datetime.now()
        requests = self.search(
            [
                ("category_id", "=", rst_category.id),
                ("request_status", "=", "pending"),
            ]
        )
        for req in requests:
            max_count = req._get_0214_reminder_max_count()
            if (
                max_count
                and req.x_psm_0214_manager_approval_reminder_count >= max_count
            ):
                continue

            last_sent = (
                req.x_psm_0214_manager_approval_reminder_sent_at
                or req.date_confirmed
                or req.create_date
            )
            if not last_sent:
                continue

            interval_days = req._get_0214_reminder_interval_days()
            if now - last_sent < timedelta(days=interval_days):
                continue

            try:
                req._send_0214_manager_approval_reminder()
            except Exception as exc:
                _logger.error(
                    "MANAGER APPROVAL REMINDER CRON ERROR: Loi xu ly request %s: %s",
                    req.id,
                    str(exc),
                    exc_info=True,
                )

    @api.model
    def _cron_send_settlement_upload_reminders(self):
        rst_category = self._get_resignation_category()
        if not rst_category:
            return

        now = fields.Datetime.now()
        requests = self.search(
            [
                ("category_id", "=", rst_category.id),
                ("request_status", "in", ["approved", "done"]),
                ("x_psm_0214_settlement_sent", "=", True),
                ("x_psm_0214_settlement_sent_date", "!=", False),
                ("x_psm_0214_settlement_reminder_sent_at", "=", False),
            ]
        )
        for req in requests:
            if req.x_psm_0214_settlement_signed:
                continue
            if now - req.x_psm_0214_settlement_sent_date < timedelta(days=3):
                continue

            template = req._get_0214_salary_settlement_template()
            email_to = ",".join(req._get_0214_employee_email_list())
            if not template or not email_to:
                continue

            try:
                template.with_context(
                    portal_url=req._get_0214_portal_resignation_url(),
                    is_reminder=True,
                ).sudo().send_mail(
                    req.id,
                    force_send=True,
                    email_values={"email_to": email_to},
                )
                req.sudo().write(
                    {"x_psm_0214_settlement_reminder_sent_at": fields.Datetime.now()}
                )
            except Exception as exc:
                _logger.error(
                    "SETTLEMENT UPLOAD REMINDER ERROR: Loi xu ly request %s: %s",
                    req.id,
                    str(exc),
                    exc_info=True,
                )

    def action_manual_reminder_extension(self):
        self._check_0214_group_access(
            _("Send Manual Reminders & Extend Deadlines"), self._GROUP_0214_REMINDER
        )
        self.ensure_one()
        if self.request_status != "approved":
            raise UserError(
                _("Reminders can only be sent for requests in the Approved status.")
            )

        today = fields.Date.today()
        pending_activities = self.env["mail.activity"].sudo().search(
            self._build_rst_activity_domain(
                request=self,
                active_only=True,
                deadline_before=today,
            )
        )
        overdue_days = self._get_0214_reminder_overdue_days()
        pending_activities = pending_activities.filtered(
            lambda act: act.date_deadline
            and (today - act.date_deadline).days > overdue_days
        )

        if not pending_activities:
            return self._build_rst_notification_action(
                _("Notice"),
                _("No overdue activities to process."),
                message_type="warning",
            )

        emp_template, dept_template = self._get_rst_reminder_templates()
        self._send_rst_reminders_by_user(
            self,
            self._group_activities_by_user(pending_activities),
            emp_template,
            dept_template,
        )

        return self._build_rst_notification_action(
            _("Success"),
            _("Sent reminders and extended deadlines for %s overdue activities.")
            % len(pending_activities),
            message_type="success",
        )
