# Bản Thiết Kế Kỹ Thuật — Module M02_P0213

**Module:** `M02_P0213` — Quy Trình Offboarding OPS  
**Nền tảng:** Odoo 19 Enterprise  
**Phạm vi:** Phân tích kỹ thuật chỉ đọc — không sửa file, không áp patch  
**Ngày phân tích:** 2026-05-13

---

## Các File Dùng Để Xác Nhận

| File | Mục đích |
|---|---|
| `convention/QUY_UOC_DAT_TEN_VA_RULE.md` | Quy ước đặt tên và quy tắc thiết kế |
| `structure/module_map.json` | Tổng quan cấu trúc module |
| `__manifest__.py` | Manifest và thứ tự nạp dữ liệu |
| `models/resignation_request.py` | Model chính — logic nghiệp vụ cốt lõi |
| `models/mail_activity.py` | Override activity |
| `models/res_company.py` | Cấu hình cấp công ty |
| `models/res_config_settings.py` | Related fields cho settings |
| `models/survey_user_input.py` | Tự động hóa sau khi survey hoàn tất |
| `security/ir.model.access.csv` | ACL cho 13 quyền truy cập model |
| `security/security.xml` | Record rules hẹp cho survey |
| `security/offboarding_request_rules.xml` | Record rules mở rộng phạm vi cho approval.request |
| `controllers/main.py` | Portal controller — 3 route |
| `views/resignation_request_views.xml` | Kế thừa form và views danh mục |
| `views/resignation_portal_template.xml` | QWeb template cho portal |
| `views/res_company_views.xml` | Form cấu hình công ty |
| `views/config_menu_views.xml` | Menu cấu hình và server action |
| `views/res_config_settings_views.xml` | Tồn tại nhưng không được nạp (cố ý) |
| `data/approval_category_data.xml` | Bản ghi danh mục nghỉ việc |
| `data/ir_cron_data.xml` | Cron nhắc nhở 3 ngày một lần |
| `data/offboarding_activity_plan_data.xml` | Kế hoạch hoạt động và 5 template |
| `data/config_ui_cleanup.xml` | Xóa view và action settings cố ý |
| `data/email_template_*.xml` | 5 email template |
| `notes/RA_SOAT_QUYEN_0213.md` | Rà soát quyền thực tế |
| `notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md` | Ma trận quyền expected |

---

## 1. Tổng Quan Module

### 1.1. Mục Đích

Module `M02_P0213` mở rộng quy trình phê duyệt Odoo (`approvals`) để xử lý **luồng offboarding OPS** — tức là toàn bộ quy trình từ khi nhân viên nộp đơn nghỉ việc đến khi tài khoản bị vô hiệu hóa và hồ sơ được đánh dấu hoàn tất.

Module không tạo model mới. Toàn bộ logic được nhúng vào model hiện có của Odoo thông qua `_inherit`.

### 1.2. Phụ Thuộc

Khai báo trong `__manifest__.py`:

```python
'depends': ['base', 'mail', 'approvals', 'hr', 'portal', 'survey', 'M02_P0200']
```

`M02_P0200` là module nền cung cấp các group phân quyền dùng trong toàn bộ dòng `M02_*`.

### 1.3. Thứ Tự Nạp Dữ Liệu

Manifest nạp data theo thứ tự phụ thuộc nghiêm ngặt:

1. Survey data (survey cần tồn tại trước)
2. Security (ACL + record rules)
3. Category (tạo category nghỉ việc, tham chiếu survey)
4. Email templates
5. Cron
6. Activity plan (tham chiếu category)
7. Config UI cleanup (xóa view settings)
8. Views (views tham chiếu category id)

`views/res_config_settings_views.xml` **không có trong manifest** — đây là cố ý, do `config_ui_cleanup.xml` đã xóa view id đó.

---

## 2. Kiến Trúc Model

### 2.1. Danh Sách Model Được Kế Thừa

| Model gốc | Class kế thừa | Vị trí |
|---|---|---|
| `approval.category` | `ApprovalCategory` | `models/resignation_request.py` |
| `approval.request` | `ResignationRequest` | `models/resignation_request.py` |
| `mail.activity` | `MailActivity` | `models/mail_activity.py` |
| `res.company` | `ResCompany` | `models/res_company.py` |
| `res.config.settings` | `ResConfigSettings` | `models/res_config_settings.py` |
| `survey.user_input` | `SurveyUserInput` | `models/survey_user_input.py` |

Module không khai báo `_name` mới — không có model nào được tạo thuần túy.

### 2.2. Quy Ước Đặt Tên Field

Theo convention trong `QUY_UOC_DAT_TEN_VA_RULE.md`:

- Field mới thêm vào model gốc: prefix `x_psm_0213_`  
  Ví dụ: `x_psm_0213_employee_id`, `x_psm_0213_is_offboarding`
- Action mới: prefix `action_psm_*` hoặc đặt thẳng `action_*` nếu là override
- View mới: prefix `view_psm_*`
- XML ID data record: prefix `psm_0213_*`

### 2.3. Guard Pattern

Mọi override logic đặc thù của 0213 đều kiểm tra trước:

```python
if not self._is_0213_offboarding_request():
    return super()...
```

`_is_0213_offboarding_request()` kiểm tra `category_id.x_psm_0213_is_offboarding == True`.

---

## 3. Fields Được Thêm

### 3.1. `approval.request` — 21 Field

| Field | Kiểu | Mô tả |
|---|---|---|
| `x_psm_0213_employee_id` | Many2one `hr.employee` | Nhân viên nghỉ việc |
| `x_psm_0213_resignation_reason` | Text | Lý do nghỉ việc dạng mô tả tự do |
| `x_psm_0213_resignation_reason_id` | Many2one `hr.departure.reason` | Loại nghỉ việc |
| `x_psm_0213_resignation_date` | Date | Ngày nghỉ dự kiến |
| `request_status` | Selection | Extend trạng thái base với giá trị `done` |
| `x_psm_0213_is_rehire` | Boolean | Đã đánh dấu tái tuyển |
| `x_psm_0213_is_blacklisted` | Boolean | Đã đánh dấu blacklist |
| `x_psm_0213_adecco_notification_sent` | Boolean | Đã gửi Adecco |
| `x_psm_0213_resignation_employee_name` | Char (related) | Họ tên nhân viên |
| `x_psm_0213_resignation_manager_name` | Char (related) | Line Manager |
| `x_psm_0213_resignation_department` | Char (related) | Phòng ban |
| `x_psm_0213_job_id` | Many2one `hr.job` (related) | Chức vụ |
| `x_psm_0213_employee_activity_ids` | Many2many `mail.activity` (compute) | Danh sách activity offboarding của nhân viên |
| `x_psm_0213_exit_survey_completed` | Boolean (compute) | Survey đã hoàn tất |
| `x_psm_0213_all_activities_completed` | Boolean (compute) | Tất cả activity đã done |
| `x_psm_0213_type_contract` | Char (compute) | Loại hợp đồng hiển thị |
| `x_psm_0213_is_social_insurance_contract` | Boolean (compute) | Có thuộc luồng BHXH trực tiếp |
| `x_psm_0213_resignation_owner_email` | Char (related) | Email người yêu cầu |
| `x_psm_0213_is_plan_launched` | Boolean | Đã khởi chạy plan |
| `x_psm_0213_exit_survey_user_input_id` | Many2one `survey.user_input` | Bài làm exit interview |
| `x_psm_0213_owner_related_activity_ids` | Many2many `mail.activity` (related) | Activity liên quan owner |

**Lưu ý dead code:** `_compute_owner_related_activity_ids` được định nghĩa trong class nhưng field `x_psm_0213_owner_related_activity_ids` dùng `related=` thay vì `compute=`. Method này không được gọi và là dead code.

### 3.2. `approval.category` — 1 Field

| Field | Kiểu | Mô tả |
|---|---|---|
| `x_psm_0213_is_offboarding` | Boolean | Marker nhận diện category offboarding |

### 3.3. `mail.activity` — 2 Field

| Field | Kiểu | Mô tả |
|---|---|---|
| `x_psm_0213_ops_display_state` | Selection (compute, không stored) | Trạng thái hiển thị trên portal |
| `x_psm_0213_is_offboarding_activity` | Boolean (compute, stored) | Marker dùng cho record rule activity thuộc flow 0213 |

### 3.4. `res.company` — 11 Field

| Field | Kiểu | Mô tả |
|---|---|---|
| `x_psm_0213_exit_survey_template_id` | Many2one `mail.template` | Template email gửi survey |
| `x_psm_0213_adecco_template_id` | Many2one `mail.template` | Template Adecco |
| `x_psm_0213_social_insurance_template_id` | Many2one `mail.template` | Template BHXH |
| `x_psm_0213_employee_reminder_template_id` | Many2one `mail.template` | Template nhắc nhở nhân viên |
| `x_psm_0213_department_reminder_template_id` | Many2one `mail.template` | Template nhắc nhở phòng ban |
| `x_psm_0213_adecco_notification_email` | Char | Email Adecco nhận thông báo |
| `x_psm_0213_default_it_user_id` | Many2one `res.users` | User mặc định cho task IT |
| `x_psm_0213_default_on_demand_user_id` | Many2one `res.users` | User mặc định cho task on-demand |
| `x_psm_0213_social_insurance_contract_type_ids` | Many2many `hr.contract.type` | Loại hợp đồng đi luồng BHXH trực tiếp |
| `x_psm_0213_reminder_overdue_days` | Integer | Số ngày trễ tối thiểu trước khi gửi nhắc |
| `x_psm_0213_reminder_extension_days` | Integer | Số ngày gia hạn sau khi gửi nhắc |

Bảng quan hệ custom: `res_company_hr_contract_type_0213_rel`

---

## 4. Logic Nghiệp Vụ Cốt Lõi

### 4.1. Luồng Chính

```
Portal submit đơn
    → tạo approval.request (sudo, owner locked)
    → approver = line manager
    → approval gửi đi phê duyệt

Approver phê duyệt (action_approve override)
    → gửi email exit survey
    → tạo survey.user_input
    → khởi chạy activity plan (5 tasks)

Nhân viên hoàn tất survey (SurveyUserInput._mark_done override)
    → tìm activity "Hoàn thành Exit Interview"
    → action_done() activity đó
    → gửi email BHXH nếu đủ điều kiện

HR hoàn tất quy trình (action_done)
    → kiểm tra group (HR_ADMIN_M / HR_HRBP_M / HR_HEAD / SYSTEM)
    → tìm user từ employee.user_id (fallback request_owner_id)
    → vô hiệu hóa tài khoản nếu là portal/internal user (không đụng admin)

Tùy chọn sau đó:
    → action_rehire: đánh dấu x_psm_0213_is_rehire
    → action_blacklist: đánh dấu x_psm_0213_is_blacklisted (chỉ HR_HRBP_M trở lên)
```

### 4.2. Override Quan Trọng

**`action_withdraw` / `action_cancel`:**  
Nếu là request offboarding 0213 và đơn đã `approved` hoặc `refused` → raise `UserError`. Không chỉ ẩn nút UI mà còn chặn ở backend, kể cả gọi trực tiếp qua RPC.

**`action_approve`:**  
Tự động:
1. Gọi `_get_or_create_0213_survey_user_input()` để tạo bài làm survey
2. Gửi email exit interview với URL survey trong context
3. Khởi chạy `mail.activity.plan` nếu chưa launch

**`mail.activity.unlink` override:**  
Nếu activity gắn với request offboarding 0213 → không xóa cứng, chuyển sang `active = False` (archive). Mục đích: giữ lịch sử audit.

**`mail.activity._action_done` override:**  
Sau khi mark done → trigger recompute checklist trên `approval.request` liên quan.

### 4.3. Cron Nhắc Nhở

File `data/ir_cron_data.xml` (`noupdate="1"`):
- Chạy mỗi 3 ngày
- Gọi `ResignationRequest._cron_send_offboarding_reminders()`
- Domain tìm: request offboarding 0213, trạng thái approved, chưa done
- Gửi email nhắc nhân viên + email nhắc phòng ban nếu có activity trễ hạn
- Tự động gia hạn deadline activity nếu cấu hình `x_psm_0213_reminder_extension_days > 0`

### 4.4. Multi-company Fallback

`_get_0213_company()` trả về company theo thứ tự ưu tiên:
1. `self.company_id` (nếu có trên request)
2. `self.env.company` (company hiện tại của user)
3. `env.ref('base.main_company')` (fallback cuối)

**Rủi ro:** Activity plan trong `offboarding_activity_plan_data.xml` hard-code `company_id ref="base.main_company"` → không tự động nhân bản cho multi-company.

---

## 5. Phân Quyền Và Record Rules

### 5.1. ACL — `security/ir.model.access.csv`

13 dòng ACL. Các điểm đáng chú ý:

| ACL | Group | CRUD | Rủi ro |
|---|---|---|---|
| `access_approval_request_internal_user` | `base.group_user` | 1111 | Quá rộng — mọi internal user |
| `access_mail_activity_internal_user` | `base.group_user` | 1111 | Quá rộng |
| `access_hr_employee_internal_user` | `base.group_user` | 1100 | Có thể ghi đè dữ liệu HR |
| `access_survey_user_input_internal_user` | `base.group_user` | 1111 | Unlink survey response |
| `access_survey_user_input_portal` | `base.group_portal` | 1110 | Không unlink — đúng |
| `access_hr_departure_reason_internal` | `base.group_user` | 1000 | Chỉ đọc — đúng |

### 5.2. Record Rules — `security/security.xml` (`noupdate="1"`)

5 rule scope hẹp:

| Rule | Model | Domain |
|---|---|---|
| `rule_psm_0213_survey_survey_internal` | `survey.survey` | Chỉ survey exit interview của 0213 |
| `rule_psm_0213_survey_question_internal` | `survey.question` | Câu hỏi của survey đó |
| `rule_psm_0213_survey_question_answer_internal` | `survey.question.answer` | Đáp án của survey đó |
| `rule_psm_0213_survey_user_input_portal_own` | `survey.user_input` | Portal chỉ thấy bài làm của mình (`partner_id = user.partner_id` hoặc `email = user.email`) |
| `rule_psm_0213_survey_user_input_internal_done` | `survey.user_input` | Internal chỉ thấy bài làm đã `done` của survey 0213 |

### 5.3. Record Rules — `security/offboarding_request_rules.xml` (`noupdate="0"`)

4 rule POSITIVE extension scope (mở rộng phạm vi theo group):

| Rule | Model | Group | Quyền |
|---|---|---|---|
| `rule_psm_0213_approval_request_ops_read` | `approval.request` | OPS groups | Chỉ đọc request offboarding 0213 |
| `rule_psm_0213_approval_request_hr_read` | `approval.request` | HR groups | Chỉ đọc request offboarding 0213 |
| `rule_psm_0213_approval_request_hr_write` | `approval.request` | HR_ADMIN_M, HR_HRBP_M, HR_HEAD, SYSTEM | Đọc + ghi request offboarding 0213 |
| `rule_psm_0213_approval_approver_all_read` | `approval.approver` | Tất cả nhóm 0213 | Chỉ đọc approver lines |

Domain chung: `category_id.x_psm_0213_is_offboarding = True`

### 5.4. Ma Trận Quyền Expected (Phase 0)

Theo `notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md`, 8 nhóm 0200 cần phân quyền:

| Nhóm | approval.request | survey.user_input | mail.activity |
|---|---|---|---|
| `GDH_RST_OPS_OC_S` | Read (scope được giao) | Không xem | Read (scope được giao) |
| `GDH_RST_OPS_OM_M` | Read (toàn bộ OPS) | Read (done only) | Read |
| `GDH_RST_HR_ADMIN_S` | Read + Write | Read | Read + xử lý |
| `GDH_RST_HR_ADMIN_M` | Read + Write + Done | Read | Read + xử lý |
| `GDH_RST_HR_HRBP_S` | Read | Read | Read |
| `GDH_RST_HR_HRBP_M` | Read + Write | Read | Read |
| `GDH_RST_HR_HEAD_M` | Read + Write | Read | Read + xử lý |
| `GDH_RST_SYSTEM_ST_M` | Read + Write | Read | Read + xử lý |
| Portal employee | Chỉ đơn của mình | Chỉ bài làm của mình | Chỉ activity giao cho mình |

---

## 6. Portal Controller

### 6.1. Các Route

File `controllers/main.py`. Tất cả route đều dùng `auth="user"` — bắt buộc đăng nhập.

| Route | Method | Mô tả |
|---|---|---|
| `/my/resignation/ops` | GET | Hiển thị form portal — đơn hiện tại + checklist activity |
| `/my/resignation/submit` | POST | Tạo đơn nghỉ việc mới |
| `/my/resignation/ops/activity/done` | POST | Đánh dấu hoàn tất activity |

### 6.2. Kiểm Soát Phạm Vi Trong Controller

**`_get_latest_resignation_request()`:**
- Tìm `approval.request` theo `request_owner_id = request.env.user.id`
- Đúng category nghỉ việc của 0213
- Không có cách nào portal lấy đơn của người khác

**`_get_owned_resignation_request_by_id(id)`:**
- Thêm ràng buộc `id` cụ thể
- Vẫn phải đúng `request_owner_id` và category

**Route `activity/done`:**
1. Kiểm tra activity gắn với `approval.request`
2. Request đó phải thuộc chính user hiện tại
3. `activity.user_id` phải đúng bằng user đang đăng nhập
4. Chỉ khi đủ điều kiện mới gọi `activity.sudo().action_feedback(...)`

**Route `submit`:**
- Tạo đơn bằng `sudo()`
- Owner bị khóa về `request.env.user.id`
- Category bị khóa về category offboarding
- Approver được lấy từ line manager của nhân viên

### 6.3. Rủi Ro Trong Controller

**`_get_resignation_category()` thiếu `raise_if_not_found=False`:**

```python
# Hiện tại — có thể raise 500 nếu category bị xóa khỏi DB
category = self.env.ref('M02_P0213.psm_0213_approval_category_resignation')
```

Nếu category bị xóa hoặc XML ID bị đổi, route sẽ trả về 500 thay vì xử lý lỗi gracefully.

---

## 7. Views Và QWeb

### 7.1. View Kế Thừa Backend

`views/resignation_request_views.xml` kế thừa:
- `approvals.approval_request_view_form` — thêm tab offboarding, các trường 0213, nút action
- `approvals.approval_category_view_form` — thêm field marker `x_psm_0213_is_offboarding`

Dùng id substitution: `%(M02_P0213.psm_0213_approval_category_resignation)d`

**Rủi ro xpath không ổn định:**
```xml
<xpath expr="//notebook/page[1]" position="before">
```
Nếu module khác thêm page trước page đầu tiên của notebook, xpath này sẽ nhắm sai vị trí.

### 7.2. Điều Kiện Hiển Thị Nút Action

Các nút nhạy cảm được ẩn bằng `invisible` theo tổ hợp điều kiện:

| Nút | Điều kiện hiển thị |
|---|---|
| `action_send_social_insurance` | Đúng category + trạng thái approved + activity done + survey done |
| `action_send_adecco_notification` | Đúng category + approved + Full-Time + chưa gửi Adecco |
| `action_done` | Đúng category + approved + tất cả activity done + survey done |
| `action_rehire` | Done + chưa rehire + chưa blacklist |
| `action_blacklist` | Done + chưa blacklist + chưa rehire |
| `action_withdraw` | Không phải approved/refused |
| `action_cancel` | Request owner + không phải approved/refused |

**Lưu ý:** Đây là lớp chặn UI — lớp bảo vệ thật sự vẫn ở Python (group check + UserError).

### 7.3. QWeb Portal Template

`views/resignation_portal_template.xml`:
- CSS scoped trong class `.psm-ops-resignation-portal`
- CSRF token: `request.csrf_token()`
- Form submit POST đến `/my/resignation/submit`
- Hiển thị checklist activity theo trạng thái `x_psm_0213_ops_display_state`

### 7.4. Config UI Cleanup

`data/config_ui_cleanup.xml` (`noupdate="0"`) chứa:
```xml
<delete id="view_psm_0213_res_config_settings_form" model="ir.ui.view"/>
<delete id="action_psm_0213_offboarding_settings" model="ir.actions.act_window"/>
```

View `views/res_config_settings_views.xml` tồn tại trong source nhưng không nạp qua manifest — cố ý. Class Python `ResConfigSettings` phải tồn tại để ORM nhận các `related` field. View bị xóa để ẩn khỏi Settings UI.

---

## 8. Email Templates

Module có 5 email template:

### 8.1. `psm_0213_email_template_exit_survey`
- **Model:** `approval.request`
- **Gửi tới:** `object.request_owner_id.partner_id.email`
- **Đặc điểm:** URL survey được truyền qua `ctx.get('survey_url')` trong context khi gửi — không lưu trực tiếp vào template

### 8.2. `psm_0213_email_template_adecco_notification`
- **Model:** `hr.employee`
- **Gửi tới:** `x_psm_0213_adecco_email` từ company config
- **Nội dung:** Thông báo nhân viên nghỉ việc gửi cho Adecco

### 8.3. `psm_0213_email_template_social_insurance`
- **Model:** `hr.employee`
- **Gửi tới:** `object.work_email`
- **Rủi ro:** `work_email` có thể `False` nếu nhân viên chưa có email công ty → gửi thất bại

### 8.4. `psm_0213_email_template_offboarding_reminder`
- **Model:** `approval.request`
- **Gửi tới:** `object.request_owner_id.partner_id.email`
- **Nội dung:** Nhắc nhở nhân viên hoàn thành thủ tục nghỉ việc

### 8.5. `psm_0213_email_template_dept_offboarding_reminder`
- **Model:** `approval.request`
- **Gửi tới:** Người dùng nội bộ có activity trễ hạn (gửi từ cron)
- **Nội dung:** Nhắc phòng ban xử lý đầu việc offboarding

---

## 9. Rủi Ro Kỹ Thuật Cần Ưu Tiên Xử Lý

### 9.1. Mức Độ Cao

**ACL `base.group_user` quá rộng:**
- `approval.request` + `mail.activity` mở `unlink` cho toàn bộ internal user
- Người dùng nội bộ có thể xóa approval request và activity của bất kỳ quy trình nào nếu record rules không chặn đủ
- **Cần làm:** Thu hẹp ACL về group cụ thể của 0213; bổ sung record rule NEGATIVE nếu cần

**`sudo()` không có guard scope trước:**
- Nhiều chỗ dùng `sudo()` trực tiếp mà không kiểm tra category trước
- Rủi ro: nếu domain check bị bỏ sót, code chạy với quyền `sudo` trên dữ liệu ngoài 0213
- **Cần làm:** Mọi `sudo()` phải đứng sau block `if not self._is_0213_offboarding_request(): return`

**`_get_resignation_category()` thiếu `raise_if_not_found=False`:**
- Nếu XML ID bị đổi hoặc record bị xóa → 500 error tại portal route
- **Cần làm:** Thêm `raise_if_not_found=False` và xử lý `None` gracefully

### 9.2. Mức Độ Trung Bình

**Activity plan hard-code `base.main_company`:**
- Multi-company deployment sẽ không tự động có plan cho company phụ
- **Cần làm:** Xem xét tạo plan theo từng company hoặc dùng `company_id = False` nếu plan dùng chung

**`approval_category_data.xml` dùng `noupdate="0"`:**
- Mỗi lần upgrade ghi đè category record
- Nếu admin đã sửa tên/config category qua UI → bị reset
- **Cân nhắc:** Đổi sang `noupdate="1"` sau khi production đã ổn định

**`email_to: object.work_email` có thể null:**
- Template BHXH gửi tới `work_email` — nếu trống → gửi thất bại im lặng
- **Cần làm:** Fallback sang `object.private_email` hoặc kiểm tra trước khi gửi

### 9.3. Mức Độ Thấp (Cần Theo Dõi)

**xpath `//notebook/page[1]` không ổn định:**
- Phụ thuộc vào thứ tự page trong form gốc
- Nếu module khác thêm page trước → nhắm sai vị trí

**Dead code `_compute_owner_related_activity_ids`:**
- Method được định nghĩa nhưng field dùng `related=` thay vì `compute=`
- Không gây lỗi runtime nhưng gây nhầm lẫn khi đọc code

**`offboarding_request_rules.xml` dùng `noupdate="0"`:**
- Record rules bị ghi đè mỗi lần upgrade
- Nếu admin đã tinh chỉnh rule qua UI → bị reset

---

## 10. Điểm Cần Xác Nhận Nghiệp Vụ Trước Khi Sửa Code

Các quyết định sau cần xác nhận từ business owner trước khi thay đổi:

### 10.1. Internal User `unlink` trên `approval.request`

Hiện tại: mọi internal user có quyền `unlink` trên `approval.request`.  
Câu hỏi: nghiệp vụ có muốn người dùng nội bộ được xóa đơn nghỉ việc không?  
Expected theo Phase 0: không nhóm nào được `unlink` mặc định.

### 10.2. `OPS_OC_S` có được xem survey result không?

Ma trận Phase 0: OPS staff không xem trực tiếp survey result.  
Cần xác nhận business case nếu có trường hợp ngoại lệ.

### 10.3. `action_view_survey_results` ai được bấm?

Hiện tại: logic Python dùng `sudo()` để mở kết quả survey — không có group check.  
Expected: chỉ từ `OPS_OM_M` trở lên.  
Cần thêm guard `has_group(...)` trước khi call.

### 10.4. Cờ `rehire` / `blacklist` / `done` — ai được bấm?

Các cờ này hiện được ghi qua `sudo().write()` bên trong action method.  
Lớp chặn duy nhất là `invisible` trên UI.  
Cần thêm group check ở Python để chặn RPC trực tiếp.

### 10.5. Portal có được `write` trên `survey.user_input` ngoài bài làm của chính mình không?

Hiện tại: ACL mở `write/create` cho portal trên `survey.user_input`.  
Record rule chặn theo `partner_id = user.partner_id`.  
Cần test case: portal đoán ID bài làm của người khác và gửi `write` request trực tiếp.

---

## Phụ Lục: Sơ Đồ Luồng Tóm Tắt

```
[Portal] Nhân viên nộp đơn
         ↓ POST /my/resignation/submit
         ↓ sudo() + owner locked + category locked
[Backend] approval.request tạo → gửi phê duyệt → Line Manager

[Line Manager] Phê duyệt
         ↓ action_approve override
         ↓ tạo survey.user_input
         ↓ gửi email exit survey (URL qua context)
         ↓ khởi chạy mail.activity.plan (5 tasks)

[Portal] Nhân viên làm survey
         ↓ survey.user_input._mark_done override
         ↓ tìm activity "Hoàn thành Exit Interview"
         ↓ action_done() → recompute checklist
         ↓ gửi email BHXH nếu đủ điều kiện

[Cron] Mỗi 3 ngày
         ↓ _cron_send_offboarding_reminders()
         ↓ tìm request approved + chưa done
         ↓ gửi email nhắc nhân viên + phòng ban
         ↓ gia hạn deadline nếu cấu hình

[HR] Hoàn tất quy trình
         ↓ action_done (group check: ADMIN_M / HRBP_M / HEAD / SYSTEM)
         ↓ vô hiệu hóa tài khoản (portal/internal only, không đụng admin)
         ↓ Tùy chọn: action_rehire hoặc action_blacklist
```

---

## 11. Kế Hoạch Triển Khai Theo Từng Bước

Phần này mô tả cách triển khai nội dung blueprint theo từng bước thực tế. Thứ tự ưu tiên là: nắm quy ước và cấu trúc module trước, xác nhận bằng source code hiện tại, sau đó mới sửa theo từng lớp phụ thuộc.

### 11.1. Bước 0 — Chốt Phạm Vi Và Đối Chiếu Blueprint Với Source

Trước khi code, cần đối chiếu blueprint với source hiện tại vì một số tên field trong tài liệu phân tích có thể khác với code thật.

Ví dụ source hiện tại đang dùng:

- `x_psm_0213_resignation_reason_id`, không phải `x_psm_0213_departure_reason_id`
- `x_psm_0213_resignation_date`, không phải `x_psm_0213_last_working_day`
- `x_psm_0213_is_rehire`, `x_psm_0213_is_blacklisted`
- `x_psm_0213_adecco_notification_email`
- `x_psm_0213_reminder_overdue_days`
- `x_psm_0213_reminder_extension_days`

Nguyên tắc: nếu `structure/module_map.json` hoặc blueprint khác source code hiện tại thì ưu tiên source code, sau đó regenerate lại module map nếu cần.

### 11.2. Bước 1 — Nền Module Và Manifest

Rà hoặc triển khai trước:

- `__manifest__.py`
- `depends`: `base`, `mail`, `approvals`, `hr`, `portal`, `survey`, `M02_P0200`
- thứ tự nạp data trong manifest

Thứ tự data nên giữ theo dependency:

1. `data/survey_exit_interview_data.xml`
2. security: ACL và record rules
3. `data/approval_category_data.xml`
4. email templates
5. cron
6. activity plan
7. config cleanup
8. views

Bước này cần làm kỹ vì XML data tham chiếu nhau chặt. Sai thứ tự có thể làm upgrade module lỗi ngay.

### 11.3. Bước 2 — Khai Báo Field Và Model Inherit

Triển khai các `_inherit`, không tạo model mới:

- `approval.category`: marker `x_psm_0213_is_offboarding`
- `approval.request`: field offboarding và các compute field liên quan
- `mail.activity`: trạng thái hiển thị portal `x_psm_0213_ops_display_state`
- `res.company`: cấu hình template, email, user mặc định, số ngày nhắc việc
- `res.config.settings`: related fields cho settings
- `survey.user_input`: hook sau khi survey hoàn tất

Ở bước này chỉ nên thêm field và compute cơ bản. Chưa nên nhồi toàn bộ action nghiệp vụ để dễ kiểm tra lỗi ORM, view, và upgrade.

### 11.4. Bước 3 — Data Nghiệp Vụ Nền

Sau khi field đã tồn tại, mới nạp các data nghiệp vụ:

- survey exit interview
- approval category offboarding
- email templates
- activity plan và activity templates
- cron reminder

Cần kiểm tra các XML ID chính:

- `M02_P0213.psm_0213_approval_category_resignation`
- `M02_P0213.psm_0213_survey_exit_interview`
- các `psm_0213_email_template_*`
- activity plan và task templates của offboarding

### 11.5. Bước 4 — Logic Chính Của `approval.request`

Triển khai logic chính trong `models/resignation_request.py` theo luồng:

1. Portal tạo đơn nghỉ việc
2. Line manager approve
3. Gửi email exit survey
4. Tạo hoặc tái dùng `survey.user_input`
5. Launch activity plan
6. Nhân viên hoàn tất survey thì mark activity Exit Interview done
7. Nếu đủ điều kiện thì gửi email BHXH
8. HR hoàn tất quy trình thì deactivate user
9. Sau khi done mới cho thao tác rehire hoặc blacklist

Mọi override đặc thù 0213 cần giữ guard pattern:

```python
if not self._is_0213_offboarding_request():
    return super()
```

Mọi chỗ dùng `sudo()` nên đứng sau block kiểm tra scope 0213 để tránh chạy quyền cao trên dữ liệu ngoài phạm vi module.

### 11.6. Bước 5 — Portal Controller

Triển khai hoặc rà `controllers/main.py` sau khi model logic cơ bản đã chạy:

- `GET /my/resignation/ops`
- `POST /my/resignation/submit`
- `POST /my/resignation/ops/activity/done`

Cần xử lý sớm các điểm rủi ro:

- `_get_resignation_category()` nên dùng `raise_if_not_found=False`
- nếu category không còn tồn tại thì trả lỗi thân thiện, không để 500
- mọi search portal phải khóa theo `request_owner_id = request.env.user.id`
- route mark activity done phải kiểm tra cả owner của request và `activity.user_id`

### 11.7. Bước 6 — Security Và Quyền

Làm security thành một phase riêng, không trộn với UI.

Các file cần rà:

- `security/ir.model.access.csv`
- `security/security.xml`
- `security/offboarding_request_rules.xml`

Ưu tiên siết các ACL đang quá rộng cho `base.group_user`, nhất là:

- `approval.request`
- `mail.activity`
- `survey.user_input`

Ngoài record rule, các action nhạy cảm cần có Python group guard:

- `action_view_survey_results`
- `action_done`
- `action_rehire`
- `action_blacklist`
- các action gửi mail nếu nghiệp vụ yêu cầu giới hạn nhóm

### 11.8. Bước 7 — Views Backend Và Portal Template

Sau khi security và logic ổn, mới hoàn thiện UI:

- `views/resignation_request_views.xml`
- `views/resignation_portal_template.xml`
- `views/res_company_views.xml`
- `views/config_menu_views.xml`

Nên hạn chế xpath phụ thuộc vị trí như:

```xml
<xpath expr="//notebook/page[1]" position="before">
```

Nếu có anchor ổn định hơn trong view gốc thì nên dùng anchor đó để tránh lệch vị trí khi module khác cũng inherit cùng form.

### 11.9. Bước 8 — Cron Và Reminder

Sau khi activity plan, email template, và company config ổn mới bật cron:

- `_cron_send_offboarding_reminders()`
- gửi reminder cho nhân viên
- gửi reminder cho phòng ban hoặc người phụ trách activity
- tự gia hạn deadline activity theo config nếu được bật

Nên test bằng manual call trước khi phụ thuộc lịch chạy thật của cron.

### 11.10. Bước 9 — Xử Lý Rủi Ro Theo Ưu Tiên

Thứ tự xử lý risk nên là:

1. ACL `base.group_user` quá rộng
2. `sudo()` thiếu guard scope 0213
3. portal category ref thiếu `raise_if_not_found=False`
4. `action_view_survey_results` thiếu group check
5. `action_done`, `action_rehire`, `action_blacklist` thiếu backend group check
6. email BHXH thiếu fallback nếu `work_email` rỗng
7. activity plan hard-code `base.main_company`
8. dead code `_compute_owner_related_activity_ids`

### 11.11. Bước 10 — Test Theo Phase

Test theo từng vai trò, không chỉ test happy path:

- Portal employee: tạo đơn, chỉ thấy đơn của mình, chỉ done activity của mình
- Line manager: approve đúng đơn được giao
- HR: xử lý done, gửi mail, deactivate user đúng điều kiện
- OPS hoặc department owner: xem và xử lý activity đúng phạm vi
- User không có quyền: gọi RPC hoặc action trực tiếp phải bị chặn

Kết luận triển khai: đi theo thứ tự `field/data nền → logic approval → portal → security siết chặt → views → cron → test quyền`. Điểm cần cẩn thận nhất là không triển khai máy móc theo tên field trong blueprint nếu source hiện tại đã dùng tên khác.
