# M09_0901_demo — Dữ Liệu Mẫu Xuyên Suốt 0801 + 0901

> Module dữ liệu mẫu liên thông cho 2 quy trình:
> - **M08_P0801** — PIF Management (Product Initiation Form, phòng RSG)
> - **M09_0901** — PAF Management (Project/Promotion Approval Form, phòng MKT)
>
> Sau khi cài, ta có ngay 11 PAF demo phủ đủ 10 state + 1 case end-to-end đi
> trọn vẹn 12 bước nghiệp vụ, có liên kết PIF object thực tế.

---

## 1. Mục tiêu

Tạo bộ dữ liệu mẫu tối thiểu nhưng đầy đủ để:

1. **Demo UI từng state** — mỗi state quan trọng của `mkt_paf.request` có ít
   nhất 1 record để screenshot / training.
2. **Demo luồng tích hợp** — 1 PAF (`PAF-DEMO-E2E`) đi từ MKT tạo phiếu
   → đánh giá 5 phòng → duyệt Heads → duyệt C-Level → trigger PIF tại M08
   → publish Valuation report. Đây là case duy nhất chạm vào cả 2 module.
3. **Tận dụng lại** dữ liệu sẵn có trong `M08_P0801_demo` (department,
   user, product, BOM, PIF) — chỉ bổ sung phần mà PAF cần thêm.

---

## 2. Quan hệ giữa các module

```
base, mail, hr, product, mrp, ...
            │
            ▼
     ┌──────────────┐
     │  M08_P0801   │  (PIF Management)
     └──────┬───────┘
            │
   ┌────────┴─────────┐
   ▼                  ▼
┌──────────────┐  ┌──────────────┐
│M08_P0801_demo│  │  M09_0901    │ (PAF, kéo theo purchase/loyalty/POS/...)
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
         ┌──────────────┐
         │M09_0901_demo │  (module này — depends cả 2 nhánh)
         └──────────────┘
```

`M09_0901_demo.depends = ['M08_P0801_demo', 'M09_0901']`.

---

## 3. Thứ tự install bắt buộc

> ⚠️ KHÔNG cài `M08_P0801_demo` trước `M09_0901`. File
> `M08_P0801_demo/data/05_partners.xml:6` dùng field `supplier_rank` mà
> field này chỉ tồn tại sau khi `purchase` được kéo vào — `purchase` được
> kéo theo `M09_0901`, không được kéo theo `M08_P0801`.

```powershell
# 1. PIF core
powershell -ExecutionPolicy Bypass -File "tools\Invoke-OdooModule.ps1" -Module M08_P0801 -Action install -Database admin

# 2. PAF core (KÉO purchase + loyalty + point_of_sale + account)
powershell -ExecutionPolicy Bypass -File "tools\Invoke-OdooModule.ps1" -Module M09_0901 -Action install -Database admin

# 3. PIF demo data (cần purchase đã có)
powershell -ExecutionPolicy Bypass -File "tools\Invoke-OdooModule.ps1" -Module M08_P0801_demo -Action install -Database admin

# 4. PAF demo data + post_init_hook chạy end-to-end
powershell -ExecutionPolicy Bypass -File "tools\Invoke-OdooModule.ps1" -Module M09_0901_demo -Action install -Database admin
```

Tổng thời gian: ~4–5 phút trên DB sạch.

---

## 4. Cấu trúc thư mục

```
M09_0901_demo/
├── __init__.py                          # import hooks
├── __manifest__.py                      # depends + 'post_init_hook'
├── hooks.py                             # post_init_hook + case end-to-end
└── data/
    ├── 01_extra_departments.xml         # OPS, Finance, Legal
    ├── 02_extra_users_employees.xml     # 6 user + 6 employee (3 phòng × 2)
    ├── 03_paf_master_data_patch.xml     # bật paf_can_use cho FG + BOM
    ├── 04_paf_templates.xml             # 2 template PAF
    ├── 05_paf_static_states.xml         # 10 PAF mỗi cái 1 state
    └── 06_grant_paf_groups.xml          # gán group M09_0901 cho user demo
```

---

## 5. Phần dữ liệu được tạo / patched

### 5.1 Departments (`01_extra_departments.xml`)

Tận dụng từ `M08_P0801_demo`: `dept_rsg`, `dept_it`, `dept_menu`,
`dept_digital`, `dept_mkt`, `dept_si`, `dept_sc`. Bổ sung 3 phòng mới mà
PAF evaluation cần:

| XML ID | Tên | Lý do |
|---|---|---|
| `M09_0901_demo.dept_ops` | OPS | đánh giá B5 (`pilot_capacity_score`) |
| `M09_0901_demo.dept_finance` | Finance | đánh giá B6 (`roi_estimated_percent`) |
| `M09_0901_demo.dept_legal` | Legal | đánh giá B8 (`regulatory_sla_days`) |

> Tên được chọn để `_get_dept_code_mapping` trong
> `mkt_paf.evaluation.line` tự map đúng `department_code`:
> "OPS" → `ops`, "Finance" → `finance`, "Legal" → `legal`.

### 5.2 Users + Employees (`02_extra_users_employees.xml`)

6 user mới (mỗi phòng 1 nhân viên + 1 trưởng phòng), mật khẩu `1`:

| Login | Role | Phòng |
|---|---|---|
| `demo.ops@mcvn.local` | OPS Evaluator | OPS |
| `demo.ops.head@mcvn.local` | OPS Head | OPS |
| `demo.finance@mcvn.local` | Finance Evaluator | Finance |
| `demo.finance.head@mcvn.local` | Finance Head | Finance |
| `demo.legal@mcvn.local` | Legal Evaluator | Legal |
| `demo.legal.head@mcvn.local` | Legal Head | Legal |

6 `hr.employee` link `user_id` → `department_id`. 3 phòng mới được gán
`manager_id` ở data block không-noupdate (để mỗi lần upgrade vẫn được
reconcile).

### 5.3 Master data patch (`03_paf_master_data_patch.xml`)

Bật `paf_can_use = True` cho 3 thành phẩm + 3 BOM hiện có trong
`M08_P0801_demo`:

- `demo_tmpl_spicy_mcdouble` + `demo_bom_spicy_mcdouble`
- `demo_tmpl_bbq_chicken_burger` + `demo_bom_bbq_chicken`
- `demo_tmpl_mccrispy` + `demo_bom_mccrispy`

Dùng `<function name="write">` để patch — không tạo record mới.

### 5.4 PAF Templates (`04_paf_templates.xml`)

| XML ID | Tên | Required Departments |
|---|---|---|
| `demo_paf_template_lto` | LTO Promotion — Mẫu chuẩn 5 phòng ban | S&I, OPS, Finance, SC, Legal |
| `demo_paf_template_core` | Core Product Launch — Mẫu rút gọn 3 phòng ban | S&I, Finance, SC |

### 5.5 PAF Static states (`05_paf_static_states.xml`)

10 record `mkt_paf.request`, mỗi cái 1 state. Dùng `<field name="state">…</field>`
trực tiếp để bypass workflow — phù hợp cho demo UI từng state.

| XML ID | Name | State | Đặc trưng |
|---|---|---|---|
| `demo_paf_draft` | PAF-DEMO-DRAFT | `draft` | MKT vừa tạo, chưa điền đủ |
| `demo_paf_eval` | PAF-DEMO-EVAL | `dept_evaluation` | 3 line `done` + 1 `in_review` + 1 `pending` |
| `demo_paf_head` | PAF-DEMO-HEAD | `head_approval` | 3 line eval đã `done` |
| `demo_paf_clevel` | PAF-DEMO-CLEVEL | `clevel_approval` | — |
| `demo_paf_approved` | PAF-DEMO-APPROVED | `approved` | vừa duyệt, chưa trigger PIF |
| `demo_paf_pif` | PAF-DEMO-PIF | `pif_running` | `pif_object_id` → `M08_P0801_demo.demo_pif_003` (McChicken Crispy) |
| `demo_paf_val` | PAF-DEMO-VAL | `valuation` | + 1 `mkt_paf.valuation.report` (draft) |
| `demo_paf_done` | PAF-DEMO-DONE | `done` | + 1 report (published) |
| `demo_paf_rej` | PAF-DEMO-REJ | `rejected` | có 1 eval line `failed` của Legal |
| `demo_paf_cancel` | PAF-DEMO-CANCEL | `cancelled` | — |

### 5.6 Groups grant (`06_grant_paf_groups.xml`)

Gán group `M09_0901.MKT_0901_*` cho user demo qua `<function name="write">`,
để khi đăng nhập demo user vào UI là dùng được luôn:

| User | Group |
|---|---|
| `demo_user_mkt`, `demo_user_mkt_head` | `MKT_0901_creator` |
| `demo_user_si`, `demo_user_si_head` | `MKT_0901_si_analyst` |
| `demo_user_ops`, `demo_user_ops_head` | `MKT_0901_ops_evaluator` |
| `demo_user_finance`, `demo_user_finance_head` | `MKT_0901_finance_evaluator` |
| `demo_user_sc`, `demo_user_sc_head` | `MKT_0901_sc_evaluator` |
| `demo_user_legal`, `demo_user_legal_head` | `MKT_0901_legal_evaluator` |
| Tất cả `*_head` (10 user) | `MKT_0901_approver_head` |
| `demo_user_mkt_head` | `MKT_0901_clevel_approver` |

---

## 6. Post-init hook — case end-to-end

`hooks.py` chạy 1 lần khi module được cài, tạo `PAF-DEMO-E2E` đi trọn 12
bước nghiệp vụ. **Idempotent** — nếu PAF-DEMO-E2E đã tồn tại thì hook bỏ
qua.

### 6.1 Tiền xử lý — `_configure_approval_categories(env)`

3 approval category bắt buộc phải có ít nhất 1 approver để
`action_confirm()` không raise UserError. Hook tự gán:

| Category | Approver | Minimum |
|---|---|---|
| `M09_0901.mkt_0901_approval_category_paf_head` | `demo_user_mkt_head` | 1 |
| `M09_0901.mkt_0901_approval_category_paf_clevel` | `demo_user_mkt_head` | 1 |
| `M08_P0801.approval_category_data_pif` | `demo_user_rsg_head` | 1 |

> Production thực tế sẽ cấu hình thủ công qua UI Approvals > Categories.
> Hook chỉ patch nếu `approver_ids` còn rỗng (idempotent).

### 6.2 Luồng `_build_and_run_e2e(env)` — 12 bước

```
B3  draft
      │  paf.action_submit_to_evaluation()  (sudo, tránh AccessError)
      ▼
B4-8 dept_evaluation                    │
      │  for line in evaluation_line_ids:
      │      line.action_start_review()
      │      line.write(<dept-specific fields>)
      │      line.action_submit_done()   ← line cuối auto trigger
      │         _notify_all_evaluations_complete()
      │         → action_collect_evaluations()
      ▼
B9   head_approval (head_approval_request_id created)
      │  paf.action_request_clevel()     (bypass duyệt thật)
      ▼
B10  clevel_approval (clevel_approval_request_id created)
      │  paf.action_mark_approved()
      │  → state=approved → _run_pif_workflow()
      │     → tạo approval.request category PIF (marketing, không fast-track)
      │     → state=pif_running
      ▼
B11  pif_running (PIF approval.request created, chưa có pif_object)
      │  _create_pif_object_for_paf(env, paf)
      │  → env['x_psm_pif_object'].create({..., state='lab_test'})
      │  → override M09_0901/models/pif_object.py.create() set paf.pif_object_id
      ▼
     pif_running + pif_object_id
      │  paf.action_open_valuation()
      ▼
B12  valuation (mkt_paf.valuation.report draft)
      │  report.write({actual_revenue, actual_cost, summary_html})
      │  report.action_publish()
      ▼
     done
```

### 6.3 Payload eval line theo `department_code`

```python
EVAL_PAYLOAD = {
    'si':      {forecast_demand=1800, confidence_score=0.91, ...},
    'ops':     {pilot_capacity_score='high', bottleneck_note=..., ...},
    'finance': {roi_estimated_percent=42.5, gross_margin_estimated=175M, ...},
    'sc':      {supply_risk_level='low', lead_time_days=10, ...},
    'legal':   {regulatory_sla_days=30, requires_government_approval=True, ...},
}
```

Phải khớp validation trong `mkt_paf.evaluation.line.action_submit_done()`,
nếu không sẽ raise `ValidationError`.

---

## 7. Quá trình triển khai thực tế

Tóm lược những lỗi đã gặp và cách giải khi build module này:

### 7.1 Lỗi: `supplier_rank` không tồn tại trên `res.partner`

**Triệu chứng:** install `M08_P0801_demo` trực tiếp sau `M08_P0801` →
`ParseError ... Invalid field 'supplier_rank' in 'res.partner'`.

**Nguyên nhân:** `supplier_rank` đến từ module `purchase`. `M08_P0801` không
depends `purchase`, nên `purchase` chưa được cài.

**Giải pháp:** Cài `M09_0901` trước `M08_P0801_demo` (M09_0901 depends
purchase). Đó là lý do thứ tự install ở mục 3 đảo so với thứ tự tự nhiên.

### 7.2 Lỗi: `AccessError ... PAF Request`

**Triệu chứng:** hook ban đầu dùng
`PafRequest.with_user(creator).create({...})` → `demo_user_mkt` chưa có
group `MKT_0901_creator` → AccessError.

**Giải pháp:**
1. Bỏ `.with_user(creator)`, dùng thẳng `PafRequest.sudo().create(...)`.
   `creator_id` vẫn được set qua vals → computed
   `creator_department_id` / `creator_job_id` vẫn đúng.
2. Tạo file `06_grant_paf_groups.xml` để gán group cho user demo. Lần
   sau đăng nhập demo dùng UI là có quyền luôn.

### 7.3 Lỗi: `You have to add at least N approvers to confirm your request`

**Triệu chứng:** `action_collect_evaluations()` → `request.action_confirm()`
fail vì approval category không có approver được pre-config.

**Áp dụng cho 3 category:**
- `mkt_0901_approval_category_paf_head` (`approval_minimum=5` mặc định)
- `mkt_0901_approval_category_paf_clevel`
- `approval_category_data_pif` (M08, `approval_minimum=1` nhưng không
  approver)

**Giải pháp:** thêm `_configure_approval_categories(env)` vào hook, chạy
trước `_build_and_run_e2e()`. Gán 1 approver + `approval_minimum=1`.
Idempotent — chỉ ghi nếu chưa có approver.

### 7.4 Bài học: log của post_init_hook đi đâu?

Tool `Invoke-OdooModule.ps1` dùng `docker-compose run --rm` → spin up
container tạm, log đi ra stdout/stderr của lệnh đó (PowerShell capture
vào biến `$output`), **không** đi vào `/var/log/odoo/odoo.log` của
container web đang chạy. Tool chỉ in lại các dòng match
`ERROR|CRITICAL|WARNING|modules loaded`. Hook chỉ log `INFO` → không
hiện ra.

**Cách debug hook khi cần xem log INFO:** chạy tay trong container:

```powershell
docker exec odoo-190e20250918-web-1 bash -c 'cd /opt/odoo && python3 << "EOF"
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
from odoo.tools import config
config.parse_config(["-c", "/opt/odoo/odoo.conf"])
from odoo.api import Environment
from odoo.modules.registry import Registry
reg = Registry("admin")
with reg.cursor() as cr:
    env = Environment(cr, 1, {})
    from odoo.addons.M09_0901_demo.hooks import post_init_hook
    post_init_hook(env)
    cr.commit()
EOF'
```

> Lưu ý: hook là idempotent (return sớm nếu `PAF-DEMO-E2E` đã tồn tại).
> Muốn rerun, xóa trước: `DELETE FROM mkt_paf_request WHERE name = 'PAF-DEMO-E2E';`

---

## 8. Verify sau khi cài

### 8.1 Đếm 11 PAF + state phân bố

```sql
SELECT name, state, pif_object_id
FROM mkt_paf_request
ORDER BY id;
```

Phải thấy đủ 11 dòng. `PAF-DEMO-PIF` link đến `M08_P0801_demo.demo_pif_003`,
`PAF-DEMO-E2E` link đến PIF mới tạo state `lab_test`.

### 8.2 Eval lines của PAF-DEMO-E2E

```sql
SELECT r.name, l.department_code, l.status
FROM mkt_paf_evaluation_line l
JOIN mkt_paf_request r ON r.id = l.paf_request_id
WHERE r.name = 'PAF-DEMO-E2E'
ORDER BY l.sequence;
```

5 line, đều `done`, department_code = `si|ops|finance|sc|legal`.

### 8.3 Valuation reports

```sql
SELECT r.name, v.status, v.actual_revenue, v.actual_cost
FROM mkt_paf_valuation_report v
JOIN mkt_paf_request r ON r.id = v.paf_request_id
ORDER BY r.id;
```

3 record: `PAF-DEMO-VAL` (draft), `PAF-DEMO-DONE` (published),
`PAF-DEMO-E2E` (published).

### 8.4 Đăng nhập UI

| Login | Mật khẩu | Vai trò trong PAF |
|---|---|---|
| `admin` | (như cài đặt) | full admin |
| `demo.mkt@mcvn.local` | `1` | Creator — tạo / sửa PAF |
| `demo.mkt.head@mcvn.local` | `1` | Head + C-Level Approver |
| `demo.si@mcvn.local` | `1` | S&I Evaluator |
| `demo.ops@mcvn.local` | `1` | OPS Evaluator |
| `demo.finance@mcvn.local` | `1` | Finance Evaluator |
| `demo.sc@mcvn.local` | `1` | SC Evaluator |
| `demo.legal@mcvn.local` | `1` | Legal Evaluator |
| `demo.rsg.head@mcvn.local` | `1` | PIF Approver (M08) |

---

## 9. Reset / rerun

### 9.1 Rerun chỉ hook end-to-end (giữ static records)

```sql
-- Xóa PAF-DEMO-E2E + cascade (eval lines, valuation report)
DELETE FROM mkt_paf_request WHERE name = 'PAF-DEMO-E2E';
```

Rồi chạy lại hook bằng snippet ở mục 7.4.

### 9.2 Reset toàn bộ demo data

```powershell
# Uninstall theo thứ tự ngược
powershell -ExecutionPolicy Bypass -File "tools\Invoke-OdooModule.ps1" -Module M09_0901_demo -Action uninstall -Database admin
# rồi cài lại theo thứ tự mục 3
```

---

## 10. Field / Method tham chiếu (cheat sheet)

| Model | Field / Method | Ghi chú |
|---|---|---|
| `mkt_paf.request` | `state` selection | 10 giá trị (xem `mkt_paf_request.py:67-78`) |
| `mkt_paf.request` | `action_submit_to_evaluation()` | yêu cầu `state='draft'` + `planned_start_date` + `planned_end_date` |
| `mkt_paf.request` | `action_collect_evaluations()` | tự gọi từ line.action_submit_done() khi tất cả `done` |
| `mkt_paf.request` | `action_request_clevel()` | không validate state — bypass được |
| `mkt_paf.request` | `action_mark_approved()` | gọi `_run_pif_workflow()` |
| `mkt_paf.request` | `_run_pif_workflow()` | tạo approval.request PIF (marketing **không** fast-track) |
| `mkt_paf.request` | `action_open_valuation()` | yêu cầu `state='pif_running'` |
| `mkt_paf.evaluation.line` | `action_submit_done()` | validate field theo `department_code` |
| `mkt_paf.valuation.report` | `action_publish()` | đặt `paf.state='done'`; có sql_constraint unique(paf_request_id) |
| `x_psm_pif_object` (M09 override) | `create()` | tự set `paf.pif_object_id` qua `x_psm_approval_request_id.x_psm_mkt_paf_request_id` |
| `approval.category` | `approver_ids` One2many → `approval.category.approver(user_id)` | dùng để pre-config approver |
| `approval.request.action_confirm()` | raise nếu `len(approver_ids) < approval_minimum` | xem `approvals/models/approval_request.py:158` |
