# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class Xpsm0214FinanceOverrideWizard(models.TransientModel):
    _name = "x_psm_0214_finance_override_wizard"
    _description = "RST Accounting Override Wizard"

    request_id = fields.Many2one(
        "approval.request",
        string="Resignation Request",
        required=True,
        readonly=True,
    )
    reason = fields.Text(string="Override Reason", required=True)

    def action_apply(self):
        self.ensure_one()
        request = self.request_id
        request._check_0214_group_access(
            _("Override Accounting Check"),
            ("M02_P0200.GDH_RST_HR_HEAD_M", "M02_P0200.GDH_RST_SYSTEM_ST_M"),
        )
        if request.x_psm_0214_finance_check_state != "blocked":
            raise UserError(_("Only requests blocked by Accounting can be overridden."))

        request.sudo().write(
            {
                "x_psm_0214_finance_check_state": "overridden",
                "x_psm_0214_finance_override_reason": self.reason,
                "x_psm_0214_finance_override_user_id": self.env.user.id,
                "x_psm_0214_finance_checked_date": fields.Datetime.now(),
            }
        )
        request.message_post(
            body=_("Accounting check overridden. Reason: %s") % self.reason
        )
        return {"type": "ir.actions.act_window_close"}
