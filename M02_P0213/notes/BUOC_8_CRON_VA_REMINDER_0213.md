# Buoc 8 - Cron Va Reminder 0213

Ngay thuc hien: 2026-05-13

## 1. Tai lieu dinh huong da dung

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Buoc 6: `addons/M02_P0213/notes/BUOC_6_SECURITY_VA_QUYEN_0213.md`
- Buoc 7: `addons/M02_P0213/notes/BUOC_7_VIEWS_BACKEND_VA_PORTAL_TEMPLATE_0213.md`

## 2. Source chinh dung de xac nhan

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/res_company.py`
- `addons/M02_P0213/data/ir_cron_data.xml`
- `addons/M02_P0213/data/email_template_offboarding_reminder.xml`
- `addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml`
- `addons/M02_P0213/data/offboarding_activity_plan_data.xml`

## 3. Thay doi logic reminder

File sua:

- `addons/M02_P0213/models/resignation_request.py`

Dieu chinh:

- Them `_get_0213_activity_template_summaries()` de lay summary cua cac template trong `psm_0213_offboarding_activity_plan`.
- Them `_filter_0213_offboarding_activities()` de chi giu activity thuoc flow 0213:
  - activity gan truc tiep `approval.request` hien tai
  - hoac activity gan `hr.employee` co summary nam trong activity plan 0213
- Ap dung filter nay cho:
  - `_get_overdue_activities_by_request()`
  - `action_manual_reminder_extension()`
- Khi gui reminder cho employee owner, truyen `email_values={'email_to': email_to}` de dung fallback `user.email` neu partner email rong.
- Chi gia han deadline khi `x_psm_0213_reminder_extension_days > 0`.

## 4. Ly do

Truoc do cron/manual reminder co the quet ca activity qua han gan tren `hr.employee` cua nhan vien nghi viec. Neu nhan vien co activity HR khac khong thuoc offboarding, he thong co the gui nhac va gia han nham.

Sau thay doi, reminder van ho tro ca hai kieu gan activity (`approval.request` va `hr.employee`), nhung pham vi duoc khoa chat hon theo request hien tai va activity plan 0213.

## 5. Verification

- Da parse XML:
  - `data/ir_cron_data.xml`
  - `data/email_template_offboarding_reminder.xml`
  - `data/email_template_dept_offboarding_reminder.xml`
  - `data/offboarding_activity_plan_data.xml`
- Da chay `python -m py_compile` cho `models/resignation_request.py`.
- Da regenerate `structure/module_map.json`, stats va details.
- Chua chay manual call cron trong Odoo shell va chua test gui email thuc te.
