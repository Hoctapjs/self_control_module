# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    _TEMPLATE_DOMAIN_0213 = [("model_id.model", "in", ["approval.request", "hr.employee"])]

    x_psm_0213_exit_survey_template_id = fields.Many2one(
        "mail.template",
        string="Exit Survey Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to send the Exit Interview survey link to employees.",
    )
    x_psm_0213_adecco_template_id = fields.Many2one(
        "mail.template",
        string="Adecco Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to send resignation information to Adecco.",
    )
    x_psm_0213_social_insurance_template_id = fields.Many2one(
        "mail.template",
        string="Social Insurance Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to send social insurance information to resigning employees.",
    )
    x_psm_0213_employee_reminder_template_id = fields.Many2one(
        "mail.template",
        string="Employee Reminder Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to remind employees to complete offboarding tasks.",
    )
    x_psm_0213_department_reminder_template_id = fields.Many2one(
        "mail.template",
        string="Department Reminder Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to remind responsible departments to complete offboarding tasks.",
    )
    x_psm_0213_employee_approved_template_id = fields.Many2one(
        "mail.template",
        string="Employee Approved Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to notify employees after their resignation request is approved.",
    )
    x_psm_0213_completion_template_id = fields.Many2one(
        "mail.template",
        string="Completion Thank You Email Template",
        domain=_TEMPLATE_DOMAIN_0213,
        help="Email template used to thank employees when offboarding is completed.",
    )
    x_psm_0213_adecco_notification_email = fields.Char(
        string="Adecco Notification Email",
        help="Recipient email for Adecco resignation notifications in module 0213.",
    )
    x_psm_0213_default_it_user_id = fields.Many2one(
        "res.users",
        string="Default IT Task User",
        domain=[("share", "=", False)],
        help=(
            "Default user assigned to IT offboarding tasks in 0213 when the related "
            "store/department has no specific IT responsible user and the template "
            "has no specific responsible user."
        ),
    )
    x_psm_0213_default_on_demand_user_id = fields.Many2one(
        "res.users",
        string="Default On-Demand Task User",
        domain=[("share", "=", False)],
        help="Default user assigned when an offboarding template has responsible_type = on_demand but no configured responsible user.",
    )
    x_psm_0213_social_insurance_contract_type_ids = fields.Many2many(
        "hr.contract.type",
        "res_company_hr_contract_type_0213_rel",
        "company_id",
        "contract_type_id",
        string="Social Insurance Contract Types",
        help="Contract types handled directly by the social insurance flow. Other contract types go through the Adecco notification step.",
    )
    x_psm_0213_al_leave_type_ids = fields.Many2many(
        "hr.leave.type",
        "res_company_hr_leave_type_0213_rel",
        "company_id",
        "leave_type_id",
        string="Leave Types Counted as AL",
        help="Leave types used to compute remaining annual leave. If left empty, all leave types requiring allocation are used.",
    )
