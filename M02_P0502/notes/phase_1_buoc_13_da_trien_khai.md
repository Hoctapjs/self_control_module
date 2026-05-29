# Phase 1 - Bước 13 đã triển khai

## 1. Mục tiêu của bước 13

Bước 13 trong quy trình 0502 là:

- thẩm định máy móc sau khi cửa hàng đã duyệt proposal
- xác định tiếp tục xử lý nội bộ
- hoặc chuyển sang hướng cần dịch vụ ngoài

Trong `Phase 1`, mục tiêu của bước này là:

- có điểm phân nhánh tối thiểu giữa:
  - xử lý nội bộ
  - cần thuê ngoài
- có ghi chú giải thích kết quả thẩm định
- có dấu vết ai là người đã chốt kết quả thẩm định

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 13 được triển khai theo hướng rất gọn:

- chưa làm full outside service flow
- chưa tạo object hay chứng từ dịch vụ ngoài riêng
- chưa nối sang quy trình mua dịch vụ ngoài

Thay vào đó:

- dùng một cờ đơn giản trên `maintenance.request`
- ghi chú lý do
- đánh dấu thời điểm đã thẩm định

Điều này phù hợp với định hướng trong plan:

- chỉ cần biết request sẽ đi nhánh nội bộ hay nhánh dịch vụ ngoài
- phần “outside service” đầy đủ để cho giai đoạn sau

## 3. Những gì đã triển khai

### 3.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_need_outside_service`
  - xác định request có cần thuê dịch vụ ngoài hay không
- `x_psm_0502_service_assessment_note`
  - ghi chú thẩm định giải thích lý do
- `x_psm_0502_service_assessed_by_id`
  - lưu user đã thực hiện thẩm định bước 13
- `x_psm_0502_service_assessed_at`
  - lưu thời điểm thẩm định

### 3.2. Action nghiệp vụ

Đã bổ sung action:

- `action_psm_mark_service_assessed()`

Ý nghĩa:

- đánh dấu rằng request đã được thẩm định theo hướng:
  - xử lý nội bộ
  - hoặc cần dịch vụ ngoài

Validation hiện tại:

- chỉ request đã `Approved` ở bước 12 mới được thẩm định bước 13

## 4. Cập nhật giao diện

### 4.1. Trên form `maintenance.request`

Đã thêm nút:

- `Mark Service Assessed`

Đã thêm tab:

- `Service Assessment`

Trong tab này có các trường:

- `Need Outside Service`
- `Service Assessed By`
- `Service Assessed At`
- `Service Assessment Note`

### 4.2. Trên list view

Đã thêm các cột:

- `Need Outside Service`
- `Service Assessed By`
- `Service Assessed At`

### 4.3. Trên search view

Đã thêm các filter:

- `Need Outside Service`
- `Internal Service`

Đã thêm group by:

- `Need Outside Service`
- `Service Assessed By`

## 5. Ý nghĩa của bước này trong luồng 0502

Sau bước 12:

- nếu proposal đã được duyệt

thì bước 13 là nơi quyết định:

- request sẽ tiếp tục đi theo tuyến xử lý nội bộ
- hay cần rẽ sang tuyến dịch vụ ngoài

Trong `Phase 1`, quyết định này mới chỉ là:

- một cờ boolean
- một ghi chú giải thích
- một dấu mốc nghiệp vụ

chứ chưa phải là full sub-process “outside service”.

## 6. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- quy trình outside service hoàn chỉnh
- chứng từ gửi nhà cung cấp dịch vụ ngoài
- liên kết sang purchase/service procurement
- nhiều trạng thái xử lý thuê ngoài
- đánh giá SLA riêng cho dịch vụ ngoài

Các phần đó phù hợp hơn với:

- `Phase 2`
- hoặc đặc biệt là `Phase 3`

## 7. Dữ liệu mẫu nên test

Có thể test với một request đã qua bước 12 và đang `Approved`, ví dụ:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân chảy nước`
- `Approval Status`: `Approved`

### Case 1: xử lý nội bộ

Nhập:

- bỏ chọn `Need Outside Service`
- `Service Assessment Note`:

```text
Thiết bị có thể xử lý nội bộ.
Chưa cần thuê nhà cung cấp bên ngoài.
```

Sau đó bấm:

- `Mark Service Assessed`

Kỳ vọng:

- `Service Assessed By` có giá trị
- `Service Assessed At` có giá trị
- request được hiểu là đi tiếp theo nhánh nội bộ

### Case 2: cần dịch vụ ngoài

Nhập:

- chọn `Need Outside Service`
- `Service Assessment Note`:

```text
Thiết bị cần kiểm tra chuyên sâu bởi nhà cung cấp bên ngoài.
Đội nội bộ không đủ phạm vi xử lý ở giai đoạn này.
```

Sau đó bấm:

- `Mark Service Assessed`

Kỳ vọng:

- `Service Assessed By` có giá trị
- `Service Assessed At` có giá trị
- request được hiểu là sẽ rẽ sang nhánh dịch vụ ngoài trong các bước sau

## 8. Điều cần test

Checklist test tối thiểu:

- request chưa `Approved`
  - bấm `Mark Service Assessed`
  - kỳ vọng: báo lỗi validation

- request đã `Approved`
  - chọn `Need Outside Service = False`
  - nhập `Service Assessment Note`
  - bấm `Mark Service Assessed`
  - kỳ vọng: ghi đúng user và thời điểm thẩm định

- request đã `Approved`
  - chọn `Need Outside Service = True`
  - nhập `Service Assessment Note`
  - bấm `Mark Service Assessed`
  - kỳ vọng: ghi đúng user và thời điểm thẩm định

- list view hiển thị đúng:
  - cờ `Need Outside Service`
  - user thẩm định
  - thời điểm thẩm định

- search view lọc được:
  - `Need Outside Service`
  - `Internal Service`

## 9. File đã thay đổi

Các file đã thay đổi trong bước này:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 10. Kết luận

`Phase 1 - Bước 13` đã được triển khai theo hướng:

- nhẹ
- đủ để phân nhánh nội bộ / thuê ngoài
- có ghi chú và dấu vết người thẩm định
- chưa kéo full outside service flow vào quá sớm

Kết quả là:

- `maintenance.request` đã có cờ xác định `Need Outside Service`
- có ghi nhận user và thời điểm thẩm định
- đủ để làm đầu vào cho bước 14 và các bước sau trong `Phase 1`
