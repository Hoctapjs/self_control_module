# Phase 1 - Bước 7 Đã Triển Khai

## 1. Mục tiêu của bước 7

`Bước 7` trong quy trình `0502` là:

- CMT Lead tiếp nhận lịch và tổng hợp yêu cầu bảo trì

Trong `Phase 1`, mục tiêu của bước này là:

- Có một nơi để `CMT Lead` nhìn thấy các yêu cầu cần gom lại để xử lý
- Có thể lọc, nhóm và theo dõi bằng công cụ chuẩn của Odoo
- Không cần dựng dashboard riêng hoặc object tổng hợp riêng quá sớm

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở mức triển khai tối thiểu, `Bước 7` không được hiểu là tạo một “phiếu tổng hợp” riêng. Thay vào đó:

- dùng chính `maintenance.request`
- tạo một `queue` tổng hợp bằng action + filter + group by
- để `CMT Lead` có thể mở vào và nhìn ngay danh sách yêu cầu cần lập kế hoạch

Queue này hiện gom 2 nhóm yêu cầu:

- preventive request đã được notify cho `CMT Lead`
- yêu cầu phát sinh từ cửa hàng đã được kiểm tra và có kết luận `Action Needed`

## 3. Module chuẩn được dùng để triển khai

Phần này bám trên chuẩn Odoo của:

- `maintenance.request`
- search view của `maintenance.request`
- `ir.actions.act_window`
- `menuitem`

Nguồn source chính được dùng để xác nhận:

- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

Các phần chuẩn được tận dụng:

- search view của `maintenance.request`
- action chuẩn của `maintenance.request`
- menu chuẩn dưới app `Maintenance`

## 4. Những gì đã code

Phần triển khai của `Bước 7` hiện nằm trong:

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

### 4.1. Bổ sung filter tổng hợp

Đã thêm các filter:

- `Requests To Plan`
- `Store Action Needed`
- `Preventive Queue`

Ý nghĩa:

- `Requests To Plan`: filter tổng hợp chính cho `Bước 7`
- `Store Action Needed`: tập trung vào nhánh phát sinh từ cửa hàng đã xác định cần xử lý
- `Preventive Queue`: tập trung vào nhánh preventive đã được notify cho `CMT Lead`

### 4.2. Bổ sung group by phục vụ tổng hợp

Đã thêm các group by:

- `Store Department`
- `Equipment`
- `Team`
- `Request Type`
- `Request Source`
- `Lead Notified User`

Ý nghĩa:

- `CMT Lead` có thể gom yêu cầu theo đúng góc nhìn nghiệp vụ
- chưa cần viết dashboard hoặc báo cáo riêng

### 4.3. Tạo action riêng cho bước 7

Đã thêm action:

- `0502 Requests To Plan`

Action này:

- mở model `maintenance.request`
- dùng search view đã được kế thừa trong `M02_P0502`
- tự áp filter mặc định `Requests To Plan`
- tự group mặc định theo `Store Department`

### 4.4. Tạo menu nhanh cho CMT Lead

Đã thêm menu:

- `0502 Requests To Plan`

Vị trí:

- dưới menu `Maintenance > Maintenance`

Ý nghĩa:

- user không cần tự nhớ filter mỗi lần
- có thể vào thẳng danh sách tổng hợp cần lập kế hoạch

## 5. Logic của queue tổng hợp

Hiện tại, queue `Requests To Plan` lấy các request thỏa một trong hai nhánh:

### Nhánh 1 - Preventive

- `maintenance_type = preventive`
- `request_source = preventive_schedule`
- đã có `Lead Notified At`
- chưa archive
- chưa done

### Nhánh 2 - Store Request cần xử lý

- `request_source = store_request`
- `Initial Inspection Result = Action Needed`
- chưa archive
- chưa done

Như vậy, ở `Bước 7`, `CMT Lead` có thể tổng hợp chung cả:

- việc bảo trì định kỳ đến hạn
- việc phát sinh thực tế đã kiểm tra và cần xử lý tiếp

## 6. Dữ liệu mẫu nên dùng để test

Nên có ít nhất 2 loại request:

### 6.1. Preventive request

Ví dụ:

- `Maintenance Type`: `Preventive`
- `Request Source`: `Preventive Schedule`
- `Lead Notified At`: có giá trị
- `Stage`: chưa done

### 6.2. Store request cần xử lý

Ví dụ:

- `Maintenance Type`: `Corrective`
- `Request Source`: `Store Request`
- `Initial Inspection Result`: `Action Needed`
- `Stage`: chưa done

## 7. Điều cần test

### Test case 1 - Menu tổng hợp mở đúng action

Thao tác:

- vào `Maintenance > Maintenance > 0502 Requests To Plan`

Kết quả mong đợi:

- action mở ra danh sách `maintenance.request`
- filter `Requests To Plan` được áp mặc định
- danh sách đang group mặc định theo `Store Department`

### Test case 2 - Preventive request xuất hiện đúng trong queue

Thao tác:

- dùng một preventive request đã được notify cho lead

Kết quả mong đợi:

- request xuất hiện trong `Requests To Plan`
- request cũng xuất hiện trong `Preventive Queue`

### Test case 3 - Store request cần xử lý xuất hiện đúng trong queue

Thao tác:

- dùng một store request có `Initial Inspection Result = Action Needed`

Kết quả mong đợi:

- request xuất hiện trong `Requests To Plan`
- request cũng xuất hiện trong `Store Action Needed`

### Test case 4 - Group by hoạt động đúng

Thao tác:

- group theo `Store Department`
- group theo `Equipment`
- group theo `Request Type`

Kết quả mong đợi:

- các request được gom đúng nhóm
- CMT Lead có thể đọc danh sách ở mức tổng hợp

### Test case 5 - Request không liên quan không vào queue

Thao tác:

- kiểm tra một request có `No Action Needed`
- hoặc request đã done
- hoặc request đã archive

Kết quả mong đợi:

- request đó không xuất hiện trong `Requests To Plan`

## 8. Những gì chưa làm trong bước 7

Để giữ đúng scope `Phase 1`, hiện tại chưa làm:

- dashboard riêng cho CMT Lead
- object “bản tổng hợp yêu cầu” riêng
- wizard tổng hợp hoặc chốt batch
- cơ chế đánh dấu “đã tổng hợp”
- màn hình thống kê đặc thù theo khu vực, chi nhánh, loại máy

Những phần đó có thể để cho `Phase 2`.

## 9. Kết luận của bước 7

`Bước 7` đã được triển khai theo hướng:

- tận dụng chuẩn Odoo
- không tạo thêm model mới
- đủ để CMT Lead có một queue tổng hợp rõ ràng cho Phase 1

Giá trị đạt được:

- preventive request và store request cần xử lý đã có thể được gom chung
- có thể lọc và group lại theo góc nhìn nghiệp vụ
- chưa cần dựng dashboard riêng mà vẫn vận hành được

## 10. Các file đã thay đổi

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
