from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _get_linked_0214_request(self, user_input):
        return self.env["approval.request"].sudo().search(
            [("x_psm_0214_exit_survey_user_input_id", "=", user_input.id)],
            order="create_date desc",
            limit=1,
        )

    def _find_related_employee(self, user_input):
        linked_request = self._get_linked_0214_request(user_input)
        if linked_request and linked_request.x_psm_0214_employee_id:
            return linked_request.x_psm_0214_employee_id
        return self.env["approval.request"].sudo()._find_rst_employee(
            partner=user_input.partner_id,
            email=user_input.email,
        )

    def write(self, vals):
        res = super().write(vals)
        if vals.get("state") == "done":
            self._check_and_mark_exit_interview_done()
        return res

    def _check_and_mark_exit_interview_done(self):
        activity_summary = "Complete Exit Interview"
        exit_survey = self.env.ref(
            "M02_P0214.survey_exit_interview",
            raise_if_not_found=False,
        )

        for user_input in self:
            if not exit_survey or user_input.survey_id != exit_survey:
                continue

            linked_request = self._get_linked_0214_request(user_input)
            employee = self._find_related_employee(user_input)
            if not employee or not linked_request:
                continue

            activities = self.env["mail.activity"].search(
                [
                    "|",
                    "&",
                    ("res_model", "=", "approval.request"),
                    ("res_id", "=", linked_request.id),
                    "&",
                    ("res_model", "=", "hr.employee"),
                    ("res_id", "=", employee.id),
                    ("summary", "=", activity_summary),
                    ("active", "=", True),
                ]
            )
            if activities:
                activities.action_done()
