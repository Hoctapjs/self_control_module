# Phase 1 - Bước 2 Đã Triển Khai

## 1. Mục tiêu của bước 2

Trong kế hoạch `Phase 1`, bước 2 là:

- Tạo phiếu yêu cầu bảo trì

Mục tiêu của bước này là:

- Có chứng từ đầu vào tối thiểu để bắt đầu xử lý
- Tiếp tục bám vào `maintenance.request`
- Chỉ bổ sung những thông tin nghiệp vụ thực sự cần trong giai đoạn đầu
- Không tạo model riêng cho “phiếu yêu cầu bảo trì” nếu chuẩn Odoo vẫn còn đáp ứng được

Kết luận triển khai ở bước này là:

- Tiếp tục dùng `maintenance.request` làm phiếu đầu vào chính
- Bổ sung thêm các field tối thiểu để phù hợp hơn với nghiệp vụ `0502`
- Giữ `priority` của Odoo chuẩn, không custom lại

## 2. Cách hiểu nghiệp vụ ở bước 2

Bước 2 của quy trình là:

- Cửa hàng hoặc hệ thống tạo phiếu yêu cầu bảo trì để bắt đầu xử lý

Trong `Phase 1`, phiếu này chưa cần phản ánh toàn bộ logic nghiệp vụ phức tạp. Điều cần nhất là:

- Có thể nhận diện đơn vị vận hành phát sinh yêu cầu
- Có thể nhận diện loại yêu cầu
- Có thể phân biệt nguồn phát sinh đã làm ở bước 1

Ban đầu, hướng triển khai của bước 2 là lưu `mã cửa hàng` dạng text. Tuy nhiên sau khi đối chiếu thêm với cách tổ chức dữ liệu thực tế, hướng này đã được điều chỉnh.

Hiện tại, quyết định thiết kế được chốt là:

- Không lưu `store_code` dạng `Char`
- Không dùng `pos.config` cho bài toán này
- Dùng trực tiếp `hr.department` để đại diện cho “cửa hàng”
- Lấy mặc định phòng ban theo người tạo yêu cầu nếu user hiện tại có liên kết employee và department

## 3. Cơ sở để thay đổi từ `store_code` sang `department_id`

Sau khi tham khảo module `0200`, nhận định chính là:

- Trong hệ thống hiện tại, “store” đang được tổ chức theo phòng ban
- Vì vậy việc lưu mã cửa hàng dạng text sẽ yếu hơn so với việc liên kết trực tiếp đến `hr.department`
- Dùng `Many2one` tới `hr.department` giúp dữ liệu chặt hơn, ít nhập sai hơn và dễ báo cáo hơn

Tài liệu và source đã tham chiếu khi ra quyết định:

- [QUY_UOC_DAT_TEN_VA_RULE.md](/d:/odoo-19.0+e.20250918/addons/M02_P0200/convention/QUY_UOC_DAT_TEN_VA_RULE.md)
- [module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0200/structure/module_map.json)
- [hr_department_ext.py](/d:/odoo-19.0+e.20250918/addons/M02_P0200/models/hr_department_ext.py)

Ngoài ra, phần chuẩn Odoo được dùng làm nền ở bước này vẫn là:

- [maintenance.py](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/models/maintenance.py)
- [maintenance_views.xml](/d:/odoo-19.0+e.20250918/odoo/addons/maintenance/views/maintenance_views.xml)

## 4. Module chuẩn được dùng

Các module chuẩn đang được tận dụng trong bước này là:

- `maintenance`
- `hr`

Phần chuẩn Odoo được dùng làm nền:

- model `maintenance.request`
- model `hr.department`
- form view của `maintenance.request`
- list view của `maintenance.request`
- search view của `maintenance.request`
- field chuẩn `priority`

## 5. Những gì đã code

### 5.1. Bổ sung field phòng ban cửa hàng trên `maintenance.request`

Đã thêm field:

- `x_0502_department_id`

Loại dữ liệu:

- `Many2one`

Model liên kết:

- `hr.department`

Mục đích:

- Ghi nhận phòng ban đại diện cho cửa hàng phát sinh yêu cầu
- Bám đúng cách tổ chức dữ liệu thực tế của hệ thống
- Tránh việc nhập tay mã cửa hàng dễ sai
- Tạo nền dữ liệu tốt hơn cho lọc, tìm kiếm, báo cáo và phân quyền

File liên quan:

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)

### 5.2. Thiết lập mặc định phòng ban theo người tạo yêu cầu

Đã thêm logic mặc định:

- lấy `employee_id.department_id` từ user hiện tại

Ý nghĩa:

- Nếu user có employee và employee có department, phiếu sẽ tự đổ phòng ban
- Nếu user không có department, field vẫn để trống để người dùng chọn tay

Lợi ích:

- Giảm thao tác nhập liệu
- Bám sát thực tế “người gửi yêu cầu thuộc cửa hàng nào thì phiếu thuộc cửa hàng đó”

### 5.3. Bổ sung field loại yêu cầu trên `maintenance.request`

Đã thêm field:

- `x_0502_request_type_id`

Loại dữ liệu:

- `Many2one`

Model liên kết:

- `x_0502.request.type`

Mục đích:

- Phân loại yêu cầu theo góc nhìn nghiệp vụ `0502`
- Tránh fix cứng giá trị trong code
- Cho phép mở rộng loại yêu cầu về sau mà không phải sửa Python

File liên quan:

- [maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)

### 5.4. Tạo model master data cho loại yêu cầu

Đã tạo model:

- `x_0502.request.type`

File:

- [request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)

Các field chính:

- `name`
- `code`
- `sequence`
- `active`

Ý nghĩa:

- Đây là danh mục loại yêu cầu cho `0502`
- Có thể quản lý theo dữ liệu thay vì hard-code

### 5.5. Tạo dữ liệu mẫu ban đầu cho loại yêu cầu

Đã thêm dữ liệu khởi tạo:

- `Maintenance`
- `Repair`
- `Inspection`

File:

- [request_type_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/request_type_data.xml)

Ý nghĩa:

- Có dữ liệu để test ngay sau khi upgrade module
- Là bộ giá trị tối thiểu, chưa phải danh mục cuối cùng

### 5.6. Giữ lại phần nguồn phát sinh đã làm ở bước 1

Các field vẫn đang được dùng:

- `x_0502_request_source_id`
- `x_0502_request_source_code`

Ý nghĩa:

- Vẫn bảo toàn được khả năng phân biệt:
  - `Store Request`
  - `Preventive Schedule`
- Search filter vẫn hoạt động ổn định

### 5.7. Cập nhật giao diện `maintenance.request`

Đã cập nhật:

- form view
- list view
- search view

File:

- [maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

Những gì đã hiển thị thêm:

- `Store Department`
- `Request Type`
- `Request Source`

Ý nghĩa:

- Người dùng đã có thể nhập các thông tin tối thiểu của phiếu yêu cầu bảo trì
- Có thể tìm kiếm nhanh theo phòng ban, loại yêu cầu, nguồn phát sinh

### 5.8. Cập nhật manifest và quyền truy cập

Đã cập nhật:

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)

Nội dung chính:

- Load thêm `request_type_data.xml`
- Cấp quyền cho model `x_0502.request.type`
- Bổ sung dependency `hr` vì hiện tại module dùng trực tiếp `hr.department`

## 6. Những gì đã thay đổi so với thiết kế ban đầu

Thiết kế ban đầu:

- dùng `x_0502_store_code: Char`

Thiết kế hiện tại:

- dùng `x_0502_department_id: Many2one('hr.department')`

Ý nghĩa của thay đổi này:

- dữ liệu chặt hơn
- ít nhập sai hơn
- phù hợp hơn với mô hình tổ chức thực tế
- tránh phải duy trì một mã cửa hàng text riêng trong `0502`

## 7. Những gì không làm trong bước 2

Để giữ đúng phạm vi `Phase 1 - Bước 2`, các nội dung sau chưa được triển khai:

- Chưa tạo model riêng cho phiếu yêu cầu bảo trì
- Chưa tạo model store riêng
- Chưa làm approval ở bước tạo phiếu
- Chưa thêm logic kiểm tra tính hợp lệ phức tạp giữa các field
- Chưa sinh số chứng từ riêng cho 0502
- Chưa tạo menu riêng cho nhập phiếu 0502
- Chưa làm workflow xử lý sau khi tạo phiếu

## 8. Vì sao cách làm này phù hợp với Phase 1

Hướng triển khai này phù hợp với `Phase 1` vì:

- Giữ `maintenance.request` làm chứng từ đầu vào thống nhất
- Bổ sung đúng lượng thông tin nghiệp vụ cần thiết
- Không tạo thêm object thừa
- Không tự đẩy dự án sang custom nặng quá sớm
- Đồng thời vẫn điều chỉnh được theo cấu trúc dữ liệu thực tế của hệ thống

Nói ngắn gọn:

- Bước 2 làm cho phiếu yêu cầu bảo trì “đủ dùng” hơn cho `0502`
- Nhưng vẫn còn nằm trong biên an toàn của chuẩn Odoo

## 9. Dữ liệu mẫu nên dùng để test bước 2

### Trường hợp 1 - Yêu cầu phát sinh từ cửa hàng

- `Request`: `Cửa hàng Q1 - Máy lạnh quầy thu ngân không mát`
- `Equipment`: `Máy lạnh quầy thu ngân - CH Q1`
- `Store Department`: chọn phòng ban của cửa hàng Q1
- `Request Type`: `Repair`
- `Request Source`: `Store Request`
- `Maintenance Type`: `Corrective`
- `Priority`: `High`

### Trường hợp 2 - Yêu cầu từ lịch bảo trì định kỳ

- `Request`: `Bảo trì định kỳ tháng 4 - Máy lạnh quầy thu ngân CH Q1`
- `Equipment`: `Máy lạnh quầy thu ngân - CH Q1`
- `Store Department`: chọn phòng ban của cửa hàng Q1
- `Request Type`: `Maintenance`
- `Request Source`: `Preventive Schedule`
- `Maintenance Type`: `Preventive`
- `Priority`: `Normal`

## 10. Điều cần test ở bước 2

Sau khi upgrade module, cần test các điểm sau:

- Tạo được `maintenance.request` mới mà không lỗi
- Field `Store Department` tự đổ mặc định nếu user có department
- Nếu user không có department thì vẫn chọn tay được
- Chọn được `Request Type`
- `Request Source` vẫn hoạt động đúng như bước 1
- Lưu record thành công
- Mở lại record vẫn giữ nguyên dữ liệu
- List view hiển thị đúng các cột mới
- Search view tìm và lọc được theo các field mới

## 11. Tác động lên các bước sau

Sau khi hoàn thành bước 2, các bước sau có nền dữ liệu tốt hơn:

- Bước 3 có thể tiếp nhận yêu cầu rõ ràng hơn theo phòng ban và loại yêu cầu
- Bước 7, 8 có thể tổng hợp theo phòng ban hoặc loại yêu cầu
- Bước 10 có thể báo cáo theo các chiều dữ liệu cơ bản

Điều này giúp `Phase 1` tiếp tục giữ đúng nguyên tắc:

- phát triển từ từ
- bám sát quy trình
- kiểm soát được phạm vi code

## 12. File đã thay đổi trong bước 2

- [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/__manifest__.py)
- [models/__init__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/__init__.py)
- [models/maintenance_request.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/maintenance_request.py)
- [models/request_type.py](/d:/odoo-19.0+e.20250918/addons/M02_P0502/models/request_type.py)
- [data/request_type_data.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/data/request_type_data.xml)
- [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0502/security/ir.model.access.csv)
- [views/maintenance_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0502/views/maintenance_request_views.xml)

## 13. Kết luận

`Phase 1 - Bước 2` đã được triển khai theo đúng tinh thần:

- tiếp tục dùng `maintenance.request` làm phiếu đầu vào
- bổ sung dữ liệu nghiệp vụ tối thiểu
- giữ `priority` của chuẩn Odoo
- không tạo model phiếu riêng
- điều chỉnh từ `store_code` sang `department_id` để bám dữ liệu thực tế của hệ thống

Đây là bước giúp chứng từ đầu vào của `0502` trở nên rõ ràng hơn, đủ để chuyển sang các bước tiếp theo như tiếp nhận yêu cầu, tổng hợp và lập kế hoạch.
