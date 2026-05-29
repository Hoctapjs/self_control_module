# Quy trình xử lý kỷ luật nhân viên - 0215

## Đặc tả dễ hiểu

Quy trình xử lý kỷ luật nhân viên bắt đầu khi nhân viên phát sinh lỗi trong quá trình làm việc. Quản lý là người ghi nhận sự việc, phân loại lỗi ban đầu và chuyển thông tin cho nhân viên để nhân viên viết bản tường trình. Sau khi nhân viên hoàn tất tường trình, quản lý kiểm tra lại nội dung, xác nhận tính đầy đủ của thông tin và chuẩn bị chuyển hồ sơ sang bước xử lý tiếp theo.

Sau giai đoạn ghi nhận, hệ thống sẽ hỗ trợ kiểm tra dữ liệu tái phạm của nhân viên trong thời gian cải thiện đã được cấu hình trước. Việc kiểm tra này giúp quản lý biết nhân viên có đang lặp lại lỗi trong khoảng thời gian theo dõi hay không. Dựa trên dữ liệu đầu vào của MIC, hệ thống xác định trường hợp nào cần phản hồi ngay. Nếu cần phản hồi ngay, quản lý ca sẽ trao đổi trực tiếp với nhân viên để cải thiện hiệu quả công việc. Nếu không thuộc trường hợp phản hồi ngay, hồ sơ sẽ được chuyển sang bước xác nhận cấp độ kỷ luật.

Ở bước xác nhận cấp độ, RGM/RDM quyết định vụ việc được xử lý ở cấp cửa hàng hay cấp công ty. Nếu là cấp cửa hàng, RGM/RDM trực tiếp xác định hình thức kỷ luật và thời gian áp dụng, sau đó chuyển sang bước nhân viên xác nhận và ký biên bản. Nếu là cấp công ty, hồ sơ sẽ được chuyển cho các bộ phận liên quan như OC, HR, Công đoàn và Kế toán. OC phối hợp cùng HR để đề xuất hình thức kỷ luật, HR sắp xếp lịch họp, Công đoàn tham gia xác định hình thức xử lý, còn Kế toán định giá bồi thường nếu có thiệt hại vật chất.

Sau khi các bên liên quan thống nhất, kết quả xử lý được tổng hợp vào biên bản họp để trình CEO. CEO xem xét quyết định kỷ luật và nội dung đền bù nếu có. Nếu CEO đồng ý, quy trình tiếp tục sang bước ban hành và ký xác nhận. Nếu CEO không đồng ý, hồ sơ quay lại bước tổng hợp để điều chỉnh. Sau khi được phê duyệt, hệ thống tiếp tục phân loại luồng theo cấp xử lý để đảm bảo hồ sơ đi đúng nhánh: cấp công ty tiếp tục phần xử lý của công ty, còn cấp cửa hàng chuyển đến bước nhân viên xác nhận.

Kết thúc quy trình, nhân viên xác nhận và ký các biên bản kỷ luật. Nếu nhân viên đồng ý, hồ sơ hoàn tất phần ký kết. Nếu nhân viên từ chối, kết quả được phản hồi lại về bước tổng hợp để xem xét và xử lý lại. Khi hồ sơ đã hoàn tất, hệ thống cập nhật hình thức kỷ luật và thời gian kỷ luật vào hồ sơ nhân viên. Thời gian kỷ luật được tính từ ngày RGM xác nhận đã trao đổi với nhân viên.

## I. Giai đoạn ghi nhận và tường trình

**Bước 1:** Nhân viên phát sinh lỗi trong quá trình làm việc.

**Bước 2:** Quản lý phát hiện, ghi nhận thông tin trong ca và thực hiện phân loại lỗi.

**Bước 3:** Nhân viên tiếp nhận thông tin và viết bản tường trình dựa trên phiếu ghi nhận từ quản lý.

**Bước 4:** Quản lý kiểm tra và xác nhận bản tường trình trước khi luân chuyển sang bộ phận khác.

## II. Giai đoạn kiểm tra và phân loại xử lý

**Bước 5:** Hệ thống tự động kiểm tra số lần tái phạm trong thời gian cải thiện, dựa trên cấu hình sẵn, để quản lý theo dõi dữ liệu (tracking data).

**Bước 6:** Hệ thống dựa trên dữ liệu đầu vào của MIC để xác định trường hợp cần phản hồi (feedback) ngay lập tức:

- **Trường hợp 1 (YES):** Tiến hành **Bước 17** - Trao đổi cải thiện ngay.
- **Trường hợp 2 (NO):** Tiến hành **Bước 7**.

**Bước 7:** RGM/RDM xác nhận cấp độ kỷ luật:

- **Nhánh 1: Cấp cửa hàng (Store Level):** Tiến hành **Bước 8**.
- **Nhánh 2: Cấp công ty (Company Level):** Tiến hành **Bước 9, 10, 11, 12**.

## III. Quy trình xử lý chi tiết

### Nhánh A: Xử lý cấp cửa hàng (Store Level)

**Bước 8:** RGM/RDM trực tiếp xác định hình thức và thời gian kỷ luật, sau đó chuyển đến **Bước 18**.

### Nhánh B: Xử lý cấp công ty (Company Level)

**Bước 9:** Bộ phận OC tiếp nhận thông báo, phối hợp cùng HR để đề xuất hình thức kỷ luật.

**Bước 10:** HR sắp xếp lịch họp giữa các bên liên quan tùy theo tính chất lỗi.

**Bước 11:** Công đoàn tham gia vào quá trình xác định hình thức kỷ luật.

**Bước 12:** Kế toán tham gia định giá bồi thường nếu có phát sinh thiệt hại vật chất.

**Bước 13:** Tổng hợp, xác nhận hình thức và thời gian xử lý vào biên bản họp để trình CEO.

## IV. Giai đoạn phê duyệt và ban hành

**Bước 14:** CEO xem xét phê duyệt quyết định kỷ luật và đền bù:

- **Đồng ý (YES):** Tiến hành **Bước 15**.
- **Từ chối (NO):** Quay lại **Bước 13** để điều chỉnh.

**Bước 15:** Hệ thống phân loại lại luồng thực hiện:

- **Company Level:** Tiến hành **Bước 16**.
- **Store Level:** Tiến hành **Bước 18**.

**Bước 16:** Tiếp tục quy trình cấp công ty.

**Bước 17:** Quản lý ca và nhân viên trao đổi trực tiếp để cải thiện hiệu quả công việc.

**Bước 18:** Nhân viên xác nhận và ký các biên bản kỷ luật:

- **Đồng ý (YES):** Hoàn tất ký kết.
- **Từ chối (NO):** Phản hồi lại kết quả về **Bước 13**.

**Bước 19:** Cập nhật hình thức và thời gian kỷ luật vào hồ sơ nhân viên. Thời gian tính từ ngày RGM xác nhận trao đổi với nhân viên.
