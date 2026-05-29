from odoo import Command, api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta
# import models la nen tang cua moi model
    # vai tro la de tao table, co ORM cua Odoo, dung duoc create, write, search, unlink
    # khong co models khong viet duoc model

# fields dung de dinh nghia truong du lieu cua model
    # mapping voi database
    # ho tro: tracking, related, compute, ondelete, help, readonly, copy, index, store, default
    # cac truong du lieu co san trong Odoo: Char, Text, Integer, Float, Boolean, Datetime, Date, Selection, Many2one, One2many, Many2many
    # khong co fields khong tao duoc cau truc du lieu cho model

# command dung de tao cac lenh thao tac tren recordset
    # one2many va many2many dung Command de thao tac them, xoa, sua cac record lien ket

# UserError dung de tao loi hien thi cho nguoi dung khi co dieu kien khong duoc thoa
    # dung de dung flow va hien thi popup thong bao loi cho nguoi dung
    # dung cho validation va business rules trong action method cua model


class MaintenanceRequest(models.Model):
    # ke thua model maintenance.request de them truong moi vao ma khong can sua code goc cua Odoo
    # de tranh loi khi cap nhat Odoo trong tuong lai
    _inherit = "maintenance.request"

    _PSM_0502_STAGE_XMLIDS = (
        "M02_P0502.stage_psm_0502_intake",
        "M02_P0502.stage_psm_0502_inspected",
        "M02_P0502.stage_psm_0502_planned",
        "M02_P0502.stage_psm_0502_proposed",
        "M02_P0502.stage_psm_0502_approved",
        "M02_P0502.stage_psm_0502_service_assessed",
        "M02_P0502.stage_psm_0502_material_ready",
        "M02_P0502.stage_psm_0502_in_execution",
        "M02_P0502.stage_psm_0502_acceptance_review",
        "M02_P0502.stage_psm_0502_done",
        "M02_P0502.stage_psm_0502_cancelled",
    )

    _PSM_0502_STAGE_SYNC_FIELDS = {
        "stage_id",
        "x_psm_0502_received_at",
        "x_psm_0502_inspection_result",
        "x_psm_0502_inspected_at",
        "x_psm_0502_ready_to_plan",
        "x_psm_0502_planned_at",
        "x_psm_0502_proposed_at",
        "x_psm_0502_approval_status",
        "x_psm_0502_service_route",
        "x_psm_0502_service_assessed_at",
        "x_psm_0502_has_material_request",
        "x_psm_0502_material_checked_at",
        "x_psm_0502_stock_picking_id",
        "x_psm_0502_stock_check_result",
        "x_psm_0502_material_approval_status",
        "x_psm_0502_stock_issue_status",
        "x_psm_0502_purchase_order_id",
        "x_psm_0502_fsm_task_id",
        "x_psm_0502_execution_started_at",
        "x_psm_0502_execution_completed_at",
        "x_psm_0502_acceptance_result",
        "x_psm_0502_acceptance_reviewed_at",
    }

    _PSM_0502_DOCUMENT_SEQUENCE_CODES = {
        "request": "psm.maintenance.request",
        "inspection": "psm.inspection.report",
        "proposal": "psm.proposal.document",
        "material": "psm.material.issue.request",
        "acceptance": "psm.acceptance.record",
    }

    # list method

    # ham default de tra ve gia tri mac dinh cho truong x_psm_0502_request_source_id khi tao maintenance request moi
    def _default_x_psm_0502_request_source_id(self):
        # lay mot record trong model x_psm_request_source bang external id
        return self.env.ref(
            # external id cua record trong model x_psm_request_source, duoc dinh nghia trong file data/request_source_data.xml
            "M02_P0502.psm_request_source_store_request",
            raise_if_not_found=False,
        )

    # ham default de tra ve phong ban cua employee gan voi user hien tai
    # neu user khong co employee hoac employee khong co department thi de trong
    # tu dong chon phong ban mac dinh khi tao maintenance request moi
    # dau . la truy cap thuoc tinh hoac quan he cua mot object
    # lay cai ben phai tu cai ben trai
    # self la record hien tai
    # self.env la environment cua record hien tai, dung de truy cap user hien tai, database, model khac
    # self.env.user la user dang dang nhap hien tai, tra ve mot record cua model res.users
    # self.env.user.employee_id la employee tuong ung voi user hien tai, tra ve mot record cua model hr.employee neu co
    def _default_x_psm_0502_department_id(self):
        # lay user hien tai, tu user lay employee tuong ung
        employee = self.env.user.employee_id
        # neu co employee thi tra ve department_id cua employee, neu khong thi tra ve false
        return employee.department_id if employee else False

    # ham tra ve danh sach field intake con thieu de tao maintenance request day du hon
    def _psm_get_missing_request_input_labels(self):
        self.ensure_one()
        missing_labels = []

        if not self.x_psm_0502_department_id:
            missing_labels.append("Store Department")

        if not self.x_psm_0502_request_type_id:
            missing_labels.append("Request Type")

        if not self.x_psm_0502_request_source_id:
            missing_labels.append("Request Source")

        if (
            self.x_psm_0502_source_system in ("helpdesk_ticket", "imported_request")
            and not self.x_psm_0502_source_reference
        ):
            missing_labels.append("Source Reference")

        return missing_labels

    # ham phan nhom nguon phat sinh thuc te cua nhu cau bao tri de user nhin nhanh hon o buoc 1
    def _psm_get_request_origin_group(self):
        self.ensure_one()

        if self.x_psm_0502_source_system == "preventive_cron":
            return "preventive_need"
        if self.x_psm_0502_source_system == "manual_request":
            return "store_need"
        return "system_need"

    # ham tra ve danh sach du lieu toi thieu con thieu de coi nhu cau da du dieu kien ghi nhan o buoc 1 hay chua
    def _psm_get_intake_minimum_gap_labels(self):
        self.ensure_one()
        missing_labels = []

        if not self.name:
            missing_labels.append("Request Title")
        if not self.x_psm_0502_request_source_id:
            missing_labels.append("Request Source")
        if not self.x_psm_0502_source_system:
            missing_labels.append("Source System")
        if (
            self.x_psm_0502_source_system in ("helpdesk_ticket", "imported_request")
            and not self.x_psm_0502_source_reference
        ):
            missing_labels.append("Source Reference")

        return missing_labels

    # ham tra ve huong dan intake theo loai request, uu tien cau hinh tren master data truoc
    # neu master data chua co noi dung thi fallback ve template mac dinh theo code de khong can tao them dynamic form
    def _psm_get_request_type_intake_template_text(self):
        self.ensure_one()

        request_type = self.x_psm_0502_request_type_id
        if not request_type:
            return False

        if request_type.x_psm_0502_intake_question_template:
            return request_type.x_psm_0502_intake_question_template

        if request_type.code == "maintenance":
            return (
                "1. Thiết bị nào đang cần bảo trì định kỳ?\n"
                "2. Hiện trạng vận hành hiện tại của thiết bị ra sao?\n"
                "3. Có dấu hiệu hao mòn, cảnh báo, rung, nóng hoặc tiếng ồn bất thường không?\n"
                "4. Cửa hàng mong muốn bảo trì vào khung giờ nào để ít ảnh hưởng vận hành nhất?"
            )
        if request_type.code == "repair":
            return (
                "1. Triệu chứng hư hỏng đang gặp là gì?\n"
                "2. Thiết bị đang dừng hẳn hay vẫn chạy nhưng có lỗi?\n"
                "3. Mức độ ảnh hưởng tới vận hành cửa hàng hiện tại ra sao?\n"
                "4. Ai là người liên hệ trực tiếp khi CMT cần xác minh thêm thông tin?"
            )
        if request_type.code == "inspection":
            return (
                "1. Nội dung cần kiểm tra là gì?\n"
                "2. Kiểm tra định kỳ hay kiểm tra do nghi ngờ bất thường?\n"
                "3. Có khu vực hoặc thời điểm nào cần ưu tiên kiểm tra trước không?\n"
                "4. Ai là đầu mối phối hợp tại cửa hàng?"
            )
        return False

    # ham tra ve template de xuat xu ly theo loai request de buoc 11 co artifact proposal ro hon ma chua can tach object proposal rieng
    def _psm_get_request_type_proposal_template_text(self):
        self.ensure_one()

        request_type = self.x_psm_0502_request_type_id
        if not request_type:
            return False

        if request_type.x_psm_0502_proposal_template:
            return request_type.x_psm_0502_proposal_template

        if request_type.code == "maintenance":
            return (
                "1. Mô tả nguyên nhân gốc hoặc giả định bảo trì.\n"
                "2. Ghi rõ hạng mục bảo trì / thay thế / vệ sinh / hiệu chỉnh.\n"
                "3. Nêu ảnh hưởng vận hành nếu trì hoãn thực hiện.\n"
                "4. Ghi rõ chi phí và timeline dự kiến theo khung giờ vận hành."
            )
        if request_type.code == "repair":
            return (
                "1. Ghi rõ lỗi thực tế đã xác nhận.\n"
                "2. Ghi rõ phương án sửa chữa hoặc thay thế.\n"
                "3. Nêu rủi ro nếu không xử lý ngay.\n"
                "4. Ghi rõ chi phí và timeline xử lý dự kiến."
            )
        if request_type.code == "inspection":
            return (
                "1. Nêu phạm vi kiểm tra đã thực hiện.\n"
                "2. Ghi rõ phát hiện chính sau kiểm tra.\n"
                "3. Đề xuất xử lý tiếp theo nếu có.\n"
                "4. Ghi rõ timeline hoặc mốc theo dõi đề xuất."
            )
        return False

    # ham tra ve danh sach field intake chi tiet con thieu de phan biet request da du thong tin ban dau theo phase 3 buoc 2 hay chua
    # chi ep cho nhu cau store/system; nhanh preventive khong bat buoc co contact va problem detail theo cung mot mau
    def _psm_get_intake_detail_gap_labels(self):
        self.ensure_one()
        missing_labels = []

        if self.x_psm_0502_request_origin_group == "preventive_need":
            return missing_labels

        if not self.x_psm_0502_intake_problem_detail:
            missing_labels.append("Intake Problem Detail")
        if not self.x_psm_0502_intake_impact_scope:
            missing_labels.append("Intake Impact Scope")
        if not self.x_psm_0502_intake_contact_name:
            missing_labels.append("Intake Contact Name")

        return missing_labels

    # compute phan nhom nguon phat sinh de tranh user phai tu suy luan tu cac ma source system ky thuat
    @api.depends("x_psm_0502_source_system")
    def _compute_x_psm_0502_request_origin_group(self):
        for request in self:
            request.x_psm_0502_request_origin_group = request._psm_get_request_origin_group()

    # compute co du lieu toi thieu cho buoc phat sinh nhu cau hay chua
    @api.depends("name", "x_psm_0502_request_source_id", "x_psm_0502_source_system", "x_psm_0502_source_reference")
    def _compute_x_psm_0502_intake_minimum_ready_fields(self):
        for request in self:
            missing_labels = request._psm_get_intake_minimum_gap_labels()
            request.x_psm_0502_intake_minimum_ready = not missing_labels
            request.x_psm_0502_intake_minimum_gap_reason = ", ".join(missing_labels)

    # compute huong dan intake dang ap dung theo request type de user nhin ngay tren form request
    @api.depends("x_psm_0502_request_type_id", "x_psm_0502_request_type_id.x_psm_0502_intake_question_template")
    def _compute_x_psm_0502_intake_template_fields(self):
        for request in self:
            request.x_psm_0502_intake_template_guide = request._psm_get_request_type_intake_template_text() or False
            request.x_psm_0502_intake_example_note = request.x_psm_0502_request_type_id.x_psm_0502_intake_example_note or False

    # compute huong dan proposal theo request type de user nhin ngay trong tab Treatment Proposal
    @api.depends("x_psm_0502_request_type_id", "x_psm_0502_request_type_id.x_psm_0502_proposal_template")
    def _compute_x_psm_0502_proposal_template_fields(self):
        for request in self:
            request.x_psm_0502_proposal_template_guide = request._psm_get_request_type_proposal_template_text() or False

    # compute intake chi tiet da day du theo phase 3 buoc 2 hay chua
    @api.depends(
        "x_psm_0502_request_origin_group",
        "x_psm_0502_intake_problem_detail",
        "x_psm_0502_intake_impact_scope",
        "x_psm_0502_intake_contact_name",
    )
    def _compute_x_psm_0502_intake_detail_ready_fields(self):
        for request in self:
            missing_labels = request._psm_get_intake_detail_gap_labels()
            request.x_psm_0502_intake_detail_ready = not missing_labels
            request.x_psm_0502_intake_detail_gap_reason = ", ".join(missing_labels)

    # compute owner intake de nhin ro request dang thuoc ai theo doi tai moc tiep nhan
    @api.depends("x_psm_0502_received_by_id", "maintenance_team_id", "maintenance_team_id.x_psm_0502_lead_user_id", "maintenance_team_id.member_ids", "user_id", "create_uid")
    def _compute_x_psm_0502_intake_owner_user_id(self):
        for request in self:
            request.x_psm_0502_intake_owner_user_id = request._psm_get_intake_owner_user()

    # compute deadline SLA tiep nhan dua tren create_date va cau hinh team
    @api.depends("create_date", "maintenance_team_id", "maintenance_team_id.x_psm_0502_intake_sla_hours")
    def _compute_x_psm_0502_intake_sla_deadline_at(self):
        for request in self:
            if request.create_date and request.maintenance_team_id.x_psm_0502_intake_sla_hours:
                request.x_psm_0502_intake_sla_deadline_at = request.create_date + timedelta(hours=request.maintenance_team_id.x_psm_0502_intake_sla_hours)
            else:
                request.x_psm_0502_intake_sla_deadline_at = False

    # compute ket qua SLA tiep nhan sau khi da receive; request chua receive thi de pending
    @api.depends("x_psm_0502_received_at", "x_psm_0502_intake_sla_deadline_at")
    def _compute_x_psm_0502_intake_sla_result(self):
        for request in self:
            if not request.x_psm_0502_received_at:
                request.x_psm_0502_intake_sla_result = "pending"
            elif request.x_psm_0502_intake_sla_deadline_at and request.x_psm_0502_received_at > request.x_psm_0502_intake_sla_deadline_at:
                request.x_psm_0502_intake_sla_result = "late"
            else:
                request.x_psm_0502_intake_sla_result = "on_time"

    # compute tuoi intake theo gio de user nhin nhanh request da ton bao lau
    @api.depends("create_date", "x_psm_0502_received_at")
    def _compute_x_psm_0502_intake_age_hours(self):
        for request in self:
            if not request.create_date:
                request.x_psm_0502_intake_age_hours = 0.0
                continue

            end_at = request.x_psm_0502_received_at or fields.Datetime.now()
            delta = end_at - request.create_date
            request.x_psm_0502_intake_age_hours = delta.total_seconds() / 3600.0

    # ham tra ve checkpoint tien do nghiep vu de monitoring buoc 10 nhin ro request dang tac o moc nao
    def _psm_get_progress_checkpoint(self):
        self.ensure_one()

        if self.stage_id.done:
            return "closed"
        if self.x_psm_0502_acceptance_reviewed_at:
            return "acceptance"
        if self.x_psm_0502_execution_completed_at or self.x_psm_0502_execution_started_at or self.x_psm_0502_fsm_task_id:
            return "execution"
        if self.x_psm_0502_purchase_order_id or self.x_psm_0502_stock_check_result == "not_available":
            return "purchase"
        if self.x_psm_0502_stock_picking_id or self.x_psm_0502_stock_issue_status in ("pending_issue", "issued", "cancelled"):
            return "stock_issue"
        if self.x_psm_0502_material_approval_status or self.x_psm_0502_stock_check_result == "available":
            return "material_approval"
        if self.x_psm_0502_material_checked_at or self.x_psm_0502_has_material_request:
            return "material_assessment"
        if self.x_psm_0502_service_assessed_at or self.x_psm_0502_service_route:
            return "service_assessment"
        if self.x_psm_0502_approval_status or self.x_psm_0502_proposed_at:
            return "approval"
        if self.x_psm_0502_planned_at or self.x_psm_0502_ready_to_plan:
            return "proposal"
        if self.x_psm_0502_inspected_at or self.x_psm_0502_inspection_result:
            return "planning"
        if self.x_psm_0502_received_at:
            return "inspection"
        return "intake"

    # ham tra ve trang thai nhanh vat tu/kho/mua ngoai de man hinh monitoring nhin dung nhanh cung cap
    def _psm_get_supply_branch_status(self):
        self.ensure_one()

        if self.x_psm_0502_need_outside_service or self.x_psm_0502_service_route == "outside_service":
            return "outside_service"
        if self.x_psm_0502_material_checked_at and not self.x_psm_0502_has_material_request:
            return "no_material_needed"
        if not self.x_psm_0502_has_material_request:
            return "no_material_flow"
        if self.x_psm_0502_purchase_order_id:
            if self.x_psm_0502_purchase_order_state in ("purchase", "done"):
                return "purchase_confirmed"
            return "purchase_in_progress"
        if self.x_psm_0502_stock_check_result == "not_available":
            return "purchase_required"
        if self.x_psm_0502_stock_issue_status == "issued":
            return "stock_issued"
        if self.x_psm_0502_material_approval_status == "approved":
            return "pending_stock_issue"
        if self.x_psm_0502_material_approval_status == "pending":
            return "awaiting_material_approval"
        if self.x_psm_0502_stock_picking_id:
            return "waiting_stock_check"
        return "material_assessment"

    # helper lay danh sach stage chuan 0502 de dong bo Kanban voi checkpoint nghiep vu
    def _psm_get_0502_stage_records(self):
        stages = self.env["maintenance.stage"]
        for xmlid in self._PSM_0502_STAGE_XMLIDS:
            stage = self.env.ref(xmlid, raise_if_not_found=False)
            if stage:
                stages |= stage
        return stages

    # helper nhan dien request thuoc luong 0502 de khong khoa nham request maintenance ngoai module
    def _psm_is_0502_request(self):
        self.ensure_one()

        return bool(
            self.x_psm_0502_request_source_id
            or self.x_psm_0502_request_type_id
            or self.x_psm_0502_source_system
            or self.x_psm_0502_department_id
        )

    # helper check nhanh user co nam trong bat ky group 0502 nao duoc phep hay khong
    def _psm_user_has_any_group(self, group_xmlids):
        user = self.env.user
        return any(user.has_group(group_xmlid) for group_xmlid in group_xmlids)

    # helper chan action duyet de khong chi dua vao viec an nut tren UI
    def _psm_ensure_proposal_approval_group(self):
        for record in self:
            if self.env.user.has_group("M02_P0502.group_psm_0502_manager"):
                continue
            if record.x_psm_0502_approval_current_level == 2:
                allowed_groups = ("M02_P0502.group_psm_0502_store_final_approver",)
            else:
                allowed_groups = ("M02_P0502.group_psm_0502_store_approver",)
            if not record._psm_user_has_any_group(allowed_groups):
                raise UserError("Only a 0502 Store Approver can approve or reject this proposal.")

    # helper chan action duyet vat tu cho vai tro CMT Lead/Manager
    def _psm_ensure_material_approval_group(self):
        if not self._psm_user_has_any_group((
            "M02_P0502.group_psm_0502_cmt_lead",
            "M02_P0502.group_psm_0502_manager",
        )):
            raise UserError("Only a 0502 CMT Lead can approve or reject this material request.")

    # helper quy doi checkpoint/hien trang sang stage chuan 0502 duoc phep dat
    def _psm_get_0502_stage_xmlid_from_progress(self):
        self.ensure_one()

        if self.x_psm_0502_acceptance_reviewed_at and self.x_psm_0502_acceptance_result == "accepted":
            return "M02_P0502.stage_psm_0502_done"
        if self.x_psm_0502_acceptance_reviewed_at or self.x_psm_0502_execution_completed_at:
            return "M02_P0502.stage_psm_0502_acceptance_review"
        # chi coi la In Execution khi da thuc su bat dau thi cong
        # khong dua vao rieng fsm_task_id vi task co the duoc tao ngay sau buoc lap ke hoach
        # (truoc propose/approve/material) khien stage nhay som va lam vo state machine guard
        if self.x_psm_0502_execution_started_at:
            return "M02_P0502.stage_psm_0502_in_execution"
        if (
            self.x_psm_0502_stock_issue_status == "issued"
            or self.x_psm_0502_material_approval_status == "approved"
            or self.x_psm_0502_stock_check_result in ("available", "not_available")
            or self.x_psm_0502_purchase_order_id
            or (self.x_psm_0502_material_checked_at and not self.x_psm_0502_has_material_request)
        ):
            return "M02_P0502.stage_psm_0502_material_ready"
        if self.x_psm_0502_material_checked_at or self.x_psm_0502_has_material_request:
            return "M02_P0502.stage_psm_0502_service_assessed"
        if self.x_psm_0502_service_assessed_at or self.x_psm_0502_service_route:
            return "M02_P0502.stage_psm_0502_service_assessed"
        if self.x_psm_0502_approval_status == "approved":
            return "M02_P0502.stage_psm_0502_approved"
        if self.x_psm_0502_approval_status or self.x_psm_0502_proposed_at:
            return "M02_P0502.stage_psm_0502_proposed"
        if self.x_psm_0502_planned_at or self.x_psm_0502_ready_to_plan:
            return "M02_P0502.stage_psm_0502_planned"
        if self.x_psm_0502_inspected_at or self.x_psm_0502_inspection_result:
            return "M02_P0502.stage_psm_0502_inspected"
        return "M02_P0502.stage_psm_0502_intake"

    def _psm_get_0502_stage_from_progress(self):
        self.ensure_one()

        return self.env.ref(
            self._psm_get_0502_stage_xmlid_from_progress(),
            raise_if_not_found=False,
        )

    # helper khong cho user keo request vuot qua moc nghiep vu da du dieu kien
    def _psm_validate_0502_stage_write(self, target_stage_id):
        if not target_stage_id:
            return

        target_stage = self.env["maintenance.stage"].browse(target_stage_id)
        if not target_stage:
            return

        stages_0502 = self._psm_get_0502_stage_records()
        for record in self:
            if not record._psm_is_0502_request():
                continue
            if target_stage not in stages_0502:
                raise UserError("Please use the standard 0502 maintenance stages for 0502 requests.")

            allowed_stage = record._psm_get_0502_stage_from_progress()
            if allowed_stage and target_stage.sequence > allowed_stage.sequence:
                raise UserError(
                    "This request cannot be moved to '%s' yet. The current allowed 0502 stage is '%s'."
                    % (target_stage.display_name, allowed_stage.display_name)
                )

    # helper dong bo stage sau khi action/write cap nhat checkpoint nghiep vu
    def _psm_sync_0502_stage_from_progress(self):
        for record in self:
            if not record._psm_is_0502_request():
                continue

            target_stage = record._psm_get_0502_stage_from_progress()
            if target_stage and record.stage_id != target_stage:
                record.with_context(
                    psm_0502_skip_stage_sync=True,
                    psm_0502_skip_stage_validation=True,
                ).write({
                    "stage_id": target_stage.id,
                })

    # helper cap so chung tu 0502 dung mot lan khi request di qua tung moc nghiep vu
    def _psm_assign_missing_document_numbers(self):
        sequence_model = self.env["ir.sequence"].sudo()
        for record in self:
            vals = {}
            if not record.name or record.name in ("New Request", "New"):
                vals["name"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["request"]
                ) or record.name
            if record.x_psm_0502_inspected_at and not record.x_psm_0502_inspection_doc_no:
                vals["x_psm_0502_inspection_doc_no"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["inspection"]
                )
            if record.x_psm_0502_proposed_at and not record.x_psm_0502_proposal_doc_no:
                vals["x_psm_0502_proposal_doc_no"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["proposal"]
                )
            if (
                record.x_psm_0502_material_checked_at
                and record.x_psm_0502_has_material_request
                and not record.x_psm_0502_material_issue_doc_no
            ):
                vals["x_psm_0502_material_issue_doc_no"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["material"]
                )
            if record.x_psm_0502_acceptance_reviewed_at and not record.x_psm_0502_acceptance_doc_no:
                vals["x_psm_0502_acceptance_doc_no"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["acceptance"]
                )
            vals = {key: value for key, value in vals.items() if value}
            if vals:
                record.with_context(psm_0502_skip_document_sequence=True).write(vals)

    def action_psm_open_document_pack_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Print 0502 Document Pack",
            "res_model": "x_psm_0502_document_pack_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_x_psm_request_id": self.id,
            },
        }

    def _psm_print_0502_report(self, report_xmlid):
        self._psm_assign_missing_document_numbers()
        return self.env.ref(report_xmlid).report_action(self)

    def action_psm_print_request_document(self):
        return self._psm_print_0502_report("M02_P0502.action_report_psm_0502_request_document")

    def action_psm_print_inspection_report(self):
        return self._psm_print_0502_report("M02_P0502.action_report_psm_0502_inspection_report")

    def action_psm_print_treatment_proposal(self):
        return self._psm_print_0502_report("M02_P0502.action_report_psm_0502_treatment_proposal")

    def action_psm_print_material_issue_request(self):
        return self._psm_print_0502_report("M02_P0502.action_report_psm_0502_material_issue_request")

    def action_psm_print_acceptance_record(self):
        return self._psm_print_0502_report("M02_P0502.action_report_psm_0502_acceptance_record")

    # compute hai field monitoring tong hop de tranh dung qua nhieu domain manh mun trong reporting
    @api.depends(
        "stage_id",
        "stage_id.done",
        "x_psm_0502_received_at",
        "x_psm_0502_inspection_result",
        "x_psm_0502_inspected_at",
        "x_psm_0502_ready_to_plan",
        "x_psm_0502_planned_at",
        "x_psm_0502_proposed_at",
        "x_psm_0502_approval_status",
        "x_psm_0502_service_route",
        "x_psm_0502_service_assessed_at",
        "x_psm_0502_need_outside_service",
        "x_psm_0502_has_material_request",
        "x_psm_0502_material_checked_at",
        "x_psm_0502_stock_picking_id",
        "x_psm_0502_stock_check_result",
        "x_psm_0502_material_approval_status",
        "x_psm_0502_stock_issue_status",
        "x_psm_0502_purchase_order_id",
        "x_psm_0502_purchase_order_state",
        "x_psm_0502_fsm_task_id",
        "x_psm_0502_execution_started_at",
        "x_psm_0502_execution_completed_at",
        "x_psm_0502_acceptance_reviewed_at",
    )
    def _compute_x_psm_0502_monitoring_status_fields(self):
        for request in self:
            request.x_psm_0502_progress_checkpoint = request._psm_get_progress_checkpoint()
            request.x_psm_0502_supply_branch_status = request._psm_get_supply_branch_status()

    # compute template checklist/worksheet theo category cua thiet bi de user biet can kiem tra gi o buoc 4
    @api.depends(
        "equipment_id",
        "equipment_id.category_id",
        "equipment_id.category_id.x_psm_0502_inspection_checklist_template",
        "equipment_id.category_id.x_psm_0502_inspection_worksheet_template",
    )
    def _compute_x_psm_0502_inspection_template_fields(self):
        for request in self:
            category = request.equipment_id.category_id
            request.x_psm_0502_inspection_checklist_template = category.x_psm_0502_inspection_checklist_template if category else False
            request.x_psm_0502_inspection_worksheet_template = category.x_psm_0502_inspection_worksheet_template if category else False

    # ham validate bo field dau vao quan trong cua request
    def _psm_validate_request_input_data(self):
        for request in self:
            missing_labels = request._psm_get_missing_request_input_labels()
            if missing_labels:
                raise UserError(
                    "Please complete the required request intake fields before continuing: %s"
                    % ", ".join(missing_labels)
                )

    # ham validate bo intake chi tiet o phase 3 buoc 2 truoc khi request duoc CMT xac nhan tiep nhan
    def _psm_validate_request_intake_detail_data(self):
        for request in self:
            missing_labels = request._psm_get_intake_detail_gap_labels()
            if missing_labels:
                raise UserError(
                    "Please complete the intake detail fields before CMT receive: %s"
                    % ", ".join(missing_labels)
                )

    # ham resolve owner intake de queue tiep nhan co nguoi theo doi ro rang hon
    def _psm_get_intake_owner_user(self):
        self.ensure_one()

        if self.x_psm_0502_received_by_id:
            return self.x_psm_0502_received_by_id
        if self.maintenance_team_id.x_psm_0502_lead_user_id:
            return self.maintenance_team_id.x_psm_0502_lead_user_id
        if self.maintenance_team_id.member_ids[:1]:
            return self.maintenance_team_id.member_ids[:1]
        if self.user_id:
            return self.user_id
        return self.create_uid

    # ham nay auto dong dau vet tiep nhan cho cac request di vao queue tiep nhan theo cach tao thong thuong
    # khong ap dung cho preventive request do cron sinh ra vi nhanh nay van can lead/CMT xu ly rieng
    def _psm_auto_receive_request_if_needed(self):
        auto_receivable_requests = self.filtered(
            lambda request: (
                not request.x_psm_0502_received_at
                and request.x_psm_0502_source_system == "manual_request"
                and not request._psm_get_intake_detail_gap_labels()
            )
        )
        if not auto_receivable_requests:
            return

        super(MaintenanceRequest, auto_receivable_requests).write({
            "x_psm_0502_received_by_id": self.env.user.id,
            "x_psm_0502_received_at": fields.Datetime.now(),
        })

    @api.model_create_multi
    def create(self, vals_list):
        sequence_model = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") in ("New Request", "New"):
                vals["name"] = sequence_model.next_by_code(
                    self._PSM_0502_DOCUMENT_SEQUENCE_CODES["request"]
                ) or vals.get("name") or "New"
        records = super().create(vals_list)
        records._psm_auto_receive_request_if_needed()
        records._psm_validate_request_input_data()
        records._psm_sync_0502_stage_from_progress()
        records._psm_assign_missing_document_numbers()
        return records

    def write(self, vals):
        if "stage_id" in vals and not self.env.context.get("psm_0502_skip_stage_validation"):
            self._psm_validate_0502_stage_write(vals.get("stage_id"))

        planning_history_field_names = {
            "schedule_date",
            "schedule_end",
            "user_id",
            "x_psm_0502_plan_note",
        }
        proposal_history_field_names = {
            "x_psm_0502_root_cause_analysis",
            "x_psm_0502_technical_solution",
            "x_psm_0502_estimated_cost",
            "x_psm_0502_estimated_timeline",
            "x_psm_0502_cost_note",
            "x_psm_0502_timeline_note",
        }
        planning_history_snapshots = {}
        proposal_history_snapshots = {}
        if planning_history_field_names.intersection(vals.keys()):
            for record in self:
                planning_history_snapshots[record.id] = {
                    "planned_at": record.x_psm_0502_planned_at,
                    "schedule_date": record.schedule_date,
                    "schedule_end": record.schedule_end,
                    "user_id": record.user_id.id,
                    "plan_note": record.x_psm_0502_plan_note,
                }
        if proposal_history_field_names.intersection(vals.keys()):
            for record in self:
                proposal_history_snapshots[record.id] = {
                    "proposed_at": record.x_psm_0502_proposed_at,
                    "root_cause_analysis": record.x_psm_0502_root_cause_analysis,
                    "technical_solution": record.x_psm_0502_technical_solution,
                    "estimated_cost": record.x_psm_0502_estimated_cost,
                    "estimated_timeline": record.x_psm_0502_estimated_timeline,
                    "cost_note": record.x_psm_0502_cost_note,
                    "timeline_note": record.x_psm_0502_timeline_note,
                }

        result = super().write(vals)
        intake_field_names = {
            "x_psm_0502_department_id",
            "x_psm_0502_request_type_id",
            "x_psm_0502_request_source_id",
            "x_psm_0502_source_system",
            "x_psm_0502_source_reference",
        }
        if intake_field_names.intersection(vals.keys()):
            self._psm_validate_request_input_data()

        if planning_history_field_names.intersection(vals.keys()):
            for record in self:
                snapshot = planning_history_snapshots.get(record.id, {})
                if not snapshot.get("planned_at"):
                    continue

                has_planning_changed = any([
                    snapshot.get("schedule_date") != record.schedule_date,
                    snapshot.get("schedule_end") != record.schedule_end,
                    snapshot.get("user_id") != record.user_id.id,
                    snapshot.get("plan_note") != record.x_psm_0502_plan_note,
                ])
                if not has_planning_changed:
                    continue

                change_reason = vals.get("x_psm_0502_plan_change_reason") or record.x_psm_0502_plan_change_reason
                if not change_reason:
                    raise UserError(
                        "Please fill in Planning Change Reason before changing a planned schedule."
                    )

                record._psm_create_planning_history_line(
                    change_type="replan",
                    change_reason=change_reason,
                )

        if proposal_history_field_names.intersection(vals.keys()):
            for record in self:
                snapshot = proposal_history_snapshots.get(record.id, {})
                if not snapshot.get("proposed_at"):
                    continue

                has_proposal_changed = any([
                    snapshot.get("root_cause_analysis") != record.x_psm_0502_root_cause_analysis,
                    snapshot.get("technical_solution") != record.x_psm_0502_technical_solution,
                    snapshot.get("estimated_cost") != record.x_psm_0502_estimated_cost,
                    snapshot.get("estimated_timeline") != record.x_psm_0502_estimated_timeline,
                    snapshot.get("cost_note") != record.x_psm_0502_cost_note,
                    snapshot.get("timeline_note") != record.x_psm_0502_timeline_note,
                ])
                if not has_proposal_changed:
                    continue

                change_reason = vals.get("x_psm_0502_proposal_change_reason") or record.x_psm_0502_proposal_change_reason
                if not change_reason:
                    raise UserError(
                        "Please fill in Proposal Change Reason before changing a proposed treatment proposal."
                    )

                record.write({
                    "x_psm_0502_treatment_proposal": record._psm_build_treatment_proposal_summary(),
                    "x_psm_0502_proposal_document": record._psm_build_proposal_document(),
                })
                record._psm_create_proposal_history_line(
                    change_type="reproposal",
                    change_reason=change_reason,
                )
        if (
            not self.env.context.get("psm_0502_skip_stage_sync")
            and self._PSM_0502_STAGE_SYNC_FIELDS.intersection(vals.keys())
            and set(vals.keys()) != {"stage_id"}
        ):
            self._psm_sync_0502_stage_from_progress()
        document_trigger_fields = {
            "name",
            "x_psm_0502_inspected_at",
            "x_psm_0502_proposed_at",
            "x_psm_0502_material_checked_at",
            "x_psm_0502_has_material_request",
            "x_psm_0502_acceptance_reviewed_at",
        }
        if (
            not self.env.context.get("psm_0502_skip_document_sequence")
            and document_trigger_fields.intersection(vals.keys())
        ):
            self._psm_assign_missing_document_numbers()
        return result

    # ham action de danh dau maintenance request da duoc tiep nhan
    # ham nay se duoc goi khi user nhan nut "Receive Request" tren giao dien maintenance request
    def action_psm_receive_request(self):
        for record in self:
            if not record.x_psm_0502_received_at:
                record._psm_validate_request_intake_detail_data()
                record.write({
                    "x_psm_0502_received_by_id": self.env.user.id,
                    "x_psm_0502_received_at": fields.Datetime.now(),
                })

    # ham action de danh dau maintenance request da duoc kiem tra thuc te ban dau tai hien truong
    # ham nay se duoc goi khi user nhan nut "Mark Inspected" tren giao dien maintenance request
    def action_psm_mark_inspected(self):
        # lap qua tung record trong self
        # neu co record nao chua co thoi diem tiep nhan thi gan thoi diem tiep nhan bang thoi diem hien tai va user tiep nhan bang user hien tai
        for record in self:
            if record.x_psm_0502_inspected_at:
                continue

            missing_labels = []

            if not record.x_psm_0502_inspection_result:
                missing_labels.append("Initial Inspection Result")

            if not record.x_psm_0502_inspection_symptom_status:
                missing_labels.append("Symptom Status")

            if record.x_psm_0502_inspection_result != "no_action_needed":
                if not record.x_psm_0502_inspection_equipment_status:
                    missing_labels.append("Equipment Status")

            if not record.x_psm_0502_inspection_safety_risk:
                missing_labels.append("Safety Risk Level")

            if record.x_psm_0502_inspection_result != "no_action_needed":
                if not record.x_psm_0502_inspection_action_urgency:
                    missing_labels.append("Action Urgency")

                if record.x_psm_0502_inspection_checklist_template and not record.x_psm_0502_inspection_checklist_result:
                    missing_labels.append("Inspection Checklist Result")

                if record.x_psm_0502_inspection_worksheet_template and not record.x_psm_0502_inspection_worksheet:
                    missing_labels.append("Inspection Worksheet")

            if missing_labels:
                raise UserError(
                    "Please complete the structured initial inspection fields before marking this request as inspected: %s"
                    % ", ".join(missing_labels)
                )

            record.write({
                "x_psm_0502_inspected_by_id": self.env.user.id,
                "x_psm_0502_inspected_at": fields.Datetime.now(),
            })

    # ham resolve user dong vai tro CMT Lead theo rule cua phase 2
    # uu tien user duoc cau hinh ro tren maintenance team, sau do moi fallback ve cac nguon co san
    def _psm_get_lead_notification_resolution(self):
        # chi goi 1 record, neu co nhieu hon se bao loi
        self.ensure_one()

        # uu tien lead duoc cau hinh truc tiep tren maintenance team
        lead_user = self.maintenance_team_id.x_psm_0502_lead_user_id
        if lead_user:
            return lead_user, "team_lead"

        # neu chua cau hinh lead rieng thi fallback ve thanh vien dau tien cua team
        lead_user = self.maintenance_team_id.member_ids[:1]
        # neu co thanh vien trong maintenance team thi tra ve user tuong ung
        if lead_user:
            return lead_user, "team_member_fallback"
        # neu khong co thanh vien nao trong maintenance team thi fallback ve technician
        # fallback ve field user_id cua maintenance request, field nay da co san va duoc hien thi tren form voi nhan Technician
        if self.user_id:
            return self.user_id, "technician_fallback"
        return self.env.user, "current_user_fallback"

    # ham resolve nguoi duyet de xuat xu ly/timeline/cost va rule chi phi cua phase 2
    # phase 2 van giu 1 cap duyet, nhung bo sung ro ai duyet va khi nao de xuat duoc auto approve
    def _psm_get_proposal_approval_resolution(self):
        self.ensure_one()

        approval_required = True
        approval_cost_rule = "manual_review_required"
        auto_approve_limit = self.maintenance_team_id.x_psm_0502_proposal_auto_approve_limit or 0.0

        if auto_approve_limit and self.x_psm_0502_estimated_cost <= auto_approve_limit:
            approval_required = False
            approval_cost_rule = "auto_approved_under_limit"

        approver_user = self.x_psm_0502_department_id.x_psm_0502_proposal_approver_id
        if approver_user:
            return approver_user, "store_approver", approval_required, approval_cost_rule

        approver_user = self.maintenance_team_id.x_psm_0502_proposal_approver_id
        if approver_user:
            return approver_user, "team_approver", approval_required, approval_cost_rule

        approver_user = self.maintenance_team_id.x_psm_0502_lead_user_id
        if approver_user:
            return approver_user, "team_lead_fallback", approval_required, approval_cost_rule

        approver_user = self.maintenance_team_id.member_ids[:1]
        if approver_user:
            return approver_user, "team_member_fallback", approval_required, approval_cost_rule

        if self.user_id:
            return self.user_id, "technician_fallback", approval_required, approval_cost_rule

        return self.env.user, "current_user_fallback", approval_required, approval_cost_rule

    # ham boc them logic 2 cap duyet toi thieu cho phase 3 buoc 12
    # chi kich hoat khi request can manual approval va department co cau hinh final approver khac voi nguoi duyet cap dau
    def _psm_get_proposal_approval_flow_resolution(self):
        self.ensure_one()

        approver_user, approval_rule, approval_required, approval_cost_rule = self._psm_get_proposal_approval_resolution()

        final_approver_user = self.x_psm_0502_department_id.x_psm_0502_proposal_final_approver_id
        flow_type = "single_level"
        level_count = 1

        if (
            approval_required
            and approver_user
            and final_approver_user
            and final_approver_user != approver_user
        ):
            flow_type = "two_level"
            level_count = 2

        return {
            "approver_user": approver_user,
            "approval_rule": approval_rule,
            "approval_required": approval_required,
            "approval_cost_rule": approval_cost_rule,
            "flow_type": flow_type,
            "level_count": level_count,
            "final_approver_user": final_approver_user if flow_type == "two_level" else False,
        }

    # ham resolve nguoi duyet nhanh vat tu va rule auto/manual review cho nhanh xuat kho noi bo
    # phase 2 dua owner approval vat tu ve vai tro noi bo tren maintenance team thay vi chi pending/approved toi thieu
    def _psm_get_material_approval_resolution(self):
        self.ensure_one()

        estimated_material_value = sum(
            (line.x_psm_estimated_unit_price or 0.0) * line.x_psm_estimated_qty
            for line in self.x_psm_0502_material_line_ids
        )

        approval_required = True
        approval_value_rule = "manual_review_required"
        auto_approve_limit = self.maintenance_team_id.x_psm_0502_material_auto_approve_limit or 0.0

        # neu trong danh sach vat tu co dong du kien lay tu purchase/other thi khong auto approve
        # day la dau hieu bo line vat tu chua thuan nhat voi nhanh xuat kho noi bo va can user noi bo xem lai
        has_exception_source_type = any(
            line.x_psm_source_type in ("purchase", "other")
            for line in self.x_psm_0502_material_line_ids
        )
        if has_exception_source_type:
            approval_value_rule = "manual_review_required_source_type"
        elif auto_approve_limit and estimated_material_value <= auto_approve_limit:
            approval_required = False
            approval_value_rule = "auto_approved_under_limit"

        approver_user = self.maintenance_team_id.x_psm_0502_material_approver_id
        if approver_user:
            return approver_user, "team_material_approver", approval_required, approval_value_rule, estimated_material_value

        approver_user = self.maintenance_team_id.x_psm_0502_lead_user_id
        if approver_user:
            return approver_user, "team_lead_fallback", approval_required, approval_value_rule, estimated_material_value

        approver_user = self.maintenance_team_id.member_ids[:1]
        if approver_user:
            return approver_user, "team_member_fallback", approval_required, approval_value_rule, estimated_material_value

        if self.user_id:
            return self.user_id, "technician_fallback", approval_required, approval_value_rule, estimated_material_value

        return self.env.user, "current_user_fallback", approval_required, approval_value_rule, estimated_material_value

    # ham tra ve business status cua nhanh xuat kho dua tren state hien tai cua stock.picking
    # muc tieu cua phase 2 buoc 18 la de request khong chi hien state ky thuat cua picking ma con co status de user nghiep vu de doc hon
    def _psm_get_stock_issue_sync_values(self, picking):
        self.ensure_one()

        stock_issue_status = "pending_issue"
        if not picking:
            stock_issue_status = "no_picking"
        elif picking.state == "done":
            stock_issue_status = "issued"
        elif picking.state == "cancel":
            stock_issue_status = "cancelled"

        sync_vals = {
            "x_psm_0502_stock_issue_status": stock_issue_status,
            "x_psm_0502_stock_issue_synced_at": fields.Datetime.now(),
        }

        if picking and picking.state == "done" and not self.x_psm_0502_stock_issued_at:
            sync_vals.update({
                "x_psm_0502_stock_issued_by_id": self.env.user.id,
                "x_psm_0502_stock_issued_at": fields.Datetime.now(),
            })

        return sync_vals

    # ham tao activity thong bao cho CMT Lead biet request preventive da den han can xu ly
    # phase 1 chi can dung mail.activity de "nhin thay duoc" viec den han
    def action_psm_notify_lead(self):
        # lay activity type de tao activity loai todo
        # self.env.ref(...) : tim record trong model mail.activity.type bang external id
        todo_activity_type = self.env.ref(
            # xml id voi 2 phan : ten module va id record
            # model nam trong mail.activity.type
            "mail.mail_activity_data_todo",
            # neu khong tim thay record thi tra ve None ma khong bao loi
            raise_if_not_found=False,
        )

        # lap qua tung record trong self de tao activity thong bao cho CMT Lead
        for record in self:
            # tim user phu hop de nhan thong bao, neu khong tim duoc user nao thi bo qua khong tao activity
            lead_user, lead_rule = record._psm_get_lead_notification_resolution()
            # cau dieu kien bo qua vong lap hien tai neu thieu du lieu can thiet
            # neu chua co activity type hoac chua co user lead thi khong the tao activity thong bao
            if not todo_activity_type or not lead_user:
                continue

            # neu lead da notify truoc do bi doi cau hinh, xoa activity cu de khong treo viec cho lead cu
            if (
                record.x_psm_0502_lead_notified_user_id
                and record.x_psm_0502_lead_notified_user_id != lead_user
            ):
                old_activities = self.env["mail.activity"].search([
                    ("res_model", "=", record._name),
                    ("res_id", "=", record.id),
                    ("activity_type_id", "=", todo_activity_type.id),
                    ("user_id", "=", record.x_psm_0502_lead_notified_user_id.id),
                    ("summary", "=", "0502 Preventive Request Due"),
                ])
                old_activities.unlink()

            # kiem tra xem da ton tai activity thong bao cho CMT Lead ve request preventive den han chua
            # neu da ton tai thi khong tao them de tranh lap di lap lai nhieu activity cho cung 1 request preventive
            existing_activity = self.env["mail.activity"].search([
                ("res_model", "=", record._name),
                ("res_id", "=", record.id),
                ("activity_type_id", "=", todo_activity_type.id),
                ("user_id", "=", lead_user.id),
                ("summary", "=", "0502 Preventive Request Due"),
            ], limit=1)

            # neu chua ton tai activity nao nhu vay thi tao moi activity de thong bao cho CMT Lead
            # pattern : fallback value chain : luon co mot chuoi uu tien, dam bao luon co gia tri de dung
            if not existing_activity:
                # khoi tao bien deadline_date de tinh ngay het han cua request preventive, mac dinh la False neu khong tinh duoc
                deadline_date = False
                # neu co schedule_date thi thuc hien convert gia tri ve date
                if record.schedule_date:
                    deadline_date = fields.Datetime.to_datetime(record.schedule_date).date()
                # neu khong co schedule_date thi dung ngay request_date neu co
                elif record.request_date:
                    deadline_date = record.request_date
                # neu khong co ca hai thi lay luon ngay hom nay
                else:
                    deadline_date = fields.Date.context_today(record)

                # method built-in cua Odoo, tao 1 activity va gan no voi record hien tai
                # tao mot task nhac viec co deadline va assign cho user, gan voi record do
                record.activity_schedule(
                    # activity type de xac dinh loai activity, o day la todo
                    "mail.mail_activity_data_todo",
                    # user_id de xac dinh ai la nguoi nhan task, o day la lead_user da tim duoc o tren
                    user_id=lead_user.id,
                    # date_deadline de xac dinh ngay het han cua task, o day la deadline_date da duoc tinh toan o tren
                    date_deadline=deadline_date,
                    # summary de xac dinh tieu de cua task
                    summary="0502 Preventive Request Due",
                    note=(
                        "A preventive maintenance request has been generated automatically from the equipment schedule. "
                        "The CMT Lead should review it and consolidate it into the planning queue."
                    ),
                )

            # sau khi tao xong activity thong bao cho CMT Lead thi cap nhat lai maintenance request
            # voi user duoc xem la CMT Lead va thoi diem da gui thong bao
            record.write({
                "x_psm_0502_lead_notified_user_id": lead_user.id,
                "x_psm_0502_lead_notification_rule": lead_rule,
                "x_psm_0502_lead_notified_at": fields.Datetime.now(),
                "x_psm_0502_lead_acknowledgment_status": "pending",
                "x_psm_0502_lead_acknowledged_by_id": False,
                "x_psm_0502_lead_acknowledged_at": False,
            })

    @api.model
    def cron_psm_create_intake_sla_warning_activities(self):
        todo_activity_type = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        if not todo_activity_type:
            return

        now_dt = fields.Datetime.now()
        warning_deadline = now_dt + timedelta(hours=1)
        requests = self.search([
            ("archive", "=", False),
            ("x_psm_0502_received_at", "=", False),
            ("x_psm_0502_intake_sla_deadline_at", "!=", False),
            ("x_psm_0502_intake_sla_deadline_at", "<=", warning_deadline),
        ])

        for record in requests:
            owner_user = record.x_psm_0502_intake_owner_user_id or record._psm_get_intake_owner_user()
            if not owner_user:
                continue

            existing_activity = self.env["mail.activity"].search([
                ("res_model", "=", record._name),
                ("res_id", "=", record.id),
                ("activity_type_id", "=", todo_activity_type.id),
                ("user_id", "=", owner_user.id),
                ("summary", "=", "0502 Intake SLA Warning"),
            ], limit=1)
            if existing_activity:
                continue

            record.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=owner_user.id,
                date_deadline=fields.Datetime.to_datetime(record.x_psm_0502_intake_sla_deadline_at).date(),
                summary="0502 Intake SLA Warning",
                note=(
                    "This 0502 maintenance request is close to or past its intake SLA deadline. "
                    "Please receive the request or update the intake information."
                ),
            )

    # ham de chinh lead duoc notify xac nhan da nhan viec preventive
    def action_psm_acknowledge_lead_assignment(self):
        for record in self:
            if not record.x_psm_0502_lead_notified_user_id:
                raise UserError("No lead assignment has been notified for this request yet.")

            if record.x_psm_0502_lead_notified_user_id != self.env.user:
                raise UserError("Only the notified CMT Lead can acknowledge this assignment.")

            record.write({
                "x_psm_0502_lead_acknowledgment_status": "acknowledged",
                "x_psm_0502_lead_acknowledged_by_id": self.env.user.id,
                "x_psm_0502_lead_acknowledged_at": fields.Datetime.now(),
            })

    # ham xac dinh request da du dieu kien nghiep vu de dua vao buoc lap ke hoach hay chua
    def _psm_get_planning_block_reasons(self):
        self.ensure_one()
        missing_labels = []

        if not self.x_psm_0502_department_id:
            missing_labels.append("Store Department")
        if not self.x_psm_0502_request_type_id:
            missing_labels.append("Request Type")
        if not self.x_psm_0502_request_source_id:
            missing_labels.append("Request Source")

        if self.maintenance_type == "preventive" and self.x_psm_0502_request_source_code == "preventive_schedule":
            if not self.x_psm_0502_lead_notified_at:
                missing_labels.append("Lead Notification")
            return missing_labels

        if not self.x_psm_0502_received_at:
            missing_labels.append("CMT Receive")
        if not self.x_psm_0502_inspected_at:
            missing_labels.append("Initial Inspection")
        if self.x_psm_0502_inspection_result != "action_needed":
            missing_labels.append("Inspection Result = Action Needed")

        return missing_labels

    # ham compute cho biet request nay da ready de lap ke hoach hay chua va neu chua thi bi chan boi ly do nao
    @api.depends(
        "maintenance_type",
        "x_psm_0502_request_source_code",
        "x_psm_0502_department_id",
        "x_psm_0502_request_type_id",
        "x_psm_0502_request_source_id",
        "x_psm_0502_received_at",
        "x_psm_0502_inspected_at",
        "x_psm_0502_inspection_result",
        "x_psm_0502_lead_notified_at",
    )
    def _compute_x_psm_0502_planning_ready_fields(self):
        for record in self:
            missing_labels = record._psm_get_planning_block_reasons()
            record.x_psm_0502_ready_to_plan = not missing_labels
            record.x_psm_0502_planning_block_reason = ", ".join(missing_labels) if missing_labels else False

    @api.depends("x_psm_0502_material_line_ids", "x_psm_0502_material_line_ids.x_psm_request_id")
    def _compute_x_psm_0502_material_line_count(self):
        for record in self:
            record.x_psm_0502_material_line_count = len(record.x_psm_0502_material_line_ids)

    # ham validation dung chung cho buoc lap ke hoach phase 2
    def _psm_validate_planning_inputs(self):
        for record in self:
            missing_labels = record._psm_get_planning_block_reasons()
            if missing_labels:
                raise UserError(
                    "This request is not ready to plan yet. Please complete: %s"
                    % ", ".join(missing_labels)
                )
            if not record.schedule_date:
                raise UserError("Please set Scheduled Date before marking this request as planned.")
            if record.schedule_end and record.schedule_end < record.schedule_date:
                raise UserError("Scheduled End must be greater than or equal to Scheduled Date.")
            if not record.user_id:
                raise UserError("Please set Responsible before marking this request as planned.")

    # ham tao dong lich su planning de truy vet lan dau lap ke hoach va cac lan re-plan o phase 3
    def _psm_create_planning_history_line(self, change_type, change_reason=False):
        self.ensure_one()

        next_revision = (self.x_psm_0502_planning_revision_count or 0) + 1
        history_line = self.env["x_psm_request_planning_history"].create({
            "x_psm_request_id": self.id,
            "x_psm_revision": next_revision,
            "x_psm_change_type": change_type,
            "x_psm_schedule_date": self.schedule_date,
            "x_psm_schedule_end": self.schedule_end,
            "x_psm_responsible_user_id": self.user_id.id,
            "x_psm_plan_note": self.x_psm_0502_plan_note or False,
            "x_psm_change_reason": change_reason or False,
            "x_psm_changed_by_id": self.env.user.id,
            "x_psm_changed_at": fields.Datetime.now(),
        })

        self.write({
            "x_psm_0502_planning_revision_count": next_revision,
            "x_psm_0502_last_planning_changed_by_id": self.env.user.id,
            "x_psm_0502_last_planning_changed_at": history_line.x_psm_changed_at,
        })

        return history_line

    # ham build proposal document ro hon summary de phase 3 buoc 11 co artifact de xuat tren request ma chua can tach object proposal rieng
    def _psm_build_proposal_document(self):
        self.ensure_one()

        document_sections = []

        if self.name:
            document_sections.append("Request: %s" % self.name)
        if self.x_psm_0502_department_id:
            document_sections.append("Store Department: %s" % self.x_psm_0502_department_id.display_name)
        if self.x_psm_0502_request_type_id:
            document_sections.append("Request Type: %s" % self.x_psm_0502_request_type_id.display_name)
        if self.x_psm_0502_proposal_template_guide:
            document_sections.append("Proposal Template Guide:\n%s" % self.x_psm_0502_proposal_template_guide.strip())
        if self.x_psm_0502_root_cause_analysis:
            document_sections.append("Root Cause Analysis:\n%s" % self.x_psm_0502_root_cause_analysis.strip())
        if self.x_psm_0502_technical_solution:
            document_sections.append("Technical Solution:\n%s" % self.x_psm_0502_technical_solution.strip())

        cost_lines = []
        if self.x_psm_0502_estimated_cost:
            currency_name = self.x_psm_0502_currency_id.name or ""
            if currency_name:
                cost_lines.append("Estimated Cost: %s %s" % (self.x_psm_0502_estimated_cost, currency_name))
            else:
                cost_lines.append("Estimated Cost: %s" % self.x_psm_0502_estimated_cost)
        if self.x_psm_0502_cost_note:
            cost_lines.append(self.x_psm_0502_cost_note.strip())
        if cost_lines:
            document_sections.append("Cost:\n%s" % "\n".join(cost_lines))

        timeline_lines = []
        if self.x_psm_0502_estimated_timeline:
            timeline_lines.append("Estimated Timeline: %s" % self.x_psm_0502_estimated_timeline)
        if self.x_psm_0502_timeline_note:
            timeline_lines.append(self.x_psm_0502_timeline_note.strip())
        if timeline_lines:
            document_sections.append("Timeline:\n%s" % "\n".join(timeline_lines))

        if self.x_psm_0502_treatment_proposal:
            document_sections.append("Proposal Summary:\n%s" % self.x_psm_0502_treatment_proposal.strip())

        return "\n\n".join(section for section in document_sections if section).strip()

    # ham tao proposal revision compare text de user nhin nhanh lan sua de xuat gan nhat da thay doi nhung gi so voi lan truoc
    def _psm_build_proposal_revision_compare(self):
        self.ensure_one()

        history_lines = self.x_psm_0502_proposal_history_ids.sorted(lambda line: (-line.x_psm_revision, -line.id))
        if len(history_lines) < 2:
            return False

        latest_history = history_lines[0]
        previous_history = history_lines[1]
        compare_lines = [
            "Compare Revision %s vs Revision %s" % (latest_history.x_psm_revision, previous_history.x_psm_revision)
        ]

        if latest_history.x_psm_root_cause_analysis != previous_history.x_psm_root_cause_analysis:
            compare_lines.append("- Root Cause Analysis changed")
        if latest_history.x_psm_technical_solution != previous_history.x_psm_technical_solution:
            compare_lines.append("- Technical Solution changed")
        if latest_history.x_psm_estimated_cost != previous_history.x_psm_estimated_cost:
            compare_lines.append("- Estimated Cost changed")
        if latest_history.x_psm_estimated_timeline != previous_history.x_psm_estimated_timeline:
            compare_lines.append("- Estimated Timeline changed")
        if latest_history.x_psm_cost_note != previous_history.x_psm_cost_note:
            compare_lines.append("- Cost Note changed")
        if latest_history.x_psm_timeline_note != previous_history.x_psm_timeline_note:
            compare_lines.append("- Timeline Note changed")

        if len(compare_lines) == 1:
            compare_lines.append("- No structural difference detected")

        return "\n".join(compare_lines)

    # compute proposal compare text de request nhin ngay tren form ma khong can mo tung revision
    @api.depends(
        "x_psm_0502_proposal_history_ids",
        "x_psm_0502_proposal_history_ids.x_psm_revision",
        "x_psm_0502_proposal_history_ids.x_psm_root_cause_analysis",
        "x_psm_0502_proposal_history_ids.x_psm_technical_solution",
        "x_psm_0502_proposal_history_ids.x_psm_estimated_cost",
        "x_psm_0502_proposal_history_ids.x_psm_estimated_timeline",
        "x_psm_0502_proposal_history_ids.x_psm_cost_note",
        "x_psm_0502_proposal_history_ids.x_psm_timeline_note",
    )
    def _compute_x_psm_0502_proposal_revision_compare(self):
        for request in self:
            request.x_psm_0502_proposal_revision_compare = request._psm_build_proposal_revision_compare() or False

    # ham tao dong lich su de xuat xu ly de truy vet initial proposal va cac lan reproposal o phase 3
    def _psm_create_proposal_history_line(self, change_type, change_reason=False):
        self.ensure_one()

        next_revision = (self.x_psm_0502_proposal_revision_count or 0) + 1
        history_line = self.env["x_psm_request_proposal_history"].create({
            "x_psm_request_id": self.id,
            "x_psm_revision": next_revision,
            "x_psm_change_type": change_type,
            "x_psm_root_cause_analysis": self.x_psm_0502_root_cause_analysis or False,
            "x_psm_technical_solution": self.x_psm_0502_technical_solution or False,
            "x_psm_estimated_cost": self.x_psm_0502_estimated_cost or 0.0,
            "x_psm_currency_id": self.x_psm_0502_currency_id.id or False,
            "x_psm_estimated_timeline": self.x_psm_0502_estimated_timeline or False,
            "x_psm_cost_note": self.x_psm_0502_cost_note or False,
            "x_psm_timeline_note": self.x_psm_0502_timeline_note or False,
            "x_psm_proposal_summary": self.x_psm_0502_treatment_proposal or False,
            "x_psm_proposal_document": self.x_psm_0502_proposal_document or False,
            "x_psm_change_reason": change_reason or False,
            "x_psm_changed_by_id": self.env.user.id,
            "x_psm_changed_at": fields.Datetime.now(),
        })

        self.write({
            "x_psm_0502_proposal_revision_count": next_revision,
            "x_psm_0502_last_proposal_changed_by_id": self.env.user.id,
            "x_psm_0502_last_proposal_changed_at": history_line.x_psm_changed_at,
        })

        return history_line

    # ham validate bo dong vat tu phat sinh de buoc 14 khong dung lai o muc co/khong
    def _psm_validate_material_assessment_inputs(self):
        for record in self:
            if not record.x_psm_0502_has_material_request and record.x_psm_0502_material_line_ids:
                raise UserError(
                    "This request is marked as not requiring material, but material detail lines still exist. "
                    "Please either remove the lines or enable Has Material Request."
                )

            if not record.x_psm_0502_has_material_request:
                continue

            if not record.x_psm_0502_material_line_ids:
                raise UserError(
                    "Please add at least one material detail line before marking this request as material checked."
                )

            invalid_line_messages = []
            for index, line in enumerate(record.x_psm_0502_material_line_ids, start=1):
                line_missing_labels = []
                if not line.x_psm_product_id:
                    line_missing_labels.append("Material")
                if line.x_psm_estimated_qty <= 0:
                    line_missing_labels.append("Estimated Quantity > 0")
                if not line.x_psm_source_type:
                    line_missing_labels.append("Expected Source")

                if line_missing_labels:
                    invalid_line_messages.append(
                        "Line %s: %s" % (index, ", ".join(line_missing_labels))
                    )

            if invalid_line_messages:
                raise UserError(
                    "Please complete the structured material detail lines before marking this request as material checked:\n%s"
                    % "\n".join(invalid_line_messages)
                )

    # ham resolve cau hinh kho se dung cho buoc 15 theo uu tien team truoc, sau do moi fallback ve warehouse mac dinh
    def _psm_get_material_stock_flow_resolution(self):
        self.ensure_one()

        warehouse = self.env["stock.warehouse"].search([
            ("company_id", "=", self.company_id.id),
        ], limit=1)

        picking_type = self.maintenance_team_id.x_psm_0502_material_picking_type_id
        picking_rule = "team_configured_picking_type"

        if not picking_type:
            picking_type = warehouse.int_type_id
            picking_rule = "warehouse_internal_type"

        if not picking_type:
            picking_type = self.env["stock.picking.type"].search([
                ("code", "=", "internal"),
                "|",
                ("company_id", "=", self.company_id.id),
                ("company_id", "=", False),
            ], limit=1)
            picking_rule = "generic_internal_type_fallback"

        if not picking_type:
            raise UserError("No internal transfer operation type was found. Please configure the Stock module first.")

        source_location = self.maintenance_team_id.x_psm_0502_material_source_location_id
        if not source_location:
            source_location = picking_type.default_location_src_id or warehouse.lot_stock_id

        destination_location = self.maintenance_team_id.x_psm_0502_material_destination_location_id
        if not destination_location:
            destination_location = picking_type.default_location_dest_id or warehouse.lot_stock_id

        if not source_location or not destination_location:
            raise UserError(
                "The internal stock flow is not fully configured. Please configure the material source and destination locations first."
            )

        return {
            "warehouse": warehouse,
            "picking_type": picking_type,
            "picking_rule": picking_rule,
            "source_location": source_location,
            "destination_location": destination_location,
        }

    # ham quy doi compute chuan cua stock.picking thanh bo snapshot de buoc 16 va cac buoc sau dung nhat quan
    def _psm_get_stock_check_snapshot_values(self, picking):
        self.ensure_one()

        availability_message = picking.products_availability or False
        availability_state = picking.products_availability_state or False
        stock_check_result = "available" if availability_state == "available" else "not_available"

        return {
            "x_psm_0502_stock_check_availability": availability_message,
            "x_psm_0502_stock_check_availability_state": availability_state,
            "x_psm_0502_stock_check_result": stock_check_result,
        }

    # ham build mo ta mac dinh cho FSM task de ky thuat vien nhin nhanh du context tu request
    def _psm_build_fsm_task_description(self):
        self.ensure_one()

        description_sections = []

        if self.description:
            description_sections.append(self.description.strip())

        request_context_lines = []

        if self.x_psm_0502_request_type_id:
            request_context_lines.append(f"Request Type: {self.x_psm_0502_request_type_id.display_name}")
        if self.x_psm_0502_request_source_id:
            request_context_lines.append(f"Request Source: {self.x_psm_0502_request_source_id.display_name}")
        if self.x_psm_0502_source_system:
            request_context_lines.append(f"Source System: {self._fields['x_psm_0502_source_system'].convert_to_export(self.x_psm_0502_source_system, self)}")
        if self.x_psm_0502_source_reference:
            request_context_lines.append(f"Source Reference: {self.x_psm_0502_source_reference}")
        if self.x_psm_0502_inspection_result:
            request_context_lines.append(
                "Initial Inspection Result: %s"
                % self._fields["x_psm_0502_inspection_result"].convert_to_export(self.x_psm_0502_inspection_result, self)
            )
        if self.x_psm_0502_inspection_equipment_status:
            request_context_lines.append(
                "Equipment Status: %s"
                % self._fields["x_psm_0502_inspection_equipment_status"].convert_to_export(self.x_psm_0502_inspection_equipment_status, self)
            )
        if self.x_psm_0502_inspection_safety_risk:
            request_context_lines.append(
                "Safety Risk Level: %s"
                % self._fields["x_psm_0502_inspection_safety_risk"].convert_to_export(self.x_psm_0502_inspection_safety_risk, self)
            )
        if self.x_psm_0502_inspection_action_urgency:
            request_context_lines.append(
                "Action Urgency: %s"
                % self._fields["x_psm_0502_inspection_action_urgency"].convert_to_export(self.x_psm_0502_inspection_action_urgency, self)
            )

        if request_context_lines:
            description_sections.append("0502 Request Context:\n- " + "\n- ".join(request_context_lines))

        if self.x_psm_0502_treatment_proposal:
            description_sections.append("Treatment Proposal Summary:\n%s" % self.x_psm_0502_treatment_proposal.strip())

        if self.x_psm_0502_plan_note:
            description_sections.append("Planning Note:\n%s" % self.x_psm_0502_plan_note.strip())

        return "\n\n".join(section for section in description_sections if section)

    # ham build execution package template cho FSM task bang cach gom template theo request type, equipment category va service route
    def _psm_get_fsm_task_package_values(self):
        self.ensure_one()

        request_type = self.x_psm_0502_request_type_id
        equipment_category = self.equipment_id.category_id
        service_route_label = False
        service_route_reason_label = False

        if self.x_psm_0502_service_route:
            service_route_label = dict(self._fields["x_psm_0502_service_route"].selection).get(
                self.x_psm_0502_service_route,
                self.x_psm_0502_service_route,
            )
        if self.x_psm_0502_service_route_reason:
            service_route_reason_label = dict(self._fields["x_psm_0502_service_route_reason"].selection).get(
                self.x_psm_0502_service_route_reason,
                self.x_psm_0502_service_route_reason,
            )

        task_template_sections = []
        checklist_template_sections = []
        material_template_sections = []

        if request_type and request_type.x_psm_0502_fsm_task_template:
            task_template_sections.append(
                "Request Type Template:\n%s" % request_type.x_psm_0502_fsm_task_template.strip()
            )
        if equipment_category and equipment_category.x_psm_0502_fsm_task_template:
            task_template_sections.append(
                "Equipment Category Template:\n%s" % equipment_category.x_psm_0502_fsm_task_template.strip()
            )
        if service_route_label:
            route_lines = ["Service Route: %s" % service_route_label]
            if service_route_reason_label:
                route_lines.append("Service Route Reason: %s" % service_route_reason_label)
            task_template_sections.append("\n".join(route_lines))

        if request_type and request_type.x_psm_0502_fsm_checklist_template:
            checklist_template_sections.append(
                "Request Type Checklist:\n%s" % request_type.x_psm_0502_fsm_checklist_template.strip()
            )
        if equipment_category and equipment_category.x_psm_0502_fsm_checklist_template:
            checklist_template_sections.append(
                "Equipment Category Checklist:\n%s" % equipment_category.x_psm_0502_fsm_checklist_template.strip()
            )
        if self.x_psm_0502_inspection_checklist_template:
            checklist_template_sections.append(
                "Inspection Checklist Template:\n%s" % self.x_psm_0502_inspection_checklist_template.strip()
            )

        if request_type and request_type.x_psm_0502_fsm_material_template:
            material_template_sections.append(
                "Request Type Material Package:\n%s" % request_type.x_psm_0502_fsm_material_template.strip()
            )
        if equipment_category and equipment_category.x_psm_0502_fsm_material_template:
            material_template_sections.append(
                "Equipment Category Material Package:\n%s" % equipment_category.x_psm_0502_fsm_material_template.strip()
            )
        if self.x_psm_0502_material_line_ids:
            material_summary_lines = []
            for line in self.x_psm_0502_material_line_ids:
                source_label = dict(line._fields["x_psm_source_type"].selection).get(
                    line.x_psm_source_type,
                    line.x_psm_source_type,
                )
                material_summary_lines.append(
                    "- %s | Qty: %s | Source: %s" % (
                        line.x_psm_product_id.display_name,
                        line.x_psm_estimated_qty,
                        source_label,
                    )
                )
            material_template_sections.append(
                "Request Material Detail Lines:\n%s" % "\n".join(material_summary_lines)
            )

        return {
            "task_template_note": "\n\n".join(task_template_sections) if task_template_sections else False,
            "execution_checklist_template": "\n\n".join(checklist_template_sections) if checklist_template_sections else False,
            "material_package_template": "\n\n".join(material_template_sections) if material_template_sections else False,
        }

    # ham chuan hoa summary de xuat xu ly tu bo field co cau truc cua phase 2
    # van giu field x_psm_0502_treatment_proposal lam summary chuan de cac buoc sau tiep tuc dung duoc
    def _psm_build_treatment_proposal_summary(self):
        self.ensure_one()
        proposal_sections = []

        if self.x_psm_0502_root_cause_analysis:
            proposal_sections.append(
                "Root Cause Analysis:\n%s" % self.x_psm_0502_root_cause_analysis.strip()
            )

        if self.x_psm_0502_technical_solution:
            proposal_sections.append(
                "Technical Solution:\n%s" % self.x_psm_0502_technical_solution.strip()
            )

        cost_lines = []
        if self.x_psm_0502_estimated_cost:
            currency_name = self.x_psm_0502_currency_id.name or ""
            if currency_name:
                cost_lines.append(
                    "Estimated Cost: %s %s" % (self.x_psm_0502_estimated_cost, currency_name)
                )
            else:
                cost_lines.append("Estimated Cost: %s" % self.x_psm_0502_estimated_cost)
        if self.x_psm_0502_cost_note:
            cost_lines.append(self.x_psm_0502_cost_note.strip())
        if cost_lines:
            proposal_sections.append("Cost Summary:\n%s" % "\n".join(cost_lines))

        timeline_lines = []
        if self.x_psm_0502_estimated_timeline:
            timeline_lines.append("Estimated Timeline: %s" % self.x_psm_0502_estimated_timeline)
        if self.x_psm_0502_timeline_note:
            timeline_lines.append(self.x_psm_0502_timeline_note.strip())
        if timeline_lines:
            proposal_sections.append("Timeline Summary:\n%s" % "\n".join(timeline_lines))

        if not proposal_sections and self.x_psm_0502_treatment_proposal:
            return self.x_psm_0502_treatment_proposal.strip()

        return "\n\n".join(proposal_sections).strip()

    # ham danh dau request da duoc CMT Lead lap ke hoach xu ly trong phase 1
    # phase 1 tan dung luon Scheduled Date va Technician co san cua maintenance.request
    # button nay chi dong vai tro chot dau vet da lap ke hoach, chua thay the module planning
    def action_psm_mark_planned(self):
        # loop qua tung record trong maintenance request de danh dau da lap ke hoach
        for record in self:
            if record.x_psm_0502_planned_at:
                continue

            record._psm_validate_planning_inputs()

            record.write({
                "x_psm_0502_planned_by_id": self.env.user.id,
                "x_psm_0502_planned_at": fields.Datetime.now(),
            })
            if not record.x_psm_0502_planning_history_ids:
                record._psm_create_planning_history_line(
                    change_type="initial_plan",
                    change_reason=record.x_psm_0502_plan_change_reason or "Initial planning confirmation",
                )

    # ham tao field service task tu maintenance request da duoc lap ke hoach
    # phase 1 tan dung module industry_fsm de tao task thuc thi cho ky thuat vien
    def action_psm_create_fsm_task(self):
        # chi xu ly tung request mot de dam bao task tao ra dung voi request hien tai
        self.ensure_one()

        # neu request da co field service task roi thi mo lai task do de tranh tao trung
        if self.x_psm_0502_fsm_task_id:
            return self.action_psm_open_fsm_task()

        # buoc 9 chi cho tao task khi request da duoc lap ke hoach toi thieu o buoc 8
        self._psm_validate_planning_inputs()
        if not self.x_psm_0502_department_id:
            raise UserError("Please set Store Department before creating an FSM task.")

        # lay partner dai dien cua phong ban/cua hang de map vao Customer tren FSM task
        department_partner = self.x_psm_0502_department_id.x_psm_0502_partner_id
        if not department_partner:
            raise UserError(
                "Please configure 0502 FSM Customer on the selected Store Department before creating an FSM task."
            )

        # tim field service project de dua task thuc thi vao dung khong gian fsm
        # uu tien project cung cong ty, neu khong co thi fallback ve mot project fsm bat ky
        fsm_project = self.env["project.project"].search([
            ("is_fsm", "=", True),
            "|",
            ("company_id", "=", self.company_id.id),
            ("company_id", "=", False),
        ], limit=1)
        if not fsm_project:
            fsm_project = self.env["project.project"].search([
                ("is_fsm", "=", True),
            ], limit=1)
        if not fsm_project:
            raise UserError("No Field Service project was found. Please configure industry_fsm first.")

        # mo ta bo sung de task hien thi du dau vet request nguon trong phase 1
        # mo ta cua task se duoc tao tu mo ta cua maintenace request
        task_description = self._psm_build_fsm_task_description()
        task_package_values = self._psm_get_fsm_task_package_values()

        # tao field service task va lien ket nguoc lai ve maintenance request
        fsm_task = self.env["project.task"].with_context(fsm_mode=True).create({
            "name": self.name,
            "project_id": fsm_project.id,
            "partner_id": department_partner.id,
            "user_ids": [Command.set([self.user_id.id])],
            "planned_date_begin": self.schedule_date,
            "date_deadline": self.schedule_end or self.schedule_date,
            "description": task_description or False,
            "priority": self.priority or "0",
            "x_psm_0502_request_id": self.id,
            "x_psm_0502_task_template_note": task_package_values["task_template_note"],
            "x_psm_0502_execution_checklist_template": task_package_values["execution_checklist_template"],
            "x_psm_0502_material_package_template": task_package_values["material_package_template"],
        })

        # luu lien ket task de nhung lan sau mo lai va theo doi de dang hon
        self.write({
            "x_psm_0502_fsm_task_id": fsm_task.id,
        })
        return self.action_psm_open_fsm_task()

    # ham mo form field service task da tao tu maintenance request
    def action_psm_open_fsm_task(self):
        # chi xu ly mot request de dam bao mo dung task lien ket voi request
        self.ensure_one()

        # neu request chua co task lien ket thi bao loi cho nguoi dung biet phai tao task truoc khi mo
        if not self.x_psm_0502_fsm_task_id:
            raise UserError("No FSM task has been created for this request yet.")
        
        # mo form cua fsm task lien ket voi request hien tai
        return {
            "type": "ir.actions.act_window",
            "name": "FSM Task",
            # model se duoc mo khi user nhan nut
            "res_model": "project.task",
            # kieu view se duoc su dung de mo
            "view_mode": "form",
            # id cua record can mo
            "res_id": self.x_psm_0502_fsm_task_id.id,
            # mo o dau, trong tab hien tai cua trinh duyet (current) hay mo o tab moi (new)
            "target": "current",
        }

    # ham danh dau request da duoc CMT de xuat phuong an xu ly hoac muc bao gia so bo
    # phase 1 chi luu tru de xuat tren maintenance request, chua tach thanh quy trinh bao gia rieng
    def action_psm_mark_proposed(self):
        for record in self:
            if record.x_psm_0502_proposed_at:
                continue

            missing_labels = []

            if not record.x_psm_0502_root_cause_analysis:
                missing_labels.append("Root Cause Analysis")

            if not record.x_psm_0502_technical_solution:
                missing_labels.append("Technical Solution")

            if not record.x_psm_0502_estimated_cost:
                missing_labels.append("Estimated Cost")

            if not record.x_psm_0502_estimated_timeline:
                missing_labels.append("Estimated Timeline")

            # phai co bo noi dung de xuat co cau truc toi thieu truoc khi danh dau da de xuat
            if missing_labels:
                raise UserError(
                    "Please complete the structured treatment proposal fields before marking this request as proposed: %s"
                    % ", ".join(missing_labels)
                )

            # neu da ket luan khong can xu ly thi khong nen di tiep sang buoc de xuat
            if record.x_psm_0502_inspection_result == "no_action_needed":
                raise UserError("This request is marked as No Action Needed, so no treatment proposal should be recorded.")

            record.write({
                "x_psm_0502_treatment_proposal": record._psm_build_treatment_proposal_summary(),
                "x_psm_0502_proposal_document": record._psm_build_proposal_document(),
                "x_psm_0502_proposed_by_id": self.env.user.id,
                "x_psm_0502_proposed_at": fields.Datetime.now(),
            })
            if not record.x_psm_0502_proposal_history_ids:
                record._psm_create_proposal_history_line(
                    change_type="initial_proposal",
                    change_reason=record.x_psm_0502_proposal_change_reason or "Initial proposal confirmation",
                )

    # ham gui de xuat xu ly/timeline/cost sang trang thai cho duyet o muc toi thieu cho phase 1
    # phase 1 chua dung approval matrix, chi can diem quyet dinh pending -> approved/rejected
    def action_psm_submit_for_approval(self):
        for record in self:
            # phai co de xuat xu ly truoc khi gui cua hang duyet
            if not record.x_psm_0502_proposed_at or not record.x_psm_0502_treatment_proposal:
                raise UserError("Please complete and mark the treatment proposal before submitting it for approval.")

            approval_resolution = record._psm_get_proposal_approval_flow_resolution()
            approver_user = approval_resolution["approver_user"]
            approval_rule = approval_resolution["approval_rule"]
            approval_required = approval_resolution["approval_required"]
            approval_cost_rule = approval_resolution["approval_cost_rule"]

            approval_vals = {
                "x_psm_0502_approval_required": approval_required,
                "x_psm_0502_approval_user_id": approver_user.id if approver_user else False,
                "x_psm_0502_approval_rule": approval_rule,
                "x_psm_0502_approval_cost_rule": approval_cost_rule,
                "x_psm_0502_approval_flow_type": approval_resolution["flow_type"],
                "x_psm_0502_approval_level_count": approval_resolution["level_count"],
                "x_psm_0502_approval_current_level": 1 if approval_required else approval_resolution["level_count"],
                "x_psm_0502_approval_initial_user_id": approver_user.id if approver_user else False,
                "x_psm_0502_approval_final_user_id": approval_resolution["final_approver_user"].id if approval_resolution["final_approver_user"] else False,
                "x_psm_0502_approval_first_decided_by_id": False,
                "x_psm_0502_approval_first_decided_at": False,
            }

            if approval_required:
                approval_vals.update({
                    "x_psm_0502_approval_status": "pending",
                    "x_psm_0502_approval_decided_by_id": False,
                    "x_psm_0502_approval_decided_at": False,
                })
            else:
                approval_vals.update({
                    "x_psm_0502_approval_status": "approved",
                    "x_psm_0502_approval_decided_by_id": self.env.user.id,
                    "x_psm_0502_approval_decided_at": fields.Datetime.now(),
                })

                if not record.x_psm_0502_approval_note:
                    approval_vals["x_psm_0502_approval_note"] = (
                        "Auto approved because the estimated cost is within the team auto approve limit."
                    )

            record.write(approval_vals)

    # ham danh dau cua hang da duyet de xuat timeline/cost trong phase 1
    def action_psm_approve_proposal(self):
        self._psm_ensure_proposal_approval_group()
        for record in self:
            if record.x_psm_0502_approval_status != "pending":
                raise UserError("Only requests waiting for approval can be approved.")

            if record.x_psm_0502_approval_user_id and record.x_psm_0502_approval_user_id != self.env.user:
                raise UserError("Only the configured proposal approver can approve this request.")

            if (
                record.x_psm_0502_approval_flow_type == "two_level"
                and record.x_psm_0502_approval_current_level == 1
                and record.x_psm_0502_approval_final_user_id
            ):
                record.write({
                    "x_psm_0502_approval_status": "pending",
                    "x_psm_0502_approval_user_id": record.x_psm_0502_approval_final_user_id.id,
                    "x_psm_0502_approval_rule": "store_final_approver",
                    "x_psm_0502_approval_current_level": 2,
                    "x_psm_0502_approval_first_decided_by_id": self.env.user.id,
                    "x_psm_0502_approval_first_decided_at": fields.Datetime.now(),
                })
                continue

            record.write({
                "x_psm_0502_approval_status": "approved",
                "x_psm_0502_approval_decided_by_id": self.env.user.id,
                "x_psm_0502_approval_decided_at": fields.Datetime.now(),
                "x_psm_0502_approval_current_level": record.x_psm_0502_approval_level_count or 1,
            })

    # ham danh dau cua hang tu choi de xuat timeline/cost trong phase 1
    def action_psm_reject_proposal(self):
        self._psm_ensure_proposal_approval_group()
        for record in self:
            if record.x_psm_0502_approval_status != "pending":
                raise UserError("Only requests waiting for approval can be rejected.")

            if record.x_psm_0502_approval_user_id and record.x_psm_0502_approval_user_id != self.env.user:
                raise UserError("Only the configured proposal approver can reject this request.")

            record.write({
                "x_psm_0502_approval_status": "rejected",
                "x_psm_0502_approval_decided_by_id": self.env.user.id,
                "x_psm_0502_approval_decided_at": fields.Datetime.now(),
            })

    # ham danh dau da tham dinh viec xu ly noi bo hay can thue ngoai sau buoc duyet
    # phase 1 chi can xac dinh nhanh luong noi bo/ngoai dich vu, chua dung full outside service flow
    def action_psm_mark_service_assessed(self):
        # cho phep goi action tren nhieu record de danh dau da tham dinh dich vu cho tung request, nhung chi khi tat ca record duoc chon deu o trang thai approved thi moi duoc danh dau da tham dinh dich vu
        for record in self:
            if record.x_psm_0502_service_assessed_at:
                if record.x_psm_0502_service_route == "outside_service":
                    record._psm_create_outside_service_request_if_needed()
                continue

            # neu de xuat chua duoc duyet thi khong the danh dau da tham dinh dich vu duoc
            if record.x_psm_0502_approval_status != "approved":
                raise UserError("Please approve the proposal before assessing whether outside service is needed.")

            missing_labels = []

            if not record.x_psm_0502_service_route:
                missing_labels.append("Service Route")

            if not record.x_psm_0502_service_route_reason:
                missing_labels.append("Service Route Reason")

            if missing_labels:
                raise UserError(
                    "Please complete the structured service assessment fields before marking this request as service assessed: %s"
                    % ", ".join(missing_labels)
                )

            # ai la nguoi thuc hien tham dinh va vao luc nao
            record.write({
                "x_psm_0502_need_outside_service": record.x_psm_0502_service_route == "outside_service",
                "x_psm_0502_service_assessed_by_id": self.env.user.id,
                "x_psm_0502_service_assessed_at": fields.Datetime.now(),
            })
            if record.x_psm_0502_service_route == "outside_service":
                record._psm_create_outside_service_request_if_needed()

    def _psm_create_outside_service_request_if_needed(self):
        self.ensure_one()

        active_outside_request = self.x_psm_0502_outside_service_request_ids.filtered(
            lambda outside_request: outside_request.x_psm_state != "cancelled"
        )[:1]
        if active_outside_request:
            return active_outside_request

        service_scope_parts = []
        if self.x_psm_0502_service_assessment_note:
            service_scope_parts.append(self.x_psm_0502_service_assessment_note.strip())
        if self.x_psm_0502_treatment_proposal:
            service_scope_parts.append(self.x_psm_0502_treatment_proposal.strip())
        if self.x_psm_0502_technical_solution:
            service_scope_parts.append("Technical Solution:\n%s" % self.x_psm_0502_technical_solution.strip())

        return self.env["x_psm_outside_service_request"].create({
            "x_psm_request_id": self.id,
            "x_psm_vendor_id": self.maintenance_team_id.x_psm_0502_default_vendor_id.id or False,
            "x_psm_service_type": "inspection" if self.x_psm_0502_request_type_id.code == "inspection" else "repair",
            "x_psm_expected_complete_date": self.schedule_end.date() if self.schedule_end else False,
            "x_psm_scope_of_work": "\n\n".join(service_scope_parts) or False,
        })

    def action_psm_open_outside_service_request(self):
        self.ensure_one()

        outside_requests = self.x_psm_0502_outside_service_request_ids.sorted(
            key=lambda outside_request: ((outside_request.create_date or fields.Datetime.now()), outside_request.id),
            reverse=True,
        )
        if not outside_requests:
            raise UserError("No outside service request has been created for this maintenance request yet.")

        if len(outside_requests) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "0502 Outside Service Request",
                "res_model": "x_psm_outside_service_request",
                "view_mode": "form",
                "res_id": outside_requests.id,
                "target": "current",
            }

        return {
            "type": "ir.actions.act_window",
            "name": "0502 Outside Service Requests",
            "res_model": "x_psm_outside_service_request",
            "view_mode": "list,form",
            "domain": [("id", "in", outside_requests.ids)],
            "target": "current",
            "context": {
                "default_x_psm_request_id": self.id,
            },
        }

    # ham danh dau request da duoc xac dinh co phat sinh vat tu hay khong
    # buoc 14 chi dung de re nhanh luong kho, chua tao chung tu xuat kho o day
    def action_psm_mark_material_checked(self):
        for record in self:
            if record.x_psm_0502_material_checked_at:
                continue

            # request da can dich vu ngoai thi khong nen di tiep nhanh vat tu noi bo
            if record.x_psm_0502_need_outside_service:
                raise UserError("Requests marked as Need Outside Service should not continue to the internal material assessment step.")

            # buoc 14 chi nen xu ly sau khi buoc 13 da tham dinh xong
            if not record.x_psm_0502_service_assessed_at:
                raise UserError("Please complete the service assessment before checking whether material is needed.")

            record._psm_validate_material_assessment_inputs()

            record.write({
                "x_psm_0502_material_checked_by_id": self.env.user.id,
                "x_psm_0502_material_checked_at": fields.Datetime.now(),
            })

    # ham tao phieu kho noi bo toi thieu tu maintenance request cho buoc 15
    # phase 1 chi can tao duoc stock picking draft va lien ket voi request, chua bat buoc co dong vat tu ngay tai buoc nay
    def action_psm_create_stock_picking(self):
        self.ensure_one()

        # neu request da co phieu kho roi thi mo lai de tranh tao trung
        if self.x_psm_0502_stock_picking_id:
            return self.action_psm_open_stock_picking()

        # chi tao phieu kho khi request da xac dinh co phat sinh vat tu
        if not self.x_psm_0502_material_checked_at:
            raise UserError("Please complete the material assessment before creating a stock picking.")
        if not self.x_psm_0502_has_material_request:
            raise UserError("This request is marked as not requiring material, so no stock picking should be created.")
        self._psm_validate_material_assessment_inputs()

        stock_flow = self._psm_get_material_stock_flow_resolution()
        internal_picking_type = stock_flow["picking_type"]
        source_location = stock_flow["source_location"]
        destination_location = stock_flow["destination_location"]

        material_move_commands = []
        for material_line in self.x_psm_0502_material_line_ids:
            material_move_commands.append(Command.create({
                "product_id": material_line.x_psm_product_id.id,
                "product_uom_qty": material_line.x_psm_estimated_qty,
                "product_uom": material_line.x_psm_uom_id.id or material_line.x_psm_product_id.uom_id.id,
                "location_id": source_location.id,
                "location_dest_id": destination_location.id,
                "origin": self.name,
                "description_picking_manual": material_line.x_psm_note or material_line.x_psm_product_id.display_name,
            }))

        # fallback customer/contact tu phong ban cua hang neu co
        department_partner = self.x_psm_0502_department_id.x_psm_0502_partner_id

        # ghi chu kho o muc toi thieu de doi kho/coordinator biet request nao dang can vat tu
        picking_note = self.x_psm_0502_material_assessment_note or self.x_psm_0502_treatment_proposal or False

        # tao phieu kho draft va sinh san dong vat tu tu noi dung material assessment cua buoc 14
        stock_picking = self.env["stock.picking"].create({
            "picking_type_id": internal_picking_type.id,
            "location_id": source_location.id,
            "location_dest_id": destination_location.id,
            "scheduled_date": self.schedule_date or fields.Datetime.now(),
            "origin": self.name,
            "partner_id": department_partner.id if department_partner else False,
            "note": picking_note,
            "company_id": self.company_id.id,
            "x_psm_0502_request_id": self.id,
            "move_ids": material_move_commands,
        })

        # luu lien ket nguoc lai tren request de mo lai va theo doi de dang hon
        self.write({
            "x_psm_0502_stock_picking_id": stock_picking.id,
        })
        return self.action_psm_open_stock_picking()

    # ham kiem tra ton kho vat tu dua tren stock picking da tao o buoc 15
    # phase 1 tan dung logic confirm + reserve san co cua module stock
    def action_psm_check_stock_availability(self):
        # chi xu ly mot request de dam bao kiem tra ton kho dung voi phieu kho lien ket voi request hien tai
        self.ensure_one()

        # phai co phieu kho vat tu truoc khi kiem tra ton
        if not self.x_psm_0502_stock_picking_id:
            raise UserError("Please create a stock picking before checking stock availability.")
        # buoc 16 chi nen xu ly khi buoc 14 da xong va request da duoc danh dau co phat sinh vat tu, tranh truong hop chua danh dau co phat sinh vat tu ma da tao phieu kho roi check ton
        if not self.x_psm_0502_has_material_request:
            raise UserError("This request is marked as not requiring material, so no stock availability check is needed.")

        # lay phieu kho lien ket voi request hien tai de thuc hien cac buoc tiep theo
        picking = self.x_psm_0502_stock_picking_id

        # buoc 16 can co dong vat tu va demand toi thieu de stock co co so check availability (san co)
        # kiem tra xem trong phieu kho co it nhat mot san pham co so luong yeu cau > 0 hay khong
        # neu khong thi bao loi cho nguoi dung biet phai them dong vat tu co demand vao phieu kho truoc
        # picking : record cua model stock.picking
        # move_ids : danh sach cac dong vat tu trong phieu kho, lien ket one2many tu stock.picking -> stock.move
        moves_to_check = picking.move_ids.filtered(lambda move: move.product_uom_qty > 0)
        if not moves_to_check:
            raise UserError("Please add at least one product with demand on the stock picking before checking availability.")

        # neu phieu kho con o draft thi dua sang confirmed truoc khi reserve ton
        if picking.state == "draft":
            # method action_confirm la method co san cua model stock.picking, dung de chuyen phieu kho tu draft sang confirmed
            picking.action_confirm()

        # reserve ton theo logic chuan cua stock de Odoo tu danh gia available / not available
        if picking.state not in ("done", "cancel"):
            # method action_assign la method co san cua model stock.picking, dung de reserve ton cho cac dong vat tu trong phieu kho
            picking.action_assign()

        # buoc 16 cua phase 2 luu ro 2 lop thong tin:
        # - availability hien tai: related truc tiep tu stock.picking
        # - checked availability: snapshot tai thoi diem user bam check
        stock_check_snapshot_values = self._psm_get_stock_check_snapshot_values(picking)

        # update du lieu cho maintenance request sau khi kiem tra ton kho xong
        self.write({
            **stock_check_snapshot_values,
            "x_psm_0502_stock_checked_by_id": self.env.user.id,
            "x_psm_0502_stock_checked_at": fields.Datetime.now(),
        })

    # ham gui nhanh vat tu sang trang thai cho CMT Lead duyet truoc khi xuat kho
    # phase 1 chi can diem quyet dinh toi thieu cho nhanh xuat vat tu, chua tach approval module rieng
    def action_psm_submit_material_approval(self):
        for record in self:
            # buoc 17 chi co y nghia khi request da di qua nhanh vat tu noi bo
            if not record.x_psm_0502_has_material_request:
                raise UserError("This request is marked as not requiring material, so no material approval is needed.")
            if record.x_psm_0502_need_outside_service:
                raise UserError("Requests marked as Need Outside Service should not continue to the internal material approval step.")

            # phai kiem tra ton kho xong va da co ket qua co ton moi duoc gui duyet xuat kho
            if not record.x_psm_0502_stock_picking_id or not record.x_psm_0502_stock_checked_at:
                raise UserError("Please complete stock availability checking before submitting material approval.")
            if record.x_psm_0502_stock_check_result != "available":
                raise UserError("Only requests with Stock Available can be submitted for material approval.")
            record._psm_validate_material_assessment_inputs()

            approver_user, approval_rule, approval_required, approval_value_rule, estimated_material_value = (
                record._psm_get_material_approval_resolution()
            )

            material_approval_vals = {
                "x_psm_0502_material_approval_required": approval_required,
                "x_psm_0502_material_approval_user_id": approver_user.id if approver_user else False,
                "x_psm_0502_material_approval_rule": approval_rule,
                "x_psm_0502_material_approval_value_rule": approval_value_rule,
                "x_psm_0502_material_approval_value": estimated_material_value,
            }

            if approval_required:
                material_approval_vals.update({
                    "x_psm_0502_material_approval_status": "pending",
                    "x_psm_0502_material_approval_decided_by_id": False,
                    "x_psm_0502_material_approval_decided_at": False,
                })
            else:
                material_approval_vals.update({
                    "x_psm_0502_material_approval_status": "approved",
                    "x_psm_0502_material_approval_decided_by_id": self.env.user.id,
                    "x_psm_0502_material_approval_decided_at": fields.Datetime.now(),
                })
                if not record.x_psm_0502_material_approval_note:
                    material_approval_vals["x_psm_0502_material_approval_note"] = (
                        "Automatically approved because the estimated material value is within the configured team limit."
                    )

            record.write(material_approval_vals)

    # ham danh dau CMT Lead da duyet nhanh xuat vat tu
    def action_psm_approve_material_request(self):
        self._psm_ensure_material_approval_group()
        for record in self:
            if record.x_psm_0502_material_approval_status != "pending":
                raise UserError("Only requests waiting for material approval can be approved.")
            if (
                record.x_psm_0502_material_approval_user_id
                and record.x_psm_0502_material_approval_user_id != self.env.user
            ):
                raise UserError("Only the resolved material approver can approve this material issue request.")

            record.write({
                "x_psm_0502_material_approval_status": "approved",
                "x_psm_0502_material_approval_decided_by_id": self.env.user.id,
                "x_psm_0502_material_approval_decided_at": fields.Datetime.now(),
            })

    # ham danh dau CMT Lead tu choi nhanh xuat vat tu
    def action_psm_reject_material_request(self):
        self._psm_ensure_material_approval_group()
        for record in self:
            if record.x_psm_0502_material_approval_status != "pending":
                raise UserError("Only requests waiting for material approval can be rejected.")
            if (
                record.x_psm_0502_material_approval_user_id
                and record.x_psm_0502_material_approval_user_id != self.env.user
            ):
                raise UserError("Only the resolved material approver can reject this material issue request.")

            record.write({
                "x_psm_0502_material_approval_status": "rejected",
                "x_psm_0502_material_approval_decided_by_id": self.env.user.id,
                "x_psm_0502_material_approval_decided_at": fields.Datetime.now(),
            })

    # ham goi flow validate picking chuan cua Odoo de thuc hien xuat kho thuc te
    # phase 1 uu tien tan dung button_validate cua stock.picking, tranh custom sau vao nghiep vu kho
    def action_psm_validate_stock_picking(self):
        # chi xu ly mot request
        self.ensure_one()

        if not self.x_psm_0502_stock_picking_id:
            raise UserError("No stock picking has been created for this request yet.")
        if self.x_psm_0502_material_approval_status != "approved":
            raise UserError("Please approve the material request before validating stock issue.")

        picking = self.x_psm_0502_stock_picking_id

        if picking.state == "cancel":
            raise UserError("The linked stock picking has been cancelled.")
        if picking.state == "done":
            self.write(self._psm_get_stock_issue_sync_values(picking))
            return self.action_psm_open_stock_picking()

        move_lines = picking.move_ids.filtered(lambda move: move.product_uom_qty > 0)
        if not move_lines:
            raise UserError("Please add at least one stock move with Demand greater than zero before validating stock issue.")

        # neu picking con draft thi dua ve flow kho chuan truoc khi validate
        if picking.state == "draft":
            picking.action_confirm()

        validate_result = picking.button_validate()

        # dong bo business status cua nhanh xuat kho ve maintenance request sau moi lan validate
        # neu validate xong ma Odoo mo wizard rieng thi request van co dau vet sync de user thay duoc picking chua sang done
        self.write(self._psm_get_stock_issue_sync_values(picking))

        return validate_result or self.action_psm_open_stock_picking()

    # ham chot dau vet request da xuat kho xong sau khi stock.picking da di vao state done
    # ham nay dung cho truong hop flow kho chuan mo wizard rieng va request can cap nhat lai dau vet buoc 18 sau do
    def action_psm_mark_stock_issued(self):
        for record in self:
            if record.x_psm_0502_stock_issued_at:
                continue

            if not record.x_psm_0502_stock_picking_id:
                raise UserError("No stock picking has been created for this request yet.")
            if record.x_psm_0502_stock_picking_id.state != "done":
                raise UserError("Only requests whose linked stock picking is Done can be marked as stock issued.")

            record.write(record._psm_get_stock_issue_sync_values(record.x_psm_0502_stock_picking_id))

    # ham build RFQ suggestion cho nhanh mua ngoai dua tren material lines da co cau truc
    # phase 2 buoc 19 van mo form purchase.order chuan, nhung prefill du lieu de user khong phai nhap lai tu dau
    def _psm_get_purchase_order_resolution(self):
        self.ensure_one()

        self._psm_validate_material_assessment_inputs()

        non_purchaseable_lines = self.x_psm_0502_material_line_ids.filtered(
            lambda line: not line.x_psm_product_id.purchase_ok
        )
        if non_purchaseable_lines:
            raise UserError(
                "Please enable Purchase on these materials before creating an RFQ: %s"
                % ", ".join(non_purchaseable_lines.mapped("x_psm_product_id.display_name"))
            )

        suggested_vendor = self.maintenance_team_id.x_psm_0502_default_vendor_id
        expected_arrival = self.schedule_date or fields.Datetime.now()
        purchase_priority = "1" if self.x_psm_0502_inspection_action_urgency == "immediate" else "0"

        order_line_commands = []
        for material_line in self.x_psm_0502_material_line_ids:
            line_description_parts = [material_line.x_psm_product_id.display_name]
            if material_line.x_psm_note:
                line_description_parts.append(material_line.x_psm_note)

            order_line_commands.append((0, 0, {
                "product_id": material_line.x_psm_product_id.id,
                "product_qty": material_line.x_psm_estimated_qty,
                "product_uom_id": (
                    material_line.x_psm_product_id.uom_po_id.id
                    or material_line.x_psm_uom_id.id
                    or material_line.x_psm_product_id.uom_id.id
                ),
                "date_planned": expected_arrival,
                "name": " - ".join(line_description_parts),
            }))

        summary_lines = [
            "<p><strong>0502 Outside Purchase Context</strong></p>",
            "<p><strong>Maintenance Request:</strong> %s</p>" % self.display_name,
        ]
        if self.x_psm_0502_department_id:
            summary_lines.append("<p><strong>Store Department:</strong> %s</p>" % self.x_psm_0502_department_id.display_name)
        if self.x_psm_0502_request_type_id:
            summary_lines.append("<p><strong>Request Type:</strong> %s</p>" % self.x_psm_0502_request_type_id.display_name)
        if self.x_psm_0502_source_system:
            summary_lines.append("<p><strong>Source System:</strong> %s</p>" % dict(self._fields["x_psm_0502_source_system"].selection).get(self.x_psm_0502_source_system, self.x_psm_0502_source_system))
        if self.x_psm_0502_stock_check_result:
            summary_lines.append("<p><strong>Stock Check Result:</strong> %s</p>" % dict(self._fields["x_psm_0502_stock_check_result"].selection).get(self.x_psm_0502_stock_check_result, self.x_psm_0502_stock_check_result))
        if self.x_psm_0502_treatment_proposal:
            summary_lines.append("<p><strong>Proposal Summary:</strong> %s</p>" % self.x_psm_0502_treatment_proposal)

        return {
            "suggested_vendor": suggested_vendor,
            "vendor_rule": "team_default_vendor" if suggested_vendor else "no_default_vendor",
            "expected_arrival": expected_arrival,
            "purchase_priority": purchase_priority,
            "order_line_commands": order_line_commands,
            "summary_note": "".join(summary_lines),
        }

    # ham mo man hinh RFQ/PO de xu ly nhanh mua ngoai khi kho khong du ton
    # phase 1 uu tien tan dung purchase.order co san, chi mo form RFQ voi context co san tu request
    def action_psm_create_purchase_order(self):
        self.ensure_one()

        if not self.x_psm_0502_has_material_request:
            raise UserError("This request is marked as not requiring material, so no purchase order is needed.")
        if self.x_psm_0502_need_outside_service:
            raise UserError("Requests marked as Need Outside Service should not continue to the internal material purchase step.")
        if not self.x_psm_0502_stock_checked_at:
            raise UserError("Please complete stock availability checking before moving to outside purchase.")
        if self.x_psm_0502_stock_check_result != "not_available":
            raise UserError("Only requests with Stock Not Available should continue to outside purchase.")

        # neu request da co don mua ngoai lien ket thi uu tien mo lai don do thay vi tao moi lap tuc
        active_orders = self.x_psm_0502_purchase_order_ids.filtered(lambda order: order.state != "cancel")
        if active_orders:
            return self.action_psm_open_purchase_order()

        purchase_order_resolution = self._psm_get_purchase_order_resolution()

        return {
            "type": "ir.actions.act_window",
            "name": "0502 Purchase Order",
            "res_model": "purchase.order",
            "view_mode": "form",
            "view_id": self.env.ref("purchase.purchase_order_form").id,
            "target": "current",
            "context": {
                "default_x_psm_0502_request_id": self.id,
                "default_origin": self.name,
                "default_company_id": self.company_id.id,
                "default_user_id": self.env.user.id,
                "default_partner_id": purchase_order_resolution["suggested_vendor"].id if purchase_order_resolution["suggested_vendor"] else False,
                "default_priority": purchase_order_resolution["purchase_priority"],
                "default_date_planned": purchase_order_resolution["expected_arrival"],
                "default_order_line": purchase_order_resolution["order_line_commands"],
                "default_note": purchase_order_resolution["summary_note"],
            },
        }

    def action_psm_recheck_stock_after_purchase(self):
        self.ensure_one()

        if self.x_psm_0502_purchase_order_state not in ("purchase", "done"):
            raise UserError("Only requests with a confirmed or locked purchase order can be re-checked after purchase.")
        if self.x_psm_0502_stock_check_result != "not_available":
            raise UserError("Only requests whose previous stock check was Not Available need a post-purchase re-check.")

        return self.action_psm_check_stock_availability()

    # ham mo lai don mua ngoai da lien ket voi request 0502
    def action_psm_open_purchase_order(self):
        self.ensure_one()

        purchase_orders = self.x_psm_0502_purchase_order_ids.sorted(
            key=lambda order: ((order.create_date or fields.Datetime.now()), order.id),
            reverse=True,
        )
        if not purchase_orders:
            raise UserError("No purchase order has been linked to this request yet.")

        if len(purchase_orders) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "0502 Purchase Order",
                "res_model": "purchase.order",
                "view_mode": "form",
                "res_id": purchase_orders.id,
                "target": "current",
            }

        return {
            "type": "ir.actions.act_window",
            "name": "0502 Purchase Orders",
            "res_model": "purchase.order",
            "view_mode": "list,form",
            "views": [
                (self.env.ref("purchase.purchase_order_tree").id, "list"),
                (self.env.ref("purchase.purchase_order_form").id, "form"),
            ],
            "domain": [("id", "in", purchase_orders.ids)],
            "target": "current",
            "context": {
                "default_x_psm_0502_request_id": self.id,
            },
        }

    # ham danh dau request da duoc ky thuat vien bat dau thuc thi tren hien truong
    # buoc 20 van lay FSM task lam object thuc thi chinh, request chi luu dau vet thoi diem/noi dung tong hop
    def action_psm_mark_execution_started(self):
        for record in self:
            if record.x_psm_0502_execution_started_at:
                continue

            if not record.x_psm_0502_fsm_task_id:
                raise UserError("Please create an FSM task before marking execution as started.")
            if record.x_psm_0502_execution_completed_at:
                raise UserError("This request has already been marked as execution completed.")

            if not record.x_psm_0502_execution_started_at:
                record.write({
                    "x_psm_0502_execution_started_by_id": self.env.user.id,
                    "x_psm_0502_execution_started_at": fields.Datetime.now(),
                })

    # helper validate du lieu thuc thi tren FSM task va build execution summary de dong bo ve request
    def _psm_get_execution_summary_from_fsm_task(self, task):
        self.ensure_one()

        if not task.x_psm_0502_execution_result:
            raise UserError("Please fill in 0502 Execution Result on the linked FSM task before completing execution.")
        if not task.x_psm_0502_execution_checklist_note:
            raise UserError("Please fill in 0502 Execution Checklist on the linked FSM task before completing execution.")
        if not task.x_psm_0502_execution_worksheet_note:
            raise UserError("Please fill in 0502 Technical Worksheet on the linked FSM task before completing execution.")
        if task.x_psm_0502_time_spent_hours <= 0:
            raise UserError("Please enter 0502 Actual Time Spent (Hours) greater than 0 on the linked FSM task before completing execution.")

        execution_result_label = dict(task._fields["x_psm_0502_execution_result"].selection).get(
            task.x_psm_0502_execution_result,
            task.x_psm_0502_execution_result,
        )

        summary_sections = [
            "FSM Task Execution Result: %s" % execution_result_label,
            "Actual Time Spent (Hours): %s" % task.x_psm_0502_time_spent_hours,
            "Execution Checklist:\n%s" % task.x_psm_0502_execution_checklist_note.strip(),
            "Technical Worksheet:\n%s" % task.x_psm_0502_execution_worksheet_note.strip(),
        ]

        if task.x_psm_0502_material_used_note:
            summary_sections.append("Material Used:\n%s" % task.x_psm_0502_material_used_note.strip())
        if task.x_psm_0502_follow_up_action_note:
            summary_sections.append("Follow-up Action:\n%s" % task.x_psm_0502_follow_up_action_note.strip())

        return "\n\n".join(summary_sections)

    # ham danh dau request da hoan tat thuc thi sua chua o buoc 20
    # phase 1 yeu cau FSM task phai dong/hoan tat truoc roi moi chot execution tren request
    def action_psm_mark_execution_completed(self):
        for record in self:
            if record.x_psm_0502_execution_completed_at:
                continue

            if not record.x_psm_0502_fsm_task_id:
                raise UserError("Please create an FSM task before marking execution as completed.")
            if not record.x_psm_0502_execution_started_at:
                raise UserError("Please mark execution as started before marking it as completed.")
            if not record.x_psm_0502_fsm_is_closed:
                raise UserError("Please complete the linked FSM task before marking execution as completed.")

            execution_summary = record._psm_get_execution_summary_from_fsm_task(record.x_psm_0502_fsm_task_id)

            record.write({
                "x_psm_0502_execution_completed_by_id": self.env.user.id,
                "x_psm_0502_execution_completed_at": fields.Datetime.now(),
                "x_psm_0502_execution_note": execution_summary,
            })

    # ham ghi nhan ket qua nghiem thu sau bao tri o buoc 21
    # neu accepted thi dong request bang stage Done 0502, neu can theo doi/lam lai thi giu o Acceptance Review
    def action_psm_mark_acceptance_reviewed(self):
        done_stage = self.env.ref("M02_P0502.stage_psm_0502_done", raise_if_not_found=False)
        acceptance_stage = self.env.ref("M02_P0502.stage_psm_0502_acceptance_review", raise_if_not_found=False)

        for record in self:
            if record.x_psm_0502_acceptance_reviewed_at:
                if record.x_psm_0502_acceptance_result in ("follow_up_needed", "rework_required"):
                    raise UserError("Please reopen this request for rework before recording another acceptance review.")
                continue

            outside_service_accepted = (
                record.x_psm_0502_need_outside_service
                and record.x_psm_0502_outside_service_request_id
                and record.x_psm_0502_outside_service_request_id.x_psm_state == "accepted"
                and record.x_psm_0502_outside_service_request_id.x_psm_acceptance_result == "accepted"
            )

            if not record.x_psm_0502_execution_completed_at and not outside_service_accepted:
                raise UserError("Please complete technical execution before recording post-maintenance acceptance.")
            if not record.x_psm_0502_acceptance_result:
                raise UserError("Please select Acceptance Result before recording post-maintenance acceptance.")
            if not record.x_psm_0502_acceptance_contact_name:
                raise UserError("Please fill in Store Acceptance Contact before recording post-maintenance acceptance.")
            if not record.x_psm_0502_acceptance_contact_role:
                raise UserError("Please fill in Store Acceptance Role before recording post-maintenance acceptance.")
            if not record.x_psm_0502_acceptance_equipment_result:
                raise UserError("Please fill in Post-Maintenance Equipment Result before recording post-maintenance acceptance.")
            if not record.x_psm_0502_acceptance_note:
                raise UserError("Please fill in Acceptance Note before recording post-maintenance acceptance.")
            if record.x_psm_0502_acceptance_result in ("follow_up_needed", "rework_required") and not record.x_psm_0502_acceptance_follow_up_note:
                raise UserError("Please fill in Acceptance Follow-up Note when the acceptance result requires monitoring or rework.")

            values = {
                "x_psm_0502_acceptance_reviewed_by_id": self.env.user.id,
                "x_psm_0502_acceptance_reviewed_at": fields.Datetime.now(),
            }

            # neu cua hang chap nhan ket qua sau bao tri thi dong request ve stage Done chuan 0502
            if record.x_psm_0502_acceptance_result == "accepted":
                if not done_stage:
                    raise UserError("No 0502 Done maintenance stage was found. Please update the M02_P0502 module data first.")
                values.update({
                    "stage_id": done_stage.id,
                    "kanban_state": "done",
                })
            else:
                # truong hop can lam lai/bo sung thi giu request mo va danh dau blocked de noi bo theo doi
                if not acceptance_stage:
                    raise UserError("No 0502 Acceptance Review stage was found. Please update the M02_P0502 module data first.")
                values.update({
                    "stage_id": acceptance_stage.id,
                    "kanban_state": "blocked",
                })

            record.with_context(psm_0502_skip_stage_validation=True).write(values)

    # ham mo lai request khi nghiem thu can theo doi/lam lai, giu request goc lam truc xuyen suot
    def action_psm_reopen_for_rework(self):
        in_execution_stage = self.env.ref("M02_P0502.stage_psm_0502_in_execution", raise_if_not_found=False)
        if not in_execution_stage:
            raise UserError("No 0502 In Execution maintenance stage was found. Please update the M02_P0502 module data first.")

        now = fields.Datetime.now()
        for record in self:
            if not record.x_psm_0502_acceptance_reviewed_at:
                raise UserError("Please record an acceptance review before reopening this request for rework.")
            if record.x_psm_0502_acceptance_result not in ("follow_up_needed", "rework_required"):
                raise UserError("Only follow-up or rework acceptance results can be reopened for rework.")

            next_round = record.x_psm_0502_rework_round_count + 1
            previous_result = record.x_psm_0502_acceptance_result
            reason = record.x_psm_0502_acceptance_follow_up_note or record.x_psm_0502_acceptance_note or False
            linked_task = record.x_psm_0502_fsm_task_id

            self.env["x_psm_request_rework_history"].create({
                "x_psm_request_id": record.id,
                "x_psm_round_number": next_round,
                "x_psm_previous_acceptance_result": previous_result,
                "x_psm_rework_reason": reason,
                "x_psm_created_by_id": self.env.user.id,
                "x_psm_created_at": now,
                "x_psm_linked_fsm_task_id": linked_task.id if linked_task else False,
            })

            values = {
                "x_psm_0502_rework_round_count": next_round,
                "x_psm_0502_last_rework_at": now,
                "x_psm_0502_last_rework_by_id": self.env.user.id,
                "x_psm_0502_acceptance_result": False,
                "x_psm_0502_acceptance_contact_name": False,
                "x_psm_0502_acceptance_contact_role": False,
                "x_psm_0502_acceptance_equipment_result": False,
                "x_psm_0502_acceptance_note": False,
                "x_psm_0502_acceptance_follow_up_note": False,
                "x_psm_0502_acceptance_reviewed_by_id": False,
                "x_psm_0502_acceptance_reviewed_at": False,
                "x_psm_0502_acceptance_doc_no": False,
                "x_psm_0502_execution_started_by_id": False,
                "x_psm_0502_execution_started_at": False,
                "x_psm_0502_execution_completed_by_id": False,
                "x_psm_0502_execution_completed_at": False,
                "x_psm_0502_execution_note": False,
                "stage_id": in_execution_stage.id,
                "kanban_state": "normal",
            }

            # context nay cho phep tach vong rework sang FSM task moi neu user/business muon lam tren task rieng
            if self.env.context.get("psm_0502_create_new_fsm_task") or self.env.context.get("psm_0502_rework_create_new_fsm_task"):
                values["x_psm_0502_fsm_task_id"] = False

            record.with_context(
                psm_0502_skip_stage_validation=True,
                psm_0502_skip_stage_sync=True,
            ).write(values)

            if hasattr(record, "message_post"):
                record.message_post(
                    body="Reopened for rework round %s. Reason: %s" % (
                        next_round,
                        reason or "No reason provided.",
                    )
                )

    # ham mo lai phieu kho da tao tu request 0502
    def action_psm_open_stock_picking(self):
        self.ensure_one()

        if not self.x_psm_0502_stock_picking_id:
            raise UserError("No stock picking has been created for this request yet.")

        return {
            "type": "ir.actions.act_window",
            "name": "0502 Stock Picking",
            "res_model": "stock.picking",
            "view_mode": "form",
            "res_id": self.x_psm_0502_stock_picking_id.id,
            "target": "current",
        }

    # list field start

    # field many2one lien ket maintenance request voi model x_psm_request_source
    # de luu tru nguon request cua maintenance request
    x_psm_0502_request_source_id = fields.Many2one(
        "x_psm_request_source",
        string="Request Source",
        default=_default_x_psm_0502_request_source_id,
        tracking=True,
        ondelete="restrict",
        help="Entry point of the 0502 flow for this maintenance request.",
    )

    # luu ma nguon phat sinh de filter va domain de dang hon trong search view
    x_psm_0502_request_source_code = fields.Char(
        related="x_psm_0502_request_source_id.code",
        string="Request Source Code",
        store=True,
        index=True,
    )
    x_psm_0502_source_system = fields.Selection(
        selection=[
            ("manual_request", "Manual Request"),
            ("preventive_cron", "Preventive Cron"),
            ("helpdesk_ticket", "Helpdesk Ticket"),
            ("imported_request", "Imported Request"),
            ("other", "Other"),
        ],
        string="Source System",
        default="manual_request",
        tracking=True,
        help="Technical or upstream system origin of the maintenance request.",
    )
    x_psm_0502_request_origin_group = fields.Selection(
        selection=[
            ("store_need", "Store Need"),
            ("preventive_need", "Preventive Need"),
            ("system_need", "System Need"),
        ],
        string="Request Origin Group",
        compute="_compute_x_psm_0502_request_origin_group",
        store=True,
        index=True,
        readonly=True,
        help="Business-friendly grouping of the actual origin of the maintenance need at phase 3 step 1.",
    )
    x_psm_0502_source_reference = fields.Char(
        string="Source Reference",
        tracking=True,
        help="Reference number or upstream document code from the source system.",
    )
    x_psm_0502_source_note = fields.Text(
        string="Source Mapping Note",
        help="Additional note explaining the upstream source mapping or origin context.",
    )
    x_psm_0502_intake_minimum_ready = fields.Boolean(
        string="Intake Minimum Ready",
        compute="_compute_x_psm_0502_intake_minimum_ready_fields",
        store=True,
        readonly=True,
        help="Indicates whether the request already has the minimum source-side data expected at phase 3 step 1.",
    )
    x_psm_0502_intake_minimum_gap_reason = fields.Char(
        string="Intake Minimum Gap Reason",
        compute="_compute_x_psm_0502_intake_minimum_ready_fields",
        store=True,
        readonly=True,
        help="Missing minimum data labels that still prevent the request from being considered complete at phase 3 step 1.",
    )
    x_psm_0502_intake_template_guide = fields.Text(
        string="Intake Template Guide",
        compute="_compute_x_psm_0502_intake_template_fields",
        readonly=True,
        help="Guidance template that explains which initial questions should be captured for this request type at phase 3 step 2.",
    )
    x_psm_0502_intake_example_note = fields.Text(
        string="Intake Example Note",
        compute="_compute_x_psm_0502_intake_template_fields",
        readonly=True,
        help="Example intake note inherited from the request type to help the user capture the initial information consistently.",
    )

    # field hien thi huong dan de xuat xu ly theo request type de CMT co khung proposal ro hon o phase 3 buoc 11
    x_psm_0502_proposal_template_guide = fields.Text(
        string="Proposal Template Guide",
        compute="_compute_x_psm_0502_proposal_template_fields",
        readonly=True,
        help="Guidance template inherited from the request type to help the user structure the treatment proposal consistently.",
    )
    x_psm_0502_intake_detail_ready = fields.Boolean(
        string="Intake Detail Ready",
        compute="_compute_x_psm_0502_intake_detail_ready_fields",
        store=True,
        readonly=True,
        help="Indicates whether the request already has the richer intake information expected at phase 3 step 2.",
    )
    x_psm_0502_intake_detail_gap_reason = fields.Char(
        string="Intake Detail Gap Reason",
        compute="_compute_x_psm_0502_intake_detail_ready_fields",
        store=True,
        readonly=True,
        help="Missing labels that still block the request from being considered intake-complete at phase 3 step 2.",
    )
    x_psm_0502_intake_problem_detail = fields.Text(
        string="Intake Problem Detail",
        help="Detailed initial problem description captured at the intake stage.",
    )
    x_psm_0502_intake_impact_scope = fields.Selection(
        selection=[
            ("limited", "Limited Impact"),
            ("degraded", "Degraded Operation"),
            ("blocked", "Operation Blocked"),
        ],
        string="Intake Impact Scope",
        tracking=True,
        help="Initial business impact scope captured at the intake stage.",
    )
    x_psm_0502_intake_contact_name = fields.Char(
        string="Intake Contact Name",
        help="Primary contact person captured during the initial intake.",
    )
    x_psm_0502_intake_contact_phone = fields.Char(
        string="Intake Contact Phone",
        help="Primary contact phone captured during the initial intake.",
    )

    # field luu ma chung tu kiem tra ban dau cua request 0502
    x_psm_0502_inspection_doc_no = fields.Char(
        string="Inspection Document No.",
        readonly=True,
        copy=False,
        help="Sequence number of the 0502 initial inspection document.",
    )

    # field luu ma chung tu de xuat xu ly/bao gia so bo cua request 0502
    x_psm_0502_proposal_doc_no = fields.Char(
        string="Proposal Document No.",
        readonly=True,
        copy=False,
        help="Sequence number of the 0502 treatment proposal document.",
    )

    # field luu ma phieu yeu cau xuat vat tu cua request 0502
    x_psm_0502_material_issue_doc_no = fields.Char(
        string="Material Issue Document No.",
        readonly=True,
        copy=False,
        help="Sequence number of the 0502 material issue request document.",
    )

    # field luu ma bien ban nghiem thu cua request 0502
    x_psm_0502_acceptance_doc_no = fields.Char(
        string="Acceptance Document No.",
        readonly=True,
        copy=False,
        help="Sequence number of the 0502 acceptance record document.",
    )

    # thay vi luu ma cua hang dang text, ta lien ket truc tiep den hr.department
    # vi hien tai "store" dang duoc to chuc theo phong ban trong he thong
    # field tro toi model hr.department, de luu tru cua hang nao phat sinh maintenance request
    # string: ten hien thi tren giao dien nguoi dung
    # default: gia tri mac dinh khi tao record moi, o day la ham _default_x_psm_0502_department_id de tra ve phong ban cua employee hien tai
    # tracking: theo doi thay doi cua field trong chatter, khi field thay doi se hien thi trong log vao chatter
    # ondelete: khong cho phep xoa record ben hr.department neu con maintenance request nao lien ket den no, de tranh loi du lieu
    # help: mo ta field, hien thi khi hover chuot vao label cua field tren giao dien nguoi dung
    x_psm_0502_department_id = fields.Many2one(
        "hr.department",
        string="Store Department",
        default=_default_x_psm_0502_department_id,
        tracking=True,
        ondelete="restrict",
        help="Store department that raised the 0502 maintenance request.",
    )

    x_psm_0502_request_type_id = fields.Many2one(
        "x_psm_request_type",
        string="Request Type",
        tracking=True,
        ondelete="restrict",
        help="Business type of the 0502 maintenance request.",
    )

    # field luu user tiep nhan yeu cau bao tri, khi user nhan nut "Receive Request" thi field nay se duoc gan bang user hien tai
    x_psm_0502_received_by_id = fields.Many2one(
        "res.users",
        string="Received By (CMT)",
        tracking=True,
        readonly=True,
        copy=False,
        help="CMT user who acknowledged the maintenance request into the intake flow.",
    )

    # field luu tru thoi diem tiep nhan yeu cau bao tri
    x_psm_0502_received_at = fields.Datetime(
        string="Received At (CMT)",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the CMT intake acknowledged the maintenance request.",
    )
    x_psm_0502_intake_owner_user_id = fields.Many2one(
        "res.users",
        string="Intake Owner",
        compute="_compute_x_psm_0502_intake_owner_user_id",
        store=True,
        readonly=True,
        help="User currently considered the owner of the 0502 intake checkpoint.",
    )
    x_psm_0502_intake_sla_deadline_at = fields.Datetime(
        string="Intake SLA Deadline",
        compute="_compute_x_psm_0502_intake_sla_deadline_at",
        store=True,
        readonly=True,
        help="Deadline for the CMT intake checkpoint derived from the maintenance team SLA configuration.",
    )
    x_psm_0502_intake_sla_result = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("on_time", "On Time"),
            ("late", "Late"),
        ],
        string="Intake SLA Result",
        compute="_compute_x_psm_0502_intake_sla_result",
        store=True,
        readonly=True,
        help="Stored SLA result once the intake checkpoint has been reached.",
    )
    x_psm_0502_intake_age_hours = fields.Float(
        string="Intake Age (Hours)",
        compute="_compute_x_psm_0502_intake_age_hours",
        readonly=True,
        help="Elapsed hours from request entry into the system until CMT receives it, or until now if still pending.",
    )
    x_psm_0502_progress_checkpoint = fields.Selection(
        selection=[
            ("intake", "Intake"),
            ("inspection", "Inspection"),
            ("planning", "Planning"),
            ("proposal", "Proposal"),
            ("approval", "Approval"),
            ("service_assessment", "Service Assessment"),
            ("material_assessment", "Material Assessment"),
            ("material_approval", "Material Approval"),
            ("stock_issue", "Stock Issue"),
            ("purchase", "Purchase"),
            ("execution", "Execution"),
            ("acceptance", "Acceptance"),
            ("closed", "Closed"),
        ],
        string="Progress Checkpoint",
        compute="_compute_x_psm_0502_monitoring_status_fields",
        store=True,
        readonly=True,
        help="Operational progress checkpoint used by phase 3 monitoring to show where the request is currently bottlenecked.",
    )
    x_psm_0502_supply_branch_status = fields.Selection(
        selection=[
            ("no_material_flow", "No Material Flow"),
            ("material_assessment", "Material Assessment"),
            ("no_material_needed", "No Material Needed"),
            ("waiting_stock_check", "Waiting Stock Check"),
            ("awaiting_material_approval", "Awaiting Material Approval"),
            ("pending_stock_issue", "Pending Stock Issue"),
            ("stock_issued", "Stock Issued"),
            ("purchase_required", "Purchase Required"),
            ("purchase_in_progress", "Purchase In Progress"),
            ("purchase_confirmed", "Purchase Confirmed"),
            ("outside_service", "Outside Service"),
        ],
        string="Supply Branch Status",
        compute="_compute_x_psm_0502_monitoring_status_fields",
        store=True,
        readonly=True,
        help="Operational status of the internal material, stock issue, and outside purchase branch for phase 3 monitoring.",
    )

    # field ket luan kiem tra ban dau de phan biet co can xu ly tiep hay khong
    # khi user nhan nut "Mark as Inspected" thi field nay se duoc gan gia tri tuong ung do user chon tren popup
    x_psm_0502_inspection_result = fields.Selection(
        # giu dang Selection 2 gia tri vi nghiep vu 0502 hien chi can phan biet co/khong can xu ly
        selection=[
            ("no_action_needed", "No Action Needed"),
            ("action_needed", "Action Needed"),
        ],
        string="Initial Inspection Result",
        tracking=True,
        help="Initial on-site inspection conclusion for the 0502 flow.",
    )

    # field ghi nhan noi dung kiem tra thuc te ban dau
    x_psm_0502_inspection_note = fields.Text(
        string="Initial Inspection Note",
        help="Initial inspection findings captured by CMT.",
    )
    x_psm_0502_inspection_checklist_template = fields.Text(
        string="Inspection Checklist Template",
        compute="_compute_x_psm_0502_inspection_template_fields",
        readonly=True,
        help="Checklist template inherited from the equipment category for phase 3 step 4.",
    )
    x_psm_0502_inspection_worksheet_template = fields.Text(
        string="Inspection Worksheet Template",
        compute="_compute_x_psm_0502_inspection_template_fields",
        readonly=True,
        help="Worksheet template inherited from the equipment category for phase 3 step 4.",
    )
    x_psm_0502_inspection_checklist_result = fields.Text(
        string="Inspection Checklist Result",
        help="Actual checklist result recorded by CMT during the initial inspection.",
    )
    x_psm_0502_inspection_worksheet = fields.Text(
        string="Inspection Worksheet",
        help="Structured worksheet note recorded by CMT during the initial inspection.",
    )
    x_psm_0502_inspection_symptom_status = fields.Selection(
        selection=[
            ("confirmed", "Confirmed"),
            ("not_confirmed", "Not Confirmed"),
            ("cannot_verify", "Cannot Verify Yet"),
        ],
        string="Symptom Status",
        tracking=True,
        help="Structured result describing whether the reported symptom was confirmed on site.",
    )
    x_psm_0502_inspection_equipment_status = fields.Selection(
        selection=[
            ("running", "Running"),
            ("degraded", "Running with Issue"),
            ("stopped", "Stopped"),
        ],
        string="Equipment Status",
        tracking=True,
        help="Operational status of the equipment at the time of the initial inspection.",
    )
    x_psm_0502_inspection_safety_risk = fields.Selection(
        selection=[
            ("none", "No Safety Risk"),
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Safety Risk Level",
        tracking=True,
        help="Safety risk level assessed during the initial inspection.",
    )
    x_psm_0502_inspection_action_urgency = fields.Selection(
        selection=[
            ("normal", "Normal"),
            ("urgent", "Urgent"),
            ("immediate", "Immediate"),
        ],
        string="Action Urgency",
        tracking=True,
        help="Urgency level for the follow-up action after the initial inspection.",
    )

    # field luu user thuc hien kiem tra thuc te ban dau
    x_psm_0502_inspected_by_id = fields.Many2one(
        "res.users",
        string="Inspected By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who performed the initial inspection.",
    )

    # field luu thoi diem kiem tra ban dau
    x_psm_0502_inspected_at = fields.Datetime(
        string="Inspected At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the initial inspection was recorded.",
    )

    # field luu user duoc xem la CMT Lead trong phase 1 va da duoc thong bao ve request preventive
    x_psm_0502_lead_notified_user_id = fields.Many2one(
        "res.users",
        string="Lead Notified User",
        tracking=True,
        readonly=True,
        copy=False,
        help="User considered as the CMT Lead for the phase 1 notification.",
    )

    # field luu rule resolve lead nao da duoc he thong su dung de gui notify preventive
    x_psm_0502_lead_notification_rule = fields.Selection(
        selection=[
            ("team_lead", "Team Lead"),
            ("team_member_fallback", "Team Member Fallback"),
            ("technician_fallback", "Technician Fallback"),
            ("current_user_fallback", "Current User Fallback"),
        ],
        string="Lead Notify Rule",
        tracking=True,
        readonly=True,
        copy=False,
        help="Resolution rule used to determine who received the 0502 preventive lead notification.",
    )

    # field luu thoi diem he thong da tao activity de CMT Lead nhin thay request preventive den han
    x_psm_0502_lead_notified_at = fields.Datetime(
        string="Lead Notified At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the preventive request was surfaced to the CMT Lead.",
    )
    x_psm_0502_lead_acknowledgment_status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("acknowledged", "Acknowledged"),
        ],
        string="Lead Acknowledgment Status",
        tracking=True,
        readonly=True,
        copy=False,
        help="Shows whether the notified lead has acknowledged the preventive assignment.",
    )
    x_psm_0502_lead_acknowledged_by_id = fields.Many2one(
        "res.users",
        string="Lead Acknowledged By",
        tracking=True,
        readonly=True,
        copy=False,
        help="Lead user who acknowledged the preventive assignment.",
    )
    x_psm_0502_lead_acknowledged_at = fields.Datetime(
        string="Lead Acknowledged At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the notified lead acknowledged the preventive assignment.",
    )

    # field ghi nhan ghi chu lap ke hoach xu ly o muc don gian cho phase 1
    # field dang text de de dang ghi chu va mo rong them noi dung khac trong tuong lai neu can, khong gioi han so luong ky tu
    x_psm_0502_plan_note = fields.Text(
        string="Planning Note",
        help="Simple planning note for phase 1 before introducing a full planning flow.",
    )

    # field ghi nhan ly do doi lich / re-plan de phase 3 co audit trail toi thieu ma khong can planning module rieng
    x_psm_0502_plan_change_reason = fields.Text(
        string="Planning Change Reason",
        help="Reason entered when a planned schedule or responsible user is changed in phase 3.",
    )

    # field cho biet request da du dieu kien nghiep vu de lap ke hoach hay chua
    x_psm_0502_ready_to_plan = fields.Boolean(
        string="Ready To Plan",
        compute="_compute_x_psm_0502_planning_ready_fields",
        store=True,
        help="Technical indicator showing whether the request is ready for the planning step.",
    )

    # field hien thi ly do nghiep vu khien request chua ready de lap ke hoach
    x_psm_0502_planning_block_reason = fields.Char(
        string="Planning Block Reason",
        compute="_compute_x_psm_0502_planning_ready_fields",
        store=True,
        help="Summary of missing business prerequisites before the request can be planned.",
    )

    # field ghi nhan ai la nguoi xac nhan da lap ke hoach cho request
    x_psm_0502_planned_by_id = fields.Many2one(
        "res.users",
        string="Planned By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who confirmed the request had been planned in phase 1.",
    )

    # field ghi nhan thoi diem xac nhan da lap ke hoach
    # field dang datetime de co the luu ca ngay va gio, de de dang theo doi va tinh toan thoi gian trong tuong lai neu can
    x_psm_0502_planned_at = fields.Datetime(
        string="Planned At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the request was marked as planned in phase 1.",
    )

    # field one2many luu lich su lap ke hoach va doi lich de phase 3 truy vet duoc cac revision quan trong
    x_psm_0502_planning_history_ids = fields.One2many(
        "x_psm_request_planning_history",
        "x_psm_request_id",
        string="Planning History",
        help="Planning history lines captured for the request when the schedule is planned or revised in phase 3.",
    )

    # field de nhin nhanh request da qua bao nhieu revision planning ma khong can mo tung dong history
    x_psm_0502_planning_revision_count = fields.Integer(
        string="Planning Revision Count",
        readonly=True,
        copy=False,
        help="Number of planning history revisions recorded for this request.",
    )

    # field ghi nhan user gan nhat da thay doi planning de lead/coordinator truy vet nhanh tren request
    x_psm_0502_last_planning_changed_by_id = fields.Many2one(
        "res.users",
        string="Last Planning Changed By",
        readonly=True,
        copy=False,
        help="Latest user who changed the planning revision of this request.",
    )

    # field ghi nhan thoi diem gan nhat da thay doi planning
    x_psm_0502_last_planning_changed_at = fields.Datetime(
        string="Last Planning Changed At",
        readonly=True,
        copy=False,
        help="Latest date and time when the planning revision of this request changed.",
    )

    # field luu field service task duoc tao ra tu maintenance request o buoc 9
    # phase 1 su dung project.task cua industry_fsm de giao viec cho ky thuat vien thuc thi
    x_psm_0502_fsm_task_id = fields.Many2one(
        "project.task",
        string="FSM Task",
        tracking=True,
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Field Service task created from this maintenance request in phase 1.",
    )

    # field ghi nhan phuong an xu ly hoac de xuat xu ly so bo cua CMT sau khi kiem tra thuc te
    x_psm_0502_treatment_proposal = fields.Text(
        string="Treatment Proposal",
        help="Initial treatment proposal captured in phase 1 before a formal quotation flow is introduced.",
    )

    # field luu proposal document ro hon summary de buoc 11 co artifact de xuat de gui/doi chieu ma chua can object proposal rieng
    x_psm_0502_proposal_document = fields.Text(
        string="Proposal Document",
        readonly=True,
        copy=False,
        help="Proposal document artifact generated from the structured proposal fields in phase 3.",
    )

    # field ghi nhan nguyen nhan goc duoc CMT xac dinh o muc co cau truc cho phase 2
    x_psm_0502_root_cause_analysis = fields.Text(
        string="Root Cause Analysis",
        help="Structured root cause analysis captured for the treatment proposal in phase 2.",
    )

    # field ghi nhan phuong an ky thuat de xu ly request o muc co cau truc cho phase 2
    x_psm_0502_technical_solution = fields.Text(
        string="Technical Solution",
        help="Structured technical handling proposal captured in phase 2.",
    )

    # field ghi nhan chi phi du kien o muc don gian cho phase 1
    x_psm_0502_estimated_cost = fields.Monetary(
        string="Estimated Cost",
        # field tien te de hien thi truong estimated cost theo dong tien cong ty, luon co gia tri de hien thi va tinh toan chinh xac neu can
        currency_field="x_psm_0502_currency_id",
        help="Estimated handling cost proposed by CMT in phase 1.",
    )

    # field tien te de hien thi truong estimated cost theo dong tien cong ty
    # field tro den model tien te de lay ra dong tien cua cong ty
    x_psm_0502_currency_id = fields.Many2one(
        "res.currency",
        # related field
        # gia tri cua field x_psm_0502_currency_id se duoc lay tu currency_id cua company, vi company_id la field many2one da co san trong maintenance.request lien ket den res.company
        related="company_id.currency_id",
        string="Currency",
        store=True,
        readonly=True,
    )

    # field ghi nhan timeline xu ly du kien o dang ghi chu ngan gon cho phase 1
    # time line du kien se duoc ghi chu don gian
    x_psm_0502_estimated_timeline = fields.Char(
        string="Estimated Timeline",
        help="Estimated handling timeline captured in phase 1.",
    )

    # field ghi chu bo sung cho cac gia dinh va cach tinh phan chi phi de xuat
    x_psm_0502_cost_note = fields.Text(
        string="Cost Note",
        help="Structured note explaining the cost assumptions or breakdown in phase 2.",
    )

    # field ghi chu bo sung cho timeline de xuat o muc co cau truc
    x_psm_0502_timeline_note = fields.Text(
        string="Timeline Note",
        help="Structured note explaining the proposed handling timeline in phase 2.",
    )

    # field ghi nhan ly do doi de xuat sau khi request da duoc danh dau proposed
    x_psm_0502_proposal_change_reason = fields.Text(
        string="Proposal Change Reason",
        help="Reason entered when a proposed treatment proposal is revised in phase 3.",
    )

    # field ghi nhan ai la nguoi da chot de xuat xu ly/bang gia so bo
    # field many2one tro den res.users de luu tru thong tin ai la nguoi da chot de xuat xu ly, de de dang theo doi va hien thi trong chatter
    x_psm_0502_proposed_by_id = fields.Many2one(
        "res.users",
        string="Proposed By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who confirmed the treatment proposal in phase 1.",
    )

    # field ghi nhan thoi diem da chot de xuat xu ly/bang gia so bo
    x_psm_0502_proposed_at = fields.Datetime(
        string="Proposed At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the treatment proposal was recorded in phase 1.",
    )

    # field one2many luu lich su initial proposal va cac lan reproposal de buoc 11 co audit trail ro hon
    x_psm_0502_proposal_history_ids = fields.One2many(
        "x_psm_request_proposal_history",
        "x_psm_request_id",
        string="Proposal History",
        help="Proposal history lines captured when the request is first proposed or later revised in phase 3.",
    )

    # field de nhin nhanh request da co bao nhieu revision proposal
    x_psm_0502_proposal_revision_count = fields.Integer(
        string="Proposal Revision Count",
        readonly=True,
        copy=False,
        help="Number of proposal history revisions recorded for this request.",
    )

    # field ghi nhan user gan nhat da thay doi proposal
    x_psm_0502_last_proposal_changed_by_id = fields.Many2one(
        "res.users",
        string="Last Proposal Changed By",
        readonly=True,
        copy=False,
        help="Latest user who changed the proposal revision of this request.",
    )

    # field ghi nhan thoi diem gan nhat proposal bi thay doi
    x_psm_0502_last_proposal_changed_at = fields.Datetime(
        string="Last Proposal Changed At",
        readonly=True,
        copy=False,
        help="Latest date and time when the proposal revision of this request changed.",
    )

    # field tom tat so sanh revision proposal gan nhat so voi revision truoc de user nhin nhanh tren form
    x_psm_0502_proposal_revision_compare = fields.Text(
        string="Proposal Revision Compare",
        compute="_compute_x_psm_0502_proposal_revision_compare",
        readonly=True,
        help="Quick comparison summary between the latest proposal revision and the previous one.",
    )

    # field trang thai duyet toi thieu cua buoc 12
    x_psm_0502_approval_status = fields.Selection(
        selection=[
            ("pending", "Pending Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Approval Status",
        tracking=True,
        copy=False,
        help="Simple approval decision for timeline and estimated cost in phase 1.",
    )

    # field ghi nhan request nay co can duyet thu cong hay duoc auto approve theo nguong chi phi
    x_psm_0502_approval_required = fields.Boolean(
        string="Approval Required",
        tracking=True,
        copy=False,
        help="Indicates whether the treatment proposal requires manual approval after applying the phase 2 cost rule.",
    )

    # field ghi nhan user duoc resolve de dong vai tro nguoi duyet de xuat
    x_psm_0502_approval_user_id = fields.Many2one(
        "res.users",
        string="Proposal Approver",
        tracking=True,
        readonly=True,
        copy=False,
        help="Resolved approver for the treatment proposal in phase 2.",
    )

    # field ghi nhan rule resolve approver duoc ap dung
    x_psm_0502_approval_rule = fields.Selection(
        selection=[
            ("store_approver", "Store Approver"),
            ("store_final_approver", "Store Final Approver"),
            ("team_approver", "Team Approver"),
            ("team_lead_fallback", "Team Lead Fallback"),
            ("team_member_fallback", "Team Member Fallback"),
            ("technician_fallback", "Technician Fallback"),
            ("current_user_fallback", "Current User Fallback"),
        ],
        string="Approval Rule",
        tracking=True,
        readonly=True,
        copy=False,
        help="Resolver rule used to determine who approves the treatment proposal in phase 2.",
    )

    # field ghi nhan rule chi phi duoc ap dung cho buoc duyet
    x_psm_0502_approval_cost_rule = fields.Selection(
        selection=[
            ("manual_review_required", "Manual Review Required"),
            ("auto_approved_under_limit", "Auto Approved Under Limit"),
        ],
        string="Approval Cost Rule",
        tracking=True,
        readonly=True,
        copy=False,
        help="Cost rule applied when the treatment proposal enters the approval step in phase 2.",
    )

    # field ghi nhan ai la nguoi dua ra quyet dinh approved/rejected
    x_psm_0502_approval_decided_by_id = fields.Many2one(
        "res.users",
        string="Approval Decided By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who made the phase 1 approval decision.",
    )

    # field ghi nhan thoi diem dua ra quyet dinh approved/rejected
    x_psm_0502_approval_decided_at = fields.Datetime(
        string="Approval Decided At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the phase 1 approval decision was recorded.",
    )

    # field ghi chu bo sung cua cua hang cho quyet dinh duyet/tu choi
    x_psm_0502_approval_note = fields.Text(
        string="Approval Note",
        help="Simple note captured for the approval or rejection decision in phase 1.",
    )

    # field ghi nhan request dang dung 1 cap hay 2 cap duyet o buoc 12
    x_psm_0502_approval_flow_type = fields.Selection(
        selection=[
            ("single_level", "Single-Level Approval"),
            ("two_level", "Two-Level Approval"),
        ],
        string="Approval Flow Type",
        tracking=True,
        readonly=True,
        copy=False,
        help="Indicates whether the proposal follows a single-level or two-level approval flow in phase 3 step 12.",
    )

    # field ghi nhan tong so cap duyet da duoc resolve cho request nay
    x_psm_0502_approval_level_count = fields.Integer(
        string="Approval Level Count",
        tracking=True,
        readonly=True,
        copy=False,
        help="Total number of approval levels resolved for this proposal.",
    )

    # field ghi nhan request dang cho duyet o cap nao
    x_psm_0502_approval_current_level = fields.Integer(
        string="Current Approval Level",
        tracking=True,
        readonly=True,
        copy=False,
        help="Current active approval level for the proposal while it is pending.",
    )

    # field luu approver cap dau de giu audit khi request chuyen sang cap duyet cuoi
    x_psm_0502_approval_initial_user_id = fields.Many2one(
        "res.users",
        string="Initial Proposal Approver",
        tracking=True,
        readonly=True,
        copy=False,
        help="First-level approver resolved when the proposal is first submitted for approval.",
    )

    # field luu approver cap cuoi neu request dung 2 cap duyet
    x_psm_0502_approval_final_user_id = fields.Many2one(
        "res.users",
        string="Final Proposal Approver",
        tracking=True,
        readonly=True,
        copy=False,
        help="Second-level final approver when the store side requires two-level approval for the proposal.",
    )

    # field ghi nhan ai da approve cap dau neu request co 2 cap duyet
    x_psm_0502_approval_first_decided_by_id = fields.Many2one(
        "res.users",
        string="First Approval Decided By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who completed the first approval level before the request moved to the final approver.",
    )

    # field ghi nhan thoi diem approve cap dau
    x_psm_0502_approval_first_decided_at = fields.Datetime(
        string="First Approval Decided At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the first approval level was completed.",
    )

    # field co xac dinh request nay can xu ly bang dich vu ngoai hay khong
    x_psm_0502_need_outside_service = fields.Boolean(
        string="Need Outside Service",
        tracking=True,
        help="Indicates whether the request should branch to outside service instead of internal handling.",
    )

    # field co cau truc de xac dinh request se di nhanh xu ly noi bo hay dich vu ngoai
    x_psm_0502_service_route = fields.Selection(
        selection=[
            ("internal_handling", "Internal Handling"),
            ("outside_service", "Outside Service"),
        ],
        string="Service Route",
        tracking=True,
        help="Structured routing decision used in phase 2 to clarify whether the request stays internal or goes to outside service.",
    )

    # field ghi nhan ly do nghiep vu/chuyen mon cua quyet dinh route service
    x_psm_0502_service_route_reason = fields.Selection(
        selection=[
            ("internal_capable", "Internal Team Capable"),
            ("specialist_required", "Specialist Required"),
            ("capacity_shortage", "Internal Capacity Shortage"),
            ("vendor_warranty", "Vendor / Warranty Handling"),
            ("safety_compliance", "Safety / Compliance Requirement"),
            ("other", "Other"),
        ],
        string="Service Route Reason",
        tracking=True,
        help="Structured reason explaining why the request is routed internally or to outside service.",
    )

    # field ghi chu tham dinh tai buoc 13 de giai thich ly do xu ly noi bo hoac thue ngoai
    x_psm_0502_service_assessment_note = fields.Text(
        string="Service Assessment Note",
        help="Assessment note explaining whether the request can be handled internally or requires outside service.",
    )

    # field ghi nhan ai la nguoi xac nhan ket qua tham dinh service route
    x_psm_0502_service_assessed_by_id = fields.Many2one(
        "res.users",
        string="Service Assessed By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who assessed whether outside service is needed in phase 1.",
    )

    # field ghi nhan thoi diem da tham dinh xong service route
    x_psm_0502_service_assessed_at = fields.Datetime(
        string="Service Assessed At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the internal/outside service route was assessed in phase 1.",
    )

    # field one2many luu cac yeu cau dich vu ngoai phat sinh tu request 0502 goc trong phase 3B
    x_psm_0502_outside_service_request_ids = fields.One2many(
        "x_psm_outside_service_request",
        "x_psm_request_id",
        string="Outside Service Requests",
        help="Outside service requests created when the 0502 maintenance flow is routed to a vendor.",
    )

    # field hien thi nhanh outside service request moi nhat de mo lai tu request goc
    x_psm_0502_outside_service_request_id = fields.Many2one(
        "x_psm_outside_service_request",
        string="Outside Service Request",
        compute="_compute_x_psm_0502_outside_service_summary",
        store=True,
        readonly=True,
        help="Latest outside service request linked to this 0502 maintenance request.",
    )

    # field dem nhanh so luong outside service request da lien ket
    x_psm_0502_outside_service_request_count = fields.Integer(
        string="Outside Service Count",
        compute="_compute_x_psm_0502_outside_service_summary",
        store=True,
        readonly=True,
        help="Number of outside service requests linked to this 0502 maintenance request.",
    )

    # field nhin nhanh trang thai outside service request moi nhat
    x_psm_0502_outside_service_state = fields.Selection(
        related="x_psm_0502_outside_service_request_id.x_psm_state",
        string="Outside Service State",
        store=True,
        readonly=True,
        help="Current state of the latest outside service request.",
    )

    # field co xac dinh request nay co phat sinh nhu cau vat tu hay khong
    x_psm_0502_has_material_request = fields.Boolean(
        string="Has Material Request",
        tracking=True,
        help="Indicates whether the approved internal handling requires material to be issued from stock.",
    )

    # field one2many ghi nhan chi tiet vat tu phat sinh thay vi chi danh dau co/khong
    x_psm_0502_material_line_ids = fields.One2many(
        "x_psm_request_material_line",
        "x_psm_request_id",
        string="Material Detail Lines",
        help="Structured material detail lines captured during the phase 2 material assessment step.",
    )

    # field dem nhanh so dong vat tu phat sinh de hien thi va filter de hon tren request
    x_psm_0502_material_line_count = fields.Integer(
        string="Material Line Count",
        compute="_compute_x_psm_0502_material_line_count",
        store=True,
        help="Number of structured material detail lines linked to the request.",
    )

    # field ghi chu danh gia vat tu o buoc 14 de noi ro vat tu co phat sinh hay khong
    x_psm_0502_material_assessment_note = fields.Text(
        string="Material Assessment Note",
        help="Assessment note explaining whether material is required before repair can continue.",
    )

    # field ghi nhan ai da xac nhan ket qua danh gia vat tu
    x_psm_0502_material_checked_by_id = fields.Many2one(
        "res.users",
        string="Material Checked By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who assessed whether material is required in phase 1.",
    )

    # field ghi nhan thoi diem da xac nhan ket qua danh gia vat tu
    x_psm_0502_material_checked_at = fields.Datetime(
        string="Material Checked At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the material requirement was assessed in phase 1.",
    )

    # field luu phieu kho noi bo duoc tao ra tu request 0502 o buoc 15
    x_psm_0502_stock_picking_id = fields.Many2one(
        "stock.picking",
        string="Stock Picking",
        tracking=True,
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Internal stock picking created from this maintenance request in phase 1.",
    )

    # field related de nhin nhanh state hien tai cua phieu kho tren maintenance request
    # field related cho phep hien thi gia tri cua field tren model khac ma khong can phai khai bao lai field do tren model hien tai
    x_psm_0502_stock_picking_state = fields.Selection(  
        related="x_psm_0502_stock_picking_id.state",
        string="Stock Picking State",
        readonly=True,
        help="Current state of the linked stock picking.",
    )

    # field related hien thi thong diep availability san co cua stock picking
    x_psm_0502_stock_availability = fields.Char(
        related="x_psm_0502_stock_picking_id.products_availability",
        string="Current Stock Availability",
        readonly=True,
        help="Current availability message computed live from the linked stock picking.",
    )

    # field related hien thi state availability ky thuat cua stock picking
    x_psm_0502_stock_availability_state = fields.Selection(
        related="x_psm_0502_stock_picking_id.products_availability_state",
        string="Current Stock Availability State",
        readonly=True,
        help="Current technical availability state computed live from the linked stock picking.",
    )

    # field snapshot luu thong diep availability tai thoi diem user bam check o buoc 16
    x_psm_0502_stock_check_availability = fields.Char(
        string="Checked Stock Availability",
        tracking=True,
        readonly=True,
        copy=False,
        help="Availability message captured at the moment the user checked stock availability.",
    )

    # field snapshot luu state availability ky thuat tai thoi diem user bam check
    x_psm_0502_stock_check_availability_state = fields.Char(
        string="Checked Stock Availability State",
        tracking=True,
        readonly=True,
        copy=False,
        help="Technical availability state captured at the moment the user checked stock availability.",
    )

    # field ket qua kiem tra ton kho o buoc 16
    # field dang dropdown / trang thai
    # co 2 phan, value dong trong code va label hien thi cho nguoi dung
    x_psm_0502_stock_check_result = fields.Selection(
        selection=[
            ("available", "Stock Available"),
            ("not_available", "Stock Not Available"),
        ],
        string="Stock Check Result",
        tracking=True,
        copy=False,
        # da du hang hay cho cho request nay
        help="Snapshot decision captured from the linked stock picking when stock availability was checked.",
    )

    # field ghi nhan ai da thuc hien kiem tra ton kho
    x_psm_0502_stock_checked_by_id = fields.Many2one(
        "res.users",
        string="Stock Checked By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who checked stock availability in phase 1 step 16.",
    )

    # field ghi nhan thoi diem kiem tra ton kho
    x_psm_0502_stock_checked_at = fields.Datetime(
        string="Stock Checked At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when stock availability was checked in phase 1 step 16.",
    )

    # field cho biet nhanh vat tu nay co can qua vong duyet thu cong hay khong
    x_psm_0502_material_approval_required = fields.Boolean(
        string="Material Approval Required",
        tracking=True,
        copy=False,
        help="Indicates whether the internal material issue request requires manual approval after applying the phase 2 material rule.",
    )

    # field user noi bo duoc resolve lam approver cho nhanh vat tu
    x_psm_0502_material_approval_user_id = fields.Many2one(
        "res.users",
        string="Material Approver",
        tracking=True,
        readonly=True,
        copy=False,
        help="Resolved internal approver responsible for the 0502 material issue request.",
    )

    # field luu rule resolve approver vat tu da duoc su dung
    x_psm_0502_material_approval_rule = fields.Selection(
        selection=[
            ("team_material_approver", "Team Material Approver"),
            ("team_lead_fallback", "Team Lead Fallback"),
            ("team_member_fallback", "Team Member Fallback"),
            ("technician_fallback", "Technician Fallback"),
            ("current_user_fallback", "Current User Fallback"),
        ],
        string="Material Approval Rule",
        tracking=True,
        readonly=True,
        copy=False,
        help="Resolution rule used to choose the approver for the 0502 internal material issue request.",
    )

    # field snapshot luu tong gia tri vat tu du kien tai thoi diem gui duyet
    x_psm_0502_material_approval_value = fields.Monetary(
        string="Estimated Material Value",
        currency_field="x_psm_0502_currency_id",
        tracking=True,
        readonly=True,
        copy=False,
        help="Estimated material value snapshot captured when the internal material issue request was submitted for approval.",
    )

    # field luu rule auto/manual review theo gia tri vat tu hoac nguon vat tu
    x_psm_0502_material_approval_value_rule = fields.Selection(
        selection=[
            ("auto_approved_under_limit", "Auto Approved Under Limit"),
            ("manual_review_required", "Manual Review Required"),
            ("manual_review_required_source_type", "Manual Review Required By Source Type"),
        ],
        string="Material Approval Value Rule",
        tracking=True,
        readonly=True,
        copy=False,
        help="Decision rule applied to the material issue request based on the estimated material value and source type mix.",
    )

    # field trang thai duyet nhanh xuat vat tu o buoc 17
    x_psm_0502_material_approval_status = fields.Selection(
        selection=[
            ("pending", "Pending Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Material Approval Status",
        tracking=True,
        copy=False,
        help="Stores the internal approval decision before stock issue in phase 1 step 17 and phase 2 step 17.",
    )

    # field ghi nhan ai da ra quyet dinh duyet nhanh vat tu
    x_psm_0502_material_approval_decided_by_id = fields.Many2one(
        "res.users",
        string="Material Approval Decided By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who approved or rejected the material issue request in phase 1 step 17.",
    )

    # field ghi nhan thoi diem ra quyet dinh duyet nhanh vat tu
    x_psm_0502_material_approval_decided_at = fields.Datetime(
        string="Material Approval Decided At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the material approval decision was made in phase 1 step 17.",
    )

    # field ghi chu cho quyet dinh duyet/tu choi nhanh vat tu
    x_psm_0502_material_approval_note = fields.Text(
        string="Material Approval Note",
        help="Approval note explaining why the material issue request was approved or rejected.",
    )

    # field ghi nhan ai da xac nhan viec xuat kho thuc te o buoc 18
    x_psm_0502_stock_issued_by_id = fields.Many2one(
        "res.users",
        string="Stock Issued By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who confirmed the actual stock issue in phase 1 step 18.",
    )

    # field ghi nhan thoi diem da xuat kho thuc te
    x_psm_0502_stock_issued_at = fields.Datetime(
        string="Stock Issued At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the linked stock picking was considered issued in phase 1 step 18.",
    )

    # field business status de user nghiep vu nhin nhanh nhanh xuat kho ma khong phai tu dien giai state ky thuat cua stock.picking
    x_psm_0502_stock_issue_status = fields.Selection(
        selection=[
            ("no_picking", "No Stock Picking"),
            ("pending_issue", "Pending Stock Issue"),
            ("issued", "Stock Issued"),
            ("cancelled", "Stock Flow Cancelled"),
        ],
        string="Stock Issue Status",
        tracking=True,
        readonly=True,
        copy=False,
        help="Business status of the internal stock issue branch, synchronized from the linked stock picking in phase 2 step 18.",
    )

    # field ghi nhan lan dong bo cuoi cung giua request va stock.picking cho nhanh xuat kho
    x_psm_0502_stock_issue_synced_at = fields.Datetime(
        string="Stock Issue Synced At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the internal stock issue business status was last synchronized from the linked stock picking.",
    )

    # field related de nhin nhanh stage hien tai cua FSM task trong buoc 20
    x_psm_0502_fsm_stage_id = fields.Many2one(
        "project.task.type",
        related="x_psm_0502_fsm_task_id.stage_id",
        string="FSM Stage",
        store=True,
        readonly=True,
        help="Current stage of the linked FSM task used as the main execution object in phase 1 step 20.",
    )

    # field related de biet FSM task da dong/chua theo logic chuan cua project task
    x_psm_0502_fsm_is_closed = fields.Boolean(
        related="x_psm_0502_fsm_task_id.is_closed",
        string="FSM Task Closed",
        store=True,
        readonly=True,
        help="Indicates whether the linked FSM task has reached a closed state.",
    )

    # field ghi nhan ai la nguoi xac nhan da bat dau thi cong/sua chua
    x_psm_0502_execution_started_by_id = fields.Many2one(
        "res.users",
        string="Execution Started By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who confirmed that technical execution started in phase 1 step 20.",
    )

    # field ghi nhan thoi diem bat dau thi cong/sua chua
    x_psm_0502_execution_started_at = fields.Datetime(
        string="Execution Started At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when execution was marked as started in phase 1 step 20.",
    )

    # field ghi nhan ai la nguoi xac nhan da hoan tat thi cong/sua chua
    x_psm_0502_execution_completed_by_id = fields.Many2one(
        "res.users",
        string="Execution Completed By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who confirmed that technical execution was completed in phase 1 step 20.",
    )

    # field ghi nhan thoi diem hoan tat thi cong/sua chua
    x_psm_0502_execution_completed_at = fields.Datetime(
        string="Execution Completed At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when execution was marked as completed in phase 1 step 20.",
    )

    # field ghi chu tong hop ket qua sua chua tren request
    x_psm_0502_execution_note = fields.Text(
        string="Execution Note",
        help="Summary note of the repair execution in phase 1 step 20. Detailed technical work remains on the FSM task.",
    )

    # field ket qua nghiem thu sau bao tri cua cua hang
    x_psm_0502_acceptance_result = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("follow_up_needed", "Follow-up Needed"),
            ("rework_required", "Rework Required"),
        ],
        string="Acceptance Result",
        tracking=True,
        copy=False,
        help="Structured post-maintenance acceptance result captured in phase 2 step 21.",
    )

    # field ghi nhan nguoi dai dien cua cua hang/bo phan nghiem thu ket qua bao tri
    x_psm_0502_acceptance_contact_name = fields.Char(
        string="Store Acceptance Contact",
        help="Name of the store-side or requester-side representative who reviewed the maintenance result.",
    )

    # field ghi nhan vai tro cua nguoi nghiem thu de ro ownership nghiem thu
    x_psm_0502_acceptance_contact_role = fields.Char(
        string="Store Acceptance Role",
        help="Role or title of the store-side representative who reviewed the maintenance result.",
    )

    # field ghi nhan tinh trang thiet bi sau bao tri tai thoi diem nghiem thu
    x_psm_0502_acceptance_equipment_result = fields.Selection(
        selection=[
            ("operating_normally", "Operating Normally"),
            ("operating_with_monitoring", "Operating with Monitoring"),
            ("not_operating", "Not Operating"),
        ],
        string="Post-Maintenance Equipment Result",
        tracking=True,
        copy=False,
        help="Observed equipment condition at the time of post-maintenance acceptance.",
    )

    # field ghi chu ket luan nghiem thu/danh gia sau bao tri
    x_psm_0502_acceptance_note = fields.Text(
        string="Acceptance Note",
        help="Structured conclusion and evaluation note after maintenance completion in phase 2 step 21.",
    )

    # field ghi nhan hanh dong theo doi/lam lai sau nghiem thu neu request chua duoc chap nhan hoan toan
    x_psm_0502_acceptance_follow_up_note = fields.Text(
        string="Acceptance Follow-up Note",
        help="Required follow-up or rework note when post-maintenance acceptance is not fully accepted.",
    )

    # field ghi nhan ai da xac nhan nghiem thu sau bao tri
    x_psm_0502_acceptance_reviewed_by_id = fields.Many2one(
        "res.users",
        string="Acceptance Reviewed By",
        tracking=True,
        readonly=True,
        copy=False,
        help="User who recorded the post-maintenance acceptance decision in phase 1 step 21.",
    )

    # field ghi nhan thoi diem nghiem thu sau bao tri
    x_psm_0502_acceptance_reviewed_at = fields.Datetime(
        string="Acceptance Reviewed At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when the post-maintenance acceptance was recorded in phase 1 step 21.",
    )

    # field dem so vong lam lai/bo sung sau khi nghiem thu chua dat
    x_psm_0502_rework_round_count = fields.Integer(
        string="Rework Round Count",
        default=0,
        tracking=True,
        copy=False,
        help="Number of times this request has been reopened after acceptance required follow-up or rework.",
    )

    # field lich su cac lan mo lai request sau nghiem thu
    x_psm_0502_rework_history_ids = fields.One2many(
        "x_psm_request_rework_history",
        "x_psm_request_id",
        string="Rework History",
        readonly=True,
        copy=False,
        help="History lines created each time this request is reopened for rework.",
    )

    # field ghi nhan lan gan nhat request duoc mo lai de lam lai/bo sung
    x_psm_0502_last_rework_at = fields.Datetime(
        string="Last Rework At",
        tracking=True,
        readonly=True,
        copy=False,
        help="Date and time when this request was last reopened for rework.",
    )

    # field ghi nhan user gan nhat mo lai request de lam lai/bo sung
    x_psm_0502_last_rework_by_id = fields.Many2one(
        "res.users",
        string="Last Rework By",
        tracking=True,
        readonly=True,
        copy=False,
        ondelete="set null",
        help="User who last reopened this request for rework.",
    )

    # field tap hop tat ca RFQ/PO mua ngoai duoc lien ket voi request 0502
    x_psm_0502_purchase_order_ids = fields.One2many(
        "purchase.order",
        "x_psm_0502_request_id",
        string="Purchase Orders",
        help="Outside purchase orders linked to this maintenance request in phase 1 step 19.",
    )

    # field tong hop nhanh so luong RFQ/PO da lien ket
    x_psm_0502_purchase_order_count = fields.Integer(
        string="Purchase Order Count",
        compute="_compute_x_psm_0502_purchase_summary",
        store=True,
        readonly=True,
        help="Number of outside purchase orders linked to this maintenance request.",
    )

    # field quy doi nhanh don mua ngoai moi nhat de hien thi va mo lai tren request
    x_psm_0502_purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Purchase Order",
        compute="_compute_x_psm_0502_purchase_summary",
        store=True,
        readonly=True,
        help="Latest linked outside purchase order for this maintenance request.",
    )

    # field nhin nhanh state cua RFQ/PO moi nhat
    x_psm_0502_purchase_order_state = fields.Selection(
        selection=[
            ("draft", "RFQ"),
            ("sent", "RFQ Sent"),
            ("to approve", "To Approve"),
            ("purchase", "Purchase Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ],
        string="Purchase Order State",
        compute="_compute_x_psm_0502_purchase_summary",
        store=True,
        readonly=True,
        help="State of the latest outside purchase order linked to this maintenance request.",
    )

    @api.depends(
        "x_psm_0502_outside_service_request_ids",
        "x_psm_0502_outside_service_request_ids.create_date",
        "x_psm_0502_outside_service_request_ids.x_psm_state",
    )
    def _compute_x_psm_0502_outside_service_summary(self):
        for record in self:
            outside_requests = record.x_psm_0502_outside_service_request_ids.sorted(
                key=lambda outside_request: ((outside_request.create_date or fields.Datetime.now()), outside_request.id),
                reverse=True,
            )
            latest_outside_request = outside_requests[:1]

            record.x_psm_0502_outside_service_request_count = len(outside_requests)
            record.x_psm_0502_outside_service_request_id = latest_outside_request.id if latest_outside_request else False

    @api.depends("x_psm_0502_purchase_order_ids", "x_psm_0502_purchase_order_ids.state", "x_psm_0502_purchase_order_ids.create_date")
    def _compute_x_psm_0502_purchase_summary(self):
        for record in self:
            purchase_orders = record.x_psm_0502_purchase_order_ids.sorted(
                key=lambda order: ((order.create_date or fields.Datetime.now()), order.id),
                reverse=True,
            )
            latest_purchase_order = purchase_orders[:1]

            record.x_psm_0502_purchase_order_count = len(purchase_orders)
            record.x_psm_0502_purchase_order_id = latest_purchase_order.id if latest_purchase_order else False
            record.x_psm_0502_purchase_order_state = latest_purchase_order.state if latest_purchase_order else False
