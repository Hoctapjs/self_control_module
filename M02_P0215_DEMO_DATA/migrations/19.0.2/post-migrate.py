# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


RECORD_VALUES = {
    "x_psm_discipline_demo_record_draft": {
        "x_psm_violation_type": "Late arrival / early leave without permission",
        "x_psm_section_i_description": "The employee arrived 25 minutes late for the shift without notifying the shift manager in advance.",
    },
    "x_psm_discipline_demo_record_under_review": {
        "x_psm_violation_type": "Eating during working hours outside the designated area",
        "x_psm_employee_explanation": "The employee confirmed the violation and acknowledged the initial reminder.",
        "x_psm_section_i_description": "The employee ate in the service area while assigned to lobby duty.",
        "x_psm_section_ii_feedback": "I confirm the violation and will not repeat it.",
    },
    "x_psm_discipline_demo_record_company_issued": {
        "x_psm_violation_type": "Verbal harassment",
        "x_psm_employee_explanation": "The employee stated that the reaction happened during a heated shift dispute.",
        "x_psm_section_i_description": "The manager recorded inappropriate language toward a coworker in the kitchen area.",
        "x_psm_section_ii_feedback": "I acknowledge the inappropriate language and agree to cooperate.",
        "x_psm_meeting_notes": "The record has been summarized by HRBP and is ready for company-level approval submission.",
    },
    "x_psm_discipline_demo_record_notified": {
        "x_psm_violation_type": "Incorrect uniform",
        "x_psm_section_i_description": "The employee did not wear the full required uniform when starting the morning shift.",
        "x_psm_section_ii_feedback": "I have received the notice and am reviewing my response.",
    },
    "x_psm_discipline_demo_record_active_feedback": {
        "x_psm_violation_type": "Improvement feedback after store reminder",
        "x_psm_section_iii_identification": "RGM determined this is a minor violation, prioritizing feedback and 30-day follow-up.",
        "x_psm_section_iv_agreement": "The employee agreed to the improvement plan and committed to punctuality and shift compliance.",
    },
    "x_psm_discipline_demo_record_expired_history": {
        "x_psm_violation_type": "Late arrival / early leave without permission",
        "x_psm_section_i_description": "Historical record used to test repeat-offense detection.",
        "x_psm_section_ii_feedback": "The employee completed the previous improvement period.",
    },
    "x_psm_discipline_report_case1_emp_a_1": {
        "x_psm_violation_type": "Report matrix case 1 - employee A attempt 1",
        "x_psm_section_i_description": "Sample data used to test total record count and distinct violating employee count.",
    },
    "x_psm_discipline_report_case1_emp_a_2": {
        "x_psm_violation_type": "Report matrix case 1 - employee A attempt 2",
        "x_psm_section_i_description": "Same employee A, used to confirm distinct employee count does not increase with record count.",
    },
    "x_psm_discipline_report_case1_emp_b_1": {
        "x_psm_violation_type": "Report matrix case 1 - employee B attempt 1",
        "x_psm_section_i_description": "Employee B within the same Case 1 date range.",
    },
    "x_psm_discipline_report_case1_emp_b_2": {
        "x_psm_violation_type": "Report matrix case 1 - employee B attempt 2",
        "x_psm_section_i_description": "Employee B has one additional record to test record counting.",
    },
    "x_psm_discipline_report_case1_emp_c_1": {
        "x_psm_violation_type": "Report matrix case 1 - employee C attempt 1",
        "x_psm_section_i_description": "Employee C belongs to the HR department for department-based permission testing.",
    },
    "x_psm_discipline_report_case2_emp_a_1": {
        "x_psm_violation_type": "Report matrix case 2 - employee A attempt 1",
        "x_psm_section_i_description": "Case 2 includes 3 records for the same employee.",
    },
    "x_psm_discipline_report_case2_emp_a_2": {
        "x_psm_violation_type": "Report matrix case 2 - employee A attempt 2",
        "x_psm_section_i_description": "Case 2 second record for the same employee A.",
    },
    "x_psm_discipline_report_case2_emp_a_3": {
        "x_psm_violation_type": "Report matrix case 2 - employee A attempt 3",
        "x_psm_section_i_description": "Case 2 third record for the same employee A.",
    },
    "x_psm_discipline_report_case3_active_a": {
        "x_psm_section_i_description": "First active record for state-filter testing.",
    },
    "x_psm_discipline_report_case3_draft_b": {
        "x_psm_section_i_description": "Non-cancelled record used to test the default exclusion of cancelled records.",
    },
    "x_psm_discipline_report_case3_active_c": {
        "x_psm_section_i_description": "Second active record used to test state filtering across multiple employees.",
    },
    "x_psm_discipline_report_case3_cancel_a": {
        "x_psm_section_i_description": "Cancelled record used to test the include-cancelled option.",
    },
    "x_psm_discipline_report_case7_store_a": {
        "x_psm_section_i_description": "The demo SM can see this record because it belongs to the same Store Operations department.",
    },
    "x_psm_discipline_report_case7_store_b": {
        "x_psm_section_i_description": "The demo SM can see this record because it belongs to the same Store Operations department.",
    },
    "x_psm_discipline_report_case7_hr_c": {
        "x_psm_section_i_description": "The demo SM should not see this record; HRBP and HR Manager use it to confirm broader access.",
    },
}

EXPLANATION_VALUES = {
    "x_psm_discipline_demo_explanation_company_issued": {
        "x_psm_incident_location": "0215 demo kitchen area",
        "x_psm_explanation_content": "The employee confirmed the dispute and the use of inappropriate language.",
        "x_psm_explanation_reason": "High work pressure during peak hours.",
        "x_psm_explanation_commitment": "Commits to adjusting attitude and not repeating the behavior.",
    },
}


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = "M02_P0215_DEMO_DATA"

    for xmlid, values in RECORD_VALUES.items():
        record = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if record:
            record.write(values)

    for xmlid, values in EXPLANATION_VALUES.items():
        explanation = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if explanation:
            explanation.write(values)
