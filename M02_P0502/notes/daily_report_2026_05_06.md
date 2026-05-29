# Daily Report - 2026-05-06

## 1. Phạm vi làm việc trong ngày

Hôm nay tập trung triển khai `Phase 3` của quy trình `0502 - Quản lý bảo trì`, bám theo lưu đồ nghiệp vụ đã rà soát trước đó để tránh làm dư scope.

Phạm vi thực tế đã chạm tới:

- `Phase 3 - Bước 1` đến `Phase 3 - Bước 10`
- rà soát lại kế hoạch `Phase 3` để bám sát lưu đồ nghiệp vụ thực tế
- sửa lỗi tương thích dữ liệu mẫu của module `M02_P0502_1` sau khi thêm rule audit planning ở `Phase 3 - Bước 8`

## 2. Tài liệu định hướng đã dùng

Trong suốt quá trình làm việc hôm nay, đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/plan_trien_khai_0502_theo_phase.md`
- `notes/phase_1_da_trien_khai.md`
- `notes/phase_2_da_trien_khai.md`
- `notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md`
- các note triển khai theo từng bước của `Phase 3`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- khi có khác biệt, source code hiện tại được dùng làm chuẩn xác nhận cuối cùng

## 3. Những gì đã triển khai trong ngày

### 3.1. Cụm phát sinh nhu cầu và intake đầu vào

Đã nâng phần đầu quy trình ở các bước đầu của `Phase 3` để request không chỉ “được tạo”, mà còn được mô tả rõ hơn về nguồn phát sinh và mức độ đầy đủ dữ liệu đầu vào.

Ở `Bước 1`, đã bổ sung:

- `Request Origin Group`
- `Intake Minimum Ready`
- `Intake Minimum Gap Reason`

Ý nghĩa:

- gom nguồn phát sinh theo 3 nhóm nghiệp vụ:
  - `Store Need`
  - `Preventive Need`
  - `System Need`
- cho biết request mới vào đã đủ dữ liệu tối thiểu hay chưa
- nếu chưa đủ, hiển thị rõ còn thiếu gì

Ở `Bước 2`, đã bổ sung lớp intake chi tiết hơn theo `Request Type`:

- template câu hỏi intake
- mẫu ghi chú intake
- các field:
  - `Intake Problem Detail`
  - `Intake Impact Scope`
  - `Intake Contact Name`
  - `Intake Contact Phone`
- các field đánh giá:
  - `Intake Detail Ready`
  - `Intake Detail Gap Reason`

Kết quả:

- request ở đầu vào có hướng dẫn intake rõ hơn
- `CMT Receive` không còn cho đi tiếp nếu intake detail chưa đủ

### 3.2. Cụm SLA tiếp nhận và ownership intake

Ở `Bước 3`, đã bổ sung lớp theo dõi SLA tiếp nhận trên `maintenance.request`:

- `Intake Owner`
- `Intake SLA Deadline`
- `Intake SLA Result`
- `Intake Age (Hours)`

Trên `maintenance.team`, đã thêm:

- `0502 Intake SLA Hours`

Ý nghĩa:

- biết request đang thuộc ai ở giai đoạn tiếp nhận
- biết deadline SLA tiếp nhận
- phân biệt:
  - `Pending`
  - `On Time`
  - `Late`

Đây là lớp monitoring nhẹ, chưa kéo sang activity/escalation tự động.

### 3.3. Cụm kiểm tra thực tế và preventive monitoring

Ở `Bước 4`, đã bổ sung template kiểm tra thực tế theo `Equipment Category`:

- `0502 Inspection Checklist Template`
- `0502 Inspection Worksheet Template`

Trên request, đã thêm:

- `Inspection Checklist Template`
- `Inspection Worksheet Template`
- `Inspection Checklist Result`
- `Inspection Worksheet`

Kết quả:

- kiểm tra thực tế bắt đầu có mẫu chuẩn theo loại thiết bị
- `Mark Inspected` bị chặn nếu category có template mà người dùng chưa điền dữ liệu thực tế tương ứng

Ở `Bước 5`, đã bổ sung lớp monitoring cho preventive:

- `Preventive Delay Days`
- `Preventive Pending Cycles`
- `Preventive Exception Status`

Các trạng thái exception chính:

- `Missing Next Date`
- `Due Now`
- `Multi-cycle Overdue`
- `Open Request Stalled`

Kết quả:

- nhìn thiết bị preventive rõ hơn ở góc vận hành
- chưa đụng vào reschedule workflow hay approval dời lịch

### 3.4. Cụm lead acknowledgment và queue tổng hợp

Ở `Bước 6`, đã nâng `Notify CMT Lead` từ mức “đã thông báo” lên mức “đã thông báo và lead đã xác nhận nhận việc hay chưa”.

Đã thêm:

- `Lead Acknowledgment Status`
- `Lead Acknowledged By`
- `Lead Acknowledged At`
- action `Acknowledge Lead Assignment`

Logic:

- mỗi lần notify/re-notify sẽ reset acknowledgment về `Pending`
- chỉ đúng `Lead Notified User` mới được acknowledge

Ở `Bước 7`, đã bổ sung các queue tối thiểu cho `CMT Lead`:

- `0502 Ready To Plan Queue`
- `0502 Critical Queue`
- `0502 Lead Assigned Queue`

Kết quả:

- lead có queue nhìn việc rõ hơn
- vẫn giữ scope tối thiểu, không dựng object queue riêng

### 3.5. Cụm planning history và audit replan

Ở `Bước 8`, đã bổ sung audit planning:

- model mới `x_psm_request_planning_history`
- trên request:
  - `Planning Change Reason`
  - `Planning History`
  - `Planning Revision Count`
  - `Last Planning Changed By`
  - `Last Planning Changed At`

Logic chính:

- lần `Mark Planned` đầu tạo revision `1` với loại `Initial Plan`
- nếu request đã planned mà đổi:
  - `Scheduled Date`
  - `Scheduled End`
  - `Responsible`
  - `Planning Note`
- thì bắt buộc phải có `Planning Change Reason`
- hệ thống tự tạo thêm revision `Replan`

Kết quả:

- planning bắt đầu có audit trail rõ ràng
- request re-plan nhiều lần sẽ nhìn được lịch sử thay đổi

### 3.6. Cụm execution package cho FSM task

Ở `Bước 9`, đã nâng `FSM Task` từ mức chỉ có context lên mức có “gói hướng dẫn thực thi” snapshot tại thời điểm tạo task.

Đã thêm template trên:

- `Request Type`
- `Equipment Category`

Bao gồm:

- `0502 FSM Task Template`
- `0502 FSM Checklist Template`
- `0502 FSM Material Template`

Khi tạo `FSM Task`, hệ thống snapshot sang task:

- `0502 Task Template`
- `0502 Execution Checklist Template`
- `0502 Material Package Template`

Kết quả:

- kỹ thuật viên mở task sẽ thấy ngay package hướng dẫn chuẩn hơn
- vẫn chưa kéo sang template engine hay workflow task riêng

### 3.7. Cụm monitoring tiến độ và nhánh cung ứng

Ở `Bước 10`, đã bổ sung 2 field monitoring tổng hợp trên `maintenance.request`:

- `Progress Checkpoint`
- `Supply Branch Status`

`Progress Checkpoint` giúp trả lời:

- request đang nghẽn ở bước nào của toàn bộ flow

`Supply Branch Status` giúp trả lời:

- nhánh vật tư / kho / mua ngoài đang ở trạng thái nào

Đồng thời đã thêm 3 action/menu reporting:

- `0502 Progress Monitoring`
- `0502 Supply Monitoring`
- `0502 Intake SLA Monitoring`

Kết quả:

- monitoring không còn rời theo từng nhánh nhỏ
- bắt đầu có góc nhìn vận hành tổng hợp ở mức request

## 4. Các lỗi / vấn đề đã xử lý trong ngày

### 4.1. Rà lại kế hoạch `Phase 3` để tránh làm dư

Sau khi đối chiếu lại lưu đồ nghiệp vụ thực tế, đã siết lại plan `Phase 3` để tránh over-scope.

Các điểm đã tinh chỉnh:

- không kéo `Bước 1` sang intake queue nặng
- không đẩy `Bước 10` sang dashboard/KPI engine riêng
- không mặc định tạo object riêng cho nhánh outside service ở `Bước 13`
- không mặc định kéo `purchase_requisition` vào `Bước 19`
- không tạo object execution riêng nếu `FSM task` còn đủ
- ở `Bước 21`, ưu tiên biên bản nghiệm thu / file xác nhận hơn là đi thẳng sang chữ ký điện tử

Kết quả:

- kế hoạch `Phase 3` bám sát lưu đồ hơn
- giảm rủi ro làm nhiều hơn nhu cầu thực tế

### 4.2. Lỗi seed data do rule audit planning mới

Trong quá trình cài/nâng cấp module dữ liệu mẫu `M02_P0502_1`, phát sinh lỗi:

- `Please fill in Planning Change Reason before changing a planned schedule.`

Nguyên nhân:

- `Phase 3 - Bước 8` đã thêm rule trong `write()`:
  - nếu request đã planned mà bị đổi field planning, phải có `Planning Change Reason`
- khi Odoo nạp XML seed, một số record `maintenance.request` planned bị đi qua `_load_records_write`
- dữ liệu seed cũ chưa có `x_psm_0502_plan_change_reason`

Đã xử lý:

- cập nhật file:
  - `addons/M02_P0502_1/data/psm_seed_data.xml`
- thêm `x_psm_0502_plan_change_reason` cho toàn bộ các record seed đã có `x_psm_0502_planned_at`

Kết quả:

- seed data tương thích lại với rule mới của `Phase 3 - Bước 8`

## 5. Kết quả hiện tại đến cuối ngày

Đến cuối ngày, source code đã phản ánh:

- `Phase 3 - Bước 1` đến `Phase 3 - Bước 10` đã có lớp triển khai trong source
- các cụm lớn đã được đẩy qua:
  - intake origin và intake detail
  - intake SLA và ownership
  - inspection template
  - preventive monitoring
  - lead acknowledgment
  - lead queues
  - planning history
  - FSM execution package
  - progress / supply / intake monitoring

Về tài liệu:

- các note theo bước từ `Phase 3 - Bước 1` đến `Phase 3 - Bước 10` đã được tạo
- kế hoạch `Phase 3` cũng đã được rà soát lại để bám đúng lưu đồ hơn

## 6. Kiểm tra kỹ thuật đã làm

Trong ngày đã thực hiện nhiều lượt kiểm tra kỹ thuật mức nhẹ:

- compile Python cho các model đã sửa
- parse XML cho các view và data file đã sửa bằng parser chuẩn

Kết quả:

- các file code và XML đã chốt trong ngày đều qua kiểm tra cú pháp

## 7. Danh sách note / tài liệu đã tạo hoặc cập nhật trong ngày

Đã tạo hoặc cập nhật các tài liệu sau:

- `phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md`
- `phase_3_buoc_1_da_trien_khai.md`
- `phase_3_buoc_2_da_trien_khai.md`
- `phase_3_buoc_3_da_trien_khai.md`
- `phase_3_buoc_4_da_trien_khai.md`
- `phase_3_buoc_5_da_trien_khai.md`
- `phase_3_buoc_6_da_trien_khai.md`
- `phase_3_buoc_7_da_trien_khai.md`
- `phase_3_buoc_8_da_trien_khai.md`
- `phase_3_buoc_9_da_trien_khai.md`
- `phase_3_buoc_10_da_trien_khai.md`

Ngoài ra đã cập nhật dữ liệu mẫu tại:

- `addons/M02_P0502_1/data/psm_seed_data.xml`

## 8. Việc tiếp theo đề xuất

Các việc nên làm tiếp sau report này:

- tiếp tục triển khai `Phase 3 - Bước 11` trở đi
- rà thêm seed data của `M02_P0502_1` để tìm các record cũ khác có thể đụng validation mới
- regenerate lại `structure/module_map.json`
- chạy test end-to-end theo các nhánh:
  - store request
  - preventive
  - request có replan
  - request có lead acknowledgment
  - request có supply branch nội bộ và mua ngoài

## 9. Kết luận ngắn

Ngày `06/05` là ngày đẩy `Phase 3` theo hướng kiểm soát vận hành và audit tốt hơn, nhưng vẫn giữ nguyên tắc không mở rộng quá tay so với lưu đồ nghiệp vụ thực tế.

Kết quả lớn nhất trong ngày là:

- làm dày hơn lớp intake và ownership ban đầu
- thêm audit cho planning
- chuẩn hóa package hướng dẫn cho `FSM Task`
- nâng lớp monitoring tổng hợp ở mức request
- xử lý được xung đột giữa rule mới và dữ liệu seed cũ
