# Phase 1 - Kế Hoạch Chi Tiết Theo Từng Bước

## 1. Mục tiêu của Phase 1

Phase 1 không nhằm hoàn thiện toàn bộ quy trình `0502` theo đúng lưu đồ chi tiết ngay từ đầu. Mục tiêu của phase này là:

- Dựng được luồng `end-to-end` tối thiểu
- Bám được `21 bước` của quy trình để không lạc nghiệp vụ
- Ưu tiên tận dụng chuẩn Odoo trước
- Chỉ custom ở mức tối thiểu, đủ để nối luồng
- Kiểm soát được phạm vi mã nguồn module sẽ tạo ra

Nguyên tắc thực hiện:

- Làm từ từ theo từng bước
- Mỗi bước đều phải xác định rõ dùng chuẩn Odoo gì
- Nếu có custom thì phải ghi rõ custom đó thuộc module nào
- Chưa làm custom sâu trong Phase 1 nếu chưa thực sự cần để luồng chạy

## 2. Nguyên tắc kiểm soát mã nguồn trong Phase 1

Khi triển khai từng bước, luôn trả lời 5 câu hỏi:

1. Bước này đang tận dụng module chuẩn nào
2. Có cần tạo module custom mới không
3. Nếu có, module custom đó chỉ nên làm vai trò gì
4. Có đang nhét logic sai chỗ hay không
5. Phần này có thể để sang Phase 2 hoặc Phase 3 không

Nguyên tắc kỹ thuật:

- `maintenance` là trục chính cho thiết bị và maintenance request
- `industry_fsm` là trục thực thi công việc hiện trường
- `stock` là trục kho và vật tư
- `purchase` và `purchase_stock` là trục mua ngoài
- `maintenance_worksheet` là trục checklist và biên bản kỹ thuật nếu cần

Trong Phase 1, chỉ nên tạo custom module khi cần nối luồng hoặc bổ sung field, action, wizard mức tối thiểu.

## 3. Định hướng module cho Phase 1

### 3.1. Module chuẩn dùng làm nền

- `maintenance`
- `industry_fsm`
- `stock`
- `purchase`
- `purchase_stock`
- `maintenance_worksheet`

### 3.2. Module custom nên giữ tối thiểu

Đề xuất giữ custom module ở mức gọn:

- `M02_P0502`

Vai trò chính:

- Bổ sung field nghiệp vụ 0502 tối thiểu
- Tạo action hoặc button nối luồng giữa các object
- Tạo menu hoặc màn hình điều hướng riêng cho 0502 nếu cần
- Chưa ôm workflow nặng trong Phase 1

## 4. Kế hoạch triển khai chi tiết theo từng bước

## Bước 1 - Cửa hàng phát sinh nhu cầu bảo trì, sửa chữa

### Mục tiêu

- Xác định điểm bắt đầu nghiệp vụ
- Chưa cần custom sâu ở bước này

### Dùng chuẩn Odoo

- `maintenance` nếu xem nhu cầu là maintenance request
- hoặc `helpdesk` nếu sau này muốn có lớp ticket tiếp nhận

### Hướng triển khai Phase 1

- Chốt `maintenance.request` là điểm nhận nhu cầu chính trong Phase 1
- Chưa dựng nhiều entry point khác nhau

### Mã nguồn dự kiến

- Có thể chưa cần custom
- Nếu cần thì chỉ thêm field xác định `nguồn phát sinh`

### Ghi chú kiểm soát

- Không nên tạo object mới chỉ để thay cho `maintenance.request` ở Phase 1

## Bước 2 - Tạo phiếu yêu cầu bảo trì

### Mục tiêu

- Có chứng từ đầu vào tối thiểu để bắt đầu xử lý

### Dùng chuẩn Odoo

- `maintenance.request`

### Hướng triển khai Phase 1

- Dùng trực tiếp form maintenance request
- Chỉ bổ sung các field tối thiểu nếu thiếu thông tin nghiệp vụ

### Mã nguồn dự kiến

- Kế thừa view của `maintenance.request`
- Có thể thêm field như:
  - mã cửa hàng
  - loại yêu cầu
  - mức độ ưu tiên

### Ghi chú kiểm soát

- Tránh tạo “phiếu yêu cầu bảo trì” thành model riêng nếu nội dung chưa vượt quá khả năng của `maintenance.request`

## Bước 3 - CMT tiếp nhận yêu cầu bảo trì

### Mục tiêu

- Thể hiện được trạng thái tiếp nhận

### Dùng chuẩn Odoo

- `maintenance.request`
- hoạt động trao đổi qua chatter

### Hướng triển khai Phase 1

- Dùng stage hoặc state hiện có nếu phù hợp
- Nếu chưa đủ thì thêm trạng thái tối thiểu để đánh dấu đã tiếp nhận

### Mã nguồn dự kiến

- Bổ sung state hoặc field tracking nhẹ trong `M02_P0502`

### Ghi chú kiểm soát

- Chỉ thêm những trạng thái thực sự cần cho Phase 1

## Bước 4 - Thực hiện kiểm tra thực tế tình trạng

### Mục tiêu

- Có nơi ghi nhận kết quả kiểm tra ban đầu

### Dùng chuẩn Odoo

- `maintenance.request`
- `maintenance_worksheet` nếu cần checklist sớm

### Hướng triển khai Phase 1

- Ghi nhận kết quả kiểm tra ở maintenance request
- Nếu có nhu cầu rõ ràng thì bật worksheet cơ bản

### Mã nguồn dự kiến

- Field kết luận kiểm tra:
  - không cần xử lý
  - cần xử lý
- Có thể thêm ghi chú kiểm tra ban đầu

### Ghi chú kiểm soát

- Không cần dựng hẳn workflow phức tạp ở bước này trong Phase 1

## Bước 5 - Hệ thống tự động kiểm tra lịch bảo trì máy móc

### Mục tiêu

- Có nhánh bảo trì định kỳ chạy được ở mức cơ bản

### Dùng chuẩn Odoo

- `maintenance.equipment`
- lịch và logic preventive maintenance của `maintenance`

### Hướng triển khai Phase 1

- Ưu tiên cấu hình preventive maintenance có sẵn
- Chưa custom scheduler phức tạp theo rule riêng nếu chưa cần

### Mã nguồn dự kiến

- Có thể chưa cần custom
- Nếu cần thì chỉ thêm cron hoặc action hỗ trợ mức nhẹ

### Ghi chú kiểm soát

- Chỉ custom khi chuẩn Odoo không đủ để tạo record định kỳ tối thiểu

## Bước 6 - Gửi lịch bảo trì cho CMT Lead

### Mục tiêu

- Có cơ chế nhìn thấy việc đến hạn bảo trì

### Dùng chuẩn Odoo

- activity
- chatter
- danh sách maintenance request hoặc equipment đến hạn

### Hướng triển khai Phase 1

- Chưa cần cơ chế gửi thông báo đặc thù phức tạp
- Dùng activity hoặc filter/list cơ bản

### Mã nguồn dự kiến

- Có thể thêm server action hoặc activity tạo tự động

### Ghi chú kiểm soát

- Phase 1 chỉ cần “thấy được” và “theo dõi được”, chưa cần notification quá đặc thù

## Bước 7 - CMT Lead tiếp nhận lịch và tổng hợp yêu cầu bảo trì

### Mục tiêu

- Có nơi để tổng hợp các yêu cầu cần xử lý

### Dùng chuẩn Odoo

- list view của `maintenance.request`
- search/filter/group by

### Hướng triển khai Phase 1

- Dùng search view để lọc theo:
  - cửa hàng
  - thiết bị
  - tình trạng
  - đến hạn

### Mã nguồn dự kiến

- Kế thừa search view
- Có thể thêm action `Yêu cầu cần lập kế hoạch`

### Ghi chú kiểm soát

- Chưa cần dashboard riêng quá sớm

## Bước 8 - Lập kế hoạch bảo trì máy móc

### Mục tiêu

- Xác định kế hoạch xử lý ở mức thực tế

### Dùng chuẩn Odoo

- `planning` nếu cần phân ca rõ
- hoặc xử lý đơn giản qua task/activities trong Phase 1

### Hướng triển khai Phase 1

- Nếu chưa cần planning đầy đủ, có thể ghi nhận kế hoạch ngay trên request/task
- Chỉ bật `planning` nếu doanh nghiệp thực sự cần điều phối theo lịch

### Mã nguồn dự kiến

- Field:
  - ngày dự kiến xử lý
  - người phụ trách

### Ghi chú kiểm soát

- Không bắt buộc kéo `planning` vào ngay nếu scope Phase 1 cần gọn

## Bước 9 - Điều phối nhân viên bảo trì

### Mục tiêu

- Có record thực thi cho kỹ thuật viên

### Dùng chuẩn Odoo

- `industry_fsm`

### Hướng triển khai Phase 1

- Tạo FSM task từ maintenance request
- Gán technician thực hiện

### Mã nguồn dự kiến

- Button từ `maintenance.request` sang tạo `project.task` kiểu FSM
- Field liên kết giữa request và task

### Ghi chú kiểm soát

- Đây là một trong những custom nối luồng quan trọng nhất của Phase 1

## Bước 10 - Xuất báo cáo theo dõi tình trạng

### Mục tiêu

- Có cách theo dõi tiến độ xử lý

### Dùng chuẩn Odoo

- list, pivot, graph của `maintenance.request` hoặc FSM task

### Hướng triển khai Phase 1

- Dùng report/list tiêu chuẩn trước
- Chưa làm dashboard đặc thù phức tạp

### Mã nguồn dự kiến

- Kế thừa search/filter/group
- Có thể thêm action báo cáo nhanh

### Ghi chú kiểm soát

- Báo cáo đặc thù đẹp hơn để Phase 2

## Bước 11 - CMT kiểm tra thực tế và đề xuất phương án xử lý hoặc báo giá

### Mục tiêu

- Ghi nhận phương án xử lý sơ bộ

### Dùng chuẩn Odoo

- `maintenance.request`
- `maintenance_worksheet`
- chatter/note

### Hướng triển khai Phase 1

- Chưa dựng quy trình báo giá riêng
- Ghi nhận đề xuất xử lý ở dạng text, checklist hoặc note có cấu trúc

### Mã nguồn dự kiến

- Field:
  - phương án xử lý
  - chi phí dự kiến
  - timeline dự kiến

### Ghi chú kiểm soát

- Báo giá formal và approval chặt để Phase 2

## Bước 12 - Cửa hàng duyệt timeline và cost

### Mục tiêu

- Có điểm quyết định tối thiểu trước khi sửa chữa

### Dùng chuẩn Odoo

- Không có flow chuẩn khớp hoàn toàn

### Hướng triển khai Phase 1

- Làm tối thiểu bằng trạng thái xác nhận đơn giản
- Chưa triển khai approval matrix phức tạp

### Mã nguồn dự kiến

- Field quyết định:
  - chờ duyệt
  - duyệt
  - từ chối
- Button thao tác mức cơ bản

### Ghi chú kiểm soát

- Đây là custom nhưng nên giữ ở mức nhẹ trong Phase 1

## Bước 13 - Thẩm định máy móc nếu cần dịch vụ ngoài

### Mục tiêu

- Xác định có đi nhánh xử lý nội bộ hay không

### Dùng chuẩn Odoo

- Chưa có flow chuẩn Odoo khớp hoàn toàn

### Hướng triển khai Phase 1

- Chỉ thêm cờ xác định:
  - xử lý nội bộ
  - cần thuê ngoài
- Chưa làm full outside service flow

### Mã nguồn dự kiến

- Field `need_outside_service`

### Ghi chú kiểm soát

- Nếu thuê ngoài là scope lớn, để Phase 3

## Bước 14 - Kiểm tra có phát sinh vật tư hay không

### Mục tiêu

- Xác định có đi nhánh kho hay không

### Dùng chuẩn Odoo

- `stock`
- `industry_fsm_stock` nếu cần gắn vật tư với task

### Hướng triển khai Phase 1

- Ghi nhận cờ có vật tư phát sinh
- Nếu có thì tạo luồng yêu cầu xuất kho tối thiểu

### Mã nguồn dự kiến

- Field `has_material_request`

### Ghi chú kiểm soát

- Chưa cần decision node quá phức tạp

## Bước 15 - CMT thực hiện yêu cầu xuất kho vật tư

### Mục tiêu

- Tạo được chứng từ hoặc hành động dẫn sang xuất kho

### Dùng chuẩn Odoo

- `stock`

### Hướng triển khai Phase 1

- Từ request hoặc task, tạo stock picking nội bộ hoặc chứng từ kho phù hợp

### Mã nguồn dự kiến

- Button tạo phiếu xuất kho
- Liên kết giữa maintenance request/FSM task và stock picking

### Ghi chú kiểm soát

- Nếu doanh nghiệp cần “phiếu yêu cầu xuất kho” riêng thì để Phase 2

## Bước 16 - Kiểm tra tồn kho vật tư

### Mục tiêu

- Xác định kho có đủ vật tư để xử lý hay không

### Dùng chuẩn Odoo

- `stock`
- tồn khả dụng sản phẩm

### Hướng triển khai Phase 1

- Dựa trên tồn kho hiện có để quyết định tiếp tục xuất kho hay đi mua ngoài

### Mã nguồn dự kiến

- Có thể chỉ cần logic hỗ trợ hoặc wizard nhẹ

### Ghi chú kiểm soát

- Không custom engine tồn kho riêng

## Bước 17 - CMT Lead duyệt yêu cầu

### Mục tiêu

- Có điểm duyệt tối thiểu trước khi xuất vật tư

### Dùng chuẩn Odoo

- Không có flow chuẩn khớp hoàn toàn với 0502

### Hướng triển khai Phase 1

- Dùng trạng thái duyệt đơn giản trên request hoặc picking

### Mã nguồn dự kiến

- Button duyệt
- Rule phân quyền thao tác

### Ghi chú kiểm soát

- Approval nhiều tầng để Phase 2 hoặc Phase 3

## Bước 18 - Thực hiện xuất kho

### Mục tiêu

- Vật tư được xuất thực tế

### Dùng chuẩn Odoo

- `stock.picking`
- `stock.move`
- `stock.move.line`

### Hướng triển khai Phase 1

- Dùng flow validate picking chuẩn của Odoo

### Mã nguồn dự kiến

- Chủ yếu tận dụng chuẩn

### Ghi chú kiểm soát

- Càng ít đụng vào flow kho chuẩn càng tốt

## Bước 19 - Nếu tồn kho vật tư không đủ đáp ứng, tiến hành mua ngoài

### Mục tiêu

- Có nhánh mua bù vật tư

### Dùng chuẩn Odoo

- `purchase`
- `purchase_stock`

### Hướng triển khai Phase 1

- Tạo PO thủ công hoặc bán tự động từ nhu cầu vật tư
- Chưa cần quy trình requisition phức tạp

### Mã nguồn dự kiến

- Có thể chỉ cần action mở màn hình PO có sẵn context

### Ghi chú kiểm soát

- `purchase_requisition` chưa cần đưa vào Phase 1 nếu chưa có nhu cầu nhiều báo giá

## Bước 20 - CMT tiến hành sửa chữa máy móc

### Mục tiêu

- Có nơi theo dõi thực thi sửa chữa

### Dùng chuẩn Odoo

- `industry_fsm`
- `maintenance_worksheet`

### Hướng triển khai Phase 1

- Dùng FSM task là object thực thi chính
- Ghi nhận nội dung công việc, vật tư, ghi chú xử lý

### Mã nguồn dự kiến

- Liên kết task với maintenance request
- Có thể thêm worksheet hoặc checklist kỹ thuật

### Ghi chú kiểm soát

- Không tạo object “lệnh sửa chữa” mới nếu FSM task đã đủ dùng trong Phase 1

## Bước 21 - Cửa hàng nghiệm thu và đánh giá sau bảo trì

### Mục tiêu

- Có bước xác nhận hoàn tất

### Dùng chuẩn Odoo

- `maintenance_worksheet`
- chatter
- chữ ký hoặc xác nhận cơ bản nếu có

### Hướng triển khai Phase 1

- Dùng worksheet hoặc phần ghi nhận kết quả tối thiểu
- Chưa làm form nghiệm thu quá đặc thù

### Mã nguồn dự kiến

- Field đánh giá kết quả
- kết luận nghiệm thu
- ngày hoàn tất

### Ghi chú kiểm soát

- Biên bản nghiệm thu đúng mẫu doanh nghiệp để Phase 2

## 5. Các hạng mục ưu tiên phát triển module trong Phase 1

### Nhóm 1 - Cấu hình chuẩn trước

- Cấu hình `maintenance`
- Cấu hình `industry_fsm`
- Cấu hình `stock`
- Cấu hình `purchase`
- Cấu hình `maintenance_worksheet` nếu cần

### Nhóm 2 - Custom nối luồng tối thiểu

- Liên kết `maintenance.request` với FSM task
- Bổ sung field nghiệp vụ tối thiểu
- Tạo action từ request sang kho hoặc mua hàng khi cần

### Nhóm 3 - Tối ưu giao diện dùng nội bộ

- Search view
- Filter
- Group by
- Menu điều hướng 0502

## 6. Những gì chưa nên làm sâu trong Phase 1

- Workflow 21 bước đầy đủ
- Approval nhiều tầng
- Outside service flow riêng hoàn chỉnh
- Bộ chứng từ đặc thù đầy đủ
- Dashboard quá đặc thù
- Object trục chính mới thay thế hoàn toàn chuẩn Odoo

## 7. Cách triển khai thực tế để kiểm soát mã nguồn

Đề xuất trình tự làm việc:

1. Chốt bước nào dùng chuẩn Odoo hoàn toàn
2. Chốt bước nào cần custom nhẹ để nối luồng
3. Chỉ sau đó mới bắt đầu tạo code trong `M02_P0502`
4. Mỗi lần code chỉ nên bám 1 cụm bước gần nhau
5. Sau mỗi cụm bước phải kiểm tra lại:
   - logic có đang đặt đúng module không
   - có đang tạo object thừa không
   - có đang đi quá xa phạm vi Phase 1 không

## 8. Kết luận

Trong `Phase 1`, cách phù hợp nhất là:

- Không cố làm đẹp toàn bộ quy trình ngay
- Đi lần lượt theo từng bước để kiểm soát nghiệp vụ
- Nhưng chỉ code phần tối thiểu cần thiết để luồng chạy được
- Giữ custom module `M02_P0502` ở vai trò nối luồng và bổ sung nghiệp vụ nhẹ

Mục tiêu cuối của Phase 1 là:

- Có luồng `0502` chạy được từ đầu đến cuối
- Có cơ sở mã nguồn gọn, dễ kiểm soát
- Không tự đẩy dự án vào custom nặng quá sớm
