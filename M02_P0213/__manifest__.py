# -*- coding: utf-8 -*-
{
    'name': 'M02_P0213 - Quy Trinh OFFBOARDING OPS',
    'version': '19.0.1.0.7',
    'category': 'Human Resources',
    'summary': 'Quy trình nghỉ việc',
    'description': """
        Module cho phép nhân viên gửi yêu cầu nghỉ việc từ Portal.
        - Form đơn giản với họ tên, line manager, lý do nghỉ việc
        - Tích hợp với Approvals để duyệt yêu cầu
    """,
    'author': 'PSM',
    'depends': [
        'base',
        'mail',
        'approvals',
        'hr',
        'portal',
        'survey',
        'hr_holidays',
        'M02_P0200',
        'M00_P9990',
    ],
    'data': [
        'data/survey_exit_interview_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/offboarding_request_rules.xml',
        'data/mail_message_subtype_data.xml',
        'data/approval_category_data.xml',
        'data/email_template_exit_survey.xml',
        'data/email_template_adecco_notification.xml',
        'data/email_template_social_insurance.xml',
        'data/email_template_offboarding_reminder.xml',
        'data/email_template_dept_offboarding_reminder.xml',
        'data/email_template_offboarding_completion.xml',
        'data/email_template_employee_approved_notification.xml',
        'data/ir_cron_data.xml',
        'data/offboarding_activity_plan_data.xml',
        'data/config_ui_cleanup.xml',
        'views/hr_department_views.xml',
        'views/resignation_portal_template.xml',
        'views/resignation_request_views.xml',
        'views/res_company_views.xml',
        'views/config_menu_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'M02_P0213/static/src/scss/portal_resignation_0213.scss',
            'M02_P0213/static/src/js/portal_resignation_0213.js',
        ],
        'web.assets_backend': [
            'M02_P0213/static/src/scss/backend_0213.scss',
            'M02_P0213/static/src/css/notification_style.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
