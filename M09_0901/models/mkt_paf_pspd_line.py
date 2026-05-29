# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PafPspdLine(models.Model):
    _name = 'mkt_paf.pspd.line'
    _description = 'PAF Per-Store Per-Day Forecast'
    _order = 'paf_request_id, store_id, date'

    paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='PAF Request',
        required=True,
        ondelete='cascade',
        index=True,
    )
    store_id = fields.Many2one(
        'pos.config',
        string='Store',
        required=True,
        index=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        index=True,
    )
    forecast_qty = fields.Float(
        string='Forecast Qty',
        required=True,
        default=0.0,
    )
    forecast_revenue = fields.Monetary(
        string='Forecast Revenue',
        required=True,
        default=0.0,
        currency_field='currency_id',
    )
    weight_factor = fields.Float(
        string='Weight Factor',
        help='Weight used for distribution algorithms',
        default=1.0,
    )
    # Currency inherited from request via related field for convenience
    currency_id = fields.Many2one(
        'res.currency',
        related='paf_request_id.currency_id',
        store=True,
        readonly=True,
    )

    @api.model
    def _cron_pspd_refresh(self):
        _logger.info('PAF PSPD refresh cron executed')
        return True

    @api.model
    def _cron_sla_reminder(self):
        today = fields.Date.context_today(self)
        requests = self.env['mkt_paf.request'].search([
            ('state', 'in', ['draft', 'dept_evaluation', 'head_approval', 'clevel_approval']),
            ('paf_effective_start_date', '<=', today),
            ('planned_start_date', '>=', today),
            ('regulatory_sla_days', '>', 0),
        ])
        for request in requests:
            request.message_post(body=_(
                "PAF is inside the Legal SLA window. Planned start date: %s, required SLA days: %s."
            ) % (request.planned_start_date, request.regulatory_sla_days))
        return True
