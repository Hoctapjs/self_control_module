# Phase 1 - Bước 9 Đã Triển Khai

## 1. Mục tiêu của bước 9

`Bước 9` trong quy trình `0502` là:
- Điều phối nhân viên bảo trì

Trong `Phase 1`, mục tiêu của bước này là:
- Biến `maintenance.request` đã được lập kế hoạch ở `Bước 8` thành một công việc thực thi cụ thể cho kỹ thuật viên
- Tận dụng chuẩn `industry_fsm` thay vì tự tạo một model giao việc riêng
- Tạo được liên kết rõ ràng giữa yêu cầu bảo trì và công việc thực thi ngoài hiện trường

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở mức tối thiểu của `Phase 1`, sau khi:
- request đã có `Scheduled Date`
- đã có `Responsible`
- đã được `Mark Planned`

thì hệ thống cho phép tạo một `FSM task`.

`FSM task` trong ngữ cảnh này được hiểu là:
- phiếu giao việc thực thi cho kỹ thuật viên
- nơi kỹ thuật viên theo dõi công việc cần làm
- nơi dùng các tính năng chuẩn của `industry_fsm` như:
  - assignees
  - planned date
  - trạng thái thực hiện
  - chatter
  - activity
  - timesheet

## 3. Module chuẩn được dùng

Các module chuẩn chính được dùng ở bước này:
- `maintenance`
- `project`
- `industry_fsm`

Ý nghĩa:
- `maintenance.request` tiếp tục là điểm quản lý yêu cầu
- `project.task` là nơi chứa công việc thực thi
- `industry_fsm` làm cho `project.task` hoạt động theo kiểu `Field Service Task`

## 4. Những gì đã triển khai

### 4.1. Bổ sung liên kết giữa request và FSM task

Trên `maintenance.request` đã thêm field:
- `x_psm_0502_fsm_task_id`

Trên `project.task` đã thêm field:
- `x_psm_0502_request_id`

Ý nghĩa:
- từ request có thể mở lại task thực thi
- từ task có thể biết nó được tạo ra từ request nào

### 4.2. Thêm logic tạo FSM task từ maintenance request

Đã thêm action:
- `action_psm_create_fsm_task()`

Logic hiện tại:
- chỉ tạo task khi request đã có:
  - `Scheduled Date`
  - `Responsible`
  - `Store Department`
- nếu request đã có task rồi thì không tạo trùng
- hệ thống tìm một `FSM project` có `is_fsm = True`
- sau đó tạo `project.task` trong project đó

### 4.3. Dữ liệu được đẩy từ request sang task

Khi tạo `FSM task`, hệ thống hiện đang đẩy sang:
- `name`
- `project_id`
- `partner_id`
- `user_ids`
- `planned_date_begin`
- `date_deadline`
- `description`
- `priority`
- `x_psm_0502_request_id`

## 5. Xử lý trường Customer bắt buộc của FSM

Trong quá trình test, phát hiện `industry_fsm` bắt buộc trường:
- `Customer`

Thực chất đây là field:
- `partner_id` trên `project.task`

Để không phải chọn tay mỗi lần tạo task, đã triển khai cách:
- map `Store Department -> Customer`

Cụ thể:
- trên `hr.department` thêm field:
  - `x_psm_0502_partner_id`
- field này dùng để cấu hình partner đại diện cho phòng ban/cửa hàng
- khi bấm `Create FSM Task`, hệ thống lấy:
  - `maintenance.request.x_psm_0502_department_id.x_psm_0502_partner_id`
- rồi tự gán vào:
  - `project.task.partner_id`

Nếu phòng ban chưa cấu hình partner:
- hệ thống báo lỗi rõ ràng
- không tạo task dở dang

## 6. Giao diện đã bổ sung

Trên form `maintenance.request` đã thêm:
- nút `Create FSM Task`
- nút `Open FSM Task`
- field `FSM Task`

Trên list/search view đã thêm:
- cột `FSM Task`
- filter `Has FSM Task`
- filter `No FSM Task`
- group by `FSM Task`

Trên form `hr.department` đã thêm:
- field `0502 FSM Customer`

## 7. Cách dùng trong thực tế

### Bước 1: cấu hình partner cho phòng ban

Vào:
- `Employees / Departments`

Mở đúng phòng ban đại diện cho cửa hàng và điền:
- `0502 FSM Customer`

### Bước 2: chuẩn bị request

Trên `maintenance.request`, cần có:
- `Store Department`
- `Scheduled Date`
- `Responsible`
- đã bấm `Mark Planned`

### Bước 3: tạo task

Bấm:
- `Create FSM Task`

Kết quả mong đợi:
- hệ thống tạo một `FSM task`
- tự đổ `Customer`
- tự đổ kỹ thuật viên
- tự đổ thời gian kế hoạch

### Bước 4: mở lại task

Bấm:
- `Open FSM Task`

Để mở lại công việc thực thi vừa tạo.

## 8. Điều cần test

### Case 1: tạo thành công

Điều kiện:
- phòng ban đã có `0502 FSM Customer`
- request đã planned

Kỳ vọng:
- tạo được `FSM task`
- request được liên kết với task
- task có `Customer`
- task có `Assignees`
- task có `Planned Date`

### Case 2: chưa cấu hình partner cho phòng ban

Điều kiện:
- phòng ban chưa có `0502 FSM Customer`

Kỳ vọng:
- bấm `Create FSM Task` thì hệ thống báo lỗi
- không tạo task

### Case 3: tránh tạo trùng

Điều kiện:
- request đã có `FSM task`

Kỳ vọng:
- bấm lại `Create FSM Task` không tạo mới
- hệ thống mở task hiện có

## 9. Những gì chưa làm để giữ đúng scope

Ở `Phase 1 - Bước 9`, chưa làm các phần sau:
- chưa kéo `planning` vào để phân ca chi tiết
- chưa có cơ chế điều phối nhiều kỹ thuật viên theo skill
- chưa có workflow phê duyệt giao việc
- chưa có màn hình dashboard điều phối riêng
- chưa có rule tự động đổi stage giữa request và task
- chưa xử lý sâu vật tư, timesheet, worksheet, báo cáo hiện trường

## 10. Tại sao cách làm này phù hợp với Phase 1

Cách làm hiện tại phù hợp vì:
- tận dụng chuẩn Odoo của `industry_fsm`
- không tạo object giao việc riêng
- giúp đi hết luồng từ request sang execution
- giảm custom ở giai đoạn đầu
- vẫn giữ được khả năng mở rộng về sau

## 11. Các file đã thay đổi

- `models/project_task.py`
- `models/maintenance_request.py`
- `models/hr_department.py`
- `models/__init__.py`
- `views/maintenance_request_views.xml`
- `views/hr_department_views.xml`
- `__manifest__.py`

## 12. Kết luận

`Bước 9` đã được triển khai thành công ở mức phù hợp với `Phase 1`:
- request đã lập kế hoạch có thể chuyển sang công việc thực thi
- công việc thực thi dùng chuẩn `FSM task`
- không còn phải chọn tay `Customer` nếu phòng ban đã được cấu hình đúng

Điều này giúp quy trình `0502` đi thêm một bước quan trọng:
- từ quản lý yêu cầu
- sang giao việc thực tế cho kỹ thuật viên.
