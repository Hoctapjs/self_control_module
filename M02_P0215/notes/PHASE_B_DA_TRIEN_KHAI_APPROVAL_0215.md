# Phase B - Đã triển khai dùng Approvals cho phê duyệt Company Level module 0215

Ngày thực hiện: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/PLAN_THAY_THE_CUSTOM_BANG_APPROVAL_SURVEY_0215.md`
- `notes/PHASE_A_XAC_NHAN_APPROVAL_SURVEY_0215.md`

Source chính đã sửa:

- `__manifest__.py`
- `data/approval_category_data.xml`
- `models/__init__.py`
- `models/x_psm_approval_request.py`
- `models/x_psm_hr_discipline_record.py`
- `views/x_psm_hr_discipline_record_views.xml`

## 2. Phạm vi Phase B

Phase B thay phần CEO approval custom của 0215 bằng module chuẩn Odoo `approvals`.

Không triển khai Survey trong phase này.

Không xóa method legacy `action_psm_ceo_approve()` và `action_psm_ceo_reject()` để tránh đứt tương thích với dữ liệu/view/action cũ. Hai nút này đã được ẩn khỏi form chính.

## 3. Nội dung đã triển khai

### 3.1. Thêm dependency `approvals`

Đã thêm vào manifest:

```python
"approvals",
```

Lý do dùng `approvals` thay vì `approval`: source thực tế của Odoo trong workspace là `odoo/addons/approvals`.

### 3.2. Tạo Approval Category cho 0215

Đã thêm file:

- `data/approval_category_data.xml`

XML ID chính:

- `M02_P0215.approval_category_psm_discipline_company_level`

Tên category:

- `0215 - Phê duyệt kỷ luật cấp công ty`

Category dùng minimum approval = 1. Approver cụ thể không hard-code trong XML; khi tạo request, hệ thống lấy user từ group đang được dùng cho CEO custom hiện tại là `hr.group_hr_manager`.

Đã thêm implied group:

- `hr.group_hr_manager` -> `approvals.group_approval_user`

Mục đích: người đang có quyền CEO/HR Manager trong luồng cũ có quyền mở và xử lý approval request chuẩn.

### 3.3. Thêm bridge từ `approval.request` về hồ sơ 0215

Đã thêm model kế thừa:

- `models/x_psm_approval_request.py`

Field mới trên `approval.request`:

- `x_psm_discipline_record_id`

Bridge xử lý:

- Khi `approval.request.action_approve()` làm request đạt `request_status = approved`, gọi:
  - `_x_psm_on_approval_request_approved()`
- Khi `approval.request.action_refuse()` làm request đạt `request_status = refused`, gọi:
  - `_x_psm_on_approval_request_refused()`

### 3.4. Thêm field approval trên `x_psm.hr.discipline.record`

Các field mới:

- `x_psm_approval_request_id`
- `x_psm_approval_status`
- `x_psm_approval_requested_date`
- `x_psm_approval_completed_date`
- `x_psm_approval_refuse_reason`

Các field này dùng để link, hiển thị trạng thái và lưu snapshot ngày trình/ngày hoàn tất.

### 3.5. Sửa action trình duyệt

Đã sửa `action_psm_submit_for_approval()`:

- Store Level:
  - vẫn đi `issued -> notified`
  - vẫn gửi email thông báo nhân viên
- Company Level:
  - tạo `approval.request`
  - gắn approver từ `hr.group_hr_manager`
  - gọi `approval_request.action_confirm()`
  - chuyển hồ sơ 0215 sang `approval`

Nếu approval request cũ đã bị từ chối, lần trình lại sau khi HR điều chỉnh sẽ tạo request mới thay vì kẹt ở request cũ.

### 3.6. Mapping trạng thái

Luồng mới:

- 0215 `issued` + Company Level -> tạo `approval.request`
- `approval.request` pending -> 0215 `approval`
- `approval.request` approved -> 0215 `notified` + gửi email nhân viên
- `approval.request` refused -> 0215 `proposal`

Luồng Store Level không đổi:

- 0215 `issued` -> `notified`

### 3.7. Cập nhật view

Đã sửa `views/x_psm_hr_discipline_record_views.xml`:

- Ẩn nút legacy:
  - `CEO Phê duyệt`
  - `CEO Từ chối`
- Thêm smart button mở approval request.
- Thêm group hiển thị thông tin phê duyệt:
  - approval request;
  - approval status;
  - ngày trình;
  - ngày hoàn tất;
  - ghi chú từ chối.

## 4. Kiểm tra đã chạy

Đã chạy thành công:

- `python -m compileall .\addons\M02_P0215`
- Parse toàn bộ XML trong `addons/M02_P0215` bằng `xml.etree.ElementTree`

Chưa chạy:

- upgrade module trên database Odoo;
- test UI tạo approval request thật;
- test approver approve/refuse trên database.

## 5. Lưu ý rủi ro còn lại

- Cần upgrade module trên database test để xác nhận `approvals` đã install được.
- Cần kiểm tra user trong `hr.group_hr_manager` có đúng là nhóm CEO/approver nghiệp vụ thật không.
- Nếu sau này có CEO group riêng, nên đổi `_x_psm_get_approval_approver_users()` sang group đó thay vì `hr.group_hr_manager`.
- Bridge hiện chỉ sync khi approve/refuse qua action chuẩn của `approval.request`. Nếu ai đó sửa trực tiếp DB hoặc custom write trạng thái bất thường thì cần thêm cơ chế sync dự phòng.

## 6. Đề xuất Phase tiếp theo

Phase C triển khai Survey cho tường trình nhân viên:

- thêm dependency `survey`;
- tạo survey template tường trình;
- thêm link `survey.user_input` vào hồ sơ;
- sửa portal/action gửi yêu cầu tường trình để đi qua survey.
