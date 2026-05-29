# Plan Phase 3 0502 cho Codex – Kiểm tra trạng thái và danh mục cần làm

> Tài liệu này tổng hợp:
> 1. Trạng thái triển khai hiện tại của module `M02_P0502` so với scope Phase 3 trong [plan_trien_khai_0502_theo_phase.md](plan_trien_khai_0502_theo_phase.md) và lưu đồ 21 bước trong [dac_ta_nghiep_vu_0502_bao_tri_sua_chua_may_moc.md](dac_ta_nghiep_vu_0502_bao_tri_sua_chua_may_moc.md).
> 2. Danh sách hạng mục Phase 3 còn chưa làm.
> 3. Các điểm bất hợp lý trong code/UX hiện tại + cách sửa chi tiết.
> 4. Đề xuất chia Phase 3 thành nhiều phase con (3A → 3G) cho codex triển khai tuần tự.

## 1. Tổng kết những gì Phase 1 và Phase 2 đã làm

Module hiện tại (`addons/M02_P0502`) đã hoàn thành **toàn bộ Phase 1 + Phase 2** và một **phần Phase 3**, cụ thể:

### 1.1. Cấu trúc dữ liệu đã có

- **Master data**: `x_psm_request_source`, `x_psm_request_type` + data XML mặc định (`store_request`, `preventive_schedule`, `maintenance`, `repair`, `inspection`).
- **Inherit chính**: `maintenance.request` (3.418 dòng) – chứa toàn bộ trục logic 21 bước.
- **Inherit phụ**: `maintenance.equipment`, `maintenance.equipment.category`, `maintenance.team`, `hr.department`, `project.task`, `stock.picking`, `purchase.order`.
- **Object phụ**: `x_psm_request_material_line`, `x_psm_request_planning_history`, `x_psm_request_proposal_history`.
- **Cron**: `ir_cron_psm_generate_preventive_requests` sinh request preventive hằng ngày.

### 1.2. Các action đã có

| Bước nghiệp vụ | Action | Trạng thái |
|---|---|---|
| B1–B2 Tạo phiếu / ticket | `create` + auto receive khi manual | ✅ |
| B3 CMT tiếp nhận | `action_psm_receive_request` | ✅ |
| B4 Kiểm tra thực tế ban đầu | `action_psm_mark_inspected` | ✅ |
| B5–B6 Cron + notify lead | `cron_psm_generate_preventive_requests` + `action_psm_notify_lead` + `action_psm_acknowledge_lead_assignment` | ✅ |
| B7–B8 Lập kế hoạch | `action_psm_mark_planned` + planning history | ✅ |
| B9 Điều phối nhân sự / tạo FSM task | `action_psm_create_fsm_task` | ✅ |
| B10 Báo cáo theo dõi tình trạng | `progress_checkpoint`, `supply_branch_status`, dashboard monitoring | ✅ |
| B11 Đề xuất phương án/báo giá | `action_psm_mark_proposed` + proposal history + revision compare | ✅ |
| B12 Cửa hàng duyệt timeline/cost | `action_psm_submit_for_approval` / `approve` / `reject`, hỗ trợ 2 cấp | ✅ |
| B13 Thẩm định outside service | `action_psm_mark_service_assessed` | ⚠️ (chỉ mark, **không có flow outside service tiếp theo**) |
| B14 Kiểm tra vật tư phát sinh | `action_psm_mark_material_checked` + material lines | ✅ |
| B15 Lập yêu cầu xuất kho | `action_psm_create_stock_picking` | ✅ |
| B16 Kiểm tra tồn kho | `action_psm_check_stock_availability` | ✅ |
| B17 CMT Lead duyệt yêu cầu vật tư | `action_psm_submit_material_approval` / `approve` / `reject` | ✅ |
| B18 Xuất kho thực tế | `action_psm_validate_stock_picking` + `action_psm_mark_stock_issued` | ✅ |
| B19 Mua ngoài | `action_psm_create_purchase_order` + prefill | ✅ |
| B20 Thực hiện sửa chữa | `action_psm_mark_execution_started` + `action_psm_mark_execution_completed` + FSM task execution fields | ✅ |
| B21 Nghiệm thu & đánh giá | `action_psm_mark_acceptance_reviewed` + đóng stage | ✅ |

### 1.3. Phase 3 đã có một phần

- ✅ **Approval 2 cấp** (`x_psm_0502_approval_flow_type = two_level` qua department final approver).
- ✅ **Planning history / Proposal history** với revision count, change reason bắt buộc khi re-plan / re-propose.
- ✅ **Inspection / FSM templates** theo `equipment.category` và `request_type` (intake question, proposal template, FSM task template, checklist template, material template).
- ✅ **Intake detail gap** (problem detail, impact scope, contact name/phone) bắt buộc cho store/system request.
- ✅ **SLA intake** (deadline + result on_time/late) trên team.
- ✅ **Progress checkpoint + supply branch status** monitoring xuyên 21 bước.
- ✅ **Preventive monitoring**: status, exception_status (multi_cycle_overdue / open_request_stalled / due_now).
- ✅ **Auto-approve theo cost limit** (proposal + material).
- ✅ **Lead acknowledgment** (pending / acknowledged).

## 2. Phase 3 – Những hạng mục CHƯA LÀM

Phase 3 yêu cầu 5 nhóm hạng mục (theo `plan_trien_khai_0502_theo_phase.md` mục 6.Phase 3):

1. **Workflow 21 bước đầy đủ bám sát lưu đồ** – ⚠️ **chưa đầy đủ**: thiếu state machine bắt buộc, vẫn dùng kanban_state + computed checkpoint.
2. **Object trục chính xuyên suốt toàn bộ quy trình** – ⚠️ **đang dùng `maintenance.request` làm trục chính**, chấp nhận được; không cần tách object mới nếu doanh nghiệp không yêu cầu, nhưng cần **stage tuỳ biến** cho 0502.
3. **Outside service flow riêng** – ❌ **CHƯA LÀM**, mới chỉ có flag + service_route.
4. **Bộ chứng từ đặc thù** – ❌ **CHƯA LÀM**: chưa có QWeb report nào, chưa có sequence riêng cho mã 0502.
5. **Approval nhiều tầng theo phân quyền doanh nghiệp** – ⚠️ **mới có 2 cấp store approver**, **chưa có security groups + record rules riêng** cho CMT / CMT Lead / Store Approver / Store Final Approver / Store User.

Ngoài ra còn các gap thực tế phát hiện trong quá trình rà soát code:

- ❌ **Demo data** – thư mục `demo/` rỗng, chưa có demo equipment, request, team config.
- ❌ **Report monitoring riêng** – đã có search/group view nhưng chưa có pivot/graph view tuỳ biến (`<pivot>`, `<graph>` chưa được khai báo trong xml, mặc dù action có `view_mode='...pivot,graph'`).
- ❌ **Custom stages cho `maintenance.request`** – vẫn dùng stage gốc của Odoo (New Request → In Progress → Repaired → Scrap), không tách stage theo 21 bước.
- ❌ **Activity tạo cho intake SLA late** – có field intake_sla_result nhưng không tự sinh activity cảnh báo CMT khi sắp / đã quá hạn.
- ❌ **Multi-round acceptance / rework loop** – khi acceptance_result = `rework_required`, không có button "Reopen for Rework" hay cơ chế tạo request con.
- ❌ **Wizard "Generate 0502 Document Pack"** – để in 1 lần cả: phiếu yêu cầu + phiếu kiểm tra + phiếu đề xuất + phiếu xuất kho + biên bản nghiệm thu.
- ❌ **Smoke test scripts** – chưa có `tests/` folder.

## 3. Điểm bất hợp lý hiện tại + cách sửa chi tiết

> Mỗi mục dưới đây là **một issue độc lập** Codex có thể fix mà không ảnh hưởng kiến trúc lớn.

### 3.1. `action_psm_mark_inspected` UX confusing (B4)

**Vị trí**: [maintenance_request.py:550-586](../models/maintenance_request.py), [maintenance_request_views.xml:22-29](../views/maintenance_request_views.xml).

**Vấn đề**:
- Button `Mark Inspected` chỉ hiện khi `x_psm_0502_inspection_result` đã set → nhưng button không có điều kiện ẩn sau khi đã inspected (`x_psm_0502_inspected_at`).
- Khi `inspection_result = no_action_needed`, action vẫn validate đầy đủ checklist + worksheet → quá chặt vì trường hợp không cần xử lý không cần checklist chi tiết.

**Cách sửa**:
1. Trong view, đổi `invisible="archive or not x_psm_0502_inspection_result"` thành `invisible="archive or not x_psm_0502_inspection_result or x_psm_0502_inspected_at"`.
2. Trong action, relax validation khi `inspection_result == 'no_action_needed'`: chỉ yêu cầu `inspection_result`, `inspection_symptom_status`, `inspection_safety_risk`, không bắt buộc checklist/worksheet result khi đã có template (cho phép skip checklist nếu không cần xử lý).

### 3.2. Logic auto-approve làm `flow_type` mâu thuẫn

**Vị trí**: [maintenance_request.py:1471-1515](../models/maintenance_request.py) `action_psm_submit_for_approval`.

**Vấn đề**:
- `_psm_get_proposal_approval_flow_resolution` resolve `flow_type = two_level` dựa trên `final_approver_user`, **trước khi** kiểm tra auto-approve.
- Khi auto-approve (`approval_required = False`), code set `current_level = level_count = 2` → log lưu là two_level nhưng thực tế bỏ qua duyệt → audit trail sai.

**Cách sửa**:
- Trong `_psm_get_proposal_approval_flow_resolution`, sau khi gọi `_psm_get_proposal_approval_resolution`, **chỉ tính two_level khi `approval_required = True`**. Nếu auto-approved thì luôn `flow_type = 'single_level'`, `level_count = 1`, `final_approver_user = False`.

### 3.3. Filter `filter_psm_material_manual_review_required` sai domain

**Vị trí**: [maintenance_request_views.xml:1309-1313](../views/maintenance_request_views.xml).

**Vấn đề**: Domain giống hệt `filter_psm_material_approval_required`, không lọc đúng manual review:
```xml
domain="[('x_psm_0502_material_approval_required', '=', True)]"
```

**Cách sửa**: Đổi domain thành `[('x_psm_0502_material_approval_value_rule', '=', 'manual_review_required')]` để phân biệt với case `manual_review_required_source_type`. Nếu muốn gom cả 2 manual rule, dùng `('x_psm_0502_material_approval_value_rule', 'in', ['manual_review_required', 'manual_review_required_source_type'])`.

### 3.4. Field `x_psm_0502_inspection_result` đang Selection nhưng note đánh dấu sẽ chuyển Many2one

**Vị trí**: [maintenance_request.py:2358-2367](../models/maintenance_request.py).

**Vấn đề**: Code comment ghi `note-fix: se custom lai thanh dang many2one de de dang mo rong them option moi trong tuong lai neu can` – đây là technical debt mà Phase 3 cần đóng để bộ master data nhất quán (đã có request_source, request_type là Many2one).

**Cách sửa** (Phase 3E):
1. Tạo model master `x_psm_inspection_result` với fields `name`, `code`, `sequence`, `active`, `requires_treatment` (bool, true cho action_needed), `requires_followup_documentation`.
2. Data XML chuẩn: `inspection_result_no_action_needed`, `inspection_result_action_needed` + 2-3 option mở rộng (`needs_monitoring`, `needs_outside_check`).
3. Đổi field thành `Many2one('x_psm_inspection_result')` + thêm related field `x_psm_0502_inspection_result_code` để các domain/filter hiện tại không vỡ.
4. Update tất cả `record.x_psm_0502_inspection_result == 'action_needed'` → `record.x_psm_0502_inspection_result_code == 'action_needed'`.
5. Migration script (`pre_migrate`) cập nhật giá trị cũ.

### 3.5. `_psm_get_material_approval_resolution` dùng `standard_price`

**Vị trí**: [maintenance_request.py:680-684](../models/maintenance_request.py).

**Vấn đề**: Giá auto-approve dựa trên `standard_price` (cost) → không phản ánh giá vendor nếu mua ngoài, dễ chênh lệch lớn.

**Cách sửa**:
- Thêm field `x_psm_estimated_unit_price` (Monetary) trên `x_psm_request_material_line` (mặc định = `product.standard_price`, user có thể override).
- Tính `estimated_material_value = sum(line.x_psm_estimated_unit_price * line.x_psm_estimated_qty)`.
- Thêm `x_psm_estimated_subtotal` (compute = unit_price * qty) hiển thị trên list view material lines.

### 3.6. Acceptance "rework_required" không có cách reopen luồng

**Vị trí**: [maintenance_request.py:2054-2093](../models/maintenance_request.py) `action_psm_mark_acceptance_reviewed`.

**Vấn đề**: Khi rework_required, request chỉ set `kanban_state = blocked`, không có cách quay lại bước thực thi/yêu cầu vật tư mới mà không tạo request mới.

**Cách sửa** (Phase 3F):
1. Thêm field `x_psm_0502_rework_round_count` (Integer).
2. Thêm action `action_psm_reopen_for_rework`:
- Chỉ enable khi `acceptance_result in ('rework_required', 'follow_up_needed')` và `acceptance_reviewed_at`.
- Tăng `rework_round_count` += 1.
- Reset `acceptance_*` về False, set `kanban_state = normal`.
- Reset `execution_started_at`, `execution_completed_at`, `execution_note` về False.
- Thêm note vào chatter: "Reopened for rework round %s. Reason: %s".
- Cho phép tạo FSM task mới (link cũ vẫn giữ) hoặc reopen task cũ tuỳ flag.
3. Thêm field `x_psm_0502_rework_history_ids` (One2many sang model mới `x_psm_request_rework_history`) lưu mỗi lần reopen.

### 3.7. Stock check không re-evaluate sau khi PO done

**Vị trí**: [maintenance_request.py:1908-1947](../models/maintenance_request.py) `action_psm_create_purchase_order` + [maintenance_request.py:1673-1716](../models/maintenance_request.py) `action_psm_check_stock_availability`.

**Vấn đề**: Sau khi PO về và vật tư nhập kho, user phải tự bấm "Check Stock Availability" lại → button hiện đang ẩn nếu `stock_check_result != 'not_available'` không có nhưng button submit_material_approval lại yêu cầu `stock_check_result == 'available'`.

**Cách sửa**:
- Thêm button "Re-check Stock After Purchase" hiển thị khi `purchase_order_state in ('purchase', 'done')` và `stock_check_result == 'not_available'`.
- Hoặc tự động chạy lại `action_psm_check_stock_availability` khi `purchase.order` chuyển sang `done` qua override `_action_done` của `purchase.order` để gọi back vào request (cần cẩn thận tránh recursion).

### 3.8. Cron sinh activity duplicate khi lead chưa acknowledge

**Vị trí**: [maintenance_equipment.py:357-402](../models/maintenance_equipment.py) `cron_psm_generate_preventive_requests`.

**Vấn đề**: Code đã kiểm tra `existing_activity` đúng, nhưng nếu lead user thay đổi cấu hình team (đổi lead) → activity cũ vẫn assign cho lead cũ → không bao giờ tự dọn dẹp.

**Cách sửa**:
- Trong `action_psm_notify_lead`, nếu `lead_notified_user_id` đã có và khác với resolve mới → unlink activity cũ và tạo activity mới cho lead mới.

### 3.9. Action `mark_inspected` không validate khi đã inspected

**Vị trí**: [maintenance_request.py:550](../models/maintenance_request.py).

**Vấn đề**: Action loop qua record và write `inspected_by/at`, không check nếu `inspected_at` đã có → có thể bị bấm lại và ghi đè user/timestamp.

**Cách sửa**:
- Thêm guard `if record.x_psm_0502_inspected_at: continue` (hoặc raise UserError nếu cố ý).
- Tương tự cho `action_psm_mark_planned`, `action_psm_mark_proposed`, `action_psm_mark_service_assessed`, `action_psm_mark_material_checked`, `action_psm_mark_execution_started`, `action_psm_mark_execution_completed`, `action_psm_mark_acceptance_reviewed` — kiểm tra lại tất cả mark_* để đảm bảo idempotent hoặc bị guard.

### 3.10. Stage maintenance.request không phản ánh tiến độ 0502

**Vị trí**: Stage gốc của Odoo (`maintenance.stage`: New Request / In Progress / Repaired / Scrap).

**Vấn đề**: 21 bước hiện chỉ phản ánh qua `x_psm_0502_progress_checkpoint` (compute, không control flow). Stage_id của request gốc vẫn để user tự drag → dễ tạo trạng thái không nhất quán.

**Cách sửa** (Phase 3C):
1. Tạo data stage 0502 (data XML, không update): `Intake`, `Inspected`, `Planned`, `Proposed`, `Approved`, `In Execution`, `Done`, `Rework`, `Cancelled`.
2. Override `write()` của maintenance.request: khi `progress_checkpoint` đổi → tự move `stage_id` đúng theo mapping.
3. Hoặc: Override `_compute_progress_checkpoint` để khi đến mỗi checkpoint thì set stage tương ứng (chấp nhận stage là computed/readonly).
4. Search view + filter cập nhật để default group by stage chuẩn 0502.

### 3.11. Filter Group "Approval Decided By" thiếu

Đã có nhưng theo dõi: OK.

### 3.12. Chưa có ràng buộc `_sql_constraints` tránh trùng linked picking / linked PO

**Vị trí**: [stock_picking.py](../models/stock_picking.py), [purchase_order.py](../models/purchase_order.py).

**Vấn đề**: Một request có thể tạo nhiều stock_picking (vì user có thể bấm tạo lại sau khi picking cũ bị cancel) → không sao, nhưng nên có constraint chỉ 1 active picking mỗi request để tránh confuse.

**Cách sửa**:
- Thêm helper `_psm_get_active_stock_picking` (state != cancel) trên maintenance_request.
- Trong `action_psm_create_stock_picking`, raise UserError nếu đã có active picking khác cancel.
- Tương tự PO đã có (đoạn `active_orders = ...filtered(lambda order: order.state != "cancel")`) – verify đoạn này đã chuẩn.

### 3.13. Description preventive request hard-code tiếng Việt không dấu

**Vị trí**: [maintenance_equipment.py:326-328](../models/maintenance_equipment.py) `_psm_prepare_preventive_request_vals`, và nhiều chuỗi khác.

**Vấn đề**: Chuỗi `"<p>Yeu cau phat sinh tu dong tu lich bao tri dinh ky cua thiet bi.</p>"` dùng tiếng Việt không dấu, không nhất quán với UI có dấu.

**Cách sửa**: Hoặc dùng tiếng Việt có dấu, hoặc tiếng Anh (`"<p>Preventive maintenance request automatically generated from equipment schedule.</p>"`). Đề xuất tiếng Anh để đồng bộ với phần lớn string khác trong module.

### 3.14. `x_psm_0502_treatment_proposal` không reset khi `mark_proposed` được gọi lại

**Vị trí**: [maintenance_request.py:1430-1467](../models/maintenance_request.py).

**Vấn đề**: Action chỉ raise nếu `proposed_at` đã có không, nhưng không có gì ngăn cản gọi lại nếu đã `mark_proposed`. Cụ thể, action hiện không check `proposed_at` → có thể gọi lại để regenerate summary với data mới, OK nhưng cần test.

**Cách sửa**: Có thể giữ nguyên (action chấp nhận re-run để re-build summary từ data hiện tại), nhưng nên thêm hook tạo proposal_history line khi re-mark (hiện chỉ create history nếu history list rỗng).

### 3.15. Thiếu activity SLA intake cảnh báo

**Vấn đề**: Có `intake_sla_deadline_at`, `intake_sla_result` nhưng không sinh activity nhắc CMT khi sắp đến deadline.

**Cách sửa** (Phase 3E):
- Thêm cron `cron_psm_intake_sla_warning` chạy mỗi giờ (interval_number=1, interval_type=hours):
- Tìm request có `received_at = False`, `intake_sla_deadline_at != False`, `intake_sla_deadline_at <= now + 1 hour`, không có activity todo "0502 Intake SLA Warning".
- Tạo activity todo cho `intake_owner_user_id` (đã có compute).

### 3.16. View `maintenance_request_views.xml` quá dài (1925 dòng) và filter trùng tên

**Vị trí**: [maintenance_request_views.xml:1389-1392](../views/maintenance_request_views.xml) `filter_psm_store_request` lặp lại 2 lần (line ~869 và ~1389).

**Vấn đề**: Trùng name → Odoo có thể warning hoặc override → cần dọn dẹp.

**Cách sửa**:
- Tách file `maintenance_request_views.xml` thành 4 file con: `_form.xml`, `_list.xml`, `_search.xml`, `_actions.xml` + cập nhật `__manifest__.py`.
- Rename filter duplicate: `filter_psm_store_request_v2` → đổi thành `filter_psm_requests_to_plan_store_request` hoặc gộp logic vào 1 filter duy nhất.

### 3.17. Security: tất cả group dùng `base.group_user`, chưa có phân quyền 0502

**Vị trí**: [security/ir.model.access.csv](../security/ir.model.access.csv), tất cả menu groups là `base.group_user` hoặc `maintenance.group_equipment_manager`.

**Vấn đề**: Phase 3 yêu cầu approval matrix theo vai trò, hiện không có security group / record rule nào riêng cho 0502.

**Cách sửa** (Phase 3D, xem chi tiết mục 4).

## 4. Đề xuất chia Phase 3 thành các phase con

Tổng quát: Phase 3 lớn → chia thành 7 phase con (3A → 3G). Mỗi phase con có thể trỉen khai độc lập, có acceptance criteria rõ ràng. Codex nên làm theo thứ tự liệt kê (dependency tăng dần).

### Phase 3A – Fix bug & dọn dẹp (effort thấp, độc lập)

Mục tiêu: clear technical debt + fix bug logic nhỏ. Không ảnh hưởng kiến trúc.

**Hạng mục**:
1. Fix [3.1] UX `mark_inspected` invisible + relax validate khi no_action_needed.
2. Fix [3.2] Logic `flow_type = single_level` khi auto-approved.
3. Fix [3.3] Domain filter `filter_psm_material_manual_review_required`.
4. Fix [3.9] Idempotent guard cho tất cả `action_psm_mark_*`.
5. Fix [3.13] Đổi description preventive request sang English.
6. Fix [3.16] Dọn duplicate filter name + tách file views theo loại form/list/search/actions.
7. Thêm field `x_psm_estimated_unit_price` + `x_psm_estimated_subtotal` (3.5).
8. Update `_psm_get_material_approval_resolution` dùng `estimated_unit_price`.
9. Thêm activity intake SLA warning + cron (3.15).
10. Thêm button "Re-check Stock After Purchase" + condition (3.7).
11. Audit notify_lead unlink activity cũ khi đổi lead (3.8).

**Acceptance criteria**:
- Không còn warning runtime, smoke test bằng tay đi qua 21 bước OK.
- Test idempotent: bấm `mark_inspected` 2 lần → lần 2 bị guard hoặc no-op.
- Material approval value đọc từ unit_price thay vì standard_price.

### Phase 3B – Outside Service Flow riêng

Mục tiêu: cung cấp luồng outside service đầy đủ thay vì chỉ flag.

**Hạng mục**:
1. Tạo model phụ `x_psm_outside_service_request`:
- Fields: `name` (sequence riêng `0502/OS/yyyy/nnnnn`), `request_id` (Many2one ngược về maintenance.request, required), `vendor_id` (res.partner), `quotation_received` (Boolean), `vendor_quote_amount` (Monetary), `vendor_quote_currency_id`, `vendor_lead_time_days` (Integer), `expected_complete_date` (Date), `scope_of_work` (Text), `service_type` (Selection: repair, inspection, calibration, warranty, other), `state` (draft, sent_to_vendor, quoted, approved, in_progress, completed, cancelled), `purchase_order_id` (Many2one purchase.order, optional), `acceptance_result` (Selection accepted, rejected, partial), `acceptance_note` (Text).
2. Override action `action_psm_mark_service_assessed`: nếu `service_route == 'outside_service'`, **tự tạo bản ghi `x_psm_outside_service_request`** ở trạng thái draft thay vì chỉ set flag.
3. Thêm các action trên outside service request:
- `action_send_to_vendor` (gửi RFQ qua email hoặc chỉ set state).
- `action_record_quote` (mở wizard nhập vendor_quote_amount + lead_time).
- `action_approve_vendor` (yêu cầu approver của cấp store, dùng lại approval flow).
- `action_create_purchase_order` (tạo `purchase.order` service product với vendor_id + amount).
- `action_mark_completed` (vendor xong) + `action_acceptance_review` (store nghiệm thu).
4. Trên maintenance.request, khi outside_service hoàn tất + accepted → cho phép `action_psm_mark_acceptance_reviewed` của request gốc (route bypass internal execution).
5. View form + list + search + menu cho outside_service_request.
6. Sequence `ir.sequence` cho mã `0502/OS/yyyy/nnnnn`.
7. Report QWeb in "Outside Service Quotation Request".

**Acceptance criteria**:
- Khi mark service_assessed với route = outside_service → tự tạo outside_service_request.
- Vendor flow chạy được: draft → sent → quoted → approved → PO → completed → accepted.
- Request gốc đóng được khi outside flow accepted, bypass material/stock/execution internal.

### Phase 3C – Custom Stages + State Machine

Mục tiêu: stage_id của maintenance.request phản ánh đúng tiến độ 0502, có ràng buộc chuyển stage.

**Hạng mục**:
1. Data XML stage 0502 (model `maintenance.stage`, noupdate=0 để dễ override):
- `Intake` (sequence 5)
- `Inspected` (sequence 10)
- `Planned` (sequence 15)
- `Proposed` (sequence 20)
- `Approved` (sequence 25)
- `Service Assessed` (sequence 30)
- `Material Ready` (sequence 35)
- `In Execution` (sequence 40)
- `Acceptance Review` (sequence 45)
- `Done` (sequence 50, done=True)
- `Cancelled` (sequence 55, done=True)
2. Trong compute `_compute_x_psm_0502_monitoring_status_fields`, mở rộng để auto set `stage_id` theo mapping checkpoint → stage (chỉ khi user chưa set manual qua context flag).
3. Constraint: không cho chuyển stage tự do khi flow chưa đến (vd: không cho move sang `In Execution` khi `material_approval_status != 'approved'` hoặc `service_route == 'outside_service'` đã chốt).
4. View kanban: thay group_by mặc định bằng `stage_id` (xem dạng kanban quy trình thật sự).
5. Migration script cập nhật stage cho request đang mở dựa trên checkpoint hiện tại.

**Acceptance criteria**:
- Tạo request mới → stage = Intake.
- Đi qua action_psm_receive → stage = Intake (giữ); mark_inspected → Inspected; mark_planned → Planned; ...
- Kanban hiển thị theo stage 0502.
- Drag stage không hợp lệ → raise UserError.

### Phase 3D – Security groups + Record rules

Mục tiêu: phân quyền theo vai trò CMT / CMT Lead / Store / Store Approver.

**Hạng mục**:
1. Tạo security groups (`security/0502_security.xml`):
- `group_psm_0502_store_user`: nhân viên cửa hàng, tạo request, xem request thuộc department mình, không thấy cost approval.
- `group_psm_0502_store_approver`: kế thừa store_user, có quyền approve proposal (cấp 1).
- `group_psm_0502_store_final_approver`: kế thừa store_approver, có quyền approve proposal cấp 2.
- `group_psm_0502_cmt_user`: kỹ thuật viên CMT, kế thừa `maintenance.group_equipment_user`, có quyền receive, inspect, propose, execute.
- `group_psm_0502_cmt_lead`: kế thừa cmt_user, có quyền plan, approve material, dispatch FSM.
- `group_psm_0502_manager`: kế thừa `maintenance.group_equipment_manager`, full access.
2. Record rules:
- Store user chỉ thấy maintenance.request có `x_psm_0502_department_id` thuộc `hr.employee.department_id` của user hiện tại (qua employee).
- CMT user thấy hết request trong team họ là thành viên.
- CMT lead thấy hết request trong team `x_psm_0502_lead_user_id = uid`.
- Manager thấy hết.
3. Update `ir.model.access.csv`:
- `x_psm_request_source`, `x_psm_request_type`: read all, write/create/unlink chỉ cho manager.
- `x_psm_request_material_line`: cmt_user write, store_user read.
- History tables: read all, không cho unlink trừ manager.
4. View: ẩn các trường nội bộ (cost note, approval rule) khi user không phải CMT.
5. Update menu groups: `0502 Lead Assigned Queue` chỉ hiện cho cmt_lead, `0502 Store Action Needed` hiện cho cả store_user.
6. Update button conditions: button "Approve Proposal" chỉ hiện cho user thuộc store_approver hoặc final_approver.

**Acceptance criteria**:
- Test với 3 user khác nhau: store user, cmt user, cmt lead.
- Store user chỉ thấy request department mình, không xem được approval cost rule.
- CMT user không thấy được approve proposal button (chỉ approver thấy).
- Record rule không gây leak data cross-department.

### Phase 3E – Bộ chứng từ in (QWeb Reports) + Sequence riêng

Mục tiêu: in được bộ chứng từ 0502 đặc thù.

**Hạng mục**:
1. Tạo `ir.sequence` riêng:
- `psm_0502_request_sequence`: code `psm.maintenance.request`, prefix `0502/REQ/%(year)s/`, padding 5.
- `psm_0502_inspection_sequence`: code `psm.inspection.report`, prefix `0502/INS/%(year)s/`.
- `psm_0502_proposal_sequence`: code `psm.proposal.document`, prefix `0502/PRO/%(year)s/`.
- `psm_0502_material_issue_sequence`: code `psm.material.issue.request`, prefix `0502/MAT/%(year)s/`.
- `psm_0502_acceptance_sequence`: code `psm.acceptance.record`, prefix `0502/ACC/%(year)s/`.
2. Override `create()` của maintenance.request: nếu `name` mặc định hoặc trống → set `name = sequence.next_by_code('psm.maintenance.request')`.
3. Thêm field char read-only cho mỗi mã chứng từ phụ (inspection_doc_no, proposal_doc_no, acceptance_doc_no) – set sequence khi tương ứng `*_at` được set lần đầu.
4. Tạo QWeb report `report_psm_0502_request_document`:
- Header: logo công ty, mã `0502/REQ/...`, ngày tạo, department, equipment.
- Body: thông tin request (name, request type, source, source_reference), intake detail (problem, impact, contact), initial inspection result + checklist + worksheet, treatment proposal (root cause, technical solution, cost, timeline), approval (rule, current level, approver), service assessment, material lines, execution summary, acceptance result.
- Footer: chữ ký Store, CMT, CMT Lead, Approver.
5. Tạo QWeb report sub:
- `report_psm_0502_inspection_report` (chỉ inspection phase).
- `report_psm_0502_treatment_proposal` (đóng vai trò báo giá đơn giản).
- `report_psm_0502_material_issue_request` (phiếu yêu cầu xuất kho – render lại từ material_lines).
- `report_psm_0502_acceptance_record` (biên bản nghiệm thu).
6. Thêm action `Print` trên header form cho mỗi report (dùng `action_report` Odoo standard).
7. Wizard `Print 0502 Document Pack` – cho phép tick các report cần in và in 1 lần combined.

**Acceptance criteria**:
- Mở 1 request đã có data đầy đủ → in được mỗi report ra PDF có format đúng.
- Sequence không duplicate, mỗi report có mã chứng từ riêng.
- Wizard combine in được file PDF gộp.

### Phase 3F – Multi-round Acceptance + Rework Loop

Mục tiêu: hỗ trợ chu trình lặp khi nghiệm thu không đạt.

**Hạng mục**:
1. Tạo model `x_psm_request_rework_history` (giống planning_history pattern):
- Fields: `request_id`, `round_number`, `previous_acceptance_result`, `rework_reason`, `created_by`, `created_at`, `linked_fsm_task_id`.
2. Thêm fields trên maintenance.request:
- `x_psm_0502_rework_round_count` (Integer, mặc định 0).
- `x_psm_0502_rework_history_ids` (One2many).
- `x_psm_0502_last_rework_at`, `x_psm_0502_last_rework_by_id`.
3. Action `action_psm_reopen_for_rework`:
- Chỉ enable khi `acceptance_result in ('rework_required', 'follow_up_needed')`.
- Tăng rework_round_count.
- Reset acceptance_*, execution_*.
- Cho phép choose: tạo FSM task mới hay reopen task cũ (qua context).
- Tạo rework_history line.
- Set stage_id về `In Execution`.
4. View: header button "Reopen for Rework" + page "Rework History".
5. Constraint: không cho `mark_acceptance_reviewed` lần 2 nếu rework chưa reopen.

**Acceptance criteria**:
- Mark acceptance = rework_required → button "Reopen for Rework" hiện.
- Bấm reopen → rework_round_count tăng, execution fields reset, có thể mark started/completed lại.
- Acceptance lần 2 = accepted → request đóng đúng stage Done.

### Phase 3G – Demo data + Tests + Documentation

Mục tiêu: hoàn thiện modul, có demo data đủ và test smoke chạy được.

**Hạng mục**:
1. Demo data (`demo/` folder, thêm vào manifest):
- 2-3 department demo (Hà Nội Store, HCM Store, Đà Nẵng Store) + partner mapping.
- 1 maintenance team demo có cấu hình đầy đủ (lead user, intake_sla_hours, picking_type, vendor, approvers).
- 5-6 equipment demo có category, 2 trong số đó bật preventive_schedule.
- 3-4 maintenance.request demo ở các stage khác nhau (intake, inspected, proposed, approved, in_execution, done).
- 1 outside_service_request demo (Phase 3B).
- Material lines + planning history + proposal history mẫu.
2. Smoke test (`tests/test_0502_flow.py`):
- Test 1: tạo request store_request → receive → inspect (action_needed) → plan → create_fsm → propose → submit_approval → approve → service_assess (internal) → material_check (no material) → execution_started → execution_completed → acceptance_accepted → stage Done.
- Test 2: tạo request preventive cron → cron generate → notify_lead → acknowledge → plan → ...
- Test 3: outside service flow end-to-end (Phase 3B).
- Test 4: material flow với stock not_available → create PO → re-check available → submit material approval → validate picking → execute.
- Test 5: rework loop (Phase 3F): acceptance rework_required → reopen → execute lại → acceptance accepted.
- Test 6: 2-cấp duyệt với store_final_approver.
- Test 7: auto-approve dưới limit.
- Test 8: record rule store_user không thấy request department khác.
3. Cập nhật `notes/huong_dan_su_dung_module_du_lieu_mau_M02_P0502_1.md` với data mới.
4. Tạo `notes/checklist_uat_0502_phase3.md` – checklist UAT bằng tiếng Việt cho key user duyệt.

**Acceptance criteria**:
- `odoo-bin -i M02_P0502 -d test_db --test-enable --stop-after-init` pass tất cả test.
- Demo data load không lỗi, tất cả menu mở được, mỗi menu có ít nhất 1 record.

## 5. Thứ tự ưu tiên đề xuất

| Phase con | Effort tương đối | Phụ thuộc | Có thể song song |
|---|---|---|---|
| 3A Fix bug & dọn dẹp | Thấp (1-2 ngày) | – | Có thể song song 3D |
| 3D Security groups | Trung bình (2-3 ngày) | – | Có thể song song 3A |
| 3E Reports + Sequence | Trung bình (2-3 ngày) | 3A (filter cleanup) | – |
| 3C Custom Stages | Trung bình (2 ngày) | 3A | – |
| 3B Outside Service Flow | Cao (4-5 ngày) | 3A, 3D | – |
| 3F Rework Loop | Trung bình (2 ngày) | 3A, 3C | – |
| 3G Demo + Tests | Trung bình (2-3 ngày) | Tất cả các phase trên | Cuối cùng |

**Tổng effort Phase 3** ước tính: 15–20 ngày làm việc cho 1 developer full-time.

## 6. Một số nguyên tắc Codex nên giữ

1. **Không xoá field cũ** – mọi field `x_psm_0502_*` đang có cần giữ vì có data thật/history. Khi cần đổi semantic (vd Selection → Many2one [3.4]) phải có migration script cẩn thận.
2. **Mọi action mới phải idempotent hoặc có guard rõ ràng** – tránh ghi đè timestamp/user audit.
3. **Mọi sửa view phải kèm test mở form thủ công** – view inherit dễ vỡ vì xpath.
4. **Mọi field mới phải có comment tiếng Việt giống style hiện tại** – đồng bộ codebase.
5. **Không refactor toàn bộ 3.418 dòng `maintenance_request.py`** một lần – tách dần theo phase con (vd Phase 3E tách phần build report, Phase 3B tách outside flow ra file riêng).
6. **Manifest version bump**: mỗi phase con tăng version `19.0.1.0.X` → `19.0.1.1.0` (3A), `19.0.1.2.0` (3D), `19.0.2.0.0` (3B), v.v.
7. **Mọi data XML mới phải `noupdate="1"` để bảo toàn customization khách hàng**.

## 7. Câu hỏi mở cần xác nhận với business trước khi triển khai

- [ ] Outside Service Flow có cần multi-vendor quote (3 báo giá so sánh) không? Hay 1 vendor preferred là đủ?
- [ ] Acceptance rework có giới hạn số lần không (vd max 3 round)?
- [ ] Sequence `0502/REQ/...` có cần reset hằng năm hay running số liên tục?
- [ ] Store user có được phép tạo request thay mặt department khác không (vd manager phụ trách nhiều store)?
- [ ] 2-cấp duyệt: có cần thêm cấp 3 (region manager) không?
- [ ] Outside service PO có ràng buộc về budget department không?

---

**Người soạn**: Claude (Phase 3 review).
**Ngày**: 2026-05-20.
**Nguồn dữ liệu rà soát**: toàn bộ thư mục `addons/M02_P0502` ở thời điểm rà soát.
