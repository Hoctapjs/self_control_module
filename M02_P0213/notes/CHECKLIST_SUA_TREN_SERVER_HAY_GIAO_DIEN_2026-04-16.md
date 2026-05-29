# Checklist sửa trên server hay bằng giao diện - 2026-04-16

## Mục tiêu

Checklist này giúp xác định:

- có thể sửa trực tiếp bằng giao diện Odoo hay không
- khi nào bắt buộc phải sửa code
- cách kiểm tra Odoo đang đọc addon từ thư mục nào

## 1. Khi nào có thể sửa bằng giao diện

Có thể ưu tiên sửa bằng giao diện nếu vấn đề nằm ở:

- quyền user
- group quyền
- access rights
- record rules
- dữ liệu cấu hình
- menu, action, view cấu hình từ giao diện
- field custom tạo bằng Studio
- automated action hoặc server action

Ví dụ:

- user không thấy menu
- user thiếu quyền đọc model
- record rule chặn dữ liệu
- view bị ẩn sai
- cấu hình công ty hoặc tham số hệ thống bị sai

## 2. Khi nào bắt buộc phải sửa code

Phải sửa code nếu vấn đề nằm ở:

- hàm Python trong file `.py`
- compute field
- onchange phức tạp
- override method
- logic business của module
- bug trong controller
- domain/context được dựng động từ Python
- lỗi import, dependency, service

Ví dụ:

- lỗi `Compute method failed to assign ...`
- lỗi method override
- logic duyệt sai do code
- cron chạy sai do Python

## 3. Rule nhận biết nhanh

Nếu lỗi có traceback và trỏ vào:

- `models/*.py`
- `controllers/*.py`
- `odoo/orm/fields.py`
- `odoo/orm/models.py`

thì gần như nên nghĩ tới sửa code trước.

Nếu lỗi liên quan đến:

- quyền đọc/ghi
- menu không hiện
- dữ liệu không thấy theo user
- cấu hình sai trên form setting

thì kiểm tra giao diện trước.

## 4. Với lỗi vừa gặp ở `M02_P0213_00`

Lỗi:

```python
ValueError: Compute method failed to assign approval.request(...).x_psm_0213_owner_related_activity_ids
```

Đây là lỗi compute field trong Python, nên:

- không sửa triệt để bằng giao diện được
- chỉ có thể chữa cháy bằng giao diện nếu lỗi do quyền hoặc do field đang bị gọi ở view
- cách sửa đúng là sửa code field/method trong module

## 5. Checklist trước khi sửa bằng giao diện

1. Bật `Developer Mode`
2. Kiểm tra user có phải `Internal User` không
3. Kiểm tra `Access Rights`
4. Kiểm tra `Record Rules`
5. Kiểm tra field có đang nằm trên view không
6. Kiểm tra action/menu/view có bị custom bởi Studio hay Technical không
7. Nếu mọi thứ đều đúng mà vẫn lỗi traceback Python, chuyển sang sửa code

## 6. Checklist trước khi sửa code trên server

1. Xác định đúng module đang gây lỗi
2. Xác định đúng file `.py` hoặc `.xml`
3. Kiểm tra Odoo đang chạy bản code nào
4. Kiểm tra có nhiều bản addon trùng tên không
5. Sửa đúng file mà Odoo thực sự đang dùng
6. Restart Odoo sau khi sửa
7. Test lại đúng record hoặc đúng bước gây lỗi

## 7. Cách kiểm tra Odoo đang đọc addon từ đâu

### Bước 1: kiểm tra `addons_path`

Xem file `odoo.conf`:

- local repo: `odoo.conf`
- trong container thường là: `/opt/odoo/odoo.conf`

Ví dụ:

```ini
addons_path = /mnt/extra-addons,/opt/odoo/odoo/addons
```

### Bước 2: kiểm tra có nhiều bản module trùng tên không

Ví dụ với `M02_P0213_00`:

- `/mnt/extra-addons/M02_P0213_00`
- `/opt/odoo/addons/M02_P0213_00`

Nếu có 2 bản cùng tên, rất dễ sửa nhầm.

### Bước 3: kiểm tra file đang chạy thật

Nếu traceback chỉ tới đường dẫn như:

```python
/opt/odoo/addons/M02_P0213_00/models/resignation_request.py
```

thì Odoo đang dùng bản ở đó, không phải bản local khác.

### Bước 4: nếu sửa local mà không có tác dụng

Hãy kiểm tra:

- file local có đang được mount vào container không
- Odoo có đang đọc đúng thư mục mount không
- có cần copy file sang thư mục addon khác không
- đã restart service/container chưa

## 8. Checklist deploy sau khi sửa code

1. Đồng bộ file đã sửa lên đúng nơi Odoo dùng
2. Restart service hoặc container
3. Mở lại đúng màn hình từng lỗi
4. Kiểm tra log mới
5. Nếu traceback vẫn như cũ, nghi ngờ instance chưa nạp code mới

## 9. Kết luận ngắn

- Sửa bằng giao diện phù hợp cho quyền, rule, cấu hình, view
- Sửa bằng code là bắt buộc với lỗi compute Python
- Trước khi kết luận patch không hiệu lực, phải kiểm tra Odoo đang đọc addon từ thư mục nào
