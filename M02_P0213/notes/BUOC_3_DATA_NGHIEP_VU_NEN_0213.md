# Bước 3 - Data Nghiệp Vụ Nền 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Bước 0: `addons/M02_P0213/notes/PHASE_0_DOI_CHIEU_BLUEPRINT_SOURCE_0213.md`
- Bước 1: `addons/M02_P0213/notes/BUOC_1_NEN_MODULE_VA_MANIFEST_0213.md`
- Bước 2: `addons/M02_P0213/notes/BUOC_2_KHAI_BAO_FIELD_VA_MODEL_INHERIT_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/data/survey_exit_interview_data.xml`
- `addons/M02_P0213/data/approval_category_data.xml`
- `addons/M02_P0213/data/email_template_exit_survey.xml`
- `addons/M02_P0213/data/email_template_adecco_notification.xml`
- `addons/M02_P0213/data/email_template_social_insurance.xml`
- `addons/M02_P0213/data/email_template_offboarding_reminder.xml`
- `addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml`
- `addons/M02_P0213/data/ir_cron_data.xml`
- `addons/M02_P0213/data/offboarding_activity_plan_data.xml`
- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/views/resignation_request_views.xml`

## 3. Kết luận XML ID nền

Các XML ID chính theo blueprint hiện đã có:

- `M02_P0213.psm_0213_survey_exit_interview`
- `M02_P0213.psm_0213_approval_category_resignation`
- `M02_P0213.psm_0213_email_template_exit_survey`
- `M02_P0213.psm_0213_email_template_adecco_notification`
- `M02_P0213.psm_0213_email_template_social_insurance`
- `M02_P0213.psm_0213_email_template_offboarding_reminder`
- `M02_P0213.psm_0213_email_template_dept_offboarding_reminder`
- `M02_P0213.action_psm_0213_offboarding_reminder_cron`
- `M02_P0213.psm_0213_offboarding_activity_plan`
- `M02_P0213.psm_0213_offboarding_template_asset_recovery`
- `M02_P0213.psm_0213_offboarding_template_damage_assessment`
- `M02_P0213.psm_0213_offboarding_template_deactive_email`
- `M02_P0213.psm_0213_offboarding_template_expense_claim`
- `M02_P0213.psm_0213_offboarding_template_exit_interview`

## 4. Thay đổi đã thực hiện

Đã bổ sung marker cho category offboarding:

```xml
<field name="x_psm_0213_is_offboarding" eval="True"/>
```

Lý do:

- Record rules trong `security/offboarding_request_rules.xml` dùng domain `category_id.x_psm_0213_is_offboarding = True`.
- View backend cũng dùng marker này ở một số điều kiện hiển thị.
- Logic nhận diện offboarding trong Python dựa vào category `0213`.
- Nếu category không bật marker, request offboarding có thể không khớp scope quyền và UI/logic liên quan.

File đã sửa:

- `addons/M02_P0213/data/approval_category_data.xml`

## 5. Kết luận thứ tự nạp data

Thứ tự manifest hiện phù hợp với Bước 3:

- Survey được nạp trước security vì `security.xml` ref survey exit interview.
- Security nạp trước category vẫn hợp lệ vì `offboarding_request_rules.xml` dùng domain theo field marker, không ref XML ID category.
- Category nạp trước views vì views dùng id substitution `%(M02_P0213.psm_0213_approval_category_resignation)d`.
- Email templates nạp trước các flow sử dụng template fallback trong Python.
- Cron và activity plan có XML ID riêng và đã có trong data.

## 6. Điểm giữ lại cho bước sau

- `data/offboarding_activity_plan_data.xml` vẫn hard-code `company_id` bằng `base.main_company`; đây là risk đã được blueprint đưa vào nhóm xử lý rủi ro sau, chưa đổi ở Bước 3.
- Bước 3 chưa chạy upgrade Odoo/module nên chưa xác nhận ở mức ORM/database.

## 7. Verification

- Đã parse toàn bộ file XML trong `addons/M02_P0213/data`.
- Kết quả: tất cả data XML parse được ở mức cú pháp XML.
- Đã regenerate `structure/module_map.json`, `structure/module_map_stats.json`, và `structure/details/*.json` sau thay đổi.
