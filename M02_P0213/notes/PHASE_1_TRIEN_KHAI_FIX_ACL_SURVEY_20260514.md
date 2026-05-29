# Phase 1 - Triển khai fix ACL Survey

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Source xác nhận cuối cùng:
  - `addons/M02_P0213/security/ir.model.access.csv`
  - `addons/M02_P0213/security/security.xml`
  - `addons/M02_P0213/models/survey_user_input.py`
  - `addons/M02_P0213/data/survey_exit_interview_data.xml`

## Thay đổi đã triển khai

### ACL

- Xóa ACL không có tác dụng:
  - `access_mail_activity_internal_user` 0/0/0/0
  - `access_approval_request_internal_user` 0/0/0/0
- Hạ quyền nền:
  - `access_hr_employee_internal_user`: từ 1/1/0/0 về 1/0/0/0
  - `access_hr_contract_type_internal_user`: từ 1/1/0/0 về 1/0/0/0
- Survey ACL:
  - `base.group_user` chỉ read `survey.survey`, `survey.question`, `survey.question.answer`, `survey.user_input`
  - `base.group_portal` giữ read/create/write trên `survey.user_input` để Odoo Survey có thể ghi câu trả lời, nhưng được scope lại bằng record rule
  - HR Admin S/M, HRBP M, System M có create/write trên `survey.user_input`, nhưng chỉ hiệu lực trong record rule exit interview
  - OPS OM, HRBP S, HR Head chỉ read kết quả survey

### Record rule

- Thêm `base.group_user` vào các rule read survey/question/question_answer/user_input để người dùng nội bộ không đọc lan sang survey khác.
- Siết rule portal `rule_0213_survey_user_input_portal_own`:
  - chỉ survey có `survey_id.x_psm_0213_is_exit_survey = True`
  - chỉ record của chính portal user qua `partner_id` hoặc `email`
  - không unlink
- Thêm rule `rule_0213_survey_user_input_internal_write` cho HR/System create/write user_input của exit interview.

### Field hỗ trợ scope

- Thêm field `survey.survey.x_psm_0213_is_exit_survey`.
- Đánh dấu survey `psm_0213_survey_exit_interview` bằng `x_psm_0213_is_exit_survey=True`.

Lý do: tài liệu rà soát đã giả định có field này; source hiện tại chưa có. Dùng field này giúp rule portal vừa lọc đúng exit survey vừa dùng được điều kiện `user.partner_id/user.email` ở runtime.

## Kiểm tra đã chạy

- Parse XML OK:
  - `security/security.xml`
  - `data/survey_exit_interview_data.xml`
- Compile Python OK:
  - `models/survey_user_input.py`
- CSV không còn dòng ACL 0/0/0/0.
- Đã regenerate `structure/module_map.json` và details cho `M02_P0213`.

## Test nghiệp vụ cần chạy sau khi upgrade module

- `base.group_user`: chỉ read survey exit interview, không create/write survey.user_input.
- `GDH_RST_HR_ADMIN_M`: create/write `survey.user_input` cho exit interview được, không create/write survey khác.
- `GDH_RST_HR_HRBP_M`: create/write `survey.user_input` cho exit interview được, không create/write survey khác.
- `base.group_portal`: ghi câu trả lời cho exit interview của chính mình được.
- `base.group_portal`: không ghi/tạo user_input cho survey khác hoặc cho người khác.
