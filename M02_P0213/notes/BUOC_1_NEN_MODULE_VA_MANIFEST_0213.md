# Bước 1 - Nền Module Và Manifest 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Kết quả Bước 0: `addons/M02_P0213/notes/PHASE_0_DOI_CHIEU_BLUEPRINT_SOURCE_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/__manifest__.py`
- `addons/M02_P0213/data/survey_exit_interview_data.xml`
- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/ir.model.access.csv`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/data/approval_category_data.xml`
- `addons/M02_P0213/data/email_template_*.xml`
- `addons/M02_P0213/data/ir_cron_data.xml`
- `addons/M02_P0213/data/offboarding_activity_plan_data.xml`
- `addons/M02_P0213/data/config_ui_cleanup.xml`
- `addons/M02_P0213/views/*.xml`

## 3. Kết luận manifest

Manifest hiện có đủ dependency chính theo blueprint:

- `base`
- `mail`
- `approvals`
- `hr`
- `portal`
- `survey`
- `M02_P0200`

Không cần thêm dependency mới ở Bước 1.

## 4. Kết luận thứ tự data

Thứ tự data hiện tại khớp nguyên tắc dependency của blueprint:

1. `data/survey_exit_interview_data.xml`
2. `security/security.xml`
3. `security/ir.model.access.csv`
4. `security/offboarding_request_rules.xml`
5. `data/approval_category_data.xml`
6. `data/email_template_exit_survey.xml`
7. `data/email_template_adecco_notification.xml`
8. `data/email_template_social_insurance.xml`
9. `data/email_template_offboarding_reminder.xml`
10. `data/email_template_dept_offboarding_reminder.xml`
11. `data/ir_cron_data.xml`
12. `data/offboarding_activity_plan_data.xml`
13. `data/config_ui_cleanup.xml`
14. `views/resignation_portal_template.xml`
15. `views/resignation_request_views.xml`
16. `views/res_company_views.xml`
17. `views/config_menu_views.xml`

Giải thích nhanh:

- Survey được nạp trước `security/security.xml` vì các record rule survey dùng `ref('M02_P0213.psm_0213_survey_exit_interview')`.
- Security được nạp trước category vẫn hợp lệ vì rule trên `approval.request` dùng domain theo field `category_id.x_psm_0213_is_offboarding`, không ref trực tiếp XML ID category.
- Email templates được nạp trước cron và activity plan, đúng lớp dữ liệu nền.
- `config_ui_cleanup.xml` đứng trước views backend để dọn action/view settings cũ trước khi nạp UI cấu hình hiện tại.
- `config_menu_views.xml` đứng sau `res_company_views.xml` vì server action ref view `view_psm_0213_company_offboarding_config_form`.

## 5. Thay đổi đã thực hiện ở Bước 1

- Không sửa `__manifest__.py` vì manifest hiện đã khớp blueprint.
- Sửa `structure/README.md` từ module cũ `M02_P0205_00` sang `M02_P0213`.
- Regenerate `structure/module_map.json`, `structure/module_map_stats.json`, và `structure/details/*.json` để map phản ánh các note mới.

## 6. Điểm chuyển sang bước sau

- `data/approval_category_data.xml` hiện tạo category `psm_0213_approval_category_resignation`; khi sang Bước 3 cần rà tiếp nội dung data nghiệp vụ, đặc biệt marker `x_psm_0213_is_offboarding`.
- `views/res_config_settings_views.xml` vẫn tồn tại trong thư mục views nhưng không nằm trong manifest; đây là chủ ý theo blueprint vì đã có `data/config_ui_cleanup.xml`.
