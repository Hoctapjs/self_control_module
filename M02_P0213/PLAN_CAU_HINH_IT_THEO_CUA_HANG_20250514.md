# Plan cho Codex — Cấu hình IT phụ trách offboarding theo từng cửa hàng (M02_P0213)

## 1. Mục tiêu & phạm vi

Khi task IT offboarding (vd. B12 "IT xác nhận deactivate email và các tài khoản") được tự sinh, hệ thống phải gán đúng **IT phụ trách của cửa hàng nơi nhân viên thuộc về**, thay vì luôn dùng IT mặc định cấp công ty.

**Phạm vi sửa đổi:**
- Module chứa cấu hình store: `addons/M02_P0200` (mở rộng `hr.department`).
- Module chứa logic gán activity: `addons/M02_P0213` (`resignation_request._get_0213_default_responsible_user`).

**Không trong phạm vi:** thay đổi schema `res.company`, đổi keyword IT, sửa template plan.

---

## 2. Đối chiếu hiện trạng

| Hạng mục | Vị trí | Hiện trạng |
|---|---|---|
| Logic chọn IT | `resignation_request.py:290-314` | Chỉ lấy `company.x_psm_0213_default_it_user_id`, không xét cửa hàng |
| Logic gán activity | `resignation_request.py:942-997` | Fallback `template.responsible_id → _get_0213_default_responsible_user → env.user` |
| Field cấu hình IT cấp công ty | `res_company.py:42-47` | `x_psm_0213_default_it_user_id` đã có |
| Model cửa hàng | `hr_department_ext.py` | Có `block_id`, `pos_config_id`, `x_psm_store_*` — **chưa có field IT phụ trách** |
| Liên kết nhân viên → cửa hàng | `resignation_request.py:117` | `x_psm_0213_employee_id.department_id` |
| Template B12 | `offboarding_activity_plan_data.xml:50-68` | `responsible_type = on_demand`, không gán cứng `responsible_id` |

**Lưu ý:** Field `x_psm_is_store` có trong `store_data.xml` nhưng **không khai báo trong Python** — có thể là field Studio. Plan này không dùng `x_psm_is_store` làm điều kiện; thay vào đó dùng `block_code == 'OPS'` + `pos_config_id` (đã có trong model) hoặc chấp nhận mọi department đều có thể cấu hình IT, không filter — vì fallback đã an toàn.

---

## 3. Quy ước đặt tên (theo convention)

- Field mới trong `hr.department` (model gốc, do M02_P0213 mở rộng): **`x_psm_0213_it_user_id`**.
- View kế thừa mới: **`view_psm_0213_department_form_inherit_it_user`**.
- Đặt code trong `M02_P0213` (không trong M02_P0200) — vì đây là cấu hình **dành riêng cho nghiệp vụ offboarding 0213**, đúng nguyên tắc "tách bạch rõ ràng": field 0213 thuộc module 0213.

---

## 4. Các thay đổi cụ thể

### 4.1. Thêm model file mới: `addons/M02_P0213/models/hr_department.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"

    x_psm_0213_it_user_id = fields.Many2one(
        "res.users",
        string="IT Phụ Trách Offboarding (0213)",
        domain=[("share", "=", False)],
        help=(
            "Người dùng IT phụ trách các task offboarding 0213 của cửa hàng/phòng ban này. "
            "Nếu bỏ trống, hệ thống dùng IT mặc định cấp công ty "
            "(res.company.x_psm_0213_default_it_user_id)."
        ),
    )
```

**Cập nhật** `addons/M02_P0213/models/__init__.py`: thêm dòng `from . import hr_department` (đặt **sau** import `res_company` và **trước** `resignation_request` để giữ thứ tự alphabet/phụ thuộc).

### 4.2. Sửa logic `_get_0213_default_responsible_user` tại `resignation_request.py:290-314`

Đổi signature và body để xét cửa hàng trước khi fallback company:

```python
def _get_0213_default_responsible_user(self, template):
    self.ensure_one()
    company = self._get_0213_company()
    summary = (template.summary or "").strip().lower()
    note = (template.note or "").strip().lower()
    combined_text = " ".join(part for part in [summary, note] if part)

    it_keywords = (
        "email", "odoo", "erp", "ldap", "vpn",
        "active directory",
        "tài khoản email", "tai khoan email",
        "tài khoản hệ thống", "tai khoan he thong",
        "hệ thống", "he thong",
    )
    if any(keyword in combined_text for keyword in it_keywords):
        department = self.x_psm_0213_employee_id.department_id
        store_it = department.x_psm_0213_it_user_id if department else False
        return (
            store_it
            or company.x_psm_0213_default_it_user_id
            or company.x_psm_0213_default_on_demand_user_id
        )

    return company.x_psm_0213_default_on_demand_user_id
```

**Ghi chú:**
- Chỉ tra cứu store IT cho **task IT** (đã match keyword). Task on-demand khác giữ nguyên logic cũ.
- Fallback 3 tầng: store IT → company IT → company on-demand. Tầng cuối cùng `env.user` đã được xử lý ở `resignation_request.py:962-969`, không cần lặp lại ở đây.
- Không cần `sudo()` vì hr.department là record nội bộ và phương thức đã chạy trong ngữ cảnh approval.

### 4.3. Thêm view kế thừa: `addons/M02_P0213/views/hr_department_views.xml` (file mới)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_psm_0213_department_form_inherit_it_user" model="ir.ui.view">
        <field name="name">hr.department.form.inherit.psm.0213.it.user</field>
        <field name="model">hr.department</field>
        <field name="inherit_id" ref="hr.view_department_form"/>
        <field name="arch" type="xml">
            <field name="manager_id" position="after">
                <field name="x_psm_0213_it_user_id"
                       options="{'no_create': True}"/>
            </field>
        </field>
    </record>
</odoo>
```

> Đặt sau `manager_id` để hiển thị gần phần "phụ trách". Nếu xpath không trúng (manager_id có thể đã bị inherit khác bao quanh), dùng xpath theo group đầu form thay thế. Codex cần verify khi load view.

### 4.4. Cập nhật manifest `addons/M02_P0213/__manifest__.py`

Thêm `"views/hr_department_views.xml"` vào key `data`, đặt cạnh các view khác.

### 4.5. View công ty không cần thay đổi

Field IT công ty đã hiển thị tại `res_company_views.xml:32`. Bổ sung help-text trong field `x_psm_0213_default_it_user_id` của `res_company.py:42-47` làm rõ rằng đây là **fallback khi cửa hàng chưa cấu hình IT riêng** (sửa chuỗi `help=`).

### 4.6. Không cần migration script

Field mới mặc định NULL = fallback về company, không phá dữ liệu hiện có.

---

## 5. Cập nhật cấu trúc & tài liệu

- `addons/M02_P0213/structure/module_map.json`: thêm `models/hr_department.py` vào `structure.models`, thêm `views/hr_department_views.xml` vào `structure.views`, tăng `counts.python` lên 2 và `counts.views` lên 6. (Codex tự rà sau khi thêm file.)
- Thêm ghi chú vào `addons/M02_P0213/notes/` tên `BEFORE_AFTER_IT_PER_STORE_2026-05-14.md` mô tả before/after logic `_get_0213_default_responsible_user` và rationale (1 file ngắn, theo phong cách các note hiện có).

---

## 6. Kế hoạch test (manual, không có test framework auto)

1. **Trường hợp 1 — cửa hàng có IT riêng:** set `hr.department.x_psm_0213_it_user_id = U_store` cho department của nhân viên nghỉ. Approve resignation. Mở approval.request → tab Activities → activity B12 phải có `user_id = U_store`.

2. **Trường hợp 2 — cửa hàng KHÔNG có IT riêng, công ty có IT mặc định:** clear field department, set `res.company.x_psm_0213_default_it_user_id = U_company`. Approve → activity B12 phải có `user_id = U_company`.

3. **Trường hợp 3 — không có cả 2:** clear cả 2. Approve → fallback `x_psm_0213_default_on_demand_user_id`, nếu vẫn không có thì `env.user` (do block ở line 962-969).

4. **Trường hợp 4 — task non-IT (vd. B11 đánh giá hư hại):** verify keyword không match → đi nhánh `default_on_demand_user_id`, không bị "kéo" vào store IT.

5. **Trường hợp 5 — nhân viên không có department:** không lỗi, fallback company IT.

---

## 7. Thứ tự thực hiện (gợi ý cho Codex)

1. Tạo `models/hr_department.py` + cập nhật `__init__.py`.
2. Sửa `_get_0213_default_responsible_user` trong `resignation_request.py`.
3. Sửa help-text `x_psm_0213_default_it_user_id` trong `res_company.py`.
4. Tạo `views/hr_department_views.xml` + thêm vào `__manifest__.py`.
5. Cập nhật `module_map.json`.
6. Thêm note before/after.
7. Restart Odoo, upgrade module `M02_P0213`, chạy 5 kịch bản test.

---

## 8. Rủi ro & lưu ý

- **Xpath view** sau `manager_id` có thể bị các module khác inherit chèn nội dung trước → nếu lỗi load view, đổi sang xpath theo `//group` đầu form hoặc đặt trong group tab notebook của M02_P0200 (file `hr_department_views.xml`). **Không** sửa M02_P0200 trừ khi cần thiết — vẫn ưu tiên đặt field 0213 ở module 0213.

- **Multi-company:** field nằm trên `hr.department`, không có `company_id` cụ thể; nếu hệ thống dùng multi-company thì IT cấu hình theo từng department vẫn đúng vì department thuộc 1 company. Không cần thêm domain `company_id`.

- **Security:** không cần thêm ACL — field nằm trên model có sẵn (`hr.department`), kế thừa quyền của HR.

- **Convention compliance:** field `x_psm_0213_it_user_id` đúng pattern `x_psm_<module>_tenfield` cho field mới trên model gốc; view `view_psm_0213_department_form_inherit_it_user` đúng pattern `view_psm_*`.
