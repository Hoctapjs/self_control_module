# Phase Plan Triển Khai Khóa Chặt Dữ Liệu 0214

## 1. Mục tiêu

Chia quá trình siết quyền của `M02_P0214` thành nhiều phase nhỏ để có thể triển khai theo từng đợt, review từng phần, và giảm rủi ro ảnh hưởng flow đang chạy.

Nguyên tắc xuyên suốt:

- không đụng `M02_P0200`
- chỉ siết trong `M02_P0214`
- ưu tiên thay đổi nhỏ, có thể test độc lập từng phase

## 2. Tài liệu và nguồn đã dùng

- Convention đã dùng:
  - Không thấy file convention trong `addons/M02_P0214/convention/`
- JSON map đã dùng:
  - [structure/module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0214/structure/module_map.json)
- Source chính dùng để xác nhận:
  - [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/__manifest__.py)
  - [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv)
  - [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml)
  - [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml)
  - [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)
  - [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)
  - [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)
  - [models/mail_activity.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/mail_activity.py)
  - [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)

## 3. Phase 0 - Chốt Ma Trận Quyền Expected

Mục tiêu:

- chốt nhóm nào là happy path của `0214`
- chốt nhóm nào chỉ nên xem
- chốt nhóm nào được phép xử lý action nhạy cảm

Đầu việc:

- xác định phạm vi dữ liệu cần khóa
- chốt expected matrix cho:
  - `approval.request`
  - `approval.approver`
  - `survey.user_input`
  - `mail.activity`
- chốt expected action matrix cho:
  - `action_send_exit_survey`
  - `action_view_survey_results`
  - `action_send_social_insurance`
  - `action_send_adecco_notification`
  - `action_done`
  - các action offboarding checklist

Đầu ra:

- 1 file baseline expected matrix

## 4. Phase 1 - Đối Chiếu Expected Với Actual

Mục tiêu:

- xác định lệch giữa expected và thực trạng source hiện tại

Đầu việc:

- rà `ACL` hiện tại trong `ir.model.access.csv`
- rà `record rule` hiện tại
- rà `groups=` ở view
- rà các helper/backend guard hiện có
- liệt kê điểm hở:
  - ACL rộng
  - thiếu internal rule
  - `sudo()` rộng
  - search survey/activity quá rộng

Đầu ra:

- 1 file expected vs actual
- danh sách hạng mục phải sửa trong các phase sau

## 5. Phase 2 - Siết ACL Trên Survey Và Activity

Mục tiêu:

- giảm nền quyền quá rộng cho internal user

File chính:

- [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv)

Đầu việc:

- giảm quyền internal trên:
  - `survey.survey`
  - `survey.user_input`
  - `survey.user_input.line`
  - `survey.question`
  - `survey.question.answer`
- cân nhắc giảm thêm `mail.activity` nếu có thể làm mà không vỡ flow

Expected result:

- internal user không còn mặc định sửa/xóa dữ liệu survey rộng như trước

## 6. Phase 3 - Hoàn Thiện Record Rule

Mục tiêu:

- thêm lớp rule để dữ liệu chỉ mở trong đúng scope `0214`

File chính:

- [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml)
- [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml)

Đầu việc:

- tách rule `approval.request` thành read/write rõ ràng hơn nếu cần
- bỏ `perm_create=True` khỏi scope rộng nếu business không cần
- thêm internal survey rules cho:
  - `survey.survey`
  - `survey.question`
  - `survey.question.answer`
  - `survey.user_input`
- bổ sung rule activity nếu thực sự cần giới hạn thêm

Expected result:

- dữ liệu survey và request của `0214` không còn mở rộng chỉ vì có ACL nền

## 7. Phase 4 - Siết Backend Và `sudo()`

Mục tiêu:

- không để backend bypass lớp security vừa siết

File chính:

- [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)
- [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)
- [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)
- [models/mail_activity.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/mail_activity.py)
- [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)

Đầu việc:

- chuẩn hóa helper kiểm tra request thuộc `0214`
- chuẩn hóa helper lấy hoặc tạo `survey.user_input`
- siết `action_view_survey_results()`
- siết `action_send_exit_survey()`
- siết portal survey URL
- siết search `mail.activity`
- đảm bảo mọi `sudo()` đều được bọc bởi domain và guard nghiệp vụ

Expected result:

- flow vẫn chạy
- dữ liệu không bị đọc/ghi tràn qua các search rộng hoặc `sudo()` thiếu guard

## 8. Phase 5 - Đồng Bộ UI

Mục tiêu:

- làm cho UI phản ánh đúng quyền backend

File chính:

- [views/resignation_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/resignation_request_views.xml)
- nếu cần: [views/offboarding_report_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/offboarding_report_views.xml)

Đầu việc:

- rà `groups=` trên:
  - button action survey
  - button action HR process
  - tab activity
  - tab thông tin nghỉ việc
- bỏ các `groups=` lệch với backend guard

Expected result:

- user không còn thấy các button/tab mà thực tế không nên dùng

## 9. Phase 6 - Soạn Và Chạy Test Phân Quyền

Mục tiêu:

- verify từng phase bằng tình huống thực tế

Đầu việc:

- chuẩn bị user mẫu:
  - portal employee
  - internal user theo các nhóm dùng trong `0214`
- test:
  - submit đơn portal
  - xem request
  - hoàn thành activity portal
  - gửi exit survey
  - xem survey result
  - xử lý action HR
  - thử truy cập dữ liệu ngoài scope

Đầu ra:

- checklist test phase 6
- bảng pass/fail khi UAT

## 10. Phase 7 - Chuẩn Hóa Tài Liệu Và Structure

Mục tiêu:

- đồng bộ tài liệu với source sau khi patch xong

Đầu việc:

- cập nhật note triển khai
- cập nhật file before/after nếu cần
- regenerate `structure/module_map.json`

Expected result:

- structure map không còn lệch `_00`
- tài liệu phản ánh đúng source hiện tại

## 11. Thứ Tự Khuyến Nghị

Nên làm theo thứ tự sau:

1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 4
6. Phase 5
7. Phase 6
8. Phase 7

## 12. Kết luận

`0214` cần một plan triển khai tương tự `0213`, nhưng phải bám đúng thực trạng của chính `0214`:

- source thật là `M02_P0214`, không phải `_00`
- không có convention để dựa vào
- security hiện còn mở rộng
- survey và activity là hai vùng rủi ro cao

Vì vậy cách đi phù hợp nhất là làm theo phase nhỏ, siết dần từ `ACL` và `record rule`, rồi mới khóa backend và đồng bộ UI.
