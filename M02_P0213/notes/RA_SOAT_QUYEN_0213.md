# Rà Soát Quyền Đã Làm Trên Module 0213

Tài liệu này tổng hợp những gì module `M02_P0213_00` đã làm liên quan đến quyền, phạm vi truy cập và kiểm soát thao tác.

Mục tiêu là nhìn nhanh để biết:

- module đã mở quyền nào
- module đã chặn phạm vi nào
- portal được làm gì
- internal user được làm gì
- chỗ nào đang dùng `sudo()` để đi xuyên quyền chuẩn của Odoo

## 1. Tài liệu đã dùng để rà soát

- Convention đã dùng: `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map đã dùng: `addons/M02_P0213_00/structure/module_map.json`
- Source chính dùng để xác nhận:
  - `addons/M02_P0213_00/security/ir.model.access.csv`
  - `addons/M02_P0213_00/security/security.xml`
  - `addons/M02_P0213_00/controllers/main.py`
  - `addons/M02_P0213_00/views/resignation_request_views.xml`
  - `addons/M02_P0213_00/models/resignation_request.py`
  - `addons/M02_P0213_00/models/mail_activity.py`
  - `addons/M02_P0213_00/models/survey_user_input.py`

## 2. Các quyền truy cập model đã mở

Module `0213` không tạo group riêng mới cho offboarding OPS. Phần quyền đang bám chủ yếu vào `base.group_user` và `base.group_portal`.

### 2.1. Quyền cho internal user

Theo `security/ir.model.access.csv`:

- `approval.request`: internal user có `read/write/create/unlink`
- `mail.activity`: internal user có `read/write/create/unlink`
- `hr.employee`: internal user có `read/write`, không có `create/unlink`
- `survey.survey`: internal user có `read/write`, không có `create/unlink`
- `survey.user_input`: internal user có `read/write/create/unlink`
- `survey.question`: internal user có `read/write`, không có `create/unlink`
- `survey.question.answer`: internal user có `read/write`, không có `create/unlink`
- `hr.contract.type`: internal user có `read/write`, không có `create/unlink`
- `hr.departure.reason`: internal user chỉ có `read`

Ý nghĩa thực tế:

- người dùng nội bộ có đủ quyền thao tác trên đơn nghỉ việc và activity
- danh mục loại nghỉ việc chỉ cho đọc, tránh sửa/xóa tùy tiện từ user thường

### 2.2. Quyền cho portal user

Theo `security/ir.model.access.csv`:

- `survey.survey`: portal chỉ có `read`
- `survey.user_input`: portal có `read/write/create`, không có `unlink`
- `survey.question`: portal chỉ có `read`
- `survey.question.answer`: portal chỉ có `read`

Ý nghĩa thực tế:

- portal có thể tham gia flow survey nghỉ việc
- portal không được xóa bài làm survey
- portal không được sửa dữ liệu master của survey

## 3. Record rule đã bổ sung

Module có 1 record rule quan trọng trong `security/security.xml`:

- `rule_psm_0213_survey_user_input_portal_own`
- áp cho `base.group_portal`
- domain:
  - `partner_id = user.partner_id.id`
  - hoặc `email = user.email`

Ý nghĩa:

- portal chỉ được thấy `survey.user_input` của chính mình
- đây là lớp chặn dữ liệu quan trọng để tránh nhìn thấy kết quả survey của người khác

## 4. Kiểm soát quyền ở portal controller

Trong `controllers/main.py`, các route portal đều dùng:

- `auth="user"`
- route website nhưng bắt buộc phải đăng nhập

Các kiểm soát đã làm:

### 4.1. Chỉ lấy đơn nghỉ việc của chính user

Hàm `_get_latest_resignation_request()` tìm `approval.request` theo:

- `request_owner_id = request.env.user.id`
- đúng category nghỉ việc của `0213`

Hàm `_get_owned_resignation_request_by_id()` cũng khóa theo:

- `id` của đơn
- `request_owner_id = user hiện tại`
- đúng category nghỉ việc

Ý nghĩa:

- portal không lấy bừa đơn của người khác
- kể cả khi biết `request_id`, vẫn phải là đơn của chính user

### 4.2. Chỉ cho portal mark done activity của chính mình

Route `/my/resignation/ops/activity/done` có kiểm tra:

- activity phải gắn với `approval.request`
- request đó phải thuộc chính user hiện tại
- `activity.user_id` phải đúng bằng user đang đăng nhập

Chỉ khi đủ điều kiện mới gọi:

- `activity.sudo().action_feedback(...)`

Ý nghĩa:

- portal không thể tự hoàn thành activity của người khác
- portal cũng không thể lấy activity bất kỳ rồi bấm done nếu không phải activity được giao cho mình

### 4.3. Submit đơn từ portal

Route `/my/resignation/submit`:

- tạo đơn bằng `sudo()`
- nhưng dữ liệu owner bị khóa về `request.env.user.id`
- category bị khóa về category nghỉ việc của module
- approver bị lấy theo line manager của employee hiện tại

Ý nghĩa:

- portal có thể tạo đơn dù quyền gốc trên `approval.request` của portal có thể không đủ
- nhưng request owner và loại đơn không bị user tự ý lái sang hồ sơ người khác

## 5. Kiểm soát quyền ở giao diện nội bộ

Trong `views/resignation_request_views.xml`, module đã thêm các lớp kiểm soát bằng điều kiện hiển thị nút.

### 5.1. Chặn rút đơn và hủy đơn ở một số trạng thái

Nút `action_withdraw` bị ẩn nếu:

- request mới
- user status không phù hợp
- hoặc là đơn nghỉ việc đã `approved/refused`

Nút `action_cancel` bị ẩn nếu:

- request ở `new/cancel`
- user hiện tại không phải `request_owner_id`
- hoặc là đơn nghỉ việc đã `approved/refused`

Ý nghĩa:

- giao diện chỉ cho đúng owner thấy nút hủy
- đơn nghỉ việc có kết quả cuối thì không còn cho hủy/rút trên UI

### 5.2. Chặn hiển thị action nghiệp vụ theo điều kiện

Các nút:

- `action_send_social_insurance`
- `action_send_adecco_notification`
- `action_done`
- `action_rehire`
- `action_blacklist`

đều có `invisible` theo tổ hợp điều kiện như:

- đúng category nghỉ việc
- đúng trạng thái đơn
- đã hoàn tất activity chưa
- đã hoàn tất survey chưa
- loại hợp đồng Full-Time hay không
- đã gửi Adecco hay chưa
- đã rehire/blacklist trước đó hay chưa

Ý nghĩa:

- không phải ai mở form cũng thấy được đầy đủ toàn bộ action ở mọi thời điểm
- UI đã được siết theo trạng thái nghiệp vụ

Lưu ý:

- đây là lớp chặn ở giao diện
- lớp bảo vệ thật sự vẫn cần dựa thêm vào logic Python và quyền model

## 6. Kiểm soát quyền và hành vi ở model Python

### 6.1. Chặn hủy/rút đơn bằng logic backend

Trong `models/resignation_request.py`:

- override `action_withdraw()`
- override `action_cancel()`

Nếu là category nghỉ việc của `0213` và đơn đã `approved/refused` thì raise `UserError`.

Ý nghĩa:

- không chỉ ẩn nút trên UI
- gọi method trực tiếp từ RPC cũng bị chặn

### 6.2. Tự động vô hiệu hóa tài khoản khi hoàn tất nghỉ việc

Trong `action_done()`:

- tìm user từ `employee.user_id`
- fallback sang `request_owner_id`
- chỉ vô hiệu hóa nếu user thuộc `base.group_portal` hoặc `base.group_user`
- không vô hiệu hóa nếu user thuộc `base.group_system`

Ý nghĩa:

- module có logic quyền rõ ràng khi khóa tài khoản
- tránh khóa nhầm tài khoản quản trị hệ thống

### 6.3. Giữ lịch sử activity thay vì cho xóa hẳn

Trong `models/mail_activity.py`, override `unlink()`:

- nếu activity thuộc offboarding OPS thì không xóa cứng
- chuyển sang `active = False`

Ý nghĩa:

- hỗ trợ audit
- tránh mất lịch sử checklist do người dùng xóa activity

### 6.4. Tự động xử lý survey xong để đóng activity liên quan

Trong `models/survey_user_input.py`:

- khi `survey.user_input.state = done`
- hệ thống tìm employee liên quan
- tìm activity `Hoàn thành Exit Interview`
- gọi `activities.action_done()`

Ý nghĩa:

- portal hoàn tất survey sẽ kéo theo cập nhật tiến độ offboarding
- giảm phụ thuộc vào thao tác tay của user nội bộ

## 7. Các chỗ đang dùng sudo

Module `0213` dùng `sudo()` khá nhiều. Đây là phần rất cần check kỹ khi review quyền.

### 7.1. Các mục đích dùng sudo hiện tại

- đọc category nghỉ việc bằng `env.ref(...).sudo()`
- portal đọc employee, approval request, activity, survey invitation bằng `sudo()`
- tạo `approval.request` từ portal bằng `sudo()`
- tạo và đọc `survey.user_input` bằng `sudo()`
- tạo `mail.activity` từ offboarding plan bằng `sudo()`
- gửi email template bằng `sudo()`
- đọc activity inactive và dữ liệu liên quan để hiển thị checklist bằng `sudo()`
- recompute và cập nhật các field kỹ thuật trên `approval.request` bằng `sudo()`
- ghi `request_status`, `rehire`, `blacklist`, `adecco_notification_sent` bằng `sudo()`

### 7.2. Ý nghĩa của cách làm này

- module ưu tiên đảm bảo flow offboarding chạy xuyên suốt, kể cả với portal user
- đổi lại, việc đúng phạm vi hiện đang phụ thuộc mạnh vào domain và điều kiện check thủ công trong code

## 8. Tóm tắt: 0213 đã làm gì liên quan đến quyền

Tóm gọn, `0213` đã làm các việc sau liên quan đến quyền:

1. Mở ACL cho internal user trên các model phục vụ nghỉ việc, activity và survey.
2. Mở ACL tối thiểu cho portal để làm survey nghỉ việc.
3. Thêm record rule để portal chỉ thấy `survey.user_input` của chính mình.
4. Dùng portal route `auth="user"` cho các màn hình và thao tác nghỉ việc.
5. Khóa phạm vi đơn nghỉ việc portal theo `request_owner_id`.
6. Chỉ cho portal hoàn thành activity nếu activity đó giao đúng cho user hiện tại.
7. Chặn hủy/rút đơn nghỉ việc đã có kết quả cuối ở cả UI và backend.
8. Điều kiện hóa việc hiển thị các action nhạy cảm theo trạng thái nghiệp vụ.
9. Không xóa cứng activity offboarding, mà archive để giữ lịch sử.
10. Khi hoàn tất quy trình, chỉ vô hiệu hóa user portal/internal và tránh đụng vào admin.
11. Dùng khá nhiều `sudo()` để bảo đảm flow chạy được, nên phần này là trọng điểm cần check tiếp khi review quyền.

## 9. Điểm cần ưu tiên check lại trong vòng rà soát quyền tiếp theo

Đây chưa phải kết luận bug, mà là danh sách nơi nên soi kỹ tiếp:

- portal đang có `create/write` trên `survey.user_input`: cần xác nhận phạm vi có vừa đủ không
- internal user đang có `unlink` trên `approval.request` và `mail.activity`: cần xác nhận có đúng mong muốn không
- các route portal đang dùng `sudo()`: cần test kỹ case đoán ID, đổi tham số, truy cập chéo dữ liệu
- method `action_view_survey_results()` dùng `sudo()` để mở kết quả survey: cần test xem user nào thực sự mở được
- các cờ `rehire`, `blacklist`, `done`, `adecco_notification_sent` đang có `sudo().write()`: cần check ai là người được phép bấm các nút đó trong thực tế

