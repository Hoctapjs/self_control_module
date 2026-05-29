# Phase 2 - Bước 4 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 4` tập trung vào việc chuẩn hóa phần kiểm tra thực tế ban đầu trên `maintenance.request`, để chuyển từ kiểu ghi chú rời sang form kiểm tra có cấu trúc hơn.

Mục tiêu của bước này là:

- giảm phụ thuộc vào một ô note tự do
- chuẩn hóa các tiêu chí kiểm tra ban đầu
- làm dữ liệu inspection có thể lọc, nhóm, phân tích về sau

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

Plan của `Phase 2` đặt ra 2 hướng:

- đánh giá dùng `maintenance_worksheet`
- nếu không đủ, tạo checklist/wizard kiểm tra ban đầu

Ở bước này, hướng triển khai được chọn là:

- chưa kéo `maintenance_worksheet` vào
- chưa tạo wizard riêng
- trước mắt mở rộng ngay trên `maintenance.request` bằng bộ field inspection có cấu trúc

Lý do:

- giữ scope vừa phải
- tận dụng object trung tâm đã ổn định từ `Phase 1`
- vẫn đạt mục tiêu chuyển từ “note rời” sang “form kiểm tra có cấu trúc”

## 4. Các field mới đã thêm

Trên [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `x_psm_0502_inspection_symptom_status`
- `x_psm_0502_inspection_equipment_status`
- `x_psm_0502_inspection_safety_risk`
- `x_psm_0502_inspection_action_urgency`

### Ý nghĩa của từng field

#### `Symptom Status`

Cho biết triệu chứng do cửa hàng báo lên:

- đã xác nhận đúng
- chưa xác nhận đúng
- hay chưa thể xác minh ngay

#### `Equipment Status`

Cho biết trạng thái thiết bị tại thời điểm kiểm tra:

- đang chạy bình thường
- đang chạy nhưng có lỗi
- đã dừng

#### `Safety Risk Level`

Cho biết mức độ rủi ro an toàn mà kỹ thuật viên/CMT đánh giá tại hiện trường:

- không có rủi ro
- thấp
- trung bình
- cao

#### `Action Urgency`

Cho biết mức độ khẩn của hành động xử lý tiếp theo:

- bình thường
- khẩn
- xử lý ngay

## 5. Thay đổi trong logic

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_mark_inspected()` đã được siết lại.

Trước đây:

- chỉ cần user bấm `Mark Inspected`
- dữ liệu inspection chủ yếu nằm ở `Initial Inspection Result` và `Initial Inspection Note`

Hiện tại:

- nếu thiếu các field structured inspection thì không cho chốt `Mark Inspected`

Các field bắt buộc phải có trước khi chốt:

- `Initial Inspection Result`
- `Symptom Status`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`

Nếu thiếu, hệ thống báo lỗi rõ danh sách field còn thiếu.

## 6. Thay đổi trong giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Initial Inspection` đã được mở rộng.

### Form view

Tab `Initial Inspection` hiện có:

- `Initial Inspection Result`
- `Symptom Status`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`
- `Inspected By`
- `Inspected At`
- `Initial Inspection Note`

Như vậy tab này giờ đóng vai trò như một form kiểm tra ban đầu có cấu trúc, thay vì chỉ là một kết luận và một ô note tự do.

### List view

Đã thêm các field inspection mới ở dạng `optional="hide"` để có thể bật lên khi cần:

- `Symptom Status`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`

### Search view

Đã thêm:

- field search cho các field inspection mới
- filter:
  - `High Safety Risk`
  - `Equipment Stopped`
- group by:
  - `Equipment Status`
  - `Safety Risk Level`

## 7. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 4`, hiện chưa làm:

- chưa dùng `maintenance_worksheet`
- chưa có wizard inspection riêng
- chưa có checklist line-by-line kiểu one2many
- chưa có scoring/điểm inspection
- chưa có template inspection theo từng loại thiết bị

## 8. Cách test

### Case 1 - Thiếu field structured inspection

1. Upgrade module `M02_P0502`
2. Mở một request cần kiểm tra ban đầu
3. Chỉ điền một phần thông tin inspection
4. Bấm `Mark Inspected`

Kết quả mong đợi:

- hệ thống chặn
- báo rõ field inspection nào còn thiếu

### Case 2 - Điền đủ dữ liệu inspection

1. Mở request
2. Vào tab `Initial Inspection`
3. Điền đủ:
   - `Initial Inspection Result`
   - `Symptom Status`
   - `Equipment Status`
   - `Safety Risk Level`
   - `Action Urgency`
4. Bấm `Mark Inspected`

Kết quả mong đợi:

- hệ thống cho chốt inspection
- ghi `Inspected By`
- ghi `Inspected At`

### Case 3 - Lọc dữ liệu inspection

1. Mở danh sách `Maintenance Requests`
2. Test filter:
   - `High Safety Risk`
   - `Equipment Stopped`
3. Test group by:
   - `Equipment Status`
   - `Safety Risk Level`

## 9. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 10. Kết luận

`Phase 2 - Bước 4` đã được triển khai theo hướng:

- không đổi object trung tâm
- không dựng workflow inspection mới
- nhưng đã chuyển inspection từ dạng note rời sang dạng structured form rõ hơn

Đây là bước quan trọng để:

- dữ liệu kiểm tra ban đầu có chất lượng tốt hơn
- phục vụ tốt hơn cho bước lập kế hoạch, điều phối và phân tích về sau. 
