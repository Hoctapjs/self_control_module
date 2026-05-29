# Phase 3 - Bước 5 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 5` tập trung vào việc:

- nâng phần preventive từ mức chỉ sinh request đúng hạn
- sang mức có monitoring rõ hơn cho preventive bị trễ hoặc bị treo

Bước này không nhằm:

- tạo workflow reschedule riêng
- tạo approval cho dời lịch preventive
- dựng preventive calendar / planning riêng ở lượt này

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
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [phase_2_buoc_5_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_5_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 3`, `Bước 5` cần đi theo hướng:

- thêm monitoring preventive aging
- chỉ mở rộng sang reschedule workflow nếu nhu cầu thật sự rõ

Hướng triển khai được chọn là:

- giữ nguyên cron và logic sinh request của `Phase 2`
- bổ sung lớp monitoring trên `maintenance.equipment`
- làm rõ exception trạng thái preventive bằng các field riêng và filter riêng

Lý do chọn hướng này:

- giải quyết đúng pain point nhìn preventive trễ / treo
- chưa làm scope phình sang workflow preventive mới
- bám đúng plan đã siết lại sau khi đối chiếu lưu đồ nghiệp vụ

## 4. Những gì đã thêm trên `maintenance.equipment`

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), đã bổ sung:

- `x_psm_0502_preventive_delay_days`
- `x_psm_0502_preventive_pending_cycle_count`
- `x_psm_0502_preventive_exception_status`

## 5. Ý nghĩa của các field mới

### 5.1. `Preventive Delay Days`

Field này cho biết:

- số ngày preventive hiện đang trễ hoặc bị treo

Mục tiêu:

- giúp người dùng nhìn được mức độ trễ theo số ngày, không chỉ theo status chung

### 5.2. `Preventive Pending Cycles`

Field này cho biết:

- số chu kỳ preventive đang tồn đọng ước tính

Mục tiêu:

- phân biệt được:
  - mới vừa trễ 1 kỳ
  - hay đã trễ nhiều kỳ liên tiếp

### 5.3. `Preventive Exception Status`

Field này là business status để nhìn nhanh tình trạng preventive exception:

- `Normal`
- `Missing Next Date`
- `Due Now`
- `Multi-cycle Overdue`
- `Open Request Stalled`

## 6. Logic monitoring preventive mới

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), đã thêm:

- `_compute_x_psm_0502_preventive_monitoring_fields()`

Hàm này dùng để tính:

- số ngày trễ
- số chu kỳ tồn đọng
- exception status

### 6.1. Khi nào là `Missing Next Date`

Nếu:

- đã bật preventive
- nhưng không có `Next Preventive Date`

thì:

- `Preventive Exception Status = Missing Next Date`

### 6.2. Khi nào là `Due Now`

Nếu:

- không có preventive request mở
- và thiết bị đã đến hạn đúng 1 chu kỳ

thì:

- `Preventive Exception Status = Due Now`

### 6.3. Khi nào là `Multi-cycle Overdue`

Nếu:

- không có preventive request mở
- nhưng số chu kỳ tồn đọng lớn hơn 1

thì:

- `Preventive Exception Status = Multi-cycle Overdue`

### 6.4. Khi nào là `Open Request Stalled`

Nếu:

- đã có preventive request mở
- và request đó treo quá ít nhất 1 chu kỳ preventive

thì:

- `Preventive Exception Status = Open Request Stalled`

## 7. Điều gì được giữ nguyên từ Phase 2

`Phase 3 - Bước 5` không thay đổi:

- logic chống sinh trùng preventive request
- rule không sinh request mới khi còn request preventive mở
- cách sync `last_preventive_request_id`
- cách cron tính và đẩy `next_preventive_date`

Nói ngắn gọn:

- phần “generate preventive request” vẫn giữ như `Phase 2`
- phần mới là “monitor preventive đang bị trễ / bị treo”

## 8. Thay đổi trên giao diện

Trong [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml), đã cập nhật:

### Form view

- hiển thị thêm:
  - `Preventive Exception Status`
  - `Preventive Delay Days`
  - `Preventive Pending Cycles`

### List view

- thêm cột optional:
  - `Preventive Exception Status`
  - `Preventive Delay Days`
  - `Preventive Pending Cycles`

### Search view

- thêm field search:
  - `Preventive Exception Status`
- thêm filter:
  - `Preventive Due Now`
  - `Preventive Multi-cycle Overdue`
  - `Preventive Open Request Stalled`
- thêm group by:
  - `Preventive Exception Status`

## 9. Những gì bước này cố ý chưa làm

Để tránh over-scope, `Phase 3 - Bước 5` chưa làm:

- nút reschedule preventive riêng
- approval dời lịch preventive
- preventive plan/calendar riêng
- activity / reminder / escalation tự động cho preventive overdue

Các phần này chỉ nên mở tiếp nếu vận hành thực tế xác nhận cần.

## 10. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 5` trả lời rõ hơn:

1. Thiết bị preventive này chỉ mới đến hạn, hay đã trễ nhiều kỳ?
2. Thiết bị có preventive request đang mở nhưng bị treo quá lâu không?
3. Có thiết bị nào bị thiếu `Next Preventive Date` cần xử lý cấu hình không?

Điều này giúp:

- `CMT`
- `CMT Lead`
- người theo dõi preventive

nhìn ra exception nhanh hơn mà chưa cần workflow dời lịch riêng.

## 11. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 12. Cách test

1. Upgrade `M02_P0502`.
2. Mở danh sách `Equipment`.
3. Kiểm tra các field mới:
- `Preventive Exception Status`
- `Preventive Delay Days`
- `Preventive Pending Cycles`
4. Test case `Due Now`:
- thiết bị bật preventive
- đến hạn hiện tại
- chưa có request preventive mở
- kỳ vọng `Preventive Exception Status = Due Now`
5. Test case `Multi-cycle Overdue`:
- thiết bị bị trễ quá hơn 1 chu kỳ
- chưa có request preventive mở
- kỳ vọng `Preventive Exception Status = Multi-cycle Overdue`
6. Test case `Open Request Stalled`:
- thiết bị có request preventive mở
- request này treo quá ít nhất 1 chu kỳ
- kỳ vọng `Preventive Exception Status = Open Request Stalled`
7. Dùng search filter:
- `Preventive Due Now`
- `Preventive Multi-cycle Overdue`
- `Preventive Open Request Stalled`

## 13. File đã thay đổi

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
