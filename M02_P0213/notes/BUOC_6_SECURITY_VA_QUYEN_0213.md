# Bước 6 - Security Và Quyền 0213

Ngày thực hiện: 2026-05-13

## 1. Tài liệu định hướng đã dùng

- Convention: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213/structure/module_map.json`
- Blueprint: `addons/M02_P0213/TECHNICAL_BLUEPRINT_0213.md`
- Phase 0 quyền expected: `addons/M02_P0213/notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md`
- Phase 1 group chain: `addons/M02_P0213/notes/PHASE_1_DOI_CHIEU_EXPECTED_VS_ACTUAL_GROUP_CHAIN_0213.md`
- Bước 5: `addons/M02_P0213/notes/BUOC_5_PORTAL_CONTROLLER_0213.md`

## 2. Source chính dùng để xác nhận

- `addons/M02_P0213/security/ir.model.access.csv`
- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0200/security/security.xml`

## 3. Thay đổi ACL

File sửa:

- `addons/M02_P0213/security/ir.model.access.csv`

Điều chỉnh chính:

- Gỡ quyền rộng do module này cấp cho `base.group_user` trên:
  - `approval.request`
  - `mail.activity`
  - `survey.user_input`
- Thêm ACL theo từng group 0200 cho:
  - `approval.request`
  - `approval.approver`
  - `survey.user_input`
  - `mail.activity`

Nguyên tắc áp dụng:

- Không cấp `unlink` mặc định cho nhóm 0213.
- Không mở `create` backend tràn lan cho `approval.request`.
- OPS chỉ đọc request/activity.
- HR Admin S/M, HRBP M, HR Head, System có quyền write request theo expected.
- Internal chỉ đọc survey result, không write/create/unlink survey response.
- Portal vẫn giữ quyền cần thiết trên `survey.user_input` để làm survey của chính mình, kết hợp record rule portal own.

## 4. Thay đổi record rule

File sửa:

- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/security/security.xml`

Điều chỉnh:

- Thêm rule đọc `mail.activity` theo field marker `x_psm_0213_is_offboarding_activity`.
- Thêm rule write `mail.activity` cho nhóm HR xử lý theo cùng marker.
- Chuyển `security.xml` từ `noupdate="1"` sang `noupdate="0"` để các rule survey có thể cập nhật khi upgrade module.

## 5. Thay đổi model hỗ trợ security

File sửa:

- `addons/M02_P0213/models/mail_activity.py`

Đã thêm field:

```python
x_psm_0213_is_offboarding_activity = fields.Boolean(
    string='Is 0213 Offboarding Activity',
    compute='_compute_is_offboarding_activity',
    store=True,
    compute_sudo=True,
)
```

Lý do:

- `mail.activity` dùng `res_model/res_id`, record rule XML không thể tự join tới `approval.request.category_id`.
- Field marker stored giúp rule khóa đúng activity thuộc flow offboarding 0213:
  - activity gắn trực tiếp `approval.request`
  - activity gắn `hr.employee` có request offboarding 0213 liên quan

## 6. Python group guard đã xác nhận

Các action nhạy cảm trong `models/resignation_request.py` đã có `_check_0213_group_access()`:

- `action_view_survey_results`
- `action_send_social_insurance`
- `action_send_adecco_notification`
- `action_done`
- `action_rehire`
- `action_blacklist`
- `action_manual_reminder_extension`

## 7. Residual risk cần test thực tế

- ACL là quyền cộng dồn trong Odoo. Việc siết ACL do `M02_P0213` tạo ra không tự động thu hồi quyền đến từ module lõi như `approvals`, `mail`, hoặc `survey`.
- Cần upgrade module và test bằng user thật theo từng group để xác nhận quyền thực tế sau khi cộng với quyền core.
- Các nhóm trong Phase 1 chưa chắc kéo `base.group_user`; ACL theo group 0200 đã được thêm để bám expected matrix, nhưng khả năng vào backend còn phụ thuộc group chain và cấu hình user thực tế.

## 8. Verification

- Đã parse `security/ir.model.access.csv` bằng Python `csv`.
- Kết quả: 44 ACL, không trùng ID, không thiếu cột bắt buộc.
- Đã parse XML:
  - `security/security.xml`
  - `security/offboarding_request_rules.xml`
- Đã chạy `python -m py_compile` cho:
  - `models/mail_activity.py`
  - `models/resignation_request.py`
- Chưa chạy upgrade Odoo/module và chưa test quyền bằng user thật.
