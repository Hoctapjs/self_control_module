# Phase 3 - Bước 10 đã triển khai

## 1. Mục tiêu của bước này

`Bước 10` trong `Phase 3` tập trung vào việc nâng phần monitoring từ mức:

- có các màn hình theo dõi rời theo từng nhánh

lên mức:

- nhìn được tiến độ vận hành tổng quát của request
- nhìn được request đang nghẽn ở checkpoint nào
- nhìn được nhánh vật tư / kho / mua ngoài đang ở trạng thái nào
- theo dõi intake SLA rõ hơn ở góc nhìn reporting

Mục tiêu là bám đúng lưu đồ nghiệp vụ:

- `Bước 10` là theo dõi tình trạng / báo cáo tiến độ

chứ không mở rộng quá tay sang dashboard riêng hay KPI engine nặng.

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
- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`
- tham chiếu thêm:
  - `views/project_task_views.xml`

## 3. Hướng triển khai đã chọn

Thay vì:

- dựng dashboard tổng hợp riêng
- thêm object monitoring riêng
- hoặc kéo thêm KPI engine / SLA engine mới

hướng triển khai được chọn là:

- thêm 2 field monitoring tổng hợp trên `maintenance.request`
- dùng chính các field đã có từ `Phase 1`, `Phase 2`, `Phase 3` để suy ra trạng thái tiến độ
- mở thêm các action reporting và filter/group by đúng với các điểm nghẽn vận hành

Đây là hướng:

- bám lưu đồ
- ít over-scope
- có giá trị vận hành ngay

## 4. Các field mới trên `maintenance.request`

Đã thêm:

- `Progress Checkpoint`
- `Supply Branch Status`

## 5. Ý nghĩa của `Progress Checkpoint`

`Progress Checkpoint` dùng để trả lời câu hỏi:

- request hiện đang đứng ở mốc nào của quy trình 0502?

Các giá trị hiện có:

- `Intake`
- `Inspection`
- `Planning`
- `Proposal`
- `Approval`
- `Service Assessment`
- `Material Assessment`
- `Material Approval`
- `Stock Issue`
- `Purchase`
- `Execution`
- `Acceptance`
- `Closed`

Ý nghĩa:

- không cần đọc nhiều field rời
- chỉ nhìn một field là biết request đang nghẽn ở bước nào của flow

## 6. Ý nghĩa của `Supply Branch Status`

`Supply Branch Status` dùng để trả lời câu hỏi:

- request này trong nhánh vật tư / kho / mua ngoài đang ở trạng thái nào?

Các giá trị hiện có:

- `No Material Flow`
- `Material Assessment`
- `No Material Needed`
- `Waiting Stock Check`
- `Awaiting Material Approval`
- `Pending Stock Issue`
- `Stock Issued`
- `Purchase Required`
- `Purchase In Progress`
- `Purchase Confirmed`
- `Outside Service`

Ý nghĩa:

- phân biệt rõ:
  - đang đi nhánh kho nội bộ
  - đang chờ duyệt vật tư
  - đang chờ xuất kho
  - hay đang phải đi mua ngoài

## 7. Logic `Progress Checkpoint`

Hệ thống suy ra checkpoint dựa trên các mốc đã có sẵn trong request.

Thứ tự ưu tiên hiện tại:

1. nếu request đã `done`:
   - `Closed`
2. nếu đã nghiệm thu:
   - `Acceptance`
3. nếu đã có execution / FSM task:
   - `Execution`
4. nếu đã đi nhánh mua ngoài hoặc `Stock Check Result = not_available`:
   - `Purchase`
5. nếu đã có stock picking / stock issue:
   - `Stock Issue`
6. nếu đã có material approval hoặc `Stock Check Result = available`:
   - `Material Approval`
7. nếu đã material checked:
   - `Material Assessment`
8. nếu đã service assessed:
   - `Service Assessment`
9. nếu đã proposed hoặc đang approval:
   - `Approval` / `Proposal`
10. nếu đã plan:
   - `Proposal`
11. nếu đã inspected:
   - `Planning`
12. nếu đã received:
   - `Inspection`
13. còn lại:
   - `Intake`

Mục tiêu là tạo một checkpoint vận hành dễ đọc, không thay workflow gốc.

## 8. Logic `Supply Branch Status`

Hệ thống suy ra trạng thái nhánh cung ứng như sau:

1. nếu request đi `Outside Service`:
   - `Outside Service`
2. nếu đã material checked nhưng không có vật tư:
   - `No Material Needed`
3. nếu chưa có nhánh vật tư:
   - `No Material Flow`
4. nếu đã có PO:
   - `Purchase In Progress` hoặc `Purchase Confirmed`
5. nếu `Stock Check Result = not_available`:
   - `Purchase Required`
6. nếu `Stock Issue Status = issued`:
   - `Stock Issued`
7. nếu material approval đã approved:
   - `Pending Stock Issue`
8. nếu material approval đang pending:
   - `Awaiting Material Approval`
9. nếu đã có stock picking:
   - `Waiting Stock Check`
10. còn lại:
   - `Material Assessment`

## 9. Thay đổi ở giao diện

### 9.1. Form và list của `maintenance.request`

Đã hiển thị thêm:

- `Progress Checkpoint`
- `Supply Branch Status`

### 9.2. Search view

Đã thêm filter:

- `Progress Proposal`
- `Progress Execution`
- `Progress Acceptance`
- `Purchase Required`
- `Purchase In Progress`
- `Pending Stock Issue`
- `Intake SLA Pending`

Đã thêm group by:

- `Progress Checkpoint`
- `Supply Branch Status`

## 10. Các action reporting mới

Đã thêm 3 action reporting mới dưới `Maintenance > Reporting`:

- `0502 Progress Monitoring`
- `0502 Supply Monitoring`
- `0502 Intake SLA Monitoring`

### 10.1. `0502 Progress Monitoring`

Mục tiêu:

- theo dõi request đang dừng ở checkpoint nào

Mặc định:

- chỉ nhìn request 0502 đang mở
- group theo `Progress Checkpoint`

### 10.2. `0502 Supply Monitoring`

Mục tiêu:

- theo dõi nhánh vật tư / kho / mua ngoài

Mặc định:

- chỉ nhìn request 0502 đang mở
- group theo `Supply Branch Status`

### 10.3. `0502 Intake SLA Monitoring`

Mục tiêu:

- nhìn nhanh request đang pending ở checkpoint receive
- phân biệt request `Pending`, `On Time`, `Late`

Mặc định:

- group theo `Intake SLA Result`
- bật filter `Intake SLA Pending`

## 11. Vì sao triển khai theo cách này

Lý do chọn hướng này:

- đúng với phần “Monitoring” được mô tả trong plan `Phase 3`
- tận dụng dữ liệu đã có từ các bước trước
- không tạo thêm object mới chỉ để báo cáo
- không dựng dashboard riêng khi chưa có yêu cầu thật
- giúp user vận hành nhìn request theo góc “đang nghẽn ở đâu” thay vì chỉ nhìn state rời

## 12. Các phần cố ý chưa làm

Ở bước này chưa làm:

- dashboard tổng hợp riêng
- KPI engine sâu
- SLA escalation tự động
- cross-model monitoring object riêng
- KPI tài chính / hiệu suất chuyên sâu

Các phần đó chỉ nên làm nếu người dùng xác nhận cần sau khi đã dùng đủ các màn hình monitoring hiện tại.

## 13. Case test đề xuất

### Case 1 - Progress checkpoint

1. tạo request mới chưa receive
2. kiểm tra:
   - `Progress Checkpoint = Intake`
3. receive request
4. kiểm tra:
   - `Progress Checkpoint = Inspection`
5. inspected và planned
6. kiểm tra:
   - request chuyển checkpoint đúng theo flow

### Case 2 - Supply branch

1. mở request có vật tư nội bộ
2. tạo stock picking
3. kiểm tra:
   - `Supply Branch Status = Waiting Stock Check`
4. approve vật tư
5. kiểm tra:
   - `Supply Branch Status = Pending Stock Issue`
6. validate picking done
7. kiểm tra:
   - `Supply Branch Status = Stock Issued`

### Case 3 - Purchase branch

1. mở request có `Stock Check Result = not_available`
2. kiểm tra:
   - `Supply Branch Status = Purchase Required`
3. tạo PO
4. kiểm tra:
   - `Supply Branch Status = Purchase In Progress`
5. confirm PO
6. kiểm tra:
   - `Supply Branch Status = Purchase Confirmed`

### Case 4 - Reporting menu

1. vào `Maintenance > Reporting`
2. kiểm tra có các menu:
   - `0502 Progress Monitoring`
   - `0502 Supply Monitoring`
   - `0502 Intake SLA Monitoring`
3. kiểm tra các màn hình mở đúng filter/group mặc định

## 14. File đã thay đổi

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

## 15. Kết luận

`Phase 3 - Bước 10` đã được triển khai theo hướng tối thiểu nhưng đúng trọng tâm:

- làm rõ tiến độ vận hành
- làm rõ nhánh cung ứng
- làm giàu reporting

trong khi vẫn:

- bám request làm trục chính
- không mở rộng sang dashboard nặng
- không làm dư so với lưu đồ nghiệp vụ hiện tại
