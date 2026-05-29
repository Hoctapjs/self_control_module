# Plan Triển Khai — Bổ Sung Ràng Buộc Pháp Lý VN cho PAF (M09_0901)

> **Mục tiêu:** Số hoá yêu cầu pháp lý của Nghị định 81/2018/NĐ-CP về xúc
> tiến thương mại vào model `mkt_paf.request` và `mkt_paf.template`, để hệ
> thống tự chặn lỗi pháp lý và hồ sơ Sở Công Thương được phê duyệt thuận
> lợi.
>
> **Phạm vi sửa:** chủ yếu `M09_0901` (production), `M09_0901_demo` chỉ
> cập nhật demo data theo schema mới.
>
> **Trạng thái:** ✅ ĐÃ DUYỆT (6/6 câu chốt) — sẵn sàng triển khai Phase 1.
>
> **Quyết định thiết kế (chốt 2026-05-28):**
> 1. Field design: **Structured** (Selection/Monetary/Integer + constraint)
> 2. Channel model: **Reuse `x_psm_pif_platform` của M08_P0801**
> 3. Ngưỡng 50%/90 ngày: **`ir.config_parameter`** (Legal tự sửa qua Settings)
> 4. Rollout: **3 phases** — Phase 1: 90 ngày + promotion_type + total_promotion_value; Phase 2: quà tặng + thể lệ + ATTP + template mở rộng; **Phase 3: Hình ảnh/Banner sản phẩm cho MKT** (bổ sung 2026-05-28)
> 5. ATTP: trên **`product.template`** (computed summary hiển thị trên PAF)
> 6. Migration: **Script `post-migrate.py`** set default `promotion_type='gift_attached'` + `allow_extended_duration=True` cho data cũ
>
> **Phase 3 — Quyết định bổ sung (chốt 2026-05-28):**
> 7. Banner workflow: **1 cấp** (Brand approve trực tiếp, không qua MKT submit)
> 8. Quyền duyệt banner: **Group mới `MKT_0901_brand_reviewer`** (tách khỏi PAF approver)
> 9. Sync banner sang PIF M08: **Tự động** trong `_run_pif_workflow` (B11)
> 10. Lưu image: **Field `Image`** (DB binary, Odoo auto resize thumbnail/medium/large)

---

## 1. Phân tích yêu cầu nghiệp vụ

Theo Nghị định 81/2018/NĐ-CP (Luật VN về xúc tiến thương mại):

| Quy định | Ràng buộc hệ thống |
|---|---|
| Khuyến mãi giảm giá/tặng quà không quá **90 ngày** | `planned_end_date ≤ planned_start_date + 90 ngày` |
| Phân loại hình thức khuyến mãi rõ ràng | Field `promotion_type` (Selection) bắt buộc |
| Bốc thăm trúng thưởng → cần **Đăng ký** (không phải Thông báo) | Khi `promotion_type = 'lucky_draw'` → trigger workflow Legal đăng ký |
| Giá trị quà tặng ≤ **50%** giá trị hàng (trừ lễ hội đặc biệt) | Constraint `gift_total_value ≤ 0.5 * product_value` |
| Tổng giá trị khuyến mãi phải khai báo cho Sở Công Thương | Field `total_promotion_value` (Monetary) bắt buộc |
| Thể lệ rõ ràng: kênh, số lượt/khách, điều kiện thời gian | Các field structured thay vì HTML free text |
| Cam kết chất lượng / hồ sơ tự công bố ATTP | Field `food_safety_declaration_state` |

---

## 2. Thay đổi Model `mkt_paf.request`

### 2.1 Group "Thông tin pháp lý khuyến mãi" — mới

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `promotion_type` | Selection | ✅ | `discount_direct` / `gift_attached` / `lucky_draw` |
| `promotion_legal_form` | Selection | ✅ | `notification` (Thông báo) / `registration` (Đăng ký — bắt buộc khi `lucky_draw`) |
| `regulatory_authority` | Char | — | Tên Sở Công Thương / cơ quan tiếp nhận |
| `regulatory_filing_code` | Char | — | Số văn bản chấp thuận (sau khi Legal đăng ký xong) |

**Computed:** `promotion_legal_form` mặc định `notification`, nhưng tự
chuyển `registration` khi `promotion_type = 'lucky_draw'` qua onchange.

### 2.2 Group "Cơ cấu giải thưởng" — mới

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `gift_quantity` | Integer | invisible khi `promotion_type='discount_direct'` | Dự kiến số lượng quà |
| `gift_unit_value` | Monetary | như trên | Giá trị 1 quà |
| `gift_total_value` | Monetary (computed) | — | `= gift_quantity * gift_unit_value` |
| `discount_percent` | Float | invisible khi `promotion_type='gift_attached'` | % giảm giá |
| `discount_total_estimate` | Monetary | — | Ước tính tổng giảm giá |
| `total_promotion_value` | Monetary (computed) | ✅ | `= gift_total_value + discount_total_estimate`, dùng cho khai báo Sở CT |

**Constraint pháp lý (`@api.constrains`):**
- `gift_total_value > 0` → check `gift_total_value ≤ 0.5 * (forecast_revenue / forecast_units)` (giá trị quà ≤ 50% giá trị hàng). Có flag `allow_holiday_100` để bỏ qua khi là mùa lễ.
- `total_promotion_value > 0` khi `state` chuyển ra khỏi `draft`.

### 2.3 Group "Thể lệ tham gia" — mới

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `eligible_channel_ids` | Many2many (`mkt_paf.channel` — model mới) | ✅ | Kênh áp dụng (POS / SOK / DT / MOP / Digital). Tận dụng `x_psm_pif_platform` của M08_P0801 thay vì tạo model mới |
| `max_uses_per_customer` | Integer | — | 0 = không giới hạn |
| `time_window_start` | Float (giờ trong ngày, 0–24) | — | VD: 10.0 = chỉ áp dụng sau 10h sáng |
| `time_window_end` | Float | — | — |
| `customer_eligibility_html` | Html | — | Điều kiện đặc biệt khác (membership tier, area, …) |

**Lưu ý reuse:** thay vì tạo model `mkt_paf.channel`, **kế thừa
`x_psm_pif_platform`** của M08_P0801 — đã có 6 platform sẵn (FC, SOK, DT,
WT, McCafe, Digital). Tiết kiệm và đồng bộ ngữ nghĩa với PIF.

### 2.4 Group "Cam kết chất lượng (ATTP)" — mới

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `food_safety_declaration_state` | Selection | ✅ khi product là new | `not_required` / `pending` / `done` / `expired` |
| `food_safety_declaration_no` | Char | — | Số văn bản tự công bố |
| `food_safety_declaration_date` | Date | — | Ngày tự công bố |
| `food_safety_responsible_dept_id` | Many2one (hr.department) | — | Mặc định = SC |
| `food_safety_notes` | Text | — | Ghi chú thêm |

**Onchange:** khi `product_ids` thay đổi và có sản phẩm là `new` (chưa có
WRIN từ M08), thì `food_safety_declaration_state` auto đặt `pending`.

### 2.5 Constraint pháp lý lớn — 90 ngày

```python
@api.constrains('planned_start_date', 'planned_end_date')
def _check_promotion_duration_90_days(self):
    for rec in self:
        if rec.planned_start_date and rec.planned_end_date:
            delta = (rec.planned_end_date - rec.planned_start_date).days
            if delta > 90:
                raise ValidationError(_(
                    "Theo Nghị định 81/2018/NĐ-CP, chương trình khuyến mãi "
                    "giảm giá/tặng quà không được kéo dài quá 90 ngày. "
                    "Hiện tại: %s ngày (Bắt đầu: %s, Kết thúc: %s).",
                    delta, rec.planned_start_date, rec.planned_end_date,
                ))
```

> Có thể nới bằng flag `allow_extended_duration` (do BoD approve) khi cần
> chạy chương trình loyalty dài hạn không phải khuyến mãi (ví dụ
> membership program). Mặc định `False`.

---

## 3. Thay đổi Model `mkt_paf.template`

Template phải mang được toàn bộ "khung mẫu" để khi MKT tạo PAF mới, các
field pháp lý auto-fill — không cần MKT nhớ luật.

### 3.1 Field mới trên template

Đa số field giống bên `mkt_paf.request`, dùng prefix `default_` để phân
biệt là giá trị mặc định khi tạo PAF từ template:

| Field template | Mặc định khi PAF mới |
|---|---|
| `default_promotion_type` | → `paf.promotion_type` |
| `default_promotion_legal_form` | → `paf.promotion_legal_form` |
| `default_max_uses_per_customer` | → `paf.max_uses_per_customer` |
| `default_eligible_channel_ids` (M2M) | → `paf.eligible_channel_ids` (copy ids) |
| `default_time_window_start/end` | → `paf.time_window_*` |
| `default_food_safety_responsible_dept_id` | → `paf.food_safety_responsible_dept_id` |
| `default_description_legal_html` (Html lớn) | → ghép vào `paf.description_html` |

### 3.2 Onchange `template_id` trên PAF — mở rộng

`mkt_paf_request._onchange_template_id` hiện tại chỉ copy
`description_html`, `loyalty_program_id`, `product_ids`. Mở rộng để copy
thêm 7 field mới ở trên.

---

## 4. Thay đổi View

### 4.1 Form `mkt_paf.request.form`

Thêm 4 tab mới vào notebook (xen giữa "Nội dung PAF" và "Đánh giá phòng
ban"):

```
notebook
├── Nội dung PAF              (giữ nguyên)
├── ➕ Pháp lý KM               ← mới (promotion_type, legal_form, regulatory_*)
├── ➕ Cơ cấu giải thưởng       ← mới (gift_*, discount_*, total_promotion_value)
├── ➕ Thể lệ tham gia          ← mới (channel, max_uses, time_window)
├── ➕ Cam kết ATTP             ← mới (food_safety_*)
├── Đánh giá các phòng ban    (giữ nguyên)
├── Liên kết phê duyệt & PIF  (giữ nguyên)
└── Valuation                 (giữ nguyên — nếu có)
```

**Conditional visibility (modifier `invisible`):**
- Tab "Cơ cấu giải thưởng" — hiển thị nội dung khác nhau theo
  `promotion_type` (Selection):
  - `discount_direct` → ẩn `gift_*`, hiện `discount_*`
  - `gift_attached` → ẩn `discount_*`, hiện `gift_*`
  - `lucky_draw` → hiện cả 2 + thêm thông tin giải thưởng

### 4.2 Form `mkt_paf.template.form`

Thêm 1 tab "Khung mẫu pháp lý" chứa các field `default_*`.

### 4.3 List view PAF

Thêm cột `promotion_type` (badge) và `total_promotion_value` để filter
nhanh.

### 4.4 Search view PAF

Thêm filter:
- "Khuyến mãi giảm giá / Tặng quà / Bốc thăm" (group by `promotion_type`)
- "Đang chờ Legal đăng ký" (`promotion_legal_form='registration'` +
  `regulatory_filing_code=False`)

---

## 5. Thay đổi luồng đánh giá (Evaluation Lines)

Hiện tại line Legal chỉ có `regulatory_sla_days`, `requires_government_approval`, `scheme_compliant`. Cần mở rộng:

| Field mới trên `mkt_paf.evaluation.line` | Phòng | Mục đích |
|---|---|---|
| `legal_filing_type` | Legal | `notification` / `registration` — phải khớp với PAF `promotion_legal_form` |
| `legal_50_percent_check` | Legal | Boolean — Legal xác nhận giá trị quà ≤ 50% |
| `food_safety_check_status` | SC | `not_required` / `verified` / `pending` |

**Validation `action_submit_done` cho line Legal:**
- Nếu `paf.promotion_type='lucky_draw'` → `regulatory_sla_days ≥ 30`
  (đăng ký bốc thăm cần tối thiểu 30 ngày).
- `legal_50_percent_check` phải tick true thì line mới `done` được khi
  `paf.gift_total_value > 0`.

---

## 6. Demo data update (`M09_0901_demo`)

### 6.1 Template demo — bổ sung 2 template nghiệp vụ thực

| Template | promotion_type | Đặc trưng |
|---|---|---|
| `demo_paf_template_lto` | `gift_attached` | Mua combo tặng nước ngọt, kênh POS/SOK/MOP |
| `demo_paf_template_core` | `discount_direct` | Giảm 20% combo, kênh đầy đủ |
| ➕ `demo_paf_template_lucky_draw` | `lucky_draw` | Bốc thăm xe SH, cần Legal đăng ký |
| ➕ `demo_paf_template_holiday` | `gift_attached` | Mùa Tết, được phép quà 100% giá trị |

### 6.2 Static PAF records — phủ thêm case mới

| PAF mới | promotion_type | Mục đích demo |
|---|---|---|
| `PAF-DEMO-DISCOUNT` | `discount_direct` | Giảm 20% — case đơn giản nhất |
| `PAF-DEMO-GIFT` | `gift_attached` | Tặng quà — validate ≤ 50% |
| `PAF-DEMO-LUCKY` | `lucky_draw` | Bốc thăm — chạy luồng Legal đăng ký |
| `PAF-DEMO-OVER-90` | (validation fail) | Chứng minh constraint 90 ngày — để dạng `draft` + ghi note |

### 6.3 Cập nhật `PAF-DEMO-E2E`

- Đặt `promotion_type = 'gift_attached'`
- `gift_quantity = 5000`, `gift_unit_value = 15000` (Coca M)
- `gift_total_value = 75M`, `total_promotion_value = 75M`
- `eligible_channel_ids` = [FC, SOK, MOP]
- `max_uses_per_customer = 2`
- `food_safety_declaration_state = 'done'`, số 12345/2026/ATTP-HCM
- `time_window_start = 10.0, end = 22.0`
- Eval Legal line: `regulatory_sla_days = 15`, `legal_50_percent_check = True`

---

## 7. Migration cho DB đã có data

Vì PAF static records demo đã tồn tại với schema cũ, cần **migration
file** trong `M09_0901/migrations/19.0.1.1.0/` để:

1. Set default `promotion_type = 'gift_attached'` cho tất cả PAF cũ
   (giả định an toàn nhất).
2. Set `eligible_channel_ids` = tất cả platform của M08.
3. KHÔNG enforce constraint 90 ngày trên data cũ (chạy script set
   `allow_extended_duration = True` cho record vi phạm).

---

## 8. File breakdown — danh sách thay đổi cụ thể

### M09_0901 (production)
- `models/mkt_paf_request.py` — thêm ~15 field + 3 constraint + 2 compute
- `models/mkt_paf_template.py` — thêm ~7 field `default_*`
- `models/mkt_paf_evaluation_line.py` — thêm 3 field Legal/SC + validation
- `views/mkt_paf_request_views.xml` — thêm 4 tab + cột list + filter search
- `views/mkt_paf_template_views.xml` — thêm tab "Khung mẫu pháp lý"
- `migrations/19.0.1.1.0/post-migrate.py` — migration
- `data/promotion_legal_data.xml` (mới) — ir.config_parameter cho ngưỡng (50%, 90 ngày, 30 ngày SLA bốc thăm)
- `__manifest__.py` — bump version `19.0.1.0.0` → `19.0.1.1.0`

### M09_0901_demo (chỉ demo)
- `data/04_paf_templates.xml` — bổ sung 2 template + thêm field default
- `data/05_paf_static_states.xml` — bổ sung 4 PAF + cập nhật 10 PAF cũ
- `hooks.py` — cập nhật `_build_and_run_e2e` set các field mới
- `HUONG_DAN_XEM_DEMO.md` — bổ sung mục 12 "Demo ràng buộc pháp lý"

---

## 9. Ước lượng effort

| Hạng mục | Effort (giờ) | Phụ thuộc |
|---|---|---|
| Model + constraint + compute | 3 | — |
| Template + onchange | 1 | model |
| View 4 tab + conditional | 3 | model |
| Migration script | 1 | model |
| Demo data update | 2 | model + view |
| Test syntax + upgrade + UI verify | 1 | tất cả trên |
| **Tổng** | **~11 giờ** | |

---

## 10. Câu hỏi cần duyệt trước khi triển khai

1. **Field structured vs HTML free text:** tôi đề xuất structured (selection/integer/monetary). Nếu bạn muốn linh hoạt hơn, có thể giữ `description_html` và chỉ thêm vài key field. → Câu hỏi: structured hay hybrid?

2. **Channel = `x_psm_pif_platform` (reuse M08) hay tạo `mkt_paf.channel` riêng?** Reuse có rủi ro phụ thuộc M08; tạo mới thì duplicate. Tôi nghiêng về reuse để đồng bộ.

3. **Ngưỡng 50% và 90 ngày**: hardcode hay đặt vào `ir.config_parameter` để Legal có thể tinh chỉnh? Tôi nghiêng về `ir.config_parameter` (linh hoạt hơn).

4. **Migration cho data cũ**: có chạy đè `promotion_type = 'gift_attached'` cho tất cả PAF cũ không? Hay để nullable và force điền lại?

5. **Field `food_safety_*`** đặt trên `mkt_paf.request` hay trên
   `product.template` (vì ATTP là thuộc tính sản phẩm)?
   - Đặt trên PAF: phù hợp với phiếu khuyến mãi cụ thể, không bị nhân bản.
   - Đặt trên product: chuẩn hóa hơn, dùng được cho cả PIF (M08).
   - Tôi nghiêng về **product.template** (compute helper trên PAF chỉ hiển thị summary).

6. **Triển khai 1 phát hay chia phase?** Tôi đề xuất chia 2 phase:
   - **Phase 1 (5 giờ):** constraint 90 ngày + `promotion_type` +
     `total_promotion_value` (3 field cốt lõi nhất). Đủ cho audit pháp
     lý cơ bản.
   - **Phase 2 (6 giờ):** Cơ cấu quà tặng + Thể lệ + ATTP + template
     mở rộng.

---

## 11. Định nghĩa "Done"

Sau khi triển khai xong:

- [ ] Tạo 1 PAF mới với `planned_end_date - planned_start_date = 91 ngày` → bị từ chối với thông báo nghị định 81.
- [ ] Tạo PAF `promotion_type='lucky_draw'` → field `regulatory_filing_code` xuất hiện và bắt buộc trước khi đẩy state ra khỏi `draft`.
- [ ] Tạo PAF `gift_total_value > 0.5 × product value` → constraint raise.
- [ ] Chọn template `demo_paf_template_lto` → các field default tự fill.
- [ ] 4 PAF demo mới (DISCOUNT/GIFT/LUCKY/OVER-90) hiển thị đầy đủ trong list.
- [ ] PAF-DEMO-E2E đi xuyên suốt vẫn pass (eval lines vẫn done).
- [ ] HUONG_DAN_XEM_DEMO.md được update với mục mới.

---

## 12. Phase 3 — Hình ảnh / Banner sản phẩm cho phòng MKT

> **Mục tiêu Phase 3:** Cho phòng MKT đính kèm hình ảnh/banner sản phẩm
> vào PAF, có cấu trúc theo kênh (POS / SOK / DT / MOP / Social media),
> có workflow duyệt nội bộ MKT → Brand, và tự đồng bộ sang Marketing
> Images của PIF M08 khi PAF trigger PIF (B11).
>
> **Vì sao:** Hồ sơ Sở Công Thương yêu cầu hình ảnh chính thức của
> chương trình. Bộ phận thiết kế cần biết kích thước/định dạng theo
> từng kênh. PIF M08 đã có 4 field filename cho POS/SOK/DMB/MOP nhưng
> không có cơ chế upload thật — Phase 3 sẽ làm thật chỗ đó.

### 12.1 Model mới: `mkt_paf.banner`

One2many từ `mkt_paf.request.banner_ids`. Mỗi PAF có nhiều banner.

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `paf_request_id` | Many2one(mkt_paf.request) | ✅ | parent, `ondelete='cascade'` |
| `sequence` | Integer | — | handle widget để kéo thả |
| `name` | Char | ✅ | Tên banner (VD: "Banner POS A4 — Tiếng Việt") |
| `image` | Image | ✅ | Ảnh thực (max 4MB sau resize) |
| `image_filename` | Char | — | tên file gốc khi upload |
| `purpose` | Selection | ✅ | `pos_display` / `sok_display` / `dt_menu` / `mop_app` / `social_fb` / `social_ig` / `printed` / `digital_web` / `other` |
| `platform_id` | Many2one(x_psm_pif_platform) | — | reuse M08 platform để link sang PIF |
| `language` | Selection | ✅ | `vi` / `en` / `multi` |
| `target_dimensions` | Char | — | "1920x1080", "1080x1920" (Story), v.v. |
| `target_dpi` | Integer | — | 72 (web) / 300 (print) |
| `actual_dimensions` | Char (computed) | — | đọc width/height từ image binary |
| `file_size_kb` | Float (computed) | — | từ image binary |
| `status` | Selection | ✅ | `draft` / `mkt_approved` / `brand_approved` / `rejected` |
| `approver_id` | Many2one(res.users) | — | người duyệt cuối |
| `approval_date` | Datetime | — | |
| `rejection_reason` | Text | — | required khi `status='rejected'` |
| `notes` | Text | — | ghi chú thiết kế |

**Constraint:**
- File size ≤ `ir.config_parameter('mkt_0901.banner_max_size_mb', default=4)`
- `target_dimensions` regex `^\d+x\d+$`
- `status='brand_approved'` → bắt buộc có `approver_id`

### 12.2 Field trên `mkt_paf.request`

| Field | Type | Mô tả |
|---|---|---|
| `banner_ids` | One2many(mkt_paf.banner) | tab "Hình ảnh / Banner" |
| `banner_count` | Integer (computed) | smart button count |
| `banner_approved_count` | Integer (computed) | count `status='brand_approved'` |
| `banner_completeness` | Float (computed) | % banner đã approved trên tổng số |
| `require_banner_before_submit` | Boolean | mặc định True; admin có thể tắt cho PAF nhỏ |

**Gating:** ở `action_submit_to_evaluation` thêm check:

```python
if rec.require_banner_before_submit and rec.banner_approved_count == 0:
    raise ValidationError(_(
        "PAF chưa có banner nào được Brand duyệt. "
        "Phòng MKT phải upload + duyệt ít nhất 1 banner trước khi submit."
    ))
```

### 12.3 Tích hợp với PIF M08

M08_P0801 đã có 4 field char trên `x_psm_pif_object`:
- `x_psm_img_pos_filename`
- `x_psm_img_sok_filename`
- `x_psm_img_dmb_filename` (digital menu board / DT)
- `x_psm_img_mop_filename`

Khi PAF trigger PIF tại B11 (`_run_pif_workflow`), hook sẽ:

1. Lấy banner đã `brand_approved` cho từng `purpose` (pos_display →
   pos_filename, sok_display → sok_filename, dt_menu → dmb_filename,
   mop_app → mop_filename).
2. Set 4 filename trên PIF object.
3. Đính kèm image binary qua `ir.attachment` link với PIF object (để
   user M08 mở được file).

Logic này nằm trong `mkt_paf_request._sync_banners_to_pif(pif_object)`,
gọi từ `pif_object.py.create()` override (đã có sẵn từ Phase ban đầu).

### 12.4 View — Tab "Hình ảnh / Banner"

Thêm vào notebook của form PAF, sau tab "Cam kết ATTP" (Phase 2):

```xml
<page string="Hình ảnh / Banner" name="banners">
    <field name="banner_ids" mode="kanban,list,form">
        <kanban>
            <field name="image"/>
            <field name="name"/>
            <field name="purpose"/>
            <field name="status"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click">
                        <img t-att-src="kanban_image('mkt_paf.banner','image',record.id.raw_value)"
                             class="o_image_64_cover"/>
                        <strong><field name="name"/></strong>
                        <span class="badge"><field name="purpose"/></span>
                        <span><field name="status" widget="badge"/></span>
                    </div>
                </t>
            </templates>
        </kanban>
        <list>
            <field name="sequence" widget="handle"/>
            <field name="image" widget="image" options="{'size': [60, 60]}"/>
            <field name="name"/>
            <field name="purpose"/>
            <field name="language"/>
            <field name="target_dimensions"/>
            <field name="file_size_kb"/>
            <field name="status" widget="badge"
                   decoration-success="status == 'brand_approved'"
                   decoration-warning="status == 'mkt_approved'"
                   decoration-danger="status == 'rejected'"/>
        </list>
        <form>
            <!-- chi tiết banner, preview ảnh lớn, nút approve/reject -->
        </form>
    </field>
</page>
```

Smart button đầu form:
```xml
<button class="oe_stat_button" icon="fa-image">
    <field name="banner_approved_count" widget="statinfo" string="Banner OK"/>
</button>
```

### 12.5 Workflow duyệt banner (1 cấp — chốt)

State machine `mkt_paf.banner` đơn giản 3-state:

```
draft  ──[Brand approve]──>  brand_approved
  │
  ├──[Brand reject]──>  rejected ──[MKT reset]──>  draft
  │
  └──[xóa]──> (deleted, khi state=draft)
```

Bỏ bước `mkt_approved` trung gian. MKT upload xong, Brand reviewer
duyệt thẳng. Selection chỉ còn 3 giá trị: `draft` / `brand_approved`
/ `rejected`.

Action methods:
- `action_brand_approve` — `draft` → `brand_approved` (set `approver_id`,
  `approval_date`)
- `action_brand_reject` — `draft` → `rejected` (mở wizard nhập
  `rejection_reason`)
- `action_reset_draft` — `rejected` → `draft` (MKT sửa và resubmit)

Quyền (chốt — group mới):
- MKT (`MKT_0901_creator`): create, edit khi `status='draft'`, xóa khi
  `draft`.
- Brand (`MKT_0901_brand_reviewer` — **tạo mới**): approve/reject.
- Admin: full.

### 12.6 Demo data — Phase 3

- `M09_0901_demo/static/img/` (mới) — 4 file PNG placeholder:
  - `banner_bbq_pos_vi.png` (1200x800)
  - `banner_bbq_sok_vi.png` (1080x1920 vertical)
  - `banner_bbq_dt_vi.png` (1920x1080)
  - `banner_spicy_pos_vi.png`
- `M09_0901_demo/data/07_paf_banners.xml` (mới):
  - PAF-DEMO-DRAFT: 1 banner state `draft` (MKT mới upload)
  - PAF-DEMO-EVAL: 3 banner — 2 `brand_approved` + 1 `mkt_approved`
  - PAF-DEMO-DONE: 4 banner đầy đủ `brand_approved` (POS/SOK/DT/MOP)
  - PAF-DEMO-E2E: 4 banner đầy đủ (hook tự copy sang PIF id=5)
- Cập nhật `M09_0901_demo/hooks.py`:
  - Trong `_build_and_run_e2e` thêm step tạo 4 banner cho PAF-DEMO-E2E
  - Sau khi trigger PIF (B11), gọi `paf._sync_banners_to_pif(pif)` để
    test sync filename + attachment

### 12.7 Demo: Phòng MKT thao tác trên UI

Cập nhật `HUONG_DAN_XEM_DEMO.md`:

1. Login `demo.mkt@mcvn.local / 1`.
2. Mở PAF-DEMO-DRAFT → tab "Hình ảnh / Banner" → bấm **Upload** → chọn
   `banner_bbq_pos_vi.png` → điền `purpose=pos_display`, `language=vi`,
   `target_dimensions=1200x800`.
3. Bấm **Submit to Brand** → state banner sang `mkt_approved`.
4. Switch sang user `demo.brand@mcvn.local` (group `MKT_0901_brand_reviewer`).
5. Mở banner đó → bấm **Brand Approve** → state `brand_approved`.
6. Quay lại PAF → smart button "Banner OK: 1" hiện.

### 12.8 File breakdown — Phase 3

**M09_0901 (production):**
- `models/mkt_paf_banner.py` (mới) — model + state machine
- `models/mkt_paf_request.py` — thêm `banner_ids`, `_sync_banners_to_pif`, gating ở `action_submit_to_evaluation`
- `models/pif_object.py` — override `create()` thêm sync banner sau khi link PAF
- `views/mkt_paf_banner_views.xml` (mới) — form/list/kanban
- `views/mkt_paf_request_views.xml` — thêm tab "Hình ảnh / Banner" + smart button
- `security/res_groups.xml` — thêm group `MKT_0901_brand_reviewer`
- `security/ir.model.access.csv` — quyền cho `mkt_paf.banner`
- `data/banner_config_data.xml` (mới) — `ir.config_parameter` cho `banner_max_size_mb`
- `__manifest__.py` — bump `19.0.1.1.0` → `19.0.1.2.0`

**M09_0901_demo:**
- `static/img/` (mới) — 4 PNG placeholder
- `data/07_paf_banners.xml` (mới)
- `data/06_grant_paf_groups.xml` — thêm gán group brand_reviewer cho
  `demo_user_mkt_head`
- `hooks.py` — thêm step tạo banner + sync sang PIF
- `HUONG_DAN_XEM_DEMO.md` — thêm mục 4.7 "Phòng MKT đính kèm banner"

### 12.9 Ước lượng effort Phase 3

| Hạng mục | Effort (giờ) |
|---|---|
| Model `mkt_paf.banner` + state machine + constraint | 2 |
| View kanban + list + form + smart button | 2 |
| Tích hợp `_sync_banners_to_pif` với M08 | 1 |
| Demo data + 4 PNG placeholder | 1 |
| Update hooks + HUONG_DAN_XEM_DEMO.md | 1 |
| Test syntax + upgrade + UI verify | 1 |
| **Tổng Phase 3** | **~8 giờ** |

### 12.10 Định nghĩa "Done" — Phase 3

- [ ] MKT upload 1 PNG vào tab Banner của PAF mới → record `mkt_paf.banner`
      được tạo, image binary lưu vào DB, kanban hiển thị thumbnail.
- [ ] Bấm **Submit to Brand** → state `draft → mkt_approved`.
- [ ] User group Brand bấm **Brand Approve** → state `brand_approved` +
      `approver_id` + `approval_date` được set.
- [ ] PAF state=`draft`, chưa có banner `brand_approved` → bấm Submit
      to Evaluation → bị ValidationError chặn (gating).
- [ ] PAF-DEMO-E2E sau khi hook chạy → có 4 banner `brand_approved`,
      PIF id=5 có 4 filename trong field `x_psm_img_*` + 4 attachment.
- [ ] Upload file > 4MB → bị raise file_size constraint.
- [ ] Hard reload trình duyệt sau upgrade → kanban banner hiển thị
      ảnh, không bị 3 bảng raw.

### 12.11 Câu hỏi cần duyệt cho Phase 3 — ✅ ĐÃ CHỐT

1. ✅ Workflow duyệt: **1 cấp** (Brand approve trực tiếp). State chỉ
   còn `draft / brand_approved / rejected`.
2. ✅ Quyền: **Tạo group mới `MKT_0901_brand_reviewer`**.
3. ✅ Sync sang PIF: **Tự động** trong `_run_pif_workflow` (B11).
4. ✅ Lưu image: **Field `Image`** (DB binary).

