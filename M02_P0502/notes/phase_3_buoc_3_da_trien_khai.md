# Phase 3 - Bước 3 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 3` tập trung vào việc:

- biến việc tiếp nhận thành một checkpoint có ownership rõ ràng
- nhìn được SLA tiếp nhận ở mức dữ liệu và filter
- phân biệt request nào đang pending tiếp nhận, request nào receive đúng hạn, request nào receive trễ

Bước này không nhằm:

- tạo workflow escalation tự động phức tạp
- dựng activity/reminder engine riêng
- tách object intake riêng khỏi `maintenance.request`

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
- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [phase_3_buoc_2_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_3_buoc_2_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 3`, `Bước 3` cần đi theo hướng:

- có SLA intake
- có ownership rõ hơn
- nhưng chỉ nên thêm activity/reminder/escalation nếu nhu cầu thực sự rõ

Hướng triển khai được chọn là:

- thêm cấu hình SLA intake theo `maintenance.team`
- thêm các field ownership và SLA trên `maintenance.request`
- mở rộng list/search/filter/group by để nhìn được trạng thái tiếp nhận
- chưa thêm activity hay escalation tự động

Lý do chọn hướng này:

- đủ để vận hành và theo dõi
- chưa làm scope phình sang cơ chế nhắc việc tự động
- bám đúng vai trò của `Bước 3` là checkpoint tiếp nhận

## 4. Những gì đã thêm trên `maintenance.team`

Trong [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py), đã bổ sung:

- `x_psm_0502_intake_sla_hours`

### Ý nghĩa

#### `0502 Intake SLA Hours`

Field này dùng để cấu hình:

- số giờ tối đa kỳ vọng từ lúc request vào hệ thống
- đến lúc `CMT` thực hiện `Receive`

Đây là đầu vào để hệ thống tính:

- deadline tiếp nhận
- kết quả SLA tiếp nhận

## 5. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_intake_owner_user_id`
- `x_psm_0502_intake_sla_deadline_at`
- `x_psm_0502_intake_sla_result`
- `x_psm_0502_intake_age_hours`

## 6. Ý nghĩa của các field mới trên request

### 6.1. `Intake Owner`

Cho biết:

- hiện request ở checkpoint tiếp nhận đang được xem là thuộc ai theo dõi

Đây là owner logic ở mức vận hành, không phải phân quyền cứng.

### 6.2. `Intake SLA Deadline`

Cho biết:

- deadline kỳ vọng để request phải được `CMT Receive`

Deadline này được tính từ:

- `create_date`
- cộng với `0502 Intake SLA Hours` của team

### 6.3. `Intake SLA Result`

Cho biết kết quả SLA sau khi request đi qua checkpoint tiếp nhận:

- `Pending`
- `On Time`
- `Late`

### 6.4. `Intake Age (Hours)`

Cho biết tuổi của checkpoint tiếp nhận tính theo giờ:

- nếu chưa receive thì tính đến hiện tại
- nếu đã receive thì tính đến `Received At`

## 7. Logic resolve `Intake Owner`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_intake_owner_user()`

Rule resolve hiện tại:

1. `Received By (CMT)` nếu request đã receive
2. `0502 Lead User` của team
3. member đầu tiên của team
4. technician trên request
5. `create_uid`

Ý nghĩa:

- khi request chưa receive, hệ thống vẫn có một owner logic để nhìn queue
- khi đã receive, ownership sẽ chuyển về đúng người đã tiếp nhận

## 8. Logic tính SLA tiếp nhận

Đã thêm các compute:

- `_compute_x_psm_0502_intake_sla_deadline_at()`
- `_compute_x_psm_0502_intake_sla_result()`
- `_compute_x_psm_0502_intake_age_hours()`

### 8.1. `Intake SLA Deadline`

Nếu có:

- `create_date`
- `0502 Intake SLA Hours`

thì hệ thống tính:

- `create_date + sla_hours`

Nếu không có SLA trên team:

- deadline để trống

### 8.2. `Intake SLA Result`

Rule hiện tại:

- chưa receive:
  - `Pending`
- đã receive và receive sau deadline:
  - `Late`
- đã receive và không quá deadline:
  - `On Time`

### 8.3. `Intake Age (Hours)`

Rule hiện tại:

- nếu chưa receive:
  - tính từ `create_date` đến thời điểm hiện tại
- nếu đã receive:
  - tính từ `create_date` đến `Received At`

## 9. Thay đổi trên giao diện

### 9.1. `Maintenance Team`

Trong [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml), đã cập nhật:

- form hiển thị `0502 Intake SLA Hours`
- list hiển thị optional `0502 Intake SLA Hours`
- search thêm field và filter:
  - `Configured 0502 Intake SLA`

### 9.2. `Maintenance Request`

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã cập nhật:

- form hiển thị:
  - `Intake Owner`
  - `Intake SLA Deadline`
  - `Intake SLA Result`
  - `Intake Age (Hours)`
- list thêm các cột optional tương ứng
- search thêm field tương ứng
- thêm filter:
  - `Intake Overdue`
  - `Received Late`
  - `Received On Time`
- thêm group by:
  - `Intake Owner`
  - `Intake SLA Result`

## 10. Ý nghĩa của các filter mới

### `Intake Overdue`

Lấy các request:

- chưa receive
- có `Intake SLA Deadline`
- deadline đã qua

### `Received Late`

Lấy các request:

- đã receive
- nhưng `Intake SLA Result = Late`

### `Received On Time`

Lấy các request:

- đã receive
- và `Intake SLA Result = On Time`

## 11. Những gì bước này cố ý chưa làm

Để tránh over-scope, `Phase 3 - Bước 3` chưa làm:

- activity tự động khi sắp quá hạn
- escalation sang lead hoặc manager
- cron riêng cho overdue intake
- dashboard SLA riêng
- phân quyền owner intake cứng theo user

Các phần này có thể là bước sau nếu vận hành thực tế yêu cầu.

## 12. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 3` trả lời rõ hơn các câu hỏi:

1. Request này ở checkpoint tiếp nhận đang thuộc ai theo dõi?
2. Deadline tiếp nhận là khi nào?
3. Request này đang pending, đúng hạn hay trễ hạn?
4. Request đã “nằm” trong intake bao lâu?

Điều này giúp:

- `CMT` và `CMT Lead` nhìn queue rõ hơn
- có cơ sở theo dõi SLA intake
- tách rõ `Bước 3` với các bước điều phối sâu hơn về sau

## 13. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 14. Cách test

1. Upgrade `M02_P0502`.
2. Vào `Maintenance Team`.
3. Cấu hình `0502 Intake SLA Hours` cho một team.
4. Tạo request mới thuộc team đó.
5. Kiểm tra trên request:
- `Intake Owner`
- `Intake SLA Deadline`
- `Intake Age (Hours)`
6. Test case 1:
- receive trước hạn
- kỳ vọng `Intake SLA Result = On Time`
7. Test case 2:
- để quá deadline rồi mới receive
- kỳ vọng `Intake SLA Result = Late`
8. Kiểm tra search filter:
- `Intake Overdue`
- `Received Late`
- `Received On Time`

## 15. File đã thay đổi

- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
