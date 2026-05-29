## 1. Mục đích

File này tổng hợp các file đã được triển khai để hoàn thành `Phase 1` của quy trình `0502`, từ `Bước 1` đến `Bước 21`.

Tài liệu này dùng để:

- nhìn nhanh toàn bộ phạm vi code đã chạm trong `Phase 1`
- đối chiếu bước nghiệp vụ với file kỹ thuật tương ứng
- hỗ trợ review, handover, estimate cho `Phase 2`

## 2. Nguồn dùng để tổng hợp

Khi tổng hợp tài liệu này, đã dùng:

- convention:
  - [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)
- structure map:
  - [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)
- source xác nhận chính:
  - [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
  - [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
  - [models/maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
  - [models/hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
  - [models/project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
  - [models/stock_picking.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/stock_picking.py)
  - [models/purchase_order.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/purchase_order.py)
  - [models/request_source.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_source.py)
  - [models/request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
  - [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
  - [views/maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
  - [views/hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
  - [views/project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)
  - [views/stock_picking_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/stock_picking_views.xml)
  - [views/purchase_order_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/purchase_order_views.xml)

Lưu ý:

- `module_map.json` hiện đang cũ hơn source code thực tế.
- Source code hiện tại được xem là chuẩn xác nhận cuối cùng.

## 3. Danh sách file triển khai của Phase 1

### 3.1. File manifest

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)

Vai trò:

- khai báo dependency chuẩn cho `Phase 1`
- nạp data, security, views
- mở rộng dần dependency sang `industry_fsm`, `stock`, `purchase`, `purchase_stock`

### 3.2. File data

- [data/request_source_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/request_source_data.xml)
- [data/request_type_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/request_type_data.xml)
- [data/ir_cron_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/ir_cron_data.xml)

Vai trò:

- seed master data nguồn yêu cầu
- seed master data loại yêu cầu
- khai báo cron sinh preventive request

### 3.3. File model

- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/request_source.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_source.py)
- [models/request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [models/maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [models/hr_department.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/hr_department.py)
- [models/project_task.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/project_task.py)
- [models/stock_picking.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/stock_picking.py)
- [models/purchase_order.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/purchase_order.py)

Vai trò:

- `request_source.py`, `request_type.py`
  - 2 model mới cho master data nền của `0502`
- `maintenance_request.py`
  - file trung tâm của toàn bộ `Phase 1`
  - chứa phần lớn field, action, compute, validation từ `Bước 1` đến `Bước 21`
- `maintenance_equipment.py`
  - phục vụ preventive schedule và cron ở `Bước 5`
- `hr_department.py`
  - phục vụ map `Store Department -> FSM Customer` cho `Bước 9`
- `project_task.py`
  - phục vụ theo dõi, liên kết và báo cáo FSM
- `stock_picking.py`
  - phục vụ liên kết phiếu kho với request `0502`
- `purchase_order.py`
  - phục vụ liên kết PO/RFQ với request `0502`

### 3.4. File view

- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [views/maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [views/hr_department_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/hr_department_views.xml)
- [views/project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)
- [views/stock_picking_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/stock_picking_views.xml)
- [views/purchase_order_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/purchase_order_views.xml)

Vai trò:

- `maintenance_request_views.xml`
  - file giao diện trung tâm của `Phase 1`
  - chứa hầu hết button, tab, field, filter, group by của 21 bước
- `maintenance_equipment_views.xml`
  - cấu hình preventive schedule
- `hr_department_views.xml`
  - cấu hình partner đại diện cho department/store
- `project_task_views.xml`
  - hỗ trợ monitoring FSM execution
- `stock_picking_views.xml`
  - hiển thị liên kết ngược về request `0502`
- `purchase_order_views.xml`
  - hiển thị liên kết ngược về request `0502` và search theo request

### 3.5. File security

- [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)

Vai trò:

- cấp quyền tối thiểu cho các model mới của `0502`

## 4. Ma trận bước và file triển khai

### Bước 1

- `models/request_source.py`
- `models/request_type.py`
- `data/request_source_data.xml`
- `data/request_type_data.xml`
- `models/maintenance_request.py`
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
- `data/ir_cron_data.xml`
- `__manifest__.py`

### Bước 6

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- `models/maintenance_equipment.py`

### Bước 7

- `views/maintenance_request_views.xml`

### Bước 8

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 9

- `models/maintenance_request.py`
- `models/project_task.py`
- `models/hr_department.py`
- `views/maintenance_request_views.xml`
- `views/hr_department_views.xml`
- `__manifest__.py`

### Bước 10

- `models/project_task.py`
- `views/project_task_views.xml`
- `views/maintenance_request_views.xml`

### Bước 11

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 12

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 13

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 14

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 15

- `models/maintenance_request.py`
- `models/stock_picking.py`
- `views/maintenance_request_views.xml`
- `views/stock_picking_views.xml`
- `__manifest__.py`

### Bước 16

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 17

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 18

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 19

- `models/maintenance_request.py`
- `models/purchase_order.py`
- `views/maintenance_request_views.xml`
- `views/purchase_order_views.xml`
- `__manifest__.py`

### Bước 20

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

### Bước 21

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 5. File trung tâm của toàn bộ Phase 1

Nếu phải chỉ ra các file “xương sống” của `Phase 1`, thì đó là:

- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)

Lý do:

- `maintenance_request.py`
  - gánh phần lớn logic nghiệp vụ của 21 bước
- `maintenance_request_views.xml`
  - gánh phần lớn giao diện, nút thao tác, tab, filter, group by
- `__manifest__.py`
  - phản ánh phạm vi mở rộng dependency của `Phase 1`

## 6. Danh sách note theo từng bước

Đã có đầy đủ note riêng cho từng bước:

- [phase_1_buoc_1_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_1_da_trien_khai.md)
- [phase_1_buoc_2_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_2_da_trien_khai.md)
- [phase_1_buoc_3_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_3_da_trien_khai.md)
- [phase_1_buoc_4_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_4_da_trien_khai.md)
- [phase_1_buoc_5_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_5_da_trien_khai.md)
- [phase_1_buoc_6_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_6_da_trien_khai.md)
- [phase_1_buoc_7_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_7_da_trien_khai.md)
- [phase_1_buoc_8_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_8_da_trien_khai.md)
- [phase_1_buoc_9_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_9_da_trien_khai.md)
- [phase_1_buoc_10_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_10_da_trien_khai.md)
- [phase_1_buoc_11_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_11_da_trien_khai.md)
- [phase_1_buoc_12_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_12_da_trien_khai.md)
- [phase_1_buoc_13_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_13_da_trien_khai.md)
- [phase_1_buoc_14_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_14_da_trien_khai.md)
- [phase_1_buoc_15_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_15_da_trien_khai.md)
- [phase_1_buoc_16_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_16_da_trien_khai.md)
- [phase_1_buoc_17_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_17_da_trien_khai.md)
- [phase_1_buoc_18_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_18_da_trien_khai.md)
- [phase_1_buoc_19_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_19_da_trien_khai.md)
- [phase_1_buoc_20_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_20_da_trien_khai.md)
- [phase_1_buoc_21_da_trien_khai.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_1_buoc_21_da_trien_khai.md)

## 7. Kết luận ngắn

Sau `Phase 1`, các file đã triển khai để chạy được toàn bộ 21 bước tập trung chủ yếu vào:

- 1 file model trung tâm:
  - `models/maintenance_request.py`
- 1 file view trung tâm:
  - `views/maintenance_request_views.xml`
- các file mở rộng chuẩn Odoo theo từng nhánh:
  - `maintenance_equipment`
  - `hr.department`
  - `project.task`
  - `stock.picking`
  - `purchase.order`
- 2 model master data mới:
  - `x_psm_request_source`
  - `x_psm_request_type`

Nếu bước sau cần review, refactor, estimate hoặc tách `Phase 2`, nên bắt đầu từ:

- `maintenance_request.py`
- `maintenance_request_views.xml`
- `__manifest__.py`

vì đây là 3 file phản ánh rõ nhất phạm vi kỹ thuật của `Phase 1`.
