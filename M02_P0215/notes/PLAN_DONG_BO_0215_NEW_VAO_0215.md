# PLAN: ĐỒNG BỘ TÍNH NĂNG TỪ `M02_P0215_new` VÀO `M02_P0215`

> Ngày lập: 2026-05-18
> Tài liệu nguồn: `KHAC_BIET_0215_NEW_VS_0215.md` (cùng thư mục)
> Đối tượng thực hiện: **Codex**
> Module đích: `addons/M02_P0215`
> Module nguồn (chỉ đọc, KHÔNG sửa): `addons/M02_P0215_new`

---

## 0. NGUYÊN TẮC BẮT BUỘC CHO CODEX

1. **KHÔNG copy đè nguyên thư mục.** Hai module đã phân nhánh — copy đè sẽ làm
   mất wizard báo cáo, mất `migrations/`, và hạ cấp email template. Chỉ áp dụng
   từng thay đổi theo plan này.
2. **KHÔNG đụng vào** `M02_P0215_new` (chỉ dùng để tham chiếu).
3. **KHÔNG xoá** ở `M02_P0215`: `migrations/`, `scripts/`,
   `wizards/x_psm_hr_discipline_violation_report_wizard.py`,
   `views/x_psm_hr_discipline_violation_report_wizard_views.xml`, và các dòng ACL
   của wizard đó trong `security/ir.model.access.csv`.
4. **KHÔNG hạ `version`** trong `__manifest__.py`. Giữ `19.0.1.0.20`, bump lên
   `19.0.1.0.21`.
5. Mục gắn nhãn `[CẦN XÁC NHẬN]` — DỪNG lại, hỏi người dùng trước khi làm.
6. Sau mỗi Phase: kiểm tra cú pháp Python (`python -m py_compile`) và XML
   (well-formed). Không tự ý chạy `git`.
7. Bám sát quy ước tại `convention/QUY_UOC_DAT_TEN_VA_RULE.md` (prefix `x_psm_`,
   tên model, v.v.).

---

## 1. THỨ TỰ THỰC HIỆN (tổng quan)

| Phase | Nội dung | Phụ thuộc |
|---|---|---|
| 1 | Thêm file mới (model calendar, view approval, 4 file .docx) | — |
| 2 | Cập nhật model `x_psm_hr_discipline_record.py` | — |
| 3 | Cập nhật `x_psm_approval_request.py` + 2 wizard | Phase 2 |
| 4 | Cập nhật `controllers/portal.py` | Phase 2 |
| 5 | Cập nhật security (ACL + rules) | — |
| 6 | Cập nhật views (record / master / portal) | Phase 1–2 |
| 7 | Cập nhật data + SCSS + manifest | Phase 1, 6 |
| 8 | Kiểm thử & nghiệm thu | tất cả |

---

## PHASE 1 — BỔ SUNG FILE MỚI

### Task 1.1 — Model `calendar.event`
- Tạo `addons/M02_P0215/models/x_psm_calendar_event.py`, copy y nguyên nội dung
  từ `M02_P0215_new/models/x_psm_calendar_event.py`.
- Trong `addons/M02_P0215/models/__init__.py`, thêm dòng cuối:
  `from . import x_psm_calendar_event`.

### Task 1.2 — View `approval.request`
- Tạo `addons/M02_P0215/views/x_psm_approval_request_views.xml`, copy y nguyên
  từ `M02_P0215_new/views/x_psm_approval_request_views.xml`.
- View tham chiếu field `x_psm_discipline_record_id` của `approval.request` —
  field này đã được khai báo ở `models/x_psm_approval_request.py` (xác nhận sau
  khi làm Phase 3).

### Task 1.3 — Mẫu .docx
- Tạo thư mục `addons/M02_P0215/static/src/templates/`.
- Copy 4 file (nhị phân, KHÔNG sửa nội dung):
  `mau_bien_ban_xu_ly_ky_luat.docx`, `mau_bien_ban_xu_ly_boi_thuong.docx`,
  `mau_quyet_dinh_xu_ly_ky_luat.docx`, `mau_quyet_dinh_xu_ly_boi_thuong.docx`.

**Nghiệm thu Phase 1:** 6 file/thư mục tồn tại; `models/__init__.py` import được.

---

## PHASE 2 — MODEL `x_psm_hr_discipline_record.py`

> Áp dụng đúng các thay đổi mô tả ở mục 3.2 của `KHAC_BIET_0215_NEW_VS_0215.md`.
> Cách an toàn: dùng `M02_P0215_new/models/x_psm_hr_discipline_record.py` làm
> bản tham chiếu, áp từng cụm thay đổi dưới đây.

### Task 2.1 — Field mới
Thêm: `x_psm_employee_domain` (+ compute `_compute_x_psm_employee_domain`),
`x_psm_portal_needs_attention`, `x_psm_has_ceo_refused` (+ compute),
`x_psm_meeting_attachment_ids`, `x_psm_compensation_minutes_ids`.

### Task 2.2 — Việt hoá nhãn
Đổi `string=` của field và nhãn `state` sang tiếng Việt theo bản `_new`.

### Task 2.3 — Workflow
- `allowed_transitions`: `issued` cho phép thêm `investigation`.
- `_compute_x_psm_suggested_action` → chỉ còn `pass`.
- Thêm `_x_psm_notify_hr_oc_investigation`.
- `action_psm_rgm_company_level` gọi thêm `_x_psm_notify_hr_oc_investigation`.
- Thêm `action_psm_rehear`.
- `action_psm_close_hearing`: kiểm tra biên bản họp/bồi thường với company level.
- `write()`: logic `x_psm_portal_needs_attention`.

### Task 2.4 — Luồng duyệt (Approval)
- Xoá `_x_psm_get_approval_approver_lines`,
  `_x_psm_get_approval_manager_approver_line`,
  `action_psm_open_approval_category_config`.
- Thêm `_x_psm_get_approval_approver_users`, `_x_psm_clear_approval_activities`.
- Viết lại `_x_psm_prepare_approval_request_vals`, `action_psm_submit_for_approval`,
  `action_psm_open_approval_request`, `_x_psm_on_approval_request_approved/refused`,
  `action_psm_ceo_approve`.

### Task 2.5 — Thông báo & Email
- Thay `_x_psm_notify_employee_rejection` → `_x_psm_notify_rejection(type, reason)`.
- Xoá `_x_psm_send_employee_mail_template`, `_x_psm_get_employee_email_to`,
  `_x_psm_notify_improvement_completed`.
- Đổi mọi chỗ gửi mail sang `template.sudo().send_mail(self.id, force_send=True)`.
- `action_psm_expire` bỏ gửi email hoàn tất.
- Tên file PDF quyết định: tiếng Việt + `safe_name`.

> ⚠️ Sau Task 2.5: `action_psm_send_to_employee` và reject wizard không còn
> dùng helper email cũ. Đảm bảo MỌI tham chiếu tới `_x_psm_send_employee_mail_template`
> trong toàn module đã được thay (grep kiểm tra: kết quả phải = 0).

**Nghiệm thu Phase 2:** `py_compile` sạch; grep `_x_psm_send_employee_mail_template`
trên toàn `M02_P0215` = 0 kết quả; grep `action_psm_open_approval_category_config` = 0.

---

## PHASE 3 — `x_psm_approval_request.py` + WIZARD

### Task 3.1 — `models/x_psm_approval_request.py`
Áp theo mục 3.3: bỏ `.sudo()` trong `action_approve/action_refuse`; `action_refuse`
mở reject wizard khi chưa có `ceo_reject_reason`; thêm
`action_psm_open_discipline_record`. Xác nhận field `x_psm_discipline_record_id`
vẫn được khai báo (đừng xoá).

### Task 3.2 — `wizards/x_psm_hr_discipline_reject_wizard.py`
Áp theo mục 3.4: gửi mail trực tiếp; `action_psm_ceo_reject` dùng
`approval_request.with_context(ceo_reject_reason=reason).action_refuse()`;
bỏ `x_psm_action_id: False`.

### Task 3.3 — `wizards/x_psm_hr_discipline_manual_confirm_wizard.py`
Áp theo mục 3.5: bỏ `default=` của `x_psm_start_date`, thêm `default_get`.

**Nghiệm thu Phase 3:** `py_compile` sạch 3 file.

---

## PHASE 4 — `controllers/portal.py`

Áp toàn bộ mục 3.1: phân quyền theo group, `_x_psm_portal_domain(employee, is_manager)`,
override `_prepare_portal_layout_values` (thêm `discipline_needs_action_count`),
đánh dấu đã đọc trong `portal_discipline_view`, bỏ các helper `*_sudo_model`.

**Nghiệm thu Phase 4:** `py_compile` sạch; controller không còn tham chiếu
`_x_psm_record_sudo_model` / `_x_psm_employee_sudo_model`.

---

## PHASE 5 — SECURITY

### Task 5.1 — `security/ir.model.access.csv`
- **THÊM** dòng ACL cho PM, ST, C-Level và đọc `hr.employee`/`hr.department` cho OC
  (theo bản `_new`).
- **ÁP** thay đổi quyền: record HRBP create→0, OC create→1, admin unlink→1;
  explanation admin unlink→1.
- ⚠️ **`[CẦN XÁC NHẬN]`** Bản `_new` đã bỏ 5 dòng ACL `violation_report_wizard`.
  Vì 0215 GIỮ wizard → **GIỮ NGUYÊN 5 dòng ACL đó**. Hỏi người dùng nếu họ thật
  sự muốn gỡ wizard.

### Task 5.2 — `security/security_rules.xml`
Áp mục 4.2: đơn giản hoá rule Portal Own; mở rộng group rule Store Manager;
HRBP/OC domain → `[(1,'=',1)]`; thêm 2 rule C-Level.
⚠️ File rule có `noupdate="1"` — rule **mới** sẽ nạp khi upgrade; rule **sửa nội
dung** sẽ KHÔNG tự cập nhật bản ghi cũ. Cần migration hoặc cập nhật thủ công —
xem Phase 7 Task 7.4.

**Nghiệm thu Phase 5:** XML well-formed; số cột mỗi dòng CSV = 8.

---

## PHASE 6 — VIEWS

### Task 6.1 — `views/x_psm_hr_discipline_record_views.xml`
Áp mục 4.4 cho **form view gốc**: form tiếng Việt; thêm nút `action_psm_rehear`
/ `action_psm_ceo_approve` / `action_psm_open_ceo_reject_wizard`; thêm
`domain="x_psm_employee_domain"`; khối biên bản họp/bồi thường dùng
`many2many_binary` + link tải mẫu `.docx`; bỏ nút approval-category-config;
survey stat button `invisible="1"`.

**GIỮ view kế thừa `view_psm_hr_discipline_record_form_internal_ux`** (theo
quyết định) nhưng **viết lại** cho khớp form mới:
- **XOÁ** mọi `xpath ... position="attributes"` việt-hoá-ngược-sang-tiếng-Anh
  (nhãn nút, nhãn group, nhãn field) — form gốc đã là tiếng Việt, không cần đổi.
- **XOÁ** 2 xpath `position="replace"` cho div alert (chúng dịch ngược sang
  tiếng Anh).
- **GIỮ** xpath thêm khối thẻ tóm tắt `<div class="row g-3 mb-4">` sau
  `//div[@class='oe_title']`; đổi nhãn thẻ ("Employee", "Violation", "Action",
  "Date") sang tiếng Việt cho đồng bộ.
- Kiểm tra mọi xpath còn lại vẫn khớp cấu trúc form gốc MỚI (chạy thử upgrade).

### Task 6.2 — `views/x_psm_hr_discipline_master_views.xml`
Bỏ `groups="hr.group_hr_manager"` trên các menu Configuration.

### Task 6.3 — `views/x_psm_portal_templates.xml`
Áp mục 4.5: badge `discipline_needs_action_count`; thêm 2 cột ngày bắt đầu/kết thúc.

**Nghiệm thu Phase 6:** mọi `name=` của nút trong view trỏ tới method có thật
trong model; XML well-formed.

---

## PHASE 7 — DATA / SCSS / MANIFEST

### Task 7.1 — `data/approval_category_data.xml`
Thêm block `<data>` cho `hr.group_hr_manager` kế thừa `approvals.group_approval_user`.

### Task 7.2 — `data/survey_feedback_data.xml`
Việt hoá tiêu đề/mô tả survey. ⚠️ File `noupdate="1"` → cần migration nếu muốn
áp lên dữ liệu cũ (Task 7.4).

### Task 7.3 — `static/src/scss/portal_psm_0215.scss`
Thêm width cho `.psm-col-start-date` / `.psm-col-end-date` (cần cho 2 cột mới).

### Task 7.4 — `__manifest__.py`
- `version`: `19.0.1.0.20` → `19.0.1.0.21`.
- `data`: **thêm** `views/x_psm_approval_request_views.xml`; **giữ**
  `views/x_psm_hr_discipline_violation_report_wizard_views.xml`.
- `assets`: **GIỮ NGUYÊN** block `web.assets_backend` với
  `internal_discipline_form.scss` (theo quyết định ở Task 7.5).
- Tạo `migrations/19.0.1.0.21/post-migrate.py` nếu cần áp lại `ir.rule` đã sửa
  và data `noupdate` (survey). Nếu không, ghi rõ trong nghiệm thu rằng phải
  cập nhật thủ công sau upgrade.

### Task 7.5 — Email template & view nội bộ (ĐÃ CHỐT)
**Quyết định của người dùng (2026-05-18):**
- **Email template** (`email_template_discipline_done.xml`,
  `email_template_rejection.xml`, `mail_template.xml`): **GIỮ NGUYÊN bản 0215**.
  Codex **KHÔNG sửa** 3 file này, **KHÔNG lấy** bản `_new`.
  Lưu ý: template 0215 đã có sẵn `email_to` nên vẫn hoạt động đúng với cách gửi
  mail trực tiếp `template.sudo().send_mail(...)` ở Phase 2 Task 2.5 — không cần
  chỉnh gì thêm.
- **View `view_psm_hr_discipline_record_form_internal_ux` +
  `internal_discipline_form.scss`**: **GIỮ và VIẾT LẠI** — xem chi tiết ở
  Phase 6 Task 6.1. KHÔNG xoá file SCSS, KHÔNG xoá block `assets_backend`.

---

## PHASE 8 — KIỂM THỬ & NGHIỆM THU

1. `python -m py_compile` toàn bộ `.py` đã sửa — không lỗi.
2. Tất cả XML well-formed.
3. Nâng cấp module trên môi trường test: `-u M02_P0215` không lỗi.
4. Kịch bản nghiệp vụ tối thiểu:
   - Tạo hồ sơ → gửi tường trình → RGM xử lý → company level → họp (tạo
     `calendar.event` → hồ sơ tự sang `hearing`) → kết thúc họp (bắt buộc biên
     bản) → ban hành → trình duyệt → **CEO duyệt** và **CEO từ chối → họp lại**.
   - Portal: nhân viên thấy badge "cần chú ý"; mở hồ sơ → badge tắt.
   - Phân quyền: PM/ST/OC/HRBP/C-Level truy cập đúng phạm vi.
   - Wizard báo cáo vi phạm (của 0215) vẫn chạy bình thường.
5. Đối chiếu lại với `KHAC_BIET_0215_NEW_VS_0215.md` — mọi mục đã xử lý hoặc
   đã ghi lý do bỏ qua.

---

## 9. CHECKLIST RỦI RO

- [ ] Không mất `migrations/`, `scripts/`, wizard báo cáo vi phạm.
- [ ] `version` không bị hạ.
- [ ] Không còn tham chiếu method/helper đã xoá (`_x_psm_send_employee_mail_template`,
      `action_psm_open_approval_category_config`, `_x_psm_get_approval_approver_lines`).
- [ ] Mọi nút trong view trỏ tới method tồn tại.
- [ ] ACL `violation_report_wizard` còn nguyên (trừ khi người dùng yêu cầu gỡ).
- [ ] `ir.rule` sửa nội dung đã có cơ chế áp lại (migration / thủ công).
- [x] Đã chốt 2 mục Task 7.5: GIỮ email template 0215; GIỮ & viết lại view nội bộ.
- [ ] Còn 1 mục `[CẦN XÁC NHẬN]` ở Task 5.1: có gỡ wizard báo cáo vi phạm không
      (mặc định: GIỮ).
- [ ] Bảng nối M2M (`x_psm_hr_discipline_meeting_minutes_rel`,
      `x_psm_hr_discipline_comp_minutes_rel`) tạo đúng khi upgrade.
