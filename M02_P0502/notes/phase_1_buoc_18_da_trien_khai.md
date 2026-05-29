# Phase 1 - Bước 18 đã triển khai

## 1. Mục tiêu của bước 18

Bước 18 trong quy trình 0502 là:

- thực hiện xuất kho vật tư thực tế
- ghi nhận rằng request đã đi qua nhánh vật tư nội bộ thành công

Trong `Phase 1`, mục tiêu của bước này là:

- tận dụng flow chuẩn `Validate` của `stock.picking`
- không custom sâu vào nghiệp vụ kho
- chỉ bổ sung lớp liên kết tối thiểu từ `maintenance.request`

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

Ở giai đoạn này, bước 18 được hiểu đơn giản là:

- request đã qua:
  - đánh giá vật tư
  - kiểm tra tồn
  - duyệt vật tư
- sau đó người dùng bấm xác nhận xuất kho
- hệ thống gọi flow chuẩn của `stock.picking`

Không làm ở bước này:

- wizard đặc thù 0502 cho kho
- flow cấp phát nhiều chặng
- logic tách riêng giữa kho trung tâm và kho cửa hàng

## 4. Những gì đã triển khai

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_stock_issued_by_id`
  - ghi nhận ai xác nhận xuất kho thực tế
- `x_psm_0502_stock_issued_at`
  - ghi nhận thời điểm xuất kho thực tế

### 4.2. Action nghiệp vụ

Đã bổ sung:

- `action_psm_validate_stock_picking()`
- `action_psm_mark_stock_issued()`

Ý nghĩa:

- `Validate Stock Picking`
  - gọi flow chuẩn `button_validate()` của `stock.picking`
- `Mark Stock Issued`
  - dùng để chốt dấu vết bước 18 trong trường hợp flow kho chuẩn mở wizard riêng và user quay lại request sau đó

## 5. Logic hiện tại

Khi bấm `Validate Stock Picking`, hệ thống sẽ:

1. kiểm tra request đã có `Stock Picking`
2. kiểm tra `Material Approval Status = approved`
3. nếu picking đã `cancel` thì chặn
4. nếu picking đã `done` thì chỉ cập nhật dấu vết bước 18 nếu chưa có
5. kiểm tra picking có ít nhất một dòng `stock.move` với `Demand > 0`
6. nếu picking còn `draft` thì gọi `action_confirm()`
7. gọi `button_validate()` theo flow chuẩn của Odoo
8. nếu picking sang `done` ngay trong cùng request thì ghi:
   - `Stock Issued By`
   - `Stock Issued At`

Khi bấm `Mark Stock Issued`, hệ thống sẽ:

1. kiểm tra request đã có `Stock Picking`
2. kiểm tra picking đã ở trạng thái `done`
3. ghi:
   - `Stock Issued By`
   - `Stock Issued At`

## 6. Cập nhật sau khi test thực tế

### 6.1. Sửa runtime bug do khác biệt field của Odoo 19

Khi test thực tế, đã xuất hiện lỗi:

- `AttributeError: 'stock.picking' object has no attribute 'move_ids_without_package'`

Nguyên nhân:

- code ban đầu dùng `move_ids_without_package`
- nhưng trong source Odoo 19 local, `stock.picking` dùng `move_ids`

Đã sửa:

- thay `picking.move_ids_without_package`
- bằng `picking.move_ids`

Điều chỉnh này giúp bước 18 bám đúng model chuẩn của Odoo 19.

### 6.2. Tinh chỉnh UX sau khi picking đã `Done`

Sau khi test liên thông với bước 16 và 18, đã tinh chỉnh form request:

- ẩn nút `Check Stock Availability` khi:
  - picking đã `done`
  - hoặc picking đã `cancel`
- ẩn:
  - `Stock Availability`
  - `Stock Availability State`
  khi picking đã `done`

Lý do:

- hai field availability chuẩn của `stock.picking` sẽ về rỗng khi picking `Done`
- nếu vẫn hiển thị sẽ dễ gây hiểu nhầm cho user

## 7. Cập nhật giao diện

### 7.1. Trên form `maintenance.request`

Đã thêm nút:

- `Validate Stock Picking`
- `Mark Stock Issued`

Trong tab `Material Assessment` đã hiển thị:

- `Stock Issued By`
- `Stock Issued At`

### 7.2. Trên list view

Đã thêm các cột:

- `Stock Issued By`
- `Stock Issued At`

### 7.3. Trên search view

Đã thêm các filter:

- `Stock Issued`
- `Stock Not Issued`

Đã thêm group by:

- `Stock Issued By`

## 8. Ý nghĩa của bước này trong luồng 0502

Sau bước 17:

- request đã được duyệt nhánh vật tư nội bộ

thì bước 18 là nơi:

- phiếu kho được xác nhận theo flow chuẩn
- vật tư được xem là đã xuất kho thực tế
- request có dấu vết hoàn tất nhánh xuất kho

Trong `Phase 1`, đây vẫn là một lớp tích hợp nhẹ:

- tận dụng `stock.picking`
- không thay thế logic kho của Odoo

## 9. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- wizard 0502 riêng cho xuất kho
- auto split picking theo nhiều kho
- auto xử lý backorder đặc thù 0502
- kiểm soát định mức vật tư theo loại sửa chữa
- liên kết sâu với kế toán giá vốn hoặc valuation

## 10. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã qua bước 17
- `Material Approval Status = Approved`
- đã có `Stock Picking`
- trong picking đã có ít nhất một dòng vật tư với `Demand > 0`

Ví dụ:

- `Request`: `Máy lạnh quầy thu ngân không mát`

Trên picking:

- thêm sản phẩm vật tư
- nhập `Demand`

Sau đó quay lại request và bấm:

- `Validate Stock Picking`

## 11. Điều cần test

Checklist test tối thiểu:

- request chưa có `Stock Picking`
  - bấm `Validate Stock Picking`
  - kỳ vọng: báo lỗi validation

- request chưa `Approved` ở nhánh vật tư
  - bấm `Validate Stock Picking`
  - kỳ vọng: báo lỗi validation

- picking chưa có dòng vật tư nào
  - bấm `Validate Stock Picking`
  - kỳ vọng: báo lỗi yêu cầu thêm ít nhất một dòng vật tư

- request hợp lệ, picking validate xong ngay
  - kỳ vọng:
    - `Stock Picking State = done`
    - có `Stock Issued By`
    - có `Stock Issued At`

- request hợp lệ nhưng flow chuẩn mở wizard kho
  - xử lý wizard theo chuẩn Odoo
  - quay lại request
  - bấm `Mark Stock Issued`
  - kỳ vọng:
    - có `Stock Issued By`
    - có `Stock Issued At`

## 12. Các file đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 13. Kết luận

Bước 18 hiện tại đã đạt mục tiêu của `Phase 1`:

- tận dụng được flow xuất kho chuẩn của `stock`
- có dấu vết rõ ràng trên `maintenance.request`
- đã sửa runtime bug để bám đúng field chuẩn của Odoo 19
- đã tinh chỉnh giao diện để đỡ gây nhiễu sau khi picking `Done`

