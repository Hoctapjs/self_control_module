# Before / After Thay Đổi Quyền 0213

Tài liệu này ghi lại nhanh trạng thái trước và sau của phần phân quyền trong module `M02_P0213_00` cho đợt chỉnh sửa hiện tại.

## 1. Phạm vi thay đổi

Các file đã thay đổi:

- `addons/M02_P0213_00/__manifest__.py`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/models/survey_user_input.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`

Các note liên quan:

- `addons/M02_P0213_00/notes/RA_SOAT_QUYEN_0213.md`
- `addons/M02_P0213_00/notes/DE_XUAT_PHAN_QUYEN_0213_THEO_GROUP_0200.md`

## 2. Before

Trước khi chỉnh sửa, `0213` đang có các đặc điểm sau:

### 2.1. Về dependency

- `0213` chưa depend vào `M02_P0200_00`
- vì vậy chưa thể tham chiếu chính thức các group tổ chức chuẩn của `0200`

### 2.2. Về lớp quyền tổng thể

- quyền chủ yếu dựa trên `base.group_user` và `base.group_portal`
- chưa có gắn quyền theo các group văn phòng chuẩn như `HR Admin`, `HRBP`, `OPS Manager`, `System`

### 2.3. Về UI

- nhiều button nhạy cảm trên form `approval.request` chưa có thuộc tính `groups`
- việc ai thấy nút nào chủ yếu đang dựa vào:
  - `invisible`
  - trạng thái đơn
  - category
  - một số điều kiện nghiệp vụ

Điều này dẫn tới:

- user nội bộ không đúng vai trò vẫn có thể thấy hoặc bấm các action nếu thỏa điều kiện trạng thái

### 2.4. Về backend

- các method nhạy cảm chưa có check group backend riêng
- nếu gọi method trực tiếp bằng RPC hoặc từ context khác, lớp chặn chủ yếu vẫn dựa vào quyền model mặc định và logic trạng thái

Các action đang ở trạng thái này gồm:

- `action_send_adecco_notification`
- `action_send_social_insurance`
- `action_view_survey_results`
- `action_done`
- `action_rehire`
- `action_blacklist`
- `action_manual_reminder_extension`

### 2.5. Về automation

- flow auto gửi BHXH từ `survey_user_input.py` gọi trực tiếp `action_send_social_insurance()`
- lúc đó chưa có lớp check group riêng nên không có vấn đề quyền phát sinh trong automation

## 3. After

Sau khi chỉnh sửa, `0213` đã được nối vào hệ group chuẩn của `0200` và có thêm lớp kiểm soát ở cả UI lẫn backend.

### 3.1. Về dependency

Đã thêm:

- `M02_P0200_00` vào `depends` của `0213`

Ý nghĩa:

- `0213` có thể tham chiếu chính thức các group chuẩn của `0200`

### 3.2. Về lớp group áp dụng

Đã dùng các group sau từ `0200`:

- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Ý nghĩa triển khai:

- `OPS` là lớp scope và phối hợp xử lý case offboarding OPS
- `HR/RST` là lớp xử lý các action nhân sự nhạy cảm

### 3.3. Về security folder

Đã thêm file mới:

- `security/offboarding_request_rules.xml`

File này bổ sung record rule cho:

- `approval.request`
- `approval.approver`

Theo nhóm `0200` đã map cho `0213`.

Mục tiêu:

- đưa phân quyền của `0213` xuống lớp `security/`
- không chỉ dừng ở button `groups` và backend guard
- áp quyền business scope riêng cho case offboarding `0213` trên model dùng chung

### 3.4. Về backend

Đã bổ sung trong `resignation_request.py`:

- các hằng group theo từng nhóm action
- helper `_check_0213_group_access()`

Helper này:

- bỏ qua check nếu là `superuser`
- bỏ qua check nếu có context `bypass_0213_group_check`
- chỉ check với các đơn thuộc category nghỉ việc của `0213`
- raise `AccessError` nếu user không thuộc group được phép

### 3.5. Các action đã được siết ở backend

Đã thêm check group cho:

- `action_send_adecco_notification`
- `action_send_social_insurance`
- `action_view_survey_results`
- `action_done`
- `action_rehire`
- `action_blacklist`
- `action_manual_reminder_extension`

Ý nghĩa:

- không chỉ ẩn nút trên UI
- gọi method trực tiếp cũng sẽ bị chặn nếu không đúng group

### 3.6. Về UI

Đã thêm `groups` vào các button/action nhạy cảm trong `resignation_request_views.xml`.

Các button đã được gắn group:

- `action_send_social_insurance`
- `action_send_adecco_notification`
- `action_done`
- `action_rehire`
- `action_blacklist`
- `action_view_survey_results`

Các vùng giao diện đã được gắn group:

- tab `Thông tin nghỉ việc`
- tab `Quá trình nghỉ việc`

Ý nghĩa:

- người không thuộc nhóm phù hợp sẽ không thấy các phần này ngay từ UI

### 3.7. Về automation

Do `action_send_social_insurance()` đã có check group backend, flow tự động trong `survey_user_input.py` đã được cập nhật để dùng:

- context `bypass_0213_group_check=True`

Ý nghĩa:

- automation hệ thống vẫn chạy
- user thường vẫn không thể tự gọi action nếu không đúng group

## 4. Mapping triển khai thực tế trong đợt này

### 4.1. Nhóm OPS

Được dùng cho:

- xem tab quá trình nghỉ việc
- phối hợp xử lý
- nhắc việc thủ công

Nhóm áp dụng:

- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`

### 4.2. Nhóm HR

Được dùng cho:

- gửi survey
- xem kết quả survey
- gửi BHXH
- gửi Adecco
- hoàn tất nghỉ việc
- rehire
- blacklist

Nhóm áp dụng theo mức nhạy cảm:

- `HR Admin` cho các action hành chính HR
- `HRBP/HR Head` cho các action hậu kiểm hoặc quyết định nhạy cảm hơn
- `System` cho full quyền

## 5. Tác động chính của thay đổi

### 5.1. Điểm tốt

- `0213` không còn phụ thuộc hoàn toàn vào `base.group_user`
- quyền bắt đầu bám theo nhóm tổ chức chuẩn của `0200`
- UI và backend đã đồng bộ hơn
- đã có thêm lớp `record rule` trong `security/`
- các action nhạy cảm được siết rõ ràng hơn

### 5.2. Tác động cần lưu ý khi test

- user nội bộ cũ nếu chưa được gán group phù hợp trong `0200` có thể mất quyền thấy/bấm action
- automation sau survey phụ thuộc vào context bypass mới thêm
- cần test kỹ bằng user thật theo từng group:
  - OPS OC
  - OPS OM
  - HR Admin Staff
  - HR Admin Manager
  - HRBP Staff
  - HRBP Manager
  - HR Head
  - System

## 6. Chưa làm trong đợt này

Các phần sau chưa triển khai:

- record rule nội bộ cho `mail.activity`
- bridge group kiểu `0205`
- siết lại ACL `ir.model.access.csv` theo group `0200`

Hiện tại đợt này mới tập trung vào:

- dependency
- record rule cho `approval.request` và `approval.approver`
- button visibility
- backend action guard

## 7. Kết luận ngắn

Before:

- `0213` chủ yếu chạy theo `base.group_user`
- chưa gắn group chuẩn của `0200`
- action nhạy cảm chưa có backend guard theo group

After:

- `0213` đã depend `0200`
- đã có file rule trong `security/` cho `approval.request` và `approval.approver`
- đã gắn group `OPS` và `HR/RST` theo vai trò
- đã siết action nhạy cảm ở cả UI và backend
- automation vẫn giữ chạy được bằng bypass có kiểm soát
