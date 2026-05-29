# -*- coding: utf-8 -*-
from odoo import models, api


class PifObject(models.Model):
    _inherit = 'x_psm_pif_object'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            req = rec.x_psm_approval_request_id
            if req and req.x_psm_mkt_paf_request_id:
                paf = req.x_psm_mkt_paf_request_id
                vals = {'state': 'pif_running'}
                vals['pif_object_id'] = rec.id
                paf.write(vals)
                paf._sync_banners_to_pif(rec)
        return records
