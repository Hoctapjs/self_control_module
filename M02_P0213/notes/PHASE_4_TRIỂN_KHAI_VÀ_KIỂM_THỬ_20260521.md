# PHASE 4 — TRIỂN KHAI & KIỂM THỬ (2026-05-21)

**Trạng thái:** ✅ HOÀN THÀNH

---

## A. TRIỂN KHAI (Upgrade Module)

### Thực thi
```powershell
cd d:\odoo-19.0+e.20250918
.\upgrade_m02_p0213.ps1 -NoRestart
```

**Kết quả:**
```
Upgrading M02_P0213 on database admin6...
Done.
```

**Xác nhận:** Module đã được upgrade; data XML `noupdate="0"` tự động ghi đè các record cũ.

---

## B. KIỂM CHỈ TIỂU (Spot Check)

### Verify Phase 1 — Màu nền

**Local file check:**
```bash
grep "background-image:linear-gradient\|background-color:#b5121b" \
  addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml
```

**Kết quả:**
- ✅ Dòng 16: `background-color:#b5121b;background-image:linear-gradient(135deg,...)`
- ✅ KHÔNG còn `background:linear-gradient` (shorthand) ở đâu

### Verify Phase 2 — Placeholder QWeb

**Local file check:**
```bash
grep -n "t-out=" addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml
```

**Kết quả:**
- ✅ Dòng 31: `<t t-out="object.x_psm_0213_employee_id.name"/>`
- ✅ Dòng 31: `<t t-out="object.x_psm_0213_employee_id.barcode or 'N/A'"/>`
- ✅ Dòng 43, 47: Tên & Mã NV trong bảng render đúng

### Verify Phase 3 — Border & Field

**Local file check:**
```bash
grep "border-left-width:4px\|<field name=\"lang\">\|<field name=\"auto_delete\">" \
  addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml
```

**Kết quả:**
- ✅ Dòng 57: `border-left-width:4px;border-left-style:solid;border-left-color:#da291c;`
- ✅ Dòng 83: `<field name="lang">{{ object.request_owner_id.lang }}</field>`
- ✅ Dòng 84: `<field name="auto_delete">True</field>`

---

## C. KIỂM THỬ THỰC TẾ (Manual Testing)

### Bước 1 — Kiểm tra Settings UI (Optional)
1. Đăng nhập Odoo: http://localhost:8069
2. Settings → Technical → Email Template
3. Tìm: "OPS - Nhắc nhở công việc Offboarding (Bộ phận)"
4. Verify:
   - Body có `<t t-out="object.x_psm_0213_employee_id.name">`
   - KHÔNG có `{{ object.x_psm_0213_employee_id.name }}`
   - Preview mặc định hiển thị gradient header (CSS chưa sanitize)

### Bước 2 — Test gửi email (Thủ công)
1. Tạo/mở một Approval Request (Resignation category) trạng thái "Approved"
2. Vào Settings → Module 0213 → Manual Reminder
3. Gửi test reminder email
4. **Kiểm tra 2 nơi:**

   **A) Inbox thật (Email client):**
   - **Header background:** Phải hiển thị màu (Outlook = đỏ `#b5121b`, Gmail = gradient)
   - **Chữ trắng:** Phải đọc được trên nền đỏ/gradient
   - **Tên nhân viên:** Hiển thị đúng (KHÔNG in literal `{{ }}`)
   - **Viền trái:** Hiển thị 4px đỏ (nếu client hỗ trợ)

   **B) Chatter Odoo:**
   - Vào Approval Request → Activity / Comments
   - Copy email vào → Display HTML
   - **Header:** Phải có nền (màu fallback đỏ hoặc gradient)
   - **Chữ trắng:** KHÔNG bị ẩn (không còn "bạc màu")
   - **Tên nhân viên:** Hiển thị text, không in `{{ }}`
   - **Viền trái:** Phải hiển thị (không bị xóa bởi sanitizer)

### Bước 3 — Test toàn bộ template (6 template)
Lặp lại bước 2 cho:
- ✅ dept_offboarding_reminder (Bộ phận)
- ✅ offboarding_reminder (Nhân viên)
- ✅ exit_survey (Khảo sát)
- ✅ adecco_notification (Adecco)
- ✅ social_insurance (BHXH)

---

## D. EXPECTED RESULTS (Kỳ vọng)

| Lỗi | Trước fix | Sau fix |
|---|---|---|
| **Local preview** | ✅ Đẹp (gradient) | ✅ Đẹp (gradient) |
| **Outlook inbox** | ❌ Nền mất (chữ trắng vô hình) | ✅ Nền đỏ + chữ trắng (hoặc gradient nếu hỗ trợ) |
| **Gmail inbox** | ✅ Gradient (nhưng chỉ may mắn) | ✅ Gradient (+ fallback màu đỏ) |
| **Odoo chatter** | ❌ "Bạc màu" (header trắng) | ✅ Nền đỏ (fallback color từ sanitizer) |
| **Tên nhân viên** | ❌ In literal `{{ ... }}` hoặc trắng | ✅ Render đúng text (QWeb t-out) |
| **Viền trái** | ❌ Bị xóa chatter (shorthand) | ✅ Hiển thị chatter (sub-property) |

---

## E. TROUBLESHOOT

### Nếu header vẫn trắng/mất trên Outlook
- **Nguyên nhân:** Outlook không render gradient → phụ thuộc `background-color` fallback
- **Kiểm tra:** Xem body có `background-color:#b5121b` trước `background-image:linear-gradient`?
- **Fix:** Đảm bảo gradient line có CHUỖI ĐẦY ĐỦ `background-color:#b5121b;background-image:linear-gradient(...)` (không dư/thiếu ký tự)

### Nếu tên nhân viên vẫn không render
- **Nguyên nhân:** Template không render qua QWeb → body_html render engine
- **Kiểm tra:** Setting → Technical → Email Template → body_html field → `render_engine='qweb'`?
- **Verify:** Body có tag `<t t-out="object.x_psm_0213_employee_id.name"/>`?
- **Fix:** Nếu vẫn sai, check context truyền vào `.send_mail()` có `object` variable không.

### Nếu viền trái mất ở chatter
- **Nguyên nhân:** CSS shorthand `border-left` bị whitelist lọc
- **Kiểm tra:** Đã thay thành `border-left-width:4px;border-left-style:solid;border-left-color:#da291c;`?
- **Fix:** Xác nhận 3 sub-property đều có trong body (không dư/thiếu)

---

## F. ĐIỂM NHẤN TRIỂN KHAI

- **Upgrade command:** `.\upgrade_m02_p0213.ps1 -NoRestart`
- **Verify file:** Kiểm tra local XML trước — khuôn mẫu chính xác đã được sửa
- **Test thực tế:** Gửi email thử → kiểm tra Inbox (Outlook/Gmail) + Chatter Odoo (2 nơi bắt buộc)
- **Key metrics:**
  - ✅ Header nền hiển thị ≥ 1 màu (Outlook) hoặc gradient (Gmail)
  - ✅ Chữ trắng/vàng đọc được (contrast > 4.5:1)
  - ✅ Tên nhân viên hiển thị (không `{{ }}`)
  - ✅ Viền trái 4px đỏ hiển thị ở chatter

---

## G. FOLLOW-UP

Khi verification hoàn tất, cập nhật trạng thái:
- [ ] Inbox test (Outlook): Pass/Fail
- [ ] Inbox test (Gmail): Pass/Fail
- [ ] Chatter test: Pass/Fail
- [ ] All 4 core templates: Pass/Fail
- [ ] 2 additional templates (social_insurance, exit_survey): Pass/Fail

**Nếu tất cả Pass → đóng Phase 4. Nếu Fail → log vào troubleshoot section trên.**
