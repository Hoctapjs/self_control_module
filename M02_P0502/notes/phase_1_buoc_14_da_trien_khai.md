# Phase 1 - Bước 14 đã triển khai

## 1. Mục tiêu của bước 14

Bước 14 trong quy trình 0502 là:

- kiểm tra xem trong quá trình xử lý có phát sinh nhu cầu vật tư hay không
- xác định request có đi tiếp sang nhánh kho hay không

Trong `Phase 1`, mục tiêu của bước này là:

- có điểm xác định tối thiểu:
  - có phát sinh vật tư
  - không phát sinh vật tư
- có ghi chú giải thích kết quả đánh giá
- có dấu vết ai là người đã xác nhận bước này

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 14 được triển khai theo hướng rất gọn:

- chưa tạo chứng từ kho ở ngay bước này
- chưa đi sâu vào `stock` hay `industry_fsm_stock`
- chưa làm decision node phức tạp

Thay vào đó:

- dùng một cờ boolean trên `maintenance.request`
- ghi chú đánh giá vật tư
- đánh dấu thời điểm đã hoàn tất kiểm tra vật tư

Điều này bám đúng định hướng trong plan:

- chỉ cần xác định có đi nhánh kho hay không
- phần tạo chứng từ kho để sang bước 15

## 3. Những gì đã triển khai

### 3.1. Field mới trên `maintenance.request`

Đã bổ sung các field sau:

- `x_psm_0502_has_material_request`
  - xác định request có phát sinh nhu cầu vật tư hay không
- `x_psm_0502_material_assessment_note`
  - ghi chú đánh giá vật tư
- `x_psm_0502_material_checked_by_id`
  - lưu user đã xác nhận bước 14
- `x_psm_0502_material_checked_at`
  - lưu thời điểm xác nhận bước 14

### 3.2. Action nghiệp vụ

Đã bổ sung action:

- `action_psm_mark_material_checked()`

Ý nghĩa:

- đánh dấu rằng request đã được xác định rõ:
  - có phát sinh vật tư
  - hoặc không phát sinh vật tư

Validation hiện tại:

- chỉ request đã hoàn tất `Service Assessment` ở bước 13 mới được đánh dấu bước 14
- nếu request đã đánh dấu `Need Outside Service` thì không cho đi tiếp vào nhánh vật tư nội bộ

## 4. Cập nhật giao diện

### 4.1. Trên form `maintenance.request`

Đã thêm nút:

- `Mark Material Checked`

Đã thêm tab:

- `Material Assessment`

Trong tab này có các trường:

- `Has Material Request`
- `Material Checked By`
- `Material Checked At`
- `Material Assessment Note`

### 4.2. Trên list view

Đã thêm các cột:

- `Has Material Request`
- `Material Checked By`
- `Material Checked At`

### 4.3. Trên search view

Đã thêm các filter:

- `Has Material Request`
- `No Material Request`

Đã thêm group by:

- `Has Material Request`
- `Material Checked By`

## 5. Ý nghĩa của bước này trong luồng 0502

Sau bước 13:

- nếu request vẫn đi theo tuyến xử lý nội bộ

thì bước 14 là nơi xác định:

- có cần kéo sang luồng kho để xuất vật tư không
- hay có thể tiếp tục xử lý mà không cần vật tư

Trong `Phase 1`, quyết định này mới chỉ là:

- một cờ boolean
- một ghi chú giải thích
- một dấu mốc nghiệp vụ

chứ chưa tạo chứng từ kho thật.

## 6. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- tạo stock picking ngay ở bước này
- reservation vật tư
- check tồn kho tự động ở bước 14
- liên kết trực tiếp sang `industry_fsm_stock`
- line chi tiết vật tư

Các phần đó phù hợp hơn với:

- `Bước 15`
- `Bước 16`
- và các phase sau nếu cần làm sâu hơn với kho

## 7. Dữ liệu mẫu nên test

Có thể test với một request đã qua bước 13 và đang đi theo nhánh nội bộ, ví dụ:

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân chảy nước`
- `Approval Status`: `Approved`
- `Need Outside Service`: bỏ chọn
- `Service Assessed By`: đã có
- `Service Assessed At`: đã có

### Case 1: có phát sinh vật tư

Nhập:

- chọn `Has Material Request`
- `Material Assessment Note`:

```text
Cần xuất thêm vật tư để thay ống thoát nước và phụ kiện lắp đặt.
Request sẽ đi tiếp sang bước tạo yêu cầu xuất kho.
```

Sau đó bấm:

- `Mark Material Checked`

Kỳ vọng:

- `Material Checked By` có giá trị
- `Material Checked At` có giá trị
- request được hiểu là sẽ đi tiếp sang nhánh kho ở bước 15

### Case 2: không phát sinh vật tư

Nhập:

- bỏ chọn `Has Material Request`
- `Material Assessment Note`:

```text
Không cần vật tư phát sinh.
Có thể tiếp tục xử lý bằng nguồn lực hiện có.
```

Sau đó bấm:

- `Mark Material Checked`

Kỳ vọng:

- `Material Checked By` có giá trị
- `Material Checked At` có giá trị
- request được hiểu là không cần đi nhánh kho

## 8. Điều cần test

Checklist test tối thiểu:

- request chưa hoàn tất bước 13
  - bấm `Mark Material Checked`
  - kỳ vọng: báo lỗi validation

- request đã `Need Outside Service = True`
  - bấm `Mark Material Checked`
  - kỳ vọng: báo lỗi vì không nên đi nhánh vật tư nội bộ

- request đã hoàn tất bước 13 và xử lý nội bộ
  - chọn `Has Material Request = True`
  - nhập `Material Assessment Note`
  - bấm `Mark Material Checked`
  - kỳ vọng: ghi đúng user và thời điểm

- request đã hoàn tất bước 13 và xử lý nội bộ
  - chọn `Has Material Request = False`
  - nhập `Material Assessment Note`
  - bấm `Mark Material Checked`
  - kỳ vọng: ghi đúng user và thời điểm

- list view hiển thị đúng:
  - cờ `Has Material Request`
  - user xác nhận
  - thời điểm xác nhận

- search view lọc được:
  - `Has Material Request`
  - `No Material Request`

## 9. File đã thay đổi

Các file đã thay đổi trong bước này:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 10. Kết luận

`Phase 1 - Bước 14` đã được triển khai theo hướng:

- nhẹ
- đủ để xác định có cần đi nhánh kho hay không
- có ghi chú và dấu vết người xác nhận
- chưa kéo full flow kho vào quá sớm

Kết quả là:

- `maintenance.request` đã có cờ xác định `Has Material Request`
- có ghi nhận user và thời điểm đánh giá vật tư
- đủ để làm đầu vào cho bước 15 trong `Phase 1`
