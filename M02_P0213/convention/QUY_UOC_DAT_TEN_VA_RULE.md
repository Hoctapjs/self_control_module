# Quy Ước Đặt Tên Và Rule

Tài liệu này tổng hợp các quy ước cần lưu ý khi phát triển module.

## 1. Quy ước đặt tên

### 1.1. Manifest

- Cấu trúc tên module trong manifest:
  - `M02_P0101_<TÊN_QUY_TRÌNH_VIẾT_HOA>`
- Không cần thể hiện version trong tên module.

### 1.2. model gốc

- model gốc giữ nguyên tên.
- Không đổi tên model gốc.

### 1.3. model mới

- model mới đặt theo quy ước:
  - `x_psm_<tên_model>`

### 1.4. Field mới trong model gốc

- Field mới bổ sung vào model gốc đặt theo quy ước:
  - `x_psm_0101_tenfield`

### 1.5. Field mới trong model mới

- Field mới trong model mới đặt theo quy ước:
  - `x_psm_tenfield`

### 1.6. Action mới

- Action mới đặt theo quy ước:
  - `action_psm_tenaction`

### 1.7. View mới

- View mới đặt theo quy ước:
  - `view_psm_tenview`

### 1.8. Security

#### Văn phòng

- Nhóm 1:
  - `group_gdh_rst_module_stf`
- Nhóm 2:
  - `group_gdh_rst_module_mgr`

#### Nhà hàng

- Nhóm 1:
  - `group_gdh_ops_module_crw`
- Nhóm 2:
  - `group_gdh_ops_module_mgr`

### 1.9. Duyệt

- Sử dụng chung 1 module:
  - `approval`

### 1.10. Chấm điểm, khảo sát, phỏng vấn, câu hỏi

- Sử dụng chung 1 module:
  - `survey`

### 1.11. Ứng viên

- Sử dụng tên thống nhất:
  - `applicant`

### 1.12. Nhân viên

- Sử dụng tên thống nhất:
  - `employee`

## 2. Rule cần tuân thủ

### 2.1. Ưu tiên dùng cái sẵn có

- Cố gắng tận dụng tối đa model, field, action, view, module sẵn có của Odoo hoặc hệ thống hiện tại.
- Hạn chế tối đa việc tạo model mới nếu chưa thật sự cần thiết.

### 2.2. Phân quyền tối thiểu

- Chỉ cấp đúng mức quyền cần thiết để hoàn thành công việc.
- Không phân quyền tràn lan.
- Ưu tiên nguyên tắc minimum permission.

### 2.3. Tách bạch rõ ràng

- Ngăn nào ra ngăn nấy.
- Chức năng nào thuộc module nào thì để đúng module đó.
- Hạn chế viết logic lồng ghép, chồng chéo giữa các module.

## 3. Tóm tắt nhanh

- model gốc: giữ nguyên tên.
- model mới: `x_psm_<tên_model>`.
- Field mới model gốc: `x_psm_0101_tenfield`.
- Field mới model mới: `x_psm_tenfield`.
- Action mới: `action_psm_tenaction`.
- View mới: `view_psm_tenview`.
- Approval dùng chung module `approval`.
- Survey, chấm điểm, phỏng vấn, câu hỏi dùng chung module `survey`.
- Ứng viên dùng tên `applicant`.
- Nhân viên dùng tên `employee`.
- Ưu tiên dùng sẵn có, phân quyền tối thiểu, tách bạch rõ ràng.

## 4. ACL & Record Rule Standards

### 4.1. Naming convention

- Record rule của module 0213 đặt theo mẫu:
  - `rule_0213_<model>_<action>_<scope>`
- Ví dụ:
  - `rule_0213_approval_request_ops_read`
  - `rule_0213_survey_user_input_portal_own`
- Không tạo thêm rule mới với prefix cũ `rule_psm_0213_*`.

### 4.2. Scope limiting

- Ưu tiên dùng field custom `x_psm_0213_*` để giới hạn scope record rule.
- Không cấp quyền rộng rãi cho `base.group_user`.
- ACL chỉ cấp quyền nền tối thiểu; record rule chịu trách nhiệm giới hạn business scope.
- Với survey exit interview, chỉ cho phép truy cập dữ liệu thuộc survey được đánh dấu `x_psm_0213_is_exit_survey=True`.

### 4.3. Implied IDs dependency

- Module 0213 phụ thuộc module 0200 cung cấp đúng chain implied group cho user nội bộ.
- Các group OPS/HRBP/CNB dùng trong 0213 phải nhận được `base.group_user` qua chain của 0200.
- Các group đã xác nhận cần chain nội bộ:
  - `GDH_RST_OPS_OC_S`
  - `GDH_RST_OPS_OM_M`
  - `GDH_RST_HR_HRBP_S`
  - `GDH_RST_HR_HRBP_M`
  - `GDH_RST_HR_CNB_S`
  - `GDH_RST_HR_CNB_M`

### 4.4. Protected fields

- `approval.category.x_psm_0213_is_offboarding`:
  - chỉ `base.group_system` hoặc `approvals.group_approval_manager` được bật/tắt.
  - phải có backend guard trong `create()`/`write()`, không chỉ dựa vào view.
- `mail.activity.x_psm_0213_is_offboarding_activity`:
  - là field compute/store dùng cho record rule.
  - không write trực tiếp từ nghiệp vụ thông thường.
- `survey.survey.x_psm_0213_is_exit_survey`:
  - dùng để scope record rule survey exit interview.

### 4.5. Portal vs Internal

- Portal:
  - chỉ được tạo/sửa dữ liệu của chính mình.
  - scope owner dựa trên `partner_id == user.partner_id` hoặc `email == user.email`.
  - không được truy cập survey/user_input ngoài exit interview của 0213.
- Internal:
  - cấp quyền rõ ràng theo group chuyên môn từ module 0200.
  - `base.group_user` chỉ dùng cho quyền đọc nền tối thiểu.
  - create/write trên dữ liệu nhạy cảm phải cấp cho group chuyên trách, không cấp tràn lan.
