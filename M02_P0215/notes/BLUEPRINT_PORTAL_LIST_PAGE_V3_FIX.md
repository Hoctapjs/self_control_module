# Blueprint V3 — Fix UI/UX cho List Page `/my/disciplines`

> **Phạm vi**: Chỉ tập trung sửa **trang danh sách hồ sơ kỷ luật** (`portal_psm_my_disciplines`) dựa trên screenshot thực tế. Không sửa controller, model, security.
> **Loại**: Plan thực thi cho AI Coder (Codex).
> **Ngày**: 2026-05-13
> **Baseline**: V1 + V2 đã apply. File template hiện tại đã có wrapper `.o_psm_0215_portal`, dict `status_labels` + `status_classes`, filter input, `psm-mobile-stack`.

---

## 1. Vấn Đề Phát Hiện Từ Screenshot

### 1.1. Vấn Đề Nghiêm Trọng (Functional / Data)

| # | Vấn đề | Mô tả | Mức độ |
|---|---|---|---|
| **P1** | **Date format MM/DD/YYYY** | Cột "Ngày" hiển thị `05/13/2026` thay vì `13/05/2026` chuẩn Việt Nam → user dễ nhầm. | 🔴 Cao |
| **P2** | **Empty row (hàng 5)** | Hàng thứ 5 trong screenshot: cột Reference, Employee, Date đều trống. Chỉ có cột Vi phạm và Trạng thái. → Record có thể missing `name`, `x_psm_employee_id`, `x_psm_date` nhưng vẫn render. Link click vào page null. | 🔴 Cao |
| **P3** | **Subtype mới là thông tin phân biệt nhưng bị mờ** | Cột "Vi phạm" hiển thị tên category dài (lặp lại 9/11 dòng) + subtype nhỏ muted. User scan bằng subtype ("đi trễ", "vi phạm store") nhưng nó bị visual hierarchy đảo ngược. | 🔴 Cao |
| **P4** | **Sortby chỉ có 1 option "Newest"** | Dropdown sortby ở searchbar chỉ có 1 lựa chọn → vô nghĩa. Cần thêm: theo trạng thái, theo employee, theo cũ nhất. | 🟡 Trung |

### 1.2. Vấn Đề UI (Visual)

| # | Vấn đề | Mô tả | Mức độ |
|---|---|---|---|
| **P5** | **Breadcrumb trùng lặp** | "🏠 / Disciplinary Records" hiện 2 lần: 1 lần ở top, 1 lần trong card. | 🟡 Trung |
| **P6** | **Pager active màu tím** | Nút pager "1" có background tím → KHÔNG thuộc palette McDonald's (vàng/đỏ/đen/trắng). | 🟡 Trung |
| **P7** | **Badge width inconsistent** | "KHỞI TẠO" hẹp, "BAN HÀNH QUYẾT ĐỊNH" rất rộng → cột status co giãn xấu, không thẳng hàng. | 🟡 Trung |
| **P8** | **Status badge progress đều cùng màu vàng** | 7 state khác nhau (`under_review`, `level_determination`, `investigation`, `hearing`, `proposal`, `issued`, `approval`) cùng badge vàng → không phân biệt được cấp độ workflow. | 🟡 Trung |
| **P9** | **Cột Employee co giãn** | "0215 s1" 1 dòng vs "0215 Demo Employee A" wrap 2 dòng → row height nhấp nhô. | 🟡 Trung |
| **P10** | **Header REFERENCE align center, data align left** | Lệch dọc giữa header và body. | 🟡 Trung |
| **P11** | **Cột Reference text màu mặc định** | Link ref code chưa rõ là clickable. Cần style nhấn (vàng/đỏ + underline on hover). | 🟢 Thấp |
| **P12** | **Không có visual cue cho record cần action** | Record state `notified` đáng lẽ phải nổi bật (dot pulse đỏ trong V2) nhưng không thấy trong screenshot (không có record `notified`). Verify khi có data. | 🟢 Thấp |
| **P13** | **Cột Vi phạm chiếm quá nhiều không gian** | Category name dài tới 2 dòng × 9 record → bảng dài không cần thiết. | 🟡 Trung |
| **P14** | **Viền vàng badge "ĐANG HIỆU LỰC" mảnh** | 2px inset border vàng nhìn xa như render lỗi. | 🟢 Thấp |

### 1.3. Vấn Đề UX (Behavior / Information)

| # | Vấn đề | Mô tả | Mức độ |
|---|---|---|---|
| **P15** | **Filter input không có clear button** | User gõ xong muốn reset phải Ctrl+A + Delete. | 🟡 Trung |
| **P16** | **Không có total count** | Không biết tổng bao nhiêu records trong account (ngoài pager số trang). | 🟢 Thấp |
| **P17** | **Filter chỉ trong trang hiện tại** | Filter client-side không cross-page. User filter ở page 1 mà data ở page 2 → không thấy. Cần message hint. | 🟡 Trung |
| **P18** | **Không có quick action trên row** | User phải click reference để xem chi tiết, không có "Xem nhanh" tooltip hoặc action button. | 🟢 Thấp |
| **P19** | **Hover row toàn cell clickable nhưng chỉ link ref mới đi** | Hover row đổi màu nền vàng → user tưởng click bất kỳ chỗ nào cũng đi, thực tế chỉ link ref. | 🟡 Trung |
| **P20** | **Không có grouping theo state** | Tất cả states trộn lẫn → manager khó nhìn ra "có 3 record đang chờ tôi finalize". | 🟢 Thấp (nice-to-have) |

---

## 2. Giải Pháp Theo Từng Vấn Đề

### P1 — Date format Việt Nam

**Cách fix**:
```xml
<!-- TRƯỚC -->
<span t-field="rec.x_psm_date"/>

<!-- SAU — dùng options của t-field -->
<span t-field="rec.x_psm_date" t-options="{'widget': 'date', 'format': 'dd/MM/yyyy'}"/>
```

> Odoo widget `date` với format `dd/MM/yyyy` đảm bảo render chuẩn DD/MM/YYYY, không phụ thuộc lang user.

### P2 — Bảo vệ render khi record thiếu dữ liệu

**Cách fix**: Bọc `t-if` guard, thêm fallback `---` rõ ràng cho mọi cell:

```xml
<t t-foreach="disciplines" t-as="rec">
    <tr t-if="rec.id">
        <td class="text-left psm-cell-ref" data-label="Reference">
            <a t-attf-href="/my/discipline/#{rec.id}" class="psm-cell-ref__link">
                <strong>
                    <t t-esc="rec.name or rec.display_name or ('#' + str(rec.id))"/>
                </strong>
            </a>
        </td>
        <td class="text-left" data-label="Employee">
            <t t-if="rec.x_psm_employee_id">
                <span t-field="rec.x_psm_employee_id.name"/>
            </t>
            <t t-else="">
                <span class="text-muted">---</span>
            </t>
        </td>
        <!-- ... các cell khác đều có fallback ---  -->
    </tr>
</t>
```

> **Lý do**: hiện code có `rec.name or '---'` cho cột Reference nhưng các cột khác dùng `t-field` không có fallback → render trống.

### P3 — Reorder cột "Vi phạm": subtype lên trước, category xuống dưới

**Cách fix**: Hoán đổi visual hierarchy. Subtype (`x_psm_violation_type`) thường là short note → đưa lên dòng đầu, đậm, đen. Category đưa xuống dòng dưới, nhỏ, muted, **truncate nếu quá dài**.

```xml
<td class="text-left psm-cell-violation" data-label="Vi phạm">
    <t t-set="vtype" t-value="rec.x_psm_violation_type and rec.x_psm_violation_type.strip()"/>
    <t t-set="vcat" t-value="rec.x_psm_violation_category_id.name"/>
    <t t-if="vtype">
        <div class="psm-cell-violation__type">
            <t t-esc="vtype"/>
        </div>
    </t>
    <t t-if="vcat">
        <div class="psm-cell-violation__cat" t-att-title="vcat">
            <i class="fa fa-tag" aria-hidden="true"/>
            <span><t t-esc="vcat"/></span>
        </div>
    </t>
    <t t-if="not vtype and not vcat">
        <span class="text-muted">---</span>
    </t>
</td>
```

**SCSS bổ sung**:
```scss
.o_psm_0215_portal .psm-cell-violation { max-width: 32rem; }

.o_psm_0215_portal .psm-cell-violation__type {
    color: var(--psm-0215-text-strong);
    font-size: var(--psm-0215-fs-base);
    font-weight: var(--psm-0215-fw-semibold);
    line-height: 1.35;
    margin-bottom: var(--psm-0215-space-1);
}

.o_psm_0215_portal .psm-cell-violation__cat {
    align-items: center;
    color: var(--psm-0215-text-muted);
    display: inline-flex;
    font-size: var(--psm-0215-fs-sm);
    gap: var(--psm-0215-space-1);
    max-width: 100%;
}

.o_psm_0215_portal .psm-cell-violation__cat span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.o_psm_0215_portal .psm-cell-violation__cat .fa { color: var(--psm-0215-yellow-700); }
```

> **Lý do**: subtype là phân biệt thực sự ("đi trễ" vs "vi phạm store"). Category lặp lại, dùng icon tag + truncate ellipsis + tooltip để vẫn thấy được khi cần.

### P4 — Thêm sortby options

**Cần phối hợp controller** — controller có dict `searchbar_sortings` cần kiểm tra. Nếu chỉ có 1 key thì thêm:

```python
searchbar_sortings = {
    'date_desc': {'label': 'Mới nhất', 'order': 'x_psm_date desc, id desc'},
    'date_asc':  {'label': 'Cũ nhất',  'order': 'x_psm_date asc, id asc'},
    'state':     {'label': 'Theo trạng thái', 'order': 'state, x_psm_date desc'},
    'employee':  {'label': 'Theo nhân viên',  'order': 'x_psm_employee_id, x_psm_date desc'},
}
```

> ⚠️ **Cần xác nhận với user trước** vì task baseline là "không sửa controller". Nếu chỉ giữ UI scope → skip P4.

### P5 — Bỏ breadcrumb trùng lặp

**Cách fix**: Trong template có:
```xml
<t t-call="portal.portal_searchbar">
    <t t-set="title">Disciplinary Records</t>
    ...
</t>
```
Portal layout đã render breadcrumb top → khả năng `portal_searchbar` cũng render thêm "title" trông giống breadcrumb. Kiểm tra hai khả năng:

1. **Khả năng A**: `portal.portal_searchbar` render `<title>` với icon home → trùng. Giải pháp: bỏ `<t t-set="title">` hoặc đổi title thành rỗng.
2. **Khả năng B**: Layout có `portal.portal_breadcrumbs` render top, `portal_searchbar` render in-card → cả 2 đều cần thiết, nhưng title thứ 2 chỉ là tên section. Giải pháp: giữ, nhưng đảm bảo title KHÔNG có icon home (icon home đến từ breadcrumb top).

→ **Hành động cho codex**: inspect screenshot cho thấy 2 dòng giống hệt `🏠 / Disciplinary Records`. Khả năng A đúng. Cách an toàn: kiểm tra render thực tế, nếu thấy duplicate icon home thì wrap title bằng class custom không icon, hoặc đặt `breadcrumbs_searchbar = False`.

### P6 — Pager màu tím → vàng McDonald's

Pager dùng class Odoo mặc định `.o_portal_pager`. Bootstrap pagination active dùng `--bs-pagination-active-bg`.

**Cách fix** — override scoped:
```scss
.o_psm_0215_portal .o_portal_pager .page-item.active .page-link {
    background-color: var(--psm-0215-yellow-500);
    border-color: var(--psm-0215-yellow-600);
    color: var(--psm-0215-text-strong);
    font-weight: var(--psm-0215-fw-bold);
}

.o_psm_0215_portal .o_portal_pager .page-link {
    border-radius: var(--psm-0215-radius-pill);
    color: var(--psm-0215-text);
    margin: 0 var(--psm-0215-space-1);
    min-width: 2.25rem;
    text-align: center;
}

.o_psm_0215_portal .o_portal_pager .page-link:hover {
    background-color: var(--psm-0215-yellow-100);
    color: var(--psm-0215-text-strong);
}

.o_psm_0215_portal .o_portal_pager .page-item.disabled .page-link {
    color: var(--psm-0215-text-muted);
    opacity: 0.5;
}

/* Border-radius cho nút prev/next pill */
.o_psm_0215_portal .o_portal_pager .page-item:first-child .page-link,
.o_psm_0215_portal .o_portal_pager .page-item:last-child .page-link {
    border-radius: var(--psm-0215-radius-pill);
}
```

> Đây là override CSS có scope `.o_psm_0215_portal` → không leak portal khác.

### P7 — Badge width consistent

Hiện đã có `min-width: 6rem` ở V2 plan, nhưng badge "BAN HÀNH QUYẾT ĐỊNH" dài 22 ký tự — vượt min-width.

**Cách fix**: dùng cách tiếp cận khác — **không cố định width**, mà:
- Đảm bảo cột status có `width` cố định.
- Badge wrap nếu cần, không stretch column.

```scss
.o_psm_0215_portal .psm-table th.psm-col-status,
.o_psm_0215_portal .psm-table td.psm-cell-status {
    text-align: right;
    width: 11rem; /* hoặc 12rem cho VN text dài */
    white-space: normal;
}

.o_psm_0215_portal .psm-status {
    /* Bỏ min-width cứng — để badge tự nhiên */
    display: inline-flex;
    max-width: 100%;
    white-space: nowrap;
    /* Nếu chữ quá dài (> max-width), wrap 2 dòng nhỏ */
}

/* Nếu cần wrap, dùng modifier */
.o_psm_0215_portal .psm-status--multiline { white-space: normal; line-height: 1.2; }
```

**Alternative**: shorten labels cho trạng thái dài:
```python
status_labels_short = {
    'level_determination': 'Xác định cấp',
    'issued': 'Ban hành QĐ',
    'investigation': 'Xác minh',
    # ... giữ label dài cho detail page, short cho list
}
```

Truyền cả 2 dict vào template, list dùng `status_labels_short`.

### P8 — Phân biệt progress states (7 state cùng vàng)

**Cách fix**: chia 3 mức trong nhóm progress:

```python
# Phân tầng
status_classes = {
    'draft': 'psm-status-neutral',
    'under_review': 'psm-status-progress',           # Bước đầu — vàng
    'level_determination': 'psm-status-progress',    # vàng
    'investigation': 'psm-status-progress-deep',     # Vàng đậm — đang điều tra
    'hearing': 'psm-status-progress-deep',           # Vàng đậm — đang họp
    'proposal': 'psm-status-action',                 # Cần action — viền đỏ
    'issued': 'psm-status-action',                   # Cần action — viền đỏ
    'approval': 'psm-status-progress-deep',          # Vàng đậm
    'notified': 'psm-status-pending',                # Đỏ pulse
    'active': 'psm-status-success',                  # Đen
    'expired': 'psm-status-neutral',
    'cancel': 'psm-status-neutral',
}
```

SCSS:
```scss
.o_psm_0215_portal .psm-status-progress {
    background: var(--psm-0215-yellow-100);
    color: var(--psm-0215-yellow-700);
}

.o_psm_0215_portal .psm-status-progress-deep {
    background: var(--psm-0215-yellow-500);
    color: var(--psm-0215-text-strong);
}

.o_psm_0215_portal .psm-status-action {
    background: var(--psm-0215-white);
    border: 1.5px solid var(--psm-0215-red-500);
    color: var(--psm-0215-red-700);
}
```

> User nhìn 1 lượt phân biệt được: "đang chờ ai" (vàng nhạt) vs "đang xử lý sâu" (vàng đậm) vs "cần action ngay" (viền đỏ).

### P9 — Cột Employee fixed width

```scss
.o_psm_0215_portal .psm-table th.psm-col-employee,
.o_psm_0215_portal .psm-table td.psm-cell-employee {
    max-width: 10rem;
    width: 10rem;
}

.o_psm_0215_portal .psm-cell-employee {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Hiển thị avatar nhỏ nếu có */
.o_psm_0215_portal .psm-cell-employee__avatar {
    background: var(--psm-0215-yellow-100);
    border-radius: 50%;
    color: var(--psm-0215-text-strong);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--psm-0215-fs-xs);
    font-weight: var(--psm-0215-fw-bold);
    height: 1.75rem;
    margin-right: var(--psm-0215-space-2);
    width: 1.75rem;
}
```

**QWeb** (optional avatar initials):
```xml
<td class="psm-cell-employee" data-label="Employee">
    <t t-if="rec.x_psm_employee_id">
        <span class="psm-cell-employee__avatar" t-att-title="rec.x_psm_employee_id.name">
            <t t-esc="(rec.x_psm_employee_id.name or '?')[0].upper()"/>
        </span>
        <span t-att-title="rec.x_psm_employee_id.name"><t t-esc="rec.x_psm_employee_id.name"/></span>
    </t>
    <t t-else=""><span class="text-muted">---</span></t>
</td>
```

### P10 — Header align consistency

```xml
<thead>
    <tr>
        <th class="text-left">Mã hồ sơ</th>
        <th class="text-left psm-col-employee">Nhân viên</th>
        <th class="text-left">Vi phạm</th>
        <th class="text-left psm-col-date">Ngày</th>
        <th class="text-end psm-col-status">Trạng thái</th>
    </tr>
</thead>
```

Tất cả header và cell cùng align. Đề xuất:
- Reference / Employee / Vi phạm: **left**
- Ngày: **left** (đọc tự nhiên) hoặc **center**
- Trạng thái: **right** (vì badge ở cuối hàng)

> Cũng đề xuất **đổi tên cột** sang tiếng Việt: "Mã hồ sơ" thay "Reference", "Nhân viên" thay "Employee".

### P11 — Reference link style

```scss
.o_psm_0215_portal .psm-cell-ref__link {
    color: var(--psm-0215-red-600);
    font-family: ui-monospace, "SF Mono", Consolas, Monaco, monospace;
    font-size: var(--psm-0215-fs-sm);
    font-weight: var(--psm-0215-fw-bold);
    letter-spacing: 0.3px;
    text-decoration: none;
    transition: color 0.15s ease;
}

.o_psm_0215_portal .psm-cell-ref__link:hover,
.o_psm_0215_portal .psm-cell-ref__link:focus {
    color: var(--psm-0215-red-700);
    text-decoration: underline;
    text-underline-offset: 3px;
}
```

> Monospace + đỏ McDonald's → mã hồ sơ rõ là clickable.

### P12 — Visual cue cho record cần action

**Cách fix**: thêm class `psm-row--needs-action` cho row có state cần user attention.

```xml
<t t-set="needs_action" t-value="rec.state in ('notified', 'issued', 'proposal')"/>
<tr t-att-class="'psm-row--needs-action' if needs_action else ''" t-att-data-state="rec.state">
```

SCSS:
```scss
.o_psm_0215_portal .psm-table tbody tr.psm-row--needs-action {
    box-shadow: inset 4px 0 0 var(--psm-0215-red-500);
}

.o_psm_0215_portal .psm-table tbody tr.psm-row--needs-action:hover {
    background: var(--psm-0215-red-50);
}
```

> Thanh đỏ trái 4px báo "có việc cần làm".

### P13 — Cột Vi phạm gọn lại

Đã giải quyết qua P3 (truncate category + ưu tiên subtype).

### P14 — Badge "ĐANG HIỆU LỰC" border đậm hơn

```scss
.o_psm_0215_portal .psm-status-success {
    background: var(--psm-0215-text-strong);
    border: none; /* bỏ inset 2px */
    box-shadow:
        inset 0 0 0 2px var(--psm-0215-yellow-500),
        0 1px 2px rgba(0, 0, 0, 0.15);
    color: var(--psm-0215-white);
    padding-left: var(--psm-0215-space-4);
    padding-right: var(--psm-0215-space-4);
}

/* Thay vì viền vàng, dùng icon check + chữ "Đang hiệu lực" */
.o_psm_0215_portal .psm-status-success::before {
    background: var(--psm-0215-yellow-500);
    /* mask icon check */
    content: "\f00c"; /* fa-check */
    font-family: "FontAwesome";
    color: var(--psm-0215-yellow-500);
    background: transparent;
    opacity: 1;
    flex: 0 0 auto;
    height: auto;
    width: auto;
}
```

> Đổi inset border → box-shadow + icon check vàng. Nhìn rõ ràng hơn ở mọi distance.

### P15 — Filter input có clear button

```xml
<div class="psm-list-filter-wrap">
    <i class="fa fa-search psm-list-filter__icon" aria-hidden="true"/>
    <input type="search" id="psm_discipline_list_filter" class="psm-list-filter"
           placeholder="Lọc trong trang hiện tại..."
           autocomplete="off"
           data-psm-filter-target=".psm-table tbody tr"/>
    <button type="button" class="psm-list-filter__clear" aria-label="Xóa lọc" hidden="hidden">
        <i class="fa fa-times" aria-hidden="true"/>
    </button>
    <span class="psm-list-filter__count" aria-live="polite"></span>
</div>
```

JS thêm vào `initListFilter`:
```js
function initListFilter(root) {
    const input = root.querySelector('.psm-list-filter');
    if (!input) return;
    const wrap = input.closest('.psm-list-filter-wrap');
    const clearBtn = wrap && wrap.querySelector('.psm-list-filter__clear');
    const countEl = wrap && wrap.querySelector('.psm-list-filter__count');
    const rows = root.querySelectorAll('.psm-table tbody tr');

    function apply() {
        const q = input.value.trim().toLowerCase();
        let visible = 0;
        rows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            const match = !q || text.includes(q);
            row.style.display = match ? '' : 'none';
            if (match) visible++;
        });
        if (clearBtn) clearBtn.hidden = !q;
        if (countEl) {
            countEl.textContent = q
                ? `Hiển thị ${visible}/${rows.length} trong trang này`
                : '';
        }
    }

    input.addEventListener('input', apply);
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            input.value = '';
            apply();
            input.focus();
        });
    }
}
```

SCSS:
```scss
.o_psm_0215_portal .psm-list-filter-wrap {
    align-items: center;
    background: var(--psm-0215-white);
    border: 1px solid var(--psm-0215-border);
    border-radius: var(--psm-0215-radius-pill);
    display: flex;
    gap: var(--psm-0215-space-2);
    padding: var(--psm-0215-space-2) var(--psm-0215-space-4);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.o_psm_0215_portal .psm-list-filter-wrap:focus-within {
    border-color: var(--psm-0215-yellow-500);
    box-shadow: 0 0 0 3px rgba(255, 199, 44, 0.25);
}

.o_psm_0215_portal .psm-list-filter__icon { color: var(--psm-0215-text-muted); }

.o_psm_0215_portal .psm-list-filter {
    background: transparent;
    border: 0;
    color: var(--psm-0215-text-strong);
    flex: 1 1 auto;
    font-size: var(--psm-0215-fs-base);
    outline: none;
    padding: 0;
}

.o_psm_0215_portal .psm-list-filter__clear {
    background: transparent;
    border: 0;
    border-radius: 50%;
    color: var(--psm-0215-text-muted);
    cursor: pointer;
    height: 1.5rem;
    padding: 0;
    width: 1.5rem;
}

.o_psm_0215_portal .psm-list-filter__clear:hover {
    background: var(--psm-0215-gray-100);
    color: var(--psm-0215-text-strong);
}

.o_psm_0215_portal .psm-list-filter__count {
    color: var(--psm-0215-text-muted);
    font-size: var(--psm-0215-fs-sm);
    margin-left: var(--psm-0215-space-2);
}
```

### P16 — Hiển thị total count

Trên header list:
```xml
<div class="psm-list-summary">
    <span class="psm-list-summary__label">Tổng số hồ sơ:</span>
    <span class="psm-list-summary__count">
        <t t-esc="pager.get('counter') or len(disciplines)"/>
    </span>
</div>
```

Hoặc nếu controller có `disciplines_count`:
```xml
<span class="psm-list-summary__count"><t t-esc="disciplines_count or len(disciplines)"/></span>
```

> Nếu không có biến count → fallback `len(disciplines)` chỉ tính trang hiện tại. Lý tưởng controller truyền `total_count`.

### P17 — Hint cho filter cross-page

Khi user filter ở page 2 mà có data ở page 1, không tìm thấy → cần message:

```js
if (countEl) {
    if (q && visible === 0) {
        countEl.innerHTML = `Không có hồ sơ khớp trong trang này. <a href="?search=${encodeURIComponent(q)}">Tìm trong tất cả</a>`;
    } else if (q) {
        countEl.textContent = `Hiển thị ${visible}/${rows.length} trong trang này`;
    } else {
        countEl.textContent = '';
    }
}
```

> ⚠️ **Lưu ý**: link "Tìm trong tất cả" cần controller hỗ trợ `?search=` query param. Nếu controller hiện không hỗ trợ → bỏ link, chỉ giữ message text.

### P18 — (Skip cho V3) Quick action

Skip để giữ scope nhỏ. Sau này có thể thêm dropdown menu trên row.

### P19 — Toàn row clickable

**Cách fix**: nếu user hover row đổi màu → row nên thực sự clickable.

```js
function initRowClickable(root) {
    const rows = root.querySelectorAll('.psm-table tbody tr[data-href]');
    rows.forEach((row) => {
        row.addEventListener('click', (e) => {
            // Bỏ qua nếu click vào link/button nested
            if (e.target.closest('a, button')) return;
            const href = row.getAttribute('data-href');
            if (href) window.location.href = href;
        });
        // Keyboard accessibility
        row.setAttribute('tabindex', '0');
        row.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const href = row.getAttribute('data-href');
                if (href) window.location.href = href;
            }
        });
    });
}
```

QWeb:
```xml
<tr t-att-data-href="'/my/discipline/' + str(rec.id)" t-att-data-state="rec.state" class="...">
```

SCSS:
```scss
.o_psm_0215_portal .psm-table tbody tr[data-href] {
    cursor: pointer;
}

.o_psm_0215_portal .psm-table tbody tr[data-href]:focus-visible {
    outline: 2px solid var(--psm-0215-yellow-500);
    outline-offset: -2px;
}
```

> Click bất kỳ chỗ nào trên row → đi đến detail. Click trực tiếp vào link ref vẫn dùng anchor (do `e.target.closest('a')` skip).

### P20 — (Skip cho V3) Grouping theo state

Nice-to-have, skip để giữ scope. Có thể thêm filter chips ở header sau (`Tất cả | Cần xử lý | Đang chạy | Đã xong`).

---

## 3. Tóm Tắt Files Cần Sửa

| File | Loại sửa |
|---|---|
| `addons/M02_P0215/views/x_psm_portal_templates.xml` | Template `portal_psm_my_disciplines` — refactor cell rendering, thêm `data-href` cho row, clear button, count, fallback `---` |
| `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` | Thêm: cột widths, badge variants mới, ref link style, pager override, filter wrap, row needs-action, employee avatar |
| `addons/M02_P0215/static/src/js/portal_psm_0215.js` | Mở rộng `initListFilter` (clear + count), thêm `initRowClickable` |
| `addons/M02_P0215/controllers/portal.py` | **CHỈ NẾU user approve P4** — thêm sortby options + truyền `total_count` cho P16 |

---

## 4. Order Thực Thi Cho Codex

1. **Bước 1 — Đọc files**:
   - `views/x_psm_portal_templates.xml` template `portal_psm_my_disciplines` (line 43-161 hiện tại)
   - `static/src/scss/portal_psm_0215.scss`
   - `static/src/js/portal_psm_0215.js`
   - `controllers/portal.py` route `portal_psm_my_disciplines`

2. **Bước 2 — Sửa template** (chỉ block `<template id="portal_psm_my_disciplines">`):
   - Đổi date format thành `dd/MM/yyyy` (P1).
   - Bọc `t-if="rec.id"` cho `<tr>` (P2).
   - Refactor cell Vi phạm — subtype lên đầu, category icon + truncate (P3).
   - Bỏ duplicate breadcrumb / title (P5).
   - Đổi tên cột tiếng Việt: "Mã hồ sơ" / "Nhân viên" / "Vi phạm" / "Ngày" / "Trạng thái" (P10).
   - Header + body align consistent — đổi `text-left` / `text-right` cho khớp (P10).
   - Mã ref dùng class `psm-cell-ref__link` thay `<strong>` plain (P11).
   - Cột status: thêm `psm-col-status`, badge dùng nhãn rút gọn cho list (P7).
   - Phân class status mới: `psm-status-progress-deep`, `psm-status-action` (P8).
   - Cột employee width fixed + avatar initials (P9).
   - `<tr>` có `data-href`, `tabindex`, class `psm-row--needs-action` khi state ∈ {notified, issued, proposal} (P12, P19).
   - Filter wrap + clear button + count span (P15, P17).
   - Total count summary (P16) — nếu không có data từ controller dùng `len(disciplines)`.

3. **Bước 3 — Mở rộng SCSS**:
   - Thêm rules cho `.psm-col-*`, `.psm-cell-*`, `.psm-cell-violation__*`, `.psm-cell-employee__avatar`, `.psm-cell-ref__link`, `.psm-row--needs-action`.
   - Thêm pager override `.o_portal_pager` (P6).
   - Thêm `.psm-status-progress-deep`, `.psm-status-action`.
   - Refactor `.psm-status-success` (P14): thay inset border bằng box-shadow + icon check.
   - Refactor `.psm-list-filter-wrap` (P15).

4. **Bước 4 — Mở rộng JS**:
   - Mở rộng `initListFilter`: clear button + count display.
   - Thêm `initRowClickable`.
   - Register vào boot function.

5. **Bước 5 — (Tùy chọn) Sửa controller**:
   - Hỏi user trước.
   - Nếu approve P4: thêm sortby options.
   - Nếu approve P16 full: tính `total_count` qua `search_count`.

6. **Bước 6 — Test**:
   - Upgrade module.
   - Mở `/my/disciplines` desktop 1280px.
   - Verify date `13/05/2026` format.
   - Hover row → cursor pointer + bg vàng nhẹ. Click → đi detail.
   - Gõ filter → count update. Click X → clear.
   - Pager active màu vàng, không tím.
   - Badge "BAN HÀNH QĐ" (rút gọn) không tràn cột.
   - Resize 375px mobile → cardlist OK.
   - Tab keyboard navigation: row có focus ring.
   - Mở `/my/invoices` → UI không đổi.

---

## 5. Constraints (Như V1+V2)

- KHÔNG đổi route `/my/disciplines`, `/my/disciplines/page/<int:page>`.
- KHÔNG đổi template id `portal_psm_my_disciplines`.
- KHÔNG đổi tên biến QWeb đang dùng (`disciplines`, `pager`, `is_manager`, `status_labels`, `status_classes`).
- KHÔNG đổi name input filter (đã có ID `psm_discipline_list_filter`, giữ nguyên).
- KHÔNG override CSS global (.btn, .card, .table, .badge, .alert, .o_portal_pager**\***).
  > Exception cho P6: override `.o_portal_pager` được scope dưới `.o_psm_0215_portal` → an toàn.
- KHÔNG thêm dependency mới.
- KHÔNG xóa comment có sẵn.

---

## 6. Acceptance Criteria (Verify Sau Khi Code)

| # | Tiêu chí | Verify |
|---|---|---|
| 1 | Date hiển thị `13/05/2026` (DD/MM/YYYY) | Compare với screenshot |
| 2 | Row có record empty → render với `---` thay vì trống | Tạo test record không có employee, xem render |
| 3 | Cột Vi phạm: subtype trên to/đậm, category dưới nhỏ truncate | Inspect HTML structure |
| 4 | Breadcrumb không duplicate | Screenshot mới có 1 dòng "🏠 / Disciplinary Records" |
| 5 | Pager active màu vàng `#FFC72C` | Inspect CSS computed value |
| 6 | Badge "Ban hành QĐ" (rút gọn) không tràn cột | Cột status width 11rem |
| 7 | 3 cấp badge trong nhóm progress phân biệt được | State `notified` đỏ, state `proposal` viền đỏ, state `under_review` vàng nhạt |
| 8 | Cột Employee fixed 10rem, không wrap | Hover tên dài → tooltip |
| 9 | Header và data align consistent | Visual inspect |
| 10 | Click anywhere on row → đi detail | Click cột Trạng thái → /my/discipline/<id> |
| 11 | Tab keyboard → row có focus ring vàng | Tab qua list |
| 12 | Row state ∈ {notified, issued, proposal} có thanh đỏ trái 4px | Inspect computed style |
| 13 | Filter clear button X hiện khi có text, click → reset | Test interaction |
| 14 | Filter count hint "Hiển thị X/Y" | Test interaction |
| 15 | Total count summary trên header | Compare số với pager |
| 16 | Ref code monospace + đỏ + hover underline | Inspect link |
| 17 | Badge "Đang hiệu lực" có icon check + box-shadow vàng | Visual inspect |
| 18 | Mobile 375px: cardlist render OK, không broken | DevTools mobile |
| 19 | Regression `/my/invoices` không đổi UI | Compare before/after |
| 20 | `prefers-reduced-motion` tắt transition row click | Chrome emulate |

---

## 7. Prompt Cho Codex (Ngắn Gọn, Copy-Paste)

---

**Bạn là Codex. Task: fix UI/UX cho list page `/my/disciplines` của module `addons/M02_P0215` theo blueprint V3. Baseline V1+V2 đã apply.**

### Files Đọc

- `addons/M02_P0215/notes/BLUEPRINT_PORTAL_LIST_PAGE_V3_FIX.md` (file này)
- `addons/M02_P0215/views/x_psm_portal_templates.xml` (chỉ template `portal_psm_my_disciplines`, line 43-161)
- `addons/M02_P0215/static/src/scss/portal_psm_0215.scss`
- `addons/M02_P0215/static/src/js/portal_psm_0215.js`
- `addons/M02_P0215/controllers/portal.py` (chỉ đọc method `portal_psm_my_disciplines`, KHÔNG sửa trừ khi user approve)

### 20 Điểm Sửa (P1-P20)

Xem mục 1-2 trong blueprint. Tóm:
- **P1**: Date `dd/MM/yyyy`.
- **P2**: Fallback `---` cho mọi cell rỗng.
- **P3**: Subtype lên đầu, category icon + truncate.
- **P5**: Bỏ breadcrumb trùng lặp.
- **P6**: Pager active vàng (override scoped).
- **P7**: Cột status fixed 11rem.
- **P8**: 3 cấp badge progress (`-progress`, `-progress-deep`, `-action`).
- **P9**: Cột employee 10rem + avatar initials.
- **P10**: Header + body align consistent, tên cột tiếng Việt.
- **P11**: Ref code monospace đỏ.
- **P12**: Row có thanh đỏ trái 4px cho state notified/issued/proposal.
- **P14**: Badge success — box-shadow thay inset border.
- **P15**: Filter clear button + count.
- **P16**: Total count summary.
- **P17**: Filter cross-page hint.
- **P19**: Row clickable toàn bộ + keyboard navigation.

### Constraints

- KHÔNG đổi route, template id, controller (trừ approve P4/P16).
- KHÔNG override CSS global (override `.o_portal_pager` scope `.o_psm_0215_portal`).
- KHÔNG đổi name input filter `psm_discipline_list_filter`.
- KHÔNG xóa comment.

### Test

```bash
python odoo-bin -d <db> -u M02_P0215 --stop-after-init
```

Browser desktop 1280px + mobile 375px:
- Date `13/05/2026`, badge variants phân biệt, pager vàng, click row đi detail, filter clear + count, ref code đỏ monospace.

Regression `/my/invoices`.

---

## Files Used For Confirmation

| File | Vai trò |
|---|---|
| Screenshot list page `/my/disciplines` (1920x2043) | Phát hiện 20 vấn đề UI/UX cụ thể |
| `addons/M02_P0215/views/x_psm_portal_templates.xml` line 43-161 | Xác nhận template hiện tại — dict status_labels/classes, mobile-stack, filter input đã có |
| `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` | Xác nhận tokens V1+V2, components base sẵn |
| `addons/M02_P0215/__manifest__.py` | Xác nhận assets có SCSS, sẽ thêm JS |
