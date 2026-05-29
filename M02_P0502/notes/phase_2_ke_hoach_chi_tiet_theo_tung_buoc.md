## 1. Mục tiêu của Phase 2

`Phase 2` không còn tập trung vào việc “làm cho luồng chạy được” như `Phase 1`.

Mục tiêu của phase này là:

- làm mượt các điểm đứt giữa các module chuẩn Odoo
- giảm thao tác tay và giảm trạng thái “ghi nhận tối thiểu”
- làm cho các bước gần hơn với lưu đồ nghiệp vụ thực tế của `0502`
- chuẩn hóa dữ liệu, liên kết object, approval, biểu mẫu và điểm kiểm soát
- giữ nguyên nguyên tắc: ưu tiên tận dụng chuẩn Odoo trước, chỉ custom khi thật sự tạo ra giá trị rõ ràng

## 2. Nguồn dùng để lập plan

Khi lập plan cho tài liệu này, đã dùng:

- convention:
  - [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)
- structure map:
  - [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)
- tài liệu phase:
  - [plan_trien_khai_0502_theo_phase.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/plan_trien_khai_0502_theo_phase.md)
  - [phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md)
  - [phase_1_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_da_trien_khai.md)
- source xác nhận chính:
  - [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
  - [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
  - [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
  - [models/project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
  - [models/stock_picking.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/stock_picking.py)
  - [models/purchase_order.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/purchase_order.py)

Lưu ý:

- `module_map.json` hiện cũ hơn source code thực tế.
- Source hiện tại được xem là chuẩn xác nhận cuối cùng.

## 3. Những gì Phase 1 đã có và không nên làm lại

Sau `Phase 1`, module đã có:

- luồng `21 bước` chạy được end-to-end ở mức tối thiểu
- object trung tâm là `maintenance.request`
- liên kết được với:
  - `maintenance.equipment`
  - `project.task` kiểu FSM
  - `stock.picking`
  - `purchase.order`
- các điểm duyệt, kiểm tra, nghiệm thu đã có ở mức field/action cơ bản
- các note theo từng bước đã đủ để dùng làm đầu vào refinement

Vì vậy `Phase 2` không nên:

- làm lại toàn bộ `Phase 1`
- thay trục chính khỏi `maintenance.request` quá sớm
- tạo workflow engine mới nếu chưa chứng minh được chuẩn + custom nhẹ là không đủ

## 4. Trọng tâm của Phase 2

`Phase 2` nên tập trung vào 5 nhóm việc:

### 4.1. Chuẩn hóa object mapping

- làm rõ quan hệ giữa:
  - `maintenance.request`
  - `project.task`
  - `stock.picking`
  - `purchase.order`
- giảm tình trạng một bước chỉ “ghi dấu vết” mà chưa phản ánh được object vận hành thật

### 4.2. Chuyển approval từ mức nhẹ sang mức có cấu trúc hơn

- approval timeline/cost
- approval vật tư
- vai trò người duyệt
- điều kiện duyệt theo trạng thái request

### 4.3. Làm mượt nhánh kho và mua ngoài

- từ “có phiếu” sang “phiếu có nội dung usable”
- từ “mở form PO” sang “RFQ/PO có cấu trúc chuẩn hơn”
- giảm bước thao tác tay khi chuyển giữa `maintenance`, `stock`, `purchase`

### 4.4. Bổ sung biểu mẫu và dữ liệu vận hành

- biên bản kiểm tra
- đề xuất xử lý
- nghiệm thu
- ghi chú thực thi có cấu trúc hơn

### 4.5. Báo cáo và màn hình điều phối

- dashboard / queue phục vụ vai trò
- report theo tình trạng xử lý
- report theo thiết bị, cửa hàng, vật tư, vendor, lead time

## 5. Nguyên tắc triển khai cho Phase 2

Khi đi vào từng bước, luôn trả lời 5 câu hỏi:

1. Điểm đứt của `Phase 1` ở bước này là gì
2. Có thể xử lý bằng chuẩn Odoo tốt hơn không
3. Nếu phải custom, custom đó là nhẹ hay vừa
4. Có làm tăng số object mới không
5. Có tạo ra lợi ích rõ cho user thao tác hằng ngày không

Nguyên tắc kỹ thuật:

- ưu tiên cải thiện object đã có thay vì tạo object thay thế
- ưu tiên compute/related/action/wizard trước khi tạo model mới
- nếu có approval thật, cân nhắc dùng module `approval` theo đúng convention
- nếu có biểu mẫu đánh giá/nghiệm thu có cấu trúc, ưu tiên `maintenance_worksheet` hoặc object chuẩn gần nhất trước khi tạo mẫu riêng

## 6. Kế hoạch chi tiết theo từng bước cho Phase 2

## Bước 1 - Phát sinh nhu cầu bảo trì

### Trọng tâm Phase 2

- xem có cần bổ sung entry point từ `helpdesk` hay không
- nếu có nhiều nguồn phát sinh thực tế, chuẩn hóa cách map nguồn vào `maintenance.request`

### Hướng triển khai

- giữ `maintenance.request` là điểm nhận chính
- chỉ bổ sung mapping nếu user thật sự cần:
  - ticket -> maintenance request
  - request định kỳ -> maintenance request

### Custom dự kiến

- custom nhẹ

## Bước 2 - Tạo phiếu yêu cầu bảo trì

### Trọng tâm Phase 2

- chuẩn hóa bộ field đầu vào
- giảm tạo request thiếu thông tin

### Hướng triển khai

- rà lại field bắt buộc
- xem có cần tách nhóm field theo:
  - cửa hàng
  - thiết bị
  - loại yêu cầu
  - mức độ ưu tiên

### Custom dự kiến

- custom nhẹ ở view và validation

## Bước 3 - CMT tiếp nhận yêu cầu

### Trọng tâm Phase 2

- giảm thao tác “bấm nút để ghi dấu vết”
- làm rõ vai trò nào được tiếp nhận

### Hướng triển khai

- rà lại có nên tự động set `received_by/received_at` khi request vào queue tiếp nhận
- xem có cần activity bắt buộc cho người tiếp nhận

### Custom dự kiến

- custom nhẹ

## Bước 4 - Kiểm tra thực tế ban đầu

### Trọng tâm Phase 2

- chuyển từ note rời sang form kiểm tra có cấu trúc

### Hướng triển khai

- đánh giá dùng `maintenance_worksheet`
- nếu không đủ, tạo checklist/wizard kiểm tra ban đầu

### Custom dự kiến

- custom vừa

## Bước 5 - Kiểm tra lịch bảo trì định kỳ

### Trọng tâm Phase 2

- làm chắc logic preventive
- giảm rủi ro sinh trùng

### Hướng triển khai

- bổ sung rule rõ hơn cho:
  - request nào được xem là preventive open
  - khi nào được sinh đợt mới
- review cron và test boundary theo ngày

### Custom dự kiến

- custom nhẹ

## Bước 6 - Gửi lịch cho CMT Lead

### Trọng tâm Phase 2

- chuẩn hóa người nhận notify
- làm rõ rule notify theo team/store

### Hướng triển khai

- xem có nên chuyển sang activity template chuẩn hơn
- xem có nên cấu hình lead trên team thay vì fallback nhiều tầng

### Custom dự kiến

- custom nhẹ

## Bước 7 - CMT Lead tổng hợp yêu cầu

### Trọng tâm Phase 2

- thay queue cơ bản bằng queue usable theo vai trò

### Hướng triển khai

- refine action/menu queue
- thêm search preset theo:
  - preventive
  - store request
  - action needed
  - overdue

### Custom dự kiến

- custom nhẹ

## Bước 8 - Lập kế hoạch bảo trì

### Trọng tâm Phase 2

- quyết định có cần `planning` thật hay không

### Hướng triển khai

- nếu nhu cầu phân ca mạnh:
  - cân nhắc tích hợp `planning`
- nếu chưa:
  - tiếp tục dùng request + FSM task nhưng siết validation tốt hơn

### Custom dự kiến

- custom nhẹ hoặc vừa, tùy có kéo `planning` vào không

## Bước 9 - Điều phối nhân viên bảo trì

### Trọng tâm Phase 2

- làm mượt việc tạo FSM task
- giảm phụ thuộc vào thao tác bổ sung thủ công

### Hướng triển khai

- chuẩn hóa description mặc định của FSM task
- map thêm dữ liệu từ request sang task:
  - request type
  - inspection result
  - proposal summary
- xem có cần activity/task template

### Custom dự kiến

- custom nhẹ

## Bước 10 - Theo dõi tình trạng xử lý

### Trọng tâm Phase 2

- từ monitoring cơ bản sang dashboard usable hơn

### Hướng triển khai

- bổ sung action/report theo vai trò
- cân nhắc pivot/graph preset
- thêm KPI tối thiểu:
  - số request mở
  - số overdue
  - số preventive
  - số follow-up needed

### Custom dự kiến

- custom nhẹ đến vừa

## Bước 11 - Đề xuất phương án xử lý / báo giá sơ bộ

### Trọng tâm Phase 2

- chuẩn hóa đề xuất xử lý
- tách rõ nội dung kỹ thuật và nội dung chi phí

### Hướng triển khai

- thêm cấu trúc cho:
  - nguyên nhân
  - phương án
  - chi phí
  - timeline
- cân nhắc dùng worksheet hoặc wizard thay vì chỉ text field

### Custom dự kiến

- custom vừa

## Bước 12 - Duyệt timeline và cost

### Trọng tâm Phase 2

- quyết định có dùng `approval` thật hay không

### Hướng triển khai

- nếu nghiệp vụ đã rõ:
  - chuyển từ approval nhẹ trên request sang `approval`
- xác định:
  - ai duyệt
  - 1 cấp hay nhiều cấp
  - điều kiện duyệt theo cost

### Custom dự kiến

- custom vừa

## Bước 13 - Thẩm định có cần dịch vụ ngoài

### Trọng tâm Phase 2

- làm rõ nhánh outsource

### Hướng triển khai

- chuẩn hóa tiêu chí:
  - xử lý nội bộ
  - dịch vụ ngoài
- nếu outsource là scope lớn, chuẩn bị thiết kế object cho `Phase 3`

### Custom dự kiến

- custom nhẹ trong `Phase 2`
- custom sâu để `Phase 3`

## Bước 14 - Kiểm tra phát sinh vật tư

### Trọng tâm Phase 2

- chuyển từ boolean sang nội dung vật tư thực tế

### Hướng triển khai

- không chỉ hỏi `có/không`
- mà cần nêu:
  - vật tư nào
  - số lượng dự kiến
  - nguồn lấy

### Custom dự kiến

- custom vừa

## Bước 15 - Yêu cầu xuất kho vật tư

### Trọng tâm Phase 2

- làm cho `stock.picking` usable thật, không chỉ là “phiếu khung”

### Hướng triển khai

- chuẩn hóa operation type
- chuẩn hóa source/destination location
- xem có nên sinh sẵn move line từ nội dung vật tư phát sinh

### Custom dự kiến

- custom vừa

## Bước 16 - Kiểm tra tồn kho

### Trọng tâm Phase 2

- làm rõ tiêu chí “đủ tồn / không đủ tồn”
- giảm mâu thuẫn giữa field custom và compute chuẩn

### Hướng triển khai

- bám hoàn toàn vào compute chuẩn của `stock.picking`
- nếu cần, tách:
  - availability hiện tại
  - kết quả check tại thời điểm quyết định

### Custom dự kiến

- custom nhẹ

## Bước 17 - Duyệt yêu cầu vật tư

### Trọng tâm Phase 2

- đưa approval vật tư về đúng vai trò và rule

### Hướng triển khai

- làm rõ:
  - ai duyệt
  - duyệt theo giá trị hay theo loại vật tư
- cân nhắc dùng `approval` nếu rule đã đủ rõ

### Custom dự kiến

- custom vừa

## Bước 18 - Xuất kho thực tế

### Trọng tâm Phase 2

- đảm bảo request phản ánh đúng kết quả của flow kho chuẩn

### Hướng triển khai

- tối ưu UX quanh `Validate Stock Picking`
- cân nhắc tự đồng bộ trạng thái request sau khi picking `done`

### Custom dự kiến

- custom nhẹ

## Bước 19 - Mua ngoài khi thiếu vật tư

### Trọng tâm Phase 2

- từ “mở form PO” sang “quy trình mua ngoài usable hơn”

### Hướng triển khai

- chuẩn hóa dữ liệu RFQ:
  - vendor
  - origin
  - link về request/task
- xem có cần:
  - vendor suggestion
  - nhiều báo giá
  - requisition
- mặc định chưa kéo `purchase_requisition` nếu chưa có nhu cầu thật

### Custom dự kiến

- custom nhẹ đến vừa

## Bước 20 - Thực thi sửa chữa

### Trọng tâm Phase 2

- làm rõ ranh giới giữa dữ liệu trên request và dữ liệu trên FSM task

### Hướng triển khai

- request chỉ giữ summary
- FSM task giữ execution thực tế
- nếu cần, chuẩn hóa:
  - execution checklist
  - worksheet kỹ thuật
  - time spent
  - vật tư đã dùng

### Custom dự kiến

- custom vừa

## Bước 21 - Nghiệm thu sau bảo trì

### Trọng tâm Phase 2

- chuyển từ acceptance nhẹ sang biên bản nghiệm thu có cấu trúc hơn

### Hướng triển khai

- bổ sung mẫu nghiệm thu
- làm rõ người nghiệm thu
- làm rõ kết quả:
  - đạt
  - cần theo dõi
  - cần xử lý lại
- cân nhắc chữ ký/xác nhận nếu cần

### Custom dự kiến

- custom vừa

## 7. Các cụm ưu tiên kỹ thuật nên làm trước trong Phase 2

### Cụm 1 - Object mapping và data consistency

- `maintenance.request` <-> `project.task`
- `maintenance.request` <-> `stock.picking`
- `maintenance.request` <-> `purchase.order`
- đồng bộ stage, trạng thái, related field, closed/done marker

### Cụm 2 - Approval và decision point

- proposal approval
- material approval
- rule người duyệt
- cân nhắc dùng `approval`

### Cụm 3 - Material flow

- material assessment chi tiết
- stock picking usable
- stock availability rõ nghĩa
- PO/RFQ usable hơn

### Cụm 4 - Biểu mẫu và report

- worksheet/checklist
- acceptance form
- execution monitoring
- dashboard theo vai trò

## 8. Những gì chưa nên làm trong Phase 2

- thay toàn bộ `maintenance.request` bằng object mới
- dựng workflow engine 21 bước hoàn chỉnh riêng
- full outside service flow đặc thù
- approval matrix nhiều tầng phức tạp nếu rule chưa ổn định
- bộ chứng từ đặc thù quá sâu khi user chưa chốt rõ form mẫu

## 9. Trình tự triển khai đề xuất cho Phase 2

1. Rà toàn bộ điểm đứt và dữ liệu không nhất quán còn lại từ `Phase 1`
2. Chốt object mapping chuẩn
3. Chốt material flow
4. Chốt approval flow
5. Bổ sung biểu mẫu / report / dashboard
6. Sau khi đủ dữ liệu thực tế, mới quyết định phần nào đẩy tiếp sang `Phase 3`

## 10. Kết luận

`Phase 2` nên được hiểu là phase:

- không còn dựng skeleton nữa
- mà tập trung “làm cho skeleton vận hành mượt và ít gãy”

Hướng đi an toàn là:

- giữ trục chuẩn Odoo như `Phase 1`
- chỉ tăng custom ở những điểm đã chứng minh là chuẩn Odoo chưa đủ
- dùng chính các vấn đề phát hiện trong quá trình test `Phase 1` làm backlog ưu tiên cho `Phase 2`

Mục tiêu cuối của `Phase 2` là:

- quy trình `0502` gần hơn đáng kể với vận hành thực tế
- người dùng thao tác ít gượng hơn
- dữ liệu và trạng thái giữa các object đồng nhất hơn
- sẵn sàng để quyết định phần custom sâu nào thật sự xứng đáng cho `Phase 3`
