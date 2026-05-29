# Plan thay thế phần custom bằng Approval và Survey cho module 0215

Ngày lập: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã rà theo workflow module:

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source chính xác nhận:
  - `addons/M02_P0215/__manifest__.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_explanation.py`
  - `addons/M02_P0215/wizards/x_psm_hr_discipline_reject_wizard.py`
  - `addons/M02_P0215/controllers/portal.py`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
  - `addons/M02_P0215/views/x_psm_portal_templates.xml`
  - `addons/M02_P0215/security/ir.model.access.csv`
  - `addons/M02_P0215/security/security_rules.xml`

Lưu ý hiện trạng addons:

- Manifest hiện chưa phụ thuộc `approval` hoặc `survey`.
- Trong thư mục `addons` hiện thấy `approval_engine`, chưa thấy thư mục module tên đúng `approval`.
- Chưa thấy thư mục module `survey` trong kết quả rà nhanh.
- Vì vậy trước khi triển khai thật cần xác nhận module duyệt/khảo sát đang dùng trong instance là `approval`, `approval_engine`, `survey`, hay một module nội bộ khác tương đương.

## 2. Mục tiêu thay đổi

Mục tiêu là giảm phần tự làm trùng với module gốc hoặc module dùng chung, đúng convention:

- Duyệt dùng module `approval`.
- Câu hỏi, khảo sát, phản hồi, tường trình dạng form dùng module `survey`.
- Module 0215 chỉ giữ nghiệp vụ riêng của quy trình kỷ luật:
  - hồ sơ kỷ luật;
  - phân loại lỗi;
  - hình thức xử lý;
  - xác định Store Level hoặc Company Level;
  - tính tái phạm;
  - hiệu lực kỷ luật;
  - liên kết nhân viên, quản lý, HR, RGM.

Không nên thay tất cả state custom bằng module gốc. `state` của `x_psm.hr.discipline.record` vẫn cần giữ để quản lý tiến độ nghiệp vụ của hồ sơ 0215. Approval và Survey chỉ nên đảm nhận phần chuyên trách: phê duyệt và thu thập câu trả lời.

## 3. Các phần custom hiện đang trùng

### 3.1. Phê duyệt CEO đang tự làm

Hiện trạng trong `models/x_psm_hr_discipline_record.py`:

- State `approval`.
- Method `action_psm_submit_for_approval()`.
- Method `action_psm_ceo_approve()`.
- Method `action_psm_ceo_reject()`.
- Transition custom:
  - `issued -> approval`
  - `approval -> notified`
  - `approval -> proposal`
- Button trong `views/x_psm_hr_discipline_record_views.xml`:
  - `CEO Phê duyệt`
  - `CEO Từ chối`
- Quyền đang dùng `hr.group_hr_manager`, chưa phải cơ chế approver chuẩn.

Phần này nên thay bằng approval request chuẩn.

### 3.2. Tường trình và phản hồi nhân viên đang tự làm

Hiện trạng:

- Model riêng `x_psm.hr.discipline.explanation`.
- Field text trên record:
  - `x_psm_employee_explanation`
  - `x_psm_section_ii_feedback`
  - `x_psm_section_i_description`
  - `x_psm_section_iii_identification`
  - `x_psm_section_iv_agreement`
- Chữ ký và upload ảnh bản tường trình nằm trực tiếp trên record.
- Portal tự render form và tự ghi dữ liệu vào record.
- Wizard riêng `x_psm.hr.discipline.reject.wizard` để từ chối tường trình.

Phần này có thể thay một phần bằng Survey, nhưng không nên thay toàn bộ ngay vì hiện có chữ ký, ảnh tường trình và form PDF nội bộ. Cách an toàn là dùng Survey cho nội dung câu hỏi/câu trả lời, còn chữ ký và tài liệu pháp lý vẫn giữ trên record 0215.

### 3.3. Phản hồi cải thiện ngay đang là action nội bộ

Hiện trạng:

- Master action có `x_psm_form_code = feedback`.
- `action_psm_rgm_no_repeat()` tự gán action feedback và chuyển `proposal`.
- Chưa có bộ câu hỏi/phản hồi chuẩn cho cuộc trao đổi cải thiện.

Phần này phù hợp để dùng Survey làm phiếu feedback/cải thiện ngay.

## 4. Thiết kế sau thay đổi

### 4.1. Dùng Approval cho phê duyệt Company Level

Luồng đề xuất:

1. Hồ sơ 0215 đi tới `issued`.
2. Nếu `x_psm_discipline_level = company`, hệ thống tạo approval request.
3. Hồ sơ chuyển sang state chờ duyệt, ví dụ vẫn dùng `approval` hoặc đổi nhãn thành `waiting_approval`.
4. CEO hoặc nhóm approver xử lý trên approval request.
5. Khi approval được duyệt:
   - ghi kết quả về hồ sơ 0215;
   - chuyển record sang `notified`;
   - gửi email thông báo cho nhân viên.
6. Khi approval bị từ chối:
   - ghi lý do từ chối về hồ sơ 0215;
   - chuyển record về `proposal`;
   - HR điều chỉnh lại nội dung xử lý.

Field liên kết nên thêm vào `x_psm.hr.discipline.record`:

- `x_psm_approval_request_id`: liên kết tới request duyệt.
- `x_psm_approval_state`: trạng thái duyệt đọc từ approval request hoặc lưu snapshot.
- `x_psm_approval_result_note`: ghi chú/lý do duyệt hoặc từ chối.
- `x_psm_approval_requested_date`: ngày trình duyệt.
- `x_psm_approval_completed_date`: ngày hoàn tất duyệt.

Action cần thay:

- `action_psm_submit_for_approval()`:
  - không tự chuyển thẳng logic CEO nữa;
  - tạo approval request;
  - mở hoặc link tới approval request.
- `action_psm_ceo_approve()` và `action_psm_ceo_reject()`:
  - chuyển thành legacy wrapper hoặc bỏ khỏi view;
  - không còn là nút chính nếu approval module đã xử lý.

View cần thay:

- Ẩn hoặc bỏ nút `CEO Phê duyệt`, `CEO Từ chối`.
- Thêm smart button mở approval request.
- Thêm section hiển thị trạng thái approval.
- Button `Trình duyệt / Thông báo NV` nên tách nhãn:
  - Store Level: `Thông báo nhân viên`
  - Company Level: `Tạo yêu cầu phê duyệt`

### 4.2. Dùng Survey cho tường trình nhân viên

Luồng đề xuất:

1. Khi quản lý gửi yêu cầu tường trình, hệ thống tạo hoặc gửi link survey cho nhân viên.
2. Survey chứa bộ câu hỏi chuẩn:
   - thời gian xảy ra sự việc;
   - địa điểm;
   - người chứng kiến;
   - nội dung tường trình;
   - nguyên nhân;
   - cam kết cải thiện;
   - xác nhận đã đọc nội dung.
3. Nhân viên trả lời survey qua portal.
4. Khi survey hoàn tất:
   - link kết quả survey về hồ sơ 0215;
   - đồng bộ nội dung chính về record để report/mail vẫn dùng được;
   - chuyển hoặc cho phép chuyển hồ sơ sang bước quản lý kiểm tra.
5. Nếu quản lý từ chối tường trình:
   - tạo yêu cầu trả lời lại survey hoặc mở lại survey mới;
   - lưu lý do từ chối ở hồ sơ 0215;
   - gửi mail/activity cho nhân viên.

Field liên kết nên thêm vào `x_psm.hr.discipline.record`:

- `x_psm_explanation_survey_id`: mẫu survey tường trình.
- `x_psm_explanation_survey_user_input_id`: bài trả lời survey hiện tại.
- `x_psm_explanation_survey_state`: trạng thái trả lời.
- `x_psm_explanation_rejection_reason`: lý do yêu cầu làm lại.

Model `x_psm.hr.discipline.explanation` có thể xử lý theo hai hướng:

- Giai đoạn 1: giữ lại làm snapshot lịch sử, nhưng nguồn dữ liệu chính đến từ survey.
- Giai đoạn 2: nếu survey đã đáp ứng đủ lịch sử, cân nhắc giảm vai trò model này, không xóa ngay để tránh mất dữ liệu cũ.

Portal cần thay:

- Form nhập tường trình custom chỉ còn là fallback hoặc chuyển thành link mở survey.
- Trang chi tiết hồ sơ hiển thị trạng thái survey và link làm bài.
- Khi nhân viên hoàn tất survey, portal hiển thị câu trả lời/snapshot thay vì form nhập text trực tiếp.

### 4.3. Dùng Survey cho feedback/cải thiện ngay

Luồng đề xuất:

1. Khi RGM xác định không cần kỷ luật formal và chọn feedback ngay, hệ thống gắn survey feedback.
2. Survey feedback dùng cho quản lý ca hoặc MIC ghi nhận nội dung trao đổi:
   - vấn đề cần cải thiện;
   - nguyên nhân;
   - hướng dẫn đã trao đổi;
   - cam kết của nhân viên;
   - thời gian theo dõi;
   - kết quả sau theo dõi nếu có.
3. Kết quả survey feedback được link vào hồ sơ 0215.
4. Hồ sơ có thể đi tới `notified` hoặc `active` tùy quyết định nghiệp vụ, nhưng cần thống nhất lại với note quy trình bước 17.

Field liên kết nên thêm:

- `x_psm_feedback_survey_id`
- `x_psm_feedback_survey_user_input_id`
- `x_psm_feedback_completed_date`

## 5. Các bước triển khai đề xuất

### Phase A - Xác nhận module dùng chung thực tế

- Kiểm tra chính xác module duyệt đang dùng:
  - nếu có module `approval`, dùng theo convention;
  - nếu instance chỉ có `approval_engine`, cần đọc structure/source của `approval_engine` trước khi quyết định;
  - không tự tạo module duyệt mới trong 0215.
- Kiểm tra module `survey` có tồn tại ở addons path nào khác không.
- Nếu thiếu module, cần bổ sung dependency/module nguồn trước khi sửa 0215.

Kết quả phase này:

- Chốt tên module dependency trong `__manifest__.py`.
- Chốt model approval request cần liên kết.
- Chốt model survey response cần liên kết.

### Phase B - Refactor approval

- Thêm dependency approval vào manifest.
- Thêm field liên kết approval request trên `x_psm.hr.discipline.record`.
- Tạo data cấu hình approval category/type cho quy trình kỷ luật cấp công ty.
- Sửa `action_psm_submit_for_approval()` để tạo approval request.
- Bỏ nút CEO duyệt/từ chối khỏi view chính hoặc chuyển thành nút legacy ẩn.
- Thêm smart button mở approval request.
- Đồng bộ callback/kết quả approval về state 0215:
  - approved -> `notified`;
  - refused -> `proposal`.
- Cập nhật mail template nếu nội dung email cần lấy trạng thái approval.
- Cập nhật security để approver không cần quyền quá rộng trên toàn bộ hồ sơ nếu không cần.

### Phase C - Refactor survey cho tường trình

- Thêm dependency survey vào manifest.
- Tạo survey template tường trình nhân viên.
- Thêm field link survey và response vào record.
- Sửa `action_psm_send_to_employee()`:
  - tạo/gửi survey invite hoặc response link;
  - giữ mail/activity hiện tại nhưng nội dung dẫn tới survey.
- Sửa portal:
  - trang record hiển thị link survey;
  - hạn chế form nhập tường trình custom nếu đã dùng survey.
- Tạo logic đọc câu trả lời survey để sync về các field snapshot trên record.
- Sửa wizard từ chối tường trình:
  - ghi lý do;
  - tạo lại survey response hoặc reset request;
  - gửi mail/activity.

### Phase D - Refactor survey cho feedback ngay

- Tạo survey template feedback/cải thiện ngay.
- Sửa `action_psm_rgm_no_repeat()` hoặc tạo action mới rõ nghĩa hơn:
  - gắn action feedback;
  - tạo survey feedback;
  - chuyển state theo luồng đã thống nhất.
- Thêm hiển thị kết quả survey feedback trên form record.
- Cập nhật report nếu cần in nội dung feedback.

### Phase E - Dọn code trùng và giữ tương thích dữ liệu cũ

- Không xóa ngay các field cũ đang có dữ liệu:
  - `x_psm_section_i_description`
  - `x_psm_section_ii_feedback`
  - `x_psm_section_iii_identification`
  - `x_psm_section_iv_agreement`
  - `x_psm_explanation_ids`
- Đánh dấu vai trò mới của field cũ là snapshot/report cache.
- Giữ method legacy nếu có thể đang được gọi từ view, portal, mail template hoặc dữ liệu cũ.
- Chỉ bỏ hẳn model/wizard custom sau khi đã có migration dữ liệu và xác nhận không còn reference.
- Không xóa comment tiếng Việt không dấu hoặc comment hiện có trong code nếu không bắt buộc.

### Phase F - Security và dữ liệu

- Rà lại quyền portal sau khi survey thay form custom.
- Rà lại quyền approver:
  - approver chỉ duyệt được request cần duyệt;
  - không mặc định cấp toàn quyền quản trị hồ sơ kỷ luật.
- Rà record rule liên quan `base.group_portal`.
- Rà group từ `M02_P0200` đang dùng:
  - Store manager;
  - HRBP;
  - RGM.
- Nếu approval/survey có cơ chế quyền riêng, ưu tiên dùng quyền của module đó thay vì tự mở rộng quyền trong 0215.

### Phase G - Migration dữ liệu

- Với hồ sơ cũ đang ở `approval`:
  - tạo approval request tương ứng hoặc giữ ở state cũ và chỉ áp dụng flow mới cho hồ sơ mới.
- Với tường trình cũ:
  - giữ dữ liệu text/signature/attachment trên record;
  - nếu cần, tạo survey response lịch sử dạng snapshot, nhưng không bắt buộc nếu rủi ro cao.
- Với feedback cũ:
  - giữ `x_psm_action_id` đang là feedback;
  - chỉ tạo survey feedback cho hồ sơ mới sau refactor.

## 6. File dự kiến thay đổi

Manifest:

- `addons/M02_P0215/__manifest__.py`

Models:

- `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
- `addons/M02_P0215/models/x_psm_hr_discipline_explanation.py`
- Có thể thêm model bridge mới nếu cần, ví dụ:
  - `models/x_psm_hr_discipline_approval.py`
  - `models/x_psm_hr_discipline_survey.py`

Views:

- `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
- `addons/M02_P0215/views/x_psm_portal_templates.xml`
- Có thể bỏ dần hoặc chỉnh:
  - `addons/M02_P0215/views/x_psm_hr_discipline_reject_wizard_views.xml`

Controllers:

- `addons/M02_P0215/controllers/portal.py`

Data:

- Thêm data approval category/type.
- Thêm data survey templates.
- Cập nhật mail templates:
  - `data/mail_template.xml`
  - `data/email_template_rejection.xml`
  - `data/email_template_discipline_done.xml`

Security:

- `security/ir.model.access.csv`
- `security/security_rules.xml`

Reports:

- `reports/x_psm_discipline_reports.xml`

Structure:

- Sau khi sửa code, regenerate:
  - `structure/module_map.json`
  - `structure/module_map_stats.json`
  - các file trong `structure/details/`

## 7. Rủi ro chính

- Module `approval` hoặc `survey` có thể chưa có trong instance hiện tại.
- Tên module thực tế có thể là `approval_engine` thay vì `approval`.
- Dùng `.sudo()` trong portal hiện tại có thể làm record rule của survey/approval không áp đúng nếu không chỉnh cẩn thận.
- Survey có thể không đáp ứng tốt chữ ký pháp lý; nên giữ chữ ký trên record 0215 hoặc attachment/report riêng.
- Approval chuẩn có thể không map một-một với state hiện tại; cần bridge rõ để không làm đứt luồng `issued -> notified`.
- Nếu thay quá mạnh, dữ liệu hồ sơ cũ dễ bị mất ngữ cảnh. Cần migration theo hướng giữ snapshot.

## 8. Tiêu chí hoàn thành

- Manifest khai báo đúng module dùng chung đã xác nhận.
- Company Level không còn duyệt CEO bằng nút custom chính, mà đi qua approval request.
- Hồ sơ 0215 có smart button/link tới approval request.
- Tường trình nhân viên có thể được gửi và hoàn tất qua survey.
- Feedback/cải thiện ngay có survey riêng hoặc form survey chuẩn.
- Record 0215 vẫn giữ luồng nghiệp vụ rõ ràng và không bị phụ thuộc hoàn toàn vào state của approval/survey.
- Portal user chỉ thấy và thao tác đúng hồ sơ/survey của mình.
- Store manager, RGM, HRBP, approver có quyền tối thiểu.
- Report và email vẫn in/gửi được nội dung cần thiết.
- Chạy được kiểm tra:
  - compile Python;
  - parse XML;
  - upgrade module trên database test;
  - test luồng Store Level;
  - test luồng Company Level approved/refused;
  - test nhân viên trả lời survey;
  - test feedback ngay.

## 9. Khuyến nghị triển khai

Nên triển khai theo thứ tự:

1. Xác nhận module approval/survey thực tế.
2. Làm approval trước vì phạm vi hẹp hơn và ít đụng portal.
3. Làm survey tường trình sau, giữ field cũ làm snapshot.
4. Làm survey feedback sau cùng vì cần thống nhất nghiệp vụ bước 17.
5. Sau mỗi phase regenerate structure map để JSON map không lệch source.
