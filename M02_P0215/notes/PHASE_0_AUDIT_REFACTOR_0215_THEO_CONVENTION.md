# Phase 0 - Audit refactor module 0215 theo convention

## 1. Phạm vi và giả định

Phase 0 chỉ audit, khóa baseline và lập danh sách việc cho Phase 1. Chưa refactor source trong phase này.

Giả định đã chốt với người dùng: module `M02_P0215` chưa từng được cài trên database. Vì vậy từ Phase 1 có thể đổi trực tiếp field, XML id, action id, menu id, security id trong source mà không cần migration dữ liệu cũ hoặc giữ alias tương thích.

## 2. Tài liệu đã dùng

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Plan hiện hành: `addons/M02_P0215/notes/PLAN_REFACTOR_MODULE_0215_THEO_CONVENTION.md`

Source chính đã xác nhận:

- `addons/M02_P0215/__manifest__.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_action.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_explanation.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_violation.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_violation_category.py`
- `addons/M02_P0215/wizards/x_psm_hr_discipline_reject_wizard.py`
- `addons/M02_P0215/controllers/portal.py`
- `addons/M02_P0215/views/x_psm_hr_discipline_master_views.xml`
- `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
- `addons/M02_P0215/views/x_psm_hr_discipline_reject_wizard_views.xml`
- `addons/M02_P0215/views/x_psm_portal_templates.xml`
- `addons/M02_P0215/security/ir.model.access.csv`
- `addons/M02_P0215/reports/x_psm_discipline_reports.xml`

## 3. Baseline kiểm tra kỹ thuật

Kết quả Phase 0:

- Python compile: OK, không thấy lỗi syntax trong các file `.py` của module.
- XML parse: OK cho toàn bộ XML trong `data`, `views`, `reports`.
- Structure map hiện tại còn phản ánh naming cũ; sau refactor cần regenerate bằng `structure/build_module_map.py`.
- Lệnh `rg` inventory XML có một lần bị PowerShell xử lý quote sai, đã chạy lại và thu được danh sách cần thiết.

## 4. Inventory model

Các model mới hiện đều dùng `_name` đúng prefix `x_psm`:

| File | Model | Kết luận |
|---|---|---|
| `models/x_psm_hr_discipline_record.py` | `x_psm.hr.discipline.record` | Giữ nguyên |
| `models/x_psm_hr_discipline_action.py` | `x_psm.hr.discipline.action` | Giữ nguyên |
| `models/x_psm_hr_discipline_explanation.py` | `x_psm.hr.discipline.explanation` | Giữ nguyên |
| `models/x_psm_hr_discipline_violation.py` | `x_psm.hr.discipline.violation.type` | Giữ nguyên |
| `models/x_psm_hr_discipline_violation_category.py` | `x_psm.hr.discipline.violation.category` | Giữ nguyên |
| `wizards/x_psm_hr_discipline_reject_wizard.py` | `x_psm.hr.discipline.reject.wizard` | Giữ nguyên |

Không có model gốc bị đổi tên sai trong module này.

## 5. Field cần đổi sang prefix `x_psm_`

Nhóm field nghiệp vụ cần đổi trong Phase 1:

| Field hiện tại | Đề xuất mới | File chính | Ghi chú |
|---|---|---|---|
| `employee_id` | `x_psm_employee_id` | `models/x_psm_hr_discipline_record.py` | Được dùng rất rộng trong model, portal, views, reports, mail templates |
| `violation_type` | `x_psm_violation_type` | `models/x_psm_hr_discipline_record.py` | Được dùng trong portal, views, reports |
| `discipline_purpose` | `x_psm_discipline_purpose` | `models/x_psm_hr_discipline_record.py` | Được dùng trong portal create và form view |
| `date` | `x_psm_date` | `models/x_psm_hr_discipline_record.py` | Cần cập nhật `_order`, search sort, onchange, report/template |
| `employee_explanation` | `x_psm_employee_explanation` | `models/x_psm_hr_discipline_record.py` | Có vẻ ít dùng, vẫn nên chuẩn hóa |
| `explanation_date` | `x_psm_explanation_date` | `models/x_psm_hr_discipline_record.py` | Có vẻ ít dùng, vẫn nên chuẩn hóa |
| `action_id` | `x_psm_action_id` | `models/x_psm_hr_discipline_record.py` | Được dùng rộng trong workflow, view, report, mail template |
| `start_date` | `x_psm_start_date` | `models/x_psm_hr_discipline_record.py` | Cần cập nhật compute và portal template |
| `end_date` | `x_psm_end_date` | `models/x_psm_hr_discipline_record.py` | Cần cập nhật compute, cron, view |
| `record_id` | `x_psm_record_id` | `models/x_psm_hr_discipline_explanation.py` | Cần cập nhật One2many inverse trong record |

Nhóm field có thể giữ theo pattern Odoo:

- `name`
- `sequence`
- `state`
- `currency_id`

Lưu ý: `wizards/x_psm_hr_discipline_reject_wizard.py` đã có `x_psm_record_id`, không cần đổi.

## 6. Reference cần cập nhật khi đổi field

Các khu vực phải cập nhật đồng bộ trong Phase 1:

- Python model:
  - `_order`
  - `@api.depends`
  - `@api.onchange`
  - domain search
  - `write()` vals
  - helper notify/activity/report
  - cron `_x_psm_cron_auto_expire`
- Controller portal:
  - route create
  - list domain
  - security check employee/manager
  - sort order
  - POST hidden `record_id`
- Backend views:
  - list/form/kanban/search fields
  - search filters/group by
  - domains như `action_id.x_psm_level`
- Portal templates:
  - list card
  - create form input names
  - detail view
  - response forms
- Reports:
  - `o.employee_id`
  - `o.action_id`
  - `o.violation_type`
- Mail templates:
  - `object.employee_id`
  - `object.action_id`
  - `object.date`

## 7. XML id/action/view/menu/security cần đổi

Nhóm view/action/menu chính chưa đúng convention:

| Hiện tại | Đề xuất Phase 1 |
|---|---|
| `view_hr_discipline_violation_category_tree` | `view_psm_hr_discipline_violation_category_tree` |
| `view_hr_discipline_violation_category_form` | `view_psm_hr_discipline_violation_category_form` |
| `action_hr_discipline_violation_category` | `action_psm_hr_discipline_violation_category` |
| `view_hr_discipline_violation_type_tree` | `view_psm_hr_discipline_violation_type_tree` |
| `view_hr_discipline_violation_type_form` | `view_psm_hr_discipline_violation_type_form` |
| `action_hr_discipline_violation_type` | `action_psm_hr_discipline_violation_type` |
| `view_hr_discipline_action_tree` | `view_psm_hr_discipline_action_tree` |
| `view_hr_discipline_action_form` | `view_psm_hr_discipline_action_form` |
| `action_hr_discipline_action` | `action_psm_hr_discipline_action` |
| `menu_discipline_root` | `menu_psm_hr_discipline_root` |
| `menu_discipline_configuration` | `menu_psm_hr_discipline_configuration` |
| `menu_discipline_violation_category` | `menu_psm_hr_discipline_violation_category` |
| `menu_discipline_violation_type` | `menu_psm_hr_discipline_violation_type` |
| `menu_discipline_action` | `menu_psm_hr_discipline_action` |
| `seq_hr_discipline_record` | `seq_psm_hr_discipline_record` |
| `view_hr_discipline_record_tree` | `view_psm_hr_discipline_record_tree` |
| `view_hr_discipline_record_form` | `view_psm_hr_discipline_record_form` |
| `view_hr_discipline_record_kanban` | `view_psm_hr_discipline_record_kanban` |
| `view_hr_discipline_record_search` | `view_psm_hr_discipline_record_search` |
| `action_hr_discipline_record_main` | `action_psm_hr_discipline_record_main` |
| `menu_discipline_record_main` | `menu_psm_hr_discipline_record_main` |
| `hr_discipline_reject_wizard_form` | `view_psm_hr_discipline_reject_wizard_form` |

Nhóm security id trong `ir.model.access.csv` cần đổi từ `access_hr_discipline...` sang `access_psm_hr_discipline...`.

Nhóm seed data nên cân nhắc đổi cho nhất quán:

- `action_store_feedback` -> `x_psm_action_store_feedback`
- `action_store_counseling_1` -> `x_psm_action_store_counseling_1`
- `action_store_counseling_2` -> `x_psm_action_store_counseling_2`
- `action_company_oral_warning` -> `x_psm_action_company_oral_warning`
- `action_company_written_warning` -> `x_psm_action_company_written_warning`
- `action_company_wage_delay` -> `x_psm_action_company_wage_delay`
- `action_company_termination` -> `x_psm_action_company_termination`
- `violation_category_*` -> `x_psm_violation_category_*`
- `violation_type_*` -> `x_psm_violation_type_*`

Nhóm report/template hiện chưa bắt buộc theo convention view/action, nhưng nên đổi nếu muốn sạch hoàn toàn:

- `action_report_disciplinary_decision_final`
- `action_report_compensation_decision_final`
- `email_template_ask_explanation`
- `email_template_explanation_rejected`
- `email_template_discipline_done`
- `email_template_discipline_notified`
- portal template id như `portal_my_disciplines`, `portal_discipline_create`, `portal_discipline_explanation_template`

## 8. Baseline lỗi/rủi ro phát hiện

Các điểm nên xử lý ở Phase 2 hoặc cùng Phase 1 nếu đụng đúng file:

- `controllers/portal.py` còn `print()` debug ở `_prepare_home_portal_values`.
- Portal dùng nhiều `.sudo()`, cần rà lại theo nguyên tắc phân quyền tối thiểu.
- `views/x_psm_hr_discipline_record_views.xml` có điều kiện `state != 'hr_meeting'`, trong khi state `hr_meeting` không tồn tại.
- `controllers/portal.py` có comment nhắc `manager_review`, state này cũng không tồn tại. Đây là comment/logic cũ, khi dọn code cần xử lý nhưng không xóa comment tùy tiện.
- Route POST đang ép `int(post.get("record_id"))` ở nhiều nơi, thiếu guard nếu request thiếu dữ liệu.
- `feature_summary` trong `module_map.json` có vẻ bị lệch nội dung sang recruitment, không khớp module discipline. Sau refactor cần regenerate map.
- Manifest đang là `"M02_P0215_00 Disciplinary Process"`; theo convention manifest không cần version. Vì module chưa cài, nên cân nhắc đổi thành dạng `M02_P0215_DISCIPLINARY_PROCESS` hoặc tên tiếng Việt/viết hoa thống nhất.

## 9. Đối chiếu nhanh workflow hiện tại với quy trình 19 bước

State hiện tại:

- `draft`: ghi nhận/tường trình ban đầu.
- `under_review`: quản lý/RGM kiểm tra.
- `level_determination`: xác định Store Level hoặc Company Level.
- `investigation`: xác minh nâng cao cấp công ty.
- `hearing`: họp kỷ luật.
- `proposal`: đề xuất kỷ luật.
- `issued`: ban hành quyết định.
- `approval`: CEO phê duyệt.
- `notified`: thông báo/nhân viên xác nhận.
- `active`: đang hiệu lực.
- `expired`: hết hiệu lực.
- `cancel`: hủy.

Nhận xét:

- State hiện tại bao phủ tương đối đủ các chặng chính.
- Quy trình 19 bước mới có bước MIC feedback ngay và bước cập nhật hồ sơ nhân viên; code hiện tại có action feedback qua `x_psm_form_code = feedback`, nhưng cần làm rõ mapping với MIC trong Phase 3.
- Store Level hiện đi nhanh từ proposal sang active qua `action_psm_activate_store_discipline`; cần đối chiếu lại với bước nhân viên ký/xác nhận.
- Company Level hiện có `approval` và `notified`, phù hợp hướng CEO duyệt rồi nhân viên xác nhận.

## 10. Checklist Phase 1

- [ ] Đổi field nghiệp vụ sang `x_psm_`.
- [ ] Cập nhật toàn bộ Python references.
- [ ] Cập nhật backend views.
- [ ] Cập nhật portal templates và controller.
- [ ] Cập nhật reports và mail templates.
- [ ] Đổi XML id view/action/menu/sequence/wizard view.
- [ ] Đổi security id trong CSV.
- [ ] Cân nhắc đổi seed data id cho thống nhất.
- [ ] Chạy Python compile.
- [ ] Chạy XML parse.
- [ ] Chạy regenerate `structure/module_map.json`.

## 11. Kết luận Phase 0

Phase 0 hoàn tất. Module đủ điều kiện bước sang Phase 1 theo hướng refactor greenfield, ưu tiên đổi naming toàn diện trước khi dọn portal/workflow sâu hơn.
