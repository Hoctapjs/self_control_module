# Phase Estimate 0502 Theo Mức Độ Custom

## 1. Mục đích

Tài liệu này gom các hạng mục triển khai quy trình `0502 - Quản lý bảo trì` theo 4 nhóm để thuận tiện chốt effort:

- Chuẩn Odoo dùng ngay
- Custom thấp
- Custom vừa
- Custom cao

Việc phân nhóm này dựa trên các note đã đối chiếu trước:

- `bang_doi_chieu_cau_hoi_0502_voi_module_chuan_odoo.md`
- `ma_tran_uoc_luong_theo_buoc_0502.md`
- `tong_hop_module_lien_quan_0502.md`

## 2. Bảng Phase Estimate

| Nhóm | Hạng mục | Module chuẩn liên quan | Lý do xếp nhóm | Gợi ý triển khai |
|---|---|---|---|---|
| Chuẩn Odoo dùng ngay | Quản lý danh mục thiết bị, lịch sử bảo trì, yêu cầu bảo trì | `maintenance` | Odoo chuẩn đã có `maintenance.equipment`, `maintenance.request`, phân loại bảo trì định kỳ và phát sinh | Dùng làm trục chính nếu muốn bám thiết bị |
| Chuẩn Odoo dùng ngay | Tạo ticket tiếp nhận yêu cầu từ cửa hàng | `helpdesk` | Odoo chuẩn có `helpdesk.ticket`, portal, share, team, stage, SLA | Dùng nếu muốn có lớp tiếp nhận yêu cầu kiểu service desk |
| Chuẩn Odoo dùng ngay | Điều phối kỹ thuật viên đi xử lý hiện trường | `industry_fsm` | Odoo chuẩn có task FSM, technician, worksheet, timesheet, giao diện riêng cho đội onsite | Dùng cho phần triển khai công việc thực tế |
| Chuẩn Odoo dùng ngay | Kiểm tra tồn kho và xuất vật tư theo chứng từ kho | `stock` | Odoo chuẩn có tồn kho, picking, move, move line, lot/serial, xuất nhập nội bộ | Dùng cho bước vật tư và xuất kho |
| Chuẩn Odoo dùng ngay | Mua vật tư từ nhà cung cấp và nhập kho | `purchase`, `purchase_stock` | Odoo chuẩn có PO, receipt, vendor flow, liên kết nhập kho | Dùng cho nhánh thiếu vật tư phải mua ngoài |
| Chuẩn Odoo dùng ngay | Lập lịch nhân sự bảo trì theo ca và theo thời gian | `planning` | Odoo chuẩn đã có slot, ca làm việc, điều phối lịch | Dùng khi cần tách phần scheduling khỏi request/task |
| Chuẩn Odoo dùng ngay | Tránh phân công người đang nghỉ phép | `planning_holidays` | Có tích hợp time off vào planning | Dùng nếu doanh nghiệp vận hành planning chính thức |
| Chuẩn Odoo dùng ngay | Phân công theo kỹ năng nhân sự | `planning_hr_skills` | Có tích hợp kỹ năng vào planning slot | Dùng khi cần chọn đúng kỹ thuật viên theo skill |
| Chuẩn Odoo dùng ngay | Ghi nhận checklist/biên bản kỹ thuật có cấu trúc | `maintenance_worksheet` | Odoo chuẩn có worksheet template gắn với yêu cầu bảo trì | Dùng cho kiểm tra hiện trạng và nghiệm thu kỹ thuật |
| Custom thấp | Mapping từ ticket sang maintenance request hoặc FSM task | `helpdesk`, `maintenance`, `helpdesk_fsm`, `industry_fsm` | Odoo có sẵn từng phần nhưng chưa có flow chuẩn duy nhất cho toàn bộ 0502 | Custom liên kết object, button, trạng thái |
| Custom thấp | Bổ sung trường nghiệp vụ đặc thù như `timeline xử lý`, `loại xử lý`, `nguồn phát sinh` | `maintenance`, `helpdesk`, `industry_fsm` | Chủ yếu là thêm field, view, search, filter | Là lớp custom nhẹ, ít ảnh hưởng kiến trúc |
| Custom thấp | Dashboard hoặc report theo dõi tình trạng xử lý nội bộ 0502 | `maintenance`, `helpdesk`, `industry_fsm`, `stock` | Odoo có dữ liệu nền nhưng báo cáo đúng form nghiệp vụ 0502 thường phải ráp thêm | Có thể làm search view, graph, pivot hoặc report riêng |
| Custom thấp | Tạo menu điều hướng riêng cho 0502 | nhiều module | Odoo chuẩn phân tán theo app, chưa có menu business flow 0502 thống nhất | Chỉ là custom điều hướng và action |
| Custom thấp | Gắn bước quy trình 0502 vào record để truy vết theo 21 bước | `maintenance`, `helpdesk`, `industry_fsm` | Odoo chuẩn có stage/state nhưng không theo đúng bộ bước 0502 | Có thể dùng selection/state phụ hoặc computed status |
| Custom vừa | Luồng phê duyệt riêng cho `timeline` và `cost` trước khi sửa chữa | `maintenance`, `helpdesk`, `industry_fsm` | Odoo chuẩn không có đúng approval flow này theo ngôn ngữ nghiệp vụ 0502 | Cần thêm state, button, rule, notification |
| Custom vừa | Quy trình xác định `có phát sinh vật tư hay không` theo điểm quyết định riêng | `maintenance`, `industry_fsm`, `stock` | Odoo có vật tư và kho nhưng không có decision node chuẩn y như lưu đồ 0502 | Cần thêm field quyết định, action, điều hướng bước |
| Custom vừa | Gắn yêu cầu xuất kho vật tư phát sinh trực tiếp từ luồng bảo trì 0502 | `stock`, `industry_fsm_stock`, `helpdesk_stock` | Odoo có xuất kho và stock move, nhưng rule nghiệp vụ “phiếu yêu cầu xuất kho vật tư” riêng thường cần custom | Cần custom object trung gian hoặc wizard |
| Custom vừa | Theo dõi báo giá/phương án xử lý theo ngôn ngữ riêng của CMT | `maintenance`, `helpdesk`, `purchase` | Odoo có quotation/PO và worksheet nhưng không có đúng form “đề xuất phương án xử lý/báo giá” như flow 0502 | Cần form, report hoặc model phụ |
| Custom vừa | Luồng tổng hợp kế hoạch bảo trì từ nhiều nguồn phát sinh | `maintenance`, `planning`, `industry_fsm` | Odoo có từng app riêng, nhưng việc gom toàn bộ vào một màn hình điều phối CMT Lead thường phải custom | Cần dashboard/list tổng hợp hoặc wizard lập kế hoạch |
| Custom vừa | Tách rõ nhánh bảo trì định kỳ và phát sinh không định kỳ nhưng vẫn quản lý chung 1 flow 0502 | `maintenance`, `helpdesk` | Odoo có thể làm được bằng cấu hình + custom nhẹ, nhưng không có sẵn nguyên flow hợp nhất | Cần chuẩn hóa object trục chính và rule chuyển đổi |
| Custom vừa | Biên bản nghiệm thu và đánh giá sau bảo trì theo mẫu nghiệp vụ doanh nghiệp | `maintenance_worksheet`, `industry_fsm` | Odoo có worksheet và chữ ký, nhưng biểu mẫu nghiệp vụ cụ thể thường phải thiết kế lại | Cần template, report, field đánh giá |
| Custom cao | Một màn hình hoặc một object duy nhất quản lý xuyên suốt toàn bộ quy trình 0502 | `helpdesk`, `maintenance`, `industry_fsm`, `stock`, `purchase` | Odoo chuẩn chia quy trình theo nhiều app; gom thành 1 trục xuyên suốt là thay đổi solution đáng kể | Cần thiết kế kiến trúc module trục chính hoặc orchestration layer |
| Custom cao | Luồng `outside service` riêng biệt nhưng liên thông chặt với 0502 | chưa có module chuẩn khớp trực tiếp | Odoo chuẩn không có sẵn một flow ngoài dịch vụ đúng như mô tả 0502 | Cần phân tích riêng xem dùng vendor service, purchase hay subcontract style |
| Custom cao | Cơ chế phê duyệt nhiều tầng theo phân quyền doanh nghiệp riêng cho CMT Lead, cửa hàng, cấp duyệt khác | `maintenance`, `helpdesk`, `purchase`, `approvals` nếu có | Chuẩn Odoo chỉ đáp ứng một phần; approval matrix kiểu doanh nghiệp thường cần custom đáng kể | Cần state machine và phân quyền chi tiết |
| Custom cao | Ánh xạ đầy đủ 21 bước trong lưu đồ thành state machine bắt buộc trên hệ thống | nhiều module | Odoo chuẩn có state/stage theo từng app chứ không theo full BPMN 21 bước | Cần module workflow trung tâm |
| Custom cao | Chuỗi chứng từ nghiệp vụ riêng gồm phiếu yêu cầu bảo trì, phiếu bảo trì, phiếu xuất kho vật tư, biên bản kiểm tra và bàn giao theo bộ form thống nhất | `maintenance`, `stock`, `purchase`, `maintenance_worksheet` | Odoo có từng chứng từ nền nhưng không có bộ chứng từ 0502 đồng bộ theo đúng tên gọi và logic doanh nghiệp | Cần model/report/sequence/template đồng bộ |

## 3. Gợi ý Chia Phase

### Phase 1 - Đi nhanh theo chuẩn Odoo

Nên ưu tiên các hạng mục:

- `maintenance` để quản lý thiết bị và maintenance request
- `industry_fsm` nếu có đội kỹ thuật đi xử lý thực tế
- `stock` cho vật tư
- `purchase` + `purchase_stock` cho mua ngoài
- `planning` nếu cần điều phối ca rõ ràng
- `maintenance_worksheet` nếu cần checklist và biên bản kỹ thuật

Mục tiêu của phase này là chạy được nghiệp vụ cốt lõi với ít custom nhất.

### Phase 2 - Bổ sung custom thấp và custom vừa

Nên ưu tiên các hạng mục:

- mapping giữa các object
- field và trạng thái đặc thù 0502
- report và dashboard điều hành
- approval timeline/cost
- nhánh vật tư phát sinh
- biểu mẫu nghiệm thu đặc thù

Mục tiêu của phase này là đưa hệ thống gần hơn với lưu đồ nghiệp vụ 0502 thực tế.

### Phase 3 - Xử lý custom cao

Chỉ nên làm khi doanh nghiệp thật sự cần:

- workflow 21 bước bám sát lưu đồ
- object trục chính xuyên suốt
- outside service flow riêng
- bộ chứng từ nội bộ thống nhất toàn quy trình

Mục tiêu của phase này là hoàn thiện solution đặc thù doanh nghiệp, nhưng effort và rủi ro sẽ cao hơn đáng kể.

## 4. Kết luận Nhanh

- Nếu ưu tiên triển khai nhanh, nên bám `maintenance + industry_fsm + stock + purchase`
- Nếu ưu tiên bám sát đúng lưu đồ 0502 từng bước, sẽ phát sinh nhiều custom mức vừa đến cao
- Cách an toàn là chốt `phase 1` theo chuẩn Odoo trước, sau đó mới quyết định có cần đầu tư workflow đặc thù sâu hơn hay không
