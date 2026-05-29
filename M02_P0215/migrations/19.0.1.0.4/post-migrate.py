# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


SURVEY_VALUES = {
    "survey_psm_feedback": {
        "title": "0215 - Immediate Improvement Feedback",
        "description": "<p>Form for recording an immediate improvement feedback discussion in process 0215.</p>",
        "description_done": "<p>The feedback information has been recorded.</p>",
    },
}

QUESTION_VALUES = {
    "survey_psm_feedback_page_main": {"title": "Feedback Content"},
    "survey_psm_feedback_question_issue": {"title": "Improvement Area"},
    "survey_psm_feedback_question_cause": {"title": "Root Cause"},
    "survey_psm_feedback_question_guidance": {"title": "Guidance Discussed"},
    "survey_psm_feedback_question_employee_commitment": {"title": "Employee Commitment"},
    "survey_psm_feedback_question_follow_up_period": {
        "title": "Follow-up Period",
        "question_placeholder": "Example: 30 days",
    },
    "survey_psm_feedback_question_follow_up_result": {
        "title": "Follow-up Result (if available)",
    },
}

MAIL_TEMPLATE_VALUES = {
    "email_template_psm_explanation_rejected": {
        "subject": "Request to resubmit explanation - {{ object.name }}",
        "body_html": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
                    <h2 style="margin: 0;">Explanation Rejected</h2>
                </div>
                <div style="padding: 20px; background-color: #f8f9fa;">
                    <p>Dear <strong>{{ object.x_psm_employee_name }}</strong>,</p>
                    <p>Your explanation for case <strong>{{ object.name }}</strong> has been rejected.</p>
                    <div style="background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <strong>Rejection reason:</strong><br/>
                        {{ ctx.get('rejection_reason', 'The information is incomplete or inaccurate') }}
                    </div>
                    <p>Please open the new survey form and resubmit a complete explanation.</p>
                    <div style="text-align: center; margin: 25px 0;">
                        <a t-att-href="object._x_psm_get_explanation_survey_url()"
                           style="background-color: #875a7b; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Resubmit Explanation
                        </a>
                    </div>
                    <p>Regards,<br/>HR Department</p>
                </div>
            </div>
        """,
    },
}


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = "M02_P0215"

    for xmlid, values in SURVEY_VALUES.items():
        record = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if record:
            record.write(values)

    for xmlid, values in QUESTION_VALUES.items():
        question = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if question:
            question.write(values)

    for xmlid, values in MAIL_TEMPLATE_VALUES.items():
        template = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if template:
            template.write(values)
