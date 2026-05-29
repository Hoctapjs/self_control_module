# -*- coding: utf-8 -*-
from odoo import _, models, fields


class ApprovalRequest(models.Model):
    _inherit = "approval.request"

    x_psm_discipline_record_id = fields.Many2one(
        "x_psm.hr.discipline.record",
        string="Discipline Record 0215",
        copy=False,
        index=True,
    )

    def action_approve(self, approver=None):
        result = super().action_approve(approver=approver)
        for request in self.filtered(
            lambda req: req.x_psm_discipline_record_id
            and req.request_status == "approved"
        ):
            request.x_psm_discipline_record_id._x_psm_on_approval_request_approved(request)
        return result

    def action_refuse(self, approver=None):
        if len(self) == 1 and self.x_psm_discipline_record_id and not self.env.context.get("ceo_reject_reason"):
            return {
                "type": "ir.actions.act_window",
                "name": _("Lý do từ chối"),
                "res_model": "x_psm.hr.discipline.reject.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_x_psm_record_id": self.x_psm_discipline_record_id.id,
                    "default_x_psm_mode": "ceo_reject",
                },
            }
            
        result = super().action_refuse(approver=approver)
        for request in self.filtered(
            lambda req: req.x_psm_discipline_record_id
            and req.request_status == "refused"
        ):
            request.x_psm_discipline_record_id._x_psm_on_approval_request_refused(request)
        return result

    def action_psm_open_discipline_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Hồ sơ kỷ luật",
            "res_model": "x_psm.hr.discipline.record",
            "view_mode": "form",
            "res_id": self.x_psm_discipline_record_id.id,
            "target": "current",
        }
