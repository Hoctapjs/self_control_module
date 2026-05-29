# -*- coding: utf-8 -*-
from odoo import fields, models


class HrDisciplineRejectWizard(models.TransientModel):
    _name = "x_psm.hr.discipline.reject.wizard"
    _description = "Reject Explanation Wizard"

    x_psm_mode = fields.Selection(
        [
            ("explanation", "Reject Explanation"),
            ("skip_hearing", "Skip Hearing"),
            ("ceo_reject", "CEO Reject"),
        ],
        default="explanation",
        required=True,
    )
    x_psm_record_id = fields.Many2one("x_psm.hr.discipline.record", required=True)
    x_psm_reason = fields.Text(string="Reason", required=True)
    x_psm_rejection_reason = fields.Text(string="Rejection Reason")

    def _x_psm_get_reason(self):
        self.ensure_one()
        return self.x_psm_reason or self.x_psm_rejection_reason

    def action_psm_confirm_reject(self):
        """Confirm rejection and send email to employee"""
        self.ensure_one()
        record = self.x_psm_record_id
        reason = self._x_psm_get_reason()

        if record.x_psm_active_explanation_id:
            record.x_psm_active_explanation_id.write(
                {
                    "state": "rejected",
                    "x_psm_rejection_reason": reason,
                    "x_psm_reviewed_date": fields.Datetime.now(),
                    "x_psm_reviewed_by": self.env.uid,
                }
            )

        if record.x_psm_explanation_survey_user_input_id:
            record.x_psm_explanation_survey_user_input_id.sudo().write(
                {"x_psm_0215_record_id": False}
            )

        new_user_input = record._x_psm_get_or_create_explanation_survey_user_input(
            force_new=True
        )

        record.write(
            {
                "state": "draft",
                "x_psm_explanation_rejection_reason": reason,
                "x_psm_explanation_survey_user_input_id": new_user_input.id,
            }
        )

        template = self.env.ref(
            "M02_P0215.email_template_psm_explanation_rejected",
            raise_if_not_found=False,
        )
        if template:
            template.sudo().with_context(rejection_reason=reason).send_mail(record.id, force_send=True)

        if record.x_psm_employee_id.user_id:
            record.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=record.x_psm_employee_id.user_id.id,
                summary="Yeu cau viet lai tuong trinh",
                note=(
                    "Tuong trinh cua ban da bi tu choi. "
                    f"Ly do: {reason}. "
                    f"Vui long lam lai theo link survey moi: {record._x_psm_get_explanation_survey_url()}"
                ),
            )

        record.message_post(
            body=(
                "<strong>Tuong trinh da bi tu choi</strong><br/>"
                f"Ly do: {reason}"
            ),
            subject="Explanation Rejected",
        )

        return {"type": "ir.actions.act_window_close"}

    def action_psm_skip_hearing(self):
        """Confirm skip hearing reason, then move record to proposal."""
        self.ensure_one()
        record = self.x_psm_record_id
        reason = self._x_psm_get_reason()
        record.write({"x_psm_skip_hearing_reason": reason})
        record.message_post(
            body=(
                "<strong>Khong can hop ky luat</strong><br/>"
                f"Ly do: {reason}"
            ),
            subject="Skip Hearing Reason",
        )
        record.action_psm_skip_hearing()
        return {"type": "ir.actions.act_window_close"}

    def action_psm_ceo_reject(self):
        """Confirm CEO rejection reason, then return record to issued."""
        self.ensure_one()
        record = self.x_psm_record_id
        reason = self._x_psm_get_reason()
        if record.x_psm_approval_request_id:
            record.x_psm_approval_request_id.with_context(ceo_reject_reason=reason).action_refuse()
        else:
            record._x_psm_write_state(
                "issued",
                {
                    "x_psm_approval_refuse_reason": reason,
                },
            )
        record.message_post(
            body=(
                "<strong>CEO tu choi phe duyet</strong><br/>"
                f"Ly do: {reason}"
            ),
            subject="CEO Reject Reason",
        )
        return {"type": "ir.actions.act_window_close"}
