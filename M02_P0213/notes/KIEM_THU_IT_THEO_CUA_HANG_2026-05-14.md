# Kiem thu IT theo cua hang cho offboarding 0213

## Muc tieu

Kiem thu viec task IT offboarding, vi du B12 "IT xac nhan deactivate email va cac tai khoan", duoc gan dung IT phu trach theo cua hang/phong ban cua nhan vien nghi viec.

## File va cau hinh lien quan

- Module: `M02_P0213`
- Convention da dung:
  - `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Structure map da regenerate:
  - `addons/M02_P0213/structure/module_map.json`
  - `addons/M02_P0213/structure/module_map_stats.json`
- Field cau hinh IT theo cua hang:
  - Model: `hr.department`
  - Field: `x_psm_0213_it_user_id`
  - File: `addons/M02_P0213/models/hr_department.py`
- View cau hinh tren Department:
  - File: `addons/M02_P0213/views/hr_department_views.xml`
  - XML ID: `M02_P0213.view_psm_0213_department_form_inherit_it_user`
  - Vi tri UI mong muon: tab `Offboarding Store`
- Logic gan nguoi phu trach task:
  - File: `addons/M02_P0213/models/resignation_request.py`
  - Ham: `_get_0213_default_responsible_user`
- Cau hinh fallback cap cong ty:
  - `res.company.x_psm_0213_default_it_user_id`
  - `res.company.x_psm_0213_default_on_demand_user_id`

## Luong xac dinh IT

Khi offboarding plan tao activity co `responsible_type = on_demand`:

```text
template.responsible_id
  -> neu khong co, goi _get_0213_default_responsible_user(template)
  -> neu van khong co, fallback env.user
```

Trong `_get_0213_default_responsible_user(template)`:

```text
Neu summary/note cua template match keyword IT
  -> lay employee.department_id.x_psm_0213_it_user_id
  -> neu trong, lay company.x_psm_0213_default_it_user_id
  -> neu trong, lay company.x_psm_0213_default_on_demand_user_id

Neu khong match keyword IT
  -> lay company.x_psm_0213_default_on_demand_user_id
```

Keyword IT hien tai gom cac cum nhu:

```text
email, odoo, erp, ldap, vpn, active directory,
tai khoan email, tai khoan he thong, he thong
```

## Template task IT can kiem tra

File:

```text
addons/M02_P0213/data/offboarding_activity_plan_data.xml
```

Template B12 / IT:

```text
summary: Vo hieu hoa tai khoan email va he thong
responsible_type: on_demand
```

Template nay match keyword IT vi co `email` va `he thong`.

## Cac database da xac dinh

Trong container PostgreSQL co cac DB:

```text
admin
admin4
admin5
admin6
postgres
```

Trang thai module tai thoi diem ra soat:

```text
admin:  M02_P0213 = uninstalled
admin4: M02_P0213 = installed
admin5: M02_P0213 = installed
admin6: M02_P0213 = installed
```

Luu y: sau khi doi view sang tab `Offboarding Store`, can upgrade lai module tren cac DB dang test truoc khi kiem thu UI.

Lenh upgrade goi y:

```bash
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -c /opt/odoo/odoo.conf -d admin4 -u M02_P0213 --stop-after-init --no-http
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -c /opt/odoo/odoo.conf -d admin5 -u M02_P0213 --stop-after-init --no-http
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -c /opt/odoo/odoo.conf -d admin6 -u M02_P0213 --stop-after-init --no-http
docker restart odoo-190e20250918-web-1
```

Lenh xac nhan field/view trong DB:

```sql
select model, name
from ir_model_fields
where model = 'hr.department'
  and name = 'x_psm_0213_it_user_id';

select key
from ir_ui_view
where key = 'M02_P0213.view_psm_0213_department_form_inherit_it_user';
```

## Checklist kiem thu UI cau hinh

1. Mo Employees -> Departments.
2. Mo mot Department/cua hang cua nhan vien test.
3. Kiem tra co tab `Offboarding Store`.
4. Trong tab nay co field `IT Phu Trach`.
5. Chon user IT noi bo cho field `IT Phu Trach`.
6. Save department.

Neu field van hien gan `Manager`, nghia la module chua duoc upgrade sau patch view moi.

## Checklist kiem thu nghiep vu

### Case 1: Cua hang co IT rieng

Thiet lap:

```text
employee.department_id.x_psm_0213_it_user_id = U_store
company.x_psm_0213_default_it_user_id = U_company
```

Thuc hien:

```text
Nhan vien nop don nghi viec
Line Manager approve don
He thong tao offboarding activities
```

Ket qua mong doi:

```text
Activity IT B12 user_id = U_store
```

### Case 2: Cua hang khong co IT rieng

Thiet lap:

```text
employee.department_id.x_psm_0213_it_user_id = False
company.x_psm_0213_default_it_user_id = U_company
```

Ket qua mong doi:

```text
Activity IT B12 user_id = U_company
```

### Case 3: Khong co IT cua hang, khong co IT cong ty

Thiet lap:

```text
employee.department_id.x_psm_0213_it_user_id = False
company.x_psm_0213_default_it_user_id = False
company.x_psm_0213_default_on_demand_user_id = U_on_demand
```

Ket qua mong doi:

```text
Activity IT B12 user_id = U_on_demand
```

Neu `U_on_demand` cung trong, logic tao activity se fallback ve `env.user`.

### Case 4: Task on-demand khong phai IT

Thiet lap:

```text
employee.department_id.x_psm_0213_it_user_id = U_store
company.x_psm_0213_default_on_demand_user_id = U_on_demand
```

Ket qua mong doi:

```text
Task non-IT khong bi gan cho U_store.
Task non-IT dung default_on_demand hoac logic responsible rieng cua template.
```

### Case 5: Nhan vien khong co department

Thiet lap:

```text
employee.department_id = False
company.x_psm_0213_default_it_user_id = U_company
```

Ket qua mong doi:

```text
Khong loi.
Activity IT B12 user_id = U_company
```

## SQL ho tro kiem tra nhanh activity

Sau khi approve don va plan da tao activities, co the tim activity lien quan request:

```sql
select ma.id,
       ma.summary,
       ma.user_id,
       rp.name as assigned_user
from mail_activity ma
left join res_users ru on ru.id = ma.user_id
left join res_partner rp on rp.id = ru.partner_id
where ma.res_model = 'approval.request'
  and ma.summary ilike '%email%'
order by ma.id desc
limit 20;
```

Neu can loc theo request cu the:

```sql
select ma.id,
       ma.summary,
       ma.user_id,
       rp.name as assigned_user
from mail_activity ma
left join res_users ru on ru.id = ma.user_id
left join res_partner rp on rp.id = ru.partner_id
where ma.res_model = 'approval.request'
  and ma.res_id = <approval_request_id>
order by ma.id;
```

## Kiem tra code tinh

Da chay:

```bash
python -m compileall -q addons\M02_P0213\models
python -c "import xml.etree.ElementTree as ET; ET.parse('addons/M02_P0213/views/hr_department_views.xml'); print('hr_department_views xml ok')"
python addons\M02_P0213\structure\build_module_map.py
```

## Luu y hien trang

- Code Python va XML da duoc cap nhat.
- `module_map.json` da regenerate.
- Lan upgrade truoc do da chay tren `admin4`, `admin5`, `admin6` cho logic field/assignment.
- Sau khi doi UI sang tab `Offboarding Store`, can chay lai upgrade module tren DB dang test de view moi co hieu luc.
