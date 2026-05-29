# -*- coding: utf-8 -*-
from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"

    x_psm_0213_it_user_id = fields.Many2one(
        "res.users",
        string="IT Phụ Trách Offboarding (0213)",
        domain=[("share", "=", False)],
        help=(
            "Người dùng IT phụ trách các task offboarding 0213 của cửa hàng/phòng ban này. "
            "Nếu bỏ trống, hệ thống dùng IT mặc định cấp công ty "
            "(res.company.x_psm_0213_default_it_user_id)."
        ),
    )
