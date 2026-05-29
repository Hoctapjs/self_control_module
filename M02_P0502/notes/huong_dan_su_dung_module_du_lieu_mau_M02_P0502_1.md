# Hướng Dẫn Sử Dụng Module Dữ Liệu Mẫu `M02_P0502_1`

## 1. Mục đích

`M02_P0502_1` là module phụ dùng để nạp dữ liệu mẫu phục vụ test nhanh cho quy trình `0502`.

Mục tiêu của module này:

- không làm nặng module nghiệp vụ chính `M02_P0502`
- chỉ cài khi cần môi trường test/demo
- có sẵn dữ liệu phủ đến `Phase 1 - Bước 16`

## 2. Thứ tự cài đặt

1. `M02_P0502`
2. `M02_P0502_1`

Ý nghĩa:

- `M02_P0502`: chứa logic nghiệp vụ của quy trình 0502
- `M02_P0502_1`: chứa dữ liệu mẫu để test nhanh

## 3. Bộ dữ liệu mẫu hiện có

Module `M02_P0502_1` hiện tạo sẵn:

- partner mẫu cho cửa hàng/phòng ban
- phòng ban mẫu
- maintenance team mẫu
- category thiết bị mẫu
- thiết bị mẫu
- sản phẩm vật tư mẫu
- location kho mẫu cho bảo trì
- maintenance request mẫu từ `Bước 1` đến `Bước 16`
- FSM task mẫu
- stock picking và stock move mẫu
- activity mẫu cho preventive request

## 4. Dữ liệu master mẫu

### 4.1. Partner mẫu

- `GDH - CH Q1`
- `GDH - CH Q2`
- `GDH - Khoi Ky Thuat`

### 4.2. Phòng ban mẫu

- `CH Q1 - 2 Thang 9`
- `CH Q2 - Hai Ba Trung`
- `Khoi Van Phong Ky Thuat`

Mỗi phòng ban đã được map sẵn với partner qua field:

- `0502 FSM Customer`

### 4.3. Maintenance team mẫu

- `PSM Internal Maintenance`

Members:

- `Administrator`

### 4.4. Category thiết bị mẫu

- `May Lanh`
- `Tu Mat`
- `May In`

### 4.5. Thiết bị mẫu

- `May lanh quay thu ngan - CH Q1`
- `Tu mat nuoc uong - CH Q1`
- `May in hoa don POS 01 - CH Q1`
- `May lanh bep - CH Q2`

### 4.6. Vật tư mẫu

- `Ong thoat nuoc dieu hoa DEMO`
- `Dau in hoa don DEMO`
- `Gas bo sung may lanh DEMO`

### 4.7. Location kho mẫu

- `Maintenance Demo`

Location này dùng làm đích cho internal transfer mẫu ở các bước kho.

## 5. Request mẫu theo từng bước

### Nhóm bước 1 đến 7

- `Cua hang Q1 - May lanh quay thu ngan khong mat`
- `Cua hang Q1 - Tu mat keu to`
- `Cua hang Q1 - May in hoa don mo chu`
- `Cua hang Q2 - May lanh bep chay nuoc`
- `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`
- `Bao tri dinh ky thang 3 - May lanh bep CH Q2`

### Nhóm bước 8 đến 16

- `Bao tri thang 5 - Tu mat nuoc uong CH Q1`
- `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
- `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`
- `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`
- `Cua hang Q1 - Danh gia can thue ngoai thay board may in`
- `Cua hang Q1 - Xu ly noi bo khong can vat tu`
- `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
- `Cua hang Q1 - Khong du ton de thay dau in hoa don`

## 6. FSM task mẫu

Module seed tạo sẵn các FSM task cho các request cần điều phối/thực thi:

- `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
- `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
- `Cua hang Q1 - Khong du ton de thay dau in hoa don`

## 7. Stock picking mẫu

Module seed tạo sẵn các chứng từ kho mẫu:

- picking cho `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- picking cho `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
- picking cho `Cua hang Q1 - Khong du ton de thay dau in hoa don`

Trong đó:

- một request bước 15 dừng ở mức đã tạo picking
- hai request bước 16 đã được chạy logic kiểm tồn thật từ source của `M02_P0502`

## 8. Menu nên dùng để test

### 8.1. Maintenance Requests

Vào:

- `Maintenance > Maintenance > Maintenance Requests`

Dùng để test:

- request source
- request type
- receive
- inspection
- lead notified
- planned
- proposal
- approval
- service assessment
- material assessment
- stock check result

### 8.2. Queue tổng hợp bước 7

Vào:

- `Maintenance > Maintenance > 0502 Requests To Plan`

### 8.3. Execution Monitoring bước 10

Vào:

- `Maintenance > Reporting > 0502 Execution Monitoring`

### 8.4. Equipment

Vào:

- `Maintenance > Equipment`

Dùng để test:

- preventive schedule
- department trên thiết bị
- next preventive date
- last preventive request

### 8.5. Stock Picking

Từ request có thể mở qua:

- `Open Stock Picking`

Hoặc vào trực tiếp app:

- `Inventory > Operations`

## 9. Dữ liệu nào dùng cho từng bước

### Bước 1

- `Cua hang Q1 - May lanh quay thu ngan khong mat`

### Bước 2

- `Cua hang Q1 - May lanh quay thu ngan khong mat`
- `Cua hang Q1 - Tu mat keu to`

Điểm cần xem:

- `Request Source`
- `Request Type`
- `Store Department`

### Bước 3

- `Cua hang Q1 - Tu mat keu to`

Điểm cần xem:

- `Received By`
- `Received At`

### Bước 4

- `Cua hang Q1 - May in hoa don mo chu`
- `Cua hang Q2 - May lanh bep chay nuoc`

Điểm cần xem:

- `Initial Inspection Result`
- `Initial Inspection Note`
- `Inspected By`
- `Inspected At`

### Bước 5

- `May lanh quay thu ngan - CH Q1`
- `Tu mat nuoc uong - CH Q1`
- `May lanh bep - CH Q2`

Điểm cần xem:

- `Enable Preventive Schedule`
- `Preventive Interval Days`
- `Next Preventive Date`

### Bước 6

- `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`

Điểm cần xem:

- `Lead Notified User`
- `Lead Notified At`
- activity `0502 Preventive Request Due`

### Bước 7

- `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`
- `Cua hang Q2 - May lanh bep chay nuoc`

Vào menu:

- `0502 Requests To Plan`

### Bước 8

- `Bao tri thang 5 - Tu mat nuoc uong CH Q1`

Điểm cần xem:

- `Scheduled Date`
- `Planned By`
- `Planned At`
- `Planning Note`

### Bước 9

- `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`

Điểm cần xem:

- `FSM Task`
- task đã được tạo và liên kết ngược về request

### Bước 10

- dùng chính FSM task của:
  - `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
  - `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - `Cua hang Q1 - Khong du ton de thay dau in hoa don`

Vào menu:

- `0502 Execution Monitoring`

### Bước 11

- `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`

Điểm cần xem:

- `Treatment Proposal`
- `Estimated Cost`
- `Estimated Timeline`
- `Proposed By`
- `Proposed At`

### Bước 12

- `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`

Điểm cần xem:

- `Approval Status = Pending Approval`

### Bước 13

- `Cua hang Q1 - Danh gia can thue ngoai thay board may in`

Điểm cần xem:

- `Need Outside Service = True`
- `Service Assessed By`
- `Service Assessed At`

### Bước 14

- `Cua hang Q1 - Xu ly noi bo khong can vat tu`

Điểm cần xem:

- `Need Outside Service = False`
- `Has Material Request = False`
- `Material Checked By`
- `Material Checked At`

### Bước 15

- `Cua hang Q1 - Tao phieu kho cap gas bo sung`

Điểm cần xem:

- `Stock Picking`
- picking đã được tạo và liên kết về request
- chưa có kết quả kiểm tồn

### Bước 16

- `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
- `Cua hang Q1 - Khong du ton de thay dau in hoa don`

Điểm cần xem:

- `Stock Check Result`
- `Stock Checked By`
- `Stock Checked At`
- `Stock Availability`
- `Stock Picking State`

Hai nhánh mẫu:

- `Stock Available`
- `Stock Not Available`

## 10. Kịch bản test nhanh nhất

Nếu cần chạm nhanh toàn bộ luồng từ `Bước 1` đến `Bước 16`, đi theo thứ tự:

1. mở `Cua hang Q1 - May lanh quay thu ngan khong mat`
2. mở `Cua hang Q1 - Tu mat keu to`
3. mở `Cua hang Q1 - May in hoa don mo chu`
4. mở `Cua hang Q2 - May lanh bep chay nuoc`
5. mở `Bao tri thang 5 - Tu mat nuoc uong CH Q1`
6. mở `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
7. mở `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`
8. mở `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`
9. mở `Cua hang Q1 - Danh gia can thue ngoai thay board may in`
10. mở `Cua hang Q1 - Xu ly noi bo khong can vat tu`
11. mở `Cua hang Q1 - Tao phieu kho cap gas bo sung`
12. mở `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
13. mở `Cua hang Q1 - Khong du ton de thay dau in hoa don`
14. vào `0502 Requests To Plan`
15. vào `0502 Execution Monitoring`

## 11. Lưu ý kỹ thuật

- file seed hiện đã để ở chế độ có thể update khi nâng cấp module, để khi bổ sung bước mới thì module `M02_P0502_1` có thể đồng bộ record mẫu theo source mới
- dữ liệu bước 16 không gán tay kết quả kiểm tồn; module seed gọi helper để chạy logic thật của `action_psm_check_stock_availability()`
- serial của thiết bị mẫu đã đổi sang hậu tố `DEMO` để giảm rủi ro trùng dữ liệu thật

## 12. Khi nào nên cài `M02_P0502_1`

Nên cài khi:

- cần test nhanh trên môi trường dev
- cần demo nhanh cho BA hoặc key user
- cần dữ liệu mẫu để kiểm tra view/filter/action mới

Không nên cài ở production nếu không muốn có dữ liệu test lẫn trong dữ liệu thật.

## 13. Kết luận ngắn

`M02_P0502_1` hiện là bộ seed data phục vụ:

- test nhanh `Phase 1`
- demo nghiệp vụ từ `Bước 1` đến `Bước 16`
- tách riêng dữ liệu mẫu khỏi module nghiệp vụ chính `M02_P0502`

## 14. Phase 3G trong module `M02_P0502`

Tu phase 3G, module chinh `M02_P0502` co them bo demo data rieng trong:

- `demo/psm_0502_demo_data.xml`

Bo demo nay dung de smoke test truc tiep module chinh, gom:

- 3 phong ban/cua hang mau va vendor dich vu
- 1 maintenance team da cau hinh lead, approver, vendor mac dinh, SLA va nguong auto approve
- 5 thiet bi, trong do co thiet bi bat preventive schedule
- request mau o cac trang thai intake, proposed, outside service va done
- outside service request mau
- material line, planning history va proposal history

Module chinh cung co smoke test tai:

- `tests/test_0502_flow.py`

Checklist UAT phase 3 duoc dat tai:

- `notes/checklist_uat_0502_phase3.md`

Khi test nhanh tren moi truong dev, co the cai/upgrade `M02_P0502` voi demo data de kiem tra menu va flow cot loi. Module `M02_P0502_1` van giu vai tro bo seed phu co kich ban demo chi tiet hon.
