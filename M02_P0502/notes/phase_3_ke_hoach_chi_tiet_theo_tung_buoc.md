# Phase 3 - Kế Hoạch Chi Tiết Theo Từng Bước

## 1. Mục đích

Tài liệu này dùng để lập kế hoạch chi tiết cho `Phase 3` của quy trình:

- `0502 - Quản lý bảo trì`

Khác với `Phase 1` và `Phase 2`, `Phase 3` không còn tập trung vào:

- dựng luồng tối thiểu
- hay chỉ làm mượt các điểm đứt

Mà tập trung vào:

- các phần custom sâu
- workflow đặc thù doanh nghiệp
- tính kiểm soát và truy vết toàn quy trình
- các object / chứng từ / approval nhiều tầng nếu thực sự cần

## 2. Tài liệu đã dùng để lập plan

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- khi có khác biệt, source code hiện tại phải được xem là chuẩn xác nhận cuối cùng
- trước khi làm sâu `Phase 3`, nên regenerate lại JSON map

### Tài liệu tham chiếu chính

- [plan_trien_khai_0502_theo_phase.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/plan_trien_khai_0502_theo_phase.md)
- [phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [phase_1_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_da_trien_khai.md)
- [phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [phase_2_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_da_trien_khai.md)

## 3. Cách hiểu Phase 3

Sau `Phase 1` và `Phase 2`, module hiện đã có:

- luồng end-to-end chạy được
- dữ liệu đã có cấu trúc hơn
- queue, readiness, approval, vật tư, kho, mua ngoài, execution, acceptance đã usable hơn

Vì vậy `Phase 3` không nên lặp lại các việc đã làm.

`Phase 3` nên tập trung vào các phần còn lại mà `Phase 1` và `Phase 2` chưa xử lý triệt để:

- workflow 21 bước được điều khiển chặt hơn
- object trục chính xuyên suốt hơn
- nhánh `outside service` riêng
- approval nhiều tầng nếu doanh nghiệp cần
- chứng từ / biên bản / biểu mẫu đặc thù
- KPI / SLA / audit trail sâu hơn

## 4. Nguyên tắc thiết kế cho Phase 3

### 4.0. Bám sát lưu đồ nghiệp vụ hiện tại

Lưu đồ nghiệp vụ hiện tại cho thấy:

- `Bước 1` chỉ là phát sinh nhu cầu
- `Bước 2` mới là tạo phiếu yêu cầu / raise ticket
- `Bước 7` mới là nơi `CMT Lead` tổng hợp
- `Bước 10` là báo cáo / theo dõi tình trạng theo vận hành
- `Bước 13` là quyết định có đi nhánh dịch vụ ngoài hay không
- `Bước 19` là mua ngoài vật tư khi kho không đáp ứng

Vì vậy trong `Phase 3`:

- không mặc định mở rộng `Bước 1` thành workflow intake nặng nếu lưu đồ chưa yêu cầu
- không mặc định dựng dashboard / workflow engine / object mới chỉ vì có thể làm được
- chỉ đưa vào plan những gì bám trực tiếp vào nhánh nghiệp vụ đang có trong lưu đồ
- các ý như:
  - object trục chính mới
  - approval nhiều tầng
  - requisition
  - workflow engine riêng
  chỉ xem là phương án dự phòng, không phải scope mặc định

### 4.1. Không custom sâu nếu chưa có nhu cầu thật

Các phần như:

- workflow engine riêng
- object master xuyên suốt mới
- approval nhiều tầng
- outside service riêng

chỉ nên làm nếu:

- đã chốt nghiệp vụ với user
- đã có pain point rõ từ `Phase 1` và `Phase 2`

### 4.2. Phase 3 phải ưu tiên tính truy vết

Nếu đã chấp nhận custom sâu, thì lợi ích chính phải là:

- nhìn được ai làm gì, khi nào
- bước nào đang chờ bước nào
- nhánh nào đang đi nội bộ, nhánh nào đi mua ngoài, nhánh nào đi dịch vụ ngoài
- vì sao một request bị chặn hoặc quay lại

### 4.3. Tách rõ custom sâu theo cụm

Không nên làm tất cả một lúc.  
Nên chia `Phase 3` thành các cụm:

- cụm workflow và state machine
- cụm outside service
- cụm approval nhiều tầng
- cụm chứng từ / biên bản
- cụm dashboard / SLA / audit

## 5. Các cụm ưu tiên kỹ thuật của Phase 3

### Cụm 1 - Workflow 21 bước thực sự

Mục tiêu:

- chuyển từ các action rời rạc sang state machine / progression rõ ràng hơn
- giảm tình trạng user nhảy bước
- làm rõ điều kiện vào / ra của từng bước

### Cụm 2 - Object trục chính xuyên suốt

Mục tiêu:

- cân nhắc có cần object riêng kiểu:
  - `x_psm_0502_process_case`
  - hoặc object tương đương
- gom trạng thái, approval, branch, audit về một trục chính

### Cụm 3 - Outside service riêng

Mục tiêu:

- thay vì chỉ có cờ và route
- tạo được luồng thuê ngoài có object và trạng thái riêng nếu doanh nghiệp cần

### Cụm 4 - Approval nhiều tầng

Mục tiêu:

- tách approval theo:
  - store
  - kỹ thuật
  - vật tư
  - quản lý
  - tài chính

### Cụm 5 - Biểu mẫu và audit trail

Mục tiêu:

- chuẩn hóa chứng từ
- dễ in / đối chiếu / lưu hồ sơ
- dễ truy vết khi kiểm tra lại

## 6. Kế hoạch chi tiết theo từng bước

## Bước 1 - Tiếp nhận yêu cầu

### Trọng tâm Phase 3

- giữ đúng vai trò của bước này là:
  - phát sinh nhu cầu từ cửa hàng
  - chưa đẩy sang logic điều phối sâu

### Sau Phase 2 hiện đã có

- intake validation
- source system
- source reference
- source mapping note
- CMT receive logic

### Còn thiếu để lên Phase 3

- làm rõ hơn nguồn phát sinh thực tế của nhu cầu:
  - từ cửa hàng
  - từ preventive
  - từ hệ thống khác
- làm rõ dữ liệu tối thiểu cần có trước khi sang `Bước 2`

### Hướng triển khai đề xuất

- không dựng queue riêng ở bước này
- chỉ chuẩn hóa rõ dữ liệu đầu vào và nguồn phát sinh
- nếu cần, thêm hướng dẫn / rule hiển thị theo source type

### Mức custom dự kiến

- custom nhẹ

## Bước 2 - Ghi nhận thông tin ban đầu

### Trọng tâm Phase 3

- chốt mẫu intake hoàn chỉnh theo đúng doanh nghiệp

### Sau Phase 2 hiện đã có

- validation các field intake chính

### Còn thiếu để lên Phase 3

- bộ câu hỏi intake chuẩn theo loại request
- có thể cần template theo loại thiết bị / loại yêu cầu

### Hướng triển khai đề xuất

- cân nhắc template intake theo `request_type`
- nếu cần sâu hơn, dùng worksheet hoặc dynamic form

### Mức custom dự kiến

- custom vừa

## Bước 3 - Xác nhận tiếp nhận

### Trọng tâm Phase 3

- biến việc tiếp nhận thành một checkpoint có SLA và ownership

### Sau Phase 2 hiện đã có

- `Received By (CMT)`
- `Received At (CMT)`
- auto receive có kiểm soát cho `manual_request`

### Còn thiếu để lên Phase 3

- SLA từ lúc request vào hệ thống đến lúc CMT nhận
- escalations nếu chưa receive

### Hướng triển khai đề xuất

- thêm `intake aging`
- activity / reminder / overdue intake queue nếu thực sự phát sinh nhu cầu SLA tiếp nhận

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 4 - Kiểm tra ban đầu

### Trọng tâm Phase 3

- từ inspection structured sang checklist / worksheet chuẩn hóa theo loại thiết bị

### Sau Phase 2 hiện đã có

- symptom status
- equipment status
- safety risk
- action urgency

### Còn thiếu để lên Phase 3

- checklist kiểm tra theo loại thiết bị
- evidence / ảnh / file đính kèm theo checklist

### Hướng triển khai đề xuất

- cân nhắc `maintenance_worksheet` hoặc object checklist riêng
- nếu cần, map template checklist theo equipment category

### Mức custom dự kiến

- custom vừa đến cao

## Bước 5 - Sinh preventive request

### Trọng tâm Phase 3

- nâng preventive từ cron logic sang preventive management hoàn chỉnh hơn

### Sau Phase 2 hiện đã có

- preventive status
- chống sinh trùng
- logic due/open_request rõ hơn

### Còn thiếu để lên Phase 3

- preventive plan / calendar rõ hơn
- exception handling khi preventive bị trễ nhiều kỳ

### Hướng triển khai đề xuất

- thêm reporting preventive aging
- nếu cần, thêm reschedule workflow / approval cho dời lịch preventive

### Mức custom dự kiến

- custom vừa

## Bước 6 - Notify lead

### Trọng tâm Phase 3

- biến notify lead thành assignment / acknowledgment thực sự

### Sau Phase 2 hiện đã có

- `0502 Lead User`
- lead notification rule

### Còn thiếu để lên Phase 3

- lead phải xác nhận đã nhận việc hay chưa
- theo dõi backlog theo lead thực tế

### Hướng triển khai đề xuất

- thêm `lead acknowledged`
- thêm queue theo lead owner

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 7 - Tổng hợp queue cho lead

### Trọng tâm Phase 3

- từ queue usable sang queue điều phối thực sự

### Sau Phase 2 hiện đã có

- requests to plan
- preventive queue
- store action needed
- overdue queue

### Còn thiếu để lên Phase 3

- queue theo SLA
- queue theo criticality
- queue theo exact owner

### Hướng triển khai đề xuất

- thêm:
  - `Ready To Plan Queue`
  - `Critical Queue`
  - `Lead Assigned Queue`
- không mở rộng ngược các queue này sang `Bước 1`
- giữ đúng tinh thần lưu đồ: `Bước 7` mới là điểm tổng hợp của `CMT Lead`

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 8 - Lập kế hoạch

### Trọng tâm Phase 3

- biến planning từ validation logic sang planning object / planning board rõ hơn

### Sau Phase 2 hiện đã có

- `Ready To Plan`
- `Planning Block Reason`
- validation trước khi `Mark Planned` / `Create FSM Task`

### Còn thiếu để lên Phase 3

- planning board / calendar / allocation rõ hơn
- audit rõ khi đổi lịch

### Hướng triển khai đề xuất

- cân nhắc dùng module `planning` nếu doanh nghiệp thật sự cần lịch nguồn lực
- nếu không, thêm planning history riêng trên request

### Mức custom dự kiến

- custom vừa

## Bước 9 - Tạo FSM task

### Trọng tâm Phase 3

- từ task có context sang task template / execution package chuẩn hóa hơn

### Sau Phase 2 hiện đã có

- description chuẩn hóa
- context 0502 trên task

### Còn thiếu để lên Phase 3

- task template theo loại request
- activity / checklist / vật tư chuẩn theo loại công việc

### Hướng triển khai đề xuất

- map template theo:
  - request type
  - equipment type
  - service route

### Mức custom dự kiến

- custom vừa

## Bước 10 - Monitoring

### Trọng tâm Phase 3

- làm rõ phần:
  - báo cáo tiến độ
  - theo dõi tình trạng xử lý
  theo đúng lưu đồ nghiệp vụ

### Sau Phase 2 hiện đã có

- request monitoring
- preventive monitoring
- overdue monitoring
- follow-up needed
- execution monitoring

### Còn thiếu để lên Phase 3

- báo cáo tiến độ vận hành dễ dùng hơn cho:
  - request
  - FSM task
  - nhánh kho / mua ngoài
- nếu có nhu cầu quản trị thật, mới cân nhắc KPI sâu hơn

### Hướng triển khai đề xuất

- ưu tiên:
  - report list / pivot / graph bám đúng các điểm nghẽn trong lưu đồ
- dashboard tổng hợp riêng chỉ làm nếu user xác nhận cần

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 11 - Đề xuất phương án xử lý

### Trọng tâm Phase 3

- nâng proposal structured sang proposal document / quotation artifact rõ hơn

### Sau Phase 2 hiện đã có

- root cause
- technical solution
- cost note
- timeline note
- proposal summary

### Còn thiếu để lên Phase 3

- versioning proposal
- compare proposal revisions
- template proposal theo loại sự cố

### Hướng triển khai đề xuất

- cân nhắc proposal revision log
- nếu cần, tạo object proposal riêng thay vì chỉ nằm trên request

### Mức custom dự kiến

- custom vừa đến cao

## Bước 12 - Duyệt timeline và cost

### Trọng tâm Phase 3

- approval nhiều tầng nếu doanh nghiệp thực sự cần

### Sau Phase 2 hiện đã có

- rule resolve approver
- auto approve dưới limit
- owner phía store được ưu tiên

### Còn thiếu để lên Phase 3

- nhiều tầng duyệt
- matrix theo ngưỡng chi phí / loại request / store / team
- delegation / substitute approver

### Hướng triển khai đề xuất

- nếu yêu cầu mạnh, cân nhắc chuyển sang module `approval` chuẩn hoặc approval object riêng

### Mức custom dự kiến

- custom cao

## Bước 13 - Quyết định nội bộ hay thuê ngoài

### Trọng tâm Phase 3

- hoàn thiện nhánh:
  - xử lý nội bộ
  - hoặc chuyển dịch vụ ngoài
  theo đúng điểm rẽ nhánh của lưu đồ

### Sau Phase 2 hiện đã có

- service route
- service route reason

### Còn thiếu để lên Phase 3

- làm rõ dữ liệu quyết định route service
- nếu có dùng dịch vụ ngoài thật:
  - theo dõi vendor service
  - theo dõi trạng thái xử lý ngoài

### Hướng triển khai đề xuất

- chưa mặc định tạo object outsource riêng
- trước hết chỉ chuẩn hóa đủ:
  - người quyết định
  - lý do chuyển ngoài
  - vendor / đối tác thực hiện
  - trạng thái xử lý ngoài
- chỉ tạo model riêng nếu nhánh này được dùng thường xuyên và có lifecycle riêng rõ ràng

### Mức custom dự kiến

- custom vừa đến cao

## Bước 14 - Khai báo vật tư

### Trọng tâm Phase 3

- nâng material lines từ dữ liệu dự kiến sang dữ liệu có version / actual usage / source resolution sâu hơn

### Sau Phase 2 hiện đã có

- material detail lines có cấu trúc

### Còn thiếu để lên Phase 3

- compare planned vs actual material usage
- alternative material / substitute product

### Hướng triển khai đề xuất

- tách planned lines và actual used lines nếu cần
- thêm revision audit cho material requirement

### Mức custom dự kiến

- custom vừa

## Bước 15 - Tạo phiếu kho

### Trọng tâm Phase 3

- làm chắc nhánh kho theo nhiều team / warehouse / route thực tế hơn

### Sau Phase 2 hiện đã có

- team-level stock flow
- auto tạo move từ material lines

### Còn thiếu để lên Phase 3

- route phức tạp hơn
- location động theo store / technician / van stock

### Hướng triển khai đề xuất

- cân nhắc rule engine resolve stock flow theo nhiều tiêu chí

### Mức custom dự kiến

- custom vừa

## Bước 16 - Kiểm tồn

### Trọng tâm Phase 3

- từ snapshot availability sang decision support mạnh hơn

### Sau Phase 2 hiện đã có

- `Current` vs `Checked` availability
- `Stock Check Result`

### Còn thiếu để lên Phase 3

- explainability chi tiết theo từng line thiếu
- recommendation:
  - xuất nội bộ
  - mua ngoài
  - tách phần có sẵn / phần thiếu

### Hướng triển khai đề xuất

- thêm line-level stock check result
- thêm shortage summary

### Mức custom dự kiến

- custom vừa

## Bước 17 - Duyệt vật tư nội bộ

### Trọng tâm Phase 3

- approval vật tư nhiều tầng / đúng owner theo kho và điều phối nếu cần

### Sau Phase 2 hiện đã có

- team material approver
- auto approve theo limit
- source exception manual review

### Còn thiếu để lên Phase 3

- tách rõ approver của:
  - team
  - kho
  - điều phối vật tư
- multi-step approval

### Hướng triển khai đề xuất

- nếu doanh nghiệp yêu cầu, tách approval matrix riêng cho nhánh vật tư

### Mức custom dự kiến

- custom vừa đến cao

## Bước 18 - Xuất kho thực tế

### Trọng tâm Phase 3

- làm sâu nhánh issuance / reservation / actual issue

### Sau Phase 2 hiện đã có

- business status cho stock issue
- sync từ picking về request

### Còn thiếu để lên Phase 3

- actual material issuance per line
- chênh lệch planned vs issued
- handling partial issue

### Hướng triển khai đề xuất

- thêm summary partial issue
- nếu cần, đưa line-level issued result về request

### Mức custom dự kiến

- custom vừa

## Bước 19 - Mua ngoài khi thiếu vật tư

### Trọng tâm Phase 3

- từ RFQ usable sang luồng mua ngoài đặc thù nếu doanh nghiệp cần

### Sau Phase 2 hiện đã có

- vendor suggestion
- prefilled RFQ line
- request context trên PO

### Còn thiếu để lên Phase 3

- làm rõ hơn:
  - nhà cung cấp được chọn
  - tiến độ mua ngoài
  - vật tư nào đang chờ mua
- nếu doanh nghiệp có nhu cầu thật:
  - so sánh báo giá
  - approval mua ngoài riêng

### Hướng triển khai đề xuất

- không mặc định kéo `purchase_requisition`
- tiếp tục ưu tiên `purchase` chuẩn
- chỉ thêm compare / approval / requisition nếu được xác nhận là requirement thật

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 20 - Thực thi sửa chữa

### Trọng tâm Phase 3

- nâng execution data thành execution control thực sự

### Sau Phase 2 hiện đã có

- task giữ execution thật
- request giữ execution summary

### Còn thiếu để lên Phase 3

- checklist template theo loại task
- actual material used object riêng
- time spent chuẩn hóa sâu hơn
- execution evidence / photo / signoff hiện trường

### Hướng triển khai đề xuất

- tiếp tục lấy `FSM task` làm object thực thi chính
- chưa tạo object execution riêng nếu bộ field hiện tại trên task còn đủ
- chỉ bổ sung template checklist / evidence / material used sâu hơn khi đội vận hành xác nhận cần

### Mức custom dự kiến

- custom nhẹ đến vừa

## Bước 21 - Nghiệm thu sau bảo trì

### Trọng tâm Phase 3

- biến acceptance có cấu trúc thành biên bản nghiệm thu / signoff thực sự

### Sau Phase 2 hiện đã có

- acceptance contact
- acceptance role
- equipment result
- follow-up / rework

### Còn thiếu để lên Phase 3

- chữ ký / xác nhận điện tử nếu doanh nghiệp cần
- biên bản nghiệm thu in theo mẫu
- acceptance history / re-acceptance nếu làm lại nhiều vòng

### Hướng triển khai đề xuất

- ưu tiên làm:
  - biên bản nghiệm thu in theo mẫu
  - hoặc file xác nhận đính kèm
- chữ ký / signoff điện tử chỉ làm nếu quy trình thật sự yêu cầu

### Mức custom dự kiến

- custom nhẹ đến vừa

## 7. Trình tự triển khai đề xuất cho Phase 3

Không nên làm `Phase 3` theo thứ tự 1 -> 21 cứng nhắc.  
Trình tự hợp lý hơn là theo cụm:

### Cụm A - Workflow tổng thể

- Bước 7
- Bước 8
- Bước 10
- Bước 20
- Bước 21

Lý do:

- đây là cụm quyết định user có cảm giác “quy trình được điều khiển thật” hay không

### Cụm B - Approval và decision point

- Bước 12
- Bước 17
- Bước 19

Lý do:

- đây là cụm dễ phát sinh thay đổi lớn về ownership và matrix phê duyệt

### Cụm C - Outside service và nhánh đặc thù

- Bước 13
- các phần liên quan của Bước 19, 20, 21

Lý do:

- đây là cụm custom nặng nhất và nên chỉ làm khi nghiệp vụ đã chốt

### Cụm D - Chứng từ, biểu mẫu, audit

- Bước 11
- Bước 20
- Bước 21

Lý do:

- chỉ nên đầu tư mạnh khi quy trình lõi đã đủ ổn

## 8. Những gì chưa nên làm ngay trong đầu Phase 3

Không nên lao vào ngay:

- object trục chính mới cho toàn bộ 0502
- workflow engine riêng
- many-layer approval engine riêng
- dashboard JS riêng
- outside service object riêng

nếu chưa trả lời được:

- user đang đau ở đâu
- phần chuẩn hiện tại đang thiếu cái gì
- vì sao custom sâu là cần thiết

## 9. Deliverable đề xuất của Phase 3

Nếu làm đầy đủ `Phase 3`, nên có tối thiểu:

- tài liệu workflow tổng thể đã chốt với user
- ma trận ownership cho từng bước
- ma trận approval
- ma trận branch:
  - internal
  - stock available
  - stock not available
  - purchase
  - outside service
  - follow-up
  - rework
- danh sách chứng từ / biểu mẫu chuẩn hóa
- backlog kỹ thuật theo cụm như mục 7

## 10. Kết luận

`Phase 3` không phải là phase “thêm vài field nữa”.

Đây là phase:

- chốt những gì thực sự cần custom sâu
- đưa workflow 0502 tiến gần hơn tới quy trình nội bộ thật
- đổi lại bằng effort, độ phức tạp và chi phí bảo trì cao hơn

Vì vậy hướng đúng là:

- dùng kết quả của `Phase 1` và `Phase 2` làm nền
- chỉ chọn làm sâu những cụm đã có pain point rõ hoặc được lưu đồ nghiệp vụ yêu cầu trực tiếp
- tránh biến `Phase 3` thành một đợt custom rộng nhưng mơ hồ

Nếu cần bắt đầu ngay, thứ tự ưu tiên nên là:

- workflow / queue / readiness
- approval matrix
- outside service
- chứng từ và acceptance artifact
