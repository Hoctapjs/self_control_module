# Đặc tả nghiệp vụ 0502 - Bảo trì và sửa chữa máy móc

## Liên kết nhanh tới các module gốc liên quan

- Helpdesk: [helpdesk](/d:/odoo-19.0+e.20250918/odoo/addons/helpdesk)
- Maintenance: [maintenance](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance)
- Field Service: [industry_fsm](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm)
- Field Service Sale: [industry_fsm_sale](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm_sale)
- Field Service Stock: [industry_fsm_stock](/d:/odoo-19.0+e.20250918/odoo/addons/industry_fsm_stock)
- Planning: [planning](/d:/odoo-19.0+e.20250918/odoo/addons/planning)
- Inventory: [stock](/d:/odoo-19.0+e.20250918/odoo/addons/stock)
- Purchase: [purchase](/d:/odoo-19.0+e.20250918/odoo/addons/purchase)

## 1. Mục đích

Quy trình 0502 được xây dựng để quản lý toàn bộ vòng đời xử lý nhu cầu bảo trì và sửa chữa máy móc tại cửa hàng, từ lúc phát sinh nhu cầu, kiểm tra thực tế, phê duyệt phương án, chuẩn bị vật tư, triển khai sửa chữa cho đến bước nghiệm thu sau bảo trì. Quy trình này bảo đảm mọi yêu cầu đều được ghi nhận, đánh giá, kiểm soát chi phí và timeline trước khi thực hiện.

## 2. Điểm khởi đầu của quy trình

Quy trình có hai nhánh khởi phát:

### 2.1. Nhánh phát sinh nhu cầu không định kỳ

Khi cửa hàng phát sinh nhu cầu bảo trì hoặc sửa chữa máy móc, cửa hàng tạo phiếu yêu cầu bảo trì hoặc raise ticket gửi đến bộ phận CMT. Sau khi tiếp nhận, CMT thực hiện kiểm tra thực tế tình trạng thiết bị để đánh giá mức độ cần thiết của việc xử lý.

Nếu kết quả kiểm tra cho thấy thiết bị không cần xử lý, quy trình kết thúc tại đây.

Nếu kết quả kiểm tra cho thấy thiết bị cần xử lý, quy trình chuyển sang bước đánh giá chi tiết và đề xuất phương án xử lý.

### 2.2. Nhánh bảo trì định kỳ

Song song với các yêu cầu phát sinh đột xuất, hệ thống tự động kiểm tra lịch bảo trì định kỳ của máy móc. Khi đến hạn bảo trì, hệ thống gửi lịch cho CMT Lead. Dựa trên lịch nhận được, CMT Lead tiếp nhận và tổng hợp các yêu cầu bảo trì, sau đó lập kế hoạch bảo trì máy móc và điều phối nhân sự bảo trì phù hợp với khối lượng công việc.

Trong quá trình triển khai kế hoạch, hệ thống hoặc bộ phận phụ trách tiếp tục xuất báo cáo theo dõi tình trạng để phục vụ việc kiểm soát tiến độ xử lý và hiện trạng thiết bị.

## 3. Luồng xử lý nghiệp vụ chính

### Bước 1. Cửa hàng tạo yêu cầu bảo trì hoặc ticket

Mọi nhu cầu bảo trì hoặc sửa chữa phát sinh tại cửa hàng phải được ghi nhận dưới dạng phiếu yêu cầu bảo trì hoặc ticket trước khi chuyển đến CMT.

### Bước 2. CMT tiếp nhận và kiểm tra thực tế ban đầu

CMT tiếp nhận yêu cầu từ cửa hàng và tiến hành kiểm tra thực tế để xác định máy móc có thật sự cần xử lý hay không.

- Nếu không cần xử lý: kết thúc quy trình.
- Nếu cần xử lý: chuyển sang bước đánh giá chi tiết và đề xuất phương án xử lý.

### Bước 3. CMT kiểm tra hiện trạng chi tiết và đề xuất phương án xử lý

Đối với các yêu cầu cần xử lý, CMT tiếp tục kiểm tra hiện trạng chi tiết hơn để xác định nguyên nhân, mức độ hư hỏng, phương án xử lý phù hợp và báo giá tương ứng nếu có.

Kết quả của bước này là đề xuất phương án xử lý hoặc báo giá gửi lại cho cửa hàng xem xét.

### Bước 4. Cửa hàng xem xét và phê duyệt timeline, chi phí

Cửa hàng tiếp nhận đề xuất từ CMT để xem xét và phê duyệt timeline cùng chi phí xử lý.

- Nếu cửa hàng không phê duyệt: yêu cầu quay lại bước CMT đề xuất phương án xử lý hoặc báo giá để điều chỉnh.
- Nếu cửa hàng phê duyệt: quy trình tiếp tục sang bước thẩm định máy móc.

### Bước 5. Thẩm định máy móc sau phê duyệt

Sau khi được cửa hàng phê duyệt, máy móc được thẩm định để xác định hình thức xử lý tiếp theo.

- Nếu cần sử dụng dịch vụ bên ngoài: kích hoạt quy trình outside service để xử lý theo tuyến dịch vụ ngoài.
- Nếu không cần dịch vụ bên ngoài: tiếp tục xác định nhu cầu vật tư phục vụ sửa chữa.

### Bước 6. Xác định nhu cầu vật tư

Trong quá trình chuẩn bị sửa chữa, CMT kiểm tra xem có phát sinh nhu cầu vật tư hay không.

- Nếu không phát sinh vật tư: có thể chuyển trực tiếp sang bước sửa chữa máy móc.
- Nếu có phát sinh vật tư: CMT lập yêu cầu xuất kho vật tư để chuẩn bị cho việc sửa chữa.

### Bước 7. Kiểm tra tồn kho và xử lý cấp vật tư

Khi có yêu cầu xuất kho, doanh nghiệp tiến hành kiểm tra tồn kho vật tư.

- Nếu tồn kho đủ: CMT Lead phê duyệt yêu cầu và vật tư được xuất kho để phục vụ sửa chữa.
- Nếu tồn kho không đủ: quy trình chuyển sang mua ngoài để bổ sung vật tư trước khi triển khai sửa chữa.

### Bước 8. CMT thực hiện sửa chữa máy móc

Sau khi phương án xử lý đã được duyệt và vật tư đã sẵn sàng, hoặc trong trường hợp không phát sinh nhu cầu vật tư, CMT tiến hành sửa chữa máy móc theo đúng phương án đã được phê duyệt.

### Bước 9. Cửa hàng nghiệm thu và đánh giá sau bảo trì

Sau khi sửa chữa hoàn tất, cửa hàng thực hiện nghiệm thu và đánh giá kết quả sau bảo trì. Đây là bước xác nhận cuối cùng để bảo đảm máy móc đã được xử lý đúng yêu cầu, có thể đưa trở lại vận hành và ghi nhận chất lượng dịch vụ bảo trì đã thực hiện.

## 4. Vai trò tham gia

- Cửa hàng: phát sinh nhu cầu, tạo phiếu yêu cầu hoặc ticket, xem xét phê duyệt phương án, timeline, chi phí và nghiệm thu kết quả sau bảo trì.
- CMT: tiếp nhận yêu cầu, kiểm tra thực tế, đánh giá hiện trạng, đề xuất phương án xử lý, lập yêu cầu vật tư và thực hiện sửa chữa nội bộ.
- CMT Lead: tiếp nhận lịch bảo trì định kỳ, tổng hợp kế hoạch, điều phối nhân sự bảo trì, phê duyệt yêu cầu xuất kho vật tư.
- Hệ thống: tự động kiểm tra lịch bảo trì định kỳ, gửi lịch cho CMT Lead, hỗ trợ xuất báo cáo theo dõi tình trạng.
- Bộ phận kho hoặc bộ phận liên quan: kiểm tra tồn kho, xuất vật tư hoặc phối hợp mua ngoài khi thiếu vật tư.
- Đơn vị dịch vụ ngoài: tham gia xử lý khi có nhu cầu outside service.

## 5. Điều kiện

- Mọi nhu cầu bảo trì phát sinh phải được ghi nhận bằng phiếu yêu cầu bảo trì hoặc ticket trước khi CMT tiếp nhận xử lý.
- Đối với bảo trì định kỳ, hệ thống phải có dữ liệu lịch bảo trì để tự động kiểm tra và gửi lịch cho CMT Lead.
- Việc triển khai sửa chữa chỉ được thực hiện khi CMT đã kiểm tra thực tế và cửa hàng đã phê duyệt timeline cùng chi phí xử lý.
- Trường hợp cần vật tư, yêu cầu xuất kho phải được kiểm tra tồn kho và được CMT Lead phê duyệt trước khi xuất vật tư.
- Nếu cần sử dụng dịch vụ bên ngoài, quy trình outside service phải được kích hoạt thay cho việc xử lý nội bộ.

## 6. Ngoại lệ

### 6.1. Thiết bị không cần xử lý

Nếu kiểm tra thực tế cho thấy máy móc không cần xử lý, quy trình kết thúc ngay sau bước đánh giá ban đầu và không đi tiếp vào các bước lập phương án hay sửa chữa. Đây là nhánh loại trừ nhằm tránh phát sinh xử lý không cần thiết.

### 6.2. Cửa hàng không phê duyệt timeline hoặc chi phí

Nếu cửa hàng không phê duyệt timeline hoặc chi phí, quy trình quay lại bước CMT đề xuất phương án xử lý hoặc báo giá để điều chỉnh lại cho phù hợp với nhu cầu và khả năng chấp nhận của cửa hàng. Điều này thể hiện cửa hàng giữ vai trò kiểm soát cuối cùng về tiến độ và chi phí trước khi sửa chữa được triển khai.

### 6.3. Cần dịch vụ ngoài

Nếu máy móc cần dịch vụ ngoài, quy trình không tiếp tục theo tuyến sửa chữa nội bộ mà chuyển sang quy trình outside service.

### 6.4. Thiếu vật tư tồn kho

Nếu vật tư phát sinh nhưng tồn kho không đủ, quy trình phải chuyển sang mua ngoài trước khi có thể tiếp tục sửa chữa. Trường hợp này cho thấy quy trình 0502 có liên kết chặt chẽ với quản lý kho và quy trình mua ngoài để bảo đảm việc xử lý sự cố không bị gián đoạn.

## 7. Kết quả đầu ra

Sau khi quy trình hoàn tất:

- Máy móc tại cửa hàng được kiểm tra, bảo trì hoặc sửa chữa theo đúng nhu cầu thực tế.
- Timeline, chi phí, vật tư và phương án xử lý được kiểm soát rõ ràng trước khi triển khai.
- Thiết bị được nghiệm thu sau bảo trì và có thể tiếp tục phục vụ vận hành cửa hàng trong trạng thái ổn định.
- Toàn bộ quá trình có đầy đủ dấu vết theo dõi để phục vụ công tác quản lý và đánh giá chất lượng dịch vụ sau này.

## 8. Tóm tắt logic quyết định

1. Cửa hàng phát sinh nhu cầu hoặc hệ thống đến lịch bảo trì định kỳ.
2. CMT hoặc CMT Lead tiếp nhận và tổ chức kiểm tra, lập kế hoạch.
3. Nếu không cần xử lý thì kết thúc.
4. Nếu cần xử lý thì CMT đề xuất phương án và báo giá.
5. Cửa hàng phê duyệt timeline và chi phí.
6. Nếu không phê duyệt thì quay lại bước đề xuất để điều chỉnh.
7. Nếu phê duyệt thì thẩm định có cần outside service hay không.
8. Nếu cần outside service thì chuyển sang quy trình dịch vụ ngoài.
9. Nếu xử lý nội bộ thì xác định có phát sinh vật tư hay không.
10. Nếu cần vật tư thì kiểm tra tồn kho, xuất kho hoặc mua ngoài bổ sung.
11. CMT thực hiện sửa chữa.
12. Cửa hàng nghiệm thu và đánh giá sau bảo trì.

## 9. Các bước chi tiết theo quy trình thực hiện

Phần này ghi lại chi tiết các bước theo đúng thứ tự thể hiện trên sơ đồ quy trình thực hiện.

### Bước 1. Cửa hàng phát sinh nhu cầu bảo trì, sửa chữa

Đây là điểm khởi đầu của quy trình khi cửa hàng ghi nhận máy móc có vấn đề, cần bảo trì định kỳ hoặc cần sửa chữa để tiếp tục vận hành ổn định.

### Bước 2. Tạo phiếu yêu cầu bảo trì

Cửa hàng lập phiếu yêu cầu bảo trì hoặc ticket để ghi nhận nhu cầu và chuyển thông tin đến bộ phận CMT xử lý.

### Bước 3. CMT tiếp nhận yêu cầu bảo trì

CMT tiếp nhận phiếu yêu cầu hoặc ticket từ cửa hàng, xác nhận thông tin ban đầu và chuẩn bị thực hiện kiểm tra thực tế.

### Bước 4. Thực hiện kiểm tra thực tế tình trạng

CMT kiểm tra thực tế tình trạng thiết bị để xác định mức độ hư hỏng, nhu cầu xử lý và hướng đi tiếp theo của quy trình.

- TH1: Không cần xử lý, kết thúc quy trình.
- TH2: Cần xử lý, chuyển sang bước 11 để kiểm tra chi tiết và đề xuất phương án.

### Bước 5. Hệ thống tự động kiểm tra lịch bảo trì máy móc định kỳ

Song song với nhánh phát sinh yêu cầu đột xuất, hệ thống chủ động kiểm tra lịch bảo trì định kỳ của máy móc theo dữ liệu đã được thiết lập.

### Bước 6. Gửi lịch bảo trì cho CMT Lead

Khi đến hạn bảo trì, hệ thống gửi lịch bảo trì cho CMT Lead để chủ động tiếp nhận và tổ chức nguồn lực xử lý.

### Bước 7. CMT Lead tiếp nhận lịch và tổng hợp yêu cầu bảo trì

CMT Lead nhận thông tin lịch bảo trì, tổng hợp các yêu cầu liên quan và chuẩn bị cho công tác lập kế hoạch bảo trì.

### Bước 8. Lập kế hoạch bảo trì máy móc

Từ dữ liệu lịch bảo trì và các yêu cầu đã tổng hợp, CMT Lead xây dựng kế hoạch bảo trì máy móc theo thời gian, mức độ ưu tiên và nguồn lực sẵn có.

### Bước 9. Điều phối nhân viên bảo trì

CMT Lead phân công hoặc điều phối nhân sự bảo trì phù hợp với kế hoạch, khối lượng công việc và tính chất của từng hạng mục máy móc.

### Bước 10. Xuất báo cáo theo dõi tình trạng

Trong quá trình triển khai, hệ thống hoặc bộ phận phụ trách xuất báo cáo theo dõi tình trạng để hỗ trợ giám sát tiến độ, hiện trạng thiết bị và kết quả thực hiện kế hoạch bảo trì.

### Bước 11. CMT kiểm tra thực tế và đề xuất phương án xử lý hoặc báo giá

Đối với các trường hợp cần xử lý, CMT thực hiện kiểm tra chi tiết hơn và lập đề xuất phương án xử lý, đồng thời đưa ra báo giá nếu cần.

### Bước 12. Cửa hàng duyệt timeline, cost

Cửa hàng xem xét đề xuất từ CMT và thực hiện phê duyệt về tiến độ thực hiện và chi phí xử lý.

- TH1: Không duyệt, quy trình quay lại bước 11 để CMT rà soát, điều chỉnh phương án hoặc báo giá.
- TH2: Duyệt, tiếp tục thực hiện bước tiếp theo.

### Bước 13. Thẩm định máy móc nếu cần dịch vụ ngoài thì bắt đầu quy trình outside service

Sau khi cửa hàng đã phê duyệt, máy móc được thẩm định để xác định có cần thuê dịch vụ bên ngoài hay không.

- Nếu cần dịch vụ ngoài: kích hoạt quy trình outside service.
- Nếu không cần dịch vụ ngoài: tiếp tục xử lý theo tuyến nội bộ.

### Bước 14. Nếu không cần dịch vụ ngoài, kiểm tra vật tư phát sinh

Với các trường hợp xử lý nội bộ, CMT tiếp tục đánh giá xem trong quá trình sửa chữa có phát sinh nhu cầu vật tư hay không.

- TH1: Không phát sinh vật tư, chuyển sang bước 20 để sửa chữa máy móc.
- TH2: Có phát sinh vật tư, tiếp tục bước 15.

### Bước 15. CMT đề xuất yêu cầu xuất kho vật tư

Khi có phát sinh vật tư, CMT lập đề xuất hoặc yêu cầu xuất kho vật tư để chuẩn bị cho công tác sửa chữa.

### Bước 16. Kiểm tra tồn kho vật tư

Doanh nghiệp hoặc bộ phận liên quan kiểm tra tồn kho vật tư để xác định khả năng đáp ứng yêu cầu xuất kho.

- TH1: Còn tồn, tiếp tục bước 17.
- TH2: Hết tồn hoặc không đủ đáp ứng, chuyển qua bước 19.

### Bước 17. CMT Lead duyệt yêu cầu

CMT Lead xem xét và phê duyệt yêu cầu xuất kho vật tư trước khi vật tư được cấp cho hoạt động sửa chữa.

### Bước 18. Thực hiện xuất kho

Sau khi được phê duyệt, bộ phận kho thực hiện xuất kho vật tư để cung cấp cho CMT triển khai sửa chữa.

### Bước 19. Nếu tồn kho vật tư không đủ đáp ứng, tiến hành mua ngoài

Nếu vật tư trong kho không đủ để đáp ứng yêu cầu, quy trình chuyển sang mua ngoài nhằm bổ sung vật tư cần thiết trước khi sửa chữa.

### Bước 20. CMT tiến hành sửa chữa máy móc

Sau khi đủ điều kiện về phương án xử lý, phê duyệt, vật tư hoặc nguồn lực cần thiết, CMT tiến hành sửa chữa máy móc theo kế hoạch và phương án đã được thông qua.

### Bước 21. Cửa hàng nghiệm thu và đánh giá sau bảo trì

Sau khi sửa chữa hoàn tất, cửa hàng thực hiện nghiệm thu kết quả và đánh giá sau bảo trì để xác nhận máy móc đã đáp ứng yêu cầu vận hành và chất lượng xử lý.
