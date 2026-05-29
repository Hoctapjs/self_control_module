# Phase 1 - Bước 17 đã triển khai

## 1. Mục tiêu của bước 17

Bước 17 trong quy trình 0502 là:

- duyệt yêu cầu vật tư nội bộ
- xác nhận request có thể đi tiếp sang nhánh xuất kho thực tế

Trong `Phase 1`, mục tiêu của bước này là:

- tạo một điểm duyệt tối thiểu cho nhánh vật tư nội bộ
- bám trực tiếp trên `maintenance.request`
- chưa tách sang module duyệt dùng chung `approval`

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 17 được triển khai theo hướng gọn:

- chưa tạo approval request riêng
- chưa có nhiều cấp duyệt
- chưa có rule duyệt theo số tiền, cửa hàng, vai trò hay ngưỡng ngân sách

Thay vào đó:

- request sau bước 16 nếu `đủ tồn` sẽ được submit sang trạng thái chờ duyệt vật tư
- người dùng có thể duyệt hoặc từ chối trực tiếp trên `maintenance.request`
- hệ thống lưu lại người quyết định và thời điểm quyết định

Điều này bám đúng định hướng của `Phase 1`:

- giữ luồng 21 bước chạy được end-to-end
- ưu tiên custom nhẹ
- chỉ thêm lớp kiểm soát tối thiểu trước khi đi tiếp sang bước 18

## 3. Nguồn xác nhận đã dùng

Khi triển khai và ghi lại note này, đã dùng:

- file convention:
  - `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- file structure map:
  - `addons/M02_P0502/structure/module_map.json`
- file source chính để xác nhận:
  - `addons/M02_P0502/models/maintenance_request.py`
  - `addons/M02_P0502/views/maintenance_request_views.xml`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code là chuẩn xác nhận cuối cùng

## 4. Những gì đã triển khai

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_material_approval_status`
  - trạng thái duyệt vật tư:
    - `pending`
    - `approved`
    - `rejected`
- `x_psm_0502_material_approval_decided_by_id`
  - user đã duyệt hoặc từ chối
- `x_psm_0502_material_approval_decided_at`
  - thời điểm đã duyệt hoặc từ chối
- `x_psm_0502_material_approval_note`
  - ghi chú duyệt hoặc từ chối cho nhánh vật tư

### 4.2. Action nghiệp vụ

Đã bổ sung 3 action:

- `action_psm_submit_material_approval()`
- `action_psm_approve_material_request()`
- `action_psm_reject_material_request()`

Ý nghĩa:

- `Submit Material Approval`
  - đưa request sang trạng thái chờ duyệt vật tư
- `Approve Material Request`
  - xác nhận chấp thuận nhánh vật tư nội bộ
- `Reject Material Request`
  - xác nhận từ chối nhánh vật tư nội bộ

## 5. Logic hiện tại

Khi bấm `Submit Material Approval`, hệ thống sẽ kiểm tra:

1. request có `Has Material Request = True`
2. request không đi nhánh `Need Outside Service`
3. request đã có `Stock Picking`
4. request đã được kiểm tồn:
   - có `Stock Checked At`
5. kết quả kiểm tồn phải là:
   - `Stock Check Result = available`

Nếu hợp lệ, hệ thống sẽ:

- đặt `Material Approval Status = pending`
- xóa thông tin quyết định cũ:
  - `Material Approval Decided By`
  - `Material Approval Decided At`

Khi bấm `Approve Material Request`:

- chỉ cho phép nếu trạng thái hiện tại là `pending`
- hệ thống cập nhật:
  - `Material Approval Status = approved`
  - `Material Approval Decided By = user hiện tại`
  - `Material Approval Decided At = thời điểm hiện tại`

Khi bấm `Reject Material Request`:

- chỉ cho phép nếu trạng thái hiện tại là `pending`
- hệ thống cập nhật:
  - `Material Approval Status = rejected`
  - `Material Approval Decided By = user hiện tại`
  - `Material Approval Decided At = thời điểm hiện tại`

## 6. Cập nhật giao diện

### 6.1. Trên form `maintenance.request`

Đã thêm các nút:

- `Submit Material Approval`
- `Approve Material Request`
- `Reject Material Request`

Điều kiện hiển thị chính:

- `Submit Material Approval`
  - chỉ hiện khi request đã có `Stock Picking`
  - kết quả kiểm tồn là `available`
  - chưa ở trạng thái `pending`
  - chưa ở trạng thái `approved`
- `Approve Material Request`
  - chỉ hiện khi trạng thái là `pending`
- `Reject Material Request`
  - chỉ hiện khi trạng thái là `pending`

Trong tab `Material Assessment` đã hiển thị thêm:

- `Material Approval Status`
- `Material Approval Decided By`
- `Material Approval Decided At`
- `Material Approval Note`

### 6.2. Trên list view

Đã thêm các cột:

- `Material Approval Status`
- `Material Approval Decided By`
- `Material Approval Decided At`

### 6.3. Trên search view

Đã thêm các filter:

- `Pending Material Approval`
- `Approved Material Request`
- `Rejected Material Request`

Đã thêm group by:

- `Material Approval Status`
- `Material Approval Decided By`

## 7. Ý nghĩa của bước này trong luồng 0502

Sau bước 16:

- request đã biết kho có đủ vật tư hay không

thì bước 17 là nơi xác định:

- nhánh vật tư nội bộ có được chấp thuận để đi tiếp hay không

Trong `Phase 1`, bước này mới chỉ là một điểm duyệt nhẹ:

- không dùng module `approval`
- không có matrix duyệt
- không có rule phân cấp

nhưng đủ để:

- chặn request trước khi đi tiếp sang bước 18
- giữ được dấu vết người quyết định

## 8. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- approval request riêng theo module `approval`
- nhiều cấp duyệt vật tư
- rule duyệt theo mức chi phí hoặc nhóm hàng
- phân vai trò approver theo phòng ban / cửa hàng
- notification riêng cho người duyệt
- lịch sử vòng duyệt nhiều lượt

Các phần đó phù hợp hơn với:

- `Phase 2`
- hoặc các bước/nhánh sâu hơn sau khi chốt rule nghiệp vụ thật

## 9. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã qua bước 14
- đã tạo `Stock Picking`
- đã thêm dòng vật tư vào picking
- đã chạy `Check Stock Availability`
- `Stock Check Result = Stock Available`
- `Need Outside Service = False`

Ví dụ:

- request kiểu:
  - `Có đủ tồn để thay ...`

Sau đó thao tác:

1. bấm `Submit Material Approval`
2. kiểm tra trạng thái chuyển sang `pending`
3. bấm `Approve Material Request`
4. hoặc bấm `Reject Material Request`

## 10. Điều cần test

Checklist test tối thiểu:

- request không có `Has Material Request`
  - bấm `Submit Material Approval`
  - kỳ vọng: báo lỗi validation

- request có `Need Outside Service = True`
  - bấm `Submit Material Approval`
  - kỳ vọng: báo lỗi validation

- request chưa có `Stock Picking`
  - bấm `Submit Material Approval`
  - kỳ vọng: báo lỗi validation

- request chưa chạy bước 16
  - bấm `Submit Material Approval`
  - kỳ vọng: báo lỗi validation

- request có `Stock Check Result = not_available`
  - bấm `Submit Material Approval`
  - kỳ vọng: báo lỗi validation

- request hợp lệ
  - bấm `Submit Material Approval`
  - kỳ vọng:
    - `Material Approval Status = pending`

- request đang `pending`
  - bấm `Approve Material Request`
  - kỳ vọng:
    - `Material Approval Status = approved`
    - có `Material Approval Decided By`
    - có `Material Approval Decided At`

- request đang `pending`
  - bấm `Reject Material Request`
  - kỳ vọng:
    - `Material Approval Status = rejected`
    - có `Material Approval Decided By`
    - có `Material Approval Decided At`

- search view lọc được:
  - `Pending Material Approval`
  - `Approved Material Request`
  - `Rejected Material Request`

## 11. File đã thay đổi

Các file đã thay đổi trong bước này:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 12. Kết luận

`Phase 1 - Bước 17` đã được triển khai theo hướng:

- tạo điểm duyệt tối thiểu cho nhánh vật tư nội bộ
- bám trực tiếp trên `maintenance.request`
- không mở rộng sang approval engine đầy đủ quá sớm

Kết quả là:

- request 0502 đã có thể chờ duyệt vật tư sau bước kiểm tồn
- người dùng có thể duyệt hoặc từ chối ngay trên request
- hệ thống đã có nền để đi tiếp sang bước 18 mà vẫn giữ được kiểm soát luồng
