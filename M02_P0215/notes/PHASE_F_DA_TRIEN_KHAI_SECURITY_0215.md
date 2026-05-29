# Phase F - Da trien khai security cho 0215 sau refactor approval/survey

Ngay cap nhat: 2026-05-07

## 1. Tai lieu da dung

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xac nhan:
  - `addons/M02_P0215/security/ir.model.access.csv`
  - `addons/M02_P0215/security/security_rules.xml`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
  - `addons/M02_P0215/controllers/portal.py`

## 2. Pham vi da lam

### 2.1. Portal explanation ve lai read-only

Vi luong moi da chuyen sang `survey.user_input`, quyen portal tren
`x_psm.hr.discipline.explanation` da duoc ha xuong:

- access CSV: `read=1, write=0, create=0, unlink=0`
- record rule portal explanation: `perm_write=False`, `perm_create=False`

Muc tieu:

- portal khong con ghi truc tiep vao model explanation custom nua
- uu tien dung quyen cua module `survey`

### 2.2. Bo sung quyen rieng cho RGM

Da them access va rule rieng cho group:

- `M02_P0200.GDH_OPS_STORE_RGM_M`

Cho model:

- `x_psm.hr.discipline.record`
  - read/write
  - khong create/unlink
- `x_psm.hr.discipline.explanation`
  - read-only

Scope rule cua RGM:

- nhan vien ma user la quan ly truc tiep
- ho so ma user la dai dien cong ty
- ho so trong cung department voi employee cua user

### 2.3. Khoa button RGM theo group

Da them `groups="M02_P0200.GDH_OPS_STORE_RGM_M"` cho cac button:

- `action_psm_rgm_no_repeat`
- `action_psm_rgm_repeat`
- `action_psm_rgm_store_level`
- `action_psm_rgm_company_level`

Muc tieu:

- UI khop voi security thuc te
- giam nguy co user khong dung vai tro thay duoc action nhay state

## 3. Diem chu y

- Chua mo rong quyen 0215 cho `approval.request` hoac `survey.user_input`; van uu tien quyen goc cua module `approvals` va `survey`.
- Controller portal van co `sudo()` o mot so cho de phuc vu portal guard hien tai, nhung phan write truc tiep vao explanation custom da bi ha quyen o security.

## 4. Kiem tra da chay

- `python -m compileall addons/M02_P0215`
- parse toan bo XML trong module
- regenerate `structure/module_map.json`

## 5. Ket qua

Sau phase nay:

- portal user chi con read tren explanation custom
- RGM co quyen dung vai tro tren ho so 0215
- button xu ly RGM khong con lo ra cho group khac
