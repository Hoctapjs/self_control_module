# Plan Implementation Khóa Chặt Dữ Liệu 0214

## 1. Mục tiêu

Tài liệu này chốt kế hoạch triển khai để siết quyền và khóa chặt phạm vi dữ liệu cho module `M02_P0214` theo cùng tinh thần đã áp dụng cho `0213`, với nguyên tắc:

- không đụng `M02_P0200`
- không nâng nền quyền từ chain group dùng chung
- chỉ siết lại trong `M02_P0214`
- ưu tiên khóa dữ liệu bằng `ACL + record rule + backend guard + UI alignment`

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

## 3. Ghi chú quan trọng trước khi triển khai

- `module_map.json` đang lệch source:
  - map ghi `M02_P0214_00`
  - source thật là `M02_P0214`
  - `__manifest__.py` cũng đang depend `M02_P0200`, `M02_P0213`
- Vì vậy:
  - mọi kết luận trong tài liệu này ưu tiên source thật
  - `structure/module_map.json` nên được regenerate sau khi hoàn tất patch

## 4. Hiện trạng rủi ro của 0214

### 4.1. ACL đang mở rộng

Trong [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv), `base.group_user` đang có quyền khá rộng trên:

- `approval.request`
- `mail.activity`
- `survey.user_input`
- `survey.user_input.line`
- `survey.survey`
- `survey.question`
- `survey.question.answer`

Điều này làm tăng rủi ro nội bộ nhìn hoặc sửa dữ liệu ngoài đúng scope `0214`.

### 4.2. Record rule chưa đủ lớp

Hiện mới có:

- rule `approval.request` theo category
- rule `approval.approver` theo category
- rule portal own cho `survey.user_input`

Chưa có rule nội bộ để siết:

- `survey.survey`
- `survey.question`
- `survey.question.answer`
- `survey.user_input`
- `mail.activity`

### 4.3. Nhiều luồng backend đang dùng `sudo()`

Các file có nhiều điểm cần rà:

- [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)
- [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)
- [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)
- [models/mail_activity.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/mail_activity.py)
- [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)

### 4.4. Search survey hiện còn khá rộng

Trong [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py), flow xem kết quả survey và kiểm tra hoàn thành đang dựa nhiều vào:

- `survey_id`
- `partner_id`
- `email`

Điều này có thể reuse nhầm `survey.user_input` của cùng người dùng nhưng không đúng request hiện tại.

## 5. Mục tiêu quyền sau khi siết

### 5.1. Portal

Portal user chỉ được:

- tạo đơn nghỉ việc của chính mình
- xem đơn nghỉ việc của chính mình
- xem activity của chính mình trong flow portal
- mở survey của chính mình gắn với đúng request

### 5.2. Internal

Internal chỉ được thấy và thao tác đúng dữ liệu `0214` khi:

- record thuộc category nghỉ việc `0214`
- action được phép theo nhóm nghiệp vụ của `0214`
- backend guard xác nhận đúng scope trước khi `sudo()`

### 5.3. Survey

Survey của `0214` phải được siết theo đúng survey exit interview và đúng request:

- portal chỉ thấy bài làm của chính mình
- internal chỉ đọc đúng survey result liên quan `0214`
- không mở `write/create/unlink` rộng cho survey result nếu không thật cần

## 6. Danh sách file cần chỉnh

### 6.1. [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv)

Mục tiêu:

- giảm ACL rộng cho `base.group_user`
- đặc biệt với:
  - `survey.survey`
  - `survey.user_input`
  - `survey.user_input.line`
  - `survey.question`
  - `survey.question.answer`
  - `mail.activity`

Đề xuất:

- internal survey model chỉ để `read`
- bỏ `write/create/unlink` không cần thiết
- giữ portal ACL đủ cho flow survey portal nhưng không mở thừa

Expected result:

- internal user không còn mặc định sửa hoặc xóa survey data chỉ vì có `base.group_user`
- rủi ro lan quyền trên dữ liệu survey giảm rõ

### 6.2. [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml)

Mục tiêu:

- chuẩn hóa rule theo category nghỉ việc `0214`
- tách rõ `read` và `write`
- cân nhắc bỏ `perm_create=True` ở rule HR manage nếu không cần mở rộng

Đề xuất:

- giữ rule `approval.request` read scope
- tách rule `approval.request` write scope riêng cho nhóm thực sự xử lý
- giữ hoặc tinh chỉnh rule `approval.approver` read scope
- không mở create/write trên approver line nếu không có yêu cầu nghiệp vụ rõ

Expected result:

- quyền trên `approval.request` rõ hơn
- tránh tình trạng nhóm có quyền ghi quá tay trong `0214`

### 6.3. [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml)

Mục tiêu:

- giữ rule portal own
- bổ sung internal rule cho survey và activity scope `0214`

Đề xuất:

- thêm internal read rule cho:
  - `survey.survey`
  - `survey.question`
  - `survey.question.answer`
  - `survey.user_input`
- domain phải bám đúng survey exit interview `0214`
- nếu cần, thêm rule cho `mail.activity` theo request/employee thuộc flow `0214`

Expected result:

- nội bộ không còn đọc tràn sang survey khác
- survey `0214` được khóa theo đúng phạm vi nghiệp vụ

### 6.4. [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)

Mục tiêu:

- chuẩn hóa helper và khóa chặt việc gắn `survey.user_input`
- tránh reuse nhầm bài khảo sát

Đề xuất:

- thêm helper kiểm tra request có thuộc `0214` không
- siết `_get_or_create_rst_survey_user_input(...)`
  - ưu tiên dùng `x_psm_0214_exit_survey_user_input_id`
  - validate lại survey/partner/email trước khi reuse
  - nếu tạo mới thì ghi ngược lại request
- dùng helper thống nhất cho mọi nơi đọc survey result

Expected result:

- mỗi request `0214` bám được chặt hơn vào đúng `survey.user_input`
- giảm nguy cơ nhầm survey cũ cùng partner

### 6.5. [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)

Mục tiêu:

- siết action survey và các action HR liên quan

Đề xuất:

- `_compute_rst_exit_survey_completed()`:
  - không search rộng chỉ bằng email/partner
  - ưu tiên record gắn với request hoặc helper đã chuẩn hóa
- `action_view_survey_results()`:
  - chỉ xem survey của đúng request `0214`
  - không search rộng tất cả response cùng người dùng
- `action_send_exit_survey()`:
  - nếu ACL bị siết, phần tạo `survey.user_input` cần `sudo()` có kiểm soát
  - ghi ngược `x_psm_0214_exit_survey_user_input_id`
- giữ `_check_0214_group_access(...)` làm lớp chặn backend

Expected result:

- flow survey không bị vỡ sau khi giảm ACL
- kết quả survey hiển thị đúng request, không bị “ăn nhầm” response khác

### 6.6. [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)

Mục tiêu:

- siết activity và các action offboarding

Đề xuất:

- rà các chỗ `mail.activity.sudo().create/search`
- đảm bảo action chỉ chạy cho đúng request category `0214`
- nếu action xem activity dùng `sudo()`, phải lọc domain chặt hơn

Expected result:

- activity chỉ gắn và chỉ được truy cập đúng trong flow `0214`

### 6.7. [models/mail_activity.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/mail_activity.py)

Mục tiêu:

- siết các xử lý hậu cập nhật activity

Đề xuất:

- rà mọi `sudo().write/search_count`
- chỉ tính toán và cập nhật request thuộc category `0214`
- không để logic ảnh hưởng lan sang case ngoài `0214`

Expected result:

- dữ liệu activity và trạng thái checklist không vượt ngoài scope `0214`

### 6.8. [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)

Mục tiêu:

- siết flow portal

Đề xuất:

- `_get_resignation_activities()`:
  - chỉ lấy activity đúng request thuộc `0214`
- `_get_or_create_exit_survey_url(...)`:
  - dùng helper chuẩn hóa từ model
  - tránh reuse nhầm `survey.user_input`
- `portal_activity_done()`:
  - chỉ cho hoàn thành activity đúng request của chính user
- `portal_resignation_submit()`:
  - whitelist field đầu vào
  - khóa category cố định `0214`
  - chỉ tạo request cho đúng portal owner hiện tại

Expected result:

- portal flow vẫn chạy mượt
- không có đường lách dữ liệu qua request/activity/survey ngoài scope

### 6.9. [views/resignation_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/resignation_request_views.xml)

Mục tiêu:

- đồng bộ UI với backend sau khi siết

Đề xuất:

- rà `groups=` trên các button/tab nhạy cảm
- nếu đi theo hướng giống `0213`, thu hẹp UI backend về nhóm internal ổn định nhất
- không dùng UI làm lớp bảo vệ chính, chỉ làm lớp phụ

Expected result:

- không còn tình trạng user thấy nút nhưng backend không nên cho làm
- UI và backend nhất quán hơn

## 7. Thứ tự triển khai đề xuất

1. Chốt expected matrix cho `0214`
2. Đối chiếu expected với actual security hiện tại
3. Siết `ACL`
4. Hoàn thiện `record rule`
5. Siết `sudo()` và helper backend
6. Đồng bộ `view groups`
7. Soạn checklist test
8. Regenerate `module_map.json`

## 8. Cảnh báo cần giữ nguyên khi triển khai

- Không sửa chain group trong `0200`
- Không dựa vào giả định “nhóm nào cũng là internal backend user”
- Không chỉ sửa `view groups` mà bỏ qua backend guard
- Không chỉ sửa record rule mà giữ nguyên `ACL` quá rộng

## 9. Kết luận

`0214` hiện có nhiều điểm cần siết tương tự `0213`, thậm chí ở một số chỗ còn mở rộng hơn. Vì vậy hướng triển khai hợp lý là áp dụng lại cùng framework:

- Phase 0: chốt expected
- Phase 1: đối chiếu actual
- Phase 2: siết ACL và survey scope
- Phase 3: siết request/approver rule
- Phase 4: khóa backend `sudo()` và helper
- Phase 5: đồng bộ UI
- Phase 6: test checklist

Tài liệu này là bản plan implementation gốc để team bám vào khi triển khai.
