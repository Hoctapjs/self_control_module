# Các câu hỏi cần trả lời để chốt danh sách module kế thừa cho 0502

## 1. Mục đích của note

File này dùng để liệt kê các câu hỏi nghiệp vụ và kỹ thuật cần được làm rõ trước khi chốt danh sách module Odoo sẽ kế thừa để triển khai quy trình 0502 bảo trì và sửa chữa máy móc.

Mục tiêu là tránh chọn module theo cảm tính, tránh kế thừa chồng chéo, và xác định đúng:

- module nào là trục chính
- module nào là hỗ trợ
- module nào chỉ nên tích hợp khi thật sự cần

## 2. Câu hỏi về điểm bắt đầu của quy trình

- Nhu cầu xử lý của cửa hàng sẽ được ghi nhận theo dạng ticket hay theo dạng maintenance request?
-> ghi nhận ticket và CMT sẽ kiểm tra và tạo Maintenance Request (nếu là bảo trì) hoặc FSM Task (nếu là xử lý thực địa)
- Người dùng nghiệp vụ có quen làm việc theo ticket hay theo phiếu bảo trì thiết bị?
-> quen làm theo ticket
- Cửa hàng có cần một màn hình duy nhất để tạo yêu cầu hay có nhiều loại đầu vào khác nhau?
-> cần 1 màn hình thôi, CMT sẽ tự phân loại và tạo yêu cầu
- Mọi yêu cầu 0502 đều xuất phát từ cửa hàng, hay có trường hợp hệ thống hoặc bộ phận khác chủ động tạo yêu cầu?
-> nhiều nguồn tạo như hệ thống Odoo về bảo trì định kỳ, cửa hàng về yêu cầu phát sinh sự cố, CMT tạo tạy nếu xác định được ra vấn đề
- Bảo trì định kỳ và bảo trì phát sinh có cần dùng chung một loại hồ sơ đầu vào hay phải tách riêng?
-> dùng chung 1 loại hồ sơ đầu vào
- Có yêu cầu giữ ticket để làm đầu mối trao đổi giữa cửa hàng và CMT không?
-> có nên giữ
- Nếu dùng ticket, ticket có chỉ là đầu vào hay sẽ là đối tượng theo dõi xuyên suốt toàn quy trình?
-> ticket là đối tượng theo dõi xuyên suốt toàn quy trình

## 3. Câu hỏi về đối tượng quản lý chính

- Đối tượng trung tâm của quy trình là máy móc thiết bị hay là yêu cầu xử lý?
-> đối tượng trung tâm là yêu cầu xử lý, nhưng vẫn còn dữ liệu nền là máy móc thiết bị
- Doanh nghiệp có cần quản lý danh mục equipment đầy đủ cho từng cửa hàng không?
-> có cần quản lý danh mục equipment đầy đủ
- Có cần lưu lịch sử bảo trì theo từng máy hay chỉ cần theo từng yêu cầu?
-> lưu lịch sử bảo trì theo từng máy
- Có cần theo dõi preventive maintenance và corrective maintenance tách biệt không?
-> KHÔNG cần tách model, vẫn dùng chung maintenance.request, nhưng cần tách trong cách theo dõi
- Có cần quản lý chu kỳ bảo trì định kỳ theo thiết bị không?
-> có, cần quản lý chu kỳ theo từng thiết bị
- Có cần quản lý tình trạng vận hành của từng máy trước và sau bảo trì không?
-> có, nên quản lý trạng thái trước và sau bảo trì
- Có cần truy vết đầy đủ lịch sử hỏng hóc, thay vật tư, chi phí và nghiệm thu theo từng máy không?
-> có, nên truy vết đầy đủ theo từng máy

## 4. Câu hỏi về cách tổ chức thực thi công việc

- Sau khi tiếp nhận yêu cầu, công việc có cần được phân cho kỹ thuật viên dưới dạng task không?
-> có
- Đội kỹ thuật có làm việc kiểu hiện trường, di chuyển giữa các cửa hàng như mô hình Field Service không?
-> có
- Có cần theo dõi người thực hiện, thời gian bắt đầu, thời gian kết thúc và timesheet cho từng công việc không?
-> Có
- Có cần giao diện riêng cho kỹ thuật viên khi đi xử lý tại cửa hàng không?
-> có
- Có cần quản lý báo cáo thực hiện công việc ngay trên task hiện trường không?
-> có
- Có cần phân tách rõ người tiếp nhận yêu cầu và người trực tiếp thực hiện sửa chữa không?
-> Có. Quy trình cần phân tách rõ vai trò giữa người tiếp nhận yêu cầu (CMT/điều phối) và người trực tiếp thực hiện sửa chữa (kỹ thuật viên).

Người tiếp nhận chịu trách nhiệm tiếp nhận, kiểm tra, đề xuất phương án và điều phối công việc, trong khi người thực hiện chịu trách nhiệm triển khai sửa chữa thực tế và cập nhật kết quả.

Ngoài ra, quy trình còn có vai trò CMT Lead tham gia vào việc lập kế hoạch và điều phối nguồn lực.

## 5. Câu hỏi về lập kế hoạch và điều phối nhân sự

- Việc lập kế hoạch bảo trì có cần một lớp scheduling riêng hay chỉ cần phân công trực tiếp trên yêu cầu hoặc task?
-> chỉ cần phân công trực tiếp trên task là đủ
- Đội bảo trì có quy mô đủ lớn để cần dùng Planning không?
-> chưa cần
- Có cần lên lịch theo ca, theo ngày, theo giờ hoặc theo vùng phụ trách không?
-> theo ngày và theo giờ là được
- Có cần tránh phân công người đang nghỉ phép hay không?
-> có, tránh phân công cho người đang nghỉ phép
- Có cần phân công theo kỹ năng kỹ thuật viên, loại máy, loại sự cố hoặc cấp độ tay nghề không?
-> có nhưng chỉ cần gán người phù hợp, chưa cần skill matrix phức tạp
- Có cần so sánh kế hoạch phân công với thời gian làm thực tế không?
-> chưa cần
- Có cần theo dõi năng suất hoặc hiệu suất triển khai của đội bảo trì sau này không?
-> chưa cần hiện tại

## 6. Câu hỏi về xử lý vật tư

- Trong quy trình sửa chữa có thường xuyên phát sinh vật tư không?
-> có
- Vật tư phát sinh có bắt buộc phải đi qua quy trình yêu cầu xuất kho không?
-> có
- Vật tư sẽ được xuất trực tiếp từ kho trung tâm, kho cửa hàng hay nhiều loại kho khác nhau?
-> có thể gôm kho trung tâm và kho cửa hàng
- Có cần theo dõi vật tư đã dùng theo từng yêu cầu, từng máy hoặc từng lần sửa chữa không?
-> có
- Có cần liên kết vật tư phát sinh trực tiếp với ticket, task hoặc maintenance request không?
-> có
- Có cần kiểm soát tồn kho trước khi phê duyệt sửa chữa không?
-> có
- Có cần ghi nhận tiêu hao vật tư theo stock move chuẩn của Odoo không?
-> có
- Đội kho hoặc kỹ thuật viên có dùng barcode scanner để xuất vật tư không?
-> chưa cần ở hiện tại, mở rộng sau
- Có cần quản lý lot hoặc serial cho vật tư thay thế không?
-> nếu vật tư là linh kiện có bảo hành thì cần, còn lại thì không cần

## 7. Câu hỏi về mua ngoài

- Khi thiếu vật tư, doanh nghiệp có luôn tạo purchase order hay còn bước trung gian phê duyệt nội bộ?
-> có bước phê duyệt nội bộ trước khi tạo po
- Vật tư mua ngoài có bắt buộc nhập kho trước rồi mới xuất cho sửa chữa không?
-> có
- Có trường hợp mua trực tiếp để dùng ngay mà không qua kho không?
-> chưa cần hiện tại, có thể mở rộng sau
- Doanh nghiệp có cần quản lý nhiều báo giá từ nhiều nhà cung cấp không?
-> chưa cần hiện tại, có thể mở rộng sau
- Có cần call for tender hoặc blanket order không?
-> chưa cần hiện tại
- Có cần liên kết vật tư mua ngoài trực tiếp với yêu cầu sửa chữa hay repair order không?
-> có
- Có cần kiểm soát lead time mua hàng để ảnh hưởng vào timeline xử lý không?
-> có expected delivery date

## 8. Câu hỏi về outside service

- Outside service là một quy trình độc lập hoàn toàn hay chỉ là một nhánh phụ của 0502?
-> cần thêm thông tin
- Khi chuyển outside service, đối tượng nào sẽ được chuyển tiếp: ticket, maintenance request hay task?
-> cần thêm thông tin
- Có cần theo dõi nhà cung cấp dịch vụ ngoài như vendor không?
-> cần thêm thông tin
- Có cần quản lý báo giá dịch vụ ngoài, timeline dịch vụ ngoài và nghiệm thu dịch vụ ngoài không?
-> cần thêm thông tin
- Có cần tích hợp chi phí outside service vào tổng chi phí xử lý của yêu cầu 0502 không?
-> có
- Có cần phân biệt rõ giữa mua vật tư ngoài và thuê dịch vụ ngoài không?
-> có

## 9. Câu hỏi về repair flow

- Quy trình sửa chữa có cần dùng app Repair chuẩn của Odoo không?
-> Ưu tiên Maintenance + Field Service, không cần Repair cho toàn bộ.
- Có cần tạo repair order chính thức cho từng trường hợp sửa chữa không?
-> Dùng Maintenance Request → FSM Task là đủ để theo dõi.
- Có cần liên kết yêu cầu bảo trì với repair order để theo dõi tiến độ không?
-> Tiến độ nên theo: Ticket (giao tiếp), FSM Task (thực thi), Maintenance Request (nghiệp vụ kỹ thuật)
- Có cần kết nối repair với mua hàng khi thiếu vật tư không?
-> Không, Flow đúng: Maintenance / FSM → Stock → Purchase
- Có cần giữ toàn bộ flow sửa chữa trong maintenance hoặc FSM thay vì dùng Repair không?
-> có, dùng Maintenance + FSM + Inventory + Purchase
- Tiêu chí nào để quyết định trường hợp nào đi theo repair flow và trường hợp nào chỉ là maintenance work thông thường?
-> KHÔNG cần Repair nếu: sửa tại cửa hàng, công việc kiểu: vệ sinh, thay linh kiện đơn giản, kiểm tra / bảo trì, không cần quy trình kỹ thuật phức tạp

## 10. Câu hỏi về chi phí và kế toán

- Có cần theo dõi chi phí sửa chữa theo từng yêu cầu không? -> mỗi request / task phải có tổng chi phí
- Có cần tách chi phí nhân công, vật tư, dịch vụ ngoài và chi phí khác không? -> có
- Có cần ghi nhận giá trị vật tư xuất dùng vào kế toán kho không? -> có
- Có cần tính cost thực tế để so sánh với cost được duyệt ban đầu không? -> có
- Có cần invoice hoặc billing cho cửa hàng nội bộ hoặc đơn vị liên quan không? -> chưa cần ở hiện tại
- Có cần sử dụng module `stock_account` hay logic kế toán kho chỉ là yêu cầu báo cáo? -> chưa cần hiện tại
- Nếu triển khai FSM, có cần ghi nhận timesheet mang tính costing hoặc billing không? -> Có (ở mức costing)

## 11. Câu hỏi về biểu mẫu, checklist và nghiệm thu

- Có cần checklist kiểm tra theo từng loại máy không? -> có
- Có cần mẫu biên bản sửa chữa hoặc bảo trì chuẩn không? -> có
- Có cần mẫu nghiệm thu sau bảo trì không? -> có
- Có cần kỹ thuật viên điền biểu mẫu trên hệ thống trong lúc làm việc không? -> có
- Có cần in biểu mẫu hoặc xuất PDF cho cửa hàng ký xác nhận không? -> có
- Có cần ảnh hiện trường trước và sau sửa chữa không? -> có
- Có cần chữ ký điện tử hoặc xác nhận trực tiếp trên thiết bị không? -> có

## 12. Câu hỏi về phân quyền và vai trò người dùng

- Những vai trò nào sẽ tham gia chính thức trong hệ thống: cửa hàng, CMT, CMT Lead, kho, mua hàng, kế toán, đối tác ngoài? -> cửa hàng, cmt, cmt lead, kho, mua hàng, kế toán
- Cửa hàng có được theo dõi trạng thái xử lý trực tiếp trên hệ thống không? -> có, vì cần xem tiến độ và nhận cập nhật, qua ticket hoặc portal view
- CMT có được tạo hoặc chỉnh sửa phương án, báo giá và yêu cầu vật tư không? -> có, cmt là người tạo, chỉnh sửa, cập nhật
- CMT Lead có vai trò phê duyệt nào trong hệ thống? -> có, phê duyệt vật tư, kiểm soát kế hoạch, điều phối
- Bộ phận kho có cần thao tác trực tiếp trên yêu cầu 0502 hay chỉ làm trên chứng từ kho? -> chỉ làm trên chứng từ kho
- Bộ phận mua hàng có cần thấy liên kết giữa PO và yêu cầu sửa chữa không? -> có, vì po phát sinh từ yêu cầu sửa chữa
- Có cần phân quyền theo cửa hàng, theo khu vực hay theo đội kỹ thuật không? -> có, theo cửa hàng (cửa hàng chỉ thấy yêu cầu của mình), theo đội kỹ thuật / cmt (mỗi team xử lý phần việc riêng), theo role (CMT, CMT Lead, Kho, Purchase, Store) 

## 13. Câu hỏi về báo cáo và theo dõi

- Những KPI nào là bắt buộc: thời gian xử lý, tỷ lệ đúng hạn, chi phí sửa chữa, số lần hỏng lặp lại, tiêu hao vật tư?
->
Thời gian xử lý (Lead time) → từ tạo yêu cầu → nghiệm thu
Tỷ lệ đúng hạn (On-time rate) → so với timeline đã duyệt
Chi phí sửa chữa theo yêu cầu → tổng & theo loại (nhân công/vật tư/dịch vụ ngoài)
Số lần hỏng lặp lại theo thiết bị → reliability
Tiêu hao vật tư → theo request / theo máy
- Có cần dashboard riêng cho CMT Lead không?
-> có
- Có cần báo cáo theo cửa hàng, theo máy, theo kỹ thuật viên, theo nhóm sự cố không?
-> có
Theo cửa hàng → hiệu suất vận hành từng điểm
Theo máy (equipment) → lịch sử & reliability
Theo kỹ thuật viên → năng suất / hiệu quả
Theo nhóm sự cố → pattern lỗi
- Có cần theo dõi SLA cho yêu cầu xử lý không?
-> có
SLA có thể là:
thời gian phản hồi
thời gian hoàn thành
- Có cần báo cáo chênh lệch giữa kế hoạch và thực tế không?
-> có
cần so:
thời gian kế hoạch vs thực tế
chi phí dự kiến vs thực tế
- Có cần truy vết đầy đủ từ yêu cầu đến xuất kho, mua hàng, sửa chữa và nghiệm thu không?
-> có

## 14. Câu hỏi về dữ liệu hiện có và mức độ kế thừa

- Doanh nghiệp hiện đã dùng module nào trong các nhóm `helpdesk`, `maintenance`, `industry_fsm`, `planning`, `stock`, `purchase`?
-> Quy trình 0502 sẽ là triển khai mới bằng cách kế thừa các module chuẩn của Odoo
- Có dữ liệu equipment, ticket, task, kho, vendor hoặc purchase order đang chạy thật không? -> mới hoàn toàn, hiện chưa có dữ liệu nào được triển khai
- Có quy trình nào đang vận hành dở mà 0502 phải kế thừa thay vì làm mới không? -> 0502 sẽ được làm mới bằng cách kế thừa các module gốc của Odoo, hạn chế việc xây dựng model, action mới, cái nào kế thừa được thì kế thừa hết, sau đó mới thêm các phần mới hoàn toàn vào
- Có custom module nào hiện tại đã chạm vào các luồng maintenance, helpdesk, stock hoặc purchase không? -> không có custom module nào ảnh hưởng đến các luồng này
- Có giới hạn nào về việc không được thay đổi flow chuẩn của một số module đang chạy production không? -> không có giới hạn hiện tại, nhưng ta sẽ hạn chế thay đổi flow chuẩn của Odoo, ta sẽ tận dụng mọi thứ đã có của các module gốc, và phần nào mới hoàn toàn thì ta mới thực hiện triển khai mới cho phần đó thôi
- Đội triển khai muốn tối đa kế thừa chuẩn Odoo hay chấp nhận custom mạnh để bám quy trình hiện tại? -> Ưu tiên kế thừa chuẩn Odoo, chỉ custom khi thiếu tính năng đó trong module gốc, cần fit thêm cho nghiệp vụ đặc thù

## 15. Các câu hỏi chốt để quyết định module trục chính

- Trục chính nên là `maintenance`, `helpdesk` hay `industry_fsm`?
-> maintenance là trục chính, industry_fsm = lớp thực thi, helpdesk = optional (entry point)
- Nếu chọn `maintenance`, có đủ để bao phủ bước tiếp nhận, xử lý, vật tư và nghiệm thu không?
-> Không đủ hoàn toàn

→ maintenance cover:

equipment
maintenance request
basic workflow

 Nhưng thiếu:

thực thi hiện trường → cần FSM
vật tư → cần stock
mua ngoài → cần purchase

 ⇒ phải kết hợp module khác
- Nếu chọn `helpdesk`, có cần nối tiếp sang `helpdesk_fsm` hoặc `helpdesk_repair` không?
-> Không bắt buộc
- Có cần kết hợp `maintenance` để quản lý equipment và `industry_fsm` để thực thi công việc không?
-> có
- Có cần `planning` làm lớp hỗ trợ phân công hay phân công ngay trong FSM là đủ?
-> triển khai trước fsm là vừa đủ, nếu cần sẽ phát triển planning thêm
- Có cần `stock` và `purchase_stock` ngay từ phase 1 hay có thể triển khai sau?
-> có, cần ngay từ đầu luôn

- Có cần `stock_account`, `purchase_requisition` hoặc `planning_attendance` ngay từ đầu hay để phase sau?
-> chưa cần luôn ngay từ đầu, có thể triển khai sau

## 16. Đề xuất cách dùng bộ câu hỏi này

Nên trả lời các câu hỏi theo thứ tự:

1. Chốt đối tượng trung tâm của quy trình là gì.
2. Chốt điểm bắt đầu của quy trình là ticket, maintenance request hay task.
3. Chốt cách tổ chức thực thi là theo maintenance, repair hay field service.
4. Chốt mức độ bắt buộc của vật tư, kho và mua ngoài.
5. Chốt có cần scheduling riêng hay không.
6. Chốt mức độ cần kế toán, costing và báo cáo nâng cao.

Sau khi trả lời được các nhóm câu hỏi trên, có thể chốt danh sách module kế thừa theo hướng rõ ràng hơn, ví dụ:

- hướng thiên về quản lý thiết bị: `maintenance` + `maintenance_worksheet` + `stock` + `purchase_stock`
- hướng thiên về ticket và điều phối hiện trường: `helpdesk` + `helpdesk_fsm` + `industry_fsm` + `industry_fsm_stock`
- hướng có điều phối nhân sự nâng cao: bổ sung `planning` + `planning_holidays` + `planning_hr_skill

## 17. Đánh giá từng câu trả lời theo chuẩn triển khai Odoo theo tiêu chí chặt

Ghi chú:

- Chỉ giữ `Đúng chuẩn Odoo` khi dò ra được phần có thật trong module chuẩn Odoo như model, field, view hoặc wizard.
- Nếu không chỉ ra được phần có thật trong module chuẩn, hoặc câu trả lời chỉ là quyết định thiết kế, giả định nghiệp vụ hay định hướng triển khai, thì đánh dấu `Không đúng chuẩn Odoo`.
- Các câu đang trả lời là `cần thêm thông tin` vẫn giữ trạng thái chưa đủ cơ sở kết luận.

### 17.1. Nhóm câu hỏi về điểm bắt đầu của quy trình

- Ghi nhận ticket và CMT sẽ kiểm tra và tạo Maintenance Request hoặc FSM Task: `Không đúng chuẩn Odoo`
- Quen làm theo ticket: `Không đúng chuẩn Odoo`
- Cần một màn hình duy nhất để tạo yêu cầu: `Không đúng chuẩn Odoo`
- Nhiều nguồn tạo như định kỳ, cửa hàng, CMT tạo tay: `Không đúng chuẩn Odoo`
- Dùng chung một loại hồ sơ đầu vào: `Không đúng chuẩn Odoo`
- Giữ ticket làm đầu mối trao đổi giữa cửa hàng và CMT: `Đúng chuẩn Odoo`
  Bằng chứng:
  `helpdesk.ticket` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_ticket.py) kế thừa `portal.mixin`;
  portal của ticket có trong [helpdesk_portal_templates.xml](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/views/helpdesk_portal_templates.xml);
  chia sẻ và subscribe người liên quan có trong [portal_share.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/wizard/portal_share.py).
- Ticket là đối tượng theo dõi xuyên suốt toàn quy trình: `Không đúng chuẩn Odoo`

### 17.2. Nhóm câu hỏi về đối tượng quản lý chính

- Đối tượng trung tâm là yêu cầu xử lý, nhưng vẫn có dữ liệu nền là thiết bị: `Đúng chuẩn Odoo`
  Bằng chứng:
  model `maintenance.request` có field `equipment_id` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py).
- Quản lý đầy đủ danh mục equipment theo từng cửa hàng: `Không đúng chuẩn Odoo`
- Lưu lịch sử bảo trì theo từng máy: `Đúng chuẩn Odoo`
  Bằng chứng:
  model `maintenance.equipment` có field `maintenance_ids = fields.One2many('maintenance.request', 'equipment_id')` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py).
- Không tách model preventive và corrective, vẫn dùng chung `maintenance.request`: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance.request` dùng field `maintenance_type = fields.Selection([('corrective', ...), ('preventive', ...)])` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py).
- Quản lý chu kỳ bảo trì định kỳ theo từng thiết bị: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance.request` có các field `recurring_maintenance`, `repeat_interval`, `repeat_unit`, `repeat_type`, `repeat_until` và vẫn gắn `equipment_id` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py).
- Quản lý trạng thái trước và sau bảo trì: `Không đúng chuẩn Odoo`
- Truy vết đầy đủ hỏng hóc, vật tư, chi phí và nghiệm thu theo từng máy: `Không đúng chuẩn Odoo`

### 17.3. Nhóm câu hỏi về cách tổ chức thực thi công việc

- Công việc cần được phân cho kỹ thuật viên dưới dạng task: `Đúng chuẩn Odoo`
  Bằng chứng:
  `helpdesk_fsm` có field `fsm_task_ids = fields.One2many('project.task', 'helpdesk_ticket_id', ...)` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk_fsm/models/helpdesk_ticket.py).
- Đội kỹ thuật làm việc kiểu hiện trường như Field Service: `Đúng chuẩn Odoo`
  Bằng chứng:
  `industry_fsm` mở rộng `project.task` với field `is_fsm` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py).
- Theo dõi người thực hiện, thời gian bắt đầu, kết thúc và timesheet: `Đúng chuẩn Odoo`
  Bằng chứng:
  `industry_fsm.models.project_task` dùng các field `planned_date_begin`, `date_deadline`, `user_ids` trong các compute;
  có `action_view_timesheets()` mở `account.analytic.line` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py).
- Có giao diện riêng cho kỹ thuật viên tại cửa hàng: `Đúng chuẩn Odoo`
  Bằng chứng:
  `industry_fsm` có view chuyên biệt trong [fsm_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/views/fsm_views.xml) và portal trong manifest `views/project_portal_templates.xml`.
- Có báo cáo thực hiện công việc ngay trên task hiện trường: `Đúng chuẩn Odoo`
  Bằng chứng:
  `industry_fsm` có report trong manifest: `report/worksheet_custom_report_templates.xml`, `report/worksheet_custom_reports.xml`;
  model `project.task` có các field `display_sign_report_primary`, `display_send_report_primary`, `worksheet_signature`, `worksheet_signed_by` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py).
- Phân tách rõ người tiếp nhận, người thực hiện và vai trò CMT Lead: `Không đúng chuẩn Odoo`

### 17.4. Nhóm câu hỏi về lập kế hoạch và điều phối nhân sự

- Chỉ cần phân công trực tiếp trên task là đủ: `Không đúng chuẩn Odoo`
- Chưa cần dùng Planning: `Không đúng chuẩn Odoo`
- Lên lịch theo ngày và theo giờ là đủ: `Không đúng chuẩn Odoo`
- Tránh phân công cho người đang nghỉ phép: `Đúng chuẩn Odoo`
  Bằng chứng:
  `planning_holidays.models.planning_slot` có field `leave_warning` và compute `_compute_leave_warning` trên `planning.slot` trong [planning_slot.py](/d:/odoo-19.0+e.20250918/odoo/addons/planning_holidays/models/planning_slot.py).
- Gán người phù hợp nhưng chưa cần skill matrix phức tạp: `Đúng chuẩn Odoo`
  Bằng chứng:
  `planning_hr_skills.models.planning_slot` có field `employee_skill_ids` và override `_group_expand_resource_id` để lọc resource theo skill trong [planning_slot.py](/d:/odoo-19.0+e.20250918/odoo/addons/planning_hr_skills/models/planning_slot.py).
- Chưa cần so sánh kế hoạch với thời gian làm thực tế: `Không đúng chuẩn Odoo`
- Chưa cần theo dõi năng suất hoặc hiệu suất hiện tại: `Không đúng chuẩn Odoo`

### 17.5. Nhóm câu hỏi về xử lý vật tư

- Quy trình sửa chữa thường xuyên phát sinh vật tư: `Không đúng chuẩn Odoo`
- Vật tư bắt buộc phải đi qua quy trình yêu cầu xuất kho: `Không đúng chuẩn Odoo`
- Có thể gồm kho trung tâm và kho cửa hàng: `Đúng chuẩn Odoo`
  Bằng chứng:
  module `stock` có các model `stock.warehouse`, `stock.location`, `stock.picking` và view tương ứng trong manifest, bao phủ nhiều kho và nhiều vị trí kho.
- Theo dõi vật tư đã dùng theo từng yêu cầu, từng máy hoặc từng lần sửa chữa: `Không đúng chuẩn Odoo`
- Có cần liên kết vật tư phát sinh trực tiếp với ticket, task hoặc maintenance request không: `Không đúng chuẩn Odoo`
- Có cần kiểm soát tồn kho trước khi phê duyệt sửa chữa không: `Không đúng chuẩn Odoo`
- Có cần ghi nhận tiêu hao vật tư theo stock move chuẩn của Odoo không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `stock.move` và `stock.move.line` là model lõi của module `stock`; có thể xem tại [stock_move_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_move_line.py) và [stock_picking.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_picking.py).
- Đội kho hoặc kỹ thuật viên chưa cần barcode ở hiện tại: `Không đúng chuẩn Odoo`
- Có cần quản lý lot hoặc serial cho vật tư thay thế nếu vật tư có bảo hành: `Đúng chuẩn Odoo`
  Bằng chứng:
  `product.product` có field `tracking` ở view [product_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/stock/views/product_views.xml);
  `stock.move.line` có field `lot_id` và related `tracking` trong [stock_move_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_move_line.py).

### 17.6. Nhóm câu hỏi về mua ngoài

- Có bước phê duyệt nội bộ trước khi tạo PO: `Không đúng chuẩn Odoo`
- Vật tư mua ngoài bắt buộc nhập kho trước rồi mới xuất cho sửa chữa: `Đúng chuẩn Odoo`
  Bằng chứng:
  `purchase_stock` nối `purchase.order.line` với `stock.move` qua field `move_ids` và `purchase_line_id` trong [purchase_order_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase_stock/models/purchase_order_line.py).
- Chưa cần trường hợp mua trực tiếp để dùng ngay không qua kho: `Không đúng chuẩn Odoo`
- Chưa cần nhiều báo giá từ nhiều nhà cung cấp: `Không đúng chuẩn Odoo`
- Chưa cần call for tender hoặc blanket order: `Không đúng chuẩn Odoo`
- Có cần liên kết vật tư mua ngoài trực tiếp với yêu cầu sửa chữa hay repair order không: `Không đúng chuẩn Odoo`
- Có cần expected delivery date để ảnh hưởng vào timeline xử lý không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `purchase.order` có field `date_planned = fields.Datetime(string='Expected Arrival', ...)` trong [purchase_order.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase/models/purchase_order.py);
  `purchase.order.line` có `date_planned` trong [purchase_order_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase/models/purchase_order_line.py).

### 17.7. Nhóm câu hỏi về outside service

- Outside service là một quy trình độc lập hoàn toàn hay chỉ là một nhánh phụ của 0502: `Chưa đủ thông tin để kết luận`
- Khi chuyển outside service, đối tượng nào sẽ được chuyển tiếp: ticket, maintenance request hay task: `Chưa đủ thông tin để kết luận`
- Có cần theo dõi nhà cung cấp dịch vụ ngoài như vendor: `Chưa đủ thông tin để kết luận`
- Có cần quản lý báo giá dịch vụ ngoài, timeline dịch vụ ngoài và nghiệm thu dịch vụ ngoài: `Chưa đủ thông tin để kết luận`
- Có cần tích hợp chi phí outside service vào tổng chi phí xử lý của yêu cầu 0502: `Không đúng chuẩn Odoo`
- Có cần phân biệt rõ giữa mua vật tư ngoài và thuê dịch vụ ngoài: `Không đúng chuẩn Odoo`

### 17.8. Nhóm câu hỏi về repair flow

- Ưu tiên Maintenance + Field Service, không cần Repair cho toàn bộ: `Không đúng chuẩn Odoo`
- Dùng Maintenance Request sang FSM Task là đủ để theo dõi: `Không đúng chuẩn Odoo`
- Tiến độ nên theo Ticket, FSM Task, Maintenance Request: `Không đúng chuẩn Odoo`
- Không, flow đúng là Maintenance hoặc FSM sang Stock sang Purchase: `Không đúng chuẩn Odoo`
- Có, dùng Maintenance + FSM + Inventory + Purchase: `Không đúng chuẩn Odoo`
- Không cần Repair nếu sửa tại cửa hàng và công việc đơn giản: `Không đúng chuẩn Odoo`

### 17.9. Nhóm câu hỏi về chi phí và kế toán

- Mỗi request hoặc task phải có tổng chi phí: `Không đúng chuẩn Odoo`
- Có tách chi phí nhân công, vật tư, dịch vụ ngoài và chi phí khác: `Không đúng chuẩn Odoo`
- Có ghi nhận giá trị vật tư xuất dùng vào kế toán kho: `Đúng chuẩn Odoo`
  Bằng chứng:
  `stock_account.models.stock_move` có field `account_move_id` và method `_create_account_move()` trong [stock_move.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock_account/models/stock_move.py).
- Có tính cost thực tế để so sánh với cost được duyệt ban đầu: `Không đúng chuẩn Odoo`
- Chưa cần invoice hoặc billing ở hiện tại: `Không đúng chuẩn Odoo`
- Chưa cần sử dụng module `stock_account`: `Không đúng chuẩn Odoo`
- Nếu triển khai FSM, có cần ghi nhận timesheet mang tính costing hoặc billing không: `Không đúng chuẩn Odoo`

### 17.10. Nhóm câu hỏi về biểu mẫu, checklist và nghiệm thu

- Có checklist kiểm tra theo từng loại máy không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance_worksheet.models.maintenance_request` có field `worksheet_template_id` trên `maintenance.request` trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/models/maintenance_request.py).
- Có cần mẫu biên bản sửa chữa hoặc bảo trì chuẩn không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance_worksheet` có `worksheet.template` gắn với `maintenance.request` trong [maintenance_worksheet_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/views/maintenance_worksheet_views.xml).
- Có cần mẫu nghiệm thu sau bảo trì không: `Đúng chuẩn Odoo`
  Bằng chứng:
  vẫn dùng `worksheet.template` trên `maintenance.request`; đây là phần có thật trong module chuẩn, có thể cấu hình mẫu biểu cho từng request.
- Có cần kỹ thuật viên điền biểu mẫu trên hệ thống trong lúc làm việc không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance_worksheet.models.maintenance_request` có method `action_maintenance_worksheet()` trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/models/maintenance_request.py).
- Có cần in biểu mẫu hoặc xuất PDF cho cửa hàng ký xác nhận không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `maintenance_worksheet` có `report/maintenance_custom_report.xml` và `report/maintenance_custom_report_templates.xml` trong manifest.
- Có cần ảnh hiện trường trước và sau sửa chữa không: `Không đúng chuẩn Odoo`
- Có cần chữ ký điện tử hoặc xác nhận trực tiếp trên thiết bị không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `industry_fsm.models.project_task` có field `worksheet_signature` và `worksheet_signed_by` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py).

### 17.11. Nhóm câu hỏi về phân quyền và vai trò người dùng

- Những vai trò nào sẽ tham gia chính thức trong hệ thống: cửa hàng, CMT, CMT Lead, kho, mua hàng, kế toán, đối tác ngoài: `Không đúng chuẩn Odoo`
- Cửa hàng có được theo dõi trạng thái xử lý trực tiếp trên hệ thống không: `Đúng chuẩn Odoo`
  Bằng chứng:
  helpdesk có portal ticket trong [helpdesk_portal_templates.xml](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/views/helpdesk_portal_templates.xml).
- CMT có được tạo hoặc chỉnh sửa phương án, báo giá và yêu cầu vật tư không: `Không đúng chuẩn Odoo`
- CMT Lead có vai trò phê duyệt nào trong hệ thống: `Không đúng chuẩn Odoo`
- Bộ phận kho có cần thao tác trực tiếp trên yêu cầu 0502 hay chỉ làm trên chứng từ kho: `Không đúng chuẩn Odoo`
- Bộ phận mua hàng có cần thấy liên kết giữa PO và yêu cầu sửa chữa không: `Không đúng chuẩn Odoo`
- Có cần phân quyền theo cửa hàng, theo khu vực hay theo đội kỹ thuật không: `Không đúng chuẩn Odoo`

### 17.12. Nhóm câu hỏi về báo cáo và theo dõi

- Những KPI nào là bắt buộc: lead time, on-time rate, chi phí, reliability, tiêu hao vật tư: `Không đúng chuẩn Odoo`
- Có cần dashboard riêng cho CMT Lead không: `Không đúng chuẩn Odoo`
- Có cần báo cáo theo cửa hàng, theo máy, theo kỹ thuật viên, theo nhóm sự cố không: `Không đúng chuẩn Odoo`
- Có cần theo dõi SLA cho yêu cầu xử lý không: `Đúng chuẩn Odoo`
  Bằng chứng:
  `helpdesk.ticket` có các field `sla_ids`, `sla_deadline`, `sla_deadline_hours` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_ticket.py);
  policy SLA nằm ở model `helpdesk.sla` trong [helpdesk_sla.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_sla.py).
- Có cần báo cáo chênh lệch giữa kế hoạch và thực tế không: `Không đúng chuẩn Odoo`
- Có cần truy vết đầy đủ từ yêu cầu đến xuất kho, mua hàng, sửa chữa và nghiệm thu không: `Không đúng chuẩn Odoo`

### 17.13. Nhóm câu hỏi về dữ liệu hiện có và mức độ kế thừa

- Quy trình 0502 sẽ là triển khai mới bằng cách kế thừa các module chuẩn của Odoo: `Không đúng chuẩn Odoo`
- Có dữ liệu equipment, ticket, task, kho, vendor hoặc purchase order đang chạy thật không: `Không đúng chuẩn Odoo`
- 0502 sẽ được làm mới bằng cách kế thừa các module gốc của Odoo, hạn chế việc xây dựng model mới: `Không đúng chuẩn Odoo`
- Không có custom module nào ảnh hưởng các luồng này: `Không đúng chuẩn Odoo`
- Không có giới hạn hiện tại, nhưng sẽ hạn chế thay đổi flow chuẩn của Odoo: `Không đúng chuẩn Odoo`
- Ưu tiên kế thừa chuẩn Odoo, chỉ custom khi thiếu tính năng đó trong module gốc: `Không đúng chuẩn Odoo`

### 17.14. Nhóm câu hỏi chốt module trục chính

- `maintenance` là trục chính, `industry_fsm` là lớp thực thi, `helpdesk` là optional entry point: `Không đúng chuẩn Odoo`
- `maintenance` cover equipment, maintenance request, basic workflow nhưng thiếu FSM, stock, purchase: `Không đúng chuẩn Odoo`
- Nếu chọn `helpdesk`, không bắt buộc nối tiếp `helpdesk_fsm` hoặc `helpdesk_repair`: `Không đúng chuẩn Odoo`
- Có cần kết hợp `maintenance` để quản lý equipment và `industry_fsm` để thực thi công việc không: `Không đúng chuẩn Odoo`
- Có cần `planning` làm lớp hỗ trợ phân công hay phân công ngay trong FSM là đủ: `Không đúng chuẩn Odoo`
- Có cần `stock` và `purchase_stock` ngay từ phase 1 hay có thể triển khai sau: `Không đúng chuẩn Odoo`
- Có cần `stock_account`, `purchase_requisition` hoặc `planning_attendance` ngay từ đầu hay để phase sau: `Không đúng chuẩn Odoo`
