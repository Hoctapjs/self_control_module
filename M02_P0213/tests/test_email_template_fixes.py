# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

"""
TEST FILE: Test email template fixes (Phase 1-4)
Kiểm tra các lỗi đã sửa trong email template module 0213

Phase 1: Màu nền (background-color + background-image)
Phase 2: Placeholder ({{ }} → <t t-out>)
Phase 3: Border-left sub-property + lang/auto_delete
"""

from odoo.addons.mail.tests.common import MailCommon
from odoo.tests import tagged


@tagged('M02_P0213', 'email_template', 'phase_1_2_3_4')
class TestEmailTemplateFixes(MailCommon):
    """
    Test Phase 1-4 fixes cho email template module 0213

    Lỗi cần fix:
    1. Header gradient biến mất ở Outlook + Chatter (màu nền)
    2. Placeholder {{ }} không render trong body (QWeb)
    3. Border-left shorthand bị lọc ở chatter (sanitizer)
    """

    @classmethod
    def setUpClass(cls):
        """Chuẩn bị test data"""
        super().setUpClass()

        # Tạo employee test
        cls.test_employee = cls.env['hr.employee'].create({
            'name': 'Huỳnh Thanh Sơn',
            'barcode': 'EMP123',
            'department_id': cls.env.ref('base.main_company').id,
            'job_id': cls.env.ref('base.job_position_position_open').id,
        })

        # Tạo approval request (Resignation)
        resignation_category = cls.env['approval.request'].search(
            [('category_id.name', 'ilike', 'Resignation')], limit=1
        )
        if not resignation_category:
            # Fallback: tạo category nếu không có
            resignation_category = cls.env['approval.category'].create({
                'name': 'Resignation',
            })
        else:
            resignation_category = resignation_category.category_id

        cls.test_approval = cls.env['approval.request'].create({
            'category_id': resignation_category.id if resignation_category else False,
            'x_psm_0213_employee_id': cls.test_employee.id,
            'request_owner_id': cls.user_admin.partner_id.id,
        })

    def _render_template_body(self, template_ref):
        """
        Helper: Render email template body HTML

        Args:
            template_ref (str): Template XML ID (e.g., 'M02_P0213.psm_0213_email_template_...')

        Returns:
            str: Rendered HTML body
        """
        try:
            template = self.env.ref(template_ref)
        except ValueError:
            self.skipTest(f"Template {template_ref} not found")
            return ""

        rendered_dict = template._render_template(
            template.body_html,
            'approval.request',
            [self.test_approval.id],
            engine='qweb'
        )
        return rendered_dict.get(self.test_approval.id, "")

    # ========== PHASE 1: MÀUI NỀN ==========

    def test_phase1_dept_reminder_header_gradient_and_color(self):
        """
        Phase 1: dept_offboarding_reminder header phải có background-color + background-image

        Lỗi: Header dùng `background:linear-gradient(...)` không có fallback color
        → Outlook không support gradient → nền mất → chữ trắng vô hình

        Fix: Đổi thành `background-color:#b5121b;background-image:linear-gradient(...)`
        → Outlook dùng fallback color (#b5121b), Gmail dùng gradient
        """
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        # Assert 1: Header PHẢI có background-color fallback
        self.assertIn(
            'background-color:#b5121b',
            rendered,
            "❌ FAIL: Header PHẢI có background-color:#b5121b (fallback cho Outlook)\n"
            "   Expected: background-color:#b5121b;background-image:linear-gradient(...)\n"
            "   Problem: Outlook không support gradient → cần fallback color"
        )

        # Assert 2: Header PHẢI có background-image gradient
        self.assertIn(
            'background-image:linear-gradient',
            rendered,
            "❌ FAIL: Header PHẢI có background-image gradient\n"
            "   Expected: background-image:linear-gradient(135deg,...)\n"
            "   Problem: Gmail/modern clients cần gradient"
        )

        # Assert 3: KHÔNG dùng shorthand `background:linear-gradient`
        self.assertNotIn(
            'background:linear-gradient',
            rendered,
            "❌ FAIL: KHÔNG được dùng shorthand `background:linear-gradient`\n"
            "   Reason: Không có fallback color → Outlook fails\n"
            "   Fix: Thay thành background-color + background-image"
        )

        # Assert 4: Nền đặc cũng phải dùng background-color (không shorthand)
        # Kiểm tra các box khác không dùng `background:#` shorthand
        lines_with_background_shorthand = [
            line for line in rendered.split('\n')
            if 'background:#' in line and 'background-color:' not in line
        ]
        self.assertEqual(
            len(lines_with_background_shorthand),
            0,
            f"❌ FAIL: Tìm thấy {len(lines_with_background_shorthand)} dòng dùng shorthand `background:#`\n"
            "   Fix: Thay tất cả `background:#` thành `background-color:#`\n"
            f"   Lines: {lines_with_background_shorthand[:3]}"
        )

    def test_phase1_offboarding_reminder_header_color(self):
        """Phase 1: offboarding_reminder header cũng phải có màu"""
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_offboarding_reminder'
        )

        self.assertIn('background-color:#b5121b', rendered)
        self.assertIn('background-image:linear-gradient', rendered)

    def test_phase1_exit_survey_header_and_button_color(self):
        """Phase 1: exit_survey header + button ngoài phải có màu"""
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_exit_survey'
        )

        self.assertIn('background-color:#b5121b', rendered)
        self.assertIn('background-image:linear-gradient', rendered)
        # Button "Bắt đầu khảo sát" cũng phải có background-color
        self.assertIn('background-color:#da291c', rendered)

    def test_phase1_adecco_notification_header_color(self):
        """Phase 1: adecco_notification header phải có màu"""
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_adecco_notification'
        )

        self.assertIn('background-color:#b5121b', rendered)
        self.assertIn('background-image:linear-gradient', rendered)

    # ========== PHASE 2: PLACEHOLDER ==========

    def test_phase2_dept_reminder_employee_name_placeholder_render(self):
        """
        Phase 2: dept_offboarding_reminder tên nhân viên phải render

        Lỗi: Body dùng `{{ object.x_psm_0213_employee_id.name }}` (inline_template syntax)
        → QWeb engine KHÔNG xử lý {{ }} → in ra literal text

        Fix: Thay thành `<t t-out="object.x_psm_0213_employee_id.name"/>`
        → QWeb engine render → tên hiển thị đúng
        """
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        # Assert 1: Tên nhân viên PHẢI render thành text
        self.assertIn(
            'Huỳnh Thanh Sơn',
            rendered,
            "❌ FAIL: Tên nhân viên KHÔNG được render\n"
            "   Expected: 'Huỳnh Thanh Sơn' hiển thị trong email\n"
            "   Problem: Body dùng {{ }} (inline_template) nhưng engine là qweb\n"
            "   Fix: Thay {{ }} → <t t-out>"
        )

        # Assert 2: Mã nhân viên cũng phải render
        self.assertIn(
            'EMP123',
            rendered,
            "❌ FAIL: Mã nhân viên KHÔNG được render\n"
            "   Expected: 'EMP123' hiển thị trong email\n"
            "   Fix: Thay {{ object.x_psm_0213_employee_id.barcode or 'N/A' }} → <t t-out>"
        )

        # Assert 3: KHÔNG in literal placeholder
        self.assertNotIn(
            '{{ object.x_psm_0213_employee_id.name }}',
            rendered,
            "❌ FAIL: Tìm thấy literal placeholder\n"
            "   Expected: Text 'Huỳnh Thanh Sơn' (rendered)\n"
            "   Got: `{{ object.x_psm_0213_employee_id.name }}` (not rendered)\n"
            "   Reason: QWeb không process {{ }} — phải dùng <t t-out>"
        )

        self.assertNotIn(
            '{{ object.x_psm_0213_employee_id.barcode or',
            rendered,
            "❌ FAIL: Tìm thấy literal barcode placeholder\n"
            "   Fix: Thay {{ }} → <t t-out>"
        )

    def test_phase2_offboarding_reminder_request_owner_name_render(self):
        """Phase 2: offboarding_reminder request owner tên phải render"""
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_offboarding_reminder'
        )

        # Tên user_admin là cái chúng ta render
        self.assertNotIn(
            '{{ object.request_owner_id.name }}',
            rendered,
            "❌ FAIL: Tìm thấy literal request_owner_id.name placeholder\n"
            "   Fix: Thay {{ }} → <t t-out>"
        )

    def test_phase2_exit_survey_placeholder_not_literal(self):
        """Phase 2: exit_survey KHÔNG được có literal {{ }} trong body"""
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_exit_survey'
        )

        # Exit survey dùng t-esc/t-out nên KHÔNG có {{ }} trong body
        # (subject có {{ }} là OK — subject dùng inline_template engine)
        self.assertNotIn(
            '{{ object.',
            rendered,
            "❌ FAIL: Body KHÔNG được có {{ }} placeholder\n"
            "   Note: subject có {{ }} là OK (engine khác)\n"
            "   Fix: Body phải dùng <t t-out> hoặc t-esc"
        )

    # ========== PHASE 3: BORDER-LEFT + LANG/AUTO_DELETE ==========

    def test_phase3_dept_reminder_border_left_sub_property(self):
        """
        Phase 3: dept_offboarding_reminder border-left phải dùng sub-property

        Lỗi: Dùng shorthand `border-left:4px solid #da291c`
        → Odoo sanitizer (chatter) lọc shorthand → viền mất

        Fix: Thay thành sub-property
        → border-left-width:4px + border-left-style:solid + border-left-color:#da291c
        → Sống sót sanitizer (whitelist có sub-property)
        """
        rendered = self._render_template_body(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        # Assert 1: border-left-width PHẢI có
        self.assertIn(
            'border-left-width:4px',
            rendered,
            "❌ FAIL: PHẢI có border-left-width:4px\n"
            "   Reason: Odoo sanitizer whitelist có border-left-width\n"
            "   Fix: Thay border-left:4px solid → border-left-width:4px;border-left-style:solid;border-left-color"
        )

        # Assert 2: border-left-style PHẢI có
        self.assertIn(
            'border-left-style:solid',
            rendered,
            "❌ FAIL: PHẢI có border-left-style:solid"
        )

        # Assert 3: border-left-color PHẢI có
        self.assertIn(
            'border-left-color:#da291c',
            rendered,
            "❌ FAIL: PHẢI có border-left-color:#da291c"
        )

        # Assert 4: Shorthand KHÔNG được có (sẽ bị lọc ở chatter)
        self.assertNotIn(
            'border-left:4px solid #da291c',
            rendered,
            "❌ FAIL: KHÔNG được dùng shorthand border-left\n"
            "   Reason: Odoo sanitizer CSS whitelist KHÔNG có border-left\n"
            "   → Shorthand bị xóa ở chatter\n"
            "   Fix: Thay thành sub-property (border-left-width, border-left-style, border-left-color)"
        )

    def test_phase3_all_templates_border_left_sub_property(self):
        """Phase 3: Tất cả 4 template phải dùng border-left sub-property"""
        templates = [
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder',
            'M02_P0213.psm_0213_email_template_offboarding_reminder',
            'M02_P0213.psm_0213_email_template_exit_survey',
            'M02_P0213.psm_0213_email_template_adecco_notification',
        ]

        for template_ref in templates:
            with self.subTest(template=template_ref):
                rendered = self._render_template_body(template_ref)
                self.assertIn('border-left-width:4px', rendered)
                self.assertIn('border-left-style:solid', rendered)
                self.assertIn('border-left-color:#da291c', rendered)

    def test_phase3_dept_reminder_has_lang_field(self):
        """
        Phase 3: dept_offboarding_reminder PHẢI có lang field

        Lỗi: Dept template thiếu lang field → không render lang đúng

        Fix: Thêm `<field name="lang">{{ object.request_owner_id.lang }}</field>`
        → Đồng bộ với offboarding_reminder
        """
        template = self.env.ref(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        self.assertIsNotNone(
            template.lang,
            "❌ FAIL: dept_offboarding_reminder PHẢI có lang field\n"
            "   Expected: {{ object.request_owner_id.lang }}\n"
            "   Fix: Thêm <field name=\"lang\">{{ object.request_owner_id.lang }}</field>"
        )

    def test_phase3_dept_reminder_auto_delete_true(self):
        """
        Phase 3: dept_offboarding_reminder PHẢI có auto_delete=True

        Lỗi: Dept template thiếu auto_delete → email không tự xóa

        Fix: Thêm `<field name="auto_delete">True</field>`
        → Đồng bộ với offboarding_reminder
        """
        template = self.env.ref(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        self.assertTrue(
            template.auto_delete,
            "❌ FAIL: dept_offboarding_reminder PHẢI có auto_delete=True\n"
            "   Current: auto_delete=False hoặc None\n"
            "   Fix: Thêm <field name=\"auto_delete\">True</field>"
        )


@tagged('M02_P0213', 'email_template', 'send_mail')
class TestEmailTemplateSending(MailCommon):
    """Test gửi email (mock SMTP) — kiểm tra email được tạo đúng"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_employee = cls.env['hr.employee'].create({
            'name': 'Test Employee Send',
            'barcode': 'EMP456',
        })

        cls.test_approval = cls.env['approval.request'].create({
            'category_id': cls.env.ref('M02_P0213.approval_category_resignation').id
            if cls.env.ref('M02_P0213.approval_category_resignation', raise_if_not_found=False)
            else cls.env['approval.category'].create({'name': 'Resignation'}).id,
            'x_psm_0213_employee_id': cls.test_employee.id,
            'request_owner_id': cls.user_admin.partner_id.id,
        })

    def test_send_dept_reminder_email(self):
        """Test gửi dept_offboarding_reminder email (mock)"""
        template = self.env.ref(
            'M02_P0213.psm_0213_email_template_dept_offboarding_reminder'
        )

        with self.mock_mail_gateway():
            template.send_mail(
                self.test_approval.id,
                force_send=True,
                email_values={'email_to': 'test@example.com'}
            )

        # Kiểm tra email được tạo
        email = self.env['mail.mail'].search(
            [('subject', 'ilike', 'công việc trễ hạn')],
            limit=1
        )

        self.assertIsNotNone(email, "Email PHẢI được tạo")
        self.assertIn('Test Employee Send', email.body_html, "Tên NV PHẢI trong email")
        self.assertIn('background-color:#b5121b', email.body_html, "Header color PHẢI có")
