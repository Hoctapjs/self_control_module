# Đối Chiếu Naming Module 0502 Với Convention

## 1. Mục tiêu

Tài liệu này dùng để đối chiếu:

- thành phần hiện tại trong module `M02_P0502`
- tên đang dùng trong source
- tên nên đổi theo `convention`
- mức độ ảnh hưởng nếu thực hiện rename

Mục tiêu là giúp quyết định:

- có nên rename ngay ở thời điểm hiện tại hay không
- hay nên khóa naming hiện tại và xin cập nhật lại convention

## 2. Nguồn đối chiếu

### Convention đã dùng

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map đã dùng

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

### Source chính đã dùng để xác nhận

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [maintenance_equipment.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_equipment.py)
- [request_source.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_source.py)
- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
- [maintenance_equipment_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_equipment_views.xml)
- [ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)

## 3. Bảng đối chiếu naming

| Thành phần hiện tại | Tên đang dùng | Tên nên đổi theo convention | Mức độ ảnh hưởng khi rename | Ghi chú |
|---|---|---|---|---|
| Tên module trong manifest | `M02 P0502 Maintenance Process` | `M02_P0502_<TEN_QUY_TRINH_VIET_HOA>` | Thấp | Ảnh hưởng chủ yếu ở tên hiển thị, không tác động schema database |
| Model mới nguồn yêu cầu | `x_0502.request.source` | `x_psm_request_source` | Cao | Đổi model sẽ ảnh hưởng field Many2one, XML data, access rule, external id, dữ liệu đã tạo |
| Model mới loại yêu cầu | `x_0502.request.type` | `x_psm_request_type` | Cao | Tương tự model trên, ảnh hưởng trực tiếp relation và dữ liệu master |
| Field mới trên `maintenance.request` | `x_0502_request_source_id` | `x_psm_0502_request_source_id` | Cao | Đổi field trên model gốc sẽ cần migrate cột DB, sửa view, data, code Python |
| Field mới trên `maintenance.request` | `x_0502_request_source_code` | `x_psm_0502_request_source_code` | Cao | Là field stored related, đổi tên sẽ ảnh hưởng search/filter/domain |
| Field mới trên `maintenance.request` | `x_0502_department_id` | `x_psm_0502_department_id` | Cao | Đã dùng ở form, list, search, cron prepare vals |
| Field mới trên `maintenance.request` | `x_0502_request_type_id` | `x_psm_0502_request_type_id` | Cao | Ảnh hưởng code, view, dữ liệu tạo request |
| Field mới trên `maintenance.request` | `x_0502_received_by_id` | `x_psm_0502_received_by_id` | Trung bình | Ảnh hưởng code bước 3, view và tracking |
| Field mới trên `maintenance.request` | `x_0502_received_at` | `x_psm_0502_received_at` | Trung bình | Ảnh hưởng filter và logic tiếp nhận |
| Field mới trên `maintenance.request` | `x_0502_inspection_result` | `x_psm_0502_inspection_result` | Trung bình | Ảnh hưởng bước 4 và queue bước 7 |
| Field mới trên `maintenance.request` | `x_0502_inspection_note` | `x_psm_0502_inspection_note` | Trung bình | Chủ yếu ảnh hưởng form và code inspection |
| Field mới trên `maintenance.request` | `x_0502_inspected_by_id` | `x_psm_0502_inspected_by_id` | Trung bình | Ảnh hưởng tracking, view và logic inspection |
| Field mới trên `maintenance.request` | `x_0502_inspected_at` | `x_psm_0502_inspected_at` | Trung bình | Ảnh hưởng tracking, filter và logic inspection |
| Field mới trên `maintenance.request` | `x_0502_lead_notified_user_id` | `x_psm_0502_lead_notified_user_id` | Trung bình | Ảnh hưởng bước 6 và bước 7 |
| Field mới trên `maintenance.request` | `x_0502_lead_notified_at` | `x_psm_0502_lead_notified_at` | Trung bình | Ảnh hưởng queue tổng hợp và filter notify |
| Field mới trên `maintenance.equipment` | `x_0502_department_id` | `x_psm_0502_department_id` | Cao | Đã liên quan tới cron sinh preventive request |
| Field mới trên `maintenance.equipment` | `x_0502_enable_preventive_schedule` | `x_psm_0502_enable_preventive_schedule` | Cao | Ảnh hưởng logic bước 5 |
| Field mới trên `maintenance.equipment` | `x_0502_preventive_interval_days` | `x_psm_0502_preventive_interval_days` | Cao | Ảnh hưởng constraint, cron và cấu hình thiết bị |
| Field mới trên `maintenance.equipment` | `x_0502_next_preventive_date` | `x_psm_0502_next_preventive_date` | Cao | Ảnh hưởng search/filter, cron, test dữ liệu |
| Field mới trên `maintenance.equipment` | `x_0502_last_preventive_request_id` | `x_psm_0502_last_preventive_request_id` | Cao | Ảnh hưởng liên kết ngược giữa thiết bị và request preventive |
| Method action bước 3 | `action_x_0502_receive_request` | `action_psm_receive_request` | Thấp | Không ảnh hưởng schema DB, nhưng phải sửa button XML |
| Method action bước 4 | `action_x_0502_mark_inspected` | `action_psm_mark_inspected` | Thấp | Chủ yếu ảnh hưởng button XML và code gọi method |
| Method action bước 6 | `action_x_0502_notify_lead` | `action_psm_notify_lead` | Thấp | Chủ yếu ảnh hưởng button XML và cron gọi method |
| Method helper bước 6 | `_x_0502_get_lead_notification_user` | `_psm_get_lead_notification_user` | Thấp | Ảnh hưởng nội bộ Python, không đụng DB |
| Method helper bước 5 | `_x_0502_prepare_preventive_request_vals` | `_psm_prepare_preventive_request_vals` | Thấp | Ảnh hưởng nội bộ Python |
| Method helper bước 5 | `_x_0502_compute_next_preventive_date` | `_psm_compute_next_preventive_date` | Thấp | Ảnh hưởng nội bộ Python |
| Cron method | `cron_x_0502_generate_preventive_requests` | `cron_psm_generate_preventive_requests` | Thấp | Phải sửa field `code` trong `ir.cron` XML |
| View id form request | `view_maintenance_request_form_m02_p0502` | `view_psm_maintenance_request_form` | Thấp | Chủ yếu ảnh hưởng XML id và tham chiếu nội bộ |
| View id list request | `view_maintenance_request_list_m02_p0502` | `view_psm_maintenance_request_list` | Thấp | Chủ yếu ảnh hưởng XML id |
| View id search request | `view_maintenance_request_search_m02_p0502` | `view_psm_maintenance_request_search` | Thấp | Đã được action tham chiếu trực tiếp |
| View id form equipment | `view_maintenance_equipment_form_m02_p0502` | `view_psm_maintenance_equipment_form` | Thấp | Chủ yếu ảnh hưởng XML id |
| View id list equipment | `view_maintenance_equipment_list_m02_p0502` | `view_psm_maintenance_equipment_list` | Thấp | Chủ yếu ảnh hưởng XML id |
| View id search equipment | `view_maintenance_equipment_search_m02_p0502` | `view_psm_maintenance_equipment_search` | Thấp | Chủ yếu ảnh hưởng XML id |
| Action tổng hợp bước 7 | `action_x_0502_requests_to_plan` | `action_psm_requests_to_plan` | Thấp | Ảnh hưởng menu action và XML ref |
| Filter name trong search view | `filter_x_0502_*` | `filter_psm_*` hoặc giữ nguyên nội bộ | Thấp | Convention không nói trực tiếp về filter name, đây là lệch nhẹ |
| Group by filter name | `group_x_0502_*` | `group_psm_*` hoặc giữ nguyên nội bộ | Thấp | Tương tự filter name, chủ yếu để đồng bộ naming |
| Menu id bước 7 | `menu_x_0502_requests_to_plan` | `menu_psm_requests_to_plan` | Thấp | Chủ yếu ảnh hưởng XML id |
| Access id model nguồn yêu cầu | `access_x_0502_request_source_user` | `access_psm_request_source_user` | Thấp | Ảnh hưởng security XML id, không tác động dữ liệu nghiệp vụ |
| Access id model loại yêu cầu | `access_x_0502_request_type_user` | `access_psm_request_type_user` | Thấp | Tương tự trên |
| Tên access name | `access.x.0502.request.source.user` | `access.psm.request.source.user` | Thấp | Chỉ là nhãn kỹ thuật trong CSV |
| SQL constraint name model nguồn yêu cầu | `x_0502_request_source_code_unique` | `x_psm_request_source_code_unique` | Trung bình | Đổi tên constraint có thể cần update schema DB |
| SQL constraint name model loại yêu cầu | `x_0502_request_type_code_unique` | `x_psm_request_type_code_unique` | Trung bình | Tương tự constraint trên |

## 4. Nhận định theo nhóm

### 4.1. Lệch chuẩn nặng

Đây là nhóm lệch chuẩn nhưng đổi tên sẽ ảnh hưởng mạnh:

- model mới
- field mới trên model gốc
- field mới trên equipment

Nếu rename nhóm này:

- phải migrate cột database
- sửa lại view, domain, filter, cron, XML data, access rule
- kiểm tra toàn bộ dữ liệu test đã có

### 4.2. Lệch chuẩn vừa

Nhóm này chủ yếu là:

- SQL constraint name
- một số field phụ trợ stored hoặc field đã dùng nhiều trong filter

Nhóm này đổi được, nhưng vẫn cần cẩn thận vì đã đụng tới schema hoặc search domain.

### 4.3. Lệch chuẩn nhẹ

Nhóm này chủ yếu là:

- method name
- action id
- view id
- menu id
- access id

Đây là nhóm đổi tương đối an toàn hơn vì phần lớn không đụng schema dữ liệu nghiệp vụ.

## 5. Gợi ý quyết định

### Phương án 1 - Rename toàn bộ theo convention ngay bây giờ

Phù hợp khi:

- module còn ở giai đoạn đầu
- dữ liệu test chưa nhiều
- muốn siết chuẩn naming từ sớm

Ưu điểm:

- đồng bộ với convention ngay từ đầu
- tránh nợ kỹ thuật naming về sau

Nhược điểm:

- phải sửa khá rộng
- phải migrate lại các field và relation đang có

### Phương án 2 - Giữ schema hiện tại, chỉ rename phần nhẹ trước

Phù hợp khi:

- muốn tiếp tục Phase 1 nhanh
- chưa muốn đụng schema DB lớn

Có thể ưu tiên rename trước:

- action id
- view id
- menu id
- method name
- access id

Ưu điểm:

- giảm rủi ro
- vẫn cải thiện dần mức độ chuẩn naming

Nhược điểm:

- naming sẽ ở trạng thái nửa chuẩn nửa cũ

### Phương án 3 - Giữ nguyên naming hiện tại, cập nhật lại convention

Phù hợp khi:

- team chấp nhận prefix `x_0502_*`
- muốn naming gắn trực tiếp với mã quy trình `0502`
- không muốn mất thời gian rename khi module đã bắt đầu có logic đáng kể

Ưu điểm:

- không phải migrate schema
- tiếp tục phát triển nhanh

Nhược điểm:

- convention hiện tại sẽ không còn là nguồn đúng
- phải sửa convention và thống nhất lại với team

## 6. Khuyến nghị của mình

Nếu nhìn theo trạng thái hiện tại của `M02_P0502`, mình nghiêng về:

- không rename toàn bộ schema ngay lập tức
- ưu tiên chốt xem team muốn giữ prefix `x_0502_*` hay chuyển hẳn sang `x_psm_*`

Nếu team muốn theo convention hiện tại thật chặt:

- nên rename sớm ngay bây giờ, trước khi sang sâu các bước sau của `Phase 1`

Nếu team muốn ưu tiên tiến độ:

- nên giữ schema hiện tại
- chỉ rename phần nhẹ nếu cần
- đồng thời cập nhật lại convention để phản ánh cách đặt tên thực tế của module `0502`

## 7. Kết luận ngắn

Module `M02_P0502` hiện tại:

- đúng về hướng thiết kế Odoo
- chưa đúng hoàn toàn về naming theo convention hiện có

Điểm lệch lớn nhất nằm ở:

- model mới
- field mới trên model gốc
- field mới trên equipment

Ba nhóm này là phần cần cân nhắc kỹ nhất trước khi quyết định rename.
