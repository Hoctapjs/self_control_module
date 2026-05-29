from odoo import models, fields, api, _


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    x_psm_0801_is_pif = fields.Boolean(
        string='Is PIF Process',
        help='If checked, approving a request of this category will create a PIF Object.',
    )


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    x_psm_0801_pif_object_id = fields.Many2one('x_psm_pif_object', string='Related PIF', copy=False)
    x_psm_0801_pif_object_count = fields.Integer(compute='_compute_pif_count')
    x_psm_0801_is_pif_category = fields.Boolean(related='category_id.x_psm_0801_is_pif')

    x_psm_0801_pif_request_type = fields.Selection([
        ('menu', 'Menu'),
        ('marketing', 'Marketing'),
        ('si', 'S&I'),
        ('digital', 'Digital'),
        ('supply_chain', 'Supply Chain'),
    ], string='Request Type', default='menu')

    x_psm_0801_pif_product_id = fields.Many2one(
        'product.product',
        string='Select Approved Product',
        domain="[('x_psm_0801_pif_status', '=', 'completed')]",
        help='Select a product that has been approved for PIF.',
    )

    x_psm_0801_pif_product_name = fields.Char(
        related='x_psm_0801_pif_product_id.name',
        string='Product Name',
        readonly=True,
    )
    x_psm_0801_pif_product_code = fields.Char(
        related='x_psm_0801_pif_product_id.default_code',
        string='Code/WRIN',
        readonly=True,
    )

    x_psm_0801_pif_vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        readonly=True,
        compute='_compute_from_product',
        store=True,
    )
    x_psm_0801_pif_bom_id = fields.Many2one(
        'mrp.bom',
        string='BOM',
        readonly=True,
        compute='_compute_from_product',
        store=True,
    )

    x_psm_0801_raw_item_ids = fields.One2many(
        'x_psm_pif_request_raw_line', 'x_psm_request_id', string='Raw Items', readonly=True,
    )

    x_psm_0801_request_owner_department_id = fields.Many2one(
        'hr.department', compute='_compute_owner_info', string='Department',
    )
    x_psm_0801_request_owner_job_id = fields.Many2one(
        'hr.job', compute='_compute_owner_info', string='Job Position',
    )

    @api.depends('request_owner_id')
    def _compute_owner_info(self):
        for rec in self:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', rec.request_owner_id.id)], limit=1,
            )
            rec.x_psm_0801_request_owner_department_id = employee.department_id if employee else False
            rec.x_psm_0801_request_owner_job_id = employee.job_id if employee else False

    @api.depends('x_psm_0801_pif_product_id')
    def _compute_from_product(self):
        for rec in self:
            if rec.x_psm_0801_pif_product_id:
                bom = self.env['mrp.bom'].search([
                    '|',
                    ('product_id', '=', rec.x_psm_0801_pif_product_id.id),
                    '&',
                    ('product_tmpl_id', '=', rec.x_psm_0801_pif_product_id.product_tmpl_id.id),
                    ('product_id', '=', False),
                ], limit=1, order='sequence, id')

                rec.x_psm_0801_pif_bom_id = bom

                seller = rec.x_psm_0801_pif_product_id.seller_ids[:1]
                rec.x_psm_0801_pif_vendor_id = seller.partner_id if seller else False
            else:
                rec.x_psm_0801_pif_vendor_id = False
                rec.x_psm_0801_pif_bom_id = False

    @api.onchange('x_psm_0801_pif_product_id')
    def _onchange_pif_product_id_populate(self):
        if not self.x_psm_0801_pif_product_id:
            self.x_psm_0801_raw_item_ids = [(5, 0, 0)]
            self.x_psm_0801_pif_vendor_id = False
            self.x_psm_0801_pif_bom_id = False
            return

        self._compute_from_product()

        lines = []
        if self.x_psm_0801_pif_bom_id:
            for bom_line in self.x_psm_0801_pif_bom_id.bom_line_ids:
                lines.append((0, 0, {
                    'x_psm_gri_code': bom_line.product_id.default_code,
                    'x_psm_wrin_code': '',
                    'x_psm_product_id': bom_line.product_id.id,
                    'x_psm_quantity': bom_line.product_qty,
                    'x_psm_uom_id': bom_line.product_uom_id.id,
                }))
        self.x_psm_0801_raw_item_ids = [(5, 0, 0)] + lines

    @api.model
    def default_get(self, fields_list):
        defaults = super(ApprovalRequest, self).default_get(fields_list)
        defaults['name'] = _('Request Creation PIF')
        defaults['request_owner_id'] = self.env.user.id
        return defaults

    @api.onchange('category_id')
    def _onchange_category_id_pif(self):
        if self.category_id.x_psm_0801_is_pif:
            self.name = _('Request Creation PIF')

    def _compute_pif_count(self):
        for rec in self:
            rec.x_psm_0801_pif_object_count = 1 if rec.x_psm_0801_pif_object_id else 0

    def action_confirm(self):
        res = super(ApprovalRequest, self).action_confirm()
        fast_track_types = {'digital', 'supply_chain'}
        for rec in self:
            if (
                rec.category_id.x_psm_0801_is_pif
                and rec.x_psm_0801_pif_request_type in fast_track_types
                and not rec.x_psm_0801_pif_object_id
            ):
                rec.action_approve()
        return res

    def action_approve(self, approver=None):
        super(ApprovalRequest, self).action_approve(approver=approver)
        for rec in self:
            if rec.category_id.x_psm_0801_is_pif and not rec.x_psm_0801_pif_object_id:
                fast_track = rec.x_psm_0801_pif_request_type in ('digital', 'supply_chain')
                pif_vals = {
                    'x_psm_approval_request_id': rec.id,
                    'x_psm_pif_request_type': rec.x_psm_0801_pif_request_type,
                    'x_psm_pif_product_id': rec.x_psm_0801_pif_product_id.id,
                    'x_psm_pif_bom_id': rec.x_psm_0801_pif_bom_id.id,
                    'x_psm_request_owner_id': rec.request_owner_id.id,
                    'x_psm_request_owner_department_id': rec.x_psm_0801_request_owner_department_id.id,
                    'x_psm_request_owner_job_id': rec.x_psm_0801_request_owner_job_id.id,
                }
                if fast_track:
                    pif_vals.update({
                        'state': 'it_config',
                        'x_psm_pif_size': 'adhoc',
                    })
                pif = self.env['x_psm_pif_object'].create(pif_vals)
                if fast_track:
                    pif._complete_step('1_')
                rec.x_psm_0801_pif_object_id = pif.id

    def action_open_pif(self):
        self.ensure_one()
        return {
            'name': _('PIF Execution'),
            'type': 'ir.actions.act_window',
            'res_model': 'x_psm_pif_object',
            'res_id': self.x_psm_0801_pif_object_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
