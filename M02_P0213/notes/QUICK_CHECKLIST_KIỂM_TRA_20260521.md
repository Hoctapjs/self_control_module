# QUICK CHECKLIST — Kiểm tra nhanh Phase 1-4 (1 PAGE)

**Ngày:** 2026-05-21  
**Upgrade:** ✅ `.\upgrade_m02_p0213.ps1 -NoRestart`

---

## CHECKLIST KIỂM TRA NHANH (5 MIN)

### ✅ Step 1: Local File Verify (Command Line)
```bash
# Verify Phase 1 — No more `background:` shorthand
grep "background:" addons/M02_P0213/data/email_template_*.xml
# Expected: NO OUTPUT (empty)

# Verify Phase 2 — Has `t-out` tags
grep -c 't-out=' addons/M02_P0213/data/email_template_dept_offboarding_reminder.xml
# Expected: 3 (tên NV 3 chỗ)

# Verify Phase 3 — border-left sub-property
grep "border-left-width:4px" addons/M02_P0213/data/email_template_*.xml
# Expected: 4 lines (4 files)
```

---

### ✅ Step 2: Odoo Settings Verify (3 MIN)
1. Odoo → Settings → Technical → Email Template
2. Search: `Nhắc nhở công việc Offboarding (Bộ phận)` (dept template)
3. **VERIFY:**
   - [ ] Body hiển thị `<t t-out="object.x_psm_0213_employee_id.name"/>` (KHÔNG `{{ }}`)
   - [ ] Preview header có gradient (local editor không sanitize)
   - [ ] Có field `lang` (KHÔNG blank)
   - [ ] `auto_delete` = True

---

### ✅ Step 3: Send Test Email (5 MIN)

**Tạo test approval request:**
1. HR → Approvals → Create Test Resignation Request
   - Employee: `test@mcdonalds.vn`
   - Status: Approved
2. Action → Manual Reminder Extension
3. Email được gửi

---

### ✅ Step 4: Check Inbox (5 MIN — PER EMAIL CLIENT)

#### **OUTLOOK EMAIL:**
```
[Mở email từ Step 3]
- Header: [ ] Có nền màu (đỏ hoặc gradient) — KHÔNG trắng
- Chữ: [ ] Trắng/vàng đọc được — KHÔNG ẩn
- Tên NV: [ ] Hiển thị text (VD: "Huỳnh Thanh Sơn") — KHÔNG `{{ }}`
- Mã NV: [ ] Hiển thị số/mã — KHÔNG `{{ }}`
```

#### **GMAIL EMAIL:**
```
[Mở email từ Step 3]
- Header: [ ] Gradient hoặc màu đỏ — KHÔNG mất
- Chữ: [ ] Đọc được
- Tên + Mã: [ ] Text đúng
```

---

### ✅ Step 5: Check Odoo Chatter (2 MIN)

1. Odoo → Approval Request (từ Step 3)
2. Tab "Activity" → Xem email log
3. **VERIFY:**
   - [ ] Header hiển thị nền (KHÔNG "bạc màu")
   - [ ] Chữ trắng KHÔNG ẩn
   - [ ] Box "Cần xử lý" có viền trái đỏ (KHÔNG bị xóa)
   - [ ] Tên NV hiển thị text

---

## SCORING

**PASS CRITERIA:**

| Check | PASS | FAIL |
|---|---|---|
| **Local files** (4 verify) | ✅ Background shorthand GONE, t-out 3×, border-left 4 files | ❌ |
| **Settings** (dept template) | ✅ t-out + lang + auto_delete | ❌ |
| **Outlook inbox** | ✅ Header nền OK, tên render OK | ❌ |
| **Gmail inbox** | ✅ Gradient/nền OK, tên render OK | ❌ |
| **Chatter** | ✅ Nền + viền + tên OK | ❌ |

**Tổng kết:**
- ✅ **ALL PASS** → Phase 1-4 thành công ✅
- ❌ **ANY FAIL** → Xem TEST_CASE_PHASE_1_2_3_4_20260521.md để troubleshoot

---

## COMMON ISSUES & FIX

| Vấn đề | Nguyên nhân | Fix |
|---|---|---|
| Header vẫn trắng (Outlook) | `background-color` fallback thiếu | Check line 16: `background-color:#b5121b;background-image:...` |
| Tên NV hiển thị `{{ }}` | `t-out` không render (engine sai) | Check body_html `render_engine='qweb'` |
| Viền trái mất (chatter) | Shorthand `border-left` bị lọc | Check: `border-left-width:4px;border-left-style:solid;border-left-color:...` |
| Email không gửi được | SMTP sai hoặc sandbox mode | Check: Mail Server settings, test send qua UI |

---

## QUICK LINKS

- **Full test case:** `TEST_CASE_PHASE_1_2_3_4_20260521.md`
- **Deployment guide:** `PHASE_4_TRIỂN_KHAI_VÀ_KIỂM_THỬ_20260521.md`
- **Implementation plan:** `PLAN_FIX_EMAIL_TEMPLATE_0213_20260521.md`

---

**Time to test:** ~15-20 MIN  
**Files to verify:** 4  
**Templates to test:** 4  
**Clients to check:** 3 (Outlook, Gmail, Chatter)
