# Phase 1 - Bước 19 đã triển khai

## 1. Mục tiêu của bước 19

Bước 19 trong quy trình 0502 là:

- nếu tồn kho vật tư không đủ đáp ứng
- tiến hành chuyển sang nhánh mua ngoài

Trong `Phase 1`, mục tiêu của bước này là:

- tận dụng `purchase` và `purchase_stock` chuẩn của Odoo
- chưa xây requisition phức tạp
- chỉ cần tạo hoặc mở RFQ/PO từ `maintenance.request`

## 2. File định hướng và file xác nhận đã dùng

Đã dùng:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

File source chính dùng để xác nhận:

- `models/maintenance_request.py`
- `models/purchase_order.py`
- `views/maintenance_request_views.xml`
- `views/purchase_order_views.xml`
- `odoo/addons/purchase/models/purchase_order.py`
- `odoo/addons/purchase/views/purchase_views.xml`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code là chuẩn xác nhận cuối cùng

## 3. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 19 được triển khai theo hướng nhẹ:

- không tạo quy trình requisition riêng
- không dựng bảng báo giá nhiều nhà cung cấp
- không custom sâu vào nghiệp vụ mua

Thay vào đó:

- nếu request đã đi tới nhánh `Stock Not Available`
- hệ thống cho phép mở ngay form RFQ/PO chuẩn của Odoo
- RFQ/PO sẽ mang sẵn liên kết với request 0502

Điều này bám đúng định hướng trong plan:

- dùng `purchase`
- dùng `purchase_stock`
- chỉ cần action mở màn hình PO có sẵn context

## 4. Những gì đã triển khai

### 4.1. Cập nhật dependency

Đã bổ sung dependency trong manifest:

- `purchase`
- `purchase_stock`

### 4.2. Field mới trên `purchase.order`

Đã kế thừa `purchase.order` và thêm:

- `x_psm_0502_request_id`
  - liên kết RFQ/PO với `maintenance.request`
- `x_psm_0502_fsm_task_id`
  - related để bên mua nhìn nhanh task FSM liên quan

### 4.3. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_purchase_order_ids`
  - tập hợp toàn bộ RFQ/PO mua ngoài gắn với request
- `x_psm_0502_purchase_order_count`
  - số lượng RFQ/PO đã gắn
- `x_psm_0502_purchase_order_id`
  - RFQ/PO mới nhất hoặc chính đang được dùng để theo dõi nhanh
- `x_psm_0502_purchase_order_state`
  - trạng thái của RFQ/PO mới nhất

### 4.4. Action nghiệp vụ

Đã bổ sung:

- `action_psm_create_purchase_order()`
- `action_psm_open_purchase_order()`

Ý nghĩa:

- `Create Purchase Order`
  - mở form RFQ/PO chuẩn với context sẵn
- `Open Purchase Order`
  - mở lại RFQ/PO đã liên kết với request

## 5. Logic hiện tại

Khi bấm `Create Purchase Order`, hệ thống sẽ:

1. kiểm tra request có thực sự cần vật tư
2. kiểm tra request không bị đánh dấu `Need Outside Service`
3. kiểm tra đã đi qua bước kiểm tồn
4. kiểm tra `Stock Check Result = not_available`
5. nếu request đã có RFQ/PO chưa `cancel` thì mở lại đơn đó
6. nếu chưa có thì mở form `purchase.order` chuẩn với context:
   - `default_x_psm_0502_request_id`
   - `default_origin`
   - `default_company_id`
   - `default_user_id`

Khi bấm `Open Purchase Order`, hệ thống sẽ:

1. lấy toàn bộ RFQ/PO đã liên kết
2. nếu chỉ có một đơn thì mở form
3. nếu có nhiều đơn thì mở list + form với domain đúng tập đơn liên kết

## 6. Cập nhật giao diện

### 6.1. Trên form `maintenance.request`

Đã thêm các nút:

- `Create Purchase Order`
- `Open Purchase Order`

Trong tab `Material Assessment` đã hiển thị thêm:

- `Purchase Order`
- `Purchase Order Count`
- `Purchase Order State`

### 6.2. Trên list view request

Đã thêm:

- `Purchase Order`
- `Purchase Order State`

### 6.3. Trên search view request

Đã thêm các filter:

- `Has Purchase Order`
- `No Purchase Order`
- `Purchase RFQ`
- `Purchased`

Đã thêm group by:

- `Purchase Order State`

### 6.4. Trên form/list/search của `purchase.order`

Đã thêm hiển thị:

- `0502 Maintenance Request`
- `0502 FSM Task`

Mục đích:

- bên mua nhìn thấy đơn này phát sinh từ request nào
- bên bảo trì có thể mở ngược từ request sang RFQ/PO

## 7. Ý nghĩa của bước này trong luồng 0502

Sau bước 16:

- nếu kho không đủ vật tư

và sau bước 17-18:

- request không tiếp tục đi theo nhánh cấp phát vật tư nội bộ

thì bước 19 là nơi:

- chuyển nhu cầu sang nhánh mua ngoài
- tạo RFQ/PO chuẩn để bộ phận liên quan xử lý tiếp

Trong `Phase 1`, đây chỉ là lớp tích hợp nhẹ:

- request biết mở RFQ/PO
- RFQ/PO biết request nguồn

chưa phải full flow mua ngoài đặc thù 0502.

## 8. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- purchase requisition
- nhiều báo giá nhiều vendor
- tự động sinh dòng sản phẩm từ stock move/material requirement
- duyệt RFQ/PO theo rule riêng của 0502
- theo dõi ETA nhà cung cấp trên request
- đồng bộ trạng thái mua ngoài quay ngược về quyết định sửa chữa

Các phần đó phù hợp hơn với:

- `Phase 2`
- hoặc các bước sau nếu business muốn đi sâu nhánh mua ngoài

## 9. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- `Has Material Request = True`
- `Stock Check Result = Stock Not Available`
- không đánh dấu `Need Outside Service`

Ví dụ:

- `Request`: `Cửa hàng Q1 - Máy in hóa đơn mờ chữ`

Sau đó bấm:

- `Create Purchase Order`

## 10. Điều cần test

Checklist test tối thiểu:

- request không cần vật tư
  - bấm `Create Purchase Order`
  - kỳ vọng: báo lỗi validation

- request chưa kiểm tồn
  - bấm `Create Purchase Order`
  - kỳ vọng: báo lỗi validation

- request có `Stock Check Result = available`
  - bấm `Create Purchase Order`
  - kỳ vọng: báo lỗi validation

- request có `Stock Check Result = not_available`
  - bấm `Create Purchase Order`
  - kỳ vọng:
    - mở form RFQ/PO chuẩn
    - có sẵn `0502 Maintenance Request`
    - có `Origin`

- request đã có RFQ/PO chưa cancel
  - bấm `Create Purchase Order` lại
  - kỳ vọng: không mở form tạo mới, mà mở lại đơn đã có

- sau khi lưu RFQ/PO
  - quay lại request
  - bấm `Open Purchase Order`
  - kỳ vọng: mở đúng đơn đã liên kết

## 11. Các file đã thay đổi

- `__manifest__.py`
- `models/__init__.py`
- `models/maintenance_request.py`
- `models/purchase_order.py`
- `views/maintenance_request_views.xml`
- `views/purchase_order_views.xml`

## 12. Kết luận

Bước 19 hiện tại đã đạt mục tiêu của `Phase 1`:

- có nhánh mua ngoài tối thiểu khi kho không đủ tồn
- tận dụng được RFQ/PO chuẩn của Odoo
- có liên kết ngược giữa request 0502 và đơn mua
- chưa làm nặng sang requisition hay flow mua phức tạp

