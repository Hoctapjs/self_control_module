# Hướng dẫn đi hết quy trình PIF (0801) & xem các phần đã bổ sung

> Mục đích: thao tác end-to-end trên giao diện để **nhìn thấy tận mắt** mọi phần đã thêm sau 6 phase + 2 lỗi đã fix.
> Module: `M08_P0801` (+ `M08_P0801_demo` cho dữ liệu mẫu).

---

## 0. Chuẩn bị (bắt buộc)

### 0.1 Cài / nâng cấp module kèm demo
Từ thư mục gốc `d:\odoo-19.0+e.20250918`:
```
python odoo-bin -c <config> -d <db> -u M08_P0801,M08_P0801_demo
```
Mở log, đảm bảo **không có traceback**. (Nếu trước đây gặp lỗi `Invalid field 'is_pif'` → nay đã fix, phải load sạch.)

### 0.2 Cấp quyền để thấy các nút "Done"
Các nút bước RSG/IT chỉ hiện khi user thuộc nhóm PIF. **Cách nhanh nhất để 1 mình đi hết quy trình:**
- Vào **Settings → Users & Companies → Users → (chọn user của bạn, vd Mitchell Admin)**.
- Ở khối phân quyền tìm mục **PIF Management** → chọn **PIF Manager** (nhóm này tự bao gồm cả RSG và IT).
- Lưu.

> Nếu không gán nhóm này, bạn vẫn xem được mọi trang dữ liệu nhưng **các nút "Done (RSG)/Done (IT)" sẽ bị ẩn** → không bấm chuyển bước được.

### 0.3 Hai cách đi quy trình
- **Cách A — dùng dữ liệu demo có sẵn** (khuyến nghị để xem nhanh mọi trạng thái): 3 PIF mẫu `PIF-DEMO-001` (đầu luồng), `PIF-DEMO-002` (đang Lab), `PIF-DEMO-003` (đã hoàn tất).
- **Cách B — tạo mới từ đầu** qua App *Approvals* (xem mục 2) để thấy luồng B1–B7 và **fast-track Digital/SC**.

Menu chính của module: **PIF Implementation** (ngoài cùng bên trái) → *PIF Creation*, *Projects (Products)*, *System Data List*.

---

## 1. Đi hết luồng thực thi bằng PIF-DEMO-001 (xem rõ nhất các phần mới)

Mở **PIF Implementation → PIF Creation →** mở `PIF-DEMO-001` (đang ở state **RSG Created**).

### Bước 1 — RSG Created → IT Configured  *(Phase 1, 2, 3, 4-B2A)*
Trên form, mở lần lượt các trang trong notebook để **thấy các phần đã bổ sung**:

1. **Trang "Product Information"** — *(PHASE 1 + PHASE 3)*
   - Khối **Initiator & Program**: `Program`, `Initiator Department`, `New Code Required`, `Target Effective Date`.
   - Khối **Product Identity**: `Product ID/Menu Item Code` (chỉ sửa được ở bước IT), `Short Name/PMIX Code`, tên EN/VI, `Product Form` (A la carte/Combo/Meal), `Menu Type`.
   - Khối **Category**: `Category LV1 … LV7`.
   - Khối **Platforms & Pricing**: `Platforms` (FC/SOK/DT/WT/McCafe/Digital), 3+1 tầng giá `In-store/VNM`, `Delivery`, `TSN`, `Other`.
   - Khối **PIF Sizing & SLA** *(PHASE 3)*: chọn `PIF Size` = **Large** → quan sát các ô tự tính: `Price Tier=3`, `Week Number=1st & 3rd`, `Total System Code=60`, `Build RFM=10`, `Test LAB=3`, `Back up=2`, `Total Working Days=15`, và `Calculated Effective Date` = **Thứ Hai** kế tiếp sau khi cộng working days từ `Submit Date`.
     - 👉 **Kiểm chứng Lỗi-fix #2:** đổi `PIF Size` sang **Medium** rồi **Small** → cả hai phải hiển thị `Week Number = 1st & 3rd`; đổi sang **Ad-hoc** → `Week Number = 2nd & 4th` (và `Price Tier=1`).
2. **Trang "Menu Components"** — *(PHASE 2)*
   - Cờ `Insert KETCHUP & CHILI SACHET as choice?`.
   - Bảng component: demo có 1 dòng **parent** (Spicy McDouble) + 1 dòng **drink** với `Default=true`, `Default Size=M`, `Allow Upsize=true`, `Allow Upgrade=true`, `Choice Group=Soft Drink`, kèm 3 cột giá VNM/Delivery/TSN.
   - 👉 Thử **đổi `Select BOM`** ở đầu form → bảng Menu Components & Raw Materials tự nạp lại dòng **parent** từ BOM (onchange).
3. **Trang "Marketing Images"** — *(PHASE 4 / B2A)*: chỉ hiện khi `Request Type = Marketing`. PIF-DEMO-001 là *Menu* nên trang này ẩn → xem ở PIF-DEMO-002.
4. **Trang SSBI / RFM / POS**: nhập nội dung HTML (demo-001 chưa có → cần điền đủ cả 3 mới qua được bước).
5. Nhấn **Done (RSG)**. Hệ thống kiểm tra đã nhập đủ 3 ô SSBI/RFM/POS → chuyển sang **IT Configured**, bước 1 trong tab *Tracking* chuyển *Done*.

### Bước 2 — IT Configured → Master Data Set
- Vào trang **Product Information**, lúc này ô `Product ID/Menu Item Code` **mới cho sửa** (IT input). Nhập một mã (vd `MI-0001`).
  - 👉 Constraint *(PHASE 5)*: nhập trùng mã với PIF khác → báo lỗi "must be unique".
- Nhấn **Done (IT)** → sang **Master Data Set**.

### Bước 3 — Master Data Set → Lab Tested  *(PHASE 4 / B9 + B10)*
- **Trang "Master Setup"**: tick đủ 4 mục `Code/Price/Store`, `UDP`, `Recipe/SSBI`, `Raw Item`.
  - 👉 Nếu thiếu 1 mục rồi bấm Done → báo lỗi liệt kê mục còn thiếu.
- **Trang "Display Check"** (B10): thêm vài dòng kiểm tra hiển thị của các phòng (Menu/MKT/S&I/Digital) với trạng thái Pass/Fail.
- Nhấn **Done (RSG)** → sang **Lab Tested**.

### Bước 4 — Lab Tested → Pilot Done  *(PHASE 5 — lab 2 cấp)*
- **Trang "Lab Test"**:
  - Bấm **Initiator Sign-off** → ghi nhận người + thời điểm.
  - Bấm **RSG Sign-off** → ghi nhận người + thời điểm.
  - Chọn `Lab Test Result = Pass`.
  - 👉 Nếu bấm **Done (RSG)** mà thiếu 1 trong 2 sign-off → báo lỗi "PASS requires both Initiator sign-off and RSG sign-off".
  - (Thử nhánh **Fail**: chọn Fail + nhập Note → state quay lại **IT Configured**, các bước 2–5 reset *pending*, sign-off bị xóa — đúng vòng làm lại B11→B8. Xem sẵn lịch sử fail ở PIF-DEMO-002.)
- Đủ 2 sign-off + Pass → **Done (RSG)** → sang **Pilot Done**. Mỗi lần test đều ghi vào *Historical Tests*.

### Bước 5 — Pilot Done → Valuation Done  *(PHASE 6 / API SSBI)*
- Nhấn **Done (IT)**. Override `action_pilot_deploy` sẽ **tự đẩy payload SSBI**.
- Mở **trang "SSBI Integration"**: `SSBI Push Status = Queued`, có `Last SSBI Push Date` và JSON payload đầy đủ (header + pricing + platforms + components).
- (Có thể bấm nút header **Push SSBI** để đẩy lại thủ công.)

### Bước 6 — Valuation Done → Completed  *(PHASE 6 / Report + WRIN)*
- Nhấn **Done (RSG)**:
  - State → **Completed**, bước 6 & 7 trong *Tracking* chuyển *Done*.
  - Hệ thống **sinh WRIN thành phẩm** (định dạng `FG-YYYY-XXXX`), ghi vào sản phẩm + chatter.
- Nhấn nút header **Print Valuation Report** → xuất **PDF** gồm: header PIF, bảng giá 3 tầng, platforms, components, tracking 7 bước, lab history.

---

## 2. Xem fast-track Digital/SC & luồng tạo mới  *(PHASE 4.1 — đã chốt)*

1. Mở app **Approvals → New**, chọn category **Product Initiation Form (PIF)**.
   - 👉 **Kiểm chứng Lỗi-fix #1:** category này load được nghĩa là cờ `x_psm_0801_is_pif` đúng (trước đây sai tên `is_pif` làm chết module).
2. Chọn **Request Type = Digital** (hoặc Supply Chain), chọn *Approved Product* nếu có, **Confirm**.
   - Vì là Digital/SC → hệ thống **auto-approve** và **tạo ngay PIF Object ở state `IT Configured`**, mặc định `PIF Size = Ad-hoc`. Bấm nút thông minh **PIF** trên request để mở.
3. So sánh: chọn **Request Type = Menu/MKT/S&I** → phải qua **phê duyệt B6** rồi PIF mới sinh ở state `RSG Created`.

> Lưu ý kiểm thử: với Digital/SC mà **không chọn sản phẩm/BOM**, việc tạo PIF có thể lỗi do `Select BOM` đang `required`. Nếu gặp, chọn 1 Approved Product có BOM trước khi Confirm.

---

## 3. Bảng đối chiếu: phần nào thuộc phase nào (để rà nhanh trên UI)

| Vị trí trên giao diện | Thuộc | Quan sát |
|---|---|---|
| Trang **Product Information** (Program, PMIX, tên EN/VI, Product Form, Category LV1–7, Platforms, 3+1 giá, Effective Date) | Phase 1 | Form PIF Object |
| Khối **PIF Sizing & SLA** (size → tự tính ngày, effective Monday) | Phase 3 | Cùng trang Product Information |
| Trang **Menu Components** (parent/child, Default/Upsize/Upgrade, 3 giá, Ketchup&Chili) | Phase 2 | Notebook |
| Trang **Marketing Images** (POS/SOK/DMB/MOP) | Phase 4 (B2A) | Hiện khi Request Type = Marketing |
| Trang **Master Setup** (4 checklist) + validate | Phase 4 (B9) | Bước Master Data |
| Trang **Display Check** | Phase 4 (B10) | Notebook |
| Fast-track Digital/SC (auto-approve, vào IT Config, size Ad-hoc) | Phase 4.1 | App Approvals |
| Khối **Lab Sign-off** (Initiator + RSG) | Phase 5 | Trang Lab Test |
| Báo lỗi PMIX > 7 ký tự / `Di<số>` cho digital combo; Menu Item Code unique | Phase 5 | Khi nhập sai |
| Trang **SSBI Integration** + nút **Push SSBI** | Phase 6 | Sau Pilot |
| Nút **Print Valuation Report** (PDF) | Phase 6 | State Valuation/Completed |
| Nhóm **PIF Management** (RSG/IT/Manager) trong Settings → Users | Phase 6 | Phân quyền |

---

## 4. Xác nhận nhanh 2 lỗi đã fix
- **Lỗi #1 (blocker):** module cài/nâng cấp **không còn báo** `Invalid field 'is_pif'`; category *Product Initiation Form (PIF)* mở được trong app Approvals.
- **Lỗi #2 (sai data SLA):** ở khối PIF Sizing & SLA, `Week Number` = **1st & 3rd** cho Large/Medium/Small và **2nd & 4th** cho Ad-hoc.

---

## 5. Mẹo xem nhanh theo trạng thái (không cần đi tuần tự)
- `PIF-DEMO-001` — state RSG Created: xem toàn bộ trang nhập liệu mới (Phase 1/2/3).
- `PIF-DEMO-002` — state Lab Test, Request Type Marketing: xem **Marketing Images** (B2A), **Display Check** (B10), **Master Setup** đã tick, và **Lab History** có 1 lần Fail.
- `PIF-DEMO-003` — state Completed: xem 2 sign-off đã đủ, tracking 7 bước Done, và **Print Valuation Report** ra PDF hoàn chỉnh.
