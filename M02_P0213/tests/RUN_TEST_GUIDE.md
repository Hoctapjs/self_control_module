# 🧪 HƯỚNG DẪN CHẠY TEST — Dành cho người mới

**File test:** `addons/M02_P0213/tests/test_email_template_fixes.py`

---

## I. CHUẨN BỊ

### Điều kiện
- ✅ Odoo đang chạy (`http://localhost:8069`)
- ✅ Docker compose chạy (nếu dùng Docker)
- ✅ Module M02_P0213 đã upgrade (Phase 1-4 hoàn tất)

### Kiểm tra:
```bash
# Check Docker running
docker ps | grep odoo

# Output expected:
# odoo-190e20250918-web-1  ...  Up ...
# odoo-190e20250918-db-1   ...  Up ...
```

---

## II. CHẠY TEST (3 CÁCH)

### **CÁCH 1: Docker (Khuyến nghị — Dễ nhất) ⭐**

#### Bước 1: Mở Terminal

**Windows:**
- Bấm `Win + R` → gõ `powershell` → Enter

**hoặc mở VSCode:**
- Bấm `Ctrl + \`` → chọn Terminal mới

#### Bước 2: Copy & Paste command dưới đây

```powershell
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 `
  -c /opt/odoo/odoo.conf `
  --test-tags=M02_P0213,email_template `
  --stop-after-init
```

#### Bước 3: Nhấn Enter & Chờ kết quả

**Output expected (Thành công):**
```
....
test_phase1_dept_reminder_header_gradient_and_color ... ok
test_phase1_offboarding_reminder_header_color ... ok
test_phase1_exit_survey_header_and_button_color ... ok
test_phase1_adecco_notification_header_color ... ok
test_phase2_dept_reminder_employee_name_placeholder_render ... ok
test_phase2_offboarding_reminder_request_owner_name_render ... ok
test_phase2_exit_survey_placeholder_not_literal ... ok
test_phase3_dept_reminder_border_left_sub_property ... ok
test_phase3_all_templates_border_left_sub_property ... ok
test_phase3_dept_reminder_has_lang_field ... ok
test_phase3_dept_reminder_auto_delete_true ... ok
test_send_dept_reminder_email ... ok

Ran 12 tests in 3.456s - OK
```

**Nếu có lỗi:**
- Xem phần **TROUBLESHOOT** dưới đây

---

### **CÁCH 2: Local (Nếu Odoo chạy local, không Docker)**

#### Bước 1: Mở PowerShell

```powershell
cd d:\odoo-19.0+e.20250918
```

#### Bước 2: Chạy command

```powershell
python odoo-bin `
  -d admin6 `
  -c odoo.conf `
  --test-tags=M02_P0213,email_template `
  --stop-after-init
```

#### Bước 3: Chờ kết quả

---

### **CÁCH 3: Chạy từ VSCode (UI-friendly)**

#### Bước 1: Mở file test

```
addons/M02_P0213/tests/test_email_template_fixes.py
```

#### Bước 2: Cài extension

- Extensions (Ctrl + Shift + X) → tìm "Python Test Explorer"
- Cài & Enable

#### Bước 3: Click "Test" icon ở thanh sidebar

- Chuột phải trên class → "Run tests"
- Hoặc: Bấm ▶️ ở trên hàm `def test_...`

#### Bước 4: Xem kết quả ở Output panel

---

## III. HIỂU KẾT QUẢ

### ✅ **Test PASS (Thành công)**

```
test_phase1_dept_reminder_header_gradient_and_color ... ok
```

**Ý nghĩa:** Test chạy thành công → Template đã fix đúng ✅

### ❌ **Test FAIL (Thất bại)**

```
test_phase1_dept_reminder_header_gradient_and_color ... FAIL
----------------------------------------------------------------------
AssertionError: ❌ FAIL: Header PHẢI có background-color:#b5121b (fallback cho Outlook)
   Expected: background-color:#b5121b;background-image:linear-gradient(...)
   Problem: Outlook không support gradient → cần fallback color
```

**Ý nghĩa:** Template chưa fix hoặc fix sai → cần kiểm tra lại

### 📊 **Summary (Tóm tắt)**

```
Ran 12 tests in 3.456s - OK
```

**Ý nghĩa:** Chạy 12 test, tất cả PASS ✅

---

## IV. TROUBLESHOOT (Nếu test fail)

### ❌ "Module M02_P0213 not found"

**Nguyên nhân:** Module chưa được load  
**Fix:**
```powershell
# Upgrade module trước
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf -u M02_P0213 --stop-after-init
```

---

### ❌ "Template ... not found"

**Nguyên nhân:** XML ID sai  
**Fix:**
```powershell
# Check template XML ID ở:
# addons/M02_P0213/data/email_template_*.xml
# Dòng: <record id="psm_0213_email_template_...">
```

---

### ❌ "❌ FAIL: Header PHẢI có background-color:#b5121b"

**Nguyên nhân:** Template chưa fix Phase 1  
**Fix:**
```bash
# Kiểm tra file local
grep "background-color:#b5121b" addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml

# Nếu không tìm thấy → fix Phase 1 lại
# (xem PLAN_FIX_EMAIL_TEMPLATE_0213_20260521.md)
```

---

### ❌ "❌ FAIL: Tìm thấy literal placeholder"

**Nguyên nhân:** Template chưa fix Phase 2  
**Fix:**
```bash
# Kiểm tra file local
grep 't-out="object.x_psm_0213_employee_id.name"' addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml

# Nếu không tìm thấy → fix Phase 2 lại
```

---

### ❌ "❌ FAIL: PHẢI có border-left-width:4px"

**Nguyên nhân:** Template chưa fix Phase 3  
**Fix:**
```bash
# Kiểm tra file local
grep "border-left-width:4px" addons/M02_P0213/data/email_template_*.xml

# Nếu không tìm thấy → fix Phase 3 lại
```

---

### ❌ "Assertion error: ... not in rendered"

**Nguyên nhân:** Template render sai hoặc dữ liệu test sai  
**Fix:**
```powershell
# Re-upgrade module
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf -u M02_P0213 --stop-after-init

# Chạy lại test
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=M02_P0213,email_template --stop-after-init
```

---

## V. CHẠY TEST RIÊNG (Nếu muốn test 1 cái)

### Test Phase 1 (Màu nền)

```powershell
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=phase_1_2_3_4 `
  -k "test_phase1" `
  --stop-after-init
```

### Test Phase 2 (Placeholder)

```powershell
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=phase_1_2_3_4 `
  -k "test_phase2" `
  --stop-after-init
```

### Test Phase 3 (Border-left)

```powershell
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=phase_1_2_3_4 `
  -k "test_phase3" `
  --stop-after-init
```

---

## VI. CHẠY TEST + XEM LIVE OUTPUT

**Nếu muốn xem output tức thì (không chờ kết thúc):**

```powershell
# Docker (stream output)
docker exec -it odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=M02_P0213,email_template `
  --stop-after-init --no-http
```

**Output:**
```
Loading module M02_P0213...
test_phase1_dept_reminder_header_gradient_and_color ... ok (0.123s)
test_phase1_offboarding_reminder_header_color ... ok (0.105s)
...
Ran 12 tests in 3.456s - OK
```

---

## VII. QUICK REFERENCE

| Mục đích | Command |
|---|---|
| Chạy tất cả test M02_P0213 | `--test-tags=M02_P0213` |
| Chạy test email template | `--test-tags=email_template` |
| Chạy test Phase 1-4 | `--test-tags=phase_1_2_3_4` |
| Chỉ chạy test Phase 1 | `--test-tags=phase_1_2_3_4 -k "test_phase1"` |
| Chạy test gửi mail | `--test-tags=send_mail` |
| Chạy ngay khi viết (VSCode) | Bấm ▶️ bên cạnh test name |

---

## VIII. KỲ VỌNG (EXPECTED RESULTS)

### ✅ Nếu Phase 1-4 fix đúng

```
test_phase1_dept_reminder_header_gradient_and_color ... ok
test_phase1_offboarding_reminder_header_color ... ok
test_phase1_exit_survey_header_and_button_color ... ok
test_phase1_adecco_notification_header_color ... ok
test_phase2_dept_reminder_employee_name_placeholder_render ... ok
test_phase2_offboarding_reminder_request_owner_name_render ... ok
test_phase2_exit_survey_placeholder_not_literal ... ok
test_phase3_dept_reminder_border_left_sub_property ... ok
test_phase3_all_templates_border_left_sub_property ... ok
test_phase3_dept_reminder_has_lang_field ... ok
test_phase3_dept_reminder_auto_delete_true ... ok
test_send_dept_reminder_email ... ok

Ran 12 tests in 3.456s - OK ✅
```

### ❌ Nếu có lỗi

```
test_phase1_dept_reminder_header_gradient_and_color ... FAIL
test_phase2_dept_reminder_employee_name_placeholder_render ... FAIL

FAILED: 2/12 (17%)
```

→ Xem error message chi tiết (nó sẽ nói cần fix gì)  
→ Fix Phase 1-3 lại  
→ Upgrade module  
→ Chạy test lại

---

## IX. TEST THỰC TRÊN INBOX (KHÔNG AUTO)

Test chỉ verify code logic. Để test thực trên email client (Outlook/Gmail):

1. **Tạo approval request** → HR → Approvals
2. **Gửi email** → Actions → Manual Reminder
3. **Kiểm tra Inbox** (Outlook/Gmail):
   - ✅ Header có nền màu (không "bạc màu")
   - ✅ Tên NV hiển thị (KHÔNG `{{ }}`)
   - ✅ Viền trái hiển thị
4. **Kiểm tra Chatter** (Odoo):
   - ✅ Cũng có nền + viền

(Chi tiết tại `QUICK_CHECKLIST_KIỂM_TRA_20260521.md`)

---

## X. THÊM TEST MỚI (Nếu muốn)

### Bước 1: Mở file test

```
addons/M02_P0213/tests/test_email_template_fixes.py
```

### Bước 2: Thêm method mới

```python
def test_my_new_feature(self):
    """Describe what you test"""
    rendered = self._render_template_body(
        'M02_P0213.psm_0213_email_template_...'
    )
    
    self.assertIn('expected text', rendered)
    self.assertNotIn('unwanted text', rendered)
```

### Bước 3: Chạy test

```powershell
# Sẽ tự chạy test mới
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo `
  -d admin6 -c /opt/odoo/odoo.conf `
  --test-tags=M02_P0213 --stop-after-init
```

---

**Happy testing! 🎉**

---

## **Cheat Sheet (Copy-paste nhanh)**

```powershell
# Chạy tất cả test email template 0213
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=M02_P0213,email_template --stop-after-init

# Chỉ test Phase 1
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=phase_1_2_3_4 -k "test_phase1" --stop-after-init

# Upgrade + Test
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf -u M02_P0213 --stop-after-init && docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=M02_P0213,email_template --stop-after-init
```
