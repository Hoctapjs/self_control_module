# Yêu Cầu Khi Test Module 0213

Khi test bất kỳ chức năng nào của `M02_P0213_00`, luôn soi đủ 5 góc dưới đây.

Module `0213` là luồng `offboarding` gắn với:

- portal gửi đơn nghỉ việc
- approval duyệt đơn nghỉ việc
- activity plan offboarding
- survey exit interview
- mail reminder, mail thông báo
- hoàn tất offboarding và khóa tài khoản user

## 1. Functional

Kiểm tra chức năng có đúng nghiệp vụ hay không.

Cần soi tối thiểu:

- nhân viên portal có vào đúng form nghỉ việc tại `/my/resignation/ops`
- submit đơn có tạo đúng `approval.request` thuộc category nghỉ việc
- approver đúng là line manager khi submit từ portal
- trạng thái đơn có chạy đúng các bước: draft, confirm, approved/refused, done
- sau khi duyệt có gửi exit survey và launch activity plan đúng hay không
- nút `Withdraw`, `Cancel`, `Done`, `Send Exit Survey`, `Send Social Insurance`, `Manual Reminder` có chạy đúng rule
- chỉ đơn nghỉ việc mới áp dụng logic chặn withdraw/cancel sau khi đã có kết quả cuối
- khi bấm hoàn tất quy trình, hệ thống có chặn nếu chưa xong survey hoặc chưa xong activity
- rehire và blacklist có ghi nhận đúng cờ nghiệp vụ

## 2. Data

Kiểm tra dữ liệu vào và dữ liệu ra có đúng không.

Cần soi tối thiểu:

- `x_psm_0213_employee_id` có map đúng từ `partner_id` hoặc `request_owner_id`
- loại nghỉ việc, lý do nghỉ, ngày nghỉ dự kiến lưu đúng lên đơn
- line manager, phòng ban, chức vụ hiển thị đúng theo employee liên quan
- `x_psm_0213_exit_survey_user_input_id` có tạo đúng và không bị nhân bản sai
- activity tạo từ plan có đúng người phụ trách, đúng deadline, đúng model đích
- mail reminder có gia hạn đúng 4 ngày cho activity quá hạn
- khi hoàn tất quy trình, `request_status` sang `done` và user liên quan bị `active = False` đúng đối tượng
- chatter, notification, email template có nhận đúng record và đúng người nhận

## 3. Workflow

Kiểm tra state, approval, activity, mail và các bước chuyển tiếp.

Cần soi tối thiểu:

- portal submit xong thì đơn có vào đúng luồng approval
- manager approve thì survey có được gửi và plan có được launch
- danh sách activity trên request và trên employee có phản ánh đúng tiến độ
- portal user chỉ được đánh dấu done activity mà chính họ phụ trách
- cron reminder chỉ chạy cho đơn `approved` và chỉ nhắc các activity overdue
- manual reminder có cùng logic với cron cho đúng đơn đang mở
- sau khi hoàn tất hết activity và survey, action done mới cho phép chạy
- mail/social insurance/reminder có bám đúng thời điểm nghiệp vụ

## 4. Security

Kiểm tra quyền, phạm vi thấy, sửa, xóa có đúng không.

Cần soi tối thiểu:

- portal user chỉ thấy đơn nghỉ việc của chính mình
- portal user chỉ thấy survey response của chính mình theo record rule
- portal user không nhìn thấy hoặc thao tác đơn của người khác qua URL hoặc ID thủ công
- chỉ approver/internal user phù hợp mới thấy và bấm được các action nội bộ
- portal chỉ được mark done activity khi `activity.user_id` đúng user đang đăng nhập
- không mở quá quyền trên `mail.activity`, `survey.user_input`, `approval.request`, `hr.employee`
- kiểm tra lại các case sudo trong controller/model để chắc không lộ dữ liệu ngoài phạm vi

## 5. Reporting / Auditability

Kiểm tra khả năng truy xuất, log, report và lịch sử thay đổi.

Cần soi tối thiểu:

- chatter có ghi nhận lúc duyệt, gửi mail, hoàn tất, blacklist, rehire
- activity history còn truy vết được cả activity done và activity inactive
- survey result có mở lại xem được sau khi user hoàn tất
- có phân biệt được activity nào của request và activity nào của employee
- khi reminder chạy, có dấu vết để kiểm tra ai được nhắc và deadline đã đổi thế nào
- khi khóa tài khoản user, có message hoặc log đủ để audit
- tester có thể truy lại một case từ portal submit đến done mà không mất dấu trạng thái trung gian

## Checklist Ghi Nhận Nhanh

Khi test xong một chức năng, nên chốt nhanh 5 dòng:

- Functional: pass/fail và lệch nghiệp vụ nếu có
- Data: field nào đúng, field nào sai
- Workflow: state/activity/mail nào chạy hoặc không chạy
- Security: user nào thấy được gì, sửa được gì, bị chặn ở đâu
- Reporting/Auditability: log, chatter, history, report truy được đến mức nào
