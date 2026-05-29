# Phase 2 - Bước 14 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 14` tập trung vào việc nâng bước:

- kiểm tra phát sinh vật tư

từ mức:

- chỉ đánh dấu `có / không`

sang mức có cấu trúc hơn:

- vật tư nào
- số lượng dự kiến bao nhiêu
- dự kiến lấy từ nguồn nào

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
- [request_material_line.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_material_line.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần chuyển phần vật tư từ:

- boolean đơn giản

sang:

- dữ liệu vật tư thực tế có thể dùng tiếp cho các bước kho

Hướng triển khai được chọn là:

- giữ lại `x_psm_0502_has_material_request` để tiếp tục tương thích với flow cũ
- thêm model dòng vật tư phát sinh riêng
- nối model này vào `maintenance.request`
- siết lại `Mark Material Checked` để yêu cầu dữ liệu vật tư đầy đủ hơn

Lý do chọn hướng này:

- đúng intent nghiệp vụ của bước 14
- không làm vỡ flow của các bước 15, 16, 17, 18, 19
- tạo nền tốt hơn cho bước xuất kho và mua ngoài

## 4. Model mới đã thêm

Trong [request_material_line.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_material_line.py), đã thêm model:

- `x_psm_request_material_line`

### Các field chính

- `x_psm_request_id`
- `x_psm_product_id`
- `x_psm_estimated_qty`
- `x_psm_uom_id`
- `x_psm_source_type`
- `x_psm_note`
- `x_psm_sequence`

### Ý nghĩa

Mỗi dòng ghi nhận một vật tư phát sinh trong bước 14, gồm:

- vật tư cụ thể
- số lượng dự kiến
- đơn vị tính
- nguồn lấy dự kiến
- ghi chú ngắn nếu cần

## 5. Thay đổi trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_material_line_ids`
- `x_psm_0502_material_line_count`

### Ý nghĩa

#### `Material Detail Lines`

Là tập các dòng vật tư phát sinh của request.

#### `Material Line Count`

Là số dòng vật tư đã được ghi nhận, dùng để:

- hiển thị nhanh trên request
- filter/search dễ hơn

## 6. Validation mới ở bước 14

Đã thêm helper:

- `_psm_validate_material_assessment_inputs()`

Helper này được gọi trong:

- `action_psm_mark_material_checked()`

### Rule đang áp dụng

#### Trường hợp 1 - `Has Material Request = False`

- nếu không cần vật tư thì không bắt buộc có dòng vật tư
- nhưng nếu vẫn còn dòng vật tư thì hệ thống chặn

Ý nghĩa:

- tránh trạng thái dữ liệu mâu thuẫn

#### Trường hợp 2 - `Has Material Request = True`

Bắt buộc phải có ít nhất một dòng vật tư.

Mỗi dòng phải có:

- `Material`
- `Estimated Quantity > 0`
- `Expected Source`

Nếu thiếu, hệ thống chặn `Mark Material Checked`.

## 7. Thay đổi ở giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Material Assessment` đã được cập nhật:

- thêm `Material Line Count`
- thêm khu `Material Details`
- hiển thị one2many dạng inline editable để nhập trực tiếp:
  - `Material`
  - `Estimated Quantity`
  - `UoM`
  - `Expected Source`
  - `Line Note`

Ngoài ra:

- list view thêm `Material Line Count`
- search view thêm filter:
  - `Material Details Recorded`

## 8. Ý nghĩa nghiệp vụ của bước này

Ở `Phase 1`, bước 14 mới trả lời được:

- có phát sinh vật tư hay không

Sau khi triển khai `Phase 2 - Bước 14`, request bắt đầu trả lời rõ hơn:

- cần vật tư gì
- cần bao nhiêu
- dự kiến lấy từ đâu

Điều này giúp:

- bước 15 có dữ liệu tốt hơn để tạo stock picking
- bước 19 có dữ liệu tốt hơn để mua ngoài khi thiếu tồn
- giảm việc phải đọc note tự do để đoán vật tư

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 14`, hiện chưa làm:

- chưa tự sinh sẵn `stock.move` từ các dòng vật tư
- chưa tự map trực tiếp từng dòng sang dòng purchase
- chưa có tồn khả dụng theo từng nguồn ngay trên dòng vật tư
- chưa có wizard chuyên biệt cho material assessment

## 10. Cách test

### Case 1 - Không cần vật tư

1. Mở request đã qua `Service Assessment`
2. Đặt:
   - `Has Material Request = False`
3. Không thêm dòng vật tư
4. Bấm `Mark Material Checked`

Kết quả mong đợi:

- thao tác thành công

### Case 2 - Có vật tư nhưng chưa khai báo dòng chi tiết

1. Mở request đã qua `Service Assessment`
2. Đặt:
   - `Has Material Request = True`
3. Không thêm dòng vật tư
4. Bấm `Mark Material Checked`

Kết quả mong đợi:

- hệ thống chặn

### Case 3 - Có dòng vật tư nhưng dữ liệu chưa hợp lệ

1. Thêm một dòng vật tư
2. Cố tình để:
   - thiếu `Material`
   - hoặc `Estimated Quantity = 0`
   - hoặc thiếu `Expected Source`
3. Bấm `Mark Material Checked`

Kết quả mong đợi:

- hệ thống chặn và báo rõ dòng nào thiếu gì

### Case 4 - Dữ liệu vật tư đầy đủ

1. Đặt:
   - `Has Material Request = True`
2. Thêm một hoặc nhiều dòng vật tư hợp lệ
3. Bấm `Mark Material Checked`

Kết quả mong đợi:

- thao tác thành công
- `Material Checked By`
- `Material Checked At`

được ghi đúng

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse: `OK`

## 12. File đã thay đổi

- [request_material_line.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_material_line.py)
- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)
