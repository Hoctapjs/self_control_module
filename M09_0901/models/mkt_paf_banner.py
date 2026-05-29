# -*- coding: utf-8 -*-
import base64
import io
import re

from PIL import Image

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class PafBanner(models.Model):
    _name = 'mkt_paf.banner'
    _description = 'PAF Marketing Banner'
    _inherit = ['mail.thread']
    _order = 'paf_request_id, sequence, id'

    paf_request_id = fields.Many2one(
        'mkt_paf.request',
        string='PAF Request',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Tên banner', required=True, tracking=True)
    image = fields.Image(string='Ảnh banner', required=True, max_width=3840, max_height=3840)
    image_filename = fields.Char(string='Tên file')
    purpose = fields.Selection([
        ('pos_display', 'POS Display'),
        ('sok_display', 'SOK Display'),
        ('dt_menu', 'DT/DMB Menu'),
        ('mop_app', 'MOP App'),
        ('social_fb', 'Social Facebook'),
        ('social_ig', 'Social Instagram'),
        ('printed', 'Printed'),
        ('digital_web', 'Digital Web'),
        ('other', 'Khác'),
    ], string='Mục đích', required=True, default='pos_display', tracking=True)
    platform_id = fields.Many2one('x_psm_pif_platform', string='Platform')
    language = fields.Selection([
        ('vi', 'Tiếng Việt'),
        ('en', 'English'),
        ('multi', 'Đa ngôn ngữ'),
    ], string='Ngôn ngữ', required=True, default='vi', tracking=True)
    target_dimensions = fields.Char(string='Kích thước mục tiêu')
    target_dpi = fields.Integer(string='DPI mục tiêu', default=72)
    actual_dimensions = fields.Char(
        string='Kích thước thực tế',
        compute='_compute_image_metadata',
        store=True,
    )
    file_size_kb = fields.Float(
        string='Dung lượng (KB)',
        compute='_compute_image_metadata',
        store=True,
    )
    status = fields.Selection([
        ('draft', 'Nháp'),
        ('brand_approved', 'Brand duyệt'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái', required=True, default='draft', tracking=True)
    approver_id = fields.Many2one('res.users', string='Người duyệt', readonly=True)
    approval_date = fields.Datetime(string='Ngày duyệt', readonly=True)
    rejection_reason = fields.Text(string='Lý do từ chối')
    notes = fields.Text(string='Ghi chú thiết kế')

    @api.depends('image')
    def _compute_image_metadata(self):
        for rec in self:
            rec.actual_dimensions = False
            rec.file_size_kb = 0.0
            if not rec.image:
                continue
            raw = base64.b64decode(rec.image)
            rec.file_size_kb = len(raw) / 1024.0
            try:
                with Image.open(io.BytesIO(raw)) as img:
                    rec.actual_dimensions = '%sx%s' % img.size
            except Exception:
                rec.actual_dimensions = False

    def _get_banner_max_size_mb(self):
        value = self.env['ir.config_parameter'].sudo().get_param(
            'mkt_0901.banner_max_size_mb',
            '4',
        )
        try:
            return float(value)
        except (TypeError, ValueError):
            return 4.0

    def _check_brand_reviewer(self):
        if self.env.user.has_group('M09_0901.MKT_0901_brand_reviewer') or self.env.user.has_group('M09_0901.MKT_0901_admin'):
            return
        raise AccessError(_("Bạn không có quyền duyệt banner Brand."))

    @api.constrains('image')
    def _check_image_file_size(self):
        max_kb = self._get_banner_max_size_mb() * 1024
        for rec in self:
            if rec.file_size_kb and rec.file_size_kb > max_kb:
                raise ValidationError(_("Dung lượng banner không được vượt quá %s MB.") % self._get_banner_max_size_mb())

    @api.constrains('target_dimensions')
    def _check_target_dimensions(self):
        pattern = re.compile(r'^\d+x\d+$')
        for rec in self:
            if rec.target_dimensions and not pattern.match(rec.target_dimensions):
                raise ValidationError(_("Kích thước mục tiêu phải có dạng WIDTHxHEIGHT, ví dụ 1920x1080."))

    @api.constrains('status', 'approver_id', 'rejection_reason')
    def _check_status_required_fields(self):
        for rec in self:
            if rec.status == 'brand_approved' and not rec.approver_id:
                raise ValidationError(_("Banner đã Brand duyệt phải có người duyệt."))
            if rec.status == 'rejected' and not rec.rejection_reason:
                raise ValidationError(_("Banner bị từ chối phải có lý do từ chối."))

    def action_brand_approve(self):
        for rec in self:
            rec._check_brand_reviewer()
            if rec.status != 'draft':
                raise ValidationError(_("Chỉ duyệt Brand được banner đang ở trạng thái Nháp."))
            rec.write({
                'status': 'brand_approved',
                'approver_id': self.env.user.id,
                'approval_date': fields.Datetime.now(),
                'rejection_reason': False,
            })
        return True

    def action_brand_reject(self):
        for rec in self:
            rec._check_brand_reviewer()
            if rec.status != 'draft':
                raise ValidationError(_("Chỉ từ chối được banner đang ở trạng thái Nháp."))
            if not rec.rejection_reason:
                raise ValidationError(_("Vui lòng nhập Lý do từ chối trước khi bấm Brand Reject."))
            rec.write({
                'status': 'rejected',
                'approver_id': self.env.user.id,
                'approval_date': fields.Datetime.now(),
            })
        return True

    def action_reset_draft(self):
        for rec in self:
            if rec.status != 'rejected':
                raise ValidationError(_("Chỉ reset được banner đang bị từ chối."))
            rec.write({
                'status': 'draft',
                'approver_id': False,
                'approval_date': False,
            })
        return True

    def write(self, vals):
        protected_status = {'brand_approved', 'rejected'}
        if 'status' in vals and vals['status'] in protected_status:
            self._check_brand_reviewer()
        if not self.env.user.has_group('M09_0901.MKT_0901_admin'):
            for rec in self:
                if rec.status != 'draft' and any(field not in ('status', 'approver_id', 'approval_date', 'rejection_reason') for field in vals):
                    raise AccessError(_("Chỉ được chỉnh sửa nội dung banner khi đang ở trạng thái Nháp."))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.status != 'draft' and not self.env.user.has_group('M09_0901.MKT_0901_admin'):
                raise ValidationError(_("Chỉ được xóa banner ở trạng thái Nháp."))
        return super().unlink()
