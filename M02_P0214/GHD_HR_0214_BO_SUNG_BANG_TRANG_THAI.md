# Bổ sung thông tin còn thiếu cho bảng quy trình GHD_HR_0214

## Mục đích

Tài liệu này bổ sung các thông tin còn thiếu trong bảng quy trình `GHD_HR_0214` ở ảnh chụp màn hình, theo hướng:

- ưu tiên xác nhận bằng source thật của module `M02_P0214`
- nếu source không có custom riêng cho một bước thì ghi rõ là `chưa thấy custom riêng`
- nếu một giá trị là suy luận hợp lý từ flow hệ thống thì ghi rõ là `suy luận từ flow`

## Nguồn đã dùng để xác nhận

- File convention đã dùng:
  - `addons/M02_P0200/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- File JSON map đã dùng:
  - `addons/M02_P0214/structure/module_map.json`
- Source chính dùng để xác nhận:
  - `addons/M02_P0214/__manifest__.py`
  - `addons/M02_P0214/controllers/main.py`
  - `addons/M02_P0214/models/approval_request_rst_approval.py`
  - `addons/M02_P0214/models/approval_request_rst_fields.py`
  - `addons/M02_P0214/models/approval_request_rst_offboarding.py`
  - `addons/M02_P0214/models/approval_request_rst_reminder.py`
  - `addons/M02_P0214/models/approval_request_rst_survey.py`
  - `addons/M02_P0214/models/mail_activity.py`
  - `addons/M02_P0214/models/survey_user_input.py`
  - `addons/M02_P0214/security/ir.model.access.csv`
  - `addons/M02_P0214/security/offboarding_request_rules.xml`
  - `addons/M02_P0214/security/security.xml`
  - `addons/M02_P0214/data/approval_category_data.xml`
  - `addons/M02_P0214/data/offboarding_plan_rst.xml`
  - `addons/M02_P0214/data/email_template_exit_survey.xml`
  - `addons/M02_P0214/data/email_template_adecco_notification.xml`
  - `addons/M02_P0214/data/email_template_social_insurance.xml`
  - `addons/M02_P0214/data/email_template_offboarding_reminder.xml`
  - `addons/M02_P0214/data/email_template_dept_offboarding_reminder.xml`
  - `addons/M02_P0214/data/ir_cron_data.xml`
  - `addons/M02_P0214/views/resignation_request_views.xml`
  - `addons/M02_P0214/views/offboarding_report_views.xml`
  - `addons/M02_P0214/views/res_company_views.xml`

## Bảng bổ sung

Ghi chú cách đọc:

- `Pre State` và `Current State` là trạng thái nghiệp vụ gần nhất có thể map từ source hiện tại.
- `Status` là mức độ hiện thực trong module:
  - `Đã có trong source`
  - `Có một phần`
  - `Chưa thấy custom riêng`
- `Link` là action, route, cron hoặc file/source chính liên quan trực tiếp đến bước đó.

| Bước | Actors | Mô tả bước | Pre State | Current State | Status | Link | Note | Model | Survey | Approval | Mail | Rule | ACL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | HR Admin, HR Head, System | HR cấu hình checklist offboarding cần thực hiện | Chưa phát sinh đơn nghỉ việc | Cấu hình nền sẵn sàng cho flow `0214` | Đã có trong source | `views/res_company_views.xml`, `data/offboarding_plan_rst.xml` | Cấu hình checklist được thể hiện qua `mail.activity.plan` và các template activity của plan | `res.company`, `res.config.settings`, `mail.activity.plan`, `mail.activity.plan.template` | Không | Không | Không | Chưa thấy `ir.rule` riêng cho `mail.activity.plan` | Quyền cấu hình chủ yếu thuộc user nội bộ có quyền vào màn config |
| B2 | HR Admin | HR tạo mẫu exit interview | Chưa có hoặc chưa chọn mẫu khảo sát | Mẫu survey sẵn sàng dùng cho bước gửi khảo sát | Đã có trong source | `data/survey_exit_interview_data.xml` | Survey được seed sẵn, không phải flow nhập tay riêng trong custom | `survey.survey`, `survey.question`, `survey.question.answer` | `survey_exit_interview` | Không | Không | `rule_psm_0214_survey_internal_read`, `rule_psm_0214_survey_question_internal_read`, `rule_psm_0214_survey_question_answer_internal_read` | ACL survey nội bộ là read, portal là read theo model tương ứng |
| B3 | Nhân viên | Nhân viên tạo và gửi đơn xin nghỉ | Chưa có đơn hoặc `new` | `pending` sau khi `action_confirm()` | Đã có trong source | Route `/my/resignation/rst/submit`, `action_confirm()` | Đơn được tạo từ portal và chuyển sang `pending`, đồng thời tạo approver activity | `approval.request`, `approval.approver`, `hr.employee`, `hr.departure.reason` | Không | `approval_category_resignation` | Không | `rule_0214_approval_request_rst_read`, `rule_0214_approval_request_rst_manage`, `rule_0214_approval_approver_rst_read` | Portal có quyền tạo/đọc `approval.request`; nội bộ có ACL trên `approval.request` |
| B4 | Quản lý, Nhân viên | Quản lý thương lượng với nhân viên, TH1 thành công thì dừng quy trình | `pending` | Suy luận từ flow: vẫn ở `pending` hoặc người dùng rút/hủy đơn | Chưa thấy custom riêng | Không thấy method riêng trong module | Đây là bước nghiệp vụ có trong bảng quy trình nhưng chưa thấy action riêng trong code `0214` | `approval.request` | Không | `approval request` | Không | Theo rule chung của `approval.request` | Theo ACL chung của `approval.request` |
| B5 | Quản lý | Xác nhận ngày nghỉ | `pending` | `pending` nhưng đã có `x_psm_0214_resignation_date` | Đã có trong source | `action_approve()` trong `models/approval_request_rst_approval.py` | Code chặn approve nếu chưa có ngày nghỉ dự kiến | `approval.request` | Không | `approval request` | Không | `rule_0214_approval_request_rst_manage` | ACL ghi trên `approval.request` cho user nội bộ |
| B6 | Quản lý, HR | Duyệt đơn xin nghỉ | `pending` | `approved` | Đã có trong source | `action_approve()` | Sau khi approve, hệ thống tự gửi exit survey và launch offboarding plan | `approval.request`, `approval.approver` | Có, được kích hoạt sau approve | `approval request` | `email_template_exit_survey` | `rule_0214_approval_request_rst_read/manage`, `rule_0214_approval_approver_rst_read` | ACL chuẩn trên `approval.request` và `approval.approver` |
| B7 | Nhân viên | Nhân viên thực hiện offboarding theo checklist ở bước 1 | `approved`, `x_psm_0214_is_plan_launched = True` | `approved`, checklist còn đang xử lý | Đã có trong source | `data/offboarding_plan_rst.xml`, `_schedule_offboarding_activity()` | Đây là các activity được tạo tự động sau approve | `mail.activity` | Không | Không | Có thể phát sinh mail reminder nếu quá hạn | Chưa thấy `ir.rule` riêng cho `mail.activity` trong `0214` | Portal có thể thao tác activity của chính mình qua route portal; nội bộ có ACL `mail.activity` |
| B8 | Nhân viên | Nhân viên làm exit interview theo mẫu ở bước 2 | `approved`, survey chưa hoàn thành | `approved`, `x_psm_0214_exit_survey_completed = True` khi response `done` | Đã có trong source | `action_send_exit_survey()`, `survey_user_input.py` | `survey.user_input` được gắn lại với đúng request `0214` và khi `done` thì cập nhật logic hoàn thành | `survey.user_input`, `survey.user_input.line` | `survey_exit_interview` | Không | `email_template_exit_survey` | `rule_psm_0214_survey_user_input_portal_own`, `rule_psm_0214_survey_user_input_internal_read`, `rule_psm_0214_survey_user_input_line_internal_read` | Portal có create/write trên `survey.user_input` và `survey.user_input.line` |
| B9 | Nhân viên | Tiến hành bàn giao công việc, tài liệu, giấy tờ liên quan | `approved`, activity đang `pending` | Activity `pending` hoặc `done` tùy từng việc | Đã có trong source | `rst_template_handover` trong `data/offboarding_plan_rst.xml` | Có activity riêng cho bàn giao công việc/tài liệu/giấy tờ | `mail.activity` | Không | Không | Có thể có reminder nếu trễ | Chưa thấy rule riêng cho activity này | ACL chung `mail.activity` |
| B10 | Quản lý | Đánh giá công việc bàn giao | Suy luận từ flow: activity bàn giao đã được nhân viên cập nhật | Suy luận từ flow: manager kiểm tra trước khi checklist được xem là xong | Có một phần | Dựa trên việc activity được mark done và hiển thị trong form/report | Chưa thấy method review riêng cho manager, nhưng màn hình có danh sách checklist để theo dõi | `mail.activity`, `approval.request` | Không | Không | Không thấy mail riêng | Chưa thấy rule riêng | ACL chung `mail.activity`, `approval.request` |
| B11 | HR, HRBP, HR Head | Xác nhận hoàn tất thu hồi các checklist | Survey và activity đã đủ hoặc đang được rà soát | `x_psm_0214_all_activities_completed = True` | Đã có trong source | `action_checklist_completed()` | Hệ thống đối chiếu survey + activities rồi `message_post()` kết quả hoàn tất/chưa hoàn tất | `approval.request`, `mail.activity` | Có tham gia điều kiện hoàn tất | Không | Không tạo mail mới, chỉ ghi chatter | Dữ liệu vẫn bám rule của `approval.request` và survey rule | ACL chung của `approval.request` và `mail.activity` |
| B12 | Hệ thống, HR | Hệ thống kiểm tra các khoản thanh toán chưa hoàn tất, thông báo đến nhân viên | Chưa đủ dữ liệu xác nhận từ source | Chưa đủ dữ liệu xác nhận từ source | Chưa thấy custom riêng | Không thấy file/method riêng trong `0214` | Bước này có trong bảng nghiệp vụ nhưng source hiện tại không thấy model hay action chuyên biệt cho công nợ/thanh toán | Chưa thấy custom riêng | Không | Không | Chưa thấy mail riêng | Chưa thấy rule riêng | Chưa thấy ACL riêng |
| B13 | IT | IT xác nhận hoàn thành checklist bàn giao tài khoản nội bộ, email, thiết bị | `approved`, activity IT đang `pending` | Activity IT `done` | Đã có trong source | `rst_template_it_checklist` | IT checklist đã được mô hình hóa bằng activity template riêng | `mail.activity` | Không | Không | `email_template_dept_offboarding_reminder` khi quá hạn | Chưa thấy rule riêng theo IT | ACL chung `mail.activity` |
| B14 | Admin | Admin xác nhận checklist bàn giao tài sản văn phòng | `approved`, activity Admin đang `pending` | Activity Admin `done` | Đã có trong source | `rst_template_admin_checklist` | Admin checklist đã được mô hình hóa bằng activity template riêng | `mail.activity` | Không | Không | `email_template_dept_offboarding_reminder` khi quá hạn | Chưa thấy rule riêng theo Admin | ACL chung `mail.activity` |
| B15 | HR | HR xác nhận checklist bàn giao thẻ bảo hiểm và hồ sơ liên quan | `approved`, activity HR đang `pending` | Activity HR `done` | Đã có trong source | `rst_template_hr_checklist` | HR checklist đã được mô hình hóa bằng activity template riêng | `mail.activity` | Không | Không | `email_template_dept_offboarding_reminder` khi quá hạn | Chưa thấy rule riêng theo HR checklist | ACL chung `mail.activity` |
| B16 | Hệ thống, HR | Hệ thống kiểm tra checklist bàn giao: chưa xong thì chờ, xong thì sang bước 17 | `approved`, còn activity active hoặc survey chưa xong | `approved`, đủ điều kiện đi tiếp khi survey done và không còn activity active | Đã có trong source | `_compute_rst_all_activities_completed()`, `_compute_rst_exit_survey_completed()` | Đây là bước hệ thống kiểm tra điều kiện để chuẩn bị gửi BHXH và hoàn tất quy trình | `approval.request`, `mail.activity`, `survey.user_input` | Có | Không | Có thể có reminder nếu có task quá hạn | Survey rule của `0214` và rule request hiện hữu | ACL trên `approval.request`, `mail.activity`, `survey.user_input` |
| B17 | HR, Kế toán, Nhân viên | Ký quyết toán lương | Chưa đủ dữ liệu xác nhận từ source | Chưa đủ dữ liệu xác nhận từ source | Chưa thấy custom riêng | Không thấy method/model riêng trong `0214` | Bước nghiệp vụ có trong bảng nhưng source hiện tại chưa map ra custom riêng | Chưa thấy custom riêng | Không | Không | Không | Không | Không |
| B18 | HR Admin, HR Head, System | Gửi email hướng dẫn nhận BHXH | `approved`, survey đã hoàn tất, mọi activity đã hoàn tất, chưa gửi BHXH | `approved`, `x_psm_0214_social_insurance_email_sent = True` | Đã có trong source | `action_send_social_insurance()` | Đây là bước bắt buộc trước khi cho phép `action_done()` | `approval.request`, `hr.employee` | Không | Không | `email_template_social_insurance` | Rule request của `0214`; kiểm tra group bằng `_GROUP_0214_HR_PROCESS` | Nút chỉ hiện cho nhóm HR RST phù hợp |
| B19 | Kế toán, HR | Thanh toán theo kỳ lương | Chưa đủ dữ liệu xác nhận từ source | Chưa đủ dữ liệu xác nhận từ source | Có một phần | Ảnh gợi ý `hr.payslip`, nhưng source `0214` không custom riêng | Có thể đây là bước dùng chuẩn Odoo Payroll hoặc hệ thống ngoài phạm vi module `0214` | `hr.payslip` là suy luận hợp lý từ nghiệp vụ, chưa thấy custom trong source `0214` | Không | Không | Không | Không thấy rule riêng trong `0214` | ACL thuộc module payroll nếu có cài |
| B20 | Nhân viên, HR | Nhân viên nhận quyết định nghỉ việc, lương và giấy tờ liên quan | Sau khi đã gửi BHXH và xử lý quyết toán | Trước khi hoàn tất hẳn quy trình | Chưa thấy custom riêng | Không thấy action riêng trong `0214` | Bước này có tính nghiệp vụ vận hành, source hiện tại không thấy màn hay mail riêng | Chưa thấy custom riêng | Không | Không | Không | Không | Không |
| B21 | Hệ thống | Hệ thống thay đổi trạng thái tài khoản portal | `approved`, đủ 3 điều kiện: survey done, activities done, BHXH sent | `done`, user portal/internal phù hợp bị `active = False` | Đã có trong source | `action_done()` | Đây là bước được source xác nhận rõ nhất: hoàn tất quy trình và vô hiệu hóa user phù hợp | `approval.request`, `res.users`, `mail.activity` | Không | Không | Không tạo mail mới, chỉ `message_post()` | Không có rule riêng cho `res.users` trong module | Nút `action_done` chỉ hiện cho nhóm `_GROUP_0214_DONE` |
| B22 | Hệ thống | Gửi thông báo hoàn thành offboarding | `done` hoặc gần `done` | `done` | Có một phần | `ir_cron_psm_offboarding_reminder_rst`, `action_checklist_completed()` | Source hiện tại chưa thấy template mail đúng tên “finishing offboarding”; chỉ thấy reminder và message chatter | `approval.request`, `mail.activity` | Không | Không | `email_template_offboarding_reminder`, `email_template_dept_offboarding_reminder` chỉ là nhắc việc; chưa thấy template hoàn tất riêng | Rule hiện hữu của request và survey | ACL hiện hữu trên request/activity |

## Vì sao các giá trị mới nên được thêm như trên

### 1. Cột `Pre State`

Nên thêm vì bảng hiện tại mới mô tả nghiệp vụ theo câu chữ, nhưng chưa cho thấy điều kiện đầu vào của từng bước.

Các giá trị mình thêm vào cột này dựa trên:

- trạng thái chuẩn của `approval.request` trong `0214`: `new`, `pending`, `approved`, `done`
- trạng thái logic của checklist/activity:
  - activity đang active tức là việc còn mở
  - survey chưa `done` thì chưa thể coi là hoàn tất
- điều kiện chặn trong backend:
  - `action_approve()` yêu cầu phải có `x_psm_0214_resignation_date`
  - `action_done()` yêu cầu đủ survey + activities + BHXH

Vì vậy:

- B3 nên có `Pre State = chưa có đơn hoặc new`
- B6 nên có `Pre State = pending`
- B18 nên có `Pre State = approved + survey done + activities done + chưa gửi BHXH`
- B21 nên có `Pre State = approved + đủ 3 điều kiện hoàn tất`

Nếu không thêm cột này, bảng sẽ khó dùng khi test hoặc khi đối chiếu điều kiện nghiệp vụ với điều kiện chặn trong code.

### 2. Cột `Current State`

Nên thêm vì sau mỗi bước cần biết record chính đang chuyển sang trạng thái nào.

Các giá trị mình thêm vào cột này bám theo source:

- B3 chuyển sang `pending` do `action_confirm()`
- B6 chuyển sang `approved` sau approve
- B8 chưa chuyển request sang trạng thái mới nhưng làm `x_psm_0214_exit_survey_completed = True`
- B18 chưa chuyển request sang `done` nhưng làm `x_psm_0214_social_insurance_email_sent = True`
- B21 chuyển request sang `done` và vô hiệu hóa user phù hợp

Lý do nên thêm:

- cột này giúp phân biệt bước nào thật sự đổi `request_status`
- bước nào chỉ đổi cờ nghiệp vụ như:
  - `x_psm_0214_exit_survey_completed`
  - `x_psm_0214_all_activities_completed`
  - `x_psm_0214_social_insurance_email_sent`

### 3. Cột `Status`

Nên thêm vì ảnh hiện tại chưa phân biệt được:

- bước nào đã implement thật trong module
- bước nào chỉ có một phần
- bước nào mới là mô tả quy trình nghiệp vụ nhưng chưa có custom code riêng

Mình thêm 3 loại:

- `Đã có trong source`
- `Có một phần`
- `Chưa thấy custom riêng`

Lý do:

- tránh hiểu lầm rằng toàn bộ các bước trong Excel đã được hệ thống hóa đầy đủ
- đặc biệt các bước B4, B12, B17, B20 trong source `0214` chưa thấy action/model/mail custom rõ ràng

### 4. Cột `Link`

Nên thêm vì đây là cột giúp truy ngược từ bảng nghiệp vụ sang điểm chạm kỹ thuật.

Các giá trị mình thêm là:

- route portal
- method Python
- cron
- XML record/template
- file view/config liên quan

Ví dụ:

- B3 nên trỏ tới route `/my/resignation/rst/submit`
- B6 nên trỏ tới `action_approve()`
- B18 nên trỏ tới `action_send_social_insurance()`
- B22 nên trỏ tới `ir_cron_psm_offboarding_reminder_rst`

Nếu không có cột này, bảng sẽ khó dùng khi:

- test
- debug
- đối chiếu nghiệp vụ với code
- bàn giao cho người khác

### 5. Cột `Note`

Nên thêm vì nhiều bước không thể mô tả đủ chỉ bằng một dòng ở cột `Mô tả bước`.

Mình dùng cột `Note` để ghi các ý mà code xác nhận nhưng bảng gốc chưa thể hiện rõ, ví dụ:

- B6: approve xong thì tự gửi survey và launch plan
- B8: survey phải `done` mới được tính hoàn thành
- B11: dùng `message_post()` chứ không phải gửi mail mới
- B22: chưa thấy template “hoàn thành offboarding” riêng

Lý do nên thêm:

- giữ cột `Mô tả bước` ngắn gọn
- vẫn bảo tồn được thông tin kỹ thuật quan trọng

### 6. Các giá trị ở cột `Model`

Mình chỉ thêm model khi source có căn cứ hoặc khi là suy luận nghiệp vụ rất gần source.

Ví dụ:

- B1 dùng `mail.activity.plan`, `mail.activity.plan.template` là hợp lý vì checklist được định nghĩa trong `data/offboarding_plan_rst.xml`
- B3 dùng `approval.request`, `approval.approver`, `hr.employee`, `hr.departure.reason` vì portal submit thực sự tạo và dùng các model này
- B8 dùng `survey.user_input`, `survey.user_input.line`
- B19 ghi `hr.payslip` nhưng có chú thích là suy luận hợp lý từ nghiệp vụ, chưa thấy custom trong `0214`

Lý do:

- tránh gán bừa model chỉ vì “nghe có vẻ đúng”
- nhưng vẫn giúp bảng đủ dùng cho phân tích kỹ thuật

### 7. Các giá trị ở cột `Survey`

Nên thêm khi bước thực sự dùng survey hoặc phụ thuộc vào survey.

Vì source xác nhận rõ:

- B2 tạo seed survey `survey_exit_interview`
- B6 approve xong thì gửi survey
- B8 nhân viên làm survey
- B11, B16, B21 phụ thuộc kết quả survey ở mức điều kiện hoàn tất

Do đó các bước không dùng survey trực tiếp thì để `Không`, còn bước dùng rõ thì ghi:

- `survey_exit_interview`
- hoặc `Có`

### 8. Các giá trị ở cột `Approval`

Ảnh hiện chỉ điền vài dòng là `offboarding request`, nhưng thực tế cột này nên phản ánh:

- bước nào đang thao tác trên hồ sơ approval
- bước nào chỉ dùng workflow approval như điều kiện
- bước nào không dùng approval trực tiếp

Vì vậy mình thêm:

- `approval request` cho B3, B5, B6
- `Không` với các bước chỉ xử lý checklist, survey, reminder

Lý do:

- đúng với source hơn là điền lặp lại toàn cột
- giúp phân biệt approval với checklist activity

### 9. Các giá trị ở cột `Mail`

Đây là cột nên bổ sung mạnh nhất, vì source `0214` có 5 email template thật:

- `email_template_exit_survey`
- `email_template_adecco_notification`
- `email_template_social_insurance`
- `email_template_offboarding_reminder`
- `email_template_dept_offboarding_reminder`

Mình chỉ điền mail vào các bước thật sự liên quan:

- B6, B8: `email_template_exit_survey`
- B13, B14, B15, B16, B22: reminder bộ phận hoặc reminder nhân viên nếu quá hạn
- B18: `email_template_social_insurance`

Mình không điền mail cho các bước không thấy source gửi mail trực tiếp, để tránh sai.

### 10. Các giá trị ở cột `Rule`

Nên thêm vì `0214` có rule thật cho:

- `approval.request`
- `approval.approver`
- survey nội bộ
- survey portal own

Nhưng chưa thấy rule riêng cho:

- `mail.activity`
- `mail.activity.plan`
- `res.users`

Vì vậy mình bổ sung theo hai kiểu:

- ghi tên rule cụ thể nếu source có
- ghi `chưa thấy rule riêng` nếu source không có

Lý do:

- giúp nhận ra ngay chỗ nào đang siết quyền bằng record rule
- chỗ nào đang dựa chủ yếu vào ACL, UI hoặc backend guard

### 11. Các giá trị ở cột `ACL`

Nên thêm vì bảng hiện chưa thể hiện lớp quyền model access.

Các giá trị mình thêm bám `security/ir.model.access.csv`, ví dụ:

- `approval.request`: portal có create/read, nội bộ có full hơn
- `survey.user_input`: portal có create/write/read
- `mail.activity`: portal read, nội bộ full theo CSV hiện tại

Lý do:

- cột `Rule` và `ACL` không giống nhau
- nếu chỉ có `Rule` mà không có `ACL`, người đọc dễ hiểu sai lớp quyền đang thực sự kiểm soát ở đâu

## Kết luận ngắn

Những cột nên được bổ sung giá trị rõ ràng nhất là:

- `Pre State`
- `Current State`
- `Status`
- `Link`
- `Mail`
- `Rule`
- `ACL`

Lý do là vì đây là các cột đang giúp biến bảng từ “mô tả quy trình nghiệp vụ” thành “bảng đối chiếu nghiệp vụ - kỹ thuật - phân quyền - test”.

Nếu cần dùng để triển khai hoặc review, bảng sau khi bổ sung sẽ thực tế hơn nhiều so với bảng ảnh gốc.
