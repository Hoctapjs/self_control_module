# Phase 2 - Bước 16 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 16` tập trung vào việc nâng bước:

- kiểm tra tồn kho

theo 2 hướng chính:

- làm rõ tiêu chí `đủ tồn / không đủ tồn`
- giảm mâu thuẫn giữa field custom và compute chuẩn của `stock.picking`

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- bám hoàn toàn vào compute chuẩn của `stock.picking`
- nếu cần, tách:
  - availability hiện tại
  - kết quả check tại thời điểm quyết định

Hướng triển khai được chọn là:

- giữ compute chuẩn của `stock.picking` làm nguồn sự thật cho availability hiện tại
- giữ `x_psm_0502_stock_check_result` làm snapshot quyết định nghiệp vụ
- bổ sung thêm snapshot chi tiết của lần check để người dùng nhìn rõ hơn

Lý do chọn hướng này:

- không làm vỡ flow đã có của các bước sau
- giải quyết đúng chỗ từng gây mâu thuẫn giữa live availability và checked result
- dễ hiểu hơn trên giao diện

## 4. Các lớp dữ liệu availability sau khi chỉnh

Sau bước này, trên `maintenance.request` có 2 lớp dữ liệu khác nhau:

### 4.1. Availability hiện tại

Lấy trực tiếp từ `stock.picking` bằng related field:

- `x_psm_0502_stock_availability`
- `x_psm_0502_stock_availability_state`

Đây là:

- trạng thái live hiện tại của picking
- có thể thay đổi theo tồn kho, reserve, state của picking

Để tránh hiểu nhầm, label đã được đổi thành:

- `Current Stock Availability`
- `Current Stock Availability State`

### 4.2. Availability tại thời điểm check

Là snapshot được lưu khi user bấm `Check Stock Availability`:

- `x_psm_0502_stock_check_availability`
- `x_psm_0502_stock_check_availability_state`
- `x_psm_0502_stock_check_result`

Đây là:

- kết quả đã được ghi nhận tại thời điểm quyết định nghiệp vụ
- được các bước sau dùng tiếp

## 5. Helper mới đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_stock_check_snapshot_values(picking)`

Helper này đọc từ `stock.picking`:

- `products_availability`
- `products_availability_state`

rồi quy đổi ra bộ snapshot để lưu lên request.

### Rule quy đổi

- nếu `products_availability_state == "available"`
  - `Stock Check Result = available`
- còn lại
  - `Stock Check Result = not_available`

Ý nghĩa:

- kết quả quyết định luôn bám compute chuẩn của `stock.picking`

## 6. Thay đổi trong `action_psm_check_stock_availability()`

Action này vẫn giữ flow gốc:

- yêu cầu phải có `Stock Picking`
- yêu cầu phải có dòng vật tư
- nếu picking đang draft thì confirm
- sau đó gọi `action_assign()`

Điểm thay đổi của `Phase 2 - Bước 16` là:

- sau khi reserve/check theo flow chuẩn, action sẽ lưu snapshot đầy đủ:
  - `Checked Stock Availability`
  - `Checked Stock Availability State`
  - `Stock Check Result`
  - `Stock Checked By`
  - `Stock Checked At`

## 7. Thay đổi ở giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Material Assessment` đã được cập nhật để hiển thị rõ:

- `Current Stock Availability`
- `Current Stock Availability State`
- `Checked Stock Availability`
- `Checked Stock Availability State`
- `Stock Check Result`

Ngoài ra:

- list view có thêm field snapshot kỹ thuật của lần check
- search view có thể tìm theo các field snapshot mới

## 8. Ý nghĩa nghiệp vụ của bước này

Trước đây có thể xảy ra tình huống:

- `Stock Check Result` nói một đằng
- `Stock Availability` live của picking nói một nẻo

Sau bước này:

- live availability vẫn được giữ nguyên để nhìn thực trạng hiện tại
- snapshot checked giữ lại để phục vụ quyết định nghiệp vụ tại thời điểm check

Kết quả là:

- người dùng không còn nhầm giữa “trạng thái bây giờ”
- và “kết quả đã chốt lúc quyết định”

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 16`, hiện chưa làm:

- chưa thêm lịch sử nhiều lần check riêng thành model log
- chưa tách kết luận availability theo từng dòng vật tư
- chưa thêm dashboard riêng cho biến động giữa current vs checked

## 10. Cách test

### Case 1 - Check tồn và lưu snapshot

1. Upgrade `M02_P0502`
2. Mở request đã có `Stock Picking`
3. Đảm bảo picking có dòng vật tư hợp lệ
4. Bấm `Check Stock Availability`

Kết quả mong đợi:

- `Stock Check Result` được set
- `Checked Stock Availability`
- `Checked Stock Availability State`
- `Stock Checked By`
- `Stock Checked At`

được ghi đúng

### Case 2 - So sánh current và checked

1. Sau khi đã check tồn, thay đổi dữ liệu tồn kho hoặc reserve trên picking
2. Mở lại request

Kết quả mong đợi:

- `Current Stock Availability` có thể thay đổi theo thực trạng live
- `Checked Stock Availability` vẫn giữ snapshot tại lần bấm check trước đó

### Case 3 - Quyết định downstream vẫn bám snapshot

1. Dùng request vừa check tồn
2. Thử các bước sau:
   - approval vật tư
   - tạo purchase order

Kết quả mong đợi:

- các bước sau vẫn bám `Stock Check Result`
- không bám trực tiếp field live của picking

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse: `OK`

## 12. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
