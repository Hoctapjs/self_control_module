# Phase 2 - Bước 6 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 6` tập trung vào việc chuẩn hóa người nhận notify cho `CMT Lead` trong nhánh preventive, cụ thể là:

- làm rõ ai là người nhận notify chính thức
- giảm phụ thuộc vào fallback ngầm theo `member_ids[:1]`
- ghi lại trên request rule resolve lead nào đã được hệ thống sử dụng

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
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- source chuẩn `maintenance.team` trong:
  - [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)
  - [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

## 3. Hướng triển khai đã chọn

`Phase 2 - Bước 6` trong plan nhấn mạnh:

- chuẩn hóa người nhận notify
- làm rõ rule notify theo team/store

Hướng triển khai được chọn là:

- không tạo workflow notify mới
- tiếp tục tận dụng `mail.activity` chuẩn của Odoo
- bổ sung cấu hình lead rõ ràng trên `maintenance.team`
- giữ fallback tối thiểu để không làm gãy các flow preventive cũ

## 4. Model mới kế thừa `maintenance.team`

Trong [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py), đã thêm:

- `x_psm_0502_lead_user_id`

### Ý nghĩa

Field này dùng để cấu hình rõ:

- ai là `0502 Lead User`
- người này sẽ được ưu tiên nhận notify preventive của team

Nhờ đó:

- không còn phụ thuộc hoàn toàn vào `member_ids[:1]`
- rule notify trở nên tường minh hơn
- user quản trị có thể nhìn và chỉnh trực tiếp từ `Maintenance Team`

## 5. Thay đổi trong logic resolve lead

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), logic cũ:

- lấy `maintenance_team_id.member_ids[:1]`
- rồi fallback về `user_id`
- rồi fallback về `env.user`

Logic mới được gom lại thành helper:

- `_psm_get_lead_notification_resolution()`

### Rule resolve hiện tại

Thứ tự ưu tiên:

1. `maintenance_team_id.x_psm_0502_lead_user_id`
2. `maintenance_team_id.member_ids[:1]`
3. `user_id` của `maintenance.request`
4. `self.env.user`

### Ý nghĩa các mức fallback

#### `team_lead`

- team đã cấu hình rõ `0502 Lead User`
- đây là trạng thái đúng nhất theo nghiệp vụ bước 6

#### `team_member_fallback`

- team chưa cấu hình lead riêng
- hệ thống tạm lấy thành viên đầu tiên trong team

#### `technician_fallback`

- team không có lead riêng và cũng không có member phù hợp
- hệ thống tạm fallback về technician trên request

#### `current_user_fallback`

- không có dữ liệu nào khác để dùng
- hệ thống fallback về user đang thao tác để tránh fail hoàn toàn

## 6. Field mới trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `x_psm_0502_lead_notification_rule`

### Ý nghĩa

Field này lưu lại:

- hệ thống đã resolve lead theo rule nào tại thời điểm notify

Điều này giúp:

- dễ kiểm tra logic notify có đang chạy đúng như mong muốn không
- dễ lọc ra các request đang phải fallback thay vì dùng team lead cấu hình chuẩn

## 7. Thay đổi trong action `Notify CMT Lead`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_notify_lead()` đã được cập nhật.

Sau khi resolve được lead user, hệ thống sẽ ghi lại:

- `x_psm_0502_lead_notified_user_id`
- `x_psm_0502_lead_notification_rule`
- `x_psm_0502_lead_notified_at`

Như vậy sau mỗi lần notify, request không chỉ biết:

- ai đã được notify

mà còn biết:

- vì sao user đó được chọn

## 8. Cập nhật giao diện

### Trên `Maintenance Team`

Trong [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml), đã bổ sung:

- form view:
  - field `0502 Lead User`
- list view:
  - cột `0502 Lead User`
- search view:
  - field search `0502 Lead User`
  - filter `Configured 0502 Lead`

### Trên `Maintenance Request`

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung:

- form view:
  - field `Lead Notify Rule`
- list view:
  - cột ẩn/hiện `Lead Notify Rule`
- search view:
  - field search `Lead Notify Rule`
  - filter `Team Lead Notify`
  - group by `Lead Notify Rule`

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 6`, hiện chưa làm:

- chưa tạo activity template riêng cho từng loại team/store
- chưa mapping lead theo `Store Department`
- chưa thêm escalation chain nhiều cấp
- chưa thêm cảnh báo nếu preventive request phải fallback quá nhiều lần
- chưa thêm dashboard riêng để theo dõi tỷ lệ `team_lead` so với fallback

## 10. Cách test

### Case 1 - Team đã cấu hình `0502 Lead User`

1. Vào `Maintenance Teams`
2. Chọn một team
3. Điền `0502 Lead User`
4. Tạo hoặc mở một preventive request thuộc team đó
5. Bấm `Notify CMT Lead`

Kết quả mong đợi:

- `Lead Notified User` đúng bằng `0502 Lead User`
- `Lead Notify Rule = Team Lead`
- `Lead Notified At` có giá trị

### Case 2 - Team chưa cấu hình lead riêng nhưng có team member

1. Xóa hoặc bỏ trống `0502 Lead User`
2. Giữ `member_ids` có ít nhất một user
3. Bấm `Notify CMT Lead`

Kết quả mong đợi:

- `Lead Notified User` lấy từ team member đầu tiên
- `Lead Notify Rule = Team Member Fallback`

### Case 3 - Team không có lead riêng, không có member, nhưng request có technician

1. Để trống `0502 Lead User`
2. Để `member_ids` trống
3. Bảo đảm request có `user_id`
4. Bấm `Notify CMT Lead`

Kết quả mong đợi:

- `Lead Notified User` = technician của request
- `Lead Notify Rule = Technician Fallback`

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML well-formed bằng parser chuẩn Python: `OK`

## 12. File đã thay đổi

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [models/maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [views/maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
