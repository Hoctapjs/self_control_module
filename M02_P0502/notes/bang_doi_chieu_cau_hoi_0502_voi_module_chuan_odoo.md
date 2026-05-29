# Bảng đối chiếu câu hỏi 0502 với module chuẩn Odoo

## 1. Mục đích

File này tổng hợp các câu hỏi và câu trả lời quan trọng trong quá trình chốt module kế thừa cho quy trình 0502, đối chiếu trực tiếp với module chuẩn Odoo.

Mỗi dòng gồm các cột:

- Câu hỏi
- Câu trả lời hiện tại
- Bước quy trình liên quan
- Đúng hoặc không đúng chuẩn Odoo
- Bằng chứng trong module chuẩn
- Nếu không đúng thì cần custom gì

## 2. Bảng đối chiếu

| Câu hỏi | Câu trả lời hiện tại | Bước | Đúng/Không đúng chuẩn Odoo | Bằng chứng trong module nào | Nếu không đúng thì cần custom gì |
|---|---|---|---|---|---|
| Nhu cầu xử lý của cửa hàng sẽ được ghi nhận theo dạng ticket hay theo dạng maintenance request? | Ghi nhận ticket và CMT kiểm tra rồi tạo Maintenance Request hoặc FSM Task | B1-B3 | Không đúng chuẩn Odoo | `helpdesk.ticket`, `maintenance.request`, `project.task` đều có thật, nhưng không có flow chuẩn tự động thống nhất ticket -> maintenance request hoặc ticket -> FSM task theo đúng logic 0502 trong một pipeline chung | Cần custom bridge flow giữa `helpdesk`, `maintenance`, `industry_fsm`; cần nút hoặc wizard điều hướng và đồng bộ trạng thái |
| Người dùng nghiệp vụ có quen làm việc theo ticket hay theo phiếu bảo trì thiết bị? | Quen làm theo ticket | B2 | Không đúng chuẩn Odoo | Đây là hiện trạng người dùng, không phải chức năng chuẩn của module | Không cần custom cho câu trả lời; chỉ là đầu vào workshop |
| Cửa hàng có cần một màn hình duy nhất để tạo yêu cầu hay có nhiều loại đầu vào khác nhau? | Cần 1 màn hình thôi | B2 | Không đúng chuẩn Odoo | Odoo chuẩn đang tách theo app như `helpdesk.ticket`, `maintenance.request`, `project.task`; không có một entry form chuẩn bao hết | Cần custom màn hình entry point và routing logic |
| Mọi yêu cầu 0502 đều xuất phát từ cửa hàng, hay có trường hợp hệ thống hoặc bộ phận khác chủ động tạo yêu cầu? | Nhiều nguồn tạo: hệ thống định kỳ, cửa hàng, CMT tạo tay | B1-B7 | Không đúng chuẩn Odoo | Các nguồn riêng lẻ đều có thể tồn tại, nhưng không có flow chuẩn hợp nhất chúng về một object đầu vào duy nhất | Cần custom cơ chế hợp nhất nguồn tạo và rule tạo record |
| Bảo trì định kỳ và bảo trì phát sinh có cần dùng chung một loại hồ sơ đầu vào hay phải tách riêng? | Dùng chung 1 loại hồ sơ đầu vào | B2-B6 | Không đúng chuẩn Odoo | `maintenance.request` có `maintenance_type`, nhưng nếu đầu vào là ticket chung cho mọi loại thì không có sẵn | Cần custom model đầu vào chung hoặc bridge giữa ticket và maintenance |
| Có yêu cầu giữ ticket để làm đầu mối trao đổi giữa cửa hàng và CMT không? | Có nên giữ | B2-B21 | Đúng chuẩn Odoo | `helpdesk.ticket` kế thừa `portal.mixin` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_ticket.py); portal hiển thị ở [helpdesk_portal_templates.xml](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/views/helpdesk_portal_templates.xml); chia sẻ qua [portal_share.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/wizard/portal_share.py) | Không cần custom nếu chỉ dùng ticket làm đầu mối giao tiếp |
| Ticket có là đối tượng theo dõi xuyên suốt toàn quy trình không? | Ticket là đối tượng theo dõi xuyên suốt | B2-B21 | Không đúng chuẩn Odoo | `helpdesk.ticket` có thật, nhưng Odoo chuẩn không có flow sẵn để ticket làm object trục chính xuyên suốt đồng thời bao hết maintenance, vật tư, mua hàng, nghiệm thu | Cần custom mô hình master flow hoặc liên kết chặt ticket với `maintenance.request`, `project.task`, `stock.picking`, `purchase.order` |
| Đối tượng trung tâm của quy trình là máy móc thiết bị hay là yêu cầu xử lý? | Đối tượng trung tâm là yêu cầu xử lý, nhưng vẫn có dữ liệu nền là máy móc thiết bị | B1-B21 | Đúng chuẩn Odoo | `maintenance.request` là request có `equipment_id`; `maintenance.equipment` là dữ liệu nền trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py) | Không cần custom nếu chỉ cần request + equipment cơ bản |
| Doanh nghiệp có cần quản lý danh mục equipment đầy đủ cho từng cửa hàng không? | Có | Master data, B1-B21 | Không đúng chuẩn Odoo | `maintenance.equipment` có sẵn trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py), nhưng chuẩn Odoo không có sẵn khái niệm “equipment theo cửa hàng” nếu cửa hàng là đối tượng riêng của dự án 0502 | Cần custom quan hệ equipment với store hoặc mô hình cửa hàng đang dùng trong dự án |
| Có cần lưu lịch sử bảo trì theo từng máy không? | Có | B4-B21 | Đúng chuẩn Odoo | `maintenance.equipment` có `maintenance_ids = fields.One2many('maintenance.request', 'equipment_id')` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py) | Không cần custom ở mức lịch sử maintenance cơ bản |
| Có cần theo dõi preventive maintenance và corrective maintenance tách biệt không? | Không cần tách model, dùng chung `maintenance.request` | B4-B6 | Đúng chuẩn Odoo | `maintenance.request` có field `maintenance_type = fields.Selection([('corrective', ...), ('preventive', ...)])` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py) | Không cần custom nếu chỉ cần phân loại bằng field |
| Có cần quản lý chu kỳ bảo trì định kỳ theo thiết bị không? | Có | B5-B6 | Đúng chuẩn Odoo | `maintenance.request` có `recurring_maintenance`, `repeat_interval`, `repeat_unit`, `repeat_type`, `repeat_until`, đồng thời gắn `equipment_id` trong [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py) | Không cần custom cho recurring cơ bản |
| Có cần quản lý tình trạng vận hành của từng máy trước và sau bảo trì không? | Có | B4-B21 | Không đúng chuẩn Odoo | Không tìm thấy field chuẩn tương ứng trước/sau bảo trì trên `maintenance.equipment` hoặc `maintenance.request` theo đúng semantics 0502 | Cần custom field trạng thái trước/sau |
| Có cần truy vết đầy đủ lịch sử hỏng hóc, thay vật tư, chi phí và nghiệm thu theo từng máy không? | Có | B4-B21 | Không đúng chuẩn Odoo | Không có object chuẩn nối full trace theo máy cho toàn chuỗi 0502 | Cần custom traceability layer |
| Sau khi tiếp nhận yêu cầu, công việc có cần được phân cho kỹ thuật viên dưới dạng task không? | Có | B3-B9, B20 | Đúng chuẩn Odoo | `helpdesk_fsm` có `fsm_task_ids = fields.One2many('project.task', 'helpdesk_ticket_id', ...)` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk_fsm/models/helpdesk_ticket.py) | Không cần custom nếu chấp nhận dùng task FSM để thực thi |
| Đội kỹ thuật có làm việc kiểu hiện trường như mô hình Field Service không? | Có | B9-B20 | Đúng chuẩn Odoo | `industry_fsm` mở rộng `project.task` với `is_fsm` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py) | Không cần custom để dùng FSM đúng nghĩa |
| Có cần theo dõi người thực hiện, thời gian bắt đầu, thời gian kết thúc và timesheet cho từng công việc không? | Có | B9-B20 | Đúng chuẩn Odoo | `industry_fsm.project.task` dùng `planned_date_begin`, `date_deadline`, `user_ids`; có `action_view_timesheets()` mở `account.analytic.line` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py) | Không cần custom cho theo dõi cơ bản |
| Có cần giao diện riêng cho kỹ thuật viên khi đi xử lý tại cửa hàng không? | Có | B20 | Đúng chuẩn Odoo | `industry_fsm` có các view chuyên biệt trong [fsm_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/views/fsm_views.xml) | Không cần custom nếu dùng giao diện FSM chuẩn |
| Có cần quản lý báo cáo thực hiện công việc ngay trên task hiện trường không? | Có | B10, B20, B21 | Đúng chuẩn Odoo | `industry_fsm` có report và worksheet trong manifest; `project.task` có `worksheet_signature`, `worksheet_signed_by`, các nút report trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py) | Có thể cần custom mẫu report nếu biểu mẫu đặc thù |
| Có cần phân tách rõ người tiếp nhận yêu cầu và người trực tiếp thực hiện sửa chữa không? | Có, và có thêm vai trò CMT Lead điều phối | B3, B7-B9, B20 | Không đúng chuẩn Odoo | Odoo có `user_id`, `user_ids`, `team_id`, `maintenance_team_id`, nhưng không có role chuẩn riêng tên CMT/CMT Lead theo đúng semantics 0502 | Cần custom role, security group, field vai trò và rule xử lý |
| Việc lập kế hoạch bảo trì có cần một lớp scheduling riêng hay chỉ cần phân công trực tiếp trên task? | Chỉ cần phân công trực tiếp trên task là đủ | B8-B9 | Không đúng chuẩn Odoo | Đây là quyết định solution, không phải chức năng có thật để xác nhận trong module chuẩn | Không cần custom nếu chấp nhận không dùng `planning`; nếu muốn rule điều phối riêng thì cần custom |
| Đội bảo trì có quy mô đủ lớn để cần dùng Planning không? | Chưa cần | B8-B9 | Không đúng chuẩn Odoo | Đây là quyết định phạm vi triển khai, không phải chức năng chuẩn | Không cần custom cho câu trả lời |
| Có cần lên lịch theo ca, theo ngày, theo giờ hoặc theo vùng phụ trách không? | Theo ngày và theo giờ là được | B8-B9 | Không đúng chuẩn Odoo | `planning.slot` hỗ trợ thời gian thật, nhưng câu trả lời là quyết định scope, không phải xác thực tính năng chuẩn | Nếu cần vùng phụ trách thì có thể cần custom thêm |
| Có cần tránh phân công người đang nghỉ phép không? | Có | B9 | Đúng chuẩn Odoo | `planning_holidays.models.planning_slot` có `leave_warning` và `_compute_leave_warning` trong [planning_slot.py](/d:/odoo-19.0+e.20250918/odoo/addons/planning_holidays/models/planning_slot.py) | Nếu không dùng `planning` mà vẫn muốn cảnh báo nghỉ phép trên FSM task thì cần custom |
| Có cần phân công theo kỹ năng kỹ thuật viên không? | Có nhưng chưa cần skill matrix phức tạp | B9 | Đúng chuẩn Odoo | `planning_hr_skills.models.planning_slot` có `employee_skill_ids` và lọc resource theo skill trong [planning_slot.py](/d:/odoo-19.0+e.20250918/odoo/addons/planning_hr_skills/models/planning_slot.py) | Nếu muốn áp skill trực tiếp trên FSM task thay vì planning slot thì cần custom |
| Có cần so sánh kế hoạch phân công với thời gian làm thực tế không? | Chưa cần | B9-B20 | Không đúng chuẩn Odoo | `planning_attendance` có thể làm việc này, nhưng câu trả lời là quyết định không dùng tính năng ở phase hiện tại | Không cần custom cho câu trả lời |
| Có cần theo dõi năng suất hoặc hiệu suất triển khai của đội bảo trì sau này không? | Chưa cần hiện tại | B10, B20 | Không đúng chuẩn Odoo | Đây là quyết định báo cáo/scope, không phải chức năng chuẩn được xác thực trực tiếp | Không cần custom cho câu trả lời |
| Trong quy trình sửa chữa có thường xuyên phát sinh vật tư không? | Có | B14-B20 | Không đúng chuẩn Odoo | Đây là nhận định nghiệp vụ, không phải phần có thật trong module chuẩn | Không cần custom để trả lời; nhưng nếu muốn quản lý vật tư theo flow 0502 thì cần thiết kế liên kết chuẩn |
| Vật tư phát sinh có bắt buộc phải đi qua quy trình yêu cầu xuất kho không? | Có | B15-B18 | Không đúng chuẩn Odoo | Odoo có `stock.picking`, `stock.move`, `stock.move.line`, nhưng không có sẵn “yêu cầu xuất kho” như một bước approval riêng cho 0502 | Cần custom object hoặc state approval trước khi sinh `stock.picking` |
| Vật tư sẽ được xuất trực tiếp từ kho trung tâm, kho cửa hàng hay nhiều loại kho khác nhau? | Gồm kho trung tâm và kho cửa hàng | B15-B18 | Không đúng chuẩn Odoo | `stock.warehouse` và `stock.location` có hỗ trợ nhiều kho, nhưng câu trả lời là thiết kế vận hành chứ không phải phần chuẩn cần xác thực | Nếu cần rule chọn kho theo store thì cần custom |
| Có cần theo dõi vật tư đã dùng theo từng yêu cầu, từng máy hoặc từng lần sửa chữa không? | Có | B18-B20 | Không đúng chuẩn Odoo | `stock.move` theo dõi theo chứng từ kho; liên kết trực tiếp đến request/máy/lần sửa chữa không có sẵn đồng bộ trong module chuẩn đang xét | Cần custom field liên kết và báo cáo truy vết |
| Có cần liên kết vật tư phát sinh trực tiếp với ticket, task hoặc maintenance request không? | Có | B14-B20 | Không đúng chuẩn Odoo | `industry_fsm_stock` gắn mạnh với task/sale line; `maintenance.request` chuẩn không có sẵn link vật tư trực tiếp | Cần custom liên kết vật tư với object trục chính |
| Có cần kiểm soát tồn kho trước khi phê duyệt sửa chữa không? | Có | B12, B16-B17 | Không đúng chuẩn Odoo | Odoo có tồn kho thật, nhưng không có chuẩn approval “phê duyệt sửa chữa” phụ thuộc tồn kho trong flow 0502 | Cần custom rule check tồn + approval |
| Có cần ghi nhận tiêu hao vật tư theo stock move chuẩn của Odoo không? | Có | B18-B20 | Đúng chuẩn Odoo | `stock.move` và `stock.move.line` là lõi của `stock`; xem [stock_move_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_move_line.py) và [stock_picking.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_picking.py) | Không cần custom nếu chỉ cần tiêu hao vật tư theo chứng từ kho |
| Đội kho hoặc kỹ thuật viên có dùng barcode scanner để xuất vật tư không? | Chưa cần ở hiện tại, mở rộng sau | B18 | Không đúng chuẩn Odoo | Đây là quyết định rollout, không phải phần chuẩn để xác thực | Không cần custom cho câu trả lời |
| Có cần quản lý lot hoặc serial cho vật tư thay thế không? | Nếu vật tư có bảo hành thì cần | B16-B18 | Đúng chuẩn Odoo | `product.product` có field `tracking` trong [product_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/stock/views/product_views.xml); `stock.move.line` có `lot_id`, `tracking` trong [stock_move_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock/models/stock_move_line.py) | Không cần custom cho lot/serial chuẩn |
| Khi thiếu vật tư, doanh nghiệp có luôn tạo purchase order hay còn bước trung gian phê duyệt nội bộ? | Có bước phê duyệt nội bộ trước khi tạo PO | B19 | Không đúng chuẩn Odoo | `purchase.order` có chuẩn RFQ/PO, nhưng “bước phê duyệt nội bộ trước khi tạo PO” theo 0502 không có sẵn trong flow đã nêu | Cần custom approval step hoặc dùng approval app ngoài phạm vi hiện tại |
| Vật tư mua ngoài có bắt buộc nhập kho trước rồi mới xuất cho sửa chữa không? | Có | B19-B20 | Đúng chuẩn Odoo | `purchase_stock` nối `purchase.order.line` với `stock.move` qua `move_ids`, `purchase_line_id` trong [purchase_order_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase_stock/models/purchase_order_line.py) | Không cần custom nếu đi theo nhập kho rồi xuất dùng |
| Có trường hợp mua trực tiếp để dùng ngay mà không qua kho không? | Chưa cần hiện tại | B19 | Không đúng chuẩn Odoo | Đây là quyết định nghiệp vụ/scope, không phải tính năng chuẩn cần chứng minh | Không cần custom cho câu trả lời |
| Doanh nghiệp có cần quản lý nhiều báo giá từ nhiều nhà cung cấp không? | Chưa cần hiện tại | B19 | Không đúng chuẩn Odoo | Đây là quyết định có dùng `purchase_requisition` hay không, không phải xác thực tính năng chuẩn | Không cần custom cho câu trả lời |
| Có cần call for tender hoặc blanket order không? | Chưa cần hiện tại | B19 | Không đúng chuẩn Odoo | `purchase_requisition` có thật, nhưng câu trả lời là quyết định không dùng | Không cần custom cho câu trả lời |
| Có cần liên kết vật tư mua ngoài trực tiếp với yêu cầu sửa chữa hay repair order không? | Có | B19-B20 | Không đúng chuẩn Odoo | `purchase.order` và `purchase.order.line` không có sẵn liên kết trực tiếp tới `maintenance.request` hoặc FSM task trong module chuẩn đang dùng | Cần custom field liên kết hoặc smart button giữa PO và request/task |
| Có cần kiểm soát lead time mua hàng để ảnh hưởng vào timeline xử lý không? | Có expected delivery date | B12, B19, B20 | Đúng chuẩn Odoo | `purchase.order` có `date_planned` trong [purchase_order.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase/models/purchase_order.py); `purchase.order.line` có `date_planned` trong [purchase_order_line.py](/d:/odoo-19.0+e.20250918/odoo/addons/purchase/models/purchase_order_line.py) | Không cần custom để giữ expected arrival |
| Outside service là một quy trình độc lập hoàn toàn hay chỉ là một nhánh phụ của 0502? | Cần thêm thông tin | B13 | Chưa đủ thông tin để kết luận | Chưa có câu trả lời rõ để đối chiếu module chuẩn | Cần làm rõ nghiệp vụ trước |
| Khi chuyển outside service, đối tượng nào sẽ được chuyển tiếp: ticket, maintenance request hay task? | Cần thêm thông tin | B13 | Chưa đủ thông tin để kết luận | Chưa có câu trả lời rõ để đối chiếu module chuẩn | Cần làm rõ nghiệp vụ trước |
| Có cần theo dõi nhà cung cấp dịch vụ ngoài như vendor không? | Cần thêm thông tin | B13 | Chưa đủ thông tin để kết luận | Chưa có câu trả lời rõ để đối chiếu module chuẩn | Cần làm rõ nghiệp vụ trước |
| Có cần quản lý báo giá dịch vụ ngoài, timeline dịch vụ ngoài và nghiệm thu dịch vụ ngoài không? | Cần thêm thông tin | B13, B21 | Chưa đủ thông tin để kết luận | Chưa có câu trả lời rõ để đối chiếu module chuẩn | Cần làm rõ nghiệp vụ trước |
| Có cần tích hợp chi phí outside service vào tổng chi phí xử lý của yêu cầu 0502 không? | Có | B13, B21 | Không đúng chuẩn Odoo | Không tìm thấy chuẩn sẵn để rollup chi phí dịch vụ ngoài vào request 0502 tổng hợp | Cần custom cost aggregation |
| Có cần phân biệt rõ giữa mua vật tư ngoài và thuê dịch vụ ngoài không? | Có | B13-B19 | Không đúng chuẩn Odoo | Đây là quyết định phân loại nghiệp vụ, không phải phần chuẩn có sẵn trong module được đối chiếu | Có thể cần custom taxonomy/field loại chi phí hoặc loại xử lý |
| Quy trình sửa chữa có cần dùng app Repair chuẩn của Odoo không? | Ưu tiên Maintenance + Field Service, không cần Repair cho toàn bộ | B20 | Không đúng chuẩn Odoo | Đây là quyết định solution chứ không phải phần có thật để xác nhận trực tiếp trong module chuẩn | Không cần custom cho câu trả lời; nhưng nếu muốn bỏ hẳn Repair thì cần chốt kiến trúc rõ |
| Có cần tạo repair order chính thức cho từng trường hợp sửa chữa không? | Dùng Maintenance Request -> FSM Task là đủ | B20 | Không đúng chuẩn Odoo | Odoo có `maintenance.request` và FSM task riêng, nhưng không có flow chuẩn xác nhận “đủ thay cho repair order” | Nếu muốn dùng MR + FSM làm flow chính thì cần custom logic bao phủ phần repair cần thiết |
| Có cần liên kết yêu cầu bảo trì với repair order để theo dõi tiến độ không? | Tiến độ theo Ticket, FSM Task, Maintenance Request | B3-B21 | Không đúng chuẩn Odoo | Đây là thiết kế theo 3 object; module chuẩn không có tiến độ hợp nhất kiểu này | Cần custom state sync và tracking layer |
| Có cần kết nối repair với mua hàng khi thiếu vật tư không? | Không, flow đúng là Maintenance/FSM -> Stock -> Purchase | B15-B19 | Không đúng chuẩn Odoo | Đây là quyết định solution, không phải bằng chứng trực tiếp trong module chuẩn | Không cần custom cho câu trả lời |
| Có cần giữ toàn bộ flow sửa chữa trong maintenance hoặc FSM thay vì dùng Repair không? | Có | B20 | Không đúng chuẩn Odoo | Đây là kết luận kiến trúc | Cần custom bridge để bao phủ thiếu hụt của Repair |
| Tiêu chí nào để quyết định trường hợp nào đi theo repair flow và trường hợp nào chỉ là maintenance work thông thường? | Không cần Repair nếu công việc đơn giản tại cửa hàng | B20 | Không đúng chuẩn Odoo | Đây là rule nghiệp vụ dự án, không phải phần chuẩn | Cần custom rule hoặc guideline vận hành |
| Có cần theo dõi chi phí sửa chữa theo từng yêu cầu không? | Mỗi request/task phải có tổng chi phí | B11-B12, B20-B21 | Không đúng chuẩn Odoo | Không có field cost rollup chuẩn tương ứng trên `maintenance.request`/FSM task cho bài toán 0502 | Cần custom tổng hợp cost |
| Có cần tách chi phí nhân công, vật tư, dịch vụ ngoài và chi phí khác không? | Có | B11-B12, B13, B18-B21 | Không đúng chuẩn Odoo | Không có cost structure chuẩn 0502 trên request/task | Cần custom cost breakdown |
| Có cần ghi nhận giá trị vật tư xuất dùng vào kế toán kho không? | Có | B18-B20 | Đúng chuẩn Odoo | `stock_account.models.stock_move` có `account_move_id` và `_create_account_move()` trong [stock_move.py](/d:/odoo-19.0+e.20250918/odoo/addons/stock_account/models/stock_move.py) | Cần cài `stock_account` và cấu hình valuation đúng |
| Có cần tính cost thực tế để so sánh với cost được duyệt ban đầu không? | Có | B12, B20-B21 | Không đúng chuẩn Odoo | Không có chuẩn so sánh approved cost vs actual cost trên object 0502 | Cần custom approved budget/cost variance |
| Có cần invoice hoặc billing cho cửa hàng nội bộ hoặc đơn vị liên quan không? | Chưa cần ở hiện tại | B21 | Không đúng chuẩn Odoo | Đây là quyết định scope, không phải phần chuẩn cần xác thực | Không cần custom cho câu trả lời |
| Có cần sử dụng module `stock_account` hay logic kế toán kho chỉ là yêu cầu báo cáo? | Chưa cần hiện tại | B18-B20 | Không đúng chuẩn Odoo | Đây là quyết định phase/solution, không phải tính năng chuẩn để xác thực “đúng chuẩn” | Không cần custom; chỉ là quyết định có dùng hay chưa |
| Nếu triển khai FSM, có cần ghi nhận timesheet mang tính costing hoặc billing không? | Có ở mức costing | B20-B21 | Không đúng chuẩn Odoo | `industry_fsm` có timesheet thật, nhưng câu trả lời “ở mức costing” là cách triển khai, không phải phần chuẩn xác nhận trực tiếp trong module đang đối chiếu | Nếu muốn costing riêng theo 0502 thì cần custom báo cáo hoặc cost aggregation |
| Có cần checklist kiểm tra theo từng loại máy không? | Có | B4, B11, B21 | Đúng chuẩn Odoo | `maintenance_worksheet.models.maintenance_request` có `worksheet_template_id` trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/models/maintenance_request.py) | Có thể cần custom template nếu checklist rất đặc thù |
| Có cần mẫu biên bản sửa chữa hoặc bảo trì chuẩn không? | Có | B11, B20, B21 | Đúng chuẩn Odoo | `maintenance_worksheet` gắn `worksheet.template` với `maintenance.request` trong [maintenance_worksheet_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/views/maintenance_worksheet_views.xml) | Có thể cần custom nội dung mẫu |
| Có cần mẫu nghiệm thu sau bảo trì không? | Có | B21 | Đúng chuẩn Odoo | `maintenance_worksheet` có report `maintenance_custom_report.xml` và `maintenance_custom_report_templates.xml` trong manifest | Có thể cần custom form nghiệm thu riêng |
| Có cần kỹ thuật viên điền biểu mẫu trên hệ thống trong lúc làm việc không? | Có | B11, B20 | Đúng chuẩn Odoo | `maintenance_worksheet.models.maintenance_request` có `action_maintenance_worksheet()` trong [maintenance_request.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance_worksheet/models/maintenance_request.py) | Không cần custom nếu form chuẩn đáp ứng |
| Có cần in biểu mẫu hoặc xuất PDF cho cửa hàng ký xác nhận không? | Có | B21 | Đúng chuẩn Odoo | `maintenance_worksheet` có report trong manifest; `industry_fsm` cũng có worksheet report trong manifest | Có thể cần custom bố cục PDF |
| Có cần ảnh hiện trường trước và sau sửa chữa không? | Có | B4, B20, B21 | Không đúng chuẩn Odoo | Không tìm thấy phần chuẩn rõ ràng trong các module đã đối chiếu cho logic ảnh trước/sau theo 0502 | Cần custom attachment flow hoặc media section |
| Có cần chữ ký điện tử hoặc xác nhận trực tiếp trên thiết bị không? | Có | B21 | Đúng chuẩn Odoo | `industry_fsm.models.project_task` có `worksheet_signature` và `worksheet_signed_by` trong [project_task.py](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm/models/project_task.py) | Không cần custom nếu dùng chữ ký trên worksheet FSM |
| Những vai trò nào sẽ tham gia chính thức trong hệ thống? | Cửa hàng, CMT, CMT Lead, kho, mua hàng, kế toán | Toàn quy trình | Không đúng chuẩn Odoo | Đây là mapping tổ chức nội bộ sang role hệ thống, không phải phần chuẩn sẵn theo tên đó trong Odoo | Cần custom security groups/role mapping |
| Cửa hàng có được theo dõi trạng thái xử lý trực tiếp trên hệ thống không? | Có, qua ticket hoặc portal view | B2-B21 | Đúng chuẩn Odoo | Portal ticket có trong [helpdesk_portal_templates.xml](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/views/helpdesk_portal_templates.xml) | Không cần custom nếu theo dõi qua ticket portal |
| CMT có được tạo hoặc chỉnh sửa phương án, báo giá và yêu cầu vật tư không? | Có | B11, B15 | Không đúng chuẩn Odoo | Không có role/fn chuẩn tên CMT với các hành vi này trên object 0502 | Cần custom security + field + action |
| CMT Lead có vai trò phê duyệt nào trong hệ thống? | Có, phê duyệt vật tư, kiểm soát kế hoạch, điều phối | B8-B9, B17 | Không đúng chuẩn Odoo | Không có role chuẩn CMT Lead và approval chuẩn đúng ngữ cảnh 0502 | Cần custom approval matrix |
| Bộ phận kho có cần thao tác trực tiếp trên yêu cầu 0502 hay chỉ làm trên chứng từ kho? | Chỉ làm trên chứng từ kho | B18 | Không đúng chuẩn Odoo | Đây là lựa chọn tổ chức nghiệp vụ, không phải phần chuẩn có thể xác thực trực tiếp | Nếu muốn ép đúng vai trò này trong hệ thống thì cần rule/phân quyền riêng |
| Bộ phận mua hàng có cần thấy liên kết giữa PO và yêu cầu sửa chữa không? | Có | B19 | Không đúng chuẩn Odoo | `purchase.order` không có link chuẩn đến request 0502 | Cần custom smart button / relation field |
| Có cần phân quyền theo cửa hàng, theo khu vực hay theo đội kỹ thuật không? | Có | Toàn quy trình | Không đúng chuẩn Odoo | Odoo có record rule chung, nhưng rule riêng theo store/team của 0502 chưa có sẵn | Cần custom record rules |
| Những KPI nào là bắt buộc: lead time, tỷ lệ đúng hạn, chi phí, hỏng lặp lại, tiêu hao vật tư? | Có | B10, B21 | Không đúng chuẩn Odoo | KPI tổng hợp kiểu 0502 chưa có sẵn thành một dashboard chuẩn | Cần custom reporting |
| Có cần dashboard riêng cho CMT Lead không? | Có | B10, B21 | Không đúng chuẩn Odoo | Không có dashboard chuẩn cho vai trò CMT Lead | Cần custom dashboard |
| Có cần báo cáo theo cửa hàng, theo máy, theo kỹ thuật viên, theo nhóm sự cố không? | Có | B10, B21 | Không đúng chuẩn Odoo | Báo cáo lõi rời rạc có thể có, nhưng combo báo cáo 0502 theo 4 chiều này chưa có sẵn thành chuẩn | Cần custom report views |
| Có cần theo dõi SLA cho yêu cầu xử lý không? | Có | B2-B12 | Đúng chuẩn Odoo | `helpdesk.ticket` có `sla_ids`, `sla_deadline`, `sla_deadline_hours` trong [helpdesk_ticket.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_ticket.py); policy ở `helpdesk.sla` trong [helpdesk_sla.py](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk/models/helpdesk_sla.py) | Nếu muốn SLA cho `maintenance.request` hoặc FSM task thì cần custom |
| Có cần báo cáo chênh lệch giữa kế hoạch và thực tế không? | Có | B10, B21 | Không đúng chuẩn Odoo | Không có report chuẩn variance cho timeline/cost 0502 | Cần custom variance reports |
| Có cần truy vết đầy đủ từ yêu cầu đến xuất kho, mua hàng, sửa chữa và nghiệm thu không? | Có | B2-B21 | Không đúng chuẩn Odoo | Không có object chuẩn nào đã nối full chain này sẵn | Cần custom master traceability layer |
| 0502 sẽ là triển khai mới bằng cách kế thừa các module chuẩn của Odoo | Có | Toàn dự án | Không đúng chuẩn Odoo | Đây là quyết định dự án, không phải phần chức năng chuẩn | Không cần custom cho câu trả lời; chỉ là nguyên tắc solution |
| Có dữ liệu equipment, ticket, task, kho, vendor hoặc purchase order đang chạy thật không? | Mới hoàn toàn, chưa có dữ liệu | Toàn dự án | Không đúng chuẩn Odoo | Đây là hiện trạng dự án, không phải chức năng chuẩn | Không cần custom cho câu trả lời |
| Có quy trình nào đang vận hành dở mà 0502 phải kế thừa thay vì làm mới không? | Không, làm mới và kế thừa tối đa module gốc | Toàn dự án | Không đúng chuẩn Odoo | Đây là quyết định triển khai | Không cần custom cho câu trả lời |
| Có custom module nào hiện tại đã chạm vào các luồng maintenance, helpdesk, stock hoặc purchase không? | Không có | Toàn dự án | Không đúng chuẩn Odoo | Đây là hiện trạng codebase, không phải chức năng chuẩn | Không cần custom cho câu trả lời |
| Có giới hạn nào về việc không được thay đổi flow chuẩn của một số module đang chạy production không? | Không có giới hạn hiện tại nhưng sẽ hạn chế thay đổi flow chuẩn | Toàn dự án | Không đúng chuẩn Odoo | Đây là nguyên tắc triển khai nội bộ | Không cần custom cho câu trả lời |
| Đội triển khai muốn tối đa kế thừa chuẩn Odoo hay chấp nhận custom mạnh để bám quy trình hiện tại? | Ưu tiên kế thừa chuẩn Odoo | Toàn dự án | Không đúng chuẩn Odoo | Đây là chiến lược solution | Không cần custom cho câu trả lời |
| Trục chính nên là `maintenance`, `helpdesk` hay `industry_fsm`? | `maintenance` là trục chính, `industry_fsm` là lớp thực thi, `helpdesk` là optional | Toàn quy trình | Không đúng chuẩn Odoo | Đây là kết luận kiến trúc, không phải phần có thật trong một module chuẩn cụ thể | Không cần custom cho câu trả lời; nhưng khi triển khai sẽ cần custom bridge giữa các app |
| Nếu chọn `maintenance`, có đủ để bao phủ bước tiếp nhận, xử lý, vật tư và nghiệm thu không? | Không đủ hoàn toàn | Toàn quy trình | Không đúng chuẩn Odoo | Đây là đánh giá solution, không phải chức năng chuẩn để xác nhận trực tiếp | Không cần custom cho câu trả lời |
| Nếu chọn `helpdesk`, có cần nối tiếp sang `helpdesk_fsm` hoặc `helpdesk_repair` không? | Không bắt buộc | Toàn quy trình | Không đúng chuẩn Odoo | Đây là quyết định kiến trúc triển khai | Không cần custom cho câu trả lời |
| Có cần kết hợp `maintenance` để quản lý equipment và `industry_fsm` để thực thi công việc không? | Có | Toàn quy trình | Không đúng chuẩn Odoo | Đây là định hướng thiết kế tổng thể | Nếu chốt hướng này thì cần custom liên kết giữa `maintenance.request` và `project.task` FSM |
| Có cần `planning` làm lớp hỗ trợ phân công hay phân công ngay trong FSM là đủ? | Triển khai trước FSM là vừa đủ, planning để sau nếu cần | B8-B9 | Không đúng chuẩn Odoo | Đây là quyết định phase và solution | Không cần custom cho câu trả lời |
| Có cần `stock` và `purchase_stock` ngay từ phase 1 hay có thể triển khai sau? | Có, cần ngay từ đầu | B15-B20 | Không đúng chuẩn Odoo | Đây là quyết định phase triển khai, không phải phần chức năng chuẩn | Không cần custom cho câu trả lời |
| Có cần `stock_account`, `purchase_requisition` hoặc `planning_attendance` ngay từ đầu hay để phase sau? | Chưa cần ngay từ đầu, có thể để phase sau | B10, B18-B20 | Không đúng chuẩn Odoo | Đây là quyết định roadmap, không phải tính năng chuẩn | Không cần custom cho câu trả lời |

## 3. Kết luận nhanh

Các nhóm câu trả lời hiện giữ được nhãn `Đúng chuẩn Odoo` theo tiêu chí chặt chủ yếu rơi vào:

- Các đối tượng và field có thật trong `maintenance`
- Các flow task thực địa có thật trong `industry_fsm`
- Các liên kết ticket với FSM có thật trong `helpdesk_fsm`
- Các chứng từ và tracking vật tư có thật trong `stock`
- Các ngày nhận hàng dự kiến và liên kết PO với receipt có thật trong `purchase` và `purchase_stock`
- Các worksheet, report, chữ ký có thật trong `maintenance_worksheet` và `industry_fsm`
- Các chức năng portal và SLA có thật trong `helpdesk`

Các câu còn lại bị đánh `Không đúng chuẩn Odoo` không phải vì nghiệp vụ sai, mà vì:

- đó là quyết định kiến trúc hoặc phase triển khai
- hoặc Odoo chuẩn chưa có sẵn đúng flow như câu trả lời đang mô tả
- hoặc cần bridge, state, approval, dashboard, truy vết và báo cáo riêng cho 0502

## 4. Đánh giá 21 bước của quy trình nếu chỉ dùng phần chuẩn Odoo

Nguyên tắc đánh giá:

- `Pass với chuẩn Odoo`: bước đó có thể chạy ở mức chấp nhận được nếu chỉ dùng phần chuẩn Odoo đã xác nhận trong bảng và chưa làm phần custom.
- `Không pass với chuẩn Odoo`: bước đó phụ thuộc vào ít nhất một phần `Không đúng chuẩn Odoo` mang tính bắt buộc để bước vận hành đúng theo flow 0502.

| Bước | Mô tả ngắn | Có thể pass chỉ với chuẩn Odoo không? | Lý do |
|---|---|---|---|
| B1 | Cửa hàng phát sinh nhu cầu bảo trì, sửa chữa | Không pass với chuẩn Odoo | Đây là phát sinh nghiệp vụ, nhưng chưa có object đầu vào chuẩn chung cho mọi nguồn theo thiết kế 0502 |
| B2 | Tạo phiếu yêu cầu bảo trì / raise ticket | Pass với chuẩn Odoo | Có thể dùng `helpdesk.ticket` làm đầu vào chuẩn |
| B3 | CMT tiếp nhận yêu cầu bảo trì | Pass với chuẩn Odoo | Có thể tiếp nhận trên ticket hoặc maintenance request ở mức chuẩn |
| B4 | Kiểm tra thực tế tình trạng | Pass với chuẩn Odoo | Có thể dùng `maintenance.request`, FSM task và worksheet chuẩn để ghi nhận kiểm tra ở mức cơ bản |
| B5 | Hệ thống tự động kiểm tra lịch bảo trì máy móc | Pass với chuẩn Odoo | `maintenance.request` có recurring maintenance chuẩn |
| B6 | Gửi lịch bảo trì cho CMT Lead | Không pass với chuẩn Odoo | Không có role CMT Lead và flow gửi lịch riêng đúng semantics 0502 trong chuẩn đang đối chiếu |
| B7 | CMT Lead tiếp nhận lịch và tổng hợp yêu cầu | Không pass với chuẩn Odoo | Thiếu role, quyền và dashboard tổng hợp riêng cho CMT Lead |
| B8 | Lập kế hoạch bảo trì máy móc | Pass với chuẩn Odoo | Có thể lập ở mức cơ bản trên maintenance/FSM/planning, dù chưa phải flow 0502 hoàn chỉnh |
| B9 | Điều phối nhân viên bảo trì | Pass với chuẩn Odoo | FSM và Planning có phần phân công chuẩn, dù role nội bộ chưa đúng hẳn 0502 |
| B10 | Xuất báo cáo theo dõi tình trạng | Không pass với chuẩn Odoo | Báo cáo 0502 tổng hợp theo CMT Lead / cửa hàng / thiết bị chưa có sẵn |
| B11 | CMT kiểm tra thực tế và đề xuất phương án xử lý hoặc báo giá | Không pass với chuẩn Odoo | Thiếu object/phần chuẩn cho đề xuất phương án, báo giá nội bộ theo 0502 |
| B12 | Cửa hàng duyệt timeline, cost | Không pass với chuẩn Odoo | Thiếu flow duyệt timeline/cost của store trên object 0502 |
| B13 | Outside service hoặc mua ngoài theo nhánh xử lý | Không pass với chuẩn Odoo | Outside service chưa đủ thông tin và chưa có flow chuẩn được xác nhận |
| B14 | Kiểm tra vật tư phát sinh | Không pass với chuẩn Odoo | Thiếu liên kết chuẩn giữa xử lý kỹ thuật và quyết định vật tư phát sinh theo 0502 |
| B15 | CMT yêu cầu xuất kho | Không pass với chuẩn Odoo | Odoo chuẩn không có “yêu cầu xuất kho” như bước approval riêng |
| B16 | Kiểm tra tồn kho vật tư | Pass với chuẩn Odoo | `stock` có tồn kho, lot/serial, kho, vị trí kho chuẩn |
| B17 | CMT Lead duyệt yêu cầu | Không pass với chuẩn Odoo | Thiếu role CMT Lead và approval matrix chuẩn |
| B18 | Thực hiện xuất kho | Pass với chuẩn Odoo | `stock.picking`, `stock.move`, `stock.move.line` đáp ứng chuẩn |
| B19 | Mua ngoài nếu tồn kho không đủ | Pass với chuẩn Odoo | `purchase` + `purchase_stock` đáp ứng mua hàng và nhập kho chuẩn |
| B20 | CMT tiến hành sửa chữa máy móc | Pass với chuẩn Odoo | `industry_fsm` và `maintenance` có thể hỗ trợ thực thi sửa chữa ở mức chuẩn |
| B21 | Cửa hàng nghiệm thu và đánh giá sau bảo trì | Không pass với chuẩn Odoo | Có worksheet/report/chữ ký chuẩn, nhưng thiếu flow nghiệm thu hoàn chỉnh của cửa hàng gắn với object 0502 và trace end-to-end |

## 5. Kết luận cho 21 bước

Nếu chỉ dùng phần chuẩn Odoo và chưa làm phần `Không đúng chuẩn Odoo`, các bước có thể đi được ở mức tương đối là:

- B2
- B3
- B4
- B5
- B8
- B9
- B16
- B18
- B19
- B20

Các bước còn lại sẽ bị chặn hoặc chỉ làm được rất hẹp, vì phụ thuộc vào các phần cần custom của 0502, đặc biệt là:

- entry flow hợp nhất
- vai trò CMT và CMT Lead
- approval cho timeline, cost, vật tư
- traceability end-to-end
- báo cáo 0502
- nghiệm thu cửa hàng theo đúng flow
