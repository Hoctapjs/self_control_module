# Ghi chú Before/After - 2026-04-17

## Phạm vi thay đổi

Thay đổi này áp dụng cho module `M02_P0214`, tập trung vào phần cấu hình email template trong màn cấu hình offboarding.

## Before

Trước khi chỉnh sửa:

- Màn cấu hình của `0214` chưa có các field để chọn email template giống `0213`.
- Logic gửi email trong `0214` vẫn đang gọi template theo kiểu hardcode bằng `env.ref(...)`.
- Người dùng không thể đổi template trực tiếp từ màn cấu hình công ty.
- Các email liên quan đến khảo sát nghỉ việc, Adecco, BHXH, nhắc việc nhân viên và nhắc việc bộ phận chưa được gom về cấu hình tập trung.

## After

Sau khi chỉnh sửa:

- Đã bổ sung các field cấu hình email template trên `res.company` cho `0214`.
- Đã bổ sung các field related tương ứng trên `res.config.settings`.
- Đã hiển thị các field này trên màn cấu hình offboarding của `0214`.
- Đã cập nhật logic để `0214` ưu tiên dùng template được cấu hình thay vì hardcode trực tiếp.
- Đã upgrade module `M02_P0214` và restart Odoo để thay đổi có hiệu lực trên hệ thống.

## Các cấu hình email đã thêm

- Email template khảo sát nghỉ việc
- Email template gửi Adecco
- Email template BHXH
- Email template nhắc việc nhân viên
- Email template nhắc việc bộ phận

## File source chính đã chỉnh

- `addons/M02_P0214/models/res_company.py`
- `addons/M02_P0214/models/res_config_settings.py`
- `addons/M02_P0214/views/res_company_views.xml`
- `addons/M02_P0214/models/approval_request_rst_fields.py`
- `addons/M02_P0214/models/approval_request_rst_survey.py`
- `addons/M02_P0214/models/approval_request_rst_reminder.py`

## Kết quả mong đợi

Sau khi reload màn hình cấu hình của `0214`, người dùng có thể:

- chọn template email ngay trên màn cấu hình
- đổi template mà không cần sửa code
- quản lý luồng email của `0214` tương tự cách đang làm ở `0213`

## Ghi chú thêm

- `module_map.json` của `0214` hiện chưa phản ánh các field mới, nên nếu cần đồng bộ tài liệu cấu trúc thì nên regenerate lại.
