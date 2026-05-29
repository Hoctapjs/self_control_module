# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrDisciplineViolationReportWizard(models.TransientModel):
    _name = "x_psm.hr.discipline.violation.report.wizard"
    _description = "Violation Headcount Report Wizard"

    @api.model
    def _default_x_psm_date_from(self):
        today = fields.Date.context_today(self)
        return today.replace(day=1)

    x_psm_date_from = fields.Date(
        string="Date From",
        required=True,
        default=_default_x_psm_date_from,
    )
    x_psm_date_to = fields.Date(
        string="Date To",
        required=True,
        default=fields.Date.context_today,
    )
    x_psm_state_filter = fields.Selection(
        [
            ("all", "All"),
            ("draft", "Draft"),
            ("under_review", "Under Review"),
            ("level_determination", "Level Determination"),
            ("investigation", "Investigation"),
            ("hearing", "Disciplinary Hearing"),
            ("proposal", "Discipline Proposal"),
            ("issued", "Decision Issued"),
            ("approval", "Approval"),
            ("notified", "Notified"),
            ("active", "Active"),
            ("expired", "Expired"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="all",
    )
    x_psm_include_cancelled = fields.Boolean(
        string="Include Cancelled Records",
        default=False,
    )
    x_psm_employee_count = fields.Integer(
        string="Violation Employee Count",
        compute="_compute_x_psm_counts",
        readonly=True,
    )
    x_psm_record_count = fields.Integer(
        string="Violation Record Count",
        compute="_compute_x_psm_counts",
        readonly=True,
    )

    def _x_psm_get_domain(self):
        self.ensure_one()
        if not self.x_psm_date_from or not self.x_psm_date_to:
            return []
        if self.x_psm_date_from > self.x_psm_date_to:
            raise UserError(
                _("Date From cannot be later than Date To.")
            )

        domain = [
            ("x_psm_date", ">=", self.x_psm_date_from),
            ("x_psm_date", "<=", self.x_psm_date_to),
        ]
        if not self.x_psm_include_cancelled:
            domain.append(("state", "!=", "cancel"))
        if self.x_psm_state_filter and self.x_psm_state_filter != "all":
            domain.append(("state", "=", self.x_psm_state_filter))
        return domain

    @api.depends(
        "x_psm_date_from",
        "x_psm_date_to",
        "x_psm_state_filter",
        "x_psm_include_cancelled",
    )
    def _compute_x_psm_counts(self):
        DisciplineRecord = self.env["x_psm.hr.discipline.record"]
        for rec in self:
            domain = rec._x_psm_get_domain()
            rec.x_psm_record_count = DisciplineRecord.search_count(domain)
            groups = DisciplineRecord.read_group(
                domain,
                ["__count"],
                ["x_psm_employee_id"],
                lazy=False,
            )
            rec.x_psm_employee_count = sum(
                1 for group in groups if group.get("x_psm_employee_id")
            )

    @api.constrains("x_psm_date_from", "x_psm_date_to")
    def _check_dates(self):
        for rec in self:
            if (
                rec.x_psm_date_from
                and rec.x_psm_date_to
                and rec.x_psm_date_from > rec.x_psm_date_to
            ):
                raise UserError(
                    _("Date From cannot be later than Date To.")
                )

    def action_psm_view_records(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Disciplinary Records - Violation Report"),
            "res_model": "x_psm.hr.discipline.record",
            "view_mode": "list,form",
            "domain": self._x_psm_get_domain(),
            "context": {"group_by": "x_psm_employee_id"},
        }
