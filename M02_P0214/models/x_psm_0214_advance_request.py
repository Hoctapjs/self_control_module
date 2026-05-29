# -*- coding: utf-8 -*-
from odoo import fields, models


class Xpsm0214AdvanceRequest(models.Model):
    _name = "x_psm_0214_advance_request"
    _description = "RST Advance Request"
    _order = "date desc, id desc"

    name = fields.Char(string="Reference No.", required=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        index=True,
    )
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    date = fields.Date(string="Advance Date", default=fields.Date.context_today)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("settled", "Settled"),
        ],
        string="Status",
        default="draft",
        required=True,
        index=True,
    )
