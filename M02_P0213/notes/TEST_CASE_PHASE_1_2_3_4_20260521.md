# TEST CASE KIỂM TRA PHASE 1-4 (2026-05-21)

**Mục tiêu:** Verify tất cả lỗi đã sửa trên **Inbox thật** (Outlook/Gmail) + **Chatter Odoo**

---

## I. CHUẨN BỊ TEST

### Điều kiện tiên quyết
- [ ] Module M02_P0213 đã upgrade: `.\upgrade_m02_p0213.ps1 -NoRestart`
- [ ] Odoo chạy trên `http://localhost:8069`
- [ ] Có ít nhất 1 **Approval Request** ở trạng thái **"Approved"** (category: Resignation)
- [ ] Có 1 **Employee** với email hợp lệ (để gửi test email)
- [ ] Có **Mail Server** cấu hình (hoặc mode test gửi mail local)

### Cách tạo test data (nếu cần)
1. HR → Employees → Tạo employee mới với email `test@mcdonalds.vn`
2. Settings → Approvals → Tạo Approval Request (Resignation category) với employee vừa tạo
3. Phê duyệt request (thay đổi status thành "Approved")

---

## II. TEST CASE MATRIX (4 Template × 2 Nơi Hiển Thị)

### Template: **dept_offboarding_reminder** (Nhắc nhở bộ phận)
**ID:** `psm_0213_email_template_dept_offboarding_reminder`  
**Gửi tới:** Người phụ trách công việc offboarding (IT, Admin, HR, Manager)  
**Trigger:** Cron job hoặc Manual Reminder Extension

---

#### **TC-1.1: Header Background Color (Outlook Email Client)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Gửi approval request → Trigger cron reminder (hoặc Manual Reminder) | Email được gửi |
| 2 | Kiểm tra Inbox (Outlook) | Email nhận được |
| 3 | Mở email, xem **header section** (phần "OPS REMINDER") | ✅ Nền **PHẢI có màu đỏ** (solid fallback `#b5121b` hoặc gradient) |
| 4 | Kiểm tra **chữ trắng** trên nền | ✅ Chữ trắng/vàng **PHẢI đọc được** (contrast OK) |
| **Kết luận** | Header có nền + chữ đọc được | **PASS** ✅ / **FAIL** ❌ |

**Bằng chứng xác nhận:**
- Screenshot: Header có màu (không phải trắng/ngã)
- Hoặc: Export email HTML → `grep "background-color:#b5121b"` có kết quả

---

#### **TC-1.2: Header Background Color (Gmail Email Client)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-1.1 | Email nhận được |
| 2 | Kiểm tra Inbox (Gmail) | Email mở được |
| 3 | Xem header (phần "OPS REMINDER") | ✅ Nền **PHẢI là gradient** (đỏ → cam → vàng) HOẶC **fallback màu đỏ** |
| 4 | Kiểm tra **chữ trắng/vàng** | ✅ **PHẢI đọc được** trên nền |
| **Kết luận** | Gradient/fallback + chữ OK | **PASS** ✅ / **FAIL** ❌ |

**Bằng chứng xác nhận:**
- Screenshot: Header có gradient hoặc màu solid
- Hoặc: View email source → `<td style="...background-image:linear-gradient...">`

---

#### **TC-1.3: Placeholder — Tên Nhân Viên (Outlook Email)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-1.1 | Email nhận được |
| 2 | Tìm text: "Bạn đang có nhiệm vụ trong quy trình nghỉ việc của nhân viên" | Tìm thấy |
| 3 | Kiểm tra tên nhân viên sau text | ✅ **PHẢI là tên thật** (ví dụ: "Huỳnh Thanh Sơn"), **KHÔNG phải `{{ object.x_psm_0213_employee_id.name }}`** |
| 4 | Tìm bảng "Thông tin liên quan" → row "Nhân viên" | ✅ **PHẢI có tên nhân viên** (KHÔNG `{{ }}`) |
| 5 | Tìm row "Mã nhân viên" | ✅ **PHẢI có mã** (ví dụ: "EMP123"), **KHÔNG phải `{{ object.x_psm_0213_employee_id.barcode or 'N/A' }}`** |
| **Kết luận** | Tên + Mã NV hiển thị đúng (không literal `{{ }}`) | **PASS** ✅ / **FAIL** ❌ |

**Bằng chứng xác nhận:**
- Screenshot: Tên hiển thị (không `{{ }}`)
- Hoặc: Export HTML → `grep "Huỳnh Thanh Sơn"` (tên thực)

---

#### **TC-1.4: Placeholder — Tên Nhân Viên (Gmail Email)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-1.1 | Email nhận được |
| 2 | Xem phần "Bạn đang có nhiệm vụ..." | ✅ **Tên nhân viên PHẢI là text thật** |
| 3 | Xem bảng "Thông tin liên quan" | ✅ **Tên + Mã NV hiển thị đúng** (không `{{ }}`) |
| **Kết luận** | Placeholder render OK | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-1.5: Border Left (Odoo Chatter)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Mở Approval Request trong Odoo | Request hiển thị |
| 2 | Vào tab "Activity" hoặc "Chatter" | Thấy email được gửi (log) |
| 3 | Click nút "..." → "Show original message" hoặc mở HTML email | Email HTML mở trong Odoo |
| 4 | Tìm phần "Cần xử lý:" (box viền trái) | ✅ **PHẢI có viền trái 4px màu đỏ** (KHÔNG bị xóa) |
| 5 | Kiểm tra box "Lưu ý:" (viền trái khác) | ✅ **Viền trái vẫn hiển thị** |
| **Kết luận** | Viền trái sống sót sanitizer chatter | **PASS** ✅ / **FAIL** ❌ |

**Bằng chứng xác nhận:**
- Screenshot: Chatter hiển thị box có viền trái đỏ
- Hoặc: Inspect element (F12) → `border-left-width: 4px; border-left-color: ...`

---

#### **TC-1.6: Header Background Chatter (Odoo)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng Approval Request từ TC-1.5 | Chatter mở |
| 2 | Xem email HTML trong chatter | Email preview hiển thị |
| 3 | Kiểm tra header (phần "OPS REMINDER") | ✅ **PHẢI có nền** (không "bạc màu" trắng) |
| 4 | Kiểm tra **chữ trắng/vàng** | ✅ **PHẢI đọc được** (không ẩn) |
| **Kết luận** | Chatter header không bị "bạc màu" | **PASS** ✅ / **FAIL** ❌ |

**Bằng chứng xác nhận:**
- Screenshot: Chatter header có màu (đỏ/cam/vàng), chữ đọc được
- Compare trước/sau fix: Trước bị "bạc màu", sau có nền

---

### Template: **offboarding_reminder** (Nhắc nhở nhân viên)
**ID:** `psm_0213_email_template_offboarding_reminder`  
**Gửi tới:** Employee (người yêu cầu resignation)  
**Trigger:** Cron job hoặc Manual Reminder

---

#### **TC-2.1: Header Background (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Trigger email nhắc nhở (cron hoặc manual) | Email gửi đến employee |
| 2 | Kiểm tra Inbox (Outlook) | Email nhận được |
| 3 | Xem header "Nhắc nhở hoàn thành thủ tục nghỉ việc" | ✅ **Nền PHẢI có màu đỏ/gradient** |
| 4 | Kiểm tra chữ | ✅ **Chữ trắng PHẢI đọc được** |
| **Kết luận** | Header OK, no "bạc màu" | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-2.2: Placeholder — Tên Request Owner (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-2.1 | Email nhận được |
| 2 | Tìm text: "Kính gửi..." | Tìm thấy |
| 3 | Kiểm tra tên sau "Kính gửi" | ✅ **PHẢI là tên thật** (ví dụ: "Huỳnh Thanh Sơn"), **KHÔNG `{{ object.request_owner_id.name }}`** |
| **Kết luận** | Placeholder render đúng | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-2.3: Header Background Chatter (Odoo)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Mở Approval Request → Chatter | Email log hiển thị |
| 2 | Xem email HTML | Email preview mở |
| 3 | Kiểm tra header | ✅ **PHẢI có nền** (không "bạc màu") |
| 4 | Kiểm tra viền trái box "Lưu ý" | ✅ **Viền trái 4px PHẢI hiển thị** |
| **Kết luận** | Chatter render OK | **PASS** ✅ / **FAIL** ❌ |

---

### Template: **exit_survey** (Khảo sát nghỉ việc)
**ID:** `psm_0213_email_template_exit_survey`  
**Gửi tới:** Employee (request owner)  
**Trigger:** Action "Send Exit Survey"

---

#### **TC-3.1: Header + Button Color (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Trigger: Action → Send Exit Survey | Email gửi |
| 2 | Kiểm tra Inbox (Outlook) | Email nhận được |
| 3 | Xem header "Khảo sát nghỉ việc" | ✅ **Nền có màu đỏ/gradient** |
| 4 | Tìm nút "Bắt đầu khảo sát" | ✅ **Nền nút PHẢI có màu đỏ** (KHÔNG trắng) |
| 5 | Kiểm tra **chữ trắng** trên nút | ✅ **Đọc được** |
| **Kết luận** | Header + nút color OK | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-3.2: Survey Link (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-3.1 | Email nhận được |
| 2 | Click nút "Bắt đầu khảo sát" | ✅ **Link PHẢI hoạt động**, trang khảo sát mở |
| 3 | Hoặc: Copy link từ box "Nếu nút không hoạt động..." | ✅ **Link PHẢI hợp lệ và mở được** |
| **Kết luận** | Survey link sống sót sanitize | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-3.3: Chatter Render (Odoo)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Mở Approval Request → Chatter | Email log |
| 2 | Xem email HTML | Preview hiển thị |
| 3 | Kiểm tra header + nút | ✅ **Header có nền, nút có màu đỏ** |
| 4 | Kiểm tra viền + link | ✅ **Viền + link sống sót** |
| **Kết luận** | Chatter render đầy đủ | **PASS** ✅ / **FAIL** ❌ |

---

### Template: **adecco_notification** (Thông báo Adecco)
**ID:** `psm_0213_email_template_adecco_notification`  
**Gửi tới:** Adecco email (cấu hình trong Settings)  
**Trigger:** Khi approval request → status "Completed"

---

#### **TC-4.1: Header Color (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Hoàn tất approval request → trigger Adecco email | Email gửi |
| 2 | Kiểm tra Inbox Adecco (Outlook) | Email nhận được |
| 3 | Xem header "Thông báo nghỉ việc gửi Adecco" | ✅ **Nền có màu** |
| 4 | Kiểm tra chữ | ✅ **Đọc được** |
| **Kết luận** | Header OK | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-4.2: Employee Info Render (Outlook)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Cùng email từ TC-4.1 | Email nhận được |
| 2 | Tìm bảng "Thông tin nhân viên" | Tìm thấy |
| 3 | Kiểm tra: Họ tên, Bộ phận, Chức vụ | ✅ **Tất cả PHẢI hiển thị text** (KHÔNG `<t t-out>` hoặc `{{ }}`) |
| **Kết luận** | Placeholder render OK | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-4.3: Chatter Render (Odoo)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Mở Approval Request → Chatter | Email log (nếu có) |
| 2 | Xem email HTML | Preview hiển thị |
| 3 | Kiểm tra header + info table | ✅ **Header có nền, info hiển thị text** |
| **Kết luận** | Chatter render OK | **PASS** ✅ / **FAIL** ❌ |

---

## III. BONUS TEST CASE — Chuẩn hóa (Phase 3)

#### **TC-5.1: Lang & Auto-Delete Field (dept template)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Settings → Technical → Email Template | List mở |
| 2 | Tìm: "OPS - Nhắc nhở công việc Offboarding (Bộ phận)" | Tìm thấy |
| 3 | Kiểm tra field "Language" (lang) | ✅ **PHẢI có value** (không blank): `{{ object.request_owner_id.lang }}` |
| 4 | Kiểm tra field "Auto-Delete" | ✅ **PHẢI = True** |
| **Kết luận** | Dept template đồng bộ với offboarding template | **PASS** ✅ / **FAIL** ❌ |

---

#### **TC-5.2: Border-Left Sub-properties (All templates)**

| Bước | Hành động | Kỳ vọng |
|---|---|---|
| 1 | Mở email HTML (bất kỳ template nào) | HTML source hiển thị |
| 2 | Search: `border-left:` (shorthand) | ✅ **KHÔNG tìm thấy** (đã sửa thành sub-property) |
| 3 | Search: `border-left-width:4px` | ✅ **Tìm thấy** |
| 4 | Search: `border-left-style:solid` | ✅ **Tìm thấy** |
| 5 | Search: `border-left-color:#da291c` | ✅ **Tìm thấy** |
| **Kết luận** | Border-left sub-property OK (4 file) | **PASS** ✅ / **FAIL** ❌ |

---

## IV. SUMMARY SHEET

Điền kết quả kiểm tra:

| # | Test Case | Template | Client/Chatter | Status | Notes |
|---|---|---|---|---|---|
| TC-1.1 | Header Background | dept_offboarding | Outlook | ⬜ | |
| TC-1.2 | Header Background | dept_offboarding | Gmail | ⬜ | |
| TC-1.3 | Placeholder Tên NV | dept_offboarding | Outlook | ⬜ | |
| TC-1.4 | Placeholder Tên NV | dept_offboarding | Gmail | ⬜ | |
| TC-1.5 | Border Left | dept_offboarding | Chatter | ⬜ | |
| TC-1.6 | Header Background | dept_offboarding | Chatter | ⬜ | |
| TC-2.1 | Header Background | offboarding | Outlook | ⬜ | |
| TC-2.2 | Placeholder Tên Owner | offboarding | Outlook | ⬜ | |
| TC-2.3 | Header + Border | offboarding | Chatter | ⬜ | |
| TC-3.1 | Header + Button | exit_survey | Outlook | ⬜ | |
| TC-3.2 | Survey Link | exit_survey | Outlook | ⬜ | |
| TC-3.3 | Chatter Render | exit_survey | Chatter | ⬜ | |
| TC-4.1 | Header Color | adecco | Outlook | ⬜ | |
| TC-4.2 | Employee Info | adecco | Outlook | ⬜ | |
| TC-4.3 | Chatter Render | adecco | Chatter | ⬜ | |
| TC-5.1 | Lang + Auto-Delete | dept_offboarding | Settings | ⬜ | |
| TC-5.2 | Border-Left Sub-prop | All × 4 | Source Code | ⬜ | |

**Legend:**
- ⬜ = Chưa test
- ✅ = PASS
- ❌ = FAIL

---

## V. CÁCH ĐIỀN & BÁO CÁO

### 1. Điền kết quả
```markdown
| TC-1.1 | Header Background | dept_offboarding | Outlook | ✅ | Nền đỏ, chữ trắng đọc được |
```

### 2. Nếu FAIL, log chi tiết:
```markdown
| TC-1.1 | Header Background | dept_offboarding | Outlook | ❌ | Nền vẫn trắng (not fixed) - Check: background-color missing? |
```

### 3. Report cuối:
```
PASSED: 15/17 (88%)
FAILED: 2/17 (12%)

Failed tests:
- TC-1.1: ...
- TC-5.2: ...

Root cause analysis:
- ...
```

---

## VI. EXPECTED RESULT

**Nếu Phase 1-4 thành công, tất cả TC PHẢI PASS ✅**

| Lỗi | TC COVER | Kỳ vọng PASS |
|---|---|---|
| Lỗi 1: Màu nền mất | TC-1.1, 1.2, 1.5, 1.6, 2.1, 2.3, 3.1, 3.3, 4.1, 4.3 | ✅ 10/10 |
| Lỗi 2: Placeholder `{{ }}` | TC-1.3, 1.4, 2.2, 4.2 | ✅ 4/4 |
| Phase 3: Robust hóa | TC-5.1, 5.2 | ✅ 2/2 |
| **TOTAL** | **17 test cases** | **✅ 16/17 PASS** |

> Nếu `< 15 PASS` → Có lỗi cần fix lại Phase 1-3.
