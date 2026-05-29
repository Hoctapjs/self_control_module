# Phase 3 - Bước 7 đã triển khai

## 1. Mục tiêu của bước này

`Bước 7` trong `Phase 3` tập trung vào việc nâng các queue hiện có từ mức “usable” lên mức “điều phối được thật” cho `CMT Lead`, nhưng vẫn giữ đúng scope của lưu đồ:

- `Bước 7` mới là điểm tổng hợp queue cho lead
- không mở rộng ngược các queue này sang `Bước 1`
- không dựng workflow engine hay object điều phối mới khi các field hiện có đã đủ dùng

Mục tiêu là giúp lead nhìn nhanh:

- request nào đã đủ điều kiện để lập kế hoạch
- request nào đang ở mức khẩn / critical
- request nào đã được gán ownership cho lead cụ thể

## 2. Tài liệu đã dùng để triển khai

### Convention

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`

### Structure map

- `structure/module_map.json`

Lưu ý:

- `module_map.json` hiện cũ hơn source code
- source code hiện tại là chuẩn cuối cùng

### Source xác nhận chính

- `notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md`
- `views/maintenance_request_views.xml`

## 3. Hướng triển khai đã chọn

Giữ đúng tinh thần “custom nhẹ đến vừa”:

- không thêm model mới
- không thêm object queue riêng
- không thêm cron / activity / escalation tự động
- chỉ tận dụng các field đã có để dựng thêm queue điều phối

Các queue mới được dựng trực tiếp từ dữ liệu nghiệp vụ sẵn có trên `maintenance.request`.

## 4. Các queue mới đã bổ sung

### 4.1. `Ready To Plan Queue`

Mục đích:

- gom các request đã đủ điều kiện để `CMT Lead` thực sự lập kế hoạch

Điều kiện:

- `x_psm_0502_ready_to_plan = True`
- `archive = False`
- `stage_id.done = False`

Mặc định:

- group theo `Store Department`

### 4.2. `Critical Queue`

Mục đích:

- gom các request cần được lead ưu tiên xử lý sớm

Điều kiện:

- `archive = False`
- `stage_id.done = False`
- và rơi vào ít nhất một trường hợp:
  - `Safety Risk Level = high`
  - hoặc `Action Urgency = immediate`
  - hoặc `Equipment Status = stopped`

Mặc định:

- group theo `Store Department`

### 4.3. `Lead Assigned Queue`

Mục đích:

- nhìn rõ request nào đã được giao ownership cho lead cụ thể

Điều kiện:

- `x_psm_0502_lead_notified_user_id != False`
- `archive = False`
- `stage_id.done = False`

Mặc định:

- group theo `Lead Notified User`

## 5. Thay đổi ở search view

Đã thêm các filter mới trong search view của `maintenance.request`:

- `Ready To Plan Queue`
- `Critical Queue`
- `Lead Assigned Queue`

Các filter này được thêm bên cạnh cụm queue điều phối đã có từ trước như:

- `Requests To Plan`
- `Preventive Queue`
- `Store Action Needed`
- `0502 Overdue`

## 6. Thay đổi ở action

Đã thêm các `ir.actions.act_window` mới:

- `action_psm_ready_to_plan_queue`
- `action_psm_critical_queue`
- `action_psm_lead_assigned_queue`

Các action này đều dùng:

- `res_model = maintenance.request`
- `view_mode = list,kanban,form,pivot,graph,activity`
- `search_view_id = view_psm_maintenance_request_search`

## 7. Thay đổi ở menu

Đã thêm các menu mới dưới `Maintenance > Maintenance Requests`:

- `0502 Ready To Plan Queue`
- `0502 Critical Queue`
- `0502 Lead Assigned Queue`

Mục tiêu:

- để `CMT Lead` có thể đi thẳng vào từng góc nhìn điều phối mà không phải set filter thủ công mỗi lần

## 8. Vì sao triển khai theo cách này

Lý do chọn cách làm này:

- các field phục vụ queue đã có sẵn từ `Phase 2` và `Phase 3` đầu kỳ
- không cần tạo model mới chỉ để biểu diễn queue
- bám đúng lưu đồ: `Bước 7` là điểm tổng hợp cho lead, không phải bàn intake mới
- tránh over-scope sang workflow điều phối nặng

## 9. Các phần cố ý chưa làm

Ở bước này chưa làm:

- activity tự động cho từng queue
- escalation nếu queue critical không được xử lý
- dashboard KPI riêng cho `Bước 7`
- assignment object / queue object riêng
- SLA cho từng queue điều phối

Các phần trên nếu cần thì nên để sang bước sâu hơn của `Phase 3` hoặc phase sau.

## 10. Case test đề xuất

### Case 1 - Ready to plan

1. Mở request đã có `x_psm_0502_ready_to_plan = True`
2. Vào menu `0502 Ready To Plan Queue`
3. Kỳ vọng request xuất hiện trong queue

### Case 2 - Critical

1. Tạo / mở request có một trong các điều kiện:
   - `Safety Risk Level = high`
   - hoặc `Action Urgency = immediate`
   - hoặc `Equipment Status = stopped`
2. Vào menu `0502 Critical Queue`
3. Kỳ vọng request xuất hiện trong queue

### Case 3 - Lead assigned

1. Thực hiện `Notify CMT Lead` trên request
2. Kiểm tra `Lead Notified User` đã có giá trị
3. Vào menu `0502 Lead Assigned Queue`
4. Kỳ vọng request xuất hiện trong queue

## 11. File đã thay đổi

- `views/maintenance_request_views.xml`
