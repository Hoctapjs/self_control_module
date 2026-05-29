# Phase 1 - Đã triển khai refactor naming module 0215

## 1. Phạm vi đã làm

Phase 1 đã triển khai theo hướng greenfield vì module `M02_P0215` chưa từng được cài trên database. Không tạo migration, không giữ alias field cũ.

Tài liệu đã dùng:

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map trước/sau: `addons/M02_P0215/structure/module_map.json`
- Audit Phase 0: `addons/M02_P0215/notes/PHASE_0_AUDIT_REFACTOR_0215_THEO_CONVENTION.md`
- Plan tổng: `addons/M02_P0215/notes/PLAN_REFACTOR_MODULE_0215_THEO_CONVENTION.md`

## 2. Field nghiệp vụ đã đổi sang prefix `x_psm_`

Các field chính đã đổi:

| Cũ | Mới |
|---|---|
| `employee_id` | `x_psm_employee_id` |
| `violation_type` | `x_psm_violation_type` |
| `discipline_purpose` | `x_psm_discipline_purpose` |
| `date` | `x_psm_date` |
| `employee_explanation` | `x_psm_employee_explanation` |
| `explanation_date` | `x_psm_explanation_date` |
| `action_id` | `x_psm_action_id` |
| `start_date` | `x_psm_start_date` |
| `end_date` | `x_psm_end_date` |
| `record_id` trong explanation | `x_psm_record_id` |

Đã cập nhật reference trong:

- `models/x_psm_hr_discipline_record.py`
- `models/x_psm_hr_discipline_explanation.py`
- `wizards/x_psm_hr_discipline_reject_wizard.py`
- `controllers/portal.py`
- `views/x_psm_hr_discipline_record_views.xml`
- `views/x_psm_portal_templates.xml`
- `reports/x_psm_discipline_reports.xml`
- `data/mail_template.xml`
- `data/email_template_rejection.xml`
- `data/email_template_discipline_done.xml`

Các field kỹ thuật/chung giữ nguyên:

- `name`
- `sequence`
- `state`
- `currency_id`

## 3. XML id/action/menu/security đã đổi

Đã đổi nhóm view/action/menu chính theo convention:

- `view_hr_discipline...` -> `view_psm_hr_discipline...`
- `action_hr_discipline...` -> `action_psm_hr_discipline...`
- `menu_discipline...` -> `menu_psm_hr_discipline...`
- `seq_hr_discipline_record` -> `seq_psm_hr_discipline_record`
- `hr_discipline_reject_wizard_form` -> `view_psm_hr_discipline_reject_wizard_form`

Đã đổi security id:

- `access_hr_discipline...` -> `access_psm_hr_discipline...`

Đã đổi seed/template/report id chính:

- `action_store_*` -> `x_psm_action_store_*`
- `action_company_*` -> `x_psm_action_company_*`
- `violation_category_*` -> `x_psm_violation_category_*`
- `violation_type_*` -> `x_psm_violation_type_*`
- `email_template_*` -> `email_template_psm_*`
- `portal_*` -> `portal_psm_*`
- report action id -> `action_psm_report_*`

Đã đổi reference module XML từ `M02_P0215_00` sang `M02_P0215`.

## 4. Manifest và cron

Đã đổi manifest name:

- Cũ: `M02_P0215_00 Disciplinary Process`
- Mới: `M02_P0215_DISCIPLINARY_PROCESS`

Đã sửa cron gọi đúng method hiện có:

- `model._cron_auto_expire()` -> `model._x_psm_cron_auto_expire()`
- Alias `_cron_auto_complete_improvement()` hiện gọi lại `_x_psm_cron_auto_expire()`

## 5. Kiểm tra đã chạy

Kết quả kiểm tra:

- Python compile: OK.
- XML parse: OK toàn bộ file XML trong module.
- Manifest data file check: OK, không thiếu file XML/CSV được khai báo.
- Regenerate structure map: OK bằng `structure/build_module_map.py`.

Sau regenerate, `structure/module_map.json` đã nhận field mới như:

- `x_psm_employee_id`
- `x_psm_violation_type`
- `x_psm_violation_category_id`
- `x_psm_record_id`

## 6. Rà reference cũ

Không còn các reference source chính sau trong code module:

- `M02_P0215_00`
- `x_psm_x_psm`
- `view_hr_discipline...`
- `action_hr_discipline...`
- `access_hr_discipline...`
- `seq_hr_discipline_record`
- `hr_discipline_reject_wizard_form`
- `improvement_start_date`
- `improvement_end_date`

Các lần xuất hiện còn lại của `employee_id` là field gốc của Odoo trên `res.users`/`hr.employee`, ví dụ:

- `self.env.user.employee_id`
- `request.env.user.employee_id`
- `u.employee_id`

Những chỗ này được giữ nguyên vì không phải field mới của model 0215.

## 7. Phần chuyển sang Phase 2

Các việc chưa xử lý sâu trong Phase 1 và nên làm ở Phase 2:

- Dọn `print()` debug trong `controllers/portal.py`.
- Tách helper portal để giảm lặp.
- Bổ sung guard cho route POST thiếu `x_psm_record_id`.
- Rà lại `.sudo()` theo nguyên tắc phân quyền tối thiểu.
- Chuẩn hóa thêm code style Python cho các dòng dài.
- Cài mới module trên database test để bắt lỗi Odoo runtime mà Python/XML parse không phát hiện.

## 8. Kết luận

Phase 1 hoàn tất phần refactor naming theo convention ở mức source. Module đã sẵn sàng chuyển sang Phase 2 để dọn portal, guard, quyền và ổn định runtime.
