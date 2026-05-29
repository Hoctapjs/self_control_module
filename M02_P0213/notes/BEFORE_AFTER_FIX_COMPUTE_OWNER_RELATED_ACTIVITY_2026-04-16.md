# Before/After fix compute `x_psm_0213_owner_related_activity_ids` - 2026-04-16

## Thông tin thay đổi

- Module: `M02_P0213_00`
- File sửa: `addons/M02_P0213_00/models/resignation_request.py`
- Field liên quan: `x_psm_0213_owner_related_activity_ids`
- Hàm liên quan: `_compute_owner_related_activity_ids`
- Ngày thực hiện: `2026-04-16`

## Bối cảnh lỗi

Khi mở một số record `approval.request`, Odoo phát sinh lỗi:

```python
ValueError: Compute method failed to assign approval.request(8,).x_psm_0213_owner_related_activity_ids
```

Nguyên nhân chính là field computed `x_psm_0213_owner_related_activity_ids` đang:

- `search()` bằng `sudo()`
- nhưng `browse()` và gán giá trị bằng env thường

Điều này có thể gây lỗi khi user hiện tại không có đủ quyền đọc `mail.activity`, dẫn đến compute không gán được giá trị hợp lệ vào field.

## Before

Trước khi sửa:

- Field `x_psm_0213_owner_related_activity_ids` chưa có `compute_sudo=True`
- Hàm `_compute_owner_related_activity_ids()` dùng:
  - `ActivitySudo = self.env["mail.activity"].sudo().with_context(active_test=False)`
  - `Activity = self.env["mail.activity"].with_context(active_test=False)`
- Logic thực tế:
  - tìm `activity_ids` bằng `ActivitySudo.search(...)`
  - sau đó gán bằng `Activity.browse(activity_ids)`

Rủi ro của cách làm cũ:

- `search()` lấy được dữ liệu nhờ `sudo()`
- nhưng lúc `browse()` bằng quyền user thường, một số record `mail.activity` có thể không còn đọc được
- từ đó Odoo báo lỗi `Compute method failed to assign ...`

## After

Sau khi sửa:

- Thêm `compute_sudo=True` vào field `x_psm_0213_owner_related_activity_ids`
- Hàm `_compute_owner_related_activity_ids()` dùng `ActivitySudo` xuyên suốt cho cả:
  - `browse([])`
  - `search(...)`
  - `browse(activity_ids)`
  - assign vào field

Logic mới giúp:

- compute luôn chạy ổn định trong context có quyền đọc `mail.activity`
- tránh trường hợp lấy được ID bằng `sudo()` nhưng lại không gán được recordset bằng quyền user thường
- giảm khả năng phát sinh lỗi cache/assign cho field computed trên form `approval.request`

## Tóm tắt before/after

Before:

- compute chưa dùng `compute_sudo=True`
- `search` bằng `sudo`, nhưng `browse/assign` bằng env thường
- có thể lỗi với user không đủ quyền đọc `mail.activity`

After:

- field có `compute_sudo=True`
- toàn bộ compute dùng `sudo()` nhất quán
- an toàn hơn khi form được mở bởi user nghiệp vụ

## Ghi chú triển khai

Với thay đổi này, khi deploy lên server:

- cần cập nhật file Python mới
- cần restart Odoo service/container để nạp code mới

Thông thường thay đổi này không yêu cầu thay đổi cấu trúc database vì chỉ là sửa logic compute trong Python.
