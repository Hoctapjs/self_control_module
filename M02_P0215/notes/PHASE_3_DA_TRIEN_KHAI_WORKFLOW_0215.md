# Phase 3 - Đã triển khai chuẩn hóa workflow module 0215

Ngày thực hiện: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/PLAN_REFACTOR_MODULE_0215_THEO_CONVENTION.md`
- `notes/PHASE_2_DA_TRIEN_KHAI_PORTAL_GUARD_0215.md`

Source chính dùng để xác nhận và sửa:

- `models/x_psm_hr_discipline_record.py`
- `views/x_psm_hr_discipline_record_views.xml`
- `controllers/portal.py`
- `views/x_psm_portal_templates.xml`

## 2. Phạm vi Phase 3

Phase 3 tập trung vào workflow state/action của hồ sơ kỷ luật:

- Chuẩn hóa đường đi state theo quy trình 0215.
- Không mở rộng sang phân quyền chi tiết của Phase 4.
- Không xóa comment hiện có trong code.
- Giữ method legacy nếu có khả năng đang được gọi từ view/template hoặc dữ liệu cũ.

## 3. Nội dung đã triển khai

### 3.1. Bổ sung helper kiểm soát state transition

Đã thêm trong `models/x_psm_hr_discipline_record.py`:

- `_x_psm_state_label()`
- `_x_psm_allowed_state_transitions()`
- `_x_psm_validate_state_transition()`
- `_x_psm_write_state()`
- `_x_psm_ensure_action_selected()`
- `_x_psm_ensure_discipline_level()`

Mục tiêu:

- Không cho hồ sơ nhảy state ngoài luồng quy trình 0215.
- Gom logic chuyển state vào một helper thay vì rải nhiều `write({"state": ...})`.
- Báo lỗi rõ bằng `UserError` khi người dùng thao tác sai luồng.

### 3.2. Chuẩn hóa luồng state

Các transition hợp lệ hiện tại:

- `draft` -> `under_review`, `cancel`
- `under_review` -> `proposal`, `level_determination`, `cancel`
- `level_determination` -> `proposal`, `investigation`, `cancel`
- `investigation` -> `hearing`, `proposal`, `cancel`
- `hearing` -> `proposal`, `cancel`
- `proposal` -> `issued`, `cancel`
- `issued` -> `approval`, `notified`, `cancel`
- `approval` -> `notified`, `proposal`, `cancel`
- `notified` -> `active`, `proposal`, `cancel`
- `active` -> `expired`, `cancel`

### 3.3. Sửa luồng Store Level

Trước Phase 3:

- Store Level có action `action_psm_activate_store_discipline`.
- Action này đi thẳng từ `proposal` sang `active`.
- Luồng này bỏ qua bước ban hành/thông báo/nhân viên xác nhận.

Sau Phase 3:

- Store Level đi qua `proposal` -> `issued` -> `notified` -> `active`.
- `active` chỉ xảy ra khi nhân viên chấp nhận qua `action_psm_employee_accept`.
- Method legacy `action_psm_activate_store_discipline` vẫn được giữ, nhưng chỉ map sang `action_psm_issue_decision()` và `action_psm_submit_for_approval()`, không kích hoạt thẳng.

### 3.4. Chuẩn hóa action backend

Các action chính đã chuyển sang dùng helper `_x_psm_write_state()`:

- `action_psm_rgm_no_repeat`
- `action_psm_rgm_repeat`
- `action_psm_confirm`
- `action_psm_rgm_store_level`
- `action_psm_activate_store_discipline`
- `action_psm_rgm_company_level`
- `action_psm_schedule_hearing`
- `action_psm_skip_hearing`
- `action_psm_close_hearing`
- `action_psm_issue_decision`
- `action_psm_submit_for_approval`
- `action_psm_employee_accept`
- `action_psm_employee_reject`
- `action_psm_expire`
- `action_psm_ceo_approve`
- `action_psm_ceo_reject`
- `action_psm_cancel`

### 3.5. Cập nhật view form

Đã chỉnh trong `views/x_psm_hr_discipline_record_views.xml`:

- Button `action_psm_activate_store_discipline` không còn hiển thị ở Phase 3.
- Cả Store Level và Company Level cùng dùng button `action_psm_issue_decision` khi ở `proposal`.
- Statusbar hiển thị đủ các state chính:
  - `draft`
  - `under_review`
  - `level_determination`
  - `investigation`
  - `hearing`
  - `proposal`
  - `issued`
  - `approval`
  - `notified`
  - `active`
  - `expired`

## 4. Kiểm tra đã chạy

Đã chạy và đạt:

- `python -m compileall addons\M02_P0215`
- Parse toàn bộ XML bằng `xml.etree.ElementTree`
- Kiểm tra manifest data file không thiếu
- Search các pattern rủi ro:
  - `hr_meeting`
  - `M02_P0215_00`
  - `x_psm_x_psm`
  - reference button cũ `action_psm_activate_store_discipline` trong view
- Regenerate `structure/module_map.json` bằng `structure/build_module_map.py`

Lưu ý:

- `action_psm_activate_store_discipline` vẫn còn trong model vì là legacy method tương thích.
- Comment `manager_review` trong portal vẫn được giữ lại theo rule không tự ý xóa comment hiện có; logic không chuyển state này.
- Chưa chạy test cài mới/upgrade module trong Odoo container ở Phase 3.

## 5. File đã thay đổi

- `models/x_psm_hr_discipline_record.py`
- `views/x_psm_hr_discipline_record_views.xml`
- `structure/module_map.json`
- `structure/details/models__x_psm_hr_discipline_record.py.json`
- `structure/details/views__x_psm_hr_discipline_record_views.xml.json`
- `notes/PHASE_3_DA_TRIEN_KHAI_WORKFLOW_0215.md`

## 6. Đề xuất Phase tiếp theo

Phase 4 nên tập trung vào phân quyền tối thiểu:

- Rà `ir.model.access.csv`.
- Bổ sung record rule nếu cần.
- Giảm rủi ro portal/manager đọc hoặc ghi hồ sơ không liên quan.
- Đối chiếu các group đang dùng từ `M02_P0200`.
