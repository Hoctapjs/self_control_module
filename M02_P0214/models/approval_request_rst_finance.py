# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class ResignationRequest(models.Model):
    _inherit = "approval.request"

    def _format_0214_finance_amount(self, amount, currency):
        currency_name = currency.name if currency else ""
        return "%s %s" % (amount or 0.0, currency_name)

    def _get_0214_pending_finance_items(self):
        self.ensure_one()
        employee = self.x_psm_0214_employee_id
        if not employee:
            return self.env["hr.expense"], self.env["x_psm_0214_advance_request"]

        expenses = self.env["hr.expense"].sudo().search(
            [
                ("employee_id", "=", employee.id),
                ("state", "not in", ["paid", "refused"]),
            ]
        )
        advances = self.env["x_psm_0214_advance_request"].sudo().search(
            [
                ("employee_id", "=", employee.id),
                ("state", "!=", "settled"),
            ]
        )
        return expenses, advances

    def _get_0214_pending_finance_items_summary(self):
        self.ensure_one()
        expenses, advances = self._get_0214_pending_finance_items()
        lines = []
        for expense in expenses:
            amount = self._format_0214_finance_amount(
                expense.total_amount,
                expense.company_currency_id,
            )
            lines.append(
                _("Expense: %(name)s - %(amount)s - %(state)s")
                % {
                    "name": expense.display_name,
                    "amount": amount,
                    "state": expense.state,
                }
            )
        for advance in advances:
            amount = self._format_0214_finance_amount(
                advance.amount,
                advance.currency_id,
            )
            lines.append(
                _("Advance: %(name)s - %(amount)s - %(state)s")
                % {
                    "name": advance.display_name,
                    "amount": amount,
                    "state": advance.state,
                }
            )
        if self.x_psm_0214_al_has_advance and not self.x_psm_0214_al_settled:
            lines.append(
                _("Advance Annual Leave: %(days).2f day(s) - deduction not settled")
                % {"days": self.x_psm_0214_al_advance_days}
            )
        return "\n".join(lines)

    def action_push_to_accounting(self):
        self._check_0214_group_access(
            _("Push to Accounting"),
            self._GROUP_0214_HR_PROCESS,
        )
        self.ensure_one()
        if not self._is_0214_offboarding_request():
            return self._build_rst_notification_action(
                _("Notice"),
                _("This action only applies to RST resignation requests."),
                message_type="warning",
                sticky=True,
            )

        expenses, advances = self._get_0214_pending_finance_items()
        checked_date = fields.Datetime.now()
        al_pending = (
            self.x_psm_0214_al_has_advance
            and not self.x_psm_0214_al_settled
        )
        if expenses or advances or al_pending:
            summary = self._get_0214_pending_finance_items_summary()
            self.sudo().write(
                {
                    "x_psm_0214_finance_check_state": "blocked",
                    "x_psm_0214_finance_checked_date": checked_date,
                    "x_psm_0214_finance_pending_items_summary": summary,
                }
            )
            return self._build_rst_notification_action(
                _("Cannot push to Accounting"),
                _("Pending items remain:\n%s") % summary,
                message_type="danger",
                sticky=True,
            )

        self.sudo().write(
            {
                "x_psm_0214_finance_check_state": "passed",
                "x_psm_0214_finance_checked_date": checked_date,
                "x_psm_0214_finance_pending_items_summary": False,
            }
        )
        return self._build_rst_notification_action(
            _("Success"),
            _("Check complete: no pending items. Ready to push to Accounting."),
            message_type="success",
        )

    def action_settle_advance_al(self):
        self.ensure_one()
        if not self._is_0214_offboarding_request():
            category_0213 = self.env.ref(
                "M02_P0213.psm_0213_approval_category_resignation",
                raise_if_not_found=False,
            )
            if category_0213 and self.category_id == category_0213:
                return super().action_settle_advance_al()
        self._check_0214_group_access(
            _("Settle Advance Annual Leave"),
            self._GROUP_0214_HR_PROCESS,
        )
        if not self.x_psm_0214_al_has_advance:
            raise UserError(
                _("This request has no advance annual leave to deduct.")
            )
        if self.x_psm_0214_al_deduction_amount <= 0:
            raise UserError(
                _("Please enter the advance annual leave deduction amount before settling.")
            )
        self.sudo().write({"x_psm_0214_al_settled": True})
        amount = self._format_0214_finance_amount(
            self.x_psm_0214_al_deduction_amount,
            self.x_psm_0214_al_deduction_currency_id,
        )
        self.message_post(
            body=_(
                "Advance annual leave deduction settled: %(days).2f day(s) = %(amount)s"
            )
            % {
                "days": self.x_psm_0214_al_advance_days,
                "amount": amount,
            }
        )
        return self._build_rst_notification_action(
            _("Success"),
            _("Advance annual leave deduction has been settled."),
            message_type="success",
        )

    def action_open_finance_override_wizard(self):
        self._check_0214_group_access(
            _("Override Accounting Check"),
            ("M02_P0200.GDH_RST_HR_HEAD_M", "M02_P0200.GDH_RST_SYSTEM_ST_M"),
        )
        self.ensure_one()
        if self.x_psm_0214_finance_check_state != "blocked":
            raise UserError(_("Only requests blocked by Accounting can be overridden."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Override Accounting Check"),
            "res_model": "x_psm_0214_finance_override_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_request_id": self.id},
        }
