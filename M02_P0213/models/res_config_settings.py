# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_psm_0213_exit_survey_template_id = fields.Many2one(
        related="company_id.x_psm_0213_exit_survey_template_id",
        readonly=False,
        string="Exit Survey Email Template",
    )
    x_psm_0213_adecco_template_id = fields.Many2one(
        related="company_id.x_psm_0213_adecco_template_id",
        readonly=False,
        string="Adecco Email Template",
    )
    x_psm_0213_social_insurance_template_id = fields.Many2one(
        related="company_id.x_psm_0213_social_insurance_template_id",
        readonly=False,
        string="Social Insurance Email Template",
    )
    x_psm_0213_employee_reminder_template_id = fields.Many2one(
        related="company_id.x_psm_0213_employee_reminder_template_id",
        readonly=False,
        string="Employee Reminder Email Template",
    )
    x_psm_0213_department_reminder_template_id = fields.Many2one(
        related="company_id.x_psm_0213_department_reminder_template_id",
        readonly=False,
        string="Department Reminder Email Template",
    )
    x_psm_0213_employee_approved_template_id = fields.Many2one(
        related="company_id.x_psm_0213_employee_approved_template_id",
        readonly=False,
        string="Employee Approved Email Template",
    )
    x_psm_0213_completion_template_id = fields.Many2one(
        related="company_id.x_psm_0213_completion_template_id",
        readonly=False,
        string="Completion Thank You Email Template",
    )
    x_psm_0213_adecco_notification_email = fields.Char(
        related="company_id.x_psm_0213_adecco_notification_email",
        readonly=False,
        string="Adecco Notification Email",
    )
    x_psm_0213_default_it_user_id = fields.Many2one(
        related="company_id.x_psm_0213_default_it_user_id",
        readonly=False,
        string="Default IT Task User",
    )
    x_psm_0213_default_on_demand_user_id = fields.Many2one(
        related="company_id.x_psm_0213_default_on_demand_user_id",
        readonly=False,
        string="Default On-Demand Task User",
    )
    x_psm_0213_social_insurance_contract_type_ids = fields.Many2many(
        related="company_id.x_psm_0213_social_insurance_contract_type_ids",
        readonly=False,
        string="Social Insurance Contract Types",
    )
    x_psm_0213_al_leave_type_ids = fields.Many2many(
        related="company_id.x_psm_0213_al_leave_type_ids",
        readonly=False,
        string="Leave Types Counted as AL",
    )
