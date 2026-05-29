# Hướng dẫn sử dụng module dữ liệu mẫu 0215

## 1. Mục đích

Module `M02_P0215_DEMO_DATA` dùng để cài nhanh bộ dữ liệu mẫu phục vụ:

- test nghiệp vụ module `M02_P0215`
- demo luồng thao tác cho người dùng
- UAT sau các phase refactor `approval` và `survey`

Module này không thay thế dữ liệu master của `M02_P0215`. Nó chỉ bổ sung:

- nhân sự demo theo các vai trò chính
- hồ sơ kỷ luật demo ở các trạng thái tiêu biểu
- một bản lịch sử tường trình mẫu

## 2. Tài khoản demo

Mật khẩu mặc định cho toàn bộ tài khoản là `123`.

- `demo0215_rgm`: RGM
- `demo0215_sm`: Shift Manager
- `demo0215_hrbp`: HRBP
- `demo0215_hrmgr`: HR Manager / approver
- `demo0215_emp_a`: Nhân viên A
- `demo0215_emp_b`: Nhân viên B

## 3. Hồ sơ mẫu nên dùng cho từng kịch bản

### 3.1. Tạo mới hồ sơ

Mở hồ sơ `DEMO-0215-DRAFT`.

Kịch bản phù hợp:

- kiểm tra màn hình nhập liệu ban đầu
- thử chỉnh nhân viên, loại vi phạm, mô tả vi phạm
- thử bấm gửi tường trình

### 3.2. RGM xác định tái phạm / không tái phạm

Mở hồ sơ `DEMO-0215-UNDER-REVIEW`.

Kịch bản phù hợp:

- bấm nhánh `Có tái phạm`
- bấm nhánh `Không tái phạm -> Feedback`
- kiểm tra logic repeat offense vì cùng nhân viên đã có hồ sơ lịch sử `DEMO-0215-EXPIRED`

### 3.3. Trình approval cấp công ty

Mở hồ sơ `DEMO-0215-COMPANY-ISSUED`.

Kịch bản phù hợp:

- dùng vai trò HRBP hoặc HR Manager để kiểm tra hồ sơ
- bấm `Submit for Approval`
- xác nhận hệ thống tạo `approval.request`

### 3.4. Nhân viên phản hồi quyết định

Mở hồ sơ `DEMO-0215-NOTIFIED`.

Kịch bản phù hợp:

- thử nhánh chấp nhận
- thử nhánh từ chối
- kiểm tra việc quay lại `proposal` khi từ chối

### 3.5. Kiểm tra hồ sơ đang hiệu lực

Mở hồ sơ `DEMO-0215-ACTIVE-FEEDBACK`.

Kịch bản phù hợp:

- xem nội dung feedback đã đồng bộ vào phần nhận diện vi phạm và thỏa thuận hai bên
- kiểm tra ngày bắt đầu hiệu lực và ngày hết hiệu lực tính theo action

### 3.6. Kiểm tra lịch sử tái phạm

Mở hồ sơ `DEMO-0215-EXPIRED`.

Kịch bản phù hợp:

- đối chiếu hồ sơ lịch sử của cùng nhân viên
- dùng làm record nền để test logic gợi ý hình thức xử lý và repeat offense

## 4. Ghi chú

- Module này được thiết kế để cài trên môi trường test/UAT.
- Vì là dữ liệu mẫu, không nên cài trực tiếp trên môi trường production.
- Nếu cần nhiều kịch bản hơn, có thể tạo thêm record mới dựa trên bộ nhân sự demo này thay vì tạo thêm user mới.
