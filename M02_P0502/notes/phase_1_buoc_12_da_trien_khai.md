# Phase 1 - Bước 12 đã triển khai

## 1. Mục tiêu của bước 12

Bước 12 trong quy trình 0502 là:

- cửa hàng duyệt timeline
- cửa hàng duyệt chi phí
- nếu không duyệt thì yêu cầu quay lại bước đề xuất để điều chỉnh

Trong `Phase 1`, mục tiêu của bước này là:

- tạo một điểm quyết định tối thiểu trước khi tiếp tục xử lý
- có thể phân biệt được:
  - chờ duyệt
  - đã duyệt
  - bị từ chối
- ghi lại dấu vết người quyết định và thời điểm quyết định

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 12 được triển khai theo hướng tối giản:

- chưa dùng `approval` module
- chưa làm approval matrix nhiều cấp
- chưa làm workflow phê duyệt phức tạp theo vai trò

Thay vào đó:

- dùng chính `maintenance.request`
- thêm trạng thái duyệt đơn giản
- thêm các nút thao tác cơ bản

Điều này bám đúng định hướng trong plan:

- cần có “điểm quyết định tối thiểu”
- custom nhẹ
- chưa đi vào approval flow đầy đủ ngay trong `Phase 1`

## 3. Những gì đã triển khai

### 3.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_approval_status`
  - trạng thái duyệt ở mức đơn giản
  - gồm 3 giá trị:
    - `Pending Approval`
    - `Approved`
    - `Rejected`
- `x_psm_0502_approval_decided_by_id`
  - lưu user đã đưa ra quyết định duyệt/từ chối
- `x_psm_0502_approval_decided_at`
  - lưu thời điểm đưa ra quyết định
- `x_psm_0502_approval_note`
  - lưu ghi chú duyệt hoặc từ chối

### 3.2. Action nghiệp vụ

Đã bổ sung 3 action:

- `action_psm_submit_for_approval()`
- `action_psm_approve_proposal()`
- `action_psm_reject_proposal()`

Ý nghĩa của từng action:

- `Submit for Approval`
  - chuyển request sang trạng thái `pending`
  - dùng khi proposal ở bước 11 đã hoàn tất và cần chờ cửa hàng quyết định

- `Approve Proposal`
  - chuyển request sang trạng thái `approved`
  - ghi lại người duyệt và thời điểm duyệt

- `Reject Proposal`
  - chuyển request sang trạng thái `rejected`
  - ghi lại người từ chối và thời điểm từ chối

### 3.3. Validation hiện tại

Để giữ logic đơn giản nhưng rõ ràng, đã thêm các kiểm tra sau:

- chưa có proposal thì không được `Submit for Approval`
- chỉ request đang ở trạng thái `pending` mới được `Approve` hoặc `Reject`

## 4. Cập nhật giao diện

### 4.1. Trên form `maintenance.request`

Đã thêm các nút:

- `Submit for Approval`
- `Approve Proposal`
- `Reject Proposal`

Đã thêm tab:

- `Approval`

Trong tab này có các trường:

- `Approval Status`
- `Approval Decided By`
- `Approval Decided At`
- `Approval Note`

### 4.2. Trên list view

Đã thêm các cột:

- `Approval Status`
- `Approval Decided By`
- `Approval Decided At`

### 4.3. Trên search view

Đã thêm các filter:

- `Pending Approval`
- `Approved`
- `Rejected`

Đã thêm group by:

- `Approval Status`
- `Approval Decided By`

## 5. Ý nghĩa của bước này trong luồng 0502

Sau khi bước 11 đã ghi nhận:

- phương án xử lý
- chi phí dự kiến
- timeline dự kiến

thì bước 12 là nơi:

- cửa hàng có một điểm ra quyết định tối thiểu
- xác nhận có cho đi tiếp hay không

Nếu hiểu theo logic nghiệp vụ:

- `Pending Approval` = đang chờ cửa hàng xem xét
- `Approved` = có thể tiếp tục sang bước sau
- `Rejected` = cần quay lại điều chỉnh proposal

Trong `Phase 1`, việc “quay lại điều chỉnh” được hiểu ở mức nghiệp vụ là:

- user chỉnh lại dữ liệu trong tab `Treatment Proposal`
- sau đó submit lại

chứ chưa có workflow phức tạp hoặc vòng phê duyệt riêng.

## 6. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- approval matrix nhiều cấp
- rule phân quyền chặt theo nhóm duyệt
- lịch sử nhiều vòng duyệt/từ chối
- gửi thông báo tự động theo luồng duyệt
- liên kết sang module `approval`
- lock dữ liệu proposal sau khi approved

Các phần này phù hợp hơn với:

- `Phase 2`
- hoặc giai đoạn hoàn thiện approval flow sau này

## 7. Dữ liệu mẫu nên test

Có thể test với một request đã hoàn tất bước 11, ví dụ:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân chảy nước`
- `Treatment Proposal`: đã có nội dung
- `Estimated Cost`: `350000`
- `Estimated Timeline`: `Dự kiến xử lý trong ngày, khoảng 2-3 giờ`
- `Proposed By`: đã có
- `Proposed At`: đã có

Sau đó thao tác:

### Case 1: gửi chờ duyệt

- bấm `Submit for Approval`

Kỳ vọng:

- `Approval Status = Pending Approval`

### Case 2: duyệt

- bấm `Approve Proposal`

Kỳ vọng:

- `Approval Status = Approved`
- `Approval Decided By` có giá trị
- `Approval Decided At` có giá trị

### Case 3: từ chối

- với một request khác đang `pending`
- bấm `Reject Proposal`

Kỳ vọng:

- `Approval Status = Rejected`
- `Approval Decided By` có giá trị
- `Approval Decided At` có giá trị

## 8. Điều cần test

Checklist test tối thiểu:

- request chưa có proposal
  - bấm `Submit for Approval`
  - kỳ vọng: báo lỗi validation

- request đã có proposal
  - bấm `Submit for Approval`
  - kỳ vọng: sang `Pending Approval`

- request đang `Pending Approval`
  - bấm `Approve Proposal`
  - kỳ vọng: sang `Approved`

- request đang `Pending Approval`
  - bấm `Reject Proposal`
  - kỳ vọng: sang `Rejected`

- list view hiển thị đúng:
  - trạng thái duyệt
  - người quyết định
  - thời điểm quyết định

- search view lọc được:
  - `Pending Approval`
  - `Approved`
  - `Rejected`

## 9. File đã thay đổi

Các file đã thay đổi trong bước này:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 10. Kết luận

`Phase 1 - Bước 12` đã được triển khai theo hướng:

- có điểm quyết định tối thiểu
- dễ hiểu
- dễ test
- chưa kéo approval framework phức tạp vào quá sớm

Kết quả là:

- request đã có trạng thái chờ duyệt / duyệt / từ chối
- có dấu vết người quyết định và thời điểm quyết định
- đủ để nối tiếp logic từ bước 11 sang các bước sau trong `Phase 1`
