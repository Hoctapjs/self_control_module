# Plan Triển Khai Quy Trình 0502 Theo Phase

## 1. Mục đích

Tài liệu này dùng để định hướng cách triển khai quy trình `0502 - Quản lý bảo trì` theo hướng:

- Thiết kế theo bước
- Thực thi theo phase estimate

Mục tiêu là vừa giữ được cái nhìn xuyên suốt theo `21 bước` của quy trình, vừa kiểm soát được effort triển khai theo mức độ tận dụng chuẩn Odoo và mức độ custom.

## 2. Vì sao không nên chọn một trong hai cực

### 2.1. Nếu triển khai thuần theo estimate

#### Ưu điểm

- Nhanh ra sản phẩm
- Tận dụng chuẩn Odoo tốt
- Ít rủi ro ở giai đoạn đầu

#### Nhược điểm

- Dễ bị rời rạc giữa `maintenance`, `industry_fsm`, `stock`, `purchase`
- Về sau nhìn lại sẽ thấy có đủ chức năng nhưng chưa chắc đã thành một quy trình `0502` liền mạch
- Dễ tối ưu theo kỹ thuật trước khi chốt được logic nghiệp vụ xuyên suốt

### 2.2. Nếu triển khai thuần theo 21 bước

#### Ưu điểm

- Bám rất sát nghiệp vụ
- Dễ nhìn chỗ nào thiếu, chỗ nào nghẽn
- Thuận lợi để workshop với user và key user

#### Nhược điểm

- Rất dễ đụng ngay các bước custom nặng như approval, outside service, workflow xuyên suốt
- Tốc độ triển khai chậm hơn
- Dễ sa vào thiết kế lớn quá sớm

## 3. Nguyên tắc triển khai được đề xuất

Không nên hỏi:

- Triển khai theo estimate hay theo bước

Nên hỏi:

- Ở mỗi bước của quy trình, phần nào có thể làm ngay bằng chuẩn Odoo
- Ở mỗi bước của quy trình, phần nào cần custom nhẹ
- Ở mỗi bước của quy trình, phần nào cần custom sâu

Từ đó, nguyên tắc triển khai là:

- Dùng `21 bước` làm khung phân tích và kiểm soát phạm vi
- Dùng `estimate theo nhóm chuẩn/custom` để quyết định thứ tự triển khai
- Không cố hoàn thành trọn vẹn từng bước ngay từ đầu nếu bước đó đang phụ thuộc custom nặng

## 4. Cách hiểu câu “thiết kế theo bước, nhưng thực thi theo phase estimate”

### 4.1. Thiết kế theo bước

Khi phân tích solution, luôn lấy `21 bước của quy trình 0502` làm xương sống. Mỗi bước cần được trả lời rõ:

- Bước này đang do vai trò nào thực hiện
- Bước này dùng object nào làm trục chính
- Bước này dùng module chuẩn nào của Odoo
- Bước này có chứng từ, biểu mẫu, phê duyệt hay điều kiện rẽ nhánh gì
- Bước này đang là chuẩn Odoo, custom nhẹ, hay custom sâu

Lợi ích của cách này là:

- Không bị lạc luồng nghiệp vụ
- Không bỏ sót bước
- Dễ map từng bước với module chuẩn và phần custom

### 4.2. Thực thi theo phase estimate

Khi bắt tay triển khai thật, không làm kiểu hoàn thiện toàn bộ bước 1 rồi bước 2 rồi bước 3 theo đúng lưu đồ ngay từ đầu. Thay vào đó:

- Ưu tiên làm trước các phần có thể chạy bằng chuẩn Odoo
- Sau đó xử lý các phần custom nhẹ và custom vừa
- Cuối cùng mới xử lý các phần custom nặng hoặc mang tính workflow tổng thể

Lợi ích của cách này là:

- Có thể ra được luồng chạy end-to-end sớm
- Giảm rủi ro bị kẹt ở các bước khó
- Có cơ sở để demo, workshop và hiệu chỉnh dần với user

## 5. Mô hình triển khai theo 3 lớp

Với từng bước trong 21 bước, chia nội dung triển khai thành 3 lớp:

### 5.1. Lớp 1 - Có thể chạy bằng chuẩn Odoo

Đây là phần nên ưu tiên đưa vào `Phase 1`.

Ví dụ:

- Quản lý thiết bị và yêu cầu bảo trì bằng `maintenance`
- Tổ chức công việc hiện trường bằng `industry_fsm`
- Quản lý kho và xuất vật tư bằng `stock`
- Mua vật tư bổ sung bằng `purchase` và `purchase_stock`

### 5.2. Lớp 2 - Cần custom nhẹ hoặc custom vừa

Đây là phần nên ưu tiên đưa vào `Phase 2`.

Ví dụ:

- Mapping giữa các object như ticket, maintenance request, FSM task
- Approval riêng cho timeline và cost
- Cơ chế xác định vật tư phát sinh theo logic 0502
- Biểu mẫu nghiệm thu hoặc báo giá theo mẫu nghiệp vụ

### 5.3. Lớp 3 - Cần custom sâu

Đây là phần nên đưa vào `Phase 3`.

Ví dụ:

- Workflow 21 bước đầy đủ bám sát lưu đồ
- Object trục chính xuyên suốt toàn bộ quy trình
- Outside service flow riêng
- Bộ chứng từ đặc thù đồng bộ toàn quy trình

## 6. Đề xuất plan triển khai theo phase

### Phase 1 - Dựng luồng tối thiểu chạy được end-to-end

#### Mục tiêu

- Đi hết luồng `21 bước` ở mức tối thiểu
- Chấp nhận có bước chưa đẹp hoặc chưa bám đúng hoàn toàn theo nghiệp vụ chi tiết
- Nhưng phải tạo được đường đi từ đầu đến cuối

#### Ưu tiên module

- `maintenance`
- `industry_fsm`
- `stock`
- `purchase`
- `purchase_stock`
- `maintenance_worksheet` nếu cần checklist cơ bản

#### Hạng mục chính

- Thiết lập danh mục thiết bị và yêu cầu bảo trì
- Tạo flow tiếp nhận và xử lý yêu cầu ở mức cơ bản
- Tổ chức công việc sửa chữa/bảo trì cho kỹ thuật viên
- Kiểm tra tồn kho và xuất vật tư
- Tạo mua ngoài khi thiếu vật tư
- Ghi nhận hoàn thành và nghiệm thu cơ bản

#### Kết quả mong đợi

- Có thể demo được một quy trình xử lý từ phát sinh nhu cầu đến sửa chữa và nghiệm thu
- Xác định được các điểm đứt luồng giữa các module chuẩn
- Có dữ liệu thực tế để refine design ở phase sau

### Phase 2 - Làm mượt luồng và xử lý các điểm đứt

#### Mục tiêu

- Giảm khoảng trống giữa các module chuẩn
- Làm cho quy trình 0502 gần hơn với lưu đồ nghiệp vụ thực tế

#### Hạng mục chính

- Mapping object giữa `helpdesk`, `maintenance`, `industry_fsm`, `stock`
- Approval cho `timeline` và `cost`
- Xử lý logic vật tư phát sinh
- Bổ sung biểu mẫu nghiệm thu, kiểm tra, báo giá
- Bổ sung dashboard hoặc report theo dõi trạng thái xử lý

#### Kết quả mong đợi

- Luồng vận hành mượt hơn
- User nhìn thấy quy trình gần với thực tế hơn
- Có thể chốt rõ phần nào còn phải đầu tư custom sâu

### Phase 3 - Hoàn thiện solution đặc thù doanh nghiệp

#### Mục tiêu

- Bám sát hơn với lưu đồ 21 bước
- Hoàn thiện các phần custom nặng nếu thực sự cần

#### Hạng mục chính

- Workflow 21 bước đầy đủ
- Object trục chính xuyên suốt
- Outside service riêng
- Bộ chứng từ đặc thù
- Approval nhiều tầng nếu doanh nghiệp yêu cầu

#### Kết quả mong đợi

- Có solution bám rất sát quy trình nội bộ
- Tăng khả năng kiểm soát và truy vết toàn quy trình
- Đánh đổi bằng effort và độ phức tạp cao hơn

## 7. Cách dùng tài liệu này trong quá trình triển khai

Khi phân tích từng bước của 0502, luôn trả lời 4 câu hỏi:

1. Bước này có thể pass bằng chuẩn Odoo không
2. Nếu có thì đang dùng module nào
3. Nếu không thì cần custom ở mức thấp, vừa hay cao
4. Hạng mục đó nên đưa vào phase nào

Khi chốt scope với user hoặc quản lý dự án:

- Dùng `21 bước` để nói chuyện về nghiệp vụ
- Dùng `phase` để nói chuyện về effort và thứ tự triển khai

Khi estimate:

- Không estimate theo cảm tính toàn quy trình
- Estimate theo từng cụm chức năng trong từng phase
- Gắn từng hạng mục estimate về đúng bước của quy trình để tránh bị rời rạc

## 8. Kết luận

Với bài toán `0502`, hướng phù hợp nhất là:

- Không triển khai thuần theo estimate
- Không bám cứng từng bước ngay từ đầu
- Nên thiết kế theo bước để giữ đúng logic quy trình
- Nên thực thi theo phase estimate để kiểm soát effort và rủi ro

Cách làm an toàn là:

- Phase 1 dựng luồng tối thiểu bằng chuẩn Odoo
- Phase 2 xử lý các điểm đứt bằng custom nhẹ và vừa
- Phase 3 mới đầu tư vào workflow đặc thù và các custom nặng
