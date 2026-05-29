# -*- coding: utf-8 -*-
from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install", "m02_p0213_annual_leave")
class TestM02P0213AnnualLeave(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env.ref("M02_P0213.psm_0213_approval_category_resignation")
        cls.department = cls.env["hr.department"].create({"name": "OPS Test Dept"})
        cls.manager_user = new_test_user(
            cls.env,
            login="m02_p0213_al_manager",
            groups="base.group_user,M02_P0200.GDH_RST_HR_HEAD_M",
        )
        cls.employee_user = new_test_user(
            cls.env,
            login="m02_p0213_al_employee",
            groups="base.group_user",
        )
        cls.manager = cls.env["hr.employee"].create(
            {
                "name": "OPS Test Manager",
                "user_id": cls.manager_user.id,
                "department_id": cls.department.id,
                "work_email": "ops.manager.test@example.com",
            }
        )
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "OPS Test Employee",
                "user_id": cls.employee_user.id,
                "parent_id": cls.manager.id,
                "department_id": cls.department.id,
                "work_email": "ops.employee.test@example.com",
            }
        )
        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "OPS Test Annual Leave",
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
            "name": "OPS Test Resignation",
            "category_id": self.category.id,
            "request_owner_id": self.employee_user.id,
            "employee_id": self.employee.id,
            "x_psm_0213_employee_id": self.employee.id,
            "x_psm_0213_resignation_date": fields.Date.today(),
        }
        vals.update(extra_vals)
        return self.env["approval.request"].create(vals)

    def _create_validated_al_allocation(self, days):
        allocation = self.env["hr.leave.allocation"].create(
            {
                "name": "OPS Test AL Allocation",
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
                "name": "OPS Test Advance AL Leave",
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee.id,
                "request_date_from": date(2026, 6, 1),
                "request_date_to": date(2026, 6, 16),
            }
        )
        leave._action_validate()
        return leave

    def test_remaining_al_and_advance_compute(self):
        self._create_validated_al_allocation(5.0)
        self._create_validated_al_leave()
        request = self._create_request()
        request.company_id.x_psm_0213_al_leave_type_ids = self.leave_type

        self.employee.x_psm_0200_remaining_al_days = -7.0

        self.assertEqual(request.x_psm_0200_remaining_al_days, -7.0)
        self.assertEqual(request.x_psm_0213_al_advance_days, 7.0)
        self.assertTrue(request.x_psm_0213_al_has_advance)

    def test_action_approve_snapshots_remaining_al(self):
        self._create_validated_al_allocation(5.0)
        self._create_validated_al_leave()
        request = self._create_request()
        request.company_id.x_psm_0213_al_leave_type_ids = self.leave_type

        with patch.object(
            type(request),
            "_get_0213_remaining_al",
            lambda records, employee: -7.0,
        ), patch.object(
            type(request),
            "action_send_exit_survey",
            lambda records: True,
        ), patch.object(
            type(request),
            "_push_0213_contract_end_date",
            lambda records: True,
        ), patch.object(
            type(request),
            "_schedule_offboarding_activities",
            lambda records, plan: True,
        ):
            request.action_approve()

        self.assertEqual(request.x_psm_0200_remaining_al_days, -7.0)
        self.assertEqual(request.x_psm_0213_al_advance_days, 7.0)
        self.assertTrue(request.x_psm_0213_al_has_advance)

    def test_action_settle_advance_al_validates_amount(self):
        self.employee.x_psm_0200_remaining_al_days = -7.0
        request = self._create_request()

        with self.assertRaises(UserError):
            request.action_settle_advance_al()

        request.x_psm_0213_al_deduction_amount = 700.0
        request.action_settle_advance_al()

        self.assertTrue(request.x_psm_0213_al_settled)
