# Phase 2 - Triển khai fix ACL hr.employee

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Source xác nhận cuối cùng:
  - `addons/M02_P0213/security/ir.model.access.csv`

## Kết quả triển khai

### Bước 7

`access_hr_employee_internal_user` hiện là read-only:

```csv
access_hr_employee_internal_user,hr.employee.internal.user,hr.model_hr_employee,base.group_user,1,0,0,0
```

Lưu ý: dòng này đã được hạ về read-only trong Phase 1, Phase 2 kiểm tra lại và giữ nguyên.

### Bước 8

Đã thêm ACL write cho HR Admin và HRBP manager theo XML id thực tế của module 0200:

```csv
access_hr_employee_hr_admin,hr.employee.hr.admin,hr.model_hr_employee,M02_P0200.GDH_RST_HR_ADMIN_M,1,1,0,0
access_hr_employee_hr_hrbp,hr.employee.hr.hrbp,hr.model_hr_employee,M02_P0200.GDH_RST_HR_HRBP_M,1,1,0,0
```

Không cấp create/unlink để giữ nguyên tắc minimum permission.

## Kiểm tra source

Trong `M02_P0213`, các ACL write trực tiếp trên `hr.employee` hiện chỉ còn:

- `M02_P0200.GDH_RST_HR_ADMIN_M`
- `M02_P0200.GDH_RST_HR_HRBP_M`

`base.group_user` và các group OPS không có write trên `hr.employee` từ module 0213.

## Test nghiệp vụ cần chạy sau khi upgrade module

- User chỉ có `base.group_user`: đọc được `hr.employee`, không sửa được.
- User có `M02_P0200.GDH_RST_HR_ADMIN_M`: đọc và sửa được `hr.employee`, không tạo/xóa được nhờ ACL 1/1/0/0.
- User có `M02_P0200.GDH_RST_HR_HRBP_M`: đọc và sửa được `hr.employee`, không tạo/xóa được nhờ ACL 1/1/0/0.
- User có `M02_P0200.GDH_RST_OPS_OC_S`: không có write `hr.employee` từ module 0213.
