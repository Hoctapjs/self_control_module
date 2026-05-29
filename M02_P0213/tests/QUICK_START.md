# ⚡ QUICK START — Test trong 30 giây

## 1️⃣ Copy command dưới đây

```powershell
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=M02_P0213,email_template --stop-after-init
```

## 2️⃣ Paste vào Terminal (PowerShell hoặc VSCode terminal)

## 3️⃣ Nhấn Enter & Chờ ~5 giây

## 4️⃣ Xem kết quả

### ✅ Nếu thấy `Ran 12 tests in X.XXs - OK`
→ **Test PASS** ✅ — Template fix đúng!

### ❌ Nếu thấy `FAILED: X/12`
→ **Test FAIL** ❌ — Xem error message  
→ Fix Phase 1-3 lại  
→ Upgrade module rồi chạy lại

---

## Troubleshoot nhanh

| Lỗi | Fix |
|---|---|
| "Module not found" | `docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf -u M02_P0213 --stop-after-init` |
| "Template not found" | Check XML ID ở `/data/email_template_*.xml` |
| Phase 1 fail | Kiểm tra `background-color:#b5121b` + `background-image:linear-gradient` |
| Phase 2 fail | Kiểm tra `<t t-out="object.x_psm_0213_employee_id.name"/>` |
| Phase 3 fail | Kiểm tra `border-left-width:4px;border-left-style:solid;border-left-color:#da291c` |

---

## Test riêng (nếu muốn)

```powershell
# Chỉ Phase 1
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=phase_1_2_3_4 -k "test_phase1" --stop-after-init

# Chỉ Phase 2
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=phase_1_2_3_4 -k "test_phase2" --stop-after-init

# Chỉ Phase 3
docker exec odoo-190e20250918-web-1 python3 /opt/odoo/setup/odoo -d admin6 -c /opt/odoo/odoo.conf --test-tags=phase_1_2_3_4 -k "test_phase3" --stop-after-init
```

---

**For details:** xem `RUN_TEST_GUIDE.md`  
**For implementation:** xem `test_email_template_fixes.py`

---

**Thế là xong! 🎉**
