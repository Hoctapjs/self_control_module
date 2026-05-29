# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MktPafRejectWizard(models.TransientModel):
    _name = 'mkt_paf.reject.wizard'
    _description = 'Wizard từ chối PAF'

    approval_request_id = fields.Many2one(
        'approval.request',
        string='Yêu cầu phê duyệt',
        required=True
    )

    paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='Yêu cầu PAF',
        required=True
    )

    reason = fields.Text(
        string='Lý do từ chối',
        required=True
    )

    def action_confirm_reject(self):
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise ValidationError(_("Vui lòng nhập lý do từ chối."))
            
        # Execute the actual refusal on the approval request by passing reject reason in context
        self.approval_request_id.with_context(paf_reject_reason=self.reason).action_refuse()
        
        # Reject the PAF Request (moves state to draft, logs reason in chatter)
        self.paf_request_id.action_reject(self.reason)
        
        return {'type': 'ir.actions.act_window_close'}
