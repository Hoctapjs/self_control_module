# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ExitInterviewReport(models.Model):
    _name = "x_psm_0214_exit_interview_report"
    _description = "Exit Interview Report"
    _auto = False
    _rec_name = "employee_id"

    request_id = fields.Many2one("approval.request", string="Resignation Request", readonly=True)
    employee_id = fields.Many2one("hr.employee", string="Employee", readonly=True)
    department_id = fields.Many2one("hr.department", string="Department", readonly=True)
    job_id = fields.Many2one("hr.job", string="Job Position", readonly=True)
    resignation_reason_id = fields.Many2one(
        "hr.departure.reason",
        string="Resignation Reason",
        readonly=True,
    )
    resignation_date = fields.Date(string="Resignation Date", readonly=True)
    satisfaction_score = fields.Float(
        string="Satisfaction Score (%)",
        readonly=True,
        aggregator="avg",
    )
    is_completed = fields.Boolean(
        string="Completed",
        readonly=True,
        aggregator="bool_or",
    )
    request_count = fields.Integer(
        string="Number of Surveys",
        readonly=True,
        aggregator="sum",
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    sui.id AS id,
                    ar.id AS request_id,
                    ar.x_psm_0214_employee_id AS employee_id,
                    emp_version.department_id AS department_id,
                    emp_version.job_id AS job_id,
                    ar.x_psm_0214_resignation_reason_id AS resignation_reason_id,
                    ar.x_psm_0214_resignation_date AS resignation_date,
                    COALESCE(sui.scoring_percentage, 0.0) AS satisfaction_score,
                    (sui.state = 'done') AS is_completed,
                    1 AS request_count
                FROM survey_user_input sui
                JOIN ir_model_data survey_xmlid
                    ON survey_xmlid.module = 'M02_P0214'
                   AND survey_xmlid.name = 'survey_exit_interview'
                   AND survey_xmlid.model = 'survey.survey'
                   AND survey_xmlid.res_id = sui.survey_id
                JOIN approval_request ar
                    ON ar.x_psm_0214_exit_survey_user_input_id = sui.id
                LEFT JOIN hr_employee emp
                    ON emp.id = ar.x_psm_0214_employee_id
                LEFT JOIN hr_version emp_version
                    ON emp_version.id = emp.current_version_id
            )
            """
        )
