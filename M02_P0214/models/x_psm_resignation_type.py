# -*- coding: utf-8 -*-
from odoo import fields, models


class ResignationType(models.Model):
    _name = "x_psm_resignation_type"
    _table = "resignation_type"
    _description = "Resignation Type"
    _order = "sequence, id"

    name = fields.Char(string="Resignation Type Name", required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
