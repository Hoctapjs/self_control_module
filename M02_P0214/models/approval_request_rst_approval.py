# -*- coding: utf-8 -*-
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    def action_confirm(self):
        rst_category = self._get_resignation_category()
        others = self.filtered(
            lambda request: not rst_category or request.category_id != rst_category
        )
        if others:
            super(ResignationRequest, others).action_confirm()

        resignations = self - others
        if resignations:
            resignations.sudo().write({"request_status": "pending"})

            for request in resignations:
                approvers_new = request.approver_ids.filtered(lambda a: a.status == "new")
                if approvers_new:
                    approvers_new._create_activity()
                    approvers_new.sudo().write({"status": "pending"})

                request.sudo().write({"date_confirmed": fields.Datetime.now()})
                request._send_0214_manager_approval_reminder(is_initial=True)

    def action_done(self):
        self._check_0214_group_access(
            _("Complete Resignation"), self._GROUP_0214_DONE
        )
        rst_category = self._get_resignation_category()

        non_rst_requests = self.filtered(
            lambda request: not rst_category or request.category_id != rst_category
        )
        if non_rst_requests:
            super(ResignationRequest, non_rst_requests).action_done()

        rst_requests = self.filtered(
            lambda request: rst_category and request.category_id == rst_category
        )
        if not rst_requests:
            return

        for request in rst_requests:
            if not request.x_psm_0214_exit_survey_completed:
                raise UserError(
                    _("Please complete the Exit Survey before finalising the process.")
                )
            if not request.x_psm_0214_all_activities_completed:
                raise UserError(
                    _("Please complete all offboarding activities before finalising the process.")
                )
            if not request.x_psm_0214_social_insurance_email_sent:
                raise UserError(
                    _("Please send the Social-Insurance instruction email before finalising the process.")
                )
            if request.x_psm_0214_finance_check_state not in ("passed", "overridden"):
                raise UserError(
                    _(
                        "Please push to Accounting before finalising the process, "
                        "or have HR Head override if pending items remain."
                    )
                )

        rst_requests.sudo().write({"request_status": "done"})

        for request in rst_requests:
            request._apply_0214_native_departure()
            request_sudo = request.sudo()
            user_to_deactivate = False

            if (
                request_sudo.x_psm_0214_employee_id
                and request_sudo.x_psm_0214_employee_id.user_id
            ):
                user_to_deactivate = request_sudo.x_psm_0214_employee_id.user_id
            if not user_to_deactivate and request_sudo.request_owner_id:
                user_to_deactivate = request_sudo.request_owner_id

            if user_to_deactivate and user_to_deactivate.active:
                is_portal = user_to_deactivate.has_group("base.group_portal")
                is_internal = user_to_deactivate.has_group("base.group_user")
                is_protected_rst_manager = any(
                    user_to_deactivate.has_group(group_xmlid)
                    for group_xmlid in (
                        "base.group_system",
                        "M02_P0200.GDH_RST_HR_HEAD_M",
                        "M02_P0200.GDH_RST_SYSTEM_ST_M",
                    )
                )
                if (is_portal or is_internal) and not is_protected_rst_manager:
                    _logger.info(
                        "OFFBOARDING AUTO: Deactivating user %s for request %s",
                        user_to_deactivate.login,
                        request.id,
                    )
                    try:
                        user_to_deactivate.write({"active": False})
                        request.message_post(
                            body=(
                                "System: Deactivated Portal/User account: "
                                f"{user_to_deactivate.name}"
                            )
                        )
                    except Exception as exc:
                        _logger.error(
                            "OFFBOARDING AUTO: Failed to deactivate user %s: %s",
                            user_to_deactivate.login,
                            str(exc),
                        )
                else:
                    _logger.warning(
                        "OFFBOARDING AUTO: Skip deactivating safe account %s",
                        user_to_deactivate.login,
                    )

            completion_template = request._get_0214_offboarding_completion_template()
            request_partner = request.request_owner_id.partner_id
            request_email = request_partner.email or request.request_owner_id.email
            if completion_template and request_email:
                try:
                    completion_template.sudo().send_mail(
                        request.id,
                        force_send=True,
                        email_values={"email_to": request_email},
                    )
                except Exception as exc:
                    _logger.error(
                        "OFFBOARDING AUTO: Failed to send completion email for request %s: %s",
                        request.id,
                        str(exc),
                        exc_info=True,
                    )

            domain = [
                ("res_model", "=", "approval.request"),
                ("res_id", "=", request.id),
                ("user_id", "=", request.request_owner_id.id),
                ("activity_type_id", "=", self.env.ref("mail.mail_activity_data_todo").id),
            ]
            activities = self.env["mail.activity"].search(domain)
            activities.action_feedback(feedback="Resignation procedure completed.")

    def action_approve(self, approver=None):
        rst_category = self._get_resignation_category()
        for request in self:
            if (
                rst_category
                and request.category_id == rst_category
                and not request.x_psm_0214_resignation_date
            ):
                raise UserError(
                    _("Please confirm the 'Expected Resignation Date' before approving.")
                )
            if (
                rst_category
                and request.category_id == rst_category
                and not request.x_psm_0214_signed_resignation_file
            ):
                raise UserError(
                    _(
                        "Please attach the signed Resignation Letter (PDF signed by both parties) before approving."
                    )
                )
        if rst_category:
            self.filtered(
                lambda request: request.category_id == rst_category
            )._check_0214_official_resignation_date()

        res = super(ResignationRequest, self).action_approve(approver)

        for request in self:
            if rst_category and request.category_id == rst_category:
                remaining_al = request._get_0214_remaining_al(
                    request.x_psm_0214_employee_id
                )
                if request.x_psm_0214_employee_id:
                    request.x_psm_0214_employee_id.sudo().write(
                        {"x_psm_0200_remaining_al_days": remaining_al}
                    )
                request._send_0214_employee_approved_notification()
                request.action_send_exit_survey()
                request._push_0214_contract_end_date()
                request.sudo().write(
                    {
                        "x_psm_0214_signed_resignation_hash": request._compute_0214_file_hash(
                            request.x_psm_0214_signed_resignation_file
                        ),
                        "x_psm_0214_signed_locked": True,
                    }
                )

        plan = self.env.ref(
            "M02_P0214.offboarding_activity_plan_rst",
            raise_if_not_found=False,
        )
        if plan:
            for request in self:
                if (
                    rst_category
                    and request.category_id == rst_category
                    and request.x_psm_0214_employee_id
                ):
                    self._schedule_offboarding_activity(request, plan)
                    request.sudo().write({"x_psm_0214_is_plan_launched": True})

        return res

    def _get_0214_manager_approver_user(self):
        self.ensure_one()
        employee_manager_user = (
            self.x_psm_0214_employee_id.parent_id.user_id
            if self.x_psm_0214_employee_id and self.x_psm_0214_employee_id.parent_id
            else False
        )
        if employee_manager_user:
            return employee_manager_user

        pending_approver = self.approver_ids.filtered(
            lambda approver: approver.status == "pending" and approver.user_id
        )[:1]
        return pending_approver.user_id if pending_approver else self.env["res.users"]

    def _send_0214_manager_approval_reminder(self, is_initial=False):
        for request in self:
            if not request._is_0214_offboarding_request():
                continue

            manager_user = request._get_0214_manager_approver_user()
            email_to = (
                manager_user.partner_id.email
                or manager_user.email
                if manager_user
                else False
            )
            template = request._get_0214_manager_approval_reminder_template()
            if not template or not email_to:
                _logger.warning(
                    "RST APPROVAL REMINDER: Skip request %s because template or manager email is missing.",
                    request.id,
                )
                continue

            try:
                template.sudo().send_mail(
                    request.id,
                    force_send=True,
                    email_values={"email_to": email_to},
                )
                vals = {"x_psm_0214_manager_approval_reminder_sent_at": fields.Datetime.now()}
                if not is_initial:
                    vals["x_psm_0214_manager_approval_reminder_count"] = (
                        request.x_psm_0214_manager_approval_reminder_count + 1
                    )
                request.sudo().write(vals)
            except Exception as exc:
                _logger.error(
                    "RST APPROVAL REMINDER: Failed to send manager email for request %s: %s",
                    request.id,
                    str(exc),
                    exc_info=True,
                )

    def _send_0214_employee_approved_notification(self):
        for request in self:
            if not request._is_0214_offboarding_request():
                continue

            email_to = ",".join(request._get_0214_employee_email_list())
            template = request._get_0214_employee_approved_template()
            if not template or not email_to:
                _logger.warning(
                    "RST EMPLOYEE APPROVED EMAIL: Skip request %s because template or employee email is missing.",
                    request.id,
                )
                continue

            try:
                template.sudo().send_mail(
                    request.id,
                    force_send=True,
                    email_values={"email_to": email_to},
                )
            except Exception as exc:
                _logger.error(
                    "RST EMPLOYEE APPROVED EMAIL: Failed to send for request %s: %s",
                    request.id,
                    str(exc),
                    exc_info=True,
                )

