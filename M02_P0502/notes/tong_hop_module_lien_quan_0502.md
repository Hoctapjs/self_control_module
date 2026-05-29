# Tổng hợp module liên quan đến quy trình 0502

## 1. Phạm vi ghi chú

File này tổng hợp những thông tin đã tìm hiểu từ manifest của các nhóm module liên quan đến bài toán 0502 bảo trì và sửa chữa máy móc tại cửa hàng, bao gồm:

- `helpdesk*`
- `maintenance*`
- `industry_fsm*`
- `planning*`
- `stock*`
- `purchase*`

Mục tiêu của note là:

- Ghi lại cách hiểu nhanh vai trò của từng nhóm module.
- Xác định module lõi và module mở rộng.
- Chỉ ra các module phù hợp nhất để triển khai quy trình 0502.

## 2. Nhóm module Helpdesk

Mình đã đọc manifest của nhóm `helpdesk*` trong `odoo/addons`, và có thể chia như này:

- `helpdesk` là lõi.
- `helpdesk_*` thường là module mở rộng theo domain.
- Những module có `auto_install=True` như `helpdesk_fsm`, `helpdesk_sale`, `helpdesk_sms`, `helpdesk_stock_account` thường là module bridge, không phải app độc lập.

### 2.1. Các module đáng chú ý

- `helpdesk`: tiếp nhận ticket và yêu cầu.
- `helpdesk_fsm`: nếu muốn đẩy ticket thành công việc kỹ thuật hiện trường.
- `helpdesk_stock`: nếu ticket kéo theo vật tư, trả hàng hoặc xuất kho.
- `helpdesk_repair`: nếu đi theo luồng repair chuẩn.

### 2.2. Cách hiểu trong bối cảnh 0502

Với bài toán 0502 bảo trì và sửa chữa máy móc, nhóm đáng quan tâm nhất thường là:

- `helpdesk`: tiếp nhận ticket hoặc yêu cầu từ cửa hàng.
- `helpdesk_fsm`: hỗ trợ chuyển ticket thành công việc thực địa cho kỹ thuật viên.
- `helpdesk_stock`: bám theo nhu cầu vật tư ngay từ ticket.
- `helpdesk_repair`: hỗ trợ nếu cần đi theo repair flow chuẩn của Odoo.

## 3. Nhóm module Maintenance

`maintenance` là module gốc để quản lý thiết bị và yêu cầu bảo trì. Manifest của nó ghi rất rõ: quản lý thiết bị và yêu cầu bảo trì, chỉ phụ thuộc `mail`, nên đây là app nền cho bài toán bảo trì.

Nói đơn giản, nếu cần:

- danh mục máy móc hoặc equipment
- yêu cầu bảo trì
- bảo trì định kỳ, corrective, preventive
- theo dõi tình trạng và lịch sử bảo trì

thì nên bắt đầu từ `maintenance`.

### 3.1. Module mở rộng

`maintenance_worksheet` là module mở rộng của `maintenance`, dùng để tạo biểu mẫu hoặc worksheet cho kỹ thuật viên ghi nhận khi đi bảo trì. Nó phụ thuộc `maintenance` và `worksheet`, nên không phải module lõi độc lập.

Module này phù hợp khi muốn:

- kỹ thuật viên điền checklist hoặc biên bản bảo trì
- có mẫu form theo loại máy hoặc loại công việc
- in hoặc xuất report bảo trì có cấu trúc

### 3.2. Cách hiểu trong bối cảnh 0502

- `maintenance`: quản lý yêu cầu bảo trì và thiết bị là chính
- `maintenance_worksheet`: bổ sung phần phiếu công tác, biên bản kiểm tra, checklist và nghiệm thu kỹ thuật

Nếu chỉ cần chạy quy trình bảo trì cơ bản thì `maintenance` là đủ để khảo sát trước. Nếu muốn số hóa bước kiểm tra hiện trạng, checklist sửa chữa, nghiệm thu chi tiết thì nên đào sâu thêm `maintenance_worksheet`.

## 4. Nhóm module Field Service

Ba module này là một chuỗi mở rộng theo tầng, đọc từ manifest thì vai trò khá rõ:

- `industry_fsm`: module lõi Field Service. Nó phục vụ điều phối và theo dõi công việc kỹ thuật hiện trường, dựa trên task và timesheet, có lịch, technician, báo cáo, vật tư trên task và giao diện riêng cho đội onsite.
- `industry_fsm_sale`: mở rộng FSM sang bán hàng, tức là thời gian làm việc và vật tư phát sinh trên task có thể đi vào sale order hoặc invoicing.
- `industry_fsm_stock`: mở rộng tiếp từ FSM Sale sang kho, để xử lý stock move cho vật tư hoặc sản phẩm dùng trong công việc Field Service.

### 4.1. Cách hiểu ngắn gọn theo tầng nghiệp vụ

- `industry_fsm` = điều phối người đi làm việc ngoài hiện trường
- `industry_fsm_sale` = công việc hiện trường có tính phí theo giờ công hoặc vật tư
- `industry_fsm_stock` = công việc hiện trường có tiêu hao hoặc xuất vật tư từ kho

### 4.2. Map vào quy trình 0502

- Nếu chỉ cần lập kế hoạch, phân công kỹ thuật viên, theo dõi sửa chữa hoặc bảo trì tại cửa hàng: bắt đầu từ `industry_fsm`.
- Nếu sau sửa chữa cần kiểm soát chi phí để ghi nhận hoặc billing theo giờ công hay vật tư: xem thêm `industry_fsm_sale`.
- Nếu quy trình có bước xuất kho vật tư cho sửa chữa và muốn bám chứng từ kho: `industry_fsm_stock` là phần liên quan trực tiếp nhất.

### 4.3. Cách nhìn thực tế cho 0502

- `maintenance` mạnh về quản lý thiết bị và maintenance request.
- `industry_fsm` mạnh về thực thi công việc ngoài hiện trường.
- `industry_fsm_stock` mạnh ở đoạn có vật tư phát sinh, kiểm tra tồn kho và xuất kho để sửa chữa.

## 5. Nhóm module Planning

Nhóm `planning*` đi theo mô hình một module lõi cộng với các module tích hợp mở rộng.

- `planning`: module gốc để lập lịch hoặc ca làm việc cho nhân sự. Đây là nơi quản lý slot, ca và phân công người theo thời gian.
- `planning_attendance`: nối `planning` với `hr_attendance` để so sánh giờ được phân công với giờ chấm công thực tế.
- `planning_holidays`: nối `planning` với nghỉ phép để lịch phân công phản ánh tình trạng nghỉ.
- `planning_hr_skills`: nối `planning` với kỹ năng nhân sự để tìm và phân công người theo skill.

### 5.1. Hiểu ngắn gọn theo nghiệp vụ

- `planning` = phân ca hoặc điều phối lịch làm việc
- `planning_attendance` = đối chiếu kế hoạch với thực tế đi làm
- `planning_holidays` = tránh phân công trùng người đang nghỉ
- `planning_hr_skills` = phân công đúng người có kỹ năng phù hợp

### 5.2. Map vào 0502

Nhóm này không phải trục chính quản lý bảo trì, mà là nhóm hỗ trợ mạnh cho:

- Bước 8: lập kế hoạch bảo trì máy móc
- Bước 9: điều phối nhân viên bảo trì

Nếu bài toán cần:

- lên lịch kỹ thuật viên theo ngày hoặc ca
- tránh phân người đang nghỉ
- chọn người có skill đúng loại máy
- so sánh kế hoạch với thời gian làm thực tế

thì `planning` cộng `planning_holidays` cộng `planning_hr_skills` là rất phù hợp. `planning_attendance` hữu ích khi muốn kiểm soát vận hành và hiệu suất sau này.

### 5.3. Cách nhìn thực tế cho 0502

- `maintenance` hoặc `helpdesk` hoặc `industry_fsm` thường là nơi phát sinh và quản lý yêu cầu
- `planning` là nơi hỗ trợ điều phối nhân sự cho việc thực hiện
- `planning` không thay thế `maintenance` hay `industry_fsm`, mà bổ sung cho phần scheduling

## 6. Nhóm module Stock

Nhóm `stock*` nhiều vì `stock` là module lõi kho, còn các module còn lại chủ yếu là phần mở rộng theo từng bài toán.

### 6.1. Các module chính

- `stock`: module gốc Inventory hoặc Warehouse. Đây là nền cho tồn kho, vị trí kho, picking, move, lot hoặc serial, replenishment, xuất nhập và chuyển nội bộ.
- `stock_account`: cầu nối kho với kế toán để định giá tồn kho và sinh bút toán cho stock move.
- `stock_barcode`: dùng barcode scanner cho nghiệp vụ kho.
- `stock_delivery`: nối kho với đơn vị vận chuyển hoặc carrier và giao hàng.
- `stock_dropshipping`: bài toán dropship, hàng đi thẳng từ vendor tới customer mà không qua kho.
- `stock_enterprise`: bổ sung view, report và tính năng enterprise cho kho.

### 6.2. Có thể nhóm nhanh theo chức năng

Lõi kho:

- `stock`
- `stock_enterprise`

Kế toán kho:

- `stock_account`
- `stock_accountant`

Barcode:

- `stock_barcode`
- các module `stock_barcode_*` là addon barcode cho từng domain như MRP, batch picking, expiry, quality

Logistics hoặc giao nhận:

- `stock_delivery`
- `stock_dropshipping`
- `stock_picking_batch`

Chủ đề chuyên biệt:

- `stock_landed_costs`: chi phí mua hàng hoặc nhập khẩu phân bổ vào giá vốn
- `stock_maintenance`: liên quan thiết bị hoặc kho vận
- `stock_sms`: nhắn tin cho flow kho
- `stock_fleet`, `stock_fleet_enterprise`: liên quan đội xe
- `stock_intrastat`: khai báo thương mại EU

### 6.3. Cách hiểu trong bối cảnh 0502

Với quy trình 0502, phần thực sự đáng quan tâm thường là:

- `stock`: để xử lý bước kiểm tra tồn kho, yêu cầu xuất kho và xuất vật tư
- `purchase`: khi thiếu vật tư phải mua ngoài
- `stock_account`: chỉ cần nếu muốn theo dõi giá trị vật tư xuất dùng và bút toán kế toán
- `industry_fsm_stock` hoặc `helpdesk_stock`: nếu luồng sửa chữa xuất phát từ FSM hoặc helpdesk và muốn bám kho ngay trên task hoặc ticket
- `stock_barcode`: chỉ cần nếu đội kho hoặc kỹ thuật viên xuất vật tư bằng máy quét

Còn lại, đa số module trong nhóm ảnh không phải trục chính cho 0502.

### 6.4. Nếu cần đọc trước thì nên theo thứ tự

1. `stock`
2. `purchase`
3. `industry_fsm_stock` hoặc `helpdesk_stock`
4. `stock_account` nếu có yêu cầu kế toán

## 7. Nhóm module Purchase

Nhóm `purchase*` theo đúng pattern quen thuộc: `purchase` là lõi, còn các module còn lại là tích hợp theo domain.

### 7.1. Các module chính

- `purchase`: module gốc mua hàng. Quản lý purchase order, báo giá nhà cung cấp và thỏa thuận mua hàng.
- `purchase_stock`: nối mua hàng với kho, tức là PO đi kèm receipt, replenishment, rule mua hàng và vendor bill cho hàng hóa. Đây là module rất quan trọng nếu cần mua ngoài để bổ sung vật tư.
- `purchase_repair`: nối mua hàng với repair, để theo dõi liên kết giữa purchase và repair order.
- `purchase_requisition`: quản lý purchase agreement, call for tender và blanket order. Hợp khi phải xin nhiều báo giá hoặc mua theo thỏa thuận khung.
- `purchase_requisition_stock`: nối requisition với kho.
- `purchase_mrp`: nối mua hàng với sản xuất hoặc MRP. Không phải trọng tâm cho 0502 nếu bài toán là bảo trì sửa chữa máy móc cửa hàng.

### 7.2. Hiểu ngắn gọn theo nghiệp vụ

- `purchase` = tạo và quản lý đơn mua
- `purchase_stock` = mua hàng có nhập kho
- `purchase_repair` = mua hàng phục vụ repair flow
- `purchase_requisition` = quy trình mời thầu, xin báo giá hoặc blanket order
- `purchase_requisition_stock` = requisition có gắn với luồng kho
- `purchase_mrp` = mua hàng liên quan sản xuất

### 7.3. Cách hiểu trong bối cảnh 0502

Nhóm đáng quan tâm nhất là:

- `purchase`: để tạo PO khi thiếu vật tư
- `purchase_stock`: gần như bắt buộc nếu vật tư mua về phải nhập kho rồi mới xuất cho sửa chữa
- `purchase_repair`: đáng xem nếu đi theo trục repair
- `purchase_requisition`: chỉ cần nếu doanh nghiệp có quy trình mua ngoài nhiều nhà cung cấp, cần so giá hoặc phê duyệt bài bản

### 7.4. Một số module có thể hiểu nhanh theo tên

- `purchase_stock` là quan trọng
- `purchase_repair` có thể liên quan
- `purchase_requisition`, `purchase_requisition_stock` là nâng cao
- `purchase_edi_ubl_bis3`, `purchase_intrastat` là chuyên biệt về chuẩn chứng từ hoặc khai báo, thường không liên quan 0502
- `purchase_product_matrix` là tiện ích giao diện để chọn biến thể sản phẩm
- `purchase_mrp_workorder_quality` là nhánh sản xuất hoặc chất lượng, không phải trọng tâm bảo trì cửa hàng
- `purchase_requisition_sale` là cầu nối requisition với sale, thường không phải trọng tâm ở đây

### 7.5. Nếu chốt cho 0502 thì nên ưu tiên đọc theo thứ tự

1. `purchase`
2. `purchase_stock`
3. `purchase_repair`
4. `purchase_requisition` nếu có quy trình xin báo giá nhiều nhà cung cấp

## 8. Các module phù hợp với 0502 và lý do phù hợp

Phần này tổng hợp những module phù hợp nhất để triển khai quy trình 0502, xét theo các bước nghiệp vụ đã phân tích.

### 8.1. Nhóm phù hợp nhất làm trục chính

#### `maintenance`

Phù hợp vì:

- Đây là module lõi để quản lý thiết bị và yêu cầu bảo trì.
- Hỗ trợ rất tự nhiên cho bài toán danh mục máy móc, lịch sử bảo trì, maintenance request và bảo trì định kỳ.
- Phù hợp với các bước đầu quy trình như phát sinh nhu cầu, tiếp nhận yêu cầu, kiểm tra tình trạng và theo dõi vòng đời bảo trì.

#### `maintenance_worksheet`

Phù hợp vì:

- Bổ sung khả năng số hóa biểu mẫu kiểm tra, checklist, phiếu công tác và biên bản nghiệm thu.
- Rất hợp với các bước kiểm tra hiện trạng, xác nhận xử lý, nghiệm thu sau bảo trì.
- Giúp chuẩn hóa nội dung kỹ thuật theo từng loại máy hoặc loại công việc.

#### `industry_fsm`

Phù hợp vì:

- Mạnh ở phần tổ chức thực thi công việc kỹ thuật hiện trường.
- Hỗ trợ phân công kỹ thuật viên, theo dõi task, timesheet, tiến độ và hoạt động sửa chữa thực tế.
- Phù hợp với các bước lập kế hoạch, điều phối nhân sự, triển khai sửa chữa và theo dõi công việc.

#### `stock`

Phù hợp vì:

- Là nền tảng bắt buộc nếu quy trình có bước kiểm tra tồn kho, yêu cầu xuất kho và xuất vật tư cho sửa chữa.
- Hỗ trợ chứng từ kho rõ ràng cho việc cấp phát vật tư.
- Giúp kiểm soát tồn kho trước khi quyết định mua ngoài.

#### `purchase`

Phù hợp vì:

- Cần khi quy trình phát sinh nhánh mua ngoài do thiếu vật tư.
- Cho phép quản lý đơn mua, nhà cung cấp và chuỗi phê duyệt mua hàng.
- Là nền bắt buộc cho bước mua bổ sung vật tư trước khi tiếp tục sửa chữa.

#### `purchase_stock`

Phù hợp vì:

- Đây là cầu nối thực tế giữa mua hàng và nhập kho.
- Trong 0502, vật tư mua ngoài thường phải nhập kho rồi mới cấp phát cho sửa chữa.
- Module này giúp nối liền logic mua hàng với luồng receipt và tồn kho.

### 8.2. Nhóm phù hợp tùy theo cách triển khai

#### `helpdesk`

Phù hợp nếu doanh nghiệp muốn lấy ticket làm điểm bắt đầu của quy trình.

Lý do:

- Cửa hàng có thể raise ticket cho CMT ngay từ đầu.
- Thuận lợi nếu doanh nghiệp đã quen vận hành bằng cơ chế ticket hoặc support request.
- Phù hợp với bước ghi nhận nhu cầu phát sinh không định kỳ.

#### `helpdesk_fsm`

Phù hợp nếu muốn chuyển từ ticket sang task hiện trường.

Lý do:

- Nối logic tiếp nhận yêu cầu với logic thực thi ngoài hiện trường.
- Hữu ích khi quy trình muốn giữ ticket cho đầu vào và FSM cho đầu ra thực thi.

#### `helpdesk_stock`

Phù hợp nếu doanh nghiệp muốn bám cả nhu cầu vật tư ngay trên ticket.

Lý do:

- Liên kết ticket với nghiệp vụ kho.
- Phù hợp khi muốn theo dõi vật tư phát sinh từ ticket sửa chữa.

#### `helpdesk_repair`

Phù hợp nếu doanh nghiệp triển khai theo hướng repair flow chuẩn.

Lý do:

- Giúp gắn yêu cầu helpdesk với repair order.
- Phù hợp khi quy trình sửa chữa cần dựa nhiều vào app repair của Odoo.

#### `industry_fsm_stock`

Phù hợp nếu việc sửa chữa được vận hành trên task Field Service và có tiêu hao vật tư.

Lý do:

- Gắn task sửa chữa với stock move.
- Rất sát với bước kiểm tra vật tư, xuất kho và dùng vật tư trong quá trình sửa chữa.

#### `planning`

Phù hợp nếu cần một lớp điều phối nhân sự tách riêng.

Lý do:

- Hỗ trợ lập lịch cho kỹ thuật viên theo ngày, ca hoặc nguồn lực.
- Phù hợp với bước lập kế hoạch và điều phối nhân viên bảo trì.

#### `planning_holidays`

Phù hợp nếu cần tránh phân công người đang nghỉ.

Lý do:

- Giúp kế hoạch thực tế hơn.
- Tránh xung đột tài nguyên trong quá trình điều phối đội bảo trì.

#### `planning_hr_skills`

Phù hợp nếu cần phân kỹ thuật viên đúng kỹ năng.

Lý do:

- Hỗ trợ chọn người phù hợp với loại máy hoặc loại sự cố.
- Phù hợp trong môi trường có nhiều cấp độ tay nghề hoặc chuyên môn khác nhau.

#### `planning_attendance`

Phù hợp nếu cần đối chiếu kế hoạch với giờ làm thực tế.

Lý do:

- Hữu ích cho giai đoạn tối ưu vận hành hoặc đo hiệu suất.
- Không phải module lõi để dựng 0502 ban đầu nhưng tốt cho giai đoạn hoàn thiện sau.

#### `stock_account`

Phù hợp nếu dự án yêu cầu theo dõi giá trị vật tư xuất dùng.

Lý do:

- Gắn được vật tư sửa chữa với giá trị tồn kho và kế toán.
- Chỉ cần khi bài toán có yêu cầu tài chính hoặc kế toán kho rõ ràng.

#### `purchase_repair`

Phù hợp nếu quy trình chọn hướng gắn chặt mua hàng với repair order.

Lý do:

- Hữu ích khi vật tư mua ngoài phục vụ trực tiếp cho luồng repair.
- Không phải module bắt buộc trong mọi cách triển khai 0502.

#### `purchase_requisition`

Phù hợp nếu doanh nghiệp có quy trình xin nhiều báo giá hoặc lựa chọn nhà cung cấp chính thức.

Lý do:

- Hỗ trợ call for tender và blanket order.
- Phù hợp khi nhánh mua ngoài cần nhiều bước phê duyệt hoặc so sánh giá.

### 8.3. Đề xuất cấu trúc triển khai thực tế cho 0502

#### Phương án thiên về quản lý bảo trì thiết bị

Nên lấy:

- `maintenance`
- `maintenance_worksheet`
- `stock`
- `purchase`
- `purchase_stock`

Phương án này phù hợp khi trọng tâm là quản lý máy móc, yêu cầu bảo trì, vật tư và mua ngoài.

#### Phương án thiên về ticket và điều phối thực địa

Nên lấy:

- `helpdesk`
- `helpdesk_fsm`
- `industry_fsm`
- `industry_fsm_stock`
- `stock`
- `purchase`
- `purchase_stock`

Phương án này phù hợp khi doanh nghiệp muốn quy trình bắt đầu từ ticket và sau đó đẩy mạnh sang điều phối kỹ thuật hiện trường.

#### Phương án có lớp scheduling chuyên sâu

Có thể bổ sung thêm:

- `planning`
- `planning_holidays`
- `planning_hr_skills`
- `planning_attendance`

Phương án này phù hợp khi đội kỹ thuật lớn, cần điều phối ca làm, kỹ năng và đo thực tế thực hiện.

## 9. Kết luận

Nếu cần chọn nhanh bộ module phù hợp nhất cho 0502 theo hướng tiêu chuẩn và thực dụng, bộ nên ưu tiên khảo sát đầu tiên là:

- `maintenance`
- `maintenance_worksheet`
- `stock`
- `purchase`
- `purchase_stock`

Nếu muốn bài toán bắt đầu từ ticket và gắn mạnh với hoạt động kỹ thuật hiện trường, nên khảo sát thêm:

- `helpdesk`
- `helpdesk_fsm`
- `industry_fsm`
- `industry_fsm_stock`

Nếu cần tối ưu điều phối nhân sự kỹ thuật ở mức nâng cao, nên xem tiếp:

- `planning`
- `planning_holidays`
- `planning_hr_skills`
- `planning_attendance`
