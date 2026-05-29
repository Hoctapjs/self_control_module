# Phase 2 - Bước 17 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 17` tập trung vào việc nâng bước:

- duyệt yêu cầu vật tư

từ mức:

- chỉ có điểm quyết định `pending / approved / rejected`

sang mức:

- có owner duyệt rõ ràng
- có rule resolve approver rõ ràng
- có rule auto approve / manual review rõ ràng
- có snapshot giá trị vật tư tại thời điểm gửi duyệt

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
- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [phase_2_buoc_14_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_14_da_trien_khai.md)
- [phase_2_buoc_15_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_15_da_trien_khai.md)
- [phase_2_buoc_16_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_16_da_trien_khai.md)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- làm rõ ai duyệt
- duyệt theo giá trị hay theo loại vật tư
- cân nhắc dùng `approval` nếu rule đã đủ rõ

Hướng triển khai được chọn là:

- chưa kéo module `approval` chuẩn vào ở bước này
- tiếp tục dùng approval trên `maintenance.request`
- nhưng nâng approval vật tư lên mức có:
  - approver nội bộ rõ ràng
  - rule resolve approver rõ ràng
  - rule auto approve theo giá trị rõ ràng
  - rule chặn auto approve khi source type của dòng vật tư có dấu hiệu exception

Lý do chọn hướng này:

- giữ scope vừa phải
- không làm vỡ luồng `Phase 1`
- tận dụng được dữ liệu structured material lines của `Bước 14`
- phản ánh đúng ownership nội bộ của nhánh xuất kho

## 4. Ownership nghiệp vụ đã chốt

Ở bước này, owner duyệt **không phải store** như `Bước 12`.

`Bước 17` là nhánh:

- duyệt yêu cầu vật tư nội bộ
- trước khi đi sang xuất kho thực tế

Vì vậy approver được đặt theo:

- `maintenance.team`

chứ không đặt theo:

- `hr.department`
- store approver

Điều này tách rõ:

- `Bước 12` = store-side approval cho proposal/timeline/cost
- `Bước 17` = internal approval cho material issue

## 5. Cấu hình mới trên `maintenance.team`

Trong [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py), đã bổ sung:

- `x_psm_0502_material_approver_id`
- `x_psm_0502_material_auto_approve_limit`

### Ý nghĩa

#### `0502 Material Approver`

Là user nội bộ được ưu tiên đóng vai trò approver cho:

- yêu cầu xuất vật tư nội bộ

#### `0502 Material Auto Approve Limit`

Là ngưỡng giá trị vật tư mà nếu:

- tổng giá trị vật tư dự kiến `<= ngưỡng`

thì request có thể được:

- auto approve

thay vì đi qua `pending` thủ công.

## 6. Metadata approval vật tư mới trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã bổ sung:

- `x_psm_0502_material_approval_required`
- `x_psm_0502_material_approval_user_id`
- `x_psm_0502_material_approval_rule`
- `x_psm_0502_material_approval_value`
- `x_psm_0502_material_approval_value_rule`

### Ý nghĩa

#### `Material Approval Required`

Cho biết:

- request này có cần qua duyệt thủ công hay không

#### `Material Approver`

Cho biết:

- ai là approver nội bộ đã được resolve cho request hiện tại

#### `Material Approval Rule`

Cho biết:

- approver được resolve theo rule nào

Ví dụ:

- `Team Material Approver`
- `Team Lead Fallback`
- `Team Member Fallback`
- `Technician Fallback`
- `Current User Fallback`

#### `Estimated Material Value`

Cho biết:

- tổng giá trị vật tư dự kiến tại thời điểm gửi duyệt

Hiện tại giá trị này được tính từ:

- `product.standard_price * estimated_qty`

trên các `Material Detail Lines`.

#### `Material Approval Value Rule`

Cho biết:

- request này được auto approve hay phải manual review theo rule nào

Ví dụ:

- `Auto Approved Under Limit`
- `Manual Review Required`
- `Manual Review Required By Source Type`

## 7. Helper resolve approval vật tư đã thêm

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_material_approval_resolution()`

Hàm này resolve đồng thời:

- approver user
- approval rule
- approval có bắt buộc hay không
- value rule nào được áp dụng
- tổng giá trị vật tư dự kiến

## 8. Rule resolve approver

Thứ tự resolve approver hiện tại là:

1. `0502 Material Approver` trên `maintenance.team`
2. `0502 Lead User`
3. member đầu tiên của team
4. technician trên request
5. current user

Ý nghĩa:

- nếu team đã cấu hình approver riêng thì dùng ngay
- nếu chưa có thì vẫn có fallback chain rõ ràng
- không để flow bị kẹt chỉ vì thiếu cấu hình một mức

## 9. Rule auto approve / manual review

Approval vật tư hiện tại vẫn là 1 cấp, nhưng đã có 2 lớp rule:

### 9.1. Rule theo source type của dòng vật tư

Nếu trong `Material Detail Lines` có ít nhất một dòng mà:

- `Expected Source = External Purchase`
- hoặc `Expected Source = Other`

thì request:

- **không được auto approve**
- phải đi `manual review`

Lý do:

- đây là dấu hiệu bộ line vật tư chưa thuần nhánh xuất kho nội bộ
- cần user nội bộ xem lại trước khi cho đi tiếp

### 9.2. Rule theo tổng giá trị vật tư

Nếu không có source type exception và:

- `Estimated Material Value <= 0502 Material Auto Approve Limit`

thì:

- `Material Approval Required = False`
- `Material Approval Value Rule = Auto Approved Under Limit`
- request được `Approved` ngay khi `Submit Material Approval`

Ngược lại:

- `Material Approval Required = True`
- `Material Approval Value Rule = Manual Review Required`
- request vào trạng thái `Pending Approval`

## 10. Thay đổi trong action submit / approve / reject

### `action_psm_submit_material_approval()`

Action này giờ sẽ:

1. kiểm tra request có đi đúng nhánh vật tư nội bộ hay không
2. yêu cầu đã có:
   - stock picking
   - stock checked
   - `Stock Check Result = available`
3. gọi lại validation structured material assessment của `Bước 14`
4. resolve:
   - approver
   - approval rule
   - approval required
   - value rule
   - estimated material value
5. nếu đủ điều kiện auto approve:
   - request sang `Approved`
6. nếu không:
   - request sang `Pending Approval`

### `action_psm_approve_material_request()`

Đã siết thêm:

- chỉ đúng `Material Approver` đã được resolve mới được approve

Nếu user khác bấm:

- hệ thống chặn

### `action_psm_reject_material_request()`

Tương tự:

- chỉ đúng `Material Approver` mới được reject

## 11. Thay đổi giao diện

### Trên `maintenance.team`

Trong [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml), đã hiển thị:

- `0502 Material Approver`
- `0502 Material Auto Approve Limit`

và thêm filter:

- `Configured 0502 Material Approver`

### Trên tab `Material Assessment` của request

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã hiển thị thêm:

- `Material Approval Required`
- `Material Approver`
- `Material Approval Rule`
- `Estimated Material Value`
- `Material Approval Value Rule`

### Trên list/search/group by

Đã bổ sung:

- filter:
  - `Material Approval Required`
  - `Material Auto Approved Under Limit`
  - `Material Manual Review Required`
  - `My Pending Material Approval`
- group by:
  - `Material Approver`
  - `Material Approval Rule`
  - `Material Approval Value Rule`

## 12. Ý nghĩa nghiệp vụ của bước này

Sau `Bước 16`, request đã biết:

- kho có đủ vật tư nội bộ hay không

thì `Bước 17` là nơi xác định:

- nhánh vật tư nội bộ có được nội bộ chấp thuận cho đi tiếp sang xuất kho hay không

Sau `Phase 2 - Bước 17`, approval vật tư không còn chỉ là:

- một trạng thái `pending / approved / rejected`

mà đã có thêm:

- owner rõ ràng
- rule rõ ràng
- điều kiện auto/manual rõ ràng

## 13. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 17`, hiện chưa làm:

- chưa chuyển sang module `approval` chuẩn
- chưa có nhiều cấp duyệt vật tư
- chưa duyệt theo nhóm sản phẩm riêng biệt
- chưa có rule giá trị theo store/department
- chưa tách ngưỡng theo từng source type khác nhau
- chưa có activity/notification riêng cho approver vật tư

## 14. Cách test

### Case 1 - Auto approve dưới ngưỡng

1. Upgrade `M02_P0502`
2. Vào `Maintenance Team`
3. Cấu hình:
   - `0502 Material Approver`
   - `0502 Material Auto Approve Limit`
4. Mở request đã qua `Bước 16` với:
   - `Stock Check Result = available`
   - material lines có source type nội bộ
   - tổng giá trị vật tư `<= limit`
5. Bấm `Submit Material Approval`

Kết quả mong đợi:

- request tự sang `Approved`
- `Material Approval Required = False`
- `Material Approval Value Rule = Auto Approved Under Limit`

### Case 2 - Manual review vì vượt ngưỡng

1. Giữ cùng cấu hình team
2. Dùng request có tổng giá trị vật tư `> limit`
3. Bấm `Submit Material Approval`

Kết quả mong đợi:

- request sang `Pending Approval`
- `Material Approval Required = True`
- `Material Approval Value Rule = Manual Review Required`
- `Material Approver` được fill

### Case 3 - Manual review vì source type exception

1. Tạo request có ít nhất một dòng vật tư:
   - `Expected Source = External Purchase`
   - hoặc `Other`
2. Bấm `Submit Material Approval`

Kết quả mong đợi:

- request sang `Pending Approval`
- `Material Approval Value Rule = Manual Review Required By Source Type`

### Case 4 - Chặn approve/reject sai user

1. Dùng request đang `Pending Approval`
2. Đăng nhập bằng user khác `Material Approver`
3. Thử `Approve Material Request` hoặc `Reject Material Request`

Kết quả mong đợi:

- hệ thống chặn

### Case 5 - Approve/reject đúng user

1. Đăng nhập đúng `Material Approver`
2. Thử `Approve Material Request`
3. Hoặc `Reject Material Request`

Kết quả mong đợi:

- hệ thống cho thao tác thành công
- `Material Approval Decided By / At` được ghi đúng

## 15. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML parse bằng parser chuẩn Python: `OK`

## 16. File đã thay đổi

- [maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
