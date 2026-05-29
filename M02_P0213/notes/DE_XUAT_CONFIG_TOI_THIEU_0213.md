# De xuat config toi thieu cho module 0213

## Muc tieu

Giam hard-code nghiep vu trong `M02_P0213_00`, nhung van giu pham vi patch nho, de trien khai va it anh huong den flow hien tai.

## Tai lieu da dung

- Convention: `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Structure map: `structure/module_map.json`
- Source xac nhan chinh:
  - `models/resignation_request.py`
  - `models/survey_user_input.py`
  - `views/resignation_request_views.xml`
  - `data/email_template_adecco_notification.xml`
  - `data/email_template_dept_offboarding_reminder.xml`
  - `data/ir_cron_data.xml`

## Cac hard-code nghiep vu da xu ly trong patch nay

### 1. Email Adecco nhan thong bao nghi viec

Truoc day:
- `data/email_template_adecco_notification.xml` hard-code `email_to`.

Hien tai:
- Chuyen sang field cau hinh theo cong ty:
  - `res.company.x_psm_0213_adecco_notification_email`
- Expose trong `res.config.settings`.
- Khi bam action gui Adecco, code lay email tu config va truyen qua `email_values`.

### 2. User mac dinh cho task `on_demand`

Truoc day:
- `models/resignation_request.py` fallback theo login `it_rst`.

Hien tai:
- Chuyen sang field cau hinh theo cong ty:
  - `res.company.x_psm_0213_default_on_demand_user_id`
- Neu template chua co `responsible_id`, he thong lay user mac dinh tu config.

### 3. Rule phan luong theo loai hop dong

Truoc day:
- View kiem tra cung chuoi `Full-Time`.
- Logic UI va logic auto chua hoan toan dong bo.

Hien tai:
- Them cau hinh theo cong ty:
  - `res.company.x_psm_0213_social_insurance_contract_type_ids`
- Y nghia:
  - contract type thuoc danh sach nay: di luong BHXH
  - contract type khong thuoc danh sach nay: di luong Adecco
- Them field compute tren request:
  - `approval.request.x_psm_0213_is_social_insurance_contract`
- View va logic Python cung dung field nay.
- Co fallback tuong thich nguoc:
  - neu chua cau hinh contract type nao, he thong van coi `Full-Time` la luong BHXH nhu cu.

### 4. Reminder / extension days

Truoc day:
- Code gia han cung `4 ngay`.
- Comment mo ta `3 ngay` nhung code thuc te lai xu ly moi task qua han.

Hien tai:
- Them 2 field cau hinh theo cong ty:
  - `res.company.x_psm_0213_reminder_overdue_days`
  - `res.company.x_psm_0213_reminder_extension_days`
- Y nghia:
  - `overdue_days = 0`: chi can qua han la nhac
  - `overdue_days > 0`: phai tre qua so ngay do moi nhac
  - `extension_days`: so ngay cong them sau khi gui reminder
- Ap dung cho ca:
  - cron reminder
  - action manual reminder

## Pham vi khong dua vao config trong patch toi thieu nay

### 1. XML ID ky thuat

Vi du:
- category XML ID
- survey XML ID
- mail template XML ID

Ly do:
- day la technical binding cua module, khong nen de user business chinh.

### 2. Security groups / ir.rule

Vi du:
- cac group `M02_P0200_00.GDH_RST_*`

Ly do:
- day la policy truy cap, khong nen bien thanh config runtime cho user chinh tu do.

### 3. Tan suat cron

Hien dang la:
- `interval_number = 3`

Ly do chua patch:
- admin co the chinh truc tiep trong Scheduled Actions cua Odoo.
- Khong can them config rieng trong patch toi thieu.

## Thiet ke du lieu moi

### Tren `res.company`

- `x_psm_0213_adecco_notification_email`
- `x_psm_0213_default_on_demand_user_id`
- `x_psm_0213_social_insurance_contract_type_ids`
- `x_psm_0213_reminder_overdue_days`
- `x_psm_0213_reminder_extension_days`

### Tren `res.config.settings`

Expose cac field related tuong ung de user chinh trong man hinh cau hinh rieng cua 0213 duoi Approval.

### Tren `approval.request`

- `x_psm_0213_is_social_insurance_contract`

Field nay chi la field compute phuc vu thong nhat business rule giua UI va backend.

## Luu y sau patch

- Can vao `Approvals > Configuration > Offboarding OPS` de nhap email Adecco neu muon gui duoc mail Adecco.
- Neu khong cau hinh `default_on_demand_user_id`, task `on_demand` se fallback ve `env.user`.
- Neu chua cau hinh danh sach contract type BHXH, he thong van giu hanh vi cu voi `Full-Time`.

## Goi y buoc tiep theo neu muon lam sau hon

1. Them menu cau hinh rieng cho 0213 neu doi van hanh khong dung General Settings.
2. Tach recipient Adecco sang `res.partner` thay vi `Char email`.
3. Lam data migration de map san contract type `Full-Time` vao config cua cong ty.
4. Regenerate `structure/module_map.json` vi sau patch se co them models/views moi.
