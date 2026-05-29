# Technical Blueprint V2 — Portal UI Polish & UX Enhancement (M02_P0215)

> **Phạm vi**: Nâng cấp giao diện Portal 0215 đã ổn (V1) lên mức **chuyên nghiệp** — áp dụng nguyên lý màu sắc (tương đồng / tương phản / cân bằng), tinh chỉnh spacing/padding, bổ sung **JS UX micro-interactions** để giảm tải nhận thức cho người dùng.
> **Loại**: Blueprint/Planning V2. Dùng cho AI Coder (Codex) thực thi sau.
> **Ngày**: 2026-05-12
> **Trạng thái baseline**: V1 đã được apply — manifest có asset, SCSS đã tồn tại 404 dòng, template đã có wrapper `.o_psm_0215_portal`, các class `psm-*` đã chạy. V2 chỉ refine + thêm JS nhẹ.

---

## 0. Tóm Tắt Mục Tiêu V2

| Hạng mục | Vấn đề hiện tại | Mục tiêu V2 |
|---|---|---|
| **Color harmony** | Vàng/đỏ/đen dùng đúng nhưng đặt cạnh nhau gắt, thiếu màu trung gian (cream/gray) làm "đệm" | Hệ thống 3 layer: Brand (yellow/red) → Neutral cream/gray → Accent. Áp dụng tỷ lệ 60-30-10 |
| **Contrast & padding** | Badge dính sát text date, label sát value, button cluster sát nhau | Tăng `gap` + `padding-inline` consistent. Áp dụng 4/8/12/16/24/32 spacing scale |
| **Visual hierarchy** | Section index tròn vàng tốt, nhưng title và body cùng cấp weight, khó scan | Phân 3 cấp: Banner (uppercase 700) → Section title (600) → Field label (500 muted) |
| **Micro-interactions** | Hover chỉ đổi màu nền nhẹ, không feedback rõ click/focus | Hover lift (`translateY(-1px)` + shadow), focus ring vàng, transition 150ms |
| **Form UX** | Form dài 5 section, không có progress, không auto-save, mobile cuộn dài | Section progress sticky top, auto-resize textarea, validate inline, confirm trước rời page |
| **Mobile nav** | Cardlist OK nhưng không có sticky action, signature touch khó | Bottom action bar trên mobile, signature canvas có nút "Vẽ to hơn" để mở fullscreen |
| **Empty/loading/error states** | Empty state có nhưng đơn điệu | Illustration ASCII/icon lớn + CTA contextual + helper text |
| **Status communication** | Badge OK nhưng không có timeline/stepper | Mini horizontal stepper hiển thị 12 state map, current state highlight |

---

## 1. Color System V2 — Tone & Hierarchy

### 1.1. 3-Layer Color Model

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1 — FOUNDATION (60% màn hình)                    │
│  Cream/White/Light gray nền — đệm cho mắt nghỉ           │
├─────────────────────────────────────────────────────────┤
│  LAYER 2 — STRUCTURE (30% màn hình)                     │
│  Black/Dark gray text + borders + iconography           │
├─────────────────────────────────────────────────────────┤
│  LAYER 3 — BRAND ACCENT (10% màn hình)                  │
│  Yellow #FFC72C: CTA, highlight, focus, active          │
│  Red    #DA291C: danger, urgent, reject, alert critical │
└─────────────────────────────────────────────────────────┘
```

> **Quy tắc 60-30-10** đảm bảo brand color không "ngộp" mắt, đồng thời vẫn nổi bật khi xuất hiện.

### 1.2. Mở Rộng Token (KHÔNG đổi 4 màu palette chính)

Bổ sung vào `:root` của `.o_psm_0215_portal`:

```scss
.o_psm_0215_portal {
    /* === BRAND (giữ nguyên V1) === */
    --psm-0215-yellow:        #FFC72C;
    --psm-0215-red:           #DA291C;
    --psm-0215-black:         #000000;
    --psm-0215-white:         #FFFFFF;

    /* === V2: TINTS & SHADES có hệ thống === */
    /* Yellow ramp — đi từ subtle → bold */
    --psm-0215-yellow-50:     #FFFBEC;   /* page bg cực nhạt */
    --psm-0215-yellow-100:    #FFF4D0;   /* alert/banner bg (V1 đã có với tên -soft) */
    --psm-0215-yellow-200:    #FFE89A;   /* hover state nhẹ */
    --psm-0215-yellow-500:    #FFC72C;   /* brand primary */
    --psm-0215-yellow-600:    #E6B428;   /* hover/active */
    --psm-0215-yellow-700:    #B98E1F;   /* text vàng trên nền sáng (đạt AA) */

    /* Red ramp */
    --psm-0215-red-50:        #FFF5F4;
    --psm-0215-red-100:       #FCEAE7;   /* (V1 -soft) */
    --psm-0215-red-200:       #F5B8B2;
    --psm-0215-red-500:       #DA291C;   /* brand danger */
    --psm-0215-red-600:       #B11F14;   /* hover/active */
    --psm-0215-red-700:       #8A1810;   /* text đỏ đậm */

    /* Neutral ramp — quan trọng, làm "đệm" giữa các vùng brand */
    --psm-0215-cream-50:      #FDFBF4;   /* page background — màu cream nhẹ hợp brand vàng */
    --psm-0215-gray-50:       #FAFAFA;
    --psm-0215-gray-100:      #F2F2F2;
    --psm-0215-gray-200:      #E5E5E5;
    --psm-0215-gray-300:      #D1D1D1;
    --psm-0215-gray-400:      #9CA3AF;   /* placeholder */
    --psm-0215-gray-500:      #6B6B6B;
    --psm-0215-gray-700:      #3F3F3F;
    --psm-0215-gray-900:      #111111;   /* heading thay vì pure black khi cần mềm hơn */

    /* === SEMANTIC TOKENS — UI chỉ tham chiếu vào đây === */
    --psm-0215-bg-page:       var(--psm-0215-cream-50);
    --psm-0215-bg-card:       var(--psm-0215-white);
    --psm-0215-bg-section:    var(--psm-0215-gray-50);
    --psm-0215-bg-hover:      rgba(255, 199, 44, 0.08);

    --psm-0215-text-strong:   var(--psm-0215-gray-900);
    --psm-0215-text:          var(--psm-0215-gray-700);
    --psm-0215-text-muted:    var(--psm-0215-gray-500);
    --psm-0215-text-on-dark:  var(--psm-0215-white);

    --psm-0215-border:        var(--psm-0215-gray-200);
    --psm-0215-border-strong: var(--psm-0215-gray-300);
    --psm-0215-border-focus:  var(--psm-0215-yellow-500);
}
```

### 1.3. Nguyên Lý Áp Dụng

#### Tương đồng (Analogous) — Dùng cho vùng cùng chức năng

- **Vàng + Cream + Yellow-100**: nhóm "info/highlight" → banner header, alert success, action panel.
- **Đỏ + Red-100 + Red-50**: nhóm "danger/urgent" → reject button, error alert, badge "Thông báo".

> Lý do: cùng tone tạo cảm giác "thuộc một nhóm", giảm noise.

#### Tương phản (Contrast) — Dùng cho thứ cần nổi bật ngay

- **Đen trên Vàng**: CTA primary (contrast 11.5:1 — AAA).
- **Trắng trên Đỏ**: reject button (4.5:1 — AA large).
- **Đen trên Trắng**: body text (21:1).

> Không bao giờ đặt: Vàng trên Trắng / Vàng trên Đỏ / Đỏ trên Vàng cho text (contrast < 3:1).

#### Cân bằng (Balance) — Tỷ lệ trên page

```
Detail page tiêu chuẩn:
├── Banner (Yellow):           ~ 80px / page ~ 1500px = 5%
├── Action panel (Yellow-100): ~ 200px = 13%
├── Body (Cream/White):                  ~ 60%
├── Section header (Yellow accent line): ~ 5%
├── Borders/dividers (gray-200):         ~ 5%
└── Text (gray-900):                     ~ 12%
                              TOTAL: brand 10-15%, neutral 75%, text 12%
```

### 1.4. Mapping Component → Token

| Component | Background | Text | Border |
|---|---|---|---|
| Page wrapper | `--psm-0215-bg-page` (cream-50) | `--psm-0215-text` | — |
| Card | `--psm-0215-bg-card` (white) | `--psm-0215-text` | `--psm-0215-border` |
| Banner | `--psm-0215-yellow-500` | `--psm-0215-text-strong` | — |
| Section panel | `--psm-0215-bg-section` (gray-50) | `--psm-0215-text` | `--psm-0215-border` |
| Section index circle | `--psm-0215-yellow-500` | `--psm-0215-text-strong` | — |
| Section title underline | `--psm-0215-yellow-500` (border-left 4px) | — | — |
| Field label | transparent | `--psm-0215-text-muted` | — |
| Field value | transparent | `--psm-0215-text-strong` (font-weight 600) | — |
| Status badge "progress" | `--psm-0215-yellow-500` | `--psm-0215-black` | — |
| Status badge "pending" | `--psm-0215-red-500` | `--psm-0215-white` | — |
| Status badge "success" | `--psm-0215-gray-900` | `--psm-0215-white` | `--psm-0215-yellow-500` (2px inset) |
| Status badge "neutral" | `--psm-0215-gray-100` | `--psm-0215-gray-700` | — |
| Btn primary | `--psm-0215-yellow-500` | `--psm-0215-text-strong` | `--psm-0215-yellow-600` (1px) |
| Btn primary hover | `--psm-0215-yellow-600` | `--psm-0215-text-strong` | `--psm-0215-yellow-700` |
| Btn danger | `--psm-0215-red-500` | `--psm-0215-white` | `--psm-0215-red-600` |
| Btn secondary | `--psm-0215-white` | `--psm-0215-text-strong` | `--psm-0215-border-strong` |
| Alert success | `--psm-0215-yellow-100` | `--psm-0215-text-strong` | `--psm-0215-yellow-500` (4px left) |
| Alert danger | `--psm-0215-red-100` | `--psm-0215-red-700` | `--psm-0215-red-500` (4px left) |
| Alert info | `--psm-0215-gray-100` | `--psm-0215-text` | `--psm-0215-border-strong` (4px left) |

---

## 2. Spacing & Typography Scale

### 2.1. Spacing Scale Cứng

Mọi `padding`, `margin`, `gap` phải tham chiếu vào scale:

```scss
.o_psm_0215_portal {
    --psm-0215-space-1:  0.25rem;  /*  4px */
    --psm-0215-space-2:  0.5rem;   /*  8px */
    --psm-0215-space-3:  0.75rem;  /* 12px */
    --psm-0215-space-4:  1rem;     /* 16px */
    --psm-0215-space-5:  1.5rem;   /* 24px */
    --psm-0215-space-6:  2rem;     /* 32px */
    --psm-0215-space-7:  3rem;     /* 48px */

    --psm-0215-radius-sm: 0.375rem;
    --psm-0215-radius-md: 0.5rem;
    --psm-0215-radius-lg: 0.75rem;
    --psm-0215-radius-pill: 999px;
}
```

### 2.2. Rule Padding Cụ Thể (Sửa Vấn Đề Hiện Tại)

| Element | Hiện tại | V2 |
|---|---|---|
| Status badge | `padding: .4rem .75rem` | `padding: .35rem .875rem` + `min-width: 6rem` (cố định để align) |
| Status badge + adjacent text | dính sát | `margin-left: var(--psm-0215-space-3)` |
| Table cell `<td>` | `padding: .75rem` | `padding: var(--psm-0215-space-3) var(--psm-0215-space-4)` |
| Table row gap (date ↔ badge) | dính sát | thêm `gap: var(--psm-0215-space-3)` cho `<td>` flex-end |
| Label ↔ Value (info field) | dính sát | `display: flex` + `gap: var(--psm-0215-space-2)` hoặc `<dl>` với `margin-bottom: var(--psm-0215-space-2)` |
| Section panel `padding` | `1rem` | `var(--psm-0215-space-5)` (24px) |
| Card border-radius | `.5rem` | `var(--psm-0215-radius-lg)` (12px — mềm mại hơn, hợp brand McDonald's) |
| Button padding | `.5rem 1rem` | `var(--psm-0215-space-3) var(--psm-0215-space-5)` |
| Button cluster gap | dính sát | `gap: var(--psm-0215-space-3)` (12px) |
| Banner padding | `1rem 1.25rem` | `var(--psm-0215-space-4) var(--psm-0215-space-5)` |

### 2.3. Typography Scale

```scss
.o_psm_0215_portal {
    --psm-0215-fs-xs:   0.75rem;   /* 12px — micro label, badge */
    --psm-0215-fs-sm:   0.875rem;  /* 14px — helper, footnote */
    --psm-0215-fs-base: 1rem;      /* 16px — body */
    --psm-0215-fs-md:   1.125rem;  /* 18px — section title */
    --psm-0215-fs-lg:   1.25rem;   /* 20px — page heading */
    --psm-0215-fs-xl:   1.5rem;    /* 24px — banner title */

    --psm-0215-fw-regular: 400;
    --psm-0215-fw-medium:  500;
    --psm-0215-fw-semibold: 600;
    --psm-0215-fw-bold:    700;
    --psm-0215-fw-black:   800;

    --psm-0215-lh-tight:  1.25;
    --psm-0215-lh-base:   1.5;
    --psm-0215-lh-relaxed: 1.7;
}
```

| Cấp | Element | Font size | Weight | Letter-spacing |
|---|---|---|---|---|
| 1 | Banner title | `--fs-xl` | 800 | `0.5px` uppercase |
| 2 | Page heading | `--fs-lg` | 700 | normal |
| 3 | Section title | `--fs-md` | 700 | normal |
| 4 | Card sub-title | `--fs-base` | 600 | normal |
| 5 | Field label | `--fs-sm` | 500 | uppercase + `0.4px` |
| 6 | Field value | `--fs-base` | 600 | normal |
| 7 | Body text | `--fs-base` | 400 | normal |
| 8 | Helper/hint | `--fs-sm` | 400 (italic) | normal |
| 9 | Badge | `--fs-xs` | 700 | uppercase + `0.5px` |

---

## 3. Component-Level Refinement

### 3.1. Banner Header

**Trước (V1)**:
```scss
.psm-banner { padding: 1rem 1.25rem; border-radius: .75rem .75rem 0 0; }
```

**Sau (V2)**:
```scss
.o_psm_0215_portal .psm-banner {
    align-items: center;
    background: var(--psm-0215-yellow-500);
    background-image: linear-gradient(
        135deg,
        var(--psm-0215-yellow-500) 0%,
        var(--psm-0215-yellow-600) 100%
    ); /* gradient nhẹ tăng depth */
    border-radius: var(--psm-0215-radius-lg) var(--psm-0215-radius-lg) 0 0;
    color: var(--psm-0215-text-strong);
    display: flex;
    flex-wrap: wrap;
    font-size: var(--psm-0215-fs-xl);
    font-weight: var(--psm-0215-fw-black);
    gap: var(--psm-0215-space-4);
    justify-content: space-between;
    letter-spacing: 0.5px;
    padding: var(--psm-0215-space-4) var(--psm-0215-space-5);
    position: relative;
    text-transform: uppercase;
}

/* Tạo "tab visual" — dải đen nhỏ phía trái như McDonald's */
.o_psm_0215_portal .psm-banner::before {
    background: var(--psm-0215-black);
    border-radius: 0 var(--psm-0215-radius-sm) var(--psm-0215-radius-sm) 0;
    content: "";
    height: 60%;
    left: 0;
    position: absolute;
    top: 20%;
    width: 4px;
}
```

> Nguyên lý: gradient nhẹ + thanh đen tạo "anchor" cho mắt, nhắc lại logo McDonald's (vàng + đen).

### 3.2. Section Index Circle

**Trước**: tròn vàng đơn giản.
**Sau**:
```scss
.o_psm_0215_portal .psm-section__index {
    align-items: center;
    background: var(--psm-0215-yellow-500);
    border: 2px solid var(--psm-0215-yellow-600);
    border-radius: 50%;
    box-shadow: 0 2px 6px rgba(255, 199, 44, 0.4);
    color: var(--psm-0215-text-strong);
    display: inline-flex;
    flex: 0 0 2.25rem;
    font-size: var(--psm-0215-fs-base);
    font-weight: var(--psm-0215-fw-black);
    height: 2.25rem;
    justify-content: center;
    transition: transform 0.15s ease;
    width: 2.25rem;
}

.o_psm_0215_portal .psm-section:hover .psm-section__index {
    transform: scale(1.08);
}
```

### 3.3. Status Badge

**Sửa vấn đề "dính sát text" + tăng polish**:
```scss
.o_psm_0215_portal .psm-status {
    align-items: center;
    border-radius: var(--psm-0215-radius-pill);
    display: inline-flex;
    font-size: var(--psm-0215-fs-xs);
    font-weight: var(--psm-0215-fw-bold);
    gap: var(--psm-0215-space-1);
    letter-spacing: 0.5px;
    line-height: 1;
    min-height: 1.75rem;
    min-width: 6rem; /* THÊM: align dọc trong list */
    justify-content: center;
    padding: var(--psm-0215-space-2) var(--psm-0215-space-4);
    text-transform: uppercase;
    white-space: nowrap;
}

/* Dot indicator trước text — micro detail */
.o_psm_0215_portal .psm-status::before {
    background: currentColor;
    border-radius: 50%;
    content: "";
    flex: 0 0 0.4rem;
    height: 0.4rem;
    opacity: 0.7;
    width: 0.4rem;
}

/* Variant pending có hiệu ứng pulse — hút mắt employee */
.o_psm_0215_portal .psm-status-pending::before {
    animation: psmPulse 1.6s ease-in-out infinite;
    opacity: 1;
}

@keyframes psmPulse {
    0%, 100% { transform: scale(1);   opacity: 0.8; }
    50%      { transform: scale(1.4); opacity: 0.3; }
}
```

> Dot pulse chỉ áp `psm-status-pending` (state `notified`) — báo employee có việc cần làm gấp.

### 3.4. Buttons — Hover Lift + Shadow

```scss
.o_psm_0215_portal .psm-btn {
    align-items: center;
    border-radius: var(--psm-0215-radius-pill);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
    display: inline-flex;
    font-weight: var(--psm-0215-fw-bold);
    gap: var(--psm-0215-space-2);
    justify-content: center;
    min-height: 44px;
    padding: var(--psm-0215-space-3) var(--psm-0215-space-5);
    text-decoration: none;
    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease,
        transform 0.15s ease;
    will-change: transform;
}

.o_psm_0215_portal .psm-btn:hover:not(:disabled),
.o_psm_0215_portal .psm-btn:focus:not(:disabled) {
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
    transform: translateY(-1px);
}

.o_psm_0215_portal .psm-btn:active:not(:disabled) {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(0);
}

.o_psm_0215_portal .psm-btn:disabled {
    cursor: not-allowed;
    opacity: 0.55;
}

/* Loading state */
.o_psm_0215_portal .psm-btn.is-loading {
    color: transparent !important;
    pointer-events: none;
    position: relative;
}

.o_psm_0215_portal .psm-btn.is-loading::after {
    animation: psmSpin 0.6s linear infinite;
    border: 2px solid currentColor;
    border-radius: 50%;
    border-top-color: transparent;
    color: var(--psm-0215-text-strong);
    content: "";
    height: 1rem;
    left: calc(50% - 0.5rem);
    position: absolute;
    top: calc(50% - 0.5rem);
    width: 1rem;
}

@keyframes psmSpin {
    to { transform: rotate(360deg); }
}
```

> JS sẽ add class `is-loading` khi user submit — báo "đang xử lý", chống click double.

### 3.5. Card / Panel — Soft Shadow Layered

```scss
.o_psm_0215_portal .psm-panel {
    background: var(--psm-0215-bg-card);
    border: 1px solid var(--psm-0215-border);
    border-radius: var(--psm-0215-radius-lg);
    box-shadow:
        0 1px 2px rgba(0, 0, 0, 0.04),
        0 4px 12px rgba(0, 0, 0, 0.04);
    overflow: hidden;
    transition: box-shadow 0.2s ease;
}

.o_psm_0215_portal .psm-panel:hover {
    box-shadow:
        0 1px 2px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.08);
}
```

### 3.6. Table — Zebra + Hover State

**Sửa vấn đề list trong screenshot (badge dính date, row dính nhau)**:

```scss
.o_psm_0215_portal .psm-table {
    border: 1px solid var(--psm-0215-border);
    border-collapse: separate;
    border-radius: var(--psm-0215-radius-md);
    border-spacing: 0;
    overflow: hidden;
    width: 100%;
}

.o_psm_0215_portal .psm-table thead th {
    background: var(--psm-0215-gray-900);
    color: var(--psm-0215-white);
    font-size: var(--psm-0215-fs-xs);
    font-weight: var(--psm-0215-fw-bold);
    letter-spacing: 0.5px;
    padding: var(--psm-0215-space-3) var(--psm-0215-space-4);
    text-transform: uppercase;
}

.o_psm_0215_portal .psm-table tbody td {
    border-bottom: 1px solid var(--psm-0215-border);
    padding: var(--psm-0215-space-4);
    vertical-align: middle;
}

/* Zebra striping */
.o_psm_0215_portal .psm-table tbody tr:nth-child(even) {
    background: var(--psm-0215-gray-50);
}

.o_psm_0215_portal .psm-table tbody tr:hover {
    background: var(--psm-0215-bg-hover);
    cursor: pointer;
}

/* Cột reference dùng monospace + vàng nhấn */
.o_psm_0215_portal .psm-table .psm-cell-ref {
    color: var(--psm-0215-red-600);
    font-family: ui-monospace, "SF Mono", Consolas, monospace;
    font-weight: var(--psm-0215-fw-bold);
}

/* Cột status: căn phải, có spacing với date */
.o_psm_0215_portal .psm-table .psm-cell-status {
    text-align: right;
    white-space: nowrap;
}

.o_psm_0215_portal .psm-table .psm-cell-date {
    color: var(--psm-0215-text-muted);
    font-size: var(--psm-0215-fs-sm);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}
```

### 3.7. Action Panel — Card Accent

**Sửa vấn đề "vàng-vàng-đỏ" gắt trong panel accept/reject**:

```scss
.o_psm_0215_portal .psm-action-panel {
    background: var(--psm-0215-bg-card);
    border: 1px solid var(--psm-0215-yellow-500);
    border-left: 4px solid var(--psm-0215-yellow-500);
    border-radius: var(--psm-0215-radius-md);
    box-shadow: 0 4px 16px rgba(255, 199, 44, 0.15);
    margin-top: var(--psm-0215-space-5);
    padding: var(--psm-0215-space-5);
}

.o_psm_0215_portal .psm-action-panel__heading {
    align-items: center;
    color: var(--psm-0215-text-strong);
    display: flex;
    font-size: var(--psm-0215-fs-md);
    font-weight: var(--psm-0215-fw-bold);
    gap: var(--psm-0215-space-3);
    margin-bottom: var(--psm-0215-space-4);
}

.o_psm_0215_portal .psm-action-panel__icon {
    align-items: center;
    background: var(--psm-0215-yellow-500);
    border-radius: 50%;
    color: var(--psm-0215-text-strong);
    display: inline-flex;
    flex: 0 0 2rem;
    height: 2rem;
    justify-content: center;
    width: 2rem;
}

.o_psm_0215_portal .psm-action-panel__buttons {
    display: flex;
    flex-wrap: wrap;
    gap: var(--psm-0215-space-3);
    margin-top: var(--psm-0215-space-4);
}
```

> Đổi nền vàng đậm → nền trắng + left-border 4px vàng: vẫn "thuộc nhóm brand" nhưng không gắt mắt khi đặt button cùng.

---

## 4. Tính Năng UX Mới (JS)

### 4.1. File JS Bổ Sung

Tạo: `addons/M02_P0215/static/src/js/portal_psm_0215.js`

Khai báo trong manifest:
```python
"assets": {
    "web.assets_frontend": [
        "M02_P0215/static/src/scss/portal_psm_0215.scss",
        "M02_P0215/static/src/js/portal_psm_0215.js",  # THÊM
    ],
},
```

### 4.2. Yêu Cầu Thiết Kế JS

- **Vanilla JS** thuần — không thêm dependency (jQuery có sẵn Odoo nhưng tránh dùng vì rủi ro version).
- **No ES modules** (Odoo asset bundling phức tạp với module). Dùng IIFE:
  ```js
  (function () {
      'use strict';
      // ...
  })();
  ```
- **Scoped query**: chỉ chạy DOM bên trong `.o_psm_0215_portal` để không ảnh hưởng portal khác.
- **Defensive**: check `document.querySelector(...) === null` trước khi gắn event.

### 4.3. Tính Năng 1: Auto-Resize Textarea

**Vấn đề**: textarea 5 dòng cố định, user nhập nhiều phải cuộn nội bộ.

**Giải pháp**:
```js
function initAutoResizeTextareas(root) {
    const textareas = root.querySelectorAll('textarea.psm-autosize');
    textareas.forEach((ta) => {
        const resize = () => {
            ta.style.height = 'auto';
            ta.style.height = ta.scrollHeight + 'px';
        };
        ta.addEventListener('input', resize);
        ta.addEventListener('focus', resize);
        resize(); // initial
    });
}
```

QWeb sẽ thêm class `psm-autosize` vào các `<textarea>` Section I/II/III/IV.

### 4.4. Tính Năng 2: Form Section Progress Indicator

**Vấn đề**: create form dài 5 section, user không biết mình đang ở đâu.

**Giải pháp**: sticky top bar với 5 dots — click jump-to-section.

**HTML structure** (template thêm):
```xml
<nav class="psm-form-progress" aria-label="Tiến trình điền form">
    <a href="#psm-section-1" class="psm-form-progress__dot" data-section="1">
        <span class="psm-form-progress__num">1</span>
        <span class="psm-form-progress__lbl">Các bên</span>
    </a>
    <!-- ... 2-5 -->
</nav>
```

**SCSS**:
```scss
.o_psm_0215_portal .psm-form-progress {
    background: var(--psm-0215-bg-card);
    border: 1px solid var(--psm-0215-border);
    border-radius: var(--psm-0215-radius-pill);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    display: flex;
    gap: var(--psm-0215-space-2);
    padding: var(--psm-0215-space-2);
    position: sticky;
    top: var(--psm-0215-space-4);
    z-index: 10;
}

.o_psm_0215_portal .psm-form-progress__dot {
    align-items: center;
    border-radius: var(--psm-0215-radius-pill);
    color: var(--psm-0215-text-muted);
    display: flex;
    flex: 1 1 auto;
    font-size: var(--psm-0215-fs-sm);
    font-weight: var(--psm-0215-fw-semibold);
    gap: var(--psm-0215-space-2);
    justify-content: center;
    padding: var(--psm-0215-space-2) var(--psm-0215-space-3);
    text-decoration: none;
    transition: background-color 0.15s ease, color 0.15s ease;
}

.o_psm_0215_portal .psm-form-progress__dot.is-active {
    background: var(--psm-0215-yellow-500);
    color: var(--psm-0215-text-strong);
}

.o_psm_0215_portal .psm-form-progress__dot.is-done {
    color: var(--psm-0215-yellow-700);
}

.o_psm_0215_portal .psm-form-progress__dot.is-done::after {
    content: " \2713"; /* checkmark */
    font-weight: bold;
}

.o_psm_0215_portal .psm-form-progress__num {
    align-items: center;
    background: currentColor;
    border-radius: 50%;
    color: var(--psm-0215-bg-card);
    display: inline-flex;
    flex: 0 0 1.25rem;
    font-size: var(--psm-0215-fs-xs);
    height: 1.25rem;
    justify-content: center;
    width: 1.25rem;
}

@media (max-width: 767.98px) {
    .o_psm_0215_portal .psm-form-progress__lbl { display: none; }
}
```

**JS**:
```js
function initFormProgress(root) {
    const nav = root.querySelector('.psm-form-progress');
    if (!nav) return;
    const dots = nav.querySelectorAll('.psm-form-progress__dot');
    const sections = root.querySelectorAll('[id^="psm-section-"]');
    if (!dots.length || !sections.length) return;

    // Intersection observer cập nhật active dot
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const id = entry.target.id;
            dots.forEach((dot) => {
                dot.classList.toggle('is-active', dot.getAttribute('href') === '#' + id);
            });
        });
    }, { rootMargin: '-40% 0px -50% 0px' });

    sections.forEach((s) => observer.observe(s));

    // Smooth scroll khi click
    dots.forEach((dot) => {
        dot.addEventListener('click', (e) => {
            e.preventDefault();
            const target = root.querySelector(dot.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // Đánh dấu section đã điền (is-done) khi rời focus
    sections.forEach((section, idx) => {
        const requiredInputs = section.querySelectorAll('[required]');
        section.addEventListener('focusout', () => {
            const allFilled = Array.from(requiredInputs).every((i) => i.value.trim() !== '');
            const dot = dots[idx];
            if (dot && allFilled) dot.classList.add('is-done');
        });
    });
}
```

### 4.5. Tính Năng 3: Unsaved Changes Warning

**Vấn đề**: user lỡ điền nửa form rồi click sang trang khác → mất dữ liệu.

**Giải pháp**:
```js
function initUnsavedGuard(root) {
    const form = root.querySelector('form.psm-form-create');
    if (!form) return;
    let dirty = false;

    form.addEventListener('input', () => { dirty = true; }, { once: false });
    form.addEventListener('submit', () => { dirty = false; });

    window.addEventListener('beforeunload', (e) => {
        if (!dirty) return;
        e.preventDefault();
        e.returnValue = ''; // browser hiển thị warning mặc định
    });
}
```

### 4.6. Tính Năng 4: Submit Button Loading State

**Vấn đề**: user click submit → không có feedback → click lại → tạo 2 record.

**Giải pháp**:
```js
function initSubmitLoading(root) {
    const forms = root.querySelectorAll('form[data-psm-loading="1"]');
    forms.forEach((form) => {
        form.addEventListener('submit', (e) => {
            const btn = form.querySelector('button[type="submit"]');
            if (btn && !btn.classList.contains('is-loading')) {
                btn.classList.add('is-loading');
                btn.disabled = true;
                // Nếu form fail validate native → unlock sau 5s phòng hờ
                setTimeout(() => {
                    if (btn.classList.contains('is-loading')) {
                        btn.classList.remove('is-loading');
                        btn.disabled = false;
                    }
                }, 5000);
            }
        });
    });
}
```

### 4.7. Tính Năng 5: Smart Confirm Trước Reject

**Vấn đề**: nút "Từ chối" hiện đang submit ngay → user lỡ tay.

**Giải pháp**: confirm modal 2 bước:
```js
function initRejectConfirm(root) {
    const rejectButtons = root.querySelectorAll('[data-psm-confirm="reject"]');
    rejectButtons.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const note = root.querySelector('textarea[name="note"]');
            if (note && !note.value.trim()) {
                e.preventDefault();
                note.focus();
                showFlashAlert(root, 'Vui lòng nhập lý do từ chối trước khi gửi.', 'danger');
                return;
            }
            if (!confirm('Bạn có chắc chắn từ chối hình thức kỷ luật này? Hành động này không thể hoàn tác.')) {
                e.preventDefault();
            }
        });
    });
}

function showFlashAlert(root, message, type) {
    const slot = root.querySelector('.psm-flash-slot') || root;
    const div = document.createElement('div');
    div.className = 'psm-alert psm-alert--' + type;
    div.setAttribute('role', 'alert');
    div.innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i><span></span>';
    div.querySelector('span').textContent = message;
    slot.prepend(div);
    setTimeout(() => div.remove(), 4500);
}
```

### 4.8. Tính Năng 6: Signature Touch Improvement

**Vấn đề**: signature canvas mobile khó vẽ vì nhỏ.

**Giải pháp**: thêm nút "Phóng to để ký" mở modal fullscreen với canvas lớn.

```js
function initSignatureFullscreen(root) {
    const triggers = root.querySelectorAll('.psm-signature-fullscreen-btn');
    triggers.forEach((btn) => {
        btn.addEventListener('click', () => {
            const targetSelector = btn.getAttribute('data-target');
            const sourceCanvas = root.querySelector(targetSelector);
            if (!sourceCanvas) return;
            openSignatureModal(root, sourceCanvas, btn.getAttribute('data-name'));
        });
    });
}
```

> **Lưu ý**: signature logic hiện tại đã viết bằng JS inline trong template — KHÔNG đụng vào logic ký, chỉ thêm UI mở modal copy/clone canvas. Khi user ký xong trong modal → copy `toDataURL()` về hidden input gốc.

### 4.9. Tính Năng 7: Inline Search/Filter trên List

**Vấn đề**: list có 3 trang, không có search nhanh.

**Giải pháp**: client-side filter rows theo từ khoá:
```js
function initListFilter(root) {
    const input = root.querySelector('.psm-list-filter');
    if (!input) return;
    const rows = root.querySelectorAll('.psm-table tbody tr');
    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        rows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            row.style.display = !q || text.includes(q) ? '' : 'none';
        });
    });
}
```

> Đây là filter client-side trong trang hiện tại (không cross-page). Khi user pager sang trang khác → filter reset. Đủ tốt cho phần đông use case.

### 4.10. Bootstrap Hook

```js
(function () {
    'use strict';
    function boot() {
        document.querySelectorAll('.o_psm_0215_portal').forEach((root) => {
            initAutoResizeTextareas(root);
            initFormProgress(root);
            initUnsavedGuard(root);
            initSubmitLoading(root);
            initRejectConfirm(root);
            initSignatureFullscreen(root);
            initListFilter(root);
        });
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
```

---

## 5. Mini Status Stepper (Detail Page)

Hiển thị 12 state map dưới banner — user thấy ngay hồ sơ đang ở bước nào / còn bao nhiêu bước.

### 5.1. Compact Stepper (Desktop ≥ 992px)

```
[draft] → [under_review] → [level_det.] → [investigation] → ... → [active]
                   ●
```

### 5.2. Simplified Stepper (Mobile + Tablet)

3 milestones thay vì 12:
```
Khởi tạo    →    Đang xử lý    →    Kết thúc
                      ●
```

Mapping:
- `draft`, `under_review` → "Khởi tạo"
- `level_determination`, `investigation`, `hearing`, `proposal`, `issued`, `approval`, `notified` → "Đang xử lý"
- `active`, `expired`, `cancel` → "Kết thúc"

### 5.3. SCSS

```scss
.o_psm_0215_portal .psm-stepper {
    align-items: center;
    background: var(--psm-0215-bg-section);
    border-radius: 0 0 var(--psm-0215-radius-lg) var(--psm-0215-radius-lg);
    display: flex;
    gap: var(--psm-0215-space-2);
    overflow-x: auto;
    padding: var(--psm-0215-space-4) var(--psm-0215-space-5);
}

.o_psm_0215_portal .psm-stepper__step {
    align-items: center;
    color: var(--psm-0215-text-muted);
    display: inline-flex;
    flex: 0 0 auto;
    font-size: var(--psm-0215-fs-xs);
    font-weight: var(--psm-0215-fw-semibold);
    gap: var(--psm-0215-space-1);
    text-transform: uppercase;
    white-space: nowrap;
}

.o_psm_0215_portal .psm-stepper__step::after {
    color: var(--psm-0215-gray-300);
    content: "\203A"; /* › */
    margin-left: var(--psm-0215-space-2);
}

.o_psm_0215_portal .psm-stepper__step:last-child::after { display: none; }

.o_psm_0215_portal .psm-stepper__step.is-done { color: var(--psm-0215-yellow-700); }
.o_psm_0215_portal .psm-stepper__step.is-current {
    color: var(--psm-0215-text-strong);
    font-weight: var(--psm-0215-fw-black);
}
.o_psm_0215_portal .psm-stepper__step.is-current::before {
    background: var(--psm-0215-yellow-500);
    border-radius: 50%;
    content: "";
    display: inline-block;
    height: 0.5rem;
    margin-right: var(--psm-0215-space-1);
    width: 0.5rem;
}
```

### 5.4. QWeb Render

```xml
<t t-set="state_seq" t-value="[
    ('draft','Khởi tạo'),
    ('under_review','Xem xét'),
    ('level_determination','Xác định cấp'),
    ('investigation','Xác minh'),
    ('hearing','Họp'),
    ('proposal','Đề xuất'),
    ('issued','Ban hành'),
    ('approval','Phê duyệt'),
    ('notified','Thông báo'),
    ('active','Hiệu lực')
]"/>
<t t-set="current_idx" t-value="next((i for i, (k, _) in enumerate(state_seq) if k == record.state), -1)"/>
<nav class="psm-stepper" aria-label="Tiến trình hồ sơ">
    <t t-foreach="state_seq" t-as="step">
        <t t-set="cls" t-value="
            'is-current' if step[0] == record.state else
            ('is-done' if (current_idx &gt; 0 and state_seq.index(step) &lt; current_idx) else '')"/>
        <span t-attf-class="psm-stepper__step #{cls}">
            <t t-esc="step[1]"/>
        </span>
    </t>
</nav>
```

> Stepper chỉ hiển thị khi `record.state` thuộc `state_seq`. State đặc biệt (`expired`, `cancel`) → hiển thị banner riêng "Hồ sơ đã hết hiệu lực" hoặc "Đã hủy", không stepper.

---

## 6. Microcopy & Helper Text

Soạn tiếng Việt rõ ràng cho từng tình huống:

| Vị trí | Microcopy |
|---|---|
| Empty state list (employee) | "Bạn chưa có hồ sơ kỷ luật nào. Đây là tin tốt!" |
| Empty state list (manager) | "Chưa có hồ sơ kỷ luật cho nhân viên dưới quyền. Bấm 'Tạo Counseling Log' khi cần ghi nhận vi phạm." |
| Tooltip section index | "Bấm để xem chi tiết section #N" |
| Required marker `*` | tooltip: "Trường bắt buộc" |
| Signature pad placeholder | "Vẽ chữ ký bằng chuột (desktop) hoặc ngón tay (mobile)" |
| File upload hint | "Hỗ trợ ảnh JPG/PNG. Có thể chọn nhiều ảnh. Tổng dung lượng tối đa 10MB." |
| Submit button (create) | "Lưu & Tạo Counseling Log" |
| Submit button (employee sign) | "Gửi phản hồi & Ký xác nhận" |
| Submit button (manager finalize) | "Hoàn tất & Gửi RGM xét duyệt" |
| Reject button | "Từ chối hình thức kỷ luật" |
| Accept confirm | "Bạn xác nhận chấp nhận hình thức kỷ luật này?" |
| Reject confirm | "Bạn có chắc chắn từ chối hình thức kỷ luật này? Lý do từ chối sẽ gửi tới quản lý." |
| Unsaved warning | (native browser dialog) |
| Loading button label | (giữ text gốc, chỉ thêm spinner) |
| Toast success after create | "Hồ sơ DIS/{seq} đã được tạo. Đang chờ nhân viên phản hồi." |
| Toast danger after reject | "Đã gửi yêu cầu từ chối kèm lý do. Quản lý sẽ xem xét lại." |

---

## 7. Animation & Motion

### 7.1. Quy Tắc

- **Duration**: 150ms cho UI feedback, 200ms cho card hover, 300ms cho modal/drawer.
- **Easing**: `ease` cho 99% trường hợp, `cubic-bezier(0.4, 0, 0.2, 1)` cho modal.
- **Reduced motion**: respect `prefers-reduced-motion`.

```scss
@media (prefers-reduced-motion: reduce) {
    .o_psm_0215_portal *,
    .o_psm_0215_portal *::before,
    .o_psm_0215_portal *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

### 7.2. Áp Dụng

| Element | Animation | Trigger |
|---|---|---|
| `.psm-btn` | translateY(-1px) + shadow | hover/focus |
| `.psm-panel` | shadow elevate | hover |
| `.psm-section__index` | scale(1.08) | section hover |
| `.psm-status-pending::before` (dot) | pulse 1.6s loop | state = notified |
| `.psm-flash-slot .psm-alert` | slideInDown 250ms | mount |
| Section anchor scroll | smooth scroll | click progress dot |
| Modal open | fadeIn + scale 300ms | open |

### 7.3. Toast Slide-In

```scss
@keyframes psmSlideInDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.o_psm_0215_portal .psm-flash-slot .psm-alert {
    animation: psmSlideInDown 0.25s ease;
}
```

---

## 8. Responsive Refinement

### 8.1. Breakpoints

| Width | Behavior |
|---|---|
| ≥ 1200px | Container max 1140px, 2 cột layout cho info panel |
| 992-1199px | Container 960px, 2 cột giảm gap |
| 768-991px | 1 cột stack, sticky progress vẫn hiện |
| < 768px | Cardlist thay table, bottom sticky CTA, hide progress labels |

### 8.2. Mobile Bottom Sticky CTA

Trong create form, button "Lưu" trên mobile cần luôn nhìn thấy:

```scss
@media (max-width: 767.98px) {
    .o_psm_0215_portal .psm-sticky-actions {
        background: var(--psm-0215-bg-card);
        border-radius: 0;
        border-top: 1px solid var(--psm-0215-border);
        bottom: 0;
        box-shadow: 0 -6px 16px rgba(0, 0, 0, 0.08);
        left: 0;
        margin: 0;
        padding: var(--psm-0215-space-3) var(--psm-0215-space-4);
        position: fixed;
        right: 0;
        z-index: 50;
    }
    .o_psm_0215_portal .psm-sticky-actions .psm-btn {
        flex: 1 1 auto;
    }
    /* Đệm bottom cho body khỏi che footer */
    .o_psm_0215_portal .psm-form-body {
        padding-bottom: 5rem !important;
    }
}
```

### 8.3. Mobile Cardlist

Đã có ở V1 (`.psm-mobile-stack`). V2 polish:
```scss
@media (max-width: 767.98px) {
    .o_psm_0215_portal .psm-mobile-stack tr {
        border-radius: var(--psm-0215-radius-lg);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        padding: var(--psm-0215-space-4);
    }
    .o_psm_0215_portal .psm-mobile-stack td {
        padding: var(--psm-0215-space-2) 0;
    }
    .o_psm_0215_portal .psm-mobile-stack td::before {
        font-size: var(--psm-0215-fs-xs);
        font-weight: var(--psm-0215-fw-semibold);
        text-transform: uppercase;
    }
    /* Cột reference nổi bật */
    .o_psm_0215_portal .psm-mobile-stack td.psm-cell-ref {
        border-bottom: 1px solid var(--psm-0215-border);
        font-size: var(--psm-0215-fs-md);
        margin-bottom: var(--psm-0215-space-2);
        padding-bottom: var(--psm-0215-space-3);
    }
}
```

---

## 9. Implementation Plan Cho AI Coder

### Bước 1 — Mở rộng SCSS tokens

| Mục | File | Hành động |
|---|---|---|
| File | `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` | Thêm vào đầu file: tokens scale (yellow/red/gray 50-700), spacing, typography, radius. KHÔNG xóa tokens V1 — chỉ thêm. |
| Test | install/upgrade | `python odoo-bin -d <db> -u M02_P0215 --stop-after-init` không lỗi SCSS compile |
| Rủi ro | Tên token cũ V1 vẫn được tham chiếu | Giữ alias cũ: `--psm-0215-yellow: var(--psm-0215-yellow-500);` |

### Bước 2 — Refactor existing components dùng tokens mới

| Component | Selector | Hành động |
|---|---|---|
| Banner | `.psm-banner` | Thêm gradient + `::before` thanh đen, dùng spacing tokens |
| Section index | `.psm-section__index` | Thêm border + shadow + hover scale |
| Status badge | `.psm-status` | Thêm `min-width`, `::before` dot, pulse animation cho pending |
| Buttons | `.psm-btn`, `.psm-btn--primary/danger/secondary` | Thêm hover lift, loading state |
| Panel | `.psm-panel` | Layered shadow + hover transition |
| Table | `.psm-table` | Zebra striping, header dark bg, cell padding tokens |
| Action panel | `.psm-action-panel` | Đổi nền vàng → trắng + left-border, soft shadow |

### Bước 3 — Thêm component mới

| Component | Thêm SCSS | Thêm QWeb |
|---|---|---|
| Form progress nav | `.psm-form-progress` + variants | `<nav>` trong create form, IDs `psm-section-1..5` |
| Status stepper | `.psm-stepper` + states | Block ngay sau banner trong detail page |
| Flash slot | `.psm-flash-slot` | Wrapper `<div>` empty, JS sẽ inject alerts vào |
| List filter input | `.psm-list-filter` | Input search trong header list |
| Signature fullscreen btn | `.psm-signature-fullscreen-btn` | Button cạnh canvas |

### Bước 4 — Tạo file JS

| File | Đường dẫn | Nội dung |
|---|---|---|
| JS bundle | `addons/M02_P0215/static/src/js/portal_psm_0215.js` | 7 module: autoResize, formProgress, unsavedGuard, submitLoading, rejectConfirm, signatureFullscreen, listFilter |
| Manifest | `__manifest__.py` | Thêm JS vào `web.assets_frontend` |
| Rủi ro | jQuery global pollution | Dùng vanilla JS IIFE, scope query trong `.o_psm_0215_portal` |

### Bước 5 — Sửa QWeb template

| Template | Sửa gì |
|---|---|
| `portal_psm_my_disciplines` | Thêm `<input class="psm-list-filter">`, header `<th>` đậm hơn, `<td>` thêm class `psm-cell-ref`/`psm-cell-date`/`psm-cell-status` + `data-label` đầy đủ |
| `portal_psm_discipline_create` | Thêm `<nav class="psm-form-progress">`, mỗi section block thêm `id="psm-section-N"`. Textarea thêm class `psm-autosize`. Form thêm `class="psm-form-create"` + `data-psm-loading="1"`. **Sửa bug duplicate witness select** (nếu còn trong source) |
| `portal_psm_discipline_explanation_template` | Thêm `<nav class="psm-stepper">` ngay sau banner. Action panel cho accept/reject thêm wrapper `psm-action-panel__heading` + icon. Nút reject thêm `data-psm-confirm="reject"`. Form respond thêm `data-psm-loading="1"`. Thêm `<div class="psm-flash-slot">` ngay đầu page body |

### Bước 6 — Test

```bash
# 1. Upgrade
python odoo-bin -d <db_test> -u M02_P0215 --stop-after-init

# 2. Test với Chrome DevTools mobile emulation
#    - /my → sidebar link OK
#    - /my/disciplines → table có zebra, filter input hoạt động, badge có dot pulse cho 'notified'
#    - /my/discipline/create → form progress nav sticky, click dot → smooth scroll, textarea auto-resize
#    - /my/discipline/<id> → stepper hiện 10 step, current state có dot vàng, action panel có icon
#    - Click submit → button có spinner, không double-click được
#    - Click reject mà chưa nhập note → flash alert đỏ
#    - Click reject có note → confirm dialog

# 3. Reduced motion
#    - Chrome DevTools → Rendering → Emulate CSS media feature → prefers-reduced-motion: reduce
#    - Hover button → không lift, không transition
```

### Bước 7 — Regression

Mở 1 trang portal module khác (ví dụ `/my/invoices`, `/my/orders`, `/my`):
- Bootstrap classes (`.card`, `.btn`, `.table`, `.alert`) UI không đổi.
- Sidebar link các module khác hiển thị bình thường.
- Pager `t-call="portal.pager"` không lỗi.

---

## 10. Updated Prompt Cho Executor (Codex)

> Copy-paste nguyên văn:

---

**Bạn là AI Coder thực hiện V2 polish cho Portal UI module `addons/M02_P0215`. V1 đã apply (SCSS + wrapper class `.o_psm_0215_portal` + manifest assets đã có). V2 chỉ thêm/refine, KHÔNG sửa logic, route, controller, model, security.**

### Pre-Flight

Đọc trước:
- `addons/M02_P0215/notes/BLUEPRINT_PORTAL_UI_REDESIGN_0215_V2_POLISH.md` (file này)
- `addons/M02_P0215/__manifest__.py`
- `addons/M02_P0215/static/src/scss/portal_psm_0215.scss`
- `addons/M02_P0215/views/x_psm_portal_templates.xml`
- `addons/M02_P0215/controllers/portal.py` (chỉ đọc, KHÔNG sửa)

### Palette Bắt Buộc (KHÔNG ĐỔI)

- Yellow `#FFC72C` — CTA, highlight, focus
- Red `#DA291C` — danger, reject, urgent
- Black `#000000` — text, heading
- White `#FFFFFF` — card, form bg
- Cream `#FDFBF4` — page bg (mới, là yellow-50, vẫn nằm trong "tinh thần" brand)

### Nguyên Lý Màu

- Tỷ lệ 60-30-10: 60% neutral, 30% text-strong, 10% brand accent.
- **Tương đồng**: vàng + cream cùng nhóm, đỏ + red-100 cùng nhóm.
- **Tương phản**: đen trên vàng (CTA primary), trắng trên đỏ (CTA danger).
- KHÔNG đặt chữ vàng trên trắng/cream (contrast yếu).
- KHÔNG đặt cạnh nhau 2 vùng vàng đậm rộng — phải có cream/white làm đệm.

### Spacing Tokens (Bắt Buộc)

Mọi padding/margin/gap dùng tokens: 4/8/12/16/24/32px (xem mục 2.1).

Đặc biệt sửa các điểm hiện tại:
- Status badge ↔ text liền kề: `gap: 12px`.
- Table cell padding: `12px 16px` (không phải `8px`).
- Form section panel padding: `24px`.
- Button cluster gap: `12px`.

### Files Cần Sửa

| File | Hành động |
|---|---|
| `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` | Mở rộng tokens, refactor components, thêm component mới |
| `addons/M02_P0215/static/src/js/portal_psm_0215.js` | **TẠO MỚI** — vanilla JS IIFE |
| `addons/M02_P0215/__manifest__.py` | Thêm JS vào `web.assets_frontend` |
| `addons/M02_P0215/views/x_psm_portal_templates.xml` | Thêm class/id mới, không đổi `name`/`id`/`csrf_token`/`enctype` |

### JS Module (7 features)

1. `initAutoResizeTextareas` — textarea grow theo nội dung.
2. `initFormProgress` — sticky nav 5 dot, smooth scroll, intersection observer active state.
3. `initUnsavedGuard` — `beforeunload` warn nếu form dirty.
4. `initSubmitLoading` — add `is-loading` class + disabled, timeout 5s.
5. `initRejectConfirm` — validate note trước, `confirm()` dialog xác nhận.
6. `initSignatureFullscreen` — modal canvas to hơn cho mobile.
7. `initListFilter` — client-side filter rows theo input.

Yêu cầu JS:
- Vanilla, IIFE wrapper `(function () { ... })();`
- Scope `document.querySelectorAll('.o_psm_0215_portal')` rồi traverse trong root.
- Defensive: check element tồn tại.
- Boot trên `DOMContentLoaded`.

### CSS Refinements

1. Banner: gradient + thanh đen `::before` 4px.
2. Section index circle: border + shadow + `:hover scale(1.08)`.
3. Status badge: `min-width: 6rem` + `::before` dot, pulse animation **chỉ** cho `psm-status-pending`.
4. Button: hover lift `translateY(-1px)` + shadow, loading spinner `::after`.
5. Panel: layered shadow.
6. Table: zebra striping `tbody tr:nth-child(even)`, header dark bg, monospace cho cột reference.
7. Action panel: nền trắng + left-border 4px vàng (KHÔNG nền vàng đậm).
8. Stepper: horizontal flow 10 step, dot vàng cho current.
9. Form progress: sticky top + IntersectionObserver active.
10. `@media (prefers-reduced-motion: reduce)` disable mọi animation.

### QWeb Changes (KHÔNG ĐỔI input name/id/csrf/enctype)

- List template: thêm `<input class="psm-list-filter">`, classify `<td>` với `psm-cell-ref|date|status`, `data-label` đầy đủ.
- Create template: bọc `<nav class="psm-form-progress">` ngay đầu form, `id="psm-section-1..5"` cho mỗi section, `class="psm-autosize"` cho textarea, `class="psm-form-create" data-psm-loading="1"` cho `<form>`. **KIỂM TRA bug duplicate witness select trong screenshot** — nếu source có 2 `<select name="witness_id">` thì xóa 1 cái, giữ logic JS.
- Detail template: `<nav class="psm-stepper">` sau banner, `<div class="psm-flash-slot">` trên đầu body, action panel thêm icon header, button reject thêm `data-psm-confirm="reject"`.

### Microcopy (Sửa Cố Định)

- "GỬI PHÀN HỒI" → "Gửi phản hồi & Ký xác nhận"
- "TỪ CHỐI" → "Từ chối hình thức kỷ luật"
- "CHẤP NHẬN" → "Chấp nhận"
- Empty state employee: "Bạn chưa có hồ sơ kỷ luật nào. Đây là tin tốt!"
- Empty state manager: "Chưa có hồ sơ kỷ luật. Bấm 'Tạo Counseling Log' khi cần ghi nhận vi phạm."

### Bắt Buộc Không Làm

- KHÔNG đổi `name` của input/select/textarea (xem danh sách mục 1.4 trong V1).
- KHÔNG đổi `id` của canvas (`*-pad`) hoặc hidden input (`*_sig_data`).
- KHÔNG đổi `csrf_token`, `enctype="multipart/form-data"`, `method`, `action`.
- KHÔNG đổi template XML ID.
- KHÔNG đổi controller, model, security.
- KHÔNG override CSS global (.btn, .card, .table, .form-control, .badge, .alert, .modal, .o_portal*).
- KHÔNG thêm thư viện JS external.
- KHÔNG xóa comment có sẵn.

### Test

```bash
python odoo-bin -d <db_test> -u M02_P0215 --stop-after-init
```

Browser (desktop 1280px + mobile 375px):
- `/my/disciplines` → zebra striping, dot pulse cho badge "Thông báo", filter input lọc client-side.
- `/my/discipline/create` → sticky progress nav, smooth scroll khi click dot, textarea auto-resize, submit có spinner, beforeunload nếu dirty.
- `/my/discipline/<id>` → stepper 10-step với dot vàng current, action panel nền trắng có icon, reject yêu cầu note + confirm.
- Chrome DevTools → Rendering → Emulate `prefers-reduced-motion: reduce` → animation tắt.

Regression: `/my/invoices` UI không đổi.

---

## 11. Risk Matrix V2

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| JS conflict với JS inline có sẵn (signature pad) | M | H | Vanilla JS, scope query, không touch hidden input/canvas id. Test signature flow trước khi merge |
| SCSS variable shadowing | L | M | Giữ alias V1: `--psm-0215-yellow: var(--psm-0215-yellow-500);` |
| Form progress nav che breadcrumb portal | L | L | Position sticky với `top: 16px`, z-index 10 (thấp hơn modal 1050) |
| Stepper text quá dài tràn mobile | M | M | `overflow-x: auto` + `white-space: nowrap` |
| IntersectionObserver không support IE | L | L | Odoo 19 không support IE; modern browsers OK |
| Auto-resize textarea conflict với min-height CSS | L | L | JS set `height: auto` trước khi đọc `scrollHeight` |
| `beforeunload` annoying user | M | M | Chỉ trigger nếu form thực sự dirty (set flag trên `input` event) |
| Confirm reject double dialog (browser + custom) | L | L | Chỉ dùng 1: `confirm()` native, không tạo modal custom |
| Pulse animation gây mệt mỏi | L | M | Animation chỉ 1.6s loop, opacity nhẹ. Respect `prefers-reduced-motion` |
| List filter ẩn row làm pager sai count | L | L | Filter là client-side, pager vẫn theo server-side; thông báo "Đang lọc trong trang hiện tại" nếu có hit |

---

## 12. Acceptance Criteria

| # | Tiêu chí | Verify |
|---|---|---|
| 1 | Page bg cream nhẹ `#FDFBF4`, không pure white | Mở `/my/disciplines` |
| 2 | Status badge có dot indicator + min-width đồng đều | Inspect `.psm-status` width |
| 3 | Badge "Thông báo" (pending) có pulse animation | Mở record state `notified` |
| 4 | Button hover có lift + shadow | Hover `.psm-btn--primary` |
| 5 | Submit button có spinner khi click | Submit create form |
| 6 | Form create có sticky progress nav 5 dots | Cuộn form |
| 7 | Click dot trên progress → smooth scroll | Click dot 3 |
| 8 | Dot chuyển sang `is-done` khi điền đủ required section | Điền section 1 → blur |
| 9 | Textarea Section I-IV auto-resize | Nhập 10 dòng vào Section I |
| 10 | Detail page có stepper 10 milestone | Mở record |
| 11 | Stepper highlight current state | State `under_review` → "Xem xét" có dot vàng |
| 12 | Action panel có nền trắng + left-border vàng | Mở record state `notified` |
| 13 | Reject button: nếu note rỗng → flash alert | Click reject without note |
| 14 | Reject button: nếu note có → confirm dialog | Click reject with note |
| 15 | beforeunload warn khi form dirty | Nhập field, đóng tab |
| 16 | List filter lọc rows client-side | Gõ keyword vào search |
| 17 | Table có zebra striping | Inspect `tbody tr:nth-child(even)` bg |
| 18 | Banner có gradient vàng + thanh đen trái | Inspect `.psm-banner` |
| 19 | Mobile (375px) cardlist + bottom sticky CTA | DevTools mobile mode |
| 20 | `prefers-reduced-motion: reduce` tắt animation | Chrome emulate → hover button → không lift |
| 21 | `/my/invoices` UI không thay đổi | So sánh before/after |

---

## Files Used For Confirmation (V2)

| File | Vai trò |
|---|---|
| Screenshot 1 (create form) | Phát hiện section index OK nhưng witness select bị duplicate; spacing label↔value chưa thoáng |
| Screenshot 2 (detail page) | Phát hiện action panel accept/reject có nền vàng + button vàng đặt cạnh nhau (gắt); thiếu stepper |
| Screenshot 3 (list page) | Phát hiện badge dính sát date column; không zebra; không có search/filter |
| Screenshot 4 (McDonald's website) | Tham khảo hệ tông màu vàng-đỏ-đen kết hợp white/cream làm đệm; rounded corners lớn; depth qua shadow |
| `addons/M02_P0215/__manifest__.py` | Xác nhận manifest đã có khoá `assets` với 1 SCSS — V2 sẽ thêm JS vào cùng bundle |
| `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` (404 dòng) | Xác nhận baseline V1: tokens, components, mobile cardlist đã có. V2 mở rộng không phá V1 |
| `addons/M02_P0215/views/x_psm_portal_templates.xml` (1094 dòng) | Xác nhận templates đã có wrapper `.o_psm_0215_portal`, class `psm-*`; V2 thêm class/id mới và component mới |
| `addons/M02_P0215/notes/BLUEPRINT_PORTAL_UI_REDESIGN_0215.md` | Tham chiếu V1 baseline — không lặp lại 1.4 (input names) ở V2 |
