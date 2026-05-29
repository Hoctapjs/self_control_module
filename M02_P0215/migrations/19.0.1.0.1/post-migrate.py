# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


RECORD_COMPANY_DOMAIN = """[
                '|',
                ('x_psm_employee_id.company_id', '=', False),
                ('x_psm_employee_id.company_id', 'in', company_ids)
            ]"""

EXPLANATION_COMPANY_DOMAIN = """[
                '|',
                ('x_psm_record_id.x_psm_employee_id.company_id', '=', False),
                ('x_psm_record_id.x_psm_employee_id.company_id', 'in', company_ids)
            ]"""


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    hr_manager = env.ref("hr.group_hr_manager", raise_if_not_found=False)
    approval_user = env.ref("approvals.group_approval_user", raise_if_not_found=False)
    if hr_manager and approval_user and approval_user in hr_manager.implied_ids:
        hr_manager.write({"implied_ids": [(3, approval_user.id)]})

    for xmlid in (
        "M02_P0215.access_psm_hr_discipline_record_admin",
        "M02_P0215.access_psm_hr_discipline_explanation_admin",
    ):
        access = env.ref(xmlid, raise_if_not_found=False)
        if access:
            access.write({"perm_unlink": False})

    for xmlid in (
        "M02_P0215.rule_psm_hr_discipline_record_hrbp",
        "M02_P0215.rule_psm_hr_discipline_record_oc",
    ):
        rule = env.ref(xmlid, raise_if_not_found=False)
        if rule:
            rule.write({"domain_force": RECORD_COMPANY_DOMAIN})

    rule = env.ref("M02_P0215.rule_psm_hr_discipline_explanation_hrbp", raise_if_not_found=False)
    if rule:
        rule.write({"domain_force": EXPLANATION_COMPANY_DOMAIN})
