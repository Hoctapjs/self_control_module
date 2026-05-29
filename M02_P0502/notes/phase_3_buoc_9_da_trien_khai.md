# Phase 3 - Bước 9 đã triển khai

## 1. Mục tiêu của bước này

`Bước 9` trong `Phase 3` tập trung vào việc nâng `FSM task` từ mức:

- có context từ request

lên mức:

- có `execution package` chuẩn hóa hơn ngay khi task được tạo

Mục tiêu là để kỹ thuật viên khi mở `FSM task` không chỉ thấy:

- request nào
- store nào
- proposal nào

mà còn thấy ngay:

- hướng dẫn công việc chuẩn
- checklist thực thi mẫu
- gợi ý vật tư / chuẩn bị

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
- `models/project_task.py`
- `models/request_type.py`
- `models/maintenance_equipment.py`
- `views/project_task_views.xml`
- `views/maintenance_equipment_views.xml`

## 3. Hướng triển khai đã chọn

Thay vì:

- tạo task template engine riêng
- thêm object execution package riêng
- hoặc thay đổi workflow `FSM`

hướng triển khai được chọn là:

- thêm template trên master data
- snapshot template đó sang `FSM task` lúc task được tạo

Điểm quan trọng:

- dữ liệu trên task là snapshot readonly
- tách biệt với dữ liệu thực tế do kỹ thuật viên nhập sau này

## 4. Các template mới trên `Request Type`

Đã thêm trên `x_psm_request_type`:

- `0502 FSM Task Template`
- `0502 FSM Checklist Template`
- `0502 FSM Material Template`

Ý nghĩa:

- `Request Type` có thể định nghĩa trước một bộ khung thực thi chuẩn theo loại yêu cầu

Ví dụ:

- loại `repair`
- loại `maintenance`
- loại `inspection`

mỗi loại có thể có package thực thi khác nhau

## 5. Các template mới trên `Equipment Category`

Đã thêm trên `maintenance.equipment.category`:

- `0502 FSM Task Template`
- `0502 FSM Checklist Template`
- `0502 FSM Material Template`

Ý nghĩa:

- ngoài `Request Type`, mỗi `Equipment Category` cũng có thể đóng góp thêm template sát hơn với loại thiết bị thực tế

## 6. Helper mới trên `maintenance.request`

Đã thêm helper:

- `_psm_get_fsm_task_package_values()`

Vai trò:

- gom execution package từ các nguồn dữ liệu hiện có:
  - `Request Type`
  - `Equipment Category`
  - `Service Route`
  - `Material Detail Lines`

Helper này không thay logic tạo task, mà chỉ chuẩn hóa phần package đưa sang task.

## 7. Logic snapshot khi tạo `FSM task`

Khi bấm `Create FSM Task`, ngoài `description` và context đã có từ `Phase 2`, hệ thống sẽ snapshot thêm:

- `0502 Task Template`
- `0502 Execution Checklist Template`
- `0502 Material Package Template`

Nguồn snapshot:

### 7.1. `0502 Task Template`

Được build từ:

- template theo `Request Type`
- template theo `Equipment Category`
- thông tin `Service Route`
- `Service Route Reason`

### 7.2. `0502 Execution Checklist Template`

Được build từ:

- checklist template theo `Request Type`
- checklist template theo `Equipment Category`
- `Inspection Checklist Template` đã có ở `Bước 4`

### 7.3. `0502 Material Package Template`

Được build từ:

- material template theo `Request Type`
- material template theo `Equipment Category`
- tóm tắt các `Material Detail Lines` nếu request đã có khai báo vật tư

## 8. Các field snapshot mới trên `project.task`

Đã thêm trên `project.task`:

- `0502 Task Template`
- `0502 Execution Checklist Template`
- `0502 Material Package Template`

Đặc điểm:

- `readonly`
- `copy=False`
- là snapshot tại thời điểm tạo task

Lý do:

- tránh tình trạng sau này master data thay đổi làm task cũ đổi theo
- giữ đúng ý nghĩa “task được giao với package nào tại thời điểm tạo”

## 9. Tách biệt template và dữ liệu thực tế

Ở bước này cố ý tách:

- `Execution Checklist Template`

khỏi:

- `0502 Execution Checklist`

và tách:

- package hướng dẫn

khỏi:

- `0502 Technical Worksheet`
- `0502 Material Used Note`

Ý nghĩa:

- template là cái để tham chiếu
- còn dữ liệu thực tế là cái kỹ thuật viên ghi khi làm việc

## 10. Thay đổi ở giao diện

### 10.1. `Equipment Category`

Đã cập nhật form/list để cấu hình được:

- `0502 FSM Task Template`
- `0502 FSM Checklist Template`
- `0502 FSM Material Template`

### 10.2. `FSM Task`

Trong tab `0502 Context`, đã thêm nhóm:

- `0502 Task Package`

Nhóm này hiển thị:

- `0502 Task Template`
- `0502 Execution Checklist Template`
- `0502 Material Package Template`

chỉ khi task có dữ liệu tương ứng

## 11. Vì sao triển khai theo cách này

Lý do chọn hướng này:

- bám đúng phần còn thiếu được nêu trong plan:
  - task template theo loại request
  - checklist / vật tư chuẩn theo loại công việc
- không tạo object task template riêng quá sớm
- không làm nặng luồng `FSM`
- vẫn mang lại giá trị vận hành thực tế ngay cho kỹ thuật viên

## 12. Các phần cố ý chưa làm

Ở bước này chưa làm:

- task template engine riêng
- workflow task riêng theo template
- activity template tự động
- subtask auto-generation
- material reservation riêng trên task
- approval riêng cho execution package

Các phần đó nếu cần thì phù hợp hơn ở bước sâu hơn hoặc phase sau.

## 13. Case test đề xuất

### Case 1 - Template theo Equipment Category

1. vào `Equipment Category`
2. cấu hình:
   - `0502 FSM Task Template`
   - `0502 FSM Checklist Template`
   - `0502 FSM Material Template`
3. mở request có `equipment_id` thuộc category đó
4. bấm `Create FSM Task`
5. kỳ vọng trên task có:
   - `0502 Task Template`
   - `0502 Execution Checklist Template`
   - `0502 Material Package Template`

### Case 2 - Có `Material Detail Lines`

1. mở request đã có `Material Detail Lines`
2. bấm `Create FSM Task`
3. kiểm tra `0502 Material Package Template`
4. kỳ vọng phần package có tóm tắt các dòng vật tư đã khai

### Case 3 - Có `Service Route`

1. mở request đã có:
   - `Service Route`
   - `Service Route Reason`
2. bấm `Create FSM Task`
3. kiểm tra `0502 Task Template`
4. kỳ vọng package có phần route context đi kèm

## 14. File đã thay đổi

- `models/request_type.py`
- `models/maintenance_equipment.py`
- `models/maintenance_request.py`
- `models/project_task.py`
- `views/maintenance_equipment_views.xml`
- `views/project_task_views.xml`
