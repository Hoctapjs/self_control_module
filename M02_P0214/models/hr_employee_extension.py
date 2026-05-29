# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployeeRSTExtension(models.Model):
    _inherit = "hr.employee"

    is_rst_employee = fields.Boolean(
        string="Is RST Employee",
        default=False,
        help="Check this if the employee is part of RST (Resignation & Turnover Support) team",
    )
    x_psm_0214_is_rst_employee = fields.Boolean(
        related="is_rst_employee",
        string="Is RST Employee",
        store=True,
        readonly=False,
    )
