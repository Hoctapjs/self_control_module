# Phase 2 - Bước 5 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 5` tập trung vào việc làm chắc logic preventive trong nhánh bảo trì định kỳ, đặc biệt là:

- xác định rõ khi nào thiết bị được xem là còn preventive request đang mở
- giảm rủi ro sinh trùng preventive request
- làm rõ trạng thái preventive ngay trên thiết bị

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
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)

## 3. Hướng triển khai đã chọn

`Phase 2 - Bước 5` trong plan nhấn mạnh:

- làm chắc logic preventive
- giảm rủi ro sinh trùng

Hướng triển khai được chọn là:

- chưa tách module mới
- chưa thay đổi object trung tâm
- chỉ bổ sung helper, status và rule rõ hơn trên `maintenance.equipment`

## 4. Các field mới đã thêm trên `maintenance.equipment`

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), đã thêm:

- `x_psm_0502_has_open_preventive_request`
- `x_psm_0502_preventive_status`

### Ý nghĩa

#### `x_psm_0502_has_open_preventive_request`

Field kỹ thuật để cho biết:

- thiết bị này hiện có preventive request đang mở hay không

#### `x_psm_0502_preventive_status`

Field trạng thái tổng hợp để user nhìn nhanh tình trạng preventive của thiết bị.

Các giá trị hiện có:

- `not_enabled`
- `no_next_date`
- `scheduled`
- `due`
- `open_request`

## 5. Ý nghĩa của các trạng thái preventive

### `Not Enabled`

- chưa bật lịch preventive cho thiết bị

### `Missing Next Date`

- đã bật preventive
- nhưng chưa có `Next Preventive Date`

### `Scheduled`

- đã có ngày preventive tiếp theo
- nhưng chưa tới hạn

### `Due to Generate`

- đã đến hạn sinh preventive request
- và hiện không có preventive request mở

### `Open Preventive Request`

- đang có ít nhất một preventive request mở
- vì vậy không được sinh thêm request mới

## 6. Các helper method đã thêm

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), đã thêm:

- `_compute_x_psm_0502_preventive_status()`
- `_psm_find_open_preventive_request()`
- `_psm_can_generate_preventive_request()`

### `_psm_find_open_preventive_request()`

Hàm này dùng để tìm preventive request đang mở của một thiết bị.

Điều kiện request được xem là “preventive open”:

- `equipment_id` đúng thiết bị
- `maintenance_type = preventive`
- `x_psm_0502_request_source_code = preventive_schedule`
- `archive = False`
- `stage_id.done = False`

### `_psm_can_generate_preventive_request()`

Hàm này trả lời câu hỏi:

- thiết bị này hiện tại có được phép sinh preventive request mới hay không

Chỉ được sinh khi:

- đã bật preventive
- có `Next Preventive Date`
- `Next Preventive Date <= today`
- không có preventive request mở

### `_compute_x_psm_0502_preventive_status()`

Hàm này tính trạng thái preventive để hiển thị trên thiết bị, dựa trên:

- đã bật preventive chưa
- có `Next Preventive Date` chưa
- đã tới hạn chưa
- có preventive request mở hay chưa

## 7. Thay đổi quan trọng trong cron

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), cron sinh preventive request đã được siết lại.

### Logic cũ có rủi ro

Khi đã có preventive request mở:

- cron vẫn có thể đẩy `Next Preventive Date` sang kỳ tiếp theo

Điều này làm luồng preventive thiếu chặt và dễ khó kiểm soát.

### Logic mới

Nếu thiết bị đã có preventive request mở:

- cron **không sinh request mới**
- cron **không đẩy `Next Preventive Date` sang kỳ sau**
- chỉ:
  - sync `Last Preventive Request`
  - notify lead nếu request mở đó chưa được notify

Nếu thiết bị không còn preventive request mở và đã tới hạn:

- cron sinh đúng 1 preventive request mới
- sau đó cập nhật:
  - `Last Preventive Request`
  - `Next Preventive Date`

## 8. Cập nhật giao diện

Trong [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml), đã bổ sung:

### Form view

- `Preventive Status`
- `Has Open Preventive Request` là field kỹ thuật, không hiển thị cho user cuối

### Tree view

- hiển thị `Preventive Status`

### Search view

- thêm field search:
  - `Preventive Status`
- thêm filter:
  - `Preventive Open Request`
  - `Preventive Missing Next Date`
- thêm group by:
  - `Preventive Status`

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 5`, hiện chưa làm:

- chưa tạo preventive planning object riêng
- chưa có preventive calendar riêng
- chưa có simulation/scheduler preview
- chưa có boundary test automation theo cron job ở mức unit/integration
- chưa custom màn hình dashboard preventive riêng

## 10. Cách test

### Case 1 - Còn preventive request mở

1. Chọn một thiết bị có:
   - `Enable Preventive Schedule = True`
   - `Next Preventive Date <= hôm nay`
2. Đảm bảo thiết bị đã có một preventive request mở
3. Chạy cron preventive

Kết quả mong đợi:

- không sinh preventive request mới
- `Preventive Status = Open Preventive Request`
- `Next Preventive Date` không bị đẩy sang kỳ sau

### Case 2 - Đến hạn và không còn request mở

1. Chọn một thiết bị có:
   - `Enable Preventive Schedule = True`
   - `Next Preventive Date <= hôm nay`
2. Đảm bảo không còn preventive request mở
3. Chạy cron preventive

Kết quả mong đợi:

- sinh đúng 1 preventive request mới
- request mới có:
  - `Request Source = Preventive Schedule`
  - `Source System = Preventive Cron`
- `Last Preventive Request` được cập nhật
- `Next Preventive Date` nhảy sang kỳ tiếp theo

## 11. File đã thay đổi

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)

## 12. Kết luận

`Phase 2 - Bước 5` đã được triển khai theo hướng:

- làm rõ trạng thái preventive
- làm chắc rule sinh preventive request
- giảm rủi ro sinh trùng

Điểm quan trọng nhất của bước này là:

- **khi còn preventive request mở thì không sinh đợt mới và không đẩy lịch sang kỳ sau**

Đây là phần nền quan trọng để nhánh preventive trong `0502` vận hành ổn định hơn ở các bước tiếp theo của `Phase 2`. 
