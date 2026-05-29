# Kế Hoạch Triển Khai Quyền 0214 Theo Group 0200

Tài liệu này là note triển khai quyền cho module `M02_P0214_00` theo các group chuẩn đã có trong `M02_P0200_00`.

Bối cảnh:

- `0214` là quy trình `Offboarding RST`
- khác với `0213` là quy trình `Offboarding OPS`
- vì vậy lớp group chính của `0214` nên xoay quanh `RST / văn phòng`, không phải `OPS`

## 1. Tài liệu đã dùng để định hướng

- Convention đã dùng:
  - `addons/M02_P0214_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map đã dùng:
  - `addons/M02_P0214_00/structure/module_map.json`
- Source chính dùng để xác nhận:
  - `addons/M02_P0214_00/__manifest__.py`
  - `addons/M02_P0214_00/security/ir.model.access.csv`
  - `addons/M02_P0214_00/controllers/main.py`
  - `addons/M02_P0214_00/views/resignation_request_views.xml`
  - `addons/M02_P0214_00/views/offboarding_report_views.xml`
  - `addons/M02_P0214_00/models/approval_request_rst_approval.py`
  - `addons/M02_P0214_00/models/approval_request_rst_fields.py`
  - `addons/M02_P0214_00/models/approval_request_rst_survey.py`
  - `addons/M02_P0214_00/models/approval_request_rst_reminder.py`
  - `addons/M02_P0200_00/security/security.xml`

## 2. Hiện trạng của 0214

Hiện tại `0214` đang có:

- `ACL` khá rộng trong `security/ir.model.access.csv`
- quyền chủ yếu dựa trên `base.group_portal` và `base.group_user`
- chưa thấy file `security.xml` hoặc rule riêng theo group tổ chức của `0200`
- chưa thấy lớp `groups="M02_P0200_00...."` bám rõ vào các action nhạy cảm

Điều đó có nghĩa là:

- `0214` chưa phân vai rõ theo nhóm văn phòng `RST`
- các action nhạy cảm vẫn có xu hướng dựa nhiều vào user nội bộ chung

## 3. Nhóm của 0200 nên dùng cho 0214

Vì `0214` là quy trình của `RST`, nên nhóm trọng tâm nên là các group văn phòng của `0200`.

### 3.1. Nhóm RST nên dùng

- `M02_P0200_00.GDH_RST_HR_ADMIN_S`
- `M02_P0200_00.GDH_RST_HR_ADMIN_M`
- `M02_P0200_00.GDH_RST_HR_HRBP_S`
- `M02_P0200_00.GDH_RST_HR_HRBP_M`
- `M02_P0200_00.GDH_RST_HR_HEAD_M`
- `M02_P0200_00.GDH_RST_SYSTEM_ST_M`

### 3.2. Portal giữ riêng

- `base.group_portal`

Vai trò:

- gửi đơn nghỉ việc RST
- xem tiến độ đơn của chính mình
- làm exit survey
- hoàn thành activity được giao cho chính mình trên portal

## 4. Quan điểm phân quyền cho 0214

Đề xuất chia theo 4 lớp:

### 4.1. Portal employee RST

Vai trò:

- submit đơn nghỉ việc
- xem đơn của chính mình
- làm survey
- hoàn thành activity của chính mình

Nhóm:

- `base.group_portal`

### 4.2. HR Admin RST

Vai trò:

- xử lý nghiệp vụ hành chính offboarding
- gửi survey
- gửi BHXH
- gửi mail nhắc việc
- xử lý Adecco nếu có

Nhóm:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`

### 4.3. HRBP / HR Head RST

Vai trò:

- theo dõi toàn bộ case nghỉ việc
- kiểm tra tiến độ
- hoàn tất quy trình
- quyết định hậu kiểm nhạy cảm

Nhóm:

- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`

### 4.4. System

Vai trò:

- full quyền cấu hình, sửa dữ liệu, debug

Nhóm:

- `GDH_RST_SYSTEM_ST_M`

## 5. Mapping đề xuất cho từng action của 0214

Dựa trên `module_map.json`, các action chính của `0214` cần map quyền như sau.

### 5.1. `action_send_exit_survey`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 5.2. `action_send_social_insurance`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 5.3. `action_view_survey_results`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 5.4. `action_manual_reminder_extension`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 5.5. `action_done`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Lý do:

- action này có thể kéo theo đóng quy trình và vô hiệu hóa user
- không nên để staff thường bấm

### 5.6. `action_confirm`

Nhóm đề xuất:

- portal owner theo flow portal
- nội bộ: giữ theo logic approval hiện có

Lưu ý:

- đây không phải action nên siết hoàn toàn theo HR group như các action nhạy cảm phía sau

### 5.7. `action_approve`

Nhóm đề xuất:

- giữ theo logic approver của approval
- không hard-code theo group `0200` nếu chưa có nhu cầu đặc biệt

### 5.8. `action_checklist_completed`

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 5.9. `action_view_my_activities`

Nhóm đề xuất:

- user nội bộ được giao activity
- nhóm HR liên quan
- portal vẫn theo flow portal riêng

### 5.10. `action_pending_offboarding_subordinates`

Nhóm đề xuất:

- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

## 6. Đề xuất lớp security cần triển khai cho 0214

Để làm tương tự `0213`, nên triển khai theo 4 lớp:

### 6.1. Dependency

Thêm `M02_P0200_00` vào `depends` của `0214`.

Mục tiêu:

- dùng chính thức các group chuẩn của `0200`

### 6.2. Record rule

Thêm file mới trong `security/`, ví dụ:

- `security/offboarding_request_rules.xml`

Rule nên áp cho:

- `approval.request`
- `approval.approver`

Theo hướng:

- nhóm HR được read/write/create trên case offboarding `0214`
- nhóm manager/head/system có rộng hơn
- portal vẫn dùng scope owner như flow hiện tại

### 6.3. Button visibility

Gắn `groups="M02_P0200_00...."` vào các button nhạy cảm trong:

- `views/resignation_request_views.xml`
- nếu cần thì cả `views/offboarding_report_views.xml`

### 6.4. Backend action guard

Thêm check group ở Python trong các file:

- `models/approval_request_rst_approval.py`
- `models/approval_request_rst_survey.py`
- `models/approval_request_rst_reminder.py`
- `models/approval_request_rst_offboarding.py`

Mục tiêu:

- không chỉ ẩn nút trên UI
- gọi method trực tiếp vẫn bị chặn nếu không đúng group

## 7. Thứ tự triển khai đề xuất

Nên làm theo đúng thứ tự này:

1. Thêm `M02_P0200_00` vào `depends`.
2. Thêm file rule trong `security/`.
3. Load file rule trong `__manifest__.py`.
4. Gắn `groups` cho button và tab nhạy cảm ở view.
5. Thêm backend guard trong Python cho các action nhạy cảm.
6. Giữ automation có thể bypass bằng context nếu cần.
7. Test lại bằng user thật theo từng role.

## 8. File dự kiến cần sửa khi triển khai

Các file có khả năng cần sửa:

- `addons/M02_P0214_00/__manifest__.py`
- `addons/M02_P0214_00/security/ir.model.access.csv`
- `addons/M02_P0214_00/security/offboarding_request_rules.xml`
- `addons/M02_P0214_00/views/resignation_request_views.xml`
- `addons/M02_P0214_00/views/offboarding_report_views.xml`
- `addons/M02_P0214_00/models/approval_request_rst_approval.py`
- `addons/M02_P0214_00/models/approval_request_rst_survey.py`
- `addons/M02_P0214_00/models/approval_request_rst_reminder.py`
- `addons/M02_P0214_00/models/approval_request_rst_offboarding.py`

## 9. Lưu ý riêng cho 0214

Do `0214` đang `depends` vào `M02_P0213_00`, cần chú ý:

- tránh để quyền của `0213` vô tình chi phối quá sâu sang `0214`
- rule của `0214` phải bám category hoặc field nhận diện đúng case `RST`
- không dùng group `OPS` cho `0214` chỉ vì đã có sẵn ở `0213`

Nói ngắn gọn:

- `0213` dùng tư duy `OPS + HR`
- `0214` nên dùng tư duy `RST + HR`

## 10. Kết luận triển khai

Đối với `0214`, note này chốt hướng như sau:

- đây là quy trình `RST`
- nên ưu tiên các group `RST` của `0200`
- triển khai theo cùng khung đã dùng cho `0213`
- nhưng mapping group phải đổi sang đúng ngữ cảnh `RST`

Gói tối thiểu nên làm:

1. thêm `depends` tới `M02_P0200_00`
2. thêm record rule cho `approval.request` và `approval.approver`
3. gắn group cho các action nhạy cảm
4. thêm backend guard cho các action nhạy cảm

