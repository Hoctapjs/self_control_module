# Phase 3 – Kết quả rà soát sau khi Codex triển khai + Phase 3H sửa lỗi

> Tài liệu này ghi lại kết quả kiểm tra việc Codex đã triển khai Phase 3 (các phase con 3A → 3G) so với
> [plan_phase3_0502_cho_codex.md](plan_phase3_0502_cho_codex.md), và đề xuất **Phase 3H** để sửa các điểm còn lại.
> Ngày rà soát: 2026-05-21. Module version hiện tại: `19.0.4.0.0`.

## 1. Phương pháp kiểm tra

- Đã `py_compile` toàn bộ file Python: **PASS**.
- Đã validate well-formed toàn bộ file XML (data/views/reports/security/demo/wizards): **PASS**.
- Đã đối chiếu cross-reference: report xmlid ↔ print methods, sequence code ↔ `next_by_code`, group xmlid ↔ button/`has_group`/access csv, model xmlid ↔ record rules: **khớp**.
- Đã trace logic từng action so với bộ test `tests/test_0502_flow.py` (8 test): logic nhất quán.
- **Chưa chạy live install** vì môi trường này không có PostgreSQL/DB. Cần chạy `odoo-bin -i M02_P0502 -d <db> --test-enable --stop-after-init` trên instance thật để xác nhận 8 test pass và view inherit không vỡ xpath.

## 2. Kết luận tổng quát

**Phase 3 đã được triển khai gần như đầy đủ và đúng hướng.** Tất cả 7 phase con đều có mặt và khớp với plan:

| Phase con | Trạng thái | Ghi chú |
|---|---|---|
| 3A Fix bug & dọn dẹp | ✅ Đã làm | 3.1, 3.2, 3.3, 3.5, 3.7, 3.8, 3.9, 3.13, 3.15 đều đã sửa đúng. 3.4 chủ động hoãn (xem 3.3 bên dưới). |
| 3B Outside Service Flow | ✅ Đã làm | Model `x_psm_outside_service_request` + state machine vendor + PO + acceptance + tự tạo khi route=outside_service. |
| 3C Custom Stages + state machine | ✅ Đã làm (1 điểm cần tinh chỉnh) | 11 stage + sync + validation. Còn vấn đề ordering FSM (mục 3.1 bên dưới). |
| 3D Security groups + record rules | ✅ Đã làm | 6 group + record rule cho 5 model + access csv phân quyền. |
| 3E Reports + Sequence | ✅ Đã làm | 5 report + document pack + wizard + 5 sequence chứng từ + sequence outside service. |
| 3F Rework loop | ✅ Đã làm | `x_psm_request_rework_history` + `action_psm_reopen_for_rework` + reopen-with-new-task. |
| 3G Demo + Tests | ✅ Đã làm | Demo đủ 5 stage + 8 test bao phủ các luồng chính. |

Các xác nhận cụ thể về Phase 3A (đã sửa đúng):
- **3.1** `action_psm_mark_inspected`: có guard `if record.x_psm_0502_inspected_at: continue`; relax checklist/worksheet khi `no_action_needed`; view ẩn nút sau khi đã inspected. ✅
- **3.2** `_psm_get_proposal_approval_flow_resolution`: `two_level` chỉ khi `approval_required=True`. ✅
- **3.3** filter `filter_psm_material_manual_review_required` đổi domain sang `material_approval_value_rule in (manual_review_required, manual_review_required_source_type)`. ✅
- **3.5** material approval value dùng `x_psm_estimated_unit_price` (+ subtotal compute, default từ `standard_price`). ✅
- **3.7** có `action_psm_recheck_stock_after_purchase` + nút trên view. ✅
- **3.8** `action_psm_notify_lead` unlink activity của lead cũ khi đổi lead. ✅
- **3.9** guard idempotent ở mark_inspected, mark_execution_completed, mark_acceptance_reviewed, mark_service_assessed... ✅
- **3.13** description preventive request đã chuyển sang tiếng Anh. ✅
- **3.15** có cron `cron_psm_create_intake_sla_warning_activities` + record cron trong `data/ir_cron_data.xml`. ✅
- **3.16** filter trùng tên `filter_psm_store_request` đã gom còn 1. ✅ (Lưu ý: chưa tách `maintenance_request_views.xml` thành 4 file con như gợi ý — không bắt buộc, chấp nhận được.)

## 3. Các điểm còn lại cần sửa (Phase 3H)

> **CẬP NHẬT 2026-05-21**: Phase 3H đã được triển khai trực tiếp. Version module bump lên `19.0.5.0.0`.
> Trạng thái từng mục: 3.1 ✅, 3.2 ✅, 3.3 ✅, 3.4 ✅, 3.5 ✅. 3.6 vẫn để tùy chọn (chưa làm).
> Tóm tắt thay đổi đã thực hiện:
> - **3.1**: `_psm_get_0502_stage_xmlid_from_progress` bỏ điều kiện `or self.x_psm_0502_fsm_task_id`, chỉ vào In Execution khi `execution_started_at`. Thêm test `test_09_fsm_task_does_not_force_in_execution_stage`.
> - **3.2**: thêm `post_init_hook` trong `__init__.py` (đăng ký trong manifest) để fold 4 stage maintenance gốc (`maintenance.stage_0/1/3/4`).
> - **3.3**: xoá comment `note-fix`, thay bằng giải thích giữ Selection.
> - **3.4**: đổi 6 record rule store sang `('...department_id', 'in', user.employee_ids.department_id.ids)` + chuyển block rule sang `noupdate="0"` để fix áp dụng khi upgrade. Thêm test `test_10_store_user_without_department_sees_nothing`.
> - **3.5**: `action_psm_acceptance_review` (outside service) prefill `acceptance_equipment_result='operating_normally'` khi accepted + post message hướng dẫn store hoàn tất contact name/role.
>
> Đã `py_compile` toàn bộ Python + validate XML: PASS. **Vẫn cần chạy live `--test-enable` để xác nhận 10 test pass.**

> Không có lỗi gây crash/chặn cài đặt phát hiện qua phân tích tĩnh. Các điểm dưới đây là **tinh chỉnh** để state machine và UX đúng nghiệp vụ hơn. Vì số lượng ít nên gom **một phase con duy nhất: Phase 3H**.

### 3.1. [Mức Trung bình] State machine: `fsm_task_id` đẩy stage lên "In Execution" quá sớm

**Vị trí**: [maintenance_request.py:425-426](../models/maintenance_request.py) trong `_psm_get_0502_stage_xmlid_from_progress`:
```python
if self.x_psm_0502_execution_started_at or self.x_psm_0502_fsm_task_id:
    return "M02_P0502.stage_psm_0502_in_execution"
```

**Vấn đề**:
- `action_psm_create_fsm_task` chỉ yêu cầu đã `planned` ([maintenance_request.py:1681](../models/maintenance_request.py)), nút "Create FSM Task" hiện ngay sau khi planned (trước bước propose/approve/service/material).
- Với request corrective, khi CMT Lead bấm tạo FSM task sớm, `fsm_task_id` được set → stage nhảy thẳng lên **In Execution**, bỏ qua các cột Proposed / Approved / Service Assessed / Material Ready trên Kanban.
- Hệ quả phụ: `_psm_validate_0502_stage_write` lấy `allowed_stage = in_execution (seq 40)` nên cho phép kéo request tới bất kỳ stage ≤ 40, làm **mất tác dụng của state machine guard**.
- Nhánh preventive thì hành vi này lại đúng (preventive: plan → dispatch → execute, không cần propose/approve). Nên cần phân biệt 2 nhánh, hoặc đơn giản là chỉ coi là In Execution khi đã thực sự bắt đầu thực thi.

**Cách sửa (đề xuất đơn giản, ít rủi ro nhất)**:
1. Trong `_psm_get_0502_stage_xmlid_from_progress`, đổi điều kiện in_execution để **không** dựa vào riêng `fsm_task_id`:
   ```python
   if self.x_psm_0502_execution_started_at or self.x_psm_0502_execution_completed_at:
       return "M02_P0502.stage_psm_0502_in_execution"
   ```
   (bỏ `or self.x_psm_0502_fsm_task_id`).
2. Cân nhắc đồng bộ luôn `_psm_get_progress_checkpoint` ([maintenance_request.py:324](../models/maintenance_request.py)) bỏ `or self.x_psm_0502_fsm_task_id` ở nhánh `execution` để monitoring checkpoint nhất quán với stage. **Lưu ý**: việc này ảnh hưởng các filter/report đang dùng checkpoint = `execution`; nếu muốn an toàn, chỉ sửa phần stage (bước 1) và giữ nguyên checkpoint, chấp nhận stage và checkpoint lệch nhẹ ở giai đoạn FSM-đã-tạo-nhưng-chưa-bắt-đầu.
3. Sau khi sửa, request có FSM task nhưng chưa start sẽ map về `material_ready` / `service_assessed` (theo các điều kiện phía dưới trong hàm) → đúng tiến độ thực tế hơn, và guard state machine chặt lại.
4. Bổ sung test: tạo store request, plan → create_fsm_task (chưa execution_started) → assert `stage_id` KHÔNG phải `in_execution` (kỳ vọng material_ready hoặc service_assessed tuỳ data).

**Acceptance**: Request corrective vừa tạo FSM task (chưa start) không nhảy sang In Execution; preventive request sau khi execution_started vẫn vào In Execution đúng.

### 3.2. [Mức Thấp] Stage 0502 dùng chung bảng `maintenance.stage` toàn cục

**Vị trí**: [data/maintenance_stage_data.xml](../data/maintenance_stage_data.xml) (11 stage, `<odoo>` không noupdate).

**Vấn đề**: 11 stage 0502 (seq 5–55) được thêm vào bảng `maintenance.stage` toàn cục, **cùng tồn tại** với 4 stage gốc của Odoo (New Request / In Progress / Repaired / Scrap). Kanban maintenance.request sẽ hiển thị lẫn lộn ~15 cột. Vì module đặt default `request_source` nên mọi maintenance.request đều bị coi là 0502, nhưng các stage gốc vẫn còn.

**Cách sửa (chọn 1)**:
- **Phương án A (khuyến nghị, nhẹ)**: Thêm migration/`post_init_hook` set `fold=True` (hoặc `active=False`) cho 4 stage gốc của maintenance để Kanban chỉ còn cột 0502. Phải kiểm tra không xoá data người dùng đang dùng.
- **Phương án B**: Chấp nhận và **ghi rõ trong tài liệu** rằng đây là instance maintenance dành riêng cho 0502; key user được hướng dẫn bỏ qua/ẩn cột gốc.
- Không khuyến nghị tách model stage riêng (Odoo `maintenance.request.stage_id` trỏ cứng `maintenance.stage`).

**Acceptance**: Kanban 0502 chỉ hiển thị (hoặc ưu tiên) 11 cột 0502; hoặc có tài liệu nêu rõ giới hạn này.

### 3.3. [Mức Thấp] Đóng technical debt `x_psm_0502_inspection_result` (Selection)

**Vị trí**: [maintenance_request.py:2894-2903](../models/maintenance_request.py) — vẫn là `Selection` và còn comment `# note-fix: se custom lai thanh dang many2one...`.

**Vấn đề**: Không phải lỗi (đã được hoãn có chủ ý), nhưng comment "note-fix" vẫn còn gây hiểu nhầm còn việc dang dở.

**Cách sửa (chọn 1)**:
- **Phương án A (nhẹ)**: Xoá comment `note-fix` nếu quyết định giữ Selection lâu dài (Selection 2 giá trị là đủ cho nghiệp vụ hiện tại).
- **Phương án B (đầy đủ)**: Chuyển sang master model `x_psm_inspection_result` như mô tả ở mục 3.4 của plan gốc (kèm related `_code`, data XML, đổi mọi so sánh `== 'action_needed'` sang `_code`, migration). Chỉ nên làm nếu business cần thêm option kết quả kiểm tra.

**Acceptance**: Không còn comment "note-fix" treo; hoặc model master được tạo đầy đủ + test cập nhật.

### 3.4. [Mức Thấp] Record rule store user khi không có employee/department

**Vị trí**: [security/0502_security.xml:57](../security/0502_security.xml) và các rule store khác dùng `user.employee_id.department_id.id`.

**Vấn đề**: Nếu store user không gắn `hr.employee` (hoặc employee không có department), `user.employee_id.department_id.id` = `False` → domain `[('x_psm_0502_department_id', '=', False)]` → store user nhìn thấy mọi request **chưa gán department**. Rò rỉ nhẹ + khó hiểu.

**Cách sửa**:
- Đổi domain sang dạng chặn hẳn khi không có department, ví dụ dùng `('x_psm_0502_department_id', 'in', user.employee_ids.department_id.ids)` (nếu muốn hỗ trợ nhiều employee) hoặc thêm điều kiện loại trừ `False`. Cách an toàn:
  ```xml
  <field name="domain_force">['&amp;', ('x_psm_0502_department_id', '!=', False), ('x_psm_0502_department_id', 'in', user.employee_ids.department_id.ids)]</field>
  ```
- Áp dụng nhất quán cho cả material_line / planning_history / proposal_history / rework_history / outside_service store rules.

**Acceptance**: Store user không gắn department không nhìn thấy bất kỳ request 0502 nào (thay vì thấy nhóm department rỗng). Test bổ sung 1 case store user không có employee.

### 3.5. [Mức Thấp] Outside service: acceptance review chưa set đủ field nghiệm thu trên request

**Vị trí**: [outside_service_request.py:270-287](../models/outside_service_request.py) `action_psm_acceptance_review`.

**Vấn đề**: Hàm này chỉ ghi `x_psm_0502_acceptance_result` + `x_psm_0502_acceptance_note` lên request. Nhưng `action_psm_mark_acceptance_reviewed` của request lại bắt buộc thêm `acceptance_contact_name`, `acceptance_contact_role`, `acceptance_equipment_result`. Người dùng phải tự nhập 3 field này ở request rồi mới đóng được (test_03 đang nhập tay). UX rời rạc.

**Cách sửa (chọn 1)**:
- **Phương án A**: Trong `action_psm_acceptance_review`, prefill sẵn `x_psm_0502_acceptance_equipment_result = 'operating_normally'` (nếu accepted) và để contact_name/role trống cho store nhập — kèm thông báo hướng dẫn.
- **Phương án B**: Thêm các field nhập (contact name/role/equipment result) ngay trên form outside_service `Acceptance` page, rồi copy sang request khi review. Rõ ràng hơn cho store.

**Acceptance**: Sau khi outside service accepted, store hoàn tất nghiệm thu request với số thao tác tối thiểu; có hướng dẫn field còn thiếu.

### 3.6. [Tùy chọn] Tách `maintenance_request_views.xml` (1900+ dòng)

Đây là gợi ý 3.16 trong plan gốc chưa thực hiện (file vẫn gộp form/list/search/actions). Không bắt buộc, chỉ nên làm nếu muốn dễ bảo trì. Nếu làm: tách thành `maintenance_request_form.xml`, `_list.xml`, `_search.xml`, `_actions.xml` và cập nhật thứ tự trong `__manifest__.py`.

## 4. Thứ tự đề xuất cho Phase 3H

| Việc | Mức | Bắt buộc | Ghi chú |
|---|---|---|---|
| 3.1 Sửa mapping stage In Execution | Trung bình | Nên làm | Ảnh hưởng tính đúng của state machine |
| 3.2 Xử lý stage gốc maintenance | Thấp | Nên làm | Phương án A hoặc B |
| 3.4 Record rule store no-department | Thấp | Nên làm | Bảo mật |
| 3.5 Outside service acceptance UX | Thấp | Nên làm | Giảm thao tác thủ công |
| 3.3 Đóng note-fix inspection_result | Thấp | Tùy | Xoá comment hoặc làm Many2one |
| 3.6 Tách file view | Thấp | Tùy | Chỉ là maintainability |

**Ước lượng effort Phase 3H**: ~1 ngày làm việc (chủ yếu là 3.1 + test, còn lại nhỏ).

## 5. Việc cần làm trước khi đóng Phase 3 (bắt buộc với người vận hành, không phải codex)

1. **Chạy test thật**: `odoo-bin -i M02_P0502 -d <db> --test-enable --stop-after-init` và xác nhận 8 test trong `tests/test_0502_flow.py` đều PASS.
2. **Cài demo**: cài module với `--without-demo=False` (hoặc DB có demo) để xác nhận `demo/psm_0502_demo_data.xml` nạp không lỗi và mọi menu mở được.
3. **Smoke UI**: mở form 1 request đi hết 21 bước, in thử từng report + document pack, kiểm tra Kanban theo stage 0502.
4. **Kiểm thử phân quyền**: đăng nhập bằng store user / cmt user / cmt lead / store approver để xác nhận record rule + nút theo group hoạt động đúng.

---

**Người soạn**: Claude (review Phase 3 sau khi Codex triển khai).
**Ngày**: 2026-05-21.
