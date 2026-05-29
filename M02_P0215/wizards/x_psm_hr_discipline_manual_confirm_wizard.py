# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrDisciplineManualConfirmWizard(models.TransientModel):
    _name = "x_psm.hr.discipline.manual.confirm.wizard"
    _description = "Discipline Manual Confirmation Wizard"

    x_psm_record_id = fields.Many2one("x_psm.hr.discipline.record", required=True)
    x_psm_start_date = fields.Date(
        string="Effective Start Date",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        record_id = self.env.context.get("default_x_psm_record_id")
        if record_id and "x_psm_start_date" in fields_list:
            record = self.env["x_psm.hr.discipline.record"].browse(record_id)
            if record.exists():
                res["x_psm_start_date"] = record._x_psm_resolve_effective_start_date()
        return res

    def action_psm_confirm(self):
        self.ensure_one()
        self.x_psm_record_id.action_psm_rgm_manual_confirm(self.x_psm_start_date)
        return {"type": "ir.actions.act_window_close"}
