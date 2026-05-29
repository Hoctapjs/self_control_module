# Phase 3 - Bước 1 đã triển khai

## 1. Mục tiêu của bước này

`Phase 3 - Bước 1` tập trung vào việc làm rõ:

- nhu cầu bảo trì này phát sinh từ đâu
- dữ liệu đầu vào tối thiểu ở thời điểm phát sinh đã đủ hay chưa

Bước này không nhằm:

- tạo thêm queue intake riêng
- mở rộng workflow nặng hơn lưu đồ hiện tại
- đẩy logic điều phối sớm sang ngay bước phát sinh nhu cầu

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
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [phase_2_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Sau khi rà lại lưu đồ nghiệp vụ, `Bước 1` chỉ là điểm:

- phát sinh nhu cầu từ cửa hàng
- hoặc phát sinh nhu cầu từ nhánh preventive / hệ thống

Vì vậy hướng triển khai được chọn là:

- không dựng thêm intake queue riêng ở bước này
- không thêm approval, assignment, ownership sâu ở bước này
- chỉ làm rõ:
  - nhóm nguồn phát sinh nghiệp vụ
  - mức dữ liệu đầu vào tối thiểu đã đủ hay chưa

Lý do chọn hướng này:

- bám sát lưu đồ hiện tại
- tránh làm dư hơn so với yêu cầu thực tế
- giữ `Bước 1` là bước phát sinh nhu cầu, không biến thành bước điều phối

## 4. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_request_origin_group`
- `x_psm_0502_intake_minimum_ready`
- `x_psm_0502_intake_minimum_gap_reason`

### 4.1. `Request Origin Group`

Field này gom nguồn phát sinh thành 3 nhóm dễ hiểu hơn về mặt nghiệp vụ:

- `Store Need`
- `Preventive Need`
- `System Need`

Ý nghĩa:

- không thay thế `Source System`
- mà là lớp phân nhóm nghiệp vụ dễ đọc hơn cho người dùng

### 4.2. `Intake Minimum Ready`

Field này cho biết:

- request ở thời điểm đầu vào đã đủ bộ dữ liệu tối thiểu để được xem là đã ghi nhận cơ bản hay chưa

Đây là chỉ báo nhanh để người dùng biết:

- request đã đủ thông tin cơ bản ở đầu vào
- hay vẫn còn thiếu một số thành phần quan trọng

### 4.3. `Intake Minimum Gap Reason`

Field này giải thích rõ:

- đang còn thiếu field nào ở mức dữ liệu tối thiểu

Field này giúp tránh tình trạng:

- chỉ biết request chưa đủ dữ liệu
- nhưng không biết đang thiếu gì

## 5. Logic phân nhóm nguồn phát sinh

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm helper:

- `_psm_get_request_origin_group()`

Rule phân nhóm hiện tại:

- `Source System = preventive_cron`
  - `Request Origin Group = Preventive Need`
- `Source System = manual_request`
  - `Request Origin Group = Store Need`
- các source còn lại
  - `Request Origin Group = System Need`

Ý nghĩa:

- `manual_request` được xem là nhu cầu phát sinh trực tiếp từ store
- `preventive_cron` được xem là nhu cầu bảo trì định kỳ
- `helpdesk_ticket`, `imported_request`, `other` được gom vào nhóm hệ thống / upstream source

## 6. Logic xác định dữ liệu tối thiểu

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm helper:

- `_psm_get_intake_minimum_gap_labels()`

Rule hiện tại kiểm tra các thành phần tối thiểu sau:

- `Request Title`
- `Request Source`
- `Source System`
- `Source Reference` nếu `Source System` thuộc:
  - `helpdesk_ticket`
  - `imported_request`

Nếu thiếu một trong các thành phần trên:

- `Intake Minimum Ready = False`
- `Intake Minimum Gap Reason` sẽ liệt kê các nhãn đang thiếu

Nếu đủ:

- `Intake Minimum Ready = True`
- `Intake Minimum Gap Reason` rỗng

## 7. Các compute mới đã thêm

Đã thêm các compute sau trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py):

- `_compute_x_psm_0502_request_origin_group()`
- `_compute_x_psm_0502_intake_minimum_ready_fields()`

Ý nghĩa:

- `Request Origin Group` luôn đồng bộ theo `Source System`
- `Intake Minimum Ready` và `Intake Minimum Gap Reason` luôn đồng bộ theo dữ liệu đầu vào hiện tại

## 8. Thay đổi trên giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã cập nhật:

### Form view

- hiển thị thêm:
  - `Request Origin Group`
  - `Intake Minimum Ready`
- trong tab `Notes`, phần source note được bổ sung:
  - `Intake Minimum Gap Reason`

Ý nghĩa:

- người dùng nhìn form sẽ biết ngay request thuộc nhóm nguồn nào
- đồng thời biết request còn thiếu dữ liệu tối thiểu gì hay không

### List view

- thêm cột optional:
  - `Request Origin Group`
  - `Intake Minimum Ready`

### Search view

- thêm field search:
  - `Request Origin Group`
  - `Intake Minimum Ready`
- thêm filter:
  - `Store Need`
  - `Preventive Need`
  - `System Need`
  - `Intake Minimum Ready`
  - `Intake Minimum Gap`
- thêm group by:
  - `Request Origin Group`

## 9. Những gì bước này cố ý không làm

Để tránh làm dư hơn so với lưu đồ hiện tại, `Phase 3 - Bước 1` chưa làm:

- queue intake riêng
- SLA intake riêng
- activity intake riêng
- escalation theo tuổi request
- assignment ownership ở bước phát sinh nhu cầu

Các phần trên, nếu cần, nên xem là phạm vi của:

- `Bước 3`
- `Bước 7`
- hoặc các bước monitoring / SLA sâu hơn của `Phase 3`

## 10. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 1` rõ hơn ở hai câu hỏi:

1. Nhu cầu này phát sinh từ nhóm nào?
- store
- preventive
- hay hệ thống khác

2. Ở mức dữ liệu đầu vào tối thiểu, request đã đủ chưa?
- nếu chưa, đang thiếu gì

Điều này giúp:

- bám sát lưu đồ thật
- chuẩn hóa đầu vào sớm hơn
- không làm workflow nặng hơn nhu cầu thực tế

## 11. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 12. Cách test

1. Upgrade `M02_P0502`.
2. Mở `maintenance.request`.
3. Tạo hoặc mở các request theo các source khác nhau.
4. Kiểm tra:
- `manual_request` -> `Request Origin Group = Store Need`
- `preventive_cron` -> `Request Origin Group = Preventive Need`
- `helpdesk_ticket` / `imported_request` -> `Request Origin Group = System Need`
5. Test thiếu dữ liệu:
- bỏ trống `Request Source` hoặc `Source System`
- kỳ vọng `Intake Minimum Ready = False`
- kỳ vọng `Intake Minimum Gap Reason` hiển thị rõ field còn thiếu
6. Test với `helpdesk_ticket` hoặc `imported_request` không có `Source Reference`:
- kỳ vọng `Intake Minimum Ready = False`
- kỳ vọng `Intake Minimum Gap Reason` có `Source Reference`

## 13. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
