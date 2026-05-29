# Danh Sách Request Mẫu Theo Bước 1-16

## 1. Mục đích

File này dùng để tra rất nhanh:

- bước nào dùng request mẫu nào
- bước nào có FSM task mẫu
- bước nào có stock picking mẫu

Phạm vi hiện tại:

- `Phase 1 - Bước 1` đến `Phase 1 - Bước 16`

Nguồn dữ liệu chính:

- module seed: [D:\odoo-19.0+e.20250918\addons\M02_P0502_1\data\psm_seed_data.xml](D:\odoo-19.0+e.20250918\addons\M02_P0502_1\data\psm_seed_data.xml)
- source nghiệp vụ:
  - [D:\odoo-19.0+e.20250918\addons\M02_P0502\models\maintenance_request.py](D:\odoo-19.0+e.20250918\addons\M02_P0502\models\maintenance_request.py)
  - [D:\odoo-19.0+e.20250918\addons\M02_P0502\models\project_task.py](D:\odoo-19.0+e.20250918\addons\M02_P0502\models\project_task.py)
  - [D:\odoo-19.0+e.20250918\addons\M02_P0502\models\stock_picking.py](D:\odoo-19.0+e.20250918\addons\M02_P0502\models\stock_picking.py)

## 2. Tra nhanh theo bước

### Bước 1 - Cửa hàng phát sinh nhu cầu

- Request mẫu:
  - `Cua hang Q1 - May lanh quay thu ngan khong mat`
- Mục tiêu test:
  - phát sinh request từ cửa hàng
  - `Request Source = Store Request`

### Bước 2 - Tạo phiếu yêu cầu bảo trì

- Request mẫu:
  - `Cua hang Q1 - May lanh quay thu ngan khong mat`
  - `Cua hang Q1 - Tu mat keu to`
- Mục tiêu test:
  - `Request Type`
  - `Store Department`
  - `Request Source`

### Bước 3 - CMT tiếp nhận yêu cầu

- Request mẫu:
  - `Cua hang Q1 - Tu mat keu to`
- Mục tiêu test:
  - `Received By`
  - `Received At`

### Bước 4 - Kiểm tra thực tế ban đầu

- Request mẫu:
  - `Cua hang Q1 - May in hoa don mo chu`
  - `Cua hang Q2 - May lanh bep chay nuoc`
- Mục tiêu test:
  - `Initial Inspection Result`
  - `Initial Inspection Note`
- Hai nhánh:
  - `No Action Needed`
  - `Action Needed`

### Bước 5 - Hệ thống kiểm tra lịch bảo trì

- Equipment mẫu:
  - `May lanh quay thu ngan - CH Q1`
  - `Tu mat nuoc uong - CH Q1`
  - `May lanh bep - CH Q2`
- Mục tiêu test:
  - `Enable Preventive Schedule`
  - `Preventive Interval Days`
  - `Next Preventive Date`

### Bước 6 - Gửi lịch bảo trì cho CMT Lead

- Request mẫu:
  - `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`
- Activity mẫu:
  - `0502 Preventive Request Due`
- Mục tiêu test:
  - `Lead Notified User`
  - `Lead Notified At`

### Bước 7 - CMT Lead tổng hợp yêu cầu

- Request mẫu:
  - `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`
  - `Cua hang Q2 - May lanh bep chay nuoc`
- Menu nên mở:
  - `0502 Requests To Plan`

### Bước 8 - Lập kế hoạch bảo trì

- Request mẫu:
  - `Bao tri thang 5 - Tu mat nuoc uong CH Q1`
- Mục tiêu test:
  - `Scheduled Date`
  - `Planning Note`
  - `Planned By`
  - `Planned At`

### Bước 9 - Điều phối nhân viên bảo trì

- Request mẫu:
  - `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
- FSM task mẫu:
  - `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
- Mục tiêu test:
  - request có `FSM Task`
  - task có `Customer`
  - task có liên kết ngược `0502 Maintenance Request`

### Bước 10 - Theo dõi tiến độ xử lý

- FSM task mẫu:
  - `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
  - `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - `Cua hang Q1 - Khong du ton de thay dau in hoa don`
- Menu nên mở:
  - `0502 Execution Monitoring`

### Bước 11 - Đề xuất phương án xử lý

- Request mẫu:
  - `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`
- Mục tiêu test:
  - `Treatment Proposal`
  - `Estimated Cost`
  - `Estimated Timeline`
  - `Proposed By`
  - `Proposed At`

### Bước 12 - Duyệt đề xuất

- Request mẫu:
  - `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`
- Mục tiêu test:
  - `Approval Status = Pending Approval`

### Bước 13 - Đánh giá xử lý nội bộ hay thuê ngoài

- Request mẫu:
  - `Cua hang Q1 - Danh gia can thue ngoai thay board may in`
- Mục tiêu test:
  - `Need Outside Service = True`
  - `Service Assessed By`
  - `Service Assessed At`

### Bước 14 - Đánh giá phát sinh vật tư

- Request mẫu:
  - `Cua hang Q1 - Xu ly noi bo khong can vat tu`
- Mục tiêu test:
  - `Need Outside Service = False`
  - `Has Material Request = False`
  - `Material Checked By`
  - `Material Checked At`

### Bước 15 - Tạo phiếu kho

- Request mẫu:
  - `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- FSM task mẫu:
  - `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- Stock picking mẫu:
  - picking gắn với request `Cua hang Q1 - Tao phieu kho cap gas bo sung`
- Stock move mẫu:
  - `Gas bo sung may lanh DEMO`
- Mục tiêu test:
  - request có `Stock Picking`
  - picking có `0502 Maintenance Request`
  - picking có `0502 FSM Task`

### Bước 16 - Kiểm tra tồn kho

- Request mẫu:
  - `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - `Cua hang Q1 - Khong du ton de thay dau in hoa don`
- FSM task mẫu:
  - `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - `Cua hang Q1 - Khong du ton de thay dau in hoa don`
- Stock picking mẫu:
  - picking gắn với request `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - picking gắn với request `Cua hang Q1 - Khong du ton de thay dau in hoa don`
- Stock move mẫu:
  - `Ong thoat nuoc dieu hoa DEMO`
  - `Dau in hoa don DEMO`
- Mục tiêu test:
  - `Stock Check Result = Stock Available`
  - `Stock Check Result = Stock Not Available`
  - `Stock Checked By`
  - `Stock Checked At`

## 3. Tra nhanh theo record

### Request mức đầu luồng

- `Cua hang Q1 - May lanh quay thu ngan khong mat`
  - dùng cho bước 1-2
- `Cua hang Q1 - Tu mat keu to`
  - dùng cho bước 2-3
- `Cua hang Q1 - May in hoa don mo chu`
  - dùng cho bước 4
- `Cua hang Q2 - May lanh bep chay nuoc`
  - dùng cho bước 4 và queue bước 7

### Request mức preventive / planning

- `Bao tri dinh ky thang 4 - May lanh quay thu ngan CH Q1`
  - dùng cho bước 6-7
- `Bao tri thang 5 - Tu mat nuoc uong CH Q1`
  - dùng cho bước 8

### Request mức FSM / execution

- `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
  - dùng cho bước 9-10

### Request mức proposal / approval

- `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`
  - dùng cho bước 11
- `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`
  - dùng cho bước 12

### Request mức service assessment / material assessment

- `Cua hang Q1 - Danh gia can thue ngoai thay board may in`
  - dùng cho bước 13
- `Cua hang Q1 - Xu ly noi bo khong can vat tu`
  - dùng cho bước 14

### Request mức kho

- `Cua hang Q1 - Tao phieu kho cap gas bo sung`
  - dùng cho bước 15
- `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
  - dùng cho bước 16 nhánh đủ tồn
- `Cua hang Q1 - Khong du ton de thay dau in hoa don`
  - dùng cho bước 16 nhánh thiếu tồn

## 4. Tra nhanh theo menu

- `Maintenance > Maintenance > Maintenance Requests`
  - mở hầu hết request mẫu
- `Maintenance > Maintenance > 0502 Requests To Plan`
  - test bước 7
- `Maintenance > Reporting > 0502 Execution Monitoring`
  - test bước 10
- `Maintenance > Equipment`
  - test bước 5
- `Inventory > Operations`
  - mở picking mẫu bước 15-16

## 5. Gợi ý test nhanh nhất

Nếu chỉ cần kiểm tra nhanh bộ seed đã đủ đến bước 16 hay chưa, mở lần lượt:

1. `Bao tri thang 5 - Tu mat nuoc uong CH Q1`
2. `Cua hang Q2 - Dieu phoi ky thuat xu ly may lanh bep`
3. `Cua hang Q1 - De xuat xu ly thay ong thoat nuoc`
4. `Cua hang Q2 - Cho duyet de xuat sua may lanh bep`
5. `Cua hang Q1 - Danh gia can thue ngoai thay board may in`
6. `Cua hang Q1 - Xu ly noi bo khong can vat tu`
7. `Cua hang Q1 - Tao phieu kho cap gas bo sung`
8. `Cua hang Q2 - Co du ton de thay ong thoat nuoc`
9. `Cua hang Q1 - Khong du ton de thay dau in hoa don`

Nếu 9 record trên mở đúng và dữ liệu trường khớp logic từng bước, bộ seed đã phủ đủ `Phase 1 - Bước 16`.
