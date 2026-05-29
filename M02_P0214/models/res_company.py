# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    x_psm_0214_exit_survey_template_id = fields.Many2one(
        "mail.template",
        string="Exit Survey Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template used to send the Exit Interview survey link to employees in the 0214 flow.",
    )
    x_psm_0214_adecco_template_id = fields.Many2one(
        "mail.template",
        string="Adecco Email Template",
        domain=[("model_id.model", "=", "hr.employee")],
        help="Email template used to send resignation information to Adecco in the 0214 flow.",
    )
    x_psm_0214_social_insurance_template_id = fields.Many2one(
        "mail.template",
        string="Social Insurance Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template used to send social insurance information to employees in the 0214 flow.",
    )
    x_psm_0214_offboarding_completion_template_id = fields.Many2one(
        "mail.template",
        string="Offboarding Completion Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template used to thank employees when the 0214 offboarding process is completed.",
    )
    x_psm_0214_employee_reminder_template_id = fields.Many2one(
        "mail.template",
        string="Employee Reminder Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template used to remind employees to complete offboarding tasks in the 0214 flow.",
    )
    x_psm_0214_department_reminder_template_id = fields.Many2one(
        "mail.template",
        string="Department Reminder Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template used to remind responsible departments to complete offboarding tasks in the 0214 flow.",
    )
    x_psm_0214_manager_approval_reminder_template_id = fields.Many2one(
        "mail.template",
        string="Manager Approval Reminder Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template to remind the manager to approve a resignation in the 0214 flow.",
    )
    x_psm_0214_employee_approved_template_id = fields.Many2one(
        "mail.template",
        string="Employee Approved Notification Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template to notify the employee when their resignation has been approved.",
    )
    x_psm_0214_dept_assignment_template_id = fields.Many2one(
        "mail.template",
        string="Department Assignment Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template to assign offboarding tasks to IT/Admin/HR in the 0214 flow.",
    )
    x_psm_0214_salary_settlement_template_id = fields.Many2one(
        "mail.template",
        string="Salary Settlement Email Template",
        domain=[("model_id.model", "=", "approval.request")],
        help="Email template to send the salary settlement to the resigning employee.",
    )
    x_psm_0214_adecco_notification_email = fields.Char(
        string="Adecco Notification Email",
        help="Recipient email for Adecco resignation notifications in the 0214 flow.",
    )
    x_psm_0214_default_it_user_id = fields.Many2one(
        "res.users",
        string="Default IT User",
        domain=[("share", "=", False)],
        help="Default user assigned to IT tasks when the plan template has no specific responsible user.",
    )
    x_psm_0214_default_admin_user_id = fields.Many2one(
        "res.users",
        string="Default Admin User",
        domain=[("share", "=", False)],
        help="Default user assigned to Admin tasks when the plan template has no specific responsible user.",
    )
    x_psm_0214_default_hr_user_id = fields.Many2one(
        "res.users",
        string="Default HR User",
        domain=[("share", "=", False)],
        help="Default user assigned to HR tasks when the plan template has no specific responsible user.",
    )
    x_psm_0214_default_finance_user_id = fields.Many2one(
        "res.users",
        string="Default Finance User",
        domain=[("share", "=", False)],
        help="Default Finance user for the check/settlement steps in the 0214 flow.",
    )
    x_psm_0214_al_leave_type_ids = fields.Many2many(
        "hr.leave.type",
        string="Leave Types Counted as AL",
        help="Leave types used to compute remaining annual leave. If left empty, all leave types requiring allocation are used.",
    )
