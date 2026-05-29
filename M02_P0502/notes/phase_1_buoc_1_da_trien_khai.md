# Phase 1 - Bước 1 Đã Triển Khai

## 1. Mục tiêu của bước 1

Trong `Phase 1`, bước 1 được triển khai theo đúng định hướng đã chốt trong plan:

- Chọn một điểm bắt đầu nghiệp vụ rõ ràng cho quy trình `0502`
- Ưu tiên tận dụng chuẩn Odoo
- Không tạo object mới nếu chuẩn Odoo đã có thể đáp ứng
- Chỉ custom ở mức tối thiểu để làm nền cho các bước tiếp theo

Kết luận triển khai ở bước này là:

- Chốt `maintenance.request` làm điểm nhận nhu cầu chính trong `Phase 1`
- Chưa đưa `helpdesk` vào làm entry point ở giai đoạn này
- Chưa tạo model riêng cho “phiếu yêu cầu bảo trì”

## 2. Cách hiểu nghiệp vụ ở bước 1

Bước 1 của quy trình là:

- Cửa hàng phát sinh nhu cầu bảo trì hoặc sửa chữa

Ở `Phase 1`, bước này chưa cần workflow phức tạp. Điều quan trọng nhất là hệ thống phải có:

- một object chuẩn để ghi nhận nhu cầu phát sinh
- một cách phân biệt nguồn phát sinh của yêu cầu

Từ đó, hướng triển khai được chọn là:

- dùng `maintenance.request` làm object khởi đầu
- bổ sung field để đánh dấu nguồn phát sinh của yêu cầu

## 3. Module chuẩn được dùng

Module chuẩn được tận dụng trong bước này là:

- `maintenance`

Phần chuẩn Odoo được dùng để xác nhận hướng triển khai:

- model `maintenance.request`
- form view của `maintenance.request`
- list view của `maintenance.request`
- search view của `maintenance.request`

Nguồn xác nhận chính:

- [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)
- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

## 4. Những gì đã code

### 4.1. Tạo xương sống module `M02_P0502`

Đã tạo các file nền cho module:

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__init__.py)
- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)

Ý nghĩa:

- Module `M02_P0502` đã có thể bắt đầu chứa custom code thật
- Dependency hiện tại được giữ tối thiểu, chỉ phụ thuộc `maintenance`

### 4.2. Kế thừa model `maintenance.request`

Đã tạo file:

- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)

Field đã bổ sung:

- `x_0502_request_source`

Kiểu dữ liệu:

- `Selection`

Các giá trị hiện tại:

- `store_request`: nhu cầu phát sinh từ cửa hàng
- `preventive_schedule`: nhu cầu đến từ lịch bảo trì định kỳ

Mục đích của field này:

- Ghi nhận điểm bắt đầu của yêu cầu trong flow `0502`
- Làm nền cho việc tách nhánh `phát sinh không theo định kỳ` và `bảo trì định kỳ`
- Giúp các bước sau có thể lọc và xử lý theo nguồn phát sinh

### 4.3. Kế thừa view của `maintenance.request`

Đã tạo file:

- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

Các thay đổi đã thực hiện:

- Thêm field `x_0502_request_source` vào form view
- Thêm field `x_0502_request_source` vào list view
- Thêm field `x_0502_request_source` vào search view
- Thêm 2 filter nhanh trong search view:
  - `Store Request`
  - `Preventive Schedule`

Ý nghĩa:

- Người dùng đã có thể nhìn thấy nguồn phát sinh ngay trên yêu cầu bảo trì
- Có thể lọc dữ liệu theo nguồn phát sinh từ rất sớm
- Đây là nền tốt để sang các bước tiếp theo như tổng hợp, lập kế hoạch, theo dõi

## 5. Những gì chưa làm ở bước 1

Để giữ đúng phạm vi của `Phase 1 - Bước 1`, các nội dung sau chưa được triển khai:

- Chưa tạo model riêng cho phiếu yêu cầu bảo trì
- Chưa đưa `helpdesk.ticket` vào làm điểm nhận yêu cầu
- Chưa có workflow phê duyệt
- Chưa có liên kết sang `industry_fsm`
- Chưa có liên kết sang `stock` hoặc `purchase`
- Chưa có menu hoặc action riêng cho quy trình `0502`
- Chưa có field nâng cao như mã cửa hàng, loại yêu cầu, timeline, cost

## 6. Vì sao cách làm này phù hợp với Phase 1

Hướng triển khai này phù hợp với `Phase 1` vì:

- Bám chuẩn Odoo
- Không tạo object thừa
- Giữ module custom ở mức gọn
- Có giá trị thật cho bước tiếp theo
- Không đẩy dự án vào custom nặng quá sớm

Nói ngắn gọn:

- Đây là một custom nhỏ nhưng đúng chỗ
- Nó giúp “đặt chân” quy trình `0502` vào Odoo chuẩn mà chưa phá vỡ cấu trúc chuẩn của `maintenance`

## 7. Tác động lên kế hoạch các bước sau

Sau khi hoàn thành bước 1, các bước tiếp theo có thể bám vào nền này:

- Bước 2: dùng tiếp `maintenance.request` làm phiếu yêu cầu bảo trì
- Bước 5: dùng giá trị `preventive_schedule` cho nhánh bảo trì định kỳ
- Bước 7, 8, 10: dùng filter theo nguồn phát sinh để tổng hợp và theo dõi

Điều này giúp toàn bộ `Phase 1` giữ được nguyên tắc:

- không tạo mới khi chưa cần
- phát triển từ từ
- kiểm soát được mã nguồn custom trong `M02_P0502`

## 8. File đã thay đổi trong bước 1

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__init__.py)
- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 9. Kết luận

`Phase 1 - Bước 1` đã được triển khai theo đúng tinh thần:

- lấy `maintenance.request` làm điểm bắt đầu
- chỉ custom tối thiểu
- chưa mở rộng scope quá sớm

Đây là một bước nền quan trọng để sang `Bước 2`, nơi mình sẽ tiếp tục dùng `maintenance.request` làm chứng từ đầu vào chính và chỉ bổ sung các field nghiệp vụ thật sự cần thiết.
