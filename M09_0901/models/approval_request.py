# -*- coding: utf-8 -*-
from odoo import models, fields

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    x_psm_mkt_paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='PAF gốc',
        copy=False,
        index=True
    )

    def action_approve(self, approver=None):
        result = super().action_approve(approver=approver)
        for request in self:
            if request.x_psm_mkt_paf_request_id and request.request_status == 'approved' and request.category_id and request.category_id.is_mkt_paf:
                paf = request.x_psm_mkt_paf_request_id
                stage = request.category_id.mkt_paf_stage
                if stage == 'head':
                    paf.action_request_clevel()
                elif stage == 'clevel':
                    paf.action_mark_approved()
        return result

    def action_refuse(self, approver=None):
        if len(self) == 1 and self.x_psm_mkt_paf_request_id and not self.env.context.get("paf_reject_reason"):
            return {
                "type": "ir.actions.act_window",
                "name": "Lý do từ chối PAF",
                "res_model": "mkt_paf.reject.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_approval_request_id": self.id,
                    "default_paf_request_id": self.x_psm_mkt_paf_request_id.id,
                },
            }
        return super().action_refuse(approver=approver)

    def action_open_paf_request(self):
        self.ensure_one()
        return {
            'name': 'PAF Request',
            'type': 'ir.actions.act_window',
            'res_model': 'mkt_paf.request',
            'res_id': self.x_psm_mkt_paf_request_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
