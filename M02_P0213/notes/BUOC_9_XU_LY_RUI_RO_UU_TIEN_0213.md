# Buoc 9 - Xu Ly Rui Ro Uu Tien 0213

Ngay thuc hien: 2026-05-13

## 1. Tai lieu dinh huong da dung

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Buoc 6: `addons/M02_P0213/notes/BUOC_6_SECURITY_VA_QUYEN_0213.md`
- Buoc 8: `addons/M02_P0213/notes/BUOC_8_CRON_VA_REMINDER_0213.md`

## 2. Source chinh dung de xac nhan

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/survey_user_input.py`
- `addons/M02_P0213/data/email_template_social_insurance.xml`
- `addons/M02_P0213/security/ir.model.access.csv`
- `addons/M02_P0213/controllers/main.py`

## 3. Cac rui ro da doi chieu

- ACL `base.group_user` qua rong: da duoc xu ly o Buoc 6, xac nhan CSV hien co 44 ACL va cac ACL rong cua module 0213 tren `approval.request`, `mail.activity`, `survey.user_input` da khong con cap quyen.
- Portal category ref thieu `raise_if_not_found=False`: da duoc xu ly o Buoc 5.
- `action_view_survey_results`, `action_done`, `action_rehire`, `action_blacklist`: da co Python group guard tu Buoc 6, Buoc 9 bo sung them guard scope 0213 cho cac action chi thuoc offboarding.
- Email BHXH thieu fallback khi `work_email` rong: xu ly trong Buoc 9.
- Activity tren `hr.employee` co the bi dem lan voi activity khac: tiep tuc khoa pham vi bang filter 0213 cho compute checklist va auto-send BHXH.

## 4. Thay doi code

File sua:

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/survey_user_input.py`
- `addons/M02_P0213/data/email_template_social_insurance.xml`

Dieu chinh:

- Them `_ensure_0213_offboarding_request()` de chan action chi danh cho 0213 khi bi goi RPC tren request ngoai offboarding.
- Them `_get_0213_employee_email()` voi fallback:
  - `employee.work_email`
  - `employee.private_email`
  - `employee.user_id.partner_id.email`
  - `request_owner_id.partner_id.email`
  - `request_owner_id.email`
- Ap dung guard scope 0213 cho:
  - `action_send_adecco_notification`
  - `action_send_social_insurance`
  - `action_view_survey_results`
  - `action_launch_plan`
  - `action_rehire`
  - `action_blacklist`
  - `action_manual_reminder_extension`
- `action_send_social_insurance()` khong gui mail neu khong tim duoc email nhan vien, va khi gui thi truyen `email_values={"email_to": email_to}`.
- Template `psm_0213_email_template_social_insurance` doi `email_to` sang fallback expression.
- `_compute_all_activities_completed()`, `mail.activity._action_done()`, va `survey.user_input._check_and_mark_exit_interview_done()` dung `_filter_0213_offboarding_activities()` truoc khi dem pending activity.

## 5. Viec con theo doi

- Chua doi `activity plan` hard-code `base.main_company`, vi day la quyet dinh multi-company can xac nhan nghiep vu.
- Chua xoa dead code `_compute_owner_related_activity_ids`, de tranh refactor ngoai pham vi buoc 9.
- Can upgrade module va test user thuc te de xac nhan quyen cong don tu core Odoo.

## 6. Verification

- Da chay `python -m py_compile` cho:
  - `models/resignation_request.py`
  - `models/mail_activity.py`
  - `models/survey_user_input.py`
- Da parse XML `data/email_template_social_insurance.xml`.
- Da parse CSV `security/ir.model.access.csv`, ket qua 44 ACL.
- Da regenerate `structure/module_map.json`, stats va details.
