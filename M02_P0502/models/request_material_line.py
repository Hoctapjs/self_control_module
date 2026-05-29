from odoo import api, fields, models


class X0502RequestMaterialLine(models.Model):
    _name = "x_psm_request_material_line"
    _description = "0502 Request Material Line"
    _order = "x_psm_sequence, id"

    x_psm_sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Sequence used to order the structured material assessment lines.",
    )

    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
        help="0502 maintenance request that this structured material line belongs to.",
    )

    x_psm_product_id = fields.Many2one(
        "product.product",
        string="Material",
        required=True,
        ondelete="restrict",
        help="Material or spare part identified during the material assessment step.",
    )

    x_psm_estimated_qty = fields.Float(
        string="Estimated Quantity",
        required=True,
        default=1.0,
        digits="Product Unit of Measure",
        help="Estimated quantity required for the material assessment step.",
    )

    x_psm_uom_id = fields.Many2one(
        "uom.uom",
        string="UoM",
        related="x_psm_product_id.uom_id",
        store=True,
        readonly=True,
        help="Default unit of measure taken from the selected material.",
    )

    x_psm_currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="x_psm_request_id.x_psm_0502_currency_id",
        store=True,
        readonly=True,
        help="Currency used to estimate the material line value.",
    )

    # field gia du kien cho phep user dieu chinh thay vi chi lay cost san pham
    x_psm_estimated_unit_price = fields.Monetary(
        string="Estimated Unit Price",
        currency_field="x_psm_currency_id",
        help="Estimated unit price used by the 0502 material approval rule.",
    )

    # field tong tien du kien cua tung dong vat tu de user kiem tra nhanh
    x_psm_estimated_subtotal = fields.Monetary(
        string="Estimated Subtotal",
        currency_field="x_psm_currency_id",
        compute="_compute_x_psm_estimated_subtotal",
        store=True,
        readonly=True,
        help="Estimated material subtotal calculated from unit price and quantity.",
    )

    x_psm_source_type = fields.Selection(
        selection=[
            ("warehouse_stock", "Warehouse Stock"),
            ("store_spare", "Store Spare"),
            ("technician_stock", "Technician Stock"),
            ("purchase", "External Purchase"),
            ("other", "Other"),
        ],
        string="Expected Source",
        required=True,
        help="Expected source from which the material is intended to be supplied.",
    )

    x_psm_note = fields.Char(
        string="Line Note",
        help="Short note describing the usage or special context of the material line.",
    )

    @api.depends("x_psm_estimated_unit_price", "x_psm_estimated_qty")
    def _compute_x_psm_estimated_subtotal(self):
        for line in self:
            line.x_psm_estimated_subtotal = (
                (line.x_psm_estimated_unit_price or 0.0)
                * (line.x_psm_estimated_qty or 0.0)
            )

    @api.onchange("x_psm_product_id")
    def _onchange_x_psm_product_id_set_estimated_unit_price(self):
        for line in self:
            if line.x_psm_product_id and not line.x_psm_estimated_unit_price:
                line.x_psm_estimated_unit_price = line.x_psm_product_id.standard_price

    @api.model_create_multi
    def create(self, vals_list):
        product_model = self.env["product.product"]
        for vals in vals_list:
            if vals.get("x_psm_product_id") and not vals.get("x_psm_estimated_unit_price"):
                product = product_model.browse(vals["x_psm_product_id"])
                vals["x_psm_estimated_unit_price"] = product.standard_price
        return super().create(vals_list)
