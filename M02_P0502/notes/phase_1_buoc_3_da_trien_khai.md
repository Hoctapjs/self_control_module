# Phase 1 - Bước 3 Đã Triển Khai

## 1. Mục tiêu của bước 3

Trong kế hoạch `Phase 1`, bước 3 là:

- CMT tiếp nhận yêu cầu bảo trì

Mục tiêu của bước này là:

- Thể hiện được rằng yêu cầu đã được tiếp nhận
- Có dấu vết người tiếp nhận và thời điểm tiếp nhận
- Chưa can thiệp sâu vào workflow chuẩn của `maintenance`
- Giữ triển khai ở mức tối thiểu để không làm nặng `Phase 1`

Kết luận triển khai ở bước này là:

- Không thay đổi state machine chuẩn của `maintenance.request`
- Không tạo workflow mới
- Chỉ bổ sung cơ chế xác nhận tiếp nhận ở mức nghiệp vụ tối thiểu

## 2. Cách hiểu nghiệp vụ ở bước 3

Bước 3 của quy trình là:

- CMT tiếp nhận yêu cầu bảo trì

Trong `Phase 1`, điều cần nhất ở bước này chưa phải là một quy trình phê duyệt hay luồng trạng thái phức tạp. Điều cần trước tiên là:

- biết yêu cầu nào đã được tiếp nhận
- biết ai đã tiếp nhận
- biết tiếp nhận lúc nào

Vì vậy, hướng triển khai được chọn là:

- thêm nút thao tác tiếp nhận trực tiếp trên `maintenance.request`
- khi bấm tiếp nhận thì lưu user và thời điểm
- chưa thay đổi stage chuẩn của Odoo ở bước này

## 3. Module chuẩn được dùng

Module chuẩn tiếp tục được tận dụng trong bước này là:

- `maintenance`
- `mail`

Phần chuẩn Odoo được dùng làm nền:

- model `maintenance.request`
- form view của `maintenance.request`
- list view của `maintenance.request`
- search view của `maintenance.request`
- chatter tracking

Nguồn xác nhận chính:

- [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)
- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

## 4. Những gì đã code

### 4.1. Bổ sung action tiếp nhận yêu cầu

Đã thêm method:

- `action_x_0502_receive_request`

File:

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)

Mục đích:

- Cho phép user bấm nút để xác nhận rằng yêu cầu đã được tiếp nhận
- Khi tiếp nhận, hệ thống tự động ghi nhận thông tin cần thiết

Logic hiện tại:

- nếu request chưa có thời điểm tiếp nhận, hệ thống sẽ:
  - lưu người tiếp nhận là user hiện tại
  - lưu thời điểm tiếp nhận là thời điểm bấm nút

### 4.2. Bổ sung field người tiếp nhận

Đã thêm field:

- `x_0502_received_by_id`

Loại dữ liệu:

- `Many2one`

Model liên kết:

- `res.users`

Mục đích:

- ghi nhận ai là người đã tiếp nhận yêu cầu
- hỗ trợ truy vết và báo cáo sau này

### 4.3. Bổ sung field thời điểm tiếp nhận

Đã thêm field:

- `x_0502_received_at`

Loại dữ liệu:

- `Datetime`

Mục đích:

- ghi nhận thời điểm tiếp nhận thực tế
- giúp phân biệt yêu cầu đã tiếp nhận và chưa tiếp nhận

### 4.4. Cập nhật form view

Đã cập nhật form view của `maintenance.request` trong file:

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

Những gì đã thêm:

- nút `Receive`
- field `Received By`
- field `Received At`

Logic hiển thị hiện tại:

- nút `Receive` chỉ hiện khi:
  - request chưa bị archive
  - request chưa có `Received At`

Ý nghĩa:

- tránh tiếp nhận lặp lại nhiều lần
- user nhìn thấy rõ yêu cầu nào chưa được tiếp nhận

### 4.5. Cập nhật list view

Đã bổ sung thêm cột:

- `Received By`
- `Received At`

Ý nghĩa:

- xem nhanh từ màn hình danh sách
- hỗ trợ lọc và theo dõi trong quá trình vận hành

### 4.6. Cập nhật search view

Đã thêm 2 filter mới:

- `Received`
- `Not Received`

Ý nghĩa:

- lọc nhanh các yêu cầu đã được tiếp nhận
- lọc nhanh các yêu cầu chưa được tiếp nhận

## 5. Những gì không làm trong bước 3

Để giữ đúng phạm vi `Phase 1 - Bước 3`, các nội dung sau chưa được triển khai:

- Chưa tạo stage riêng “Đã tiếp nhận”
- Chưa thay đổi stage chuẩn của `maintenance`
- Chưa có cơ chế phân quyền riêng cho người được phép tiếp nhận
- Chưa có logic bắt buộc chỉ CMT mới được bấm tiếp nhận
- Chưa có quy trình re-open hoặc nhận lại yêu cầu
- Chưa có SLA hoặc deadline xử lý theo thời điểm tiếp nhận

## 6. Vì sao cách làm này phù hợp với Phase 1

Hướng triển khai này phù hợp với `Phase 1` vì:

- rất nhẹ
- dễ test
- không phá flow chuẩn của Odoo
- vẫn tạo được dấu vết nghiệp vụ cần thiết

Nói ngắn gọn:

- bước 3 hiện tại đủ để biết “yêu cầu đã được CMT tiếp nhận hay chưa”
- nhưng chưa đẩy dự án vào việc phải thiết kế workflow phức tạp quá sớm

## 7. Dữ liệu mẫu nên dùng để test bước 3

Dùng lại một request đã tạo ở bước 2, ví dụ:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân không mát`
- `Store Department`: phòng ban cửa hàng Q1
- `Request Type`: `Repair`
- `Request Source`: `Store Request`

Hoặc:

- `Request`: `Bảo trì định kỳ tháng 4 - Máy lạnh quầy thu ngân CH Q1`
- `Store Department`: phòng ban cửa hàng Q1
- `Request Type`: `Maintenance`
- `Request Source`: `Preventive Schedule`

## 8. Điều cần test ở bước 3

Sau khi upgrade module, cần test các điểm sau:

- mở một request chưa tiếp nhận
- xác nhận thấy nút `Receive`
- xác nhận `Received By` và `Received At` đang trống
- bấm `Receive`
- kiểm tra:
  - `Received By` = user hiện tại
  - `Received At` = thời điểm hiện tại
- lưu và mở lại record vẫn còn dữ liệu
- nút `Receive` không còn hiện nữa
- list view hiển thị đúng 2 cột mới
- search view lọc đúng theo `Received` và `Not Received`

## 9. Tác động lên các bước sau

Sau khi hoàn thành bước 3:

- Bước 4 có thể bắt đầu từ các yêu cầu đã được tiếp nhận
- Bước 7, 8 có thể tổng hợp rõ hơn các yêu cầu đã vào hàng xử lý
- báo cáo nội bộ có thể phân biệt được yêu cầu mới tạo và yêu cầu đã được nhận xử lý

Điều này giúp `Phase 1` tiếp tục giữ đúng nguyên tắc:

- đi từ từ
- bám sát quy trình
- thêm đúng lượng logic tối thiểu

## 10. File đã thay đổi trong bước 3

- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 11. Kết luận

`Phase 1 - Bước 3` đã được triển khai theo đúng tinh thần:

- không làm workflow nặng
- không thay stage chuẩn quá sớm
- chỉ bổ sung cơ chế tiếp nhận đủ dùng

Đây là bước giúp quy trình `0502` có thêm một dấu mốc rõ ràng: từ chỗ chỉ “đã tạo yêu cầu” sang trạng thái “đã được tiếp nhận xử lý”.
