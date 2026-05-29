# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    block_id = fields.Many2one(
        'department.block',
        string='Khối',
        help='Khối phòng ban: Văn phòng (RST) hoặc Vận hành (OPS)',
    )
    block_code = fields.Char(
        related='block_id.code',
        string='Mã Khối',
        store=False,
    )
    pos_config_id = fields.Many2one(
        'pos.config',
        string='POS',
        help='Cửa hàng POS gắn với phòng ban (chỉ dành cho khối OPS)',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Tài Khoản',
        help='Tài khoản người dùng gắn với phòng ban/cửa hàng (quan hệ 1-1)',
        copy=False,
    )
    x_psm_state_id = fields.Many2one(
        'res.country.state',
        string='Tỉnh/Thành phố',
        domain="[('country_id.code', '=', 'VN')]",
    )
    x_psm_region = fields.Selection(
        related='x_psm_state_id.x_psm_region',
        string='Vùng',
        store=True,
    )
    x_psm_0200_salary_region_id = fields.Many2one(
        related='x_psm_state_id.x_psm_0200_salary_region_id',
        string='Vùng lương',
        store=True,
        readonly=True,
    )

    # === Store Identity & Location ===
    x_psm_store_number = fields.Char(
        string='Mã Store Number',
        help='Mã Store Department nội bộ Odoo (x_psm_store_number)',
        copy=False,
    )
    x_psm_store_code = fields.Char(
        string='Mã Hệ Thống Cũ (StoreCode)',
        help='Mã cửa hàng dùng trong hệ thống legacy (StoreCode)',
        copy=False,
    )
    x_psm_gbl_store_id = fields.Char(
        string='Mã Cửa Hàng GBL (Store Id)',
        help='Mã định danh cửa hàng toàn cầu GBL',
        copy=False,
    )
    x_psm_store_name = fields.Char(
        string='Tên Cửa Hàng (StoreName)',
        help='Tên cửa hàng theo hệ thống gốc (StoreName)',
    )
    x_psm_active = fields.Boolean(
        string='Đang Hoạt Động',
        default=True,
        help='Tình trạng hoạt động của cửa hàng (Inactive → False)',
    )
    x_psm_country = fields.Char(
        string='Quốc Gia',
        help='Quốc gia của cửa hàng (Country)',
    )
    x_psm_province = fields.Char(
        string='Tỉnh Thành',
        help='Tỉnh/Thành phố của cửa hàng (Province)',
    )
    x_psm_store_email = fields.Char(
        string='Email Cửa Hàng',
        help='Địa chỉ email chính thức của cửa hàng (StoreEmail)',
    )

    # === Peak Hours ===
    x_psm_break_first_peak_from = fields.Float(
        string='Cao Điểm Sáng (Từ)',
        help='Giờ bắt đầu cao điểm buổi sáng, ví dụ: 7.5 = 07:30 (BreakFirstPeakFrom)',
        digits=(4, 2),
    )
    x_psm_break_first_peak_to = fields.Float(
        string='Cao Điểm Sáng (Đến)',
        help='Giờ kết thúc cao điểm buổi sáng (BreakFirstPeakTo)',
        digits=(4, 2),
    )
    x_psm_lunch_peak_from = fields.Float(
        string='Cao Điểm Trưa (Từ)',
        help='Giờ bắt đầu cao điểm buổi trưa (LunchPeakFrom)',
        digits=(4, 2),
    )
    x_psm_lunch_peak_to = fields.Float(
        string='Cao Điểm Trưa (Đến)',
        help='Giờ kết thúc cao điểm buổi trưa (LunchPeakTo)',
        digits=(4, 2),
    )
    x_psm_dinner_peak_from = fields.Float(
        string='Cao Điểm Tối (Từ)',
        help='Giờ bắt đầu cao điểm buổi tối (DinnerPeakFrom)',
        digits=(4, 2),
    )
    x_psm_dinner_peak_to = fields.Float(
        string='Cao Điểm Tối (Đến)',
        help='Giờ kết thúc cao điểm buổi tối (DinnerPeakTo)',
        digits=(4, 2),
    )

    # === Legacy System Codes ===
    x_psm_sap_code = fields.Char(
        string='Mã SAP Cũ (SAPCode)',
        help='Mã định danh cửa hàng trong hệ thống SAP cũ',
        copy=False,
    )
    x_psm_cadena_code = fields.Char(
        string='Mã Cadena Cũ (CadenaCode)',
        help='Mã định danh cửa hàng trong hệ thống Cadena cũ',
        copy=False,
    )
    x_psm_cadena_name = fields.Char(
        string='Tên Cadena Cũ (CadenaName)',
        help='Tên cửa hàng theo hệ thống Cadena cũ',
    )
    x_psm_oc_group_id = fields.Char(
        string='Nhóm Tư Vấn Cửa Hàng (OCGroup_Id)',
        help='Mã nhóm tư vấn vận hành (Operation Consultant Group)',
    )

    # === Invoice Information ===
    x_psm_address_iv = fields.Char(
        string='Địa Chỉ Xuất Hóa Đơn (AddressIV)',
        help='Địa chỉ dùng khi xuất hóa đơn GTGT',
    )
    x_psm_store_name_iv = fields.Char(
        string='Tên Cửa Hàng Xuất Hóa Đơn (StoreNameIV)',
        help='Tên cửa hàng hiển thị trên hóa đơn GTGT',
    )
    x_psm_invoice_code = fields.Char(
        string='Mã Hóa Đơn (InvoiceCode)',
        help='Mã ký hiệu hóa đơn chính thức',
        copy=False,
    )
    x_psm_invoice_code_temp = fields.Char(
        string='Mã Hóa Đơn Nháp (InvoiceCodeTemp)',
        help='Mã ký hiệu hóa đơn tạm (draft)',
        copy=False,
    )

    _sql_constraints = [
        ('user_id_uniq', 'UNIQUE(user_id)',
         'Mỗi tài khoản chỉ được gắn với một phòng ban duy nhất!'),
    ]

    @api.onchange('block_id')
    def _onchange_block_id(self):
        """Xóa POS khi chuyển khối không phải OPS."""
        if not self.block_id or self.block_id.code != 'OPS':
            self.pos_config_id = False

    def action_generate_positions(self):
        """Tạo các vị trí công việc (hr.job) dựa trên danh sách mặc định
        của khối mà phòng ban thuộc về. Bỏ qua các vị trí đã tồn tại
        (kiểm tra theo code + department_id)."""
        self.ensure_one()
        if not self.block_id:
            raise UserError(_(
                'Phòng ban "%s" chưa được gắn khối. '
                'Vui lòng chọn khối trước khi tạo vị trí công việc.',
                self.name,
            ))

        defaults = self.env['hr.job.position.default'].search([
            ('block_id', '=', self.block_id.id),
        ])
        if not defaults:
            raise UserError(_(
                'Không tìm thấy vị trí mặc định nào cho khối "%s".',
                self.block_id.name,
            ))

        # Lấy danh sách code đã tồn tại cho phòng ban này
        existing_keys = {
            (job.code, job.contract_type_id.id or False)
            for job in self.env['hr.job'].search([('department_id', '=', self.id)])
        }
        created_count = 0
        for default_pos in defaults:
            contract_types = default_pos.contract_type_ids or self.env['hr.contract.type']
            contract_type_ids = contract_types.ids or [False]
            for contract_type_id in contract_type_ids:
                key = (default_pos.code, contract_type_id)
                if key in existing_keys:
                    continue
                contract_type = self.env['hr.contract.type'].browse(contract_type_id) if contract_type_id else False
                job_name = (
                    f"{default_pos.name} - {contract_type.name}"
                    if contract_type else default_pos.name
                )
                self.env['hr.job'].create({
                    'name': job_name,
                    'code': default_pos.code,
                    'level_id': default_pos.level_id.id if default_pos.level_id else False,
                    'department_id': self.id,
                    'job_default_id': default_pos.id,
                    'contract_type_id': contract_type_id,
                })
                existing_keys.add(key)
                created_count += 1

        if created_count == 0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Thông báo'),
                    'message': _(
                        'Tất cả vị trí công việc đã tồn tại cho phòng ban "%s".',
                        self.name,
                    ),
                    'type': 'warning',
                    'sticky': False,
                },
            }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _(
                    'Đã tạo %d vị trí công việc cho phòng ban "%s".',
                    created_count, self.name,
                ),
                'type': 'success',
                'sticky': False,
            },
        }
