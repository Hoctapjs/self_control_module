# Phase 2 - Đã triển khai refactor Portal Guard module 0215

Ngày thực hiện: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/PLAN_REFACTOR_MODULE_0215_THEO_CONVENTION.md`
- `notes/PHASE_0_AUDIT_REFACTOR_0215_THEO_CONVENTION.md`
- `notes/PHASE_1_DA_TRIEN_KHAI_REFACTOR_NAMING_0215.md`

Source chính dùng để xác nhận và sửa:

- `controllers/portal.py`
- `models/x_psm_hr_discipline_record.py`
- `data/email_template_discipline_done.xml`
- `views/x_psm_hr_discipline_record_views.xml`

## 2. Rà soát nhanh Phase 1

Phase 1 đã hoàn tất phần đổi tên chính:

- Không còn reference module cũ `M02_P0215_00` trong source nghiệp vụ.
- Không còn lỗi double prefix `x_psm_x_psm` trong source nghiệp vụ.
- Các field nghiệp vụ chính đã theo convention `x_psm_`.
- Các lần xuất hiện `employee_id` còn lại là field gốc của Odoo trên `res.users`/`hr.employee`, không phải field custom của module.
- Lỗi state `hr_meeting` trong view đã không còn trong source nghiệp vụ.

Điểm Phase 1 còn sót và đã xử lý trong Phase 2:

- `models/x_psm_hr_discipline_record.py` gọi XML id `M02_P0215.email_template_psm_discipline_notified`.
- Trước Phase 2, `data/email_template_discipline_done.xml` chưa có record này.
- Phase 2 đã bổ sung template `email_template_psm_discipline_notified`.

## 3. Nội dung đã triển khai Phase 2

### 3.1. Refactor helper Portal

Đã bổ sung các helper trong `controllers/portal.py`:

- `_x_psm_employee_model()`
- `_x_psm_record_model()`
- `_x_psm_empty_records()`
- `_x_psm_to_int()`
- `_x_psm_redirect_record()`
- `_x_psm_get_subordinates()`
- `_x_psm_is_manager_employee()`
- `_x_psm_can_view_record()`
- `_x_psm_can_finalize_record()`
- `_x_psm_get_record_from_post()`
- `_x_psm_portal_domain()`

Mục tiêu:

- Gom logic lấy employee/record vào một chỗ.
- Không ép `int(post.get(...))` trực tiếp trong từng route POST.
- Tránh lỗi 500 khi form thiếu `x_psm_record_id` hoặc dữ liệu id không hợp lệ.
- Giữ logic sudo cho portal nhưng có guard nghiệp vụ trước khi ghi dữ liệu.

### 3.2. Dọn debug print

Đã xóa các dòng `print()` debug trong `_prepare_home_portal_values`.

Hiện tại `controllers/portal.py` không còn `print()` debug.

### 3.3. Bổ sung guard cho route POST

Các route đã có guard:

- `/my/discipline/create`
- `/my/discipline/submit_section_ii`
- `/my/discipline/manager_finalize`
- `/my/discipline/rgm_action`
- `/my/discipline/respond`

Quy tắc chính:

- Thiếu record id hoặc record không tồn tại thì redirect về danh sách hồ sơ.
- Nhân viên chỉ được gửi phản hồi/ký cho hồ sơ của chính mình.
- Quản lý chỉ được finalize nếu là quản lý trực tiếp hoặc đại diện công ty đã tạo hồ sơ.
- RGM action chỉ cho quản lý trực tiếp của nhân viên trong hồ sơ.
- Nhân viên chỉ được accept/reject khi hồ sơ ở state `notified`.

### 3.4. Bổ sung email template bị thiếu

Đã thêm record:

- `email_template_psm_discipline_notified`

File:

- `data/email_template_discipline_done.xml`

Lý do:

- Model `_x_psm_notify_employee()` đang gọi template này.
- Nếu không có template, luồng thông báo quyết định kỷ luật sẽ không gửi mail.

## 4. Kiểm tra đã chạy

Đã chạy và đạt:

- `python -m compileall addons\M02_P0215`
- Parse toàn bộ XML bằng `xml.etree.ElementTree`
- Kiểm tra manifest data file không thiếu
- Search source nghiệp vụ cho các pattern rủi ro:
  - `print(`
  - `int(post.get`
  - `hr_meeting`
  - `M02_P0215_00`
  - `x_psm_x_psm`
- Regenerate `structure/module_map.json` bằng `structure/build_module_map.py`

Lưu ý:

- Search `int(post.get` còn match giả với helper `_x_psm_to_int(post.get(...))`; đây là cách xử lý đã chủ đích, không còn ép `int()` trực tiếp.
- Không chạy test cài/upgrade Odoo thực tế trong container ở Phase 2.

## 5. File đã thay đổi

- `controllers/portal.py`
- `data/email_template_discipline_done.xml`
- `structure/module_map.json`
- `structure/details/data__email_template_discipline_done.xml.json`
- `structure/details/controllers__portal.py.json`
- `notes/PHASE_2_DA_TRIEN_KHAI_PORTAL_GUARD_0215.md`

## 6. Đề xuất Phase tiếp theo

Phase 3 nên tập trung vào:

- Rà workflow state/action trong `models/x_psm_hr_discipline_record.py`.
- Chuẩn hóa role/responsibility giữa RGM, HR, CEO, store level/company level.
- Kiểm tra các action legacy đang giữ để tương thích.
- Chạy thử upgrade module trong Odoo container nếu môi trường đã sẵn sàng.
