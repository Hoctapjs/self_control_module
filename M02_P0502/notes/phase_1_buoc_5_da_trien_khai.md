# Phase 1 - Bước 5 Đã Triển Khai

## 1. Mục tiêu của bước 5

Trong kế hoạch `Phase 1`, bước 5 là:

- Hệ thống tự động kiểm tra lịch bảo trì máy móc

Mục tiêu của bước này là:

- Có nhánh bảo trì định kỳ chạy được ở mức cơ bản
- Cho phép cấu hình lịch bảo trì định kỳ ngay trên thiết bị
- Hệ thống tự động sinh `maintenance.request` khi đến hạn
- Chưa triển khai scheduler phức tạp theo rule đặc thù doanh nghiệp

Kết luận triển khai ở bước này là:

- Tận dụng `maintenance.equipment` làm nơi cấu hình lịch định kỳ
- Dùng cron nhẹ để quét thiết bị đến hạn
- Khi đến hạn thì sinh `maintenance.request` loại `preventive`

## 2. Cách hiểu nghiệp vụ ở bước 5

Bước 5 của quy trình là:

- Hệ thống tự động kiểm tra lịch bảo trì máy móc định kỳ

Trong `Phase 1`, điều cần trước tiên không phải là một máy lập lịch phức tạp theo nhiều rule. Điều cần nhất là:

- có thể bật hoặc tắt chế độ định kỳ cho từng thiết bị
- có ngày đến hạn tiếp theo
- có chu kỳ lặp lại
- hệ thống tự động tạo yêu cầu định kỳ khi đến hạn

Vì vậy, hướng triển khai được chọn là:

- thêm field cấu hình định kỳ trên `maintenance.equipment`
- thêm cron chạy hằng ngày
- sinh request preventive tối thiểu khi điều kiện đến hạn được thỏa

## 3. Module chuẩn được dùng

Module chuẩn được tận dụng trong bước này là:

- `maintenance`
- `mail`

Phần chuẩn Odoo được dùng làm nền:

- model `maintenance.equipment`
- model `maintenance.request`
- scheduled action `ir.cron`
- form, list, search view của `maintenance.equipment`

Nguồn xác nhận chính:

- [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)
- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)
- [maintenance_data.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/data/maintenance_data.xml)

## 4. Những gì đã code

### 4.1. Bổ sung cấu hình định kỳ trên `maintenance.equipment`

Đã thêm các field:

- `x_0502_department_id`
- `x_0502_enable_preventive_schedule`
- `x_0502_preventive_interval_days`
- `x_0502_next_preventive_date`
- `x_0502_last_preventive_request_id`

File:

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)

Ý nghĩa:

- `x_0502_department_id` xác định thiết bị thuộc phòng ban cửa hàng nào
- `x_0502_enable_preventive_schedule` bật hoặc tắt cơ chế sinh request định kỳ
- `x_0502_preventive_interval_days` xác định số ngày lặp lại
- `x_0502_next_preventive_date` xác định ngày đến hạn tiếp theo
- `x_0502_last_preventive_request_id` lưu vết request định kỳ gần nhất đã sinh

### 4.2. Bổ sung validate cho chu kỳ định kỳ

Đã thêm constraint:

- chu kỳ định kỳ phải lớn hơn hoặc bằng `1` ngày nếu bật chế độ định kỳ

Ý nghĩa:

- tránh cấu hình dữ liệu vô nghĩa
- giảm rủi ro cron sinh request sai hoặc lặp không kiểm soát

### 4.3. Bổ sung logic chuẩn bị dữ liệu request preventive

Đã thêm method:

- `_x_0502_prepare_preventive_request_vals`

Mục đích:

- chuẩn hóa bộ dữ liệu khi sinh `maintenance.request` định kỳ

Hiện tại, request được sinh với các thông tin chính:

- `Maintenance Type = preventive`
- `Request Source = Preventive Schedule`
- `Request Type = Maintenance`
- `Store Department` lấy từ thiết bị
- `Equipment` lấy từ thiết bị
- `Technician` lấy từ `technician_user_id` của thiết bị nếu có

### 4.4. Bổ sung logic tính ngày đến hạn tiếp theo

Đã thêm method:

- `_x_0502_compute_next_preventive_date`

Mục đích:

- sau khi sinh request, hệ thống tự đẩy `Next Preventive Date` sang kỳ tiếp theo

Ý nghĩa:

- tránh lặp sinh cùng một request cho cùng một kỳ
- giữ cho chu kỳ định kỳ tiếp tục chạy

### 4.5. Bổ sung cron tự động sinh preventive request

Đã thêm method:

- `cron_x_0502_generate_preventive_requests`

File:

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)

Logic hiện tại:

- cron tìm các thiết bị có:
  - bật định kỳ
  - có `Next Preventive Date`
  - `Next Preventive Date` nhỏ hơn hoặc bằng ngày hiện tại
- nếu chưa có preventive request đang mở tương ứng thì tạo mới
- sau đó cập nhật `Last Preventive Request` và `Next Preventive Date`

### 4.6. Tạo scheduled action

Đã thêm file:

- [ir_cron_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/ir_cron_data.xml)

Scheduled action đã tạo:

- `0502 Generate Preventive Maintenance Requests`

Ý nghĩa:

- hệ thống đã có tác vụ nền để chạy kiểm tra lịch định kỳ hằng ngày

### 4.7. Cập nhật giao diện `maintenance.equipment`

Đã tạo file:

- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)

Những gì đã thêm trên form equipment:

- `Store Department`
- `Enable Preventive Schedule`
- `Preventive Interval Days`
- `Next Preventive Date`
- `Last Preventive Request`

Những gì đã thêm trên list/search:

- cột theo dõi ngày đến hạn định kỳ
- filter:
  - `Preventive Enabled`
  - `Preventive Due`

Ý nghĩa:

- có thể cấu hình và theo dõi lịch định kỳ ngay trên thiết bị
- không cần tạo object cấu hình riêng ở giai đoạn này

### 4.8. Cập nhật manifest

Đã cập nhật:

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)

Nội dung chính:

- load thêm `data/ir_cron_data.xml`
- load thêm `views/maintenance_equipment_views.xml`

## 5. Những gì không làm trong bước 5

Để giữ đúng phạm vi `Phase 1 - Bước 5`, các nội dung sau chưa được triển khai:

- Chưa có rule lịch định kỳ theo loại thiết bị
- Chưa có nhiều loại chu kỳ phức tạp như tuần, tháng, quý
- Chưa có giao diện lập lịch tập trung riêng
- Chưa có dashboard theo dõi thiết bị sắp đến hạn
- Chưa có logic escalation khi cron fail hoặc không sinh request
- Chưa làm notification tự động cho CMT Lead ở bước này

## 6. Vì sao cách làm này phù hợp với Phase 1

Hướng triển khai này phù hợp với `Phase 1` vì:

- tận dụng được model chuẩn `maintenance.equipment`
- không cần tạo scheduler riêng phức tạp
- có thể test được ngay
- đủ để mở nhánh bảo trì định kỳ trong quy trình

Nói ngắn gọn:

- bước 5 hiện tại làm được điều quan trọng nhất là “đến hạn thì sinh request”
- nhưng chưa kéo dự án vào bài toán lập lịch nâng cao quá sớm

## 7. Dữ liệu mẫu nên dùng để test bước 5

Trên một thiết bị, ví dụ:

- `Equipment`: `Máy lạnh quầy thu ngân - CH Q1`
- `Store Department`: phòng ban cửa hàng Q1
- `Enable Preventive Schedule`: bật
- `Preventive Interval Days`: `30`
- `Next Preventive Date`: đặt là ngày hôm nay
- `Technician`: chọn kỹ thuật viên phụ trách nếu có

## 8. Điều cần test ở bước 5

Sau khi upgrade module, cần test các điểm sau:

- mở một equipment và nhập cấu hình định kỳ
- lưu thành công
- vào danh sách equipment thấy được `Next Preventive Date`
- filter `Preventive Enabled` hoạt động đúng
- filter `Preventive Due` hoạt động đúng
- chạy scheduled action hoặc chờ cron
- kiểm tra có sinh `maintenance.request` mới hay không
- request mới phải có:
  - `Maintenance Type = Preventive`
  - `Request Source = Preventive Schedule`
  - `Request Type = Maintenance`
  - `Store Department` lấy đúng từ thiết bị
- sau khi sinh request, `Next Preventive Date` phải được đẩy sang kỳ tiếp theo

## 9. Tác động lên các bước sau

Sau khi hoàn thành bước 5:

- Bước 6 có nền dữ liệu để nhìn thấy lịch bảo trì đến hạn
- Bước 7 có thể tổng hợp các preventive request đã sinh
- quy trình `0502` bắt đầu có đủ hai nhánh:
  - phát sinh không định kỳ
  - phát sinh từ lịch định kỳ

Điều này giúp `Phase 1` tiếp tục giữ đúng nguyên tắc:

- đi từ từ
- bám sát quy trình
- mở rộng từ chuẩn Odoo trước

## 10. File đã thay đổi trong bước 5

- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [data/ir_cron_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/ir_cron_data.xml)
- [views/maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)

## 11. Kết luận

`Phase 1 - Bước 5` đã được triển khai theo đúng tinh thần:

- tận dụng `maintenance.equipment`
- thêm cấu hình định kỳ mức tối thiểu
- dùng cron nhẹ để tự động sinh preventive request
- chưa đi vào scheduler đặc thù phức tạp

Đây là bước giúp quy trình `0502` có được nhánh định kỳ chạy thật trong hệ thống, thay vì chỉ dừng ở mức khai báo thủ công.
