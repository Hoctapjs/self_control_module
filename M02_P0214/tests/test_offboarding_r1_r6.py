# -*- coding: utf-8 -*-
import base64
from datetime import date

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install", "m02_p0214_r1_r6")
class TestM02P0214OffboardingR1R6(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env.ref("M02_P0214.approval_category_resignation")
        cls.department = cls.env["hr.department"].create({"name": "RST Test Dept"})
        cls.manager_user = new_test_user(
            cls.env,
            login="m02_p0214_r1_r6_manager",
            groups="base.group_user,M02_P0200.GDH_RST_HR_HEAD_M",
        )
        cls.employee_user = new_test_user(
            cls.env,
            login="m02_p0214_r1_r6_employee",
            groups="base.group_user",
        )
        cls.manager = cls.env["hr.employee"].create(
            {
                "name": "RST Test Manager",
                "user_id": cls.manager_user.id,
                "department_id": cls.department.id,
                "work_email": "rst.manager.test@example.com",
            }
        )
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "RST Test Employee",
                "user_id": cls.employee_user.id,
                "parent_id": cls.manager.id,
                "department_id": cls.department.id,
                "work_email": "rst.employee.test@example.com",
            }
        )
        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "RST Test Annual Leave",
                "requires_allocation": True,
                "employee_requests": True,
                "allocation_validation_type": "no_validation",
                "leave_validation_type": "no_validation",
                "request_unit": "day",
                "allows_negative": True,
                "max_allowed_negative": 20,
            }
        )

    def _create_request(self, **extra_vals):
        vals = {
            "name": "RST Test Resignation",
            "category_id": self.category.id,
            "request_owner_id": self.employee_user.id,
            "employee_id": self.employee.id,
            "x_psm_0214_employee_id": self.employee.id,
            "x_psm_0214_resignation_date": fields.Date.today(),
            "x_psm_0214_employee_personal_email": "personal.rst@example.com",
        }
        vals.update(extra_vals)
        return self.env["approval.request"].create(vals)

    def _create_validated_al_allocation(self, days):
        allocation = self.env["hr.leave.allocation"].create(
            {
                "name": "RST Test AL Allocation",
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee.id,
                "number_of_days": days,
                "date_from": date(2026, 1, 1),
                "date_to": date(2026, 12, 31),
            }
        )
        allocation._action_validate()
        return allocation

    def _create_validated_al_leave(self):
        leave = self.env["hr.leave"].create(
            {
                "name": "RST Test Advance AL Leave",
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee.id,
                "request_date_from": date(2026, 6, 1),
                "request_date_to": date(2026, 6, 16),
            }
        )
        leave._action_validate()
        return leave

    def test_remaining_al_and_employee_email_helpers(self):
        self._create_validated_al_allocation(7.0)
        request = self._create_request()
        request.company_id.x_psm_0214_al_leave_type_ids = self.leave_type

        self.assertEqual(request._get_0214_remaining_al(self.employee), 7.0)
        self.assertEqual(
            request._get_0214_employee_email_list(),
            ["rst.employee.test@example.com", "personal.rst@example.com"],
        )

    def test_negative_al_computes_advance_days(self):
        self._create_validated_al_allocation(5.0)
        self._create_validated_al_leave()
        request = self._create_request()
        request.company_id.x_psm_0214_al_leave_type_ids = self.leave_type

        self.employee.x_psm_0200_remaining_al_days = -7.0

        self.assertEqual(request.x_psm_0200_remaining_al_days, -7.0)
        self.assertEqual(request.x_psm_0214_al_advance_days, 7.0)
        self.assertTrue(request.x_psm_0214_al_has_advance)

    def test_action_approve_requires_signed_resignation_file(self):
        request = self._create_request()

        with self.assertRaises(UserError):
            request.action_approve()

    def test_finance_check_blocks_then_passes_after_settlement(self):
        request = self._create_request(
            x_psm_0214_signed_resignation_file=base64.b64encode(b"rst signed pdf"),
            x_psm_0214_signed_resignation_filename="signed.pdf",
        )
        advance = self.env["x_psm_0214_advance_request"].create(
            {
                "name": "RST-ADV-TEST",
                "employee_id": self.employee.id,
                "amount": 500.0,
                "currency_id": self.env.company.currency_id.id,
                "state": "open",
            }
        )

        request.action_push_to_accounting()
        self.assertEqual(request.x_psm_0214_finance_check_state, "blocked")
        self.assertIn("RST-ADV-TEST", request.x_psm_0214_finance_pending_items_summary)

        advance.state = "settled"
        request.action_push_to_accounting()
        self.assertEqual(request.x_psm_0214_finance_check_state, "passed")

    def test_finance_check_blocks_for_unsettled_advance_al(self):
        self.employee.x_psm_0200_remaining_al_days = -7.0
        request = self._create_request()

        request.action_push_to_accounting()
        self.assertEqual(request.x_psm_0214_finance_check_state, "blocked")
        self.assertIn(
            "Advance Annual Leave",
            request.x_psm_0214_finance_pending_items_summary,
        )

        with self.assertRaises(UserError):
            request.action_settle_advance_al()

        request.x_psm_0214_al_deduction_amount = 700.0
        request.action_settle_advance_al()
        self.assertTrue(request.x_psm_0214_al_settled)

        request.action_push_to_accounting()
        self.assertEqual(request.x_psm_0214_finance_check_state, "passed")

    def test_exit_interview_report_reads_linked_survey_input(self):
        request = self._create_request()
        user_input = self.env["survey.user_input"].create(
            {
                "survey_id": self.env.ref("M02_P0214.survey_exit_interview").id,
                "partner_id": self.employee_user.partner_id.id,
                "email": self.employee_user.email,
                "state": "done",
            }
        )
        request.x_psm_0214_exit_survey_user_input_id = user_input
        self.env.cr.flush()

        report = self.env["x_psm_0214_exit_interview_report"].search(
            [("request_id", "=", request.id)],
            limit=1,
        )
        self.assertTrue(report)
        self.assertEqual(report.employee_id, self.employee)
        self.assertTrue(report.is_completed)
