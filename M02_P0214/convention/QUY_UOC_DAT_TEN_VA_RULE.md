# Quy Uoc Dat Ten Va Rule - M02_P0214

Tai lieu nay ke thua convention tu `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md` va ap dung cho module `M02_P0214`.

## 1. Quy uoc dat ten

### 1.1. Manifest

- Cau truc ten module trong manifest:
  - `M02_P0214_<TEN_QUY_TRINH_VIET_HOA>`
- Khong can the hien version trong ten module.

### 1.2. Model goc

- Model goc giu nguyen ten.
- Khong doi ten model goc.

### 1.3. Model moi

- Model moi dat theo quy uoc:
  - `x_psm_<ten_model>`

### 1.4. Field moi trong model goc

- Field moi bo sung vao model goc dat theo quy uoc:
  - `x_psm_0214_tenfield`

### 1.5. Field moi trong model moi

- Field moi trong model moi dat theo quy uoc:
  - `x_psm_tenfield`

### 1.6. Action moi

- Action moi dat theo quy uoc:
  - `action_psm_tenaction`

### 1.7. View moi

- View moi dat theo quy uoc:
  - `view_psm_tenview`

### 1.8. Security

#### Van phong

- Nhom 1:
  - `group_gdh_rst_module_stf`
- Nhom 2:
  - `group_gdh_rst_module_mgr`

#### Nha hang

- Nhom 1:
  - `group_gdh_ops_module_crw`
- Nhom 2:
  - `group_gdh_ops_module_mgr`

### 1.9. Duyet

- Su dung chung module:
  - `approval`

### 1.10. Cham diem, khao sat, phong van, cau hoi

- Su dung chung module:
  - `survey`

### 1.11. Ung vien

- Su dung ten thong nhat:
  - `applicant`

### 1.12. Nhan vien

- Su dung ten thong nhat:
  - `employee`

## 2. Rule can tuan thu

### 2.1. Uu tien dung cai san co

- Co gang tan dung toi da model, field, action, view, module san co cua Odoo hoac he thong hien tai.
- Han che toi da viec tao model moi neu chua that su can thiet.

### 2.2. Phan quyen toi thieu

- Chi cap dung muc quyen can thiet de hoan thanh cong viec.
- Khong phan quyen tran lan.
- Uu tien nguyen tac minimum permission.

### 2.3. Tach bach ro rang

- Ngan nao ra ngan nay.
- Chuc nang nao thuoc module nao thi de dung module do.
- Han che viet logic long ghep, chong cheo giua cac module.

### 2.4. Rule rieng khi ap dung UI tu 0213 sang 0214

- Khong doi route portal hien huu:
  - `/my/resignation/rst`
  - `/my/resignation/rst/submit`
  - `/my/resignation/rst/activity/done`
- Khong doi `csrf_token`.
- Khong doi ten field submit hien huu:
  - `approver_user_id`
  - `x_psm_0214_resignation_date`
  - `x_psm_0214_resignation_reason_id`
  - `x_psm_0214_resignation_reason`
- Khong dung lai class scope cua 0213:
  - khong dung `.o_psm_0213_portal`
  - khong dung `.o_psm_0213_backend_view`
  - khong dung `.o_psm_0213_backend_action`
- Bat buoc dung class scope rieng cua 0214:
  - `.o_psm_0214_portal`
  - `.o_psm_0214_backend_view`
  - `.o_psm_0214_backend_action`
- Khong sao chep nghiep vu khong thuoc RST:
  - khong them IT theo cua hang cua 0213
  - khong them button Adecco/Rehire/Blacklist neu 0214 chua co nghiep vu do
- Khong dung label "Khoi Cua Hang" cho 0214; neu can subtitle thi dung "Khoi RST".
- Khong dung hoac sua file `desktop.ini`.

## 3. Tom tat nhanh

- Model goc: giu nguyen ten.
- Model moi: `x_psm_<ten_model>`.
- Field moi model goc: `x_psm_0214_tenfield`.
- Field moi model moi: `x_psm_tenfield`.
- Action moi: `action_psm_tenaction`.
- View moi: `view_psm_tenview`.
- Approval dung chung module `approval`.
- Survey, cham diem, phong van, cau hoi dung chung module `survey`.
- Ung vien dung ten `applicant`.
- Nhan vien dung ten `employee`.
- UI 0214 phai scoped rieng bang `.o_psm_0214_*`.
