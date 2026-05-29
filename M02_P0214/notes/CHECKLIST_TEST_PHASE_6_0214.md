# Checklist Test Phase 6 - 0214

## 1. Mục tiêu

Tài liệu này là checklist test cho `M02_P0214` sau các phase siết quyền đã triển khai.

Mục tiêu:

- verify happy path portal
- verify happy path backend
- verify dữ liệu ngoài scope không bị lộ
- verify các action nhạy cảm chỉ mở đúng nhóm
- verify flow survey và activity không bị vỡ sau khi siết ACL, record rule và backend guard

## 2. Tài liệu và nguồn đã dùng

- Convention đã dùng:
  - Không thấy file convention trong `addons/M02_P0214/convention/`
- JSON map đã dùng:
  - [structure/module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0214/structure/module_map.json)
- Source chính dùng để xác nhận:
  - [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv)
  - [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml)
  - [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml)
  - [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)
  - [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)
  - [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)
  - [models/survey_user_input.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/survey_user_input.py)
  - [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)
  - [views/resignation_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/resignation_request_views.xml)
  - [views/offboarding_report_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/offboarding_report_views.xml)
  - [views/config_menu_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/config_menu_views.xml)

## 3. Dữ liệu test cần chuẩn bị

Chuẩn bị tối thiểu các user và dữ liệu sau:

- 1 user portal là nhân viên RST hợp lệ
- 1 request nghỉ việc `0214` mới tạo
- 1 request nghỉ việc `0214` ở trạng thái `approved`
- 1 request ngoài `0214` để test ngoài scope
- 1 survey response đúng request `0214`
- 1 survey response khác cùng partner hoặc cùng email nhưng không thuộc request `0214`
- 1 vài activity thuộc request `0214`
- 1 vài activity thuộc request ngoài `0214`

## 4. User mẫu cần có

### 4.1. Portal

- `base.group_portal`
- là owner của request `0214`

### 4.2. Internal nhóm đọc

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_HRBP_S`

### 4.3. Internal nhóm xử lý

- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`

### 4.4. Nhóm hệ thống

- `GDH_RST_SYSTEM_ST_M`

## 5. Checklist test portal

### 5.1. Mở trang nghỉ việc RST

Điều kiện:

- đăng nhập bằng user portal hợp lệ

Kỳ vọng:

- vào được `/my/resignation/rst`
- chỉ thấy dữ liệu của chính mình

Kết quả:

- Pass / Fail
- Ghi chú:

### 5.2. Submit đơn nghỉ việc

Điều kiện:

- user portal chưa có request hoặc tạo request mới

Kỳ vọng:

- tạo được `approval.request` đúng category `0214`
- `request_owner_id` là chính user portal hiện tại
- không tạo được request cho user khác

Kết quả:

- Pass / Fail
- Ghi chú:

### 5.3. Xem request mới nhất của chính mình

Kỳ vọng:

- chỉ thấy request của chính owner
- không thấy request `0214` của user portal khác

Kết quả:

- Pass / Fail
- Ghi chú:

### 5.4. Xem activity trên portal

Kỳ vọng:

- chỉ thấy activity của chính user portal hiện tại
- activity phải thuộc flow `0214`
- không thấy activity của người xử lý khác trên cùng case
- không thấy activity thuộc case ngoài `0214`

Kết quả:

- Pass / Fail
- Ghi chú:

### 5.5. Hoàn thành activity từ portal

Kỳ vọng:

- chỉ hoàn thành được activity thuộc request của chính mình
- chỉ hoàn thành được activity có `user_id` là chính user hiện tại
- không hoàn thành được activity của user khác

Kết quả:

- Pass / Fail
- Ghi chú:

### 5.6. Mở link exit survey

Kỳ vọng:

- chỉ tạo hoặc lấy đúng `survey.user_input` của request `0214`
- không reuse nhầm survey response khác dù cùng partner/email

Kết quả:

- Pass / Fail
- Ghi chú:

## 6. Checklist test survey

### 6.1. Gửi exit survey từ backend

User test:

- `HR_ADMIN_M`
- `HR_HEAD_M`
- `SYSTEM_ST_M`

Kỳ vọng:

- action `action_send_exit_survey` chạy được với đúng nhóm
- nếu đã có `x_psm_0214_exit_survey_user_input_id` hợp lệ thì reuse đúng
- nếu chưa có thì tạo mới được response đúng survey `0214`

Kết quả:

- Pass / Fail
- Ghi chú:

### 6.2. Kiểm tra trạng thái đã làm survey

Kỳ vọng:

- `x_psm_0214_exit_survey_completed` chỉ lên `True` khi có response `done` đúng scope `0214`
- survey response khác cùng email/partner nhưng không đúng request không được tính nhầm

Kết quả:

- Pass / Fail
- Ghi chú:

### 6.3. Xem kết quả survey

User test:

- `HR_ADMIN_S`
- `HR_ADMIN_M`
- `HR_HRBP_S`
- `HR_HRBP_M`
- `HR_HEAD_M`
- `SYSTEM_ST_M`

Kỳ vọng:

- chỉ xem được result của đúng request `0214`
- không đọc lan survey khác
- nếu không có result `done` thì hiện cảnh báo đúng

Kết quả:

- Pass / Fail
- Ghi chú:

### 6.4. Thử mở survey ngoài scope

Kỳ vọng:

- internal user không đọc được `survey.user_input`, `survey.user_input.line`, `survey.question`, `survey.question.answer` ngoài survey exit interview `0214` qua flow này

Kết quả:

- Pass / Fail
- Ghi chú:

## 7. Checklist test activity

### 7.1. Xem tab quá trình nghỉ việc

User test:

- nhóm đọc `0214`

Kỳ vọng:

- chỉ thấy activity của đúng request `0214`
- không thấy activity ngoài scope

Kết quả:

- Pass / Fail
- Ghi chú:

### 7.2. Action “Hoạt động của tôi”

User test:

- nhóm đọc `0214`

Kỳ vọng:

- chỉ hiện activity của chính user hiện tại
- domain chỉ thuộc request đang mở

Kết quả:

- Pass / Fail
- Ghi chú:

### 7.3. Hoàn thành checklist khi survey done

Kỳ vọng:

- `action_checklist_completed()` chỉ tính survey response đúng request `0214`
- không bị đánh dấu hoàn tất chỉ vì có response khác cùng email/partner

Kết quả:

- Pass / Fail
- Ghi chú:

## 8. Checklist test action nghiệp vụ

### 8.1. Gửi BHXH

User test:

- `HR_ADMIN_S`
- `HR_ADMIN_M`
- `HR_HEAD_M`
- `SYSTEM_ST_M`

Kỳ vọng:

- chỉ các nhóm này thấy và chạy được action
- action bị chặn nếu:
  - chưa làm survey
  - chưa hoàn tất checklist
  - đã gửi trước đó

Kết quả:

- Pass / Fail
- Ghi chú:

### 8.2. Gửi Adecco

User test:

- `HR_ADMIN_S`
- `HR_ADMIN_M`
- `HR_HEAD_M`
- `SYSTEM_ST_M`

Kỳ vọng:

- chỉ các nhóm này thấy và chạy được action
- không nhóm khác backend thường tự mở được action này

Kết quả:

- Pass / Fail
- Ghi chú:

### 8.3. Hoàn tất nghỉ việc

User test:

- `HR_ADMIN_M`
- `HR_HRBP_M`
- `HR_HEAD_M`
- `SYSTEM_ST_M`

Kỳ vọng:

- chỉ các nhóm này thấy và chạy được action
- bị chặn nếu:
  - chưa làm survey
  - chưa hoàn tất activity
  - chưa gửi BHXH

Kết quả:

- Pass / Fail
- Ghi chú:

## 9. Checklist test UI

### 9.1. Menu cấu hình

Kỳ vọng:

- chỉ các nhóm:
  - `HR_ADMIN_M`
  - `HR_HEAD_M`
  - `SYSTEM_ST_M`
  thấy menu `Offboarding RST`
- user chỉ có `approvals.group_approval_manager` nhưng không có nhóm `0214` không được thấy menu này

Kết quả:

- Pass / Fail
- Ghi chú:

### 9.2. Tab và button trong form request

Kỳ vọng:

- `groups=` ở UI khớp với backend guard
- user không thấy button/tab mà thực tế không nên dùng

Những điểm nên test:

- `action_send_social_insurance`
- `action_done`
- `action_view_survey_results`
- `action_view_my_activities`
- page `resignation_info`
- page `offboarding_activities`

Kết quả:

- Pass / Fail
- Ghi chú:

## 10. Checklist test dữ liệu ngoài scope

### 10.1. Request ngoài `0214`

Kỳ vọng:

- flow `0214` không đọc hoặc không thao tác nhầm request ngoài category nghỉ việc `0214`

Kết quả:

- Pass / Fail
- Ghi chú:

### 10.2. Survey response ngoài request hiện tại

Kỳ vọng:

- helper mới không reuse nhầm response cũ cùng partner/email nếu không đúng request `0214`

Kết quả:

- Pass / Fail
- Ghi chú:

### 10.3. Activity ngoài request hiện tại

Kỳ vọng:

- portal không thấy activity không thuộc request của mình
- backend action “Hoạt động của tôi” không lôi activity ngoài request hiện tại

Kết quả:

- Pass / Fail
- Ghi chú:

## 11. Mẫu chốt kết quả

Sau khi test, nên chốt theo từng mục:

- `Pass`
- `Fail`
- `Blocked`

Và ghi thêm:

- user test
- request test
- bước tái hiện
- ảnh chụp màn hình nếu có

## 12. Kết luận

Checklist này dùng để verify toàn bộ các phase siết quyền của `0214` đã đạt mục tiêu:

- portal đúng owner
- survey đúng scope
- activity đúng scope
- action nhạy cảm đúng nhóm
- UI và backend khớp nhau

Sau khi chạy xong checklist này, nếu tất cả pass thì có thể coi `0214` đã hoàn thành vòng siết quyền chính.
