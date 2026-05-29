from odoo import fields, models


class X0502RequestPlanningHistory(models.Model):
    _name = "x_psm_request_planning_history"
    _description = "0502 Request Planning History"
    _order = "x_psm_revision desc, id desc"

    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
        help="0502 maintenance request that this planning history line belongs to.",
    )

    x_psm_revision = fields.Integer(
        string="Revision",
        required=True,
        default=1,
        help="Planning revision number used to track each planning confirmation or change.",
    )

    x_psm_change_type = fields.Selection(
        selection=[
            ("initial_plan", "Initial Plan"),
            ("replan", "Replan"),
        ],
        string="Change Type",
        required=True,
        help="Indicates whether this line records the first plan or a later planning revision.",
    )

    x_psm_schedule_date = fields.Datetime(
        string="Scheduled Date",
        help="Scheduled start captured at the time of this planning revision.",
    )

    x_psm_schedule_end = fields.Datetime(
        string="Scheduled End",
        help="Scheduled end captured at the time of this planning revision.",
    )

    x_psm_responsible_user_id = fields.Many2one(
        "res.users",
        string="Responsible",
        ondelete="set null",
        help="Responsible user assigned on this planning revision.",
    )

    x_psm_plan_note = fields.Text(
        string="Planning Note Snapshot",
        help="Planning note snapshot captured on this planning revision.",
    )

    x_psm_change_reason = fields.Text(
        string="Change Reason",
        help="Reason recorded for the planning revision or re-planning decision.",
    )

    x_psm_changed_by_id = fields.Many2one(
        "res.users",
        string="Changed By",
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
        help="User who created this planning history entry.",
    )

    x_psm_changed_at = fields.Datetime(
        string="Changed At",
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        help="Date and time when this planning history entry was recorded.",
    )
