# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import UserError


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    def action_send_adecco_notification(self):
        self.ensure_one()
        rst_category = self._get_resignation_category()

        if not rst_category or self.category_id != rst_category:
            return super(ResignationRequest, self).action_send_adecco_notification()

        self._check_0214_group_access(
            _("Send Adecco Notification"), self._GROUP_0214_HR_PROCESS
        )
        if not self.x_psm_0214_employee_id:
            return

        template = self._get_0214_adecco_template()
        email_to = self._get_0214_company().x_psm_0214_adecco_notification_email

        if template and email_to:
            template.sudo().send_mail(
                self.x_psm_0214_employee_id.id,
                force_send=True,
                email_values={"email_to": email_to},
            )
            self.sudo().message_post(
                body=_("Adecco notification sent to the configured email.")
            )
            return self._build_rst_notification_action(
                "Success",
                "Adecco notification sent.",
                message_type="success",
            )

        return self._build_rst_notification_action(
            "Error",
            "Adecco email or Adecco email template is not fully configured.",
            message_type="danger",
        )

    def action_send_social_insurance(self):
        self._check_0214_group_access(
            _("Send Social-Insurance Information"), self._GROUP_0214_HR_PROCESS
        )
        self.ensure_one()
        rst_category = self._get_resignation_category()

        if not rst_category or self.category_id != rst_category:
            return super(ResignationRequest, self).action_send_social_insurance()

        if self.x_psm_0214_social_insurance_email_sent:
            return self._build_rst_notification_action(
                "Notice",
                "Social-Insurance email has already been sent.",
                message_type="warning",
            )

        if not self.x_psm_0214_exit_survey_completed:
            raise UserError(
                _("Please complete the Exit Survey before sending Social-Insurance information.")
            )
        if not self.x_psm_0214_all_activities_completed:
            raise UserError(
                _(
                    "Please complete all offboarding activities before sending Social-Insurance information."
                )
            )
        if not self.x_psm_0214_employee_id:
            return

        template = self._get_0214_social_insurance_template()

        if template:
            employee = self.x_psm_0214_employee_id.sudo()
            email_to = (
                employee.work_email
                or employee.user_id.email
                or employee.private_email
                or self.request_owner_id.partner_id.email
                or self.request_owner_id.email
            )
            if not email_to:
                return self._build_rst_notification_action(
                    "Error",
                    "No email found to send Social-Insurance information.",
                    message_type="danger",
                )

            template.sudo().send_mail(
                self.id,
                force_send=True,
                email_values={"email_to": email_to},
            )
            self.sudo().write({"x_psm_0214_social_insurance_email_sent": True})
            return self._build_rst_notification_action(
                "Success",
                "Social-Insurance information sent by email.",
                message_type="success",
            )

        return self._build_rst_notification_action(
            "Error",
            "Social-Insurance email template not found.",
            message_type="danger",
        )

    @api.depends("request_owner_id")
    def _compute_rst_exit_survey_completed(self):
        for request in self:
            request.exit_survey_completed = bool(
                request._get_0214_exit_survey_user_inputs(done_only=True)
            )

    def action_view_survey_results(self):
        self._check_0214_group_access(
            _("View Survey Results"), self._GROUP_0214_SURVEY_RESULTS
        )
        self.ensure_one()
        if not self._is_0214_offboarding_request():
            return

        user_inputs = self._get_0214_exit_survey_user_inputs(done_only=True)

        if not user_inputs:
            return self._build_rst_notification_action(
                "Notice",
                "No completed survey results found.",
                message_type="warning",
            )

        action = {
            "name": "Exit Survey Results",
            "type": "ir.actions.act_window",
            "res_model": "survey.user_input",
            "context": {"create": False},
        }
        if len(user_inputs) == 1:
            action.update({"view_mode": "form", "res_id": user_inputs.id})
        else:
            action.update(
                {"view_mode": "list,form", "domain": [("id", "in", user_inputs.ids)]}
            )
        return action

    def action_send_exit_survey(self):
        self.ensure_one()
        survey = self._get_exit_survey()
        if not survey:
            return super().action_send_exit_survey()

        partner = self.request_owner_id.partner_id
        if not partner or not partner.email:
            return self._build_rst_notification_action(
                "Error",
                "Requester's email not found!",
                message_type="danger",
            )

        user_input = self._get_or_create_rst_survey_user_input(
            partner=partner,
            resignation_request=self,
            create_if_missing=True,
        )
        if not user_input:
            return self._build_rst_notification_action(
                "Error",
                "Unable to create or retrieve the exit-survey link.",
                message_type="danger",
            )

        survey_url = user_input.get_start_url()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        full_survey_url = base_url + survey_url

        template = self._get_0214_exit_survey_template()
        if not template:
            return super().action_send_exit_survey()

        template.with_context(survey_url=full_survey_url).send_mail(
            self.id,
            force_send=True,
            email_values={"email_to": partner.email},
        )
        return self._build_rst_notification_action(
            "Success",
            f"Survey email sent to {partner.email}",
            message_type="success",
        )
