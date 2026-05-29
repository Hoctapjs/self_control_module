# Phase 3 - Bước 2 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 2` tập trung vào việc:

- chốt mẫu intake hoàn chỉnh hơn theo đúng loại request
- giúp người dùng biết cần ghi nhận thông tin ban đầu gì
- phân biệt rõ request nào đã đủ intake chi tiết, request nào chưa

Bước này không nhằm:

- dựng dynamic form đầy đủ
- dựng worksheet intake riêng
- tạo thêm workflow điều phối mới

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [request_type_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/request_type_data.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 3`, `Bước 2` cần đi theo hướng:

- có mẫu intake theo `Request Type`
- có thêm dữ liệu ban đầu giàu ngữ cảnh hơn
- nhưng chưa kéo sang dynamic form nặng hoặc worksheet intake riêng

Hướng triển khai được chọn là:

- đặt template intake ngay trên master `Request Type`
- hiển thị template đó trực tiếp trên `maintenance.request`
- bổ sung một bộ intake detail gọn trên request
- dùng validation ở thời điểm `CMT Receive` để bảo đảm `Bước 2` thực sự được đi qua

Lý do chọn hướng này:

- bám sát lưu đồ hiện tại
- đủ dùng cho nghiệp vụ intake ban đầu
- tránh mở scope sang form động hoặc cấu trúc master phức tạp hơn

## 4. Những gì đã thêm trên `x_psm_request_type`

Trong [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py), đã bổ sung:

- `x_psm_0502_intake_question_template`
- `x_psm_0502_intake_example_note`

### 4.1. `0502 Intake Question Template`

Field này dùng để lưu:

- bộ câu hỏi intake chuẩn theo từng loại request

Mục tiêu:

- khi người dùng chọn `Request Type`, hệ thống sẽ hiển thị ngay hướng dẫn cần hỏi / cần ghi nhận

### 4.2. `0502 Intake Example Note`

Field này dùng để lưu:

- ví dụ ghi chú intake mẫu

Mục tiêu:

- giúp người dùng ghi nhận thông tin ban đầu gọn, đúng ý hơn

## 5. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_intake_template_guide`
- `x_psm_0502_intake_example_note`
- `x_psm_0502_intake_detail_ready`
- `x_psm_0502_intake_detail_gap_reason`
- `x_psm_0502_intake_problem_detail`
- `x_psm_0502_intake_impact_scope`
- `x_psm_0502_intake_contact_name`
- `x_psm_0502_intake_contact_phone`

## 6. Ý nghĩa của các field mới trên request

### 6.1. `Intake Template Guide`

Là phần hướng dẫn intake đang áp dụng cho request hiện tại theo `Request Type`.

### 6.2. `Intake Example Note`

Là ví dụ ghi chú intake được lấy từ `Request Type` để người dùng tham khảo.

### 6.3. `Intake Detail Ready`

Cho biết:

- request đã đủ intake chi tiết ở `Bước 2` hay chưa

### 6.4. `Intake Detail Gap Reason`

Cho biết:

- đang thiếu field intake chi tiết nào

### 6.5. `Intake Problem Detail`

Lưu mô tả chi tiết hơn về vấn đề / nhu cầu phát sinh ban đầu.

### 6.6. `Intake Impact Scope`

Phản ánh mức ảnh hưởng ban đầu tới vận hành:

- `Limited Impact`
- `Degraded Operation`
- `Operation Blocked`

### 6.7. `Intake Contact Name`

Lưu đầu mối liên hệ chính ở giai đoạn intake.

### 6.8. `Intake Contact Phone`

Lưu số điện thoại đầu mối liên hệ ở giai đoạn intake.

## 7. Logic template intake theo `Request Type`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_request_type_intake_template_text()`

Rule hiện tại:

- nếu `Request Type` đã cấu hình `0502 Intake Question Template` thì dùng trực tiếp
- nếu chưa có template riêng thì fallback theo `code`

Các fallback hiện có:

- `maintenance`
- `repair`
- `inspection`

Ý nghĩa:

- không cần chờ cấu hình master đầy đủ mới dùng được
- nhưng vẫn có đường để doanh nghiệp custom template riêng theo `Request Type`

## 8. Logic xác định intake detail còn thiếu

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_intake_detail_gap_labels()`

Rule hiện tại:

- với `Request Origin Group = preventive_need`
  - không ép contact và problem detail theo cùng mẫu
- với `store_need` và `system_need`
  - bắt buộc:
    - `Intake Problem Detail`
    - `Intake Impact Scope`
    - `Intake Contact Name`

Nếu thiếu:

- `Intake Detail Ready = False`
- `Intake Detail Gap Reason` sẽ liệt kê rõ field còn thiếu

Nếu đủ:

- `Intake Detail Ready = True`

## 9. Compute và validation mới

Đã thêm các compute:

- `_compute_x_psm_0502_intake_template_fields()`
- `_compute_x_psm_0502_intake_detail_ready_fields()`

Đã thêm validation:

- `_psm_validate_request_intake_detail_data()`

Ý nghĩa:

- template intake sẽ tự đổi theo `Request Type`
- trạng thái `Intake Detail Ready` luôn đồng bộ theo dữ liệu hiện tại
- khi `CMT Receive`, request sẽ bị chặn nếu intake chi tiết chưa đủ

## 10. Điều chỉnh logic `CMT Receive` và auto receive

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py):

- `action_psm_receive_request()` giờ gọi validation intake detail trước khi cho receive
- `_psm_auto_receive_request_if_needed()` giờ chỉ auto receive cho `manual_request` khi:
  - chưa receive
  - và intake detail đã đủ

Ý nghĩa:

- không cho request “nhảy qua” `Bước 2`
- auto receive không còn làm mờ ranh giới giữa:
  - ghi nhận thông tin ban đầu
  - và xác nhận tiếp nhận

## 11. Thay đổi trên giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã cập nhật:

### Form view

- hiển thị thêm:
  - `Intake Detail Ready`
  - `Intake Detail Gap Reason`
- thêm khối:
  - `Request Intake Template`
  - `Request Intake Detail`

### List view

- thêm cột optional:
  - `Intake Detail Ready`

### Search view

- thêm field search:
  - `Intake Detail Ready`
- thêm filter:
  - `Intake Detail Ready`
  - `Intake Detail Gap`
- thêm group by:
  - `Intake Detail Ready`

## 12. Những gì bước này cố ý chưa làm

Để tránh làm dư hơn so với yêu cầu hiện tại, `Phase 3 - Bước 2` chưa làm:

- dynamic form theo `Request Type`
- worksheet intake riêng
- template riêng theo `Equipment`
- activity checklist intake
- object intake riêng tách khỏi `maintenance.request`

## 13. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 2` rõ hơn ở ba câu hỏi:

1. Với loại request hiện tại, nên hỏi / ghi nhận những gì?
2. Request này đã đủ intake chi tiết chưa?
3. Nếu chưa đủ, đang thiếu đúng phần nào?

Điều này giúp:

- intake đồng nhất hơn theo loại request
- tránh ghi chú quá sơ sài
- giữ ranh giới rõ giữa `Bước 2` và `Bước 3`

## 14. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 15. Cách test

1. Upgrade `M02_P0502`.
2. Mở một request `manual_request` hoặc `helpdesk_ticket`.
3. Chọn `Request Type`.
4. Kiểm tra:
- `Intake Template Guide` hiển thị đúng theo `Request Type`
- nếu `Request Type` chưa có template riêng thì hệ thống dùng fallback theo `code`
5. Để trống một trong các field sau:
- `Intake Problem Detail`
- `Intake Impact Scope`
- `Intake Contact Name`
6. Bấm `CMT Receive`.
- kỳ vọng bị chặn
- `Intake Detail Ready = False`
- `Intake Detail Gap Reason` hiển thị rõ phần còn thiếu
7. Điền đủ các field trên rồi bấm lại:
- kỳ vọng receive thành công
8. Tạo request `preventive_need`:
- kỳ vọng không bị ép cùng bộ intake chi tiết như store/system

## 16. File đã thay đổi

- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
