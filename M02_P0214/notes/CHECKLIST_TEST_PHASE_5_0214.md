# Checklist Test Phase 5 - 0214

## 1. Mục tiêu

Checklist này dùng để xác nhận các thay đổi bảo mật sau giai đoạn 1-4 không phá vỡ luồng nghiệp vụ chính của module `M02_P0214`.

## 2. Automated tests

Đã bổ sung test package:

- `tests/__init__.py`
- `tests/test_security_hardening.py`

Các nhóm kiểm tra tự động:

- ACL trùng `mail.activity` và `approval.request` của module 0214 đã được cleanup.
- ACL `hr.contract.type` và `x_psm_resignation_type` của `base.group_user` chỉ còn read-only.
- Direct manager record rule không còn áp cho toàn bộ `base.group_user`.
- `_check_0214_group_access()` chặn user không đủ quyền khi gọi từ empty recordset hoặc `@api.model`.
- `mail.activity` của 0214 không còn override `unlink()` toàn cục.
- View báo cáo offboarding và field `x_psm_0214_is_rst_employee` có group hardening.

## 3. UAT tối thiểu cần chạy trên database

### 3.1. User test mẫu

File data mẫu: `data/test_security_users.xml`

Tất cả user dưới đây có password: `123`

| Persona | Login |
| --- | --- |
| Regular User | `0214_regular` |
| HR Admin Staff | `0214_hr_admin_s` |
| HR Admin Manager | `0214_hr_admin_m` |
| HR HRBP Staff | `0214_hr_hrbp_s` |
| HR HRBP Manager | `0214_hr_hrbp_m` |
| HR Head | `0214_hr_head` |
| System Manager | `0214_system_manager` |
| Store Manager | `0214_store_manager` |
| Portal User | `0214_portal` |

### 3.2. Checklist UAT

1. User thường `base.group_user` không thấy menu Offboarding Report.
2. HRBP/HR Head thấy được Offboarding Report.
3. HR Admin Staff không thấy field `x_psm_0214_is_rst_employee` trên form nhân viên.
4. HR Head hoặc System Manager thấy field `x_psm_0214_is_rst_employee`.
5. Regular user không tạo/sửa/xóa được `hr.contract.type`.
6. Regular user không tạo/sửa/xóa được `x_psm_resignation_type`.
7. Người không thuộc nhóm report RST không gọi được báo cáo offboarding.
8. HR Head/System Manager không bị auto deactivate khi hoàn tất quy trình.
9. Report Offboarding hiển thị toàn bộ request RST đang `approved` và còn pending survey/checklist, không phụ thuộc cấp dưới.
10. Mark done activity RST vẫn archive activity và recompute checklist.
11. Xóa activity ngoài RST vẫn đi theo hành vi chuẩn của Odoo/module khác.

## 4. Lệnh chạy gợi ý

```bash
python odoo-bin -d <db_name> --test-tags /M02_P0214:m02_p0214_security --stop-after-init
```
