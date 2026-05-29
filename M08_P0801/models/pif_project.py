from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_psm_0801_pif_status = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
    ], string='PIF Status', default='draft', tracking=True)

    x_psm_0801_pif_product_type = fields.Selection([
        ('finished', 'Finished Product'),
        ('raw', 'Raw Material'),
    ], string='PIF Type', default='finished', tracking=True)

    x_psm_0801_pif_bom_id = fields.Many2one('mrp.bom', string='PIF BOM/Formula',
                                 domain="[('product_tmpl_id', '=', id)]",
                                 help="Select the main Formula/BOM for this PIF project.")

    x_psm_0801_wrin_code = fields.Char(string='WRIN Code')
    x_psm_0801_gri_code = fields.Char(string='GRI Code')


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    x_psm_0801_pif_status = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
    ], string='PIF Status', default='draft')


class PifRequestRawLine(models.Model):
    _name = 'x_psm_pif_request_raw_line'
    _description = 'PIF Request Raw Material'

    x_psm_request_id = fields.Many2one('approval.request', string='Request', ondelete='cascade')

    x_psm_gri_code = fields.Char(string='GRI')
    x_psm_wrin_code = fields.Char(string='WRIN')
    x_psm_product_id = fields.Many2one('product.product', string='Raw Item Name')
    x_psm_quantity = fields.Float(string='Quantity')
    x_psm_uom_id = fields.Many2one('uom.uom', string='UoM')
