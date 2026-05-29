# Rà soát các ý sai trong Blueprint Spec v3 - Module M02_P0213

Ngày rà soát: 29/04/2026

Blueprint được rà soát: `D:\download Internet\GHD_HR_0213_Blueprint_Spec_v3.md`

## Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`.
- JSON map: `addons/M02_P0213/structure/module_map.json`.
- JSON stats: `addons/M02_P0213/structure/module_map_stats.json`.
- Source xác nhận chính:
  - `addons/M02_P0213/__manifest__.py`
  - `addons/M02_P0213/controllers/main.py`
  - `addons/M02_P0213/models/resignation_request.py`
  - `addons/M02_P0213/models/survey_user_input.py`
  - `addons/M02_P0213/models/mail_activity.py`
  - `addons/M02_P0213/models/res_company.py`
  - `addons/M02_P0213/security/security.xml`
  - `addons/M02_P0213/security/offboarding_request_rules.xml`
  - `addons/M02_P0213/security/ir.model.access.csv`
  - `addons/M02_P0213/views/resignation_request_views.xml`

## Ghi chú chung

File blueprint có nội dung tiếng Việt bị mojibake khi đọc từ disk, nhưng các ý kỹ thuật vẫn nhận diện được qua tên module, model, field, method, XML id và nội dung nghiệp vụ đi kèm.

## Tỷ lệ chính xác với source hiện tại

Tỷ lệ chính xác ước tính: **khoảng 59%** so với source module `M02_P0213` hiện tại.

Cách tính: rà soát các mệnh đề kỹ thuật/nghiệp vụ có thể kiểm chứng trực tiếp trong source. Có **19 ý khớp hoặc cơ bản khớp** và **13 ý sai/lệch** đã liệt kê chi tiết bên dưới. Vì vậy tỷ lệ chính xác được tính là:

```text
19 / (19 + 13) = 59,38% ~ 59%
```

Các ý khớp dùng làm mẫu số chính xác:

- Blueprint ghi module là `M02_P0213`: khớp `__manifest__.py` và `structure/module_map.json`.
- Blueprint ghi depends gồm `base`, `mail`, `approvals`, `hr`, `portal`, `survey`, `M02_P0200`: khớp `__manifest__.py:15-23`.
- Blueprint ghi primary model là `approval.request`: khớp `models/resignation_request.py:20-21`.
- Blueprint ghi core file `models/resignation_request.py` dài 1246 lines: khớp số dòng thực tế của file.
- Blueprint ghi có `mail_activity.py`, `res_company.py`, `res_config_settings.py`, `survey_user_input.py`: khớp `structure/module_map.json`.
- Blueprint ghi có `approval.category` extension với `x_psm_0213_is_offboarding`: khớp `models/resignation_request.py:10-17`.
- Blueprint ghi không có custom model hoàn toàn mới: khớp map, toàn bộ model entries đều là `inherit_only`.
- Blueprint ghi có portal form `resignation_portal_template.xml`: khớp `__manifest__.py:37`.
- Blueprint ghi có portal submit tạo `approval.request`: khớp `controllers/main.py:137-184`.
- Blueprint ghi có `survey_exit_interview_data.xml`: khớp `__manifest__.py:25`.
- Blueprint ghi có `approval_category_data.xml`: khớp `__manifest__.py:29`.
- Blueprint ghi có 5 email template: khớp `__manifest__.py:30-34`.
- Blueprint ghi có daily reminder cron: khớp `__manifest__.py:35` và `models/resignation_request.py:1119-1181`.
- Blueprint ghi có `offboarding_activity_plan_data.xml`: khớp `__manifest__.py:36`.
- Blueprint ghi `request_status` được `selection_add` thêm `done`: khớp `models/resignation_request.py:80-85`.
- Blueprint ghi có các field `x_psm_0213_is_plan_launched`, `x_psm_0213_adecco_notification_sent`, `x_psm_0213_is_rehire`, `x_psm_0213_is_blacklisted`: khớp `models/resignation_request.py:87-96` và `models/resignation_request.py:163-169`.
- Blueprint ghi employee info fields trên `approval.request`: khớp `models/resignation_request.py:98-125`.
- Blueprint ghi có `x_psm_0213_is_social_insurance_contract` computed từ contract type: khớp `models/resignation_request.py:150-158`, `models/resignation_request.py:189-212`, `models/resignation_request.py:639-642`.
- Blueprint ghi có các action `action_rehire`, `action_blacklist`, `action_manual_reminder_extension`: khớp `models/resignation_request.py:1083-1117` và `models/resignation_request.py:1183-1246`.

Các ý sai/lệch là 13 mục từ mục 1 đến mục 13 bên dưới. Tỷ lệ 59% phản ánh việc blueprint mô tả khá đúng cấu trúc module và danh sách thành phần, nhưng lệch ở nhiều hành vi nghiệp vụ cốt lõi.

## 1. Sai: module có 5 models

Blueprint metadata ghi module có `5 models`.

Theo `structure/module_map_stats.json`, module hiện có `model_count = 6`. Lý do là map tính cả extension `approval.category` và `approval.request` trong cùng `resignation_request.py`, ngoài các extension khác.

Dẫn chứng:

- `structure/module_map_stats.json`: `model_count` là `6`.
- `structure/module_map.json`: có các model entries cho `mail.activity`, `res.company`, `res.config.settings`, `approval.category`, `approval.request`, `survey.user_input`.
- `models/resignation_request.py:10-17`: class `ApprovalCategory` inherit `approval.category`.
- `models/resignation_request.py:20-21`: class `ResignationRequest` inherit `approval.request`.

## 2. Sai: portal submit tạo request ở trạng thái `draft`

Blueprint data flow và AC-001 ghi portal submit tạo `approval.request` với `state='draft'`.

Source hiện tại tạo request rồi gọi `action_confirm()` ngay. Vì vậy request đi vào luồng confirm, không dừng ở draft sau submit.

Dẫn chứng:

- `controllers/main.py:181-182`: tạo `approval.request`, sau đó gọi `approval_request.sudo().action_confirm()`.
- `models/resignation_request.py:80-85`: module dùng `request_status`, không mở rộng `state`.
- Trong source 0213 không có đoạn portal submit ghi `state='draft'`.

## 3. Sai: flow dùng `state='pending'`, `state='done'`

Blueprint mô tả luồng bằng `state='draft'`, `state='pending'`, `state='done'`.

Source 0213 dùng trường `request_status` của Approvals, không dùng field `state` làm trạng thái chính của request.

Dẫn chứng:

- `models/resignation_request.py:80-85`: `request_status` được `selection_add` thêm `done`.
- `models/resignation_request.py:533`, `models/resignation_request.py:552`: withdraw/cancel kiểm tra `request_status`.
- `models/resignation_request.py:1034`: Done ghi `request_status = "done"`.
- `models/resignation_request.py:1134-1137`: cron lọc `request_status = "approved"`.
- `views/resignation_request_views.xml:51-53`: statusbar hiển thị `new,pending,approved,done` trên field `request_status`.

## 4. Sai: HR Approve tự động gửi Adecco notification

Blueprint ghi `action_approve()` trigger exit survey và Adecco notification.

Source `action_approve()` chỉ gọi exit survey và tự động schedule offboarding activities. Không có lời gọi `action_send_adecco_notification()` trong `action_approve()`.

Dẫn chứng:

- `models/resignation_request.py:837-872`: toàn bộ `action_approve()`.
- `models/resignation_request.py:854-856`: request offboarding chỉ gọi `request.action_send_exit_survey()`.
- `models/resignation_request.py:867-870`: nếu có plan và employee thì `_schedule_offboarding_activities(plan)` và set `x_psm_0213_is_plan_launched = True`.
- Không có lời gọi `action_send_adecco_notification()` trong đoạn `models/resignation_request.py:837-872`.

## 5. Sai: `action_launch_plan()` là gate launch plan một lần và chặn duplicate activities

Blueprint mô tả `action_launch_plan()` chỉ launch một lần bằng guard `is_plan_launched = False`, AC-003 ghi lần 2 phải UserError hoặc không tạo duplicate activities.

Source hiện tại không dùng `action_launch_plan()` để tạo checklist activities trong flow approve. Flow approve gọi trực tiếp `_schedule_offboarding_activities(plan)`. Method `action_launch_plan()` chỉ mở wizard `hr.plan_wizard_action`, set `x_psm_0213_is_plan_launched = True` và không kiểm tra guard trước đó.

Dẫn chứng:

- `models/resignation_request.py:867-870`: approve tự động schedule activities và set plan launched.
- `models/resignation_request.py:931-951`: `action_launch_plan()` chỉ set `x_psm_0213_is_plan_launched = True` rồi trả về wizard action.
- `views/resignation_request_views.xml:15-16`: nút `action_launch_plan` đang bị comment, không phải nút vận hành chính trên form.
- `models/resignation_request.py:931-951`: không có `if self.x_psm_0213_is_plan_launched: raise UserError(...)`.

## 6. Sai: Done deactivate `hr.employee.active = False`

Blueprint ghi `action_done()` sẽ set `hr.employee.active = False`.

Source hiện tại không deactivate `hr.employee`. Code tìm `res.users` từ `employee.user_id` hoặc `request_owner_id`, rồi set `res.users.active = False`.

Dẫn chứng:

- `models/resignation_request.py:1039-1048`: xác định `user_to_deactivate` từ employee user hoặc request owner.
- `models/resignation_request.py:1050-1055`: gọi `user_to_deactivate.write({'active': False})`.
- Không có đoạn `x_psm_0213_employee_id.write({'active': False})` trong `action_done()`.

## 7. Sai: Done hủy/cancel contract

Blueprint AC-005 và downstream ghi Done sẽ cancel contract.

Source `action_done()` chỉ kiểm tra survey/checklist, set `request_status = done`, deactivate user và hoàn tất một số todo activity. Không có logic hủy hợp đồng.

Dẫn chứng:

- `models/resignation_request.py:1014-1081`: toàn bộ `action_done()`, không có thao tác trên `hr.contract`.
- Tìm trong module không có logic gọi cancel/close contract trong `action_done()`.

## 8. Sai: `action_send_social_insurance()` chỉ gửi BHXH và log chatter

Blueprint AC-007 ghi HR bấm Send BHXH Notification thì email BHXH template gửi và chatter log.

Source hiện tại sau khi gửi template BHXH lại gọi `self.action_done()`. Như vậy action này không chỉ gửi email, mà còn hoàn tất quy trình nếu các điều kiện Done đạt.

Dẫn chứng:

- `models/resignation_request.py:672-676`: nếu có template thì `template.sudo().send_mail(...)` rồi `self.action_done()`.
- `models/resignation_request.py:660-695`: không có `message_post()` riêng cho chatter log trong action gửi BHXH.

## 9. Sai: Employee record rule chỉ thấy đơn của mình trên `approval.request`

Blueprint mục record rules ghi employee chỉ thấy đơn mình theo `request_owner_id = user`.

Source security hiện tại không có record rule `approval.request` cho portal/employee own request. Portal controller dùng `sudo()` và tự lọc theo `request_owner_id`; record rule own chỉ tồn tại cho `survey.user_input`.

Dẫn chứng:

- `security/offboarding_request_rules.xml:10-24`: rule OPS read scope cho group OPS OC/OM, domain theo `category_id.x_psm_0213_is_offboarding`.
- `security/offboarding_request_rules.xml:26-63`: rule HR read/write scope, domain theo offboarding category.
- `security/security.xml:71-76`: rule portal own chỉ áp dụng cho `survey.user_input`, không phải `approval.request`.
- `controllers/main.py:31-43`: portal lấy latest/owned request bằng `sudo()` và domain `request_owner_id = request.env.user.id`.

## 10. Sai hoặc diễn đạt lệch: Line Manager/OC chỉ thấy subordinates

Blueprint ACL ghi Line Manager/OC thấy subordinates.

Source rule cho OPS OC/OM không lọc theo cấp dưới. Domain chỉ là category offboarding. Line manager được gán làm approver khi portal submit, nhưng record rule OPS scope không phải subordinate scope.

Dẫn chứng:

- `security/offboarding_request_rules.xml:10-24`: nhóm `GDH_RST_OPS_OC_S`, `GDH_RST_OPS_OM_M` có read scope theo `category_id.x_psm_0213_is_offboarding`, không có domain theo employee hierarchy.
- `controllers/main.py:168-179`: line manager được thêm vào `approver_ids` nếu employee có parent user.

## 11. Sai: HR HRBP M có quyền Blacklist trên UI

Blueprint ACL ghi HR HRBP M có quyền Blacklist.

Ở backend method `_GROUP_0213_BLACKLIST` có HRBP M, nhưng nút Blacklist trên form chỉ hiển thị cho HR Head M và System ST M. Vì blueprint đang mô tả theo vai trò sử dụng UI, phần HRBP M có quyền Blacklist là lệch với view hiện tại.

Dẫn chứng:

- `models/resignation_request.py:70-74`: `_GROUP_0213_BLACKLIST` gồm HRBP M, Head M, System ST M.
- `views/resignation_request_views.xml:45-49`: nút `action_blacklist` chỉ có groups `GDH_RST_HR_HEAD_M,GDH_RST_SYSTEM_ST_M`, không có `GDH_RST_HR_HRBP_M`.

## 12. Sai: Blacklist block rehire

Blueprint BR-OFF-010 và AC-006 ghi blacklist chặn tái tuyển/recruitment.

Source `action_blacklist()` chỉ set boolean và post message/notification. Không có logic kiểm tra trong recruitment, không có constraint, không có override create applicant/recruitment để block tái tuyển.

Dẫn chứng:

- `models/resignation_request.py:1100-1117`: `action_blacklist()` chỉ write `x_psm_0213_is_blacklisted = True`, post message và trả notification.
- Không có source trong module 0213 tác động đến recruitment/applicant để chặn tái tuyển.

## 13. Sai: Daily reminder gửi HR Manager và Line Manager

Blueprint email template table ghi cron daily gửi `email_template_offboarding_reminder` cho HR Manager và `email_template_dept_offboarding_reminder` cho Line Manager.

Source cron không hard-code HR Manager/Line Manager. Nó group các overdue activities theo `activity.user_id`: nếu user là request owner thì gửi employee reminder, còn các user khác nhận department reminder.

Dẫn chứng:

- `models/resignation_request.py:1142-1156`: lấy overdue activities và group theo user.
- `models/resignation_request.py:1163-1171`: nếu `user == req.request_owner_id` thì gửi employee template, ngược lại gửi department template tới email của activity user.
- `models/resignation_request.py:874-924`: assignee của activity lấy theo responsible type của template hoặc default responsible user, không mặc định luôn là HR Manager/Line Manager.

## Tổng kết

Blueprint v3 của 0213 khớp tốt ở tầng cấu trúc: module name, dependency, file chính, model extension, field chính, template, survey, cron và activity plan. Tuy nhiên các điểm lệch nằm ở nghiệp vụ vận hành:

- Portal submit không dừng ở draft.
- Flow dùng `request_status`, không dùng `state`.
- Approve không tự gửi Adecco.
- Launch plan không có guard như blueprint mô tả.
- Done deactivate `res.users`, không deactivate `hr.employee`, và không cancel contract.
- BHXH action gọi luôn `action_done()`.
- Record rule employee own request không nằm ở security XML mà được kiểm soát trong portal controller bằng `sudo()` + domain.
- Blacklist chỉ là flag trong module 0213, chưa có logic block recruitment.
- Cron reminder gửi theo activity assignee, không cố định HR Manager/Line Manager.

Nếu blueprint là tài liệu mô tả source hiện tại, nên cập nhật lại các mục trên. Nếu blueprint là yêu cầu mong muốn, source module 0213 cần chỉnh tương ứng và regenerate `structure/module_map.json` sau khi sửa.
