# Phase 1 - Đối Chiếu Expected Vs Actual 0214

## 1. Mục tiêu

Tài liệu này đối chiếu giữa:

- trạng thái expected đã chốt ở Phase 0
- trạng thái actual của source hiện tại trong `M02_P0214`

Mục tiêu là chỉ ra rõ:

- điểm nào đã khớp
- điểm nào đang lệch
- điểm nào cần đưa vào Phase 2, 3, 4, 5 để sửa

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
  - [models/survey_user_input.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/survey_user_input.py)
  - [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)
  - [views/resignation_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/resignation_request_views.xml)

## 3. Ghi chú về structure map

`module_map.json` đang lệch source:

- map ghi module `M02_P0214_00`
- path cũng đang là `addons/M02_P0214_00`
- source thật là `addons/M02_P0214`
- `__manifest__.py` dùng dependency `M02_P0200`, `M02_P0213`

Kết luận:

- source là chuẩn để đối chiếu actual
- `module_map.json` cần regenerate sau khi hoàn tất triển khai

## 4. Đối chiếu theo từng lớp

### 4.1. Lớp ACL

#### Expected

- internal user không nên có quyền rộng mặc định trên survey/activity
- `survey.user_input` không nên mở `write/create/unlink` rộng
- `survey.survey`, `survey.question`, `survey.question.answer` không nên mở `write` cho internal user thông thường
- `mail.activity` không nên mở quá rộng nếu chưa có rule và guard đủ chặt

#### Actual

Trong [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv):

- `approval.request` internal: `1,1,1,1`
- `mail.activity` internal: `1,1,1,1`
- `survey.survey` internal: `1,1,0,0`
- `survey.user_input` internal: `1,1,1,1`
- `survey.user_input.line` internal: `1,1,1,1`
- `survey.question` internal: `1,1,0,0`
- `survey.question.answer` internal: `1,1,0,0`

#### Kết luận lệch

- ACL actual đang rộng hơn expected khá nhiều
- vùng survey là điểm lệch rõ nhất
- `mail.activity` cũng đang mở rất mạnh cho internal

#### Hướng sửa ở phase sau

- Phase 2 phải siết lại ACL survey trước
- nếu đủ an toàn, rà thêm `mail.activity`

## 4.2. Lớp record rule

### Expected

- `approval.request` chỉ mở đúng case `0214`
- `approval.approver` chỉ mở đúng case `0214`
- `survey.user_input` phải có rule portal own và internal scope rõ
- `survey.survey`, `survey.question`, `survey.question.answer` phải có internal read rule theo survey `0214`
- `mail.activity` nên có lớp kiểm soát rõ nếu ACL còn rộng

### Actual

Trong [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml):

- có `approval.request` read rule theo category nghỉ việc
- có `approval.request` manage rule theo category nghỉ việc
- có `approval.approver` read rule theo category nghỉ việc
- rule manage vẫn có `perm_create=True`

Trong [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml):

- chỉ có `rule_psm_0214_survey_user_input_portal_own`
- chưa có internal survey rules

### Kết luận lệch

- phần request/approver đã có nền rule cơ bản
- nhưng survey mới chỉ khóa phía portal
- internal survey scope chưa được khóa bằng rule
- `perm_create=True` trên request manage có thể rộng hơn expected

### Hướng sửa ở phase sau

- Phase 3 phải:
  - rà lại `approval.request` manage scope
  - cân nhắc bỏ `perm_create=True`
  - thêm internal survey rules

## 4.3. Lớp backend guard và `sudo()`

### Expected

- `sudo()` chỉ dùng sau khi đã check đúng scope nghiệp vụ
- survey phải gắn chặt với đúng request
- không search survey rộng chỉ bằng email/partner nếu chưa kiểm tra request
- portal chỉ được thao tác dữ liệu đúng request của chính mình

### Actual

Trong [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py):

- đã có `_check_0214_group_access(...)`
- đã có `_get_or_create_rst_survey_user_input(...)`
- nhưng helper này vẫn dùng `sudo().search/create/write`
- logic reuse survey chủ yếu theo:
  - `x_psm_0214_exit_survey_user_input_id`
  - hoặc `survey_id + partner_id`

Trong [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py):

- `_compute_rst_exit_survey_completed()` search `survey.user_input` bằng `survey + email/partner`
- `action_view_survey_results()` search `survey.user_input` bằng `survey + email/partner`
- `action_send_exit_survey()` đang `create()` trực tiếp `survey.user_input`

Trong [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py):

- có `mail.activity.sudo().create(...)`
- có `survey.user_input.sudo().search(...)`
- có `self.sudo().search(...)`

Trong [models/mail_activity.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/mail_activity.py):

- nhiều `sudo().write/search_count`
- có cập nhật trạng thái liên quan request và checklist

Trong [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py):

- portal flow dùng nhiều `sudo()`
- `_get_resignation_activities()` đọc activity bằng `sudo()`
- `_get_or_create_exit_survey_url(...)` gọi helper `sudo()` để tạo hoặc lấy survey
- `portal_resignation_submit()` tạo request bằng `sudo().create(...)`

### Kết luận lệch

- actual có backend guard nền, nhưng chưa đủ chặt
- survey flow vẫn có nguy cơ search/reuse rộng hơn expected
- activity flow vẫn phụ thuộc mạnh vào `sudo()`
- portal flow còn dựa nhiều vào `sudo()` nên phải được siết bằng domain và helper chuẩn

### Hướng sửa ở phase sau

- Phase 4 sẽ là phase nặng nhất của `0214`
- cần chuẩn hóa helper:
  - check request thuộc `0214`
  - get/create đúng survey user input
  - get activity đúng scope request

## 4.4. Lớp UI và button visibility

### Expected

- UI phải phản ánh đúng backend
- không để user thấy button/tab mà thực tế không nên thao tác

### Actual

Theo source hiện tại:

- logic quyền chủ yếu đang nằm ở Python helper `_check_0214_group_access(...)`
- các action trong model đã có check nhóm ở mức nhất định
- nhưng Phase 1 chưa chốt rằng view groups hiện tại đã đồng bộ hoàn toàn với backend

### Kết luận lệch

- actual có lớp guard backend tốt hơn nhiều module khác
- nhưng vẫn cần rà thêm `groups=` ở view để đồng bộ với backend sau khi siết ACL/rule

### Hướng sửa ở phase sau

- Phase 5 sẽ rà lại toàn bộ `groups=` ở view nhạy cảm

## 5. Đối chiếu theo model chính

### 5.1. `approval.request`

Expected:

- đúng scope `0214`
- read/write rõ theo nhóm
- không mở create quá rộng

Actual:

- có ACL nội bộ rất rộng
- có rule category scope
- manage rule vẫn có `perm_create=True`

Kết luận:

- có nền kiểm soát
- nhưng vẫn rộng hơn expected

### 5.2. `approval.approver`

Expected:

- chỉ đọc đúng approver line của request `0214`
- không mở write/create rộng

Actual:

- có read rule theo category request
- chưa thấy lớp internal write riêng của `0214`

Kết luận:

- khá gần expected
- chưa phải vùng ưu tiên cao nhất

### 5.3. `survey.user_input`

Expected:

- portal own only
- internal read theo đúng survey `0214`
- không mở write/create/unlink rộng

Actual:

- portal own rule có
- internal rule chưa có
- ACL internal đang `1,1,1,1`

Kết luận:

- đây là vùng lệch lớn nhất và nên ưu tiên sửa sớm

### 5.4. `mail.activity`

Expected:

- chỉ thấy và cập nhật activity thuộc flow `0214`

Actual:

- ACL internal rộng
- search/create/update bằng `sudo()` khá nhiều
- chưa thấy internal rule riêng trong `security.xml`

Kết luận:

- đây là vùng lệch lớn thứ hai sau survey

## 6. Đối chiếu theo happy path

### 6.1. Portal happy path

Expected:

- submit đơn
- xem request của chính mình
- làm survey đúng request
- hoàn thành activity đúng request

Actual:

- flow portal hiện đã có đầy đủ đường đi chức năng
- nhưng đang phụ thuộc nhiều vào `sudo()` và helper chưa đủ chặt

Kết luận:

- happy path có sẵn
- cần siết chặt hơn để tránh lộ hoặc reuse sai dữ liệu

### 6.2. Backend happy path

Expected:

- mở request
- xem checklist
- gửi survey
- xem survey result
- xử lý action HR

Actual:

- đã có đủ action backend chính
- có backend guard nhóm
- nhưng nền ACL/rule/sudo chưa cân bằng

Kết luận:

- happy path backend có sẵn
- cần siết để bớt phụ thuộc vào ACL rộng

## 7. Danh sách lệch actual vs expected

### 7.1. Lệch mức cao

- `survey.user_input` internal đang quá rộng
- `survey.user_input.line` internal đang quá rộng
- `survey.survey`, `survey.question`, `survey.question.answer` internal còn có quyền write
- thiếu internal survey record rules
- search survey result còn rộng theo email/partner

### 7.2. Lệch mức trung bình

- `mail.activity` internal ACL đang rộng
- nhiều luồng activity dùng `sudo()`
- request manage rule còn `perm_create=True`

### 7.3. Lệch mức thấp

- structure map đang lệch source `_00`
- tài liệu cũ của `0214` còn bám `_00`

## 8. Mapping sang các phase tiếp theo

### Phase 2

Sửa:

- `security/ir.model.access.csv`

Mục tiêu:

- siết ACL survey
- giảm write/create/unlink không cần thiết

### Phase 3

Sửa:

- `security/offboarding_request_rules.xml`
- `security/security.xml`

Mục tiêu:

- thêm internal survey rules
- rà lại request manage scope

### Phase 4

Sửa:

- `models/approval_request_rst_fields.py`
- `models/approval_request_rst_survey.py`
- `models/approval_request_rst_offboarding.py`
- `models/mail_activity.py`
- `controllers/main.py`

Mục tiêu:

- siết `sudo()`
- chuẩn hóa helper
- khóa search survey/activity theo đúng request

### Phase 5

Sửa:

- `views/resignation_request_views.xml`
- nếu cần `views/offboarding_report_views.xml`

Mục tiêu:

- đồng bộ UI với backend security

## 9. Kết luận

Phase 1 chốt rằng:

- `0214` có cùng kiểu bài toán với `0213`
- nhưng trọng tâm rủi ro của `0214` hiện rõ nhất ở:
  - survey
  - activity
  - backend `sudo()`
- request/approver đã có nền rule ban đầu, nhưng vẫn cần tinh chỉnh

Nói ngắn gọn:

- `0214` chưa ở trạng thái khóa chặt dữ liệu
- actual hiện đang rộng hơn expected
- các phase tiếp theo có thể bám khá rõ theo thứ tự:
  - ACL
  - record rule
  - backend
  - UI
