# Phase 2 - Bước 13 đã triển khai

## 1. Mục tiêu của bước 13

`Bước 13` trong quy trình `0502` là:

- thẩm định request sẽ xử lý nội bộ
- hay phải chuyển sang nhánh dịch vụ ngoài

Trong `Phase 2`, trọng tâm của bước này là:

- làm rõ nhánh outsource
- không chỉ dùng một cờ `có/không`
- mà phải có thêm dữ liệu có cấu trúc để giải thích quyết định route service

## 2. File định hướng và file xác nhận đã dùng

Đã dùng:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

File source chính dùng để xác nhận:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code hiện tại là chuẩn xác nhận cuối cùng

## 3. Hướng triển khai đã chọn

Ở bước này, đã chọn hướng triển khai:

- custom nhẹ trong `Phase 2`
- chưa tạo object outsource riêng
- chưa dựng full flow vendor service
- vẫn giữ `maintenance.request` là nơi ghi nhận quyết định route service

Mục tiêu là:

- làm rõ request đi nhánh `Internal Handling`
- hay đi nhánh `Outside Service`
- nhưng vẫn tương thích với các bước `Phase 1` đã có

## 4. Những gì đã triển khai

### 4.1. Field structured mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_service_route`
  - xác định route xử lý:
    - `Internal Handling`
    - `Outside Service`

- `x_psm_0502_service_route_reason`
  - ghi nhận lý do route service:
    - `Internal Team Capable`
    - `Specialist Required`
    - `Internal Capacity Shortage`
    - `Vendor / Warranty Handling`
    - `Safety / Compliance Requirement`
    - `Other`

### 4.2. Giữ compatibility với flow cũ

Field cũ vẫn được giữ:

- `x_psm_0502_need_outside_service`

Nhưng ở `Phase 2`, field này không còn là nơi user tự quyết định trực tiếp nữa.

Thay vào đó:

- user chọn `Service Route`
- khi bấm `Mark Service Assessed`
- hệ thống tự sync:
  - `Need Outside Service = True` nếu route là `Outside Service`
  - `Need Outside Service = False` nếu route là `Internal Handling`

Điều này giúp:

- không làm vỡ các bước sau
- vẫn dùng được toàn bộ logic nhánh vật tư, kho và mua ngoài đã có

## 5. Thay đổi trong action nghiệp vụ

Action bị tác động:

- `action_psm_mark_service_assessed()`

Logic mới:

1. request phải có:
   - `Approval Status = Approved`
2. phải điền đủ:
   - `Service Route`
   - `Service Route Reason`
3. nếu thiếu, hệ thống chặn và báo rõ field còn thiếu
4. nếu hợp lệ, hệ thống ghi:
   - `Need Outside Service`
   - `Service Assessed By`
   - `Service Assessed At`

Ý nghĩa:

- quyết định nội bộ hay thuê ngoài giờ có cấu trúc hơn
- không còn chỉ dựa vào một boolean trống/ngẫu nhiên

## 6. Cập nhật giao diện

### 6.1. Trên form `maintenance.request`

Trong tab `Service Assessment`, đã hiển thị:

- `Service Route`
- `Service Route Reason`
- `Need Outside Service` ở chế độ readonly
- `Service Assessed By`
- `Service Assessed At`
- `Service Assessment Note`

Ý đồ UX:

- user chọn route và reason trước
- hệ thống mới suy ra cờ `Need Outside Service`

### 6.2. Trên list view

Đã bổ sung optional columns:

- `Service Route`
- `Service Route Reason`

### 6.3. Trên search view

Đã bổ sung:

- filter:
  - `Need Outside Service`
  - `Internal Service`
  - `Specialist Required`

- group by:
  - `Need Outside Service`
  - `Service Route`
  - `Service Route Reason`
  - `Service Assessed By`

## 7. Ý nghĩa nghiệp vụ của bước này sau khi nâng cấp

Sau khi `Proposal` đã được duyệt, bước 13 giờ trả lời rõ hơn:

- request này nội bộ có đủ năng lực làm không
- hay cần thuê ngoài
- nếu thuê ngoài thì vì:
  - cần chuyên gia
  - thiếu năng lực nội bộ
  - liên quan bảo hành/vendor
  - lý do an toàn/compliance

Nhờ đó:

- quyết định route service rõ ràng hơn
- lead và người theo dõi về sau dễ đọc hơn
- chuẩn bị tốt hơn cho việc thiết kế object outsource riêng ở `Phase 3` nếu cần

## 8. Những gì chưa làm để giữ đúng scope Phase 2

Chưa triển khai:

- object riêng cho outside service
- vendor service request
- service order / subcontract flow
- approval riêng cho quyết định outsource
- cost comparison giữa nội bộ và thuê ngoài
- lịch sử nhiều vòng thẩm định dịch vụ ngoài

Các phần đó phù hợp hơn với:

- `Phase 3`

## 9. Điều cần test

Checklist test tối thiểu:

1. mở một request đã `Approved`
2. vào tab `Service Assessment`
3. để trống:
   - `Service Route`
   - hoặc `Service Route Reason`
4. bấm `Mark Service Assessed`
   - kỳ vọng: bị chặn

5. điền:
   - `Service Route = Internal Handling`
   - `Service Route Reason = Internal Team Capable`
6. bấm lại
   - kỳ vọng:
     - `Need Outside Service = False`
     - có `Service Assessed By`
     - có `Service Assessed At`

7. test thêm case:
   - `Service Route = Outside Service`
   - `Service Route Reason = Specialist Required`
8. bấm lại
   - kỳ vọng:
     - `Need Outside Service = True`
     - filter `Need Outside Service` tìm ra đúng request
     - filter `Specialist Required` tìm ra đúng request

## 10. Kiểm tra kỹ thuật đã chạy

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 11. File đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 12. Kết luận

`Phase 2 - Bước 13` đã được nâng từ:

- boolean route đơn giản

lên mức:

- route có cấu trúc
- có lý do route service
- vẫn tương thích ngược với flow `Phase 1`

Đây là mức triển khai hợp lý cho `Phase 2`:

- tăng độ rõ của dữ liệu
- chưa làm phình scope sang bài toán outsource đầy đủ.
