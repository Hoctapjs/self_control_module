# Phase 1 - Bước 16 đã triển khai

## 1. Mục tiêu của bước 16

Bước 16 trong quy trình 0502 là:

- kiểm tra xem kho có đủ vật tư để xử lý hay không
- xác định request sẽ đi tiếp sang nhánh xuất kho hay phải chuyển sang nhánh mua ngoài

Trong `Phase 1`, mục tiêu của bước này là:

- tận dụng ngay logic kiểm tồn chuẩn của `stock`
- không tự xây engine tồn kho riêng
- lưu lại kết quả kiểm tra tồn kho ngay trên `maintenance.request`

## 2. File định hướng và file xác nhận đã dùng

Đã dùng:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

File source chính dùng để xác nhận:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `odoo/addons/stock/models/stock_picking.py`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code là chuẩn xác nhận cuối cùng

## 3. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 16 được triển khai theo hướng gọn:

- không tạo wizard kiểm tồn riêng
- không tự tính tồn khả dụng bằng custom code
- không thay đổi logic reservation chuẩn của Odoo

Thay vào đó:

- dùng chính `stock.picking` đã tạo ở bước 15
- nếu picking còn `Draft` thì chuyển sang flow kho chuẩn trước
- gọi logic chuẩn `Check Availability`
- đọc lại trạng thái availability của picking
- ghi kết quả `đủ tồn` hay `không đủ tồn` lên request 0502

## 4. Những gì đã triển khai

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_stock_picking_state`
  - related tới trạng thái hiện tại của `stock.picking`
- `x_psm_0502_stock_availability`
  - related tới thông điệp availability do Odoo chuẩn tính toán
- `x_psm_0502_stock_availability_state`
  - related tới trạng thái kỹ thuật availability của picking
- `x_psm_0502_stock_check_result`
  - kết quả kiểm tồn ở mức nghiệp vụ:
    - `Stock Available`
    - `Stock Not Available`
- `x_psm_0502_stock_checked_by_id`
  - user đã kiểm tồn
- `x_psm_0502_stock_checked_at`
  - thời điểm đã kiểm tồn

### 4.2. Action nghiệp vụ

Đã bổ sung action:

- `action_psm_check_stock_availability()`

Ý nghĩa:

- kiểm tra request đã có `Stock Picking` chưa
- kiểm tra request có thực sự cần vật tư hay không
- kiểm tra picking có ít nhất một dòng vật tư với `Demand > 0` chưa
- nếu picking còn `Draft` thì chuyển sang `confirmed`
- gọi logic chuẩn `action_assign()` của `stock.picking`
- ghi kết quả availability về lại `maintenance.request`

## 5. Logic hiện tại

Khi bấm `Check Stock Availability`, hệ thống sẽ:

1. kiểm tra request đã có `Stock Picking`
2. kiểm tra request đang có `Has Material Request = True`
3. kiểm tra picking có ít nhất một dòng sản phẩm với số lượng yêu cầu
4. nếu picking còn ở `Draft` thì gọi `action_confirm()`
5. gọi `action_assign()` để reserve tồn theo chuẩn Odoo
6. đọc lại:
   - `state` của picking
   - `products_availability`
   - `products_availability_state`
7. ghi kết quả lên request:
   - `Stock Available`
   - hoặc `Stock Not Available`
8. lưu lại:
   - `Stock Checked By`
   - `Stock Checked At`

## 6. Cập nhật sau khi test thực tế

Sau khi test thực tế, đã có 2 điều chỉnh quan trọng:

### 6.1. Siết lại cách kết luận `Stock Check Result`

Ban đầu, code từng cho rằng:

- nếu `picking.state == "assigned"` thì có thể coi là `Stock Available`

Sau khi đối chiếu với compute chuẩn của `stock.picking`, logic này đã được sửa.

Hiện tại:

- `x_psm_0502_stock_check_result` chỉ bám theo `products_availability_state` của `stock.picking`
- nếu `products_availability_state = available` thì mới kết luận `Stock Available`
- các trường hợp còn lại sẽ ghi `Stock Not Available`

Điều chỉnh này giúp:

- `Stock Check Result` đồng bộ với compute chuẩn của `stock`
- tránh tình huống request nói `Stock Available` nhưng picking chuẩn của Odoo lại báo `Not Available`

### 6.2. Tinh chỉnh UX trên form request

Sau khi test tiếp tới bước 18, đã thấy một điểm dễ gây hiểu nhầm:

- khi `Stock Picking` đã `Done`, hai field:
  - `Stock Availability`
  - `Stock Availability State`
  sẽ bị Odoo chuẩn tính về rỗng

Điều này là đúng theo `stock`, nhưng nếu vẫn hiển thị trên request thì user sẽ thấy khó hiểu.

Vì vậy đã chỉnh view như sau:

- ẩn `Stock Availability` khi `Stock Picking State = done`
- ẩn `Stock Availability State` khi `Stock Picking State = done`
- ẩn nút `Check Stock Availability` khi:
  - picking đã `done`
  - hoặc picking đã `cancel`

## 7. Cập nhật giao diện

### 7.1. Trên form `maintenance.request`

Đã thêm nút:

- `Check Stock Availability`

Trong tab `Material Assessment` đã hiển thị thêm:

- `Stock Picking State`
- `Stock Check Result`
- `Stock Checked By`
- `Stock Checked At`
- `Stock Availability`
- `Stock Availability State`

Lưu ý sau tinh chỉnh UX:

- `Stock Availability`
- `Stock Availability State`

sẽ chỉ còn hiển thị khi picking chưa `done`

### 7.2. Trên list view

Đã thêm các cột:

- `Stock Check Result`
- `Stock Checked By`
- `Stock Checked At`

### 7.3. Trên search view

Đã thêm các filter:

- `Stock Available`
- `Stock Not Available`
- `Stock Checked`
- `Stock Not Checked`

Đã thêm group by:

- `Stock Check Result`
- `Stock Checked By`

## 8. Ý nghĩa của bước này trong luồng 0502

Sau bước 15:

- request đã có một `stock.picking`

thì bước 16 là nơi xác định:

- kho có đủ vật tư để đi tiếp sang bước 17 và 18
- hay không đủ tồn và sẽ phải rẽ sang bước 19

Trong `Phase 1`, quyết định này mới chỉ ở mức:

- đọc availability chuẩn của Odoo
- lưu kết quả tối thiểu trên request

chứ chưa xây full decision engine cho kho.

## 9. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- wizard riêng để kiểm tồn
- logic tự đề xuất sản phẩm thay thế
- kiểm tồn theo nhiều kho/cửa hàng phức tạp
- rule ưu tiên cấp phát
- engine forecast riêng
- chuyển nhánh tự động sang mua ngoài

Các phần đó phù hợp hơn với:

- `Bước 17`
- `Bước 18`
- `Bước 19`
- hoặc các phase sau nếu cần đào sâu luồng kho

## 10. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã qua bước 14
- `Has Material Request = True`
- đã tạo `Stock Picking`
- trong picking đã có ít nhất một dòng vật tư

Ví dụ:

- `Request`: `Cửa hàng Q1 - Máy in hóa đơn mờ chữ`

Trên picking:

- thêm một sản phẩm vật tư
- nhập `Demand`

Sau đó quay lại request và bấm:

- `Check Stock Availability`

## 11. Điều cần test

Checklist test tối thiểu:

- request chưa có `Stock Picking`
  - bấm `Check Stock Availability`
  - kỳ vọng: báo lỗi validation

- request có `Has Material Request = False`
  - bấm `Check Stock Availability`
  - kỳ vọng: báo lỗi validation

- picking chưa có dòng vật tư nào
  - bấm `Check Stock Availability`
  - kỳ vọng: báo lỗi yêu cầu thêm ít nhất một dòng sản phẩm

- request hợp lệ, picking có dòng vật tư, kho đủ tồn
  - bấm `Check Stock Availability`
  - kỳ vọng:
    - `Stock Check Result = Stock Available`
    - có `Stock Checked By`
    - có `Stock Checked At`

- request hợp lệ, picking có dòng vật tư, kho không đủ tồn
  - bấm `Check Stock Availability`
  - kỳ vọng:
    - `Stock Check Result = Stock Not Available`
    - có `Stock Checked By`
    - có `Stock Checked At`

- sau khi `Stock Picking` đã `Done`
  - kỳ vọng:
    - nút `Check Stock Availability` không còn hiển thị
    - `Stock Availability` và `Stock Availability State` không còn hiện để tránh gây nhiễu

## 12. Các file đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 13. Kết luận

Bước 16 hiện tại đã đạt mục tiêu của `Phase 1`:

- tận dụng được availability chuẩn của `stock`
- ghi lại được kết quả kiểm tồn trên `maintenance.request`
- đã siết logic kết luận cho đồng bộ với compute chuẩn của Odoo
- đã tinh chỉnh form để hiển thị gọn và ít gây hiểu nhầm hơn sau khi picking `Done`

