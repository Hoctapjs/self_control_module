# Phase 3 - Bước 8 đã triển khai

## 1. Mục tiêu của bước này

`Bước 8` trong `Phase 3` tập trung vào việc nâng phần lập kế hoạch từ mức:

- chỉ có validation `Ready To Plan`
- chỉ có dấu vết `Planned By / Planned At`

lên mức có:

- lịch sử các lần lập kế hoạch
- truy vết các lần đổi lịch / đổi người phụ trách
- lý do re-plan rõ ràng

Mục tiêu là làm cho planning có audit trail tối thiểu nhưng vẫn giữ đúng scope, chưa kéo sang workflow planning nặng.

## 2. Tài liệu đã dùng để triển khai

### Convention

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`

### Structure map

- `structure/module_map.json`

Lưu ý:

- `module_map.json` hiện cũ hơn source code
- source code hiện tại là chuẩn cuối cùng

### Source xác nhận chính

- `notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md`
- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `models/request_planning_history.py`

## 3. Hướng triển khai đã chọn

Thay vì kéo module `planning` hoặc tạo planning board riêng ngay ở bước này, hướng triển khai được chọn là:

- thêm `planning history` riêng trên `maintenance.request`
- ghi lại mỗi lần:
  - lập kế hoạch lần đầu
  - hoặc đổi lịch / đổi người phụ trách / đổi planning note
- bắt buộc có lý do khi re-plan

Đây là hướng bám sát plan đã điều chỉnh:

- có audit rõ khi đổi lịch
- nhưng chưa mở rộng sang resource planning object riêng

## 4. Model mới đã thêm

Đã thêm model mới:

- `x_psm_request_planning_history`

File:

- `models/request_planning_history.py`

Model này dùng để lưu từng revision planning của một `maintenance.request`.

## 5. Các field trên planning history

Trên `x_psm_request_planning_history`, đã thêm:

- `Maintenance Request`
- `Revision`
- `Change Type`
  - `Initial Plan`
  - `Replan`
- `Scheduled Date`
- `Scheduled End`
- `Responsible`
- `Planning Note Snapshot`
- `Change Reason`
- `Changed By`
- `Changed At`

Ý nghĩa:

- mỗi lần plan hoặc re-plan sẽ được chụp lại như một snapshot riêng

## 6. Các field mới trên `maintenance.request`

Đã thêm:

- `Planning Change Reason`
- `Planning History`
- `Planning Revision Count`
- `Last Planning Changed By`
- `Last Planning Changed At`

Ý nghĩa:

- `Planning Change Reason`
  - dùng khi request đã được plan rồi và cần đổi lịch / đổi owner / đổi planning note
- `Planning History`
  - xem toàn bộ revision planning ngay trên form request
- `Planning Revision Count`
  - nhìn nhanh request đã re-plan bao nhiêu lần
- `Last Planning Changed By / At`
  - nhìn nhanh ai là người đổi planning gần nhất và đổi lúc nào

## 7. Logic đã triển khai

### 7.1. Khi lập kế hoạch lần đầu

Khi bấm `Mark Planned`:

- hệ thống vẫn dùng validation planning hiện có
- ghi `Planned By`
- ghi `Planned At`
- nếu request chưa có `Planning History`, hệ thống tự tạo:
  - revision `1`
  - `Change Type = Initial Plan`

### 7.2. Khi đổi planning sau khi đã planned

Nếu request đã có `Planned At` và user sửa một trong các field:

- `Scheduled Date`
- `Scheduled End`
- `Responsible`
- `Planning Note`

thì hệ thống sẽ:

- yêu cầu phải có `Planning Change Reason`
- tạo thêm một dòng `Planning History`
- `Change Type = Replan`
- tăng `Planning Revision Count`
- cập nhật `Last Planning Changed By`
- cập nhật `Last Planning Changed At`

## 8. Helper đã thêm

Đã thêm helper:

- `_psm_create_planning_history_line()`

Vai trò:

- tạo một snapshot planning history dùng chung cho:
  - lần plan đầu tiên
  - các lần re-plan sau đó

## 9. Thay đổi ở giao diện

### 9.1. Tab `Planning`

Đã bổ sung:

- `Planning Revision Count`
- `Last Planning Changed By`
- `Last Planning Changed At`
- `Planning Change Reason`
- bảng `Planning History`

### 9.2. List view

Đã bổ sung các cột optional:

- `Planning Revision Count`
- `Last Planning Changed By`
- `Last Planning Changed At`

### 9.3. Search view

Đã bổ sung filter:

- `Has Planning History`
- `Replanned`

Đã bổ sung group by:

- `Planning Revision Count`
- `Last Planning Changed By`

## 10. Vì sao triển khai theo cách này

Lý do chọn hướng này:

- bám đúng phần còn thiếu của `Phase 3 - Bước 8`
  - audit rõ khi đổi lịch
- không tạo planning board riêng khi chưa thật sự cần
- không kéo module `planning` vào quá sớm
- vẫn cho phép truy vết đủ rõ ở mức vận hành

## 11. Các phần cố ý chưa làm

Ở bước này chưa làm:

- planning board / calendar nguồn lực riêng
- allocation engine cho kỹ thuật viên
- reschedule approval workflow riêng
- activity / escalation khi đổi lịch nhiều lần
- object planning case riêng ngoài request

Các phần đó nếu cần thì sẽ phù hợp hơn ở bước sâu hơn hoặc phase sau.

## 12. Case test đề xuất

### Case 1 - Initial Plan

1. Mở request đã `Ready To Plan`
2. điền:
   - `Scheduled Date`
   - `Scheduled End`
   - `Responsible`
3. bấm `Mark Planned`
4. kỳ vọng:
   - có `Planned By`
   - có `Planned At`
   - `Planning Revision Count = 1`
   - `Planning History` có 1 dòng `Initial Plan`

### Case 2 - Replan không có lý do

1. Mở request đã planned
2. sửa `Scheduled Date` hoặc `Responsible`
3. không điền `Planning Change Reason`
4. kỳ vọng:
   - hệ thống chặn lưu

### Case 3 - Replan có lý do

1. Mở request đã planned
2. sửa `Scheduled Date`, `Scheduled End`, `Responsible`, hoặc `Planning Note`
3. điền `Planning Change Reason`
4. lưu lại
5. kỳ vọng:
   - tạo thêm 1 dòng `Planning History`
   - `Change Type = Replan`
   - `Planning Revision Count` tăng
   - `Last Planning Changed By / At` được cập nhật

## 13. File đã thay đổi

- `models/request_planning_history.py`
- `models/maintenance_request.py`
- `models/__init__.py`
- `views/maintenance_request_views.xml`
- `security/ir.model.access.csv`
