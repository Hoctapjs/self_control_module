# Phase 3 - Bước 11 đã triển khai

## 1. Mục tiêu của bước này

`Bước 11` trong `Phase 3` tập trung vào việc nâng phần `Treatment Proposal` từ mức:

- có proposal summary dạng structured

lên mức:

- có proposal artifact rõ hơn để đọc và đối chiếu
- có revision log cho các lần sửa proposal
- có template proposal theo `Request Type`

Mục tiêu là làm proposal dễ truy vết hơn nhưng vẫn giữ scope gọn, chưa tách object proposal trục chính riêng.

## 2. Tài liệu đã dùng để triển khai

### Convention

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md)

### Structure map

- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0502/structure/module_map.json)

Lưu ý:

- `module_map.json` hiện cũ hơn source code.
- Source code hiện tại là chuẩn xác nhận cuối cùng.

### Source xác nhận chính

- [phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md](/d:/odoo-19.0+e.20250918/addons/M02_P0502/notes/phase_3_ke_hoach_chi_tiet_theo_tung_buoc.md)
- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [request_proposal_history.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_proposal_history.py)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 3. Hướng triển khai đã chọn

Sau khi rà lại plan `Phase 3`, hướng triển khai được chọn là:

- chưa tạo object proposal trục chính riêng
- tiếp tục giữ `maintenance.request` là nơi lưu proposal chính
- thêm lớp audit trail và artifact proposal rõ hơn ngay trên request
- dùng `Request Type` để cấp template proposal

Lý do chọn hướng này:

- bám đúng scope tối thiểu của plan
- tận dụng dữ liệu proposal structured đã có từ `Phase 2`
- tránh mở rộng sang quotation engine riêng khi chưa có yêu cầu thực tế đủ mạnh

## 4. Model mới đã thêm

Đã thêm model mới:

- `x_psm_request_proposal_history`

File:

- [request_proposal_history.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_proposal_history.py)

Model này dùng để lưu:

- revision proposal
- loại revision
- snapshot các field proposal tại thời điểm thay đổi
- lý do thay đổi
- ai thay đổi
- thay đổi lúc nào

## 5. Những gì đã thêm trên `Request Type`

Trong [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py), đã thêm:

- `0502 Proposal Template`

Ý nghĩa:

- mỗi `Request Type` có thể có mẫu proposal hoặc khung hướng dẫn proposal riêng
- khi user vào tab `Treatment Proposal`, hệ thống hiển thị template này để hướng dẫn cách ghi proposal nhất quán hơn

Nếu master chưa cấu hình template riêng, hệ thống sẽ fallback theo `code` của `Request Type`.

## 6. Những gì đã thêm trên `maintenance.request`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `Proposal Template Guide`
- `Proposal Document`
- `Proposal Change Reason`
- `Proposal History`
- `Proposal Revision Count`
- `Last Proposal Changed By`
- `Last Proposal Changed At`
- `Proposal Revision Compare`

Ý nghĩa từng field:

### 6.1. `Proposal Template Guide`

- hiển thị hướng dẫn proposal đang áp dụng theo `Request Type`

### 6.2. `Proposal Document`

- artifact proposal rõ hơn summary cũ
- được build từ:
  - request info
  - proposal template
  - root cause
  - technical solution
  - cost
  - timeline
  - proposal summary

### 6.3. `Proposal Change Reason`

- lý do sửa proposal sau khi request đã được đánh dấu `Proposed`

### 6.4. `Proposal History`

- lịch sử các revision proposal

### 6.5. `Proposal Revision Count`

- số revision proposal đã ghi nhận

### 6.6. `Last Proposal Changed By / At`

- ai là người sửa proposal gần nhất
- sửa lúc nào

### 6.7. `Proposal Revision Compare`

- tóm tắt nhanh khác biệt giữa revision mới nhất và revision trước đó

## 7. Logic proposal template

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), đã thêm:

- `_psm_get_request_type_proposal_template_text()`
- `_compute_x_psm_0502_proposal_template_fields()`

Rule hiện tại:

- ưu tiên template proposal được cấu hình trực tiếp trên `Request Type`
- nếu chưa có thì fallback theo `code`:
  - `maintenance`
  - `repair`
  - `inspection`

Mục tiêu:

- không cần dựng wizard proposal riêng
- nhưng user vẫn có khung hướng dẫn để ghi proposal tốt hơn

## 8. Logic build proposal document

Đã thêm helper:

- `_psm_build_proposal_document()`

Helper này build `Proposal Document` từ các phần:

- `Request`
- `Store Department`
- `Request Type`
- `Proposal Template Guide`
- `Root Cause Analysis`
- `Technical Solution`
- `Cost`
- `Timeline`
- `Proposal Summary`

Mục tiêu:

- tạo ra một artifact proposal dễ đọc hơn summary ngắn
- đủ để đối chiếu, duyệt và theo dõi revision

## 9. Logic revision proposal

Đã thêm:

- `_psm_create_proposal_history_line()`
- `_psm_build_proposal_revision_compare()`
- `_compute_x_psm_0502_proposal_revision_compare()`

### 9.1. Initial proposal

Khi bấm `Mark Proposed`:

- hệ thống vẫn build `Treatment Proposal` summary như `Phase 2`
- đồng thời build thêm `Proposal Document`
- nếu request chưa có `Proposal History`:
  - tạo revision `1`
  - `Change Type = Initial Proposal`

### 9.2. Reproposal

Trong `write()`, nếu request đã `proposed` và user đổi một trong các field:

- `Root Cause Analysis`
- `Technical Solution`
- `Estimated Cost`
- `Estimated Timeline`
- `Cost Note`
- `Timeline Note`

thì hệ thống sẽ:

- yêu cầu có `Proposal Change Reason`
- rebuild lại `Treatment Proposal`
- rebuild lại `Proposal Document`
- tạo thêm `Proposal History` với:
  - `Change Type = Reproposal`

### 9.3. Compare revisions

Nếu đã có từ 2 revision trở lên:

- `Proposal Revision Compare` sẽ hiển thị tóm tắt phần nào đã thay đổi

## 10. Điều chỉnh trong `Mark Proposed`

Trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py), `action_psm_mark_proposed()` đã được mở rộng:

- ngoài việc build `Treatment Proposal`
- còn build `Proposal Document`
- và tạo `Proposal History` revision đầu tiên nếu chưa có

Điều này giúp `Bước 11` không chỉ dừng ở mức “đã proposed”, mà có thêm lớp proposal artifact và audit trail.

## 11. Thay đổi ở giao diện

Trong [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml), tab `Treatment Proposal` đã được mở rộng.

### Form view

Đã thêm hiển thị:

- `Proposal Template Guide`
- `Proposal Document`
- `Proposal Change Reason`
- `Proposal Revision Count`
- `Last Proposal Changed By`
- `Last Proposal Changed At`
- `Proposal Revision Compare`
- bảng `Proposal History`

### List view

Đã thêm optional fields:

- `Proposal Revision Count`
- `Last Proposal Changed By`
- `Last Proposal Changed At`

### Search view

Đã thêm filter:

- `Has Proposal History`
- `Reproposed`

Đã thêm group by:

- `Proposal Revision Count`
- `Last Proposal Changed By`

## 12. Những gì bước này cố ý chưa làm

Để tránh over-scope so với plan `Phase 3`, bước này chưa làm:

- object proposal trục chính riêng
- quotation / estimate engine riêng
- compare UI phức tạp dạng diff viewer
- email / portal / printable quote template riêng
- approval matrix mới cho proposal revision

Những phần này chỉ nên làm nếu user xác nhận thực sự cần ở các phase sau hoặc backlog tiếp theo.

## 13. Ý nghĩa nghiệp vụ của bước này

Sau thay đổi này, `Bước 11` được nâng từ:

- “có summary proposal”

lên:

- “có proposal artifact rõ hơn”
- “có lịch sử revision proposal”
- “có lý do sửa proposal”
- “có hướng dẫn proposal theo loại request”

Điều này giúp:

- proposal dễ đối chiếu hơn
- user biết proposal đã đổi mấy lần
- quản lý biết ai sửa proposal và sửa lúc nào

## 14. Kiểm tra tĩnh

Đã kiểm tra:

- Python compile: `OK`
- XML parse: `OK`

## 15. Cách test

1. Upgrade `M02_P0502`.
2. Mở một request đã qua `Planning`.
3. Điền proposal structured rồi bấm `Mark Proposed`.
4. Kiểm tra:
- `Proposal Document` đã được build
- `Proposal History` có revision `1`
- `Proposal Revision Count = 1`
5. Sửa lại một trong các field:
- `Estimated Cost`
- `Technical Solution`
- `Timeline Note`
6. Nếu không điền `Proposal Change Reason`:
- kỳ vọng bị chặn
7. Điền `Proposal Change Reason` rồi lưu:
- kỳ vọng tạo thêm revision `Reproposal`
- `Proposal Revision Count` tăng
- `Proposal Revision Compare` có dữ liệu

## 16. File đã thay đổi

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [request_proposal_history.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_proposal_history.py)
- [__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)
- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)
