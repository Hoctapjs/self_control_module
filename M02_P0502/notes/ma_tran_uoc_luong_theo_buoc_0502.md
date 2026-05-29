# Ma trận ước lượng theo bước cho quy trình 0502

## 1. Mục đích

File này dùng để hỗ trợ phase estimate cho quy trình 0502 bằng cách gom theo từng bước:

- bước nào của quy trình
- module chuẩn nào có thể dùng được ngay
- phần nào cần custom
- mức độ custom ước lượng theo 3 mức: thấp, vừa, cao

Lưu ý:

- `Thấp`: custom nhỏ, chủ yếu thêm field, view, smart button, rule đơn giản, report nhẹ
- `Vừa`: cần bridge giữa 2 đến 3 module, thêm state, approval, logic xử lý tương đối rõ
- `Cao`: cần thiết kế flow mới, traceability xuyên module, object điều phối trung tâm, dashboard hoặc approval nhiều tầng

## 2. Ma trận theo 21 bước

| Bước | Mô tả bước | Module chuẩn dùng được ngay | Phần cần custom | Mức độ custom |
|---|---|---|---|---|
| B1 | Cửa hàng phát sinh nhu cầu bảo trì, sửa chữa | Chưa có module nào bao trọn ý nghĩa “phát sinh nhu cầu” theo đúng 0502. Có thể lấy `helpdesk` làm điểm khởi phát gần nhất | Nếu muốn thống nhất mọi nguồn phát sinh vào một đầu vào chung thì cần custom entry logic và phân loại nguồn | Cao |
| B2 | Tạo phiếu yêu cầu bảo trì / raise ticket | `helpdesk` | Nếu chỉ dùng ticket thì custom thấp. Nếu muốn một form đầu vào chung vừa cho sự cố phát sinh vừa cho bảo trì định kỳ thì cần custom form và routing | Thấp đến vừa |
| B3 | CMT tiếp nhận yêu cầu bảo trì | `helpdesk`, `maintenance` | Cần custom vai trò CMT, queue tiếp nhận, rule phân công hoặc màn hình tiếp nhận riêng nếu không muốn dùng nguyên bản helpdesk | Vừa |
| B4 | Thực hiện kiểm tra thực tế tình trạng | `maintenance`, `maintenance_worksheet`, `industry_fsm` | Cần custom biểu mẫu kiểm tra hiện trạng, trạng thái trước/sau, ảnh hiện trường, mapping giữa ticket và maintenance/FSM nếu có | Vừa |
| B5 | Hệ thống tự động kiểm tra lịch bảo trì máy móc | `maintenance` | Nếu chỉ dùng recurring maintenance chuẩn thì custom thấp. Nếu cần logic nhắc việc theo cửa hàng, nhóm máy, điều kiện riêng thì cần custom scheduler | Thấp đến vừa |
| B6 | Gửi lịch bảo trì cho CMT Lead | `maintenance`, `mail` | Cần custom role CMT Lead, rule gửi lịch, thông báo theo người phụ trách đúng của 0502 | Vừa |
| B7 | CMT Lead tiếp nhận lịch và tổng hợp yêu cầu bảo trì | `maintenance`, có thể tham khảo `planning` nếu sau này mở rộng | Cần custom dashboard tổng hợp, vai trò CMT Lead, màn hình tổng hợp riêng | Vừa đến cao |
| B8 | Lập kế hoạch bảo trì máy móc | `maintenance`, `industry_fsm`, `planning` | Nếu chỉ lập đơn giản trên task/request thì custom thấp. Nếu cần kế hoạch tổng hợp nhiều cửa hàng, nhiều máy, nhiều nhân sự thì cần custom planning layer | Vừa |
| B9 | Điều phối nhân viên bảo trì | `industry_fsm`, `planning`, `planning_holidays`, `planning_hr_skills` | Nếu dùng FSM assignment cơ bản thì custom thấp. Nếu cần logic chọn người theo skill, tránh nghỉ phép, theo vùng phụ trách thì cần custom bổ sung | Vừa |
| B10 | Xuất báo cáo theo dõi tình trạng | `maintenance`, `industry_fsm`, `helpdesk`, `planning` có report rời rạc | Cần custom báo cáo tổng hợp theo 0502: cửa hàng, máy, kỹ thuật viên, trạng thái, KPI | Cao |
| B11 | CMT kiểm tra thực tế và đề xuất phương án xử lý hoặc báo giá | `maintenance`, `industry_fsm`, `maintenance_worksheet` | Cần custom phần đề xuất phương án xử lý, báo giá nội bộ, cấu trúc cost proposal, nội dung kỹ thuật | Cao |
| B12 | Cửa hàng duyệt timeline, cost | `helpdesk` có portal/ticket theo dõi, nhưng không có chuẩn duyệt timeline/cost cho 0502 | Cần custom màn hình duyệt, state duyệt, lịch sử duyệt, phản hồi từ chối/điều chỉnh | Cao |
| B13 | Nếu cần dịch vụ ngoài thì đi outside service / mua hàng dịch vụ ngoài | `purchase` chỉ hỗ trợ vendor và PO chuẩn, chưa đủ outside service flow | Cần custom nhánh outside service riêng hoặc object quản lý thuê ngoài, báo giá dịch vụ, nghiệm thu dịch vụ | Cao |
| B14 | Kiểm tra vật tư phát sinh | `industry_fsm_stock`, `stock`, `maintenance` | Cần custom logic xác định vật tư phát sinh từ request/task và gắn với bước thẩm định 0502 | Vừa đến cao |
| B15 | CMT yêu cầu xuất kho vật tư | `stock` có picking/move nhưng không có “yêu cầu xuất kho” chuẩn | Cần custom object hoặc approval state trước khi tạo chứng từ kho | Cao |
| B16 | Kiểm tra tồn kho vật tư | `stock` | Nếu chỉ kiểm tra tồn kho chuẩn thì custom thấp. Nếu cần ràng buộc theo yêu cầu sửa chữa và rule phê duyệt thì cần custom thêm | Thấp đến vừa |
| B17 | CMT Lead duyệt yêu cầu xuất kho | `stock` không có role/phê duyệt riêng theo semantics 0502 | Cần custom approval matrix, vai trò CMT Lead, điều kiện duyệt vật tư | Cao |
| B18 | Thực hiện xuất kho | `stock`, `stock_barcode` nếu mở rộng sau | Nếu chỉ xuất kho chuẩn thì custom thấp. Nếu cần link ngược về yêu cầu sửa chữa và biên bản vật tư thì cần custom thêm | Thấp đến vừa |
| B19 | Nếu tồn kho không đủ thì mua ngoài | `purchase`, `purchase_stock` | Nếu chỉ tạo PO và nhập kho chuẩn thì custom thấp. Nếu cần phê duyệt nội bộ, link tới yêu cầu sửa chữa, theo dõi vendor theo ngữ cảnh 0502 thì cần custom | Vừa |
| B20 | CMT tiến hành sửa chữa máy móc | `industry_fsm`, `maintenance`, `maintenance_worksheet`, `industry_fsm_stock` | Cần custom nếu muốn gắn chặt sửa chữa với vật tư, chi phí, checklist, trạng thái và đồng bộ với ticket/request | Vừa |
| B21 | Cửa hàng nghiệm thu và đánh giá sau bảo trì | `maintenance_worksheet`, `industry_fsm` có report/worksheet/signature, `helpdesk` có portal theo dõi | Cần custom flow nghiệm thu chính thức của store, điểm đánh giá, xác nhận hoàn thành cuối cùng, trace end-to-end | Cao |

## 3. Nhóm module chuẩn nên có ngay từ phase 1

Theo ma trận trên, các module chuẩn nên ưu tiên đưa vào phase 1 là:

- `helpdesk`
- `maintenance`
- `maintenance_worksheet`
- `industry_fsm`
- `stock`
- `purchase`
- `purchase_stock`

Các module nên cân nhắc tùy mức độ mở rộng:

- `industry_fsm_stock`
- `planning`
- `planning_holidays`
- `planning_hr_skills`
- `stock_account`
- `stock_barcode`

## 4. Các cụm custom chính dự kiến

Từ góc nhìn estimate, phần custom của 0502 thường sẽ gom vào các cụm lớn sau:

### 4.1. Cụm đầu vào và điều phối flow

- form đầu vào chung hoặc bridge giữa ticket và maintenance
- logic phân loại yêu cầu
- đồng bộ trạng thái giữa ticket, maintenance request và FSM task

Mức độ: cao

### 4.2. Cụm đề xuất và phê duyệt

- đề xuất phương án xử lý
- đề xuất timeline và chi phí
- duyệt hoặc từ chối từ phía cửa hàng
- duyệt vật tư từ CMT Lead

Mức độ: cao

### 4.3. Cụm vật tư và kho

- yêu cầu xuất kho
- link vật tư với yêu cầu sửa chữa
- truy vết vật tư đã dùng theo từng request hoặc task

Mức độ: vừa đến cao

### 4.4. Cụm mua ngoài và outside service

- link PO với yêu cầu sửa chữa
- mua ngoài vật tư theo context của 0502
- outside service nếu triển khai trong phase đầu

Mức độ: vừa đến cao

### 4.5. Cụm biểu mẫu và nghiệm thu

- checklist kỹ thuật
- biên bản sửa chữa
- biên bản nghiệm thu
- ảnh hiện trường
- đánh giá sau bảo trì

Mức độ: vừa

### 4.6. Cụm báo cáo và truy vết

- dashboard cho CMT Lead
- KPI 0502
- báo cáo theo cửa hàng, thiết bị, kỹ thuật viên, nhóm sự cố
- traceability end-to-end

Mức độ: cao

## 5. Gợi ý dùng ma trận này cho estimate

Có thể chia estimate thành 3 lớp:

### 5.1. Lớp nền chuẩn Odoo

- cài và cấu hình module gốc
- cấu hình quyền cơ bản
- cấu hình dữ liệu nền

### 5.2. Lớp custom bắt buộc để chạy đúng 0502

- bridge giữa các module
- approval flow
- yêu cầu xuất kho
- liên kết mua hàng
- nghiệm thu

### 5.3. Lớp tối ưu và mở rộng sau

- planning nâng cao
- stock barcode
- stock_account
- dashboard nâng cao
- SLA ngoài ticket
- outside service nâng cao

## 6. Kết luận nhanh

Nếu dùng ma trận này để estimate phase 1, có thể hiểu ngắn gọn như sau:

- phần chuẩn Odoo giúp dựng được xương sống của quy trình
- phần custom bắt buộc tập trung mạnh ở approval, bridge flow, vật tư và nghiệm thu
- các bước có mức custom cao nhất thường là: `B1`, `B6`, `B7`, `B10`, `B11`, `B12`, `B13`, `B15`, `B17`, `B21`

Đây là các bước nên được ưu tiên làm rõ kỹ trong workshop nghiệp vụ trước khi chốt effort và timeline triển khai.
