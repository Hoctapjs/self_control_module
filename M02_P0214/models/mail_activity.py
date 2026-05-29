# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    active = fields.Boolean(default=True, string="Active")
    rst_display_state = fields.Selection(
        [
            ("pending", "Pending"),
            ("overdue", "Overdue"),
            ("done", "Done"),
        ],
        string="RST Status",
        compute="_compute_rst_display_state",
    )
    x_psm_0214_rst_display_state = fields.Selection(
        [
            ("pending", "Pending"),
            ("overdue", "Overdue"),
            ("done", "Done"),
        ],
        related="rst_display_state",
        string="RST Status",
        readonly=True,
    )
    x_psm_0214_reminder_count = fields.Integer(
        string="Reminder Count",
        default=0,
        copy=False,
    )

    @api.depends("active", "date_deadline", "state")
    def _compute_rst_display_state(self):
        today = fields.Date.today()
        for activity in self:
            if not activity.active:
                activity.rst_display_state = "done"
            elif activity.date_deadline and activity.date_deadline < today:
                activity.rst_display_state = "overdue"
            else:
                activity.rst_display_state = "pending"

    def _get_rst_category(self):
        return self.env.ref(
            "M02_P0214.approval_category_resignation",
            raise_if_not_found=False,
        )

    def _get_related_rst_requests(self, activity, rst_cat):
        approval_request = self.env["approval.request"].sudo()
        if activity.res_model == "approval.request":
            req = approval_request.browse(activity.res_id)
            return req.filtered(lambda r: r.category_id == rst_cat)
        if activity.res_model == "hr.employee":
            return approval_request.search(
                [
                    ("x_psm_0214_employee_id", "=", activity.res_id),
                    ("category_id", "=", rst_cat.id),
                ]
            )
        return approval_request.browse([])

    def _is_rst_offboarding_activity(self, activity, rst_cat):
        return bool(self._get_related_rst_requests(activity, rst_cat))

    def _trigger_rst_recompute(self, activity, rst_cat):
        requests = self._get_related_rst_requests(activity, rst_cat)
        if requests:
            requests.modified(
                ["rst_checklist_activity_ids", "x_psm_0214_rst_checklist_activity_ids"]
            )

    def _is_0214_department_activity(self, activity, request):
        employee_user = (
            request.x_psm_0214_employee_id.user_id or request.request_owner_id
        )
        manager_user = request.x_psm_0214_employee_id.parent_id.user_id
        return bool(
            activity.res_model == "approval.request"
            and activity.user_id
            and activity.user_id not in (employee_user | manager_user)
        )

    def _notify_0214_department_done(self, activity, request):
        template = request._get_0214_dept_confirm_done_template()
        emails = request._get_0214_employee_email_list()
        manager = request.x_psm_0214_employee_id.parent_id.user_id
        manager_email = manager.partner_id.email or manager.email
        if manager_email:
            emails.append(manager_email)
        email_to = ",".join(dict.fromkeys(email for email in emails if email))
        if not template or not email_to:
            return False

        template.with_context(
            activity_summary=activity.summary,
            activity_user=activity.user_id.name,
        ).sudo().send_mail(
            request.id,
            force_send=True,
            email_values={"email_to": email_to},
        )
        return True

    def archive_rst_activities(self):
        rst_cat = self._get_rst_category()
        if not rst_cat:
            return self.env["mail.activity"]

        rst_activities = self.filtered(
            lambda activity: activity.res_model in ["hr.employee", "approval.request"]
            and self._is_rst_offboarding_activity(activity, rst_cat)
        )

        for activity in rst_activities:
            if activity.active:
                activity.sudo().write({"active": False})
                self._trigger_rst_recompute(activity, rst_cat)

        return rst_activities

    def _action_done(self, feedback=False, attachment_ids=False):
        rst_cat = self._get_rst_category()
        rst_activities = self.env["mail.activity"]
        if rst_cat:
            rst_activities = self.filtered(
                lambda activity: activity.res_model in ["hr.employee", "approval.request"]
                and self._is_rst_offboarding_activity(activity, rst_cat)
            )

        res = super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

        if not rst_cat:
            return res

        for activity in rst_activities.sudo():
            if activity.res_model not in ["hr.employee", "approval.request"] or not activity.res_id:
                continue

            requests = self._get_related_rst_requests(activity, rst_cat).filtered(
                lambda req: req.request_status == "approved"
            )
            for req in requests:
                if self._is_0214_department_activity(activity, req):
                    self._notify_0214_department_done(activity, req)
                    req._check_and_send_salary_settlement()

                pending_count = self.env["mail.activity"].sudo().search_count(
                    req._build_rst_activity_domain(request=req, active_only=True)
                )

                if pending_count == 0 and req.x_psm_0214_is_plan_launched:
                    req.sudo().all_activities_completed = True
                    if hasattr(req, "action_checklist_completed"):
                        req.action_checklist_completed()
                    else:
                        req.message_post(
                            body=_(
                                "System: All checklist activities have been completed."
                            )
                        )

                req.sudo().modified(
                    ["rst_checklist_activity_ids", "x_psm_0214_rst_checklist_activity_ids"]
                )

        return res
