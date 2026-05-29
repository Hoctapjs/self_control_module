# Phase 4 - Đã triển khai phân quyền tối thiểu module 0215

Ngày thực hiện: 2026-05-07

## 1. Tài liệu và source đã dùng

Đã bám theo:

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `notes/PLAN_REFACTOR_MODULE_0215_THEO_CONVENTION.md`
- `notes/PHASE_3_DA_TRIEN_KHAI_WORKFLOW_0215.md`

Source chính dùng để xác nhận và sửa:

- `security/ir.model.access.csv`
- `security/security_rules.xml`
- `__manifest__.py`
- `controllers/portal.py`
- `models/x_psm_hr_discipline_record.py`
- `M02_P0200/security/security.xml`

## 2. Phạm vi Phase 4

Phase 4 tập trung vào phân quyền tối thiểu:

- Rà lại model access theo nhóm.
- Bổ sung record rule cho portal, store manager và HRBP.
- Cấp quyền HRBP ở mức cần thiết vì view workflow đang dùng group `M02_P0200.GDH_RST_HR_HRBP_S`.
- Không refactor sâu `.sudo()` trong portal vì Phase 2 đã có business guard. Việc bỏ sudo hoàn toàn nên làm sau khi test cài module thực tế.

## 3. Nội dung đã triển khai

### 3.1. Cập nhật model access

Đã bổ sung quyền đọc master data cho HRBP:

- `access_psm_hr_discipline_violation_category_hrbp`
- `access_psm_hr_discipline_violation_type_hrbp`
- `access_psm_hr_discipline_action_hrbp`

Đã bổ sung quyền thao tác hồ sơ cho HRBP:

- `access_psm_hr_discipline_record_hrbp`
- `access_psm_hr_discipline_explanation_hrbp`
- `access_psm_hr_discipline_reject_wizard_hrbp`

Giữ nguyên nguyên tắc:

- Store manager có read/create/write record và explanation, không unlink.
- Portal chỉ read record; với explanation vẫn create/write để phục vụ luồng tường trình.
- HR manager có toàn quyền để quản trị.

### 3.2. Thêm security rule XML

Đã thêm file:

- `security/security_rules.xml`

Đã đưa vào manifest ngay sau `security/ir.model.access.csv`.

### 3.3. Record rule cho hồ sơ kỷ luật

Đã thêm:

- `rule_psm_hr_discipline_record_portal_own`
- `rule_psm_hr_discipline_record_store_manager`
- `rule_psm_hr_discipline_record_hrbp`

Ý nghĩa:

- Portal chỉ đọc hồ sơ của chính nhân viên được map theo `user_id` hoặc `work_email`.
- Store manager đọc/ghi/tạo hồ sơ trong phạm vi:
  - chính họ là nhân viên của hồ sơ;
  - họ là đại diện công ty tạo hồ sơ;
  - họ là quản lý trực tiếp của nhân viên;
  - nhân viên thuộc cùng department với employee của user hiện tại.
- HRBP được đọc/ghi/tạo tất cả hồ sơ để xử lý luồng company level.

### 3.4. Record rule cho tường trình

Đã thêm:

- `rule_psm_hr_discipline_explanation_portal_own`
- `rule_psm_hr_discipline_explanation_store_manager`
- `rule_psm_hr_discipline_explanation_hrbp`

Rule tường trình bám theo hồ sơ cha `x_psm_record_id`.

## 4. Kiểm tra đã chạy

Đã chạy và đạt:

- `python -m compileall addons\M02_P0215`
- Parse toàn bộ XML bằng `xml.etree.ElementTree`
- Kiểm tra manifest data file không thiếu
- Search xác nhận:
  - `security/security_rules.xml` đã nằm trong manifest
  - các rule `rule_psm_hr_discipline_*` đã có trong XML
  - các access HRBP đã có trong CSV
- Regenerate `structure/module_map.json` bằng `structure/build_module_map.py`

## 5. Lưu ý rủi ro

- Portal controller vẫn dùng `.sudo()` tại một số điểm. Phase 2 đã có business guard, nhưng record rule sẽ không tự áp vào các đoạn sudo. Việc bỏ sudo cần test thực tế vì portal user thường thiếu quyền đọc `hr.employee`.
- Rule store manager dùng department scope để hỗ trợ RGM/SM xem hồ sơ trong nhà hàng. Nếu nghiệp vụ muốn chặt hơn, có thể thu về chỉ direct manager/company rep ở Phase test.
- Chưa chạy cài mới/upgrade module trong Odoo container ở Phase 4.

## 6. File đã thay đổi

- `__manifest__.py`
- `security/ir.model.access.csv`
- `security/security_rules.xml`
- `structure/module_map.json`
- `structure/details/__manifest__.py.json`
- `structure/details/security__ir.model.access.csv.json`
- `notes/PHASE_4_DA_TRIEN_KHAI_SECURITY_0215.md`

## 7. Đề xuất Phase tiếp theo

Phase 5 nên tập trung vào test cài mới và test luồng chính:

- Install/upgrade module trên database test.
- Test quyền portal, store manager, HRBP, HR manager.
- Test luồng Store Level và Company Level sau Phase 3.
- Rà lại các `.sudo()` trong portal dựa trên kết quả test thực tế.
