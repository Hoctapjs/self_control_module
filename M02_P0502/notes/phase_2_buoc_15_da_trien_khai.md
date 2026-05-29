# Phase 2 - Bước 15 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 15` tập trung vào việc nâng bước:

- yêu cầu xuất kho vật tư

từ mức:

- chỉ tạo được một `stock.picking` dạng “phiếu khung”

sang mức:

- `stock.picking` usable thật
- có cấu hình source/destination rõ ràng
- có sẵn các dòng vật tư từ bước đánh giá vật tư

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
- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [phase_2_buoc_14_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_14_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- chuẩn hóa operation type
- chuẩn hóa source/destination location
- xem có nên sinh sẵn move line từ nội dung vật tư phát sinh

Hướng triển khai được chọn là:

- thêm cấu hình flow kho trên `maintenance.team`
- dùng helper resolve stock flow theo team trước, warehouse sau
- tự sinh `move_ids` từ `Material Detail Lines` của bước 14

Lý do chọn hướng này:

- tận dụng dữ liệu đã có từ `Phase 2 - Bước 14`
- tránh người dùng phải nhập lại dòng vật tư trên picking
- vẫn giữ scope vừa phải, không kéo thêm wizard hay engine mới

## 4. Cấu hình mới trên `maintenance.team`

Trong [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py), đã bổ sung:

- `x_psm_0502_material_picking_type_id`
- `x_psm_0502_material_source_location_id`
- `x_psm_0502_material_destination_location_id`

### Ý nghĩa

#### `0502 Material Picking Type`

Là operation type nội bộ được ưu tiên dùng khi request 0502 tạo stock picking.

#### `0502 Material Source Location`

Là location nguồn ưu tiên cho flow xuất vật tư.

#### `0502 Material Destination Location`

Là location đích ưu tiên cho flow xuất vật tư.

## 5. Thay đổi ở `maintenance.team` view

Trong [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml), đã cập nhật:

- form hiển thị 3 field cấu hình material flow
- list hiển thị nhanh `0502 Material Picking Type`
- search thêm:
  - `Configured 0502 Material Flow`

Ý nghĩa:

- người vận hành có thể cấu hình từng team
- dễ nhìn team nào đã sẵn sàng cho flow kho 0502

## 6. Helper resolve stock flow mới

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_material_stock_flow_resolution()`

Helper này resolve:

- warehouse
- picking type
- rule đã dùng
- source location
- destination location

### Thứ tự resolve

#### Picking Type

1. `0502 Material Picking Type` trên `maintenance.team`
2. `warehouse.int_type_id`
3. generic internal picking type fallback

#### Source / Destination Location

1. location cấu hình trên `maintenance.team`
2. default location của `stock.picking.type`
3. `warehouse.lot_stock_id`

Nếu không resolve được source/destination location hợp lệ:

- hệ thống chặn

## 7. Thay đổi trong `action_psm_create_stock_picking()`

Action này đã được nâng từ “phiếu khung” sang “phiếu usable”.

### Trước khi tạo picking

Action sẽ:

- yêu cầu đã qua `Material Assessment`
- yêu cầu `Has Material Request = True`
- gọi lại validation structured material của bước 14

### Khi tạo picking

Action sẽ:

- dùng stock flow đã resolve
- gán:
  - `picking_type_id`
  - `location_id`
  - `location_dest_id`
- giữ các metadata cũ:
  - `origin`
  - `partner_id`
  - `note`
  - `x_psm_0502_request_id`

### Tự sinh move lines

Action giờ sẽ tự tạo `move_ids` từ `Material Detail Lines`:

- `Material` -> `product_id`
- `Estimated Quantity` -> `product_uom_qty`
- `UoM` -> `product_uom`

Ý nghĩa:

- nếu bước 14 đã khai vật tư đúng thì bước 15 không cần nhập lại

## 8. Ý nghĩa nghiệp vụ của bước này

Ở `Phase 1`, bước 15 chủ yếu là:

- có một phiếu kho để mở được

Sau khi triển khai `Phase 2 - Bước 15`, bước này đã rõ hơn:

- request nào đi theo flow kho nội bộ
- flow đó lấy operation type nào
- lấy từ location nào
- chuyển đến location nào
- chuyển các vật tư nào với số lượng bao nhiêu

Điều này làm bước 16 dễ kiểm tồn hơn vì:

- picking đã có dữ liệu vật tư thực tế ngay từ đầu

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 15`, hiện chưa làm:

- chưa tự chọn location theo từng dòng vật tư
- chưa tách source khác nhau theo từng `Expected Source`
- chưa có logic reservation theo nguồn `store_spare` hay `technician_stock`
- chưa map trực tiếp `Expected Source` thành nhiều flow picking khác nhau

## 10. Cách test

### Case 1 - Team đã cấu hình stock flow

1. Upgrade `M02_P0502`
2. Vào `Maintenance Team`
3. Cấu hình:
   - `0502 Material Picking Type`
   - `0502 Material Source Location`
   - `0502 Material Destination Location`
4. Mở request đã hoàn tất `Phase 2 - Bước 14`
5. Bấm `Create Stock Picking`

Kết quả mong đợi:

- tạo được picking
- `Operation Type` đúng theo cấu hình team
- `Source Location` / `Destination Location` đúng theo cấu hình team

### Case 2 - Không cấu hình team, dùng fallback warehouse

1. Bỏ cấu hình flow kho trên team
2. Giữ dữ liệu bước 14 đầy đủ
3. Bấm `Create Stock Picking`

Kết quả mong đợi:

- hệ thống fallback về internal flow chuẩn của warehouse
- vẫn tạo được picking nếu warehouse đã cấu hình đúng

### Case 3 - Kiểm tra auto move lines

1. Trên request, tạo 1 hoặc nhiều `Material Detail Lines`
2. Bấm `Create Stock Picking`
3. Mở picking

Kết quả mong đợi:

- các dòng vật tư đã có sẵn trong picking
- số lượng khớp với `Estimated Quantity`

### Case 4 - Dữ liệu bước 14 chưa hợp lệ

1. Tạo request có `Has Material Request = True`
2. Cố tình không tạo dòng vật tư hoặc để quantity không hợp lệ
3. Bấm `Create Stock Picking`

Kết quả mong đợi:

- hệ thống chặn theo validation của bước 14

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse: `OK`

## 12. File đã thay đổi

- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
