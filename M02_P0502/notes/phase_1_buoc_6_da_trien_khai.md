# Phase 1 - Bước 6 Đã Triển Khai

## 1. Mục tiêu của bước 6

`Bước 6` trong quy trình `0502` là:

- Hệ thống gửi lịch bảo trì cho CMT Lead

Trong `Phase 1`, mục tiêu của bước này không phải là dựng một cơ chế thông báo đặc thù, đa kênh hoặc workflow phức tạp. Mục tiêu chỉ là:

- Có cách để `CMT Lead` nhìn thấy preventive request vừa được hệ thống sinh ra
- Có dấu vết rõ ràng rằng request đó đã được đưa tới người theo dõi phù hợp
- Tận dụng tối đa chuẩn Odoo, đặc biệt là `mail.activity`

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở mức triển khai tối thiểu, câu “gửi lịch bảo trì cho CMT Lead” được hiểu là:

- Khi hệ thống sinh `maintenance.request` từ lịch bảo trì định kỳ
- Hệ thống tự tạo một `To Do activity`
- Activity này được gán cho một user đại diện cho vai trò `CMT Lead`

Điều này giúp đạt được 2 mục tiêu:

- `CMT Lead` có thể thấy việc cần xử lý trong activity
- Hệ thống có thể lọc, kiểm tra và theo dõi việc đã notify hay chưa

## 3. Module chuẩn được dùng để triển khai

Phần này được bám theo chuẩn Odoo ở các thành phần sau:

- `maintenance.request`
- `maintenance.team`
- `mail.activity.mixin`
- `mail.activity`

Nguồn source chính được dùng để xác nhận:

- [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)

Các điểm chuẩn Odoo được tận dụng:

- `maintenance.request` đã kế thừa `mail.activity.mixin`
- `maintenance.team` có `member_ids`
- có thể dùng `activity_schedule()` để tạo activity chuẩn của Odoo

## 4. Những gì đã code

### 4.1. Bổ sung logic notify CMT Lead trên maintenance request

Trong file:

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)

Đã thêm:

- method `_x_0502_get_lead_notification_user()`
- method `action_x_0502_notify_lead()`
- field `x_0502_lead_notified_user_id`
- field `x_0502_lead_notified_at`

Ý nghĩa:

- `_x_0502_get_lead_notification_user()` chọn user đại diện cho `CMT Lead`
- `action_x_0502_notify_lead()` tạo `To Do activity` và ghi lại dấu vết đã notify

### 4.2. Cách chọn user đóng vai trò CMT Lead trong Phase 1

Thứ tự ưu tiên hiện tại:

- lấy `member` đầu tiên của `maintenance_team_id`
- nếu không có thì dùng `Technician`
- nếu vẫn không có thì fallback về `user hiện tại`

Đây là cách hiểu tối thiểu cho `Phase 1`, nhằm tránh phải custom mô hình phân vai riêng quá sớm.

### 4.3. Tự động notify khi cron sinh preventive request

Trong file:

- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)

Đã bổ sung:

- sau khi cron sinh `preventive maintenance request`, hệ thống gọi `action_x_0502_notify_lead()`
- nếu đã có preventive request mở nhưng chưa có dấu vết notify, hệ thống cũng sẽ bổ sung notify

Mục tiêu là:

- request đến hạn không chỉ được tạo ra
- mà còn ngay lập tức có activity để người phụ trách nhìn thấy

### 4.4. Cập nhật giao diện maintenance request

Trong file:

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

Đã thêm:

- nút `Notify CMT Lead`
- field `Lead Notified User`
- field `Lead Notified At`
- filter `Lead Notified`
- filter `Lead Not Notified`

Ý nghĩa:

- có thể notify thủ công nếu cần
- có thể nhìn rõ request nào đã được đẩy tới người theo dõi
- có thể lọc riêng các preventive request chưa được notify

## 5. Dữ liệu mẫu nên dùng để test

### 5.1. Equipment

Ví dụ:

- `Name`: `Máy lạnh quầy thu ngân - CH Q1`
- `Store Department`: `2 Thang 9 (Da Nang)` hoặc phòng ban test của bạn
- `Maintenance Team`: `Internal Maintenance`
- `Technician`: `RST Employee`
- `Enable Preventive Schedule`: bật
- `Preventive Interval Days`: `30`
- `Next Preventive Date`: hôm nay

### 5.2. Maintenance Team

Điều quan trọng:

- team nên có ít nhất `1 member`

Ví dụ:

- `Maintenance Team`: `Internal Maintenance`
- `Members`: `Administrator`

Như vậy khi cron chạy, hệ thống sẽ ưu tiên notify cho `Administrator` với vai trò `CMT Lead` trong `Phase 1`.

## 6. Điều cần test

### Test case 1 - Cron sinh request và tự notify

Thao tác:

- cấu hình equipment đến hạn preventive
- chạy cron `0502 Generate Preventive Maintenance Requests`

Kết quả mong đợi:

- có preventive request mới được sinh
- request có `Lead Notified User`
- request có `Lead Notified At`
- activity loại `To Do` được tạo trên request

### Test case 2 - Bấm nút Notify CMT Lead thủ công

Thao tác:

- mở một preventive request
- bấm nút `Notify CMT Lead`

Kết quả mong đợi:

- hệ thống tạo activity nếu chưa có
- ghi nhận `Lead Notified User`
- ghi nhận `Lead Notified At`

### Test case 3 - Lọc theo trạng thái notify

Thao tác:

- vào danh sách `Maintenance Requests`
- dùng filter `Lead Notified`
- dùng filter `Lead Not Notified`

Kết quả mong đợi:

- các request được phân loại đúng theo tình trạng notify

### Test case 4 - Không tạo activity trùng

Thao tác:

- bấm `Notify CMT Lead` thêm lần nữa trên cùng request
- hoặc chạy lại cron khi request preventive mở vẫn còn

Kết quả mong đợi:

- không tạo activity trùng với cùng `summary`, cùng `user`
- chỉ cập nhật dấu vết notify nếu cần

## 7. Những gì chưa làm trong bước 6

Để giữ đúng scope `Phase 1`, hiện tại chưa làm:

- mô hình `CMT Lead` riêng bằng role/business object riêng
- rule chọn lead phức tạp theo cửa hàng, vùng hoặc loại thiết bị
- gửi email riêng, SMS riêng hoặc thông báo ngoài hệ thống
- dashboard riêng cho `CMT Lead`
- cơ chế escalation nếu activity quá hạn

Các phần đó có thể để lại cho `Phase 2` hoặc `Phase 3`.

## 8. Kết luận của bước 6

`Bước 6` đã được triển khai theo hướng:

- đúng tinh thần chuẩn Odoo
- đủ nhẹ để giữ scope `Phase 1`
- đủ rõ để CMT Lead có thể nhìn thấy preventive request đến hạn

Giá trị đạt được ở bước này là:

- preventive request không chỉ được sinh ra
- mà còn được “đưa tới người theo dõi” bằng `mail.activity`
- có thể lọc, kiểm tra và test được trên giao diện

## 9. Các file đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
