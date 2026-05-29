# Phase 4 Review Quyen Va Workflow 0214

Ngay lap: 2026-05-14

## 1. Pham vi

Phase 4 theo `RA_SOAT_VA_PLAN_UI_0214_TU_0213_20250514.md` la phase kiem tra:

- group / invisible tren view
- route va field portal sau Phase 3 / 3.5
- workflow Submit -> Pending -> Approved -> Done
- khong sua controller, model, route, group hien huu trong phase nay

## 2. Tai lieu va source da dung

Convention:

- `addons/M02_P0214/convention/QUY_UOC_DAT_TEN_VA_RULE.md`

JSON map:

- `addons/M02_P0214/structure/module_map.json`

Source chinh:

- `addons/M02_P0214/views/resignation_request_views.xml`
- `addons/M02_P0214/views/resignation_portal_template.xml`
- `addons/M02_P0214/views/offboarding_report_views.xml`
- `addons/M02_P0214/views/config_menu_views.xml`
- `addons/M02_P0214/security/ir.model.access.csv`
- `addons/M02_P0214/security/offboarding_request_rules.xml`
- `addons/M02_P0214/security/security.xml`
- `addons/M02_P0214/controllers/main.py`
- `addons/M02_P0214/models/approval_request_rst_fields.py`
- `addons/M02_P0214/models/approval_request_rst_approval.py`
- `addons/M02_P0214/models/approval_request_rst_survey.py`
- `addons/M02_P0214/models/approval_request_rst_offboarding.py`
- `addons/M02_P0214/models/mail_activity.py`
- `addons/M02_P0214/models/survey_user_input.py`

## 3. Ket qua static review

### 3.1. View visibility / group

Da xac nhan cac action backend hien huu co group va invisible:

- `action_send_social_insurance`
- `action_done`
- `action_view_my_activities`
- `action_view_survey_results`
- `action_pending_offboarding_subordinates`

Menu co group:

- `menu_psm_0214_offboarding_settings`
- `menu_psm_rst_reports`
- `menu_psm_pending_offboarding_activities`
- `menu_psm_resignation_type_config`

Khong phat hien viec Phase 3 / 3.5 lam thay doi group / invisible.

### 3.2. Portal route / field

Da xac nhan route va field quan trong con giu nguyen:

- `/my/resignation/rst`
- `/my/resignation/rst/submit`
- `/my/resignation/rst/activity/done`
- `csrf_token`
- `activity_id`
- `approver_user_id`
- `x_psm_0214_resignation_date`
- `x_psm_0214_resignation_reason_id`
- `x_psm_0214_resignation_reason`

### 3.3. Workflow static

Static path hien tai:

1. Portal submit tao `approval.request` bang `sudo()`, gan `request_owner_id`, category 0214, employee, reason, date.
2. Neu employee co line manager user thi tao approver line.
3. `action_confirm()` set status `pending`.
4. Line manager approve qua approval flow.
5. `action_approve()` gui exit survey va launch offboarding activity plan.
6. Portal user chi mark done activity neu activity thuoc request cua chinh minh va activity duoc giao cho chinh user.
7. `action_done()` bi chan neu chua hoan thanh survey, activities, va chua gui BHXH.

## 4. Findings can quyet dinh truoc khi sua code

### F1. `GDH_RST_HR_ADMIN_S` dang duoc phep gui Social Insurance / Adecco

Muc do: Medium

Source:

- `views/resignation_request_views.xml`: button `action_send_social_insurance` co group `GDH_RST_HR_ADMIN_S`
- `models/approval_request_rst_fields.py`: `_GROUP_0214_HR_PROCESS` co `GDH_RST_HR_ADMIN_S`
- `models/approval_request_rst_survey.py`: `action_send_social_insurance()` va `action_send_adecco_notification()` dung `_GROUP_0214_HR_PROCESS`

Doi chieu expected:

- `PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0214.md` muc 9.1 ghi `GDH_RST_HR_ADMIN_S` gan read-only.
- Muc 8.3 / 8.4 yeu cau action nhay cam chi cho nhom HR xu ly / quan ly cao hon.

Nhan dinh:

- Neu `GDH_RST_HR_ADMIN_S` la staff read-only dung nghia, day la mismatch.
- Phase 4 khong sua group, nen chua remove group trong code.

De xuat cho phase sau:

- Neu business xac nhan `GDH_RST_HR_ADMIN_S` khong duoc xu ly email, remove group nay khoi `_GROUP_0214_HR_PROCESS` va view button `action_send_social_insurance`.

### F2. POST `/my/resignation/rst/submit` chua guard eligibility RST

Muc do: High

Source:

- `controllers/main.py`: `portal_resignation_submit()` lay employee va category, sau do `sudo().create(vals)`; chua thay guard `_is_rst_portal_employee(employee)` truoc khi create.
- `portal_resignation_unified()` co redirect OPS/RST, nhung direct POST vao `/my/resignation/rst/submit` van can server-side guard.

Doi chieu expected:

- Phase 0 muc 5.1 / 10.4 yeu cau portal chi dung du lieu cua chinh owner va dung scope 0214.
- Convention 0214 yeu cau khong doi route / field, nhung khong cam them guard server-side.

Nhan dinh:

- Day la risk workflow/security thuc te, khong phai UI.
- Phase 4 theo plan la review, khong sua controller, nen chua patch.

De xuat cho phase sau:

- Them guard trong GET `/my/resignation/rst` va POST `/my/resignation/rst/submit`:
  - neu khong co employee hoac employee khong thuoc RST portal scope thi redirect `/my/resignation/ops` hoac return forbidden tuy business.

### F3. Survey portal record rule van dua tren partner/email

Muc do: Medium

Source:

- `security/security.xml`: rule `rule_psm_0214_survey_user_input_portal_own` dung domain `partner_id = user.partner_id.id OR email = user.email`.
- `models/approval_request_rst_fields.py` da co link `x_psm_0214_exit_survey_user_input_id`, nhung record rule portal chua bind truc tiep voi request.

Doi chieu expected:

- Phase 0 muc 10.3 yeu cau survey phai gan chat vao request, khong chi search rong theo partner/email neu chua kiem tra request.

Nhan dinh:

- Helper code da co matching theo survey + partner/email + request khi build link.
- Record rule van rong theo partner/email. Can runtime test de xac dinh co leak cross-request hay khong.

De xuat cho phase sau:

- Neu can sieu chat, bo sung field lien ket request tren survey user input hoac rule domain dua vao request linked.

## 5. Test da chay

- XML parse `views/resignation_portal_template.xml`: OK
- Python manifest parse `__manifest__.py`: OK
- JS syntax `portal_resignation_0214.js`: OK
- Static grep route / field portal: OK
- Static grep group / invisible / menu: OK

## 6. Ket luan Phase 4

Phase 4 da hoan thanh o muc static review.

Khong co thay doi code trong phase nay vi plan quy dinh review-only cho group / invisible / workflow.

Can runtime test bang user that theo matrix:

- portal eligible RST employee
- portal non-RST employee
- line manager
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

