# Checklist Test Phase 6 - 0213

Tài liệu này là checklist test cho Phase 6 của module `M02_P0213_00`.

Mục tiêu:
- Kiểm tra quyền thực tế sau các phase đã triển khai.
- Xác nhận UI và backend của `0213` đang khớp nhau.
- Xác nhận dữ liệu của flow offboarding không bị lộ rộng ngoài scope mong muốn.

Tài liệu tham chiếu:
- `addons/M02_P0213_00/notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md`
- `addons/M02_P0213_00/notes/PHASE_1_DOI_CHIEU_EXPECTED_VS_ACTUAL_GROUP_CHAIN_0213.md`
- `addons/M02_P0213_00/notes/PLAN_IMPLEMENTATION_KHOA_CHAT_DU_LIEU_0213.md`
- `addons/M02_P0213_00/notes/PHASE_PLAN_TRIEN_KHAI_KHOA_CHAT_DU_LIEU_0213.md`

Source chính đã tác động:
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/controllers/main.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`

## 1. Nguyên tắc test

- Test trên môi trường dev hoặc staging.
- Mỗi lần test chỉ login đúng 1 user đại diện cho 1 nhóm.
- Nếu user có thêm group ngoài nhóm chính cần test, phải ghi chú rõ.
- Nên có ít nhất 2 request mẫu:
  - 1 request offboarding `0213` đang `approved`
  - 1 request offboarding `0213` đang `done`
- Nên có ít nhất 1 survey exit interview đã hoàn thành.
- Nên có ít nhất 1 activity active và 1 activity inactive trên request offboarding.

## 2. User mẫu cần chuẩn bị

Chuẩn bị user đại diện cho các nhóm sau:
- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`
- 1 portal employee

Ghi chú trước khi test:
- User nào là internal user
- User nào là portal user
- User nào có thêm group core như `approvals.group_approval_user` hoặc `approvals.group_approval_manager`
- Nếu có thêm group ngoài dự kiến, phải đánh dấu vì có thể làm sai lệch kết quả

## 3. Dữ liệu test cần có

Chuẩn bị tối thiểu:
- 1 request offboarding `0213` của nhân viên A ở trạng thái `approved`
- 1 request offboarding `0213` của nhân viên A ở trạng thái `done`
- 1 request approval không thuộc `0213` để kiểm tra không bị lộ
- 1 survey exit interview của `0213`
- 1 survey khác không thuộc `0213`
- 1 `survey.user_input` đã `done` của survey exit interview `0213`
- 1 `survey.user_input` của survey khác
- activity gắn với `approval.request` thuộc `0213`
- activity gắn với `hr.employee` liên quan request `0213`
- activity không thuộc `0213`

## 4. Checklist test chung cho từng user internal

Thực hiện cho từng user internal trong danh sách:

### 4.1. Truy cập request offboarding

- Mở menu hoặc action dẫn tới `approval.request`
- Tìm request offboarding `0213`
- Mở form request offboarding `0213`
- Kiểm tra có mở được không
- Kiểm tra request không thuộc `0213` có hiện hay không

Expected:
- Chỉ thấy được request đúng theo scope hiện tại của `0213`
- Không thấy rộng các request ngoài `0213` chỉ vì cùng model `approval.request`

### 4.2. Kiểm tra tab và nút trên form

- Mở form request offboarding `0213`
- Kiểm tra có thấy tab `Thông tin nghỉ việc` không
- Kiểm tra có thấy tab `Quá trình nghỉ việc` không
- Kiểm tra từng nút:
  - `Gửi thông tin bảo hiểm xã hội`
  - `Gửi thông tin Adecco`
  - `Hoàn thành nghỉ việc`
  - `Tái tuyển`
  - `Đưa vào Blacklist`
  - `Xem kết quả`

Expected:
- Chỉ thấy các tab/nút đúng với nhóm được phép trong Phase 5
- Những nhóm không còn trong `groups=` của view thì không được thấy

### 4.3. Kiểm tra survey result

- Trên request có `x_psm_0213_exit_survey_completed = True`
- Bấm `Xem kết quả`
- Kiểm tra có mở đúng `survey.user_input` của `0213` không
- Kiểm tra có đọc được survey khác ngoài `0213` không

Expected:
- Chỉ mở được survey result của exit interview `0213`
- Không mở lan sang survey khác

### 4.4. Kiểm tra activity

- Trên form request offboarding `0213`, xem tab `Quá trình nghỉ việc`
- Kiểm tra có thấy activity của request `0213` không
- Kiểm tra có thấy activity inactive không
- Kiểm tra không thấy activity ngoài `0213`

Expected:
- Chỉ thấy activity liên quan flow offboarding đang kiểm thử

## 5. Checklist riêng theo từng nhóm internal

### 5.1. `GDH_RST_OPS_OC_S`

Kiểm tra:
- Có vào được backend của request `0213` không
- Có thấy tab nghiệp vụ backend không
- Có thấy nút xử lý HR không

Expected:
- Với hướng siết hiện tại của `0213`, nhóm này không nên có đầy đủ UI backend như trước

### 5.2. `GDH_RST_OPS_OM_M`

Kiểm tra:
- Có thấy request `0213` không
- Có thấy `Xem kết quả` không
- Có thấy tab `Thông tin nghỉ việc` không

Expected:
- Theo UI đã siết của Phase 5, nhóm này không còn được hiển thị backend tab/nút như trước

### 5.3. `GDH_RST_HR_ADMIN_S`

Kiểm tra:
- Có thấy nút `Gửi BHXH`
- Có thấy nút `Gửi Adecco`
- Có thấy `Xem kết quả`

Expected:
- Theo UI hiện tại sau Phase 5, nhóm này không còn được hiển thị các nút backend đã thu hẹp

### 5.4. `GDH_RST_HR_ADMIN_M`

Kiểm tra:
- Thấy request `0213`
- Thấy tab `Thông tin nghỉ việc`
- Thấy tab `Quá trình nghỉ việc`
- Thấy `Xem kết quả`
- Thấy `Gửi BHXH`
- Thấy `Gửi Adecco`
- Thấy `Hoàn thành nghỉ việc`
- Thấy `Tái tuyển`
- Không thấy `Đưa vào Blacklist` nếu không thuộc nhóm đúng

Expected:
- Đây là một trong các nhóm chính còn được giữ UI backend trong `0213`

### 5.5. `GDH_RST_HR_HRBP_S`

Kiểm tra:
- Có còn thấy tab/nút backend đã bị thu hẹp không

Expected:
- Không còn được hiển thị UI backend rộng như trước

### 5.6. `GDH_RST_HR_HRBP_M`

Kiểm tra:
- Có thấy `Hoàn thành nghỉ việc`
- Có thấy `Tái tuyển`
- Có thấy `Đưa vào Blacklist`

Expected:
- Theo hướng B và UI sau Phase 5, nhóm này không còn được hiển thị các action backend tương ứng

### 5.7. `GDH_RST_HR_HEAD_M`

Kiểm tra:
- Thấy request `0213`
- Thấy tab `Thông tin nghỉ việc`
- Thấy tab `Quá trình nghỉ việc`
- Thấy `Xem kết quả`
- Thấy `Gửi BHXH`
- Thấy `Gửi Adecco`
- Thấy `Hoàn thành nghỉ việc`
- Thấy `Tái tuyển`
- Thấy `Đưa vào Blacklist`

Expected:
- Là một trong các nhóm backend chính còn quyền rộng trong `0213`

### 5.8. `GDH_RST_SYSTEM_ST_M`

Kiểm tra:
- Tương tự `HR_HEAD_M`

Expected:
- Có quyền rộng nhất trên UI/backend trong `0213`

## 6. Checklist riêng cho portal user

### 6.1. Submit đơn

- Login bằng portal employee
- Mở `/my/resignation/ops`
- Submit đơn nghỉ việc

Expected:
- Tạo được request của chính user đó
- Không tạo được request cho người khác

### 6.2. Xem request của mình

- Sau khi có request, mở lại trang portal
- Kiểm tra chỉ thấy request của chính mình

Expected:
- Không thấy request của user khác

### 6.3. Xem activity của mình

- Trên portal, kiểm tra danh sách activity
- Thử đánh dấu hoàn thành activity được giao cho chính mình

Expected:
- Chỉ hoàn thành được activity thuộc request của chính user
- Không hoàn thành được activity của người khác

### 6.4. Survey URL và survey response

- Mở link exit survey từ portal
- Kiểm tra link dẫn đúng survey exit interview `0213`
- Hoàn thành survey
- Kiểm tra portal không đọc được survey response của người khác

Expected:
- Survey URL bám đúng request của chính user
- Không reuse nhầm survey response ngoài đúng flow hiện tại

## 7. Checklist test dữ liệu ngoài scope

### 7.1. Request ngoài `0213`

- Dùng cùng user test, cố mở request approval không thuộc `0213`

Expected:
- Không thấy hoặc không thao tác được theo thiết kế siết hiện tại

### 7.2. Survey ngoài `0213`

- Dùng user internal được phép xem survey result `0213`
- Thử mở survey khác không thuộc `0213`

Expected:
- Không đọc rộng mọi survey response ngoài `0213` chỉ vì có quyền nội bộ

### 7.3. Activity ngoài `0213`

- Dùng user internal
- Kiểm tra activity ngoài offboarding `0213`

Expected:
- Không bị lộ qua form/tab của `0213`

## 8. Checklist test hồi quy các action chính

Test lại sau khi siết:
- `action_view_survey_results`
- `action_send_social_insurance`
- `action_send_adecco_notification`
- `action_done`
- `action_rehire`
- `action_blacklist`
- portal submit
- portal survey URL
- portal activity done

Expected:
- Action đúng nhóm thì chạy được
- Sai nhóm thì không thấy hoặc không gọi được
- Không có trường hợp mở nhầm dữ liệu ngoài request offboarding hiện tại

## 9. Cách ghi kết quả test

Cho mỗi case, ghi:
- User test
- Nhóm chính
- Có group bổ sung hay không
- Bước test
- Kết quả thực tế
- Expected
- Pass / Fail
- Ghi chú lệch nếu có

## 10. Tiêu chí pass cho Phase 6

Phase 6 được coi là pass khi:
- UI khớp với nhóm đã giữ lại trong Phase 5
- Survey result không mở rộng ngoài `0213`
- Portal chỉ thao tác đúng dữ liệu của mình
- Không có action backend nào bị hở rộng do `sudo()` trong các luồng chính đã siết
- Các nhóm `HR_ADMIN_M`, `HR_HEAD_M`, `SYSTEM_ST_M` hoạt động đúng trên flow `0213`

## 11. Rủi ro cần ghi chú khi test

- Nếu user có thêm group core ngoài nhóm test, kết quả có thể rộng hơn expected
- Nếu dữ liệu test không sạch, survey response cũ có thể làm khó đánh giá
- Nếu request chưa có đủ activity hoặc survey completed, một số nút sẽ ẩn theo nghiệp vụ chứ không phải do lỗi quyền
