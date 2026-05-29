# Phase 4 - Triển khai chuẩn hóa tên rule survey

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Source xác nhận cuối cùng:
  - `addons/M02_P0213/security/security.xml`

## Kết quả triển khai

Đã đổi XML id các rule survey trong `security/security.xml` từ prefix `rule_psm_0213_*` sang prefix thống nhất `rule_0213_*`.

| Trước | Sau |
| --- | --- |
| `rule_psm_0213_survey_internal_read` | `rule_0213_survey_internal_read` |
| `rule_psm_0213_survey_question_internal_read` | `rule_0213_survey_question_internal_read` |
| `rule_psm_0213_survey_question_answer_internal_read` | `rule_0213_survey_question_answer_internal_read` |
| `rule_psm_0213_survey_user_input_portal_own` | `rule_0213_survey_user_input_portal_own` |
| `rule_psm_0213_survey_user_input_internal_write` | `rule_0213_survey_user_input_internal_write` |
| `rule_psm_0213_survey_user_input_internal_results_read` | `rule_0213_survey_user_input_internal_results_read` |

Tài liệu Phase 4 gốc liệt kê 5 rule cũ; source hiện tại có thêm `rule_psm_0213_survey_user_input_internal_write` được tạo ở Phase 1, nên đã chuẩn hóa luôn rule này để không còn lẫn prefix.

## Kiểm tra đã chạy

- Parse XML OK:
  - `security/security.xml`
- Tìm trong source runtime (`security`, `models`, `views`, `data`, `controllers`) không còn `rule_psm_0213_survey*`.
- Đã regenerate `structure/module_map.json` và details cho `M02_P0213`.

## Lưu ý khi upgrade DB

Đổi XML id trong source có thể tạo external id/rule mới nếu database đã từng cài các id cũ. Sau khi update module, nên kiểm tra `ir.rule` và `ir.model.data` để đảm bảo không còn rule survey cũ bị trùng với rule mới.
