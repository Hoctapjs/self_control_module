# Phase E - Don code trung va giu tuong thich du lieu cu 0215

Ngay cap nhat: 2026-05-07

## 1. Tai lieu da dung

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xac nhan:
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/controllers/portal.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_explanation.py`
  - `addons/M02_P0215/wizards/x_psm_hr_discipline_reject_wizard.py`

## 2. Pham vi da lam

### 2.1. Giu nguyen field cu, khong xoa du lieu

Khong xoa cac field:

- `x_psm_section_i_description`
- `x_psm_section_ii_feedback`
- `x_psm_section_iii_identification`
- `x_psm_section_iv_agreement`
- `x_psm_explanation_ids`

### 2.2. Danh dau ro vai tro moi cua field cu

Da bo sung `help` cho cac field cu de xac dinh ro:

- field nao la nghiep vu goc
- field nao la snapshot/cache
- field nao duoc dong bo tu survey hoac fallback legacy

Muc tieu la de:

- report/mail cu van doc duoc
- nguoi doc code khong nham day la nguon du lieu chinh nua

### 2.3. Giu route portal legacy lam fallback

Khong xoa ngay cac route:

- `/my/discipline/submit_section_ii`
- `/my/discipline/manager_finalize`

Nhung da danh dau ro trong docstring va chatter la:

- `legacy fallback`
- khong phai luong survey chinh nua

### 2.4. Dong bo them snapshot khi fallback legacy duoc dung

Route legacy submit Section II hien tai se ghi them:

- `x_psm_employee_explanation`
- `x_psm_explanation_date`

de du lieu cu va report khong bi khuyet.

## 3. Cac diem co chu y

- Model `x_psm.hr.discipline.explanation` va reject wizard van duoc giu lai.
- Khong xoa method legacy trong record model.
- Khong can thiep migration pha huy du lieu o phase nay.

## 4. Kiem tra da chay

- `python -m compileall addons/M02_P0215`
- parse toan bo XML trong module
- regenerate `structure/module_map.json`

## 5. Ket qua mong muon sau phase nay

- Codebase phan biet ro hon giua:
  - nguon du lieu moi: approval/survey
  - truong tuong thich: snapshot/cache/legacy
- Giam rui ro xoa som field, model, route dang con du lieu cu hoac reference cu.
