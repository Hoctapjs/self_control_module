# Đề Xuất Phân Quyền 0213 Theo Group 0200

Tài liệu này đề xuất cách phân quyền cho module `M02_P0213_00` bằng cách tái sử dụng các group tổ chức mẫu đã có trong `M02_P0200_00`.

Mục tiêu:

- không để `0213` tiếp tục phụ thuộc quá nhiều vào `base.group_user`
- tận dụng group văn phòng đã chuẩn hóa trong `0200`
- tách rõ vai trò xem, xử lý, hoàn tất, audit trong flow offboarding OPS
- giữ đúng nguyên tắc: group dùng chung ở `0200`, rule nghiệp vụ đặt ở `0213`

## 1. Tài liệu đã dùng để đề xuất

- Convention đã dùng:
  - `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
  - `addons/M02_P0200_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map đã dùng:
  - `addons/M02_P0213_00/structure/module_map.json`
  - `addons/M02_P0200_00/structure/module_map.json`
- Source chính dùng để xác nhận:
  - `addons/M02_P0200_00/security/security.xml`
  - `addons/M02_P0213_00/security/ir.model.access.csv`
  - `addons/M02_P0213_00/security/security.xml`
  - `addons/M02_P0213_00/views/resignation_request_views.xml`
  - `addons/M02_P0213_00/controllers/main.py`
  - `addons/M02_P0213_00/models/resignation_request.py`
  - `addons/M02_P0205_00/security/recruitment_group_bridge.xml`
  - `addons/M02_P0205_00/security/approval_groups.xml`
  - `addons/M02_P0205_00/security/recruitment_request_rules.xml`

## 2. Nhóm của 0200 có thể tái sử dụng cho 0213

Vì `0213` là quy trình `Offboarding OPS`, nên cần tách rõ 2 lớp group:

- nhóm `OPS`: xác định phạm vi nghiệp vụ OPS, ai được xem và phối hợp theo case OPS
- nhóm `HR/RST`: xác định ai được làm các tác vụ nhân sự nhạy cảm như hoàn tất hồ sơ, BHXH, Adecco, blacklist, rehire

### 2.1. Nhóm OPS nên là lớp nền của phạm vi 0213

Các group OPS văn phòng trong `0200` phù hợp để dùng cho `0213`:

- `M02_P0200_00.GDH_RST_OPS_OC_S`
- `M02_P0200_00.GDH_RST_OPS_OM_M`

Ý nghĩa đề xuất:

- `OPS_OC_S`: người dùng OPS tham gia theo dõi hoặc phối hợp xử lý case offboarding OPS
- `OPS_OM_M`: quản lý OPS xem và giám sát toàn bộ case offboarding OPS

### 2.2. Nhóm HR/RST là lớp xử lý nghiệp vụ nhân sự

Các group HR văn phòng trong `0200` vẫn cần cho `0213`, nhưng không phải để thay thế OPS, mà để xử lý các bước HR:

- `M02_P0200_00.GDH_RST_HR_ADMIN_S`
- `M02_P0200_00.GDH_RST_HR_ADMIN_M`
- `M02_P0200_00.GDH_RST_HR_HRBP_S`
- `M02_P0200_00.GDH_RST_HR_HRBP_M`
- `M02_P0200_00.GDH_RST_HR_HEAD_M`
- `M02_P0200_00.GDH_RST_SYSTEM_ST_M`

Portal flow vẫn giữ riêng:

- `base.group_portal`

## 3. Quan điểm phân quyền đề xuất cho 0213

Đề xuất chia vai trò theo 4 lớp:

### 3.1. Portal employee

Vai trò:

- gửi đơn nghỉ việc
- xem tiến độ đơn của chính mình
- làm exit survey
- hoàn thành activity được giao cho chính mình trên portal

Nhóm:

- `base.group_portal`

### 3.2. OPS theo dõi và phối hợp xử lý

Vai trò:

- xem các case thuộc Offboarding OPS
- theo dõi tiến độ activity và checklist
- phối hợp với HR khi cần xác nhận nghiệp vụ OPS
- không mặc định được làm các action HR nhạy cảm

Nhóm đề xuất:

- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`

### 3.3. HR xử lý nghiệp vụ nhân sự

Vai trò:

- theo dõi case offboarding
- xem thông tin nghỉ việc
- gửi survey, BHXH, Adecco
- xử lý nhắc nhở
- hoàn tất quy trình nghỉ việc
- thực hiện các quyết định hậu kiểm như rehire hoặc blacklist nếu được phân quyền

Nhóm đề xuất:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`

### 3.4. System / Admin kỹ thuật

Vai trò:

- full quyền cấu hình, support dữ liệu, debug

Nhóm đề xuất:

- `GDH_RST_SYSTEM_ST_M`

## 4. Nguyên tắc mapping OPS và HR trong 0213

Do đây là `Offboarding OPS`, nên nên hiểu như sau:

- `OPS` là lớp quyết định phạm vi business object: case nào là case OPS, ai phía OPS được xem và phối hợp
- `HR` là lớp quyết định ai được xử lý tác vụ nhân sự nhạy cảm

Nói ngắn gọn:

- không nên dùng toàn nhóm `RST` để thay cho `OPS`
- cũng không nên dùng toàn nhóm `OPS` để làm các action HR nhạy cảm
- nên phối hợp cả 2 lớp

## 5. Đề xuất mapping group cụ thể cho từng phạm vi

## 5.1. Phạm vi xem `approval.request` của offboarding

Đề xuất:

- `GDH_RST_OPS_OC_S`: xem các case offboarding OPS trong phạm vi được giao
- `GDH_RST_OPS_OM_M`: xem toàn bộ case offboarding OPS
- `GDH_RST_HR_ADMIN_S`: xem và xử lý các đơn offboarding OPS
- `GDH_RST_HR_ADMIN_M`: xem và xử lý toàn bộ các đơn offboarding OPS
- `GDH_RST_HR_HRBP_S`: xem các đơn offboarding OPS để phối hợp kiểm soát
- `GDH_RST_HR_HRBP_M`: xem toàn bộ các đơn offboarding OPS
- `GDH_RST_HR_HEAD_M`: xem toàn bộ
- `GDH_RST_SYSTEM_ST_M`: xem toàn bộ

Gợi ý rule:

- staff OPS có thể read
- manager OPS có thể read toàn bộ case OPS
- staff HR có thể read/write các đơn offboarding
- manager/head/system có full read/write
- nếu muốn chặt hơn, có thể giới hạn `HRBP_S` chỉ đọc

Lưu ý:

- nếu cần đúng chuẩn như `0205`, có thể tạo rule theo group của `0200`
- còn nếu chưa đủ dữ liệu để tách phạm vi theo department, giai đoạn đầu có thể cho `OPS_OM_M` read toàn bộ case `0213`

## 5.2. Phạm vi xem `mail.activity` của offboarding

Đề xuất:

- user được giao activity: thấy activity của chính mình
- nhóm OPS phù hợp: thấy activity liên quan case OPS để phối hợp
- nhóm HR Admin, HRBP, HR Head: thấy toàn bộ activity của case offboarding
- portal chỉ thấy activity của chính mình trong giao diện portal

Gợi ý:

- không nên dựa hoàn toàn vào ACL `base.group_user`
- nên có rule hoặc domain riêng cho activity gắn với `approval.request` category `0213`

## 5.3. Phạm vi xem kết quả survey nghỉ việc

Đề xuất:

- portal user: chỉ xem bài làm của chính mình
- `OPS_OC_S`: cân nhắc không cho xem mặc định, trừ khi thật sự cần nghiệp vụ
- `OPS_OM_M`: có thể cho xem nếu cần theo dõi chất lượng offboarding OPS
- `HR_ADMIN_S/M`: xem kết quả survey của các case offboarding
- `HR_HRBP_S/M`, `HR_HEAD_M`: xem kết quả survey để audit
- `SYSTEM_ST_M`: full

Lưu ý:

- hiện tại `action_view_survey_results()` đang dùng `sudo()`
- nếu siết lại quyền, nên kiểm tra method này cùng record rule cho `survey.user_input`

## 6. Đề xuất mapping group cho từng action của 0213

Dưới đây là mapping đề xuất theo từng action chính trong `models/resignation_request.py` và `views/resignation_request_views.xml`.

### 6.1. `action_withdraw`

Mục đích:

- người tạo đơn rút lại đơn khi chưa có kết quả cuối

Đề xuất quyền:

- không gắn group `0200`
- tiếp tục để owner của đơn thao tác
- kiểm soát bằng `request_owner_id` và trạng thái đơn

Lý do:

- đây là action nghiệp vụ của chính người tạo đơn, không phải vai trò HR

### 6.2. `action_cancel`

Mục đích:

- hủy đơn khi còn ở pha cho phép

Đề xuất quyền:

- không gắn group `0200`
- tiếp tục để owner của đơn thao tác nếu đúng trạng thái

### 6.3. `action_send_exit_survey`

Mục đích:

- gửi khảo sát nghỉ việc

Đề xuất quyền:

- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- có thể cho `OPS_OM_M` nếu muốn OPS manager chủ động phối hợp
- không nên mở cho toàn bộ `base.group_user`

### 6.4. `action_send_adecco_notification`

Mục đích:

- gửi thông báo nghỉ việc cho Adecco

Đề xuất quyền:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- đây là action hành chính HR, không nên mở cho nhóm OPS
- không cần mở cho HRBP staff nếu không thật sự cần

### 6.5. `action_send_social_insurance`

Mục đích:

- gửi thông tin BHXH

Đề xuất quyền:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- đây là action rất nghiệp vụ HR admin/C&B, không nên mở rộng cho user nội bộ nói chung
- không nên mở cho nhóm OPS

### 6.6. `action_done`

Mục đích:

- hoàn tất quy trình nghỉ việc
- khóa tài khoản liên quan

Đề xuất quyền:

- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- không nên để staff thường bấm `Done`
- vì action này kéo theo deactive user, là thao tác nhạy cảm
- không nên giao cho nhóm OPS nếu chưa có quyết định nghiệp vụ rất rõ

### 6.7. `action_manual_reminder_extension`

Mục đích:

- chạy nhắc việc thủ công và gia hạn deadline

Đề xuất quyền:

- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

### 6.8. `action_rehire`

Mục đích:

- đánh dấu đủ điều kiện tái tuyển

Đề xuất quyền:

- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- đây là quyết định hậu kiểm nhân sự, không nên mở cho staff thường
- không nên mở cho nhóm OPS

### 6.9. `action_blacklist`

Mục đích:

- đưa vào blacklist

Đề xuất quyền:

- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- đây là action nhạy cảm nhất
- nếu muốn chặt, chỉ để `HR_HEAD_M` và `SYSTEM_ST_M`
- không nên mở cho nhóm OPS

### 6.10. `action_view_survey_results`

Mục đích:

- xem kết quả survey nghỉ việc

Đề xuất quyền:

- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Gợi ý:

- nếu lo survey là dữ liệu nhạy cảm, có thể không mở cho `OPS_OM_M`
- còn nếu cần góc nhìn quản lý OPS, chỉ nên mở cho manager OPS, không mở cho `OPS_OC_S`

## 7. Đề xuất kỹ thuật triển khai theo mẫu 0205

Nếu triển khai theo hướng giống `0205`, đề xuất làm theo thứ tự:

1. Thêm `M02_P0200_00` vào `depends` của `0213`.
2. Tạo file bridge trong `0213` nếu cần kế thừa thêm quyền chuẩn của Odoo.
3. Thêm `groups="M02_P0200_00...."` vào các button nhạy cảm ở view form.
4. Thêm `ir.rule` cho `approval.request`, có thể thêm cho `approval.approver` và `mail.activity` nếu cần.
5. Giữ portal rule riêng cho `survey.user_input`.
6. Rà lại các method đang dùng `sudo()` để chắc rằng group ở UI không phải là lớp bảo vệ duy nhất.

## 8. Đề xuất tối thiểu nên làm ngay

Nếu muốn đi từng bước nhỏ, đây là gói tối thiểu nên làm trước:

1. Thêm dependency `M02_P0200_00` vào `0213`.
2. Gắn group cho các action nhạy cảm:
   - `action_send_social_insurance`
   - `action_send_adecco_notification`
   - `action_done`
   - `action_rehire`
   - `action_blacklist`
   - `action_manual_reminder_extension`
   - `action_view_survey_results`
3. Gắn thêm quyền `read` hoặc `read/audit` cho nhóm OPS phù hợp trên case `0213`.
4. Giữ `portal submit`, `portal survey`, `portal activity done` như hiện tại.
5. Sau đó mới bổ sung record rule nếu cần siết phạm vi dữ liệu nội bộ.

## 9. Kết luận đề xuất

Có thể và nên cho người dùng thuộc các group văn phòng tương ứng của `0200` có quyền trong module `0213`.

Hướng đúng là:

- group chuẩn nằm ở `0200`
- `0213` tham chiếu các group đó để gắn quyền nghiệp vụ
- triển khai theo mẫu `0205`

Đề xuất ưu tiên:

- dùng `OPS` để xác định lớp phạm vi và phối hợp xử lý của case Offboarding OPS
- dùng `HR Admin`, `HRBP`, `HR Head`, `System` của `0200` để phân lớp quyền xử lý nghiệp vụ nhân sự trong `0213`
- không tiếp tục để toàn bộ `base.group_user` có cùng mức quyền trong offboarding
- action nào càng nhạy cảm thì càng nên đẩy lên manager/head thay vì staff
