# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, new_test_user, tagged

from odoo.addons.M02_P0214.models.mail_activity import MailActivity as RSTMailActivity


@tagged("post_install", "-at_install", "m02_p0214_security")
class TestM02P0214SecurityHardening(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.regular_user = new_test_user(
            cls.env,
            login="m02_p0214_regular_security_user",
            groups="base.group_user",
        )
        cls.hr_head_user = new_test_user(
            cls.env,
            login="m02_p0214_hr_head_security_user",
            groups="base.group_user,M02_P0200.GDH_RST_HR_HEAD_M",
        )

    def _access_record(self, xmlid):
        return self.env.ref(xmlid)

    def test_phase_1_acl_normalization(self):
        self.assertFalse(
            self.env.ref(
                "M02_P0214.access_mail_activity_internal_user",
                raise_if_not_found=False,
            )
        )
        self.assertFalse(
            self.env.ref(
                "M02_P0214.access_approval_request_internal_user",
                raise_if_not_found=False,
            )
        )

        contract_type_access = self._access_record(
            "M02_P0214.access_hr_contract_type_internal_user"
        )
        self.assertTrue(contract_type_access.perm_read)
        self.assertFalse(contract_type_access.perm_write)
        self.assertFalse(contract_type_access.perm_create)
        self.assertFalse(contract_type_access.perm_unlink)

        resignation_type_access = self._access_record(
            "M02_P0214.access_resignation_type_internal_user"
        )
        self.assertTrue(resignation_type_access.perm_read)
        self.assertFalse(resignation_type_access.perm_write)
        self.assertFalse(resignation_type_access.perm_create)
        self.assertFalse(resignation_type_access.perm_unlink)

    def test_phase_2_direct_manager_rule_groups(self):
        direct_manager_rule = self.env.ref(
            "M02_P0214.rule_0214_approval_request_direct_manager_manage"
        )
        expected_group_ids = {
            self.env.ref("M02_P0200.GDH_RST_HR_ADMIN_M").id,
            self.env.ref("M02_P0200.GDH_RST_HR_CNB_M").id,
            self.env.ref("M02_P0200.GDH_RST_HR_HRBP_M").id,
            self.env.ref("M02_P0200.GDH_RST_HR_HEAD_M").id,
            self.env.ref("M02_P0200.GDH_OPS_STORE_RGM_M").id,
        }
        self.assertEqual(set(direct_manager_rule.groups.ids), expected_group_ids)
        self.assertNotIn(self.env.ref("base.group_user"), direct_manager_rule.groups)

    def test_phase_3_group_check_empty_recordset(self):
        allowed_groups = ("M02_P0200.GDH_RST_HR_HEAD_M",)
        approval_request = self.env["approval.request"]

        with self.assertRaises(AccessError):
            approval_request.with_user(self.regular_user)._check_0214_group_access(
                "Test action",
                allowed_groups,
            )

        approval_request.with_user(self.hr_head_user)._check_0214_group_access(
            "Test action",
            allowed_groups,
        )

    def test_phase_3_mail_activity_does_not_override_unlink(self):
        self.assertNotIn("unlink", RSTMailActivity.__dict__)
        self.assertIn("archive_rst_activities", RSTMailActivity.__dict__)

    def test_phase_4_report_views_and_employee_flag_groups(self):
        report_group_ids = {
            self.env.ref("M02_P0200.GDH_RST_HR_HRBP_S").id,
            self.env.ref("M02_P0200.GDH_RST_HR_HRBP_M").id,
            self.env.ref("M02_P0200.GDH_RST_HR_HEAD_M").id,
            self.env.ref("M02_P0200.GDH_RST_SYSTEM_ST_M").id,
        }
        tree_view = self.env.ref("M02_P0214.view_psm_offboarding_report_tree")
        search_view = self.env.ref("M02_P0214.view_psm_offboarding_report_search")
        self.assertEqual(set(tree_view.group_ids.ids), report_group_ids)
        self.assertEqual(set(search_view.group_ids.ids), report_group_ids)

        employee_view = self.env.ref("M02_P0214.view_psm_employee_form_rst_extension")
        self.assertIn(
            'groups="M02_P0200.GDH_RST_HR_HEAD_M,M02_P0200.GDH_RST_SYSTEM_ST_M"',
            employee_view.arch_db,
        )
