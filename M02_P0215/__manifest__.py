# -*- coding: utf-8 -*-
{
    "name": "M02_P0215_EMPLOYEE_DISCIPLINARY_PROCESS",
    "summary": """
        Manage employee disciplinary records, explanations, reviews, and decisions.
    """,
    "description": """
        Employee Disciplinary Process (M02_P0215)
        =========================================
        Supports the employee disciplinary workflow from violation recording to
        explanation, review, disciplinary level determination, decision issuance,
        employee acknowledgement, and effective-period tracking.

        Key Features:
        - Master data for violation categories, violation types, and actions.
        - Store Level and Company Level handling paths.
        - Portal flow for managers and employees.
        - Meeting, decision, compensation, and attachment tracking.
        - Repeat-offense and effective-period tracking.
    """,
    "author": "PSM",
    "category": "Human Resources",
    "version": "19.0.1.0.21",
    "depends": [
        "base",
        "hr",
        "mail",
        "portal",
        "calendar",
        "approvals",
        "survey",
        "portal_custom",
        "M02_P0200",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security_rules.xml",
        "data/approval_category_data.xml",
        "data/survey_explanation_data.xml",
        "data/survey_feedback_data.xml",
        "data/mail_template.xml",
        "data/email_template_rejection.xml",
        "views/x_psm_hr_discipline_master_views.xml",
        "views/x_psm_hr_discipline_record_views.xml",
        "views/x_psm_hr_discipline_reject_wizard_views.xml",
        "views/x_psm_hr_discipline_manual_confirm_wizard_views.xml",
        "views/x_psm_approval_request_views.xml",
        "views/x_psm_hr_discipline_violation_report_wizard_views.xml",
        "views/x_psm_portal_templates.xml",
        "data/hr_discipline_violation_data.xml",
        "data/hr_discipline_action_data.xml",
        "data/cron_auto_archive.xml",
        "data/email_template_discipline_done.xml",
        "reports/x_psm_discipline_reports.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "M02_P0215/static/src/scss/internal_discipline_form.scss",
        ],
        "web.assets_frontend": [
            "M02_P0215/static/src/scss/portal_psm_0215.scss",
            "M02_P0215/static/src/js/portal_psm_0215.js",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "auto_install": False,
}
