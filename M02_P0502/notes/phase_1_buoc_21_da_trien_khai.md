# Phase 1 - Bước 21 đã triển khai

## 1. Mục tiêu của bước 21

Bước 21 trong quy trình 0502 là:

- cửa hàng nghiệm thu
- đánh giá sau bảo trì
- có bước xác nhận hoàn tất

Trong `Phase 1`, mục tiêu của bước này là:

- có một điểm ghi nhận nghiệm thu tối thiểu
- không làm form nghiệm thu quá đặc thù
- tận dụng tối đa cơ chế chuẩn của `maintenance`

## 2. File định hướng và file xác nhận đã dùng

Đã dùng:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`

File source chính dùng để xác nhận:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `odoo/addons/maintenance/models/maintenance.py`
- `odoo/addons/project/models/project_task.py`
- `odoo/addons/industry_fsm/models/project_task.py`

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế
- source code là chuẩn xác nhận cuối cùng

## 3. Cách hiểu nghiệp vụ trong Phase 1

Ở giai đoạn này, bước 21 được hiểu như sau:

- sau khi `Bước 20` đã hoàn tất thi công/sửa chữa
- cửa hàng hoặc người phụ trách nội bộ xác nhận:
  - đã chấp nhận kết quả
  - hoặc còn cần làm tiếp

Trong `Phase 1`, mình không làm:

- biên bản nghiệm thu đặc thù
- chữ ký số riêng
- form đánh giá sâu nhiều tiêu chí

Thay vào đó:

- dùng một kết luận nghiệm thu tối thiểu
- ghi chú đánh giá sau bảo trì
- nếu chấp nhận thì đóng request bằng stage done chuẩn của `maintenance`

## 4. Những gì đã triển khai

### 4.1. Field mới trên `maintenance.request`

Đã bổ sung:

- `x_psm_0502_acceptance_result`
  - kết quả nghiệm thu:
    - `Accepted`
    - `Follow-up Needed`
- `x_psm_0502_acceptance_note`
  - ghi chú kết luận nghiệm thu và đánh giá sau bảo trì
- `x_psm_0502_acceptance_reviewed_by_id`
  - ai xác nhận nghiệm thu
- `x_psm_0502_acceptance_reviewed_at`
  - thời điểm xác nhận nghiệm thu

### 4.2. Action nghiệp vụ

Đã bổ sung:

- `action_psm_mark_acceptance_reviewed()`

Ý nghĩa:

- ghi nhận kết quả nghiệm thu sau bảo trì
- nếu `Accepted` thì đồng thời khép request bằng flow chuẩn của `maintenance`

## 5. Logic hiện tại

Khi bấm `Mark Acceptance Reviewed`, hệ thống sẽ:

1. kiểm tra request đã qua `Bước 20`
   - tức là đã có `Execution Completed At`
2. kiểm tra user đã chọn `Acceptance Result`
3. ghi:
   - `Acceptance Reviewed By`
   - `Acceptance Reviewed At`
4. nếu `Acceptance Result = accepted`
   - tìm stage chuẩn của `maintenance` có `done = True`
   - chuyển request sang stage done đó
   - set `kanban_state = done`
   - để `close_date` chuẩn của Odoo tự được cập nhật theo logic chuẩn
5. nếu `Acceptance Result = follow_up_needed`
   - giữ request mở
   - set `kanban_state = blocked`

## 6. Tận dụng chuẩn Odoo

Ở bước này, mình tận dụng chuẩn:

- `maintenance.stage.done`
- `maintenance.request.close_date`
- `kanban_state`

Điều này giúp:

- không phải tạo cơ chế đóng request riêng
- bám đúng workflow chuẩn của `maintenance`
- dễ báo cáo hơn về sau

## 7. Cập nhật giao diện

### 7.1. Trên form `maintenance.request`

Đã thêm:

- nút `Mark Acceptance Reviewed`
- tab `Acceptance`

Trong tab `Acceptance` đã hiển thị:

- `Acceptance Result`
- `Acceptance Reviewed By`
- `Acceptance Reviewed At`
- `Close Date`
- `Acceptance Note`

### 7.2. Trên list view

Đã thêm các cột:

- `Acceptance Result`
- `Acceptance Reviewed At`

### 7.3. Trên search view

Đã thêm các filter:

- `Acceptance Reviewed`
- `Acceptance Pending`
- `Accepted`
- `Follow-up Needed`

Đã thêm group by:

- `Acceptance Result`
- `Acceptance Reviewed By`

## 8. Ý nghĩa của bước này trong luồng 0502

Sau bước 20:

- kỹ thuật viên đã hoàn tất phần thi công/sửa chữa

thì bước 21 là nơi:

- cửa hàng xác nhận kết quả sau bảo trì
- quyết định request đã thực sự khép lại hay còn phải làm tiếp

Trong `Phase 1`, đây là lớp kết thúc luồng tối thiểu:

- accepted thì đóng request
- follow-up needed thì giữ request mở để xử lý tiếp

## 9. Những gì chưa làm để giữ đúng scope Phase 1

Chưa triển khai:

- biên bản nghiệm thu đúng mẫu doanh nghiệp
- chữ ký của cửa hàng hoặc kỹ thuật viên
- bảng khảo sát/hài lòng sau sửa chữa
- worksheet nghiệm thu riêng
- scoring hoặc đánh giá nhiều tiêu chí

Các phần đó phù hợp hơn với:

- `Phase 2`
- hoặc khi business chốt rõ biểu mẫu nghiệm thu chuẩn

## 10. Dữ liệu mẫu nên test

Có thể test với một request như sau:

- đã có `FSM Task`
- đã `Mark Execution Started`
- đã `Mark Execution Completed`

Sau đó vào tab `Acceptance` để chọn kết quả nghiệm thu.

## 11. Điều cần test

Checklist test tối thiểu:

1. request chưa qua `Bước 20` thì không nên đi tiếp nghiệm thu
2. request đã có `Execution Completed At` thì thấy nút `Mark Acceptance Reviewed`
3. chọn `Accepted` rồi bấm nút:
   - request vào stage done
   - có `close_date`
   - có `Acceptance Reviewed By / At`
4. chọn `Follow-up Needed` rồi bấm nút:
   - request không đóng
   - `kanban_state = blocked`
   - có `Acceptance Reviewed By / At`

## 12. Kiểm tra kỹ thuật đã chạy

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 13. File đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
