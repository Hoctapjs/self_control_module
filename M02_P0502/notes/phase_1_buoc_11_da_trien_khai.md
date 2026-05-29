# Phase 1 - Bước 11 đã triển khai

## 1. Mục tiêu của bước 11

Bước 11 trong quy trình 0502 là:

- CMT kiểm tra thực tế chi tiết hơn
- ghi nhận đề xuất phương án xử lý
- ghi nhận chi phí dự kiến
- ghi nhận timeline dự kiến

Trong `Phase 1`, mục tiêu của bước này là:

- có nơi để lưu đề xuất xử lý sơ bộ ngay trên `maintenance.request`
- có dấu vết rõ ràng ai là người chốt đề xuất
- chưa tách thành quy trình báo giá formal riêng

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 11 được hiểu theo hướng:

- chưa làm báo giá độc lập
- chưa làm approval matrix
- chưa tạo object quotation riêng

Thay vào đó:

- dùng chính `maintenance.request` để lưu phương án xử lý sơ bộ
- cho phép nhập chi phí dự kiến và timeline dự kiến
- dùng một action nhẹ để xác nhận rằng request đã được CMT đề xuất phương án

Điều này phù hợp với định hướng trong:

- `phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md`

vì plan của bước 11 xác định rõ:

- ưu tiên `maintenance.request`
- ghi nhận đề xuất ở dạng text, note có cấu trúc
- báo giá formal để Phase 2

## 3. Những gì đã triển khai

### 3.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_treatment_proposal`
  - lưu phương án xử lý sơ bộ
- `x_psm_0502_estimated_cost`
  - lưu chi phí dự kiến
- `x_psm_0502_currency_id`
  - tiền tệ đi kèm chi phí dự kiến
  - đang dùng tiền tệ của công ty
- `x_psm_0502_estimated_timeline`
  - lưu timeline dự kiến ở mức text ngắn
- `x_psm_0502_proposed_by_id`
  - lưu user đã xác nhận đề xuất
- `x_psm_0502_proposed_at`
  - lưu thời điểm xác nhận đề xuất

### 3.2. Action nghiệp vụ

Đã bổ sung action:

- `action_psm_mark_proposed()`

Ý nghĩa:

- dùng để đánh dấu request đã có đề xuất xử lý/báo giá sơ bộ
- tạo dấu vết nghiệp vụ tối thiểu cho bước 11

Validation hiện tại:

- bắt buộc phải có `Treatment Proposal` trước khi bấm `Mark Proposed`
- nếu request đang có kết luận `No Action Needed` thì không cho đánh dấu đề xuất

### 3.3. Cập nhật giao diện

Trên form `maintenance.request`:

- thêm nút `Mark Proposed`
- thêm tab `Treatment Proposal`

Trong tab này có các trường:

- `Treatment Proposal`
- `Estimated Cost`
- `Estimated Timeline`
- `Proposed By`
- `Proposed At`

Trên list view:

- thêm các cột:
  - `Proposed By`
  - `Proposed At`
  - `Estimated Cost`
  - `Estimated Timeline`

Trên search view:

- thêm filter:
  - `Proposed`
  - `Not Proposed`
- thêm group by:
  - `Proposed By`

## 4. Ý nghĩa của bước này trong luồng 0502

Sau các bước trước:

- bước 3: tiếp nhận
- bước 4: kiểm tra ban đầu
- bước 8: lập kế hoạch
- bước 9: điều phối nhân sự
- bước 10: theo dõi thực thi

thì bước 11 là nơi:

- CMT quay lại ghi nhận kết quả kiểm tra chi tiết hơn
- đề xuất cách xử lý cụ thể hơn
- đưa ra mức chi phí và timeline sơ bộ để làm đầu vào cho bước 12

Nói ngắn gọn:

- bước 11 tạo ra “đầu vào để cửa hàng duyệt”
- nhưng trong `Phase 1`, đầu vào này đang ở dạng record đơn giản trên `maintenance.request`

## 5. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai ở bước này:

- báo giá chính thức dạng chứng từ riêng
- approval workflow nhiều cấp
- versioning nhiều lần đề xuất/báo giá
- tách riêng phần vật tư, nhân công, dịch vụ ngoài thành các dòng chi tiết
- cơ chế gửi/duyệt báo giá từ portal

Các phần trên sẽ phù hợp hơn với:

- `Phase 2`
- hoặc các bước sau như bước 12 và bước 13

## 6. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân chảy nước`
- `Request Source`: `Store Request`
- `Request Type`: `Repair`
- `Initial Inspection Result`: `Action Needed`

Trong tab `Treatment Proposal`, nhập ví dụ:

- `Treatment Proposal`:

```text
Kiểm tra lại đường ống thoát nước và vệ sinh dàn lạnh.
Nếu ống thoát bị tắc thì xử lý thông tắc và chạy test lại.
Nếu phát hiện hỏng linh kiện nhỏ thì thay thế trong phạm vi xử lý nội bộ.
```

- `Estimated Cost`: `350000`
- `Estimated Timeline`: `Dự kiến xử lý trong ngày, khoảng 2-3 giờ`

Sau đó bấm:

- `Mark Proposed`

## 7. Điều cần test

Checklist test tối thiểu:

- mở được tab `Treatment Proposal`
- nhập được `Treatment Proposal`
- nhập được `Estimated Cost`
- nhập được `Estimated Timeline`
- bấm `Mark Proposed` không lỗi
- hệ thống ghi đúng:
  - `Proposed By`
  - `Proposed At`
- list view hiển thị được các cột đề xuất
- search view lọc được:
  - `Proposed`
  - `Not Proposed`

Case validation nên test thêm:

- để trống `Treatment Proposal` rồi bấm `Mark Proposed`
  - kỳ vọng: báo lỗi validation
- request có `Initial Inspection Result = No Action Needed`
  - kỳ vọng: không cho đánh dấu đề xuất

## 8. File đã thay đổi

Các file đã thay đổi trong bước này:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 9. Kết luận

`Phase 1 - Bước 11` đã được triển khai theo hướng:

- nhẹ
- dễ test
- đúng tinh thần tận dụng chuẩn Odoo
- chưa đẩy sớm sang báo giá formal

Kết quả là:

- `maintenance.request` đã có nơi lưu đề xuất xử lý sơ bộ
- có dấu vết người đề xuất và thời điểm đề xuất
- đủ làm đầu vào cho bước 12 trong `Phase 1`
