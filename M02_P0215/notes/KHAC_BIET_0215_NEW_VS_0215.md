# SO SÁNH KHÁC BIỆT: `M02_P0215_new` so với `M02_P0215`

> Ngày lập: 2026-05-18
> Nguồn (source): `addons/M02_P0215_new`
> Đích (target): `addons/M02_P0215` (module 0215 hiện tại đang chạy)
> Mục đích: ghi nhận toàn bộ điểm khác biệt để làm cơ sở cho plan đồng bộ
> (xem `PLAN_DONG_BO_0215_NEW_VAO_0215.md`).

---

## 0. CẢNH BÁO QUAN TRỌNG — HAI MODULE ĐÃ PHÂN NHÁNH (DIVERGED)

`M02_P0215_new` **không phải** là phiên bản mới hơn hoàn toàn của `M02_P0215`.
Hai bên đã phát triển song song và mỗi bên có phần riêng:

- `M02_P0215_new` có thêm **tính năng nghiệp vụ mới** (phân quyền theo group,
  luồng CEO duyệt/từ chối, tự động chuyển trạng thái theo lịch họp, cờ "cần
  chú ý" trên Portal, biên bản họp nhiều file, mẫu .docx...).
- `M02_P0215` (hiện tại) lại có phần mà `M02_P0215_new` **KHÔNG có**:
  - Wizard báo cáo vi phạm (`x_psm_hr_discipline_violation_report_wizard`)
  - Thư mục `migrations/` (19.0.1.0.1 / .2 / .4)
  - Thư mục `scripts/`
  - `static/src/scss/internal_discipline_form.scss`
  - **Bộ email template HTML có thương hiệu, mới hơn** (sửa ngày 2026-05-18).
    Bản trong `M02_P0215_new` là HTML thô, cũ hơn (2026-05-12/14).

➡️ **Hệ quả:** KHÔNG được copy đè nguyên thư mục `M02_P0215_new` lên
`M02_P0215`. Phải đồng bộ **có chọn lọc** theo plan. Các mục xung đột/thoái lui
được đánh dấu `[GIỮ 0215]` hoặc `[CẦN XÁC NHẬN]` ở dưới.

---

## 1. KHÁC BIỆT VỀ FILE (cấu trúc thư mục)

### 1.1. Chỉ có trong `M02_P0215_new` → cần BỔ SUNG vào 0215

| File | Vai trò |
|---|---|
| `models/x_psm_calendar_event.py` | Kế thừa `calendar.event`: khi tạo/sửa cuộc họp gắn với hồ sơ kỷ luật ở trạng thái `investigation` → tự động chuyển hồ sơ sang `hearing`. |
| `views/x_psm_approval_request_views.xml` | Kế thừa form `approval.request`: thêm nút stat "Hồ sơ KL" mở hồ sơ kỷ luật liên kết; thêm field ẩn `x_psm_discipline_record_id`. |
| `static/src/templates/mau_bien_ban_xu_ly_ky_luat.docx` | Mẫu biên bản xử lý kỷ luật (file tải về cho người dùng). |
| `static/src/templates/mau_bien_ban_xu_ly_boi_thuong.docx` | Mẫu biên bản xử lý bồi thường. |
| `static/src/templates/mau_quyet_dinh_xu_ly_ky_luat.docx` | Mẫu quyết định xử lý kỷ luật. |
| `static/src/templates/mau_quyet_dinh_xu_ly_boi_thuong.docx` | Mẫu quyết định xử lý bồi thường. |

### 1.2. Chỉ có trong `M02_P0215` → `[GIỮ 0215]` — KHÔNG xoá

| File / thư mục | Ghi chú |
|---|---|
| `wizards/x_psm_hr_discipline_violation_report_wizard.py` | Wizard báo cáo số người vi phạm. Giữ lại. |
| `views/x_psm_hr_discipline_violation_report_wizard_views.xml` | View của wizard trên. Giữ lại. |
| `migrations/19.0.1.0.1|.2|.4/post-migrate.py` | Script migration đã chạy. **Tuyệt đối giữ.** |
| `scripts/` | Script tiện ích. Giữ lại. |
| `static/src/scss/internal_discipline_form.scss` | SCSS cho form nội bộ (xem mục 4.10). |
| `notes/PHASE_H...`, `PLAN_BAO_CAO...`, `PLAN_CAU_HINH...`, `daily_report_..._ra_soat_lai.md` | Tài liệu nội bộ, không ảnh hưởng. |

---

## 2. `__manifest__.py`

| Mục | `M02_P0215` (đích) | `M02_P0215_new` (nguồn) | Quyết định |
|---|---|---|---|
| `version` | `19.0.1.0.20` | `19.0.1` | **GIỮ 0215** và bump tiếp (vd `19.0.1.0.21`). KHÔNG hạ version. |
| `data` | có `views/x_psm_hr_discipline_violation_report_wizard_views.xml` | thay bằng `views/x_psm_approval_request_views.xml` | **BỔ SUNG** dòng approval view; **GIỮ** dòng violation report wizard. |
| `assets.web.assets_backend` | có `internal_discipline_form.scss` | đã bỏ block `assets_backend` | Xem mục 4.10 — phụ thuộc việc có giữ view nội bộ hay không. |

---

## 3. KHÁC BIỆT VỀ MODEL / CONTROLLER (nghiệp vụ — ưu tiên cao)

### 3.1. `controllers/portal.py`
- Bỏ helper `_x_psm_employee_sudo_model` / `_x_psm_record_sudo_model`; bỏ hầu hết
  `.sudo()` (chuyển sang dựa vào `ir.rule` + ACL).
- Bỏ `try/except AccessError` khi tìm nhân viên.
- `_x_psm_get_subordinates`: phân quyền theo group `M02_P0200`:
  - `GDH_RST_OPS_OC_S` → toàn bộ nhân viên thuộc khối `block_code = 'OPS'`.
  - `GDH_RST_HR_HRBP_S` / `GDH_RST_SYSTEM_ST_M` → toàn bộ nhân viên.
  - Còn lại (quản lý cửa hàng) → nhân viên cùng `department_id`.
- `_x_psm_is_manager_employee`: xác định quản lý qua danh sách group quản lý
  (`GDH_OPS_STORE_SM_M/RGM_M/PM_M/ST_M`, `GDH_RST_OPS_OC_S`, `GDH_RST_SYSTEM_ST_M`),
  fallback `employee.child_ids`.
- `_x_psm_portal_domain(employee, is_manager=False)`: thêm tham số `is_manager`;
  OC chỉ thấy hồ sơ khối OPS; HRBP/SYSTEM thấy tất cả; quản lý thấy của mình +
  cấp dưới; nhân viên thường chỉ thấy hồ sơ của chính mình.
- **Mới:** override `_prepare_portal_layout_values` → thêm `discipline_needs_action_count`
  (đếm hồ sơ của nhân viên có `x_psm_portal_needs_attention = True`).
- `portal_discipline_view`: khi nhân viên (chủ thể) xem hồ sơ của mình →
  tự động set `x_psm_portal_needs_attention = False` (đánh dấu đã đọc).

### 3.2. `models/x_psm_hr_discipline_record.py`
**Field mới:**
- `x_psm_employee_domain` (Char, compute) — domain động giới hạn chọn
  nhân viên/người làm chứng (OC → khối OPS; còn lại → theo phòng ban của ĐD).
- `x_psm_portal_needs_attention` (Boolean, default `True`, `copy=False`).
- `x_psm_has_ceo_refused` (Boolean, compute) — có ≥1 `approval.request` bị `refused`.
- `x_psm_meeting_attachment_ids` (M2M `ir.attachment`, bảng nối
  `x_psm_hr_discipline_meeting_minutes_rel`) — biên bản họp kỷ luật (nhiều file).
- `x_psm_compensation_minutes_ids` (M2M `ir.attachment`, bảng nối
  `x_psm_hr_discipline_comp_minutes_rel`) — biên bản bồi thường (nhiều file).

**Thay đổi logic:**
- Toàn bộ `string=` của field và nhãn `state` → tiếng Việt.
- `allowed_transitions`: trạng thái `issued` được phép quay lại `investigation`
  (phục vụ luồng "Cần họp lại").
- `_compute_x_psm_suggested_action`: bỏ hết logic gợi ý → chỉ `pass`
  (RGM chọn hình thức thủ công ở stage `proposal`).
- Hàm gom partner thông báo họp: bổ sung user thuộc group HRBP + OC.
- `action_psm_rgm_company_level`: gọi thêm `_x_psm_notify_hr_oc_investigation`.
- **Mới** `_x_psm_notify_hr_oc_investigation`: tạo activity cho user HRBP/OC.
- **Mới** `action_psm_rehear`: CEO từ chối + hồ sơ company level → quay về
  `investigation` để họp lại.
- `action_psm_close_hearing`: với company level, bắt buộc đã tải lên biên bản
  họp (và biên bản bồi thường nếu có bồi thường) trước khi kết thúc họp.
- **Tái cấu trúc luồng duyệt:**
  - Bỏ `_x_psm_get_approval_approver_lines` và `_x_psm_get_approval_manager_approver_line`.
  - Thêm `_x_psm_get_approval_approver_users` → lấy user nhóm `hr.group_hr_manager`.
  - `_x_psm_prepare_approval_request_vals`: lý do tiếng Việt; tên request động
    "Phê duyệt lại kỷ luật ... (Lần N)" khi đã có request trước đó.
  - `action_psm_submit_for_approval`: viết lại — tạo approval request, thêm
    approver là HR manager, tạo activity nhắc duyệt.
  - **Mới** `_x_psm_clear_approval_activities` — dọn activity sau khi duyệt xong.
  - `action_psm_open_approval_request`: nếu có nhiều approval → mở list lịch sử.
  - **Bỏ** `action_psm_open_approval_category_config`.
- **Thông báo từ chối:** thay `_x_psm_notify_employee_rejection` bằng
  `_x_psm_notify_rejection(rejection_type, reason)` — luôn báo RGM (theo phòng ban),
  company level báo thêm HRBP + OC; phân biệt CEO từ chối / nhân viên từ chối.
- **Email:** bỏ helper `_x_psm_send_employee_mail_template` và
  `_x_psm_get_employee_email_to`; gọi trực tiếp `template.sudo().send_mail(...)`.
- Bỏ `_x_psm_notify_improvement_completed`; `action_psm_expire` không còn gửi
  email hoàn tất cải thiện.
- Tên file PDF quyết định → tiếng Việt, dùng `safe_name` (thay `/` bằng `_`).
- `write()`: thêm logic `x_psm_portal_needs_attention` (chuyển `notified` → `True`,
  `active`/`cancel` → `False`).
- `action_psm_ceo_approve`: gọi thẳng `x_psm_approval_request_id.action_approve()`.

### 3.3. `models/x_psm_approval_request.py`
- `action_approve` / `action_refuse`: bỏ `.sudo()`, thao tác trực tiếp trên `self`.
- `action_refuse`: nếu 1 record gắn hồ sơ kỷ luật và chưa có context
  `ceo_reject_reason` → mở wizard `x_psm.hr.discipline.reject.wizard`
  (mode `ceo_reject`) thay vì từ chối ngay.
- **Mới** `action_psm_open_discipline_record` — action cho nút stat mở hồ sơ kỷ luật.

### 3.4. `wizards/x_psm_hr_discipline_reject_wizard.py`
- Gửi email qua `template.sudo().with_context(...).send_mail(...)` thay helper cũ.
- `action_psm_ceo_reject`: gọi
  `x_psm_approval_request_id.with_context(ceo_reject_reason=reason).action_refuse()`.
- Bỏ `x_psm_action_id: False` khi ghi ở trạng thái `issued`.
- Một số chuỗi → tiếng Việt.

### 3.5. `wizards/x_psm_hr_discipline_manual_confirm_wizard.py`
- Bỏ `default=fields.Date.context_today` cho `x_psm_start_date`.
- **Mới** `default_get`: lấy ngày bắt đầu từ
  `record._x_psm_resolve_effective_start_date()`.

---

## 4. KHÁC BIỆT VỀ SECURITY / VIEW / DATA / ASSET

### 4.1. `security/ir.model.access.csv`
- **Thêm** quyền cho group PM (`GDH_OPS_STORE_PM_M`) và ST (`GDH_OPS_STORE_ST_M`)
  trên 5 model + reject wizard.
- **Thêm** quyền cho C-Level (`GDH_RST_MGMT_MANAGER_M`).
- **Thêm** quyền đọc `hr.employee` và `hr.department` cho OC.
- Đổi quyền: record HRBP `create` 1→0; record OC `create` 0→1;
  record/explanation admin `unlink` 0→1.
- **Bỏ** các dòng ACL của `violation_report_wizard` → `[CẦN XÁC NHẬN]`:
  vì 0215 vẫn giữ wizard nên KHÔNG được bỏ các dòng này.

### 4.2. `security/security_rules.xml`
- Rule "Portal Own" (record + explanation): bỏ nhánh
  `user_id = False AND work_email in [...]` → còn OR đơn giản.
- Rule Store Manager: mở rộng `groups` thêm PM + ST.
- Rule HRBP và OC: domain `company_ids` → `[(1, '=', 1)]` (thấy tất cả).
- **Thêm** rule mới: `rule_psm_hr_discipline_record_clevel` và
  `rule_psm_hr_discipline_explanation_clevel` cho group C-Level.

### 4.3. `views/x_psm_hr_discipline_master_views.xml`
- Bỏ `groups="hr.group_hr_manager"` trên các menu Configuration
  (quyền truy cập giờ do ACL quyết định).

### 4.4. `views/x_psm_hr_discipline_record_views.xml`
- Form view gốc viết thẳng bằng tiếng Việt.
- **Bỏ** view kế thừa `view_psm_hr_discipline_record_form_internal_ux`
  (việt hoá nhãn nút + khối thẻ tóm tắt) — xem mục 4.10.
- **Nút mới:** `action_psm_rehear` ("Cần họp lại"),
  `action_psm_ceo_approve` ("CEO Phê duyệt"),
  `action_psm_open_ceo_reject_wizard` ("CEO Từ chối").
  (Cả hai module đều đã có method tương ứng → an toàn.)
- Nút bước Draft bỏ ràng buộc `groups`.
- `action_psm_submit_for_approval`: mở rộng group (RGM, HRBP, OC).
- `action_psm_issue_decision`: chỉ còn group RGM.
- `action_psm_cancel` và `action_psm_migrate_legacy_bridge` → `invisible="1"`.
- **Bỏ** nút stat `action_psm_open_approval_category_config`.
- Hai nút stat survey (explanation/feedback) → `invisible="1"`.
- Field `x_psm_employee_id` và `x_psm_witness_id` thêm `domain="x_psm_employee_domain"`.
- `x_psm_action_id`: `required` chỉ khi `state == 'issued'` (trước là `('proposal','issued')`).
- Khối "Biên bản họp & Quyết định" làm lại: dùng `widget="many2many_binary"` cho
  `x_psm_meeting_attachment_ids` / `x_psm_compensation_minutes_ids`, kèm link
  "Tải mẫu" trỏ tới file `.docx` trong `static/src/templates/`.
- Bỏ các nút "Generate Decision" (PDF tự sinh) → thay bằng upload binary thủ công.
- Bỏ alert "Configure approvers in Approvals > ...".

### 4.5. `views/x_psm_portal_templates.xml`
- Badge thông báo dùng `discipline_needs_action_count` thay `discipline_count`.
- Bảng danh sách Portal thêm 2 cột: "Ngày bắt đầu", "Ngày kết thúc".
- Việt hoá + reformat khoảng trắng.

### 4.6. `data/approval_category_data.xml`
- Thêm block `<data>`: cho `hr.group_hr_manager` kế thừa
  `approvals.group_approval_user` (để HR manager dùng được Approvals).

### 4.7. `data/survey_feedback_data.xml`
- Tiêu đề/mô tả survey → tiếng Việt. (Lưu ý: `noupdate="1"`.)

### 4.8. `data/email_template_discipline_done.xml`, `email_template_rejection.xml`, `mail_template.xml`
- Bản trong `M02_P0215_new` là **HTML thô, cũ hơn**; bản trong `M02_P0215` là
  HTML có thương hiệu, **mới hơn (sửa 2026-05-18)**.
- `M02_P0215_new` bỏ field `partner_to` / `use_default_to`.
- **✅ ĐÃ CHỐT (2026-05-18): GIỮ NGUYÊN template của `M02_P0215`.** Không lấy bản
  `_new`, không hạ cấp giao diện email.

### 4.9. `static/src/scss/portal_psm_0215.scss`
- Thêm width cho cột `.psm-col-start-date` / `.psm-col-end-date`; chỉnh nhẹ vài
  width khác. Cần lấy để khớp 2 cột mới ở mục 4.5.

### 4.10. `static/src/scss/internal_discipline_form.scss` + view nội bộ
- `M02_P0215_new` đã **bỏ** cả view `..._internal_ux` lẫn SCSS này và block
  `assets_backend`.
- **✅ ĐÃ CHỐT (2026-05-18): GIỮ view nội bộ + SCSS + block `assets_backend`,
  nhưng VIẾT LẠI** view kế thừa cho khớp form gốc mới (giữ thẻ tóm tắt, bỏ các
  xpath việt-hoá-ngược-sang-tiếng-Anh). Chi tiết ở Plan — Phase 6 Task 6.1.

---

## 5. KHÁC BIỆT KHÔNG ẢNH HƯỞNG NGHIỆP VỤ (cosmetic)
- Rất nhiều thay đổi chỉ là **xuống dòng thuộc tính XML / line-ending (CRLF↔LF)** —
  không thay đổi hành vi, có thể bỏ qua hoặc gộp một lần khi chạy formatter.
- File `structure/**` là metadata sinh tự động — sẽ tự cập nhật, không cần sửa tay.

---

## 6. ĐIỀU KIỆN TIỀN ĐỀ (đã kiểm tra — ĐẠT)
- Tất cả group `M02_P0200` mà `0215_new` tham chiếu đều tồn tại:
  `GDH_OPS_STORE_SM_M/RGM_M/PM_M/ST_M`, `GDH_RST_HR_HRBP_S`, `GDH_RST_OPS_OC_S`,
  `GDH_RST_SYSTEM_ST_M`, `GDH_RST_MGMT_MANAGER_M`.
- Field `block_code` trên `hr.department` tồn tại (`M02_P0200/models/hr_department_ext.py`).
- Method `action_psm_ceo_approve`, `action_psm_open_ceo_reject_wizard`,
  `action_psm_cancel`, `_x_psm_resolve_effective_start_date` đã có ở **cả hai** module.
