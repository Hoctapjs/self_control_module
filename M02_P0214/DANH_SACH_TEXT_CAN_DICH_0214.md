# DANH SÁCH TEXT / LABEL / EMAIL TEMPLATE CẦN CHUYỂN NGỮ — Module M02_P0214

> **Mục đích:** Liệt kê đầy đủ các chuỗi text/label tiếng Việt trong module 0214 + đề xuất bản dịch.
> **Quy ước:**
> - **Phần A → D (UI/Backend):** Vietnamese → **English**
> - **Phần E (Email templates):** Giữ **Vietnamese**, chỉ chuẩn hoá lại các template hiện đang transliterate (bỏ dấu) thành Vietnamese có dấu đầy đủ.
> - **Phần F (Bỏ qua):** demo data, comments Python/XML, docstrings — không động vào theo thoả thuận.
>
> **Hành động kế tiếp:** Review danh sách → confirm phạm vi → tôi apply Edit theo từng file.

---

## TỔNG QUAN SỐ LƯỢNG

| Nhóm | File | Số chuỗi |
|------|------|---------:|
| A. Views XML (backend forms, lists, search, menus) | 10 | ~80 |
| B. Portal templates (resignation + offboarding activities) | 2 | ~60 |
| C. Python models (field string/help, UserError, _()) | 13 .py | ~120 |
| D. Wizard + controllers | 3 | ~10 |
| E. Data XML (offboarding plans, survey questions) | 3 | ~152 |
| F. Email templates (giữ Vietnamese, chuẩn hoá dấu) | 11 | ~11 subject + body |
| **TỔNG** | **42 file** | **~430 mục** |

---

## A. VIEWS XML — BACKEND (→ English)

### A.1. `views/resignation_request_views.xml`

| Line | Original (Vietnamese) | Đề xuất (English) |
|-----:|----------------------|-------------------|
| 20 | `string="Chot &amp; chuyen Ke toan"` | `string="Lock &amp; Push to Accounting"` |
| 25 | `string="Override Ke toan"` | `string="Override Accounting"` |

> Các string khác trong file này đã là English (`Send Social Insurance Information`, `Complete Resignation`, `My Activities`, `Resignation Information`, `Employee Information`, `Request Details`, `Signed Resignation`, `Salary Settlement`, `Finance Check`, `Offboarding Process`, `Status`, `View Results`, `Resignation Type`). ✅

### A.2. `views/offboarding_report_views.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 17 | `string="Tên đơn"` | `string="Request Name"` |
| 18 | `string="Nhân viên"` | `string="Employee"` |
| 19 | `string="Ngày nghỉ dự kiến"` | `string="Expected Resignation Date"` |
| 20 | `string="Khảo sát"` | `string="Survey"` |
| 21 | `string="Công việc"` | `string="Activities"` |
| 22 | `string="Trạng thái"` | `string="Status"` |
| 43 | `string="Group by Lý do nghỉ việc"` | `string="Group by Resignation Reason"` |
| 44 | `string="Group by Trạng thái"` | `string="Group by Status"` |

### A.3. `views/finance_check_report_views.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 11 | `<list string="Bao cao kiem tra Ke toan" ...>` | `<list string="Accounting Check Report" ...>` |
| 13 | `string="Ten don"` | `string="Request Name"` |
| 14 | `string="Nhan vien"` | `string="Employee"` |
| 15 | `string="Ngay nghi"` | `string="Resignation Date"` |
| 16 | `string="Trang thai"` | `string="Status"` |
| 20 | `string="Ngay kiem tra"` | `string="Check Date"` |
| 21 | `string="Nguoi override"` | `string="Override By"` |
| 22 | `string="Ly do override"` | `string="Override Reason"` |
| 43 | `string="Group by Trang thai"` | `string="Group by Status"` |
| 45 | `string="Group by Nhan vien"` | `string="Group by Employee"` |
| 52 | `<field name="name">Bao cao kiem tra Ke toan</field>` | `<field name="name">Accounting Check Report</field>` |
| 62 | `name="Bao cao kiem tra Ke toan"` (menuitem) | `name="Accounting Check Report"` |

### A.4. `views/exit_interview_dashboard_views.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 61 | `string="Group by Phong ban"` | `string="Group by Department"` |
| 63 | `string="Group by Chuc danh"` | `string="Group by Job Position"` |
| 65 | `string="Group by Ly do"` | `string="Group by Reason"` |
| 67 | `string="Group by Thang nghi"` | `string="Group by Resignation Month"` |
| 69 | `string="Group by Hoan thanh"` | `string="Group by Completed"` |

### A.5. `views/res_company_views.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 21 | `<group string="Tham so nhac viec" col="2">` | `<group string="Reminder Parameters" col="2">` |
| 34 | `<group string="Template email" col="2">` | `<group string="Email Templates" col="2">` |
| 51 | `<group string="User mac dinh theo vai tro" col="4">` | `<group string="Default Users by Role" col="4">` |
| 65 | `<group string="Cau hinh phep nam (AL)">` | `<group string="Annual Leave (AL) Configuration">` |

### A.6. `views/resignation_request_views.xml` — page strings

> Đã English sẵn (lines 56, 60, 71, 85, 96, 108, 128, 150). Không cần đổi.

### A.7. Các view khác (`config_menu_views.xml`, `hr_employee_views.xml`, `res_config_settings_views.xml`)

Đã là English hoàn toàn. ✅

---

## B. PORTAL TEMPLATES (→ English)

> **⚠️ Lưu ý nghiệp vụ:** Portal templates là trang dành cho **nhân viên Việt Nam** (người dùng cuối tự nộp đơn nghỉ việc). Dịch toàn bộ sang English có thể ảnh hưởng UX. **Đề nghị xác nhận lại trước khi apply** — tôi đã liệt kê bản dịch nhưng bạn có thể chọn:
> - **Option 1:** Dịch hết (theo quy ước "views → English")
> - **Option 2:** Giữ tiếng Việt cho portal templates vì user-facing
> - **Option 3:** Dùng `t-call="web.translation"` để bilingual

### B.1. `views/resignation_portal_template.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 3 | `name="Form yêu cầu nghỉ việc"` | `name="Resignation Request Form"` |
| 10 | `<strong>Đã gửi yêu cầu:</strong> Đơn của bạn đang chờ quản lý <strong>...</strong> phê duyệt.` | `<strong>Request submitted:</strong> Your request is awaiting approval from your manager <strong>...</strong>.` |
| 13 | `<strong>Đã phê duyệt:</strong> Đơn nghỉ việc đã được chấp thuận. Vui lòng hoàn thành các đầu việc bên dưới.` | `<strong>Approved:</strong> Your resignation has been approved. Please complete the tasks below.` |
| 16 | `<strong>Hoàn tất:</strong> Quy trình nghỉ việc của bạn đã hoàn thành. Chúc bạn thành công trên chặng đường mới!` | `<strong>Completed:</strong> Your resignation process is complete. Wishing you success on your new journey!` |
| 23 | `Danh sách công việc của bạn` | `Your Task List` |
| 30 | `Khảo sát Nghỉ việc (Exit Interview)` | `Exit Interview Survey` |
| 31 | `Vui lòng hoàn thành khảo sát này trước ngày nghỉ chính thức.` | `Please complete this survey before your official resignation date.` |
| 34 | `Làm khảo sát` | `Take Survey` |
| 62 | `Hạn:` | `Due:` |
| 74 | `Xác nhận thực hiện` | `Confirm Done` |
| 97 | `Phụ trách:` | `Assignee:` |
| 109 | `Quyết toán lương` | `Salary Settlement` |
| 115 | `File quyết toán lương` | `Salary Settlement File` |
| 116 | `Tải file, ký xác nhận và upload lại bản đã ký.` | `Download the file, sign, and upload the signed version.` |
| 120 | `Tải file` | `Download` |
| 126 | `<strong>Đã nộp:</strong> Hệ thống đã nhận bản quyết toán lương đã ký.` | `<strong>Submitted:</strong> The signed salary settlement has been received.` |
| 134 | `Bản đã ký` | `Signed Copy` |
| 142 | `Upload bản ký` | `Upload Signed Copy` |
| 153 | `Quay lại Portal` | `Back to Portal` |
| 161 | `<strong>Lỗi:</strong> Không tìm thấy thông tin nhân viên liên kết với tài khoản này. Vui lòng liên hệ bộ phận IT hoặc HR.` | `<strong>Error:</strong> No employee record linked to this account. Please contact IT or HR.` |
| 170 | `Đơn Xin Nghỉ Việc - Khối Văn Phòng` | `Resignation Request - Office Staff` |
| 173 | `aria-label="Các bước gửi đơn nghỉ việc"` | `aria-label="Resignation submission steps"` |
| 177 | `Thông tin` | `Information` |
| 180 | `Nghỉ việc` | `Resignation` |
| 184 | `Xác nhận` | `Confirm` |
| 193 | `Thông tin nhân viên` | `Employee Information` |
| 199 | `Họ tên nhân viên` | `Employee Full Name` |
| 205 | `Ngày sinh` | `Date of Birth` |
| 214 | `Quốc tịch` | `Nationality` |
| 220 | `CCCD` | `National ID` |
| 229 | `Phòng ban` | `Department` |
| 235 | `Chức vụ` | `Job Position` |
| 244 | `Line Manager` | (giữ nguyên) |
| 247 | `'Chưa có Line Manager'` | `'No Line Manager assigned'` |
| 252 | `Email công việc` | `Work Email` |
| 261 | `Email cá nhân` | `Personal Email` |
| 271 | `(comment) Nay tôi làm đơn này, kính xin quý công ty cho tôi được nghỉ việc.` | (đang trong HTML comment, giữ hoặc xoá) |
| 279 | `Thông tin nghỉ việc` | `Resignation Information` |
| 285 | `Ngày nghỉ dự kiến` | `Expected Resignation Date` |
| 292 | `Loại nghỉ việc` | `Resignation Type` |
| 294 | `-- Chọn loại nghỉ việc --` | `-- Select Resignation Type --` |
| 305 | `Mô tả lý do nghỉ việc` | `Resignation Reason Description` |
| 309 | `placeholder="Vui lòng nhập mô tả chi tiết cho lý do nghỉ việc đã chọn"` | `placeholder="Please provide a detailed description for the selected resignation reason"` |
| 319 | `Xác nhận và cam kết` | `Confirmation and Commitment` |
| 326 | `Bước xác nhận cuối` | `Final Confirmation Step` |
| 327 | `Vui lòng đọc kỹ các điều khoản trước khi gửi yêu cầu nghỉ việc` | `Please read carefully before submitting your resignation request` |
| 331 | `Nội dung dưới đây giữ nguyên ý nghĩa cam kết hiện tại, chỉ được trình bày lại rõ ràng hơn để bạn dễ đọc và xác nhận.` | `The terms below preserve the original commitment in clearer wording for easier review.` |
| 336 | (Commitment 1, dài) `Tuân thủ quy trình nghỉ việc của công ty và các trách nhiệm, chế độ thanh toán khi chấm dứt hợp đồng lao động, bao gồm nhưng không giới hạn quy định hoàn trả đồng phục, tài sản, quyết toán lương, nhận sổ/tờ rời BHXH & Quyết định nghỉ việc.` | `Comply with the company's resignation procedure and all responsibilities and settlement obligations upon contract termination, including but not limited to the return of uniforms, assets, salary settlement, and receipt of the social-insurance book/slip and Resignation Decision.` |
| 340 | (Commitment 2) `Nếu chấm dứt làm việc trước thời hạn cho phép, công ty có quyền khấu trừ vào bất kỳ khoản thanh toán nào của tôi một khoản tương ứng với số ngày nghỉ trước hạn.` | `If I terminate employment before the allowed notice period, the company may deduct from any payment due to me an amount corresponding to the early-leave days.` |
| 344 | (Commitment 3) `Cho phép Công ty lưu trữ Dữ liệu cá nhân sau khi các bên kết thúc mối quan hệ lao động, hoặc sau khi các bên chấm dứt hợp đồng là năm (5) năm, tùy trường hợp pháp luật yêu cầu một thời gian dài hơn.` | `Allow the Company to retain Personal Data for five (5) years after the employment relationship ends or after contract termination, or longer if required by law.` |
| 348 | (Commitment 4) `Cam kết bảo mật thông tin theo Thỏa thuận Bảo mật thông tin đã ký tại thời điểm ký kết hợp đồng lao động với công ty, cũng như các thông tin mật hoặc thông tin cần bảo mật mà cá nhân có được trong quá trình làm việc tại công ty.` | `Commit to information confidentiality per the NDA signed at contract execution, including any confidential information obtained during employment.` |
| 357 | `<strong>Lưu ý:</strong> Sau khi gửi yêu cầu, Line Manager của bạn sẽ nhận được thông báo và xem xét yêu cầu nghỉ việc. Bạn sẽ được thông báo kết quả qua email.` | `<strong>Note:</strong> After submission, your Line Manager will be notified and will review the request. You will be informed of the result by email.` |
| 365 | `Gửi yêu cầu nghỉ việc` | `Submit Resignation Request` |
| 368 | `Quay lại` | `Back` |
| 374 | `aria-label="Lên đầu trang"` | `aria-label="Scroll to top"` |

### B.2. `views/offboarding_activities_portal_template.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 3 | `name="Hoạt động cần làm Offboarding RST"` | `name="Offboarding Activities — RST"` |
| 9 | `<strong>Đã ghi nhận:</strong> Hoạt động đã được xác nhận hoàn tất.` | `<strong>Recorded:</strong> Activity marked as completed.` |
| 14 | `Hoạt động cần làm` | `Pending Activities` |
| 38 | `Hạn:` | `Due:` |
| 41 | `Đã nhắc:` | `Reminders sent:` |
| 53 | `Xác nhận thực hiện` | `Confirm Done` |
| 57 | `Đã hoàn tất` | `Completed` |
| 67 | `Hiện không có hoạt động offboarding nào được giao cho bạn.` | `You have no offboarding activities assigned at the moment.` |

---

## C. PYTHON MODELS (→ English)

### C.1. `models/approval_request_rst_fields.py`

| Line | Field / Context | Original | Đề xuất |
|-----:|-----------------|----------|---------|
| 587 | `employee_id` string | `Nhan vien yeu cau nghi viec` | `Resigning Employee (Request Owner)` |
| 663 | `x_psm_0214_employee_personal_email` string | `Email ca nhan nhan vien` | `Employee Personal Email` |
| 664 | `x_psm_0214_employee_personal_email` help | `Email ca nhan cua nhan vien nghi viec, dung cho cac email sau khi roi cong ty.` | `Personal email of the resigning employee, used for post-departure communications.` |
| 667 | `x_psm_0214_remaining_al_days` string | `So ngay phep nam con lai` | `Remaining Annual Leave Days` |
| 670 | `x_psm_0214_remaining_al_days` help | `Snapshot so ngay phep nam con lai tai thoi diem don nghi viec duoc duyet.` | `Snapshot of remaining annual leave days at the time the resignation request was approved.` |
| 673 | `x_psm_0214_manager_approval_reminder_count` string | `So lan nhac quan ly duyet` | `Manager Approval Reminders Sent` |
| 679 | `x_psm_0214_manager_approval_reminder_sent_at` string | `Lan gan nhat gui email nhac quan ly` | `Last Manager Reminder Email Sent At` |
| 684 | `x_psm_0214_signed_resignation_file` string | `Phieu nghi viec da ky (PDF)` | `Signed Resignation Letter (PDF)` |
| 689 | `x_psm_0214_signed_resignation_filename` string | `Ten file phieu nghi viec da ky` | `Signed Resignation Filename` |
| 693 | `x_psm_0214_signed_resignation_hash` string | `Ma kiem tra (SHA-256)` | `Checksum (SHA-256)` |
| 698 | `x_psm_0214_signed_locked` string | `Da khoa phieu ky` | `Signed Letter Locked` |
| 704 | `x_psm_0214_can_view_signed_resignation` string | `Co quyen xem phieu ky` | `Can View Signed Letter` |
| 709 | `x_psm_0214_salary_settlement_file` string | `File quyet toan luong (PDF)` | `Salary Settlement File (PDF)` |
| 714 | `x_psm_0214_salary_settlement_filename` string | `Ten file quyet toan luong` | `Salary Settlement Filename` |
| 718 | `x_psm_0214_signed_settlement_file` string | `Ban quyet toan da ky` | `Signed Settlement Copy` |
| 723 | `x_psm_0214_signed_settlement_filename` string | `Ten file quyet toan da ky` | `Signed Settlement Filename` |
| 727 | `x_psm_0214_settlement_sent` string | `Da gui quyet toan luong` | `Salary Settlement Sent` |
| 733 | `x_psm_0214_settlement_sent_date` string | `Ngay gui quyet toan luong` | `Salary Settlement Sent Date` |
| 738 | `x_psm_0214_settlement_reminder_sent_at` string | `Lan gan nhat nhac nop ban ky quyet toan` | `Last Settlement Reminder Sent At` |
| 743 | `x_psm_0214_settlement_signed` string | `Da nop ban ky quyet toan` | `Signed Settlement Submitted` |
| 747 | `x_psm_0214_can_view_salary_settlement` string | `Co quyen xem quyet toan luong` | `Can View Salary Settlement` |
| 758 | `x_psm_0214_finance_check_state` string | `Trang thai kiem tra Ke toan` | `Accounting Check Status` |
| 764 | `x_psm_0214_finance_pending_items_summary` string | `Phieu ton dong` | `Pending Items Summary` |
| 769 | `x_psm_0214_finance_override_reason` string | `Ly do override Ke toan` | `Accounting Override Reason` |
| 775 | `x_psm_0214_finance_override_user_id` string | `Nguoi override Ke toan` | `Accounting Override By` |
| 780 | `x_psm_0214_finance_checked_date` string | `Ngay kiem tra Ke toan` | `Accounting Check Date` |
| 844 | `x_psm_0214_official_resignation_date` string | `Ngày nghỉ việc chính thức` | `Official Resignation Date` |
| 901, 906 | `owner_related_activity_ids` string | `Hoat dong lien quan (Res Name)` | `Related Activities (Res Name)` |
| 912, 919 | `rst_checklist_activity_ids` string | `Qua trinh nghi viec (RST)` | `Resignation Checklist (RST)` |
| 255, 267 | `AccessError` | `Báº¡n khÃ´ng cÃ³ quyá»n thá»±c hiá»‡n thao tÃ¡c: %s.` (bị lỗi encoding) | `You do not have permission to perform: %s.` |
| 952-957 | `UserError` | `Ngày nghỉ việc chính thức (%(date)s) không được sớm hơn ngày bắt đầu hợp đồng của nhân viên %(name)s.` | `Official resignation date (%(date)s) cannot be earlier than the contract start date of employee %(name)s.` |
| 1041 | `UserError` | `Phieu nghi viec da duoc ky va khoa. Muon thay doi, vui long huy don va tao don moi.` | `The resignation letter has been signed and locked. To make changes, please cancel and create a new request.` |

### C.2. `models/approval_request_rst_approval.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 36 | string (encoded) | `HoÃ n táº¥t nghá»‰ viá»‡c` | `Complete Resignation` |
| 55 | UserError | `Vui lòng hoàn thành khảo sát Nghỉ việc trước khi Hoàn tất quy trình.` | `Please complete the Exit Survey before finalising the process.` |
| 59 | UserError | `Vui lòng hoàn thành tất cả công việc Offboarding trước khi Hoàn tất quy trình.` | `Please complete all offboarding activities before finalising the process.` |
| 63 | UserError | `Vui lòng gửi Email hướng dẫn BHXH trước khi Hoàn tất quy trình.` | `Please send the Social-Insurance instruction email before finalising the process.` |
| 109 | message_post | `Hệ thống: Đã vô hiệu hóa tài khoản Portal/User: ` | `System: Deactivated Portal/User account: ` |
| 150 | feedback | `Đã hoàn thành thủ tục nghỉ việc.` | `Resignation procedure completed.` |
| 161 | UserError | `Vui lòng xác nhận 'Ngày nghỉ dự kiến' trước khi phê duyệt.` | `Please confirm the 'Expected Resignation Date' before approving.` |
| 170 | UserError | `Vui lòng đính kèm Phiếu nghỉ việc đã ký (PDF có chữ ký 2 bên) trước khi duyệt.` | `Please attach the signed Resignation Letter (PDF signed by both parties) before approving.` |

### C.3. `models/approval_request_rst_offboarding.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 175 | message_post | `Canh bao: Chua cau hinh PIC cho cong viec %s.` | `Warning: No PIC configured for activity %s.` |
| 245 | message_post | `Toàn bộ checklist offboarding đã hoàn thành.` | `The entire offboarding checklist has been completed.` |
| 258 | message_post | `Email BHXH đã được gửi.` | `Social-Insurance email has been sent.` |
| 260 | message_post | `HR có thể gửi hướng dẫn BHXH từ nút trên form.` | `HR can send the Social-Insurance instructions from the button on the form.` |
| 268 | message_post | `(Chờ hoàn thành: %s)` | `(Waiting on: %s)` |
| 267 | string literal | `Công việc Offboarding` | `Offboarding Activities` |
| 273 | _() call | `Xem hoạt động của tôi` | `View My Activities` |
| 288 | _() call | `Xem báo cáo offboarding RST` | `View RST Offboarding Report` |
| 293 | UserError | `Không tìm thấy category Quy trình nghỉ việc RST.` | `RST Resignation category not found.` |
| 308 | notification title | `Thông báo` | `Notice` |
| 309 | notification body | `Không có nhân sự RST nào đang pending offboarding.` | `No RST employees currently pending offboarding.` |
| 314 | action name | `Offboarding Report - RST` | (giữ nguyên — đã English) |

### C.4. `models/approval_request_rst_survey.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 17 | _() | `Gửi thông tin Adecco` | `Send Adecco Notification` |
| 32 | message_post | `Đã gửi thông tin Adecco đến email cấu hình.` | `Adecco notification sent to the configured email.` |
| 35, 101, 190 | notification title | `Thành công` | `Success` |
| 36 | notification body | `Đã gửi thông tin Adecco.` | `Adecco notification sent.` |
| 41, 89, 107, 159, 171 | notification title | `Lỗi` | `Error` |
| 42 | notification body | `Chưa cấu hình đủ email Adecco hoặc Email Template Adecco.` | `Adecco email or Adecco email template is not fully configured.` |
| 48 | _() | `Gửi thông tin bảo hiểm xã hội` | `Send Social-Insurance Information` |
| 58, 131 | notification title | `Thông báo` | `Notice` |
| 59 | notification body | `Email BHXH đã được gửi trước đó.` | `Social-Insurance email has already been sent.` |
| 65 | UserError | `Vui lòng hoàn thành khảo sát Nghỉ việc trước khi gửi thông tin BHXH.` | `Please complete the Exit Survey before sending Social-Insurance information.` |
| 70 | UserError | `Vui lòng hoàn thành tất cả công việc Offboarding trước khi gửi thông tin BHXH.` | `Please complete all offboarding activities before sending Social-Insurance information.` |
| 90 | notification body | `Không tìm thấy email để gửi thông tin BHXH.` | `No email found to send Social-Insurance information.` |
| 102 | notification body | `Đã gửi thông tin BHXH qua email.` | `Social-Insurance information sent by email.` |
| 108 | notification body | `Không tìm thấy Email Template BHXH.` | `Social-Insurance email template not found.` |
| 121 | _() | `Xem kết quả khảo sát` | `View Survey Results` |
| 132 | notification body | `Không tìm thấy kết quả khảo sát đã hoàn thành.` | `No completed survey results found.` |
| 137 | action name | `Kết quả khảo sát nghỉ việc` | `Exit Survey Results` |
| 160 | notification body | `Không tìm thấy email của người yêu cầu!` | `Requester's email not found!` |
| 172 | notification body | `Không thể tạo hoặc lấy link khảo sát nghỉ việc.` | `Unable to create or retrieve the exit-survey link.` |
| 191 | notification body | `Đã gửi email khảo sát đến {partner.email}` | `Survey email sent to {partner.email}` |

### C.5. `models/approval_request_rst_reminder.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 217 | _() | `Nhắc nhở và gia hạn thủ công` | `Send Manual Reminders & Extend Deadlines` |
| 222 | UserError | `Chi co the nhac nho cac don dang o trang thai Approved.` | `Reminders can only be sent for requests in the Approved status.` |
| 241 | notification title | `Thong bao` | `Notice` |
| 242 | notification body | `Khong co cong viec nao bi tre han de xu ly.` | `No overdue activities to process.` |
| 255 | notification title | `Thanh cong` | `Success` |
| 256-257 | notification body | `Da gui nhac nho va gia han cho %s cong viec tre han.` | `Sent reminders and extended deadlines for %s overdue activities.` |

### C.6. `models/approval_request_rst_finance.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 56 | _() | `Tam ung: %(name)s - %(amount)s - %(state)s` | `Advance: %(name)s - %(amount)s - %(state)s` |
| 73 | notification title | `Thong bao` | `Notice` |
| 74 | notification body | `Tac vu nay chi ap dung cho don nghi viec RST.` | `This action only applies to RST resignation requests.` |
| 91 | notification title | `Khong the chot sang Ke toan` | `Cannot push to Accounting` |
| 92 | notification body | `Con phieu ton dong:\n%s` | `Pending items remain:\n%s` |
| 105 | notification title | `Thanh cong` | `Success` |
| 106 | notification body | `Da kiem tra: khong con phieu ton dong. Co the chuyen Ke toan.` | `Check complete: no pending items. Ready to push to Accounting.` |
| 117 | UserError | `Chi co the override don dang bi chan Ke toan.` | `Only requests blocked by Accounting can be overridden.` |
| 120 | action name | `Override kiem tra Ke toan` | `Override Accounting Check` |

### C.7. `models/x_psm_0214_advance_request.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 7 | _description | `Phieu tam ung RST` | `RST Advance Request` |
| 10 | string | `So phieu` | `Reference No.` |
| 13 | string | `Nhan vien` | `Employee` |
| 17 | string | `So tien` | `Amount` |
| 20 | string | `Tien te` | `Currency` |
| 24 | string | `Ngay tam ung` | `Advance Date` |
| 31 | string | `Trang thai` | `Status` |

### C.8. `models/x_psm_resignation_type.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 8 | _description | `Loai nghi viec` | `Resignation Type` |
| 11 | string | `Ten loai nghi viec` | `Resignation Type Name` |

### C.9. `models/exit_interview_report.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 7 | _description | `Bao cao khao sat Exit Interview` | `Exit Interview Report` |
| 11 | string | `Don nghi viec` | `Resignation Request` |
| 12 | string | `Nhan vien` | `Employee` |
| 13 | string | `Phong ban` | `Department` |
| 14 | string | `Chuc danh` | `Job Position` |
| 17 | string | `Ly do nghi viec` | `Resignation Reason` |
| 20 | string | `Ngay nghi viec` | `Resignation Date` |
| 23 | string | `Diem hai long (%)` | `Satisfaction Score (%)` |
| 27 | string | `Da hoan thanh` | `Completed` |
| 32 | string | `So luot khao sat` | `Number of Surveys` |

### C.10. `models/res_company.py`

| Line | Field help | Original | Đề xuất |
|-----:|------------|----------|---------|
| 11 | `x_psm_0214_reminder_interval_days` | `Khoang cach giua hai lan nhac viec trong flow 0214.` | `Interval (in days) between two reminder emails within the 0214 flow.` |
| 16 | `x_psm_0214_reminder_max_count` | `So lan nhac toi da cho mot activity trong flow 0214.` | `Maximum number of reminders per activity in the 0214 flow.` |
| 21 | `x_psm_0214_activity_deadline_days` | `Deadline mac dinh cua activity phong ban, tinh tu ngay tao.` | `Default deadline for department activities, counted from creation date.` |
| 26 | `x_psm_0214_reminder_overdue_days` | `So ngay qua han toi thieu truoc khi gui nhac viec offboarding 0214.` | `Minimum days overdue before sending an offboarding 0214 reminder.` |
| 31 | `x_psm_0214_reminder_extension_days` | `So ngay gia han deadline sau khi gui nhac viec offboarding 0214.` | `Number of days to extend the deadline after sending a 0214 offboarding reminder.` |
| 36 | `x_psm_0214_portal_block_codes` | `Danh sach ma khoi cho phep nhan vien tao don RST tren portal, cach nhau bang dau phay.` | `Comma-separated list of block codes allowed to create RST requests from the portal.` |
| 41 | `x_psm_0214_portal_block_names` | `Danh sach ten khoi cho phep nhan vien tao don RST tren portal, cach nhau bang dau phay.` | `Comma-separated list of block names allowed to create RST requests from the portal.` |
| 83 | `x_psm_0214_manager_approval_reminder_template_id` | `Template email nhac quan ly duyet don nghi viec trong flow 0214.` | `Email template to remind the manager to approve a resignation in the 0214 flow.` |
| 89 | `x_psm_0214_employee_approved_template_id` | `Template email thong bao cho nhan vien khi don nghi viec da duoc duyet.` | `Email template to notify the employee when their resignation has been approved.` |
| 95 | `x_psm_0214_dept_assignment_template_id` | `Template email giao viec cho IT/Admin/HR trong flow 0214.` | `Email template to assign offboarding tasks to IT/Admin/HR in the 0214 flow.` |
| 101 | `x_psm_0214_salary_settlement_template_id` | `Template email gui quyet toan luong cho nhan vien nghi viec.` | `Email template to send the salary settlement to the resigning employee.` |
| 129 | `x_psm_0214_default_finance_user_id` | `User Finance mac dinh cho cac buoc kiem tra/quyet toan trong flow 0214.` | `Default Finance user for the check/settlement steps in the 0214 flow.` |
| 134 | `x_psm_0214_al_leave_type_ids` | `Cac loai phep dung de tinh so ngay phep nam con lai. Neu de trong, he thong lay tat ca loai phep can allocation.` | `Leave types used to compute remaining annual leave. If left empty, all leave types requiring allocation are used.` |

### C.11. `models/res_config_settings.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 121 | field string | `Loai phep tinh vao AL` | `Leave Types Counted as AL` |

### C.12. `models/mail_activity.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 15 | selection string | `Trang thai RST` | `RST Status` |
| 25 | related string | `Trang thai RST` | `RST Status` |
| 29 | string | `So lan da nhac` | `Reminder Count` |
| 161 | message_post | `He thong: Tat ca cac cong viec trong checklist da duoc hoan thanh.` | `System: All checklist activities have been completed.` |

### C.13. `models/survey_user_input.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 30 | activity_summary | `Hoàn thành Exit Interview` | `Complete Exit Interview` |

---

## D. WIZARD + CONTROLLERS

### D.1. `wizards/finance_override_wizard.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 8 | _description | `Override kiem tra Ke toan RST` | `RST Accounting Override Wizard` |
| 12 | string | `Don nghi viec` | `Resignation Request` |
| 16 | string | `Ly do override` | `Override Reason` |
| 22 | _() | `Override kiem tra Ke toan` | `Override Accounting Check` |
| 26 | UserError | `Chi co the override don dang bi chan Ke toan.` | `Only requests blocked by Accounting can be overridden.` |
| 37 | message_post | `Da override kiem tra Ke toan. Ly do: %s` | `Accounting check overridden. Reason: %s` |

### D.2. `wizards/finance_override_wizard_views.xml`

| Line | Original | Đề xuất |
|-----:|----------|---------|
| 7 | `<form string="Override kiem tra Ke toan">` | `<form string="Override Accounting Check">` |
| 10 | `placeholder="Nhap ly do override..."` | `placeholder="Enter override reason..."` |

### D.3. `controllers/main.py`

| Line | Context | Original | Đề xuất |
|-----:|---------|----------|---------|
| 199 | feedback | `Hoàn thành từ Portal` | `Completed from Portal` |
| 238 | feedback | `Xac nhan thuc hien tu Portal Hoat dong can lam` | `Confirmed from Portal — Pending Activities` |

---

## E. DATA XML — OFFBOARDING PLANS & SURVEY (→ English)

### E.1. `data/offboarding_activity_plan_data.xml`

| record id | field | Original | Đề xuất |
|-----------|-------|----------|---------|
| `offboarding_activity_plan` | name | `Quy trình nghỉ việc RST (22 Bước)` | `RST Resignation Process (22 Steps)` |
| `plan_step_8_exit_interview` | summary | `Bước 8: Thực hiện Exit Interview` | `Step 8: Conduct Exit Interview` |
| `plan_step_8_exit_interview` | note | `Nhân viên thực hiện làm exit interview theo mẫu.` | `Employee completes the exit interview using the template.` |
| `plan_step_9_handover_work` | summary | `Bước 9: Bàn giao công việc, tài liệu` | `Step 9: Hand over work and documents` |
| `plan_step_9_handover_work` | note | `Tiến hành bàn giao công việc, tài liệu, giấy tờ liên quan.` | `Hand over work, documents and related papers.` |
| `plan_step_10_evaluate` | summary | `Bước 10: Đánh giá công việc bàn giao` | `Step 10: Evaluate the handover` |
| `plan_step_10_evaluate` | note | `Quản lý trực tiếp đánh giá chất lượng bàn giao.` | `Direct manager evaluates handover quality.` |
| `plan_step_11_confirm_recovery` | summary | `Bước 11: Xác nhận hoàn tất thu hồi` | `Step 11: Confirm full recovery completion` |
| `plan_step_11_confirm_recovery` | note | `Xác nhận đã thu hồi đầy đủ các checklist bàn giao.` | `Confirm all handover checklist items have been recovered.` |
| `plan_step_12_check_payments` | summary | `Bước 12: Kiểm tra các khoản thanh toán chưa hoàn tất` | `Step 12: Check outstanding payments` |
| `plan_step_12_check_payments` | note | (Vietnamese paragraph listing advances/business trips/loans) | `System/Accounting reviews outstanding payments: - Unsettled advances - Unpaid business-trip expenses - Company loans/borrowings. Notify the employee if any items remain.` |
| `plan_step_13_it_confirm` | summary | `Bước 13: IT xác nhận hoàn thành checklist` | `Step 13: IT confirms checklist completion` |
| `plan_step_13_it_confirm` | note | (IT list) | `IT confirms: - Email deactivated - Internal accounts deactivated - Equipment/devices recovered.` |
| `plan_step_14_admin_confirm` | summary | `Bước 14: Admin xác nhận checklist bàn giao` | `Step 14: Admin confirms handover checklist` |
| `plan_step_14_admin_confirm` | note | (Admin list) | `Admin confirms recovery: - Office keyboard - Biometric Staff ID deletion - Desk/cabinet keys - Mobile phone & accessories - ...` |
| `plan_step_15_hr_pvi` | summary | `Bước 15: HR xác nhận thẻ PVI` | `Step 15: HR confirms PVI card` |
| `plan_step_15_hr_pvi` | note | `HR xác nhận hoàn thành checklist bàn giao PVI Health Insurance Card (included dependents).` | `HR confirms PVI Health Insurance Card handover (including dependents).` |
| `plan_step_17_sign_settlement` | summary | `Bước 17: Ký quyết toán lương` | `Step 17: Sign salary settlement` |
| `plan_step_17_sign_settlement` | note | `Ký biên bản quyết toán lương cuối cùng.` | `Sign the final salary settlement record.` |
| `plan_step_19_pay_period` | summary | `Bước 19: Thanh toán theo kỳ lương` | `Step 19: Pay according to payroll cycle` |
| `plan_step_19_pay_period` | note | `Thực hiện thanh toán theo kỳ lương.` | `Execute payment per the payroll cycle.` |
| `plan_step_20_final_handover` | summary | `Bước 20: Bàn giao Quyết định & Giấy tờ` | `Step 20: Hand over Resignation Decision & Documents` |
| `plan_step_20_final_handover` | note | `Nhân viên nhận quyết định nghỉ việc, lương và các giấy tờ liên quan.` | `Employee receives the resignation decision, final pay and related documents.` |

### E.2. `data/offboarding_plan_rst.xml`

| record id | field | Original | Đề xuất |
|-----------|-------|----------|---------|
| `offboarding_activity_plan_rst` | name | `Quy trình nghỉ việc RST` | `RST Resignation Process` |
| `rst_template_employee_checklist` | summary | `Thực hiện checklist nghỉ việc` | `Complete resignation checklist` |
| `rst_template_employee_checklist` | note | `Thực hiện các công việc bàn giao theo quy trình.` | `Complete handover tasks per the process.` |
| `rst_template_handover` | summary | `Bàn giao công việc, tài liệu, giấy tờ` | `Hand over work, documents and papers` |
| `rst_template_handover` | note | `Bàn giao toàn bộ tài liệu và công việc cho người kế nhiệm hoặc quản lý.` | `Hand over all documents and work to the successor or manager.` |
| `rst_template_it_checklist` | summary | `IT: Thu hồi thiết bị & Vô hiệu hóa tài khoản` | `IT: Recover equipment & Deactivate accounts` |
| `rst_template_it_checklist` | note | (HTML list with "Tài khoản nội bộ", "Thiết bị máy móc liên quan") | `<ul><li>Deactivate email</li><li>Internal accounts</li><li>Related equipment</li></ul>` |
| `rst_template_admin_checklist` | summary | `Admin: Thu hồi tài sản văn phòng` | `Admin: Recover office assets` |
| `rst_template_admin_checklist` | note | (HTML list — English items, keep) | (no change) |
| `rst_template_hr_checklist` | summary | `HR: Thu hồi thẻ BHYT & Giấy tờ` | `HR: Recover insurance card & documents` |
| `rst_template_hr_checklist` | note | (HTML list mixing English/Vietnamese items) | `<ul><li>PVI Health Insurance Card (including dependents)</li><li>Recover personnel papers and HR records</li><li>Confirm final settlement record</li></ul>` |

### E.3. `data/survey_exit_interview_data.xml`

**Quan trọng:** Survey này có 114 chuỗi tiếng Việt (sections, questions, answers) gửi tới nhân viên VN. Tương tự portal templates, **nếu dịch sang English có thể ảnh hưởng UX**. Tôi đề xuất 1 trong 2 option:

- **Option 1:** Giữ Vietnamese (vì survey gửi cho NV Việt Nam điền) — chỉ chuẩn hoá lỗi typo/diacritics nếu có.
- **Option 2:** Dịch toàn bộ sang English theo quy ước chung.

Nếu chọn Option 2 → tôi sẽ liệt kê chi tiết 114 chuỗi với bản dịch trong file phụ `DANH_SACH_SURVEY_DICH_EN_0214.md` (tránh file này quá dài). Xin xác nhận hướng nào trước khi tôi mở rộng.

---

## F. EMAIL TEMPLATES — GIỮ VIETNAMESE + CHUẨN HOÁ DẤU

> **Hành động:** Chỉ chuẩn hoá lại 4 template hiện đang viết Vietnamese **không dấu** (transliterate). Body content giữ nguyên cấu trúc, chỉ thêm dấu cho đúng tiếng Việt chuẩn.

| # | File | Tình trạng | Hành động |
|--:|------|-----------|-----------|
| 1 | `email_template_adecco_notification.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 2 | `email_template_dept_confirm_done.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 3 | `email_template_dept_offboarding_assignment.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 4 | `email_template_dept_offboarding_reminder.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 5 | `email_template_employee_approved_notification.xml` | **Không dấu** | 🔧 Thêm dấu: `Thong bao don nghi viec da duoc duyet` → `Thông báo đơn nghỉ việc đã được duyệt`, v.v. |
| 6 | `email_template_exit_survey.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 7 | `email_template_manager_approval_reminder.xml` | **Không dấu** | 🔧 Thêm dấu: `Nhac quan ly duyet don nghi viec` → `Nhắc quản lý duyệt đơn nghỉ việc`, v.v. |
| 8 | `email_template_offboarding_completion.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 9 | `email_template_offboarding_reminder.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 10 | `email_template_salary_settlement.xml` | Vietnamese có dấu | ✅ Giữ nguyên |
| 11 | `email_template_social_insurance.xml` | Vietnamese có dấu | ✅ Giữ nguyên |

**Subject & template name cần chuẩn hoá:**

| File | Field | Hiện tại | Đề xuất (Vietnamese có dấu) |
|------|-------|----------|-----------------------------|
| `email_template_employee_approved_notification.xml` | `name` | `RST - Thong bao don nghi viec da duoc duyet` | `RST - Thông báo đơn nghỉ việc đã được duyệt` |
| `email_template_employee_approved_notification.xml` | `subject` | `[RST Offboarding] Don nghi viec cua ban da duoc duyet` | `[RST Offboarding] Đơn nghỉ việc của bạn đã được duyệt` |
| `email_template_manager_approval_reminder.xml` | `name` | `RST - Nhac quan ly duyet don nghi viec` | `RST - Nhắc quản lý duyệt đơn nghỉ việc` |
| `email_template_manager_approval_reminder.xml` | `subject` | `[RST Offboarding] Ban co don nghi viec can duyet - {{ ... }}` | `[RST Offboarding] Bạn có đơn nghỉ việc cần duyệt - {{ ... }}` |

> Sau khi confirm, tôi sẽ rà từng body_html của 2 template này và thêm dấu cho tất cả Vietnamese strings bên trong.

---

## H. BO SUNG PHASE 5 - ANNUAL LEAVE ADVANCE / DEDUCTION

| File | Context | Source string | Proposed Vietnamese |
|------|---------|---------------|---------------------|
| `models/approval_request_rst_fields.py` | Field string | `Advance Annual Leave Days` | `So ngay phep nam ung truoc` |
| `models/approval_request_rst_fields.py` | Field string | `Has Advance Annual Leave` | `Co phep nam ung truoc` |
| `models/approval_request_rst_fields.py` | Field string | `AL Deduction Currency` | `Tien te khau tru phep nam` |
| `models/approval_request_rst_fields.py` | Field string | `AL Deduction Rate (per day)` | `Don gia khau tru phep nam (moi ngay)` |
| `models/approval_request_rst_fields.py` | Field string | `AL Deduction Amount` | `So tien khau tru phep nam` |
| `models/approval_request_rst_fields.py` | Field string | `AL Deduction Note` | `Ghi chu khau tru phep nam` |
| `models/approval_request_rst_fields.py` | Field string | `Advance AL Settled` | `Da chot phep nam ung truoc` |
| `models/approval_request_rst_finance.py` | Pending summary | `Advance Annual Leave: %(days).2f day(s) - deduction not settled` | `Phep nam ung truoc: %(days).2f ngay - chua chot khau tru` |
| `models/approval_request_rst_finance.py` | Action/UserError | `Settle Advance Annual Leave` | `Chot khau tru phep nam ung truoc` |
| `models/approval_request_rst_finance.py` | UserError | `This request has no advance annual leave to deduct.` | `Don nay khong co phep nam ung truoc can khau tru.` |
| `models/approval_request_rst_finance.py` | UserError | `Please enter the advance annual leave deduction amount before settling.` | `Vui long nhap so tien khau tru phep nam truoc khi chot.` |
| `models/approval_request_rst_finance.py` | Chatter | `Advance annual leave deduction settled: %(days).2f day(s) = %(amount)s` | `Da chot khau tru phep nam ung truoc: %(days).2f ngay = %(amount)s` |
| `models/approval_request_rst_finance.py` | Notification | `Advance annual leave deduction has been settled.` | `Da chot khau tru phep nam ung truoc.` |
| `views/resignation_request_views.xml` | Group string | `Advance Annual Leave Deduction` | `Khau tru phep nam ung truoc` |
| `views/resignation_request_views.xml` | Button string | `Chot khau tru phep` | `Chot khau tru phep` |
| `views/finance_check_report_views.xml` | Column string | `Advance AL` | `Phep nam ung truoc` |
| `views/finance_check_report_views.xml` | Column string | `AL Deduction` | `Khau tru phep nam` |
| `views/finance_check_report_views.xml` | Column string | `AL Settled` | `Da chot phep nam` |
| `data/email_template_employee_approved_notification.xml` | Email body | `Phep nam ung truoc` | `Phep nam ung truoc` |
| `data/email_template_salary_settlement.xml` | Email body | `Khau tru phep nam ung truoc` | `Khau tru phep nam ung truoc` |

Ghi chu Phase 5: module hien chua co file `.po`, nen chua bo sung ban dich trong i18n.

---

## G. KHÔNG ĐỘNG VÀO (đã thoả thuận)

- Demo data: `rst_demo_data.xml`, `test_security_users.xml`, `departure_reason_data.xml`, `approval_category_data.xml`
- Comments Python (`# ...`) & XML (`<!-- ... -->`)
- Docstrings (`"""..."""`)
- `notes/`, `docs/`, `*.md` documentation
- File config technical: `ir_cron_data.xml`, `config_ui_cleanup.xml`, `acl_cleanup.xml`, `offboarding_request_rules.xml`, `security.xml` (đều đã English/technical only)

---

## ❓ CÁC ĐIỂM CẦN BẠN QUYẾT ĐỊNH TRƯỚC KHI APPLY EDIT

1. **Portal templates (B.1, B.2):** dịch English hay giữ Vietnamese?
2. **Survey exit interview (E.3 — 114 strings):** dịch English hay giữ Vietnamese?
3. **Encoding errors** trong `approval_request_rst_fields.py` lines 36, 255, 267, `approval_request_rst_approval.py` line 36 (`Báº¡n khÃ´ng...`): cần fix encoding khi translate (đây là tiếng Việt bị mojibake utf-8).
4. **Mức chi tiết cho email template name/subject:** chỉ chuẩn hoá dấu 2 template không dấu, hay dịch luôn toàn bộ name+subject sang English (chỉ giữ body Vietnamese)?

---

*File này được tạo tự động bằng quá trình scan toàn module M02_P0214 ngày 2026-05-20.*
