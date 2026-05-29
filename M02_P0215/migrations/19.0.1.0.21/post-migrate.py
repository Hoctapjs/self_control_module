# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


RECORD_PORTAL_DOMAIN = """[
                '|',
                ('x_psm_employee_id.user_id', '=', user.id),
                ('x_psm_employee_id.work_email', 'in', [user.login, user.email])
                ]"""

RECORD_STORE_MANAGER_DOMAIN = """[
                '|', '|', '|',
                ('x_psm_employee_id.user_id', '=', user.id),
                ('x_psm_company_rep_id.user_id', '=', user.id),
                ('x_psm_employee_id.parent_id.user_id', '=', user.id),
                '&',
                ('x_psm_employee_id.department_id', '!=', False),
                ('x_psm_employee_id.department_id', '=', user.employee_id.department_id.id)
                ]"""

RECORD_ALL_DOMAIN = "[(1, '=', 1)]"

RECORD_RGM_DOMAIN = """[
                '|', '|',
                ('x_psm_employee_id.parent_id.user_id', '=', user.id),
                ('x_psm_company_rep_id.user_id', '=', user.id),
                '&',
                ('x_psm_employee_id.department_id', '!=', False),
                ('x_psm_employee_id.department_id', '=', user.employee_id.department_id.id)
                ]"""

EXPLANATION_PORTAL_DOMAIN = """[
                '|',
                ('x_psm_record_id.x_psm_employee_id.user_id', '=', user.id),
                ('x_psm_record_id.x_psm_employee_id.work_email', 'in', [user.login, user.email])
                ]"""

EXPLANATION_STORE_MANAGER_DOMAIN = """[
                '|', '|', '|',
                ('x_psm_record_id.x_psm_employee_id.user_id', '=', user.id),
                ('x_psm_record_id.x_psm_company_rep_id.user_id', '=', user.id),
                ('x_psm_record_id.x_psm_employee_id.parent_id.user_id', '=', user.id),
                '&',
                ('x_psm_record_id.x_psm_employee_id.department_id', '!=', False),
                ('x_psm_record_id.x_psm_employee_id.department_id', '=',
                user.employee_id.department_id.id)
                ]"""

EXPLANATION_ALL_DOMAIN = "[(1, '=', 1)]"

EXPLANATION_RGM_DOMAIN = """[
                '|', '|',
                ('x_psm_record_id.x_psm_employee_id.parent_id.user_id', '=', user.id),
                ('x_psm_record_id.x_psm_company_rep_id.user_id', '=', user.id),
                '&',
                ('x_psm_record_id.x_psm_employee_id.department_id', '!=', False),
                ('x_psm_record_id.x_psm_employee_id.department_id', '=',
                user.employee_id.department_id.id)
                ]"""

SURVEY_VALUES = {
    "survey_psm_feedback": {
        "title": "0215 - Feedback cai thien ngay",
        "description": "<p>Phieu ghi nhan trao doi cai thien ngay trong quy trinh 0215.</p>",
        "description_done": "<p>Thong tin feedback da duoc ghi nhan.</p>",
    },
}

QUESTION_VALUES = {
    "survey_psm_feedback_page_main": {"title": "Noi dung feedback"},
    "survey_psm_feedback_question_issue": {"title": "Van de can cai thien"},
    "survey_psm_feedback_question_cause": {"title": "Nguyen nhan"},
    "survey_psm_feedback_question_guidance": {"title": "Huong dan da trao doi"},
    "survey_psm_feedback_question_employee_commitment": {"title": "Cam ket cua nhan vien"},
    "survey_psm_feedback_question_follow_up_period": {
        "title": "Thoi gian theo doi",
        "question_placeholder": "Vi du: 30 ngay",
    },
    "survey_psm_feedback_question_follow_up_result": {
        "title": "Ket qua sau theo doi (neu da co)",
    },
}


def _ref(env, xmlid):
    return env.ref(xmlid, raise_if_not_found=False)


def _group_ids(env, xmlids):
    groups = [_ref(env, xmlid) for xmlid in xmlids]
    return [group.id for group in groups if group]


def _write_rule(env, xmlid, domain, group_xmlids=None):
    rule = _ref(env, f"M02_P0215.{xmlid}")
    if not rule:
        return
    values = {"domain_force": domain}
    if group_xmlids:
        group_ids = _group_ids(env, group_xmlids)
        if group_ids:
            values["groups"] = [(6, 0, group_ids)]
    rule.write(values)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    hr_manager = _ref(env, "hr.group_hr_manager")
    approval_user = _ref(env, "approvals.group_approval_user")
    if hr_manager and approval_user and approval_user not in hr_manager.implied_ids:
        hr_manager.write({"implied_ids": [(4, approval_user.id)]})

    _write_rule(env, "rule_psm_hr_discipline_record_portal_own", RECORD_PORTAL_DOMAIN)
    _write_rule(
        env,
        "rule_psm_hr_discipline_record_store_manager",
        RECORD_STORE_MANAGER_DOMAIN,
        [
            "M02_P0200.GDH_OPS_STORE_SM_M",
            "M02_P0200.GDH_OPS_STORE_PM_M",
            "M02_P0200.GDH_OPS_STORE_ST_M",
        ],
    )
    _write_rule(env, "rule_psm_hr_discipline_record_hrbp", RECORD_ALL_DOMAIN)
    _write_rule(env, "rule_psm_hr_discipline_record_oc", RECORD_ALL_DOMAIN)
    _write_rule(env, "rule_psm_hr_discipline_record_rgm", RECORD_RGM_DOMAIN)
    _write_rule(env, "rule_psm_hr_discipline_record_clevel", RECORD_ALL_DOMAIN)

    _write_rule(env, "rule_psm_hr_discipline_explanation_portal_own", EXPLANATION_PORTAL_DOMAIN)
    _write_rule(
        env,
        "rule_psm_hr_discipline_explanation_store_manager",
        EXPLANATION_STORE_MANAGER_DOMAIN,
        [
            "M02_P0200.GDH_OPS_STORE_SM_M",
            "M02_P0200.GDH_OPS_STORE_PM_M",
            "M02_P0200.GDH_OPS_STORE_ST_M",
        ],
    )
    _write_rule(env, "rule_psm_hr_discipline_explanation_hrbp", EXPLANATION_ALL_DOMAIN)
    _write_rule(env, "rule_psm_hr_discipline_explanation_rgm", EXPLANATION_RGM_DOMAIN)
    _write_rule(env, "rule_psm_hr_discipline_explanation_clevel", EXPLANATION_ALL_DOMAIN)

    for xmlid, values in SURVEY_VALUES.items():
        record = _ref(env, f"M02_P0215.{xmlid}")
        if record:
            record.write(values)

    for xmlid, values in QUESTION_VALUES.items():
        question = _ref(env, f"M02_P0215.{xmlid}")
        if question:
            question.write(values)
