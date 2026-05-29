# Hướng Dẫn Xem Các Thành Phần Module M08_P0801 Khi Có Data Mẫu

Sau khi cài module `M08_P0801_demo`, đây là cách điều hướng để xem toàn bộ dữ liệu đã được tạo.

---

## Bước 0 — Cài module

**Settings → Apps** → bỏ filter "Apps" → tìm `M08_P0801 Demo Data` → Install.

> Yêu cầu: phải cài `M08_P0801` trước.  
> Nếu đã cài rồi và vừa cập nhật: Settings → Apps → M08_P0801 Demo Data → ⚙️ → **Upgrade**.

---

## 1. Phòng ban & Nhân viên

**Employees → Departments**
- 6 phòng ban: RSG, IT, MENU/DIGITAL, MKT, S&I, SC/DC
- RSG và IT đã có manager được gán sẵn (Võ Xuân Hùng, Bùi Thành Nam)

**Employees → Employees**
- **8 nhân viên demo**, mỗi người gắn với phòng ban và chức danh tương ứng

| Tên | Phòng ban | Chức danh |
|-----|----------|----------|
| Nguyễn Minh Tuấn | RSG | RSG Analyst |
| Võ Xuân Hùng | RSG | RSG Department Head |
| Trần Quốc Bảo | IT | IT Engineer |
| Bùi Thành Nam | IT | IT Department Head |
| Lê Thị Thu | MENU / DIGITAL | Menu Developer |
| Phạm Hồng Nhung | MKT | Marketing Specialist |
| Đặng Quỳnh Anh | S&I | Data Analyst |
| Nguyễn Thái Sơn | SC / DC | Supply Chain Coordinator |

---

## 2. Users Demo

**Settings → Users & Companies → Users** → lọc theo `@mcvn.local`

| Login | Password | Phòng ban | Vai trò trong quy trình PIF |
|-------|----------|----------|----------------------------|
| demo.rsg@mcvn.local | 1 | RSG | Thực hiện B7, B9, B11, B14 |
| demo.rsg.head@mcvn.local | 1 | RSG | Trưởng phòng — nhận thông báo |
| demo.it@mcvn.local | 1 | IT | Thực hiện B8, B12 |
| demo.it.head@mcvn.local | 1 | IT | Trưởng phòng — nhận thông báo |
| demo.menu@mcvn.local | 1 | MENU/DIGITAL | Gửi yêu cầu PIF (B1, B4) |
| demo.mkt@mcvn.local | 1 | MKT | Gửi yêu cầu PIF (B2) |
| demo.si@mcvn.local | 1 | S&I | Gửi yêu cầu PIF (B3) |
| demo.sc@mcvn.local | 1 | SC/DC | Gửi yêu cầu PIF (B5) |

> **Lưu ý:** Đủ người cho cả 5 lane yêu cầu B1–B5.

---

## 3. Sản phẩm & Nguyên liệu

**Inventory → Products → Products** hoặc **Manufacturing → Products**

| Filter | Kết quả |
|--------|---------|
| PIF Type = Raw | 9 nguyên liệu thô (Beef Patty, Sesame Bun, Chicken Fillet...) |
| PIF Type = Finished | 3 thành phẩm (Spicy McDouble, BBQ Chicken Burger, McChicken Crispy) |
| PIF Status = Completed | 3 thành phẩm đã sẵn sàng cho PIF |

Mở **McChicken Crispy** → tab PIF Info → WRIN Code = `FG-2025-0042`

---

## 4. Bill of Materials (Công thức nguyên liệu)

**Manufacturing → Products → Bills of Materials**
- 3 BOM, mỗi cái gắn với 1 thành phẩm
- PIF Status = Completed → đủ điều kiện để PIF chọn
- Mở BOM → xem danh sách nguyên liệu và số lượng từng thứ

---

## 5. Xem 3 PIF Mẫu (Điểm chính)

**Trước tiên bật menu:**
Settings → Technical → User Interface → Menu Items → tìm "PIF Implementation" → bật Active.

Vào **PIF Implementation → PIF Creation**:

| PIF | Sản phẩm | Trạng thái | Nội dung cần xem |
|-----|----------|------------|-----------------|
| PIF-DEMO-001 | Spicy McDouble | RSG Created | Mới tạo, chưa có gì — dùng để thực hành luồng từ đầu |
| PIF-DEMO-002 | BBQ Chicken Burger | Lab Tested | Tab SSBI/RFM/POS đã điền, tab Lab Test có 1 lần FAIL |
| PIF-DEMO-003 | McChicken Crispy | Completed | 7/7 tracking steps done, Lab PASS, WRIN đã sinh |

---

## 6. Test Permission Theo Từng User

Đây là cách test thực tế nhất — đăng nhập từng user và thử tương tác với PIF:

```
Đăng nhập: demo.rsg@mcvn.local (pass: 1)
→ Mở PIF-DEMO-001
→ Thấy nút "Done (RSG)" màu xanh ✅ (đúng phòng ban RSG)

Đăng nhập: demo.it@mcvn.local (pass: 1)
→ Mở PIF-DEMO-001
→ KHÔNG thấy nút Done ✅ (đúng, IT chưa đến lượt ở state rsg_create)
```

**Thử luồng đầy đủ từ PIF-DEMO-001:**
1. Đăng nhập `demo.rsg` → điền tab SSBI, RFM, POS → nhấn "Done (RSG)"
2. State → IT Config; IT Head (Bùi Thành Nam) nhận activity
3. Đăng nhập `demo.it` → nhấn "Done (IT)"
4. State → Master Data; RSG nhận activity
5. Đăng nhập `demo.rsg` → nhấn "Done (RSG)"
6. State → Lab Test → chọn Fail → điền ghi chú → nhấn Done
7. Xem vòng lặp: state quay về IT Config, tracking reset

---

## 7. Nhà Cung Cấp

**Contacts** → tìm `HAVI` hoặc `Trasas`

---

## Sơ Đồ Điều Hướng Nhanh

```
Settings
  └── Users (@mcvn.local) ................. 8 demo users

Employees
  ├── Departments ......................... RSG, IT, MKT, S&I, MENU/DIGITAL, SC/DC
  └── Employees ........................... 8 nhân viên demo (đủ 5 lane B1–B5)

Manufacturing / Inventory
  ├── Products ............................ 9 nguyên liệu + 3 thành phẩm
  └── Bills of Materials .................. 3 BOM (x_psm_0801_pif_status=completed)

PIF Implementation  ← bật menu nếu chưa thấy
  ├── PIF Creation ........................ 3 PIF mẫu ở 3 state khác nhau
  ├── Projects (Products) ................. 3 thành phẩm
  └── System Data List .................... data lines (trống ở demo)

Contacts
  └── HAVI Vietnam, Trasas Vietnam ........ nhà cung cấp
```
