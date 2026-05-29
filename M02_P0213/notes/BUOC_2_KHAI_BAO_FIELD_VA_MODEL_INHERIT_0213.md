# Bước 2 - Khai Báo Field Và Model Inherit 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Bước 0: `addons/M02_P0213/notes/PHASE_0_DOI_CHIEU_BLUEPRINT_SOURCE_0213.md`
- Bước 1: `addons/M02_P0213/notes/BUOC_1_NEN_MODULE_VA_MANIFEST_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/models/__init__.py`
- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/res_company.py`
- `addons/M02_P0213/models/res_config_settings.py`
- `addons/M02_P0213/models/survey_user_input.py`

## 3. Kết luận model inherit

Module hiện không tạo model mới. Không phát hiện `_name` mới trong `models/`.

Các model đang được kế thừa đúng phạm vi blueprint:

| File | Class | `_inherit` | Ghi chú |
|---|---|---|---|
| `models/resignation_request.py` | `ApprovalCategory` | `approval.category` | Thêm marker `x_psm_0213_is_offboarding` |
| `models/resignation_request.py` | `ResignationRequest` | `approval.request` | Thêm field offboarding và compute/related fields |
| `models/mail_activity.py` | `MailActivity` | `mail.activity` | Thêm trạng thái portal `x_psm_0213_ops_display_state` |
| `models/res_company.py` | `ResCompany` | `res.company` | Thêm cấu hình template/email/user/ngày nhắc |
| `models/res_config_settings.py` | `ResConfigSettings` | `res.config.settings` | Related fields tới `company_id` |
| `models/survey_user_input.py` | `SurveyUserInput` | `survey.user_input` | Hook sau khi survey hoàn tất |

## 4. Kết luận field theo convention

Các field custom thêm trên model gốc đang dùng prefix `x_psm_0213_`, đúng convention của module.

Ngoại lệ hợp lệ:

- `request_status` không dùng prefix vì đây là field gốc của `approval.request`, module chỉ `selection_add=[("done", "Done")]`.

## 5. Các field chính đã chốt theo source

### 5.1. `approval.category`

- `x_psm_0213_is_offboarding`

### 5.2. `approval.request`

- `x_psm_0213_resignation_reason`
- `x_psm_0213_resignation_reason_id`
- `x_psm_0213_resignation_date`
- `x_psm_0213_is_rehire`
- `x_psm_0213_is_blacklisted`
- `x_psm_0213_employee_id`
- `x_psm_0213_resignation_employee_name`
- `x_psm_0213_resignation_manager_name`
- `x_psm_0213_resignation_department`
- `x_psm_0213_job_id`
- `x_psm_0213_employee_activity_ids`
- `x_psm_0213_exit_survey_completed`
- `x_psm_0213_all_activities_completed`
- `x_psm_0213_type_contract`
- `x_psm_0213_is_social_insurance_contract`
- `x_psm_0213_resignation_owner_email`
- `x_psm_0213_is_plan_launched`
- `x_psm_0213_adecco_notification_sent`
- `x_psm_0213_exit_survey_user_input_id`
- `x_psm_0213_owner_related_activity_ids`

### 5.3. `mail.activity`

- `x_psm_0213_ops_display_state`

### 5.4. `res.company` và `res.config.settings`

- `x_psm_0213_exit_survey_template_id`
- `x_psm_0213_adecco_template_id`
- `x_psm_0213_social_insurance_template_id`
- `x_psm_0213_employee_reminder_template_id`
- `x_psm_0213_department_reminder_template_id`
- `x_psm_0213_adecco_notification_email`
- `x_psm_0213_default_it_user_id`
- `x_psm_0213_default_on_demand_user_id`
- `x_psm_0213_social_insurance_contract_type_ids`
- `x_psm_0213_reminder_overdue_days`
- `x_psm_0213_reminder_extension_days`

## 6. Ghi chú triển khai

Blueprint nói Bước 2 chỉ nên thêm field và compute cơ bản, chưa nhồi toàn bộ action nghiệp vụ. Source hiện tại đã có cả action nghiệp vụ trong `models/resignation_request.py` và hook trong `models/survey_user_input.py`. Bước 2 lần này không tách hoặc lược bỏ logic đã có; chỉ xác nhận nền field/model inherit đang tồn tại và hợp lệ để đi tiếp các bước sau.

`x_psm_0213_owner_related_activity_ids` đang là related field tới `x_psm_0213_employee_activity_ids`; method `_compute_owner_related_activity_ids` vẫn tồn tại nhưng không được field gọi. Đây là dead code đã được ghi nhận từ Bước 0, chưa xử lý ở Bước 2.

## 7. Verification

- Đã chạy `python -m py_compile` cho toàn bộ file Python trong `models/`.
- Kết quả: không có lỗi cú pháp Python.
- Chưa chạy upgrade Odoo/module ở Bước 2.
