# Phase 2 - Bước 1 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 1` tập trung chuẩn hóa thông tin về **nguồn phát sinh kỹ thuật / upstream** của `maintenance.request`, để chuẩn bị cho các bước tích hợp tiếp theo trong `Phase 2`.

Mục tiêu không phải là thay đổi object trung tâm của module.  
Object trung tâm vẫn là:

- `maintenance.request`

Mục tiêu của bước này là:

- phân biệt rõ giữa `nguồn nghiệp vụ` và `nguồn hệ thống`
- giữ luồng hiện tại của `Phase 1` ổn định
- chuẩn bị dữ liệu cho các nhánh như:
  - request tạo tay
  - request preventive do cron sinh ra
  - request đến từ helpdesk
  - request import từ nguồn ngoài

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi đối chiếu có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Những gì đã thêm

### Trên `maintenance.request`

Đã thêm 3 field mới:

- `x_psm_0502_source_system`
- `x_psm_0502_source_reference`
- `x_psm_0502_source_note`

Ý nghĩa:

- `x_psm_0502_source_system`
  - cho biết request đến từ hệ thống / entry point kỹ thuật nào
- `x_psm_0502_source_reference`
  - lưu mã tham chiếu upstream nếu có
- `x_psm_0502_source_note`
  - lưu ghi chú bổ sung về nguồn phát sinh hoặc ngữ cảnh mapping

### Giá trị của `x_psm_0502_source_system`

Hiện tại field này dùng `Selection`, gồm:

- `manual_request`
- `preventive_cron`
- `helpdesk_ticket`
- `imported_request`
- `other`

## 4. Cập nhật logic preventive request

Trong [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py), logic `_psm_prepare_preventive_request_vals()` đã được cập nhật để khi hệ thống tự sinh request preventive thì request mới sẽ có thêm:

- `x_psm_0502_source_system = preventive_cron`
- `x_psm_0502_source_reference = self.display_name`

Ý nghĩa:

- request preventive không chỉ biết `Request Source = Preventive Schedule`
- mà còn biết luôn `Source System = Preventive Cron`

Điều này giúp phân biệt:

- nguồn nghiệp vụ
- và nguồn hệ thống sinh request

## 5. Cập nhật giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung:

### Form view

- hiển thị:
  - `Request Source`
  - `Source System`
  - `Source Reference`
- thêm:
  - `Source Note`

### Tree view

- thêm cột tùy chọn:
  - `Source System`
  - `Source Reference`

### Search view

- thêm field tìm kiếm:
  - `Source System`
  - `Source Reference`
- thêm filter:
  - `Manual Request`
  - `Preventive Cron`
  - `Helpdesk Ticket`
- thêm group by:
  - `Source System`

## 6. Vì sao bước này chưa dùng `Many2one`

Ở bước này, `x_psm_0502_source_system` được giữ ở dạng `Selection`, chưa đổi sang `Many2one`.

Lý do:

- tập giá trị hiện tại ít và ổn định
- đây là metadata kỹ thuật nội bộ
- chưa cần user cấu hình thêm từ giao diện
- chưa cần thêm model master data mới chỉ để chứa vài giá trị cố định

Kết luận thiết kế ở bước này:

- `Request Source` tiếp tục là **master nghiệp vụ**
- `Source System` là **metadata kỹ thuật nhẹ**

## 7. Những gì chưa làm ở bước này

Để giữ đúng scope của `Phase 2 - Bước 1`, hiện chưa làm:

- chưa thêm dependency `helpdesk`
- chưa sinh request thật từ `helpdesk.ticket`
- chưa làm mapping import file / tích hợp ngoài
- chưa tạo model master mới cho `source_system`
- chưa thêm workflow đồng bộ đa nguồn

## 8. Cách test

### Case 1 - Request tạo tay

1. Upgrade module `M02_P0502`
2. Tạo một `maintenance.request` mới
3. Kiểm tra:
   - `Source System` mặc định là `Manual Request`

### Case 2 - Request preventive

1. Dùng flow preventive hiện tại để hệ thống sinh request
2. Mở request vừa sinh
3. Kiểm tra:
   - `Request Source = Preventive Schedule`
   - `Source System = Preventive Cron`
   - `Source Reference` có giá trị từ thiết bị

### Case 3 - Search / Filter / Group By

1. Mở danh sách `Maintenance Requests`
2. Kiểm tra search view
3. Test:
   - filter `Manual Request`
   - filter `Preventive Cron`
   - group by `Source System`

## 9. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 10. Kết luận

`Phase 2 - Bước 1` đã được triển khai theo hướng:

- không thay object trung tâm
- không kéo thêm module lớn quá sớm
- chuẩn hóa metadata nguồn phát sinh để chuẩn bị cho các bước tích hợp tiếp theo

Đây là bước mở nền dữ liệu cho `Phase 2`, không phải bước tích hợp sâu.  
Nó giúp các bước sau có thể mở rộng nguồn phát sinh mà không làm rối kiến trúc đã ổn định từ `Phase 1`.
