# Before / After cho patch config module 0214

## Pham vi

Patch nay tap trung vao cac diem hard-code nghiep vu trong `M02_P0214_00` co kha nang thay doi theo van hanh:

1. Email nhan thong bao Adecco
2. Reminder overdue va so ngay gia han
3. Rule nhan dien nhan vien portal RST
4. User fallback theo vai tro IT / Admin / HR
5. Man hinh cau hinh rieng trong Approval

## Tai lieu va nguon da doi chieu

- Structure map:
  - `addons/M02_P0214_00/structure/module_map.json`
- Source chinh:
  - `models/approval_request_rst_fields.py`
  - `models/approval_request_rst_reminder.py`
  - `models/approval_request_rst_offboarding.py`
  - `models/approval_request_rst_survey.py`
  - `controllers/main.py`
  - `data/email_template_adecco_notification.xml`

## 1. Email Adecco

### Before

- `data/email_template_adecco_notification.xml` hard-code `email_to`.
- Muon doi nguoi nhan phai sua XML/data.
- Neu flow RST goi action Adecco thi de bi phu thuoc vao data co dinh.

### After

- `email_to` trong template duoc de trong.
- Email nhan duoc lay tu config theo cong ty:
  - `res.company.x_psm_0214_adecco_notification_email`
- Them man hinh cau hinh de user quan tri co the doi email ma khong can sua code/XML.
- Override `action_send_adecco_notification()` rieng cho `0214` de dam bao dung template va config cua `0214`.

## 2. Reminder va gia han

### Before

- Reminder chi can task qua han la duoc dua vao xu ly.
- Sau khi gui reminder, code cong cung `+4 ngay`.
- Muon doi rule phai sua Python.

### After

- Them config theo cong ty:
  - `res.company.x_psm_0214_reminder_overdue_days`
  - `res.company.x_psm_0214_reminder_extension_days`
- Cron reminder va manual reminder cung dung chung config nay.
- `overdue_days = 0` giu hanh vi gan voi code cu:
  - chi can qua han la nhac.

## 3. Rule nhan dien portal RST

### Before

- Controller xac dinh nhan vien RST bang hard-code:
  - `block.code == "RST"`
  - hoac `block.name == "HEAD OFFICE"`
- Neu doi code block hoac ten block thi flow portal se lech.

### After

- Them config theo cong ty:
  - `res.company.x_psm_0214_portal_block_codes`
  - `res.company.x_psm_0214_portal_block_names`
- Controller parse danh sach cach nhau bang dau phay va doi chieu dong:
  - code block
  - ten block
- Nguoi van hanh co the doi rule nhan dien portal ma khong can sua code.

## 4. User fallback theo vai tro IT / Admin / HR

### Before

- Logic phan bo task fallback theo ten group hien thi:
  - `Technical Manager`
  - `Access Rights`
  - `Human Resources / User`
- Day la kieu hard-code mong manh vi phu thuoc ten group display.
- Neu moi truong khong co dung ten group nhu vay thi de lech assignment.

### After

- Them config theo cong ty:
  - `res.company.x_psm_0214_default_it_user_id`
  - `res.company.x_psm_0214_default_admin_user_id`
  - `res.company.x_psm_0214_default_hr_user_id`
- Logic moi uu tien user cau hinh truoc.
- Neu chua cau hinh moi fallback lai cach cu theo group name, de giu tinh tuong thich nguoc.

## 5. Settings UI trong Approval

### Before

- Chua co man hinh cau hinh rieng cho `0214`.
- User muon doi tham so nghiep vu thi phai sua data/code.

### After

- Them form cau hinh rieng:
  - `views/res_config_settings_views.xml`
- Them menu:
  - `Approvals > Configuration > Offboarding RST`
- User quan tri co the vao dung ngu canh Approval de chinh config cua `0214`.

## 6. Mo hinh du lieu moi

### Tren `res.company`

- `x_psm_0214_adecco_notification_email`
- `x_psm_0214_default_it_user_id`
- `x_psm_0214_default_admin_user_id`
- `x_psm_0214_default_hr_user_id`
- `x_psm_0214_reminder_overdue_days`
- `x_psm_0214_reminder_extension_days`
- `x_psm_0214_portal_block_codes`
- `x_psm_0214_portal_block_names`

### Tren `res.config.settings`

- Expose cac field related tuong ung de user chinh tren form cau hinh rieng.

## 7. Tinh tuong thich nguoc

- Neu chua cau hinh user IT/Admin/HR:
  - he thong van fallback tiep theo group name nhu cu.
- Neu `reminder_overdue_days = 0`:
  - hanh vi reminder van gan voi code cu.
- Neu chua doi block config:
  - gia tri mac dinh van la `RST` va `HEAD OFFICE`.

## 8. Luu y sau patch

- Can upgrade module `M02_P0214_00` de thay menu va man hinh cau hinh moi.
- `structure/module_map.json` cua `0214` se khong con khop hoan toan voi source hien tai vi co them models/views moi.
- Nen regenerate structure map sau khi merge patch.
