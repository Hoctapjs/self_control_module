# Hướng dẫn thao tác sử dụng quy trình xử lý kỷ luật nhân viên 0215

Ngày cập nhật: 2026-05-13

## 1. Mục đích tài liệu

Tài liệu này hướng dẫn thao tác sử dụng module `M02_P0215` theo từng bước trong quy trình xử lý kỷ luật nhân viên.

Tài liệu bám theo:

- quy trình nghiệp vụ trong `QUY_TRINH_XU_LY_KY_LUAT_NHAN_VIEN_0215.md`
- luồng hệ thống hiện tại của module sau các phase refactor `approval` và `survey`

## 2. Vai trò tham gia

- Quản lý cửa hàng / Quản lý trực tiếp: tạo hồ sơ, gửi yêu cầu tường trình, chốt nội dung ban đầu
- RGM: kiểm tra tái phạm, xác định nhánh xử lý
- HRBP: xử lý nhánh cấp công ty, sắp xếp họp, chốt đề xuất
- HR Manager / người duyệt: duyệt hồ sơ cấp công ty qua `Approvals`
- Nhân viên: làm tường trình, xác nhận hoặc từ chối quyết định

## 3. Màn hình sử dụng chính

- Backoffice:
  - menu hồ sơ kỷ luật `x_psm.hr.discipline.record`
- Portal:
  - danh sách hồ sơ của nhân viên
  - trang chi tiết hồ sơ
  - link survey tường trình
  - link survey feedback
- Module dùng chung:
  - `Approvals` để duyệt cấp công ty
  - `Survey` để làm tường trình và feedback

## 4. Nguyên tắc đọc trạng thái

Các trạng thái chính của hồ sơ:

- `draft`: khởi tạo
- `under_review`: chờ RGM xem xét
- `level_determination`: xác định cấp xử lý
- `investigation`: xác minh cấp công ty
- `hearing`: họp kỷ luật
- `proposal`: đã có đề xuất xử lý
- `issued`: đã ban hành quyết định
- `approval`: đang chờ duyệt cấp công ty
- `notified`: đã thông báo cho nhân viên
- `active`: đang hiệu lực
- `expired`: hết hiệu lực

## 5. Hướng dẫn theo từng bước

### Bước 1 - Nhân viên phát sinh lỗi

Người thực hiện:

- Quản lý ghi nhận sự việc ngoài thực tế

Thao tác trên hệ thống:

- Chưa thao tác ngay ở bước này

Kết quả:

- Có thông tin đầu vào để tạo hồ sơ ở bước 2

---

### Bước 2 - Quản lý ghi nhận và tạo hồ sơ

Người thực hiện:

- Quản lý cửa hàng / quản lý trực tiếp

Thao tác:

1. Vào danh sách hồ sơ kỷ luật.
2. Tạo mới hồ sơ.
3. Nhập các thông tin:
   - Nhân viên
   - Danh mục vi phạm
   - Loại vi phạm
   - Mô tả tình huống vi phạm
   - Mục đích xử lý
4. Bấm `Gửi yêu cầu tường trình`.

Hệ thống xử lý:

- Tạo hoặc gắn `survey` tường trình cho hồ sơ
- Gửi email cho nhân viên
- Tạo activity yêu cầu nhân viên làm tường trình

Kết quả mong đợi:

- Hồ sơ vẫn ở `draft`
- Nhân viên nhận được link survey tường trình

---

### Bước 3 - Nhân viên làm tường trình

Người thực hiện:

- Nhân viên

Thao tác:

1. Mở email hoặc portal.
2. Bấm link survey tường trình.
3. Điền đầy đủ các nội dung:
   - Thời gian xảy ra sự việc
   - Địa điểm
   - Người chứng kiến
   - Nội dung tường trình
   - Nguyên nhân
   - Cam kết cải thiện
   - Xác nhận nội dung
4. Gửi survey.

Hệ thống xử lý:

- Lưu `survey.user_input`
- Đồng bộ nội dung chính về hồ sơ
- Tạo snapshot lịch sử vào `x_psm.hr.discipline.explanation`

Kết quả mong đợi:

- Hồ sơ có dữ liệu phần tường trình
- Smart button survey hiển thị trạng thái đã hoàn tất

---

### Bước 4 - Quản lý kiểm tra và xác nhận tường trình

Người thực hiện:

- Quản lý cửa hàng / quản lý trực tiếp

Thao tác:

1. Mở lại hồ sơ ở backoffice.
2. Kiểm tra phần mô tả, tường trình, hình ảnh đính kèm nếu có.
3. Nếu cần yêu cầu làm lại:
   - bấm `Từ chối / Yêu cầu lại`
   - nhập lý do từ chối
4. Nếu thông tin đã đủ:
   - nhập/chốt các nội dung cần thiết
   - bấm `Gửi RGM Xem xét`

Hệ thống xử lý khi từ chối:

- Tạo survey tường trình mới
- Gửi lại email cho nhân viên
- Ghi nhận lý do từ chối

Hệ thống xử lý khi xác nhận:

- Chuyển hồ sơ sang `under_review`
- Tạo activity cho RGM

---

### Bước 5 - Kiểm tra tái phạm

Người thực hiện:

- RGM xem hồ sơ
- Hệ thống hỗ trợ tính dữ liệu tái phạm

Thao tác:

1. RGM mở hồ sơ ở trạng thái `under_review`.
2. Kiểm tra cảnh báo tái phạm và hồ sơ liên quan nếu có.

Hệ thống xử lý:

- Tự tính số hồ sơ trước đó của nhân viên
- Hiển thị cờ tái phạm nếu còn trong thời hạn theo dõi

---

### Bước 6 - Xác định có xử lý feedback ngay hay không

Người thực hiện:

- RGM

Thao tác:

- Nếu không cần đi nhánh kỷ luật chính thức, bấm `Không tái phạm → Feedback`
- Nếu cần xử lý tiếp theo nhánh đầy đủ, bấm `Có tái phạm`

Kết quả:

- `Không tái phạm → Feedback`:
  - hồ sơ sang `proposal`
  - tự tạo survey feedback
  - mở ngay survey feedback
- `Có tái phạm`:
  - hồ sơ sang `level_determination`

---

### Bước 7 - RGM xác định cấp xử lý

Người thực hiện:

- RGM

Điều kiện:

- Hồ sơ đang ở `level_determination`

Thao tác:

- Bấm `Store Level` nếu xử lý ở cấp cửa hàng
- Bấm `Company Level` nếu chuyển lên cấp công ty

Kết quả:

- `Store Level`:
  - hồ sơ sang `proposal`
- `Company Level`:
  - hồ sơ sang `investigation`

---

## 6. Nhánh A - Xử lý cấp cửa hàng

### Bước 8 - Xác định hình thức và thời gian xử lý

Người thực hiện:

- RGM / quản lý theo phân quyền

Thao tác:

1. Mở hồ sơ ở `proposal`.
2. Chọn `Hình thức kỷ luật`.
3. Kiểm tra thời hạn hiệu lực dự kiến theo action.
4. Bấm `Ban hành Quyết định`.

Kết quả:

- Hồ sơ sang `issued`
- Có ngày ban hành

---

### Bước 18 - Nhân viên xác nhận quyết định

Người thực hiện:

- Nhân viên

Thao tác:

1. Sau khi quản lý bấm `Trình duyệt / Thông báo NV`, hồ sơ Store Level sẽ sang `notified`.
2. Nhân viên vào portal.
3. Chọn:
   - `Chấp nhận`
   - hoặc `Từ chối` và nhập lý do

Kết quả:

- `Chấp nhận`:
  - hồ sơ sang `active`
- `Từ chối`:
  - hồ sơ quay lại `proposal`

---

## 7. Nhánh B - Xử lý cấp công ty

### Cấu hình người duyệt cấp công ty

Người thực hiện:

- HR Manager

Mục đích:

- Cấu hình danh sách người duyệt cho approval category `0215 - Phê duyệt kỷ luật cấp công ty`
- Cho phép HR tự thêm/sửa/xóa người duyệt mà không cần sửa code

Thao tác:

1. HR Manager vào app `Approvals`.
2. Vào `Configuration > Approval Categories`.
3. Mở `0215 - Phê duyệt kỷ luật cấp công ty`.
4. Tại tab `Approvers`, thêm/sửa/xóa người duyệt.
5. Với từng người duyệt, kiểm tra:
   - `Required`: người này có bắt buộc duyệt hay không
   - `Sequence`: thứ tự duyệt
6. Nếu cần, chỉnh:
   - `Minimum Approval`
   - `Approvers Sequence`
   - `Employee's Manager`

Lối tắt:

- Trên form hồ sơ 0215 cấp công ty, HR Manager có thể bấm smart button `Approvers 0215` để mở thẳng category cấu hình.

Lưu ý:

- Hệ thống không seed cứng approver mặc định.
- Nếu category chưa có người duyệt và không bật `Employee's Manager`, khi bấm `Trình duyệt / Thông báo NV` hệ thống sẽ báo lỗi yêu cầu cấu hình approver.
- Không cần tạo model cấu hình riêng và không cần tạo group bảo mật mới.

---

### Bước 9 - OC / HR tiếp nhận và đề xuất

Người thực hiện:

- HRBP / bộ phận liên quan

Điều kiện:

- Hồ sơ ở `investigation`

Thao tác:

- Kiểm tra hồ sơ, tài liệu, mức độ vi phạm
- Chuẩn bị hướng xử lý

Lưu ý:

- Trong hệ thống hiện tại, phần phối hợp OC/HR chưa tách thành task riêng; chủ yếu thao tác trên chính hồ sơ

---

### Bước 10 - HR sắp xếp lịch họp

Người thực hiện:

- HRBP

Thao tác:

1. Từ hồ sơ, bấm smart button `Meetings`.
2. Tạo cuộc họp liên quan hồ sơ.
3. Hoặc dùng nút `Cần họp kỷ luật`.

Kết quả:

- Hồ sơ sang `hearing` nếu cần họp
- Có liên kết `calendar.event`

Nếu không cần họp:

- Bấm `Không cần họp → Đề xuất`
- Hồ sơ sang `proposal`

---

### Bước 11 - Công đoàn tham gia

Người thực hiện:

- Công đoàn và các bên liên quan ngoài hệ thống

Thao tác trên hệ thống:

- Ghi nhận kết quả vào nội dung họp / đề xuất trên hồ sơ

Lưu ý:

- Module hiện chưa có bước workflow riêng cho Công đoàn

---

### Bước 12 - Kế toán xác định bồi thường

Người thực hiện:

- HRBP / Kế toán theo phân công

Thao tác:

1. Trên hồ sơ cấp công ty, đánh dấu `Có bồi thường` nếu có.
2. Nhập `Giá trị bồi thường`.
3. Nếu cần, tạo file quyết định đền bù.

Kết quả:

- Dữ liệu bồi thường được lưu trên hồ sơ

---

### Bước 13 - Tổng hợp biên bản và chốt đề xuất

Người thực hiện:

- HRBP

Thao tác:

1. Hoàn thiện:
   - Nội dung họp
   - Biên bản họp
   - Hình thức xử lý
   - File quyết định nếu cần
2. Khi đã chốt action xử lý, bấm `Ban hành Quyết định`.

Kết quả:

- Hồ sơ sang `issued`

---

### Bước 14 - Duyệt cấp công ty

Người thực hiện:

- HR Manager / người duyệt trong `Approvals`

Thao tác:

1. Từ hồ sơ `issued`, bấm `Trình duyệt / Thông báo NV`.
2. Hệ thống tạo `approval.request`.
3. Hệ thống lấy danh sách người duyệt từ category `0215 - Phê duyệt kỷ luật cấp công ty`.
4. Người duyệt mở app `Approvals` hoặc smart button `Approval`.
5. Thực hiện:
   - `Approve`
   - hoặc `Refuse`

Kết quả:

- Nếu duyệt:
  - hồ sơ sang `notified`
- Nếu từ chối:
  - hồ sơ quay lại `proposal`

---

### Bước 15 - Hệ thống phân loại luồng sau duyệt

Người thực hiện:

- Hệ thống

Thao tác:

- Không cần thao tác tay

Kết quả:

- Company Level tiếp tục sang bước thông báo nhân viên
- Store Level không dùng bước duyệt `Approvals`

---

### Bước 16 - Tiếp tục quy trình cấp công ty

Người thực hiện:

- HRBP / quản lý / nhân viên

Thao tác:

- Sau khi `Approvals` duyệt, theo dõi hồ sơ ở `notified`
- Chuyển sang bước nhân viên xác nhận trên portal

---

## 8. Nhánh feedback cải thiện ngay

### Bước 17 - Trao đổi cải thiện ngay

Người thực hiện:

- RGM / quản lý được phân quyền

Điều kiện:

- Đã bấm `Không tái phạm → Feedback`

Thao tác:

1. Survey feedback được mở ra.
2. Điền các nội dung:
   - Vấn đề cần cải thiện
   - Nguyên nhân
   - Hướng dẫn đã trao đổi
   - Cam kết của nhân viên
   - Thời gian theo dõi
   - Kết quả sau theo dõi nếu có
3. Gửi survey feedback.

Hệ thống xử lý:

- Đồng bộ dữ liệu feedback về hồ sơ
- Cập nhật các phần:
   - `III. Xác định hành vi vi phạm`
   - `IV. Nội dung hai bên đồng ý`
- Chuyển hồ sơ sang `active`

Kết quả:

- Hồ sơ bước vào thời gian theo dõi cải thiện

---

## 9. Bước cuối cùng

### Bước 19 - Theo dõi hiệu lực và kết thúc

Người thực hiện:

- Hệ thống và HR/Quản lý

Thao tác:

1. Theo dõi `Ngày bắt đầu`, `Ngày hết hiệu lực`, `Ngày hiệu lực còn lại`.
2. Khi đến hạn:
   - hệ thống cron có thể tự chuyển sang `expired`
   - hoặc người dùng bấm `Đánh dấu Hết hiệu lực`

Kết quả:

- Hồ sơ sang `expired`
- Dữ liệu vẫn được giữ để tra cứu tái phạm về sau

## 10. Các tình huống thường gặp

### 10.1. Nhân viên chưa thấy survey tường trình

Kiểm tra:

- hồ sơ đã bấm `Gửi yêu cầu tường trình` chưa
- email nhân viên có đúng không
- hồ sơ có smart button survey chưa

### 10.2. Tường trình cần làm lại

Thao tác:

- quản lý bấm `Từ chối / Yêu cầu lại`
- nhập lý do từ chối

Kết quả:

- hệ thống tạo survey mới và gửi lại cho nhân viên

### 10.3. Hồ sơ cấp công ty chưa có approval request

Kiểm tra:

- hồ sơ đã ở `issued` chưa
- đã chọn `Company Level` chưa
- đã bấm `Trình duyệt / Thông báo NV` chưa

### 10.4. Hồ sơ cũ cần bridge sang luồng mới

Người thực hiện:

- HR Manager

Thao tác:

- bấm `Bridge dữ liệu cũ`

Kết quả:

- hệ thống ghi trạng thái migrate trong phần `Migration`

### 10.5. Trình duyệt báo chưa có người duyệt

Nguyên nhân thường gặp:

- approval category `0215 - Phê duyệt kỷ luật cấp công ty` chưa có approver
- category chưa bật `Employee's Manager`
- người duyệt không thuộc công ty hiện tại hoặc là portal/share user

Thao tác:

- HR Manager bấm smart button `Approvers 0215` trên hồ sơ cấp công ty
- hoặc vào `Approvals > Configuration > Approval Categories`
- mở category `0215 - Phê duyệt kỷ luật cấp công ty`
- thêm ít nhất một approver hợp lệ, hoặc bật `Employee's Manager` nếu quy trình cho phép duyệt theo quản lý trực tiếp

## 11. Khuyến nghị sử dụng

- Hồ sơ mới nên đi theo đúng luồng `survey` và `approvals`
- Chỉ dùng các route/nhập liệu legacy khi thật sự cần tương thích dữ liệu cũ
- Trước khi ban hành hoặc trình duyệt, luôn kiểm tra:
  - action xử lý
  - cấp xử lý
  - tài liệu đính kèm
  - trạng thái survey/approval
