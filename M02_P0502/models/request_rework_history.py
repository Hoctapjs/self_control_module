from odoo import fields, models


class X0502RequestReworkHistory(models.Model):
    _name = "x_psm_request_rework_history"
    _description = "0502 Request Rework History"
    _order = "x_psm_round_number desc, id desc"

    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
        help="0502 maintenance request that this rework history line belongs to.",
    )

    x_psm_round_number = fields.Integer(
        string="Rework Round",
        required=True,
        default=1,
        help="Sequential rework round number recorded each time acceptance is reopened.",
    )

    x_psm_previous_acceptance_result = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("follow_up_needed", "Follow-up Needed"),
            ("rework_required", "Rework Required"),
        ],
        string="Previous Acceptance Result",
        required=True,
        help="Acceptance result that triggered this rework round.",
    )

    x_psm_rework_reason = fields.Text(
        string="Rework Reason",
        help="Reason or follow-up note captured before the request was reopened for rework.",
    )

    x_psm_created_by_id = fields.Many2one(
        "res.users",
        string="Created By",
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
        help="User who reopened the request for this rework round.",
    )

    x_psm_created_at = fields.Datetime(
        string="Created At",
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        help="Date and time when this rework history entry was recorded.",
    )

    x_psm_linked_fsm_task_id = fields.Many2one(
        "project.task",
        string="Linked FSM Task",
        ondelete="set null",
        help="FSM task that was linked to the request before the rework round was opened.",
    )
