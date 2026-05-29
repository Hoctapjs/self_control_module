## 1. Mục đích

File này tổng hợp những gì đã được triển khai trong `Phase 2` của quy trình `0502`, dựa trên:

- các note triển khai theo từng bước của `Phase 2`
- source code hiện tại của module

Tài liệu này dùng để:

- nhìn nhanh toàn bộ phạm vi kỹ thuật của `Phase 2`
- đối chiếu bước nghiệp vụ với file kỹ thuật tương ứng
- phục vụ review, handover, estimate cho các phase tiếp theo

## 2. Nguồn dùng để tổng hợp

Khi tổng hợp tài liệu này, đã dùng:

- convention:
  - [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)
- structure map:
  - [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)
- plan chi tiết:
  - [phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md)
- tài liệu tham chiếu:
  - [phase_1_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_da_trien_khai.md)
- source xác nhận chính:
  - [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
  - [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
  - [models/maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
  - [models/hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
  - [models/maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
  - [models/project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
  - [models/stock_picking.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/stock_picking.py)
  - [models/purchase_order.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/purchase_order.py)
  - [models/request_material_line.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_material_line.py)
  - [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
  - [views/maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
  - [views/hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
  - [views/maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
  - [views/project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)
  - [views/stock_picking_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/stock_picking_views.xml)
  - [views/purchase_order_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/purchase_order_views.xml)

Lưu ý:

- `module_map.json` hiện đang cũ hơn source code thực tế.
- Source code hiện tại được xem là chuẩn xác nhận cuối cùng.

## 3. Tổng quan kỹ thuật của Phase 2

So với `Phase 1`, `Phase 2` tập trung vào 5 hướng chính:

- chuẩn hóa dữ liệu đầu vào và nguồn phát sinh request
- làm chắc preventive, queue và readiness trước khi lập kế hoạch
- nâng chất lượng dữ liệu của proposal, approval, vật tư, kho và mua ngoài
- làm rõ ranh giới dữ liệu giữa:
  - `maintenance.request`
  - `project.task`
  - `stock.picking`
  - `purchase.order`
- chuyển các bước cuối từ mức “ghi chú nhẹ” sang mức “dữ liệu có cấu trúc hơn”

`Phase 2` không thay object trung tâm của module.  
Object trung tâm vẫn là:

- `maintenance.request`

Nhưng `Phase 2` làm rõ hơn vai trò của các object vệ tinh:

- `maintenance.equipment`
- `maintenance.team`
- `project.task`
- `stock.picking`
- `purchase.order`
- `x_psm_request_material_line`

## 4. Danh sách file triển khai của Phase 2

### 4.1. File model

- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [models/maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [models/hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
- [models/maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [models/project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
- [models/stock_picking.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/stock_picking.py)
- [models/purchase_order.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/purchase_order.py)
- [models/request_material_line.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_material_line.py)

Vai trò:

- `maintenance_request.py`
  - file trung tâm của hầu hết logic `Phase 2`
  - chứa phần lớn field, helper, validation, action của 21 bước
- `maintenance_equipment.py`
  - làm chắc preventive schedule, preventive status, chống sinh trùng
- `hr_department.py`
  - mở rộng ownership nghiệp vụ ở nhánh duyệt proposal theo store
- `maintenance_team.py`
  - chứa cấu hình lead, approver, stock flow, vendor mặc định
- `project_task.py`
  - mở rộng metadata và dữ liệu thực thi thật của `FSM Task`
- `purchase_order.py`
  - mở rộng liên kết ngược từ PO/RFQ về request 0502
- `request_material_line.py`
  - model mới để cấu trúc hóa vật tư phát sinh

### 4.2. File view

- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [views/maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [views/hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
- [views/maintenance_team_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_team_views.xml)
- [views/project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)
- [views/purchase_order_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/purchase_order_views.xml)

Vai trò:

- `maintenance_request_views.xml`
  - file giao diện trung tâm của `Phase 2`
  - chứa intake, inspection, planning, proposal, approval, material, execution, acceptance
- `maintenance_equipment_views.xml`
  - thêm preventive status và queue/filter preventive
- `hr_department_views.xml`
  - thêm approver phía store cho bước duyệt proposal
- `maintenance_team_views.xml`
  - thêm các cấu hình team dùng cho notify, approval, stock flow, default vendor
- `project_task_views.xml`
  - nâng `FSM Task` thành nơi giữ execution thật
- `purchase_order_views.xml`
  - hiển thị thêm ngữ cảnh 0502 trên RFQ/PO

### 4.3. File security

- [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)

Vai trò:

- cấp quyền tối thiểu cho model mới `x_psm_request_material_line`

## 5. Ma trận bước và file triển khai

### Bước 1

- `models/maintenance_request.py`
- `models/maintenance_equipment.py`
- `views/maintenance_request_views.xml`

### Bước 2

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 3

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 4

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 5

- `models/maintenance_equipment.py`
- `views/maintenance_equipment_views.xml`

### Bước 6

- `models/maintenance_request.py`
- `models/maintenance_team.py`
- `views/maintenance_request_views.xml`
- `views/maintenance_team_views.xml`

### Bước 7

- `views/maintenance_request_views.xml`

### Bước 8

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 9

- `models/maintenance_request.py`
- `models/project_task.py`
- `views/project_task_views.xml`

### Bước 10

- `views/maintenance_request_views.xml`
- `views/project_task_views.xml`

### Bước 11

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 12

- `models/maintenance_request.py`
- `models/maintenance_team.py`
- `models/hr_department.py`
- `views/maintenance_request_views.xml`
- `views/maintenance_team_views.xml`
- `views/hr_department_views.xml`

### Bước 13

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 14

- `models/request_material_line.py`
- `models/maintenance_request.py`
- `models/__init__.py`
- `views/maintenance_request_views.xml`
- `security/ir.model.access.csv`

### Bước 15

- `models/maintenance_request.py`
- `models/maintenance_team.py`
- `views/maintenance_team_views.xml`

### Bước 16

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 17

- `models/maintenance_request.py`
- `models/maintenance_team.py`
- `views/maintenance_request_views.xml`
- `views/maintenance_team_views.xml`

### Bước 18

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 19

- `models/maintenance_request.py`
- `models/maintenance_team.py`
- `models/purchase_order.py`
- `views/maintenance_team_views.xml`
- `views/purchase_order_views.xml`

### Bước 20

- `models/project_task.py`
- `models/maintenance_request.py`
- `views/project_task_views.xml`
- `views/maintenance_request_views.xml`

### Bước 21

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 6. Tóm tắt kết quả theo cụm nghiệp vụ

### 6.1. Intake và nguồn phát sinh

Đã triển khai:

- phân biệt `Request Source` và `Source System`
- thêm:
  - `Source Reference`
  - `Source Mapping Note`
- chuẩn hóa validation intake
- chuẩn hóa dấu vết `CMT Receive`

Kết quả:

- request vào hệ thống rõ nguồn hơn
- giảm tạo request thiếu dữ liệu

### 6.2. Inspection và readiness

Đã triển khai:

- inspection có cấu trúc:
  - symptom
  - equipment status
  - safety risk
  - urgency
- `Ready To Plan`
- `Planning Block Reason`
- queue usable cho `CMT Lead`

Kết quả:

- giảm plan khi request chưa đủ điều kiện
- lead có backlog/queue rõ hơn để xử lý

### 6.3. Preventive và điều phối lead

Đã triển khai:

- `Preventive Status`
- chặn sinh trùng preventive request
- cấu hình `0502 Lead User`
- chuẩn hóa logic notify lead

Kết quả:

- nhánh preventive rõ trạng thái hơn
- tránh việc cron sinh trùng khi request cũ còn mở

### 6.4. Proposal và approval

Đã triển khai:

- proposal có cấu trúc:
  - root cause
  - technical solution
  - cost note
  - timeline note
- approval 1 cấp với rule rõ ràng
- auto approve dưới ngưỡng
- ownership của bước duyệt proposal ưu tiên phía `store`

Kết quả:

- dữ liệu proposal usable hơn
- approval bớt mơ hồ hơn

### 6.5. Vật tư, kho và mua ngoài

Đã triển khai:

- model dòng vật tư phát sinh
- `stock.picking` usable thật từ dữ liệu vật tư
- tách current stock availability và checked snapshot
- approval vật tư nội bộ theo team
- business status cho nhánh xuất kho
- RFQ/PO được prefill từ request 0502

Kết quả:

- nhánh vật tư và mua ngoài liền mạch hơn
- giảm nhập lại dữ liệu

### 6.6. FSM task, execution và acceptance

Đã triển khai:

- `FSM Task` mang đủ context 0502
- `FSM Task` trở thành nơi giữ execution thật
- request chỉ giữ execution summary
- acceptance có cấu trúc hơn:
  - người nghiệm thu
  - vai trò
  - tình trạng thiết bị sau bảo trì
  - follow-up / rework

Kết quả:

- tách rõ trách nhiệm dữ liệu giữa request và task
- các bước cuối của quy trình có tính vận hành tốt hơn

## 7. File trung tâm của toàn bộ Phase 2

Nếu phải chỉ ra các file “xương sống” của `Phase 2`, thì đó là:

- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [models/maintenance_team.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_team.py)
- [views/project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)

Lý do:

- `maintenance_request.py`
  - gánh phần lớn logic nghiệp vụ của `Phase 2`
- `maintenance_request_views.xml`
  - gánh phần lớn UI, filter, queue, monitoring, acceptance
- `maintenance_team.py`
  - là nơi tập trung phần lớn rule cấu hình động của `Phase 2`
- `project_task_views.xml`
  - phản ánh rõ nhất phần chuyển dịch từ request-summary sang task-execution

## 8. Danh sách note theo từng bước

Đã có note riêng cho các bước:

- [phase_2_buoc_1_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_1_da_trien_khai.md)
- [phase_2_buoc_2_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_2_da_trien_khai.md)
- [phase_2_buoc_3_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_3_da_trien_khai.md)
- [phase_2_buoc_4_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_4_da_trien_khai.md)
- [phase_2_buoc_5_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_5_da_trien_khai.md)
- [phase_2_buoc_6_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_6_da_trien_khai.md)
- [phase_2_buoc_7_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_7_da_trien_khai.md)
- [phase_2_buoc_8_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_8_da_trien_khai.md)
- [phase_2_buoc_9_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_9_da_trien_khai.md)
- [phase_2_buoc_10_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_10_da_trien_khai.md)
- [phase_2_buoc_11_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_11_da_trien_khai.md)
- [phase_2_buoc_12_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_12_da_trien_khai.md)
- [phase_2_buoc_13_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_13_da_trien_khai.md)
- [phase_2_buoc_14_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_14_da_trien_khai.md)
- [phase_2_buoc_15_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_15_da_trien_khai.md)
- [phase_2_buoc_16_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_16_da_trien_khai.md)
- [phase_2_buoc_17_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_2_buoc_17_da_trien_khai.md)

Lưu ý:

- tại thời điểm tổng hợp này, các bước `18` đến `21` đã có triển khai trong source code
- nhưng chưa có note riêng đầy đủ theo đúng format từng bước
- phần tổng hợp của tài liệu này cho các bước `18` đến `21` được xác nhận trực tiếp từ source hiện tại

## 9. Kết luận ngắn

Sau `Phase 2`, module `M02_P0502` đã đi từ mức:

- có flow nghiệp vụ chạy được

sang mức:

- dữ liệu rõ ràng hơn
- ranh giới giữa các object rõ hơn
- validation ở các decision point chặt hơn
- queue, monitoring, approval, stock, purchase và acceptance usable hơn cho vận hành

Nếu cần review hoặc lên plan `Phase 3`, nên bắt đầu từ:

- `maintenance_request.py`
- `maintenance_request_views.xml`
- `maintenance_team.py`
- `project_task.py`
- `project_task_views.xml`

vì đây là các file phản ánh rõ nhất phần mở rộng kỹ thuật của `Phase 2`.
