# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


RECORD_PORTAL_DOMAIN = """[
                '|',
                ('x_psm_employee_id.user_id', '=', user.id),
                '&',
                    ('x_psm_employee_id.user_id', '=', False),
                    ('x_psm_employee_id.work_email', 'in', [user.login, user.email])
            ]"""

EXPLANATION_PORTAL_DOMAIN = """[
                '|',
                ('x_psm_record_id.x_psm_employee_id.user_id', '=', user.id),
                '&',
                    ('x_psm_record_id.x_psm_employee_id.user_id', '=', False),
                    ('x_psm_record_id.x_psm_employee_id.work_email', 'in', [user.login, user.email])
            ]"""


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid, domain in (
        ("M02_P0215.rule_psm_hr_discipline_record_portal_own", RECORD_PORTAL_DOMAIN),
        ("M02_P0215.rule_psm_hr_discipline_explanation_portal_own", EXPLANATION_PORTAL_DOMAIN),
    ):
        rule = env.ref(xmlid, raise_if_not_found=False)
        if rule:
            rule.write({"domain_force": domain})
