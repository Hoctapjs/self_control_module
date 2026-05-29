# Phase 5 - Hotfix lỗi gỡ cài đặt module 0215

Ngày thực hiện: 2026-05-07

## Bối cảnh

Khi gỡ cài đặt `M02_P0215`, Odoo lỗi trong quá trình build registry và uninstall dữ liệu:

```text
KeyError: 'x_psm.hr.discipline.action'
```

Sau khi kiểm tra log, lỗi gốc không nằm ở model `x_psm.hr.discipline.action` mà do module `M02_P0215` không được load đầy đủ khi registry khởi tạo. Các nguyên nhân được ghi nhận:

- Manifest `M02_P0215` có UTF-8 BOM ở đầu file, làm Odoo parse manifest không ổn định.
- Manifest dùng version ngắn `0.2`, đã đổi sang format rõ ràng `19.0.0.3`.
- `auto_install` đang bật trong manifest, không phù hợp với module nghiệp vụ cần cài/gỡ thủ công.
- `M02_P0215` phụ thuộc cứng vào `M02_P0200`, trong khi database hiện tại có `M02_P0200` ở trạng thái installed nhưng các dependency của `M02_P0200` như `hr_payroll`, `hr_work_entry` đang uninstalled. Vì vậy Odoo skip `M02_P0200`, kéo theo lỗi load `M02_P0215`.
- Sau khi bỏ dependency cứng `M02_P0200`, `M02_P0215` vẫn còn related field trỏ trực tiếp đến `hr.job.level_id`, đây là field do `M02_P0200` mở rộng nên registry tiếp tục lỗi nếu `M02_P0200` bị skip.

## Thay đổi đã triển khai

### 1. Cập nhật manifest

File: `addons/M02_P0215/__manifest__.py`

- Loại bỏ BOM đầu file.
- Đổi version sang `19.0.0.3`.
- Đổi `auto_install` thành `False`.
- Bỏ dependency cứng `M02_P0200` để module 0215 có thể load/gỡ trong database mà `M02_P0200` đang lỗi dependency.

### 2. Gỡ phụ thuộc registry vào `hr.job.level_id`

File: `addons/M02_P0215/models/x_psm_hr_discipline_record.py`

- Đổi `x_psm_rep_level` từ related field sang computed field.
- Đổi `x_psm_emp_level` từ related field sang computed field.
- Thêm helper `_x_psm_get_employee_level_name()` để lấy cấp bậc theo thứ tự:
  - dùng `employee.job_level_id` nếu field tồn tại;
  - dùng `employee.job_id.level_id` nếu field tồn tại;
  - trả về rỗng nếu module mở rộng cấp bậc chưa được load.

Cách này giúp registry không crash khi `M02_P0200` bị skip, nhưng vẫn hiển thị cấp bậc nếu các field mở rộng có sẵn.

### 3. Vá portal tránh lỗi runtime

File: `addons/M02_P0215/controllers/portal.py`

- Thêm helper `_x_psm_get_employee_level()`.
- `_x_psm_is_manager_employee()` không truy cập trực tiếp `employee.job_id.level_id` nữa.

### 4. Cập nhật structure map

Đã chạy lại:

```powershell
python structure\build_module_map.py
```

Các file map được cập nhật theo source hiện tại.

### 5. Đồng bộ metadata trong database

Database `admin5` vẫn đang lưu `M02_P0215.auto_install = true` từ trạng thái cũ. Đã dùng Odoo ORM để cập nhật lại:

```python
module = env["ir.module.module"].search([("name", "=", "M02_P0215")], limit=1)
module.write({"auto_install": False})
env.cr.commit()
```

Kết quả kiểm tra DB:

```text
M02_P0215 | installed | auto_install = f | latest_version = 19.0.0.2
```

## Kết quả kiểm tra

Đã chạy kiểm tra tĩnh:

```powershell
python -m compileall addons\M02_P0215
python -c "import ast, pathlib; ast.literal_eval(pathlib.Path('addons/M02_P0215/__manifest__.py').read_text(encoding='utf-8')); print('manifest ok')"
```

Đã restart container Odoo và gọi request vào database `admin5`.

Kết quả log mới:

```text
Modules loaded.
Registry loaded in 2.359s
```

Danh sách module bị skip sau hotfix chỉ còn:

```text
['M02_P0200', 'M02_P0213', 'M02_P0214']
```

`M02_P0215` không còn bị skip và không còn lỗi:

```text
KeyError: 'Field level_id referenced in related field definition x_psm.hr.discipline.record.x_psm_rep_level does not exist.'
```

## Ghi chú còn lại

Lỗi nền của database vẫn còn ở `M02_P0200`: module này đang installed nhưng các dependency `hr_payroll`, `hr_work_entry` đang uninstalled, nên Odoo vẫn skip `M02_P0200`. Hotfix này giúp `M02_P0215` không còn phụ thuộc cứng vào tình trạng load của `M02_P0200` để có thể tiếp tục thao tác gỡ cài đặt.

Nếu muốn xử lý triệt để hệ module liên quan, cần rà soát riêng `M02_P0200`, `M02_P0213`, `M02_P0214` và trạng thái dependency trong database.

## Bổ sung hotfix lỗi BOM CSV

Khi cài lại module, Odoo phát sinh lỗi:

```text
ValueError: Invalid field name '\ufeffid'
```

Nguyên nhân là file `security/ir.model.access.csv` có UTF-8 BOM ở đầu file. Odoo đọc header đầu tiên thành `\ufeffid` thay vì `id`, nên import CSV thất bại.

Đã quét và loại bỏ BOM ở đầu toàn bộ file source/data chính của module `M02_P0215`, bao gồm `.py`, `.xml`, `.csv`, `.md`. Sau đó đã kiểm tra lại:

```text
no bom found
CSV header: ['id', 'name', 'model_id:id', 'group_id:id', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink']
xml ok
compileall ok
```

Đã chạy install kiểm chứng qua Odoo ORM. Kết quả:

```text
M02_P0215 | installed | auto_install = f | latest_version = 19.0.0.3
```
