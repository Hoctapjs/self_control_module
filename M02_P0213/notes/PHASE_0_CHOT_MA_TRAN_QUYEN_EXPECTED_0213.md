# Phase 0 - Chốt Ma Trận Quyền Expected 0213

Tài liệu này là đầu ra của Phase 0 cho module `M02_P0213_00`.

Mục tiêu của tài liệu:
- Chốt quyền mong muốn theo từng nhóm 0200 trước khi sửa code.
- Tách rõ quyền expected khỏi quyền actual hiện tại.
- Làm chuẩn để bám vào các phase tiếp theo, đặc biệt là Phase 1, 2, 3 và 4.

Tài liệu đã dùng:
- Convention: `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213_00/structure/module_map.json`

Source chính dùng để xác nhận:
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0200/security/security.xml`
- `odoo/addons/approvals/security/approval_security.xml`
- `odoo/addons/survey/security/survey_security.xml`

Lưu ý:
- Nếu source và JSON map khác nhau, ưu tiên source.
- Tài liệu này chốt `expected rights`, không khẳng định `actual rights` hiện tại đã khớp.

## 1. Phạm vi dữ liệu cần khóa

Phase 0 chốt scope cho 4 nhóm dữ liệu chính trong flow `0213`:
- `approval.request`
- `approval.approver`
- `survey.user_input`
- `mail.activity`

Định nghĩa dữ liệu thuộc `0213`:
- request thuộc category offboarding OPS của module `0213`
- approver line gắn với request offboarding OPS của module `0213`
- survey response gắn với survey exit interview của `0213`
- activity gắn với `approval.request` hoặc `hr.employee` liên kết tới request offboarding `0213`

## 2. Các nhóm 0200 nằm trong phạm vi chốt quyền

Nhóm cần chốt:
- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`

## 3. Nguyên tắc chốt quyền expected

Nguyên tắc sử dụng:
- OPS staff chủ yếu xem tiến độ và danh sách activity, không xử lý quyết định HR.
- OPS manager được xem rộng hơn OPS staff và được xem kết quả survey nếu business cần phối hợp.
- HR Admin staff được xử lý các bước vận hành HR cơ bản.
- HR Admin manager được hoàn thành quy trình và đánh dấu trạng thái sau xử lý.
- HRBP staff được xem và phối hợp kiểm soát.
- HRBP manager được quyết định các bước cuối như hoàn tất, tái tuyển, blacklist nếu business xác nhận.
- HR Head và System là nhóm có quyền rộng nhất trong `0213`.
- Portal employee chỉ nhìn và thao tác trên dữ liệu của chính mình.

## 4. Ma trận quyền expected theo từng model

### 4.1. `approval.request`

| Nhóm | Quyền expected |
|---|---|
| `GDH_RST_OPS_OC_S` | Đọc các request offboarding `0213` trong scope được giao |
| `GDH_RST_OPS_OM_M` | Đọc toàn bộ request offboarding `0213` thuộc phạm vi OPS phụ trách |
| `GDH_RST_HR_ADMIN_S` | Đọc và cập nhật các request offboarding `0213` phục vụ xử lý nghiệp vụ HR |
| `GDH_RST_HR_ADMIN_M` | Đọc, cập nhật và hoàn tất các request offboarding `0213` |
| `GDH_RST_HR_HRBP_S` | Đọc các request offboarding `0213` để theo dõi và phối hợp |
| `GDH_RST_HR_HRBP_M` | Đọc và cập nhật các request offboarding `0213` ở mức quản lý |
| `GDH_RST_HR_HEAD_M` | Đọc và cập nhật toàn bộ request offboarding `0213` |
| `GDH_RST_SYSTEM_ST_M` | Đọc và cập nhật toàn bộ request offboarding `0213` |

Quyết định expected:
- Không nhóm nào được thấy request ngoài `0213` chỉ vì có cùng model `approval.request`.
- `unlink` không phải quyền mặc định cho bất kỳ nhóm nào trong `0213`.
- `create` không mở rộng tràn lan; nếu cần tạo từ backend thì chỉ cấp cho nhóm thật sự có nghiệp vụ tạo request.

### 4.2. `approval.approver`

| Nhóm | Quyền expected |
|---|---|
| `GDH_RST_OPS_OC_S` | Đọc approver lines của request offboarding `0213` trong scope xem |
| `GDH_RST_OPS_OM_M` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_HR_ADMIN_S` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_HR_ADMIN_M` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_HR_HRBP_S` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_HR_HRBP_M` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_HR_HEAD_M` | Đọc approver lines của request offboarding `0213` |
| `GDH_RST_SYSTEM_ST_M` | Đọc approver lines của request offboarding `0213` |

Quyết định expected:
- Mặc định chỉ cần `read`.
- Không nhóm nào được `create`, `unlink`, hoặc `write` trên `approval.approver` nếu business chưa xác nhận nhu cầu chỉnh approver line thủ công.

### 4.3. `survey.user_input`

| Nhóm | Quyền expected |
|---|---|
| `GDH_RST_OPS_OC_S` | Không xem trực tiếp survey result |
| `GDH_RST_OPS_OM_M` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_HR_ADMIN_S` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_HR_ADMIN_M` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_HR_HRBP_S` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_HR_HRBP_M` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_HR_HEAD_M` | Đọc survey result của request offboarding `0213` |
| `GDH_RST_SYSTEM_ST_M` | Đọc survey result của request offboarding `0213` |
| Portal employee | Chỉ đọc và thao tác trên survey response của chính mình |

Quyết định expected:
- Không nhóm internal nào được nhìn mọi `survey.user_input` chỉ vì có `base.group_user`.
- `survey.user_input` của `0213` phải bị khóa theo đúng survey exit interview của `0213`.
- Internal gần như không cần `write`, `create`, `unlink` trên survey response; nếu có thì phải chỉ định riêng và rất hẹp.

### 4.4. `mail.activity`

| Nhóm | Quyền expected |
|---|---|
| `GDH_RST_OPS_OC_S` | Đọc activity của offboarding `0213` trong phạm vi được giao |
| `GDH_RST_OPS_OM_M` | Đọc activity của offboarding `0213` |
| `GDH_RST_HR_ADMIN_S` | Đọc activity của offboarding `0213` và xử lý activity thuộc vai trò HR |
| `GDH_RST_HR_ADMIN_M` | Đọc và xử lý activity của offboarding `0213` |
| `GDH_RST_HR_HRBP_S` | Đọc activity của offboarding `0213` |
| `GDH_RST_HR_HRBP_M` | Đọc activity của offboarding `0213` |
| `GDH_RST_HR_HEAD_M` | Đọc và xử lý activity của offboarding `0213` |
| `GDH_RST_SYSTEM_ST_M` | Đọc và xử lý activity của offboarding `0213` |
| Portal employee | Chỉ hoàn thành activity được giao cho chính mình trong flow portal `0213` |

Quyết định expected:
- Activity ngoài `0213` không được lộ chỉ vì cùng dùng model `mail.activity`.
- Portal chỉ được đụng đúng activity của mình và đúng request của mình.

## 5. Ma trận action nghiệp vụ expected

### 5.1. Action cấp xử lý nghiệp vụ

| Action | Nhóm expected |
|---|---|
| `action_view_survey_results` | `OPS_OM_M`, `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HRBP_S`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `action_send_social_insurance` | `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `action_send_adecco_notification` | `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `action_done` | `HR_ADMIN_M`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `action_rehire` | `HR_ADMIN_M`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `action_blacklist` | `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |
| `manual reminder / extension` | `OPS_OC_S`, `OPS_OM_M`, `HR_ADMIN_S`, `HR_ADMIN_M`, `HR_HRBP_S`, `HR_HRBP_M`, `HR_HEAD_M`, `SYSTEM_ST_M` |

### 5.2. Action portal expected

| Action portal | Quyền expected |
|---|---|
| Submit đơn nghỉ việc | Chỉ user portal của chính nhân viên đó |
| Xem request hiện tại | Chỉ owner của request |
| Xem activity portal | Chỉ activity của request thuộc owner đó |
| Done activity portal | Chỉ activity được giao đúng cho user hiện tại |
| Mở survey exit interview | Chỉ survey response của chính user đó |

## 6. Quyết định expected về nền quyền group

Phase 0 chưa sửa code, nhưng chốt kỳ vọng sau để đưa sang Phase 1:

- Nhóm nào cần thao tác backend Odoo thật thì phải có nền quyền internal rõ ràng.
- Nhóm nào chỉ cần xem hoặc thao tác qua UI portal thì không nên được mở backend thừa.
- Không dùng việc “user có thêm group core” như một phần chính thức của thiết kế quyền `0213`.
- Nếu đang có user mang thêm `approvals.group_approval_user`, `approvals.group_approval_manager`, `survey.group_survey_user`, `survey.group_survey_manager`, phải coi đó là ngoại lệ cần rà soát chứ không phải expected design.

## 7. Danh sách điểm chưa chốt ở source hiện tại nhưng đã chốt ở expected

Các điểm cần coi là quyết định đầu vào cho phase sau:

1. `approval.request`
- expected là chỉ thấy request offboarding `0213`
- không chấp nhận quyền nhìn rộng toàn bộ request chỉ vì group core của `approvals`

2. `approval.approver`
- expected là chỉ `read`
- chưa coi chỉnh approver line là nhu cầu mặc định

3. `survey.user_input`
- expected là internal chỉ đọc survey result thuộc `0213`
- không mở rộng read/write trên toàn bộ survey response

4. `mail.activity`
- expected là phải có scope riêng cho activity của `0213`
- không để lộ activity ngoài flow offboarding

5. `sudo()`
- expected là chỉ dùng sau khi đã check đúng group và đúng scope bản ghi

## 8. Điều kiện hoàn tất Phase 0

Phase 0 được coi là hoàn tất khi:
- ma trận expected cho từng nhóm 0200 đã được ghi rõ
- action nào thuộc nhóm nào đã được chốt
- portal scope đã được chốt
- phạm vi dữ liệu cần khóa đã được chốt
- các phase sau có thể bám vào tài liệu này mà không phải đoán lại ý đồ quyền

## 9. Đầu ra để chuyển sang Phase 1

Sau tài liệu này, Phase 1 cần thực hiện:
- đối chiếu expected matrix với chain group thực tế trong `M02_P0200/security/security.xml`
- xác định nhóm nào đang thiếu `base.group_user`
- xác định những chỗ actual rights đang lệch khỏi expected rights

Tài liệu này là baseline chính thức để làm bước đối chiếu đó.
