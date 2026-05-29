# Plan Implementation Khóa Chặt Dữ Liệu 0213

Tài liệu này mô tả kế hoạch triển khai theo từng file để siết chặt phạm vi dữ liệu của module `M02_P0213_00`.

Tài liệu đã tham chiếu:
- Convention: `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213_00/structure/module_map.json`

Source chính dùng để xác nhận:
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0213_00/controllers/main.py`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`
- `addons/M02_P0200/security/security.xml`
- `odoo/addons/approvals/security/approval_security.xml`
- `odoo/addons/survey/security/survey_security.xml`

Lưu ý quan trọng:
- Nếu source hiện tại khác với JSON map, ưu tiên source hiện tại.
- Sau khi hoàn tất chỉnh sửa security, nên regenerate lại `structure/module_map.json`.

## 1. Mục tiêu triển khai

Mục tiêu là đưa `0213` về trạng thái:
- User chỉ thấy đúng dữ liệu offboarding OPS được phép thấy.
- User chỉ sửa đúng dữ liệu offboarding OPS được phép sửa.
- Portal chỉ thấy dữ liệu survey và activity của chính mình trong flow `0213`.
- Không còn phụ thuộc vào UI để chặn quyền.
- Các chỗ dùng `sudo()` vẫn giữ đúng ranh giới nghiệp vụ.

## 2. Phạm vi file cần sửa

File cần chỉnh trực tiếp:
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/controllers/main.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`

File cần rà soát đồng bộ:
- `addons/M02_P0200/security/security.xml`

## 3. Kế hoạch triển khai theo từng file

### 3.1. File `security/ir.model.access.csv`

Mục tiêu:
- Bỏ quyền nền quá rộng cho `base.group_user` trên các model nhạy cảm của flow `0213`.

Các dòng cần xử lý:
- `access_approval_request_internal_user`
- `access_survey_user_input_internal_user`
- rà thêm quyền liên quan tới `mail.activity` nếu muốn siết tiếp theo scope nghiệp vụ

Việc cần làm:
- Giảm hoặc loại bỏ ACL quá rộng đang cấp cho `base.group_user` trên `approval.request`.
- Giảm hoặc loại bỏ ACL quá rộng đang cấp cho `base.group_user` trên `survey.user_input`.
- Nếu cần giữ ACL nền để không ảnh hưởng module dùng chung, phải bù bằng record rule nội bộ chặt hơn ở bước sau.
- Không cấp `unlink` cho các model nghiệp vụ nhạy cảm nếu business không yêu cầu.

Expected result sau thay đổi:
- Internal user không còn mặc định có toàn quyền trên `approval.request` và `survey.user_input` chỉ vì có `base.group_user`.
- Quyền thật sự sẽ do ACL theo nhóm nghiệp vụ và record rule quyết định.

### 3.2. File `security/offboarding_request_rules.xml`

Mục tiêu:
- Hoàn thiện bộ `record rule` cho `approval.request`, `approval.approver`, và nếu cần thì thêm `mail.activity`.

Rule hiện có:
- `rule_0213_approval_request_ops_read`
- `rule_0213_approval_request_hr_manage`
- `rule_0213_approval_approver_scope_read`

Việc cần làm:
- Giữ rule đọc cho OPS, nhưng rà lại domain để chắc chắn chỉ áp cho offboarding `0213`.
- Tách rule HR quản lý thành các rule rõ mục đích nếu cần:
  - rule `read`
  - rule `write`
  - rule `create`
- Không để một rule quá rộng bao trùm mọi nhóm nếu quyền thực tế khác nhau.
- Bổ sung rule cho `approval.approver` nếu có nhu cầu sửa line approver; nếu không, chỉ giữ `read`.
- Bổ sung rule cho `mail.activity` theo domain:
  - activity gắn với `approval.request` thuộc offboarding `0213`
  - hoặc activity gắn với `hr.employee` liên kết tới request offboarding `0213`
- Nếu business có khái niệm phạm vi phụ trách theo store, department, manager, cần thêm domain theo phạm vi đó thay vì chỉ chặn theo category.

Expected result sau thay đổi:
- Người dùng chỉ thấy được `approval.request` và `approval.approver` thuộc flow `0213`.
- OPS chỉ xem được dữ liệu đúng loại.
- HR chỉ sửa được dữ liệu đúng loại và đúng vai trò.
- Activity hiển thị đúng phạm vi offboarding, không lộ các activity ngoài `0213`.

### 3.3. File `security/security.xml`

Mục tiêu:
- Bổ sung `record rule` cho `survey.user_input` phía internal, không chỉ portal.

Rule hiện có:
- `rule_psm_0213_survey_user_input_portal_own`

Việc cần làm:
- Giữ nguyên rule portal-own hiện tại.
- Bổ sung rule internal `read` cho `survey.user_input` chỉ áp với nhóm được phép xem kết quả survey trong `0213`.
- Domain phải khóa theo survey của `0213`, không dùng domain mở cho mọi survey response.
- Không mở `write`, `create`, `unlink` cho internal trên `survey.user_input` nếu business không cần.
- Nếu cần chỉnh sửa dữ liệu survey, phải chỉ định đúng nhóm rất hẹp và có rule riêng.

Expected result sau thay đổi:
- Portal chỉ thấy bài survey của chính mình.
- Internal chỉ đọc được survey response của flow offboarding `0213` nếu nằm trong nhóm được phép.
- Không còn tình trạng internal có `base.group_user` là xem rộng mọi `survey.user_input`.

### 3.4. File `models/resignation_request.py`

Mục tiêu:
- Mọi `sudo()` đều phải đi sau kiểm tra đúng quyền và đúng scope nghiệp vụ.

Method cần rà và chỉnh:
- `_check_0213_group_access`
- `action_view_survey_results`
- `action_send_adecco_notification`
- `action_send_social_insurance`
- `action_done`
- `action_rehire`
- `action_blacklist`
- các đoạn compute/search dùng `sudo()` với `mail.activity`, `survey.user_input`, `approval.request`

Việc cần làm:
- Tạo helper dùng chung để kiểm tra request có phải offboarding `0213` không.
- Trong `action_view_survey_results`, không chỉ search theo `email` hoặc `partner_id`, mà phải ràng thêm survey đúng của `0213` và đúng request hiện tại.
- Với các action nghiệp vụ, kiểm tra group trước khi `sudo().write()` hoặc `sudo().search()`.
- Với các đoạn compute activity, giới hạn domain để chỉ lấy activity liên quan tới offboarding `0213`.
- Với các luồng gửi mail hoặc cập nhật trạng thái, tránh để `sudo()` vô tình mở rộng sang bản ghi ngoài scope.
- Nếu có context bypass như `bypass_0213_group_check`, chỉ dùng ở luồng thật sự kiểm soát được và ghi rõ lý do.

Expected result sau thay đổi:
- Backend không còn bypass record rule một cách vô điều kiện.
- Mọi action nhạy cảm đều chặn đúng nếu user không thuộc nhóm phù hợp.
- Survey result và activity chỉ mở đúng trong biên nghiệp vụ `0213`.

### 3.5. File `controllers/main.py`

Mục tiêu:
- Siết chặt flow portal để mọi truy cập đều đúng owner và đúng scope `0213`.

Method cần rà:
- `_get_latest_resignation_request`
- `_get_owned_resignation_request_by_id`
- `_get_resignation_activities`
- `_get_or_create_exit_survey_url`
- `portal_activity_done`
- `portal_resignation_submit`

Việc cần làm:
- Giữ điều kiện `request_owner_id = request.env.user.id` khi lấy request.
- Trong `_get_resignation_activities`, đảm bảo chỉ lấy activity của request offboarding `0213`.
- Trong `_get_or_create_exit_survey_url`, không reuse nhầm `survey.user_input` cũ của cùng partner nhưng khác đợt hoặc khác flow.
- Khi tạo `survey.user_input`, lưu liên kết chặt với request hiện tại nếu cần.
- Trong `portal_activity_done`, xác nhận activity thuộc đúng request của chính user và đúng flow `0213`.
- Trong `portal_resignation_submit`, chỉ whitelist các field được phép từ portal; không cho portal tự can thiệp field nhạy cảm ngoài business flow.

Expected result sau thay đổi:
- Portal không thể đọc hay tác động activity/request ngoài đơn của chính mình.
- Portal không thể đụng nhầm survey response của đợt khác hoặc flow khác.
- Luồng portal vẫn hoạt động, nhưng không còn hở do `sudo()`.

### 3.6. File `views/resignation_request_views.xml`

Mục tiêu:
- Đồng bộ UI với backend, tránh lệch giữa `groups=` trên nút và check trong Python.

Nội dung cần rà:
- nút `action_send_social_insurance`
- nút `action_send_adecco_notification`
- nút `action_done`
- nút `action_rehire`
- nút `action_blacklist`
- nút `action_view_survey_results`
- các tab có `groups=`

Việc cần làm:
- Đảm bảo `groups=` trên view khớp với tuple `_GROUP_0213_*` trong `models/resignation_request.py`.
- Không dựa vào `invisible` để thay thế kiểm tra backend.
- Nếu nhóm nào không có quyền thật sự ở backend, không nên hiển thị nút ở UI.

Expected result sau thay đổi:
- Người dùng chỉ thấy đúng nút họ có quyền dùng.
- UI không tạo cảm giác “thấy được nhưng bấm bị chặn” quá nhiều.
- Logic view và logic Python nhất quán hơn.

### 3.7. File `addons/M02_P0200/security/security.xml`

Mục tiêu:
- Rà lại chain group để tránh lệch giữa “ý đồ business” và “ACL thực tế”.

Các group cần rà:
- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

Việc cần làm:
- Xác nhận nhóm nào thật sự phải imply `GDH_RST_ALL_BASE_S`.
- Nếu một nhóm cần dùng backend Odoo nhưng không imply `base.group_user`, phải quyết định:
  - hoặc thêm imply phù hợp
  - hoặc không dùng nhóm đó để cấp quyền model backend
- Sau khi chốt chain group, cập nhật lại ma trận quyền expected.

Expected result sau thay đổi:
- Nhóm 0200 có cấu trúc quyền rõ ràng, không mâu thuẫn với ACL/rule của `0213`.
- Không còn trường hợp rule đã khai báo nhưng group lại không đủ nền quyền để thực thi như kỳ vọng.

## 4. Thứ tự triển khai đề xuất

1. Chốt ma trận quyền expected theo từng nhóm 0200.
2. Rà chain group trong `M02_P0200/security/security.xml`.
3. Sửa `security/ir.model.access.csv`.
4. Sửa `security/offboarding_request_rules.xml`.
5. Sửa `security/security.xml`.
6. Sửa `models/resignation_request.py`.
7. Sửa `controllers/main.py`.
8. Rà đồng bộ `views/resignation_request_views.xml`.
9. Regenerate `structure/module_map.json` nếu có script generator phù hợp.

## 5. Checklist expected result sau toàn bộ triển khai

- `approval.request`
  - OPS chỉ đọc được offboarding đúng scope.
  - HR xử lý chỉ sửa được offboarding đúng scope.
  - User không thấy request ngoài phạm vi chỉ vì có quyền nền rộng.

- `approval.approver`
  - Chỉ đọc được approver lines của offboarding được phép xem.
  - Không ai sửa line approver nếu business chưa cho phép rõ ràng.

- `survey.user_input`
  - Portal chỉ thấy bài của chính mình.
  - Internal chỉ xem survey response của `0213` nếu có quyền.
  - Không ai vô tình xem hoặc sửa toàn bộ survey response chỉ vì có `base.group_user`.

- `mail.activity`
  - Chỉ hiển thị activity liên quan tới offboarding `0213`.
  - Portal chỉ hoàn thành activity được giao cho chính mình.

- `sudo()`
  - Mọi chỗ dùng `sudo()` đều có guard nghiệp vụ rõ ràng trước đó.

## 6. Rủi ro cần test sau khi sửa

- User nội bộ đang quen xem nhiều dữ liệu có thể bị mất quyền nếu ACL bị siết quá nhanh.
- Flow portal survey có thể hỏng nếu domain mới quá chặt nhưng chưa lưu đủ liên kết request-survey.
- Nếu user đang mang thêm group từ `approvals` hoặc `survey`, cần test lại vì quyền thực tế có thể vẫn rộng hơn mong muốn.

## 7. Bộ test tối thiểu sau triển khai

Test bằng user đại diện cho từng nhóm:
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
- mở danh sách và form `approval.request`
- mở `approval.approver`
- bấm nút nghiệp vụ trong form offboarding
- xem kết quả survey
- portal submit đơn
- portal mở survey
- portal complete activity
- internal xem activity offboarding

## 8. Gợi ý đầu ra tiếp theo sau file plan này

Sau khi duyệt plan, nên làm tiếp một tài liệu nhỏ hơn theo format:
- file nào sửa trước
- patch nào áp trước
- test case nào chạy ngay sau patch đó

Format này sẽ phù hợp nếu muốn triển khai từng bước an toàn trên môi trường dev/staging.
