# Before / After IT theo cua hang cho offboarding 0213

## Pham vi

Patch nay bo sung cau hinh IT phu trach offboarding theo tung cua hang/phong ban cho module `M02_P0213`.

File thay doi:

- `models/hr_department.py`
- `models/__init__.py`
- `models/resignation_request.py`
- `models/res_company.py`
- `views/hr_department_views.xml`
- `__manifest__.py`

## Before

- Task IT offboarding dang la template `responsible_type = on_demand`.
- Khi template co keyword IT nhu `email`, `odoo`, `erp`, `ldap`, `vpn`, he thong chi lay:
  - `res.company.x_psm_0213_default_it_user_id`
- Neu nhieu cua hang co IT phu trach khac nhau, task B12 co the bi giao ve mot IT mac dinh cap cong ty.

## After

- Them field tren `hr.department`:
  - `x_psm_0213_it_user_id`
- Khi task on-demand match keyword IT, he thong uu tien:
  - IT cau hinh tren department/cua hang cua nhan vien nghi viec
  - sau do fallback ve `res.company.x_psm_0213_default_it_user_id`
  - sau do fallback ve `res.company.x_psm_0213_default_on_demand_user_id`
- Cac task on-demand khong phai IT giu logic cu: dung `default_on_demand_user_id`.

## Rationale

Nhan vien OPS dang gan cua hang qua `hr.employee.department_id`. Vi vay cau hinh IT theo `hr.department` giup task IT offboarding di dung nguoi phu trach cua cua hang ma khong can tao model moi.

Field moi nam trong `M02_P0213` vi day la cau hinh rieng cho nghiep vu offboarding 0213, khong phai cau hinh master data dung chung cua `M02_P0200`.

## Test goi y

- Department co `x_psm_0213_it_user_id`: task IT duoc gan cho user nay.
- Department khong co IT rieng: fallback ve IT mac dinh cap cong ty.
- Company khong co IT mac dinh: fallback ve default on-demand, sau cung la `env.user` trong logic tao activity.
- Task non-IT khong bi gan ve store IT.
