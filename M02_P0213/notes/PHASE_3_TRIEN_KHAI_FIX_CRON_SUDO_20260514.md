# Phase 3 - Triển khai fix cron job

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Source xác nhận cuối cùng:
  - `addons/M02_P0213/data/ir_cron_data.xml`
  - `addons/M02_P0213/models/resignation_request.py`

## Kết quả đối chiếu

Cron `action_psm_0213_offboarding_reminder_cron` gọi:

```xml
<field name="code">model._cron_send_offboarding_reminders()</field>
```

Method `_cron_send_offboarding_reminders()` trước Phase 3 dùng `self.search(...)`, nên vẫn phụ thuộc quyền của user chạy cron.

## Thay đổi đã triển khai

Trong `models/resignation_request.py`, thêm recordset sudo cho cron:

```python
cron_self = self.sudo()
rst_category = cron_self._get_0213_resignation_category()
...
requests = cron_self.search([...])
...
activities_by_request = cron_self._get_overdue_activities_by_request(requests, today=today)
```

Các helper xử lý activity vốn đã dùng `mail.activity.sudo()` khi search/browse activity, nên thay đổi này tập trung vào phần còn thiếu: đọc category và tìm `approval.request` offboarding bằng quyền cron an toàn.

## Kiểm tra đã chạy

- Compile Python OK:
  - `models/resignation_request.py`
- Parse XML OK:
  - `data/ir_cron_data.xml`

## Test nghiệp vụ cần chạy sau khi upgrade module

- Cron tìm được các đơn offboarding `approved` dù user chạy cron không có ACL thủ công trên `approval.request`.
- Cron gửi reminder cho activity quá hạn.
- Cron gia hạn `date_deadline` theo cấu hình công ty.
- Cron không gửi/gia hạn khi không có activity quá hạn.
