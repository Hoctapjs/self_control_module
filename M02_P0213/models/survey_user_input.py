from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    x_psm_0213_is_exit_survey = fields.Boolean(
        string="0213 Exit Interview Survey",
        default=False,
        copy=False,
        help="Đánh dấu khảo sát dùng cho quy trình nghỉ việc OPS 0213.",
    )


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _mark_done(self):
        result = super(SurveyUserInput, self)._mark_done()
        self._check_and_mark_exit_interview_done()
        return result

    def write(self, vals):
        res = super(SurveyUserInput, self).write(vals)
        if "state" in vals and vals["state"] == "done":
            self._check_and_mark_exit_interview_done()
        return res

    def _check_and_mark_exit_interview_done(self):
        # Activity Summary to find
        ACTIVITY_SUMMARY = "Hoàn thành Exit Interview"

        exit_survey = self.env.ref(
            "M02_P0213.psm_0213_survey_exit_interview", raise_if_not_found=False
        )

        for user_input in self:
            # Check if this is the exit survey
            if exit_survey and user_input.survey_id == exit_survey:
                # Find employee linked to this participant
                employee = False
                if user_input.partner_id:
                    employee = self.env["hr.employee"].sudo().search(
                        [("work_contact_id", "=", user_input.partner_id.id)], limit=1
                    )
                    if not employee:
                        # Fallback: check if partner is user's partner
                        user = self.env["res.users"].sudo().search(
                            [("partner_id", "=", user_input.partner_id.id)], limit=1
                        )
                        if user:
                            employee = self.env["hr.employee"].sudo().search(
                                [("user_id", "=", user.id)], limit=1
                            )
                elif user_input.email:
                    # Fallback by email
                    employee = self.env["hr.employee"].sudo().search(
                        [("work_email", "=", user_input.email)], limit=1
                    )

                if employee:
                    rst_category = self.env.ref("M02_P0213.psm_0213_approval_category_resignation", raise_if_not_found=False)
                    resignation_request = self.env['approval.request'].sudo().browse()
                    if rst_category:
                        # Tìm resignation request của nhân viên
                        resignation_request = self.env['approval.request'].sudo().search([
                            ('x_psm_0213_employee_id', '=', employee.id),
                            ('category_id', '=', rst_category.id),
                            ('request_status', '=', 'approved'),
                        ], order='create_date desc', limit=1)

                    # Find and mark activity done
                    activity_domain = [
                        ("summary", "=", ACTIVITY_SUMMARY),
                        ("active", "=", True),  # Only active ones
                    ]
                    if resignation_request:
                        activity_domain += [
                            "|",
                            "&", ("res_model", "=", "approval.request"), ("res_id", "=", resignation_request.id),
                            "&", ("res_model", "=", "hr.employee"), ("res_id", "=", employee.id),
                        ]
                    else:
                        activity_domain += [
                            ("res_model", "=", "hr.employee"),
                            ("res_id", "=", employee.id),
                        ]
                    activities = self.env["mail.activity"].sudo().search(activity_domain)
                    # Fix: use action_done() correctly
                    if activities:
                        # action_done returns/handles feedback and archiving
                        activities.action_done()
                    
                    # === AUTO SEND BHXH EMAIL ===
                    if resignation_request:
                        # Kiểm tra cách khác: tự đếm xem còn bao nhiêu activity active
                        pending_activities = self.env['mail.activity'].sudo().search([
                            ('active', '=', True),
                            '|',
                            '&', ('res_model', '=', 'approval.request'), ('res_id', '=', resignation_request.id),
                            '&', ('res_model', '=', 'hr.employee'), ('res_id', '=', employee.id),
                        ])
                        pending_count = len(
                            resignation_request._filter_0213_offboarding_activities(pending_activities)
                        )
                        
                        # Gửi email BHXH nếu:
                        # 1. Exit Interview hoàn thành (cái này đang là True vì survey.state='done')
                        # 2. Tất cả công việc Offboarding hoàn thành (pending_count == 0)
                        if pending_count == 0 and resignation_request.x_psm_0213_is_social_insurance_contract:
                            try:
                                resignation_request.with_context(
                                    bypass_0213_group_check=True
                                ).action_send_social_insurance()
                            except Exception as e:
                                _logger.warning(f"Failed to auto-send BHXH email for resignation request {resignation_request.id}: {str(e)}")
