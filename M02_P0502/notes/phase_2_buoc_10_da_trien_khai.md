# Phase 2 - Bước 10 đã triển khai

## 1. Mục tiêu của bước này

`Phase 2 - Bước 10` tập trung vào việc nâng phần theo dõi tình trạng xử lý từ mức:

- monitoring cơ bản

lên mức:

- usable hơn cho `CMT Lead`
- có thể nhìn nhanh backlog đang mở
- có góc nhìn riêng cho:
  - overdue
  - preventive
  - follow-up needed

Mục tiêu chính là:

- không bắt người dùng phải tự lọc tay quá nhiều
- tận dụng `list / kanban / pivot / graph / activity` chuẩn của Odoo
- bổ sung các action/report theo vai trò để mở ra là dùng được ngay

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
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [project_task_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/project_task_views.xml)

## 3. Hướng triển khai đã chọn

Theo plan của `Phase 2`, bước này cần:

- bổ sung action/report theo vai trò
- cân nhắc pivot/graph preset
- thêm KPI tối thiểu:
  - số request mở
  - số overdue
  - số preventive
  - số follow-up needed

Hướng triển khai được chọn là:

- không làm dashboard JS riêng
- không tạo model KPI mới
- không thêm logic tính toán nặng ở backend
- tận dụng `maintenance.request` làm business object chính cho reporting
- giữ `project.task` monitoring hiện có cho phần execution
- bổ sung thêm lớp monitoring ở mức `request`

Đây là hướng `custom nhẹ đến vừa`, đúng với scope của `Phase 2 - Bước 10`.

## 4. Những gì đã thêm

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), đã bổ sung:

### Search filter mới

- `0502 Open Requests`

Ý nghĩa:

- gom tất cả request thuộc luồng `0502`
- đang còn mở
- chưa archive
- chưa done

Filter này là filter nền để mở màn hình monitoring tổng hợp ở mức request.

### Action/report mới

- `0502 Request Monitoring`
- `0502 Preventive Monitoring`
- `0502 Overdue Monitoring`
- `0502 Follow-up Needed`

### Menu reporting mới

Đã thêm 4 menu dưới `Maintenance > Reporting`:

- `0502 Request Monitoring`
- `0502 Preventive Monitoring`
- `0502 Overdue Monitoring`
- `0502 Follow-up Needed`

## 5. Ý nghĩa nghiệp vụ của từng màn hình monitoring

### `0502 Request Monitoring`

Đây là màn hình tổng hợp ở mức `maintenance.request`.

Mục tiêu:

- giúp `CMT Lead` nhìn backlog đang mở của toàn luồng 0502
- nhìn nhanh số request còn sống trong hệ thống
- làm entry point để dùng tiếp các group by, pivot, graph

Mặc định:

- lọc theo `0502 Open Requests`
- group theo `Store Department`

### `0502 Preventive Monitoring`

Màn hình này tập trung riêng vào preventive request.

Mục tiêu:

- theo dõi riêng nhánh bảo trì định kỳ
- xem nhanh preventive request theo team

Mặc định:

- lọc theo `Preventive Request`
- group theo `Team`

### `0502 Overdue Monitoring`

Màn hình này tập trung riêng vào request quá hạn hoặc tồn đọng.

Mục tiêu:

- giúp lead ưu tiên xử lý các request trễ
- dùng như màn hình escalation nhẹ

Mặc định:

- lọc theo `0502 Overdue`
- group theo `Store Department`

### `0502 Follow-up Needed`

Màn hình này tập trung vào các request đã đi đến bước nghiệm thu nhưng kết quả là:

- `Follow-up Needed`

Mục tiêu:

- giúp lead nhìn nhanh các case chưa đóng hẳn về mặt vận hành
- tránh sót các request cần quay lại xử lý hoặc theo dõi bổ sung

Mặc định:

- lọc theo `Follow-up Needed`
- group theo `Store Department`

## 6. KPI tối thiểu mà bước này hỗ trợ

Sau bước này, lead có thể nhìn tương đối nhanh các KPI tối thiểu bằng cách mở đúng monitoring action:

- số request mở
  - qua `0502 Request Monitoring`
- số overdue
  - qua `0502 Overdue Monitoring`
- số preventive
  - qua `0502 Preventive Monitoring`
- số follow-up needed
  - qua `0502 Follow-up Needed`

Ở mức `Phase 2`, KPI này đang được hiện thực bằng:

- search preset
- action mặc định
- group by / pivot / graph chuẩn của Odoo

chứ chưa phải dashboard số liệu custom riêng.

## 7. Vì sao vẫn giữ `project.task` monitoring song song

Trước bước này, module đã có:

- `0502 Execution Monitoring`

ở mức `project.task`.

Màn hình đó phù hợp để:

- theo dõi phần execution
- xem kỹ tiến độ task FSM

Nhưng nó chưa đủ để nhìn toàn bộ tình trạng của quy trình ở mức request.

Vì vậy sau bước này:

- `project.task` monitoring dùng cho execution
- `maintenance.request` monitoring dùng cho monitoring vận hành tổng hợp

Hai lớp này bổ sung cho nhau, không thay thế nhau.

## 8. Những gì bước này chưa làm

Để giữ đúng scope của `Phase 2 - Bước 10`, hiện chưa làm:

- chưa có dashboard JS riêng
- chưa có KPI counter box riêng trên form/menu
- chưa có scheduled snapshot hoặc bảng tổng hợp KPI riêng
- chưa có role-based ACL/report riêng cho từng chức danh ngoài group hiện tại
- chưa có default pivot layout chuyên biệt cho từng monitoring action

## 9. Cách test

### Case 1 - Monitoring tổng hợp request mở

1. Upgrade `M02_P0502`
2. Vào `Maintenance > Reporting > 0502 Request Monitoring`

Kết quả mong đợi:

- màn hình mở ở model `maintenance.request`
- mặc định lọc request 0502 đang mở
- mặc định group theo `Store Department`

### Case 2 - Monitoring preventive

1. Vào `Maintenance > Reporting > 0502 Preventive Monitoring`

Kết quả mong đợi:

- chỉ thấy preventive request
- mặc định group theo `Team`

### Case 3 - Monitoring overdue

1. Vào `Maintenance > Reporting > 0502 Overdue Monitoring`

Kết quả mong đợi:

- chỉ thấy request overdue / tồn đọng theo rule đã có
- mặc định group theo `Store Department`

### Case 4 - Monitoring follow-up needed

1. Vào `Maintenance > Reporting > 0502 Follow-up Needed`

Kết quả mong đợi:

- chỉ thấy request có:
  - `Acceptance Result = Follow-up Needed`

### Case 5 - Dùng pivot/graph để nhìn KPI nhanh

1. Mở một trong các monitoring action ở trên
2. chuyển qua `Pivot` hoặc `Graph`

Kết quả mong đợi:

- có thể dùng trực tiếp action mặc định + group by để nhìn nhanh số lượng request theo:
  - `Store Department`
  - `Team`
  - `Acceptance Result`
  - các chiều dữ liệu đã có sẵn trên search view

## 10. Kiểm tra tĩnh đã chạy

- XML well-formed: `OK`

## 11. File đã thay đổi

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
