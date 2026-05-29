# Phase 3 - Bước 6 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 6` tập trung vào việc:

- biến `Notify CMT Lead` từ dấu vết notify đơn thuần
- sang checkpoint có xác nhận nhận việc thực sự

Bước này không nhằm:

- tạo object assignment riêng
- dựng workflow notify nhiều tầng
- thêm escalation tự động nếu lead chưa acknowledge

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
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [phase_2_buoc_6_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_6_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 3`, `Bước 6` cần đi theo hướng:

- lead phải xác nhận đã nhận việc hay chưa
- nhìn được backlog theo lead owner thực tế

Hướng triển khai được chọn là:

- không thay object notify hiện tại
- không tạo object assignment riêng
- mở rộng trực tiếp trên `maintenance.request`:
  - thêm acknowledgment status
  - thêm action acknowledge
  - thêm filter queue theo lead owner

Lý do chọn hướng này:

- tận dụng được luồng `Notify CMT Lead` đã có ở `Phase 2`
- đủ để phân biệt “đã notify” với “đã nhận việc”
- chưa làm scope phình sang engine assignment hoặc escalation

## 4. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_lead_acknowledgment_status`
- `x_psm_0502_lead_acknowledged_by_id`
- `x_psm_0502_lead_acknowledged_at`

Đồng thời bổ sung action:

- `action_psm_acknowledge_lead_assignment()`

## 5. Ý nghĩa của các field mới

### 5.1. `Lead Acknowledgment Status`

Cho biết:

- lead đã xác nhận nhận việc chưa

Các trạng thái hiện tại:

- `Pending`
- `Acknowledged`

### 5.2. `Lead Acknowledged By`

Cho biết:

- user nào là người thực hiện xác nhận nhận việc

### 5.3. `Lead Acknowledged At`

Cho biết:

- thời điểm lead xác nhận đã nhận việc

## 6. Điều chỉnh trong `Notify CMT Lead`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_notify_lead()` đã được cập nhật.

Sau khi notify, request sẽ ghi:

- `Lead Notified User`
- `Lead Notify Rule`
- `Lead Notified At`
- `Lead Acknowledgment Status = Pending`
- reset:
  - `Lead Acknowledged By = False`
  - `Lead Acknowledged At = False`

Ý nghĩa:

- mỗi lần notify/re-notify sẽ tạo lại checkpoint acknowledgment mới
- tránh giữ trạng thái acknowledged cũ không còn đúng với lần giao việc hiện tại

## 7. Action xác nhận nhận việc

Đã thêm action:

- `action_psm_acknowledge_lead_assignment()`

Rule hiện tại:

- request phải có `Lead Notified User`
- chỉ đúng user đó mới được phép acknowledge

Nếu user khác bấm:

- hệ thống chặn bằng `UserError`

Khi acknowledge thành công:

- `Lead Acknowledgment Status = Acknowledged`
- `Lead Acknowledged By = current user`
- `Lead Acknowledged At = now`

## 8. Thay đổi trên giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã cập nhật:

### Header

- thêm nút:
  - `Acknowledge Lead Assignment`

Nút này chỉ hiện khi:

- request đã có `Lead Notified User`
- trạng thái acknowledgment chưa là `Acknowledged`
- user hiện tại chính là `Lead Notified User`

### Form view

- hiển thị thêm:
  - `Lead Acknowledgment Status`
  - `Lead Acknowledged By`
  - `Lead Acknowledged At`

### List view

- thêm cột optional:
  - `Lead Acknowledgment Status`
  - `Lead Acknowledged By`
  - `Lead Acknowledged At`

### Search view

- thêm field search tương ứng
- thêm filter:
  - `My Lead Queue`
  - `Lead Acknowledged`
  - `Lead Not Acknowledged`
- thêm group by:
  - `Lead Acknowledgment Status`

## 9. Ý nghĩa của các filter mới

### `My Lead Queue`

Lấy các request:

- `Lead Notified User = user hiện tại`
- đã được notify
- chưa archive
- chưa done

### `Lead Acknowledged`

Lấy các request:

- `Lead Acknowledgment Status = Acknowledged`

### `Lead Not Acknowledged`

Lấy các request:

- đã được notify
- nhưng `Lead Acknowledgment Status = Pending`

## 10. Những gì bước này cố ý chưa làm

Để tránh over-scope, `Phase 3 - Bước 6` chưa làm:

- activity riêng cho acknowledge
- escalation tự động nếu quá lâu chưa acknowledge
- SLA acknowledgment riêng
- object assignment riêng tách khỏi `maintenance.request`
- chuyển giao ownership planning tự động sau acknowledgment

Các phần này có thể mở tiếp nếu vận hành thực tế yêu cầu sâu hơn.

## 11. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 6` trả lời rõ hơn:

1. Lead nào đã được giao request preventive?
2. Lead đó đã xác nhận nhận việc hay chưa?
3. Những request nào đang nằm trong queue của đúng lead hiện tại?

Điều này giúp:

- `CMT Lead` có checkpoint rõ hơn
- `CMT` biết request đã giao mà chưa được acknowledge
- queue preventive bớt mơ hồ hơn so với mức chỉ có `Lead Notified`

## 12. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 13. Cách test

1. Upgrade `M02_P0502`.
2. Mở một preventive request.
3. Bấm `Notify CMT Lead`.
4. Kiểm tra:
- `Lead Acknowledgment Status = Pending`
- `Lead Notified User` có giá trị
5. Đăng nhập bằng đúng `Lead Notified User`.
6. Bấm `Acknowledge Lead Assignment`.
7. Kiểm tra:
- `Lead Acknowledgment Status = Acknowledged`
- `Lead Acknowledged By`
- `Lead Acknowledged At`
8. Test user khác không phải lead:
- bấm acknowledge
- kỳ vọng bị chặn
9. Dùng search filter:
- `My Lead Queue`
- `Lead Not Acknowledged`
- `Lead Acknowledged`

## 14. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
