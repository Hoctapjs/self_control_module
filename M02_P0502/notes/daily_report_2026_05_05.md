# Daily Report - 2026-05-05

## 1. Phạm vi làm việc trong ngày

Hôm nay tập trung triển khai `Phase 2` của quy trình `0502 - Quản lý bảo trì`, từ lớp chuẩn hóa dữ liệu đầu vào cho tới các bước cuối của nhánh thực thi và nghiệm thu.

Phạm vi thực tế đã chạm tới:

- `Phase 2 - Bước 1` đến `Phase 2 - Bước 21`
- các phần điều chỉnh phát sinh trong khi test:
  - ownership của `Bước 12`
  - giao diện `FSM Task` của `Bước 9`
  - validation và mapping ở nhánh vật tư / kho / mua ngoài

## 2. Tài liệu định hướng đã dùng

Trong suốt quá trình làm việc hôm nay, đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md`
- các note triển khai đã có của `Phase 1` và `Phase 2`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thật
- trong ngày đã bổ sung thêm khá nhiều field, helper, action và view cho `Phase 2`
- khi phân tích và sửa code, đã ưu tiên dùng source code thật để xác nhận cuối cùng

## 3. Những gì đã triển khai trong ngày

### 3.1. Cụm chuẩn hóa intake và nguồn phát sinh

Đã hoàn thiện lớp intake ban đầu cho `maintenance.request`:

- thêm metadata nguồn hệ thống:
  - `Source System`
  - `Source Reference`
  - `Source Mapping Note`
- chuẩn hóa validation intake:
  - `Store Department`
  - `Request Type`
  - `Request Source`
  - `Source Reference` cho các nguồn cần tham chiếu
- chuẩn hóa dấu vết tiếp nhận `CMT`:
  - chỉ auto receive cho `manual_request`
  - không auto cho:
    - `helpdesk_ticket`
    - `imported_request`
    - `preventive_cron`

Kết quả:

- request vào hệ thống rõ nguồn hơn
- giảm nhập thiếu dữ liệu ở bước đầu
- dấu vết tiếp nhận chặt nghiệp vụ hơn

### 3.2. Cụm kiểm tra ban đầu, preventive và queue điều phối

Đã nâng phần đầu luồng cho `CMT` và `CMT Lead`:

- bổ sung bộ field inspection có cấu trúc:
  - `Symptom Status`
  - `Equipment Status`
  - `Safety Risk Level`
  - `Action Urgency`
- siết logic preventive:
  - tránh sinh trùng preventive request
  - thêm `Preventive Status`
- cấu hình `0502 Lead User` trên `maintenance.team`
- chuẩn hóa logic notify lead và lưu `Lead Notify Rule`
- bổ sung queue / action / menu cho lead:
  - `0502 Requests To Plan`
  - `0502 Preventive Queue`
  - `0502 Store Action Needed`
  - `0502 Overdue Queue`
- thêm khái niệm `Ready To Plan` và `Planning Block Reason`

Kết quả:

- phân nhánh request rõ hơn ngay từ đầu
- lead có queue để gom việc và nhìn backlog
- request không còn được plan / tạo FSM task khi chưa đủ điều kiện

### 3.3. Cụm FSM task, monitoring và dữ liệu thực thi

Đã nâng lớp dữ liệu trên `project.task`:

- chuẩn hóa description mặc định khi tạo `FSM Task`
- đưa thêm metadata 0502 sang task:
  - `Source System`
  - `Initial Inspection Result`
  - `Proposal Summary`
- sửa layout giao diện `FSM Task`:
  - tách `0502 Context` thành tab riêng để tránh vỡ bố cục
- bổ sung monitoring / reporting cho request và execution:
  - `0502 Request Monitoring`
  - `0502 Preventive Monitoring`
  - `0502 Overdue Monitoring`
  - `0502 Follow-up Needed`
  - `0502 Execution Monitoring`
- ở `Bước 20`, tách rõ vai trò:
  - `FSM Task` giữ dữ liệu thực thi thật
  - `request` chỉ giữ summary

Đã thêm trên `FSM Task`:

- `0502 Execution Result`
- `0502 Execution Checklist`
- `0502 Technical Worksheet`
- `0502 Material Used Note`
- `0502 Actual Time Spent (Hours)`
- `0502 Follow-up Action Note`

Kết quả:

- task không còn chỉ là object đổi stage
- dữ liệu thực thi thực tế đã có chỗ chuẩn để ghi
- request chỉ nhận summary khi hoàn tất

### 3.4. Cụm proposal và approval

Đã chuẩn hóa nhánh đề xuất và duyệt:

- ở `Bước 11`:
  - tách `Treatment Proposal` thành các phần có cấu trúc:
    - `Root Cause Analysis`
    - `Technical Solution`
    - `Cost Note`
    - `Timeline Note`
  - giữ `Proposal Summary` để downstream flow tiếp tục dùng được
- ở `Bước 12`:
  - thêm rule resolve approver
  - thêm auto approve theo limit
  - siết `approve/reject` theo đúng approver đã resolve

Điều chỉnh quan trọng trong ngày:

- ban đầu approver của `Bước 12` đặt trên `maintenance.team`
- sau khi rà lại ownership nghiệp vụ, đã điều chỉnh để:
  - ưu tiên `Store Proposal Approver` trên `hr.department`
  - fallback về team nếu store chưa cấu hình

Kết quả:

- approval của proposal đúng ownership hơn
- vẫn giữ tương thích ngược với dữ liệu và cấu hình cũ

### 3.5. Cụm vật tư, kho và mua ngoài

Đây là cụm được đẩy mạnh nhất trong ngày.

#### `Bước 14` - Vật tư có cấu trúc

Đã thêm model dòng vật tư:

- `x_psm_request_material_line`

Mỗi request giờ có thể khai báo chi tiết:

- vật tư nào
- số lượng dự kiến
- UoM
- nguồn lấy dự kiến
- ghi chú dòng

#### `Bước 15` - Tạo `stock.picking` usable thật

Đã thêm cấu hình material flow trên `maintenance.team`:

- `0502 Material Picking Type`
- `0502 Material Source Location`
- `0502 Material Destination Location`

Đã sửa `Create Stock Picking` để:

- validate lại `Material Detail Lines`
- tự tạo `move_ids` từ các dòng vật tư đã khai
- gán source / destination location đúng theo rule resolve

#### `Bước 16` - Tách current availability và checked snapshot

Đã tách rõ:

- `Current Stock Availability`
- `Current Stock Availability State`
- `Checked Stock Availability`
- `Checked Stock Availability State`
- `Stock Check Result`

Kết quả:

- không còn trộn trạng thái live của picking với kết quả snapshot đã check

#### `Bước 17` - Approval vật tư nội bộ

Đã thêm:

- `Material Approver`
- `Material Auto Approve Limit`
- metadata approval vật tư
- auto/manual review theo:
  - tổng giá trị vật tư dự kiến
  - source type ngoại lệ như `External Purchase` / `Other`

#### `Bước 18` - Trạng thái nghiệp vụ xuất kho

Đã thêm:

- `Stock Issue Status`
- `Stock Issue Synced At`

Mục tiêu:

- không bắt user tự diễn giải state kỹ thuật của `stock.picking`
- request có thêm business status dễ đọc:
  - `No Stock Picking`
  - `Pending Stock Issue`
  - `Stock Issued`
  - `Stock Flow Cancelled`

#### `Bước 19` - Mua ngoài có prefill ngữ cảnh

Đã nâng `Create Purchase Order` từ mức mở form RFQ trống lên mức mở RFQ có dữ liệu sẵn:

- gợi ý `Default Vendor` từ `maintenance.team`
- build `order_line` từ `Material Detail Lines`
- build `summary note` từ ngữ cảnh request 0502
- bổ sung related field trên `purchase.order`:
  - `0502 Store Department`
  - `0502 Source System`

Kết quả:

- nhánh mua ngoài liền mạch hơn
- giảm nhập lại dữ liệu giữa request và RFQ/PO

### 3.6. Cụm nghiệm thu sau bảo trì

Đã nâng `Bước 21` từ acceptance nhẹ sang acceptance có cấu trúc hơn:

- mở rộng `Acceptance Result`:
  - `Accepted`
  - `Follow-up Needed`
  - `Rework Required`
- thêm:
  - `Store Acceptance Contact`
  - `Store Acceptance Role`
  - `Post-Maintenance Equipment Result`
  - `Acceptance Follow-up Note`
- siết validation khi bấm `Mark Acceptance Reviewed`

Kết quả:

- bước nghiệm thu rõ người, rõ kết quả, rõ follow-up hơn
- phân biệt được:
  - đạt
  - cần theo dõi
  - cần xử lý lại

## 4. Các lỗi / vấn đề đã xử lý trong ngày

### 4.1. `Source Mapping Note` nhìn như text rời, khó phân biệt

Đã xử lý bằng cách:

- đổi label cho rõ hơn
- gom lại trong cụm `Source Metadata`

Kết quả:

- user nhìn form không còn nhầm với ghi chú nghiệp vụ chung

### 4.2. `Preventive Status` không searchable trong search view

Nguyên nhân:

- field computed chưa `store=True`

Đã xử lý:

- thêm `store=True` cho:
  - `x_psm_0502_preventive_status`
  - `x_psm_0502_has_open_preventive_request`

### 4.3. Giao diện `FSM Task` bị vỡ ở cụm `0502 Context`

Nguyên nhân:

- cụm context đặt ở cột phải hẹp

Đã xử lý:

- chuyển `0502 Context` sang tab riêng

### 4.4. `Mark Proposed` bị ẩn sai sau khi chuyển proposal sang dạng structured

Nguyên nhân:

- điều kiện hiển thị nút vẫn bám field summary cũ

Đã xử lý:

- đổi điều kiện hiển thị sang bộ field structured thật của `Bước 11`

### 4.5. Tạo `stock.move` bị lỗi `Invalid field 'name' on model 'stock.move'`

Nguyên nhân:

- payload tạo `move_ids` đang gửi field `name`

Đã xử lý:

- bỏ `name`
- dùng:
  - `origin`
  - `description_picking_manual`

### 4.6. Ownership approval của `Bước 12` chưa đúng

Nguyên nhân:

- rule ban đầu coi `maintenance.team` là chủ thể approver chính
- trong nghiệp vụ thực tế, `store` mới là bên duyệt proposal

Đã xử lý:

- thêm approver trên `hr.department`
- đổi resolve order để ưu tiên approver phía store
- vẫn giữ fallback về team để không làm gãy flow cũ

## 5. Kết quả hiện tại đến cuối ngày

Đến cuối ngày, source code của module đã phản ánh:

- `Phase 2 - Bước 1` đến `Phase 2 - Bước 21` đã có lớp triển khai trong source
- các cụm lớn đã được đẩy qua:
  - intake
  - inspection
  - preventive
  - lead queue / planning
  - FSM task
  - proposal / approval
  - vật tư / kho / mua ngoài
  - execution
  - acceptance

Lưu ý về tài liệu:

- note triển khai theo bước hiện đã có rõ ràng tới:
  - `phase_2_buoc_17_da_trien_khai.md`
- các bước `18` đến `21` tại thời điểm chốt report này:
  - source đã có
  - nhưng note theo bước chưa tách đầy đủ thành file riêng

## 6. Kiểm tra kỹ thuật đã làm

Trong ngày đã thực hiện lặp lại nhiều lượt kiểm tra kỹ thuật mức nhẹ:

- compile Python cho các model đã sửa
- parse XML cho các view đã sửa bằng parser chuẩn Python

Kết quả:

- không phát hiện lỗi cú pháp ở các file đã được chốt lại sau từng lượt sửa

## 7. Danh sách note / tài liệu đã tạo hoặc cập nhật trong ngày

Đã tạo hoặc cập nhật các tài liệu của `Phase 2`:

- `phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md`
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
- `phase_2_buoc_14_da_trien_khai.md`
- `phase_2_buoc_15_da_trien_khai.md`
- `phase_2_buoc_16_da_trien_khai.md`
- `phase_2_buoc_17_da_trien_khai.md`

## 8. Việc tiếp theo đề xuất

Các việc nên làm tiếp sau report này:

- tách note triển khai riêng cho:
  - `Phase 2 - Bước 18`
  - `Phase 2 - Bước 19`
  - `Phase 2 - Bước 20`
  - `Phase 2 - Bước 21`
- regenerate lại `structure/module_map.json`
- chạy test end-to-end theo các nhánh chính:
  - preventive
  - store request nội bộ có vật tư
  - store request thiếu tồn dẫn tới mua ngoài
- rà lại reporting / queue để chắc UI vẫn nhất quán sau tất cả các thay đổi của `Phase 2`

## 9. Kết luận ngắn

Ngày 05/05 là ngày đẩy mạnh `Phase 2` trên diện rộng.

Kết quả lớn nhất không chỉ là thêm field hay nút, mà là:

- chuẩn hóa ranh giới dữ liệu giữa các object
- nối mạch request với FSM / stock / purchase rõ hơn
- siết validation ở các decision point quan trọng
- chuyển nhiều bước từ “ghi chú nhẹ” sang “dữ liệu có cấu trúc”

Điều này giúp `M02_P0502` tiến từ mức chạy được flow sang mức có nền tảng dữ liệu tốt hơn để vận hành, báo cáo và kiểm soát nghiệp vụ.
