# Portal UI Plan 0214

Ngay lap: 2026-05-14

## 1. Muc tieu

Tai lieu nay la gate cua Phase 1 cho viec ap dung pattern UI tu `M02_P0213` sang `M02_P0214`.

Pham vi Phase 1 chi gom:

- Tao convention rieng cho 0214.
- Tao backup portal template truoc khi redesign.
- Lap mapping class/file/button/route de dung cho Phase 2 va Phase 3.

Phase 1 khong sua controller, model, route, field submit, group quyen, hay nghiep vu.

## 2. Tai lieu va source da doi chieu

- Plan chinh: `addons/M02_P0214/notes/RA_SOAT_VA_PLAN_UI_0214_TU_0213_20250514.md`
- Convention nguon: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Convention 0214 moi: `addons/M02_P0214/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Module map 0214: `addons/M02_P0214/structure/module_map.json`
- Controller portal 0214: `addons/M02_P0214/controllers/main.py`
- Template portal 0214: `addons/M02_P0214/views/resignation_portal_template.xml`

## 3. Backup

Backup portal template truoc khi redesign:

`addons/M02_P0214/notes/backups/resignation_portal_template.step1.20260514.bak`

Dung backup nay de rollback Phase 3 neu template portal bi vo layout, doi nham field, hoac submit fail.

## 4. Mapping file 0213 -> 0214

| 0213 | 0214 du kien | Ghi chu |
|---|---|---|
| `static/src/scss/backend_0213.scss` | `static/src/scss/backend_0214.scss` | Tao moi trong Phase 2 |
| `static/src/scss/portal_resignation_0213.scss` | `static/src/scss/portal_resignation_0214.scss` | Tao moi trong Phase 3 |
| `static/src/js/portal_resignation_0213.js` | `static/src/js/portal_resignation_0214.js` | Tao moi trong Phase 3 |
| `views/resignation_portal_template.xml` | `views/resignation_portal_template.xml` | Sua tren file hien huu, khong doi template id |
| `views/resignation_request_views.xml` | `views/resignation_request_views.xml` | Chi them wrapper/class backend, khong doi group |
| `views/res_company_views.xml` | `views/res_company_views.xml` | Chi them class form backend |
| `views/res_config_settings_views.xml` | `views/res_config_settings_views.xml` | Co file trong views nhung hien chua nam trong manifest data |
| `views/hr_department_views.xml` | `views/hr_employee_views.xml` | 0214 mo rong employee, khong ap dung IT theo department |

## 5. Mapping class 0213 -> 0214

| 0213 class | 0214 class | Trang thai |
|---|---|---|
| `.o_psm_0213_portal` | `.o_psm_0214_portal` | Bat buoc doi, khong dung lai class 0213 |
| `.o_psm_0213_backend_view` | `.o_psm_0214_backend_view` | Dung cho backend form/page wrapper |
| `.o_psm_0213_backend_action` | `.o_psm_0214_backend_action` | Dung cho button backend hien huu |
| `.psm-form-header` | `.psm-form-header` | Co the dung lai vi scoped trong `.o_psm_0214_portal` |
| `.psm-form-header__subtitle` | `.psm-form-header__subtitle` | Subtitle 0214 phai la "Don Xin Nghi Viec - Khoi RST" |
| `.psm-form-progress` | `.psm-form-progress` | Co the dung lai trong wrapper 0214 |
| `.psm-form-section` | `.psm-form-section` | Co the dung lai trong wrapper 0214 |
| `.psm-section__index` | `.psm-section__index` | Co the dung lai trong wrapper 0214 |
| `.psm-section__title` | `.psm-section__title` | Co the dung lai trong wrapper 0214 |
| `.psm-form-control` | `.psm-form-control` | Dung thay `form-control bg-light` khi redesign |
| `.psm-alert--approved` | `.psm-alert--approved` | Co the dung lai, scoped trong wrapper 0214 |
| `.theme-task-card` | `.theme-task-card` | Co the dung lai, scoped trong wrapper 0214 |
| `.theme-task-owner` | `.theme-task-owner` | Khi style font, khong de len `.fa` icon |
| `.theme-survey-title` | `.theme-survey-title` | Co the dung lai, scoped trong wrapper 0214 |

## 6. Mapping button/action backend

Chi gan class `o_psm_0214_backend_action` cho button hien huu cua 0214. Khong copy button nghiep vu tu 0213.

| 0213 button | 0214 tuong ung | Xu ly Phase 2 |
|---|---|---|
| `action_send_social_insurance` | `action_send_social_insurance` | Them class backend action |
| `action_done` | `action_done` | Them class backend action |
| `action_view_survey_results` | `action_view_survey_results` neu co trong view | Them class backend action neu dang co |
| `action_send_adecco_notification` | Khong ap dung | Khong them button moi |
| `action_rehire` | Khong ap dung | Khong them button moi |
| `action_blacklist` | Khong ap dung | Khong them button moi |
| Button stat `My Activities` cua 0214 | Khong co trong 0213 | Giu nguyen, khong xoa, chi style neu an toan |

## 7. Route va field submit phai giu nguyen

Controller `addons/M02_P0214/controllers/main.py` dang dung:

- `GET /my/resignation/rst`
- `POST /my/resignation/rst/submit`
- `POST /my/resignation/rst/activity/done`

Template `addons/M02_P0214/views/resignation_portal_template.xml` dang co cac input/form quan trong:

- `form action="/my/resignation/rst/submit" method="post"`
- `form action="/my/resignation/rst/activity/done" method="post"`
- `name="csrf_token"`
- `name="activity_id"`
- `name="approver_user_id"`
- `name="x_psm_0214_resignation_date"`
- `name="x_psm_0214_resignation_reason_id"`
- `name="x_psm_0214_resignation_reason"`

Phase 3 bat buoc giu nguyen cac route va `name=` tren.

## 8. Mapping portal section

| Hien tai 0214 | Sau Phase 3 | Ghi chu |
|---|---|---|
| Wrapper `.psm-rst-resignation-portal` | Wrapper `.o_psm_0214_portal` | Doi class scope chinh |
| Heading `Gui yeu cau nghi viec` | Banner `psm-form-header` | Subtitle dung "Don Xin Nghi Viec - Khoi RST" |
| Khoi thong tin nhan vien bang `h5` | `section#psm-section-1` | Giu field readonly hien huu |
| Khoi thong tin nghi viec bang `h5` | `section#psm-section-2` | Giu date/select/textarea name hien huu |
| Khoi xac nhan cam ket | `section#psm-section-3` | Giu noi dung cam ket hien huu |
| Alert pending/approved/done | `psm-alert psm-alert--info/success/approved` | Khong doi dieu kien status |
| Task card sau approved | Giua theme classes + style scoped | Khong doi route done activity |

## 9. Constraint cho cac phase tiep theo

- Khong doi controller/model/route.
- Khong doi group/invisible hien huu.
- Khong them button nghiep vu moi.
- Khong dung class `.o_psm_0213_*`.
- Khong sua file `desktop.ini`.
- Neu style icon FontAwesome, khong ep `font-family: Roboto` len `.fa`.

## 10. Gate Phase 1

Phase 1 duoc xem la pass khi co du:

- `addons/M02_P0214/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0214/notes/backups/resignation_portal_template.step1.20260514.bak`
- `addons/M02_P0214/notes/PORTAL_UI_PLAN_0214.md`
- Mapping da doi chieu voi controller va template hien tai.
