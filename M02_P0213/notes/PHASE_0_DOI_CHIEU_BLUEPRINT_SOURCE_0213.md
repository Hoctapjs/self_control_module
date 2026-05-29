# Phase 0 - Đối Chiếu Blueprint Với Source 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- JSON stats: `addons/M02_P0213/structure/module_map_stats.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/__manifest__.py`
- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/res_company.py`
- `addons/M02_P0213/models/res_config_settings.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/survey_user_input.py`
- `addons/M02_P0213/controllers/main.py`
- `addons/M02_P0213/security/ir.model.access.csv`
- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/views/resignation_request_views.xml`
- `addons/M02_P0213/views/res_company_views.xml`
- `addons/M02_P0213/views/resignation_portal_template.xml`

## 3. Kết luận đối chiếu

Source hiện tại là nguồn ưu tiên. `structure/module_map.json` đang phản ánh source hiện tại khá sát, chưa cần regenerate ở Phase 0.

Blueprint có một số tên field cũ ở phần mô tả tổng quan. Đã cập nhật `TECHNICAL_BLUEPRINT_0213.md` để thống nhất với source thật, đặc biệt ở bảng field `approval.request`, bảng field `res.company`, luồng `rehire/blacklist`, và cấu hình cron reminder.

## 4. Tên field chốt theo source hiện tại

### 4.1. `approval.request`

- Dùng `x_psm_0213_resignation_reason_id`, không dùng `x_psm_0213_departure_reason_id`.
- Dùng `x_psm_0213_resignation_date`, không dùng `x_psm_0213_last_working_day`.
- Dùng `request_status` extend thêm `done`, không dùng field riêng `x_psm_0213_request_status`.
- Dùng `x_psm_0213_is_rehire`, không dùng `x_psm_0213_rehire`.
- Dùng `x_psm_0213_is_blacklisted`, không dùng `x_psm_0213_blacklist`.
- Dùng `x_psm_0213_exit_survey_user_input_id`, không dùng `x_psm_0213_survey_user_input_id`.
- Dùng `x_psm_0213_exit_survey_completed`, không dùng `x_psm_0213_survey_done`.
- Dùng `x_psm_0213_employee_activity_ids`, không dùng `x_psm_0213_activity_ids`.
- Dùng `x_psm_0213_all_activities_completed`, không dùng `x_psm_0213_all_activities_done`.
- Dùng `x_psm_0213_is_plan_launched`, không dùng `x_psm_0213_plan_launched`.

### 4.2. `res.company` và `res.config.settings`

- Dùng `x_psm_0213_employee_reminder_template_id`.
- Dùng `x_psm_0213_department_reminder_template_id`.
- Dùng `x_psm_0213_adecco_notification_email`.
- Dùng `x_psm_0213_default_it_user_id`.
- Dùng `x_psm_0213_default_on_demand_user_id`.
- Dùng `x_psm_0213_social_insurance_contract_type_ids`.
- Dùng `x_psm_0213_reminder_overdue_days`.
- Dùng `x_psm_0213_reminder_extension_days`.

## 5. Phạm vi module đã chốt cho các bước sau

- Module không tạo model mới, chỉ `_inherit` các model Odoo có sẵn.
- Tất cả field mới trên model gốc vẫn tuân thủ prefix `x_psm_0213_`.
- Manifest hiện có đúng dependency chính: `base`, `mail`, `approvals`, `hr`, `portal`, `survey`, `M02_P0200`.
- Thứ tự data trong manifest hiện khớp nguyên tắc blueprint: survey, security, category, email templates, cron, activity plan, cleanup, views.
- Các action nhạy cảm trong `models/resignation_request.py` hiện đã có tuple group guard theo ma trận Phase 0.

## 6. Điểm cần giữ lại cho bước sau

- `controllers/main.py` vẫn dùng `request.env.ref("M02_P0213.psm_0213_approval_category_resignation")` trong `_get_resignation_category()` mà chưa có `raise_if_not_found=False`; đây là rủi ro đã nêu ở blueprint cho Bước 5.
- ACL `base.group_user` trên `approval.request` và `mail.activity` vẫn là điểm cần rà ở phase security; Phase 0 chỉ chốt nguồn tên và phạm vi, chưa siết quyền.
- `_compute_owner_related_activity_ids` vẫn là dead code theo ghi chú blueprint vì field `x_psm_0213_owner_related_activity_ids` đang dùng `related=`.
