# Khai bao ma hoa file Python
# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class X0502OutsideServiceRequest(models.Model):
    _name = "x_psm_outside_service_request"
    _description = "0502 Outside Service Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(
        string="Outside Service No.",
        required=True,
        copy=False,
        readonly=True,
        default="New",
        help="Sequence number for the 0502 outside service request.",
    )

    # field lien ket request thue ngoai ve maintenance request goc cua quy trinh 0502
    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        tracking=True,
        ondelete="cascade",
        index=True,
        help="0502 maintenance request that requires outside service.",
    )

    x_psm_department_id = fields.Many2one(
        "hr.department",
        string="Store Department",
        related="x_psm_request_id.x_psm_0502_department_id",
        store=True,
        readonly=True,
        help="Store department inherited from the linked 0502 maintenance request.",
    )

    x_psm_equipment_id = fields.Many2one(
        "maintenance.equipment",
        string="Equipment",
        related="x_psm_request_id.equipment_id",
        store=True,
        readonly=True,
        help="Equipment inherited from the linked 0502 maintenance request.",
    )

    # field nha cung cap du kien thuc hien dich vu ngoai
    x_psm_vendor_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        tracking=True,
        domain="[('supplier_rank', '>', 0)]",
        help="Vendor proposed to perform the outside service.",
    )

    x_psm_quotation_received = fields.Boolean(
        string="Quotation Received",
        tracking=True,
        help="Indicates whether a quotation has been received from the vendor.",
    )

    x_psm_vendor_quote_amount = fields.Monetary(
        string="Vendor Quote Amount",
        currency_field="x_psm_vendor_quote_currency_id",
        tracking=True,
        help="Quoted amount received from the outside service vendor.",
    )

    x_psm_vendor_quote_currency_id = fields.Many2one(
        "res.currency",
        string="Quote Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for the outside service vendor quotation.",
    )

    x_psm_vendor_lead_time_days = fields.Integer(
        string="Vendor Lead Time (Days)",
        tracking=True,
        help="Estimated lead time proposed by the vendor.",
    )

    x_psm_expected_complete_date = fields.Date(
        string="Expected Complete Date",
        tracking=True,
        help="Expected completion date for the outside service.",
    )

    x_psm_scope_of_work = fields.Text(
        string="Scope of Work",
        tracking=True,
        help="Scope of work that should be sent to the outside service vendor.",
    )

    x_psm_service_type = fields.Selection(
        selection=[
            ("repair", "Repair"),
            ("inspection", "Inspection"),
            ("calibration", "Calibration"),
            ("warranty", "Warranty"),
            ("other", "Other"),
        ],
        string="Service Type",
        default="repair",
        required=True,
        tracking=True,
        help="Type of outside service required for this request.",
    )

    x_psm_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent_to_vendor", "Sent to Vendor"),
            ("quoted", "Quoted"),
            ("approved", "Approved"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("accepted", "Accepted"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        copy=False,
        help="Operational status of the 0502 outside service flow.",
    )

    x_psm_purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Purchase Order",
        tracking=True,
        copy=False,
        ondelete="set null",
        help="Purchase order created for the approved outside service vendor quote.",
    )

    x_psm_acceptance_result = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("partial", "Partial"),
        ],
        string="Vendor Service Acceptance Result",
        tracking=True,
        copy=False,
        help="Acceptance result after the vendor completes the outside service.",
    )

    x_psm_acceptance_note = fields.Text(
        string="Acceptance Note",
        tracking=True,
        help="Acceptance note for the outside service result.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("psm.0502.outside.service.request")
                    or "New"
                )
        return super().create(vals_list)

    def action_psm_send_to_vendor(self):
        for record in self:
            if record.x_psm_state != "draft":
                continue
            if not record.x_psm_vendor_id:
                raise UserError("Please select a Vendor before sending the outside service request.")
            if not record.x_psm_scope_of_work:
                raise UserError("Please fill in Scope of Work before sending the outside service request.")
            record.write({"x_psm_state": "sent_to_vendor"})

    def action_psm_record_quote(self):
        for record in self:
            if record.x_psm_state not in ("sent_to_vendor", "draft"):
                raise UserError("Only draft or sent outside service requests can record a vendor quote.")
            if not record.x_psm_vendor_id:
                raise UserError("Please select a Vendor before recording a quote.")
            if record.x_psm_vendor_quote_amount <= 0:
                raise UserError("Please enter Vendor Quote Amount greater than zero.")
            if record.x_psm_vendor_lead_time_days < 0:
                raise UserError("Vendor Lead Time cannot be negative.")
            record.write({
                "x_psm_quotation_received": True,
                "x_psm_state": "quoted",
            })

    def action_psm_approve_vendor(self):
        for record in self:
            if record.x_psm_state != "quoted":
                raise UserError("Only quoted outside service requests can be approved.")
            if not record.x_psm_quotation_received:
                raise UserError("Please record the vendor quote before approving the vendor.")
            if not (
                self.env.user.has_group("M02_P0502.group_psm_0502_store_approver")
                or self.env.user.has_group("M02_P0502.group_psm_0502_store_final_approver")
                or self.env.user.has_group("M02_P0502.group_psm_0502_manager")
            ):
                raise UserError("Only a 0502 Store Approver can approve this outside service vendor.")

            approver_user = record.x_psm_request_id.x_psm_0502_approval_user_id
            final_approver_user = record.x_psm_request_id.x_psm_0502_approval_final_user_id
            allowed_users = (approver_user | final_approver_user).filtered("id")
            if allowed_users and self.env.user not in allowed_users:
                raise UserError("Only the resolved 0502 proposal approver can approve this outside service vendor.")

            record.write({"x_psm_state": "approved"})

    def action_psm_create_purchase_order(self):
        self.ensure_one()

        if self.x_psm_state != "approved":
            raise UserError("Please approve the vendor quote before creating a purchase order.")
        if not self.x_psm_vendor_id:
            raise UserError("Please select a Vendor before creating a purchase order.")
        if self.x_psm_purchase_order_id and self.x_psm_purchase_order_id.state != "cancel":
            return self.action_psm_open_purchase_order()

        uom_unit = self.env.ref("uom.product_uom_unit", raise_if_not_found=False)
        if not uom_unit:
            raise UserError("Unit of Measure 'Units' was not found. Please configure UoM before creating the PO.")

        purchase_order = self.env["purchase.order"].create({
            "partner_id": self.x_psm_vendor_id.id,
            "origin": "%s - %s" % (self.name, self.x_psm_request_id.display_name),
            "company_id": self.x_psm_request_id.company_id.id,
            "currency_id": self.x_psm_vendor_quote_currency_id.id,
            "x_psm_0502_request_id": self.x_psm_request_id.id,
            "x_psm_0502_outside_service_request_id": self.id,
            "order_line": [(0, 0, {
                "name": self.x_psm_scope_of_work or self.display_name,
                "product_qty": 1.0,
                "product_uom_id": uom_unit.id,
                "price_unit": self.x_psm_vendor_quote_amount,
                "date_planned": self.x_psm_expected_complete_date or fields.Date.context_today(self),
            })],
        })
        self.write({
            "x_psm_purchase_order_id": purchase_order.id,
            "x_psm_state": "in_progress",
        })
        return self.action_psm_open_purchase_order()

    def action_psm_open_purchase_order(self):
        self.ensure_one()
        if not self.x_psm_purchase_order_id:
            raise UserError("No purchase order has been created for this outside service request yet.")
        return {
            "type": "ir.actions.act_window",
            "name": "Outside Service Purchase Order",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": self.x_psm_purchase_order_id.id,
            "target": "current",
        }

    def action_psm_mark_completed(self):
        for record in self:
            if record.x_psm_state not in ("approved", "in_progress"):
                raise UserError("Only approved or in-progress outside service requests can be marked completed.")
            record.write({"x_psm_state": "completed"})

    def action_psm_acceptance_review(self):
        for record in self:
            if record.x_psm_state != "completed":
                raise UserError("Please mark the outside service as completed before acceptance review.")
            if not record.x_psm_acceptance_result:
                raise UserError("Please select Vendor Service Acceptance Result.")
            if not record.x_psm_acceptance_note:
                raise UserError("Please fill in Acceptance Note.")

            request = record.x_psm_request_id
            request_values = {
                "x_psm_0502_acceptance_result": "accepted" if record.x_psm_acceptance_result == "accepted" else "follow_up_needed",
                "x_psm_0502_acceptance_note": record.x_psm_acceptance_note,
            }
            # prefill ket qua thiet bi sau dich vu ngoai de store khong phai nhap lai field nay khi nghiem thu request
            if record.x_psm_acceptance_result == "accepted" and not request.x_psm_0502_acceptance_equipment_result:
                request_values["x_psm_0502_acceptance_equipment_result"] = "operating_normally"
            if record.x_psm_acceptance_result != "accepted":
                request_values["x_psm_0502_acceptance_follow_up_note"] = record.x_psm_acceptance_note

            request.write(request_values)
            # nhac store hoan tat cac field nghiem thu con thieu truoc khi dong request
            if request.x_psm_0502_acceptance_result == "accepted" and hasattr(request, "message_post"):
                request.message_post(
                    body=(
                        "Outside service has been accepted. Please complete the Store Acceptance Contact "
                        "and Role on the maintenance request, then click Mark Acceptance Reviewed to close it."
                    )
                )
            record.write({"x_psm_state": "accepted" if record.x_psm_acceptance_result == "accepted" else "completed"})

    def action_psm_cancel(self):
        for record in self:
            if record.x_psm_state == "accepted":
                raise UserError("Accepted outside service requests cannot be cancelled.")
            record.write({"x_psm_state": "cancelled"})
