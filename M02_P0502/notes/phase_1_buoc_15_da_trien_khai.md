# Phase 1 - Bước 15 đã triển khai

## 1. Mục tiêu của bước 15

Bước 15 trong quy trình 0502 là:

- CMT thực hiện yêu cầu xuất kho vật tư
- tạo được hành động hoặc chứng từ để chuyển sang luồng kho

Trong `Phase 1`, mục tiêu của bước này là:

- từ `maintenance.request` tạo được một chứng từ kho tối thiểu
- có liên kết rõ giữa request 0502 và chứng từ kho
- có nơi để người dùng mở lại và xử lý tiếp trên `stock`

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 15 được triển khai theo hướng gọn:

- chưa tạo “phiếu yêu cầu xuất kho” riêng
- chưa làm form trung gian cho kho
- chưa tạo line vật tư chi tiết ngay tại bước này

Thay vào đó:

- tạo trực tiếp một `stock.picking` kiểu `internal`
- lưu liên kết ngược với `maintenance.request`
- để người dùng tiếp tục bổ sung nghiệp vụ kho ở các bước sau

Điều này bám đúng định hướng trong plan:

- dùng chuẩn `stock`
- có button tạo chứng từ kho
- liên kết giữa request/FSM task và stock picking

## 3. Những gì đã triển khai

### 3.1. Bổ sung dependency

Trong `__manifest__.py` đã thêm:

- `stock`

để module có thể sử dụng model và view chuẩn của kho.

### 3.2. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_stock_picking_id`

Ý nghĩa:

- lưu chứng từ kho được tạo từ request 0502 ở bước 15

### 3.3. Action nghiệp vụ

Đã bổ sung 2 action:

- `action_psm_create_stock_picking()`
- `action_psm_open_stock_picking()`

Ý nghĩa:

- `Create Stock Picking`
  - tạo mới một `stock.picking` draft kiểu `internal`
- `Open Stock Picking`
  - mở lại chứng từ kho đã tạo

### 3.4. Kế thừa `stock.picking`

Đã bổ sung model kế thừa `stock.picking` với các field:

- `x_psm_0502_request_id`
  - request 0502 nguồn
- `x_psm_0502_fsm_task_id`
  - FSM task liên kết, lấy related từ request

Mục đích:

- giúp đội kho hoặc người xử lý kho nhìn ra chứng từ này đến từ request nào
- và có liên hệ với công việc FSM nào

## 4. Logic hiện tại

Khi bấm `Create Stock Picking`, hệ thống sẽ:

1. kiểm tra request đã hoàn tất bước 14 chưa
2. kiểm tra request có `Has Material Request = True` chưa
3. kiểm tra request không đi nhánh `Need Outside Service`
4. tìm `stock.picking.type` có `code = internal`
5. tạo một `stock.picking` draft tối thiểu
6. liên kết picking đó ngược về `maintenance.request`

Thông tin chính được gán cho picking:

- `picking_type_id`
- `location_id`
- `location_dest_id`
- `scheduled_date`
- `origin`
- `partner_id` nếu có partner từ phòng ban
- `note`
- `company_id`
- `x_psm_0502_request_id`

## 5. Cập nhật giao diện

### 5.1. Trên form `maintenance.request`

Đã thêm 2 nút:

- `Create Stock Picking`
- `Open Stock Picking`

Trong tab `Material Assessment` đã thêm field:

- `Stock Picking`

### 5.2. Trên list/search view của `maintenance.request`

Đã thêm:

- cột `Stock Picking`
- filter:
  - `Has Stock Picking`
  - `No Stock Picking`
- group by:
  - `Stock Picking`

### 5.3. Trên form/list của `stock.picking`

Đã thêm hiển thị:

- `0502 Maintenance Request`
- `0502 FSM Task`

để nhìn lại nguồn phát sinh từ quy trình 0502.

## 6. Ý nghĩa của bước này trong luồng 0502

Sau bước 14:

- nếu request đã xác định có phát sinh vật tư

thì bước 15 là nơi:

- tạo ra móc nối đầu tiên sang quy trình kho
- giúp request đi tiếp sang bước 16 và các bước sau

Trong `Phase 1`, bước này mới chỉ làm:

- tạo chứng từ kho draft tối thiểu
- chưa xử lý sâu logic xuất vật tư

Tức là:

- đã có đường đi sang `stock`
- nhưng chưa hoàn thiện chi tiết kho nâng cao

## 7. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- dòng vật tư chi tiết ngay lúc tạo picking
- reservation tồn kho tại bước 15
- quy trình “phiếu yêu cầu xuất kho” riêng
- xác nhận kho nhiều cấp
- mapping kho nguồn/đích theo cửa hàng một cách nâng cao

Các phần đó phù hợp hơn với:

- `Bước 16`
- `Bước 17`
- `Bước 18`
- hoặc các phase sau nếu cần đào sâu thêm luồng kho

## 8. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã qua bước 13
- đã qua bước 14
- `Need Outside Service = False`
- `Has Material Request = True`
- `Material Checked By`: đã có
- `Material Checked At`: đã có

Ví dụ:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân chảy nước`

Sau đó bấm:

- `Create Stock Picking`

Kỳ vọng:

- hệ thống tạo 1 `stock.picking` draft
- request được gắn với `Stock Picking`
- mở picking lên thấy rõ:
  - `0502 Maintenance Request`
  - `0502 FSM Task`

## 9. Điều cần test

Checklist test tối thiểu:

- request chưa qua bước 14
  - bấm `Create Stock Picking`
  - kỳ vọng: báo lỗi validation

- request có `Has Material Request = False`
  - bấm `Create Stock Picking`
  - kỳ vọng: báo lỗi validation

- request có `Need Outside Service = True`
  - bấm `Create Stock Picking`
  - kỳ vọng: báo lỗi validation

- request hợp lệ
  - bấm `Create Stock Picking`
  - kỳ vọng: tạo được `stock.picking` draft

- request đã có picking
  - bấm `Open Stock Picking`
  - kỳ vọng: mở lại đúng chứng từ kho

- list/search view lọc được:
  - `Has Stock Picking`
  - `No Stock Picking`

## 10. File đã thay đổi

Các file đã thay đổi trong bước này:

- `__manifest__.py`
- `models/__init__.py`
- `models/maintenance_request.py`
- `models/stock_picking.py`
- `views/maintenance_request_views.xml`
- `views/stock_picking_views.xml`

## 11. Kết luận

`Phase 1 - Bước 15` đã được triển khai theo hướng:

- tận dụng chuẩn `stock`
- tạo được chứng từ kho tối thiểu
- có liên kết rõ với request 0502
- đủ để nối tiếp sang các bước kiểm tra tồn kho và xử lý kho tiếp theo

Kết quả là:

- `maintenance.request` đã có thể tạo `stock.picking`
- người dùng có thể mở lại và xử lý tiếp trên luồng kho
- hệ thống đã có đường nối thực tế giữa 0502 và `stock`
