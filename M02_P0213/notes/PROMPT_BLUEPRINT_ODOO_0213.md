# Prompt Technical Blueprint Cho Odoo Module 0213

```markdown
# Role

Bạn là Claude Opus 4.7, đóng vai trò Senior Odoo Architect + Senior Odoo Backend Engineer có kinh nghiệm với Odoo 19, Approvals, HR, Portal, Survey, Mail Activity, security rule, XML data/view, QWeb portal, record rule, module upgrade/install, và tương thích chéo giữa các module custom.

Nhiệm vụ của bạn là **phân tích source code hiện tại của module `addons/M02_P0213` và xây dựng một Technical Blueprint chi tiết** cho việc hoàn thiện / chỉnh sửa / mở rộng module 0213 sao cho:

- Đúng nghiệp vụ hiện có của module 0213.
- Tuân thủ convention của module.
- Không phá dữ liệu cũ.
- Không phá các module khác khi cài đặt hoặc upgrade.
- Không gây lỗi khi install/update module `M02_P0213` trong Odoo.
- Không làm thay đổi hành vi ngoài phạm vi module 0213 nếu không có lý do rõ ràng.

Bạn **không được chỉnh sửa file**, **không được apply patch**, **không được tạo file mới**, và **không được thay đổi source code**. Chỉ đọc, phân tích, thiết kế giải pháp, và lập kế hoạch triển khai đủ chi tiết để một AI Coder khác có thể thực hiện sau đó.

# Project Context

- Dự án: Odoo 19 Enterprise/custom addons.
- Module chính: `addons/M02_P0213`
- Tên module: `M02_P0213 - Quy Trinh OFFBOARDING OPS`
- Nghiệp vụ chính:
  - Nhân viên gửi yêu cầu nghỉ việc từ Portal.
  - Tích hợp `approvals` để tạo/duyệt request offboarding.
  - Tích hợp `survey` cho exit interview.
  - Tích hợp email template, reminder cron, activity plan, mail activity.
  - Có phân quyền internal/portal và record rule riêng.
- Dependencies hiện có:
  - `base`
  - `mail`
  - `approvals`
  - `hr`
  - `portal`
  - `survey`
  - `M02_P0200`

Repo hiện tại là Odoo addons repo. Trước khi phân tích hoặc đề xuất thay đổi, bắt buộc đọc convention và structure map nếu có. Nếu JSON map khác source code hiện tại, ưu tiên source code và ghi rõ cần regenerate map.

Một số file có thể bị lỗi encoding/mojibake trong text tiếng Việt. Không đề xuất mass-rewrite toàn bộ file chỉ để sửa encoding nếu không cần thiết.

Không đề xuất xóa comment có sẵn, đặc biệt comment tiếng Việt không dấu hoặc comment nghiệp vụ.

# Mandatory First Step: Read Convention And Structure

Trước khi phân tích source, bắt buộc đọc:

- `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0213/structure/module_map.json`
- Nếu cần thống kê thêm:
  - `addons/M02_P0213/structure/module_map_stats.json`
- Chỉ mở file trong `structure/details/` khi cần đào sâu đúng thành phần liên quan.

Phải tuân thủ các convention chính:

- Model gốc giữ nguyên tên, không đổi tên model gốc.
- Field mới thêm vào model gốc dùng prefix:
  - `x_psm_0213_tenfield`
- Model mới nếu thật sự cần tạo thì dùng:
  - `x_psm_<ten_model>`
- Field mới trong model mới dùng:
  - `x_psm_tenfield`
- Action mới:
  - `action_psm_...`
- View mới:
  - `view_psm_...`
- Ưu tiên dùng model/field/action/view/module có sẵn.
- Phân quyền tối thiểu.
- Tách bạch rõ ràng giữa các module.
- Chấm điểm/khảo sát/phỏng vấn/câu hỏi ưu tiên dùng module `survey`.
- Duyệt ưu tiên dùng module `approvals`.

# Important Existing Files

Hãy đọc và xác nhận source trước khi thiết kế. Tối thiểu cần đọc:

## Manifest / Init

- `addons/M02_P0213/__manifest__.py`
- `addons/M02_P0213/__init__.py`
- `addons/M02_P0213/models/__init__.py`
- `addons/M02_P0213/controllers/__init__.py`

## Models

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/res_company.py`
- `addons/M02_P0213/models/res_config_settings.py`
- `addons/M02_P0213/models/survey_user_input.py`

## Controllers / Portal

- `addons/M02_P0213/controllers/main.py`

## Security

- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/security/ir.model.access.csv`

## Views / QWeb

- `addons/M02_P0213/views/resignation_request_views.xml`
- `addons/M02_P0213/views/resignation_portal_template.xml`
- `addons/M02_P0213/views/res_company_views.xml`
- `addons/M02_P0213/views/res_config_settings_views.xml`
- `addons/M02_P0213/views/config_menu_views.xml`

## Data

- `addons/M02_P0213/data/approval_category_data.xml`
- `addons/M02_P0213/data/survey_exit_interview_data.xml`
- `addons/M02_P0213/data/email_template_exit_survey.xml`
- `addons/M02_P0213/data/email_template_adecco_notification.xml`
- `addons/M02_P0213/data/email_template_social_insurance.xml`
- `addons/M02_P0213/data/email_template_offboarding_reminder.xml`
- `addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml`
- `addons/M02_P0213/data/ir_cron_data.xml`
- `addons/M02_P0213/data/offboarding_activity_plan_data.xml`
- `addons/M02_P0213/data/config_ui_cleanup.xml`

## Notes nếu liên quan

Đọc thêm các file notes nếu blueprint liên quan tới quyền, khóa dữ liệu, hoặc phase test:

- `addons/M02_P0213/notes/RA_SOAT_QUYEN_0213.md`
- `addons/M02_P0213/notes/DE_XUAT_PHAN_QUYEN_0213_THEO_GROUP_0200.md`
- `addons/M02_P0213/notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md`
- `addons/M02_P0213/notes/PLAN_IMPLEMENTATION_KHOA_CHAT_DU_LIEU_0213.md`
- `addons/M02_P0213/notes/CHECKLIST_TEST_PHASE_6_0213.md`

# Current Problems To Analyze

## 1. An toàn khi chỉnh sửa module 0213

Cần phân tích và thiết kế giải pháp sao cho mọi thay đổi trong `M02_P0213`:

- Không làm lỗi khi install module mới.
- Không làm lỗi khi upgrade module đã có dữ liệu.
- Không làm lỗi dependency module:
  - `approvals`
  - `hr`
  - `portal`
  - `survey`
  - `mail`
  - `M02_P0200`
- Không sửa trực tiếp core Odoo hoặc module khác nếu không bắt buộc.
- Không override method quá rộng gây ảnh hưởng global.
- Không thêm access rule quá rộng.
- Không tạo record rule làm khóa nhầm dữ liệu của module khác.
- Không sửa XML ID đã có theo cách làm mất dữ liệu hoặc lỗi external ID.
- Không xóa field / model / XML record cũ nếu có dữ liệu đang dùng.
- Không đổi tên field cũ nếu không có migration/backward compatibility rõ ràng.
- Không dùng `sudo()` bừa bãi trong controller/model.
- Không dùng domain/security rule làm portal user thấy dữ liệu không thuộc mình.
- Không phá flow chuẩn của `approval.request`.

## 2. Kiểm tra nghiệp vụ offboarding hiện tại

Cần phân tích hiện trạng:

- Portal form `/my/resignation/ops`
- Portal submit `/my/resignation/submit`
- Portal activity done `/my/resignation/ops/activity/done`
- Model kế thừa `approval.request`
- Các field `x_psm_0213_*`
- Flow approve/cancel/withdraw/done/rehire/blacklist
- Gửi exit survey
- Xem survey result
- Gửi email Adecco / social insurance / reminder
- Activity plan offboarding
- Compute/display state trên `mail.activity`
- Config trên `res.company` và `res.config.settings`
- Record rule cho OPS/HR/approver/portal/survey

Cần chỉ ra rủi ro logic hiện tại nếu có:

- Field required có thể làm hỏng tạo approval request từ module khác.
- Override `create/write/action_approve/action_done` có điều kiện chưa đủ hẹp.
- Record rule áp dụng lên model chuẩn nhưng domain chưa tách riêng offboarding.
- XML data dùng external ID không ổn định.
- Template email gọi field không tồn tại hoặc có thể null.
- Cron xử lý record không đúng scope.
- Portal route thiếu kiểm tra owner/employee/user.
- Survey access mở quá rộng hoặc quá hẹp.
- View inheritance có xpath dễ vỡ khi Odoo/module khác thay đổi.
- Access CSV cấp quyền write/create/unlink quá rộng trên model chuẩn.

## 3. Thiết kế thay đổi mới nhưng không phá module khác

Nếu đề xuất bổ sung logic mới cho 0213, phải phân tích theo các nguyên tắc:

- Ưu tiên thêm field `x_psm_0213_*` vào model hiện có thay vì tạo model mới.
- Chỉ tạo model mới nếu có business object độc lập rõ ràng.
- Mọi override trên model chuẩn phải guard bằng điều kiện:
  - Chỉ áp dụng khi request/category là offboarding 0213.
  - Không ảnh hưởng approval request thường.
- Mọi record rule trên model chuẩn phải domain chặt theo marker 0213, ví dụ:
  - `category_id.x_psm_0213_is_offboarding = True`
  - hoặc survey cụ thể của module 0213.
- Không thay đổi behavior của survey khác.
- Không thay đổi behavior của approval category khác.
- Không thay đổi behavior của mail activity khác nếu activity không thuộc offboarding 0213.
- Giữ backward compatibility với dữ liệu cũ.

# Required Blueprint Content

Hãy trả về một Technical Blueprint bằng Markdown gồm đúng các phần sau.

## 1. Source Analysis Summary

Tóm tắt hiện trạng dựa trên source đã đọc:

- Manifest và dependencies hiện có.
- Model kế thừa hiện có.
- Field `x_psm_0213_*` hiện có.
- Controller/portal route hiện có.
- View/QWeb hiện có.
- Security/access/record rule hiện có.
- Data XML/email template/cron/activity plan/survey hiện có.
- Những điểm có nguy cơ ảnh hưởng module khác.
- Những điểm có nguy cơ lỗi install/upgrade.
- Những điểm lệch giữa `structure/module_map.json` và source thật nếu có.

Ở phần này phải nêu rõ đã dùng các file source nào để xác nhận.

## 2. Target Architecture

Đề xuất kiến trúc chỉnh sửa cho module 0213:

- Model layer.
- Controller/portal layer.
- View/QWeb layer.
- Security layer.
- Data XML layer.
- Email/survey/activity/cron integration.
- Config layer.
- Upgrade/install compatibility.
- Cross-module safety.

Giữ kiến trúc hiện tại, không đề xuất rewrite lớn nếu không cần.

## 3. Odoo Data Model Design

Thiết kế schema mục tiêu cho các model liên quan.

### `approval.request`

Nêu:

- Field hiện có nên giữ nguyên.
- Field `x_psm_0213_*` nên bổ sung nếu cần.
- Field nào không nên rename vì có thể phá dữ liệu cũ.
- Compute field nào cần `store=True/False`, dependency nào.
- Constraint Python/SQL nếu cần.
- Override method nào cần guard chặt bằng offboarding category.
- Backward compatibility với request cũ.

### `approval.category`

Nêu:

- Cách dùng marker `x_psm_0213_is_offboarding`.
- Cách tránh ảnh hưởng category khác.
- XML data cần ổn định thế nào.

### `mail.activity`

Nêu:

- Field hoặc compute hiện có liên quan 0213.
- Cách đảm bảo logic chỉ áp dụng cho activity offboarding 0213.
- Không làm sai activity của module khác.

### `res.company` / `res.config.settings`

Nêu:

- Field config hiện có.
- Validation cần có cho template/user/email/days.
- Default value nên xử lý thế nào.
- Multi-company compatibility.

### `survey.user_input`

Nêu:

- Logic liên kết exit interview với offboarding request nếu có.
- Cách giới hạn scope survey 0213.
- Cách không ảnh hưởng survey khác.

## 4. Security And Access Design

Thiết kế phân quyền chi tiết:

- Nhóm user nào được đọc/tạo/sửa/xóa.
- Portal user chỉ được tạo/xem request của chính mình thế nào.
- OPS/HR/Manager/Approver scope thế nào.
- Record rule nào cần giữ.
- Record rule nào cần sửa nếu quá rộng.
- Access CSV nào có rủi ro vì cấp quyền trên model chuẩn.
- Khi nào được dùng `sudo()`, khi nào tuyệt đối không.
- Cách kiểm tra không leak dữ liệu giữa nhân viên.

Phải tuân thủ nguyên tắc minimum permission.

## 5. Portal And Workflow Design

Thiết kế flow portal/offboarding:

- Mở form nghỉ việc.
- Submit request.
- Tìm employee tương ứng với portal/internal user.
- Validate line manager/department/job/resignation date/reason.
- Tạo `approval.request` đúng category offboarding.
- Gửi survey exit interview.
- Tạo activity plan.
- Cho nhân viên hoặc người phụ trách mark activity done nếu hợp lệ.
- Withdraw/cancel/approve/done/rehire/blacklist.
- Email notification.
- Reminder cron.

Nêu rõ:

- Rule nào chặn cứng bằng `ValidationError/UserError/AccessError`.
- Rule nào chỉ cảnh báo bằng chatter/message/activity.
- State nào cho phép sửa.
- State nào khóa chỉnh sửa.
- Dữ liệu cũ vẫn render được thế nào.

## 6. XML/View/Data Compatibility Design

Thiết kế nguyên tắc sửa XML:

- Không đổi XML ID cũ nếu không bắt buộc.
- Không xóa record data cũ.
- Nếu cần thay record data, dùng update an toàn.
- View inheritance cần xpath ổn định.
- QWeb portal template cần giữ CSRF.
- Email template phải tránh lỗi khi field null.
- Cron phải có domain hẹp.
- Survey data không được phá response cũ.
- Config cleanup không được ẩn nhầm menu/view của module khác.

Nêu cách tránh lỗi install/upgrade phổ biến:

- External ID missing.
- Model/field not found.
- Invalid domain.
- Invalid xpath.
- Access right missing.
- Record rule khóa chính admin/internal flow.
- Email template render error.
- Cron gọi method không tồn tại.

## 7. Cross-Module Regression Risk Analysis

Phân tích rủi ro với module khác:

- `approvals`: approval request/category/approver flow.
- `hr`: employee, department, job, contract type, departure reason.
- `portal`: portal user route/access.
- `survey`: survey template, question, answer, user_input.
- `mail`: activity, template, chatter.
- `M02_P0200`: group/security phụ thuộc.
- Các module custom khác nếu cùng inherit `approval.request`, `mail.activity`, `survey.user_input`.

Với mỗi nhóm, nêu:

- Rủi ro có thể xảy ra.
- Cách thiết kế guard/scope.
- Check cần chạy sau khi sửa.

## 8. Business Logic Rules

Nêu rõ toàn bộ rule nghiệp vụ cho module 0213:

- Request offboarding chỉ là `approval.request` có category marker 0213.
- Logic 0213 không áp dụng cho approval request thường.
- Portal user chỉ thao tác trên dữ liệu của chính mình.
- Internal user chỉ thấy/sửa theo nhóm và record rule.
- Survey exit interview chỉ dùng survey 0213.
- Email template phải lấy từ config/company hoặc fallback rõ ràng.
- Cron reminder chỉ xử lý request offboarding 0213.
- Activity plan chỉ tạo cho request offboarding 0213.
- Không tự động xóa request/survey/activity cũ.
- Không đổi trạng thái nghiệp vụ nếu validation chưa đạt.
- Không dùng `sudo()` để bỏ qua quyền nếu có thể dùng access/domain đúng.

## 9. Implementation Roadmap For AI Coder

Lập thứ tự triển khai cụ thể:

1. Read convention and structure.
2. Verify source against map.
3. Backend model safeguards.
4. Security and record rule review.
5. Portal controller validation.
6. View/QWeb adjustments.
7. XML data/email/template/cron safety.
8. Compatibility and migration/backward compatibility.
9. Regression checks.
10. Regenerate structure map if source changed and generator exists.

Với mỗi bước, ghi:

- File cần đọc/sửa.
- Mục tiêu.
- Logic cần implement.
- Rủi ro cần tránh.
- Test/check cần chạy.

Các file chính cần nhắc AI Coder đọc/sửa nếu phù hợp:

- `addons/M02_P0213/models/resignation_request.py`
- `addons/M02_P0213/models/mail_activity.py`
- `addons/M02_P0213/models/res_company.py`
- `addons/M02_P0213/models/res_config_settings.py`
- `addons/M02_P0213/models/survey_user_input.py`
- `addons/M02_P0213/controllers/main.py`
- `addons/M02_P0213/security/security.xml`
- `addons/M02_P0213/security/offboarding_request_rules.xml`
- `addons/M02_P0213/security/ir.model.access.csv`
- `addons/M02_P0213/views/resignation_request_views.xml`
- `addons/M02_P0213/views/resignation_portal_template.xml`
- `addons/M02_P0213/views/res_company_views.xml`
- `addons/M02_P0213/views/res_config_settings_views.xml`
- `addons/M02_P0213/data/*.xml`
- `addons/M02_P0213/__manifest__.py`

## 10. Prompt Cho Executor

Viết một prompt riêng, cực kỳ rõ ràng, để copy cho AI Coder thực hiện.

Prompt này phải:

- Yêu cầu AI Coder sửa code trực tiếp.
- Bắt buộc đọc convention và structure trước.
- Liệt kê file cần đọc/sửa.
- Nêu thứ tự sửa.
- Nêu rule quan trọng về Odoo/Odoo module install/upgrade.
- Nêu rule không làm lỗi module khác.
- Nêu lệnh kiểm tra nên chạy.
- Nhắc không xóa comment có sẵn.
- Nhắc giữ backward compatibility.
- Nhắc không đổi XML ID/field/model cũ nếu không có migration rõ.
- Nhắc guard mọi override bằng scope offboarding 0213.
- Nhắc kiểm tra install/upgrade module.

Các lệnh kiểm tra nên đề xuất, tùy môi trường thực tế:

```bash
python odoo-bin -d <db_test> -i M02_P0213 --stop-after-init
python odoo-bin -d <db_test> -u M02_P0213 --stop-after-init
python odoo-bin -d <db_test> -u M02_P0213 --test-enable --stop-after-init
```

Nếu repo chạy bằng Docker, đề xuất kiểm tra tương đương bằng lệnh docker hiện có của dự án, ví dụ:

```bash
docker ps
docker logs <odoo_container> --tail 200
docker restart <odoo_container>
```

Không tự ý chạy destructive command. Không reset database nếu chưa được phép.

# Constraints

- Đây chỉ là blueprint/planning task.
- Không chỉnh sửa file.
- Không tạo file mới.
- Không apply patch.
- Không chạy formatter tự động làm đổi nhiều file.
- Không đề xuất rewrite toàn bộ module.
- Không đề xuất thêm dependency mới nếu không thật sự cần.
- Không sửa core Odoo.
- Không sửa module khác nếu chưa chứng minh bắt buộc.
- Không xóa comment hiện có.
- Không đổi tên field/model/XML ID cũ nếu không có migration/backward compatibility rõ.
- Luôn ưu tiên tương thích với dữ liệu/API/view/security hiện tại.
- Luôn ưu tiên source code thật hơn JSON map nếu có khác biệt.
- Nếu JSON map lỗi thời, ghi rõ cần regenerate sau khi source ổn định.

# Output Format

Trả về Markdown rõ ràng, có heading theo đúng 10 mục trong Required Blueprint Content.

Ở cuối, thêm mục:

## Files Used For Confirmation

Liệt kê các file đã đọc và vai trò của từng file trong phân tích.
```

## Files Used For Confirmation

- `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`: convention đặt tên, field prefix, rule dùng `approvals`/`survey`, minimum permission.
- `addons/M02_P0213/structure/module_map.json`: manifest, dependency, models, views, security, controllers, data và relations của module 0213.
- Danh sách thư mục thực tế của `addons/M02_P0213`: xác nhận module có `models`, `controllers`, `views`, `security`, `data`, `notes`, `structure`.
