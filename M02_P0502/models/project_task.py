from odoo import fields, models


class ProjectTask(models.Model):
    # ke thua project.task de tao lien ket nguoc tu FSM task ve maintenance request 0502
    _inherit = "project.task"

    # field lien ket FSM task voi maintenance request nguon
    #         ondelete="set null",
        # khi ban ghi cha bi xoa thi se khong xoa ban ghi con ma se set la null
    x_psm_0502_request_id = fields.Many2one(
        "maintenance.request",
        string="0502 Maintenance Request",
        readonly=True,
        copy=False,
        ondelete="set null", 
        help="Maintenance request that created this FSM execution task in process 0502.",
    )

    # related field de bao cao nhanh theo phong ban cua request goc
    x_psm_0502_department_id = fields.Many2one(
        "hr.department",
        related="x_psm_0502_request_id.x_psm_0502_department_id",
        string="Store Department",
        store=True,
        index=True,
        readonly=True,
    )

    # related field de gom bao cao theo loai yeu cau 0502
    x_psm_0502_request_type_id = fields.Many2one(
        "x_psm_request_type",
        related="x_psm_0502_request_id.x_psm_0502_request_type_id",
        string="Request Type",
        store=True,
        index=True,
        readonly=True,
    )

    # related field de gom bao cao theo nguon phat sinh request
    x_psm_0502_request_source_id = fields.Many2one(
        "x_psm_request_source",
        related="x_psm_0502_request_id.x_psm_0502_request_source_id",
        string="Request Source",
        store=True,
        index=True,
        readonly=True,
    )

    # related field de nhin nhanh request den tu he thong/upstream nao
    x_psm_0502_source_system = fields.Selection(
        related="x_psm_0502_request_id.x_psm_0502_source_system",
        string="Source System",
        store=True,
        index=True,
        readonly=True,
    )

    # related field de nhin nhanh ket qua kiem tra ban dau tren task thuc thi
    x_psm_0502_inspection_result = fields.Selection(
        related="x_psm_0502_request_id.x_psm_0502_inspection_result",
        string="Initial Inspection Result",
        store=True,
        index=True,
        readonly=True,
    )

    # related field de dua tom tat de xuat xu ly sang task de ky thuat vien nhin nhanh
    x_psm_0502_proposal_summary = fields.Text(
        related="x_psm_0502_request_id.x_psm_0502_treatment_proposal",
        string="Proposal Summary",
        store=True,
        readonly=True,
    )

    # snapshot template huong dan cong viec duoc dua sang task luc tao tu request o phase 3 buoc 9
    x_psm_0502_task_template_note = fields.Text(
        string="0502 Task Template",
        readonly=True,
        copy=False,
        help="Snapshot of the standardized 0502 task instruction template copied to the FSM task at creation time.",
    )

    # snapshot checklist template de ky thuat vien tham chieu khi thuc thi, tach voi checklist thuc te
    x_psm_0502_execution_checklist_template = fields.Text(
        string="0502 Execution Checklist Template",
        readonly=True,
        copy=False,
        help="Snapshot of the standardized 0502 execution checklist template copied to the FSM task at creation time.",
    )

    # snapshot goi y vat tu/chuan bi de task co package thuc thi ro hon ngay tu luc duoc tao
    x_psm_0502_material_package_template = fields.Text(
        string="0502 Material Package Template",
        readonly=True,
        copy=False,
        help="Snapshot of the standardized 0502 material preparation template copied to the FSM task at creation time.",
    )

    # field ket luan thuc thi thuc te tren FSM task de tach voi summary tren request
    x_psm_0502_execution_result = fields.Selection(
        selection=[
            ("completed_as_planned", "Completed as Planned"),
            ("completed_with_adjustment", "Completed with Adjustment"),
            ("temporary_fix", "Temporary Fix Applied"),
            ("follow_up_needed", "Follow-up Needed"),
        ],
        string="0502 Execution Result",
        tracking=True,
        help="Actual execution result recorded on the FSM task in phase 2 step 20.",
    )

    # field checklist thuc thi de ky thuat vien ghi lai cac buoc da xu ly
    x_psm_0502_execution_checklist_note = fields.Text(
        string="0502 Execution Checklist",
        help="Checklist-style note of the execution steps performed on site.",
    )

    # field worksheet ky thuat de ghi lai nhan xet/chuan doan va xu ly thuc te tren task
    x_psm_0502_execution_worksheet_note = fields.Text(
        string="0502 Technical Worksheet",
        help="Detailed technical worksheet note recorded during execution on the FSM task.",
    )

    # field tong hop vat tu da dung thuc te trong qua trinh sua chua
    x_psm_0502_material_used_note = fields.Text(
        string="0502 Material Used Note",
        help="Actual material usage note recorded on the FSM task.",
    )

    # field ghi nhan tong thoi gian thuc te da su dung cho cong viec
    x_psm_0502_time_spent_hours = fields.Float(
        string="0502 Actual Time Spent (Hours)",
        digits=(16, 2),
        help="Actual time spent on technical execution for process 0502.",
    )

    # field ghi nhan hanh dong theo doi bo sung neu task chua xu ly dut diem
    x_psm_0502_follow_up_action_note = fields.Text(
        string="0502 Follow-up Action Note",
        help="Required follow-up action after the current execution, if any.",
    )
