# Daily Report - 2026-05-04

## 1. Phạm vi làm việc trong ngày

Hôm qua tập trung triển khai `Phase 2` của quy trình `0502 - Quản lý bảo trì`, chủ yếu từ:

- `Bước 1`
- `Bước 2`
- `Bước 3`
- `Bước 4`
- `Bước 5`
- `Bước 6`
- `Bước 7`
- `Bước 8`
- `Bước 9`
- `Bước 10`
- `Bước 11`
- `Bước 12`

Đồng thời xử lý thêm một số điều chỉnh về nghiệp vụ intake, preventive, queue cho CMT Lead, monitoring, proposal và approval.

## 2. Tài liệu định hướng đã dùng

Trong quá trình làm việc, đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thật
- trong quá trình triển khai `Phase 2`, source code đã tiếp tục thay đổi nhưng JSON map chưa được regenerate lại
- khi phân tích và sửa code, đã ưu tiên dùng source code thật để xác nhận cuối cùng

## 3. Những gì đã triển khai trong ngày

### 3.1. Phase 2 - Bước 1

Đã bổ sung metadata nguồn phát sinh request trên `maintenance.request`:

- `Source System`
- `Source Reference`
- `Source Mapping Note`

Đã cập nhật logic preventive request để tự ghi metadata nguồn hệ thống:

- `Source System = Preventive Cron`
- `Source Reference = tên thiết bị`

Ý nghĩa:

- tách rõ `nguồn nghiệp vụ`
- và `nguồn hệ thống/upstream`

### 3.2. Phase 2 - Bước 2

Đã chuẩn hóa validation intake đầu vào trên `maintenance.request`:

- bắt buộc:
  - `Store Department`
  - `Request Type`
  - `Request Source`
- bắt buộc thêm `Source Reference` nếu nguồn hệ thống là:
  - `Helpdesk Ticket`
  - `Imported Request`

Validation được áp dụng ở:

- `create()`
- `write()`

### 3.3. Phase 2 - Bước 3

Đã tinh chỉnh logic tiếp nhận request theo hướng nghiệp vụ chặt hơn:

- chỉ auto receive cho:
  - `manual_request`
- không auto receive cho:
  - `helpdesk_ticket`
  - `imported_request`
  - `preventive_cron`

Đồng thời đổi nhãn để làm rõ đây là dấu vết của `CMT`:

- `Received By (CMT)`
- `Received At (CMT)`

### 3.4. Phase 2 - Bước 4

Đã chuyển phần kiểm tra ban đầu sang bộ field có cấu trúc:

- `Symptom Status`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`

Và siết lại `Mark Inspected`:

- không cho đi tiếp nếu thiếu các field kiểm tra có cấu trúc

### 3.5. Phase 2 - Bước 5

Đã chuẩn hóa preventive status trên `maintenance.equipment` và siết logic cron preventive:

- `Not Enabled`
- `Missing Next Date`
- `Scheduled`
- `Due to Generate`
- `Open Preventive Request`

Logic mới:

- nếu còn preventive request đang mở:
  - cron không sinh request mới
  - không đẩy `next_preventive_date` sang kỳ sau
- chỉ sinh request mới khi:
  - đến hạn
  - không còn preventive request mở

### 3.6. Phase 2 - Bước 6

Đã chuẩn hóa rule xác định `CMT Lead`:

- thêm `0502 Lead User` trên `maintenance.team`
- ưu tiên resolve lead từ cấu hình team
- fallback lần lượt:
  - team member đầu tiên
  - technician
  - current user

Đã ghi thêm dấu vết:

- `Lead Notify Rule`

### 3.7. Phase 2 - Bước 7

Đã bổ sung các queue cho `CMT Lead`:

- `0502 Requests To Plan`
- `0502 Preventive Queue`
- `0502 Store Action Needed`
- `0502 Overdue Queue`

Mục tiêu:

- giúp lead tiếp nhận lịch
- gom việc cần lên kế hoạch
- nhìn được request tồn và quá hạn

### 3.8. Phase 2 - Bước 8

Đã thêm logic `Ready To Plan` và `Planning Block Reason` trên `maintenance.request`.

Đã thống nhất rule planning:

- preventive:
  - phải được `Notify CMT Lead`
  - và đủ bộ field intake
- request thường:
  - phải `CMT Receive`
  - đã `Initial Inspection`
  - `Inspection Result = Action Needed`
  - và đủ bộ field intake

Đã đồng bộ validation giữa:

- `Mark Planned`
- `Create FSM Task`

### 3.9. Phase 2 - Bước 9

Đã chuẩn hóa dữ liệu context khi tạo `FSM Task`:

- description mặc định tự gom context từ request 0502
- thêm metadata related trên `project.task`
- form FSM hiển thị cụm `0502 Context`

Thông tin được đưa vào task gồm:

- nguồn request
- inspection result
- proposal summary
- planning note

### 3.10. Phase 2 - Bước 10

Đã bổ sung các màn hình monitoring cho `maintenance.request`:

- `0502 Request Monitoring`
- `0502 Preventive Monitoring`
- `0502 Overdue Monitoring`
- `0502 Follow-up Needed`

Mục tiêu:

- giúp lead nhìn open backlog
- tách riêng preventive
- theo dõi overdue
- theo dõi request cần follow-up sau nghiệm thu

### 3.11. Phase 2 - Bước 11

Đã tách `Treatment Proposal` thành bộ field structured:

- `Root Cause Analysis`
- `Technical Solution`
- `Cost Note`
- `Timeline Note`

Đã giữ `Treatment Proposal` summary để không làm vỡ các bước sau.

Khi bấm `Mark Proposed`, hệ thống sẽ:

- kiểm tra các field bắt buộc
- tự build lại `Proposal Summary`

### 3.12. Phase 2 - Bước 12

Đã nâng approval proposal lên mức có rule rõ ràng, nhưng vẫn giữ scope nhẹ:

- chưa kéo `approval` module thật vào
- vẫn dùng approval custom trên `maintenance.request`

Đã thêm cấu hình trên `maintenance.team`:

- `0502 Proposal Approver`
- `0502 Auto Approve Limit`

Đã thêm metadata approval trên request:

- `Approval Required`
- `Proposal Approver`
- `Approval Rule`
- `Approval Cost Rule`

Logic mới:

- nếu `Estimated Cost` nhỏ hơn hoặc bằng ngưỡng team:
  - request auto approved
- nếu vượt ngưỡng:
  - request vào `Pending Approval`
- chỉ đúng `Proposal Approver` đã resolve mới được approve/reject

## 4. Các quyết định nghiệp vụ và điều chỉnh quan trọng trong ngày

### 4.1. Giữ `Source System` ở dạng `Selection`

Sau khi xem xét, đã quyết định:

- chưa đổi `x_psm_0502_source_system` sang `Many2one`

Lý do:

- tập giá trị hiện tại còn nhỏ và ổn định
- đây là metadata kỹ thuật
- chưa cần master data riêng để cấu hình động

### 4.2. Làm rõ `Source Mapping Note`

Đã tinh chỉnh UX để tránh nhầm `Source Mapping Note` với ghi chú chung:

- thêm cụm `Source Metadata`
- đổi label để người dùng hiểu đây là ghi chú về nguồn phát sinh request

### 4.3. Siết lại auto receive theo đúng nghiệp vụ hơn

Ban đầu auto receive áp dụng cho nhiều source system hơn.

Sau khi đánh giá nghiệp vụ, đã chỉnh lại:

- chỉ `manual_request` mới auto receive

Đây là thay đổi quan trọng để tránh hiểu nhầm:

- người tạo request
- và người thực sự tiếp nhận request

### 4.4. Xử lý vấn đề searchable field ở preventive status

Trong lúc hoàn thiện `Phase 2 - Bước 5`, đã gặp lỗi:

- computed field không searchable trong filter domain

Đã sửa bằng cách:

- thêm `store=True` cho các field preventive status liên quan

## 5. Kết quả hiện tại đến cuối ngày

Đến cuối ngày 2026-05-04:

- `Phase 2 - Bước 1` đã triển khai xong
- `Phase 2 - Bước 2` đã triển khai xong
- `Phase 2 - Bước 3` đã triển khai xong
- `Phase 2 - Bước 4` đã triển khai xong
- `Phase 2 - Bước 5` đã triển khai xong
- `Phase 2 - Bước 6` đã triển khai xong
- `Phase 2 - Bước 7` đã triển khai xong
- `Phase 2 - Bước 8` đã triển khai xong
- `Phase 2 - Bước 9` đã triển khai xong
- `Phase 2 - Bước 10` đã triển khai xong
- `Phase 2 - Bước 11` đã triển khai xong
- `Phase 2 - Bước 12` đã triển khai xong

Toàn bộ phần triển khai trong ngày vẫn giữ đúng nguyên tắc:

- ưu tiên tận dụng model gốc Odoo
- mở rộng nhẹ trên model chuẩn
- hạn chế tạo thêm object mới nếu chưa cần

## 6. Kiểm tra kỹ thuật đã làm

Trong ngày đã thực hiện các kiểm tra kỹ thuật mức nhẹ:

- compile Python cho các model đã sửa
- parse XML cho các view đã sửa

Kết quả:

- không phát hiện lỗi cú pháp ở các file đã triển khai sau khi hoàn tất từng bước

## 7. Danh sách note đã tạo trong ngày

- `phase_2_buoc_1_da_trien_khai.md`
- `phase_2_buoc_2_da_trien_khai.md`
- `phase_2_buoc_3_da_trien_khai.md`
- `phase_2_buoc_4_da_trien_khai.md`
- `phase_2_buoc_5_da_trien_khai.md`
- `phase_2_buoc_6_da_trien_khai.md`
- `phase_2_buoc_7_da_trien_khai.md`
- `phase_2_buoc_8_da_trien_khai.md`
- `phase_2_buoc_9_da_trien_khai.md`
- `phase_2_buoc_10_da_trien_khai.md`
- `phase_2_buoc_11_da_trien_khai.md`
- `phase_2_buoc_12_da_trien_khai.md`

## 8. Việc tiếp theo đề xuất

Bước hợp lý tiếp theo là:

- triển khai `Phase 2 - Bước 13`

Trọng tâm đề xuất:

- tiếp tục siết rule của nhánh service assessment
- làm rõ hơn tiêu chí nội bộ hay thuê ngoài
- đồng bộ tiếp với các bước vật tư và approval phía sau
