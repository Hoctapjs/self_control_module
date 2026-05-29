# Before / After cho patch config module 0213

## Pham vi

Patch nay tap trung vao 4 diem hard-code nghiep vu:

1. Email nhan thong bao Adecco
2. User mac dinh cho task `on_demand`
3. Rule phan luong theo contract type
4. Tham so reminder va gia han

## 1. Email Adecco

### Before

- Template `data/email_template_adecco_notification.xml` hard-code `email_to`.
- Muon doi nguoi nhan phai sua XML/data.

### After

- `email_to` trong template duoc de trong.
- Email nhan duoc lay tu config theo cong ty:
  - `res.company.x_psm_0213_adecco_notification_email`
- User chinh trong Settings qua `res.config.settings`.

## 2. User fallback cho `on_demand`

### Before

- `models/resignation_request.py` fallback theo login `it_rst`.
- Neu moi truong khong co user nay, assignment se phu thuoc vao fallback cuoi cung.

### After

- Fallback user duoc lay tu config theo cong ty:
  - `res.company.x_psm_0213_default_on_demand_user_id`
- Neu chua cau hinh, code moi fallback ve `env.user`.

## 3. Rule contract type

### Before

- View dung chuoi cứng `Full-Time`.
- Rule UI va rule backend co nguy co lech nhau.
- Auto flow trong `survey_user_input.py` co the goi gui BHXH ma khong di qua rule contract type.

### After

- Them config:
  - `res.company.x_psm_0213_social_insurance_contract_type_ids`
- Them field compute:
  - `approval.request.x_psm_0213_is_social_insurance_contract`
- View dung field compute thay vi so sanh chuoi `Full-Time`.
- Backend `action_send_adecco_notification`, `action_send_social_insurance` va auto flow survey cung dung chung rule nay.
- Co fallback giu hanh vi cu neu chua cau hinh contract type:
  - `Full-Time` van duoc coi la luong BHXH.

## 4. Reminder / extension days

### Before

- Gia han Due Date hard-code `+4 ngay`.
- Comment nghiep vu nhac den `3 ngay`, nhung code thuc te xu ly task vua qua han.
- Manual reminder va cron cung co logic cung trong code.

### After

- Them config:
  - `res.company.x_psm_0213_reminder_overdue_days`
  - `res.company.x_psm_0213_reminder_extension_days`
- Cron va manual reminder deu dung cung tham so config.
- `overdue_days = 0` giu hanh vi gan voi code cu:
  - chi can qua han la duoc dua vao reminder.

## 5. Settings UI

### Before

- Chua co man hinh settings rieng de chinh cac tham so nghiep vu nay.

### After

- Them view form rieng `views/res_config_settings_views.xml`
- Them menu `Approvals > Configuration > Offboarding OPS`
- User chinh tham so tren man hinh cau hinh rieng cua 0213, khong can di qua General Settings.

## 6. Tai lieu di kem

### Before

- Chua co note tong hop de giai thich tai sao patch theo huong config.

### After

- Da them:
  - `notes/DE_XUAT_CONFIG_TOI_THIEU_0213.md`
  - `notes/BEFORE_AFTER_CONFIG_PATCH_0213.md`

## Luu y

- Sau patch, `structure/module_map.json` se khong con khop hoan toan voi source hien tai vi co them models/views moi.
- Nen regenerate structure map sau khi merge patch.
