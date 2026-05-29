# Phase 5 - Triển khai protect field x_psm_0213_is_offboarding

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Source xác nhận cuối cùng:
  - `addons/M02_P0213/models/resignation_request.py`
  - `addons/M02_P0213/views/resignation_request_views.xml`
  - `addons/M02_P0213/data/approval_category_data.xml`

## Kết quả triển khai

Field `approval.category.x_psm_0213_is_offboarding` đã được bảo vệ bằng hai lớp:

1. Field-level groups:

```python
groups='approvals.group_approval_manager,base.group_system'
```

2. Backend guard trong `create()` và `write()`:

- Cho phép superuser/module data.
- Cho phép user thuộc `base.group_system`.
- Cho phép user thuộc `approvals.group_approval_manager`.
- Chặn user khác nếu cố bật/tắt `x_psm_0213_is_offboarding`, kể cả ghi trực tiếp qua RPC/API.

Không dùng mẫu `_get_stored_value()` trong tài liệu vì source/Odoo không có helper đó cho field này. Thay vào đó, `write()` so sánh giá trị hiện tại với giá trị mới trong `vals` trước khi chặn quyền.

## Kiểm tra đã chạy

- Compile Python OK:
  - `models/resignation_request.py`
- Parse XML OK:
  - `views/resignation_request_views.xml`
  - `data/approval_category_data.xml`

## Test nghiệp vụ cần chạy sau khi upgrade module

- User thường có quyền ghi `approval.category` nhưng không có `base.group_system`/`approvals.group_approval_manager`: không đổi được `x_psm_0213_is_offboarding`.
- User `approvals.group_approval_manager`: đổi được marker.
- User `base.group_system`: đổi được marker.
- Module data vẫn update được category `psm_0213_approval_category_resignation` với marker `True`.
