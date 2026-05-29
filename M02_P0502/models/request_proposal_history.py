from odoo import fields, models


class X0502RequestProposalHistory(models.Model):
    _name = "x_psm_request_proposal_history"
    _description = "0502 Request Proposal History"
    _order = "x_psm_revision desc, id desc"

    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
        help="0502 maintenance request that this proposal history line belongs to.",
    )

    x_psm_revision = fields.Integer(
        string="Revision",
        required=True,
        default=1,
        help="Proposal revision number used to track each initial proposal and later revision.",
    )

    x_psm_change_type = fields.Selection(
        selection=[
            ("initial_proposal", "Initial Proposal"),
            ("reproposal", "Reproposal"),
        ],
        string="Change Type",
        required=True,
        help="Indicates whether this line records the first proposal or a later proposal revision.",
    )

    x_psm_root_cause_analysis = fields.Text(
        string="Root Cause Analysis Snapshot",
        help="Root cause analysis captured at the time of this proposal revision.",
    )

    x_psm_technical_solution = fields.Text(
        string="Technical Solution Snapshot",
        help="Technical solution captured at the time of this proposal revision.",
    )

    x_psm_estimated_cost = fields.Float(
        string="Estimated Cost Snapshot",
        help="Estimated cost captured at the time of this proposal revision.",
    )

    x_psm_currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        ondelete="set null",
        help="Currency used when the estimated cost snapshot was recorded.",
    )

    x_psm_estimated_timeline = fields.Char(
        string="Estimated Timeline Snapshot",
        help="Estimated timeline captured at the time of this proposal revision.",
    )

    x_psm_cost_note = fields.Text(
        string="Cost Note Snapshot",
        help="Cost note captured at the time of this proposal revision.",
    )

    x_psm_timeline_note = fields.Text(
        string="Timeline Note Snapshot",
        help="Timeline note captured at the time of this proposal revision.",
    )

    x_psm_proposal_summary = fields.Text(
        string="Proposal Summary Snapshot",
        help="Structured proposal summary captured at the time of this proposal revision.",
    )

    x_psm_proposal_document = fields.Text(
        string="Proposal Document Snapshot",
        help="Proposal document snapshot captured at the time of this proposal revision.",
    )

    x_psm_change_reason = fields.Text(
        string="Change Reason",
        help="Reason recorded for the proposal revision.",
    )

    x_psm_changed_by_id = fields.Many2one(
        "res.users",
        string="Changed By",
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
        help="User who created this proposal history entry.",
    )

    x_psm_changed_at = fields.Datetime(
        string="Changed At",
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        help="Date and time when this proposal history entry was recorded.",
    )
