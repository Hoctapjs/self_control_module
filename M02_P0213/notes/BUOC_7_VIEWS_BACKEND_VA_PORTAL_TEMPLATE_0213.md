# Bước 7 - Views Backend Và Portal Template 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Bước 6: `addons/M02_P0213/notes/BUOC_6_SECURITY_VA_QUYEN_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/views/resignation_request_views.xml`
- `addons/M02_P0213/views/resignation_portal_template.xml`
- `addons/M02_P0213/views/res_company_views.xml`
- `addons/M02_P0213/views/config_menu_views.xml`
- `addons/M02_P0213/__manifest__.py`
- `addons/M02_P0213/models/resignation_request.py`

## 3. Thay đổi backend view

File sửa:

- `addons/M02_P0213/views/resignation_request_views.xml`

Điều chỉnh:

- Đồng bộ group hiển thị nút với Python group guard:
  - `action_send_social_insurance`: `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HEAD_M`, `SYSTEM_ST_M`
  - `action_send_adecco_notification`: `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HEAD_M`, `SYSTEM_ST_M`
  - `action_done`: `HR_ADMIN_M`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M`
  - `action_rehire`: `HR_ADMIN_M`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M`
  - `action_blacklist`: `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M`
  - `action_view_survey_results`: `OPS_OM_M`, các nhóm HR, `HR_HEAD_M`, `SYSTEM_ST_M`
- Mở tab thông tin nghỉ việc và tab activity cho các group có quyền đọc theo Bước 6.
- Đổi xpath thêm tab từ `//notebook/page[1]` sang `//notebook` với `position="inside"` để tránh phụ thuộc vị trí page đầu tiên của view gốc.
- Đặt `x_psm_0213_all_activities_completed` readonly trong form vì đây là field compute.

## 4. Thay đổi logic hỗ trợ view

File sửa:

- `addons/M02_P0213/models/resignation_request.py`

Điều chỉnh:

- Tách `action_send_social_insurance()` khỏi `action_done()`.

Lý do:

- Ma trận quyền expected cho phép `HR_ADMIN_S` gửi thông tin BHXH.
- Quyền hoàn tất quy trình chỉ dành cho `HR_ADMIN_M`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M`.
- Nếu gửi BHXH tự gọi `action_done()`, UI và Python guard sẽ mâu thuẫn.

## 5. Portal template

File đã rà:

- `addons/M02_P0213/views/resignation_portal_template.xml`

Không cần sửa thêm ở Bước 7 vì Bước 5 đã xử lý các lỗi portal chính:

- `portal_error`
- không render form khi thiếu employee
- route activity done kiểm tra owner và user phụ trách

## 6. Config views

File đã rà:

- `addons/M02_P0213/views/res_company_views.xml`
- `addons/M02_P0213/views/config_menu_views.xml`

Kết luận:

- `res_company_views.xml` đang là view cấu hình chính được nạp trong manifest.
- `config_menu_views.xml` ref đúng `view_psm_0213_company_offboarding_config_form`.
- `views/res_config_settings_views.xml` vẫn không nằm trong manifest theo chủ ý từ blueprint và `data/config_ui_cleanup.xml`.

## 7. Verification

- Đã parse XML các view được nạp trong manifest:
  - `views/resignation_request_views.xml`
  - `views/resignation_portal_template.xml`
  - `views/res_company_views.xml`
  - `views/config_menu_views.xml`
- Đã chạy `python -m py_compile` cho `models/resignation_request.py`.
- Chưa chạy upgrade Odoo/module hoặc kiểm tra render view thực tế trên UI.
