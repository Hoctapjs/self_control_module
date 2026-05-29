# Phase 2 - Bước 9 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 9` tập trung vào việc làm mượt bước:

- điều phối nhân viên bảo trì
- tạo `FSM Task` từ `maintenance.request`

Mục tiêu chính là:

- làm cho `FSM Task` tự mang đủ ngữ cảnh nghiệp vụ từ request
- giảm phụ thuộc vào việc user phải bổ sung mô tả thủ công
- giúp kỹ thuật viên mở task ra là hiểu nhanh request đến từ đâu và cần xử lý theo hướng nào

## 2. Tài liệu đã dùng khi triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện đã cũ hơn source code thực tế.
- Khi có khác biệt, source code hiện tại được xem là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
- [project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- chuẩn hóa description mặc định của `FSM Task`
- map thêm dữ liệu từ request sang task:
  - `Request Type`
  - `Inspection Result`
  - `Proposal Summary`
- cân nhắc activity/task template

Hướng triển khai được chọn là:

- không thêm activity template ở bước này
- không đổi workflow FSM chuẩn
- chỉ làm mượt dữ liệu đầu vào của `FSM Task`
- bổ sung hiển thị/search/report trên chính `project.task`

Đây là hướng `custom nhẹ`, đúng với scope đã chốt cho `Phase 2 - Bước 9`.

## 4. Chuẩn hóa description mặc định của FSM task

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm helper:

- `_psm_build_fsm_task_description()`

Hàm này dùng để build description mặc định cho `FSM Task` khi request bấm `Create FSM Task`.

### Dữ liệu được đưa vào description

Description mặc định hiện tại có thể gom các phần sau:

- mô tả gốc của request
- `Request Type`
- `Request Source`
- `Source System`
- `Source Reference`
- `Initial Inspection Result`
- `Equipment Status`
- `Safety Risk Level`
- `Action Urgency`
- `Treatment Proposal Summary`
- `Planning Note`

### Ý nghĩa

Trước bước này:

- task thường chỉ có mô tả gốc
- nhiều ngữ cảnh quan trọng vẫn nằm trên request
- kỹ thuật viên phải quay lại request để tự hiểu thêm

Sau bước này:

- task mở ra đã có context 0502 đầy đủ hơn
- giảm việc user phải copy/paste hoặc ghi lại thủ công

## 5. Thay đổi trong logic tạo FSM task

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_create_fsm_task()` đã được cập nhật:

- thay vì tự ghép đơn giản từ `description + Planning Note`
- giờ dùng:
  - `_psm_build_fsm_task_description()`

Điều này làm cho rule tạo task nhất quán hơn và dễ mở rộng về sau.

## 6. Các field đã thêm trên project.task

Trong [project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py), đã bổ sung thêm các related field:

- `x_psm_0502_source_system`
- `x_psm_0502_inspection_result`
- `x_psm_0502_proposal_summary`

### Ý nghĩa

#### `x_psm_0502_source_system`

Giúp nhìn nhanh task này đến từ upstream nào:

- `Manual Request`
- `Preventive Cron`
- `Helpdesk Ticket`
- `Imported Request`
- `Other`

#### `x_psm_0502_inspection_result`

Giúp nhìn nhanh kết luận kiểm tra ban đầu từ request nguồn.

#### `x_psm_0502_proposal_summary`

Giúp đưa phần đề xuất xử lý sơ bộ sang `FSM Task` để kỹ thuật viên có thể đọc ngay trên task.

## 7. Thay đổi giao diện

Trong [project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml), đã cập nhật:

### Form view

Thêm cụm:

- `0502 Context`

Trong đó hiển thị:

- `0502 Maintenance Request`
- `Store Department`
- `Request Type`
- `Request Source`
- `Source System`
- `Initial Inspection Result`

Ngoài ra, trong tab `Description`, thêm cụm:

- `0502 Summary`

để hiển thị:

- `Proposal Summary`

### List view

Đã thêm các cột optional:

- `Source System`
- `Initial Inspection Result`

### Search view

Đã thêm field search:

- `Source System`
- `Initial Inspection Result`
- `Proposal Summary`

Đã thêm group by:

- `Source System`
- `Initial Inspection Result`

## 8. Ý nghĩa nghiệp vụ của bước này

`Phase 1 - Bước 9` đã tạo được `FSM Task`.

Nhưng sang `Phase 2`, vấn đề thực tế là:

- task vẫn còn “mỏng” về context
- user phải quay lại request nhiều
- khó search hoặc group theo góc nhìn intake/inspection

Sau bước này:

- task mang rõ hơn ngữ cảnh nguồn gốc
- đội kỹ thuật nhìn task dễ hiểu hơn
- màn hình monitoring của `project.task` usable hơn

## 9. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 9`, hiện chưa làm:

- chưa thêm activity template tự động
- chưa thêm checklist/subtask template
- chưa thêm assignment rule tự động theo loại request
- chưa thêm auto-stage logic riêng cho FSM
- chưa thay đổi hành vi chuẩn `Start / Mark as done` của industry_fsm

## 10. Cách test

### Case 1 - Tạo FSM task từ request đã ready

1. Mở một `maintenance.request` đã đủ điều kiện planning
2. Bấm `Create FSM Task`

Kết quả mong đợi:

- task được tạo thành công
- description có context 0502 đầy đủ hơn trước

### Case 2 - Kiểm tra form FSM task

1. Mở `FSM Task` vừa tạo

Kết quả mong đợi:

- thấy cụm `0502 Context`
- thấy `Proposal Summary`

### Case 3 - Kiểm tra monitoring/search

1. Vào `0502 Execution Monitoring`
2. Thử search/group theo:
   - `Source System`
   - `Initial Inspection Result`

Kết quả mong đợi:

- task có thể được lọc và group theo các metadata 0502 mới

## 11. Kiểm tra tĩnh đã chạy

- Python compile: `OK`
- XML well-formed: `OK`

## 12. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
- [project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)
