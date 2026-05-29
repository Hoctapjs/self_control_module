# Phase 1 - Bước 10 Đã Triển Khai

## 1. Mục tiêu của bước 10

`Bước 10` trong quy trình `0502` là:
- Xuất báo cáo theo dõi tình trạng

Trong `Phase 1`, mục tiêu của bước này là:
- Có một cách theo dõi tiến độ xử lý của các công việc đã được điều phối cho kỹ thuật viên
- Tận dụng chuẩn Odoo thay vì làm dashboard đặc thù quá sớm
- Cho phép lọc, nhóm và xem nhanh tình trạng các `FSM task` phát sinh từ quy trình `0502`

## 2. Cách hiểu nghiệp vụ trong Phase 1

Sau `Bước 9`, mỗi yêu cầu cần thực thi đã được chuyển thành một:
- `FSM task`

Vì vậy, ở `Bước 10`, thay vì làm một báo cáo mới hoàn toàn, `Phase 1` chọn cách:
- dùng `project.task`
- chỉ lấy các task có nguồn từ `0502`
- bổ sung action/menu/filter/group để theo dõi

Hiểu đơn giản:
- `Bước 9` tạo việc
- `Bước 10` theo dõi việc đó đang ở đâu

## 3. Module chuẩn được dùng

Các module chuẩn chính được dùng:
- `project`
- `industry_fsm`
- `maintenance`

Ý nghĩa:
- `project.task` là nơi lưu công việc thực thi
- `industry_fsm` cung cấp ngữ cảnh Field Service
- `maintenance.request` vẫn là nguồn gốc của công việc

## 4. Những gì đã triển khai

### 4.1. Bổ sung field related để báo cáo trên project.task

Đã thêm các field related trên `project.task`:
- `x_psm_0502_department_id`
- `x_psm_0502_request_type_id`
- `x_psm_0502_request_source_id`

Các field này lấy dữ liệu từ:
- `x_psm_0502_request_id`

Ý nghĩa:
- không cần nhập lại dữ liệu
- nhưng vẫn có thể lọc/nhóm trực tiếp trên task

### 4.2. Kế thừa search view của project.task

Đã thêm vào search view các field:
- `0502 Request`
- `Store Department`
- `Request Type`
- `Request Source`

Đồng thời thêm các filter:
- `0502 Execution`
- `0502 Open Execution`
- `0502 Done Execution`
- `0502 Overdue`

### 4.3. Bổ sung group by cho phần theo dõi

Đã thêm các group by:
- `Store Department`
- `Request Type`
- `Request Source`
- `0502 Request`

Mục đích:
- giúp nhìn nhanh tiến độ xử lý theo cửa hàng/phòng ban
- hỗ trợ tổng hợp các việc đang mở và đã hoàn tất

### 4.4. Kế thừa list view của project.task

Đã bổ sung các cột:
- `0502 Request`
- `Store Department`
- `Request Type`
- `Request Source`

Như vậy khi xem danh sách task, người dùng không cần mở từng record vẫn thấy được:
- task này thuộc yêu cầu nào
- phát sinh từ đâu
- thuộc cửa hàng/phòng ban nào

### 4.5. Tạo action và menu theo dõi nhanh

Đã tạo action:
- `0502 Execution Monitoring`

Đã tạo menu:
- `Maintenance > Reporting > 0502 Execution Monitoring`

Action này mặc định:
- chỉ lấy các `project.task` có `x_psm_0502_request_id`
- bật sẵn filter `0502 Open Execution`
- group mặc định theo `Store Department`

## 5. Ý nghĩa của màn hình 0502 Execution Monitoring

Màn hình này là nơi dùng để:
- xem những việc `0502` đang mở
- xem những việc đã đóng
- xem việc nào đang quá hạn
- nhóm theo phòng ban/cửa hàng
- nhóm theo request để kiểm tra một yêu cầu đã phát sinh bao nhiêu task thực thi

Nó chưa phải dashboard đẹp hay báo cáo đặc thù, nhưng đủ để:
- theo dõi tiến độ xử lý
- kiểm soát vận hành ở mức `Phase 1`

## 6. Cách dùng trong thực tế

### Bước 1: vào menu báo cáo

Vào:
- `Maintenance > Reporting > 0502 Execution Monitoring`

### Bước 2: dùng filter theo nhu cầu

Có thể chọn:
- `0502 Open Execution`
- `0502 Done Execution`
- `0502 Overdue`

### Bước 3: group theo góc nhìn nghiệp vụ

Có thể group theo:
- `Store Department`
- `Request Type`
- `Request Source`
- `0502 Request`

### Bước 4: mở task để xem chi tiết

Từ danh sách:
- mở `FSM task`
- xem trạng thái
- xem kỹ thuật viên
- xem planned date
- xem chatter và timesheet nếu có

## 7. Điều cần test

### Case 1: có task 0502 đang mở

Kỳ vọng:
- task xuất hiện trong `0502 Execution Monitoring`
- lọc `0502 Open Execution` thấy record

### Case 2: task đã hoàn tất

Kỳ vọng:
- sau khi task được đóng
- lọc `0502 Done Execution` thấy record

### Case 3: task quá hạn

Điều kiện:
- task có `date_deadline`
- chưa đóng
- ngày hạn nhỏ hơn ngày hiện tại

Kỳ vọng:
- lọc `0502 Overdue` thấy record

### Case 4: group theo Store Department

Kỳ vọng:
- task được gom đúng theo phòng ban/cửa hàng của request gốc

## 8. Những gì chưa làm để giữ đúng scope

Ở `Phase 1 - Bước 10`, chưa làm:
- dashboard đặc thù riêng cho `0502`
- KPI riêng dạng card
- biểu đồ custom phức tạp
- báo cáo in ấn riêng
- tổng hợp chéo sâu giữa request, task, vật tư, chi phí

Những phần này để dành cho:
- `Phase 2`
- hoặc khi scope báo cáo vận hành đã rõ hơn

## 9. Tại sao cách làm này phù hợp với Phase 1

Cách làm hiện tại phù hợp vì:
- tận dụng chuẩn Odoo
- không tạo model báo cáo riêng
- triển khai nhanh
- đủ để theo dõi vận hành
- vẫn mở rộng tốt về sau

## 10. Các file đã thay đổi

- `models/project_task.py`
- `views/project_task_views.xml`
- `__manifest__.py`

## 11. Kết luận

`Bước 10` đã được triển khai ở mức phù hợp với `Phase 1`:
- có nơi theo dõi tiến độ xử lý
- dùng chuẩn `project.task` và `industry_fsm`
- có filter, group và menu riêng cho ngữ cảnh `0502`

Điều này giúp quy trình `0502` không chỉ dừng ở chỗ tạo việc, mà đã có thể:
- quan sát việc đang mở
- kiểm tra việc đã xong
- phát hiện việc quá hạn
- theo dõi tình trạng xử lý theo từng cửa hàng/phòng ban.
