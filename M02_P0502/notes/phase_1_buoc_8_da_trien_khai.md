# Phase 1 - Bước 8 đã triển khai

## 1. Mục tiêu của bước 8

Bước 8 trong quy trình `0502` là:

- `CMT Lead lập kế hoạch bảo trì máy móc`

Trong `Phase 1`, mục tiêu của bước này không phải là dựng đầy đủ một bài toán `planning` hoàn chỉnh, mà là:

- có nơi ghi nhận kế hoạch xử lý ở mức tối thiểu
- tận dụng tối đa field chuẩn của `maintenance.request`
- có dấu vết rõ ràng rằng request đã được lập kế hoạch

## 2. Cách hiểu nghiệp vụ trong Phase 1

Ở mức triển khai tối thiểu, một request được xem là `đã lập kế hoạch` khi:

- đã có `Scheduled Date`
- đã có `Responsible`
- có thể có thêm ghi chú kế hoạch
- có một thao tác xác nhận rõ ràng để lưu dấu vết

Vì vậy, `Phase 1` chọn cách:

- tận dụng `schedule_date` chuẩn của `maintenance.request`
- tận dụng `user_id` chuẩn của `maintenance.request`
- chỉ bổ sung thêm các field ghi nhận dấu vết lập kế hoạch

Chưa triển khai trong bước này:

- module `planning`
- điều phối theo ca
- planning slot
- phân ca nhiều người
- logic tối ưu tải công việc

## 3. Đã dùng chuẩn Odoo nào

Nguồn chuẩn Odoo được tận dụng:

- `maintenance.request.schedule_date`
- `maintenance.request.schedule_end`
- `maintenance.request.user_id`

Source đối chiếu chính:

- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

## 4. Những gì đã code

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_plan_note`
- `x_psm_0502_planned_by_id`
- `x_psm_0502_planned_at`

Ý nghĩa:

- `x_psm_0502_plan_note`: ghi chú kế hoạch xử lý ở mức nhẹ
- `x_psm_0502_planned_by_id`: ai là người xác nhận request đã được lập kế hoạch
- `x_psm_0502_planned_at`: thời điểm xác nhận lập kế hoạch

### 4.2. Action mới

Đã bổ sung method:

- `action_psm_mark_planned()`

Logic:

- bắt buộc phải có `Scheduled Date`
- bắt buộc phải có `Responsible`
- khi bấm nút, hệ thống ghi:
  - `Planned By`
  - `Planned At`

### 4.3. Giao diện mới

Đã bổ sung trên form view:

- nút `Mark Planned`
- tab `Planning`

Đã bổ sung trên list/search view:

- cột `Planned By`
- cột `Planned At`
- filter `Planned`
- filter `Not Planned`
- group by `Planned By`

## 5. Cách dùng trong Phase 1

Luồng thao tác đề xuất:

1. Mở request từ queue `0502 Requests To Plan`
2. Điền `Scheduled Date`
3. Điền `Responsible`
4. Ghi `Planning Note` nếu cần
5. Bấm `Mark Planned`

Khi đó request sẽ có:

- kế hoạch xử lý cơ bản
- dấu vết người lập kế hoạch
- dấu vết thời điểm lập kế hoạch

## 6. Điều cần test

Checklist test tối thiểu:

- mở được request trong form mà không lỗi
- nhập được `Scheduled Date`
- nhập được `Responsible`
- nhập được `Planning Note`
- bấm được `Mark Planned`
- sau khi bấm, hệ thống ghi đúng:
  - `Planned By`
  - `Planned At`
- filter `Planned` hoạt động đúng
- filter `Not Planned` hoạt động đúng

## 7. Dữ liệu mẫu nên test

Có thể dùng các request thuộc queue lập kế hoạch, ví dụ:

- preventive request đã được notify lead
- store request đã có `Initial Inspection Result = Action Needed`

Ví dụ thao tác test:

- `Scheduled Date`: nhập ngày giờ xử lý dự kiến
- `Responsible`: chọn kỹ thuật viên
- `Planning Note`: `Xử lý vào buổi sáng, ưu tiên kiểm tra trước khu vực quầy thu ngân.`

## 8. Những gì chưa làm để giữ đúng scope

Trong `Phase 1 - Bước 8`, chưa làm các phần sau:

- planning slot
- phân ca theo ngày/ca
- kiểm tra xung đột lịch
- gợi ý người theo skill
- đồng bộ sang module `planning`
- tự động cân tải công việc giữa nhiều kỹ thuật viên

Các phần này nếu cần sẽ phù hợp hơn ở:

- `Phase 2`
- hoặc khi triển khai sâu `Bước 9`

## 9. File đã thay đổi

Các file chính đã thay đổi cho bước này:

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 10. Kết luận

`Phase 1 - Bước 8` đã được triển khai theo hướng:

- bám chuẩn Odoo
- không kéo `planning` vào quá sớm
- đủ để CMT Lead lập kế hoạch ở mức tối thiểu
- có dấu vết rõ ràng để tiếp tục sang bước điều phối ở các bước sau
