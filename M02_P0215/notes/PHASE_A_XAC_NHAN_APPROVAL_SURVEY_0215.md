# Phase A - Xác nhận module dùng chung Approval và Survey cho module 0215

Ngày thực hiện: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã rà theo workflow module:

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- Plan gốc: `addons/M02_P0215/notes/PLAN_THAY_THE_CUSTOM_BANG_APPROVAL_SURVEY_0215.md`

Source đã đọc để xác nhận:

- `odoo/addons/approvals/__manifest__.py`
- `odoo/addons/approvals/models/approval_request.py`
- `odoo/addons/approvals/models/approval_category.py`
- `odoo/addons/approvals/security/approval_security.xml`
- `odoo/addons/approvals/security/ir.model.access.csv`
- `odoo/addons/survey/__manifest__.py`
- `odoo/addons/survey/models/survey_survey.py`
- `odoo/addons/survey/models/survey_user_input.py`
- `odoo/addons/survey/wizard/survey_invite.py`
- `odoo/addons/survey/security/survey_security.xml`
- `odoo/addons/survey/security/ir.model.access.csv`
- `addons/approval_engine/__manifest__.py`
- `addons/approval_engine/models/approval_mixin.py`
- `addons/approval_engine/models/approval_request.py`
- `addons/approval_engine/security/security.xml`
- `addons/approval_engine/security/ir.model.access.csv`

Lưu ý: thử đọc `config/odoo.conf` để xác nhận `addons_path` nhưng bị hệ điều hành từ chối quyền đọc. Vì vậy kết luận Phase A dựa trên source hiện có trong workspace, chưa xác nhận trạng thái cài đặt trong database.

## 2. Kết quả tìm module thực tế

Trong workspace hiện có các module liên quan:

- `odoo/addons/approvals`
- `odoo/addons/survey`
- `addons/approval_engine`
- `addons/approval_engine/portal_contact_update`
- `addons/psm_approval_advance_claim`

Không thấy module có thư mục tên đúng `approval`. Module chuẩn của Odoo trong workspace này là `approvals`, không phải `approval`.

Convention của 0215 ghi "Approval dùng chung module `approval`", nhưng source thực tế của Odoo 19 trong workspace dùng module `approvals`. Khi triển khai Phase B, cần dùng tên dependency thực tế là `approvals`, hoặc phải điều chỉnh convention nếu team muốn gọi thống nhất là `approval`.

## 3. Kết luận cho Approval

### 3.1. Module nên dùng cho 0215

Khuyến nghị dùng module chuẩn Odoo:

- Dependency: `approvals`
- Model category: `approval.category`
- Model request: `approval.request`
- Model approver line: `approval.approver`
- Field trạng thái request: `request_status`
- Giá trị trạng thái chính:
  - `new`
  - `pending`
  - `approved`
  - `refused`
  - `cancel`

Lý do:

- Đây là module chuẩn Odoo, nằm trong `odoo/addons`.
- Đúng mục tiêu "ưu tiên dùng cái sẵn có".
- Có sẵn cấu hình category, approver, minimum approval, approver sequence, manager approval.
- Có sẵn activity cho approver và cơ chế approve/refuse.
- Phù hợp thay phần custom CEO duyệt trong 0215.

### 3.2. Không chọn `approval_engine` cho Phase B

`approval_engine` là module nội bộ có các model:

- `approval.workflow`
- `approval.step`
- `approval.engine.request`
- `approval.engine.request.step.run`
- `approval.engine.request.approver.run`
- `approval.mixin`
- `approval.log`

Module này mạnh ở hướng gắn mixin vào chứng từ và chặn action kỹ thuật, ví dụ `button_confirm` hoặc `action_post`. Nó phù hợp với các chứng từ như purchase/account hơn là nhu cầu thay phần CEO approval đơn giản của 0215.

Không chọn `approval_engine` cho Phase B vì:

- Không phải module gốc Odoo.
- Thêm `approval.mixin` vào `x_psm.hr.discipline.record` sẽ làm 0215 phụ thuộc vào workflow engine nội bộ.
- Luồng 0215 hiện đã có state nghiệp vụ riêng, chỉ cần external approval request để duyệt Company Level.
- Convention đang yêu cầu dùng module approval chung, không tạo thêm logic duyệt riêng trong 0215.

`approval_engine` có thể được xem là phương án dự phòng nếu database không cài được module `approvals`, nhưng không phải hướng ưu tiên.

## 4. Thiết kế Approval đã chốt cho Phase B

### 4.1. Dependency

Thêm vào manifest 0215:

```python
"approvals",
```

Không thêm `approval_engine` trong Phase B.

### 4.2. Field liên kết đề xuất

Thêm vào `x_psm.hr.discipline.record`:

- `x_psm_approval_request_id`: Many2one tới `approval.request`
- `x_psm_approval_category_id`: Many2one tới `approval.category`, hoặc dùng XML ID cố định từ data
- `x_psm_approval_status`: related/snapshot từ `approval.request.request_status`
- `x_psm_approval_requested_date`: ngày tạo/trình request
- `x_psm_approval_completed_date`: ngày request về `approved` hoặc `refused`
- `x_psm_approval_refuse_reason`: ghi chú nội bộ nếu cần, vì `approval.request` chuẩn không có field lý do từ chối dạng text riêng rõ ràng

### 4.3. Data cần tạo

Tạo approval category riêng cho 0215, ví dụ:

- XML ID: `approval_category_psm_discipline_company_level`
- Model: `approval.category`
- Name: `0215 - Phê duyệt kỷ luật cấp công ty`
- Minimum approval: `1`
- Approver sequence: tùy nghiệp vụ CEO một cấp hay nhiều cấp
- Approver: nên cấu hình bằng user/group thực tế sau, không hard-code bừa nếu chưa có CEO group rõ ràng

### 4.4. Mapping state

Mapping đề xuất:

- 0215 `issued` + Company Level -> tạo `approval.request`
- `approval.request.action_confirm()` -> request sang `pending`
- 0215 chuyển sang `approval`
- Nếu `approval.request.request_status = approved`:
  - 0215 chuyển sang `notified`
  - gửi email thông báo nhân viên
- Nếu `approval.request.request_status = refused`:
  - 0215 chuyển về `proposal`
  - HR chỉnh lại đề xuất
- Store Level không tạo approval request:
  - 0215 `issued -> notified`

### 4.5. Điểm cần xử lý kỹ ở Phase B

`approval.request` chuẩn tự compute `request_status` từ các dòng `approval.approver`. Để đồng bộ ngược về 0215 có hai hướng:

1. Tạo method sync thủ công trên 0215, ví dụ button hoặc cron nhẹ kiểm tra request.
2. Kế thừa `approval.request.write()` trong 0215 hoặc file bridge để khi `request_status` đổi sang `approved/refused` thì cập nhật record 0215.

Khuyến nghị Phase B dùng bridge kế thừa `approval.request` có kiểm tra category XML ID của 0215. Cách này giúp luồng tự động hơn nhưng vẫn giới hạn phạm vi.

## 5. Kết luận cho Survey

### 5.1. Module nên dùng cho 0215

Khuyến nghị dùng module chuẩn Odoo:

- Dependency: `survey`
- Model survey: `survey.survey`
- Model response: `survey.user_input`
- Model response line: `survey.user_input.line`
- Model question: `survey.question`
- Model suggested answer: `survey.question.answer`
- Wizard invite: `survey.invite`

Lý do:

- Đây là module chuẩn Odoo, nằm trong `odoo/addons`.
- Có sẵn link public/token qua `access_token`.
- Có sẵn response `survey.user_input` với trạng thái:
  - `new`
  - `in_progress`
  - `done`
- Có sẵn method tạo bài trả lời: `survey.survey._create_answer(...)`
- Có sẵn URL làm bài: `survey.user_input.get_start_url()`
- Có sẵn email invite qua `survey.invite`.

### 5.2. Dependency

Thêm vào manifest 0215:

```python
"survey",
```

### 5.3. Field liên kết đề xuất

Thêm vào `x_psm.hr.discipline.record`:

- `x_psm_explanation_survey_id`: Many2one tới `survey.survey`
- `x_psm_explanation_survey_user_input_id`: Many2one tới `survey.user_input`
- `x_psm_explanation_survey_state`: related/snapshot từ `survey.user_input.state`
- `x_psm_feedback_survey_id`: Many2one tới `survey.survey`
- `x_psm_feedback_survey_user_input_id`: Many2one tới `survey.user_input`
- `x_psm_feedback_survey_state`: related/snapshot từ `survey.user_input.state`

### 5.4. Data cần tạo

Tạo tối thiểu hai survey template:

1. `0215 - Bản tường trình nhân viên`
2. `0215 - Phiếu feedback/cải thiện ngay`

Survey tường trình nên có câu hỏi:

- Thời gian xảy ra sự việc
- Địa điểm
- Người chứng kiến
- Nội dung tường trình
- Nguyên nhân
- Cam kết cải thiện
- Xác nhận đã gửi tường trình

Survey feedback nên có câu hỏi:

- Vấn đề cần cải thiện
- Nội dung đã trao đổi
- Hướng dẫn/cam kết cải thiện
- Thời gian theo dõi
- Kết quả sau theo dõi

### 5.5. Mapping với portal

Hiện portal 0215 đang tự render form tường trình. Sau Phase C:

- `action_psm_send_to_employee()` tạo `survey.user_input` bằng `_create_answer(...)`.
- Gửi link `user_input.get_start_url()` cho nhân viên.
- Trang `/my/discipline/<id>` hiển thị link survey và trạng thái response.
- Khi `survey.user_input.state = done`, 0215 sync nội dung trả lời về field snapshot để report/mail vẫn dùng được.

## 6. Chốt tên module dependency cho các phase sau

Phase B:

- Dùng `approvals`
- Không dùng `approval_engine` mặc định

Phase C và D:

- Dùng `survey`

Manifest sau các phase nên có thêm:

```python
"approvals",
"survey",
```

## 7. Việc chưa làm trong Phase A

Phase A chưa sửa manifest và chưa sửa code nghiệp vụ 0215. Phase này chỉ xác nhận module thực tế và chốt hướng triển khai.

Chưa xác nhận được trạng thái cài đặt trong database vì chưa truy vấn Odoo runtime/database. Khi bắt đầu Phase B, nên kiểm tra trên database test:

- module `approvals` có install được không;
- module `survey` có install được không;
- group approver/CEO thực tế là group nào;
- user nào sẽ là approver mặc định cho category 0215.

## 8. Khuyến nghị bước tiếp theo

Triển khai Phase B theo hướng:

1. Thêm dependency `approvals`.
2. Thêm data approval category cho 0215.
3. Thêm field link `approval.request` vào record 0215.
4. Sửa `action_psm_submit_for_approval()` để tạo và confirm approval request.
5. Kế thừa `approval.request` bằng bridge nhỏ để sync `approved/refused` về state 0215.
6. Ẩn nút CEO custom khỏi view chính, giữ method legacy để tương thích.
