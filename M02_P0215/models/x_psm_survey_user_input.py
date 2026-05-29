# -*- coding: utf-8 -*-
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    x_psm_0215_record_id = fields.Many2one(
        "x_psm.hr.discipline.record",
        string="0215 Discipline Record",
        copy=False,
        readonly=True,
        index=True,
    )
    x_psm_0215_flow_type = fields.Selection(
        [
            ("explanation", "Explanation"),
            ("feedback", "Feedback"),
        ],
        string="0215 Flow Type",
        copy=False,
        readonly=True,
    )

    def _mark_done(self):
        result = super()._mark_done()
        for user_input in self.filtered("x_psm_0215_record_id"):
            if user_input.x_psm_0215_flow_type == "feedback":
                user_input.x_psm_0215_record_id._x_psm_on_feedback_survey_done(
                    user_input
                )
            else:
                user_input.x_psm_0215_record_id._x_psm_on_explanation_survey_done(
                    user_input
                )
        return result
