# Khai bao ma hoa file Python
# -*- coding: utf-8 -*-

from odoo import fields, models


class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    # field cau hinh ro user nao dong vai tro CMT Lead cho flow preventive 0502
    x_psm_0502_lead_user_id = fields.Many2one(
        "res.users",
        string="0502 Lead User",
        tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]",
        help="Preferred user to receive 0502 preventive lead notifications for this maintenance team.",
    )

    # field cau hinh ro user nao la nguoi duyet de xuat xu ly/timeline/cost cho nhom 0502
    x_psm_0502_proposal_approver_id = fields.Many2one(
        "res.users",
        string="0502 Proposal Approver",
        tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]",
        help="Preferred user to approve the 0502 treatment proposal for this maintenance team.",
    )

    # field tien te dung de hien thi nguong auto approve theo dong tien cong ty cua team
    x_psm_0502_currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        string="Currency",
        store=True,
        readonly=True,
    )

    # field cau hinh nguong chi phi duoi muc nay thi de xuat co the auto approve
    x_psm_0502_proposal_auto_approve_limit = fields.Monetary(
        string="0502 Auto Approve Limit",
        currency_field="x_psm_0502_currency_id",
        help="Treatment proposals at or below this amount can be auto approved in the 0502 flow.",
    )

    # field cau hinh user noi bo phu trach duyet nhanh vat tu cho nhanh xuat kho 0502
    x_psm_0502_material_approver_id = fields.Many2one(
        "res.users",
        string="0502 Material Approver",
        tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]",
        help="Preferred internal approver for 0502 material issue requests on this maintenance team.",
    )

    # field cau hinh nguong gia tri vat tu duoi muc nay thi co the auto approve trong nhanh kho noi bo
    x_psm_0502_material_auto_approve_limit = fields.Monetary(
        string="0502 Material Auto Approve Limit",
        currency_field="x_psm_0502_currency_id",
        help="Material issue requests at or below this amount can be auto approved in the 0502 internal stock flow.",
    )

    # field cau hinh nha cung cap goi y cho nhanh mua ngoai khi thieu vat tu
    x_psm_0502_default_vendor_id = fields.Many2one(
        "res.partner",
        string="0502 Default Vendor",
        tracking=True,
        domain="[('supplier_rank', '>', 0)]",
        help="Preferred vendor suggested when 0502 opens an RFQ for outside material purchase.",
    )

    # field cau hinh operation type kho noi bo uu tien cho nhanh vat tu 0502
    x_psm_0502_material_picking_type_id = fields.Many2one(
        "stock.picking.type",
        string="0502 Material Picking Type",
        tracking=True,
        domain="[('code', '=', 'internal')]",
        help="Preferred internal operation type used when 0502 creates a stock picking from material detail lines.",
    )

    # field cau hinh location nguon uu tien cho nhanh xuat vat tu 0502
    x_psm_0502_material_source_location_id = fields.Many2one(
        "stock.location",
        string="0502 Material Source Location",
        tracking=True,
        help="Preferred source location used when 0502 creates an internal stock picking.",
    )

    # field cau hinh location dich uu tien cho nhanh xuat vat tu 0502
    x_psm_0502_material_destination_location_id = fields.Many2one(
        "stock.location",
        string="0502 Material Destination Location",
        tracking=True,
        help="Preferred destination location used when 0502 creates an internal stock picking.",
    )

    # field cau hinh SLA tiep nhan theo gio cho intake 0502
    x_psm_0502_intake_sla_hours = fields.Float(
        string="0502 Intake SLA Hours",
        help="Expected maximum number of hours from request entry into the system until CMT intake receives it.",
    )
