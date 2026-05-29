# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PafValuationReport(models.Model):
    _name = 'mkt_paf.valuation.report'
    _description = 'PAF Valuation Report'
    _inherit = ['mail.thread']
    _order = 'report_date desc, id desc'

    paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='PAF Request',
        required=True,
        ondelete='cascade',
        index=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='paf_request_id.currency_id',
        string='Tiền tệ'
    )

    actual_revenue = fields.Monetary(
        string='Doanh thu thực tế',
        currency_field='currency_id',
        tracking=True
    )

    actual_cost = fields.Monetary(
        string='Chi phí thực tế',
        currency_field='currency_id',
        tracking=True
    )

    actual_roi_percent = fields.Float(
        string='Tỷ suất ROI thực tế (%)',
        compute='_compute_valuation_stats',
        store=True,
        tracking=True
    )

    variance_vs_forecast = fields.Float(
        string='Chênh lệch ROI vs Dự báo (%)',
        compute='_compute_valuation_stats',
        store=True,
        tracking=True
    )

    summary_html = fields.Html(
        string='Tóm tắt đánh giá',
        tracking=True
    )

    report_date = fields.Date(
        string='Ngày báo cáo',
        default=fields.Date.today,
        required=True
    )

    status = fields.Selection([
        ('draft', 'Nháp'),
        ('published', 'Đã công bố')
    ], string='Trạng thái', default='draft', tracking=True)

    _sql_constraints = [
        ('paf_request_uniq', 'unique(paf_request_id)', 'Mỗi yêu cầu PAF chỉ được có một báo cáo Valuation!')
    ]

    @api.depends('actual_revenue', 'actual_cost', 'paf_request_id.roi_percent')
    def _compute_valuation_stats(self):
        for rec in self:
            if rec.actual_cost:
                rec.actual_roi_percent = (rec.actual_revenue - rec.actual_cost) / rec.actual_cost * 100.0
            else:
                rec.actual_roi_percent = 0.0
            rec.variance_vs_forecast = rec.actual_roi_percent - (rec.paf_request_id.roi_percent or 0.0)

    def action_publish(self):
        self.ensure_one()
        if self.status != 'draft':
            raise ValidationError(_("Báo cáo đã được công bố trước đó."))
        self.write({'status': 'published'})
        # Move parent PAF state to done
        self.paf_request_id.write({'state': 'done'})
        return True
