# PLAN FIX EMAIL TEMPLATE — MODULE 0213 (2026-05-21)

> Mục tiêu: Sửa lỗi email template module `M02_P0213` để màu nền hiển thị đúng trên **mọi client (Outlook/Gmail) + chatter Odoo**, và sửa lỗi placeholder không render. Plan viết đủ chi tiết để **Haiku** thực thi bằng tool `Edit` (mỗi bước có chuỗi `old` → `new` chính xác).

---

## A. KẾT QUẢ RÀ SOÁT (Root cause)

### Phạm vi
Module thực thi trên server: `addons/M02_P0213`. Các file email template:
- `data/email_template_dept_offboarding_reminder.xml`  (Nhắc nhở bộ phận — ảnh user gửi)
- `data/email_template_offboarding_reminder.xml`        (Nhắc nhở nhân viên)
- `data/email_template_exit_survey.xml`                 (Khảo sát nghỉ việc)
- `data/email_template_adecco_notification.xml`         (Thông báo Adecco)
- `data/email_template_social_insurance.xml`            (BHXH — đơn giản, KHÔNG có lỗi màu)

### LỖI 1 — Màu nền biến mất (lỗi chính user báo)
Header dùng CSS shorthand **`background:linear-gradient(...)` KHÔNG có màu nền đặc dự phòng**, và toàn bộ khối dùng `background:#xxxxxx` (shorthand).

Vì sao **local đúng, server sai**:
1. `mail.template.body_html` sanitize ở chế độ `email_outgoing` → **`sanitize_style=False`** → giữ nguyên gradient. ⇒ **Preview/editor (local) hiển thị đẹp** (`odoo/orm/fields_textual.py:580`).
2. Email gửi SMTP lấy từ `mail.mail.body_html` = `fields.Text` → **KHÔNG sanitize** → gradient được giữ. NHƯNG **Outlook (engine Word) không hỗ trợ `linear-gradient`** ⇒ nền mất ⇒ chữ trắng/vàng trên nền trắng = vô hình (`odoo/addons/mail/models/mail_mail.py:49,351-357`).
3. Bản copy trong **chatter Odoo** = `mail.message.body` có **`sanitize_style=True`** (`mail_message.py:93`). Bộ lọc `_style_whitelist` (`odoo/tools/mail.py:97-110`) **KHÔNG chứa `background` (shorthand)** ⇒ xóa sạch cả `background:linear-gradient` lẫn `background:#xxx` ⇒ header trắng, chữ vô hình (đúng như ảnh bị "bạc màu").

> Tóm lại: local chỉ xem Preview (không sanitize, browser hỗ trợ gradient) nên thấy đẹp; còn email thật + chatter trên server thì nền biến mất.

Thuộc tính KHÁC bị bộ lọc xóa (chỉ ảnh hưởng bản chatter, không ảnh hưởng email thật): `border-left` (shorthand — whitelist chỉ có `border-top`/`border-bottom` + `border-left-style/color/width`), `overflow`, `box-shadow`, `word-break`. → Xử lý ở Phase 3 (tùy chọn).

### LỖI 2 — Placeholder `{{ }}` trong BODY không render
`body_html` render bằng engine **qweb** (`mail_template.py:70`, `render_engine='qweb'`). QWeb **chỉ** nội suy giá trị qua `<t t-out>` / `t-esc` / `t-field` (text) và `t-attf-*` (attribute). **`{{ ... }}` đặt trong text của body sẽ in ra nguyên văn** (đã đối chiếu template chuẩn Odoo `addons/sale/data/mail_template_data.xml`: body dùng `t-out` 50 lần, `{{ }}` chỉ ở `subject` và trong `t-attf-src`).

Bị dính:
- `email_template_dept_offboarding_reminder.xml`: 4 chỗ `{{ object.x_psm_0213_employee_id.* }}` trong body.
- `email_template_offboarding_reminder.xml`: 1 chỗ `{{ object.request_owner_id.name }}` trong body.

> LƯU Ý: `{{ }}` trong `subject`, `email_from`, `email_to`, `lang` là **ĐÚNG** (các field này dùng engine `inline_template`). **KHÔNG được sửa các field đó.**

### Phần ĐÚNG (không sửa)
- `exit_survey` & `adecco`: body đã dùng `<t t-out>` / `<t t-esc>` / `t-att-href` đúng chuẩn.
- `ctx.get('survey_url')` trong exit_survey: hợp lệ — `ctx` có trong context qweb (`mail_render_mixin.py:309`), và `survey_url` được truyền qua `with_context` (`models/resignation_request.py:1203`).
- Logic gửi mail (cron + thủ công) tại `resignation_request.py:1363-1458`: đúng.

---

## B. CHIẾN LƯỢC SỬA (áp dụng cho 4 file có màu)

Cho phần header gradient — thêm **màu nền đặc** + chuyển gradient sang `background-image` (cả 2 đều nằm trong whitelist nên sống sót ở chatter, và `background-color` là fallback cho Outlook):

```
background:linear-gradient(135deg,#b5121b 0%,#da291c 58%,#ffbc0d 100%);
   →
background-color:#b5121b;background-image:linear-gradient(135deg,#b5121b 0%,#da291c 58%,#ffbc0d 100%);
```

Cho mọi nền đặc — đổi shorthand `background:#` thành `background-color:#` (dùng `replace_all`, vì gradient dùng `background:linear-gradient` nên KHÔNG bị dính):

```
background:#   →   background-color:#
```

---

## PHASE 1 — Fix màu nền (BẮT BUỘC, ưu tiên cao nhất)

Làm tuần tự cho 4 file. Mỗi file gồm **2 thao tác Edit**.

### 1.1 — `data/email_template_dept_offboarding_reminder.xml`
**Edit #1 (header gradient):**
- old: `<td style="padding:0;background:linear-gradient(135deg,#b5121b 0%,#da291c 58%,#ffbc0d 100%);">`
- new: `<td style="padding:0;background-color:#b5121b;background-image:linear-gradient(135deg,#b5121b 0%,#da291c 58%,#ffbc0d 100%);">`

**Edit #2 (nền đặc — dùng `replace_all: true`):**
- old: `background:#`
- new: `background-color:#`

### 1.2 — `data/email_template_offboarding_reminder.xml`
Y hệt 1.1: Edit #1 (header gradient, chuỗi giống hệt) + Edit #2 (`background:#` → `background-color:#`, `replace_all: true`).

### 1.3 — `data/email_template_exit_survey.xml`
Y hệt: Edit #1 (header gradient) + Edit #2 (`replace_all`). Edit #2 cũng tự sửa nút bấm `background:#da291c` (dòng nút "Bắt đầu khảo sát") thành `background-color:#da291c`.

### 1.4 — `data/email_template_adecco_notification.xml`
Y hệt: Edit #1 (header gradient) + Edit #2 (`replace_all`).

> **Kiểm tra nhanh sau Phase 1:** `grep -n "background:" addons/M02_P0213/data/email_template_*.xml` — kết quả mong đợi: KHÔNG còn dòng nào (mọi `background:` đã thành `background-color:` hoặc `background-image:`). Nếu còn → sửa nốt.

---

## PHASE 2 — Fix placeholder `{{ }}` trong body (BẮT BUỘC)

### 2.1 — `data/email_template_dept_offboarding_reminder.xml`

**Edit #1** (câu mở đầu, dòng ~31):
- old:
  `Bạn đang có nhiệm vụ trong quy trình nghỉ việc của nhân viên <strong>{{ object.x_psm_0213_employee_id.name }}</strong> (Mã NV: {{ object.x_psm_0213_employee_id.barcode or 'N/A' }}) hiện đang bị trễ hạn xử lý.`
- new:
  `Bạn đang có nhiệm vụ trong quy trình nghỉ việc của nhân viên <strong><t t-out="object.x_psm_0213_employee_id.name"/></strong> (Mã NV: <t t-out="object.x_psm_0213_employee_id.barcode or 'N/A'"/>) hiện đang bị trễ hạn xử lý.`

**Edit #2** (ô bảng "Nhân viên", dòng ~43):
- old:
  `<td style="padding:0 0 10px 0;font-size:14px;color:#221f1c;font-weight:700;">{{ object.x_psm_0213_employee_id.name }}</td>`
- new:
  `<td style="padding:0 0 10px 0;font-size:14px;color:#221f1c;font-weight:700;"><t t-out="object.x_psm_0213_employee_id.name"/></td>`

**Edit #3** (ô bảng "Mã nhân viên", dòng ~47):
- old:
  `<td style="padding:0;font-size:14px;color:#221f1c;font-weight:600;">{{ object.x_psm_0213_employee_id.barcode or 'N/A' }}</td>`
- new:
  `<td style="padding:0;font-size:14px;color:#221f1c;font-weight:600;"><t t-out="object.x_psm_0213_employee_id.barcode or 'N/A'"/></td>`

> KHÔNG sửa dòng `<field name="subject">...{{ object.x_psm_0213_employee_id.name }}</field>` — subject dùng `{{ }}` là đúng.

### 2.2 — `data/email_template_offboarding_reminder.xml`

**Edit #1** (dòng ~31):
- old:
  `<p style="margin:0 0 16px 0;font-size:15px;line-height:1.7;">Kính gửi <strong>{{ object.request_owner_id.name }}</strong>,</p>`
- new:
  `<p style="margin:0 0 16px 0;font-size:15px;line-height:1.7;">Kính gửi <strong><t t-out="object.request_owner_id.name"/></strong>,</p>`

> **Kiểm tra nhanh sau Phase 2:** `grep -n "{{" addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml addons/M02_P0213/data/email_template_offboarding_reminder.xml` — chỉ còn `{{ }}` ở các field `subject` / `email_from` / `email_to` / `lang`. Trong `body_html` KHÔNG còn `{{`.

---

## PHASE 3 — Robust hóa & chuẩn hóa (TÙY CHỌN, nên làm)

Mục tiêu: bản hiển thị trong chatter Odoo cũng giữ được viền nhấn + đồng bộ template.

### 3.1 — Đổi `border-left` shorthand sang sub-property (sống sót sanitizer chatter)
Áp dụng cho 4 file (dept ~57, offboarding ~45, exit_survey ~60, adecco ~62). Dùng `replace_all: true` mỗi file:
- old: `border-left:4px solid #da291c;`
- new: `border-left-width:4px;border-left-style:solid;border-left-color:#da291c;`

### 3.2 — Bổ sung `lang` + `auto_delete` cho dept template (đồng bộ với template nhân viên)
Trong `email_template_dept_offboarding_reminder.xml`, ngay trước `</record>` thêm:
```xml
            <field name="lang">{{ object.request_owner_id.lang }}</field>
            <field name="auto_delete">True</field>
```

### 3.3 — (Tùy chọn) Chuẩn hóa `t-esc` → `t-out` trong `exit_survey` (2 chỗ) để đồng bộ phong cách. Không bắt buộc (t-esc vẫn chạy).

### 3.4 — (Tùy chọn) Đồng bộ snapshot `for_github/M02_P0213_00/data/*` nếu repo đó còn dùng. Lưu ý snapshot này KHÔNG có file dept reminder.

---

## PHASE 4 — Triển khai & kiểm thử

1. Nâng cấp module (data có `noupdate="0"` nên template sẽ được cập nhật khi upgrade):
   - Dùng `upgrade_m02_p0213.ps1` (ở thư mục gốc repo) hoặc `-u M02_P0213`.
   - Vì các record nằm trong `<data noupdate="0">` → upgrade sẽ ghi đè body_html. Nếu trên server template ĐÃ bị sửa tay (UI), `noupdate="0"` vẫn ghi đè → OK cho mục đích này.
2. Kiểm thử từng template — gửi thử và xem **2 nơi**:
   - **Inbox thật** (ưu tiên test Outlook + Gmail): header có nền đỏ (Outlook) hoặc gradient (Gmail), chữ trắng đọc được.
   - **Chatter Odoo**: header có màu (gradient/đỏ), không còn "bạc màu".
3. Checklist từng template:
   - [ ] dept reminder: màu OK + tên/Mã NV hiện đúng (không còn `{{ }}`).
   - [ ] offboarding reminder (nhân viên): màu OK + tên hiện đúng.
   - [ ] exit survey: màu OK + nút "Bắt đầu khảo sát" có nền đỏ + link đúng.
   - [ ] adecco: màu OK + thông tin nhân viên đúng.
   - [ ] social insurance: không đổi (sanity check vẫn gửi được).

---

## C. TÓM TẮT THỨ TỰ THỰC THI CHO HAIKU
1. Phase 1 (4 file × 2 edit) → grep kiểm tra hết `background:`.
2. Phase 2 (dept 3 edit, offboarding 1 edit) → grep kiểm tra hết `{{` trong body.
3. Phase 3 (tùy chọn) nếu có thời gian.
4. Báo lại danh sách file đã đổi; KHÔNG tự upgrade/gửi mail (để user chạy Phase 4).
