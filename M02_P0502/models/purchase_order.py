# Khai bao ma hoa file Python
# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # field lien ket nguoc tu don mua ngoai ve maintenance request cua quy trinh 0502
    x_psm_0502_request_id = fields.Many2one(
        "maintenance.request",
        string="0502 Maintenance Request",
        tracking=True,
        copy=False,
        index=True,
        ondelete="set null",
        help="Maintenance request that triggered this purchase order in 0502 phase 1 step 19.",
    )

    # field related de ben mua nhin nhanh task FSM dang thuc thi phat sinh nhu cau mua ngoai
    x_psm_0502_fsm_task_id = fields.Many2one(
        "project.task",
        related="x_psm_0502_request_id.x_psm_0502_fsm_task_id",
        string="0502 FSM Task",
        store=True,
        readonly=True,
        help="FSM task linked to the 0502 maintenance request that triggered this purchase order.",
    )

    # field related de ben mua nhin nhanh cua hang/phong ban phat sinh nhu cau mua ngoai
    x_psm_0502_department_id = fields.Many2one(
        "hr.department",
        related="x_psm_0502_request_id.x_psm_0502_department_id",
        string="0502 Store Department",
        store=True,
        readonly=True,
        help="Store department linked to the 0502 maintenance request that triggered this purchase order.",
    )

    # field related de ben mua nhin nhanh source system cua request 0502
    x_psm_0502_source_system = fields.Selection(
        related="x_psm_0502_request_id.x_psm_0502_source_system",
        string="0502 Source System",
        store=True,
        readonly=True,
        help="Source system of the 0502 maintenance request that triggered this purchase order.",
    )

    # field lien ket don mua voi outside service request cua phase 3B neu don nay phat sinh tu thue ngoai
    x_psm_0502_outside_service_request_id = fields.Many2one(
        "x_psm_outside_service_request",
        string="0502 Outside Service Request",
        tracking=True,
        copy=False,
        index=True,
        ondelete="set null",
        help="Outside service request that triggered this purchase order in phase 3B.",
    )
