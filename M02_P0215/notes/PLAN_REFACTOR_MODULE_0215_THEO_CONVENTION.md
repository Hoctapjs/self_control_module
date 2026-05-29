# Plan refactor module 0215 theo convention

## 1. Tài liệu và source đã dùng để định hướng

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xác nhận chính:
  - `addons/M02_P0215/__manifest__.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_action.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_explanation.py`
  - `addons/M02_P0215/wizards/x_psm_hr_discipline_reject_wizard.py`
  - `addons/M02_P0215/controllers/portal.py`
  - `addons/M02_P0215/views/x_psm_hr_discipline_master_views.xml`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
  - `addons/M02_P0215/security/ir.model.access.csv`

## 2. Nguyên tắc refactor

Module hiện đang dùng các model mới theo đúng prefix `x_psm...`, ví dụ `x_psm.hr.discipline.record`, `x_psm.hr.discipline.action`, `x_psm.hr.discipline.explanation`. Vì vậy vẫn giữ `_name` của các model này vì đang đúng convention và đúng business object.

Vì module chưa từng được cài trước đây, refactor có thể thực hiện theo hướng greenfield: đổi field, XML id, action id, view id, menu id, security id trực tiếp trong source mà không cần viết migration giữ dữ liệu cũ. Đây là điểm rất quan trọng vì giúp plan gọn hơn, ít lớp tương thích hơn và bám convention tốt ngay từ đầu.

Các field nghiệp vụ mới trong model mới nên dùng prefix `x_psm_`. Hiện module còn một số field chưa đúng convention như `employee_id`, `violation_type`, `discipline_purpose`, `date`, `employee_explanation`, `explanation_date`, `action_id`, `start_date`, `end_date`, `record_id`. Một số field kỹ thuật phổ biến của Odoo như `name`, `sequence`, `state`, `currency_id` có thể giữ lại nếu không gây mâu thuẫn và giúp module tự nhiên hơn với Odoo.

XML id hiện chưa bám convention: nhiều id đang là `view_hr_discipline...`, `action_hr_discipline...`, `menu_discipline...`, `access_hr_discipline...`. Theo convention, action mới nên là `action_psm_tenaction`, view mới nên là `view_psm_tenview`. Vì module chưa cài, có thể đổi trực tiếp các external id này ngay trong phase refactor chính.

Không xóa comment hiện có, đặc biệt comment tiếng Việt không dấu hoặc comment nghiệp vụ. Khi sửa code chỉ chỉnh đúng vùng cần thiết.

## 3. Phase 0 - Audit nhanh và khóa baseline

Mục tiêu: tạo danh sách chính xác các điểm lệch convention và điểm rủi ro trước khi sửa.

Việc cần làm:

- Lập bảng inventory model, field, method, view id, action id, menu id, security id, report id, template id.
- Phân loại field thành 2 nhóm: giữ nguyên theo pattern Odoo hoặc đổi sang prefix `x_psm_`.
- Đối chiếu workflow hiện tại với quy trình 19 bước đã ghi trong note nghiệp vụ.
- Ghi rõ giả định: module chưa từng cài, không cần migration dữ liệu cũ.
- Chạy kiểm tra syntax Python/XML trước khi động vào code.

Kết quả kỳ vọng:

- Có file checklist audit trong `notes`.
- Chốt danh sách rename field/XML id và baseline lỗi hiện tại.

## 4. Phase 1 - Chuẩn hóa naming theo convention

Mục tiêu: đưa model field, view id, action id, menu id, security id về convention ngay từ đầu.

Việc cần làm:

- Giữ `_name` model hiện tại vì đã đúng prefix `x_psm`.
- Đổi field nghiệp vụ sang prefix `x_psm_`:
  - `employee_id` -> `x_psm_employee_id`
  - `violation_type` -> `x_psm_violation_type`
  - `discipline_purpose` -> `x_psm_discipline_purpose`
  - `date` -> `x_psm_date`
  - `employee_explanation` -> `x_psm_employee_explanation`
  - `explanation_date` -> `x_psm_explanation_date`
  - `action_id` -> `x_psm_action_id`
  - `start_date` -> `x_psm_start_date`
  - `end_date` -> `x_psm_end_date`
  - `record_id` trong explanation -> `x_psm_record_id`
- Giữ lại `name`, `sequence`, `state`, `currency_id` nếu xem là field kỹ thuật/chung theo Odoo.
- Cập nhật toàn bộ reference trong Python, XML views, portal templates, reports, mail templates, data, cron, domains, `@api.depends`.
- Đổi external id:
  - `view_hr_discipline...` -> `view_psm_hr_discipline...`
  - `action_hr_discipline...` -> `action_psm_hr_discipline...`
  - `menu_discipline...` -> `menu_psm_hr_discipline...`
  - `access_hr_discipline...` -> `access_psm_hr_discipline...`
  - `seq_hr_discipline_record` -> `seq_psm_hr_discipline_record`
- Cập nhật action/menu/report/template references theo external id mới.

Kết quả kỳ vọng:

- Source sạch convention ngay từ lần cài đầu.
- Không có lớp alias/migration dữ liệu cũ.

## 5. Phase 2 - Dọn code và portal

Mục tiêu: tăng tính ổn định, giảm lặp code, giữ behavior nghiệp vụ sau rename.

Việc cần làm:

- Xóa `print()` debug trong `controllers/portal.py`, chuyển sang logging chuẩn nếu cần.
- Tách helper lặp trong portal:
  - lấy employee từ user
  - kiểm tra manager/RGM
  - build domain xem hồ sơ
  - browse record an toàn
- Bổ sung guard cho các route POST khi thiếu `record_id`, thiếu employee, record không tồn tại.
- Giảm `.sudo()` trong portal ở các điểm có thể kiểm tra quyền bằng domain nghiệp vụ trước khi ghi.
- Chuẩn hóa string quote và format code Python theo style nhất quán.
- Sửa lỗi view rõ ràng đang sai state: nút tạo lại quyết định bồi thường đang kiểm tra `state != 'hr_meeting'` trong khi state này không tồn tại.
- Giữ nguyên comment hiện có, chỉ bổ sung comment ngắn ở các helper phức tạp nếu cần.

Kết quả kỳ vọng:

- Portal và backend chạy ổn với naming mới.
- Các lỗi hiển nhiên về state/debug/guard được xử lý.

## 6. Phase 3 - Chuẩn hóa workflow theo quy trình 19 bước

Mục tiêu: làm state/action phản ánh đúng quy trình xử lý kỷ luật 0215.

Việc cần làm:

- Đối chiếu state hiện tại với quy trình:
  - `draft`: ghi nhận/tường trình
  - `under_review`: quản lý/RGM kiểm tra
  - `level_determination`: xác nhận Store Level/Company Level
  - `investigation`, `hearing`, `proposal`: xử lý cấp công ty
  - `approval`: CEO phê duyệt
  - `notified`: nhân viên xác nhận
  - `active`, `expired`: cập nhật hiệu lực/hết hiệu lực
- Rà lại method action hiện có để đặt đúng ý nghĩa từng bước.
- Tách helper workflow trong model record:
  - kiểm tra hình thức kỷ luật bắt buộc
  - thông báo nhân viên
  - thông báo RGM
  - tạo activity
  - chuyển state có kiểm soát
- Bổ sung constraint/guard để không nhảy state sai luồng.
- Giữ các method legacy hiện có nếu đang được view/template gọi, nhưng ghi chú rõ alias tương thích.

Kết quả kỳ vọng:

- Workflow code dễ đọc hơn và bám sát note quy trình.
- Mỗi button/action có trách nhiệm rõ ràng.
- Hạn chế trường hợp hồ sơ bị ghi state sai.

## 7. Phase 4 - Rà phân quyền tối thiểu

Mục tiêu: giảm quyền thừa và tách đúng trách nhiệm theo nhóm.

Việc cần làm:

- Rà lại `ir.model.access.csv` sau khi rename id:
  - portal đang có create/write trên `x_psm.hr.discipline.explanation`
  - SM có write/create trên record và explanation
  - HR manager có toàn quyền master data
- Xác định đúng nhóm theo convention và module `M02_P0200`.
- Tách quyền đọc master data và quyền thao tác hồ sơ.
- Bổ sung record rule nếu cần để portal/manager chỉ thấy đúng hồ sơ của mình hoặc cấp dưới.
- Kiểm tra các route đang dùng `.sudo()` để tránh bypass phân quyền không cần thiết.

Kết quả kỳ vọng:

- Quyền tối thiểu hơn.
- Portal không thể đọc/ghi hồ sơ không liên quan.

## 8. Phase 5 - Kiểm thử và regenerate structure map

Mục tiêu: xác nhận refactor không làm hỏng module và cập nhật tài liệu map.

Việc cần làm:

- Chạy kiểm tra syntax Python.
- Chạy parse XML cho view/data/report.
- Cài mới module trên database test.
- Test luồng chính:
  - quản lý tạo hồ sơ
  - nhân viên tường trình/ký
  - RGM xác nhận tái phạm/không tái phạm
  - Store Level xử lý nhanh
  - Company Level qua HR/CEO
  - nhân viên đồng ý/từ chối
  - cron hết hiệu lực
- Regenerate `structure/module_map.json` bằng `structure/build_module_map.py`.
- Ghi note before/after sau mỗi phase lớn.

Kết quả kỳ vọng:

- Module cài mới sạch.
- JSON map khớp source mới.
- Có checklist test rõ ràng trong `notes`.

## 9. Nhóm việc đã loại bỏ khỏi plan vì module chưa cài

Không cần làm các việc sau:

- Không cần migration copy dữ liệu từ field cũ sang field mới.
- Không cần alias field cũ để tương thích.
- Không cần rename `ir.model.data` trong database.
- Không cần giữ external id cũ để upgrade database đã cài.

## 10. Thứ tự khuyến nghị mới

Nên thực hiện theo thứ tự:

1. Phase 0: audit nhanh và khóa baseline.
2. Phase 1: chuẩn hóa naming field/XML id/security id.
3. Phase 2: dọn code và portal.
4. Phase 3: chuẩn hóa workflow theo quy trình 19 bước.
5. Phase 4: rà phân quyền tối thiểu.
6. Phase 5: test cài mới và regenerate map.

Nếu cần triển khai ngay, bắt đầu từ Phase 1 là hợp lý nhất vì module chưa cài, đổi naming sớm sẽ tránh kéo theo nợ kỹ thuật sang các phase sau.

<!-- Nội dung cũ bên dưới được giữ tạm để đối chiếu, sẽ xóa khi bắt đầu refactor thực tế. -->

## Nội dung plan cũ - không ưu tiên

### Phase cũ - Chuẩn hóa naming field nghiệp vụ có migration nhẹ

Mục tiêu: đưa field nghiệp vụ trong model mới về prefix `x_psm_` theo convention, nhưng không làm gãy dữ liệu.

Việc cần làm:

- Đề xuất mapping field:
  - `employee_id` -> `x_psm_employee_id`
  - `violation_type` -> `x_psm_violation_type`
  - `discipline_purpose` -> `x_psm_discipline_purpose`
  - `employee_explanation` -> `x_psm_employee_explanation`
  - `explanation_date` -> `x_psm_explanation_date`
  - `action_id` -> `x_psm_action_id`
  - `start_date` -> `x_psm_start_date`
  - `end_date` -> `x_psm_end_date`
  - `record_id` trong explanation/wizard -> `x_psm_record_id`
- Giữ lại các field kỹ thuật phổ biến nếu cần: `name`, `sequence`, `state`.
- Nếu database đã có dữ liệu, dùng migration/pre-init hoặc post-init để copy dữ liệu từ cột cũ sang cột mới.
- Cập nhật toàn bộ model, view, report, mail template, portal template, controller, domain, depends, search.
- Chạy upgrade module trên database test trước.

Kết quả kỳ vọng:

- Field nghiệp vụ bám convention hơn.
- Có đường migration rõ, không mất dữ liệu cũ.

## 7. Phase 4 - Chuẩn hóa XML id/action/view/menu/security id

Mục tiêu: đưa external id về convention `view_psm...`, `action_psm...`, menu/security id có prefix PSM rõ ràng.

Việc cần làm:

- Đề xuất mapping:
  - `view_hr_discipline_record_form` -> `view_psm_hr_discipline_record_form`
  - `view_hr_discipline_record_tree` -> `view_psm_hr_discipline_record_tree`
  - `action_hr_discipline_record_main` -> `action_psm_hr_discipline_record_main`
  - `menu_discipline_root` -> `menu_psm_hr_discipline_root`
  - `access_hr_discipline_record_sm` -> `access_psm_hr_discipline_record_sm`
- Cập nhật tất cả reference trong XML.
- Nếu module đã cài, chuẩn bị migration `ir.model.data` để rename external id thay vì tạo record mới trùng.
- Cập nhật `structure/module_map.json` sau khi đổi.

Kết quả kỳ vọng:

- XML id/action/view/menu/security bám convention.
- Không tạo trùng menu/action/view khi upgrade.

## 8. Phase 5 - Rà phân quyền tối thiểu

Mục tiêu: giảm quyền thừa và tách đúng trách nhiệm theo nhóm.

Việc cần làm:

- Rà lại `ir.model.access.csv` hiện tại:
  - portal đang có create/write trên `x_psm.hr.discipline.explanation`
  - SM có write/create trên record và explanation
  - HR manager có toàn quyền master data
- Xác định đúng nhóm theo convention và module `M02_P0200`.
- Tách quyền đọc master data và quyền thao tác hồ sơ.
- Bổ sung record rule nếu cần để portal/manager chỉ thấy đúng hồ sơ của mình hoặc cấp dưới.
- Kiểm tra các route đang dùng `.sudo()` để tránh bypass phân quyền không cần thiết.

Kết quả kỳ vọng:

- Quyền tối thiểu hơn.
- Portal không thể đọc/ghi hồ sơ không liên quan.

## 9. Phase 6 - Kiểm thử và regenerate structure map

Mục tiêu: xác nhận refactor không làm hỏng module và cập nhật tài liệu map.

Việc cần làm:

- Chạy kiểm tra syntax Python.
- Chạy parse XML cho view/data/report.
- Upgrade module trên database test.
- Test luồng chính:
  - quản lý tạo hồ sơ
  - nhân viên tường trình/ký
  - RGM xác nhận tái phạm/không tái phạm
  - Store Level xử lý nhanh
  - Company Level qua HR/CEO
  - nhân viên đồng ý/từ chối
  - cron hết hiệu lực
- Regenerate `structure/module_map.json` bằng `structure/build_module_map.py`.
- Ghi note before/after sau mỗi phase lớn.

Kết quả kỳ vọng:

- Module upgrade sạch.
- JSON map khớp source mới.
- Có checklist test rõ ràng trong `notes`.

## 10. Thứ tự khuyến nghị

Nên thực hiện theo thứ tự:

1. Phase 0: audit.
2. Phase 1: refactor an toàn không đổi schema.
3. Phase 2: chuẩn hóa workflow.
4. Phase 5: phân quyền tối thiểu.
5. Phase 6: test/regenerate map.
6. Phase 3 và Phase 4 chỉ làm sau khi xác nhận chiến lược migration, vì có rủi ro ảnh hưởng dữ liệu đã cài.

Nếu cần đi nhanh, có thể bắt đầu ngay bằng Phase 1 vì ít rủi ro nhất và xử lý được các lỗi rõ ràng như debug `print()`, route guard, helper portal và state `hr_meeting` không tồn tại.
