# Bước 4 - Logic Chính Của `approval.request` 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Bước 0: `addons/M02_P0213/notes/PHASE_0_DOI_CHIEU_BLUEPRINT_SOURCE_0213.md`
- Bước 1: `addons/M02_P0213/notes/BUOC_1_NEN_MODULE_VA_MANIFEST_0213.md`
- Bước 2: `addons/M02_P0213/notes/BUOC_2_KHAI_BAO_FIELD_VA_MODEL_INHERIT_0213.md`
- Bước 3: `addons/M02_P0213/notes/BUOC_3_DATA_NGHIEP_VU_NEN_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/survey_user_input.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/data/approval_category_data.xml`
- `addons/M02_P0213/data/survey_exit_interview_data.xml`
- `addons/M02_P0213/data/offboarding_activity_plan_data.xml`
- `addons/M02_P0213/data/email_template_*.xml`

## 3. Luồng chính đã xác nhận

Các thành phần luồng chính hiện đã có trong source:

- Nhận diện request 0213 qua category `M02_P0213.psm_0213_approval_category_resignation`.
- `action_approve()` gửi exit survey và tự launch activity plan.
- `_get_or_create_0213_survey_user_input()` tạo hoặc tái dùng `survey.user_input`.
- `action_send_exit_survey()` gửi email bằng template `psm_0213_email_template_exit_survey`.
- `_schedule_offboarding_activities()` tạo checklist từ `psm_0213_offboarding_activity_plan`.
- `SurveyUserInput._mark_done()` và `write()` gọi `_check_and_mark_exit_interview_done()`.
- `action_send_social_insurance()` gửi email BHXH khi đúng loại hợp đồng.
- `action_done()` hoàn tất request và vô hiệu hóa user nếu đủ điều kiện.
- `action_rehire()` và `action_blacklist()` đánh dấu trạng thái sau khi done.

## 4. Thay đổi đã thực hiện

### 4.1. Sửa hook survey done để mark đúng activity Exit Interview

File sửa:

- `addons/M02_P0213/models/survey_user_input.py`

Lý do:

- Activity plan hiện tạo activity trên `approval.request`.
- Hook survey done trước đó chỉ tìm activity có `res_model = hr.employee`.
- Vì vậy activity `Hoàn thành Exit Interview` có thể không được mark done, làm `x_psm_0213_all_activities_completed` không lên đúng.

Điều chỉnh:

- Tìm `approval.request` offboarding 0213 đang `approved` theo employee.
- Tìm activity `Hoàn thành Exit Interview` trên cả:
  - `approval.request` theo request id
  - `hr.employee` theo employee id
- Dùng `sudo()` khi tìm employee, request, và activity để hook survey có thể chạy ổn sau khi user portal hoàn tất survey.

### 4.2. Siết `action_done()` chỉ xử lý request offboarding 0213

File sửa:

- `addons/M02_P0213/models/resignation_request.py`

Lý do:

- `action_done()` là logic đặc thù 0213 nhưng trước đó xử lý toàn bộ recordset `approval.request`.
- Nếu bị gọi trên request không thuộc 0213, method có thể kiểm tra các field offboarding và raise lỗi không đúng ngữ cảnh.

Điều chỉnh:

- Tách `offboarding_requests` và `other_requests`.
- Chỉ chạy kiểm tra survey/activity, write `request_status = done`, và deactivate user trên request offboarding 0213.
- Với request ngoài 0213, nếu super có `action_done()` thì trả về super; nếu không có thì bỏ qua.

## 5. Điểm giữ lại cho bước sau

- `Portal Controller` thuộc Bước 5, chưa xử lý ở Bước 4.
- `Security và quyền` thuộc Bước 6, chưa siết ACL ở Bước 4.
- `action_send_social_insurance()` đã được tách khỏi `action_done()` ở Bước 7 để khớp ma trận quyền: quyền gửi email BHXH và quyền hoàn tất quy trình là hai quyền khác nhau.

## 6. Verification

- Đã chạy `python -m py_compile` cho:
  - `models/resignation_request.py`
  - `models/survey_user_input.py`
  - `models/mail_activity.py`
- Kết quả: không có lỗi cú pháp Python.
- Chưa chạy upgrade Odoo/module ở Bước 4.
