# Daily Report - 2026-04-29

## 1. Phạm vi làm việc trong ngày

Hôm nay tập trung hoàn tất phần cuối của `Phase 1` cho quy trình `0502 - Quản lý bảo trì`, chủ yếu từ:

- `Bước 17`
- `Bước 18`
- `Bước 19`
- `Bước 20`
- `Bước 21`

Đồng thời xử lý thêm các vấn đề phát sinh khi test thực tế nhánh:

- duyệt vật tư
- xuất kho
- mua ngoài
- thực thi FSM
- nghiệm thu kết thúc request

## 2. Tài liệu định hướng đã dùng

Trong quá trình làm việc hôm nay, đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thật
- trong ngày đã tiếp tục bổ sung logic ở `maintenance.request`, `purchase.order`, `project.task`, `maintenance_team` và các view liên quan
- khi phân tích và sửa code, đã ưu tiên dùng source code thật để xác nhận cuối cùng

## 3. Những gì đã triển khai trong ngày

### 3.1. Phase 1 - Bước 17

Đã triển khai bước duyệt vật tư nội bộ trên `maintenance.request`:

- thêm trạng thái duyệt vật tư:
  - `Pending Approval`
  - `Approved`
  - `Rejected`
- thêm các action:
  - `Submit Material Approval`
  - `Approve Material Request`
  - `Reject Material Request`
- lưu lại:
  - người quyết định
  - thời điểm quyết định
  - ghi chú duyệt

Mục tiêu của bước này:

- tạo điểm duyệt tối thiểu cho nhánh vật tư nội bộ
- chưa tách sang module `approval`

### 3.2. Phase 1 - Bước 18

Đã triển khai bước xác nhận xuất kho thực tế:

- tận dụng flow chuẩn `button_validate()` của `stock.picking`
- thêm dấu vết trên request:
  - `Stock Issued By`
  - `Stock Issued At`
- thêm các action:
  - `Validate Stock Picking`
  - `Mark Stock Issued`

Đồng thời đã xử lý bug runtime quan trọng:

- code cũ dùng `move_ids_without_package`
- nhưng trong Odoo 19 local phải dùng `move_ids`

Ngoài ra đã tinh chỉnh UX:

- ẩn `Check Stock Availability` sau khi picking đã `done` hoặc `cancel`
- ẩn `Stock Availability` và `Stock Availability State` khi picking đã `done`

### 3.3. Phase 1 - Bước 19

Đã triển khai nhánh mua ngoài khi kho không đủ vật tư:

- bổ sung dependency:
  - `purchase`
  - `purchase_stock`
- kế thừa `purchase.order`
- thêm liên kết giữa `purchase.order` và `maintenance.request`
- thêm các action:
  - `Create Purchase Order`
  - `Open Purchase Order`

Mục tiêu:

- mở RFQ/PO chuẩn của Odoo từ request 0502
- không xây requisition riêng trong `Phase 1`

### 3.4. Phase 1 - Bước 20

Đã triển khai bước theo dõi thực thi sửa chữa dựa trên `FSM Task`:

- thêm các field execution trên `maintenance.request`:
  - `FSM Stage`
  - `FSM Task Closed`
  - `Execution Started By / At`
  - `Execution Completed By / At`
  - `Execution Note`
- thêm các action:
  - `Mark Execution Started`
  - `Mark Execution Completed`

Hướng triển khai đã giữ đúng plan:

- `FSM Task` là object thực thi chính
- `maintenance.request` chỉ giữ dấu vết tổng hợp

### 3.5. Phase 1 - Bước 21

Đã triển khai bước nghiệm thu kết thúc request:

- thêm các field:
  - `Acceptance Result`
  - `Acceptance Note`
  - `Acceptance Reviewed By`
  - `Acceptance Reviewed At`
- thêm action:
  - `Mark Acceptance Reviewed`

Logic kết thúc:

- nếu `Accepted`:
  - request chuyển sang stage done chuẩn của `maintenance`
  - `close_date` chuẩn được dùng luôn
- nếu `Follow-up Needed`:
  - request vẫn mở
  - `kanban_state = blocked`

## 4. Các vấn đề và điều chỉnh đã xử lý trong ngày

### 4.1. Đồng bộ logic kiểm tồn ở bước 16

Trong lúc test liên thông với bước 17-18, đã phát hiện:

- `Stock Check Result` custom của 0502
- và `Stock Availability` chuẩn của `stock.picking`

có lúc không nhất quán.

Đã sửa theo hướng:

- `Stock Check Result` bám theo compute chuẩn của `stock.picking`
- không còn coi `picking.state = assigned` là đủ để kết luận `available`

### 4.2. Làm rõ flow test bước 19 trên thực tế

Trong quá trình test request nhánh `Stock Not Available`, đã làm rõ:

- bước 19 chỉ chịu trách nhiệm mở/tạo RFQ/PO
- sau khi PO được confirm và receipt hoàn tất, vật tư được xem là đã về kho theo flow chuẩn của `purchase_stock`

### 4.3. Làm sạch dữ liệu hiển thị cho bước 20

Khi test `FSM Task`, đã rà lại cách đóng task:

- task phải được đưa sang `Done` thật trên form FSM
- sau đó request mới `Mark Execution Completed`

Điều này giúp:

- `FSM Stage`
- `FSM Task Closed`
- `Execution Completed By / At`

trên request phản ánh đúng trạng thái thực tế hơn

## 5. Hỗ trợ giải thích nghiệp vụ và thao tác test

Ngoài phần code, hôm nay cũng đã giải thích thêm cho người dùng:

- ý nghĩa của form `purchase.order` ở bước 19
- cách nhận biết vật tư đã vào kho
- cách dùng `FSM Task` để đi hết bước 20
- ý nghĩa của `Execution Note`
- ý nghĩa của tab `Acceptance`

Mục tiêu:

- giúp việc test end-to-end bám sát nghiệp vụ hơn
- không chỉ dừng ở mức “code chạy”

## 6. Kết quả hiện tại đến cuối ngày

Đến cuối ngày làm việc:

- `Phase 1 - Bước 17` đã triển khai xong
- `Phase 1 - Bước 18` đã triển khai xong
- `Phase 1 - Bước 19` đã triển khai xong
- `Phase 1 - Bước 20` đã triển khai xong
- `Phase 1 - Bước 21` đã triển khai xong

Như vậy:

- toàn bộ `Phase 1` từ `Bước 1` đến `Bước 21` đã hoàn tất
- nhánh nội bộ, nhánh kho, nhánh mua ngoài, nhánh thực thi và nhánh nghiệm thu đều đã có lớp triển khai tối thiểu chạy xuyên suốt

## 7. Kiểm tra kỹ thuật đã làm

Trong ngày đã thực hiện các kiểm tra kỹ thuật mức nhẹ:

- compile Python cho các model đã sửa
- parse XML cho các file view đã sửa

Kết quả:

- không phát hiện lỗi cú pháp sau khi hoàn tất từng bước

## 8. Danh sách note đã tạo trong ngày

- `phase_1_buoc_17_da_trien_khai.md`
- `phase_1_buoc_18_da_trien_khai.md`
- `phase_1_buoc_19_da_trien_khai.md`
- `phase_1_buoc_20_da_trien_khai.md`
- `phase_1_buoc_21_da_trien_khai.md`

## 9. Việc tiếp theo đề xuất

Bước hợp lý tiếp theo sau khi hoàn tất `Phase 1` là:

- tổng hợp lại phạm vi file đã triển khai của `Phase 1`
- rà lại dữ liệu mẫu và tài liệu test
- chuẩn bị plan chi tiết cho `Phase 2`

Trọng tâm tiếp theo nên là:

- chuẩn hóa intake
- siết queue/lead/planning
- tăng mức structured data cho inspection, proposal và monitoring
