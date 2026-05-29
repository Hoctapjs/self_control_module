# Phase 2 - Bước 3 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 3` tập trung vào việc làm rõ cách `CMT` tiếp nhận `maintenance.request`, đồng thời giảm bớt thao tác ghi dấu vết thủ công đối với các request tạo theo luồng thông thường.

Mục tiêu của bước này là:

- làm rõ ai là người tiếp nhận request
- giảm thao tác bấm nút chỉ để ghi dấu vết
- không làm sai dấu vết nghiệp vụ ở các nguồn phát sinh đặc thù

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

- giảm thao tác “bấm nút để ghi dấu vết”
- làm rõ vai trò người tiếp nhận

Sau khi rà lại nghiệp vụ, hướng triển khai cuối cùng được chọn là:

- chỉ auto `receive` cho `manual_request`
- không auto `receive` cho:
  - `helpdesk_ticket`
  - `imported_request`
  - `preventive_cron`

Lý do:

- chỉ với `manual_request` mới còn có thể chấp nhận giả định:
  - người tạo request cũng là người CMT tiếp nhận
- với `helpdesk_ticket` hoặc `imported_request`, người tạo record không nhất thiết là người intake thực tế
- với `preventive_cron`, đây là request hệ thống tự sinh nên càng không nên auto đóng dấu tiếp nhận

## 4. Các thay đổi trong model

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_auto_receive_request_if_needed()`

Hàm này dùng để:

- lọc ra các request đủ điều kiện auto tiếp nhận
- tự ghi:
  - `x_psm_0502_received_by_id`
  - `x_psm_0502_received_at`

### Logic cuối cùng của auto receive

Auto receive chỉ chạy khi:

- request chưa có `x_psm_0502_received_at`
- và `x_psm_0502_source_system == manual_request`

### Các nguồn không auto receive

- `helpdesk_ticket`
- `imported_request`
- `preventive_cron`
- `other`

## 5. Hàm này được gọi ở đâu

Hàm `_psm_auto_receive_request_if_needed()` được gọi ngay trong `create()`.

Ý nghĩa:

- request vừa được tạo xong
- nếu đúng là `manual_request`
- thì hệ thống tự đóng dấu:
  - ai tiếp nhận
  - tiếp nhận lúc nào

Nếu request đến từ các nguồn khác thì không tự ghi dấu này.

## 6. Các thay đổi về label và giao diện

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã đổi label:

- `Received By` -> `Received By (CMT)`
- `Received At` -> `Received At (CMT)`

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã đổi và bổ sung:

- nút:
  - `Receive` -> `CMT Receive`
- filter:
  - `0502 Intake Queue`
  - `Received by CMT`
  - `Not Received by CMT`

Ý nghĩa:

- user nhìn vào sẽ hiểu rõ hơn đây là dấu vết tiếp nhận ở vai trò `CMT`
- tránh hiểu nhầm với các loại “nhận” khác trong quy trình

## 7. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 3`, hiện chưa làm:

- chưa thêm activity bắt buộc cho người tiếp nhận
- chưa tự gán người tiếp nhận theo role/group
- chưa có queue intake riêng theo từng loại source
- chưa tách workflow riêng cho `helpdesk_ticket` và `imported_request`

## 8. Cách test

### Case 1 - Manual Request

1. Upgrade module `M02_P0502`
2. Tạo một request mới với:
   - `Source System = Manual Request`
3. Save request

Kết quả mong đợi:

- request tự có:
  - `Received By (CMT)`
  - `Received At (CMT)`

### Case 2 - Helpdesk Ticket

1. Tạo một request mới với:
   - `Source System = Helpdesk Ticket`
2. Save request

Kết quả mong đợi:

- request không tự có:
  - `Received By (CMT)`
  - `Received At (CMT)`
- user phải dùng thao tác tiếp nhận riêng nếu business cần

### Case 3 - Imported Request

1. Tạo một request mới với:
   - `Source System = Imported Request`
2. Save request

Kết quả mong đợi:

- request không auto receive

### Case 4 - Preventive Cron

1. Để hệ thống sinh request preventive
2. Mở request vừa sinh

Kết quả mong đợi:

- request không auto receive

## 9. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 10. Kết luận

`Phase 2 - Bước 3` đã được triển khai theo hướng:

- tự động hóa ở mức vừa đủ
- không làm sai dấu vết nghiệp vụ
- làm rõ vai trò `CMT` trong bước tiếp nhận

Điểm quan trọng nhất của bước này là:

- **chỉ auto receive cho `manual_request`**

Đây là lựa chọn cân bằng giữa:

- giảm thao tác thủ công
- và giữ dấu vết tiếp nhận đủ đúng với nghiệp vụ thực tế.
