# Phase 1 - Đối Chiếu Expected Vs Actual Group Chain 0213

Tài liệu này là đầu ra của Phase 1 cho module `M02_P0213_00`.

Mục tiêu:
- Đối chiếu ma trận quyền expected của Phase 0 với chain group thực tế đang có trong `M02_P0200`.
- Xác định nhóm nào đang có nền quyền internal thật sự.
- Xác định các điểm lệch lớn giữa expected rights và actual nền quyền hiện tại.
- Làm đầu vào trực tiếp cho Phase 2 và Phase 3.

Tài liệu tham chiếu:
- `addons/M02_P0213_00/notes/PHASE_0_CHOT_MA_TRAN_QUYEN_EXPECTED_0213.md`
- `addons/M02_P0213_00/notes/PHASE_PLAN_TRIEN_KHAI_KHOA_CHAT_DU_LIEU_0213.md`

Tài liệu định hướng đã dùng:
- Convention: `addons/M02_P0213_00/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0213_00/structure/module_map.json`

Source chính dùng để xác nhận:
- `addons/M02_P0200/security/security.xml`
- `addons/M02_P0213_00/security/ir.model.access.csv`
- `addons/M02_P0213_00/security/offboarding_request_rules.xml`
- `addons/M02_P0213_00/security/security.xml`
- `addons/M02_P0213_00/models/resignation_request.py`
- `addons/M02_P0213_00/views/resignation_request_views.xml`
- `odoo/addons/approvals/security/approval_security.xml`

Lưu ý quan trọng:
- Source thật của group chain hiện nằm ở `addons/M02_P0200/security/security.xml`.
- Trong code `0213`, XMLID đang tham chiếu dạng `M02_P0200_00.*`.
- Đây là dấu hiệu cần rà thêm sau ở phase sau để đảm bảo tên module và XMLID không bị lệch logic triển khai.
- Ở tài liệu này, phần kết luận ưu tiên theo source group chain đang có.

## 1. Tóm tắt nhanh kết luận Phase 1

Kết luận chính:
- Không phải tất cả nhóm 0200 của `0213` đều đang kéo theo `base.group_user`.
- Vì ACL nền trong `0213` chủ yếu đang bám `base.group_user`, nên nhiều nhóm được đưa vào `groups=` hoặc `record rule` nhưng chưa chắc đã có nền quyền backend thật như expected.
- Nhóm đang có nền internal rõ nhất theo chain hiện tại là:
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- Các nhóm còn lại trong phạm vi `0213` đang có nguy cơ lệch expected nếu chỉ xét theo chain group hiện tại.

## 2. Chuỗi implied group thực tế trong `M02_P0200`

### 2.1. Nền internal user

Group nền internal:
- `GDH_RST_ALL_BASE_S`
  - imply `base.group_user`

Ý nghĩa:
- Chỉ nhóm nào kéo theo `GDH_RST_ALL_BASE_S` mới chắc chắn có nền internal user của Odoo từ chain group này.

### 2.2. Chuỗi implied của các nhóm liên quan `0213`

| Group | Implied trực tiếp | Có kéo tới `base.group_user` không |
|---|---|---|
| `GDH_RST_OPS_OC_S` | Không | Không |
| `GDH_RST_OPS_OM_M` | `GDH_RST_OPS_OC_S` | Không |
| `GDH_RST_HR_ADMIN_S` | Không | Không |
| `GDH_RST_HR_ADMIN_M` | `GDH_RST_HR_ADMIN_S`, `GDH_RST_ALL_BASE_S` | Có |
| `GDH_RST_HR_HRBP_S` | Không | Không |
| `GDH_RST_HR_HRBP_M` | `GDH_RST_HR_HRBP_S`, `GDH_RST_HR_ADMIN_S` | Không |
| `GDH_RST_HR_HEAD_M` | `GDH_RST_HR_ADMIN_M`, `GDH_RST_HR_HRBP_M`, `GDH_RST_OPS_OM_M`, ... | Có |
| `GDH_RST_SYSTEM_ST_M` | `GDH_RST_ALL_BASE_S`, `GDH_RST_HR_HEAD_M` | Có |

Kết luận từ chain:
- Có internal nền chắc chắn:
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- Chưa có internal nền chắc chắn chỉ từ chain hiện tại:
  - `GDH_RST_OPS_OC_S`
  - `GDH_RST_OPS_OM_M`
  - `GDH_RST_HR_ADMIN_S`
  - `GDH_RST_HR_HRBP_S`
  - `GDH_RST_HR_HRBP_M`

## 3. Đối chiếu expected của Phase 0 với actual nền quyền hiện tại

### 3.1. `GDH_RST_OPS_OC_S`

Expected:
- được đọc request offboarding trong scope được giao
- được xem activity trong scope được giao

Actual nền quyền hiện tại:
- không kéo `base.group_user`
- không có nền internal chắc chắn từ chain group

Đánh giá:
- Lệch expected.
- Nếu không có grant quyền khác ngoài chain hiện tại, group này không đủ nền để dùng ACL bám `base.group_user`.

Kết luận:
- Phase 2 hoặc Phase 1.5 cần quyết định rõ:
  - hoặc cho nhóm này có nền internal
  - hoặc không dùng group này để thao tác backend model trực tiếp

### 3.2. `GDH_RST_OPS_OM_M`

Expected:
- được xem request offboarding rộng hơn OPS staff
- được xem survey result
- được xem activity và hỗ trợ theo dõi

Actual nền quyền hiện tại:
- chỉ imply `GDH_RST_OPS_OC_S`
- không kéo `base.group_user`

Đánh giá:
- Lệch expected.
- UI và group check trong `0213` đang dùng group này khá nhiều, nhưng chain hiện tại chưa chứng minh có backend access nền tương ứng.

Kết luận:
- Đây là một trong các điểm lệch lớn cần xử lý sớm.

### 3.3. `GDH_RST_HR_ADMIN_S`

Expected:
- đọc request offboarding
- xử lý các bước HR cơ bản
- xem survey result

Actual nền quyền hiện tại:
- không imply `GDH_RST_ALL_BASE_S`
- không kéo `base.group_user`

Đánh giá:
- Lệch expected.
- Đây là nhóm đang được gắn mạnh vào nút nghiệp vụ trong view và tuple Python của `0213`, nhưng chain nền hiện tại chưa khớp.

Kết luận:
- Cần quyết định rõ ở Phase 2:
  - hoặc bổ sung internal nền cho nhóm này
  - hoặc hạ lại kỳ vọng action/backend access của nhóm này

### 3.4. `GDH_RST_HR_ADMIN_M`

Expected:
- đọc, cập nhật và hoàn tất request offboarding

Actual nền quyền hiện tại:
- imply `GDH_RST_ALL_BASE_S`
- có `base.group_user`

Đánh giá:
- Khớp expected ở mức nền internal.
- Đây là nhóm hiện có khả năng cao nhất để các ACL/rule bám `base.group_user` phát huy tác dụng như mong muốn.

Kết luận:
- Có thể dùng làm nhóm chuẩn để test flow backend trong phase sau.

### 3.5. `GDH_RST_HR_HRBP_S`

Expected:
- xem request offboarding
- xem survey result
- phối hợp kiểm soát

Actual nền quyền hiện tại:
- không imply `GDH_RST_ALL_BASE_S`
- không kéo `base.group_user`

Đánh giá:
- Lệch expected.

Kết luận:
- Nếu business muốn nhóm này vào backend xem dữ liệu thật, chain group hiện tại chưa hỗ trợ rõ.

### 3.6. `GDH_RST_HR_HRBP_M`

Expected:
- xem và cập nhật request offboarding ở mức quản lý
- thực hiện các action như `done`, `rehire`, `blacklist` theo expected matrix

Actual nền quyền hiện tại:
- imply `GDH_RST_HR_HRBP_S` và `GDH_RST_HR_ADMIN_S`
- không imply `GDH_RST_ALL_BASE_S`
- không kéo `base.group_user`

Đánh giá:
- Lệch expected rất rõ.
- Đây là nhóm manager trong expected matrix, nhưng chain nền hiện tại chưa kéo internal user.

Kết luận:
- Đây là điểm lệch quan trọng nhất cần xử lý trước khi sửa sâu ACL/rule.

### 3.7. `GDH_RST_HR_HEAD_M`

Expected:
- quyền rộng trên toàn bộ offboarding `0213`

Actual nền quyền hiện tại:
- imply `GDH_RST_HR_ADMIN_M`
- từ đó kéo `GDH_RST_ALL_BASE_S`
- có `base.group_user`

Đánh giá:
- Khớp expected ở mức nền internal.

Kết luận:
- Có thể dùng làm nhóm test full-access nghiệp vụ trong phase sau.

### 3.8. `GDH_RST_SYSTEM_ST_M`

Expected:
- quyền rộng nhất trong `0213`

Actual nền quyền hiện tại:
- imply `GDH_RST_ALL_BASE_S`
- imply `GDH_RST_HR_HEAD_M`
- có `base.group_user`

Đánh giá:
- Khớp expected ở mức nền internal.

Kết luận:
- Có thể dùng làm nhóm kiểm tra access cao nhất trong phase sau.

## 4. Ảnh hưởng của actual chain lên ACL hiện tại của `0213`

### 4.1. ACL hiện tại đang bám `base.group_user`

Trong `addons/M02_P0213_00/security/ir.model.access.csv`, các model chính đang mở cho `base.group_user`:
- `mail.activity`
- `approval.request`
- `hr.employee`
- `survey.survey`
- `survey.user_input`
- `survey.question`
- `survey.question.answer`
- `hr.contract.type`
- `hr.departure.reason`

Hệ quả:
- Chỉ nhóm nào thực sự kéo được `base.group_user` mới tận dụng được nền ACL này từ chain group 0200.
- Những nhóm không kéo `base.group_user` thì dù có xuất hiện trong `record rule` hoặc `groups=` ở view, vẫn có thể không có backend access nền như kỳ vọng.

### 4.2. Record rule hiện tại của `0213` chưa tự giải quyết được vấn đề chain

`record rule` hiện tại của `0213` có gắn các group:
- OPS
- HR Admin
- HRBP
- HR Head
- System

Nhưng:
- `record rule` không thay thế được ACL nền
- nếu group không có nền quyền nội bộ đủ, rule vẫn không biến thành backend access hoàn chỉnh

Kết luận:
- Phase 2 không thể chỉ “sửa ACL và record rule” một cách mù; phải bám kết luận chain group của Phase 1.

## 5. Ảnh hưởng của core `approvals` lên actual rights

Trong `odoo/addons/approvals/security/approval_security.xml`:
- `base.group_user` có rule đọc/sửa/tạo request theo owner/approver/line manager
- `group_approval_user` có rule thấy toàn bộ `approval.request`
- `group_approval_manager` có rule thấy toàn bộ `approval.request`
- `group_approval_user` và `group_approval_manager` cũng mở rộng mạnh cho `approval.approver`

Kết luận:
- Nếu user của `0213` đang mang thêm group core của `approvals`, quyền actual sẽ rộng hơn rất nhiều so với expected matrix.
- Phase 1 chưa có dữ liệu user thực tế đang được gán group gì, nên đây được ghi nhận là rủi ro mở.

## 6. Danh sách lệch lớn giữa expected và actual

### 6.1. Lệch loại 1 - Nhóm được kỳ vọng có backend access nhưng chain chưa cho nền internal

Nhóm bị lệch:
- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`

Ý nghĩa:
- Các nhóm này đang xuất hiện trong expected matrix, tuple Python, view group, hoặc record rule.
- Nhưng chain group hiện tại chưa chứng minh có `base.group_user`.

### 6.2. Lệch loại 2 - Nhóm manager chưa chắc có nền mạnh như expected

Nhóm bị lệch nổi bật:
- `GDH_RST_HR_HRBP_M`

Ý nghĩa:
- Theo expected được làm `done`, `rehire`, `blacklist`
- Nhưng actual nền quyền chain hiện tại chưa kéo internal user rõ ràng

### 6.3. Lệch loại 3 - Có nguy cơ quyền thực tế bị mở rộng bởi group core ngoài thiết kế 0213

Nhóm/rủi ro:
- user có thêm `approvals.group_approval_user`
- user có thêm `approvals.group_approval_manager`
- user có thêm group survey quản trị

Ý nghĩa:
- Dù Phase 0 đã chốt expected matrix, actual rights vẫn có thể bị phá vỡ nếu user mang thêm group core này

## 7. Quyết định đầu vào cho Phase 2

Sau Phase 1, cần chốt một trong hai hướng:

### Hướng A - Điều chỉnh chain group để khớp expected

Ý tưởng:
- Nhóm nào được expected dùng backend thật thì phải kéo `GDH_RST_ALL_BASE_S`

Nhóm cần xem xét:
- `GDH_RST_OPS_OM_M`
- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- có thể cả `GDH_RST_OPS_OC_S` nếu thật sự cần backend read trực tiếp

Ưu điểm:
- Expected matrix và nền ACL sẽ khớp hơn

Rủi ro:
- Có thể ảnh hưởng module khác dùng chung group 0200

### Hướng B - Giữ chain hiện tại, hạ expected backend của một số nhóm

Ý tưởng:
- Chỉ coi các nhóm đã có internal nền là nhóm backend thật
- các nhóm còn lại chỉ nên:
  - xem qua UI hạn chế
  - hoặc bỏ khỏi action backend

Ưu điểm:
- An toàn hơn với group chain dùng chung

Rủi ro:
- Sẽ phải sửa lại expected matrix của Phase 0
- Có thể lệch với ý đồ nghiệp vụ ban đầu

## 8. Đề xuất chốt của Phase 1

Đề xuất hiện tại:
- Không nên sang Phase 2 khi chưa quyết định xong giữa Hướng A và Hướng B.
- Nếu muốn giữ đúng expected matrix của Phase 0, gần như bắt buộc phải xử lý chain group ở `M02_P0200`.
- Nếu không muốn đụng `M02_P0200` sớm, phải thu hẹp lại expected backend access của các nhóm chưa có `base.group_user`.

Đề xuất thực dụng nhất:
- Giữ expected matrix của Phase 0 làm mục tiêu business.
- Trong Phase 2, triển khai theo hướng:
  - chưa sửa chain group ngay
  - nhưng đánh dấu rõ các nhóm lệch để test
  - song song chuẩn bị một quyết định riêng cho `M02_P0200`

## 9. Điều kiện hoàn tất Phase 1

Phase 1 được coi là hoàn tất khi:
- chain group thực tế đã được bóc tách xong
- nhóm nào có `base.group_user` từ chain đã được xác định
- các điểm lệch expected vs actual đã được ghi rõ
- đã có đầu vào rõ ràng để bước sang Phase 2

## 10. Đầu ra để chuyển sang Phase 2

Phase 2 cần nhận từ tài liệu này:
- danh sách nhóm có internal nền thật
- danh sách nhóm đang lệch expected
- các rủi ro về group core của `approvals`
- quyết định sẽ đi theo:
  - Hướng A: sửa chain group
  - hoặc Hướng B: thu expected backend access

Tài liệu này là baseline cho bước đó.
