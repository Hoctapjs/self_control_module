from datetime import timedelta

from odoo import Command, fields
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class Test0502Phase3Flow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.admin.write({"groups_id": [Command.link(cls.env.ref("M02_P0502.group_psm_0502_manager").id)]})
        cls.company = cls.env.company
        cls.Request = cls.env["maintenance.request"].sudo()
        cls.Equipment = cls.env["maintenance.equipment"].sudo()
        cls.Department = cls.env["hr.department"].sudo()
        cls.Partner = cls.env["res.partner"].sudo()
        cls.Team = cls.env["maintenance.team"].sudo()
        cls.Product = cls.env["product.product"].sudo()
        cls.Project = cls.env["project.project"].sudo()
        cls.TaskType = cls.env["project.task.type"].sudo()

        cls.store_partner = cls.Partner.create({"name": "0502 Test Store Partner"})
        cls.vendor = cls.Partner.create({
            "name": "0502 Test Vendor",
            "supplier_rank": 1,
        })
        cls.department = cls.Department.create({
            "name": "0502 Test Store Department",
            "x_psm_0502_partner_id": cls.store_partner.id,
            "x_psm_0502_proposal_approver_id": cls.admin.id,
            "x_psm_0502_proposal_final_approver_id": cls.admin.id,
        })
        cls.other_department = cls.Department.create({
            "name": "0502 Test Other Department",
            "x_psm_0502_partner_id": cls.Partner.create({"name": "0502 Test Other Store Partner"}).id,
        })

        cls.team = cls.Team.create({
            "name": "0502 Test CMT Team",
            "member_ids": [Command.link(cls.admin.id)],
            "x_psm_0502_lead_user_id": cls.admin.id,
            "x_psm_0502_proposal_approver_id": cls.admin.id,
            "x_psm_0502_proposal_auto_approve_limit": 9999999,
            "x_psm_0502_material_approver_id": cls.admin.id,
            "x_psm_0502_material_auto_approve_limit": 9999999,
            "x_psm_0502_default_vendor_id": cls.vendor.id,
            "x_psm_0502_intake_sla_hours": 4,
        })

        cls.category = cls.env["maintenance.equipment.category"].sudo().create({
            "name": "0502 Test Equipment Category",
            "technician_user_id": cls.admin.id,
            "x_psm_0502_inspection_checklist_template": "Check input, output, and safety.",
            "x_psm_0502_inspection_worksheet_template": "Record symptom and root observation.",
            "x_psm_0502_fsm_task_template": "Repair, test, and confirm.",
            "x_psm_0502_fsm_checklist_template": "Lockout, repair, test.",
            "x_psm_0502_fsm_material_template": "Standard maintenance kit.",
        })
        cls.equipment = cls.Equipment.create({
            "name": "0502 Test Equipment",
            "category_id": cls.category.id,
            "owner_user_id": cls.admin.id,
            "technician_user_id": cls.admin.id,
            "maintenance_team_id": cls.team.id,
            "x_psm_0502_department_id": cls.department.id,
        })
        cls.preventive_equipment = cls.Equipment.create({
            "name": "0502 Test Preventive Equipment",
            "category_id": cls.category.id,
            "owner_user_id": cls.admin.id,
            "technician_user_id": cls.admin.id,
            "maintenance_team_id": cls.team.id,
            "x_psm_0502_department_id": cls.department.id,
            "x_psm_0502_enable_preventive_schedule": True,
            "x_psm_0502_preventive_interval_days": 30,
            "x_psm_0502_next_preventive_date": fields.Date.context_today(cls.env["maintenance.equipment"]),
        })
        cls.material = cls.Product.create({
            "name": "0502 Test Spare Part",
            "is_storable": True,
            "purchase_ok": True,
            "standard_price": 10,
        })
        cls._ensure_fsm_project()

    @classmethod
    def _ensure_fsm_project(cls):
        project = cls.Project.search([("is_fsm", "=", True)], limit=1)
        if not project:
            done_stage = cls.TaskType.create({"name": "Done"})
            project = cls.Project.create({
                "name": "0502 Test Field Service",
                "is_fsm": True,
                "company_id": cls.company.id,
                "type_ids": [Command.link(done_stage.id)],
            })
        cls.fsm_project = project

    def _create_base_request(self, **extra_vals):
        vals = {
            "name": extra_vals.pop("name", "0502 Test Request"),
            "equipment_id": self.equipment.id,
            "maintenance_team_id": self.team.id,
            "user_id": self.admin.id,
            "owner_user_id": self.admin.id,
            "maintenance_type": "corrective",
            "request_date": fields.Date.context_today(self.Request),
            "schedule_date": fields.Datetime.now(),
            "schedule_end": fields.Datetime.now() + timedelta(hours=2),
            "x_psm_0502_request_source_id": self.env.ref("M02_P0502.psm_request_source_store_request").id,
            "x_psm_0502_source_system": "manual_request",
            "x_psm_0502_department_id": self.department.id,
            "x_psm_0502_request_type_id": self.env.ref("M02_P0502.psm_request_type_repair").id,
            "x_psm_0502_intake_problem_detail": "Test symptom for 0502 flow.",
            "x_psm_0502_intake_impact_scope": "degraded",
            "x_psm_0502_intake_contact_name": "Store contact",
            "x_psm_0502_intake_contact_phone": "0902000000",
        }
        vals.update(extra_vals)
        return self.Request.create(vals)

    def _inspect_plan_propose(self, request, cost=1000):
        request.write({
            "x_psm_0502_inspection_result": "action_needed",
            "x_psm_0502_inspection_symptom_status": "confirmed",
            "x_psm_0502_inspection_equipment_status": "degraded",
            "x_psm_0502_inspection_safety_risk": "low",
            "x_psm_0502_inspection_action_urgency": "normal",
            "x_psm_0502_inspection_checklist_result": "Checked.",
            "x_psm_0502_inspection_worksheet": "Fault confirmed.",
        })
        request.action_psm_mark_inspected()
        request.action_psm_mark_planned()
        request.write({
            "x_psm_0502_root_cause_analysis": "Root cause for test.",
            "x_psm_0502_technical_solution": "Technical solution for test.",
            "x_psm_0502_estimated_cost": cost,
            "x_psm_0502_estimated_timeline": "Two hours.",
        })
        request.action_psm_mark_proposed()
        request.action_psm_submit_for_approval()

    def _inspect_plan_propose_approve(self, request, cost=1000, route="internal_handling"):
        self._inspect_plan_propose(request, cost=cost)
        self.assertEqual(request.x_psm_0502_approval_status, "approved")
        request.write({
            "x_psm_0502_service_route": route,
            "x_psm_0502_service_route_reason": "internal_capable" if route == "internal_handling" else "specialist_required",
            "x_psm_0502_service_assessment_note": "Service assessment test.",
        })
        request.action_psm_mark_service_assessed()

    def _complete_internal_execution(self, request):
        request.action_psm_create_fsm_task()
        task = request.x_psm_0502_fsm_task_id
        task.write({
            "x_psm_0502_execution_result": "completed_as_planned",
            "x_psm_0502_execution_checklist_note": "Checklist completed.",
            "x_psm_0502_execution_worksheet_note": "Worksheet completed.",
            "x_psm_0502_time_spent_hours": 1.0,
            "state": "1_done",
        })
        request.action_psm_mark_execution_started()
        request.action_psm_mark_execution_completed()

    def test_01_internal_flow_to_done(self):
        request = self._create_base_request(name="0502 Test Internal Flow")
        self._inspect_plan_propose_approve(request)
        request.write({
            "x_psm_0502_has_material_request": False,
            "x_psm_0502_material_assessment_note": "No material required.",
        })
        request.action_psm_mark_material_checked()
        self._complete_internal_execution(request)
        request.write({
            "x_psm_0502_acceptance_result": "accepted",
            "x_psm_0502_acceptance_contact_name": "Store contact",
            "x_psm_0502_acceptance_contact_role": "Store Lead",
            "x_psm_0502_acceptance_equipment_result": "operating_normally",
            "x_psm_0502_acceptance_note": "Accepted.",
        })
        request.action_psm_mark_acceptance_reviewed()
        self.assertEqual(request.stage_id, self.env.ref("M02_P0502.stage_psm_0502_done"))

    def test_02_preventive_cron_generates_request(self):
        self.Equipment.cron_psm_generate_preventive_requests()
        generated = self.preventive_equipment.x_psm_0502_last_preventive_request_id
        self.assertTrue(generated)
        self.assertEqual(generated.x_psm_0502_request_source_code, "preventive_schedule")
        self.assertTrue(generated.x_psm_0502_lead_notified_at)
        generated.action_psm_acknowledge_lead_assignment()
        self.assertEqual(generated.x_psm_0502_lead_acknowledgment_status, "acknowledged")

    def test_03_outside_service_flow(self):
        request = self._create_base_request(name="0502 Test Outside Service")
        self._inspect_plan_propose_approve(request, cost=1000, route="outside_service")
        outside = request.x_psm_0502_outside_service_request_id
        self.assertTrue(outside)
        outside.write({
            "x_psm_vendor_id": self.vendor.id,
            "x_psm_scope_of_work": "Vendor diagnosis.",
        })
        outside.action_psm_send_to_vendor()
        outside.write({
            "x_psm_vendor_quote_amount": 1000,
            "x_psm_vendor_lead_time_days": 1,
        })
        outside.action_psm_record_quote()
        outside.action_psm_approve_vendor()
        outside.action_psm_mark_completed()
        outside.write({
            "x_psm_acceptance_result": "accepted",
            "x_psm_acceptance_note": "Vendor work accepted.",
        })
        outside.action_psm_acceptance_review()
        request.write({
            "x_psm_0502_acceptance_contact_name": "Store contact",
            "x_psm_0502_acceptance_contact_role": "Store Lead",
            "x_psm_0502_acceptance_equipment_result": "operating_normally",
        })
        request.action_psm_mark_acceptance_reviewed()
        self.assertEqual(request.stage_id, self.env.ref("M02_P0502.stage_psm_0502_done"))

    def test_04_material_purchase_recheck_flow(self):
        request = self._create_base_request(name="0502 Test Material Flow")
        self._inspect_plan_propose_approve(request)
        request.write({
            "x_psm_0502_has_material_request": True,
            "x_psm_0502_material_assessment_note": "Material required.",
            "x_psm_0502_material_line_ids": [Command.create({
                "x_psm_product_id": self.material.id,
                "x_psm_estimated_qty": 1,
                "x_psm_estimated_unit_price": 10,
                "x_psm_source_type": "warehouse_stock",
            })],
        })
        request.action_psm_mark_material_checked()
        request.action_psm_create_stock_picking()
        request.action_psm_check_stock_availability()
        if request.x_psm_0502_stock_check_result == "not_available":
            po_action = request.action_psm_create_purchase_order()
            self.assertEqual(po_action["res_model"], "purchase.order")
            self.env["stock.quant"].sudo()._update_available_quantity(
                self.material,
                request.x_psm_0502_stock_picking_id.location_id,
                5,
            )
            po = self.env["purchase.order"].sudo().create({
                "partner_id": self.vendor.id,
                "x_psm_0502_request_id": request.id,
            })
            po.write({"state": "purchase"})
            request.action_psm_recheck_stock_after_purchase()
        self.assertEqual(request.x_psm_0502_stock_check_result, "available")
        request.action_psm_submit_material_approval()
        self.assertEqual(request.x_psm_0502_material_approval_status, "approved")

    def test_05_rework_loop(self):
        request = self._create_base_request(name="0502 Test Rework Loop")
        self._inspect_plan_propose_approve(request)
        request.write({
            "x_psm_0502_has_material_request": False,
            "x_psm_0502_material_assessment_note": "No material.",
        })
        request.action_psm_mark_material_checked()
        self._complete_internal_execution(request)
        request.write({
            "x_psm_0502_acceptance_result": "rework_required",
            "x_psm_0502_acceptance_contact_name": "Store contact",
            "x_psm_0502_acceptance_contact_role": "Store Lead",
            "x_psm_0502_acceptance_equipment_result": "operating_with_monitoring",
            "x_psm_0502_acceptance_note": "Not accepted.",
            "x_psm_0502_acceptance_follow_up_note": "Adjust and retest.",
        })
        request.action_psm_mark_acceptance_reviewed()
        request.action_psm_reopen_for_rework()
        self.assertEqual(request.x_psm_0502_rework_round_count, 1)
        self.assertFalse(request.x_psm_0502_execution_completed_at)
        self._complete_internal_execution(request)
        request.write({
            "x_psm_0502_acceptance_result": "accepted",
            "x_psm_0502_acceptance_contact_name": "Store contact",
            "x_psm_0502_acceptance_contact_role": "Store Lead",
            "x_psm_0502_acceptance_equipment_result": "operating_normally",
            "x_psm_0502_acceptance_note": "Accepted after rework.",
        })
        request.action_psm_mark_acceptance_reviewed()
        self.assertEqual(request.stage_id, self.env.ref("M02_P0502.stage_psm_0502_done"))

    def test_06_two_level_approval_resolution(self):
        final_user = self.env["res.users"].sudo().create({
            "name": "0502 Final Approver",
            "login": "0502_final_approver",
            "groups_id": [Command.link(self.env.ref("M02_P0502.group_psm_0502_store_final_approver").id)],
        })
        self.env["hr.employee"].sudo().create({
            "name": "0502 Final Approver Employee",
            "user_id": final_user.id,
            "department_id": self.department.id,
        })
        self.department.x_psm_0502_proposal_final_approver_id = final_user.id
        self.team.x_psm_0502_proposal_auto_approve_limit = 0
        request = self._create_base_request(name="0502 Test Two Level Approval")
        self._inspect_plan_propose(request, cost=999999)
        self.assertEqual(request.x_psm_0502_approval_status, "pending")
        self.assertEqual(request.x_psm_0502_approval_current_level, 1)
        request.action_psm_approve_proposal()
        self.assertEqual(request.x_psm_0502_approval_status, "pending")
        self.assertEqual(request.x_psm_0502_approval_current_level, 2)
        request.with_user(final_user).action_psm_approve_proposal()
        self.assertEqual(request.x_psm_0502_approval_status, "approved")
        self.team.x_psm_0502_proposal_auto_approve_limit = 9999999

    def test_07_auto_approval_under_limit(self):
        request = self._create_base_request(name="0502 Test Auto Approval")
        self._inspect_plan_propose_approve(request, cost=1, route="internal_handling")
        self.assertEqual(request.x_psm_0502_approval_status, "approved")
        self.assertFalse(request.x_psm_0502_approval_required)

    def test_09_fsm_task_does_not_force_in_execution_stage(self):
        request = self._create_base_request(name="0502 Test FSM Stage Guard")
        self._inspect_plan_propose_approve(request)
        request.write({
            "x_psm_0502_has_material_request": False,
            "x_psm_0502_material_assessment_note": "No material required.",
        })
        request.action_psm_mark_material_checked()
        # tao FSM task nhung chua bat dau thi cong: stage khong duoc nhay sang In Execution
        request.action_psm_create_fsm_task()
        self.assertTrue(request.x_psm_0502_fsm_task_id)
        self.assertNotEqual(
            request.stage_id,
            self.env.ref("M02_P0502.stage_psm_0502_in_execution"),
        )
        # sau khi thuc su bat dau thi cong moi chuyen sang In Execution
        request.action_psm_mark_execution_started()
        self.assertEqual(
            request.stage_id,
            self.env.ref("M02_P0502.stage_psm_0502_in_execution"),
        )

    def test_10_store_user_without_department_sees_nothing(self):
        no_dept_user = self.env["res.users"].sudo().create({
            "name": "0502 Store User No Dept",
            "login": "0502_store_user_no_dept",
            "groups_id": [Command.link(self.env.ref("M02_P0502.group_psm_0502_store_user").id)],
        })
        request = self._create_base_request(name="0502 No Dept Visibility Request")
        visible_requests = self.env["maintenance.request"].with_user(no_dept_user).search([
            ("id", "=", request.id)
        ])
        self.assertNotIn(request, visible_requests)

    def test_08_store_record_rule_own_department(self):
        store_user = self.env["res.users"].sudo().create({
            "name": "0502 Store User",
            "login": "0502_store_user",
            "groups_id": [Command.link(self.env.ref("M02_P0502.group_psm_0502_store_user").id)],
        })
        self.env["hr.employee"].sudo().create({
            "name": "0502 Store Employee",
            "user_id": store_user.id,
            "department_id": self.department.id,
        })
        own_request = self._create_base_request(name="0502 Own Department Request")
        other_request = self._create_base_request(
            name="0502 Other Department Request",
            x_psm_0502_department_id=self.other_department.id,
        )
        visible_requests = self.env["maintenance.request"].with_user(store_user).search([
            ("id", "in", [own_request.id, other_request.id])
        ])
        self.assertIn(own_request, visible_requests)
        self.assertNotIn(other_request, visible_requests)
