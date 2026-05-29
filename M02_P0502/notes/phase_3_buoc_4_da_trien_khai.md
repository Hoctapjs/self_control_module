# Phase 3 - Bước 4 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 4` tập trung vào việc:

- nâng phần kiểm tra ban đầu từ mức field structured chung
- sang mức có checklist / worksheet chuẩn hóa theo loại thiết bị

Bước này không nhằm:

- dựng object checklist riêng
- kéo `maintenance_worksheet` vào ngay
- thêm evidence / ảnh / file đính kèm riêng ở lượt này

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [phase_2_buoc_4_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_4_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 3`, `Bước 4` cần đi theo hướng:

- chuẩn hóa checklist / worksheet theo loại thiết bị
- nhưng chưa nhất thiết phải tạo object checklist riêng hoặc dùng worksheet engine đầy đủ

Hướng triển khai được chọn là:

- đặt template checklist / worksheet ngay trên `maintenance.equipment.category`
- để `maintenance.request` tự lấy template theo `equipment.category`
- buộc người dùng ghi checklist result / worksheet thực tế khi category đã có template

Lý do chọn hướng này:

- tận dụng được `category_id` chuẩn của Odoo
- đúng với nhu cầu “theo loại thiết bị”
- tránh mở scope quá sớm sang object checklist hoặc module worksheet riêng

## 4. Những gì đã thêm trên `maintenance.equipment.category`

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), đã bổ sung:

- `x_psm_0502_inspection_checklist_template`
- `x_psm_0502_inspection_worksheet_template`

### 4.1. `0502 Inspection Checklist Template`

Field này dùng để cấu hình:

- checklist kiểm tra ban đầu chuẩn cho từng loại thiết bị

Ví dụ:

- kiểm tra nguồn điện
- kiểm tra cảnh báo lỗi
- kiểm tra nhiệt độ / rung / tiếng ồn

### 4.2. `0502 Inspection Worksheet Template`

Field này dùng để cấu hình:

- khung worksheet để ghi nhận chi tiết việc kiểm tra ban đầu

Mục tiêu:

- giúp `CMT` có khung ghi nhận nhất quán theo loại thiết bị

## 5. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_inspection_checklist_template`
- `x_psm_0502_inspection_worksheet_template`
- `x_psm_0502_inspection_checklist_result`
- `x_psm_0502_inspection_worksheet`

## 6. Ý nghĩa của các field mới trên request

### 6.1. `Inspection Checklist Template`

Là checklist mẫu readonly được lấy từ `equipment.category`.

### 6.2. `Inspection Worksheet Template`

Là worksheet mẫu readonly được lấy từ `equipment.category`.

### 6.3. `Inspection Checklist Result`

Là nội dung checklist thực tế mà `CMT` ghi lại khi kiểm tra request cụ thể.

### 6.4. `Inspection Worksheet`

Là worksheet thực tế của request, phản ánh kết quả kiểm tra ban đầu có cấu trúc hơn.

## 7. Logic lấy template theo loại thiết bị

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_compute_x_psm_0502_inspection_template_fields()`

Rule hiện tại:

- request lấy template từ:
  - `equipment_id.category_id.x_psm_0502_inspection_checklist_template`
  - `equipment_id.category_id.x_psm_0502_inspection_worksheet_template`

Ý nghĩa:

- cùng một loại thiết bị sẽ có chung khung kiểm tra ban đầu
- không phải nhập lại checklist/worksheet mẫu trên từng request

## 8. Điều chỉnh validation của `Mark Inspected`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_mark_inspected()` vẫn giữ validation structured của `Phase 2`, gồm:

- `Initial Inspection Result`
- `Symptom Status`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`

Ngoài ra đã bổ sung thêm rule:

- nếu có `Inspection Checklist Template`
  - bắt buộc phải có `Inspection Checklist Result`
- nếu có `Inspection Worksheet Template`
  - bắt buộc phải có `Inspection Worksheet`

Ý nghĩa:

- nếu category đã định nghĩa checklist/worksheet chuẩn
- người dùng không thể bỏ qua phần ghi nhận thực tế tương ứng

## 9. Thay đổi trên giao diện

### 9.1. `Equipment Category`

Trong [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml), đã cập nhật:

- form category hiển thị:
  - `0502 Inspection Checklist Template`
  - `0502 Inspection Worksheet Template`
- list category có thêm cột optional tương ứng

### 9.2. `Maintenance Request`

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Initial Inspection` đã được mở rộng với:

- `Inspection Checklist Template` readonly
- `Inspection Checklist Result`
- `Inspection Worksheet Template` readonly
- `Inspection Worksheet`

### 9.3. List / Search

Đã bổ sung:

- cột optional:
  - `Inspection Checklist Result`
  - `Inspection Worksheet`
- filter:
  - `Inspection Checklist Recorded`
  - `Inspection Worksheet Recorded`

## 10. Những gì bước này cố ý chưa làm

Để tránh over-scope, `Phase 3 - Bước 4` chưa làm:

- object checklist line riêng
- object worksheet riêng
- file evidence / ảnh / attachment riêng cho từng mục checklist
- mapping checklist nhiều tầng phức tạp hơn một level `equipment.category`

Các phần này có thể là bước sau nếu nghiệp vụ thực tế yêu cầu sâu hơn.

## 11. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 4` rõ hơn ở các điểm:

1. Mỗi loại thiết bị có thể có checklist kiểm tra chuẩn riêng.
2. Mỗi loại thiết bị có thể có worksheet ghi nhận chuẩn riêng.
3. Request cụ thể phải ghi lại kết quả checklist / worksheet thực tế nếu template đã tồn tại.

Điều này giúp:

- kiểm tra ban đầu nhất quán hơn
- giảm phụ thuộc vào ghi chú tự do
- chuẩn bị dữ liệu tốt hơn cho các bước proposal / planning / execution về sau

## 12. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 13. Cách test

1. Upgrade `M02_P0502`.
2. Vào `Equipment Category`.
3. Cấu hình:
- `0502 Inspection Checklist Template`
- `0502 Inspection Worksheet Template`
4. Mở request có `equipment_id` thuộc category đó.
5. Vào tab `Initial Inspection`.
6. Kiểm tra:
- template hiện ra đúng theo category
7. Thử bấm `Mark Inspected` khi chưa điền:
- `Inspection Checklist Result`
- `Inspection Worksheet`
- kỳ vọng bị chặn nếu category có template tương ứng
8. Điền đủ rồi bấm lại:
- kỳ vọng pass
9. Dùng search filter:
- `Inspection Checklist Recorded`
- `Inspection Worksheet Recorded`

## 14. File đã thay đổi

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
