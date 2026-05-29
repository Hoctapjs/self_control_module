# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_psm_0214_exit_survey_template_id = fields.Many2one(
        related="company_id.x_psm_0214_exit_survey_template_id",
        readonly=False,
        string="Exit Survey Email Template",
    )
    x_psm_0214_adecco_template_id = fields.Many2one(
        related="company_id.x_psm_0214_adecco_template_id",
        readonly=False,
        string="Adecco Email Template",
    )
    x_psm_0214_social_insurance_template_id = fields.Many2one(
        related="company_id.x_psm_0214_social_insurance_template_id",
        readonly=False,
        string="Social Insurance Email Template",
    )
    x_psm_0214_offboarding_completion_template_id = fields.Many2one(
        related="company_id.x_psm_0214_offboarding_completion_template_id",
        readonly=False,
        string="Offboarding Completion Email Template",
    )
    x_psm_0214_employee_reminder_template_id = fields.Many2one(
        related="company_id.x_psm_0214_employee_reminder_template_id",
        readonly=False,
        string="Employee Reminder Email Template",
    )
    x_psm_0214_department_reminder_template_id = fields.Many2one(
        related="company_id.x_psm_0214_department_reminder_template_id",
        readonly=False,
        string="Department Reminder Email Template",
    )
    x_psm_0214_manager_approval_reminder_template_id = fields.Many2one(
        related="company_id.x_psm_0214_manager_approval_reminder_template_id",
        readonly=False,
        string="Manager Approval Reminder Email Template",
    )
    x_psm_0214_employee_approved_template_id = fields.Many2one(
        related="company_id.x_psm_0214_employee_approved_template_id",
        readonly=False,
        string="Employee Approved Notification Email Template",
    )
    x_psm_0214_dept_assignment_template_id = fields.Many2one(
        related="company_id.x_psm_0214_dept_assignment_template_id",
        readonly=False,
        string="Department Assignment Email Template",
    )
    x_psm_0214_salary_settlement_template_id = fields.Many2one(
        related="company_id.x_psm_0214_salary_settlement_template_id",
        readonly=False,
        string="Salary Settlement Email Template",
    )
    x_psm_0214_adecco_notification_email = fields.Char(
        related="company_id.x_psm_0214_adecco_notification_email",
        readonly=False,
        string="Adecco Notification Email",
    )
    x_psm_0214_default_it_user_id = fields.Many2one(
        related="company_id.x_psm_0214_default_it_user_id",
        readonly=False,
        string="Default IT User",
    )
    x_psm_0214_default_admin_user_id = fields.Many2one(
        related="company_id.x_psm_0214_default_admin_user_id",
        readonly=False,
        string="Default Admin User",
    )
    x_psm_0214_default_hr_user_id = fields.Many2one(
        related="company_id.x_psm_0214_default_hr_user_id",
        readonly=False,
        string="Default HR User",
    )
    x_psm_0214_default_finance_user_id = fields.Many2one(
        related="company_id.x_psm_0214_default_finance_user_id",
        readonly=False,
        string="Default Finance User",
    )
    x_psm_0214_al_leave_type_ids = fields.Many2many(
        related="company_id.x_psm_0214_al_leave_type_ids",
        readonly=False,
        string="Leave Types Counted as AL",
    )
