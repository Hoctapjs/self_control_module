# Phase 2 - Bước 7 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 7` tập trung vào việc chuyển từ queue cơ bản sang queue usable theo vai trò `CMT Lead`, cụ thể là:

- tách các hàng đợi theo đúng góc nhìn vận hành
- giảm phụ thuộc vào việc user phải nhớ nhiều filter thủ công
- làm rõ nhóm request nào cần lead tổng hợp và ưu tiên xử lý

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
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Hướng triển khai đã chọn

`Phase 2 - Bước 7` trong plan nhấn mạnh:

- thay queue cơ bản bằng queue usable theo vai trò
- refine action/menu queue
- thêm search preset theo:
  - preventive
  - store request
  - action needed
  - overdue

Hướng triển khai được chọn là:

- không đổi object trung tâm
- không tạo model queue mới
- chỉ mở rộng `search`, `action`, `menu` trên `maintenance.request`

Đây là hướng phù hợp với scope `custom nhẹ`.

## 4. Search preset đã thêm

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung thêm các filter:

- `Store Request`
- `Preventive Request`
- `0502 Overdue`

### Ý nghĩa

#### `Store Request`

Lọc ra:

- request có `x_psm_0502_request_source_code = store_request`
- chưa archive
- chưa done

Mục đích:

- nhìn riêng nhánh phát sinh từ cửa hàng

#### `Preventive Request`

Lọc ra:

- request preventive
- chưa archive
- chưa done

Mục đích:

- nhìn riêng nhánh preventive đang còn mở

#### `0502 Overdue`

Lọc ra:

- request chưa đóng
- và quá hạn theo một trong hai trường hợp:
  - có `schedule_date` nhưng `schedule_date < hôm nay`
  - hoặc chưa có `schedule_date` nhưng `request_date < hôm nay`

Mục đích:

- giúp lead nhìn nhanh các request tồn đọng hoặc đã trễ hạn

## 5. Các queue/action/menu đã thêm

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung các action/menu mới:

- `0502 Preventive Queue`
- `0502 Store Action Needed`
- `0502 Overdue Queue`

Đồng thời giữ lại queue đã có:

- `0502 Requests To Plan`

### `0502 Requests To Plan`

Đây là queue tổng hợp cho `CMT Lead`.

Domain hiện tại gom 2 nhóm:

- preventive request đã được notify lead
- store request đã inspection và kết luận `action_needed`

Context mặc định:

- `Active`
- preset `Requests To Plan`
- group theo `Store Department`

### `0502 Preventive Queue`

Đây là queue riêng cho preventive đã sẵn sàng để lead theo dõi.

Domain:

- `maintenance_type = preventive`
- `x_psm_0502_request_source_code = preventive_schedule`
- `x_psm_0502_lead_notified_at != False`
- chưa archive
- chưa done

Context mặc định:

- `Active`
- preset `Preventive Queue`
- group theo `Team`

### `0502 Store Action Needed`

Đây là queue riêng cho request từ cửa hàng đã qua kiểm tra và xác định cần xử lý.

Domain:

- `x_psm_0502_request_source_code = store_request`
- `x_psm_0502_inspection_result = action_needed`
- chưa archive
- chưa done

Context mặc định:

- `Active`
- preset `Store Action Needed`
- group theo `Store Department`

### `0502 Overdue Queue`

Đây là queue ưu tiên để lead xử lý các request bị trễ hoặc tồn.

Domain:

- chưa archive
- chưa done
- quá hạn theo `schedule_date` hoặc `request_date`

Context mặc định:

- `Active`
- preset `0502 Overdue`
- group theo `Store Department`

## 6. Ý nghĩa nghiệp vụ của bước này

Trước bước này, user vẫn có thể làm việc bằng search/filter thủ công, nhưng:

- khó nhớ đúng tổ hợp filter
- khó tách riêng từng góc nhìn vận hành
- khó dùng ổn định cho vai trò `CMT Lead`

Sau bước này:

- lead có queue tổng hợp để lên kế hoạch
- có queue preventive riêng
- có queue store request cần xử lý riêng
- có queue overdue để ưu tiên

Điều này làm cho bước tổng hợp request thực tế usable hơn nhiều mà chưa cần dashboard mới.

## 7. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 7`, hiện chưa làm:

- chưa tạo dashboard lead riêng
- chưa thêm KPI/number card trên action/menu
- chưa có rule phân queue theo từng lead cụ thể
- chưa có saved favorite riêng theo user
- chưa có permission split riêng giữa `CMT` và `CMT Lead`

## 8. Cách test

### Case 1 - Queue tổng hợp `0502 Requests To Plan`

1. Vào `Maintenance > Maintenance Requests > 0502 Requests To Plan`
2. Kiểm tra queue có gom:
   - preventive request đã notify
   - store request `action_needed`

Kết quả mong đợi:

- queue mở đúng preset
- group mặc định theo `Store Department`

### Case 2 - Queue preventive riêng

1. Vào `Maintenance > Maintenance Requests > 0502 Preventive Queue`
2. Kiểm tra chỉ thấy preventive request đã notify

Kết quả mong đợi:

- không lẫn store request
- group mặc định theo `Team`

### Case 3 - Queue store action needed riêng

1. Vào `Maintenance > Maintenance Requests > 0502 Store Action Needed`
2. Kiểm tra chỉ thấy request:
   - source là `store_request`
   - inspection result là `action_needed`

Kết quả mong đợi:

- không lẫn preventive request
- group mặc định theo `Store Department`

### Case 4 - Queue overdue

1. Vào `Maintenance > Maintenance Requests > 0502 Overdue Queue`
2. Kiểm tra:
   - request có `schedule_date` quá hạn xuất hiện
   - request cũ chưa có `schedule_date` cũng xuất hiện

Kết quả mong đợi:

- queue tập trung được các request cần ưu tiên xử lý

## 9. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML well-formed: `OK`

## 10. File đã thay đổi

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
