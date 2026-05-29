# Phase 1 - Bước 20 đã triển khai

## 1. Mục tiêu của bước 20

Bước 20 trong quy trình 0502 là:

- CMT tiến hành sửa chữa máy móc
- có nơi theo dõi việc thực thi thực tế

Trong `Phase 1`, mục tiêu của bước này là:

- tận dụng `FSM task` của `industry_fsm` làm object thực thi chính
- không tạo object “lệnh sửa chữa” mới
- chỉ bổ sung lớp ghi nhận tối thiểu trên `maintenance.request`

## 2. File định hướng và file xác nhận đã dùng

Đã dùng:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

File source chính dùng để xác nhận:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `models/project_task.py`
- `odoo/addons/project/models/project_task.py`
- `odoo/addons/industry_fsm/models/project_task.py`
- `odoo/addons/industry_fsm/views/project_task_views.xml`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code là chuẩn xác nhận cuối cùng

## 3. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 20 được hiểu như sau:

- `FSM task` là nơi kỹ thuật viên thực hiện công việc sửa chữa thật
- `maintenance.request` không thay thế `FSM task`
- `maintenance.request` chỉ lưu dấu vết:
  - đã bắt đầu thi công chưa
  - đã hoàn tất thi công chưa
  - ghi chú tổng hợp việc xử lý

Điều này bám đúng plan:

- dùng `industry_fsm`
- không tạo object mới nếu `FSM task` đã đủ dùng

## 4. Những gì đã triển khai

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_fsm_stage_id`
  - related để nhìn nhanh stage hiện tại của `FSM task`
- `x_psm_0502_fsm_is_closed`
  - related để biết `FSM task` đã đóng/chưa
- `x_psm_0502_execution_started_by_id`
  - ai xác nhận đã bắt đầu thi công
- `x_psm_0502_execution_started_at`
  - thời điểm bắt đầu thi công
- `x_psm_0502_execution_completed_by_id`
  - ai xác nhận đã hoàn tất thi công
- `x_psm_0502_execution_completed_at`
  - thời điểm hoàn tất thi công
- `x_psm_0502_execution_note`
  - ghi chú tổng hợp việc sửa chữa

### 4.2. Action nghiệp vụ

Đã bổ sung:

- `action_psm_mark_execution_started()`
- `action_psm_mark_execution_completed()`

Ý nghĩa:

- `Mark Execution Started`
  - ghi nhận request đã bước vào giai đoạn thi công thực tế
- `Mark Execution Completed`
  - ghi nhận request đã hoàn tất phần thực thi sửa chữa sau khi `FSM task` đã đóng

## 5. Logic hiện tại

### 5.1. Khi bấm `Mark Execution Started`

Hệ thống sẽ:

1. kiểm tra request đã có `FSM Task`
2. kiểm tra request chưa bị đánh dấu hoàn tất execution
3. nếu chưa có `Execution Started At` thì ghi:
   - `Execution Started By`
   - `Execution Started At`

### 5.2. Khi bấm `Mark Execution Completed`

Hệ thống sẽ:

1. kiểm tra request đã có `FSM Task`
2. kiểm tra request đã được `Mark Execution Started`
3. kiểm tra `FSM task` đã ở trạng thái đóng theo logic chuẩn `project/industry_fsm`
4. ghi:
   - `Execution Completed By`
   - `Execution Completed At`

## 6. Cập nhật giao diện

### 6.1. Trên form `maintenance.request`

Đã thêm:

- nút `Mark Execution Started`
- nút `Mark Execution Completed`
- tab `Execution`

Trong tab `Execution` đã hiển thị:

- `FSM Task`
- `FSM Stage`
- `FSM Task Closed`
- `Execution Started By`
- `Execution Started At`
- `Execution Completed By`
- `Execution Completed At`
- `Execution Note`

### 6.2. Trên list view

Đã thêm các cột:

- `FSM Stage`
- `Execution Started At`
- `Execution Completed At`

### 6.3. Trên search view

Đã thêm các filter:

- `Execution Started`
- `Execution Not Started`
- `Execution Completed`
- `Execution In Progress`

Đã thêm group by:

- `FSM Stage`
- `Execution Started By`
- `Execution Completed By`

## 7. Ý nghĩa của bước này trong luồng 0502

Sau bước 19:

- request đã chốt được hướng vật tư nội bộ hoặc mua ngoài

thì bước 20 là nơi:

- kỹ thuật viên tiến hành xử lý thực tế
- `FSM task` phản ánh tiến độ thao tác thực địa
- request ghi lại dấu vết tổng hợp của giai đoạn thi công

Trong `Phase 1`, đây vẫn là lớp tích hợp nhẹ:

- tận dụng `FSM task`
- không thay thế workflow chuẩn của `industry_fsm`

## 8. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- worksheet/checklist kỹ thuật riêng cho 0502
- định mức vật tư thực tế theo từng bước sửa chữa
- biên bản thi công đặc thù
- tracking chi tiết từng thao tác kỹ thuật trên request
- rule chuyển stage tự động giữa request và task

Các phần đó phù hợp hơn với:

- `Phase 2`
- hoặc bước 21 nếu cần đào sâu phần nghiệm thu

## 9. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã có `FSM Task`
- kỹ thuật viên đã nhận và bắt đầu xử lý

Ví dụ:

- request có `FSM task` đang ở trạng thái mở

## 10. Điều cần test

Checklist test tối thiểu:

1. request có `FSM Task` thì thấy nút `Mark Execution Started`
2. bấm `Mark Execution Started` thì có:
   - `Execution Started By`
   - `Execution Started At`
3. khi `FSM task` chưa đóng thì bấm `Mark Execution Completed` phải bị chặn
4. khi `FSM task` đã đóng thì bấm `Mark Execution Completed` thành công
5. tab `Execution` hiển thị đúng:
   - `FSM Stage`
   - `FSM Task Closed`
   - dấu vết started/completed

## 11. Kiểm tra kỹ thuật đã chạy

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 12. File đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
