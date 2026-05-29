# Phase 3 - Bước 12 đã triển khai

## Mục tiêu

Hoàn thiện `Bước 12 - Duyệt timeline và cost` theo hướng tối thiểu của `Phase 3`:

- giữ tương thích với flow duyệt 1 cấp đã có từ `Phase 2`
- bổ sung khả năng duyệt `2 cấp` khi phía `store/department` thực sự cần
- không tạo approval engine riêng
- không kéo module `approval` chuẩn vào ở bước này để tránh over-scope

## Tài liệu đã dùng để triển khai

- convention:
  - `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- structure map:
  - `addons/M02_P0502/structure/module_map.json`
- kế hoạch chi tiết:
  - `addons/M02_P0502/notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md`
- source xác nhận chính:
  - `addons/M02_P0502/models/hr_department.py`
  - `addons/M02_P0502/models/maintenance_request.py`
  - `addons/M02_P0502/views/hr_department_views.xml`
  - `addons/M02_P0502/views/maintenance_request_views.xml`

## Lưu ý về source và structure map

- `module_map.json` hiện cũ hơn source.
- Source code hiện tại là chuẩn cuối cùng.
- Nếu cần dùng lại `module_map.json` để điều hướng trong các bước sau, nên regenerate lại map.

## Hướng triển khai đã chọn

`Phase 2` đã có:

- resolve approver
- auto approve dưới limit
- owner phía `store` được ưu tiên trước `maintenance.team`

Ở `Phase 3 - Bước 12`, thay vì làm approval nhiều tầng tổng quát, bước này chỉ bổ sung:

- một `final approver` tùy chọn ở phía `store department`
- metadata để nhìn được request đang ở flow 1 cấp hay 2 cấp
- logic chuyển từ cấp 1 sang cấp 2 khi request dùng two-level approval

## Các field mới đã thêm

### Trên `hr.department`

- `x_psm_0502_proposal_final_approver_id`
  - `0502 Store Final Approver`
  - dùng để cấu hình người duyệt cấp cuối ở phía store nếu doanh nghiệp cần 2 cấp duyệt cho proposal

### Trên `maintenance.request`

- `x_psm_0502_approval_flow_type`
  - `single_level`
  - `two_level`

- `x_psm_0502_approval_level_count`
  - tổng số cấp duyệt được resolve cho request

- `x_psm_0502_approval_current_level`
  - request đang chờ duyệt ở cấp nào

- `x_psm_0502_approval_initial_user_id`
  - approver cấp đầu tại thời điểm submit

- `x_psm_0502_approval_final_user_id`
  - approver cấp cuối nếu flow là 2 cấp

- `x_psm_0502_approval_first_decided_by_id`
  - ai đã hoàn tất cấp duyệt đầu tiên

- `x_psm_0502_approval_first_decided_at`
  - thời điểm hoàn tất cấp duyệt đầu tiên

## Helper mới

### `_psm_get_proposal_approval_flow_resolution()`

Helper này bọc trên logic `_psm_get_proposal_approval_resolution()` của `Phase 2`.

Nhiệm vụ:

- lấy kết quả resolve approver/cost rule hiện có
- xác định request là:
  - `single_level`
  - hay `two_level`
- chỉ bật `two_level` khi:
  - request cần manual approval
  - department có `Store Final Approver`
  - final approver khác approver cấp đầu

## Logic nghiệp vụ hiện tại

### Case 1: Auto approve dưới limit

Request vẫn đi như `Phase 2`:

- `Approval Required = False`
- `Approval Status = Approved`
- không đi vào pending

### Case 2: Manual approval, không có final approver

Request vẫn đi `1 cấp` như cũ:

- `Approval Flow Type = Single-Level Approval`
- `Approval Level Count = 1`
- `Current Approval Level = 1`
- approver hiện hành là approver đã resolve ban đầu

### Case 3: Manual approval, có final approver

Request đi `2 cấp`:

#### Khi submit

- `Approval Flow Type = Two-Level Approval`
- `Approval Level Count = 2`
- `Current Approval Level = 1`
- `Proposal Approver` là approver cấp đầu
- `Final Proposal Approver` là approver cấp cuối

#### Khi cấp 1 approve

Request chưa `approved` ngay.

Hệ thống sẽ:

- giữ `Approval Status = Pending`
- chuyển `Proposal Approver` sang `Final Proposal Approver`
- đổi `Approval Rule = Store Final Approver`
- đổi `Current Approval Level = 2`
- ghi:
  - `First Approval Decided By`
  - `First Approval Decided At`

#### Khi cấp 2 approve

Request mới được:

- `Approval Status = Approved`
- ghi `Approval Decided By`
- ghi `Approval Decided At`

## Các thay đổi trên giao diện

### `hr.department`

Đã hiển thị thêm:

- `0502 Store Final Approver`

### Tab `Approval` trên `maintenance.request`

Đã hiển thị thêm:

- `Approval Flow Type`
- `Approval Level Count`
- `Current Approval Level`
- `Initial Proposal Approver`
- `Final Proposal Approver`
- `First Approval Decided By`
- `First Approval Decided At`

Mục tiêu là để user nhìn được ngay:

- request đang duyệt 1 cấp hay 2 cấp
- hiện đang chờ ai
- cấp đầu đã xong chưa

### Search / Filter / Group By

Đã thêm filter:

- `Two-Level Approval`
- `Pending Final Approval`

Đã thêm group by:

- `Approval Flow Type`
- `Current Approval Level`

## Các file đã thay đổi

- `addons/M02_P0502/models/hr_department.py`
- `addons/M02_P0502/models/maintenance_request.py`
- `addons/M02_P0502/views/hr_department_views.xml`
- `addons/M02_P0502/views/maintenance_request_views.xml`

## Kiểm tra tĩnh đã thực hiện

- Python compile:
  - `OK`
- XML parse bằng parser chuẩn Python:
  - `OK`

## Các phần cố ý chưa làm

Để tránh làm dư hơn yêu cầu của lưu đồ và plan `Phase 3`, bước này chưa làm:

- approval engine nhiều tầng tổng quát
- matrix duyệt theo nhiều chiều phức tạp
  - store
  - team
  - request type
  - cost range
- delegation / substitute approver
- escalations / reminder tự động
- tích hợp module `approval`

## Cách test đề xuất

### Case 1: Flow 1 cấp

1. Cấu hình `0502 Store Proposal Approver`
2. Không cấu hình `0502 Store Final Approver`
3. Mở request đã `Mark Proposed`
4. Bấm `Submit for Approval`
5. Kỳ vọng:
   - `Approval Flow Type = Single-Level Approval`
   - `Approval Level Count = 1`
   - `Current Approval Level = 1`
6. Dùng đúng approver bấm `Approve Proposal`
7. Kỳ vọng:
   - `Approval Status = Approved`

### Case 2: Flow 2 cấp

1. Cấu hình:
   - `0502 Store Proposal Approver`
   - `0502 Store Final Approver`
2. Đảm bảo 2 user này khác nhau
3. Mở request đã `Mark Proposed`
4. Bấm `Submit for Approval`
5. Kỳ vọng:
   - `Approval Flow Type = Two-Level Approval`
   - `Approval Level Count = 2`
   - `Current Approval Level = 1`
6. Đăng nhập approver cấp 1, bấm `Approve Proposal`
7. Kỳ vọng:
   - `Approval Status = Pending`
   - `Current Approval Level = 2`
   - `Proposal Approver` đổi sang final approver
   - có `First Approval Decided By/At`
8. Đăng nhập final approver, bấm `Approve Proposal`
9. Kỳ vọng:
   - `Approval Status = Approved`
   - có `Approval Decided By/At`

## Kết luận

`Phase 3 - Bước 12` hiện đã được nâng từ:

- `1 cấp duyệt đơn giản`

lên:

- `1 cấp mặc định`
- `2 cấp tùy chọn theo store`

theo hướng tối thiểu, tương thích ngược, và chưa làm phình scope sang approval engine tổng quát.
