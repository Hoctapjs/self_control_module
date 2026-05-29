from odoo import fields, models


class StockPicking(models.Model):
    # ke thua stock.picking de luu lien ket nguoc lai ve request 0502
    _inherit = "stock.picking"

    # field many2one luu request 0502 da tao ra phieu kho nay
    x_psm_0502_request_id = fields.Many2one(
        "maintenance.request",
        string="0502 Maintenance Request",
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Maintenance request that created this stock picking in process 0502.",
    )

    # field related de nhin nhanh task fsm lien ket voi request 0502 nguon
    x_psm_0502_fsm_task_id = fields.Many2one(
        "project.task",
        related="x_psm_0502_request_id.x_psm_0502_fsm_task_id",
        string="0502 FSM Task",
        store=True,
        readonly=True,
    )
