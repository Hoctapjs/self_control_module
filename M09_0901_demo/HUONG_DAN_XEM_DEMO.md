# Hướng Dẫn Xem & Thao Tác Demo — M09_0901_demo v19.0.0.3.0

> Hướng dẫn dùng dữ liệu mẫu của `M09_0901_demo` để xem nhanh giao diện
> từng state của PAF, thao tác thử các vai trò trong luồng 0801 + 0901,
> và verify các ràng buộc pháp lý VN (Nghị định 81/2018) cùng workflow
> banner/hình ảnh sản phẩm.
>
> **Phiên bản:** `19.0.0.3.0` — đã có đủ Phase 1 (90 ngày + promotion_type),
> Phase 2 (gift/discount/channel/ATTP/template) và Phase 3 (banner + brand reviewer + sync PIF).
>
> Trước khi đọc, cần đã cài 4 module theo thứ tự trong [README.md](README.md) mục 3.

---

## 1. URL & menu chính

| Mục đích | Vị trí |
|---|---|
| Đăng nhập Odoo | `http://localhost:8069` (DB `admin`) |
| Menu chính PAF | App switcher → **PAF** (icon vàng/đỏ) |
| Menu PIF (M08) | App switcher → **Approvals** → category *Product Initiation Form (PIF)* |

Menu **PAF**:

```
PAF
├── PAF của tôi
├── Đang chờ tôi đánh giá
├── Đang chờ tôi duyệt
├── Templates
├── Valuation Reports
├── Báo cáo Valuation
├── PSPD Forecast
└── Cấu hình → Categories duyệt
```

---

## 2. Bảng tra cứu user demo

Mọi user demo có mật khẩu `1`.

| Login | Vai trò | Vào đâu để thấy việc của mình |
|---|---|---|
| `admin` | System | Thấy tất cả |
| `demo.mkt@mcvn.local` | **PAF Creator** (MKT) | PAF → *PAF của tôi* |
| `demo.mkt.head@mcvn.local` | **Head + C-Level Approver + Brand Reviewer** (kiêm 3 vai) | *Đang chờ tôi duyệt* + Approvals + Banner approve |
| `demo.si@mcvn.local` | S&I Evaluator | *Đang chờ tôi đánh giá* |
| `demo.ops@mcvn.local` | OPS Evaluator | *Đang chờ tôi đánh giá* |
| `demo.finance@mcvn.local` | Finance Evaluator | *Đang chờ tôi đánh giá* |
| `demo.sc@mcvn.local` | SC Evaluator | *Đang chờ tôi đánh giá* |
| `demo.legal@mcvn.local` | Legal Evaluator | *Đang chờ tôi đánh giá* |
| `demo.rsg.head@mcvn.local` | PIF Approver (M08) | Approvals → *PIF* |
| `demo.{si,ops,finance,sc,legal}.head@mcvn.local` | Heads | *Đang chờ tôi duyệt* |
| `demo.{rsg,it,menu,digital}@mcvn.local` | nhân viên M08 | Approvals (PIF flow) |

> **Mẹo nhanh:** vào `Settings → Users` → click user → **Log in as** để
> giả lập, không cần logout.

---

## 3. Bảng tra cứu 11 PAF demo (static records)

Tìm theo Name trong list view *PAF của tôi*. List view có cột badge
**Promotion Type** + tổng `total_promotion_value`.

| Name | State | Promotion Type | Cơ cấu / Kênh | Banner | Xem được gì |
|---|---|---|---|---|---|
| `PAF-DEMO-DRAFT` | 🟦 Nháp | (chưa set) | Chưa điền | 1 (draft) | Form trống, nút **Gửi đánh giá** + tab Pháp lý KM còn rỗng |
| `PAF-DEMO-EVAL` | 🟨 Đánh giá | `gift_attached` | 2.500 quà × 20K, FC/SOK/Digital | 3 (2 approved + 1 rejected) | 5 eval line (3 done + 1 in_review + 1 pending) |
| `PAF-DEMO-HEAD` | 🟧 Chờ Heads | `discount_direct` | Giảm 20%, tất cả kênh, allow_extended | — | 3 eval line (template Core) |
| `PAF-DEMO-CLEVEL` | 🟧 Chờ C-Level | `gift_attached` | 2.100 quà × 20K, FC/SOK | — | — |
| `PAF-DEMO-APPROVED` | 🟩 Đã duyệt | `discount_direct` | Giảm 20%, tất cả kênh | — | Chưa trigger PIF (`pif_object_id` rỗng) |
| `PAF-DEMO-PIF` | 🟪 PIF chạy | `gift_attached` | 5.000 quà × 15K, FC/SOK/Digital | — | Link sang `demo_pif_003` (McChicken Crispy) |
| `PAF-DEMO-VAL` | 🟫 Valuation | `discount_direct` | Giảm 20%, FC/SOK/Digital | — | Report draft (revenue 240M / cost 170M) |
| `PAF-DEMO-DONE` | ✅ Done | `gift_attached` | 3.000 quà × 20K, FC/SOK | 4 (all approved) | Report published + 4 banner final |
| `PAF-DEMO-REJ` | ❌ Rejected | — | — | — | Legal `failed` với comment lý do |
| `PAF-DEMO-CANCEL` | ⛔ Cancelled | — | — | — | MKT tự hủy |
| **`PAF-DEMO-E2E`** | ✅ **Done** | `gift_attached` | hook chạy | 4 (sync sang PIF) | **Case xuyên suốt** — xem mục 5 |

---

## 4. Demo theo từng vai trò

### 4.1 MKT (PAF Creator) — `demo.mkt`

1. Đăng nhập `demo.mkt@mcvn.local / 1`.
2. PAF → *PAF của tôi* → **NEW**.
3. Chọn template (4 lựa chọn, xem mục 6) → onchange tự fill
   `promotion_type`, `eligible_channel_ids`, `max_uses_per_customer`,
   `time_window_*`, `description_html`.
4. Điền `planned_start_date`, `planned_end_date` (≤ 90 ngày trừ khi tick
   `allow_extended_duration`).
5. Sang tab **Pháp lý KM** → chọn `promotion_type`, điền
   `total_promotion_value` cho khai báo Sở Công Thương. Nếu chọn
   `lucky_draw`, field `regulatory_filing_code` bắt buộc.
6. Sang tab **Cơ cấu giải thưởng** → điền chi tiết quà / giảm giá theo
   `promotion_type`.
7. Sang tab **Hình ảnh / Banner** → upload PNG banner cho từng kênh (xem mục 4.7).
8. Bấm **Gửi đánh giá** → tạo các eval line theo template.

> Nếu PAF chưa có banner `brand_approved` → tùy cấu hình
> `require_banner_before_submit`, nút Submit có thể chặn.

### 4.2 S&I / OPS / Finance / SC / Legal Evaluator

1. Đăng nhập user phòng tương ứng (ví dụ `demo.si@mcvn.local / 1`).
2. PAF → *Đang chờ tôi đánh giá*.
3. Mở PAF, tab **Đánh giá các phòng ban** → mở line của phòng mình.
4. Bấm **Start Review** (status `pending → in_review`).
5. Điền field bắt buộc theo phòng:

| Phòng | Field bắt buộc |
|---|---|
| S&I | `forecast_demand > 0`, `0 ≤ confidence_score ≤ 1` |
| OPS | `pilot_capacity_score` ∈ {low, medium, high} |
| Finance | `roi_estimated_percent`, `gross_margin_estimated` |
| SC | `supply_risk_level`, `lead_time_days ≥ 0`, `food_safety_check_status` |
| Legal | `regulatory_sla_days`, `legal_filing_type`, `legal_50_percent_check` (tick true khi `gift_total_value > 0`) |

6. Bấm **Submit Done**. Line cuối Done → auto trigger
   `_notify_all_evaluations_complete` → PAF sang `head_approval`.

### 4.3 Vai trò từ chối — minh họa qua `PAF-DEMO-REJ`

1. `admin` → mở `PAF-DEMO-REJ` → tab Eval Lines.
2. Line Legal status `failed`, đọc `comment_html` thấy lý do từ chối.
3. PAF state `rejected` toàn phiếu — xem
   `mkt_paf_evaluation_line.action_submit_failed()`.

### 4.4 Heads + C-Level — `demo.mkt.head`

1. `demo.mkt.head@mcvn.local / 1` (kiêm 3 vai: Head + C-Level + Brand Reviewer).
2. *Đang chờ tôi duyệt* → mở PAF → smart link `head_approval_request_id`.
3. Bấm **Approve** trên approval.request → M09 override auto gọi
   `paf.action_request_clevel()` → state `clevel_approval`.
4. Mở `clevel_approval_request_id` → Approve → PAF `approved` →
   `_run_pif_workflow()` → state `pif_running` + tạo approval.request PIF.

### 4.5 RSG duyệt PIF — `demo.rsg.head`

1. `demo.rsg.head@mcvn.local / 1`.
2. Approvals → category **Product Initiation Form (PIF)** → mở
   approval.request có link `x_psm_mkt_paf_request_id` = PAF mới.
3. Bấm **Approve** → M08 tạo `x_psm_pif_object` → override M09
   set `paf.pif_object_id`.
4. Quay lại PAF → smart link "Đối tượng PIF" mở được sang PIF.
   **Phase 3 bonus**: 4 filename `x_psm_img_*` trên PIF được auto-sync
   từ banner của PAF.

### 4.6 S&I publish Valuation

1. `demo.si@mcvn.local / 1` hoặc admin.
2. Mở PAF state `pif_running` → bấm **Mở Valuation** → tạo report draft
   → PAF state `valuation`.
3. Điền `actual_revenue`, `actual_cost`, `summary_html` → bấm **Publish**
   → PAF `done`.

### 4.7 ➕ Brand Reviewer — duyệt banner (Phase 3)

1. `demo.mkt.head@mcvn.local / 1` (cũng là Brand Reviewer).
2. Mở PAF có banner `draft` (ví dụ `PAF-DEMO-DRAFT`).
3. Tab **Hình ảnh / Banner** → kanban gallery hiển thị thumbnail.
4. Mở banner status `draft` → bấm **Brand Approve** → status
   `brand_approved`, set `approver_id` + `approval_date`.
5. Hoặc bấm **Brand Reject** → wizard nhập `rejection_reason` → status
   `rejected`.
6. MKT muốn sửa banner bị reject → bấm **Reset to Draft** → status về
   `draft`, MKT chỉnh ảnh xong lại submit.

> Workflow 1-cấp: bỏ qua bước MKT submit trung gian. Brand approve
> trực tiếp từ `draft`.

#### Smart button đếm banner approved

Đầu form PAF có nút **Banner OK: N** — `banner_approved_count` realtime
đếm số banner đã `brand_approved`. Click vào mở list view banner của PAF.

---

## 5. Case end-to-end — `PAF-DEMO-E2E`

Case duy nhất đi trọn 12 bước nghiệp vụ, đã có đủ Phase 1+2+3 data.

### 5.1 Dữ liệu đã có

Đăng nhập `admin`, mở `PAF-DEMO-E2E`:

| Field | Giá trị | Phase |
|---|---|---|
| `state` | `done` | — |
| `template_id` | LTO Promotion 5 phòng | — |
| `product_ids` | BBQ Chicken Burger (có `food_safety_declaration_state='done'`) | Phase 2 |
| `creator_id` | demo_user_mkt | — |
| `planned_start_date / end_date` | 2026-08-15 → 2026-10-31 (~77 ngày, dưới 90) | Phase 1 |
| `forecast_revenue` | 420M VND | — |
| `promotion_type` | `gift_attached` | Phase 1 |
| `promotion_legal_form` | `notification` | Phase 1 |
| `total_promotion_value` | ≈ 75M VND | Phase 1 |
| `gift_quantity / unit_value / total_value` | 5.000 / 15K / 75M | Phase 2 |
| `eligible_channel_ids` | [FC, SOK, MOP] | Phase 2 |
| `max_uses_per_customer` | 2 | Phase 2 |
| `time_window_start / end` | 10.0 / 22.0 | Phase 2 |
| `banner_ids` | 4 banner đều `brand_approved` (POS / SOK / DT / MOP) | Phase 3 |
| `banner_approved_count` | 4 (smart button hiện "Banner OK: 4") | Phase 3 |
| `head_approval_request_id` | có | — |
| `clevel_approval_request_id` | có | — |
| `pif_object_id` | x_psm_pif_object state `lab_test`, có 4 filename `x_psm_img_*` đã sync | Phase 3 |
| Tab Valuation | report `published`, revenue 480M / cost 305M / ROI ~57% | — |

### 5.2 Smart link traversal

```
PAF-DEMO-E2E (state=done)
  ├─ tab Pháp lý KM         → promotion_type, total_promotion_value
  ├─ tab Cơ cấu giải thưởng → gift breakdown
  ├─ tab Hình ảnh / Banner  → 4 banner kanban thumbnail, all brand_approved
  ├─ tab Eval Lines         → 5 line done (S&I/OPS/Finance/SC/Legal)
  ├─ smart button Banner OK: 4
  ├─ smart link Head Approval     → approval.request (approved)
  ├─ smart link C-Level Approval  → approval.request (approved)
  ├─ smart link Đối tượng PIF     → x_psm_pif_object id=5
  │      └─ 4 field x_psm_img_*_filename đã được sync từ banner
  │      └─ 4 ir.attachment chứa file PNG gốc
  └─ tab Valuation         → report (published)
```

### 5.3 Verify SQL

```sql
-- toàn cảnh PAF-DEMO-E2E + Phase 1+2 fields
SELECT name, state, promotion_type, total_promotion_value,
       gift_quantity, gift_unit_value, max_uses_per_customer,
       head_approval_request_id, clevel_approval_request_id, pif_object_id
FROM mkt_paf_request
WHERE name = 'PAF-DEMO-E2E';

-- Banner đã sync sang PIF
SELECT id, state, x_psm_img_pos_filename, x_psm_img_sok_filename,
       x_psm_img_dmb_filename, x_psm_img_mop_filename
FROM x_psm_pif_object
WHERE id = (SELECT pif_object_id FROM mkt_paf_request WHERE name='PAF-DEMO-E2E');

-- 4 banner brand_approved của PAF-DEMO-E2E
SELECT name, purpose, status, target_dimensions
FROM mkt_paf_banner
WHERE paf_request_id = (SELECT id FROM mkt_paf_request WHERE name='PAF-DEMO-E2E')
ORDER BY purpose;
```

---

## 6. PAF Templates — 4 template demo (Phase 2)

PAF → **Templates**:

| Template | Code | promotion_type | Required Depts | Đặc trưng |
|---|---|---|---|---|
| LTO Promotion — Mẫu chuẩn 5 phòng ban | `PAF-TPL-LTO-01` | `gift_attached` | S&I, OPS, Finance, SC, Legal | Default: FC/SOK/Digital, 2 lần/khách, 10h–22h |
| Core Product Launch — Mẫu rút gọn 3 phòng ban | `PAF-TPL-CORE-01` | `discount_direct` | S&I, Finance, SC | Default: tất cả kênh, không giới hạn lần, 24/24 |
| Lucky Draw — Mẫu đăng ký Legal | `PAF-TPL-LUCKY-01` | `lucky_draw` | S&I, Finance, SC, Legal | `promotion_legal_form='registration'`, FC/Digital, 1 lần/khách |
| Holiday Gift — Mẫu mùa lễ | `PAF-TPL-HOLIDAY-01` | `gift_attached` | đủ 5 phòng | Cờ `allow_holiday_100` ngầm, 9h–23h |

Khi MKT tạo PAF mới, chọn template → onchange tự fill:
- `description_html` (từ `default_description_html` + `default_description_legal_html`)
- `product_ids` (từ `default_product_ids`)
- `promotion_type`, `promotion_legal_form`
- `eligible_channel_ids` (Many2many)
- `max_uses_per_customer`, `time_window_start/end`
- `food_safety_responsible_dept_id`

---

## 7. PIF tích hợp xem từ M08

5 PIF có trong DB:

| PIF | State | Origin | Link với PAF |
|---|---|---|---|
| `PIF-DEMO-001` Spicy McDouble | `rsg_create` | M08_P0801_demo | — |
| `PIF-DEMO-002` BBQ Chicken Burger | `lab_test` | M08_P0801_demo | — |
| `PIF-DEMO-003` McChicken Crispy | `completed` | M08_P0801_demo | `PAF-DEMO-PIF` |
| `PIF-DEMO-004` Spicy Strips Digital | `it_config` | M08_P0801_demo (fast-track) | — |
| (PIF id=5) | `lab_test` | M09_0901_demo hook | `PAF-DEMO-E2E` (có 4 filename `x_psm_img_*`) |

**Approvals → category Product Initiation Form (PIF):** thấy approval.request gốc của các PIF.

---

## 8. Cấu hình Approval Categories (hook auto-config)

PAF → **Cấu hình → Categories duyệt**:

| Category | Approval Minimum | Approver | Note |
|---|---|---|---|
| 0901 - PAF Head Review | 1 | `demo_user_mkt_head` | Hook hạ minimum từ 5 xuống 1 |
| 0901 - PAF C-Level | 1 | `demo_user_mkt_head` | — |
| Product Initiation Form (PIF) (M08) | 1 | `demo_user_rsg_head` | M08 category, được hook M09 demo configure |

> Production sẽ cấu hình thủ công qua UI. Hook chỉ patch khi
> `approver_ids` rỗng (idempotent).

---

## 9. Demo Phase 1 — Ràng buộc pháp lý 90 ngày + promotion_type

### 9.1 Verify constraint 90 ngày

1. `demo.mkt@mcvn.local / 1` → tạo PAF mới.
2. Điền `planned_start_date = 2026-08-01`, `planned_end_date = 2026-12-01` (122 ngày).
3. Bấm Save → raise `ValidationError`:
   > Theo Nghị định 81/2018/NĐ-CP, chương trình khuyến mãi giảm giá/tặng quà
   > không được kéo dài quá 90 ngày. Hiện tại: 122 ngày...
4. Tick `allow_extended_duration` → Save OK (escape hatch cho BoD-approved).

### 9.2 Verify Lucky Draw bắt buộc filing code

1. Tạo PAF mới, chọn template `Lucky Draw — Mẫu đăng ký Legal`.
2. Onchange tự set `promotion_type='lucky_draw'`, `promotion_legal_form='registration'`.
3. Sang state khác `draft` (bấm Gửi đánh giá) khi `regulatory_filing_code` rỗng → bị chặn.

### 9.3 Tham số cấu hình động

Settings → Technical → Parameters:

| Key | Default | Vai trò |
|---|---|---|
| `mkt_0901.max_duration_days` | 90 | Ngưỡng thời lượng khuyến mãi |
| `mkt_0901.gift_max_percent` | 50 | Quà tặng ≤ 50% giá trị hàng |
| `mkt_0901.lucky_draw_min_sla_days` | 30 | SLA Legal tối thiểu cho bốc thăm |
| `mkt_0901.banner_max_size_mb` | 4 | Max size 1 file banner |

> Legal có thể sửa khi luật thay đổi không cần dev.

---

## 10. Demo Phase 2 — Cơ cấu quà tặng + Thể lệ + ATTP

### 10.1 Verify 50% rule

1. PAF mới với `forecast_revenue=100M`, `promotion_type='gift_attached'`.
2. Điền `gift_quantity=1000`, `gift_unit_value=60K` → `gift_total_value=60M`.
3. Save → raise: giá trị quà 60M > 50% revenue 100M = 50M.
4. Giảm `gift_unit_value=40K` → `gift_total_value=40M` ≤ 50M → OK.
5. Nếu là mùa lễ, tick `allow_holiday_100` → cho phép quà tới 100% (escape hatch).

### 10.2 Verify ATTP trên product

Settings → Inventory → Products → mở `BBQ Chicken Burger`:

| Field ATTP | Giá trị (sau khi hook chạy E2E) |
|---|---|
| `food_safety_declaration_state` | `done` |
| `food_safety_declaration_no` | `12345/2026/ATTP-HCM` |
| `food_safety_declaration_date` | 2026-05-15 |

PAF có computed field tổng hợp summary từ product.

---

## 11. Demo Phase 3 — Banner / Hình ảnh sản phẩm

### 11.1 Upload banner mới (MKT)

1. `demo.mkt@mcvn.local / 1` → mở `PAF-DEMO-DRAFT` → tab **Hình ảnh / Banner**.
2. Bấm **Add** trên kanban view → upload PNG.
3. Điền `name`, `purpose` (Selection: `pos_display` / `sok_display` /
   `dt_menu` / `mop_app` / `social_fb` / `social_ig` / `printed` /
   `digital_web` / `other`).
4. Điền `language` (vi/en/multi), `target_dimensions` (vd `1920x1080`),
   `target_dpi`.
5. Save → state `draft`. Brand reviewer sẽ thấy trong queue.

### 11.2 Brand duyệt banner

1. `demo.mkt.head@mcvn.local / 1` (Brand Reviewer).
2. Mở banner draft → bấm **Brand Approve** → state `brand_approved`,
   ghi nhận `approver_id`, `approval_date`.
3. Hoặc bấm **Brand Reject** → wizard nhập `rejection_reason` → state
   `rejected`.

### 11.3 Kiểm tra 8 banner demo có sẵn

PAF → tab Hình ảnh / Banner:

| PAF | Số banner | Trạng thái |
|---|---|---|
| `PAF-DEMO-DRAFT` | 1 | 1 `draft` (BBQ POS Draft Banner) |
| `PAF-DEMO-EVAL` | 3 | 2 `brand_approved` (POS, SOK) + 1 `rejected` (DT, "Logo chưa đúng guideline") |
| `PAF-DEMO-DONE` | 4 | All `brand_approved` (POS, SOK, DT, MOP) |
| `PAF-DEMO-E2E` (hook tạo) | 4 | All `brand_approved`, sync sang PIF id=5 |

### 11.4 Sync banner sang PIF M08 (auto)

Khi PAF chuyển sang `pif_running` (B11), hook
`_sync_banners_to_pif()` chạy tự động:

- Lấy banner `brand_approved` theo từng `purpose`:
  - `pos_display` → `x_psm_img_pos_filename`
  - `sok_display` → `x_psm_img_sok_filename`
  - `dt_menu` → `x_psm_img_dmb_filename`
  - `mop_app` → `x_psm_img_mop_filename`
- Tạo `ir.attachment` link với x_psm_pif_object để user M08 download file thật.

Verify: mở PIF id=5 sau khi cài → 4 field filename có giá trị, 4 attachment.

---

## 12. Checkpoint phổ biến (Q&A)

| Câu hỏi | Trả lời |
|---|---|
| "PAF có bao nhiêu state?" | 10 — xem `mkt_paf_request.py:67-78` |
| "Cài 90 ngày từ đâu?" | `ir.config_parameter('mkt_0901.max_duration_days')` mặc định 90 |
| "PAF Marketing có fast-track PIF không?" | Không. Chỉ Digital/Supply Chain fast-track ở M08 |
| "Brand reject banner thì MKT làm gì?" | Bấm **Reset to Draft** → sửa ảnh → re-upload → submit lại |
| "Ngưỡng 50% quà tặng đổi được không?" | Có, sửa `ir.config_parameter('mkt_0901.gift_max_percent')` |
| "Lưu image ở đâu?" | Field `Image` trên `mkt_paf.banner` (DB binary, Odoo auto resize) |
| "Bypass constraint 90 ngày?" | Tick `allow_extended_duration` (cần admin/BoD-approved) |
| "Bypass 50%?" | Tick `allow_holiday_100` cho mùa lễ |
| "Sync banner sang PIF có manual override?" | Không trong phase này. Auto khi B11 trigger |
| "Reset hook E2E?" | `DELETE FROM mkt_paf_request WHERE name='PAF-DEMO-E2E'` → rerun |

---

## 13. Limitations của demo data

- **Eval line evaluator** = `__system__` trên PAF-DEMO-E2E (hook chạy
  bằng sudo). Production thực tế là user phòng ban.
- **Approval workflow** trong E2E được **bypass** bằng cách gọi trực
  tiếp `action_request_clevel()`, `action_mark_approved()`. Smart link
  Head/CLevel approval.request có status `new` không phải `approved`.
  Để demo approve thật, dùng `PAF-DEMO-HEAD` hoặc `PAF-DEMO-CLEVEL` và
  bấm Approve thủ công.
- **PIF object** trong E2E được tạo trực tiếp ở state `lab_test`, mô
  phỏng RSG đã duyệt. Để demo flow thật, dùng `PAF-DEMO-APPROVED`
  (chưa có pif_object) → bấm trigger PIF → approve qua approval.request.
- **`loyalty.program`** chưa có trong demo. Tất cả template để rỗng
  `default_loyalty_program_id`.
- **Banner image** dùng 4 PNG placeholder trong `static/img/`, kích
  thước chưa chính xác với `target_dimensions` (giả lập cho demo).

---

## 14. Cheat sheet thao tác nhanh

```
[Demo 3 phút - showcase]
1. Login admin → menu PAF → list view PAF của tôi.
2. Mở PAF-DEMO-E2E → quan sát đủ 5 tab (Nội dung, Pháp lý KM,
   Cơ cấu giải thưởng, Hình ảnh/Banner, Eval Lines).
3. Click smart link "Đối tượng PIF" → PIF id=5 với 4 filename sync.

[Demo 10 phút - constraint pháp lý]
1. Login demo.mkt → tạo PAF mới, chọn template Core.
2. Điền start=2026-08-01, end=2026-12-15 (> 90 ngày) → save → bị chặn.
3. Tick allow_extended_duration → save OK.
4. Sang tab Cơ cấu giải thưởng: forecast=100M, gift 60M → save → bị chặn
   bởi 50% rule. Giảm gift xuống 40M → OK.

[Demo 20 phút - flow MKT đầy đủ]
1. Login demo.mkt → tạo PAF mới, template LTO.
2. Upload 2 banner (POS, SOK), submit (state draft).
3. Switch demo.mkt.head (Brand Reviewer) → approve 2 banner.
4. Quay lại demo.mkt → bấm Gửi đánh giá.
5. Switch demo.si → đánh giá line S&I (start_review → fill → submit_done).
6. Lặp với Finance/SC/OPS/Legal (line cuối → auto trigger head_approval).
7. Switch demo.mkt.head → Approve head approval → Approve clevel.
8. Switch demo.rsg.head → Approve PIF approval → tạo x_psm_pif_object.
9. Verify PIF có 4 filename x_psm_img_* sync từ 2 banner POS/SOK + 2
   banner placeholder (purpose chưa upload → empty).
10. Switch demo.si → Mở Valuation → fill report → Publish → state done.

[Verify cuối]
SELECT name, state, promotion_type, total_promotion_value,
       banner_approved_count
FROM mkt_paf_request ORDER BY id;
```
