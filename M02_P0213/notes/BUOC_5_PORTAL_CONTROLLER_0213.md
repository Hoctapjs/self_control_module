# Bước 5 - Portal Controller 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Bước 4: `addons/M02_P0213/notes/BUOC_4_LOGIC_CHINH_APPROVAL_REQUEST_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/controllers/main.py`
- `addons/M02_P0213/views/resignation_portal_template.xml`
- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/survey_user_input.py`

## 3. Route portal đã xác nhận

`controllers/main.py` hiện có 3 route đúng blueprint:

- `GET /my/resignation/ops`
- `POST /my/resignation/submit`
- `POST /my/resignation/ops/activity/done`

Tất cả route dùng `auth="user"`.

## 4. Thay đổi đã thực hiện

### 4.1. Không để portal 500 khi thiếu category

File sửa:

- `addons/M02_P0213/controllers/main.py`
- `addons/M02_P0213/views/resignation_portal_template.xml`

Điều chỉnh:

- `_get_resignation_category()` dùng `raise_if_not_found=False`.
- Nếu category thiếu, route GET hiển thị lỗi thân thiện qua biến `portal_error`.
- Route POST submit không tạo request khi thiếu category, redirect về portal với lỗi.

### 4.2. Khóa submit khi không tìm thấy employee portal

File sửa:

- `addons/M02_P0213/controllers/main.py`
- `addons/M02_P0213/views/resignation_portal_template.xml`

Điều chỉnh:

- `portal_resignation_submit()` redirect về portal nếu không tìm thấy employee liên kết user hiện tại.
- Template không render form submit nếu `employee` rỗng.

### 4.3. Siết route mark activity done

File sửa:

- `addons/M02_P0213/controllers/main.py`

Điều chỉnh:

- Bắt lỗi `activity_id` không hợp lệ.
- Vẫn bắt buộc activity thuộc request owner hiện tại.
- Vẫn bắt buộc `activity.user_id == request.env.user`.
- Hỗ trợ activity gắn với cả:
  - `approval.request`
  - `hr.employee`

Lý do:

- Bước 4 đã sửa hook survey done để hỗ trợ activity trên cả `approval.request` và `hr.employee`.
- Portal checklist giờ cũng đọc được cả hai kiểu activity liên quan tới request offboarding của user.

### 4.4. Bắt lỗi loại nghỉ việc không hợp lệ

File sửa:

- `addons/M02_P0213/controllers/main.py`

Điều chỉnh:

- Parse `resignation_type_id` bằng `try/except`.
- Nếu value không hợp lệ thì ghi `False`, không để route POST raise lỗi parse.

## 5. Phạm vi bảo mật portal đã chốt

- Search request portal khóa theo `request_owner_id = request.env.user.id`.
- Search activity done không dùng activity ID đơn lẻ để thao tác ngay; trước tiên phải tìm được request offboarding thuộc owner hiện tại.
- Sau khi đã xác nhận owner, vẫn kiểm tra activity được giao đúng cho user hiện tại.

## 6. Điểm giữ lại cho bước sau

- Bước 5 chưa siết ACL/record rule nền; phần đó thuộc Bước 6.
- Chưa chạy test HTTP thực tế qua Odoo server/browser.

## 7. Verification

- Đã chạy `python -m py_compile` cho `controllers/main.py`.
- Đã parse `views/resignation_portal_template.xml` ở mức XML.
- Kết quả: không có lỗi cú pháp Python/XML.
