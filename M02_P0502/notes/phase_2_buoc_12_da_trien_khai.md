# Phase 2 - Bước 12 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 12` tập trung vào việc chuẩn hóa bước:

- duyệt timeline
- duyệt cost

Mục tiêu chính là:

- làm rõ ai là người duyệt
- giữ approval ở mức 1 cấp nhưng có rule rõ ràng
- đưa thêm điều kiện duyệt theo cost
- giảm các case duyệt mơ hồ hoặc phụ thuộc hoàn toàn vào thao tác thủ công

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
- [hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần quyết định:

- có chuyển sang dùng `approval` thật hay không
- ai duyệt
- 1 cấp hay nhiều cấp
- điều kiện duyệt theo cost

Hướng triển khai được chọn là:

- chưa kéo module `approval` chuẩn vào ở bước này
- tiếp tục dùng approval trên `maintenance.request`
- nhưng nâng lên mức có:
  - approver rõ ràng
  - rule resolve approver rõ ràng
  - rule cost rõ ràng
  - auto approve dưới ngưỡng cấu hình

Lý do chọn hướng này:

- giữ scope vừa phải
- không làm vỡ luồng đã có ở `Phase 1`
- vẫn giải quyết được câu hỏi nghiệp vụ chính của bước 12

## 4. Cấu hình mới trên `maintenance.team`

Trong [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py), đã bổ sung:

- `x_psm_0502_proposal_approver_id`
- `x_psm_0502_proposal_auto_approve_limit`
- `x_psm_0502_currency_id`

### Ý nghĩa

#### `0502 Proposal Approver`

Là user được ưu tiên đóng vai trò approver cho:

- treatment proposal
- timeline
- estimated cost

#### `0502 Auto Approve Limit`

Là ngưỡng cost mà nếu:

- `Estimated Cost <= ngưỡng`

thì request có thể được:

- auto approve

thay vì phải đi qua pending approval thủ công.

#### `Currency`

Field related để hiển thị đúng đơn vị tiền tệ theo company của team.

## 5. Metadata approval mới trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_approval_required`
- `x_psm_0502_approval_user_id`
- `x_psm_0502_approval_rule`
- `x_psm_0502_approval_cost_rule`

### Ý nghĩa

#### `Approval Required`

Cho biết:

- request này có cần duyệt thủ công hay không

#### `Proposal Approver`

Cho biết:

- ai là approver đã được resolve cho request hiện tại

#### `Approval Rule`

Cho biết:

- approver được resolve theo rule nào

Ví dụ:

- `Team Approver`
- `Team Lead Fallback`
- `Team Member Fallback`
- `Technician Fallback`
- `Current User Fallback`

#### `Approval Cost Rule`

Cho biết:

- cost rule nào đã được áp dụng

Ví dụ:

- `Manual Review Required`
- `Auto Approved Under Limit`

## 6. Helper resolve approval đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm helper:

- `_psm_get_proposal_approval_resolution()`

Hàm này resolve đồng thời:

- approver user
- approval rule
- approval có bắt buộc hay không
- cost rule nào được áp dụng

## 7. Rule resolve approver

Thứ tự resolve approver hiện tại là:

1. `0502 Proposal Approver` trên `maintenance.team`
2. `0502 Lead User`
3. member đầu tiên của team
4. technician trên request
5. current user

Ý nghĩa:

- nếu team đã cấu hình approver rõ thì dùng ngay
- nếu chưa thì có fallback chain rõ ràng
- luôn cố gắng ra được một approver hợp lệ để không làm flow bị kẹt

## 8. Rule cost đã thêm

Approval hiện tại vẫn là 1 cấp, nhưng đã thêm logic cost:

### Trường hợp 1 - Cost nằm trong ngưỡng auto approve

Nếu:

- `Estimated Cost <= 0502 Auto Approve Limit`

thì:

- `Approval Required = False`
- `Approval Cost Rule = Auto Approved Under Limit`
- request được `Approved` ngay khi `Submit for Approval`

### Trường hợp 2 - Cost vượt ngưỡng hoặc không có ngưỡng

Nếu:

- cost vượt ngưỡng
- hoặc team chưa cấu hình ngưỡng auto approve

thì:

- `Approval Required = True`
- `Approval Cost Rule = Manual Review Required`
- request vào trạng thái `Pending Approval`

## 9. Thay đổi trong action submit / approve / reject

### `action_psm_submit_for_approval()`

Khi submit:

1. request phải đã có proposal
2. hệ thống resolve:
   - approver
   - approval rule
   - cost rule
3. nếu đủ điều kiện auto approve:
   - request chuyển ngay sang `Approved`
4. nếu không:
   - request chuyển sang `Pending Approval`

### `action_psm_approve_proposal()`

Đã siết thêm:

- chỉ đúng `Proposal Approver` được resolve mới được approve

Nếu user khác bấm:

- hệ thống chặn

### `action_psm_reject_proposal()`

Tương tự:

- chỉ đúng `Proposal Approver` mới được reject

## 10. Thay đổi giao diện

### Trên `maintenance.team`

Trong [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml), đã hiển thị:

- `0502 Proposal Approver`
- `0502 Auto Approve Limit`

và thêm filter:

- `Configured 0502 Proposal Approver`

### Trên tab `Approval` của request

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã hiển thị thêm:

- `Approval Required`
- `Proposal Approver`
- `Approval Rule`
- `Approval Cost Rule`

### Trên search/filter/group by của request

Đã thêm các filter:

- `Approval Required`
- `Auto Approved Under Limit`
- `Manual Review Required`
- `My Pending Approval`

Đã thêm group by:

- `Approval Required`
- `Proposal Approver`
- `Approval Rule`
- `Approval Cost Rule`

## 11. Ý nghĩa nghiệp vụ của bước này

`Phase 1 - Bước 12` chỉ có approval đơn giản:

- pending
- approved
- rejected

Nhưng chưa trả lời rõ:

- ai duyệt
- theo rule nào
- có auto approve theo cost hay không

Sau bước này:

- approval vẫn nhẹ
- nhưng đã rõ hơn về:
  - ownership
  - decision rule
  - cost rule

## 12. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 12`, hiện chưa làm:

- chưa chuyển sang module `approval` chuẩn
- chưa có nhiều cấp duyệt
- chưa có matrix phức tạp theo nhiều ngưỡng cost
- chưa có route approval riêng theo request type
- chưa có SLA hoặc escalation tự động cho approver chậm duyệt

## 13. Cách test

### Case 1 - Auto approve dưới ngưỡng

1. Upgrade `M02_P0502`
2. Vào `Maintenance Team`, cấu hình:
   - `0502 Proposal Approver`
   - `0502 Auto Approve Limit`
3. Mở một request đã `Mark Proposed`
4. Đặt `Estimated Cost` nhỏ hơn hoặc bằng limit
5. Bấm `Submit for Approval`

Kết quả mong đợi:

- request chuyển thẳng sang `Approved`
- `Approval Required = False`
- `Approval Cost Rule = Auto Approved Under Limit`

### Case 2 - Pending approval khi vượt ngưỡng

1. Giữ cùng team hoặc team khác
2. Đặt `Estimated Cost` lớn hơn limit
3. Bấm `Submit for Approval`

Kết quả mong đợi:

- request vào `Pending Approval`
- `Approval Required = True`
- `Proposal Approver` có giá trị
- `Approval Rule` có giá trị
- `Approval Cost Rule = Manual Review Required`

### Case 3 - Sai user không được approve

1. Đăng nhập bằng user không phải approver
2. Bấm `Approve Proposal`

Kết quả mong đợi:

- hệ thống chặn

### Case 4 - Đúng approver approve/reject

1. Đăng nhập đúng `Proposal Approver`
2. Bấm `Approve Proposal` hoặc `Reject Proposal`

Kết quả mong đợi:

- thao tác thành công
- `Approval Decided By`
- `Approval Decided At`

được ghi đúng

## 14. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse: `OK`

## 15. File đã thay đổi

- [hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 16. Điều chỉnh ownership của bước 12

Sau khi rà lại nghiệp vụ, bước 12 được điều chỉnh theo hướng:

- store là bên duyệt proposal
- `maintenance.team` chỉ còn là cấu hình fallback

Các thay đổi đã áp dụng:

- thêm `x_psm_0502_proposal_approver_id` trên `hr.department`
- hiển thị field này trên form department
- đổi helper resolve approval để ưu tiên:
  1. `Store Proposal Approver`
  2. `Team Proposal Approver`
  3. `Team Lead`
  4. member đầu tiên của team
  5. technician
  6. current user

Ý nghĩa:

- request sẽ ưu tiên người duyệt phía store theo đúng ownership nghiệp vụ
- các request cũ hoặc department chưa cấu hình vẫn không bị gãy vì còn fallback chain cũ
- cost rule và auto approve limit vẫn giữ theo `maintenance.team` để tránh nở scope của bước 12 quá nhanh
