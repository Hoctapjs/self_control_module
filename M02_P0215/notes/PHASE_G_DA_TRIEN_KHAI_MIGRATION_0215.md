# Phase G - Da trien khai migration bridge cho du lieu cu 0215

Ngay cap nhat: 2026-05-07

## 1. Tai lieu da dung

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xac nhan:
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
  - `addons/M02_P0215/__manifest__.py`

## 2. Huong trien khai da chon

Phase nay khong auto-migrate khi upgrade module.

Da chon huong:

- them co che `manual bridge`
- chay theo tung record hoac nhom record do admin chu dong thao tac
- ghi lai trang thai migrate tren chinh ho so

Ly do:

- an toan hon cho production
- tranh tu dong tao approval request/snapshot tren toan bo du lieu cu
- de test va rollback theo lo

## 3. Cac thay doi da lam

### 3.1. Them field theo doi migration

Da them tren `x_psm.hr.discipline.record`:

- `x_psm_migration_status`
- `x_psm_migration_date`
- `x_psm_migration_note`

### 3.2. Them action bridge du lieu cu

Da them method:

- `action_psm_migrate_legacy_bridge()`

Action nay se chay 3 nhom bridge:

1. `legacy explanation`
2. `legacy approval`
3. `legacy feedback`

### 3.3. Bridge explanation cu

Method:

- `_x_psm_migrate_legacy_explanation_snapshot()`

Neu record cu:

- co text/signature/attachment explanation
- nhung chua co `x_psm_explanation_ids`

thi se tao 1 snapshot `x_psm.hr.discipline.explanation` de giu lich su.

### 3.4. Bridge approval cu

Method:

- `_x_psm_migrate_legacy_approval_bridge()`

Neu record cu:

- dang o `state = approval`
- la `company level`
- chua co `x_psm_approval_request_id`

thi se tao approval request theo flow moi.

Neu khong du dieu kien, action se danh dau note thay vi cuong ep migrate.

### 3.5. Chinh sach feedback cu

Method:

- `_x_psm_migrate_legacy_feedback_policy()`

Neu action dang la `feedback` ma chua co survey feedback:

- khong tu dong tao survey feedback cho record cu
- danh dau la `feedback_kept_legacy_only`

Huong nay dung voi plan goc: survey feedback chi ap dung bat buoc cho record moi sau refactor.

### 3.6. Them UI cho admin

Da them:

- button `Bridge dữ liệu cũ` tren form, group `hr.group_hr_manager`
- group `Migration` hien:
  - status
  - date
  - note

## 4. Cach doc ket qua migrate

`x_psm_migration_status` co cac gia tri:

- `not_needed`
- `pending`
- `partial`
- `done`
- `failed`

`x_psm_migration_note` se ghi chi tiet tung nhom:

- `explanation=...`
- `approval=...`
- `feedback=...`

## 5. Kiem tra da chay

- `python -m compileall addons/M02_P0215`
- parse toan bo XML trong module
- regenerate `structure/module_map.json`

## 6. Ghi chu van hanh

De migrate an toan, nen test theo thu tu:

1. record company level dang o `approval`
2. record co explanation cu nhung chua co snapshot history
3. record feedback cu

Khong nen chay hang loat tren production truoc khi da xac nhan nhom mau.
