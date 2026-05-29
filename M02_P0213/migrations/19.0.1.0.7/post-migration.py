# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    approved_template = env.ref(
        'M02_P0213.psm_0213_email_template_employee_approved_notification',
        raise_if_not_found=False,
    )
    completion_template = env.ref(
        'M02_P0213.psm_0213_email_template_offboarding_completion',
        raise_if_not_found=False,
    )

    values = {}
    if approved_template:
        values['x_psm_0213_employee_approved_template_id'] = approved_template.id
    if completion_template:
        values['x_psm_0213_completion_template_id'] = completion_template.id
    if not values:
        return

    companies = env['res.company'].search([])
    for company in companies:
        company_values = {
            field_name: template_id
            for field_name, template_id in values.items()
            if not company[field_name]
        }
        if company_values:
            company.write(company_values)
