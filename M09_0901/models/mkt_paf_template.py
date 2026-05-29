# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PafTemplate(models.Model):
    _name = 'mkt_paf.template'
    _description = 'PAF Template'
    _inherit = ['mail.thread']
    _order = 'name, id'

    name = fields.Char(
        string='Tên Template',
        required=True,
        tracking=True
    )

    code = fields.Char(
        string='Mã Template',
        required=True,
        tracking=True
    )

    description_html = fields.Html(
        string='Mô tả'
    )

    default_loyalty_program_id = fields.Many2one(
        'loyalty.program',
        string='Loyalty Program (Scheme)'
    )

    default_product_ids = fields.Many2many(
        'product.template',
        'mkt_paf_template_product_rel',
        'template_id',
        'product_tmpl_id',
        string='Sản phẩm mặc định',
        domain=[('paf_can_use', '=', True)]
    )

    default_promotion_type = fields.Selection([
        ('discount_direct', 'Giảm giá trực tiếp'),
        ('gift_attached', 'Tặng quà kèm'),
        ('lucky_draw', 'Bốc thăm trúng thưởng'),
    ], string='Hình thức khuyến mãi mặc định', default='gift_attached', required=True, tracking=True)

    default_promotion_legal_form = fields.Selection([
        ('notification', 'Thông báo'),
        ('registration', 'Đăng ký'),
    ], string='Hồ sơ pháp lý mặc định', default='notification', required=True, tracking=True)

    default_eligible_channel_ids = fields.Many2many(
        'x_psm_pif_platform',
        'mkt_paf_template_pif_platform_rel',
        'template_id',
        'platform_id',
        string='Kênh áp dụng mặc định'
    )

    default_max_uses_per_customer = fields.Integer(
        string='Số lượt tối đa/khách mặc định',
        default=0
    )

    default_time_window_start = fields.Float(
        string='Giờ bắt đầu mặc định',
        default=0.0
    )

    default_time_window_end = fields.Float(
        string='Giờ kết thúc mặc định',
        default=24.0
    )

    default_food_safety_responsible_dept_id = fields.Many2one(
        'hr.department',
        string='Phòng phụ trách ATTP mặc định'
    )

    default_description_legal_html = fields.Html(
        string='Mô tả pháp lý mặc định'
    )

    required_dept_evaluation = fields.Many2many(
        'hr.department',
        'mkt_paf_template_dept_rel',
        'template_id',
        'dept_id',
        string='Phòng ban đánh giá'
    )

    active = fields.Boolean(
        string='Đang hoạt động',
        default=True,
        tracking=True
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Mã template phải là duy nhất!')
    ]

    @api.onchange('default_promotion_type')
    def _onchange_default_promotion_type(self):
        for rec in self:
            if rec.default_promotion_type == 'lucky_draw':
                rec.default_promotion_legal_form = 'registration'
            elif not rec.default_promotion_legal_form:
                rec.default_promotion_legal_form = 'notification'
