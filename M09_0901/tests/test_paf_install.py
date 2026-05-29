# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields
from datetime import timedelta


class TestPafInstall(TransactionCase):

    def test_required_xmlids_are_loaded(self):
        xmlids = [
            'M09_0901.mail_template_paf_evaluation_request',
            'M09_0901.mkt_0901_cron_pspd_refresh',
            'M09_0901.mkt_0901_cron_sla_reminder',
            'M09_0901.mkt_0901_view_paf_pspd_wizard_form',
            'M09_0901.mkt_0901_action_paf_pspd_line',
            'M09_0901.mkt_0901_action_paf_valuation_report',
            'M08_P0801.approval_category_data_pif',
        ]
        for xmlid in xmlids:
            self.assertTrue(self.env.ref(xmlid, raise_if_not_found=False), xmlid)

    def test_m08_pif_category_is_enabled(self):
        category = self.env.ref('M08_P0801.approval_category_data_pif')
        self.assertTrue(category.x_psm_0801_is_pif)

    def test_department_xmlid_mapping(self):
        line_model = self.env['mkt_paf.evaluation.line']
        cases = {
            'M02_P0200.dept_rst_strategy_insights': 'si',
            'M02_P0200.dept_rst_operation': 'ops',
            'M02_P0200.dept_rst_finance': 'finance',
            'M02_P0200.dept_rst_supply_chain': 'sc',
            'M02_P0200.dept_rst_legal': 'legal',
        }
        for xmlid, expected_code in cases.items():
            department = self.env.ref(xmlid, raise_if_not_found=False)
            if department:
                self.assertEqual(line_model._get_dept_code_mapping(department), expected_code)

    def test_promotion_duration_limit_blocks_over_90_days(self):
        template = self.env['mkt_paf.template'].create({
            'name': 'Legal Duration Test',
            'code': 'LEGAL-DURATION-TEST',
        })
        with self.assertRaises(ValidationError):
            self.env['mkt_paf.request'].create({
                'template_id': template.id,
                'planned_start_date': fields.Date.today(),
                'planned_end_date': fields.Date.today() + timedelta(days=91),
            })
