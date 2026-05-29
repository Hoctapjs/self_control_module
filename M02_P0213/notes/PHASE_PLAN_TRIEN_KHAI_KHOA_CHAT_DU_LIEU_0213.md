# Phase Plan Triển Khai Khóa Chặt Dữ Liệu 0213

Tài liệu này chia việc siết quyền và khóa chặt dữ liệu của module `M02_P0213_00` thành nhiều phase để có thể triển khai theo từng đợt, giảm rủi ro và dễ bám theo thực tế vận hành.

Tài liệu tham chiếu:
- Convention: `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213_00/structure/module_map.json`
- Plan gốc chi tiết theo file: `addons/M02_P0213_00/notes/PLAN_IMPLEMENTATION_KHOA_CHAT_DU_LIEU_0213.md`

Source chính dùng để xác nhận:
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/controllers/main.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`
- `addons/M02_P0200/security/security.xml`
- `odoo/addons/approvals/security/approval_security.xml`
- `odoo/addons/survey/security/survey_security.xml`

## 1. Mục tiêu của việc chia phase

Việc chia phase nhằm đạt các mục tiêu sau:
- Có thể triển khai theo từng đợt nhỏ, an toàn hơn.
- Sau mỗi đợt đều có điểm dừng để test và xác nhận.
- Hạn chế việc sửa ACL, record rule, `sudo()` và UI cùng lúc gây khó debug.
- Dễ rollback nếu một phase gây ảnh hưởng quyền ngoài mong muốn.

## 2. Nguyên tắc triển khai theo phase

- Mỗi phase phải có mục tiêu rõ ràng.
- Mỗi phase chỉ sửa một nhóm vấn đề chính.
- Sau mỗi phase phải có checklist test.
- Chỉ chuyển sang phase tiếp theo khi phase hiện tại đã ổn trên môi trường dev hoặc staging.
- Nếu source khác JSON map, ưu tiên source và regenerate map sau khi hoàn tất phase liên quan.

## 3. Tổng quan các phase

### Phase 0 - Chốt thiết kế quyền trước khi code

Mục tiêu:
- Chốt ma trận quyền expected theo từng nhóm 0200.
- Xác nhận group nào được xem, group nào được sửa, group nào chỉ dùng UI, group nào cần backend access thật.

Việc cần làm:
- Rà lại ma trận quyền cho:
  - `approval.request`
  - `approval.approver`
  - `survey.user_input`
  - `mail.activity`
- Xác nhận các nhóm:
  - `GDH_RST_OPS_OC_S`
  - `GDH_RST_OPS_OM_M`
  - `GDH_RST_HR_ADMIN_S`
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HRBP_S`
  - `GDH_RST_HR_HRBP_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- Xác định nhóm nào phải imply `base.group_user`.
- Xác định user nào đang mang thêm group từ `approvals` hoặc `survey`.

Expected result:
- Có một ma trận quyền expected được business và dev thống nhất.
- Không bước vào code khi chưa rõ “ai được thấy gì, sửa gì”.

Điểm dừng xác nhận:
- Chỉ sang Phase 1 khi ma trận expected đã được chốt.

### Phase 1 - Rà chain group và quyền nền

Mục tiêu:
- Làm rõ nền quyền thực tế của các group 0200 trước khi siết `record rule`.

File liên quan:
- `addons/M02_P0200/security/security.xml`

Việc cần làm:
- Kiểm tra các `implied_ids` hiện tại.
- Chốt nhóm nào phải có `GDH_RST_ALL_BASE_S`.
- Nếu có nhóm đang được dùng để cấp quyền model backend nhưng chưa imply `base.group_user`, cần quyết định sửa hay giữ.
- Không sửa business rule của `0213` ở phase này.

Expected result:
- Nền quyền group rõ ràng và không còn mâu thuẫn với ý đồ nghiệp vụ.
- Dev biết chính xác nhóm nào sẽ có khả năng thao tác backend thật.

Checklist test:
- Login user mẫu theo từng nhóm.
- Kiểm tra user có phải internal user thật không.
- Kiểm tra user có xuất hiện backend menu Odoo theo đúng mong muốn không.

Rủi ro:
- Nếu đổi `implied_ids` quá sớm, có thể ảnh hưởng nhiều module khác dùng chung group 0200.

### Phase 2 - Siết ACL nền

Mục tiêu:
- Loại bớt các ACL quá rộng đang mở đường cho user thấy hoặc sửa dữ liệu ngoài phạm vi `0213`.

File liên quan:
- `addons/M02_P0213_00/security/ir.model.access.csv`

Việc cần làm:
- Rà ACL của:
  - `approval.request`
  - `survey.user_input`
  - các model liên quan nếu cần
- Giảm quyền quá rộng cho `base.group_user`.
- Hạn chế `unlink`.
- Nếu business chưa sẵn sàng thay ACL mạnh, phase này có thể tạm giữ ACL và chuyển nhanh sang Phase 3 để bù bằng record rule.

Expected result:
- User không còn “được nhiều quyền vì ACL nền quá mở”.
- Record rule ở phase sau sẽ có giá trị thực tế hơn.

Checklist test:
- User nội bộ mở list/form của các model chính.
- Xác nhận user không có quyền bất thường chỉ vì là internal user.

Rủi ro:
- Nếu cắt ACL mạnh mà chưa có rule bù đúng, một số flow có thể lỗi truy cập.

### Phase 3 - Hoàn thiện record rule cho dữ liệu nghiệp vụ

Mục tiêu:
- Dùng `record rule` để khóa chặt phạm vi dữ liệu theo flow offboarding `0213`.

File liên quan:
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`

Việc cần làm:
- Hoàn thiện rule cho `approval.request`.
- Hoàn thiện rule cho `approval.approver`.
- Bổ sung rule internal cho `survey.user_input`.
- Cân nhắc thêm rule cho `mail.activity`.
- Nếu business có scope theo owner, manager, store hoặc department thì đưa luôn vào domain ở phase này.

Expected result:
- User chỉ thấy dữ liệu đúng phạm vi `0213`.
- OPS chỉ đọc đúng phần được giao.
- HR chỉ xử lý đúng phần được giao.
- Portal chỉ thấy dữ liệu survey của chính mình.

Checklist test:
- Test list view, form view, search, open record bằng ID.
- Test user không cùng scope không thấy record.
- Test user đúng scope vẫn thao tác được.

Rủi ro:
- Nếu domain chưa đủ chặt hoặc sai quan hệ, có thể chặn nhầm record hợp lệ.

### Phase 4 - Khóa chặt backend logic và `sudo()`

Mục tiêu:
- Không để `sudo()` vô hiệu hóa lớp bảo vệ vừa dựng ở ACL và `record rule`.

File liên quan:
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/controllers/main.py`

Việc cần làm:
- Rà mọi method đang `sudo().search()`, `sudo().create()`, `sudo().write()`.
- Thêm helper kiểm tra scope nghiệp vụ.
- Thêm helper kiểm tra group cho từng action nhạy cảm.
- Với `action_view_survey_results`, khóa đúng survey `0213` và đúng request hiện tại.
- Với controller portal, kiểm tra chặt owner và scope trước khi `sudo()`.

Expected result:
- Người dùng không thể đi vòng qua backend để vượt quyền.
- Các action nhạy cảm chỉ chạy khi đúng group và đúng bản ghi.

Checklist test:
- Test gọi action bằng UI.
- Test gọi action qua RPC hoặc URL nếu có thể.
- Test portal submit, portal survey, portal activity done.

Rủi ro:
- Nếu check quá chặt mà bỏ sót luồng hợp lệ, business action có thể bị chặn nhầm.

### Phase 5 - Đồng bộ UI với backend

Mục tiêu:
- UI phản ánh đúng quyền thực, tránh nút hiện ra nhưng backend chặn hoặc ngược lại.

File liên quan:
- `addons/M02_P0213_00/views/resignation_request_views.xml`

Việc cần làm:
- Đồng bộ `groups=` ở button và tab với logic Python.
- Rà các nút:
  - `action_send_social_insurance`
  - `action_send_adecco_notification`
  - `action_done`
  - `action_rehire`
  - `action_blacklist`
  - `action_view_survey_results`
- Giữ backend là nguồn sự thật, UI chỉ là lớp hiển thị đúng hơn.

Expected result:
- User chỉ thấy các nút mình thật sự được dùng.
- Trải nghiệm ít gây nhầm lẫn hơn.

Checklist test:
- So sánh user theo từng nhóm khi mở cùng một request offboarding.
- Kiểm tra tab và button hiển thị có đúng như expected matrix không.

Rủi ro:
- Nếu chỉ sửa UI mà chưa sửa backend đầy đủ, vẫn chưa an toàn.

### Phase 6 - Test phân quyền toàn diện

Mục tiêu:
- Chạy test người dùng thật theo từng nhóm trước khi coi là xong.

Nhóm user cần test:
- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`
- 1 user portal employee

Kịch bản test:
- mở list `approval.request`
- mở form `approval.request`
- sửa request nếu được phép
- xem `approval.approver`
- xem kết quả survey
- gửi BHXH
- gửi Adecco
- hoàn thành nghỉ việc
- rehire
- blacklist
- portal submit đơn
- portal mở survey
- portal complete activity

Expected result:
- Quyền thực tế khớp với ma trận expected đã chốt từ Phase 0.

Điểm dừng xác nhận:
- Chỉ sang Phase 7 khi mọi scenario chính đã pass.

### Phase 7 - Hoàn thiện tài liệu và regenerate structure

Mục tiêu:
- Đảm bảo tài liệu định hướng khớp với source mới sau khi đã sửa xong.

File liên quan:
- `addons/M02_P0213_00/structure/module_map.json`
- nếu có script generator trong `structure/`
- tài liệu notes liên quan tới phân quyền

Việc cần làm:
- Regenerate `module_map.json`.
- Nếu cần, cập nhật note review quyền hoặc note vận hành.
- Ghi lại final matrix và các giả định triển khai.

Expected result:
- Tài liệu, JSON map và source thống nhất.
- Người sau vào module có thể hiểu nhanh hơn.

## 4. Gợi ý triển khai theo từng đợt thực tế

### Đợt 1

Bao gồm:
- Phase 0
- Phase 1

Mục tiêu:
- Chốt thiết kế quyền và nền group.

Không nên làm ở đợt này:
- Chưa sửa mạnh ACL hoặc `sudo()`.

### Đợt 2

Bao gồm:
- Phase 2
- Phase 3

Mục tiêu:
- Siết quyền dữ liệu ở lớp security.

Không nên làm ở đợt này:
- Chưa thay đổi quá nhiều logic portal nếu chưa test xong rule.

### Đợt 3

Bao gồm:
- Phase 4
- Phase 5

Mục tiêu:
- Khóa chặt ở lớp backend logic và UI.

Không nên làm ở đợt này:
- Không đổi lại security domain lớn nếu chưa có lý do rõ ràng.

### Đợt 4

Bao gồm:
- Phase 6
- Phase 7

Mục tiêu:
- Test thật, chốt tài liệu, regenerate structure.

## 5. Điều kiện hoàn thành toàn bộ kế hoạch

Chỉ coi là hoàn tất khi đồng thời đạt đủ:
- ACL không còn mở rộng bất thường.
- Record rule chặn đúng scope nghiệp vụ.
- `sudo()` không bypass quyền vô điều kiện.
- UI khớp với backend.
- Test theo từng nhóm đều pass.
- JSON map đã được cập nhật lại nếu cần.

## 6. Gợi ý cách quản lý công việc khi bắt tay vào làm

Khi triển khai thật, nên tạo ticket hoặc checklist theo format:
- Phase
- File sẽ sửa
- Mục tiêu thay đổi
- Người review
- Checklist test sau phase
- Kết quả test
- Quyết định sang phase tiếp theo hay rollback

Format này sẽ giúp kiểm soát rủi ro tốt hơn thay vì sửa một lèo toàn bộ security và logic cùng lúc.
