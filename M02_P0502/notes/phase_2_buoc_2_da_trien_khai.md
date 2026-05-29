# Phase 2 - Bước 2 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 2` tập trung vào việc chuẩn hóa dữ liệu đầu vào khi tạo `maintenance.request`, để giảm tình trạng request được tạo ra nhưng thiếu các thông tin cơ bản cần cho luồng 0502.

Mục tiêu của bước này là:

- làm rõ các field intake quan trọng
- giảm request thiếu thông tin ngay từ lúc tạo
- thêm validation nhẹ ở backend
- không làm nặng thêm kiến trúc của module

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này chỉ cần:

- custom nhẹ ở view
- custom nhẹ ở validation

Không nên:

- tạo thêm model mới
- kéo thêm module lớn
- áp validation quá cứng làm vỡ các flow tự động đang chạy ổn từ `Phase 1`

Vì vậy, bước này được triển khai theo hướng:

- đánh dấu rõ các field đầu vào quan trọng trên form
- thêm validation backend ở `create()` và `write()`
- chỉ kiểm tra các field thực sự có ý nghĩa ở bước intake

## 4. Các field intake đang được chuẩn hóa

Ở bước này, hệ thống xem các field sau là quan trọng khi tạo request:

- `Store Department`
- `Request Type`
- `Request Source`

Ngoài ra:

- nếu `Source System` là:
  - `helpdesk_ticket`
  - hoặc `imported_request`
- thì `Source Reference` cũng được xem là bắt buộc

## 5. Các thay đổi trong model

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_missing_request_input_labels()`
- `_psm_validate_request_input_data()`
- override `create()`
- override `write()`

### Ý nghĩa của từng phần

#### `_psm_get_missing_request_input_labels()`

Hàm này dùng để:

- kiểm tra request hiện tại còn thiếu field intake nào
- trả về danh sách label để hiển thị lỗi dễ hiểu cho user

#### `_psm_validate_request_input_data()`

Hàm này dùng để:

- gọi `_psm_get_missing_request_input_labels()`
- nếu còn thiếu field thì raise `UserError`

#### `create()`

Sau khi request được tạo, hệ thống chạy validation intake.

Ý nghĩa:

- tránh việc lưu request với bộ field đầu vào thiếu

#### `write()`

Khi user sửa các field intake quan trọng, hệ thống validate lại.

Việc này chỉ chạy khi có thay đổi các field intake liên quan, để tránh ảnh hưởng không cần thiết lên các bước sau.

## 6. Các thay đổi trong view

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung:

- `required="1"` cho:
  - `x_psm_0502_department_id`
  - `x_psm_0502_request_type_id`
  - `x_psm_0502_request_source_id`

Ý nghĩa:

- user nhìn form sẽ nhận ra ngay đâu là field đầu vào quan trọng
- giảm khả năng bỏ sót dữ liệu ngay từ giao diện

## 7. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 2`, hiện chưa làm:

- chưa tách một form intake riêng
- chưa thêm wizard tạo request
- chưa ép `priority` phải khác giá trị mặc định
- chưa thêm logic branch theo từng loại source system
- chưa thêm rule phức tạp theo cửa hàng / team / company

## 8. Cách test

### Case 1 - Thiếu field intake cơ bản

1. Upgrade module `M02_P0502`
2. Tạo một `maintenance.request` mới
3. Bỏ trống một trong các field:
   - `Store Department`
   - `Request Type`
   - `Request Source`
4. Thử save

Kết quả mong đợi:

- hệ thống chặn save
- báo lỗi nêu rõ các field còn thiếu

### Case 2 - Source system cần reference

1. Tạo một request mới
2. Chọn:
   - `Source System = Helpdesk Ticket`
   - hoặc `Source System = Imported Request`
3. Để trống `Source Reference`
4. Thử save

Kết quả mong đợi:

- hệ thống chặn save
- báo thiếu `Source Reference`

### Case 3 - Request hợp lệ

1. Điền đủ:
   - `Store Department`
   - `Request Type`
   - `Request Source`
2. Nếu dùng:
   - `Helpdesk Ticket`
   - hoặc `Imported Request`
   thì điền thêm `Source Reference`
3. Save request

Kết quả mong đợi:

- request được tạo bình thường

## 9. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 10. Kết luận

`Phase 2 - Bước 2` đã được triển khai theo hướng:

- chuẩn hóa đầu vào
- validation nhẹ
- không làm nặng kiến trúc

Đây là bước nền để các request đi vào luồng 0502 có chất lượng dữ liệu tốt hơn, trước khi triển khai sâu hơn các bước tiếp theo của `Phase 2`.
