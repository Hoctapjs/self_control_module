# Technical Blueprint V1 — Portal UI Redesign cho Form Yêu Cầu Nghỉ Việc (M02_P0213)

> **Phạm vi**: Cải thiện UI/UX cho Portal form yêu cầu nghỉ việc (`portal_psm_resignation_request`) của module `M02_P0213_LEAVE_MANAGEMENT`, áp dụng palette McDonald's, design system từ module 0215 V1/V2/V3.
> **Loại**: Blueprint/Planning. Không sửa code, không tạo file mới, không apply patch.
> **Ngày**: 2026-05-13
> **Baseline**: Module 0213 hiện có template `resignation_portal_template.xml` với form nhân viên tạo đơn xin nghỉ việc.

---

## 1. Phân Tích Hiện Trạng

### 1.1. Vấn Đề UI/UX Từ Screenshot

| # | Vấn đề | Mô tả | Mức độ |
|---|---|---|---|
| **P1** | **Heading multiple levels không rõ ràng** | "Gửi yêu cầu nghỉ việc" + "CÔNG HÒA..." + "ĐỀ LÀP..." + "ĐƠN XIN..." — 4 line heading khác nhau, không hierarchy rõ. | 🔴 Cao |
| **P2** | **Input field readonly dùng bg-light thay form-control style** | Form-control readonly không có border rõ, chỉ bg-light muted — khó phân biệt với background page. | 🔴 Cao |
| **P3** | **Không có progress indicator/section nav** | Form dài 3 section (info + ngày nghỉ + xác nhận), user không biết đang ở đâu. | 🟡 Trung |
| **P4** | **Warning box nền đỏ sáng, contrast yếu** | "BUỘC PHẢI NHÂN CỬ CUỐI" box — nền đỏ-sáng (có thể là #FCEAE7), chữ đỏ đậm trên đỏ nhạt, khó đọc. | 🔴 Cao |
| **P5** | **Icon size không đồng bộ** | Icon "người" "đỏ" ở heading, icon "tag" vàng ở section → không unified. | 🟡 Trung |
| **P6** | **Không có visual feedback khi hover button** | 2 button cuối ("Gửi yêu cầu" + "Quay lại") nằm sát nhau, gap chặt. | 🟡 Trung |
| **P7** | **Divider giữa header content** | HR line ở giữa text CỘNG HÒA... — style cổ điển, không hợp brand. | 🟢 Thấp |
| **P8** | **Palette không theo McDonald's** | Hiện dùng Bootstrap default colors (danger đỏ, primary xanh, light gray) — không vàng `#FFC72C`, đỏ `#DA291C` bắt buộc. | 🔴 Cao |
| **P9** | **Label text muted quá nhẹ** | Field label "(Nhân viên)" nhỏ muted gray — khó đọc trên white background. | 🟡 Trung |
| **P10** | **Số thứ tự section 1-4 trong warning box không style** | Numbered list 1-4 có text dài, không background highlight hay visual distinction. | 🟡 Trung |

### 1.2. Vấn Đề Logic & Controller

| # | Vấn đề | Mô tả |
|---|---|---|
| **L1** | Form action `/my/resignation/submit` — cần confirm route | Xác nhận controller có route này, không phá khi sửa UI. |
| **L2** | CSRF token trong form — GIỮ NGUYÊN | Không được bỏ token. |
| **L3** | Read-only field — không được đổi thành editable | Field employee info là display-only. |

### 1.3. Đối Chiếu Với V1/V2/V3 Plan Của Module 0215

| Yếu tố | 0215 V1-V3 | 0213 Hiện tại | Cần cải |
|---|---|---|---|
| **Palette** | 4 màu: vàng #FFC72C, đỏ #DA291C, đen #000000, trắng #FFFFFF | Dùng Bootstrap, không đúng palette | Cần áp dụng bắt buộc |
| **Section layout** | 5 section với numbered circle + title + underline | 3 section (info, date, confirm) — heading ở `<h5 class="text-primary">` | Cần section index circle + underline |
| **Progress nav** | Sticky top với 5-dot nav (click → smooth scroll) | Không có | Cần thêm 3-dot nav |
| **Button style** | Primary (vàng) + danger (đỏ) + secondary (trắng viền) | Bootstrap btn-primary, btn-secondary (blue) | Cần đổi class |
| **Alert/warning** | Alert box background tint đúng, text contrast 4.5:1 AA | Warning box nền đỏ sáng, contrast yếu | Cần refactor |
| **Form control** | Input border-warning → class `psm-form-control` | `form-control bg-light readonly` | Cần style bao | spacing |

---

## 2. Giải Pháp Tổng Quát

### 2.1. Scope & Constraint

- **KHÔNG** thay đổi form action `/my/resignation/submit`.
- **KHÔNG** thay đổi field `name`, `readonly`, `enctype`.
- **KHÔNG** thay đổi CSRF token.
- **KHÔNG** sửa controller/model.
- **CHỈ** sửa template XML + thêm SCSS (hoặc inline `<style>`).
- **ÁÙNG** asset manifest nếu cần (check xem manifest 0213 có `assets` key chưa).

### 2.2. Design System Áp Dụng

Dùng **nguyên lý từ V2 plan của 0215**:
- **Palette**: Dùng 4 màu chính + token ramp (yellow-50→700, red-50→700, gray-50→900, cream-50).
- **Spacing**: 4/8/12/16/24/32px scale.
- **Typography**: 9 cấp với weight + letter-spacing.
- **Components**: Section index circle, status badge, buttons, alerts theo spec V2.

### 2.3. Wrapper Class

Thêm wrapper class mới cho module 0213:
- `.o_psm_0213_portal` (replace hiện tại `.psm-ops-resignation-portal`)

Mục đích: scope CSS, tránh conflict với module 0215 (`.o_psm_0215_portal`) và module khác.

---

## 3. UI/UX Redesign Chi Tiết

### 3.1. Header Banner (P1, P7, P8)

**Trước**:
```
Gửi yêu cầu nghỉ việc
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
---
Độc lập - Tự do - Hạnh phúc
ĐƠN XIN NGHỈ VIỆC
```

**Sau** — Banner vàng McDonald's:
```
┌────────────────────────────────┐
│ ┼ GỬI YÊU CẦU NGHỈ VIỆC     │ (yellow bg, uppercase, centered)
│ CỘNG HÒA XÃ HỘI CHỦ NGHĨA...  │ (normal, smaller, gray)
│ Độc lập - Tự do - Hạnh phúc   │ (normal, smallest, gray)
│ ĐƠN XIN NGHỈ VIỆC             │ (bold, larger, black)
└────────────────────────────────┘
```

**SCSS**:
```scss
.o_psm_0213_portal .psm-form-header {
    background: var(--psm-0213-yellow-500); /* #FFC72C */
    color: var(--psm-0213-black);
    padding: var(--psm-0213-space-5) var(--psm-0213-space-4);
    border-radius: var(--psm-0213-radius-lg) var(--psm-0213-radius-lg) 0 0;
    text-align: center;
}

.o_psm_0213_portal .psm-form-header__title {
    font-size: var(--psm-0213-fs-xl);
    font-weight: var(--psm-0213-fw-black);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: var(--psm-0213-space-2);
}

.o_psm_0213_portal .psm-form-header__seal {
    font-size: var(--psm-0213-fs-md);
    font-weight: var(--psm-0213-fw-semibold);
    color: var(--psm-0213-gray-700);
    margin-bottom: var(--psm-0213-space-1);
}

.o_psm_0213_portal .psm-form-header__tagline {
    font-size: var(--psm-0213-fs-sm);
    color: var(--psm-0213-text-muted);
    margin-bottom: var(--psm-0213-space-3);
}

.o_psm_0213_portal .psm-form-header__divider {
    border: 0;
    border-top: 2px solid var(--psm-0213-black);
    margin: var(--psm-0213-space-2) auto;
    width: 60%;
}

.o_psm_0213_portal .psm-form-header__subtitle {
    font-size: var(--psm-0213-fs-lg);
    font-weight: var(--psm-0213-fw-bold);
    color: var(--psm-0213-text-strong);
    margin: var(--psm-0213-space-3) 0 0 0;
}
```

### 3.2. Section Layout (P3, P5, P10)

Mỗi section có:
- Index circle vàng (1, 2, 3)
- Title với left-border vàng
- Fields grouped

**HTML qWeb pattern**:
```xml
<section class="psm-form-section" id="psm-section-1">
    <div class="psm-section__head">
        <span class="psm-section__index">1</span>
        <h5 class="psm-section__title">Thông tin nhân viên</h5>
    </div>
    <!-- content -->
</section>
```

**SCSS** (từ V2):
```scss
.o_psm_0213_portal .psm-form-section {
    border: 1px solid var(--psm-0213-border);
    border-radius: var(--psm-0213-radius-md);
    margin-bottom: var(--psm-0213-space-5);
    padding: var(--psm-0213-space-5);
}

.o_psm_0213_portal .psm-section__head {
    align-items: center;
    display: flex;
    gap: var(--psm-0213-space-3);
    margin-bottom: var(--psm-0213-space-4);
}

.o_psm_0213_portal .psm-section__index {
    align-items: center;
    background: var(--psm-0213-yellow-500);
    border-radius: 50%;
    color: var(--psm-0213-text-strong);
    display: inline-flex;
    flex: 0 0 2.25rem;
    font-weight: var(--psm-0213-fw-black);
    height: 2.25rem;
    justify-content: center;
    width: 2.25rem;
    font-size: var(--psm-0213-fs-base);
}

.o_psm_0213_portal .psm-section__title {
    border-left: 4px solid var(--psm-0213-yellow-500);
    color: var(--psm-0213-text-strong);
    font-weight: var(--psm-0213-fw-bold);
    margin: 0;
    padding-left: var(--psm-0213-space-3);
}
```

### 3.3. Form Control Style (P2, P9)

**Read-only input** hiện tại là `readonly="1" class="form-control bg-light"`.

**Sau**:
```xml
<input type="text" class="form-control psm-form-control" 
       t-att-value="employee.name" readonly="1"/>
```

**SCSS**:
```scss
.o_psm_0213_portal .psm-form-control {
    background: var(--psm-0213-gray-50);
    border: 1px solid var(--psm-0213-border);
    border-radius: var(--psm-0213-radius-sm);
    color: var(--psm-0213-text);
    padding: var(--psm-0213-space-3) var(--psm-0213-space-4);
}

.o_psm_0213_portal .psm-form-control:focus,
.o_psm_0213_portal .psm-form-control:active {
    border-color: var(--psm-0213-yellow-500);
    box-shadow: 0 0 0 3px rgba(255, 199, 44, 0.25);
    outline: none;
}

.o_psm_0213_portal .psm-form-control:read-only,
.o_psm_0213_portal .psm-form-control[readonly] {
    background: var(--psm-0213-gray-100);
    color: var(--psm-0213-text-muted);
    cursor: not-allowed;
}

.o_psm_0213_portal .form-label {
    color: var(--psm-0213-text-strong);
    font-size: var(--psm-0213-fs-sm);
    font-weight: var(--psm-0213-fw-semibold);
    letter-spacing: 0.3px;
    margin-bottom: var(--psm-0213-space-2);
    text-transform: uppercase;
}
```

### 3.4. Progress Navigation (P3)

Sticky top với 3 dots (Thông tin → Ngày/lý do → Xác nhận).

**Từ V2 plan 0215**:
```scss
.o_psm_0213_portal .psm-form-progress {
    background: var(--psm-0213-white);
    border: 1px solid var(--psm-0213-border);
    border-radius: var(--psm-0213-radius-pill);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    display: flex;
    gap: var(--psm-0213-space-2);
    padding: var(--psm-0213-space-2);
    position: sticky;
    top: var(--psm-0213-space-4);
    z-index: 10;
}

.o_psm_0213_portal .psm-form-progress__dot {
    border-radius: var(--psm-0213-radius-pill);
    color: var(--psm-0213-text-muted);
    display: flex;
    flex: 1;
    font-size: var(--psm-0213-fs-sm);
    font-weight: var(--psm-0213-fw-semibold);
    gap: var(--psm-0213-space-1);
    justify-content: center;
    padding: var(--psm-0213-space-2) var(--psm-0213-space-3);
    text-decoration: none;
    transition: background-color 0.15s ease;
}

.o_psm_0213_portal .psm-form-progress__dot.is-active {
    background: var(--psm-0213-yellow-500);
    color: var(--psm-0213-text-strong);
}
```

### 3.5. Warning/Commitment Panel (P4, P10)

**Trước** — nền đỏ sáng, chữ đỏ:
```
[BUỘC PHẢI NHÂN CỬ CUỐI — chữ đỏ trên nền đỏ nhạt]
```

**Sau** — Design từ V2 (white bg + left-border đỏ + icon):
```scss
.o_psm_0213_portal .psm-commitment-panel {
    background: var(--psm-0213-white);
    border: 1px solid var(--psm-0213-red-500);
    border-left: 4px solid var(--psm-0213-red-500);
    border-radius: var(--psm-0213-radius-md);
    box-shadow: 0 4px 16px rgba(218, 41, 28, 0.15);
    margin-bottom: var(--psm-0213-space-5);
    padding: var(--psm-0213-space-5);
}

.o_psm_0213_portal .psm-commitment-panel__title {
    color: var(--psm-0213-red-600);
    font-size: var(--psm-0213-fs-md);
    font-weight: var(--psm-0213-fw-bold);
    margin-bottom: var(--psm-0213-space-3);
}

.o_psm_0213_portal .psm-commitment-panel__intro {
    color: var(--psm-0213-text);
    font-size: var(--psm-0213-fs-sm);
    margin-bottom: var(--psm-0213-space-4);
}

.o_psm_0213_portal .psm-commitment-item {
    align-items: flex-start;
    display: flex;
    gap: var(--psm-0213-space-3);
    margin-bottom: var(--psm-0213-space-3);
}

.o_psm_0213_portal .psm-commitment-item__num {
    align-items: center;
    background: var(--psm-0213-red-100);
    border-radius: 50%;
    color: var(--psm-0213-red-600);
    display: inline-flex;
    flex: 0 0 1.75rem;
    font-size: var(--psm-0213-fs-xs);
    font-weight: var(--psm-0213-fw-bold);
    height: 1.75rem;
    justify-content: center;
    width: 1.75rem;
}

.o_psm_0213_portal .psm-commitment-item__text {
    color: var(--psm-0213-text);
    font-size: var(--psm-0213-fs-sm);
    line-height: 1.6;
    margin-top: var(--psm-0213-space-1);
}
```

### 3.6. Buttons (P6, P8)

**Trước**:
- "Gửi yêu cầu" → `btn-primary` (blue Bootstrap)
- "Quay lại" → `btn-secondary` (gray Bootstrap)

**Sau**:
```xml
<button type="submit" class="psm-btn psm-btn--danger">
    <i class="fa fa-sign-out" aria-hidden="true"/> Gửi yêu cầu
</button>
<a href="/my" class="psm-btn psm-btn--secondary">
    <i class="fa fa-arrow-left" aria-hidden="true"/> Quay lại
</a>
```

**SCSS** (từ V2):
```scss
.o_psm_0213_portal .psm-btn {
    border-radius: var(--psm-0213-radius-pill);
    display: inline-flex;
    align-items: center;
    gap: var(--psm-0213-space-2);
    justify-content: center;
    min-height: 44px;
    padding: var(--psm-0213-space-3) var(--psm-0213-space-5);
    font-weight: var(--psm-0213-fw-bold);
    text-decoration: none;
    transition: all 0.15s ease;
}

.o_psm_0213_portal .psm-btn--danger {
    background: var(--psm-0213-red-500);
    color: var(--psm-0213-white);
    border: 1px solid var(--psm-0213-red-600);
}

.o_psm_0213_portal .psm-btn--danger:hover {
    background: var(--psm-0213-red-600);
    box-shadow: 0 6px 14px rgba(218, 41, 28, 0.3);
    transform: translateY(-1px);
}

.o_psm_0213_portal .psm-btn--secondary {
    background: var(--psm-0213-white);
    color: var(--psm-0213-text-strong);
    border: 1px solid var(--psm-0213-border-strong);
}

.o_psm_0213_portal .psm-btn--secondary:hover {
    background: var(--psm-0213-gray-50);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.o_psm_0213_portal .psm-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

### 3.7. Alert Boxes (Info/Success/Error)

**Từ V2**, sửa mapping status alert:
```scss
.o_psm_0213_portal .psm-alert {
    align-items: flex-start;
    border-radius: var(--psm-0213-radius-md);
    border-left: 4px solid;
    display: flex;
    gap: var(--psm-0213-space-3);
    padding: var(--psm-0213-space-4) var(--psm-0213-space-5);
}

.o_psm_0213_portal .psm-alert--info {
    background: var(--psm-0213-yellow-100);
    border-color: var(--psm-0213-yellow-500);
    color: var(--psm-0213-text-strong);
}

.o_psm_0213_portal .psm-alert--success {
    background: var(--psm-0213-gray-50);
    border-color: var(--psm-0213-yellow-500);
    color: var(--psm-0213-text-strong);
}

.o_psm_0213_portal .psm-alert--danger {
    background: var(--psm-0213-red-100);
    border-color: var(--psm-0213-red-500);
    color: var(--psm-0213-red-700);
}
```

---

## 4. Implementation Files

### 4.1. Template Changes

**File**: `addons/M02_P0213/views/resignation_portal_template.xml`

**Thay đổi**:
1. Wrapper class: `.psm-ops-resignation-portal` → `.o_psm_0213_portal`.
2. Thay đổi structure header — bọc vào `.psm-form-header`.
3. Bọc mỗi section vào `.psm-form-section` với index/title.
4. Thêm progress nav `.psm-form-progress` sticky top.
5. Refactor warning box → `.psm-commitment-panel` với numbered items.
6. Đổi button class: `btn-danger` → `psm-btn psm-btn--danger`.
7. Đổi input class: `form-control bg-light` → `form-control psm-form-control`.
8. Refactor alert boxes theo mapping `psm-alert--info/success/danger`.

### 4.2. CSS (Inline hoặc External)

**Option A** (recommended): Tạo file:
- `addons/M02_P0213/static/src/scss/portal_resignation_0213.scss`

Thêm vào manifest:
```python
"assets": {
    "web.assets_frontend": [
        "M02_P0213/static/src/scss/portal_resignation_0213.scss",
    ],
},
```

**Option B** (fallback): Giữ inline `<style>` trong template, refactor thành:
```xml
<style>
    /* Root tokens */
    .o_psm_0213_portal {
        --psm-0213-yellow: #FFC72C;
        --psm-0213-red: #DA291C;
        --psm-0213-black: #000000;
        --psm-0213-white: #FFFFFF;
        /* ... */
    }

    /* Components */
    .o_psm_0213_portal .psm-form-header { ... }
    .o_psm_0213_portal .psm-section__head { ... }
    /* ... */
</style>
```

### 4.3. JavaScript (Optional)

Nếu cần progress nav interactivity (smooth scroll, active state):
- Tạo file `addons/M02_P0213/static/src/js/portal_resignation_0213.js`.
- Hook vào progress nav click.
- IntersectionObserver update active dot khi scroll.

---

## 5. Nguyên Lý Design

### 5.1. Palette Tokens (Bắt Buộc)

```scss
.o_psm_0213_portal {
    --psm-0213-yellow: #FFC72C;       /* CTA, accent, highlight */
    --psm-0213-red: #DA291C;          /* Danger, rejection, urgent */
    --psm-0213-black: #000000;        /* Text, heading, strong */
    --psm-0213-white: #FFFFFF;        /* Card, form bg */
    
    /* Tints/shades */
    --psm-0213-yellow-100: #FFF4D0;
    --psm-0213-yellow-500: var(--psm-0213-yellow);
    --psm-0213-yellow-600: #E6B428;
    
    --psm-0213-red-100: #FCEAE7;
    --psm-0213-red-500: var(--psm-0213-red);
    --psm-0213-red-600: #B11F14;
    
    --psm-0213-gray-50: #FAFAFA;
    --psm-0213-gray-100: #F2F2F2;
    --psm-0213-gray-200: #E5E5E5;
    --psm-0213-gray-500: #6B6B6B;
    --psm-0213-gray-700: #3F3F3F;
    --psm-0213-gray-900: #111111;
    
    /* Semantic */
    --psm-0213-text: var(--psm-0213-gray-700);
    --psm-0213-text-strong: var(--psm-0213-gray-900);
    --psm-0213-text-muted: var(--psm-0213-gray-500);
    --psm-0213-border: var(--psm-0213-gray-200);
    --psm-0213-border-strong: var(--psm-0213-gray-300);
}
```

### 5.2. Spacing (4px scale)

4/8/12/16/24/32px — dùng CSS variables `--psm-0213-space-1` đến `--psm-0213-space-6`.

### 5.3. Typography

9 cấp với font-size, font-weight, letter-spacing rõ ràng.

### 5.4. Compliance vs 0215

- **Scope class**: `.o_psm_0213_portal` (khác 0215 `.o_psm_0215_portal`).
- **Token naming**: `--psm-0213-*` (khác 0215 `--psm-0215-*`).
- **Component class**: `psm-*` (có thể dùng chung như `.psm-btn`, `.psm-alert`).

→ **Không có conflict** giữa 2 module.

---

## 6. Đối Chiếu Với Module 0215

| Yếu tố | 0215 V1-V3 | 0213 V1 | Chú thích |
|---|---|---|---|
| Palette | 4 màu | 4 màu (giống) | Clone 0215 spec |
| Tokens | `--psm-0215-*` | `--psm-0213-*` | Scope riêng |
| Components | Banner, section, button, alert | Banner, section, button, alert | Pattern giống |
| Assets | SCSS file + manifest | SCSS file + manifest (option A) | Pattern giống |
| JavaScript | Vanilla JS IIFE | Progress nav script (option) | Tương tự V2 |
| Mobile | Responsive classes | Responsive classes | Tương tự |

---

## 7. Acceptance Criteria

| # | Tiêu chí | Verify |
|---|---|---|
| 1 | Header banner vàng McDonald's, centered, uppercase | Screenshot so sánh |
| 2 | 3 section có index circle vàng, left-border vàng | Inspect CSS `.psm-section__head` |
| 3 | Form input readonly bg-gray-100, border rõ | Input event read-only |
| 4 | Label text uppercase, semibold, muted-less | Compare weight/color |
| 5 | Progress nav sticky top, 3 dots với active indicator | Scroll page |
| 6 | Warning/commitment panel: white bg + left-border đỏ | Inspect box-shadow, border |
| 7 | Numbered items (1-4) trong commitment panel có background số | Inspect `.psm-commitment-item__num` |
| 8 | Button "Gửi yêu cầu" đỏ McDonald's, hover lift + shadow | Hover button |
| 9 | Button "Quay lại" trắng-viền, hover bg nhạt | Hover button |
| 10 | Alert info/success/error màu đúng theo mapping | Compare colors |
| 11 | Spacing uniform dùng 4px scale | Inspect gap/padding |
| 12 | Mobile responsive (375px): form stack, button full-width | DevTools mobile |
| 13 | No CSS leak sang module khác (0215, portal, etc) | Mở `/my` portal khác |
| 14 | Form submit `/my/resignation/submit` không lỗi | Submit form, check backend log |
| 15 | CSRF token vẫn có trong form | Inspect hidden input |

---

## 8. Implementation Roadmap

1. **Bước 1** — Backup + đọc file hiện tại.
2. **Bước 2** — Tạo token + spacing + typography variables.
3. **Bước 3** — Refactor template wrapper class + section structure.
4. **Bước 4** — Implement component CSS (header, section, form-control, commitment-panel, button, alert).
5. **Bước 5** — Thêm progress nav HTML + CSS.
6. **Bước 6** — (Optional) Thêm JS untuk interactivity.
7. **Bước 7** — Test + Regression check.

---

## 9. Constraint & Risk

### Constraint

- KHÔNG sửa form action, field name, readonly, CSRF.
- KHÔNG sửa controller/model.
- KHÔNG thêm dependency.
- KHÔNG override CSS global.

### Risk

| Risk | Likelihood | Mitigation |
|---|---|---|
| CSS conflict với 0215/portal | Low | Scope class `.o_psm_0213_portal`, token `0213` |
| Form submit fail | Low | Giữ name/action/enctype, test form post |
| Asset load fail | Low | Check manifest syntax, asset path |
| Mobile layout break | Medium | Test 375px width, use responsive utilities |

---

## 10. Prompt Cho Executor (Codex)

> Copy-paste khi giao task:

---

**Bạn là Codex. Task: chỉnh sửa UI Portal form yêu cầu nghỉ việc module `addons/M02_P0213` theo Blueprint V1. Không sửa logic, route, form field. Chỉ UI/UX.**

### Files Đọc

- `addons/M02_P0213/notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md` (file này)
- `addons/M02_P0213/views/resignation_portal_template.xml`
- `addons/M02_P0213/__manifest__.py`

### Palette McDonald's (Bắt Buộc)

- Yellow `#FFC72C` — CTA, accent, highlight
- Red `#DA291C` — danger, urgent, rejection
- Black `#000000` — text, heading
- White `#FFFFFF` — background

### 10 Điểm Sửa

Xem mục 3.1-3.7 blueprint. Tóm:
- **P1**: Header banner vàng, uppercase, centered.
- **P2**: Input readonly style border+bg, không plain readonly.
- **P3**: Thêm progress nav 3-dot sticky top.
- **P4**: Warning panel: white bg + left-border đỏ (không nền đỏ).
- **P5**: Section index circle vàng, left-border.
- **P6**: Button gap 12px, hover lift.
- **P7**: Bỏ HR line cổ điển.
- **P8**: Áp dụng palette #FFC72C, #DA291C bắt buộc.
- **P9**: Label text uppercase + semibold.
- **P10**: Numbered items (1-4) commitment panel có background số.

### Implement

1. Backup file.
2. Đổi wrapper `.psm-ops-resignation-portal` → `.o_psm_0213_portal`.
3. Bọc header → `.psm-form-header` + 4 heading levels rút gọn.
4. Bọc section → `.psm-form-section` với index/title.
5. Thêm progress nav trước form.
6. Refactor commitment panel → white bg + left-border đỏ + numbered items.
7. Input class: `form-control bg-light` → `form-control psm-form-control`.
8. Button class: `btn-danger` → `psm-btn psm-btn--danger`.
9. Alert class mapping: `alert-info` → `psm-alert psm-alert--info`.
10. SCSS: thêm (inline hoặc file) tokens + components.

### Constraint

- KHÔNG đổi `name`, `readonly`, `action`, CSRF.
- KHÔNG sửa controller.
- Scope CSS dưới `.o_psm_0213_portal`.
- Token `--psm-0213-*` (khác `0215`).

### Test

```bash
python odoo-bin -d <db> -u M02_P0213 --stop-after-init
```

Browser: `/my/resignation` (hoặc route form) — desktop 1280px + mobile 375px.
- Header vàng, section index tròn, warning panel trắng-viền đỏ, button hover lift, input bg-gray.

Regression: `/my` portal khác không đổi.

---

## Files Used For Confirmation

| File | Vai trò |
|---|---|
| Screenshot form yêu cầu nghỉ việc (1920x2688) | Phát hiện 10 vấn đề UI/UX |
| `addons/M02_P0213/views/resignation_portal_template.xml` (37690 bytes) | Xác nhận template hiện tại — form action, field structure, alert/button bootstrap |
| Module 0215 Blueprint V1-V3 | Tham chiếu design system, component pattern, token naming |
| `addons/M02_P0213/__manifest__.py` | Xác nhận manifest — dependencies, check assets key |
