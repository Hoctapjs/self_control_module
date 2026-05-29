# Daily Report - 2026-04-28

## 1. Phạm vi làm việc trong ngày

Hôm nay tập trung tiếp tục triển khai `Phase 1` của quy trình `0502 - Quản lý bảo trì`, chủ yếu từ:

- `Bước 12`
- `Bước 13`
- `Bước 14`
- `Bước 15`
- `Bước 16`

Đồng thời xử lý thêm các vấn đề phát sinh khi test luồng kho và giải thích nghiệp vụ/thuật ngữ liên quan.

## 2. Tài liệu định hướng đã dùng

Trong quá trình làm việc hôm nay, đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thật
- nguyên nhân là trong ngày đã bổ sung thêm phần `stock` và logic của các bước 15-16 nhưng map chưa được regenerate lại
- khi phân tích và sửa code, đã ưu tiên dùng source code thật để xác nhận cuối cùng

## 3. Những gì đã triển khai trong ngày

### 3.1. Phase 1 - Bước 12

Đã triển khai bước duyệt proposal ở mức tối thiểu trên `maintenance.request`:

- thêm trạng thái duyệt:
  - `Pending Approval`
  - `Approved`
  - `Rejected`
- thêm các action:
  - `Submit for Approval`
  - `Approve Proposal`
  - `Reject Proposal`
- lưu lại:
  - người quyết định
  - thời điểm quyết định
  - ghi chú duyệt

Đã tạo note:

- `phase_1_buoc_12_da_trien_khai.md`

### 3.2. Phase 1 - Bước 13

Đã triển khai bước thẩm định nội bộ hay dịch vụ ngoài:

- thêm cờ `Need Outside Service`
- thêm ghi chú thẩm định dịch vụ
- thêm dấu vết:
  - ai thẩm định
  - thời điểm thẩm định
- thêm action:
  - `Mark Service Assessed`

Đã tạo note:

- `phase_1_buoc_13_da_trien_khai.md`

### 3.3. Phase 1 - Bước 14

Đã triển khai bước đánh giá phát sinh vật tư:

- thêm cờ `Has Material Request`
- thêm ghi chú đánh giá vật tư
- thêm dấu vết:
  - ai kiểm tra
  - thời điểm kiểm tra
- thêm action:
  - `Mark Material Checked`

Đã tạo note:

- `phase_1_buoc_14_da_trien_khai.md`

### 3.4. Phase 1 - Bước 15

Đã triển khai bước tạo chứng từ kho tối thiểu từ `maintenance.request`:

- thêm dependency `stock`
- thêm field liên kết:
  - `x_psm_0502_stock_picking_id` trên `maintenance.request`
  - `x_psm_0502_request_id` trên `stock.picking`
  - `x_psm_0502_fsm_task_id` trên `stock.picking`
- thêm action:
  - `Create Stock Picking`
  - `Open Stock Picking`
- kế thừa form/list của `stock.picking` để hiển thị liên kết 0502

Đã tạo note:

- `phase_1_buoc_15_da_trien_khai.md`

### 3.5. Phase 1 - Bước 16

Đã triển khai bước kiểm tra tồn kho vật tư ở mức nhẹ:

- tận dụng chuẩn `stock.picking`
- dùng `action_confirm()` và `action_assign()` của Odoo chuẩn để check availability
- thêm các field:
  - `x_psm_0502_stock_picking_state`
  - `x_psm_0502_stock_availability`
  - `x_psm_0502_stock_availability_state`
  - `x_psm_0502_stock_check_result`
  - `x_psm_0502_stock_checked_by_id`
  - `x_psm_0502_stock_checked_at`
- thêm action:
  - `Check Stock Availability`

Đã tạo note:

- `phase_1_buoc_16_da_trien_khai.md`

## 4. Các lỗi / vấn đề đã xử lý trong ngày

### 4.1. Vấn đề `Operation Type` của stock picking bị ra `Receipts`

Trong quá trình test `Bước 15`, đã phát hiện:

- chứng từ kho tạo ra có `Operation Type = Receipts`
- thay vì `Internal Transfers`

Sau khi kiểm tra, nguyên nhân thực tế là:

- dữ liệu test trước đó đã bị chỉnh nhầm ở `Operation Type`
- có thao tác thay đổi kiểu nghiệp vụ kho không đúng

Đồng thời đã siết lại logic code để an toàn hơn:

- ưu tiên lấy `warehouse.int_type_id`
- chỉ fallback sang tìm `stock.picking.type` có `code = internal` nếu cần

Kết quả:

- giảm rủi ro lấy nhầm `Operation Type`
- logic tạo `stock.picking` ổn định hơn trong môi trường test

### 4.2. Vấn đề cấu hình kho chưa đủ để test `Internal Transfer`

Trong quá trình test luồng kho, đã gặp và xử lý các vấn đề:

- chưa có `Internal Transfer` đúng chuẩn
- chưa bật `Storage Locations`
- chưa hiểu rõ `Warehouse`, `Operation Type`, `Source Location`, `Destination Location`

Đã làm rõ:

- cần bật `Storage Locations`
- cần có `Internal Transfer` đúng chuẩn
- cần hiểu đúng vai trò của:
  - `stock.picking`
  - `stock.picking.type`
  - `Internal Transfer`
  - `Source Location`
  - `Destination Location`
  - `Demand`
  - `Validate`

## 5. Hỗ trợ phân tích và giải thích nghiệp vụ

Ngoài phần code, hôm nay cũng đã giải thích và làm rõ thêm:

- ý nghĩa của giao diện `stock.picking`
- các action trên giao diện kho
- cách test `Bước 15`
- cách test `Bước 16`
- thuật ngữ kho chuẩn của Odoo mà quy trình 0502 vừa bắt đầu dùng

## 6. Kết quả hiện tại đến cuối ngày

Đến thời điểm kết thúc ngày làm việc:

- `Phase 1 - Bước 12` đã triển khai xong
- `Phase 1 - Bước 13` đã triển khai xong
- `Phase 1 - Bước 14` đã triển khai xong
- `Phase 1 - Bước 15` đã triển khai xong và đã test
- `Phase 1 - Bước 16` đã triển khai xong

Toàn bộ phần triển khai trong ngày đều đã:

- bám theo convention của module
- ưu tiên tận dụng chuẩn Odoo
- có note triển khai tương ứng cho từng bước

## 7. Kiểm tra kỹ thuật đã làm

Trong ngày đã thực hiện các kiểm tra kỹ thuật mức nhẹ:

- compile Python cho các file model đã sửa
- parse XML cho các file view đã sửa

Kết quả:

- không phát hiện lỗi cú pháp ở các file vừa triển khai

## 8. Việc tiếp theo đề xuất

Bước hợp lý tiếp theo là:

- triển khai `Phase 1 - Bước 17`

Theo plan hiện tại, bước này sẽ tập trung vào:

- điểm duyệt tối thiểu của CMT Lead trước khi xuất vật tư
- tận dụng `maintenance.request` hoặc `stock.picking`
- chưa kéo approval nhiều tầng vào ngay trong `Phase 1`

## 9. Danh sách note đã tạo trong ngày

- `phase_1_buoc_12_da_trien_khai.md`
- `phase_1_buoc_13_da_trien_khai.md`
- `phase_1_buoc_14_da_trien_khai.md`
- `phase_1_buoc_15_da_trien_khai.md`
- `phase_1_buoc_16_da_trien_khai.md`

## 10. Kết luận ngắn

Hôm nay đã đẩy quy trình `0502` đi thêm được một đoạn quan trọng:

- từ khâu duyệt proposal
- qua phân nhánh nội bộ / thuê ngoài
- tới phân nhánh vật tư
- tạo được chứng từ kho
- và có luôn lớp kiểm tra tồn kho bước đầu

Điều này giúp `Phase 1` tiến gần hơn tới một luồng end-to-end có thể test được thực tế.
