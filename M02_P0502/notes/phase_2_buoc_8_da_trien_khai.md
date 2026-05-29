# Phase 2 - Bước 8 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 8` tập trung vào việc chuẩn hóa điều kiện để một `maintenance.request` được xem là:

- đã đủ điều kiện để lập kế hoạch
- có thể bấm `Mark Planned`
- có thể đi tiếp sang bước tạo `FSM Task`

Mục tiêu chính là:

- làm rõ request nào thật sự `Ready To Plan`
- chặn các trường hợp lập kế hoạch khi request còn thiếu điều kiện nghiệp vụ
- thống nhất rule giữa `Bước 8` và `Bước 9`

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
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- làm rõ queue/request nào đã đủ điều kiện để lập kế hoạch
- chặn lập kế hoạch khi request còn thiếu bước intake hoặc inspection
- tránh việc `Mark Planned` và `Create FSM Task` dùng hai rule khác nhau

Hướng triển khai được chọn là:

- không kéo module `planning` vào ở bước này
- tiếp tục dùng `maintenance.request` làm nơi chuẩn hóa điều kiện lập kế hoạch
- thêm field tính toán `ready/block reason`
- gom validation planning vào helper dùng chung

Đây là hướng phù hợp với scope `custom nhẹ` của `Phase 2`.

## 4. Các field đã thêm

Trên `maintenance.request`, đã thêm:

- `x_psm_0502_ready_to_plan`
- `x_psm_0502_planning_block_reason`

### Ý nghĩa

#### `x_psm_0502_ready_to_plan`

Cho biết request này đã đủ điều kiện nghiệp vụ để đi vào bước lập kế hoạch hay chưa.

Đây là một cờ kỹ thuật để:

- điều khiển hiển thị nút
- hỗ trợ queue/search/filter
- giảm việc user phải tự suy luận thủ công

#### `x_psm_0502_planning_block_reason`

Tóm tắt các lý do khiến request chưa được xem là `Ready To Plan`.

Field này giúp user nhìn ngay:

- đang thiếu bước nào
- vì sao chưa được lập kế hoạch

## 5. Các helper và validation đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_planning_block_reasons()`
- `_compute_x_psm_0502_planning_ready_fields()`
- `_psm_validate_planning_inputs()`

### `_psm_get_planning_block_reasons()`

Hàm này trả về danh sách lý do nghiệp vụ khiến request chưa sẵn sàng để lập kế hoạch.

Rule hiện tại:

- luôn yêu cầu đủ intake cơ bản:
  - `Store Department`
  - `Request Type`
  - `Request Source`

- nếu là preventive request từ `preventive_schedule`:
  - bắt buộc đã có `Lead Notified At`

- nếu là request không phải preventive:
  - bắt buộc đã `CMT Receive`
  - bắt buộc đã `Initial Inspection`
  - bắt buộc `Initial Inspection Result = Action Needed`

### `_compute_x_psm_0502_planning_ready_fields()`

Hàm compute này:

- set `x_psm_0502_ready_to_plan = True/False`
- ghép các lý do thiếu thành `x_psm_0502_planning_block_reason`

### `_psm_validate_planning_inputs()`

Đây là validation dùng chung cho thao tác lập kế hoạch.

Ngoài điều kiện `ready to plan`, hàm này còn kiểm tra:

- phải có `Scheduled Date`
- phải có `Responsible`
- nếu có `Scheduled End` thì:
  - `Scheduled End >= Scheduled Date`

Nếu thiếu, hệ thống sẽ chặn bằng `UserError`.

## 6. Thay đổi trong logic nút hành động

### `Mark Planned`

`action_psm_mark_planned()` không còn chỉ kiểm tra sơ sài như trước.

Giờ đây action này sẽ gọi:

- `_psm_validate_planning_inputs()`

Tức là request chỉ được đánh dấu planned khi:

- đủ intake cơ bản
- đủ điều kiện nghiệp vụ theo loại request
- có lịch
- có người phụ trách
- khoảng thời gian hợp lệ

### `Create FSM Task`

`action_psm_create_fsm_task()` giờ cũng gọi cùng validation:

- `_psm_validate_planning_inputs()`

Ý nghĩa:

- tránh lệch rule giữa `Bước 8` và `Bước 9`
- không còn trường hợp:
  - request chưa thật sự ready
  - nhưng vẫn tạo được `FSM Task`

## 7. Thay đổi giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã cập nhật:

### Trên tab `Planning`

Hiển thị thêm:

- `Ready To Plan`
- `Planning Block Reason`

`Planning Block Reason` chỉ hiện khi request chưa ready.

### Trên nút `Mark Planned`

Nút này giờ chỉ hiện khi:

- request đã `Ready To Plan`
- và thỏa các điều kiện hiển thị khác như trước

### Trên list/search

Đã thêm field/filter/group by cho:

- `Ready To Plan`

Filter mới:

- `Ready To Plan`
- `Planning Blocked`

Group by mới:

- `Ready To Plan`

## 8. Ý nghĩa nghiệp vụ của bước này

Trước bước này:

- user phải tự hiểu request đã đủ điều kiện để plan hay chưa
- `Mark Planned` và `Create FSM Task` có nguy cơ lệch rule
- queue tổng hợp cho lead chưa cho biết request nào thật sự đã sẵn sàng để plan

Sau bước này:

- request có chỉ báo rõ ràng `Ready To Plan`
- request chưa đủ điều kiện sẽ có `Planning Block Reason`
- thao tác planning được siết lại
- rule giữa bước plan và bước điều phối task được thống nhất

Điều này giúp queue planning usable hơn cho `CMT Lead`.

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 8`, hiện chưa làm:

- chưa dùng module `planning`
- chưa tự động gán slot theo lịch thực tế
- chưa có wizard lập lịch riêng
- chưa có queue `Critical` riêng theo mức độ an toàn/khẩn
- chưa có cơ chế auto-reschedule

## 10. Cách test

### Case 1 - Preventive request chưa notify lead

1. Mở một preventive request từ `preventive_schedule`
2. Kiểm tra tab `Planning`

Kết quả mong đợi:

- `Ready To Plan = False`
- `Planning Block Reason` có `Lead Notification`

### Case 2 - Preventive request đã notify lead

1. Bấm `Notify CMT Lead`
2. Quay lại tab `Planning`

Kết quả mong đợi:

- `Ready To Plan = True`

### Case 3 - Store request chưa đủ điều kiện

1. Mở request từ cửa hàng
2. Để thiếu một trong các bước:
   - chưa `CMT Receive`
   - hoặc chưa `Initial Inspection`
   - hoặc `Inspection Result` khác `Action Needed`

Kết quả mong đợi:

- `Ready To Plan = False`
- `Planning Block Reason` hiển thị đúng phần còn thiếu

### Case 4 - Store request đã đủ điều kiện

1. Bảo đảm request:
   - đã `CMT Receive`
   - đã `Initial Inspection`
   - `Initial Inspection Result = Action Needed`
   - đủ `Store Department`, `Request Type`, `Request Source`

Kết quả mong đợi:

- `Ready To Plan = True`

### Case 5 - Validation của `Mark Planned`

1. Để request chưa ready hoặc thiếu:
   - `Scheduled Date`
   - `Responsible`
   - hoặc `Scheduled End < Scheduled Date`
2. Bấm `Mark Planned`

Kết quả mong đợi:

- hệ thống chặn và báo lỗi phù hợp

### Case 6 - Đồng bộ với `Create FSM Task`

1. Dùng request chưa đủ điều kiện planning
2. Bấm `Create FSM Task`

Kết quả mong đợi:

- hệ thống cũng chặn như `Mark Planned`

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML well-formed: `OK`

## 12. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
