# Phase 2 - Bước 11 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 11` tập trung vào việc chuẩn hóa bước:

- đề xuất phương án xử lý
- báo giá sơ bộ

Mục tiêu chính là:

- tách rõ nội dung kỹ thuật và nội dung chi phí
- giảm việc người dùng ghi tất cả vào một text field duy nhất
- vẫn giữ tương thích với flow `Phase 1` và các bước sau đang dùng `Treatment Proposal` như một summary chung

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

- thêm cấu trúc cho:
  - nguyên nhân
  - phương án
  - chi phí
  - timeline
- cân nhắc dùng worksheet hoặc wizard thay vì chỉ text field

Hướng triển khai được chọn là:

- chưa kéo `worksheet` vào ở bước này
- chưa tạo wizard riêng
- tiếp tục làm trực tiếp trên `maintenance.request`
- thêm bộ field có cấu trúc
- vẫn giữ `x_psm_0502_treatment_proposal` như summary chuẩn hóa để không làm vỡ các bước đã có

Đây là hướng `custom vừa`, đúng với scope của `Phase 2 - Bước 11`.

## 4. Các field có cấu trúc đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_root_cause_analysis`
- `x_psm_0502_technical_solution`
- `x_psm_0502_cost_note`
- `x_psm_0502_timeline_note`

### Ý nghĩa của từng field

#### `Root Cause Analysis`

Ghi nguyên nhân gốc mà `CMT` xác định sau khi kiểm tra.

Ví dụ:

- hỏng do hao mòn linh kiện
- tắc nghẽn đường ống
- motor yếu, hoạt động không ổn định

#### `Technical Solution`

Ghi phương án kỹ thuật để xử lý.

Ví dụ:

- thay ống thoát nước
- thay đầu in
- vệ sinh, cân chỉnh và kiểm tra lại

#### `Cost Note`

Ghi chú bổ sung cho phần chi phí, ví dụ:

- chi phí đã gồm vật tư nhưng chưa gồm công ngoài giờ
- giá tạm tính theo báo giá hiện tại
- cần chờ xác nhận giá mua ngoài

#### `Timeline Note`

Ghi chú bổ sung cho timeline, ví dụ:

- cần chờ hàng về
- phải xử lý ngoài giờ hoạt động của cửa hàng
- chia làm 2 đợt thi công

## 5. Giữ `Treatment Proposal` như summary chuẩn hóa

Module vẫn giữ field:

- `x_psm_0502_treatment_proposal`

nhưng vai trò của field này sau bước 11 là:

- summary chuẩn hóa
- dùng lại cho các bước sau

Lý do giữ lại:

- `FSM Task` đang đọc summary này
- flow vật tư/kho/mua ngoài có chỗ đang reuse summary này
- nếu bỏ ngay sẽ làm vỡ compatibility với phần đã triển khai ở `Phase 1` và `Phase 2`

## 6. Helper build summary đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm helper:

- `_psm_build_treatment_proposal_summary()`

Hàm này dùng để build lại `Treatment Proposal` summary từ các field structured.

### Nội dung summary được gom từ

- `Root Cause Analysis`
- `Technical Solution`
- `Estimated Cost`
- `Cost Note`
- `Estimated Timeline`
- `Timeline Note`

Kết quả:

- user điền dữ liệu có cấu trúc
- hệ thống tự tạo summary text nhất quán để downstream tiếp tục dùng

## 7. Thay đổi trong logic `Mark Proposed`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_mark_proposed()` đã được siết lại.

Trước đây:

- chỉ cần có `Treatment Proposal`

Sau bước này:

- phải có đủ bộ tối thiểu:
  - `Root Cause Analysis`
  - `Technical Solution`
  - `Estimated Cost`
  - `Estimated Timeline`

Nếu thiếu, hệ thống sẽ chặn và báo rõ field nào còn thiếu.

Khi bấm `Mark Proposed`, hệ thống sẽ:

1. validate các field structured
2. tự build lại `Treatment Proposal` summary
3. ghi:
   - `Proposed By`
   - `Proposed At`

## 8. Thay đổi giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Treatment Proposal` đã được bố cục lại.

### Phần hiển thị chính

- `Proposed By`
- `Proposed At`
- `Estimated Cost`
- `Estimated Timeline`
- `Root Cause Analysis`
- `Technical Solution`
- `Cost Note`
- `Timeline Note`

### Phần summary

Đã thêm một cụm:

- `Proposal Summary`

Trong đó:

- `x_psm_0502_treatment_proposal` được hiển thị `readonly`

Ý nghĩa:

- người dùng nhập dữ liệu ở các field structured
- summary chỉ để xem kết quả chuẩn hóa sau khi hệ thống build lại

## 9. Ý nghĩa nghiệp vụ của bước này

`Phase 1 - Bước 11` đã cho phép:

- ghi proposal
- ghi cost
- ghi timeline

Nhưng proposal lúc đó còn quá tự do:

- mỗi người ghi một kiểu
- khó phân tích lại
- khó tách nội dung kỹ thuật với nội dung chi phí/timeline

Sau bước này:

- proposal có cấu trúc hơn
- người đọc dễ hiểu hơn
- dữ liệu có thể reuse tốt hơn ở các bước sau

## 10. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 11`, hiện chưa làm:

- chưa tạo wizard proposal riêng
- chưa dùng `worksheet`
- chưa tách proposal thành model con riêng
- chưa thêm cost line chi tiết theo vật tư/công/chi phí khác
- chưa thêm approval matrix mới cho proposal

## 11. Cách test

### Case 1 - Chặn khi thiếu field structured

1. Upgrade `M02_P0502`
2. Mở một `maintenance.request` cần đề xuất xử lý
3. Vào tab `Treatment Proposal`
4. Bấm `Mark Proposed` khi còn thiếu các field structured

Kết quả mong đợi:

- hệ thống chặn
- báo rõ các field còn thiếu

### Case 2 - Tạo proposal đầy đủ

1. Điền đủ:
   - `Root Cause Analysis`
   - `Technical Solution`
   - `Estimated Cost`
   - `Estimated Timeline`
2. điền thêm:
   - `Cost Note`
   - `Timeline Note`
   nếu cần
3. Bấm `Mark Proposed`

Kết quả mong đợi:

- `Proposed By` có giá trị
- `Proposed At` có giá trị
- `Proposal Summary` được build tự động

### Case 3 - Kiểm tra compatibility với bước sau

1. Sau khi `Mark Proposed`, tiếp tục đi qua:
   - approval
   - create FSM task
   - các bước downstream có dùng summary

Kết quả mong đợi:

- các bước sau vẫn đọc được `Treatment Proposal` summary như trước

## 12. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse: `OK`

## 13. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
