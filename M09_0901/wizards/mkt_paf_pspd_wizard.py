# -*- coding: utf-8 -*-
"""Wizard to distribute PSPD forecast per store per day.
Implements simple even distribution and placeholder for weighted algorithms.
"""
import logging
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PafPspdWizard(models.TransientModel):
    _name = 'mkt_paf.pspd.wizard'
    _description = 'Wizard for PSPD distribution'

    paf_request_id = fields.Many2one('mkt_paf.request', string='PAF Request', required=True)
    algorithm = fields.Selection([
        ('even', 'Even distribution'),
        ('by_pos_weight', 'By POS weight'),
        ('by_history', 'By historical sales')
    ], string='Algorithm', default='even', required=True)
    total_target_qty = fields.Float(string='Total target quantity', required=True)

    def action_distribute(self):
        self.ensure_one()
        request = self.paf_request_id
        if not request:
            raise ValidationError(_('No PAF Request selected'))
        # Basic validation
        if not request.planned_start_date or not request.planned_end_date:
            raise ValidationError(_('PAF must have planned start and end dates'))
        # Determine store list
        stores = request.target_store_ids or self.env['pos.config'].search([])
        if not stores:
            raise ValidationError(_('No stores found for distribution'))
        # Compute date range
        start = fields.Date.from_string(request.planned_start_date)
        end = fields.Date.from_string(request.planned_end_date)
        delta_days = (end - start).days + 1
        if delta_days <= 0:
            raise ValidationError(_('Planned end date must be after start date'))
        weights = self._get_distribution_weights(stores, start)
        total_weight = sum(weights.values()) or len(stores)
        lines_vals = []
        for store in stores:
            qty_per_line = (self.total_target_qty * weights.get(store.id, 1.0) / total_weight) / delta_days
            current_date = start
            while current_date <= end:
                lines_vals.append({
                    'paf_request_id': request.id,
                    'store_id': store.id,
                    'date': fields.Date.to_string(current_date),
                    'forecast_qty': qty_per_line,
                    'forecast_revenue': 0.0,
                    'weight_factor': 1.0,
                })
                current_date += timedelta(days=1)
        # Clean existing lines if any (optional)
        request.env['mkt_paf.pspd.line'].search([('paf_request_id', '=', request.id)]).unlink()
        self.env['mkt_paf.pspd.line'].create(lines_vals)
        _logger.info('Created %d PSPD lines for request %s', len(lines_vals), request.name)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _get_distribution_weights(self, stores, start_date):
        self.ensure_one()
        if self.algorithm == 'by_pos_weight':
            return self._get_pos_config_weights(stores)
        if self.algorithm == 'by_history':
            return self._get_history_weights(stores, start_date)
        return {store.id: 1.0 for store in stores}

    def _get_pos_config_weights(self, stores):
        weight_fields = ('paf_weight_factor', 'pspd_weight_factor', 'weight_factor')
        weights = {}
        for store in stores:
            weight = 0.0
            for field_name in weight_fields:
                if field_name in store._fields:
                    weight = store[field_name] or 0.0
                    break
            weights[store.id] = weight if weight > 0 else 1.0
        return weights

    def _get_history_weights(self, stores, start_date):
        PosOrder = self.env['pos.order']
        history_start = start_date - timedelta(days=90)
        grouped = PosOrder.read_group(
            [
                ('config_id', 'in', stores.ids),
                ('date_order', '>=', fields.Date.to_string(history_start)),
                ('date_order', '<', fields.Date.to_string(start_date)),
            ],
            ['amount_total:sum'],
            ['config_id'],
        )
        weights = {store.id: 0.0 for store in stores}
        for group in grouped:
            config = group.get('config_id')
            if config:
                weights[config[0]] = max(group.get('amount_total', 0.0), 0.0)
        if not sum(weights.values()):
            return {store.id: 1.0 for store in stores}
        return weights
